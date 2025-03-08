# mhscr interpreter
mhscr is a small scripting language.

## Functionalities
- Static and dynamic typing
- Branching
- Cycles
- Functions
- Printing and Inputting

## Code example - Fibonnaci sequence function
```mhscr
fn fib int to
if to == 0
return 0
endif
if to == 1
return 1
endif
int last_last = 0
int last = 1
int result = 0
for int i = 1; i < to; i = i + 1
result = last_last + last
last_last = last
last = result
endfor
return result
endfn
```