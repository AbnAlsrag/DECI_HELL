#WIP
#DEPRECATED
import GUI
import threading

app = GUI.App()

def graphic_thread():
    pass

def init_gui(title: str = "", width: int = 600, height: int = 600):
    thread = threading.Thread(target=graphic_thread)
    thread.start()

def gui_print(txt: str = ""):
    pass

def gui_input(txt: str = ""):
    pass