import DECI
import random

game = DECI.Game(DECI.load_story("./res/stories/story.txt"))

game.set_sleep_time(0)
game.start()