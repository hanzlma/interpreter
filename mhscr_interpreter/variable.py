from mhscr_interpreter.datatypes import String, Int, Float, Bool, Let
from mhscr_interpreter.errors import MHscr_TypeError


class Variable:
    name: str
    datatype: type
    var: String | Int | Float | Bool | Let
    const: bool

    def __init__(
        self,
        name: str,
        datatype: type,
        var: String | Int | Float | Bool,
        const: bool = False,
        *,
        local: bool = False,
    ) -> None:
        if datatype != Let and not isinstance(var, datatype):
            raise MHscr_TypeError(
                f"Wrong datatype {type(var)} to assign to variable of type {datatype}"
            )
        self.name = name
        self.datatype = datatype
        self.var = var if datatype != Let else Let(var)
        self.const = const
        self.local = local

    def getVariableAsDatatype(self) -> String | Int | Float | Bool | Let:
        return self.var

    def __str__(self) -> str:
        return f"[name: {self.name}, const: {self.const}, datatype: {self.datatype}, value: {self.var.value}, local: {self.local}]"
