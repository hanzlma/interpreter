import sys
from mhscr_interpreter.runner_cli import CLIRunner
from mhscr_interpreter.runner_wholefile import WholefileRunner


def Run():
    if len(sys.argv) <2:
        CLIRunner().Run()
    if len(sys.argv) == 2:
        WholefileRunner(sys.argv[1]).Run()

