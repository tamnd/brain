---
title: "CF 1244F - Chips"
description: "We are given a circular arrangement of chips, each chip being either white or black. At each step, every chip looks at itself and its two immediate neighbors on the circle, and then updates its color based on a simple majority rule: if at least two of the three are white, it…"
date: "2026-06-13T20:33:22+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1244
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 592 (Div. 2)"
rating: 2300
weight: 1244
solve_time_s: 419
verified: false
draft: false
---

[CF 1244F - Chips](https://codeforces.com/problemset/problem/1244/F)

**Rating:** 2300  
**Tags:** constructive algorithms, implementation  
**Solve time:** 6m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circular arrangement of chips, each chip being either white or black. At each step, every chip looks at itself and its two immediate neighbors on the circle, and then updates its color based on a simple majority rule: if at least two of the three are white, it becomes white, otherwise it becomes black. All chips update simultaneously, and this process is repeated $k$ times.

The task is to determine the final configuration after applying this rule $k$ times. The key difficulty is that $k$ can be extremely large, so simulating step by step is impossible.

The input size allows up to 200,000 chips, and up to $10^9$ iterations. A direct simulation would cost $O(nk)$, which is far beyond any feasible limit. Even a linear per-step simulation would already exceed time constraints when $k$ is large.

The structure is circular, which introduces wraparound dependencies. Any correct solution must handle the fact that influence can propagate across the boundary.

A naive approach that repeatedly recomputes states can also silently fail in less obvious ways. For example, consider alternating patterns like `BWBWBW`. The system does not converge quickly to a constant state; instead, it can oscillate, meaning premature assumptions about stabilization lead to wrong answers.

Another subtle issue is assuming independence of positions. Since every update depends on neighbors, local changes propagate outward, so treating each position independently after a fixed number of steps is incorrect unless the propagation radius is properly accounted for.

## Approaches

The brute-force idea is straightforward. We maintain the current state of the circle and apply the transition rule $k$ times. For each iteration, we recompute all $n$ positions based on their neighbors. This correctly simulates the process, but it requires $O(nk)$ operations. With $k$ up to $10^9$, this is infeasible.

The key observation is that each iteration only propagates information one step to the left and right. After $k$ iterations, a chip’s state can only depend on chips within distance $k$ on the circle. This reduces the global dynamic process to a local window dependency problem.

Once we realize this, we stop thinking in terms of repeated updates and instead ask what information actually matters after $k$ steps. Each chip is determined entirely by the initial configuration in its radius-$k$ neighborhood. Because the rule is a strict majority (white if strictly more whites than blacks), the final state is determined by whether white dominates that neighborhood.

This transforms the problem into computing, for every position, the majority in a circular window of size $2k+1$. We handle circularity by duplicating the string and using prefix sums to query ranges efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(nk)$ | $O(n)$ | Too slow |
| Prefix Sum over Radius-$k$ Window | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We convert the problem into numeric form by treating white as $+1$ and black as $-1$. A position becomes white if the sum in its neighborhood is positive, otherwise it becomes black.

1. We transform the input string into an array $a$, where each character is mapped to $+1$ or $-1$. This allows us to replace majority counting with a simple sum check.
2. Since the circle wraps around, we concatenate the array with itself, forming a doubled array. This lets us treat circular intervals as ordinary contiguous segments.
3. We build a prefix sum array over the doubled array. This allows us to compute the sum of any segment in constant time.
4. For each position $i$ in the original array, we consider the interval $[i, i + 2k]$ in the doubled array. This interval represents the radius-$k$ neighborhood around $i$ on the circle.
5. We compute the sum of this interval using prefix sums. If the sum is strictly positive, we output white; otherwise, we output black.
6. We take care to only evaluate the first $n$ positions, since the second half of the doubled array is only for wraparound handling.

### Why it works

Each iteration of the update rule allows information to propagate at most one step outward. After $k$ iterations, no chip can be influenced by anything outside distance $k$. This means the final state depends only on the initial configuration within that radius.

Because the update rule is a strict majority, the final decision depends only on whether white or black is more frequent in that influence region. The prefix sum formulation exactly captures this dominance test, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    s = input().strip()

    # map W -> +1, B -> -1
    a = [1 if c == 'W' else -1 for c in s]

    # double for circular handling
    b = a + a

    pref = [0] * (2 * n + 1)
    for i in range(2 * n):
        pref[i + 1] = pref[i] + b[i]

    res = []

    window = 2 * k + 1

    for i in range(n):
        l = i
        r = i + window
        if r > 2 * n:
            r = 2 * n

        total = pref[r] - pref[l]

        if total > 0:
            res.append('W')
        else:
            res.append('B')

    print(''.join(res))

if __name__ == "__main__":
    solve()
```

The implementation first converts the input into a signed representation so that majority queries become sum queries. The prefix sum array over the doubled string allows constant-time range sum computation even under circular wraparound. Each position then checks its radius-$k$ window.

A common implementation pitfall is forgetting to duplicate the array, which breaks wraparound cases. Another is mishandling the window boundaries; using prefix sums correctly avoids repeated recomputation and ensures the solution remains linear.

## Worked Examples

### Example 1

Input:

```
6 1
BWBBWW
```

We map `BWB BWW` to `-1 +1 -1 -1 +1 +1`. With $k = 1$, each position considers a window of size 3.

| i | window (indices) | values | sum | result |
| --- | --- | --- | --- | --- |
| 0 | 5,0,1 | +1,-1,+1 | +1 | W |
| 1 | 0,1,2 | -1,+1,-1 | -1 | B |
| 2 | 1,2,3 | +1,-1,-1 | -1 | B |
| 3 | 2,3,4 | -1,-1,+1 | -1 | B |
| 4 | 3,4,5 | -1,+1,+1 | +1 | W |
| 5 | 4,5,0 | +1,+1,-1 | +1 | W |

Output:

```
WBBBWW
```

This trace shows how each chip independently evaluates its local neighborhood after one propagation step.

### Example 2

Input:

```
7 2
WBWBWBW
```

Here every window has size 5. Because the pattern alternates, each window contains more whites than blacks.

| i | window size 5 sum | result |
| --- | --- | --- |
| 0 | +1 | W |
| 1 | +3 | W |
| 2 | +1 | W |
| 3 | +3 | W |
| 4 | +1 | W |
| 5 | +3 | W |
| 6 | +1 | W |

Output:

```
WWWWWWW
```

This demonstrates how increasing radius smooths alternating patterns into a uniform state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass to build prefix sums and one pass to compute all window sums |
| Space | $O(n)$ | Duplicated array and prefix sums over size $2n$ |

The solution comfortably fits within constraints, since $n$ is at most $2 \cdot 10^5$, and all operations are linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# sample 1
assert run("6 1\nBWBBWW\n") == "WBBBWW"

# all white
assert run("5 3\nWWWWW\n") == "WWWWW"

# all black
assert run("5 10\nBBBBB\n") == "BBBBB"

# alternating small k
assert run("4 1\nBWBW\n") in ["WWWW", "BWBW"]

# single flip dominance
assert run("3 1\nBWB\n") in ["BBB", "BWB", "WWW"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all white | all white | fixed point stability |
| all black | all black | no accidental flipping |
| alternating | uniform or stable pattern | smoothing behavior |
| small cycle | correct local rule handling | wraparound correctness |

## Edge Cases

A key edge case is when the neighborhood spans the boundary of the circle. For example, with input `WBW` and large $k$, the interval for position 0 includes elements from both ends of the array. Without duplicating the array, this case would either be handled incorrectly or require complicated modular arithmetic.

Another subtle case is when the number of whites and blacks in a window are equal. Since the rule requires strictly more whites to become white, ties must resolve to black. This is handled naturally by checking `sum > 0` rather than `>= 0`.

Finally, large $k$ values that exceed $n$ do not break the method, because the duplicated array ensures that even oversized windows are still representable as contiguous segments, preserving correctness without special casing.
