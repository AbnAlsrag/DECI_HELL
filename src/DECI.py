# GUI IS AN DEPRECATED IDIA DON'T BOTHER LOOKING AT IT
import os
import time
import random

#Containre class for possible options
class Scenario:
    txt: str = ""

    def __init__(self, txt: str) -> None:
        self.txt = txt

#Containre class for situatuions
class Situation:
    txt: str = []
    scenarios: int = []
    next_situation: int = []

    def __init__(self, txt: str, scenarios: int, next_situation: int) -> None:
        self.txt = txt
        self.scenarios = scenarios
        self.next_situation = next_situation

#Containre class for the game
class Story:
    scenarios: Scenario = []
    situations: Situation = []
    entry_point: int = 0

    def __init__(self, scenarios: Scenario, situations: Situation, entry_point: int = 0) -> None:
        self.scenarios = scenarios
        self.situations = situations
        self.entry_point = entry_point

#The class that runs the story in cmd or graphical window
class Game:
    def __init__(self, story: Story):
        self.__scenarios: Scenario = []
        self.__situations: Situation = []
        self.__entry_point: int = 0
        self.__next_situation: int = self.__entry_point
        self.__sleep_time: float = 0.5

        self.__init_from_story(story)

    #Method that is called to start the running of the story
    def start(self):
        while self.__next_situation != -1:
            if self.__next_situation == "~":
                self.__play_situation(self.__entry_point)
            else:
                self.__play_situation(self.__next_situation)

    #Method that runs specific situation specified by situation parameter
    def __play_situation(self, situation: int):
        self.__clear_window()

        for i in self.__situations[situation].txt:
            self.__slow_print(i)

        if len(self.__situations[situation].scenarios) == 0: 
            self.__next_situation = self.__situations[situation].next_situation[0]
            self.__slow_print()
            self.__pause()
            self.__clear_window()
            return
        
        self.__slow_print()
        self.__slow_print("Please choose one option: ")
        self.__slow_print()

        for i in range(len(self.__situations[situation].scenarios)):
            self.__slow_print(f"{i+1}) {self.__scenarios[self.__situations[situation].scenarios[i]].txt}")
        
        self.__slow_print()
        inputString = self.__input("> ")

        try:
            choosenOne = int(inputString)

            if choosenOne > len(self.__situations[situation].scenarios) or choosenOne < 1:
                self.__clear_window()
                self.__slow_print("####################################################")
                self.__slow_print(f"Invalid input ({choosenOne}) input ranges from ({1}, {len(self.__situations[situation].scenarios)})")
                self.__slow_print("####################################################")
                self.__slow_print()
                self.__pause()
                return
        except ValueError:
            self.__clear_window()
            self.__slow_print("####################################################")
            self.__slow_print(f"Invalid input {inputString} is not a valid input the only valid input is integer numbers (0-9)")
            self.__slow_print("####################################################")
            self.__slow_print()
            self.__pause()
            return

        self.__next_situation = self.__situations[situation].next_situation[choosenOne-1]
        self.__clear_window()
        
    #Method that clears the graphical window or cmd for new situation to run
    def __clear_window(self):
        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")

    #Method that prints with delay to cmd or graphical window
    def __slow_print(self, txt: str = ""):
        time.sleep(self.__sleep_time)
        print(txt)

    def __input(self, txt: str = ""):
        time.sleep(self.__sleep_time)
        return input(txt)


    #Method that pauses the game until the player presses (Enter) key
    def __pause(self):
        time.sleep(self.__sleep_time)
        self.__input("Press enter to continue: ")

    #Method that intialize the class from story object
    def __init_from_story(self, story: Story):
        self.__scenarios = story.scenarios
        self.__situations = story.situations
        self.__entry_point = story.entry_point
        self.__next_situation = self.__entry_point

    #Method that set the slowdown of (__slow_print) and (__pause) and (__input) funcs
    def set_sleep_time(self, __time: float):
        self.__sleep_time = __time

#TODO: add parser errors
#Function that creats story object from txt file that has all the needed data
# Bad thing that i don't like that the randomness (^&^) keyword only works when the app restarts and i am to lazy to fix it there for it is a feature from now and on
def load_story(path: str):
    story = Story([], [], 0)

    current_situation: int = 0
    file = open(path)

    lines = file.readlines()
    line = lines[0]
    for i in range(len(lines)):
        if line[:10] == "scenarios:":
            line = lines[i]
            line = line.rstrip()
            while line[:4] != "end:":
               story.scenarios.append(Scenario(line))
               line = lines[i]
               line = line.rstrip()
               i += 1

            line = lines[i]
            line = line.rstrip()
        elif line[:6] == "entry:":
            story.entry_point = current_situation
            line = lines[i]
            line = line.rstrip()
        elif line[:10] == "situation:":
            current_situation += 1
            situation = Situation([], [], [])
            
            while line != "action:":
                line = lines[i]
                line = line.rstrip()

                if line == "action:":
                    break
                
                txt: str = ""
                for x in range(len(line)):
                    tmp: str = ""
                    tmp = line[x]

                    if x+2 < len(line):
                        if line[x] == "^" and line[x+1] == "&" and line[x+2] == "^":
                            x += 4

                            if x >= len(line):
                                print("ERROR: You should not use (^&^) and not put any thing after it")
                                breakpoint()

                            rand = random.randint(0, 1)
                            if rand == 0:
                                break
                            else:
                                txt = ""
                                
                                while x < len(line):
                                    txt += line[x]
                                    x += 1
                                
                                break
                    txt += tmp

                situation.txt.append(txt)

                i += 1

                while lines[i] == "\n":
                    i += 1

            i += 1
            line = lines[i]
            line = line.rstrip()
            
            if line[0] != "*":
                for c in line:
                    try:
                        situation.scenarios.append(int(c))
                    except ValueError:
                        pass

                i += 1
                line = lines[i]
                line = line.rstrip()

                for c in line:
                    if c == "~":
                        situation.next_situation.append("~")
                    elif c == "!":
                        situation.next_situation.append(-1)
                    else:
                        try:
                            situation.next_situation.append(int(c)-1)
                        except ValueError:
                            pass
            else:
                i += 1
                line = lines[i]
                line = line.rstrip()
                if line[0] == "~":
                    situation.next_situation.append("~")
                elif line[0] == "!":
                    situation.next_situation.append(-1)
                else:
                    try:
                        situation.next_situation.append(int(line[0])-1)
                    except ValueError:
                        pass

            story.situations.append(situation)
            line = lines[i]
            line = line.rstrip()
        elif line == "\n":
               line = lines[i]
               line = line.rstrip()
        else:
            line = lines[i]
            line = line.rstrip()

    file.close()

    return story