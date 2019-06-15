import sys

#initialize the general status
STATUS_g = {"BATTERY_LEVEL": 100,
              "SPOT": True,
              "GENERAL": True,
              "DUSTY_SPOT": True,
              "COUNT": 0,
              "DOING_NOTHING": False
              }

#state the results
class TaskStatus():
    FAILURE = 0
    SUCCESS = 1
    RUNNING = 2

#initialize the input later
class Task(object):
    def __init__(self, children = None, time = None):
        if children == None:
            self.children = list()
        else:
            self.children = children
        self.time = time

    def add_child(self, child):
        self.children.append(child)

#initialize the Priority
class Priority(Task):
    def run(self):
        for child in self.children:
            status = child.run(self.children)
            if status != TaskStatus.FAILURE:
                return status
        return TaskStatus.FAILURE

#initialize the Sequence
class Sequence(Task):
    def run(self, children = None):
        for child in self.children:
            child.status = child.run(children)
            if child.status == TaskStatus.FAILURE:
                return child.status
            else:
                while child.status != TaskStatus.SUCCESS:
                    child.status = child.run()
        return TaskStatus.SUCCESS

#initialize the Selector
class Selector(Task):
    def run(self, children = None):
        for child in self.children:
            child.status = child.run(children)
            if child.status != TaskStatus.FAILURE:
                return child.status
        return TaskStatus.FAILURE

#counting the times
class Timer(Task):
    def __init__(self, children = None, mtime = None):
        super().__init__(children)
        self.time = mtime

    def run(self, children = None, mtime = None):
        print("cleaning is set up for: " + str(self.time) + " seconds")
        if STATUS_g['COUNT'] < self.time:
            STATUS_g['COUNT'] += 1
            print('Still Cleaning')
            status = TaskStatus.RUNNING
        else:
            print("SPOT cleaning is done!")
            STATUS_g['COUNT'] = 0
            STATUS_g['SPOT'] = False
            status = TaskStatus.SUCCESS
        return status

#try before fail
class Try(Task):
    def run(self, children = None):
        status = self.children.run(self)
        return  status + 1

#change status
class Neg(Task):
    def run(self, children = None):
        status = self.children.run(self)
        status = 1 - status
        return status

#check the batteru level
class CheckBattery():
    def run(self):
        if STATUS_g['BATTERY_LEVEL'] < 30:
            print('low battery level')
            return TaskStatus.SUCCESS
        else:
            print("high battery level")
            return TaskStatus.FAILURE

#Looking For Path
class FindHome():
    def run(self):
        print('Looking For Path')
        return TaskStatus.SUCCESS

#Going Home
class GoHome():
    def run(self):
        print('Going Home')
        return TaskStatus.SUCCESS

#Docked
class Dock():
    def run(self):
        print('Docked')
        return TaskStatus.SUCCESS

#Going to clean up spot
class Spot():
    def run(self):
        if STATUS_g['SPOT'] == True:
            print('Going to clean up spot')
            return TaskStatus.SUCCESS
        else:
            return TaskStatus.FAILURE

#Cleaning Spot
class CleanSpot():
    def run(self):
        print("Cleaning Spot")
        return TaskStatus.SUCCESS

#Spot is done!
class DoneSpot():
    def run(self):
        print("Spot is done! ")
        return TaskStatus.SUCCESS

#Going to do general tasks
class General():
    def run(self):
        if STATUS_g['GENERAL']:
            print('Going to do general tasks')
            return TaskStatus.SUCCESS
        else:
            return TaskStatus.FAILURE

#General tasks is Done
class DoneGeneral():
    def run(self):
        STATUS_g['GENERAL'] = False
        STATUS_g['COUNT'] = 0
        print('General tasks is Done')
        return TaskStatus.SUCCESS

#check whether there is a Dusty Spot
class DustySpot():
    def run(self):
        STATUS_g['DUSTY_SPOT'] = False
        print(STATUS_g['DUSTY_SPOT'])
        if STATUS_g['DUSTY_SPOT']:
            print('There is a dusty spot')
            return TaskStatus.SUCCESS
        else:
            print('No dusty spot')
            return TaskStatus.FAILURE

#check whether clearn
class Clean():
    def run(self):
        print('It is clean')
        STATUS_g['DOING_NOTHING'] = True
        return TaskStatus.FAILURE

class DoNothing():
    def run(self):
        print('Doing Nothing')

if __name__ == '__main__':

    # initialize the priority root child, eftmost sequence child, middle selector child
    Root = Priority()
    Left = Sequence()
    Mid = Selector()


    # initialize sub_sequence child under the middle child
    S_spot = Sequence()
    S_general = Sequence()
    S_done = Sequence()
    S_bat = Sequence()
    S_ds = Sequence()

    # initialize sub selector
    Se_clean = Selector()

    # add children to the root
    Root.add_child(Left)
    Root.add_child(Mid)
    Root.add_child(DoNothing)

    # add children to Left
    Left.add_child(CheckBattery)
    Left.add_child(FindHome)
    Left.add_child(GoHome)
    Left.add_child(Dock)

    # add children to Mid
    Mid.add_child(S_spot)
    Mid.add_child(S_general)

    # add children to spot
    S_spot.add_child(Spot)
    S_spot.add_child(Timer(CleanSpot, 20))
    S_spot.add_child(DoneSpot)

    # add children to general
    S_general.add_child(General)
    S_general.add_child(S_done)

    # add children to S_done
    S_done.add_child(Try(S_bat))
    S_done.add_child(DoneGeneral)

    # add children to S_bat
    S_bat.add_child(Neg(CheckBattery))
    S_bat.add_child(Se_clean)

    # add children to Se_clean
    Se_clean.add_child(S_ds)
    Se_clean.add_child(Clean)

    # add children to S_ds
    S_ds.add_child(DustySpot)
    S_ds.add_child(Timer(CleanSpot, 35))

    while(1):
        STATUS_g = {"BATTERY_LEVEL": 100,
                    "SPOT": True,
                    "GENERAL": True,
                    "DUSTY_SPOT": True,
                    "COUNT": 0,
                    "DOING_NOTHING": False
                    }

        print("Creating A new job now.")
        S = int(input("Spot status: input 0 for False, input 0 for True: "))
        if S == 0:
            STATUS_g['SPOT'] = False

        G = int(input("General status: input 0 for False, input 0 for True: "))
        if G == 0:
            STATUS_g['GENERAL'] = False


        count = 5
        for i in range(count):
            STATUS_g['BATTERY_LEVEL'] = int(input("BATTERY LEVEL is: "))
            print(STATUS_g)
            P = Root
            P.run()

            if (STATUS_g['DOING_NOTHING'] == True):
                print("\n")
                Finsh = str(input(
                    "Your room is shiny clean and everything is done, do you want to finish the job?\n(Y or N) N for No, Y for Yes: "))
                if Finsh.lower() == 'y':
                    sys.exit()
                else:
                    break