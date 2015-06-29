
import time

from PIL import Image, ImageChops, ImageOps, ImageStat, ImageFilter
import math, operator
class VisAgent:
    def Solve(self, problem, answers):
        problem_figures={}
        transforms={}
        for figureName in problem.figures:

            figure = problem.figures[figureName]
            image = Image.open(figure.visualFilename).convert('L')
            problem_figures[figureName] = ImageOps.invert(image).filter(ImageFilter.GaussianBlur(3))

        transforms['CF'] = self.generateTransform(problem_figures['C'], problem_figures['F'])
        transforms['GH'] = self.generateTransform(problem_figures['G'], problem_figures['H'])
        transforms['AB'] = self.generateTransform(problem_figures['A'], problem_figures['B'])
        transforms['AD'] = self.generateTransform(problem_figures['A'], problem_figures['D'])
        transforms['BC'] = self.generateTransform(problem_figures['B'], problem_figures['C'])
        transforms['DE'] = self.generateTransform(problem_figures['D'], problem_figures['E'])
        transforms['BE'] = self.generateTransform(problem_figures['B'], problem_figures['E'])
        transforms['DG'] = self.generateTransform(problem_figures['D'], problem_figures['G'])
        transforms['EF'] = self.generateTransform(problem_figures['E'], problem_figures['F'])
        transforms['EH'] = self.generateTransform(problem_figures['E'], problem_figures['H'])

        scores={}
        row_scores ={}
        col_scores={}
        avg_score={}
        for x in answers:

            candidate = problem_figures[str(x)]

            transforms['F'+ str(x)] = self.generateTransform(problem_figures['F'], candidate)
            transforms['H'+ str(x)] = self.generateTransform(problem_figures['H'], candidate)

            row_scores[x]=(transforms['AB']+transforms['BC'] )- (transforms['DE']+transforms['EF'] )\
                      -(transforms['DE']+transforms['EF']-
                        (transforms['GH']+transforms['H'+ str(x)] ))

            col_scores[x]=(transforms['AD']+transforms['DG'] )\
                      - (transforms['BE']+transforms['EH'] )\
                      -(transforms['CF']+transforms['F'+ str(x)])

            scores[x]= abs(((transforms['CF']-transforms['F'+ str(x)])+\
                       (transforms['GH']-transforms['H'+ str(x)])))/2

            avg_score[x]=(abs(row_scores[x]+scores[x]))/2

        return min(scores,  key=scores.get)

    def generateTransform(self, srcImage, destImage):

        return self.rmsdiff(srcImage, destImage)

    def rmsdiff(self, im1, im2):
        "Calculate the root-mean-square difference between two images"

        h = ImageChops.difference(im2, im1).histogram()

        # calculate rms
        return math.sqrt(reduce(operator.add,
            map(lambda h, i: h*(i**2), h, range(256))
        ) / (float(im2.size[0]) * im2.size[1]))