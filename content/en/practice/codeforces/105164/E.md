---
title: "CF 105164E - Evaluating Linear Expressions"
description: "We are given a simple linear rule that transforms an integer input $x$ into an output value $ax + b$. The task is to apply this rule repeatedly for consecutive values of $x$, starting from 1 up to $k$, and print all resulting outputs in order."
date: "2026-06-27T10:44:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105164
codeforces_index: "E"
codeforces_contest_name: "2024 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 105164
solve_time_s: 65
verified: false
draft: false
---

[CF 105164E - Evaluating Linear Expressions](https://codeforces.com/problemset/problem/105164/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a simple linear rule that transforms an integer input $x$ into an output value $ax + b$. The task is to apply this rule repeatedly for consecutive values of $x$, starting from 1 up to $k$, and print all resulting outputs in order.

In more concrete terms, imagine a machine that takes a number, multiplies it by $a$, then adds $b$. We feed this machine the inputs 1, 2, 3, all the way to $k$, and we record each result as a sequence. The final output is simply this list of transformed values.

The constraints are extremely small, with all parameters bounded by 100. This means any reasonable computation per term is already fast enough, and even the most straightforward simulation runs in negligible time. There is no need for optimization beyond direct evaluation.

There are no tricky hidden edge cases in the input structure itself, but a common mistake is misreading the sequence start. The sequence must begin at $x = 1$, not $x = 0$. If someone incorrectly starts from 0, the first term becomes $b$, which is invalid unless explicitly intended.

Another potential mistake is attempting to be overly clever and deriving a closed-form sequence without realizing that each term is independent. Since each term depends only on its own $x$, there is no recurrence or interaction between terms.

## Approaches

The most direct approach is to compute each term independently. For each $x$ from 1 to $k$, we evaluate $ax + b$ and print the result immediately. This works because the expression is linear and does not depend on previous computations.

A brute-force interpretation might suggest building a list of values and then printing them, but even that is already optimal in this setting. The total number of operations is $k$, and each operation is a constant-time arithmetic computation.

The key observation is that the problem has no state dependency. Each output is fully determined by its index $x$, so there is no benefit to storing intermediate results or attempting incremental updates. Any optimization beyond a simple loop would only add complexity without reducing runtime.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (direct evaluation) | O(k) | O(1) | Accepted |
| Optimal (same idea) | O(k) | O(1) | Accepted |

## Algorithm Walkthrough

We compute each term one by one using the definition of the expression.

1. Read integers $a$, $b$, and $k$. These define the linear transformation and the number of terms we must generate.
2. Iterate $x$ from 1 to $k$. Each value of $x$ corresponds to one term in the sequence.
3. For each $x$, compute $ax + b$. This is the direct evaluation of the given algebraic expression.
4. Store or immediately print the computed value. Since output order matters, we preserve increasing $x$.
5. Separate values with spaces in a single line.

The computation inside the loop is constant time, so the loop itself fully defines the runtime.

### Why it works

Each term in the output is independently defined by substituting a specific value of $x$ into the same formula. There is no dependency between terms, so evaluating them sequentially or independently yields identical results. The loop simply enumerates the domain of $x$ and applies the same deterministic function to each element.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, k = map(int, input().split())

res = []
for x in range(1, k + 1):
    res.append(str(a * x + b))

print(" ".join(res))
```

The solution reads the three integers and then constructs the sequence by iterating over all valid values of $x$. Each computed value is converted to a string immediately to avoid repeated conversions during joining. The final output is printed as a single space-separated line.

A subtle implementation detail is using `range(1, k + 1)` rather than starting from 0. Starting at 0 would incorrectly produce $b$ as the first term, which does not match the required sequence definition.

Using a list and `" ".join(...)` ensures that output formatting is consistent and avoids repeated printing overhead inside the loop.

## Worked Examples

### Example 1

Input:

```
1 1 5
```

We compute $x + 1$ for each $x$.

| x | Computation | Result |
| --- | --- | --- |
| 1 | 1*1 + 1 | 2 |
| 2 | 1*2 + 1 | 3 |
| 3 | 1*3 + 1 | 4 |
| 4 | 1*4 + 1 | 5 |
| 5 | 1*5 + 1 | 6 |

Output:

```
2 3 4 5 6
```

This confirms the direct mapping from index to value and shows that each term is independent.

### Example 2

Input:

```
1 10 7
```

We compute $x + 10$ for each $x$.

| x | Computation | Result |
| --- | --- | --- |
| 1 | 1*1 + 10 | 11 |
| 2 | 1*2 + 10 | 12 |
| 3 | 1*3 + 10 | 13 |
| 4 | 1*4 + 10 | 14 |
| 5 | 1*5 + 10 | 15 |
| 6 | 1*6 + 10 | 16 |
| 7 | 1*7 + 10 | 17 |

Output:

```
11 12 13 14 15 16 17
```

This demonstrates the uniform shift applied by $b$, which affects all terms equally without changing their spacing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k) | One iteration per value of $x$, each performing constant-time arithmetic |
| Space | O(1) | Only a small list of size $k$ (or streamed output if optimized further) |

Given $k \leq 100$, the runtime is trivial even in interpreted languages. The solution is well within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    a, b, k = map(int, input().split())
    res = []
    for x in range(1, k + 1):
        res.append(str(a * x + b))
    return " ".join(res)

# provided samples
assert run("1 1 5") == "2 3 4 5 6", "sample 1"
assert run("1 10 7") == "11 12 13 14 15 16 17", "sample 2"
assert run("3 1 4") == "4 7 10 13", "sample 3"

# custom cases
assert run("2 0 1") == "2", "minimum k"
assert run("1 0 5") == "1 2 3 4 5", "simple identity progression"
assert run("5 5 3") == "10 15 20", "uniform step with offset"
assert run("100 100 2") == "200 300", "max coefficient small k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 0 1 | 2 | Minimum sequence length |
| 1 0 5 | 1 2 3 4 5 | Pure arithmetic progression without offset |
| 5 5 3 | 10 15 20 | Combined slope and intercept correctness |
| 100 100 2 | 200 300 | Handling of maximum coefficients |

## Edge Cases

One edge case is when $k = 1$. In this situation, the loop runs exactly once and produces a single value $a \cdot 1 + b$. The algorithm handles this naturally because the range includes only the starting point.

Another edge case is when $b = 0$. The sequence becomes a pure arithmetic progression starting from $a$. The algorithm still applies the same formula per index, producing correct scaling without special handling.

A final edge case is when both $a$ and $b$ are at their maximum values. Even then, each computation is within safe integer bounds in Python, and no overflow or precision issues arise.
