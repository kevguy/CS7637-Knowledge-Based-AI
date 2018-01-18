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
from PIL import Image
import numpy

show_weight = False

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
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

        # loop over the figures, each figure has a name
        self.obj_info, self.fig_list, self.ans_list = self.Create_Obj_Info(problem)
        self.transformations = {}
        self.scores = {}
        for candidate in self.ans_list:
            # print(candidate)
            # print(self.obj_info[candidate])
            self.scores[candidate] = self.Compare2x2(candidate, self.obj_info[candidate])
            print('\n')
        # print(self.obj_info)
        # print(self.fig_list)
        # print(self.ans_list)
        # print('\n\n')

        # print(self.scores)
        # print(self.transformations)
        # for transformation in self.transformations:
        #     print(self.transformations[transformation]['shape'])
        return -1

    # take a file path and display the image
    def ShowImage(self, file_path):
        img = Image.open(file_path, 'r')
        img.show()

    # Show all images in the problem
    def ShowAllImages(self, problem):
        for fig_name in problem.figures:
            file_path = problem.figures[fig_name].visualFilename
            self.ShowImage(file_path)

    def Create_Obj_Info(self, problem):
        # loop over the figures, each figure has a name
        # and each figure has a list of objects
        # each object also has a name and its attributes
        obj_dict = {}
        fig_list = []
        ans_list = []

        for fig_name in problem.figures:
            if (fig_name.isdigit()):
                ans_list.append(fig_name)
            else:
                fig_list.append(fig_name)

            fig = problem.figures[fig_name]

            obj_arr = []
            for raven_obj in fig.objects:
                obj_arr.append(fig.objects[raven_obj])
                # print(fig.objects[raven_obj].name)
                # print(fig.objects[raven_obj].attributes)
            obj_dict[fig_name] = obj_arr
        # print('\n\n')
        fig_list.sort()
        ans_list.sort()
        return obj_dict, fig_list, ans_list

    def Compare2x2(self, candidate_name, candidate):
        figure_a = self.obj_info['A']
        figure_b = self.obj_info['B']
        figure_c = self.obj_info['C']
        figure_candidate = self.obj_info[candidate_name]

        self.transformations['AB'] = self.InitTransformation()
        self.transformations['AC'] = self.InitTransformation()
        self.transformations['C' + candidate_name] = self.InitTransformation()
        self.transformations['B' + candidate_name] = self.InitTransformation()

        delWeight = 1 # weight for same deletion of objects
        alignWeight = 3 # weight for same alignments
        fillWeight = 3 # weight for fill
        reflectionWeight = 4 # weight for reflection
        angleWeight = 3 # weight for angle
        sizeWeight = 2 # weight for size
        unchangeWeight = 30 # weight for a shape being unchanged
        shapeUnchangeWeight = 30 # weight for a shape being unchanged
        shapeWeight = 3 # weight for a same shape transformation
        fillUnchangeWeight = 2 # weight for fill property being unchanged
        angleUnchangeWeight = 2 # weight for angle property being unchanged
        sizeUnchangeWeight = 2 # weight for size property being unchanged

        abScore = 0
        acScore = 0

        # loop over the objects inside a figure
        # compare A with B
        for obj_a in figure_a:
            for obj_b in figure_b:
                self.LinkAlignment('A', obj_a, 'B', obj_b)
                self.LinkShape('A', obj_a, 'B', obj_b)

        # compare A with C
        for obj_a in figure_a:
            for obj_c in figure_c:
                self.LinkAlignment('A', obj_a, 'C', obj_b)
                self.LinkShape('A', obj_a, 'C', obj_b)

        # compare B with candidate
        for obj_b in figure_b:
            for obj_cand in figure_candidate:
                self.LinkAlignment('B', obj_b, candidate_name, obj_cand)
                self.LinkShape('B', obj_b, candidate_name, obj_cand)

        # compare C with candidate
        for obj_c in figure_c:
            for obj_cand in figure_candidate:
                self.LinkAlignment('C', obj_c, candidate_name, obj_cand)
                self.LinkShape('C', obj_c, candidate_name, obj_cand)

        # Compare deletion from AB to CD
        self.CompareObjsDeletion('A', figure_a, 'B', figure_b)
        self.CompareObjsDeletion('C', figure_c, candidate_name, figure_candidate)

        # Compare deletion from AC to BD
        self.CompareObjsDeletion('A', figure_a, 'C', figure_c)
        self.CompareObjsDeletion('B', figure_b, candidate_name, figure_candidate)

        #######################################################################
        # compare deletions
        # number of deletions are the same
        print('calculating AB Score')

        abScore = self.CalculateScore(['A', 'B'], ['C', candidate_name])
        acScore = self.CalculateScore(['A', 'C'], ['B', candidate_name])

        print(abScore)
        print(acScore)
        print('-------------------------------------------\n')

        # return score
        return -1

    def CalculateScore(self, from_pair, to_pair):
        orgPair = from_pair[0] + from_pair[1]
        newPair = to_pair[0] + to_pair[1]

        score = 0

        delWeight = 1 # weight for same deletion of objects
        alignWeight = 3 # weight for same alignments
        fillWeight = 3 # weight for fill
        reflectionWeight = 4 # weight for reflection
        angleWeight = 3 # weight for angle
        sizeWeight = 2 # weight for size
        shapeUnchangeWeight = 30 # weight for a shape being unchanged
        shapeWeight = 3 # weight for a same shape transformation
        fillUnchangeWeight = 2 # weight for fill property being unchanged
        angleUnchangeWeight = 2 # weight for angle property being unchanged
        sizeUnchangeWeight = 2 # weight for size property being unchanged

        sameShapeModifier = 1.5

        if (self.transformations[newPair]['deletion'] == self.transformations[orgPair]['deletion']):
            score += (delWeight * abs(self.transformations[orgPair]['deletion']))

        # compare alignments
        if ('alignment' in self.transformations[orgPair] and 'alignment' in self.transformations[newPair]):
            for alignment in self.transformations[newPair]['alignment']:
                for alignmentOrg in self.transformations[orgPair]['alignment']:
                    if (alignment['from'] == alignmentOrg['from'] and alignment['to'] == alignmentOrg['to']):
                        score += alignWeight
                        if show_weight:
                            print('alignWeight')

        # compare shapes
        for shape_cand in self.transformations[newPair]['shape']:
            for shape_ab in self.transformations[orgPair]['shape']:

                # first verify the transformation is unchanged in both relationships
                if (shape_cand['changed'] == shape_ab['changed'] and shape_cand['changed'] == False):
                    score += shapeUnchangeWeight
                    if show_weight:
                        print('shapeUnchangeWeight')
                else:
                    # compare transformation
                    if (shape_cand['transform']['changed'] == False and
                        shape_ab['transform']['changed'] == False):
                        score += shapeUnchangeWeight
                        if show_weight:
                            print('shapeUnchangeWeight')
                    elif (shape_cand['transform']['changed'] == True and
                        shape_ab['transform']['changed'] == True):
                        if (shape_cand['transform']['from'] == shape_ab['transform']['from'] and
                            shape_cand['transform']['to'] == shape_ab['transform']['to']):
                            score += shapeWeight
                            if show_weight:
                                print('shapeWeight')


                    # compare fill, angle, size
                    if ('fill' in shape_cand and 'fill' in shape_ab):
                        if (shape_cand['fill']['changed'] == False and shape_ab['fill']['changed'] == False):
                            # fill property unchanged
                            score += fillUnchangeWeight
                            if show_weight:
                                print('fillUnchangeWeight')
                        elif (shape_cand['fill']['changed'] == True and shape_ab['fill']['changed'] == True):
                            if (shape_cand['fill']['from'] == shape_ab['fill']['from'] and
                                shape_cand['fill']['to'] == shape_ab['fill']['to']):
                                # fill property changed, but transformation are the same
                                score += fillWeight
                                if show_weight:
                                    print('fillWeight')

                    if ('angle' in shape_cand and 'angle' in shape_ab):
                        if (shape_cand['angle']['changed'] == False and shape_ab['angle']['changed'] == False):
                            # fill property unchanged
                            score += angleUnchangeWeight
                            if show_weight:
                                print('angleUnchangeWeight')
                        elif (shape_cand['angle']['changed'] == True and shape_ab['angle']['changed'] == True):
                            if (shape_cand['angle']['diff'] == shape_ab['angle']['diff']):
                                # fill property changed, but transformation are the same
                                if (abs(shape_cand['angle']['diff']) == 180 or abs(shape_cand['angle']['diff']) == 360):
                                    score += reflectionWeight
                                    if show_weight:
                                        print('reflectionWeight')
                                else:
                                    score += angleWeight
                                    if show_weight:
                                        print('angleWeight')



                    if ('size' in shape_cand and 'size' in shape_ab):
                        if (shape_cand['size']['changed'] == False and shape_ab['size']['changed'] == False):
                            # size property unchanged
                            score += sizeUnchangeWeight
                            if show_weight:
                                print('sizeUnchangeWeight')
                        elif (shape_cand['size']['changed'] == True and shape_ab['size']['changed'] == True):
                            if (shape_cand['size']['from'] == shape_ab['size']['from'] and
                                shape_cand['size']['to'] == shape_ab['size']['to']):
                                # size property changed, but transformation are the same
                                score += sizeWeight
                                if show_weight:
                                    print('sizeUnchangeWeight')

        return score

    def InitTransformation(self):
        transformation = {
            'deletion': float("inf"),
            'shape': [],
            'alignment': [],
            'inside': []
        }
        return transformation

    def CompareObjsDeletion(self, candidate_name_1, candidate_1, candidate_name_2, candidate_2):
        key = candidate_name_1 + candidate_name_2
        self.transformations[key]['deletion'] = len(candidate_1) - len(candidate_2)

    def LinkAlignment(self, candidate_name_1, obj_1, candidate_name_2, obj_2):
        key = candidate_name_1 + candidate_name_2

        # if ('alignment' in obj_1.attributes and 'alignment' in obj_2.attributes and
        #     obj_1.name == obj_2.name):
        if ('alignment' in obj_1.attributes and 'alignment' in obj_2.attributes):
            self.transformations[key]['alignment'].append({
                'from_name': obj_1.name,
                'from': obj_1.attributes['alignment'],
                'to_name': obj_2.name,
                'to': obj_2.attributes['alignment']
            })

    def LinkShape(self, candidate_name_1, obj_1, candidate_name_2, obj_2):
        key = candidate_name_1 + candidate_name_2
        info = {
            'from_name': obj_1.name,
            'to_name': obj_2.name,
            'changed': False
        }

        # check if both shapes are the same
        if (obj_1.attributes['shape'] == obj_2.attributes['shape']):
            # shapes are the same
            info['transform'] = {
                'changed': False
            }
        else:
            # shape transformation
            info['changed'] = True
            info['transform'] = {
                'changed': True,
                'from': obj_1.attributes['shape'],
                'to': obj_2.attributes['shape']
            }

        # see if shape goes from unfilled to filled or vice versa
        if ('fill' in obj_1.attributes and 'fill' in obj_2.attributes and
            (obj_1.attributes['fill'] != obj_2.attributes['fill'])):
            info['changed'] = True
            info['fill'] = {
                'changed': True,
                'from': obj_1.attributes['fill'],
                'to': obj_2.attributes['fill']
            }
        else:
            info['fill'] = {
                'changed': False
            }

        # see if shape has angle transformation
        if ('angle' in obj_1.attributes and 'angle' in obj_2.attributes and
            (obj_1.attributes['angle'] != obj_2.attributes['angle'])):
            info['changed'] = True
            info['angle'] = {
                'changed': True,
                'from': int(obj_1.attributes['angle']),
                'to': int(obj_2.attributes['angle']),
                'diff': int(obj_2.attributes['angle']) - int(obj_1.attributes['angle'])
            }
        else:
            info['angle'] = {
                'changed': False
            }

        # see if shape has size change
        if ('size' in obj_1.attributes and 'size' in obj_2.attributes and
            (obj_1.attributes['size'] != obj_2.attributes['size'])):
            info['changed'] = True
            info['size'] = {
                'changed': True,
                'from': obj_1.attributes['size'],
                'to': obj_2.attributes['size']
            }
        else:
            info['size'] = {
                'changed': False
            }


        self.transformations[key]['shape'].append(info)
