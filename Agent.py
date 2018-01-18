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
        # print(self.obj_info)
        # print(self.fig_list)
        # print(self.ans_list)
        # print('\n\n')

        # print(self.scores)
        # print(self.transformations)
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

        delWeight = 300 # weight for same deletion of objects

        score = 0

        # compare A to B
        for obj_a in figure_a:

            for obj_b in figure_b:
                self.CompareAlignment('A', obj_a, 'B', obj_b)

        # Compare deletion from AB to CD
        self.CompareObjsDeletion('A', figure_a, 'B', figure_b)
        self.CompareObjsDeletion('C', figure_c, candidate_name, figure_candidate)

        # number of deletions are the same
        if (self.transformations['C' + candidate_name]['deletion'] == self.transformations['AB']['deletion']):
            score += (delWeight * self.transformations['AB']['deletion'])

        # Compare deletion from AC to BD
        self.CompareObjsDeletion('A', figure_a, 'C', figure_c)
        self.CompareObjsDeletion('B', figure_b, candidate_name, figure_candidate)

        # number of deletions are the same
        if (self.transformations['B' + candidate_name]['deletion'] == self.transformations['AC']['deletion']):
            score += (delWeight * self.transformations['AC']['deletion'])

        # loop over the objects inside a candidate figure
        # for obj_cand in figure_candidate:




        # return score
        return -1

    def InitTransformation(self):
        transformation = {
            'deletion': float("inf"),
            'angle': {},
            'fill': {},
            'shape': {},
            'alignment': {}
        }
        return transformation

    def CompareObjsDeletion(self, candidate_name_1, candidate_1, candidate_name_2, candidate_2):
        key = candidate_name_1 + candidate_name_2
        self.transformations[key]['deletion'] = len(candidate_1) - len(candidate_2)

    def CompareAlignment(self, candidate_name_1, obj_1, candidate_name_2, obj_2):
        key = candidate_name_1 + candidate_name_2
        obj_key = obj_1.name + '->' + obj_2.name

        # if ('alignment' in obj_1.attributes and 'alignment' in obj_2.attributes and
        #     obj_1.name == obj_2.name):
        if ('alignment' in obj_1.attributes and 'alignment' in obj_2.attributes):
            self.transformations[key]['alignment'] = {
                'from_name': obj_1.name,
                'from': obj_1.attributes['alignment'],
                'to_name': obj_2.name,
                'to': obj_2.attributes['alignment']
            }

            print(self.transformations[key]['alignment'])
