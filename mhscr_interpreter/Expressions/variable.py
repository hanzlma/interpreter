from .expressions import Expression, PrepareValue
from mhscr_interpreter.datatypes import String, Int, Float, Bool, Let
from mhscr_interpreter.errors import (
    MHscr_KeywordError,
    MHscr_OperatorError,
    MHscr_TypeError,
    MHscr_ValueError,
    MHscr_SyntaxError,
    getErrorLine,
)
from mhscr_interpreter.variable import Variable
from mhscr_interpreter.operators import SplitByOperators


class VariableExp(Expression):
    """ """

    cli: bool
    inp: str
    name: str
    argument: str
    arguments: list
    datatype: type
    var: String | Int | Float | Bool
    const: bool

    def __init__(self, runner, inp: str, cli: bool, const: bool = False) -> None:
        super().__init__(runner, inp, cli)
        self.const = const

        self.prepareArguments()

    def prepareArguments(self) -> None:
        try:
            parts: list[str] = self.inp.split(" ")
            self.__getDatatype(parts[0])
            self.name = parts[1]

            if parts[2] != "=":
                raise MHscr_OperatorError(
                    f"Unexpected value {parts[2]}",
                    line=getErrorLine(self.runner, self) if not self.cli else None,
                )
            self.argument = self.inp.replace(f"{parts[0]} {parts[1]} {parts[2]} ", "")
            self.arguments = SplitByOperators(self.argument)
        except IndexError:
            raise MHscr_SyntaxError(
                "Wrong arguments for Variable Expression",
                line=getErrorLine(self.runner, self) if not self.cli else None,
            )

    def execute(self, /, *, functionCall=False) -> None:
        super().execute(functionCall=functionCall)

        self.var = PrepareValue(self.runner, self.argument, self.arguments)
        if self.name in self.runner.variables:
            raise MHscr_ValueError(
                f"Variable '{self.name}' already initialized.",
                line=getErrorLine(self.runner, self) if not self.cli else None,
            )
        self.runner.variables[self.name] = Variable(
            self.name, self.datatype, self.var, self.const, local=functionCall
        )
        if not self.const:
            self.runner.keywords.dictionary[self.name] = VariableAssignmentExp

    def __getDatatype(self, datatypeName: str) -> None:
        dictionary: dict[str,] = {
            "string": String,
            "int": Int,
            "float": Float,
            "bool": Bool,
            "let": Let,
        }
        if self.const:
            dictionary.pop("let")
        try:
            self.datatype = dictionary[datatypeName]
        except KeyError:
            raise MHscr_KeywordError(
                f"Datatype {datatypeName} is not a valid datatype for a {'constant ' if self.const else ''}variable.",
                line=self.runner.expressions.index(self) if not self.cli else None,
            )

    def GetDatatype(runner, callerExpression, datatypeName: str):
        dictionary: dict[str,] = {
            "string": String,
            "int": Int,
            "float": Float,
            "bool": Bool,
            "let": Let,
        }

        try:
            return dictionary[datatypeName]
        except KeyError:
            from mhscr_interpreter.runner_cli import CLIRunner

            raise MHscr_KeywordError(
                f"Datatype {datatypeName} is not a valid datatype for a variable.",
                line=runner.expressions.index(callerExpression)
                if not isinstance(runner, CLIRunner)
                else None,
            )


class ConstantVariableExp(Expression):
    cli: bool
    inp: str

    def __init__(self, runner, inp: str, cli: bool) -> None:
        super().__init__(runner, inp.replace("const ", ""), cli)

    def execute(self, /, *, functionCall=False) -> None:
        super().execute(functionCall=functionCall)
        VariableExp(self.runner, self.inp, self.cli, True).execute(
            functionCall=functionCall
        )


class VariableAssignmentExp(Expression):
    cli: bool
    inp: str
    name: str
    argument: str
    arguments: list[str]
    var: String | Int | Float | Bool | Let

    def __init__(self, runner, inp: str, cli: bool) -> None:
        super().__init__(runner, inp, cli)

        self.prepareArguments()

    def execute(self, /, *, functionCall=False) -> None:
        super().execute(functionCall=functionCall)
        self.var = PrepareValue(self.runner, self.argument, self.arguments)
        if self.name not in self.runner.variables:
            raise MHscr_ValueError(
                f"Variable {self.name} not initialized",
                line=getErrorLine(self.runner, self) if not self.cli else None,
            )
        if type(self.var) is not type(
            self.runner.variables[self.name].var
        ) and not isinstance(self.runner.variables[self.name].var, Let):
            val = (
                f'"{self.var.value}"'
                if isinstance(self.var.value, str)
                else self.var.value
            )
            raise MHscr_TypeError(
                f"Type {self.runner.variables[self.name].datatype.__name__} cannot hold value {val}",
                line=self.runner.expressions.index(self) if not self.cli else None,
            )
        if self.runner.variables[self.name].const:
            raise MHscr_TypeError(
                "Cannot assign value to constant.",
                line=getErrorLine(self.runner, self) if not self.cli else None,
            )
        if isinstance(self.runner.variables[self.name].var, Let):
            self.var = Let(self.var)

        self.runner.variables[self.name] = Variable(
            self.name,
            self.runner.variables[self.name].datatype,
            self.var,
            False,
            local=self.runner.variables[self.name].local,
        )

    def prepareArguments(self) -> None:
        parts = self.inp.split(" ")
        self.name = parts[0]
        if parts[1] != "=":
            raise MHscr_OperatorError(
                f'Unexpected operator "{parts[1]}"',
                line=getErrorLine(self.runner, self) if not self.cli else None,
            )
        self.argument = self.inp.replace(f"{parts[0]} {parts[1]} ", "")
        self.arguments = SplitByOperators(self.argument)
