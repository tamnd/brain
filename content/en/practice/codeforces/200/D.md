---
title: "CF 200D - Programming Language"
description: "We are given a collection of procedure declarations and a collection of variables. Each procedure declaration consists of a name and a list of parameter types. A parameter type may be one of the concrete types int, string, or double, or it may be the wildcard type T."
date: "2026-06-03T16:27:03+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "expression-parsing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 200
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 126 (Div. 2)"
rating: 1800
weight: 200
solve_time_s: 129
verified: true
draft: false
---

[CF 200D - Programming Language](https://codeforces.com/problemset/problem/200/D)

**Rating:** 1800  
**Tags:** binary search, brute force, expression parsing, implementation  
**Solve time:** 2m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of procedure declarations and a collection of variables.

Each procedure declaration consists of a name and a list of parameter types. A parameter type may be one of the concrete types `int`, `string`, or `double`, or it may be the wildcard type `T`. The type `T` matches any variable type.

Later, procedure calls are given. A call contains a procedure name and a list of variable names. Since every variable has a known type, each call can be viewed as a procedure name together with an ordered list of argument types.

For every call, we must count how many declared procedures are compatible with it.

A procedure is compatible if all three conditions hold:

1. The names are identical.
2. The number of parameters is identical.
3. For every position, either the procedure parameter type is `T`, or it exactly equals the corresponding argument type.

The main difficulty is not the matching logic. The difficult part is parsing the input correctly because arbitrary spaces may appear almost everywhere around keywords, commas, and parentheses.

The constraints are fairly small. There are at most 1000 procedure declarations and at most 1000 calls. Every parameter list has length at most 5. A straightforward comparison between a call and every procedure already requires only about

$$1000 \times 1000 \times 5 = 5 \cdot 10^6$$

type comparisons in the worst case.

Five million simple string comparisons is easily acceptable within a 2 second limit. This means the problem is primarily an implementation and parsing problem rather than an algorithmic optimization problem.

Several edge cases can silently break a careless parser.

Consider:

```
void  f ( int , T )
```

and

```
f(a,b)
```

The declaration contains arbitrary spaces around every token. A parser based on fixed positions or simple splitting by spaces will fail.

Another subtle case is matching `T`.

```
void f(T)
void f(int)

int a
f(a)
```

The correct answer is:

```
2
```

because both declarations are suitable. A common mistake is to treat `T` as a concrete type rather than a wildcard.

Another edge case is differing parameter counts.

```
void f(T)
void f(T,T)

int a
f(a)
```

The correct answer is:

```
1
```

Even though `T` matches anything, the number of parameters must still match exactly.

Finally, procedure names may contain digits:

```
void foo123(int)
```

A parser that assumes identifiers contain only letters would incorrectly reject valid names.

## Approaches

The most direct solution is to parse all declarations, store them, and for every call test every procedure declaration.

For a single comparison we check three things. The names must match. The parameter counts must match. Then each parameter position must satisfy either exact type equality or a wildcard `T`.

This brute-force approach is obviously correct because it implements the definition of suitability literally. For each call it examines every declaration and counts exactly those that satisfy the rules.

The natural concern is efficiency. With 1000 declarations and 1000 calls, we perform at most one million declaration-call comparisons. Since each declaration contains at most five parameters, the total work is roughly five million parameter checks. That is easily fast enough.

There is no need for sophisticated indexing, hashing schemes, or binary search. The problem is categorized under several tags because parsing and matching patterns can sometimes be optimized, but the given constraints make a direct implementation entirely sufficient.

The real observation is that the parameter count is capped at five. Even a complete scan of all procedures for every call remains comfortably within the limit. Once we realize this, the task becomes careful parsing and faithful implementation of the matching rules.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nkL) | O(n + m) | Accepted |
| Optimal | O(nkL) | O(n + m) | Accepted |

Here $L \le 5$ is the maximum number of parameters.

## Algorithm Walkthrough

1. Read all procedure declarations.
2. For each declaration, remove surrounding whitespace and parse:

- procedure name
- ordered list of parameter types
3. Store every declaration as a pair:

- procedure name
- parameter type list
4. Read all variable declarations.
5. Store a mapping from variable name to variable type.
6. For each procedure call, parse:

- called procedure name
- ordered list of variable names
7. Convert the variable names into their corresponding types using the variable table.
8. Initialize the answer for this call to zero.
9. Iterate through every stored procedure declaration.
10. Skip immediately if the names differ.
11. Skip immediately if the parameter counts differ.
12. Compare corresponding positions one by one.

A position matches when the declaration type is `T` or when it equals the argument type.
13. If every position matches, increment the answer.
14. Output the final count for the call.

### Why it works

For every call, the algorithm examines every declared procedure exactly once. A procedure contributes to the count if and only if all conditions from the definition are satisfied.

The name check enforces identical procedure names. The length check enforces identical parameter counts. The positional comparison enforces the exact matching rule that either the declaration contains `T` or the concrete types are equal.

Since every declaration is tested and no declaration is counted unless all rules hold, the resulting count is exactly the number of suitable procedures.

## Python Solution

```python
import sys
input = sys.stdin.readline

def parse_signature(line):
    line = line.strip()

    if line.startswith("void"):
        line = line[4:].strip()

    pos_l = line.find('(')
    pos_r = line.rfind(')')

    name = line[:pos_l].strip()

    inside = line[pos_l + 1:pos_r].strip()

    if inside == "":
        params = []
    else:
        params = [x.strip() for x in inside.split(',')]

    return name, params

def solve():
    n = int(input())

    procedures = []

    for _ in range(n):
        procedures.append(parse_signature(input()))

    m = int(input())

    var_type = {}

    for _ in range(m):
        parts = input().strip().split()
        var_type[parts[1]] = parts[0]

    k = int(input())

    answers = []

    for _ in range(k):
        name, vars_used = parse_signature(input())

        arg_types = [var_type[v] for v in vars_used]

        cnt = 0

        for proc_name, proc_types in procedures:
            if proc_name != name:
                continue

            if len(proc_types) != len(arg_types):
                continue

            ok = True

            for p, a in zip(proc_types, arg_types):
                if p != "T" and p != a:
                    ok = False
                    break

            if ok:
                cnt += 1

        answers.append(str(cnt))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The parser is the most delicate part of the implementation.

Both declarations and calls share the same general structure:

```
name(type1,type2,...)
```

The only difference is that declarations may begin with the keyword `void`. The helper function removes that prefix when present and then extracts the procedure name and the comma-separated contents between parentheses.

Every extracted token is individually stripped of whitespace. This makes the parser immune to arbitrary spacing around commas, parentheses, and keywords.

The matching loop follows the definition directly. Names and parameter counts are checked first because they allow early rejection. Only then do we compare corresponding parameter positions.

The wildcard rule is implemented by:

```
if p != "T" and p != a:
```

which rejects only when the declaration parameter is neither a wildcard nor the correct concrete type.

Because the maximum parameter count is only five, no additional optimization is necessary.

## Worked Examples

### Sample 1

Input:

```
4
void f(int,T)
void f(T, T)
void foo123(int,double,string,string)
void p(T,double)
3
int a
string s
double x123
5
f(a,a)
f(s,a)
foo(a,s,s)
f(s,x123)
proc(a)
```

Procedures:

| Procedure | Types |
| --- | --- |
| f | [int, T] |
| f | [T, T] |
| foo123 | [int, double, string, string] |
| p | [T, double] |

Variables:

| Variable | Type |
| --- | --- |
| a | int |
| s | string |
| x123 | double |

Call `f(a,a)`:

| Candidate | Match |
| --- | --- |
| f(int,T) | Yes |
| f(T,T) | Yes |

Answer = 2.

Call `f(s,a)`:

| Candidate | Match |
| --- | --- |
| f(int,T) | No |
| f(T,T) | Yes |

Answer = 1.

Call `foo(a,s,s)`:

| Candidate | Match |
| --- | --- |
| foo123(...) | Name mismatch |

Answer = 0.

This trace shows that procedure names must match exactly and that `T` behaves as a wildcard.

### Custom Example

Input:

```
3
void g(T)
void g(int)
void g(string)
2
int a
string b
2
g(a)
g(b)
```

For `g(a)`:

| Candidate | Parameter Types | Match |
| --- | --- | --- |
| g(T) | [T] | Yes |
| g(int) | [int] | Yes |
| g(string) | [string] | No |

Answer = 2.

For `g(b)`:

| Candidate | Parameter Types | Match |
| --- | --- | --- |
| g(T) | [T] | Yes |
| g(int) | [int] | No |
| g(string) | [string] | Yes |

Answer = 2.

This example demonstrates that multiple declarations can match the same call simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nkL) | Every call checks every procedure, each with at most L ≤ 5 parameter comparisons |
| Space | O(n + m) | Stored procedures and variable table |

With $n \le 1000$, $k \le 1000$, and $L \le 5$, the total work is at most about five million parameter comparisons. This comfortably fits within the time limit. Memory usage is tiny because only the declarations and variable type mapping are stored.

## Test Cases

```python
# helper: run solution on input string, return output string
import io
import sys

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    def parse_signature(line):
        line = line.strip()

        if line.startswith("void"):
            line = line[4:].strip()

        l = line.find("(")
        r = line.rfind(")")

        name = line[:l].strip()

        inside = line[l + 1:r].strip()

        if inside:
            params = [x.strip() for x in inside.split(",")]
        else:
            params = []

        return name, params

    n = int(input())
    procedures = [parse_signature(input()) for _ in range(n)]

    m = int(input())
    vars_ = {}

    for _ in range(m):
        t, v = input().split()
        vars_[v] = t

    k = int(input())
    ans = []

    for _ in range(k):
        name, vars_used = parse_signature(input())
        arg_types = [vars_[v] for v in vars_used]

        cur = 0

        for pname, ptypes in procedures:
            if pname != name:
                continue

            if len(ptypes) != len(arg_types):
                continue

            ok = True

            for p, a in zip(ptypes, arg_types):
                if p != "T" and p != a:
                    ok = False
                    break

            if ok:
                cur += 1

        ans.append(str(cur))

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return "\n".join(ans)

# sample 1
assert run(
"""4
void f(int,T)
void f(T, T)
void foo123(int,double,string,string)
void p(T,double)
3
int a
string s
double x123
5
f(a,a)
f(s,a)
foo(a,s,s)
f(s,x123)
proc(a)
"""
) == "2\n1\n0\n1\n0"

# minimum case
assert run(
"""1
void f(T)
1
int a
1
f(a)
"""
) == "1"

# parameter count mismatch
assert run(
"""2
void f(T)
void f(T,T)
1
int a
1
f(a)
"""
) == "1"

# wildcard and exact match together
assert run(
"""3
void g(T)
void g(int)
void g(string)
2
int a
string b
2
g(a)
g(b)
"""
) == "2\n2"

# many spaces
assert run(
"""1
  void   abc123 (  int , T )   
2
int x
double y
1
 abc123 ( x , y )
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single declaration with `T` | 1 | Minimum valid instance |
| Different parameter counts | 1 | Exact arity matching |
| Exact types plus wildcard | 2, 2 | Multiple matching declarations |
| Excessive whitespace | 1 | Robust parsing |
| Sample input | 2,1,0,1,0 | Full problem behavior |

## Edge Cases

Consider declarations with different parameter counts:

```
2
void f(T)
void f(T,T)
1
int a
1
f(a)
```

The call has one argument. The first declaration survives the length check. The second declaration is rejected immediately because it expects two parameters. The algorithm outputs:

```
1
```

which is correct.

Consider wildcard matching:

```
2
void f(T)
void f(string)
1
int a
1
f(a)
```

The call type list is `[int]`.

For `f(T)`, the comparison succeeds because `T` accepts any type.

For `f(string)`, the comparison fails because `string != int`.

The answer is:

```
1
```

which matches the language rules.

Consider names containing digits:

```
1
void foo123(int)
1
int a
1
foo123(a)
```

The parser extracts `foo123` as the name without imposing any alphabetic-only restriction. The declaration matches the call, producing:

```
1
```

This confirms that identifier parsing handles the full set of valid names.
