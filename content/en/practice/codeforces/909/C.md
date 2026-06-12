---
title: "CF 909C - Python Indentation"
description: "We are given a sequence of program statements. Each statement is either: f , a for statement whose body must contain at least one statement at one indentation level deeper. s , a simple statement that occupies exactly one line and does not create a new block."
date: "2026-06-12T10:26:25+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 909
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 455 (Div. 2)"
rating: 1800
weight: 909
solve_time_s: 180
verified: true
draft: false
---

[CF 909C - Python Indentation](https://codeforces.com/problemset/problem/909/C)

**Rating:** 1800  
**Tags:** dp  
**Solve time:** 3m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of program statements. Each statement is either:

`f` , a `for` statement whose body must contain at least one statement at one indentation level deeper.

`s` , a simple statement that occupies exactly one line and does not create a new block.

The indentation has been removed from the program. Our task is to count how many valid indentation layouts can produce a syntactically correct Python-like program.

The crucial detail is that indentation determines block structure. Every `for` statement must have a non-empty body, so the statement immediately following an `f` must be indented one level deeper and belong to its body. After a simple statement, however, the next statement may stay at the same indentation level or dedent by any amount that still keeps the program valid.

The number of commands is at most 5000. This immediately rules out any approach that explicitly builds all possible indentation trees. Even quadratic algorithms must be implemented carefully because $5000^2 = 25$ million operations. A cubic solution would require roughly $1.25 \times 10^{11}$ operations and is completely infeasible.

The answer must be computed modulo $10^9+7$.

A subtle aspect of the problem is that indentation choices are not made at `for` statements. A `for` forces the next line to be one level deeper. The real freedom appears after simple statements, because a simple statement may terminate several currently open loops.

Consider:

```
2
f
s
```

There is exactly one valid program:

```
for
    simple
```

The simple statement must be inside the loop body.

Another interesting case is:

```
3
f
s
s
```

The second `s` may either remain inside the loop or close the loop first.

The two valid layouts are:

```
for
    simple
    simple
```

and

```
for
    simple
simple
```

A solution that only tracks current indentation and greedily keeps it unchanged would miss one of these possibilities.

A third edge case is a chain of loops:

```
4
f
f
f
s
```

The answer is 1.

Every loop requires its immediate successor to be inside its body, so the nesting depth is completely forced:

```
for
    for
        for
            simple
```

No choices exist.

## Approaches

The most direct idea is to reconstruct all valid indentation patterns. We process statements from top to bottom, maintain the current indentation level, and whenever we encounter a simple statement we try every possible amount of dedentation before the next statement.

This brute-force search is correct because every valid indentation configuration corresponds to one sequence of dedentation decisions. Unfortunately, the number of possibilities grows exponentially. Even a sequence consisting mostly of simple statements can generate an enormous branching factor, making exhaustive enumeration impossible.

The key observation is that only the current indentation depth matters. The exact history that produced that depth is irrelevant.

This suggests dynamic programming.

Suppose we process statements one by one. Let `dp[d]` represent the number of ways to reach indentation depth `d` before processing the current statement.

Now consider how the next statement is affected.

If the current statement is `f`, then the next statement must be one level deeper. Every state at depth `d` transitions to depth `d+1`.

If the current statement is `s`, then before the next statement we may close zero or more currently open loops. Starting from depth `d`, we may move to any depth between `0` and `d`.

This second transition appears expensive because each state branches into many states. A naive implementation would require $O(n^2)$ work per row and $O(n^3)$ overall.

The structure of the transition saves us. For a simple statement, every depth receives contributions from all deeper-or-equal depths:

$$new[d] = \sum_{k=d}^{n} dp[k]$$

This is exactly a suffix sum. We can compute an entire DP row in linear time.

Since there are at most 5000 statements and each step costs $O(n)$, the total complexity becomes $O(n^2)$, which comfortably fits the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal DP with suffix sums | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

Let `dp[d]` denote the number of valid ways to be at indentation depth `d` before processing the next statement.

Initially, before the first statement, the program starts at depth 0.

1. Create an array `dp` of size `n + 1` and set `dp[0] = 1`.
2. Process statements from the first command through the second-last command.

We stop at the second-last command because each statement determines how the following statement may be placed.
3. If the current statement is `f`, create a new DP row where every state shifts one level deeper.

For every depth `d`, add `dp[d]` into `new[d+1]`.

This models the rule that the next statement must belong to the loop body.
4. If the current statement is `s`, compute suffix sums.

Let

$$suffix[d] = dp[d] + suffix[d+1]$$

Then set

$$new[d] = suffix[d]$$

Every configuration at depth `k` can dedent to any depth from `0` through `k`, so depth `d` receives contributions from all states with depth at least `d`.
5. Replace `dp` with the newly computed row.
6. After all transitions are processed, sum all values in the final DP row.

The last statement is guaranteed to be `s`, so every remaining depth represents a valid complete program.
7. Output the result modulo $10^9+7$.

### Why it works

The invariant is that after processing statement `i`, `dp[d]` equals the number of valid indentation assignments for the prefix ending at statement `i`, such that statement `i+1` is positioned at depth `d`.

For a `for` statement, Python syntax forces the next statement to be exactly one level deeper, so shifting every state from `d` to `d+1` is both necessary and sufficient.

For a simple statement, the next statement may remain at the current depth or appear after closing any number of active loops. A state at depth `k` can thus transition to every depth `0..k`. Computing suffix sums aggregates exactly these possibilities.

Since every valid indentation choice corresponds to one DP transition and every DP transition corresponds to a valid indentation choice, the DP counts all valid programs exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    n = int(input())
    cmds = [input().strip() for _ in range(n)]

    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(n - 1):
        ndp = [0] * (n + 1)

        if cmds[i] == 'f':
            for d in range(n):
                ndp[d + 1] = dp[d]
        else:
            suffix = 0
            for d in range(n, -1, -1):
                suffix = (suffix + dp[d]) % MOD
                ndp[d] = suffix

        dp = ndp

    print(sum(dp) % MOD)

if __name__ == "__main__":
    solve()
```

The DP array stores counts indexed by indentation depth. Only depths up to `n` are needed because no program can become deeper than the number of statements.

For an `f`, the transition is a pure shift. A common mistake is to update the array in place. Doing so mixes states from the current row with states of the next row. Using a fresh `ndp` avoids that issue.

For an `s`, every depth receives contributions from all deeper depths. Computing these sums directly would take quadratic time per transition. The suffix-sum sweep accumulates them in one pass from right to left.

The loop runs only through `n - 1` statements. This is intentional. Statement `i` determines the placement of statement `i + 1`, so the final command has no outgoing transition.

Finally, all remaining depths are valid ending states, so their counts are summed.

## Worked Examples

### Sample 1

Input:

```
4
s
f
f
s
```

Processing states:

| Step | Statement | DP depths with nonzero values |
| --- | --- | --- |
| Start | - | {0: 1} |
| After s | suffix transition | {0: 1} |
| After f | shift | {1: 1} |
| After f | shift | {2: 1} |

Final DP:

| Depth | Ways |
| --- | --- |
| 2 | 1 |

Answer = 1.

The chain of consecutive `f` statements forces nesting. No dedentation choices ever appear.

### Sample 2

Input:

```
4
f
s
f
s
```

Processing states:

| Step | Statement | DP depths with nonzero values |
| --- | --- | --- |
| Start | - | {0: 1} |
| After f | shift | {1: 1} |
| After s | suffix | {0: 1, 1: 1} |
| After f | shift | {1: 1, 2: 1} |

Final DP:

| Depth | Ways |
| --- | --- |
| 1 | 1 |
| 2 | 1 |

Answer = 2.

The suffix step after the first simple statement creates two possibilities. We may either stay inside the current loop or close it before starting the next `for`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | There are `n` DP rows, each processed in O(n) time |
| Space | O(n) | Only the current and next DP rows are stored |

With $n \le 5000$, the algorithm performs roughly 25 million simple operations, which fits comfortably within the given limits in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    cmds = [input().strip() for _ in range(n)]

    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(n - 1):
        ndp = [0] * (n + 1)

        if cmds[i] == "f":
            for d in range(n):
                ndp[d + 1] = dp[d]
        else:
            suffix = 0
            for d in range(n, -1, -1):
                suffix = (suffix + dp[d]) % MOD
                ndp[d] = suffix

        dp = ndp

    return str(sum(dp) % MOD)

# sample 1
assert run("4\ns\nf\nf\ns\n") == "1"

# sample 2 from statement discussion
assert run("4\nf\ns\nf\ns\n") == "2"

# minimum size
assert run("1\ns\n") == "1"

# single loop
assert run("2\nf\ns\n") == "1"

# one loop followed by another simple statement
assert run("3\nf\ns\ns\n") == "2"

# fully forced nesting
assert run("5\nf\nf\nf\nf\ns\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 s` | `1` | Smallest valid program |
| `f s` | `1` | Mandatory loop body |
| `f s s` | `2` | Optional dedentation after simple statement |
| `f f f f s` | `1` | Completely forced nesting |
| `f s f s` | `2` | Branching created by suffix-sum transition |

## Edge Cases

Consider the smallest possible input:

```
1
s
```

The DP starts with `dp[0] = 1`. No transitions are processed because there is no following statement. Summing the final row gives 1. This correctly counts the single valid program consisting of one simple statement.

Consider a chain of loops:

```
4
f
f
f
s
```

The transitions are:

```
depth 0 -> depth 1
depth 1 -> depth 2
depth 2 -> depth 3
```

No suffix-sum transition ever occurs. The final DP contains exactly one state, so the answer is 1. Every loop must contain the next statement, forcing complete nesting.

Consider:

```
3
f
s
s
```

After the first `f`, the DP contains only depth 1. The simple statement then performs a suffix transition and creates states at depths 0 and 1. These represent the two legal choices: close the loop before the next statement, or keep the next statement inside the loop. The algorithm outputs 2, matching the actual number of valid indentation layouts.

These examples illustrate the central invariant: `f` creates forced nesting, while `s` creates all legal dedentation choices through the suffix-sum transition.
