# Author: Daniel Rozen

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
from collections import OrderedDict

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().

    # . The constructor will be called at the beginning of the program, so you may
    #  use this method to initialize any information necessary before your agent begins
    #  solving problems.
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an integer representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These integers
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName() (as Strings).
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(int givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will *not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.

    # If your agent wants to skip a question, it should return a negative number.
    def Solve(self, problem):

        print("\n" + problem.name + "\n")
        print(self.removeDuplicates("I-love-love"))

        # compare shapes and attributes across figures A,B,C:

        # Define figure variables
        a = problem.figures['A']
        b = problem.figures['B']
        c = problem.figures['C']

        p1 = problem.figures['1']
        p2 = problem.figures['2']
        p3 = problem.figures['3']
        p4 = problem.figures['4']
        p5 = problem.figures['5']
        p6 = problem.figures['6']

        maxTot = 0   # initiate a best answer score variable to 0
        answer = 1   # initialize best answer response

        sameIncr = .1  # same general property increment value
        angleIncr = 20   # same angle rotation transform increment value
        reflectIncr = 30  # same reflection transform increment value
        fillIncr = 25  # increment for correct fill transformation
        shapeIncr = 200 # increment for correct shape transformation
        deleteIncr = 300 # increment for correct deletion of objects
        alignIncr = 30 # increment for correct alignment transformation
        # TODO: add size, above, and inside transformations

        for x in range(1, 7):     # loop through each potential answer from 1 to 6:

            print('\n  Now comparing answer: ' + str(x) + ' to ' + problem.name )
            tot = 0   # initialize

            transformDict = {}  # create dictionary for transformations
            # initialize empty keys for angle transformations
            transformDict['abAngleDiff'] = None
            transformDict['cdAngleDiff'] = None
            transformDict['acAngleDiff'] = None
            transformDict['bdAngleDiff'] = None

            # initialize empty keys for fill transformations
            transformDict['abFillDiff'] = None
            transformDict['cdFillDiff'] = None
            transformDict['acFillDiff'] = None
            transformDict['bdFillDiff'] = None

            # initialize empty keys for shape transformations
            transformDict['abShapeDiff'] = ''
            transformDict['cdShapeDiff'] = ''
            transformDict['acShapeDiff'] = ''
            transformDict['bdShapeDiff'] = ''

            # initialize empty keys for alignment transformations

            transformDict['abAlignDiff'] = 'empty-'
            transformDict['cdAlignDiff'] = 'empty-'
            transformDict['acAlignDiff'] = 'empty-'
            transformDict['bdAlignDiff'] = 'empty-'


            # compare deletion from AB to CD
            transformDict['abDeleteDiff'] = len(a.objects) - len(b.objects)
            print('abDeleteDiff: ' + str(transformDict['abDeleteDiff']))
            transformDict['cdDeleteDiff'] = len(c.objects) - len(problem.figures[str(x)].objects)
            print('cdDeleteDiff: ' + str(transformDict['cdDeleteDiff']))

            if transformDict['abDeleteDiff'] ==  transformDict['cdDeleteDiff']:
                tot += (deleteIncr * transformDict['abDeleteDiff'])
                # tot += (deleteIncr)
                print('AB CD same deletion!')
            # compare deltion from AC to BD
            transformDict['acDeleteDiff'] = len(a.objects) - len(c.objects)
            print('acDeleteDiff: ' + str(transformDict['acDeleteDiff']))

            transformDict['bdDeleteDiff'] = len(b.objects) - len(problem.figures[str(x)].objects)
            print('bdDeleteDiff: ' + str(transformDict['bdDeleteDiff']))

            if transformDict['acDeleteDiff'] ==  transformDict['bdDeleteDiff']:
                tot += (deleteIncr * transformDict['acDeleteDiff'])
                # tot += (deleteIncr)

                print('AC BD same deletion!')

            for ansObjName in self.sortDict(problem.figures[str(x)].objects):
                ansObj = problem.figures[str(x)].objects[ansObjName]

                # compare A to B
                for aObjName in self.sortDict(a.objects):
                    aObj = a.objects[aObjName]
                    for bObjName in self.sortDict(b.objects):
                        bObj = b.objects[bObjName]
                        makeAngTransCompAB = False   # flags to ensure that angle transformations are only made for objects with angles
                        # make alignment transformation comparison
                        if 'alignment' in aObj.attributes and 'alignment' in bObj.attributes:
                            if aObj.attributes['alignment'] != bObj.attributes['alignment']:
                                transformDict['abAlignDiff'] = aObj.attributes['alignment'] + '-' + bObj.attributes['alignment']
                                # remove duplicate words
                                transformDict['abAlignDiff'] = self.removeDuplicates(transformDict['abAlignDiff'])
                                print('abAlignDiff: ' + transformDict['abAlignDiff'])

                        # TODO: Investigate the following if statement.  Perhaps some items under it should be brought above it
                        # check for same shape or sizes in objects in A and B for comparison of same objects
                        if aObj.attributes['shape'] == bObj.attributes['shape']:
                        # if aObj.attributes['shape'] == bObj.attributes['shape'] or aObj.attributes['size'] == bObj.attributes['size']:

                            # make fill transform:  if same int = 0, if different, int = 1
                            #calculate AB fill difference
                            if aObj.attributes['fill'] == bObj.attributes['fill']:
                                transformDict['abFillDiff'] = 0
                            else:
                                transformDict['abFillDiff'] = 1 # if the fill changed across the transformation assign a 1

                            # make transformation comparisons for angles:

                            print("making angle transformation comparisons")
                            if 'angle' in aObj.attributes and 'angle' in bObj.attributes: # check that this object has angles

                                #calculate AB angle difference
                                transformDict['abAngleDiff'] = int(aObj.attributes['angle']) - int(bObj.attributes['angle'])
                                makeAngTransCompAB = True
                                print("abAngleDiff= " + str(transformDict['abAngleDiff']))
                            else:
                                makeAngTransCompAB = False

                        # check for shape transform:
                        else:
                            transformDict['abShapeDiff'] = (aObj.attributes['shape'] + bObj.attributes['shape'])
                            print('\n  SHAPE TRANSFORM for AB: ' + transformDict['abShapeDiff'])

                # compare C to D

                for cObjName in self.sortDict(c.objects):
                    makeAngTransCompCD = False
                    cObj = c.objects[cObjName]

                    #calculate CD fill difference
                    ansValue = ansObj.attributes['fill']
                    if (cObj.attributes['fill'] == ansValue):
                        transformDict['cdFillDiff'] = 0
                    else:
                        transformDict['cdFillDiff'] = 1
                     # Make fill transformation comparison:
                    if transformDict['abFillDiff']== transformDict['cdFillDiff']:
                        tot += fillIncr
                        print("CORRECT ab = cd FILL transformations!")

                    # check alignment transform
                    if 'alignment' in cObj.attributes and 'alignment' in ansObj.attributes:
                        if cObj.attributes['alignment'] != ansObj.attributes['alignment']:
                            transformDict['cdAlignDiff'] = cObj.attributes['alignment'] + '-' + ansObj.attributes['alignment']
                            print('cdAlignDiff: ' + transformDict['cdAlignDiff'])
                            # remove duplicate words
                            transformDict['cdAlignDiff'] = self.removeDuplicates(transformDict['cdAlignDiff'])
                            print('cdAlignDiff: ' + transformDict['cdAlignDiff'])
                    # calculate alignment transform differences
                    if sorted(transformDict['abAlignDiff']) == sorted(transformDict['cdAlignDiff']) and transformDict['abAlignDiff'] != 'empty-' and transformDict['cdAlignDiff'] != 'empty-':
                        tot += alignIncr
                        print("CORRECT ab = cd Align transformations!")

                    if cObj.attributes['shape'] == ansObj.attributes['shape']: # check for same shape in objects
                    # if cObj.attributes['shape'] == ansObj.attributes['shape'] or cObj.attributes['size'] == ansObj.attributes['size']:


                            # if angle transformation equal tot+=1

                        if 'angle' in cObj.attributes and 'angle' in ansObj.attributes: # check that this object has angles
                                transformDict['cdAngleDiff'] = int(cObj.attributes['angle']) - int(ansObj.attributes['angle'])
                                makeAngTransCompCD = True
                                print("cdAngleDiff= " + str(transformDict['cdAngleDiff']))
                        else:
                            makeAngTransCompCD = False
                    else:
                        # TODO: check for shape transform:
                        transformDict['cdShapeDiff'] = (cObj.attributes['shape'] + ansObj.attributes['shape'])
                        print('\n  SHAPE TRANSFORM! for CD: ' + transformDict['cdShapeDiff'])

                        if transformDict['abShapeDiff'] != '' and transformDict['cdShapeDiff'] != '':
                            # the sorting corrects the issue of the same shapes appearing in different orders
                            if sorted(transformDict['abShapeDiff']) == sorted(transformDict['cdShapeDiff']):
                                tot += shapeIncr
                                print("CORRECT SHAPE TRANSFORM! FOR AB TO CD")

                    if makeAngTransCompAB == True and makeAngTransCompCD == True:

                        if abs(transformDict['abAngleDiff'] + 180) % 360 == abs(transformDict['cdAngleDiff']):
                            tot += reflectIncr
                            print("ab = cd same reflections!")
                        elif transformDict['abAngleDiff'] == transformDict['cdAngleDiff']:
                            tot += angleIncr
                            print("ab = cd angle transformations!")

                # # compare A to C
                makeAngTransCompAC = False
                makeAngTransCompBD = False

                for aObjName in self.sortDict(a.objects):
                    aObj = a.objects[aObjName]
                    for cObjName in self.sortDict(c.objects):
                        cObj = c.objects[cObjName]

                        # make fill transform:  if same int = 0, if different, int = 1
                            #calculate AB fill difference
                        if (aObj.attributes['fill'] == cObj.attributes['fill']):
                            transformDict['acFillDiff'] = 0
                        else:
                            transformDict['acFillDiff'] = 1 # if the fill changed across the transformation assign a 1

                        # make alignment transformation comparison
                        if 'alignment' in aObj.attributes and 'alignment' in cObj.attributes:
                            if aObj.attributes['alignment'] != cObj.attributes['alignment']:
                                transformDict['acAlignDiff'] = aObj.attributes['alignment'] + '-' + cObj.attributes['alignment']
                                # remove duplicate words
                                transformDict['acAlignDiff'] = self.removeDuplicates(transformDict['acAlignDiff'])
                                print('acAlignDiff: ' + transformDict['acAlignDiff'])

                        if aObj.attributes['shape'] == cObj.attributes['shape']: # check for same shape in objects

                            if 'angle' in aObj.attributes and 'angle' in cObj.attributes: # check that this object has angles
                                #calculate AC angle difference
                                transformDict['acAngleDiff'] = int(aObj.attributes['angle']) - int(cObj.attributes['angle'])
                                makeAngTransCompAC = True
                                print("acAngleDiff= " + str(transformDict['acAngleDiff']))
                            else:
                                makeAngTransCompAC = False

                        #  check for shape transform:
                        else:
                            transformDict['acShapeDiff'] = (aObj.attributes['shape'] + cObj.attributes['shape'])
                            print('\n  SHAPE TRANSFORM! for AC: ' + transformDict['acShapeDiff'])

                # # compare B to D
                for bObjName in self.sortDict(b.objects):
                    bObj = b.objects[bObjName]

                    ansValue = ansObj.attributes['fill']
                    if (bObj.attributes['fill'] == ansValue):
                        transformDict['bdFillDiff'] = 0
                    else:
                        transformDict['bdFillDiff'] = 1

                     # Make fill transformation comparison:
                    if transformDict['acFillDiff'] == transformDict['bdFillDiff']:
                        tot += fillIncr
                        print("CORRECT ac = bd FILL transformations!")

                     # check alignment transform
                    if 'alignment' in bObj.attributes and 'alignment' in ansObj.attributes:
                        if bObj.attributes['alignment'] != ansObj.attributes['alignment']:
                            transformDict['bdAlignDiff'] = bObj.attributes['alignment'] + '-' + ansObj.attributes['alignment']
                            print('bdAlignDiff: ' + transformDict['bdAlignDiff'])
                            # remove duplicate words
                            transformDict['bdAlignDiff'] = self.removeDuplicates(transformDict['bdAlignDiff'])
                            print('bdAlignDiff: ' + transformDict['bdAlignDiff'])
                    # calculate alignment transform differences
                    if sorted(transformDict['acAlignDiff']) == sorted(transformDict['bdAlignDiff']) and transformDict['acAlignDiff'] != 'empty-' and transformDict['bdAlignDiff'] != 'empty-':
                        tot += alignIncr
                        print("CORRECT ac = bd Align transformations!")


                    if bObj.attributes['shape'] == ansObj.attributes['shape']: # check for same shape in objects
                        if 'angle' in bObj.attributes and 'angle' in ansObj.attributes: # check that this object has angles
                            transformDict['bdAngleDiff'] = int(bObj.attributes['angle']) - int(ansObj.attributes['angle'])
                            makeAngTransCompBD = True
                            print("bdAngleDiff= " + str(transformDict['bdAngleDiff']))
                        else:
                            makeAngTransCompBD = False

                    else:
                        # TODO: check for shape transform:
                        transformDict['bdShapeDiff'] = (bObj.attributes['shape'] + ansObj.attributes['shape'])
                        print('\n  SHAPE TRANSFORM! for BD: ' + transformDict['bdShapeDiff'])
                        if transformDict['acShapeDiff'] != '' and transformDict['bdShapeDiff'] != '':
                            # the sorting corrects the issue of the same shapes appearing in differnet orders
                            if sorted(transformDict['acShapeDiff']) == sorted(transformDict['bdShapeDiff']):
                                tot += shapeIncr
                                print("CORRECT SHAPE TRANSFORM! FOR AC TO BD")

                # if transformation equal tot+=1
                if makeAngTransCompAC == True and makeAngTransCompBD == True:
                    if abs(transformDict['acAngleDiff'] + 180) % 360 == abs(transformDict['bdAngleDiff']):
                        tot += reflectIncr
                        print("ac = bd same reflections!")
                    elif transformDict['acAngleDiff'] == transformDict['bdAngleDiff']:
                        tot += reflectIncr
                        print("ac = bd angle transformations!")

                # Todo: compare remaining attributes to answer

                for fig in [a, b, c]:
                    for matrixObjName in fig.objects:
                        attributeList = ['size', 'shape', 'fill', 'alignment', 'angle', 'above', 'inside']
                        for attributeName in attributeList:
                            if attributeName in fig.objects[matrixObjName].attributes and attributeName in ansObj.attributes:
                                if ansObj.attributes[attributeName] == fig.objects[matrixObjName].attributes[attributeName]:
                                    tot += sameIncr
                                    print('Figure' + str(fig.name) + ' attrib: ' +attributeName+ ' compared to ' + str(
                                        x) + ', current total = ' + str(tot))

                # if local answer > max answer:

                if tot > maxTot:
                    # max answer = local answer
                    print("previous maxTot = " + str(maxTot))
                    maxTot = tot
                    print("new maxTot = " + str(maxTot))
                    # answer = current answer
                    print("previous answer = " + str(answer))

                    answer = x

                    print("new answer = " + str(answer))

        print("final answer = " + str(answer))

        return answer

    def removeDuplicates(self, inputString):
        alignList = inputString.split('-')
        listString = ''
        removeWords = []
        for word in alignList:
            if word in listString:
                removeWords.append(word)
            else:
                listString += word
        for removeWord in removeWords:
            listString = listString.replace(removeWord, "")
        return listString

    def sortDict(self, dict):
        # return sorted(dict, key=dict.get)
        return dict
