# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from RavensObject import RavensObject
from PIL import Image
import numpy
import itertools
import copy

# _PLACEHOLDER_DELETED_PREFIX = 'PLACEHOLDER_DELETED_'
_PLACEHOLDER_DELETED_PREFIX = 'DEL'
_PLACEHOLDER_NEW_PREFIX = 'NEW'

_DELETED = 'DELETED'
_REFLECTION = 'REFLECTION'
_INSIDE = 'INSIDE'
_ABOVE = 'ABOVE'


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.align_reflections_map = {
          'x': [
            ['left', 'right'],
            ['top-left', 'top-right'],
            ['bottom-left', 'bottom-right'],
          ],
          'y': [
            ['top', 'bottom'],
            ['top-left', 'bottom-left'],
            ['top-right', 'bottom-right']
          ]
        }

        self.angle_reflections_map = {
          'x': [],
          'y': [
            ['45', '135'],
            ['315', '225'],
            ['270', '0']
          ]
        }

        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):

        print('Solving ' + problem.name)
        self.candidate_answers = []

        if ((problem.name.startswith('Basic Problem C')) or (problem.name.startswith('Challenge Problem C'))):
            return -1

        self.__init_problem_2x2(problem, 'A', 'B')

        # GENERATE: generate all possible figure object-to-object mapping
        self.possible_mappings = self.generate_mappings(self.figures['A'], self.figures['B'])

        # Calculate transformation
        self.possible_transformations = self.get_transformations(
            self.possible_mappings, self.figures['A'], self.figures['B'])

        # Keep Track of the lowest transformation in case there is more than one candidate answer
        self.best_transformation = self.__find_best_transformation(self.possible_transformations)

        applied_transformations = self.__apply_transformation(self.best_transformation, self.figures['C'])

        # For each of the applied transformation, remove the ones don't match any answers
        for applied_transformation in applied_transformations:
            for possible_answer in self.answer_list:
                if self.compare_figures(applied_transformation, possible_answer):
                    self.__add_candidate_answer(possible_answer)

        abList = copy.deepcopy(self.candidate_answers)
        # print(abList)

        self.__init_problem_2x2(problem, 'A', 'C')

        # GENERATE: generate all possible figure object-to-object mapping
        self.possible_mappings = self.generate_mappings(self.figures['A'], self.figures['C'])

        # Calculate transformation
        self.possible_transformations = self.get_transformations(
            self.possible_mappings, self.figures['A'], self.figures['C'])

        # Keep Track of the lowest transformation in case there is more than one candidate answer
        self.best_transformation = self.__find_best_transformation(self.possible_transformations)

        applied_transformations = self.__apply_transformation(self.best_transformation, self.figures['B'])

        # For each of the applied transformation, remove the ones don't match any answers
        for applied_transformation in applied_transformations:
            for possible_answer in self.answer_list:
                if self.compare_figures(applied_transformation, possible_answer):
                    self.__add_candidate_answer(possible_answer)

        acList = copy.deepcopy(self.candidate_answers)
        # print(acList)

        answers_by_score = sorted(abList + acList, key=lambda k: k['score'], reverse=True)

        print(answers_by_score)


        # Make a guess or skip
        answer = 2
        if len(answers_by_score) > 0:
            answer = int(answers_by_score[0]['figure'].name)
        elif len(self.answer_list) == 1:
            answer = int(self.answer_list[0].name)

        print(answer)
        return answer
        # return -1

    def __add_candidate_answer(self, figure):
        answer = { 'score': 1, 'figure': figure }

        # if the answer is already a candidate, just increment its score
        for candidate_answer in self.candidate_answers:
            if candidate_answer['figure'].name == figure.name:
                candidate_answer['score'] += 1
                return

        self.candidate_answers.append(answer)

    def compare_figures(self, fig_1, fig_2):
        if not len(fig_1.objects) == len(fig_2.objects):
            return False

        objs_equal_count = 0
        for obj_1 in fig_1.objects.items():
            for obj_2 in fig_2.objects.items():
                if self.compare_objects(obj_1[1], obj_2[1]):
                    objs_equal_count += 1

        return objs_equal_count == len(fig_1.objects)

    # def filterFiguresBasedDiff(self, expected_diff, target_figure, figures):
    #     filtered_figures = []
    #     # Remove answers that are clearly wrong beause they don't have the expected number of objects
    #     for figure in figures:
    #         figure_diff = len(target_figure.objects) - len(figure.objects)
    #         if expected_diff == figure_diff:
    #             filtered_figures.append(figure)
    #
    #     return filtered_figures

    def compare_objects(self, obj_1, obj_2):
        if len(obj_1.attributes) != len(obj_2.attributes):
            return False

        identical_count = 0
        try:
            for attr in obj_1.attributes:
                if obj_1.attributes[attr] == obj_2.attributes[attr]:
                    identical_count += 1
                elif attr in ['inside', 'above']:
                    identical_count += 1
        except:
            print "Attribute not found in obj_2, so not identical"

        return identical_count == len(obj_1.attributes)

    def __init_problem_2x2(self, problem, from_name, to_name):
        """Initialization for a 2x2 problem

        Initialize figure_list, candidate_list, answer_list and figures

        Args:
            problem: the problem passed from the Solve method
        """
        self.figure_list = ['A', 'B', 'C']
        self.candidate_list = ['1', '2', '3', '4', '5', '6']

        self.figures = {}
        self.figures['A'] = copy.deepcopy(problem.figures['A'])
        self.figures['B'] = copy.deepcopy(problem.figures['B'])
        self.figures['C'] = copy.deepcopy(problem.figures['C'])

        # Initialization
        self.answer_list = []
        for key in self.candidate_list:
            self.answer_list.append(problem.figures[key])

        # remove answers that don't have same deletions/insertions
        self.ab_diff = len(self.figures[from_name].objects) - len(self.figures[to_name].objects)
        if self.ab_diff > 0:
            # A has more objects so pad B with special "DEL" nodes
            for i in range(abs(self.ab_diff)):
                self.figures[to_name].objects[_PLACEHOLDER_DELETED_PREFIX + str(i)] = RavensObject(_PLACEHOLDER_DELETED_PREFIX)

        elif self.ab_diff < 0:
            # B has more objects so pad A with special "INS" nodes
            for i in range(abs(self.ab_diff)):
                self.figures[from_name].objects[_PLACEHOLDER_NEW_PREFIX + str(i)] = RavensObject(_PLACEHOLDER_NEW_PREFIX)

        if to_name == 'B':
            self.answer_list = list(
                filter(lambda answer:
                    (len(self.figures['C'].objects) - len(answer.objects)) == self.ab_diff,
                    self.answer_list))
        elif to_name == 'C':
            self.answer_list = list(
                filter(lambda answer:
                    (len(self.figures['B'].objects) - len(answer.objects)) == self.ab_diff,
                    self.answer_list))

    def generate_mappings(self, figure_from, figure_to):
        """Generate possible mappings

        Generate a list of mappings from objects of figure_from to figure_to

        Args:
            figure_from: the figure mapping from
            figure_to: the figure mapping to

        Returns:
            possible_mappings: [ [ <object, object> ], [ <object, object> ] ]
        """
        # diff = len(figure_from.objects) - len(figure_to.objects)
        # for i in range(abs(diff)):
        #     if diff > 0:
        #         figure_from.objects[_PLACEHOLDER_DELETED_PREFIX + str(i)] = RavensObject(_PLACEHOLDER_DELETED_PREFIX + 'OBJ')
        #     elif diff < 0:
        #         figure_to.objects[_PLACEHOLDER_NEW_PREFIX + str(i)] = RavensObject(_PLACEHOLDER_NEW_PREFIX + 'OBJ')

        possible_mappings = [zip(mapping, figure_to.objects) for mapping in itertools.permutations(figure_from.objects, len(figure_to.objects))]

        return possible_mappings

    def __init_transformation(self, mapping):
        return {
            'mapping': mapping,
            'mutations': []
        }

    def __init_mutation(self, from_obj, to_obj, is_placeholder=False):
        mutation = {
            'type': 'placeholder' if is_placeholder == True else 'normal',
            'from': from_obj,
            'to': to_obj,
            'attribute_changes': []
        }

        if not is_placeholder:
            # compare attribute changes

            # obj: exists => deleted
            if to_obj.name.startswith(_PLACEHOLDER_DELETED_PREFIX):
                mutation['attribute_changes'].append(_DELETED)
                return mutation

            attribute_found = False
            from_shape = ''
            from_fill = ''
            from_size = ''
            to_shape = ''
            to_fill = ''
            to_size = ''
            for to_attr in to_obj.attributes.items():
                # looping over attributes found in to_obj
                if to_attr[0] == 'shape':
                    to_shape = to_attr[1]

                if to_attr[0] == 'fill':
                    to_fill = to_attr[1]

                if to_attr[0] == 'size':
                    to_size = to_attr[1]

                for from_attr in from_obj.attributes.items():
                    # looping over attributes found in from_obj
                    if from_attr[0] == 'shape':
                        from_shape = from_attr[1]

                    if from_attr[0] == 'fill':
                        from_fill = from_attr[1]

                    if from_attr[0] == 'size':
                        from_size = from_attr[1]

                    if (to_attr == from_attr):
                        # attrbute and its value are the same
                        attribute_found = True
                    elif to_attr[0] == from_attr[0]:
                        # attribute are the same, but values are different

                        # case 'inside' and 'above'
                        if to_attr[0] == 'inside' or to_attr[0] == 'above':
                            attribute_found = True
                        # case 'alignment' => check if there's a reflection
                        elif from_attr[0] == 'alignment':
                            attribute_found = True
                            result = self.get_alignment_reflection_axis(from_attr[1], to_attr[1])
                            if result:
                                mutation['attribute_changes'].append((_REFLECTION, result))
                        # case 'angle' => check if there's a reflection
                        elif from_attr[0] == 'angle':
                            attribute_found = True
                            result = self.get_angle_reflection_axis(from_attr[1], to_attr[1])
                            if result:
                                mutation['attribute_changes'].append((_REFLECTION, result))

                if not attribute_found:
                    mutation['attribute_changes'].append(to_attr)

                attribute_found = False

            if (from_shape == to_shape):
                if from_fill != to_fill:
                    mutation['attribute_changes'].append(['fill', to_fill])
                if from_size != to_size:
                    mutation['attribute_changes'].append(['size', to_size])

        return mutation

    def get_transformations(self, mappings, figure_from, figure_to):
        """ Get Transformations

        Create a list of possible transformation based on each mapping

        """
        transformations = []

        for mapping in mappings:
            # for each possible mapping
            transformation = self.__init_transformation(mapping)

            # For each
            for obj_link in mapping:
                # get names
                from_name = obj_link[0]
                to_name = obj_link[1]

                # retrieve the real objects
                from_obj = figure_from.objects[from_name]
                to_obj = figure_to.objects[to_name]
                mutation = self.__init_mutation(from_obj, to_obj)

                transformation['mutations'].append(mutation)

            transformations.append(transformation)

        return transformations

    def __apply_transformation(self, transformation, figure):

        # print(transformation)
        # print(figure.objects)
        # initialization
        diff = len(transformation['mutations']) - len(figure.objects)
        if diff < 0:
            # if target figure has more objects than available transformation, add placeholder objects to mutations
            for i in range(abs(diff)):
                transformation['mutations'].append(self.__init_mutation(None, None, True))
        elif diff > 0:
            # if target figure has more objects than available transformation, add new placeholder objects to figure
            for i in range(abs(diff)):
                figure.objects[_PLACEHOLDER_NEW_PREFIX + str(i)] = RavensObject(_PLACEHOLDER_NEW_PREFIX)


        # iterate over all mutations
        mutation_list = {}
        for index, mutation in enumerate(transformation['mutations']):

            if mutation['type'] != 'placeholder':
                # use from_obj name as key
                from_obj_name = mutation['from'].name
                mutation_list[from_obj_name] = mutation
            else:
                # use a dummy name as key
                mutation_list[_PLACEHOLDER_NEW_PREFIX + str(index)] = mutation

        # create new possible mappings with mutation_list
        new_possible_mappings = [zip(mapping, figure.objects) for mapping in
                                      itertools.permutations(mutation_list, len(figure.objects))]

        transformations = []
        for mapping in new_possible_mappings:
            # deep copy figure_from
            figure_copy = copy.deepcopy(figure)

            # give it a new name
            figure_copy.name = self.__tuple_list_to_string(mapping)

            for obj_link in mapping:
                from_obj_name = obj_link[0]
                to_obj_name = obj_link[1]

                obj_link_mutations = mutation_list[from_obj_name]['attribute_changes']

                # Convert target attributes from dict to list
                target_attributes = []
                for attr in figure_copy.objects[to_obj_name].attributes.items():
                    target_attributes.append(attr)

                # apply deletion
                if len(obj_link_mutations) > 0 and obj_link_mutations[0] == _DELETED:
                    del figure_copy.objects[to_obj_name]
                    # probably not necessary
                    continue

                for target_attr in target_attributes:
                    for mutation in obj_link_mutations:
                        if target_attr[0] == mutation[0]:
                            figure_copy.objects[to_obj_name].attributes[target_attr[0]] = \
                                mutation[1]

                        # Special case for when there is a reflection (Remove angle, flie reflectable properties)
                        elif mutation[0] == _REFLECTION:
                            figure_copy.objects[to_obj_name].attributes[_REFLECTION] = \
                                mutation[1]

                attributes = figure_copy.objects[to_obj_name].attributes
                if _REFLECTION in attributes:
                    reflection_axis = attributes[_REFLECTION]

                    # Handle alignment reflection
                    if 'alignment' in attributes:
                        # Delete angle
                        if 'angle' in figure_copy.objects[to_obj_name].attributes:
                            del figure_copy.objects[to_obj_name].attributes['angle']

                        figure_copy.objects[to_obj_name].attributes['alignment'] = \
                            self.__flip_alignment(reflection_axis, attributes['alignment'])

                    # Handle angle reflection
                    if 'angle' in attributes:
                        figure_copy.objects[to_obj_name].attributes['angle'] = \
                            self.__flip_angle(reflection_axis, attributes['angle'])
                    # Delete reflection property introduced by the agent
                    del figure_copy.objects[to_obj_name].attributes[_REFLECTION]


            transformations.append(figure_copy)

        return transformations

    def __find_best_transformation(self, transformations):
        best_transformation = None
        best_transformation = transformations[0]
        best_transformation_count = 0
        best_transformation_count = self.__get_mutations_count(best_transformation)

        # Apply each transformation to C, and see what comes out at the other end
        for transformation in transformations:
            count = self.__get_mutations_count(transformation)
            if (count < best_transformation_count):
                best_transformation = transformation
                best_transformation_count = count
                continue

        return best_transformation

    def __get_mutations_count(self, transformation):
        # return reduce(lambda acc, curr: acc + len(curr['mutations']) if isinstance(acc, int) \
        #     else len(acc['mutations']) + len(curr['mutations']), transformation)

        count = 0
        for mutation in transformation['mutations']:
            count += len(mutation['attribute_changes'])
        return count

    def get_alignment_reflection_axis(self, align_from, align_to):
        if align_from.startswith('top'):
            if ((align_from == 'top-left' and  align_to == 'top-right') or
                (align_from == 'top-right' and  align_to == 'top-left')):
                return 'x'

            if ((align_from == 'top-left' and  align_to == 'bottom-left') or
                (align_from == 'top-right' and  align_to == 'bottom-right')):
                return 'y'

        if align_from.startswith('bottom'):
            if ((align_from == 'bottom-left' and  align_to == 'bottom-right') or
                (align_from == 'bottom-right' and  align_to == 'bottom-left')):
                return 'x'

            if ((align_from == 'bottom-left' and  align_to == 'top-left') or
                (align_from == 'bottom-right' and  align_to == 'top-right')):
                return 'y'
        return False

    def get_angle_reflection_axis(self, angle_from, angle_to):
        # the value is misleading, here it just indicates there's reflection
        # the value y is chosen to align with Get_Alignment_Reflection_Axis
        if ((angle_from == '45' and angle_to == '135') or
            (angle_from == '135' and angle_to == '45')):
            return 'y'
        if ((angle_from == '315' and angle_to == '225') or
            (angle_from == '225' and angle_to == '315')):
            return 'y'
        if ((angle_from == '270' and angle_to == '0') or
            (angle_from == '0' and angle_to == '270')):
            return 'y'
        return False

    def __tuple_list_to_string(self, list):
        items = []
        for tuple in list:
            items.append('(' + str(tuple[0]) + ' -> ' + str(tuple[1]) + ')')
        return ', '.join(items)

    def __flip_alignment(self, axis, alignment):
        for reflection in self.align_reflections_map[axis]:
            if reflection[0] == alignment:
                return reflection[1]
            elif reflection[1] == alignment:
                return reflection[0]

    def __flip_angle(self, axis, angle):
        for axis in self.angle_reflections_map.items():
            for property in axis[1]:
                if property[0] == angle:
                    return  property[1]
                elif property[1] == angle:
                    return property[0]
