---
title: "CF 978E - Bus Video System"
description: "We are given a sequence of recorded changes in the number of passengers on a bus. Each value tells us how the passenger count changes after a stop, so if we denote the starting number of passengers by $x$, then after each stop we repeatedly add the given deltas and obtain a…"
date: "2026-06-17T01:23:31+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 978
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 481 (Div. 3)"
rating: 1400
weight: 978
solve_time_s: 71
verified: true
draft: false
---

[CF 978E - Bus Video System](https://codeforces.com/problemset/problem/978/E)

**Rating:** 1400  
**Tags:** combinatorics, math  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of recorded changes in the number of passengers on a bus. Each value tells us how the passenger count changes after a stop, so if we denote the starting number of passengers by $x$, then after each stop we repeatedly add the given deltas and obtain a running prefix sum process.

The bus has a hard constraint: at every moment, the number of passengers must stay between $0$ and $w$, inclusive. This applies not only after each recorded stop, but also immediately before the first stop (where the count is $x$).

The task is not to reconstruct one valid scenario, but to count how many integer values of the initial passenger count $x$ are valid so that all intermediate prefix sums remain within the allowed range.

The constraints already suggest that an $O(n)$ or $O(n \log n)$ solution is required. With $n \le 1000$, even an $O(n^2)$ approach might pass, but anything that tries to simulate all possible starting values directly across a wide range up to $10^9$ is impossible.

A key subtlety is that the initial value $x$ is not bounded by the input, only implicitly by feasibility. A naive reader might try to iterate over all possible starting values from $0$ to $w$, but the actual feasible range can shift outside that in intermediate states due to negative prefix sums.

One common failure case comes from ignoring intermediate constraints. For example, if prefix sums dip below zero, a starting value that looks valid globally may still violate constraints at some step. Similarly, if prefix sums exceed a certain range, that also invalidates the start. The correctness depends on tracking the entire prefix sum trajectory, not just its final value.

## Approaches

The core observation is that the passenger count at step $i$ can be written as:

$$x + p_i$$

where $p_i$ is the prefix sum of the recorded changes up to $i$.

Thus every constraint becomes:

$$0 \le x + p_i \le w$$

Rearranging gives an interval constraint on $x$:

$$-p_i \le x \le w - p_i$$

So each prefix sum contributes an interval of valid starting values. The final answer is the intersection of all these intervals over all $i$, including the implicit prefix sum $p_0 = 0$.

The brute-force idea would be to test every possible $x$ from $0$ to $w$ and simulate all steps, which costs $O(wn)$, far too large since $w$ can be $10^9$. The observation above turns the problem into maintaining an intersection of intervals, reducing everything to tracking only two values.

The intersection of all constraints is itself a single interval $[L, R]$, updated incrementally. Each prefix sum narrows this interval. If at any point the interval becomes empty, no valid starting value exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nw)$ | $O(1)$ | Too slow |
| Interval intersection | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We define $p$ as the running prefix sum of changes.

1. Initialize $p = 0$, and set the valid range for $x$ as $L = 0$, $R = w$. This reflects the fact that initially the bus must already satisfy the capacity constraint.
2. For each recorded change $a_i$, update the prefix sum $p = p + a_i$. This represents the net shift from the initial state to step $i$.
3. Convert the condition $0 \le x + p \le w$ into constraints on $x$, producing the interval $[-p, w - p]$.
4. Intersect this interval with the current valid range:

$L = \max(L, -p)$, $R = \min(R, w - p)$.

This ensures we only keep starting values that satisfy all constraints so far.
5. If at any point $L > R$, stop early because no valid initial value exists.
6. After processing all steps, the answer is $R - L + 1$, since all integers in the final interval are valid starting passenger counts.

### Why it works

Each step imposes a linear constraint on the initial value $x$. Since all constraints are of the form $x \in [\ell_i, r_i]$, the valid set is the intersection of intervals. Intersection of intervals is associative and can be maintained incrementally without losing information. The algorithm preserves exactly the set of all feasible starting values after each step, so no valid solution is ever discarded and no invalid one is introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, w = map(int, input().split())
    a = list(map(int, input().split()))

    prefix = 0
    L, R = 0, w

    for x in a:
        prefix += x

        L = max(L, -prefix)
        R = min(R, w - prefix)

        if L > R:
            print(0)
            return

    print(max(0, R - L + 1))

if __name__ == "__main__":
    solve()
```

The implementation keeps a single running prefix sum and updates the feasible range at each step. The bounds $L$ and $R$ always represent the intersection of all constraints seen so far. The early exit when $L > R$ avoids unnecessary computation once feasibility is broken.

A subtle point is ensuring that the final answer is clamped correctly: if constraints are consistent, $R - L + 1$ counts all integer initial values. If inconsistencies arise, the function already returns zero.

## Worked Examples

### Example 1

Input:

```
3 5
2 1 -3
```

We track prefix sums and intervals.

| Step | a_i | prefix p | valid interval for x [-p, w-p] | current [L, R] |
| --- | --- | --- | --- | --- |
| init | - | 0 | [0, 5] | [0, 5] |
| 1 | 2 | 2 | [-2, 3] | [0, 3] |
| 2 | 1 | 3 | [-3, 2] | [0, 2] |
| 3 | -3 | 0 | [0, 5] | [0, 2] |

Final answer is $2 - 0 + 1 = 3$.

This trace shows how constraints progressively shrink the feasible starting interval without needing to enumerate any initial values.

### Example 2

Input:

```
4 4
1 2 -1 -2
```

| Step | a_i | prefix p | interval [-p, w-p] | [L, R] |
| --- | --- | --- | --- | --- |
| init | - | 0 | [0, 4] | [0, 4] |
| 1 | 1 | 1 | [-1, 3] | [0, 3] |
| 2 | 2 | 3 | [-3, 1] | [0, 1] |
| 3 | -1 | 2 | [-2, 2] | [0, 1] |
| 4 | -2 | 0 | [0, 4] | [0, 1] |

Answer is $2$, corresponding to starting values $0$ and $1$.

This example shows that even when the final prefix sum returns to zero, intermediate constraints still restrict the valid initial values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each stop updates prefix sum and interval once |
| Space | $O(1)$ | Only prefix sum and two bounds are stored |

The linear scan over at most 1000 elements is easily fast enough, and no additional data structures are required.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isfinite

    n, w = map(int, sys.stdin.readline().split())
    a = list(map(int, sys.stdin.readline().split()))

    prefix = 0
    L, R = 0, w

    for x in a:
        prefix += x
        L = max(L, -prefix)
        R = min(R, w - prefix)
        if L > R:
            return "0\n"

    return str(max(0, R - L + 1)) + "\n"

# provided sample
assert run("3 5\n2 1 -3\n") == "3\n"

# all zero changes
assert run("4 10\n0 0 0 0\n") == "11\n"

# immediate overflow
assert run("2 3\n5 -10\n") == "0\n"

# tight range
assert run("3 4\n1 2 -1\n") == "2\n"

# boundary case
assert run("1 0\n0\n") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zero changes | 11 | full range remains valid |
| immediate overflow | 0 | early infeasibility detection |
| tight range | 2 | interval shrinking correctness |
| boundary case w=0 | 1 | handling degenerate capacity |

## Edge Cases

One edge case occurs when all changes are zero. In that situation, prefix sums remain zero throughout, so every starting value from $0$ to $w$ is valid. The algorithm keeps $L=0$ and $R=w$ unchanged, producing $w+1$, which matches the correct count.

Another edge case is when constraints become impossible immediately. For example, if $w = 3$ and the first change is $+5$, then the prefix sum is already outside the feasible range for any starting value. The interval becomes $[L, R] = [0, 3] \cap [-5, -2]$, which is empty, and the algorithm correctly outputs zero without further processing.

A final subtle case is when intermediate prefix sums force constraints that are not visible from the final sum. The second worked example demonstrates this: even though the total change is small, intermediate accumulation restricts valid starts. The interval intersection approach captures this automatically because it evaluates constraints at every prefix, not only at the end.
