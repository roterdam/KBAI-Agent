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
#from PIL import Image

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
    def Solve(self,problem):

        parsedObject= self.constructCorrectStructures(problem)
        answer =self.findAnswer(parsedObject)

        if len(answer)>0:
            return answer.keys()[0]
        else:
            return -1

    def constructCorrectStructures(self, problem):
        problems={}
        problems['given']={}
        problems['solutions']={}
        problems['problemSize']= str.split(problem.problemType, 'x')
        newProblem ={};
        for figure in  problem.figures:
            if figure.isalpha():
                self.appendProblemToCorrectStructures(problems, problem, figure, 1)
            else:
                 self.appendProblemToCorrectStructures(problems, problem, figure, 0)
        newProblem=problems;

        return newProblem;




    def appendProblemToCorrectStructures(self, problems, problem, figure, isProblem):
        if isProblem:
            parsedProblem={problem.figures[figure].name :[]}
            for object in  problem.figures[figure].objects:
                parsedProblem[problem.figures[figure].name].append(problem.figures[figure].objects[object].attributes )
            problems['given'].update(parsedProblem)
        else:
            parsedSolution={ problem.figures[figure].name:[]}
            for object in  problem.figures[figure].objects:
                parsedSolution[problem.figures[figure].name].append(problem.figures[figure].objects[object].attributes)
            problems['solutions'].update(parsedSolution)




    def findAnswer(self, parsedObject):
        filteredSolution = parsedObject['solutions']

        #if 2x2 matrix
        if parsedObject['problemSize'][0] == '2' and parsedObject['problemSize'][1] == '2' :
            #if same # of figures present
            self.removeAnswersBasedOnSize(parsedObject, filteredSolution)

            problem_A = parsedObject['given']['A']
            problem_B = parsedObject['given']['B']
            problem_C = parsedObject['given']['C']
            if len(problem_A)== len(problem_B):
                for index, shape in enumerate(problem_A):

                    for attribute in shape:

                        if attribute =='shape':
                            if problem_A[index]['shape']== problem_B[index]['shape']:
                                indexToDelete =[]
                                for solution in filteredSolution:
                                    if problem_C[index]['shape']==filteredSolution[solution][index]['shape']:
                                        continue
                                    else:
                                        indexToDelete.append(solution);
                                for x in indexToDelete:
                                    filteredSolution.pop(x)

                        elif attribute =='fill':
                            if problem_A[index]['fill']== problem_B[index]['fill']:
                                indexToDelete =[]
                                for solution in filteredSolution:
                                    if problem_C[index]['fill']==filteredSolution[solution][index]['fill']:
                                        continue
                                    else:
                                        indexToDelete.append(solution);

                                for x in indexToDelete:
                                    filteredSolution.pop(x)

                        elif attribute =='size':
                            if problem_A[index]['size']== problem_B[index]['size']:
                                indexToDelete =[]
                                for solution in filteredSolution:
                                    if problem_C[index]['size']==filteredSolution[solution][index]['size']:
                                        continue
                                    else:
                                        indexToDelete.append(solution);

                                for x in indexToDelete:
                                    filteredSolution.pop(x)

                        elif attribute =='angle':
                            if 'angle' in problem_B[index] and  problem_A[index]['angle']== problem_B[index]['angle']:
                                indexToDelete =[]
                                for solution in filteredSolution:
                                    if problem_C[index]['angle']==filteredSolution[solution][index]['angle']:
                                        continue
                                    else:
                                        indexToDelete.append(solution);

                                for x in indexToDelete:
                                    filteredSolution.pop(x)
                            elif 'angle' in problem_B[index] and problem_A[index]['angle']!= problem_B[index]['angle']:
                                rotation= abs(int(problem_A[index]['angle'])- int(problem_B[index]['angle']))
                                indexToDelete =[]
                                for solution in filteredSolution:
                                    if abs(int(problem_C[index]['angle'])-int(filteredSolution[solution][index]['angle']))==rotation:
                                        continue
                                    else:
                                        indexToDelete.append(solution);

                                for x in indexToDelete:
                                    filteredSolution.pop(x)




        return filteredSolution;

    def removeAnswersBasedOnSize(self,parsedObject,filteredSolution):
        problem_A = parsedObject['given']['A']
        problem_B = parsedObject['given']['B']
        problem_C = parsedObject['given']['C']
        indexToDelete=[]
        if  len(problem_A)== len(problem_B):
            #remove all solutions that miss cases number
            for solution in filteredSolution:
                if len(problem_C)==len(filteredSolution[solution]):
                    continue
                else:
                    indexToDelete.append(solution)

            for x in indexToDelete:
                filteredSolution.pop(x)
        elif len(problem_A)>len(problem_B):
            for solution in filteredSolution:
                if len(problem_C)>len(filteredSolution[solution]):
                    continue
                else:
                    indexToDelete.append(solution);

            for x in indexToDelete:
                filteredSolution.pop(x)

        elif len(problem_A)<len(problem_B):
            for solution in filteredSolution:
                if len(problem_C)>len(filteredSolution[solution]):
                    continue
                else:
                    indexToDelete.append(solution)

            for x in indexToDelete:
                filteredSolution.pop(x)