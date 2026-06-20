---
title: "CF 106398G - \u0412\u0430\u0441\u044f \u0438 \u0442\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0438"
description: "We are given a sequence of scheduled training sessions. Ideally, there are $n$ sessions, but Vasya may skip some of them. Every skipped session is not lost: it must be compensated later at a future visited session."
date: "2026-06-20T23:08:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106398
codeforces_index: "G"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u043d\u0430 \u0412\u041a\u041e\u0428\u041f.Junior 2026"
rating: 0
weight: 106398
solve_time_s: 46
verified: true
draft: false
---

[CF 106398G - \u0412\u0430\u0441\u044f \u0438 \u0442\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0438](https://codeforces.com/problemset/problem/106398/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of scheduled training sessions. Ideally, there are $n$ sessions, but Vasya may skip some of them. Every skipped session is not lost: it must be compensated later at a future visited session. If a missed session $i$ is compensated at session $j$, the effort cost is $j - i + 1$, and this already includes the training done on day $j$ itself.

Vasya is allowed to skip any number of sessions, and he can compensate multiple missed sessions in a single visit. However, the total accumulated effort across all compensations cannot exceed $k$. The goal is to minimize how many sessions Vasya actually attends while still ensuring all $n$ sessions are eventually compensated within the total effort budget.

What matters is not the exact schedule but how skipped sessions are grouped and where they are eventually paid off. If a long block of consecutive sessions is skipped and only later attended once, the cost becomes large because earlier missed sessions accumulate increasing penalties.

The input gives two integers $n$ and $k$, and the output is the minimum number of visited sessions such that all missed sessions can be compensated without exceeding total effort $k$.

The constraints reach up to $10^{18}$, so any solution depending on linear or quadratic iteration over $n$ is impossible. We need a purely mathematical or greedy structure that reduces the problem to a closed-form condition or logarithmic search.

A key edge case is when Vasya attends almost all sessions. A naive assumption might be that attending $n-1$ sessions always works, but the cost can still exceed $k$ depending on how the skipped session is positioned. Another subtle case is when all skipped sessions are grouped at the beginning or at the end, since that minimizes or maximizes the cost in very different ways.

## Approaches

A brute-force strategy would try all subsets of attended sessions. For each subset, we simulate which sessions are skipped, then assign each skipped session to some later attended session to minimize cost and check if the total cost stays within $k$. This is correct because it directly follows the rules, but the number of subsets is $2^n$, and even for moderate $n$ this is completely infeasible.

The key observation is that the optimal structure is not arbitrary. If we fix the number of attended sessions, the best arrangement is to spread them in a way that minimizes accumulated compensation cost. The cost structure depends only on relative gaps between attended sessions, and the worst penalties come from long consecutive skipped segments. This turns the problem into analyzing how large a block of skipped sessions can be “absorbed” under budget $k$.

If we think in reverse, suppose Vasya attends only $m$ sessions. Then there are $n - m$ skipped sessions, and the total cost is minimized when these skipped sessions are grouped as tightly as possible and compensated in an optimal order. This reduces the problem into a combinatorial cost function over block sizes rather than explicit scheduling.

The hidden structure is that optimal strategies always behave greedily in terms of grouping skips, and the cost becomes a function of how many sessions are attended, not which ones. This allows us to derive a monotone condition and search for the minimum number of attended sessions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | exponential | exponential | Too slow |
| Structural + monotone analysis | $O(1)$ or $O(\log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reinterpret the problem in terms of how many sessions are skipped. Let $x$ be the number of sessions Vasya skips, so he attends $n - x$ sessions. The goal is to determine the maximum $x$ such that all skipped sessions can be compensated within cost $k$.

1. We first observe that the cost depends only on how skipped sessions are paired with later attended sessions. To minimize cost, every skipped session should be compensated as early as possible, because cost grows linearly with delay.
2. We arrange the schedule so that attended sessions are evenly distributed as “anchor points” that absorb skipped sessions. Each anchor can compensate a block of skipped sessions, and the cost within each block follows an arithmetic structure based on distances.
3. For a fixed number of skipped sessions $x$, the minimal possible cost is achieved when these skipped sessions form a single continuous prefix, because this minimizes average distance to the first available attended session. Any fragmentation would only increase distances.
4. Under this optimal arrangement, the cost becomes a triangular structure: skipped sessions contribute $1 + 2 + \dots + x$, which equals $x(x+1)/2$, because each skipped session is eventually matched to the next available attended session in the best possible way.
5. We now solve the inequality $x(x+1)/2 \le k$. This gives the maximum number of skips allowed. We then compute the answer as $n - x$.

### Why it works

The key invariant is that the cost function depends only on relative ordering between skipped and attended sessions, not their absolute labels. Any configuration of skips can be transformed into a contiguous block without increasing cost. Once reduced to this canonical form, the cost becomes a pure prefix sum structure, which is uniquely minimized by grouping skips together. This makes the triangular number bound both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    lo, hi = 0, n

    def cost(x):
        return x * (x + 1) // 2

    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cost(mid) <= k:
            lo = mid
        else:
            hi = mid - 1

    skipped = lo
    print(n - skipped)

if __name__ == "__main__":
    solve()
```

The solution performs a binary search over the number of skipped sessions. The helper function computes the triangular cost of a given number of skips. We search for the largest feasible number of skips whose cost does not exceed $k$, and subtract it from $n$ to obtain the minimum number of attended sessions.

The binary search is safe because the cost function $x(x+1)/2$ is strictly increasing in $x$, ensuring monotonicity of feasibility.

## Worked Examples

### Example 1

Input:

```
5 7
```

We test possible values of skipped sessions:

| x (skipped) | cost x(x+1)/2 | valid |
| --- | --- | --- |
| 0 | 0 | yes |
| 1 | 1 | yes |
| 2 | 3 | yes |
| 3 | 6 | yes |
| 4 | 10 | no |

Maximum valid skipped sessions is 3, so answer is $5 - 3 = 2$.

This shows that even though Vasya can skip most sessions, cost grows quadratically.

### Example 2

Input:

```
5 15
```

| x | cost |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 3 |
| 3 | 6 |
| 4 | 10 |
| 5 | 15 |

Here all 5 sessions can be skipped, so minimum attended sessions is 0.

This demonstrates the boundary case where budget exactly matches full triangular cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log n)$ | binary search over number of skipped sessions |
| Space | $O(1)$ | only arithmetic variables used |

The solution easily handles $n, k \le 10^{18}$ because it avoids iteration over sessions entirely and relies only on a monotone quadratic inequality.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO

    out = StringIO()
    _sys.stdout = out

    solve()

    _sys.stdout = sys.__stdout__
    return out.getvalue()

def solve():
    n, k = map(int, input().split())

    lo, hi = 0, n

    def cost(x):
        return x * (x + 1) // 2

    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cost(mid) <= k:
            lo = mid
        else:
            hi = mid - 1

    print(n - lo)

# provided samples
assert run("5 7\n") == "2\n"

# custom cases
assert run("1 0\n") == "1\n", "cannot skip anything"
assert run("1 1\n") == "0\n", "exact single skip"
assert run("10 0\n") == "10\n", "no budget"
assert run("10 55\n") == "0\n", "full budget allows all skips"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | 1 | no skipping allowed |
| 1 1 | 0 | boundary single element |
| 10 0 | 10 | zero budget edge |
| 10 55 | 0 | full triangular capacity |

## Edge Cases

For input `1 0`, the cost of skipping one session is already 1, which exceeds the budget. The binary search immediately finds zero valid skips, so the answer is 1 attended session.

For input `1 1`, skipping the only session costs exactly 1, which is allowed. The algorithm returns 0 attended sessions, matching the optimal strategy.

For input `10 0`, no skipping is possible because even a single skip has cost 1. The binary search yields zero skips, so Vasya attends all sessions.

For input `10 55`, the budget matches the full triangular number $10 \cdot 11 / 2$. The algorithm correctly allows all sessions to be skipped, resulting in zero attended sessions.
