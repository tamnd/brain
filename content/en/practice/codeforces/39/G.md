---
title: "CF 39G - Inverse Function"
description: "We are given the source code of a tiny recursive function f(n) written in a heavily restricted subset of C++. The functi"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 39
codeforces_index: "G"
codeforces_contest_name: "School Team Contest 1 (Winter Computer School 2010/11)"
rating: 2400
weight: 39
solve_time_s: 122
verified: true
draft: false
---

[CF 39G - Inverse Function](https://codeforces.com/problemset/problem/39/G)

**Rating:** 2400  
**Tags:** implementation  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the source code of a tiny recursive function `f(n)` written in a heavily restricted subset of C++. The function only contains sequential `if (...) return ...;` statements and unconditional `return ...;` statements. Expressions may contain arithmetic, comparisons, and recursive calls to `f`.

The machine arithmetic is unusual. Addition, subtraction, and multiplication are performed modulo `32768`, while division is ordinary integer division. Every valid input `n` lies in `[0, 32767]`, and every function result also lies in that range.

The task is reversed from the usual direction. We are given a value `y = f(n)` and the function definition itself. We must recover the largest `n` such that `f(n) = y`. If no such `n` exists, we print `-1`.

The most intimidating part of the statement is the recursive syntax, but the actual input size completely changes the nature of the problem. The entire program text is at most 100 bytes. That means the parsed syntax tree is tiny. The domain size is also fixed at exactly `32768` possible inputs. Even evaluating the function separately for every possible `n` is realistic if each evaluation is efficient.

The recursive restriction is the key structural guarantee. Whenever we evaluate `f(N)`, recursive calls may only use smaller arguments. This means the dependency graph is acyclic. We can safely compute all values from `0` upward using memoization or dynamic programming.

A careless implementation can silently fail in several places.

One common mistake is forgetting that multiplication is also modulo `32768`.

For example:

```
return 200 * 200;
```

The mathematical result is `40000`, but the function value is:

```
40000 mod 32768 = 7232
```

Using ordinary integer multiplication would produce completely wrong answers.

Another subtle issue is evaluation order for division.

Consider:

```
return 7 / 2 * 3;
```

Operations are evaluated left to right within the same precedence level. The result is:

```
(7 / 2) * 3 = 3 * 3 = 9
```

not:

```
7 / (2 * 3) = 1
```

A parser that ignores associativity will mis-evaluate many expressions.

Recursive calls also create traps if memoization is omitted.

Example:

```
if (n == 0) return 1;
return f(n - 1) + 1;
```

Without caching, evaluating all `32768` states recursively becomes quadratic. With memoization, each state is computed once.

The final subtlety is the answer requirement. We need the maximum valid `n`, not the first one encountered.

Example:

```
if (n < 100) return 17;
return 17;
```

Every input maps to `17`, so the answer is `32767`. Stopping at the first match would incorrectly return `0`.

## Approaches

The direct brute-force idea is straightforward. Parse the function, then for every `n` from `0` to `32767`, evaluate `f(n)` and compare it with the target value. Since recursive calls only go to smaller arguments, recursion terminates naturally.

This already sounds feasible because the domain size is only `32768`. The problem is repeated recomputation. Suppose the function is:

```
return f(n - 1) + 1;
```

Evaluating `f(30000)` recursively recomputes almost the entire prefix every time. The total work becomes roughly:

```
1 + 2 + 3 + ... + 32768
```

which is about `5 * 10^8` evaluations, far too slow in Python.

The crucial observation is that the recursive dependency graph is strictly one-directional. Every state depends only on smaller states. That means each `f(n)` can be computed exactly once and reused forever.

After parsing the program into an abstract syntax tree, we evaluate values in increasing order of `n`. Whenever an expression needs `f(x)`, the value for `x` has already been computed because `x < n`.

The syntax itself is small enough that a handwritten recursive-descent parser is ideal. The grammar already encodes precedence rules:

```
product before sum
left associativity inside each level
```

So we parse expressions exactly according to the grammar and evaluate them against the current `n`.

The brute-force works because the domain is tiny, but repeated recursive expansion makes it too expensive. Memoization transforms the recursion into a linear-time dynamic program over all `32768` states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force without memoization | Exponential in worst recursive chains | O(recursion depth) | Too slow |
| Optimal memoized evaluation | O(32768 × program size) | O(32768) | Accepted |

## Algorithm Walkthrough

1. Read the target value and concatenate the remaining input into one string.

Spaces and line breaks are irrelevant to the grammar, so working on one compact string simplifies parsing.
2. Build a tokenizer and recursive-descent parser for the grammar.

We parse expressions using the standard precedence hierarchy:

`comparison -> sum -> product -> atom`

This guarantees correct evaluation order for `+`, `-`, `*`, and `/`.
3. Parse the function body into a list of statements.

Each statement is either:

```
return expr;
```

or:

```
if (cond) return expr;
```
4. Represent expressions as syntax tree nodes.

Each node stores its type:

```
number
variable n
binary operator
recursive call
```

This allows fast repeated evaluation for different values of `n`.
5. Create an array `dp[0..32767]`.

`dp[x]` will store the computed value of `f(x)`.
6. Evaluate values in increasing order from `0` to `32767`.

When evaluating `f(n)`, scan statements sequentially.

For a conditional return:

- evaluate the condition
- if true, evaluate and return the expression immediately

For an unconditional return:

- evaluate and return immediately

Since recursive calls only use smaller arguments, every needed `dp[k]` already exists.
7. During expression evaluation:

- addition, subtraction, and multiplication are reduced modulo `32768`
- subtraction is normalized back into `[0, 32767]`
- division uses ordinary integer division
- recursive calls use previously computed `dp[value]`
8. Track the largest `n` whose computed value equals the target.
9. Print the largest matching `n`, or `-1` if no match exists.

### Why it works

The problem guarantees that recursive calls from `f(N)` only target values smaller than `N`. This creates a topological order over states:

```
0, 1, 2, ...
```

When computing `dp[n]`, every recursive dependency has already been finalized. Expression evaluation exactly follows the language grammar, so operator precedence and associativity match the specification. Since statements are processed sequentially and evaluation stops at the first returning statement, the simulated execution is identical to the original program. Every `dp[n]` is therefore exactly equal to the true function value `f(n)`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 32768

class Parser:
    def __init__(self, s):
        self.s = s
        self.i = 0

    def skip(self):
        while self.i < len(self.s) and self.s[self.i].isspace():
            self.i += 1

    def match(self, t):
        self.skip()
        if self.s.startswith(t, self.i):
            self.i += len(t)
            return True
        return False

    def expect(self, t):
        assert self.match(t)

    def parse_number(self):
        self.skip()
        j = self.i
        while self.i < len(self.s) and self.s[self.i].isdigit():
            self.i += 1
        return ("num", int(self.s[j:self.i]))

    def parse_atom(self):
        self.skip()

        if self.match("n"):
            return ("n",)

        if self.match("f"):
            self.expect("(")
            expr = self.parse_sum()
            self.expect(")")
            return ("call", expr)

        if self.s[self.i].isdigit():
            return self.parse_number()

        if self.match("("):
            expr = self.parse_sum()
            self.expect(")")
            return expr

    def parse_product(self):
        node = self.parse_atom()

        while True:
            self.skip()

            if self.match("*"):
                node = ("bin", "*", node, self.parse_atom())
            elif self.match("/"):
                node = ("bin", "/", node, self.parse_atom())
            else:
                break

        return node

    def parse_sum(self):
        node = self.parse_product()

        while True:
            self.skip()

            if self.match("+"):
                node = ("bin", "+", node, self.parse_product())
            elif self.match("-"):
                node = ("bin", "-", node, self.parse_product())
            else:
                break

        return node

    def parse_condition(self):
        left = self.parse_sum()

        self.skip()

        if self.match("=="):
            op = "=="
        elif self.match(">"):
            op = ">"
        else:
            self.expect("<")
            op = "<"

        right = self.parse_sum()

        return (op, left, right)

    def parse_statement(self):
        self.skip()

        if self.match("if"):
            self.expect("(")
            cond = self.parse_condition()
            self.expect(")")
            self.expect("return")
            expr = self.parse_sum()
            self.expect(";")
            return ("if", cond, expr)

        self.expect("return")
        expr = self.parse_sum()
        self.expect(";")
        return ("ret", expr)

    def parse_program(self):
        self.expect("int")
        self.expect("f")
        self.expect("(")
        self.expect("int")
        self.expect("n")
        self.expect(")")
        self.expect("{")

        stmts = []

        while True:
            self.skip()
            if self.match("}"):
                break
            stmts.append(self.parse_statement())

        return stmts

def eval_expr(node, n, dp):
    t = node[0]

    if t == "num":
        return node[1]

    if t == "n":
        return n

    if t == "call":
        x = eval_expr(node[1], n, dp)
        return dp[x]

    op = node[1]

    a = eval_expr(node[2], n, dp)
    b = eval_expr(node[3], n, dp)

    if op == "+":
        return (a + b) % MOD

    if op == "-":
        return (a - b) % MOD

    if op == "*":
        return (a * b) % MOD

    return a // b

def eval_cond(cond, n, dp):
    op, left, right = cond

    a = eval_expr(left, n, dp)
    b = eval_expr(right, n, dp)

    if op == "<":
        return a < b

    if op == ">":
        return a > b

    return a == b

def solve():
    target = int(input())

    code = sys.stdin.read()

    parser = Parser(code)
    stmts = parser.parse_program()

    dp = [0] * MOD

    ans = -1

    for n in range(MOD):
        for stmt in stmts:
            if stmt[0] == "if":
                _, cond, expr = stmt

                if eval_cond(cond, n, dp):
                    dp[n] = eval_expr(expr, n, dp)
                    break
            else:
                _, expr = stmt
                dp[n] = eval_expr(expr, n, dp)
                break

        if dp[n] == target:
            ans = n

    print(ans)

solve()
```

The parser mirrors the grammar directly. `parse_product` handles `*` and `/`, while `parse_sum` handles `+` and `-`. Because each level repeatedly consumes operators from left to right, associativity automatically becomes correct.

Expression trees are represented with tuples instead of classes. This keeps evaluation lightweight and fast enough for tens of thousands of executions.

The dynamic programming order is the most important implementation detail. We compute `dp[0]`, then `dp[1]`, and so on. The problem guarantee says recursive calls only use smaller arguments, so every recursive dependency is already available.

Modulo handling is another place where mistakes happen easily. Python's `%` already keeps subtraction results non-negative:

```
(a - b) % MOD
```

matches the problem definition exactly.

The statement loop stops immediately after the first returning branch, just like real execution. Forgetting the `break` would incorrectly continue scanning later statements.

## Worked Examples

### Example 1

Input:

```
17
int f(int n)
{
if (n < 100) return 17;
if (n > 99) return 27;
}
```

Trace for selected values:

| n | First condition `n < 100` | Returned value | Matches target |
| --- | --- | --- | --- |
| 0 | true | 17 | yes |
| 50 | true | 17 | yes |
| 99 | true | 17 | yes |
| 100 | false | 27 | no |
| 32767 | false | 27 | no |

The largest matching input is `99`.

This example demonstrates that execution stops at the first satisfied return statement. The second condition is never checked for `n < 100`.

### Example 2

Input:

```
1
int f(int n)
{
if(n==0)return 1;
return f(n-1)+1;
}
```

Trace for first few states:

| n | Recursive dependency | Computed value |
| --- | --- | --- |
| 0 | none | 1 |
| 1 | f(0) | 2 |
| 2 | f(1) | 3 |
| 3 | f(2) | 4 |

The target value `1` only appears at `n = 0`.

This trace confirms why increasing-order DP works. Every recursive dependency already exists before the current state is evaluated.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(32768 × S) | `S` is the tiny parsed program size |
| Space | O(32768) | DP array for all function values |

The source code length is at most 100 bytes, so the syntax tree is extremely small. Evaluating every input from `0` to `32767` is completely safe within the 5-second limit. Memory usage is dominated by the DP array of size `32768`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 32768

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    input = sys.stdin.readline

    class Parser:
        def __init__(self, s):
            self.s = s
            self.i = 0

        def skip(self):
            while self.i < len(self.s) and self.s[self.i].isspace():
                self.i += 1

        def match(self, t):
            self.skip()
            if self.s.startswith(t, self.i):
                self.i += len(t)
                return True
            return False

        def expect(self, t):
            assert self.match(t)

        def parse_number(self):
            self.skip()
            j = self.i
            while self.i < len(self.s) and self.s[self.i].isdigit():
                self.i += 1
            return ("num", int(self.s[j:self.i]))

        def parse_atom(self):
            self.skip()

            if self.match("n"):
                return ("n",)

            if self.match("f"):
                self.expect("(")
                expr = self.parse_sum()
                self.expect(")")
                return ("call", expr)

            if self.s[self.i].isdigit():
                return self.parse_number()

            self.expect("(")
            expr = self.parse_sum()
            self.expect(")")
            return expr

        def parse_product(self):
            node = self.parse_atom()

            while True:
                self.skip()

                if self.match("*"):
                    node = ("bin", "*", node, self.parse_atom())
                elif self.match("/"):
                    node = ("bin", "/", node, self.parse_atom())
                else:
                    break

            return node

        def parse_sum(self):
            node = self.parse_product()

            while True:
                self.skip()

                if self.match("+"):
                    node = ("bin", "+", node, self.parse_product())
                elif self.match("-"):
                    node = ("bin", "-", node, self.parse_product())
                else:
                    break

            return node

        def parse_condition(self):
            left = self.parse_sum()

            if self.match("=="):
                op = "=="
            elif self.match(">"):
                op = ">"
            else:
                self.expect("<")
                op = "<"

            right = self.parse_sum()

            return (op, left, right)

        def parse_statement(self):
            if self.match("if"):
                self.expect("(")
                cond = self.parse_condition()
                self.expect(")")
                self.expect("return")
                expr = self.parse_sum()
                self.expect(";")
                return ("if", cond, expr)

            self.expect("return")
            expr = self.parse_sum()
            self.expect(";")
            return ("ret", expr)

        def parse_program(self):
            self.expect("int")
            self.expect("f")
            self.expect("(")
            self.expect("int")
            self.expect("n")
            self.expect(")")
            self.expect("{")

            stmts = []

            while True:
                self.skip()
                if self.match("}"):
                    break
                stmts.append(self.parse_statement())

            return stmts

    def eval_expr(node, n, dp):
        t = node[0]

        if t == "num":
            return node[1]

        if t == "n":
            return n

        if t == "call":
            return dp[eval_expr(node[1], n, dp)]

        op = node[1]
        a = eval_expr(node[2], n, dp)
        b = eval_expr(node[3], n, dp)

        if op == "+":
            return (a + b) % MOD
        if op == "-":
            return (a - b) % MOD
        if op == "*":
            return (a * b) % MOD

        return a // b

    def eval_cond(cond, n, dp):
        op, l, r = cond
        a = eval_expr(l, n, dp)
        b = eval_expr(r, n, dp)

        if op == "<":
            return a < b
        if op == ">":
            return a > b
        return a == b

    target = int(input())
    code = sys.stdin.read()

    parser = Parser(code)
    stmts = parser.parse_program()

    dp = [0] * MOD
    ans = -1

    for n in range(MOD):
        for stmt in stmts:
            if stmt[0] == "if":
                _, cond, expr = stmt
                if eval_cond(cond, n, dp):
                    dp[n] = eval_expr(expr, n, dp)
                    break
            else:
                _, expr = stmt
                dp[n] = eval_expr(expr, n, dp)
                break

        if dp[n] == target:
            ans = n

    return str(ans)

# provided sample
assert run("""17
int f(int n)
{
if (n < 100) return 17;
if (n > 99) return 27;
}
""") == "99"

# constant function
assert run("""5
int f(int n){return 5;}
""") == "32767"

# modulo multiplication
assert run("""7232
int f(int n){return 200*200;}
""") == "32767"

# recursive chain
assert run("""4
int f(int n){
if(n==0)return 1;
return f(n-1)+1;
}
""") == "3"

# impossible target
assert run("""123
int f(int n){return 0;}
""") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Constant function returning 5 | 32767 | Must return largest valid input |
| `200*200` | 32767 | Correct modulo multiplication |
| Recursive increment chain | 3 | Recursive DP evaluation |
| Constant zero function with target 123 | -1 | Proper handling of missing answers |

## Edge Cases

Consider the modulo arithmetic case:

```
7232
int f(int n){return 200*200;}
```

The algorithm evaluates:

```
200 * 200 = 40000
40000 mod 32768 = 7232
```

Every input maps to `7232`, so the largest answer is `32767`. Because multiplication is reduced modulo `32768`, the implementation matches the problem's arithmetic model exactly.

Now consider recursive dependencies:

```
3
int f(int n){
if(n==0)return 1;
return f(n-1)+1;
}
```

The DP array fills in this order:

```
dp[0] = 1
dp[1] = 2
dp[2] = 3
```

When computing `dp[2]`, the recursive call `f(1)` simply reads `dp[1]`, which is already finalized. No repeated recursion occurs.

Finally, consider multiple matching inputs:

```
17
int f(int n){return 17;}
```

Every `n` is valid. The algorithm scans all `32768` values and continuously updates the answer whenever another match appears. The final stored answer becomes `32767`, which is exactly what the statement requires.
