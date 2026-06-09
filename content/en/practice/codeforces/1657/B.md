---
title: "CF 1657B - XY Sequence"
description: "We need to construct an array $a0, a1, dots, an$ starting from $a0 = 0$. For every next position, we have exactly two choices. We can either increase the current value by $x$, or decrease it by $y$. The only restriction is that every value in the sequence must stay at most $B$."
date: "2026-06-10T03:27:50+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1657
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 125 (Rated for Div. 2)"
rating: 800
weight: 1657
solve_time_s: 116
verified: true
draft: false
---

[CF 1657B - XY Sequence](https://codeforces.com/problemset/problem/1657/B)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to construct an array $a_0, a_1, \dots, a_n$ starting from $a_0 = 0$.

For every next position, we have exactly two choices. We can either increase the current value by $x$, or decrease it by $y$. The only restriction is that every value in the sequence must stay at most $B$. Negative values are completely allowed.

Among all valid sequences, we want the one whose total sum of elements is as large as possible.

The constraints are small enough that we can process each position individually. Although $t$ can be as large as $10^4$, the sum of all $n$ values is at most $2 \cdot 10^5$. That means an $O(n)$ algorithm per test case, or more precisely $O(\sum n)$ across all test cases, easily fits within the time limit. Exponential exploration of all possible choices is impossible because every position has two options, leading to $2^n$ sequences.

The tricky part is recognizing that maximizing the total sum is not a global optimization problem requiring dynamic programming. The structure is much simpler.

Consider this input:

```
1
4 1 7 3
```

The correct sequence is:

```
0, -3, -6, 1, -2
```

with sum $-10$.

A careless strategy that always tries to add $x$ would immediately violate the bound because $0 + 7 > 1$. Since values are allowed to become negative, the optimal solution may intentionally move downward first and only later take an upward step.

Another interesting case is:

```
1
3 5 5 1
```

The optimal sequence is:

```
0, 5, 4, 3
```

with sum $12$.

After reaching $5$, adding another $5$ would exceed $B$, so we must subtract $1$. A solution that blindly alternates operations or always prefers subtraction after hitting the limit would miss the best total.

Large answers are also possible:

```
1
7 1000000000 1000000000 1000000000
```

The answer is:

```
4000000000
```

Using 32-bit integers would overflow. The implementation must use Python integers or 64-bit arithmetic in other languages.

## Approaches

The most direct approach is to view every position as a binary choice. At step $i$, either add $x$ or subtract $y$. We could recursively try both possibilities whenever they produce valid values and keep the best total sum.

This brute-force search is correct because it examines every valid sequence. Unfortunately, it has $2^n$ states in the worst case. With $n$ up to $2 \cdot 10^5$, this is completely infeasible.

The key observation is that the objective is to maximize the sum of all sequence values. At every step, the future depends only on the current value. If both operations are allowed, choosing the larger resulting value is always better.

Suppose the current value is $cur$.

If $cur + x \le B$, then the two candidate next values are:

$$cur + x$$

and

$$cur - y$$

Since $x > 0$ and $y > 0$,

$$cur + x > cur - y.$$

The larger next value not only increases the current contribution to the answer, it also gives a larger starting point for all future decisions. There is never a reason to choose subtraction when addition is valid.

That means the decision is forced:

If adding $x$ stays within the limit, do it.

Otherwise, subtract $y$.

This yields a simple greedy simulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal Greedy Simulation | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Initialize the current value as $cur = 0$.
2. Initialize the answer as $ans = 0$, since $a_0 = 0$ contributes to the sum.
3. For each position from $1$ to $n$, check whether adding $x$ would keep the value within the allowed bound.
4. If $cur + x \le B$, set $cur = cur + x$.

This is the best possible choice because it produces a strictly larger value than $cur - y$.
5. Otherwise, set $cur = cur - y$.

Addition is forbidden in this situation, so subtraction is the only valid move.
6. Add the new value of $cur$ to the running total.
7. After processing all $n$ positions, output the accumulated sum.

### Why it works

The greedy choice is locally and globally optimal.

Whenever $cur + x \le B$, both operations are legal. The resulting value after addition is always greater than the resulting value after subtraction because $x$ and $y$ are positive.

Choosing the larger value immediately increases the current term in the total sum. It also leaves us with a larger current value for future steps. Any sequence obtainable after choosing $cur - y$ can be replicated from the larger state $cur + x$ with equal or better future contributions.

Thus every time addition is available, it dominates subtraction. The only time we subtract is when addition would violate the constraint. Repeating this rule at every step produces the maximum possible sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    answers = []

    for _ in range(t):
        n, B, x, y = map(int, input().split())

        cur = 0
        total = 0

        for _ in range(n):
            if cur + x <= B:
                cur += x
            else:
                cur -= y

            total += cur

        answers.append(str(total))

    sys.stdout.write("\n".join(answers))

solve()
```

The variable `cur` stores the current sequence value. We start at `0`, corresponding to $a_0$.

For every new position, we first check whether adding $x$ remains within the upper bound $B$. If it does, we take that option. Otherwise we must subtract $y$.

After determining the new value, we immediately add it to `total`. Since `total` starts at zero and $a_0 = 0$, no separate handling is required for the first element.

One common mistake is to think that negative values are forbidden. The problem only restricts values from above, so subtraction can produce arbitrarily negative numbers.

Another common mistake is using 32-bit integers. The sample itself contains an answer of $4 \times 10^9$, which exceeds the signed 32-bit range. Python handles this automatically.

## Worked Examples

### Example 1

Input:

```
n = 5, B = 100, x = 1, y = 30
```

| Step | Current Before | Action | Current After | Running Sum |
| --- | --- | --- | --- | --- |
| 0 | 0 | Start | 0 | 0 |
| 1 | 0 | +1 | 1 | 1 |
| 2 | 1 | +1 | 2 | 3 |
| 3 | 2 | +1 | 3 | 6 |
| 4 | 3 | +1 | 4 | 10 |
| 5 | 4 | +1 | 5 | 15 |

Answer:

```
15
```

The bound is so large that addition is always possible. The greedy rule keeps increasing the value and produces the obvious optimal sequence.

### Example 2

Input:

```
n = 7, B = 1000000000, x = 1000000000, y = 1000000000
```

| Step | Current Before | Action | Current After | Running Sum |
| --- | --- | --- | --- | --- |
| 0 | 0 | Start | 0 | 0 |
| 1 | 0 | +x | 1000000000 | 1000000000 |
| 2 | 1000000000 | -y | 0 | 1000000000 |
| 3 | 0 | +x | 1000000000 | 2000000000 |
| 4 | 1000000000 | -y | 0 | 2000000000 |
| 5 | 0 | +x | 1000000000 | 3000000000 |
| 6 | 1000000000 | -y | 0 | 3000000000 |
| 7 | 0 | +x | 1000000000 | 4000000000 |

Answer:

```
4000000000
```

This trace demonstrates that the sequence may oscillate between two values. Whenever the upper bound blocks addition, subtraction becomes mandatory.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | One constant-time decision for each position |
| Space | $O(1)$ | Only a few variables are maintained |

Since the sum of all $n$ values across test cases is at most $2 \cdot 10^5$, the total running time is $O(2 \cdot 10^5)$. This is comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, B, x, y = map(int, input().split())

        cur = 0
        total = 0

        for _ in range(n):
            if cur + x <= B:
                cur += x
            else:
                cur -= y
            total += cur

        out.append(str(total))

    return "\n".join(out)

# provided sample
assert run(
"""3
5 100 1 30
7 1000000000 1000000000 1000000000
4 1 7 3
"""
) == """15
4000000000
-10"""

# minimum size
assert run(
"""1
1 1 1 1
"""
) == "1", "single move"

# boundary where addition exactly reaches B
assert run(
"""1
2 5 5 1
"""
) == "9", "equality with B is allowed"

# alternating behavior
assert run(
"""1
4 2 2 2
"""
) == "4", "repeated hit of upper bound"

# larger negative excursion
assert run(
"""1
3 1 5 3
"""
) == "-8", "must go negative first"

# large values
assert run(
"""1
7 1000000000 1000000000 1000000000
"""
) == "4000000000", "64-bit answer"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `1` | Smallest meaningful case |
| `2 5 5 1` | `9` | Equality with `B` is legal |
| `4 2 2 2` | `4` | Alternating add and subtract pattern |
| `3 1 5 3` | `-8` | Negative values are allowed |
| `7 10^9 10^9 10^9` | `4000000000` | Large answer size |

## Edge Cases

### Addition exactly reaches the bound

Input:

```
1
2 5 5 1
```

Trace:

```
0 -> 5 -> 4
```

The first move uses addition because $0 + 5 = 5$, which is still valid. Some incorrect implementations use a strict inequality and reject this move. The resulting sum is:

```
0 + 5 + 4 = 9
```

### Negative values are allowed

Input:

```
1
3 1 5 3
```

Trace:

```
0 -> -3 -> -6 -> -1
```

The first addition would exceed $B$, so subtraction is mandatory. The algorithm correctly allows the sequence to go below zero because the problem imposes no lower bound. The final sum is:

```
0 + (-3) + (-6) + (-1) = -8
```

### Large answers exceeding 32-bit range

Input:

```
1
7 1000000000 1000000000 1000000000
```

Trace:

```
0 -> 10^9 -> 0 -> 10^9 -> 0 -> 10^9 -> 0 -> 10^9
```

The answer is:

```
4000000000
```

Any implementation using 32-bit signed integers would overflow. The greedy algorithm itself remains correct, but the data type must be large enough to store the accumulated sum.
