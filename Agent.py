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
# from PIL import Image
import itertools, copy
from DictDiff import DictDiffer


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

    row1 = ["A", "B", "C"]
    row2 = ["D", "E", "F"]
    row3 = ["G", "H", "X"]

    LOCATION_ATTR = ['left-of', 'right-of', 'above', "inside", "overlaps"]

    X_COST_OBJECTS = {
        "fill": 2,
        "size": 3,
        "width": 5,
        "height": 5,
        "angle": 7,
        "shape": 9,

    }
    SIZE={
        "very small" :1,
        "small" :2,
        "medium" :3,
        "large" :4,
        "very large" :5,
        "huge" :6,
        }
    transformation_hash={}

    def Solve(self, problem):
        similarity_scores = {}

        # print "problem***************"
        # print "problem type: "+ problem.problemType
        print "problem name: " + problem.name
        # print "problem visual?: ",  problem.hasVisual
        # print "problem verbal: ", problem.hasVerbal
        # print "problem figures: ",  problem.figures

        # TODO: account for the angle
        # TODO: calculate


        figure_a = problem.figures["A"]
        figure_b = problem.figures["B"]
        figure_c = problem.figures["C"]
        figure_d = problem.figures["D"]
        figure_e = problem.figures["E"]
        figure_f = problem.figures["F"]
        figure_g = problem.figures["G"]
        figure_h = problem.figures["H"]
        similarity_scores['A_B'] = self.CalculateFigureScores(figure_a, figure_b)
        similarity_scores['A_D'] = self.CalculateFigureScores(figure_a, figure_d)
        similarity_scores['B_C'] = self.CalculateFigureScores(figure_b, figure_c)
        similarity_scores['B_E'] = self.CalculateFigureScores(figure_b, figure_e)
        similarity_scores['C_F'] = self.CalculateFigureScores(figure_c, figure_f)
        similarity_scores['E_H'] = self.CalculateFigureScores(figure_e, figure_h)
        similarity_scores['E_F'] = self.CalculateFigureScores(figure_e, figure_f)
        similarity_scores['D_E'] = self.CalculateFigureScores(figure_d, figure_e)
        similarity_scores['D_G'] = self.CalculateFigureScores(figure_d, figure_g)
        similarity_scores['G_H'] = self.CalculateFigureScores(figure_g, figure_h)

        first_row_score = similarity_scores['A_B'] + similarity_scores['B_C']
        second_row_score = similarity_scores['D_E'] + similarity_scores['E_F']

        first_col_score = similarity_scores['A_D'] + similarity_scores['D_G']
        second_col_score = similarity_scores['B_E'] + similarity_scores['E_H']

        answers = {}

        for x in range(1, 9):
            candidate = problem.figures[str(x)]

            scores_F_CANDIDATE = self.CalculateFigureScores(figure_f, candidate)
            scores_H_CANDIDATE = self.CalculateFigureScores(figure_h, candidate)
            # print "h:", scores_H_CANDIDATE, "f:",scores_F_CANDIDATE

            col_distance = scores_F_CANDIDATE - similarity_scores['C_F']
            row_distance = scores_H_CANDIDATE - similarity_scores['G_H']

            third_col_score = similarity_scores['C_F'] + scores_F_CANDIDATE
            third_row_score = similarity_scores['G_H'] + scores_H_CANDIDATE

            candidate_score = (abs(col_distance) + abs(row_distance))+ \
                              ( abs((first_row_score - second_row_score) - (second_row_score - third_row_score))) +\
                              ( abs((first_col_score - second_col_score) - (second_col_score - third_col_score)))

            # print "values: ", (abs(col_distance) + abs(row_distance)),( abs(first_row_score - second_row_score) - abs(second_row_score - third_row_score)) ,( abs(first_col_score - second_col_score) - abs(second_col_score - third_col_score))

            answers[x]=candidate_score

        # best_candidates_count=  [i for i, x in enumerate(answers) if x == min(answers, key=answers.get)]
        best_candidates= []
        first_lowest_index= min(answers, key=answers.get)
        lowest_score=answers[first_lowest_index]
        # print "count", best_candidates_count, "ls",lowest_score, "fls:", first_lowest_index


        for k, v in answers.items():
            if v==lowest_score:
                best_candidates.append(k)
        print "candidates", best_candidates
        print answers
            #        self.calculateBasedOnTransform(best_candidates)
        if len(best_candidates)>1:
            return-1
        else:
            print answers
            return best_candidates[0]


    def CalculateFigureScores(self, fig1, fig2):
        # add a point for every object added or deleted
        #obj_count_change= len(fig1.objects) - len(fig2.objects)
        self.transformation_hash[fig1.name+"_"+fig2.name]= {}
        score = 0

        obj1 = sorted(fig1.objects, key=fig1.objects.get)
        obj2 = sorted(fig2.objects, key=fig2.objects.get)
        for x, y in zip(obj1, obj2):
            self.transformation_hash[fig1.name+"_"+fig2.name][x]={'transform':self.calculateObjectScores(fig1.objects[x].attributes, fig2.objects[y].attributes)['transform']}
            score += self.calculateObjectScores(fig1.objects[x].attributes, fig2.objects[y].attributes)['score']

        return score

    def calculateObjectScores(self, obj1, obj2):
        score = 1
        diff = DictDiffer(obj1, obj2)
        new_att = diff.added()
        del_attr = diff.removed()
        changed_attr = diff.changed()
        unchanged_att = diff.unchanged()
        transform_values={}


        for x in changed_attr:
            transform_values[x]={"from":obj1[x], "to": obj2[x]}
            if x in self.LOCATION_ATTR:
                score*=1 #To DO figure out how to to deal with location
                # if abs(len(obj2[x])-len(obj1[x]))>0:
                #     score+=abs(len(obj1[x])-len(obj2[x]))
            elif x=='size':
                score *= self.SIZE[obj2[x]]-self.SIZE[obj1[x]]
            else:
                score *= self.X_COST_OBJECTS[x]
        for x in new_att:
            score+=4
        for x in del_attr:
            score+=14
        return {'score':score, "transform":{'changed':changed_attr, "unchanged" : unchanged_att, "deleted": del_attr, 'changed_values':transform_values}}



