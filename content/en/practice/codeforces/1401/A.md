---
title: "CF 1401A - Distance and Axis"
description: "We are given a point $A$ placed on the integer number line at coordinate $n$. We are allowed to adjust this point one unit left or right per move."
date: "2026-06-11T08:40:59+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1401
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 665 (Div. 2)"
rating: 900
weight: 1401
solve_time_s: 95
verified: true
draft: false
---

[CF 1401A - Distance and Axis](https://codeforces.com/problemset/problem/1401/A)

**Rating:** 900  
**Tags:** constructive algorithms, math  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a point $A$ placed on the integer number line at coordinate $n$. We are allowed to adjust this point one unit left or right per move. After adjusting it to some final position $n'$, we want to choose another integer point $B$ on the same line such that the absolute difference between the distance from the origin to $B$, and the distance from $A$ to $B$, equals a fixed value $k$.

In simpler geometric terms, once we pick $n'$, we are asking whether there exists an integer $b$ such that:

$$\big||b| - |b - n'|\big| = k$$

If such a $b$ exists, the configuration is valid. Otherwise, we must move $A$ until it becomes possible, and we want the minimum number of moves.

The key difficulty is that validity depends only on the relationship between $n'$ and $k$, not on $b$ directly. So the real task is to understand for which values of $n'$ a solution exists.

The constraints are large, with up to $6000$ test cases and coordinates up to $10^6$. This immediately rules out any attempt to simulate possible positions of $B$ or try all configurations. Even a linear scan per test case would be too slow if it depends on $n$ or $k$.

A common failure case comes from misunderstanding symmetry of the expression. For example, assuming only $b = 0$ or $b = n'$ matters leads to incorrect conclusions, because the optimal $b$ depends on the relative ordering of $0$, $b$, and $n'$.

Another subtle issue is treating the expression as linear. The presence of absolute values creates piecewise behavior, so the condition splits into multiple geometric regions.

## Approaches

We first try to understand the brute-force idea. Fix a candidate position $n'$. Then we try all possible integer values of $b$ and check whether:

$$\big||b| - |b - n'|\big| = k$$

For each $b$, computing this is constant time, so for one $n'$ this is $O(M)$, where $M$ is the range of possible coordinates we consider. Since $n'$ itself can vary up to $10^6$, a full brute-force over both $n'$ and $b$ becomes on the order of $10^{12}$, which is completely infeasible.

The key observation is that we do not actually need to search over $b$. The expression represents a distance imbalance relative to the origin and point $n'$, and this structure has a known simplification: depending on the relative position of $b$, the expression collapses into linear forms. This leads to a characterization of when solutions exist purely in terms of $n'$ and $k$.

If we analyze the geometry, we find that valid configurations depend on whether we can place $n'$ so that it is not “too small” compared to $k$. Concretely, the condition reduces to:

$$n' \ge k \quad \text{or} \quad n' \equiv k \pmod{2}$$

More precisely, the standard simplification yields that the minimal adjustment depends only on how far $n$ is from the nearest valid value in the set:

$$\{x \mid x \ge k \text{ and } x \equiv k \ (\mathrm{mod}\ 2)\}$$

This reduces the problem to a simple nearest-point adjustment on the integer line.

So instead of exploring $b$, we reduce the problem to checking whether $n$ already satisfies the structural constraint, otherwise moving it minimally to the nearest valid integer.

### Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over $b$ and adjustments | $O(n^2)$ | $O(1)$ | Too slow |
| Parity + threshold reasoning | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

The correct solution can be derived from two constraints: a lower bound condition and a parity condition.

1. Compute whether the current position $n$ already satisfies $n \ge k$.

If it does, we only need to check parity compatibility. If not, we already know we must move upward to at least $k$, because any valid configuration requires sufficient “distance budget” to realize the absolute difference.
2. If $n < k$, the closest valid candidate is $k$ itself, so the answer is simply $k - n$.

This is because increasing $n$ preserves parity changes one-by-one, so the shortest path is direct movement to the threshold.
3. If $n \ge k$, compute the parity of $n$ and compare it with $k \mod 2$.

If they match, we can choose a suitable $b$ without further adjustment, so the answer is $0$.
4. If the parity does not match, we need one extra step to flip parity while staying above or equal to $k$. The nearest such value is either $n-1$ or $n+1$, and both keep us in the valid region. Hence the answer is $1$.

### Why it works

The expression $\big||b| - |b - n|\big|$ induces a piecewise linear structure depending on where $b$ lies relative to $0$ and $n$. When $n$ is large enough compared to $k$, the system always admits a solution, but only if the parity alignment allows the absolute-value symmetry to match exactly $k$. Otherwise, shifting $n$ by one toggles the parity without breaking feasibility, and no smaller adjustment is possible because parity flips only occur in unit steps.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())

    if n < k:
        print(k - n)
    else:
        if (n - k) % 2 == 0:
            print(0)
        else:
            print(1)
```

The implementation directly follows the derived conditions. The first branch handles the case where $n$ is below the feasibility threshold, forcing a linear increase. The second branch relies on parity alignment, which determines whether a valid $b$ can already be constructed.

A subtle point is that we check $(n - k) \% 2$ instead of separately checking $n \% 2$ and $k \% 2$, because only their relative parity matters. This avoids redundant logic and keeps the condition symmetric.

## Worked Examples

### Example 1: $n = 5, k = 8$

| Step | n | k | Condition | Action | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 8 | n < k | Move up | 3 |

Here, since the starting point is below the required threshold, we must move from 5 to 8. That takes 3 steps, and once we reach 8, a valid $b$ exists immediately.

### Example 2: $n = 4, k = 0$

| Step | n | k | Condition | Action | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 0 | n ≥ k | Check parity | 0 |

Since $k = 0$, any valid configuration only requires symmetry. The current position already allows a suitable $b$, so no movement is needed.

This example confirms that once $n \ge k$, feasibility depends only on structural compatibility, not magnitude.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ per test case | Each case uses only a couple of arithmetic checks |
| Space | $O(1)$ | No auxiliary structures are used |

With up to 6000 test cases, this constant-time approach easily fits within limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = []
    t = int(sys.stdin.readline())
    for _ in range(t):
        n, k = map(int, sys.stdin.readline().split())
        if n < k:
            out.append(str(k - n))
        else:
            out.append(str(0 if (n - k) % 2 == 0 else 1))
    return "\n".join(out)

# provided samples
assert run("""6
4 0
5 8
0 1000000
0 0
1 0
1000000 1000000
""") == """0
3
1000000
0
1
0"""

# custom cases
assert run("""1
0 5
""") == "5"

assert run("""1
10 10
""") == "0"

assert run("""1
7 2
""") == "1"

assert run("""1
8 2
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (0,5) | 5 | pure upward movement case |
| (10,10) | 0 | exact threshold alignment |
| (7,2) | 1 | parity mismatch above threshold |
| (8,2) | 0 | parity match above threshold |

## Edge Cases

One important boundary is when $k = 0$. In that case, the condition reduces to finding a point $b$ such that $|b| = |b - n|$, which always holds for some integer $b$ when $n$ is even-distance balanced. Under the algorithm, if $n \ge 0$, we directly check parity against $k = 0$. If $n$ is even, the answer is zero; otherwise one move suffices to flip parity.

Another edge case is when $n = 0$. If $k > 0$, we fall into the $n < k$ branch and move directly to $k$. For example, $n = 0, k = 1000000$ yields answer $1000000$, matching the need to reach the minimal feasible region.

A final edge case is when $n = k$. The algorithm treats this as zero cost because the parity condition becomes automatically satisfied, and the configuration already lies on the boundary where valid $b$ can be chosen.
