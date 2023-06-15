import DECI

game = DECI.Game(DECI.load_story("./res/stories/rescue.txt"))

game.set_sleep_time(0)
game.start()