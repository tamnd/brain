---
title: "CF 102419L - Cheating detection."
description: "We have two programs written in a tiny language with three kinds of statements: defining a variable, reading a variable, printing a variable, and assigning the sum of two variables to another variable."
date: "2026-08-12T20:38:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102419
codeforces_index: "L"
codeforces_contest_name: "SPC 2019"
rating: 0
weight: 102419
solve_time_s: 769
verified: true
draft: false
---

[CF 102419L - Cheating detection.](https://codeforces.com/problemset/problem/102419/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 12m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two programs written in a tiny language with three kinds of statements: defining a variable, reading a variable, printing a variable, and assigning the sum of two variables to another variable. A variable is defined at most once, and every variable is defined before it is used.

The two programs are considered equivalent if we can rename variables in the first program so that every statement becomes exactly the corresponding statement in the second program. The renaming is global, so if `a` is renamed to `x`, every occurrence of `a` must become `x`. The order of variables in `define` statements is part of the program, and the two operands of an addition are also positional. The expression `a=b+c` is not equivalent to `a=c+b` merely because addition is mathematically commutative.

The input contains the number of lines in the first program followed by those lines, then the number of lines in the second program followed by those lines. Each program has at most 1000 lines. This is small enough that a linear scan is easily fast enough, but it is also large enough that trying every possible correspondence between variables is completely impractical. With up to 1000 distinct variables, there can be as many as `1000!` possible renamings.

A first edge case is different program lengths. For example,

```
1
define a
2
define x
define y
```

must produce `NO`. A variable renaming cannot insert or remove statements, so programs with different numbers of lines can never match. A careless implementation that only compares the variables used in corresponding positions could overlook this immediately.

A second edge case is the order of operands. Consider

```
5
define a
define b
define c
a=b+c
print a
5
define x
define y
define z
x=z+y
print x
```

The correct output is `NO`. The only possible mapping from the three definitions is `a -> x`, `b -> y`, and `c -> z`. Under that mapping, `a=b+c` becomes `x=y+z`, not `x=z+y`. Treating `+` as mathematically commutative would incorrectly accept this pair.

A third edge case is that a variable mapping must be one-to-one. For example,

```
3
define a
define b
print a
3
define x
define x2
print x
```

is `NO`. The first program requires `a -> x`, while `b` must map to a different variable. If an implementation stores only a mapping from the first program's names to the second program's names and never checks the reverse direction, it can accidentally allow two different variables to map to the same name.

A final useful case is when the definition order differs. For example,

```
5
define a
define b
define c
a=b+c
print a
5
define x
define z
define y
x=y+z
print x
```

is `YES`, using `a -> x`, `b -> y`, and `c -> z`. The textual names themselves have no meaning. What matters is whether one consistent renaming makes the complete sequence of statements identical.

## Approaches

The most direct brute-force approach is to collect all variables in the first program and all variables in the second program, then try every bijection between the two sets. For each candidate bijection, we replace every variable in the first program and compare the resulting program with the second one. This is correct because the definition of cheating is exactly the existence of such a bijection.

The problem is the number of bijections. If there are `k` distinct variables, there are `k!` possible mappings. Testing one mapping requires `O(n+m)` work, so the total complexity is `O(k! (n+m))`. With `k=1000`, even the number of candidates is unimaginably large, long before the line comparison becomes relevant.

The key observation is that the program itself tells us which variables must correspond. We do not need to guess a complete mapping first. Whenever the first program mentions a variable in some statement position, the corresponding position in the second program tells us which variable it has to map to. Once that correspondence is established, every later occurrence of the same variable must use exactly the same target.

We can enforce this directly with two dictionaries. One dictionary maps variables from the first program to variables in the second. The reverse dictionary maps variables from the second program back to variables in the first. When a pair of variable occurrences is compared, either the mapping has not been seen before and we establish it, or it has already been established and must agree with the current pair. The reverse mapping prevents two different source variables from being assigned to the same target variable.

The brute-force method works because it explicitly searches all possible renamings, but fails because there are factorially many of them. The observation that each corresponding occurrence immediately constrains the only possible mapping lets us construct the required bijection while scanning the programs once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(k! (n+m))` | `O(k+n+m)` | Too slow |
| Bidirectional mapping | `O(n+m)` | `O(k+n+m)` | Accepted |

## Algorithm Walkthrough

1. Read both complete programs and immediately reject them if their numbers of lines differ. A renaming changes names but cannot change the program structure.
2. Parse each line into a command and its variable positions. A `define`, `read`, or `print` line contains one variable. An assignment contains three variables: the destination, the left operand, and the right operand. The command itself is never renamed.
3. Create two empty dictionaries. The first stores mappings from variables in the first program to variables in the second program. The second stores the reverse mapping.
4. Scan corresponding lines of the two programs from top to bottom. If their commands differ, return `NO`, because variable renaming cannot change a command such as `read` into `print`.
5. For every pair of corresponding variable positions, inspect the two variable names. If the first variable already has a mapping, verify that it maps to the current second variable. If it does not, return `NO`.
6. If the first variable has no mapping yet, check whether the second variable is already mapped from a different first variable. If it is, return `NO`. Otherwise establish both directions of the mapping.
7. If every corresponding position passes these checks, return `YES`. At that point every variable has a single consistent counterpart, and because every command and every variable position matched, renaming the first program produces exactly the second program.

### Why it works

The central invariant is that after processing any prefix of the two programs, the two dictionaries describe a valid one-to-one variable renaming for that entire prefix. When a new pair of variables is encountered, an existing mapping must agree with it, while a new mapping can only be introduced if its target has not already been assigned to another source variable. Thus the invariant is preserved after every variable occurrence.

If the algorithm rejects, either the program structure differs or some variable would need two different names, or two different variables would need the same name. None of those situations can be repaired by another global renaming, so the programs cannot be equivalent.

If the algorithm reaches the end, every variable correspondence used by either program is consistent and one-to-one. Replacing every first-program variable with its mapped second-program variable makes every corresponding statement identical, which is exactly the required condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def parse_line(line):
    line = line.strip()

    parts = line.replace(" ", "").split("=")

    if len(parts) == 1:
        command, var = line.split()
        return command, [var]

    left = parts[0]
    right = parts[1]
    b, c = right.split("+")
    return "assign", [left, b, c]

def equivalent(program1, program2):
    if len(program1) != len(program2):
        return False

    forward = {}
    backward = {}

    for line1, line2 in zip(program1, program2):
        command1, vars1 = parse_line(line1)
        command2, vars2 = parse_line(line2)

        if command1 != command2 or len(vars1) != len(vars2):
            return False

        for a, b in zip(vars1, vars2):
            if a in forward:
                if forward[a] != b:
                    return False
            else:
                if b in backward:
                    return False

                forward[a] = b
                backward[b] = a

    return True

def solve():
    n = int(input())
    program1 = [input().strip() for _ in range(n)]

    m = int(input())
    program2 = [input().strip() for _ in range(m)]

    print("YES" if equivalent(program1, program2) else "NO")

if __name__ == "__main__":
    solve()
```

The `parse_line` function normalizes the assignment syntax by removing spaces before splitting it into its three variable positions. This handles both compact forms such as `a=b+c` and spaced forms such as `a = b + c`.

For a simple command, `split()` separates the command word from its variable. The parser returns a common internal representation, with `assign` representing an assignment and the associated list containing destination, left operand, and right operand in exactly that order.

The `equivalent` function first checks the number of lines because the two programs must have identical structure. It then maintains `forward` and `backward`, which implement the two directions of the bijection.

The check `forward[a] != b` catches a variable that is forced to have two different names. The `backward` lookup catches two different variables being forced to share one target name. Both checks are necessary because the required renaming is a bijection between the variables appearing in the two programs.

There is no recursion and no numeric computation, so integer overflow and recursion depth are irrelevant. The scan processes every line and every variable occurrence once, with dictionary operations taking expected constant time.

## Worked Examples

### Sample 1

The two programs have the same structure, so the algorithm begins comparing their statements. The first three definitions establish the only possible mappings.

| Line | Command | First variable positions | Second variable positions | Mapping state | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | define | `a` | `a` | `a -> a` | continue |
| 2 | define | `b` | `b` | `a -> a`, `b -> b` | continue |
| 3 | define | `c` | `c` | `a -> a`, `b -> b`, `c -> c` | continue |
| 4 | assign | `a,b,c` | `a,c,b` | `a -> a` agrees, `b -> c` conflicts | reject |

At line 4, the destination `a` is consistent, but the first program requires `b -> c` and the existing mapping requires `b -> b`. A single global renaming cannot satisfy both requirements, so the answer is `NO`.

### Sample 2

Here the definition order differs, so the first occurrences establish a nontrivial renaming.

| Line | Command | First variable positions | Second variable positions | Mapping state | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | define | `a` | `a` | `a -> a` | continue |
| 2 | define | `b` | `c` | `a -> a`, `b -> c` | continue |
| 3 | define | `c` | `b` | `a -> a`, `b -> c`, `c -> b` | continue |
| 4 | assign | `a,b,c` | `a,c,b` | all mappings agree | continue |
| 5 | print | `a` | `a` | `a -> a` agrees | accept |

The mapping swaps `b` and `c`. Applying it to the first program transforms `a=b+c` into `a=c+b`, exactly matching the second program. The algorithm accepts because every later occurrence respects the mapping established by the definitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n+m)` | Every input line and every variable occurrence is processed once, with expected `O(1)` dictionary operations. |
| Space | `O(n+m)` | The two programs are stored, and the two mappings require space proportional to the number of distinct variables. |

Since both programs contain at most 1000 lines, there are only a few thousand variable occurrences to process. The linear solution is far below the limits of 1 second and 256 MB. The factorial brute-force search is the only approach that is fundamentally unsuitable.

## Test Cases

```python
import sys
import io

def parse_line(line):
    line = line.strip()

    parts = line.replace(" ", "").split("=")

    if len(parts) == 1:
        command, var = line.split()
        return command, [var]

    left = parts[0]
    right = parts[1]
    b, c = right.split("+")
    return "assign", [left, b, c]

def equivalent(program1, program2):
    if len(program1) != len(program2):
        return False

    forward = {}
    backward = {}

    for line1, line2 in zip(program1, program2):
        command1, vars1 = parse_line(line1)
        command2, vars2 = parse_line(line2)

        if command1 != command2 or len(vars1) != len(vars2):
            return False

        for a, b in zip(vars1, vars2):
            if a in forward:
                if forward[a] != b:
                    return False
            else:
                if b in backward:
                    return False
                forward[a] = b
                backward[b] = a

    return True

def solve():
    n = int(input())
    program1 = [input().strip() for _ in range(n)]

    m = int(input())
    program2 = [input().strip() for _ in range(m)]

    return "YES" if equivalent(program1, program2) else "NO"

def run(inp: str) -> str:
    global input
    old_stdin = sys.stdin
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    try:
        return solve()
    finally:
        sys.stdin = old_stdin
        input = old_input

sample1 = """\
5
define a
define b
define c
a=b+c
print a
5
define a
define b
define c
a=c+b
print a
"""
assert run(sample1) == "NO", "sample 1"

sample2 = """\
5
define a
define b
define c
a=b+c
print a
5
define a
define c
define b
a=c+b
print a
"""
assert run(sample2) == "YES", "sample 2"

sample3 = """\
5
define a
define b
define c
a=b+c
print a
5
define a
define b
define c
a=b+c
print a
"""
assert run(sample3) == "YES", "sample 3"

# Minimum-size programs. A single variable can always be renamed to another
# variable because there is no second constraint.
assert run("""\
1
define a
1
define x
""") == "YES", "minimum size"

# Different program lengths can never be made equal by renaming.
assert run("""\
1
define a
2
define x
define y
""") == "NO", "different lengths"

# The same source variable is forced to map to two different target variables.
assert run("""\
4
define a
define b
print a
print a
4
define x
define y
print x
print y
""") == "NO", "inconsistent mapping"

# The target variables are swapped, but the whole program is still equivalent.
assert run("""\
6
define first
define second
define third
first=second+third
print third
read first
6
define x
define z
define y
x=z+y
print y
read x
""") == "YES", "nontrivial bijection"

# Large input, exercising the linear scan.
lines1 = ["define v0"]
lines1.extend(f"define v{i}" for i in range(1, 1000))
lines1.append("print v999")

lines2 = ["define x0"]
lines2.extend(f"define x{i}" for i in range(1, 1000))
lines2.append("print x999")

large_input = (
    str(len(lines1)) + "\n" +
    "\n".join(lines1) + "\n" +
    str(len(lines2)) + "\n" +
    "\n".join(lines2) + "\n"
)
assert run(large_input) == "YES", "maximum-size linear scan"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One `define` line in each program | `YES` | Minimum input size and basic renaming |
| Programs with 1 and 2 lines | `NO` | Different program lengths |
| Repeated source variable mapped to different targets | `NO` | Consistency of the forward mapping |
| Three variables with a nontrivial permutation | `YES` | Bidirectional renaming and repeated uses |
| 1000 definitions plus a final use | `YES` | Maximum-size input and linear complexity |

## Edge Cases

The different-length case is handled before any variable comparison. For

```
1
define a
2
define x
define y
```

`equivalent` sees that the program lengths are `1` and `2` and immediately returns `False`. The output is `NO`. No mapping can change the number of statements.

For the operand-order case,

```
4
define a
define b
define c
a=b+c
4
define x
define y
define z
x=z+y
```

the definitions establish `a -> x`, `b -> y`, and `c -> z`. When the assignment is reached, its first variable pair is `a -> x`, which is valid. The second pair asks for `b -> z`, but `b` is already mapped to `y`, so the algorithm rejects. The output is `NO`. The algorithm never sorts the operands, so it correctly treats the expression as syntax rather than mathematical addition.

For the nontrivial permutation,

```
4
define a
define b
define c
a=b+c
4
define x
define z
define y
x=z+y
```

the first three lines establish `a -> x`, `b -> z`, and `c -> y`. At the assignment, the three pairs are `a -> x`, `b -> z`, and `c -> y`, all of which agree with the existing mapping. The output is `YES`. This demonstrates why comparing raw variable names or definition positions is insufficient.

For an inconsistent reuse,

```
4
define a
define b
print a
print b
4
define x
define y
print x
print x
```

the first print establishes `a -> x`. The second print asks for `b -> x`. The reverse dictionary already contains `x -> a`, so the algorithm rejects the mapping. The output is `NO`. Without the reverse dictionary, a careless implementation could accept two different variables being renamed to the same variable, which is not a valid renaming.
