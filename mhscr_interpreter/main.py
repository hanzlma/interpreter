import sys
import re
from mhscr_interpreter.runner_cli import CLIRunner
from mhscr_interpreter.runner_wholefile import WholefileRunner


def Run():
    if len(sys.argv) <2:
        CLIRunner().Run()
    elif len(sys.argv) == 2:
        if re.search(".*\.(txt|mhscr)$", sys.argv[1]) is None:
            print("Wrong argument for mhscr inerpreter. Allowed filetypes are .txt and .mhscr\nCorrect format: mshcr [filepath]")
            return
        WholefileRunner(sys.argv[1]).Run()
    else:
        print("Wrong arguments for mhscr interpreter.\nCorrect format: mshcr [filepath]")

if __name__ == "__main__":
    Run()