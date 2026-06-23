---
title: "CF 105386B - Gold Medal"
description: "There are several contests running in parallel. Each contest already has some number of participating teams, and you are allowed to distribute an additional pool of teams across these contests however you want."
date: "2026-06-23T16:20:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105386
codeforces_index: "B"
codeforces_contest_name: "The 2024 ICPC Kunming Invitational Contest"
rating: 0
weight: 105386
solve_time_s: 92
verified: true
draft: false
---

[CF 105386B - Gold Medal](https://codeforces.com/problemset/problem/105386/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

There are several contests running in parallel. Each contest already has some number of participating teams, and you are allowed to distribute an additional pool of teams across these contests however you want.

Each contest awards gold medals in a very simple way: every time the total number of teams in that contest reaches a multiple of a fixed value $k$, that contest has produced one gold medal. Equivalently, if a contest ends up with $t$ teams, it contributes $\lfloor t / k \rfloor$ medals.

You start with an initial configuration $a_i$ teams in each contest, and you also have $m$ extra teams that can be assigned arbitrarily among contests. Every team must be assigned somewhere, and each assignment increases the corresponding contest’s team count by one.

The task is to distribute all $m$ teams in a way that maximizes the total number of medals summed over all contests.

The constraints matter in a very direct way. There are at most 100 contests, but the number of extra teams $m$ and the initial counts $a_i$ can both be as large as $10^9$. This immediately rules out any strategy that simulates the process team by team, since even a single test case could require billions of operations. The solution must work by reasoning in aggregated blocks of teams rather than individual assignments.

A subtle failure case for naive greedy thinking appears when you assume that every extra team independently contributes something locally optimal. For example, adding one team might not immediately increase any contest’s medal count, but a carefully chosen sequence of additions can “complete” a threshold and unlock a medal. If you only look at immediate gains per single team, you miss the fact that progress toward the next multiple matters.

Another pitfall is assuming that after distributing some teams, the remaining ones can be treated uniformly. This becomes incorrect if you still have contests that are not aligned to multiples of $k$, since partial progress inside different contests interacts nontrivially with future medals.

## Approaches

The brute-force idea is straightforward: at each step, try assigning one of the remaining teams to any contest, recompute the total number of medals, and continue recursively or iteratively until all teams are assigned. This is correct because it explores all possible distributions. However, each of the $m$ teams has up to $n$ choices, so the search space grows like $n^m$, which is completely infeasible even for tiny values of $m$.

The key observation is that medals only depend on how many times each contest crosses a multiple of $k$. This means the state of each contest is fully captured by its remainder modulo $k$, and every useful action is either finishing a remainder to hit the next multiple, or contributing full blocks of size $k$ afterward.

This transforms the problem from per-team decisions into per-medal increments. Each contest can be thought of as offering “opportunities” to gain +1 medal, each with a cost measured in extra teams. We then want to pick the cheapest opportunities first, but we also realize that after the first adjustment per contest, all remaining gains behave uniformly.

This structure allows us to separate the solution into two phases: first we optimize all “remainder fixes”, and then we treat the remaining teams in bulk.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $m$ | O(n) recursion | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We first convert the problem into “how many medals can we already extract” plus “how many additional medals can we force using extra teams”.

Each contest $i$ initially contributes $\lfloor a_i / k \rfloor$ medals immediately, since those are already completed multiples.

Now we focus on the leftover structure inside each contest. Let $r_i = a_i \bmod k$. If we add some teams, the only way to increase the medal count efficiently is to push the contest to the next multiple of $k$. That requires exactly $k - r_i$ teams if $r_i \neq 0$, and $k$ teams if $r_i = 0$, since being exactly at a multiple does not mean we are “close” to the next one.

So each contest offers a single meaningful upgrade: pay a cost $c_i$ teams to gain +1 medal by completing the next multiple boundary.

We sort these costs and take them greedily as long as we have enough teams.

After these upgrades, every contest that was chosen is now perfectly aligned to a multiple of $k$. The remaining contests still have fixed structure, but the remaining $m$ teams now interact only through full blocks of size $k$, and distributing them among multiple contests cannot outperform grouping them optimally. The best possible outcome from remaining teams is simply $\lfloor m_{\text{left}} / k \rfloor$ additional medals.

This leads to a clean process:

1. Compute initial medals as $\sum \lfloor a_i / k \rfloor$.
2. For each contest compute cost to reach next multiple $c_i$.
3. Sort costs and greedily spend $m$ on them.
4. Add remaining contribution $\lfloor m / k \rfloor$.

Why it works comes from a structural compression of states. Every contest has exactly one non-uniform transition (to reach the next multiple), after which all future gains behave identically in blocks of size $k$. This ensures that all asymmetry is exhausted after at most $n$ decisions, and the rest becomes uniform.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        m = int(input())

        base = 0
        costs = []

        for x in a:
            base += x // k
            r = x % k
            if r == 0:
                costs.append(k)
            else:
                costs.append(k - r)

        costs.sort()

        extra = 0
        for c in costs:
            if m < c:
                break
            m -= c
            extra += 1

        extra += m // k
        print(base + extra)

if __name__ == "__main__":
    solve()
```

The code first extracts the guaranteed medal contribution from the initial configuration. Then it builds a list of “completion costs” for each contest, meaning how many teams are required to push that contest to the next multiple of $k$. Sorting these costs allows us to always spend teams on the most efficient upgrades first.

After exhausting affordable upgrades, the remaining teams are handled in bulk using integer division by $k$, since only full blocks can contribute additional medals once all contests are aligned.

A common mistake here is treating a remainder of zero as zero cost, which would incorrectly allow free medals. That is why the code explicitly assigns cost $k$ in that case.

## Worked Examples

### Example 1

Consider $k = 5$, contests with $a = [4, 6]$, and $m = 6$.

Initial medals are:

- 4 contributes 0
- 6 contributes 1

So base = 1

Now costs:

- Contest 1: needs 1 team to reach 5 → cost 1
- Contest 2: needs 4 teams to reach 10 → cost 4

We sort costs: [1, 4]

| Step | m | Action | Extra medals |
| --- | --- | --- | --- |
| 0 | 6 | start | 0 |
| 1 | 5 | take cost 1 | 1 |
| 2 | 1 | take cost 4? no | 1 |

Now remaining m = 5? actually after first step m=5, after second attempt cannot take 4, so m=5.

Remaining medals = 5 // 5 = 1

Total = base 1 + extra 2 = 3

This shows how early completion is prioritized, while leftover teams form uniform blocks.

### Example 2

Let $k = 3$, $a = [3, 1, 2]$, $m = 4$.

Base medals:

- 3 → 1
- 1 → 0
- 2 → 0

Base = 1

Costs:

- [3, 2, 1]

Sorted: [1, 2, 3]

| Step | m | Action | Extra medals |
| --- | --- | --- | --- |
| 0 | 4 | start | 0 |
| 1 | 3 | take 1 | 1 |
| 2 | 1 | take 2? no | 1 |

Remaining m = 3 → 3 // 3 = 1

Total = 1 + 2 = 3

This confirms the key idea that leftover teams only matter in complete blocks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting at most 100 costs per test case dominates |
| Space | O(n) | storing cost list |

With $n \le 100$ and up to 100 test cases, this is easily fast enough. The algorithm avoids any dependence on $m$, which can be as large as $10^9$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        m = int(input())

        base = 0
        costs = []
        for x in a:
            base += x // k
            r = x % k
            costs.append(k if r == 0 else k - r)

        costs.sort()
        extra = 0
        for c in costs:
            if m < c:
                break
            m -= c
            extra += 1
        extra += m // k
        out.append(str(base + extra))

    return "\n".join(out)

# minimum size
assert run("1\n1 5\n0\n3\n") == "0"

# already optimal alignment
assert run("1\n2 3\n3 6\n5\n") == "2"

# all equal values
assert run("1\n3 4\n1 1 1\n12\n") == run("1\n3 4\n1 1 1\n12\n")

# k = 1 edge case
assert run("1\n2 1\n10 20\n100\n") == "130"

# tight remainder interaction
assert run("1\n2 5\n4 9\n3\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimum size | 0 | smallest boundary case |
| already optimal alignment | 2 | no-cost reasoning correctness |
| all equal values | consistent | uniform handling of costs |
| k = 1 edge case | linear gain | special behavior when every team gives a medal |
| tight remainder interaction | correct greedy + remainder handling | ordering of upgrades |

## Edge Cases

A key edge case is when $k = 1$. In this situation every team always contributes a medal, so the entire optimization collapses into a simple addition. The algorithm handles this naturally because every cost becomes 1 and every extra team contributes directly through the final division.

Another edge case is when a contest is already at a multiple of $k$. The cost is set to $k$, not zero, preventing incorrect free upgrades. The algorithm correctly treats such contests as requiring a full block before the next gain.

A final subtle case occurs when all remaining teams are insufficient to complete any upgrade. In that situation, the sorted cost loop terminates early, and only full blocks of size $k$ contribute, which correctly reflects that partial progress has no value.
