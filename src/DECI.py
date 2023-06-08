import os
import time

class Scenario:
    txt: str = ""

    def __init__(self, txt: str) -> None:
        self.txt = txt

class Situation:
    txt: str = []
    scenarios: int = []
    next_situation: int = []

    def __init__(self, txt: str, scenarios: int, next_situation: int) -> None:
        self.txt = txt
        self.scenarios = scenarios
        self.next_situation = next_situation

class Story:
    scenarios: Scenario = []
    situations: Situation = []
    imgs: str = []
    entry_point: int = 0

    def __init__(self, scenarios: Scenario, situations: Situation, imgs: str, entry_point: int = 0) -> None:
        self.scenarios = scenarios
        self.situations = situations
        self.imgs = imgs
        self.entry_point = entry_point

class Game:
    def __init__(self, story: Story) -> None:
        self.__scenarios: Scenario = []
        self.__situations: Situation = []
        self.__entry_point: int = 0
        self.__next_situation: int = self.__entry_point
        self.__sleep_time: float = 0.5

        self.__init_from_story(story)

    def start(self):
        while self.__next_situation != -1:
            if self.__next_situation == "~":
                self.__play_situation(self.__entry_point)
            else:
                self.__play_situation(self.__next_situation)

    def __play_situation(self, situation: int):
        self.__clear_cmd()

        for i in self.__situations[situation].txt:
            self.__slow_print(i)

        if len(self.__situations[situation].scenarios) == 0: 
            self.__next_situation = self.__situations[situation].next_situation[0]
            self.__slow_print()
            input("Press enter to continue: ")
            self.__clear_cmd()
            return
        
        self.__slow_print()
        self.__slow_print("Please choose one option: ")
        self.__slow_print()

        for i in range(len(self.__situations[situation].scenarios)):
            self.__slow_print(f"{i+1}) {self.__scenarios[self.__situations[situation].scenarios[i]].txt}")
        
        self.__slow_print()
        inputString = input("-> ")

        try:
            choosenOne = int(inputString)
        except ValueError:
            self.__clear_cmd()
            self.__slow_print("####################################################")
            self.__slow_print(f"Invalid input {inputString} is not a valid input the only valid input is integer numbers (0-9)")
            self.__slow_print("####################################################")
            input("Press enter to continue: ")
            self.__play_situation(situation)

        if(choosenOne > len(self.__situations[situation].scenarios) or choosenOne < 1):
            self.__clear_cmd()
            self.__slow_print("####################################################")
            self.__slow_print(f"Invalid input input ranges from ({1}, {len(self.__situations[situation].scenarios)})")
            self.__slow_print("####################################################")
            input("Press enter to continue: ")
            self.__play_situation(situation)

        self.__next_situation = self.__situations[situation].next_situation[choosenOne-1]
        self.__enable_clear = True
        self.__clear_cmd()
        
    def __clear_cmd(self):
        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")

    def __slow_print(self, txt: str = ""):
        print(txt)
        time.sleep(self.__sleep_time)

    def __init_from_story(self, story: Story):
        self.__scenarios = story.scenarios
        self.__situations = story.situations
        self.__entry_point = story.entry_point
        self.__next_situation = self.__entry_point

    def set_sleep_time(self, time: float):
        self.__sleep_time = time

#TODO: add parser errors
def load_story(path: str):
    story = Story([], [], [], 0)

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
        elif line[:5] == "imgs:":
            line = lines[i]
            line = line.rstrip()
            i += 1
            while line[:4] != "end:":
                story.imgs.append(line)
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

                situation.txt.append(line)
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