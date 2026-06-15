---
title: "CF 1303B - National Project"
description: "We are building a road of length $n$, where each unit of road must eventually be asphalted exactly once. The construction proceeds day by day, and on each day we may either work on exactly one unit or do nothing. The weather is periodic."
date: "2026-06-16T05:41:22+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1303
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 82 (Rated for Div. 2)"
rating: 1400
weight: 1303
solve_time_s: 213
verified: false
draft: false
---

[CF 1303B - National Project](https://codeforces.com/problemset/problem/1303/B)

**Rating:** 1400  
**Tags:** math  
**Solve time:** 3m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are building a road of length $n$, where each unit of road must eventually be asphalted exactly once. The construction proceeds day by day, and on each day we may either work on exactly one unit or do nothing.

The weather is periodic. It starts with a block of $g$ good days, followed by $b$ bad days, and this pattern repeats forever. The process always begins on a good day. If we lay asphalt on a good day, that unit becomes high quality; if we lay it on a bad day, it becomes low quality. Skipping a day does not advance construction but still advances the calendar.

The goal is not to minimize cost or time in a naive sense, but to minimize total days needed so that all $n$ units are completed, with the extra constraint that at least half of them must be high quality. The required number of high quality units is $\lceil n/2 \rceil$.

The constraint $n, g, b \le 10^9$ and $T \le 10^4$ rules out any simulation over days. Even simulating a single test case up to the answer scale is impossible, since the answer itself can be on the order of $10^{18}$. The solution must rely on a direct mathematical characterization of how many good days appear in a prefix of time.

A subtle issue appears when good days are scarce compared to bad days. A naive greedy strategy like “always work on good days and fill the rest with bad days” can mislead intuition because skipping changes alignment with the periodic structure. Another failure case is assuming we can independently choose which days are used as good without respecting their fixed periodic positions.

## Approaches

A brute force interpretation would simulate day by day, tracking whether each day is good or bad and counting how many good-quality and total units we have built. We would stop once we reach $n$ units and check if at least half are high quality. This works conceptually because it directly follows the process definition, but it requires potentially iterating until the answer time, which can be extremely large. In worst cases, when good days are rare and we frequently skip or waste alignment, the simulation can grow to $O(\text{answer})$, which is far beyond limits.

The key observation is that we never benefit from completing fewer total units if we already have enough good opportunities earlier. Instead, the structure depends only on how many good days occur in the first $d$ days of the calendar. Because the pattern is perfectly periodic, we can compute the number of good days in any prefix without simulation.

For any prefix of $d$ days, we have full cycles of length $g+b$, and each cycle contributes exactly $g$ good days. The remainder contributes $\min(g, d \bmod (g+b))$ good days. Thus:

$$\text{good}(d) = \left\lfloor \frac{d}{g+b} \right\rfloor g + \min(g, d \bmod (g+b))$$

Now the construction problem becomes: find the smallest $d$ such that we can place $n$ total units in $d$ days, while ensuring at least $\lceil n/2 \rceil$ of those placements fall on good days. Since we can always work on any day, total placements in $d$ days is simply $d$, so we only need $d \ge n$, and the real constraint is whether good days in the first $d$ days are at least $\lceil n/2 \rceil$. If not, we must extend $d$ until enough good days appear.

Thus the problem reduces to a binary search on $d$, checking a monotone condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(\text{answer})$ | $O(1)$ | Too slow |
| Binary Search + arithmetic counting | $O(T \log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We focus on a single test case.

1. Compute the required number of high-quality units as $need = \lceil n/2 \rceil$. This is the minimum number of good days we must “cover” with asphalt placement.
2. Define a function $good(d)$ that returns how many good days appear in the first $d$ days using cycle arithmetic. This avoids simulation and directly uses periodic structure.
3. Check whether a given $d$ is sufficient: it must satisfy both $d \ge n$ (we must have at least enough days to lay all units) and $good(d) \ge need$ (enough good-quality placements exist).
4. Use binary search over $d$ in a large range, typically $[1, 10^{18}]$, because the answer can be very large when bad days dominate.
5. For each midpoint, evaluate the condition. If it is feasible, move left; otherwise move right. We are searching for the smallest feasible day count.
6. Output the first $d$ that satisfies both constraints.

The reason binary search is valid is that increasing $d$ can only increase the number of good days and total available slots, so feasibility is monotone.

### Why it works

The core invariant is that feasibility depends only on prefix length and not on scheduling choices. For any fixed $d$, we always have exactly $d$ opportunities to place asphalt, and exactly $good(d)$ of those are good-quality opportunities. Since we can choose which units to assign to which days, the only limitation is whether enough good days exist to satisfy the required count. Once a prefix is feasible, any larger prefix remains feasible because both total and good counts are non-decreasing.

## Python Solution

```python
import sys
input = sys.stdin.readline

def good_days(d, g, b):
    cycle = g + b
    full = d // cycle
    rem = d % cycle
    return full * g + min(g, rem)

def solve():
    T = int(input())
    for _ in range(T):
        n, g, b = map(int, input().split())
        need = (n + 1) // 2

        lo, hi = 1, 10**18
        ans = hi

        while lo <= hi:
            mid = (lo + hi) // 2
            if mid >= n and good_days(mid, g, b) >= need:
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        print(ans)

if __name__ == "__main__":
    solve()
```

The function `good_days` implements the periodic counting formula directly. The binary search enforces the two constraints simultaneously: enough total days to finish the road and enough good days to satisfy the quality requirement.

A common pitfall is forgetting the `mid >= n` condition. Without it, the search may return a prefix that has enough good days but not enough total days to complete construction.

## Worked Examples

### Example 1

Input:

```
5 1 1
```

We need $need = 3$. Good days alternate every cycle of 2.

| d | cycle full | rem | good(d) | d ≥ n | feasible |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | no | no |
| 3 | 1 | 1 | 2 | yes | no |
| 5 | 2 | 1 | 3 | yes | yes |

The first feasible point is $d = 5$. This shows that even though good days are sparse, waiting longer aligns enough good days with required placements.

### Example 2

Input:

```
8 10 10
```

Here $g \ge n$, so every day in the first block is good.

| d | cycle full | rem | good(d) | d ≥ n | feasible |
| --- | --- | --- | --- | --- | --- |
| 8 | 0 | 8 | 8 | yes | yes |

The answer is 8 immediately, since all required units can be placed in good days without needing to extend into bad periods.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T \log n)$ | Each test case performs binary search over up to $10^{18}$ with constant-time good day computation |
| Space | $O(1)$ | Only arithmetic variables are stored |

The logarithmic factor is small enough for $10^4$ test cases, and all operations are integer arithmetic, so the solution easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import ceil

    def good_days(d, g, b):
        cycle = g + b
        full = d // cycle
        rem = d % cycle
        return full * g + min(g, rem)

    def solve():
        T = int(input())
        for _ in range(T):
            n, g, b = map(int, input().split())
            need = (n + 1) // 2

            lo, hi = 1, 10**18
            ans = hi

            while lo <= hi:
                mid = (lo + hi) // 2
                if mid >= n and good_days(mid, g, b) >= need:
                    ans = mid
                    hi = mid - 1
                else:
                    lo = mid + 1

            print(ans)

    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("3\n5 1 1\n8 10 10\n1000000 1 1000000\n") == "5\n8\n499999500000"

# minimum input
assert run("1\n1 1 1\n") == "1"

# all good days dominate
assert run("1\n10 100 1\n") == "10"

# equal pattern boundary
assert run("1\n6 2 2\n") == "6"

# bad-heavy stress
assert run("1\n5 1 1000000000\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 | minimal edge case |
| 10 100 1 | 10 | abundant good days |
| 6 2 2 | 6 | balanced cycle boundary |
| 5 1 1e9 | 5 | extreme bad dominance |

## Edge Cases

When $g \ge n$, all required good units can be placed inside the first block of good days. The algorithm handles this because $good(n) = n$, making the binary search settle immediately at $d = n$.

When $g \ll b$, good days are extremely sparse and most cycles are wasted. The binary search expands $d$ until enough cycles accumulate, and the arithmetic formula correctly counts partial cycles without needing simulation.

When $n = 1$, the requirement is trivial, and the first day always works since the sequence starts on a good day, so $good(1) = 1$.
