import os
import time

class Scenario:
    def __init__(self, txt: str) -> None:
        self.txt = txt

class Situation:
    def __init__(self, txt: str, scenarios: int, next_situation: int) -> None:
        self.txt = txt
        self.scenarios = scenarios
        self.next_situation = next_situation

class Game:
    def __init__(self) -> None:
        self.__scenarios: Scenario = []
        self.__situations: Situation = []
        self.__next_situation: int = 0
        self.__sleep_time: float = 0.5

    def start(self):
        while self.__next_situation != None:
            self.__play_situation(self.__next_situation)

    def __play_situation(self, situation: int):
        self.__clear_cmd()

        for i in self.__situations[situation].txt:
            self.__slow_print(i)
        
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
        self.__clear_cmd()
        
    def __clear_cmd(self):
        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")

    def __slow_print(self, txt: str = ""):
        print(txt)
        time.sleep(self.__sleep_time)

    def add_scenario(self, scenario: Scenario):
        self.__scenarios.append(scenario)
    
    def add_situation(self, situation: Situation):
        self.__situations.append(situation)

    def set_sleep_time(self, time: float):
        self.__sleep_time = time