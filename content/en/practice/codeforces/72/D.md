---
title: "CF 72D - Perse-script"
description: "We are given a single expression written in a tiny string-processing language. Every value in this language is a string surrounded by quotation marks, and the only allowed operations are four built-in functions: concat(x,y) joins two strings. reverse(x) reverses a string."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "expression-parsing"]
categories: ["algorithms"]
codeforces_contest: 72
codeforces_index: "D"
codeforces_contest_name: "Unknown Language Round 2"
rating: 2300
weight: 72
solve_time_s: 148
verified: false
draft: false
---

[CF 72D - Perse-script](https://codeforces.com/problemset/problem/72/D)

**Rating:** 2300  
**Tags:** *special, expression parsing  
**Solve time:** 2m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a single expression written in a tiny string-processing language. Every value in this language is a string surrounded by quotation marks, and the only allowed operations are four built-in functions:

`concat(x,y)` joins two strings.

`reverse(x)` reverses a string.

`substr(x,a,b)` extracts characters from index `a` to `b`, inclusive.

`substr(x,a,b,c)` extracts every `c`-th character from `a` to `b`.

Function names are case-insensitive, so `ReVeRsE` and `reverse` mean the same thing. Expressions can be nested arbitrarily, which means arguments themselves may be complete expressions.

The task is simply to evaluate the whole expression and print the resulting string, still surrounded by quotation marks.

The input length is at most `10^3`, which is small. Even an `O(n^2)` parser would fit comfortably. The output length can reach `10^4`, so repeated string copying inside deeply nested concatenations deserves attention, although Python handles this size without trouble.

The main challenge is not performance but parsing correctly. The grammar mixes strings, integers, commas, parentheses, and nested function calls. A parser that only scans greedily or splits by commas will fail immediately because commas may appear inside nested subexpressions.

One easy mistake is mishandling nested calls.

Input:

```
concat(reverse("abc"),"d")
```

Correct output:

```
"cbad"
```

A naive parser that splits arguments by the first comma would incorrectly split inside nested parentheses.

Another subtle case is the stepped version of `substr`.

Input:

```
substr("abcdefg",2,7,2)
```

Correct output:

```
"bdf"
```

The indices are 1-based and inclusive. Forgetting either detail produces `"ceg"` or `"bdfg"`.

Case-insensitive function names are another trap.

Input:

```
ReVeRsE("abc")
```

Correct output:

```
"cba"
```

Comparing names without normalizing case incorrectly rejects valid expressions.

The final common bug is mixing Python slicing rules with the statement rules.

Input:

```
substr("abcdef",1,6)
```

Correct output:

```
"abcdef"
```

Python slicing excludes the right endpoint, while this language includes it.

## Approaches

The brute-force idea is straightforward: recursively evaluate the expression exactly as written.

If we encounter a quoted string, return it directly.

If we encounter a function call, recursively evaluate all arguments, apply the corresponding operation, and return the result.

This already works efficiently enough because the entire input is only `1000` characters long. Even if every recursive call scans part of the expression again, the total amount of work remains manageable.

The real difficulty is parsing arguments correctly. A naive implementation might try to split the inside of `concat(a,b)` using `s.split(',')`. That fails for nested expressions like:

```
concat(reverse("abc"),substr("xyz",1,2))
```

The comma inside nested parentheses must not split the top-level arguments.

The key observation is that this language has a very regular recursive structure. Every expression is either:

```
"literal"
```

or:

```
function(arg1,arg2,...)
```

This naturally suggests recursive descent parsing. Instead of trying to preprocess the whole expression, we keep a pointer into the string and parse one complete expression at a time.

When we see `"`, we parse a literal string.

Otherwise we read a function name, consume `(`, recursively parse arguments separated by commas, then consume `)`.

Because each character is processed only a constant number of times, the parser runs in linear time relative to the input size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with naive splitting | O(n²) | O(n) | Error-prone |
| Recursive descent parser | O(n + answer length) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the entire input expression as a string.
2. Maintain a global pointer `pos` representing the current parsing position.
3. Create a recursive function `parse()` that parses exactly one complete expression starting at `pos`.
4. If the current character is `"`, parse a string literal.

Move past the opening quote, collect characters until the closing quote, then return the extracted string.
5. Otherwise parse a function call.

Read consecutive alphabetic characters to obtain the function name, then convert it to lowercase so case differences disappear.
6. Consume the opening parenthesis `(`.
7. Repeatedly parse arguments recursively.

After parsing one argument:

If the next character is `,`, continue parsing another argument.

If the next character is `)`, stop.
8. Apply the corresponding operation based on the function name.

For `concat`, join two strings.

For `reverse`, reverse the string using slicing.

For `substr(x,a,b)`, extract characters from `a-1` through `b`.

For `substr(x,a,b,c)`, extract characters from `a-1` through `b` with step `c`.
9. Return the computed result string to the caller.
10. After parsing the top-level expression, print the final string surrounded by quotation marks.

### Why it works

The parser always maintains one invariant: `parse()` consumes exactly one valid expression and leaves `pos` immediately after that expression.

String literals are self-contained between matching quotes, so parsing them is unambiguous.

Function calls are also unambiguous because parentheses determine nesting depth. Recursive calls fully consume nested expressions before the outer parser looks for commas or closing parentheses. That guarantees commas inside nested calls never interfere with outer argument parsing.

Since every expression is evaluated immediately after parsing its arguments, the returned value is exactly the semantic value defined by the language rules.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
pos = 0

def parse_number():
    global pos
    sign = 1

    if s[pos] == '-':
        sign = -1
        pos += 1

    val = 0
    while pos < len(s) and s[pos].isdigit():
        val = val * 10 + ord(s[pos]) - ord('0')
        pos += 1

    return sign * val

def parse():
    global pos

    if s[pos] == '"':
        pos += 1
        start = pos

        while s[pos] != '"':
            pos += 1

        res = s[start:pos]
        pos += 1
        return res

    start = pos

    while pos < len(s) and s[pos].isalpha():
        pos += 1

    func = s[start:pos].lower()

    pos += 1  # '('

    args = []

    while True:
        if s[pos] == '"':
            args.append(parse())

        elif s[pos].isalpha():
            args.append(parse())

        else:
            args.append(parse_number())

        if s[pos] == ',':
            pos += 1
        else:
            break

    pos += 1  # ')'

    if func == "concat":
        return args[0] + args[1]

    if func == "reverse":
        return args[0][::-1]

    if func == "substr":
        x = args[0]
        a = args[1]
        b = args[2]

        if len(args) == 3:
            return x[a - 1:b]

        c = args[3]
        return x[a - 1:b:c]

    return ""

ans = parse()
print(f'"{ans}"')
```

The parser revolves around the global pointer `pos`. Every helper function advances this pointer as it consumes input.

`parse_number()` handles integer arguments used by `substr`. The statement allows negative integers syntactically, so supporting an optional minus sign keeps the parser robust even though valid indices are positive in official tests.

The main `parse()` function first distinguishes literals from function calls. A leading quote means the expression is a raw string. Otherwise the parser reads alphabetic characters to obtain the function name.

Arguments are parsed recursively. This is the crucial part of the solution. When parsing:

```
concat(reverse("abc"),"d")
```

the recursive call for `reverse("abc")` consumes the entire nested expression before control returns to the outer `concat`.

The implementation checks the next character to decide whether the next argument is a string/function expression or an integer. Integer arguments only appear inside `substr`, so this distinction is enough.

The substring logic carefully converts from 1-based inclusive indexing to Python slicing. For:

```
substr(x,a,b)
```

the correct Python slice is:

```
x[a - 1:b]
```

because Python excludes the right endpoint automatically.

The stepped version uses:

```
x[a - 1:b:c]
```

which also preserves the inclusive behavior correctly because Python stops before index `b`, and the original inclusive endpoint corresponds exactly to Python's exclusive upper bound.

## Worked Examples

### Example 1

Input:

```
"HelloWorld"
```

| Step | pos | Current token | Returned value |
| --- | --- | --- | --- |
| Start parse | 0 | `"` | parse literal |
| Read string | 1..10 | `HelloWorld` | `HelloWorld` |

Output:

```
"HelloWorld"
```

This example demonstrates the base case of the recursion. No function parsing is needed, so the parser directly extracts the literal contents between quotes.

### Example 2

Input:

```
concat(reverse("abc"),substr("uvwxyz",2,5,2))
```

| Step | pos | Current token | Returned value |
| --- | --- | --- | --- |
| Parse function | 0 | `concat` | pending |
| Parse argument 1 | 7 | `reverse` | pending |
| Parse literal | 15 | `"abc"` | `abc` |
| Apply reverse | 20 |  | `cba` |
| Parse argument 2 | 22 | `substr` | pending |
| Parse literal | 29 | `"uvwxyz"` | `uvwxyz` |
| Read integers |  | `2,5,2` |  |
| Apply substr |  |  | `vx` |
| Apply concat |  |  | `cbavx` |

Output:

```
"cbavx"
```

This trace shows why recursive parsing works cleanly. Each nested call completely resolves before the outer function resumes argument parsing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + answer length) | Each input character is parsed a constant number of times |
| Space | O(n) | Recursive call stack and temporary strings |

The input length is at most `1000`, so recursion depth and parser overhead remain tiny. Even the largest possible output comfortably fits inside memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    import sys
    input = sys.stdin.readline

    s = input().strip()
    pos = 0

    def parse_number():
        nonlocal pos

        sign = 1

        if s[pos] == '-':
            sign = -1
            pos += 1

        val = 0

        while pos < len(s) and s[pos].isdigit():
            val = val * 10 + ord(s[pos]) - ord('0')
            pos += 1

        return sign * val

    def parse():
        nonlocal pos

        if s[pos] == '"':
            pos += 1
            start = pos

            while s[pos] != '"':
                pos += 1

            res = s[start:pos]
            pos += 1
            return res

        start = pos

        while pos < len(s) and s[pos].isalpha():
            pos += 1

        func = s[start:pos].lower()

        pos += 1

        args = []

        while True:
            if s[pos] == '"' or s[pos].isalpha():
                args.append(parse())
            else:
                args.append(parse_number())

            if s[pos] == ',':
                pos += 1
            else:
                break

        pos += 1

        if func == "concat":
            return args[0] + args[1]

        if func == "reverse":
            return args[0][::-1]

        x = args[0]
        a = args[1]
        b = args[2]

        if len(args) == 3:
            return x[a - 1:b]

        return x[a - 1:b:args[3]]

    ans = parse()
    print(f'"{ans}"')

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run('"HelloWorld"\n') == '"HelloWorld"', "sample 1"

# custom cases
assert run('reverse("abcd")\n') == '"dcba"', "basic reverse"

assert run('substr("abcdef",1,6)\n') == '"abcdef"', "inclusive bounds"

assert run('substr("abcdefg",2,7,2)\n') == '"bdf"', "step slicing"

assert run('concat(reverse("abc"),"xyz")\n') == '"cbaxyz"', "nested parsing"

assert run('ReVeRsE(concat("ab","cd"))\n') == '"dcba"', "case-insensitive functions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `reverse("abcd")` | `"dcba"` | Basic unary function |
| `substr("abcdef",1,6)` | `"abcdef"` | Inclusive indexing |
| `substr("abcdefg",2,7,2)` | `"bdf"` | Step-based slicing |
| `concat(reverse("abc"),"xyz")` | `"cbaxyz"` | Nested recursion |
| `ReVeRsE(concat("ab","cd"))` | `"dcba"` | Case-insensitive parsing |

## Edge Cases

Consider nested expressions with commas inside subcalls.

Input:

```
concat(reverse("abc"),substr("uvwxyz",2,4))
```

The parser begins reading `concat`. While parsing the first argument, it recursively consumes the entire substring:

```
reverse("abc")
```

Only after the recursive call finishes does the outer parser encounter the separating comma. The result becomes:

```
"cbavwx"
```

This confirms commas inside nested expressions never confuse the outer level.

Now consider inclusive substring boundaries.

Input:

```
substr("abcdef",1,6)
```

The algorithm converts this into:

```
x[0:6]
```

which correctly returns all characters. Using `x[0:5]` would incorrectly drop the final `f`.

Now consider stepped extraction.

Input:

```
substr("abcdefgh",1,8,3)
```

The parser extracts:

```
x[0:8:3]
```

producing:

```
"adg"
```

The stopping condition matches the statement because Python slicing already excludes the upper endpoint.

Finally consider case-insensitive function names.

Input:

```
SuBsTr("abcdef",2,5)
```

The parser lowercases the name immediately after reading it, transforming `SuBsTr` into `substr`. The evaluation proceeds normally and returns:

```
"bcde"
```

Without normalization, valid expressions would fail unpredictably depending on capitalization.
