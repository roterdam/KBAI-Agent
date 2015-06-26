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

import itertools, copy
MY_DEBUG=0
ATTRIBUTE_RANKING = ['shape', 'size', 'fill', 'angle', 'alignment']
#ATTRIBUTE_RANKING = ['shape', 'size', 'fill', 'angle', 'alignment', 'inside', 'above']
COST =  {'unchanaged': 0, 'reflected': 1, 'rotated': 2, 'moved': 2, 'scaled': 3, 'removed': 4, 'added': 4, 'fill': 5, 'changed': 6}

def get_cost(attribute, start, goal):
    if attribute == "shape":
        return COST['changed']
    elif attribute == "size":
        return COST['scaled']
    elif attribute == "fill":
        return COST['fill']
    elif attribute == "angle":
        return  COST['rotated']
    elif attribute == "alignment" or attribute == "inside" or attribute == "above":
        return COST['moved']
    else:
        raise Exception("Dont't know attribute '%s'"%attribute)

def print_objects(o):
    for obj1 in o: #loop thru all objects
        atts1=o[obj1].attributes
        print "Object Name: %s Attributes: %s"%(obj1,atts1)

def print_figure(f):
    print "Figure Name: ", f.name
    print_objects(f.objects)

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
        print ""
        print ""
        print "----------------------------------------------------------"
        print " -------Solving "+problem.name+", "+problem.problemType;

        # Convert input into dict
        if(problem.problemType=="2x2"):
            figure_a = problem.figures["A"]
            figure_b = problem.figures["B"]
            figure_c = problem.figures["C"]
            diff_score1=[]
            diff_score2=[]
            lowest1=float('inf');
            lowest2=float('inf');
            selection1=-1;
            selection2=-1;
            print print_objects(figure_a.objects)
            print print_objects(figure_b.objects)
            print print_objects(figure_c.objects)
            print "----------------------------------------------------------"
            print "------  Compare Question Figures -------------------------"
            trans_ac =  self.associate_figures(figure_a, figure_c)
            print "-- A to C: %s"%str(trans_ac)
            trans_ab =  self.associate_figures(figure_a, figure_b)
            print "-- A to B: %s"%str(trans_ab)

            print ""
            print "----------------------------------------------------------"
            print "------  Apply (A-C relationship ) to B -------------------"
            processed_b = copy.deepcopy(figure_b)
            processed_b.name="Processed_B"
            self.apply_trans(trans_ac,processed_b,figure_b,trans_ab,figure_a)
            print "-- Processed: "
            print_figure(processed_b)

            print ""
            print "----------------------------------------------------------"
            print "------  Find the best match to Processed B ---------------"
            for num in range(1,7):
                this_figure = problem.figures[str(num)]
                this_trans =  self.associate_figures(processed_b, this_figure)
                print "-- Processed_B to %s: %s"%(str(num),str(this_trans))
                this_score=this_trans['best_cost']
                diff_score1.append(this_score)
                if(this_score<=lowest1):
                    selection1=num
                    lowest1=this_score
            selection1_occurs=diff_score1.count(lowest1)
            print "Lowest occurs %s time(s)"%str(selection1_occurs)

            if selection1_occurs==1:
                print "*********** SELECTION 1 (option, cost): Figure %s with Cost %s"%(selection1,lowest1)
            else:
                selection1=-1

            print ""
            print "----------------------------------------------------------"
            print "------  Apply (A-B relationship ) to C -------------------"
            processed_c = copy.deepcopy(figure_c)
            processed_c.name="Processed_C"
            self.apply_trans(trans_ab,processed_c,figure_c,trans_ac,figure_a)
            print "-- Processed: "
            print_figure(processed_c)

            print ""
            print "----------------------------------------------------------"
            print "------  Find the best match to Processed C ---------------"
            for num in range(1,7):
                this_figure = problem.figures[str(num)]
                this_trans =  self.associate_figures(processed_c, this_figure)
                print "-- Processed_C to %s: %s"%(str(num),str(this_trans))
                this_score=this_trans['best_cost']
                diff_score2.append(this_trans['best_cost'])
                if(this_score<=lowest1):
                    selection2=num
                    lowest2=this_score
            selection2_occurs=diff_score2.count(lowest2)
            print "Lowest occurs %s time(s)"%str(selection2_occurs)

            if selection2_occurs==1:
                print "*********** SELECTION2 (option, cost): Figure %s with Cost %s"%(selection2,lowest2)
            else:
                selection2=-1

            print ""
            print ""
            print "----------------------------------------------------------"
            if(selection1==-1 and selection2==-1):
                 print "------- DECISION for %s: SKIPPING THIS ONE!"%problem.name
            elif(lowest1<=lowest2):
                print "------- DECISION for %s: ANSWER IS! "%problem.name, selection1
                problem.checkAnswer(selection1)
            elif(lowest2<lowest1):
                print "------- DECISION for %s: ANSWER IS! "%problem.name, selection2
                problem.checkAnswer(selection2)
            print "----------------------------------------------------------"
            print ""
        return -1

    def associate_figures(self, f1, f2):
        # extend figure with missing objects if necessary
        if len(f1.objects) < len(f2.objects):
            _figure_a = copy.deepcopy(f1)
            to_add = len(f2.objects) - len(f1.objects)
            for i in range(to_add):
                _figure_a.objects['temp'+str(i)]={}
            _figure_b = f2
        
        elif len(f1.objects) > len(f2.objects):
            _figure_b = copy.deepcopy(f2)
            to_add = len(f2.objects) - len(f1.objects)
            for i in range(-to_add):
                _figure_b.objects['temp'+str(i)]={}
            _figure_a = f1
        else:
            to_add = 0
            _figure_a = f1
            _figure_b = f2
        
        best_cost = float("inf")
        best_permutation = None
        changes = None
        
        # find best permutation of initial objects to correspond to goal objects
        for permutation in itertools.permutations(range(len(_figure_a.objects))):
            total_cost = 0
            total_change = []
            _fig_a_keys = _figure_a.objects.keys()
            _fig_b_keys = _figure_b.objects.keys()
            for x,y in zip(permutation, xrange(len(_figure_b.objects))):
                to_change, cost = self.associate_objects(_figure_a.objects[_fig_a_keys[x]],
                                                 _figure_b.objects[_fig_b_keys[y]])
                total_cost += cost
                total_change.append(to_change)

                if total_cost >= best_cost:
                    break
            
            if total_cost < best_cost:
                best_cost = total_cost
                best_permutation = permutation
                changes = total_change

            ret={'best_permutation': best_permutation, 'best_cost': best_cost, 'changes': changes, 'to_add': to_add}
        return ret

    def associate_objects(self, o1, o2):
        to_change=[]
        if not o1:
            to_change.append(("add", o2))

            cost = COST['added']
        elif not o2:
            to_change.append(("remove", o1))
            cost = COST['removed']
        else:
            cost = 0
            for attribute in ATTRIBUTE_RANKING:
                if attribute in o1.attributes and attribute in o2.attributes:
                    if o1.attributes[attribute] != o2.attributes[attribute]:
                        _cost = get_cost(attribute, o1.attributes[attribute], o2.attributes[attribute])
                        to_change.append((attribute, o1.attributes[attribute], o2.attributes[attribute]))
                        cost += _cost
        return to_change, cost

    def apply_attribute_to_object(self, object, change, reflection=0):
        #apply change to the object
        if MY_DEBUG:
            print "Applying Change...reflection: %s"%reflection
            print change
        key=change[0]
        old_value = change[1]
        new_value = change[2]

        if key in object.attributes:
            current_value = object.attributes[key]
            if key == "angle":
                if MY_DEBUG:
                    print "New %s, Old %s, Current %s"%(new_value,old_value,current_value)
                new_value=(abs(int(new_value)-int(old_value))+int(current_value))
                if reflection==1:
                    if MY_DEBUG:
                        print "Applying reflection: changed val from %s "%new_value
                    new_value=abs(new_value-180)
                    if MY_DEBUG:
                        print "Applying reflection: changed val to %s"%new_value
                new_value=new_value%360
                if MY_DEBUG:
                    print "Applying mod 360: changed val to %s"%new_value
                    print "-- Change, angle: ", new_value
            # process alignment - vertical and horizontal separately
            if key == "alignment":
                old_valign = old_value.split('-')[0]
                old_halign = old_value.split('-')[1]
                new_valign = new_value.split('-')[0]
                new_halign = new_value.split('-')[1]
                current_valign = current_value.split('-')[0];
                current_halign = current_value.split('-')[1];
                if old_valign != new_valign:
                    current_valign = new_valign
                if old_halign != new_halign:
                    current_halign = new_halign
                new_value = current_valign + "-" + current_halign
                if MY_DEBUG:
                    print "-- Change, alignment: ", str(new_value)
            object.attributes[key] = str(new_value);
        else:
            if MY_DEBUG:
                print "%s does not exist in attribute, no changes" % key
        return object;

    def apply_trans(self, trans, pfigure, ofigure, other_trans, other_figure):
        # pfigure is the copy of ofigure, other_trans and other_figure to determine angle vs. reflection
        if MY_DEBUG:
            print "Applying Trans: %s to Figure: "%trans
            print_figure(pfigure)

        # no changes, return figure back
        changes=ctr=0
        for c in trans['changes']:
            if MY_DEBUG==1:
                print "C is %s, ctr %s"%(c, ctr)
            if(len(c)>0):
                this_change=c
                changes=changes+1
                if MY_DEBUG:
                    print "! Processing change set (%s) caught from trans:"%str(ctr)
                    print (this_change)
                cctr=0
                for change in this_change :
                    if MY_DEBUG:
                        print "Change is %s, ctr %s"%(change, cctr)
                        print "! Processing set %s, change %s: "%(str(ctr),str(cctr))
                        print (change)
                    # select the changed figure key from original
                    ofig_keys= ofigure.objects.keys()
                    # grab from processing figure
                    if MY_DEBUG:
                        print "! to compare and apply to this figure (BEFORE)"
                        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                        print_figure(pfigure)
                    action=change[0]
                    if action=="add":
                        if MY_DEBUG:
                            print " ! ADDED "
                        to_add=change[1]
                        pfigure.objects[to_add.name]=to_add
                    elif action=="remove":
                        if MY_DEBUG:
                            print " ! REMOVED"
                        match_costs={}
                        obj_to_remove=change[1]
                        lowest_cost=float("inf")
                        selection=-1
                        if MY_DEBUG:
                            print "Object to remove..."
                            print (obj_to_remove)
                        for o in pfigure.objects:
                            to_change, cost = self.associate_objects(pfigure.objects[o],obj_to_remove)
                            if MY_DEBUG:
                                print "Associated objects CHANGE %s COST %s"%(to_change, cost)
                            match_costs[o]=cost
                            if cost<lowest_cost:
                                lowest_cost=cost
                                selection=o
                        if MY_DEBUG:
                            print "RESULT COSTS (selection %s, cost %s)"%(selection,str(lowest_cost))
                        if selection!=-1:
                            del pfigure.objects[selection]
                            if MY_DEBUG:
                                print "FOUND - removed"
                        else:
                            if MY_DEBUG:
                                print "NOT found, nothing removed"
                    else:
                        if MY_DEBUG:
                            print " !!! CHANGE ATTRIBUTE"
                            print ofig_keys, ctr
                            print "counter %s"%str(len(ofig_keys))
                        if len(ofig_keys)>ctr:
                            reflection = 0
                            if MY_DEBUG:
                                print " !! OK to change -- let's first check if reflection is applicable"

                            if change[0]=="angle":
                                new_value=change[2]
                                old_value=change[1]
                                diff=abs(int(new_value)-int(old_value))
                                print "Diff val is %s"%diff
                                #diff between other
                                print_figure(pfigure)
                                print_figure(ofigure)
                                print_figure(other_figure)
                                print ofig_keys
                                other_fig_keys= other_figure.objects.keys()
                                print ("Other fig keys %s"%other_fig_keys)
                                print (other_trans)
                                print trans
                                print "Here"
                                this_index=trans['best_permutation'][ctr]
                                print "ctr is %s index is: %s"%(ctr,this_index)
                                other_index=other_trans['best_permutation'][ctr]
                                other_change=other_trans['changes'][ctr]
                                print "other ctr is %s index is: %s"%(ctr,this_index)
                                odiff=-1
                                for oc in other_change:
                                    print "OC is %s"%str(oc)
                                    ochange=oc[0]
                                    if ochange=="angle":
                                        odiff=abs(int(oc[2])-int(oc[1]))
                                print "odiff is %s"%odiff
                                if (odiff==90 and diff==270) or (odiff==270 and diff==90):
                                    reflection=1
                            self.apply_attribute_to_object(pfigure.objects[ofig_keys[ctr]],change,reflection)
                        else:
                            if MY_DEBUG:
                                print " !! NOT changing"
                    if MY_DEBUG:
                        print "! has been applied (AFTER)"
                        print_figure(pfigure)
                    cctr=cctr+1
            ctr=ctr+1
        if MY_DEBUG:
            print "Number of changes: %s"%str(changes)
        return pfigure


