#To run Jarvis

import multiprocessing  # Allows running multiple processes in parallel, useful for tasks like listening and responding simultaneously
import subprocess  # Lets you run external commands or programs from Python (e.g., opening apps, executing scripts)


def startJarvis():
    #code for process 1
    print("Process 1 is running.")
    from main import start
    start()

#  To run hotword
def listenHotword():
    #code for process 2
    print("Process 2 is running.")
    from engine.features import hotword
    hotword()

  # Start both processes
if __name__ == '__main__':
        p1 = multiprocessing.Process(target=startJarvis)
        p2 = multiprocessing.Process(target=listenHotword)
        p1.start()
        p2.start()
        p1.join() 

        if p2.is_alive():
            p2.terminate()
            p2.join()

        print("system stop")