---
title: "CF 1036A - Function Height"
description: "The figure is a broken line made from points at integer x-coordinates from 0 to 2n. Initially every point lies on the x-axis, so every y-coordinate is zero. The only way to modify the shape is to pick an odd-indexed point and increase its height by one unit per move."
date: "2026-06-16T19:03:00+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1036
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 50 (Rated for Div. 2)"
rating: 1000
weight: 1036
solve_time_s: 360
verified: true
draft: false
---

[CF 1036A - Function Height](https://codeforces.com/problemset/problem/1036/A)

**Rating:** 1000  
**Tags:** math  
**Solve time:** 6m  
**Verified:** yes  

## Solution
## Problem Understanding

The figure is a broken line made from points at integer x-coordinates from 0 to 2n. Initially every point lies on the x-axis, so every y-coordinate is zero. The only way to modify the shape is to pick an odd-indexed point and increase its height by one unit per move. Even-indexed points are never changed.

Once heights are assigned, consecutive points are connected by straight segments, forming a polygonal chain. The “area of the plot” is the geometric area between this chain and the x-axis. The “height of the plot” is simply the maximum y-value among all points.

The task is to choose how many times to increase each odd-indexed point so that the total enclosed area becomes exactly k, while making the maximum height as small as possible.

The constraints allow both n and k up to 10^18. That immediately rules out any approach that tries to simulate increments or build the structure explicitly. Any solution must compress the problem into a closed-form expression or at worst a logarithmic or constant-time computation.

A subtle edge case arises from interpreting the geometry correctly. A naive reader might think the area depends on the shape of each segment in a complicated way, or that interactions between neighboring odd points matter. For example, one might suspect that increasing adjacent odd points changes shared segment contributions in a nontrivial way. If that were true, even small inputs would require careful geometric accumulation. However, this intuition leads to overcomplication and incorrect dynamic formulations.

Another potential pitfall is assuming that distributing height changes unevenly could somehow reduce the maximum height more efficiently than uniform distribution. This often leads to incorrect greedy strategies like filling one point fully before moving to the next, which can appear optimal locally but fails globally.

## Approaches

The brute-force idea is to treat each odd-indexed point as a variable and simulate distributing unit increments among them. Each increment updates the geometry and we recompute total area after every assignment. This would require exploring all distributions of k increments across n positions. The number of states is combinatorial, essentially the number of weak compositions of k into n parts, which grows on the order of $\binom{k+n-1}{n-1}$. Even for moderate values this is completely infeasible.

The key simplification comes from observing how area is formed. Each segment connects either a zero-height point to an odd point or vice versa. Because even-indexed points always stay at zero, every “bump” created by an odd-indexed point forms two identical triangular contributions, one on each adjacent segment. These two halves combine into a single linear contribution proportional only to the height of that odd point. This removes all interaction between positions.

Once the area is seen to be a pure sum of independent contributions, the problem becomes purely combinatorial: we are distributing k identical units across n independent buckets, and we want to minimize the maximum bucket value. This is a classic load-balancing structure where optimality is achieved by equalizing as much as possible.

If we try to keep the maximum height at H, then each of the n odd positions can contribute at most H to the total area, so the maximum achievable area is n·H. This immediately gives a feasibility condition for H.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Distribution | Exponential in k | O(n) | Too slow |
| Optimal Equal Distribution | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Interpret each odd-indexed point as an independent variable $a_i$, representing how many times it is increased. This transforms the geometric problem into an allocation problem over n variables.
2. Compute how each $a_i$ contributes to area. Each unit increase at an odd point increases area by exactly one unit in total, because it forms two symmetric half-triangles across adjacent segments. This establishes that total area equals $\sum a_i$.
3. Reformulate the problem as distributing k identical units among n variables $a_1, a_2, \dots, a_n$, where the objective is to minimize $\max a_i$.
4. Observe that for a fixed maximum height H, the largest possible sum occurs when all variables equal H, giving total n·H. This means feasibility requires $n \cdot H \ge k$.
5. Choose the smallest integer H satisfying this inequality, since any smaller value cannot accommodate k, and any larger value is unnecessary.
6. Conclude that $H = \lceil k / n \rceil$.

### Why it works

The key invariant is that the area depends only on the multiset of odd-index heights and is exactly their sum. Because there is no coupling between variables, any redistribution that preserves the total sum does not change the area. Therefore, minimizing the maximum under a fixed sum reduces to balancing the distribution as evenly as possible. Any deviation from uniformity only increases the maximum without increasing capacity beyond the same total sum bound.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
print((k + n - 1) // n)
```

The entire implementation reduces to computing a ceiling division. The key simplification is that the geometry collapses into an additive model, so no simulation or structure building is required. The only careful detail is ensuring integer ceiling division is implemented correctly; using `(k + n - 1) // n` avoids floating-point issues and handles large values up to 10^18 safely.

## Worked Examples

### Example 1

Input:

```
4 3
```

We have n = 4 odd positions contributing independently. We distribute 3 units among 4 variables.

| Step | Distribution state | Current max | Total sum |
| --- | --- | --- | --- |
| 1 | [1,0,0,0] | 1 | 1 |
| 2 | [1,1,0,0] | 1 | 2 |
| 3 | [1,1,1,0] | 1 | 3 |

The maximum height needed is 1 because all units can be placed without exceeding 1 per position. This matches the formula ceil(3/4) = 1.

### Example 2

Input:

```
4 12
```

Now we distribute 12 units across 4 positions.

| Step | Distribution state | Current max | Total sum |
| --- | --- | --- | --- |
| 1 | [3,3,3,3] | 3 | 12 |

Here the distribution is perfectly balanced, so maximum height is 3. This matches ceil(12/4) = 3 and shows the tight case where all variables must reach the same level.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations are performed |
| Space | O(1) | No additional data structures are used |

The solution is constant time, which is necessary given that both n and k can be as large as 10^18. Any iterative or simulation-based approach would be impossible under these constraints.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    n, k = map(int, input().split())
    print((k + n - 1) // n)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.strip()

# provided sample
assert run("4 3\n") == "1"

# minimum case
assert run("1 1\n") == "1"

# evenly divisible
assert run("5 10\n") == "2"

# large skew case
assert run("3 1000000000000000000\n") == str((10**18 + 2)//3)

# k smaller than n
assert run("10 3\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | smallest nontrivial case |
| 5 10 | 2 | even distribution |
| 3 10^18 | ceil division correctness | large boundary values |
| 10 3 | 1 | k < n behavior |

## Edge Cases

A common misunderstanding is when k is smaller than n. For example, with input `n = 10, k = 3`, the optimal strategy is to place each unit in a different position, producing heights like `[1,1,1,0,...]`, so the maximum height is 1. The formula correctly returns `ceil(3/10) = 1`, matching this intuition.

Another edge case is when k is exactly divisible by n, such as `n = 5, k = 10`. The optimal configuration is perfectly uniform, with every odd point set to 2. The algorithm returns 2 exactly, and no uneven distribution can reduce the maximum further without violating the sum constraint.

Finally, when k is extremely large, such as 10^18, the solution still works because it avoids constructing any distribution and relies only on integer arithmetic, ensuring no overflow or performance issues.
