import sys
from runner_cli import CLIRunner
from runner_wholefile import WholefileRunner

if len(sys.argv) <2:
    CLIRunner().Run()
if len(sys.argv) == 2:
    WholefileRunner(sys.argv[1]).Run()
