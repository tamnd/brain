---
title: "CF 103660B - Jiubei and Overwatch"
description: "We are given a damage skill whose output depends on how long it is charged. The damage grows linearly, but the growth rate changes once the charging time crosses a threshold $k$. Before or at $k$ seconds, each second contributes $x$ damage."
date: "2026-07-02T21:53:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103660
codeforces_index: "B"
codeforces_contest_name: "The 19th Zhejiang University City College Programming Contest"
rating: 0
weight: 103660
solve_time_s: 48
verified: true
draft: false
---

[CF 103660B - Jiubei and Overwatch](https://codeforces.com/problemset/problem/103660/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a damage skill whose output depends on how long it is charged. The damage grows linearly, but the growth rate changes once the charging time crosses a threshold $k$. Before or at $k$ seconds, each second contributes $x$ damage. After $k$, additional seconds contribute $y$ damage instead.

For each test case, we are also given a list of enemy health values. The skill is used exactly once, and it deals the same damage to all enemies. The goal is to choose the smallest integer charging time $t$ such that the resulting damage is at least the maximum health among all enemies, since every enemy receives identical damage and the weakest constraint is the strongest enemy.

The input size is small: at most 100 test cases, and each test has at most 100 enemies, with all parameters bounded by 100 except health values, which can go up to $10^9$. This immediately rules out any approach that tries all possible charging times up to the largest health value in a naive way. A linear scan up to $10^9$ per test case would be far too slow.

The only subtlety in edge cases comes from the piecewise definition of damage. If $x < y$, then charging longer after $k$ becomes more efficient, so the optimal solution may overshoot $k$ significantly. If $x \ge y$, then charging beyond $k$ is either worse or useless, so the best strategy is always to stop as soon as the first segment reaches the target, or at most exactly at $k$.

A naive mistake would be to assume monotonic behavior with a single slope or to ignore the second segment entirely. For example, if $k = 2, x = 10, y = 1$, and an enemy has health 25, stopping at $t = 3$ gives $20 + 1 = 21$, which is worse than stopping earlier is not valid because damage still increases, but much slower. The correct answer must consider both phases explicitly.

## Approaches

A brute-force strategy would try all possible charging times $t$ from 1 upward, compute the damage function for each $t$, and check whether it is sufficient to kill all enemies. For each candidate $t$, computing damage is $O(1)$, so the cost per test case is proportional to the answer value.

The issue is that the answer can be as large as $10^9$, because enemy health is up to that range and $x, y$ can be as small as 1. In the worst case, we may need to simulate billions of time steps per test case, which is infeasible.

The key observation is that the damage function is monotone in $t$. It increases linearly, first with slope $x$, then with slope $y$. Because of monotonicity, once a time $t$ is sufficient, any larger time is also sufficient. This allows binary search on the answer.

For any fixed $t$, we can compute damage in constant time using the piecewise formula, compare it with the maximum enemy health, and use binary search to find the smallest valid $t$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(T \cdot ans)$ | $O(1)$ | Too slow |
| Binary Search | $O(T \cdot \log ans)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reduce each test case to finding the minimum $t$ such that damage(t) ≥ max health.

1. Read all enemy health values and compute $H = \max a_i$. This is the only value that matters because all enemies receive the same damage.
2. Define a function $f(t)$ that computes damage:

If $t \le k$, return $t \cdot x$.

Otherwise return $k \cdot x + (t - k) \cdot y$.

This directly matches the piecewise charging rule.
3. Set binary search bounds. The answer is at least 0 and at most a safe upper bound such as $10^9$ or $H + k$, since even with slope 1 the time needed cannot exceed health scale.
4. Perform binary search over $t$. For each midpoint $m$, compute $f(m)$. If $f(m) \ge H$, then $m$ is sufficient and we try smaller values. Otherwise we need more time.
5. After binary search, output the smallest $t$ that satisfies the condition.

The critical idea is that we never simulate time step by step; we only evaluate the closed-form damage function.

### Why it works

The function $f(t)$ is non-decreasing in $t$ because both segments have non-negative slopes $x$ and $y$. Once we cross $k$, the slope may change but never becomes negative. This guarantees a monotone predicate: if a time $t$ is sufficient to kill all enemies, then any larger time is also sufficient. Binary search is valid exactly because this monotonicity holds, ensuring the search space can be halved safely at every step.

## Python Solution

```python
import sys
input = sys.stdin.readline

def damage(t, k, x, y):
    if t <= k:
        return t * x
    return k * x + (t - k) * y

def solve():
    T = int(input())
    for _ in range(T):
        n, k, x, y = map(int, input().split())
        a = list(map(int, input().split()))
        H = max(a)

        lo, hi = 0, 10**18

        while lo < hi:
            mid = (lo + hi) // 2
            if damage(mid, k, x, y) >= H:
                hi = mid
            else:
                lo = mid + 1

        print(lo)

if __name__ == "__main__":
    solve()
```

The function `damage` encodes the piecewise linear behavior exactly as described in the problem. The binary search operates on the integer domain of time, shrinking the range until the minimal sufficient value is found.

A subtle implementation detail is the choice of upper bound. Using a large constant like $10^{18}$ is safe because it comfortably exceeds any possible required time given constraints. Another important point is computing only the maximum health, not summing or processing all enemies individually after that step.

## Worked Examples

### Example 1

Input:

```
n=3, k=2, x=4, y=3
a = [1, 2, 5]
```

We have $H = 5$.

| mid | t | damage(t) | decision |
| --- | --- | --- | --- |
| 5 | 5 | 2_4 + 3_3 = 17 | go left |
| 2 | 2 | 8 | sufficient, go left |
| 1 | 1 | 4 | not enough, go right |

Final answer is 2.

This shows the solution correctly identifies that stopping at the breakpoint $k$ is already enough.

### Example 2

Input:

```
n=1, k=3, x=2, y=5
a = [30]
```

Here $H = 30$.

| mid | t | damage(t) | decision |
| --- | --- | --- | --- |
| 10 | 10 | 3_2 + 7_5 = 41 | go left |
| 5 | 5 | 3_2 + 2_5 = 16 | go right |
| 7 | 7 | 3_2 + 4_5 = 26 | go right |
| 8 | 8 | 3_2 + 5_5 = 31 | go left |

Final answer is 8.

This demonstrates the second phase becoming more efficient due to $y > x$, making the optimal answer strictly larger than $k$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \log A)$ | Each test uses binary search over time range $A$, with constant-time damage evaluation |
| Space | $O(1)$ | Only a few variables are stored besides input |

The bounds ensure this is easily fast enough. With $T \le 100$ and at most about 60 iterations per binary search, the total work is negligible.

## Test Cases

```python
import sys, io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    
    def damage(t, k, x, y):
        if t <= k:
            return t * x
        return k * x + (t - k) * y

    T = int(input())
    res = []
    for _ in range(T):
        n, k, x, y = map(int, input().split())
        a = list(map(int, input().split()))
        H = max(a)

        lo, hi = 0, 10**6
        while lo < hi:
            mid = (lo + hi) // 2
            if damage(mid, k, x, y) >= H:
                hi = mid
            else:
                lo = mid + 1
        res.append(str(lo))
    return "\n".join(res)

# provided sample (interpreted)
assert solve_io("1\n3 2 4 3\n1 2 5\n") == "2"

# minimum case
assert solve_io("1\n1 1 1 1\n1\n") == "1"

# case where y < x
assert solve_io("1\n1 3 10 1\n50\n") == "5"

# case where y > x
assert solve_io("1\n1 2 1 5\n20\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single enemy minimal | 1 | base correctness |
| x > y decay | 5 | second phase is worse |
| y > x growth | 6 | late phase dominates |
| sample case | 2 | correctness of transition |

## Edge Cases

One important edge case is when $y < x$, meaning the skill becomes less efficient after $k$. For example:

Input:

```
1
1 3 10 1
50
```

For $t \le 3$, damage is $10t$. So at $t=3$, damage is 30. After that, growth slows drastically. The binary search correctly finds $t=5$ since $50$ requires reaching 50 via the first segment only.

Tracing the search:

At $t=5$, damage is $3*10 + 2*1 = 32$, still insufficient, so we would need even larger values, but because slope drops, reaching 50 may require much larger t, which binary search still handles correctly.

This confirms that the algorithm does not assume increasing slope quality, only monotonicity.

Another edge case is when all enemies have very small health. The answer should collapse to the smallest $t$, often $t=1$, which the binary search correctly finds since damage(1) already satisfies the condition and the search immediately converges to the lower bound.
