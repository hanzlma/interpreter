import re

from .expressions import Expression
from mhscr_interpreter.datatypes import String, Let, GetDatatypeDynamically
from mhscr_interpreter.errors import MHscr_TypeError, MHscr_ValueError
from mhscr_interpreter.variable import Variable


class InputExp(Expression):
    """
    Input expression.
    Structure:
        input <variable to assign input to>
    Example:
        input test //assigns input to variable 'test'

    """

    cli: bool
    inp: str
    name: str | None
    msg: str | None

    def __init__(self, runner, inp: str, cli: bool) -> None:
        super().__init__(runner, inp, cli)
        self.name = None
        self.msg = None

        self.prepareArguments()

    def prepareArguments(self) -> None:
        args: list[str] = [
            match[0] or match[1]
            for match in re.findall(
                r"(\b[a-zA-Z]*\b)|(['|\"][^'\"]*['|\"])", self.inp.replace("input ", "")
            )
        ]
        while args.count("") > 0:
            args.remove("")
        if len(args) == 0:
            return
        if len(args) == 1:
            try:
                self.msg = String(self.inp.replace("input ", "")).value
                return
            except MHscr_ValueError:
                pass
            if args[0] in self.runner.keywords.dictionary.keys():
                self.name = args[0]
            else:
                raise MHscr_ValueError(
                    "Variable not initialized",
                    line=self.runner.expressions.index(self) if not self.cli else None,
                )
        elif len(args) == 2:
            if args[0] in self.runner.keywords.dictionary.keys():
                self.name = args[0]
                self.msg = String(args[1]).value
            elif args[1] in self.runner.keywords.dictionary.keys():
                self.name = args[1]
                self.msg = String(args[0]).value
            else:
                raise MHscr_ValueError(
                    "Variable not initialized",
                    line=self.runner.expressions.index(self) if not self.cli else None,
                )
        else:
            raise MHscr_ValueError(
                "Unexpected argument count",
                line=self.runner.expressions.index(self) if not self.cli else None,
            )

    def execute(self, /, *, functionCall=False) -> None:
        super().execute(functionCall=functionCall)

        value = input(
            f"{'[input]> ' if self.cli else ''}{self.msg if self.msg is not None else ''}"
        )
        if self.name:
            value = GetDatatypeDynamically(self.runner, value)
            if (
                not isinstance(value, self.runner.variables[self.name].datatype)
                and self.runner.variables[self.name].datatype is not Let
            ):
                raise MHscr_TypeError(
                    f"Variable of type {self.runner.variables[self.name].datatype} cannot be assigned value of type {type(value)}.",
                    line=self.runner.expressions.index(self) if not self.cli else None,
                )
            self.runner.variables[self.name] = Variable(self.name, type(value), value)
