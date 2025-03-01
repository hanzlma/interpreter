import sys
import re
from mhscr_interpreter.runner_cli import CLIRunner
from mhscr_interpreter.runner_wholefile import WholefileRunner


def Run():
    if len(sys.argv) <2:
        CLIRunner().Run()
    elif len(sys.argv) == 2:
        if re.search(r".*\.(txt|mhscr)$", sys.argv[1]) is None:
            print("Wrong argument for mhscr inerpreter. Allowed filetypes are .txt and .mhscr\nCorrect format: mshcr [filepath]")
            return
        WholefileRunner(sys.argv[1]).Run()
    else:
        print("Wrong arguments for mhscr interpreter.\nCorrect format: mshcr [filepath]")

def IDE_Run():
    WholefileRunner("temp.txt").Run()
def Interpreter_Program_Run():
    argument: str = input("For file interpretation, enter a filepath\nFor CLI interpreter, press Enter\n> ")
    if argument == "":
        CLIRunner().Run()
    else:
        if re.search(r".*\.(txt|mhscr)$", argument) is None:
            print("Wrong argument for mhscr inerpreter. Allowed filetypes are .txt and .mhscr\nCorrect format: mshcr [filepath]")
            return
        WholefileRunner(argument).Run()
        input("\nProgram output ended.\nPress enter to exit.")
if __name__ == "__main__":
    Interpreter_Program_Run()