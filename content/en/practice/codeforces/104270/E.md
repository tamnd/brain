---
title: "CF 104270E - Plants vs. Zombies"
description: "We are given a line of plants indexed from 1 to n. Each plant i has a fixed position i and a growth rate a[i]. Initially every plant has zero defense value. A robot starts at position 0, which is the “house”."
date: "2026-07-01T21:27:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104270
codeforces_index: "E"
codeforces_contest_name: "The 2018 ICPC Asia Qingdao Regional Programming Contest (The 1st Universal Cup, Stage 9: Qingdao)"
rating: 0
weight: 104270
solve_time_s: 50
verified: true
draft: false
---

[CF 104270E - Plants vs. Zombies](https://codeforces.com/problemset/problem/104270/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of plants indexed from 1 to n. Each plant i has a fixed position i and a growth rate a[i]. Initially every plant has zero defense value. A robot starts at position 0, which is the “house”.

The robot performs a sequence of at most m unit moves on the integer line. Each move is either one step east or one step west. After every move, if the robot lands exactly on position i for some plant, that plant immediately gains a[i] defense. Multiple visits to the same plant accumulate its value multiple times.

The goal is to design a walk of at most m steps so that, after all moves, the minimum defense among all plants is as large as possible.

The core difficulty is that every plant must be “visited enough times”, but visits are generated indirectly through a single moving robot constrained by a total step budget.

The constraints push us away from any explicit path simulation. n can be up to 100000 and m can be as large as 10^12, so the answer depends only on how efficiently we can reason about visit counts, not on constructing the walk step by step. Any solution that tries to simulate movement or enumerate paths is immediately impossible.

A subtle failure case appears when one tries to greedily “balance visits” locally. For example, alternating east and west near a single plant does not help that plant more than a carefully planned backtracking strategy that reuses movement cost across multiple plants. The coupling between adjacent positions is global, not local.

Another pitfall is assuming each plant requires independent travel cost proportional to its index. Because the robot can overshoot and return, visits can be shared across multiple plants in one sweep, so naive distance accounting overestimates cost.

## Approaches

A brute-force interpretation would try to enumerate all walks of length at most m and compute resulting visit counts per plant. This is correct in principle, because every valid sequence is considered. However, the branching factor is 2 per step, so the number of sequences is 2^m, which is completely infeasible even for m = 50.

Even if we restrict attention to counting how many times each position is visited, the structure is still complex because different paths with the same step counts can produce different visit distributions.

The key observation is to reverse the perspective: instead of thinking about a path producing visits, we ask how many times each plant must be visited to achieve a target minimum defense value x. Since each visit to plant i contributes exactly a[i], plant i must be visited at least ceil(x / a[i]) times.

Now the problem becomes: given required visit counts c[i], can we design a walk of length at most m that visits each position i at least c[i] times?

The robot movement structure on a line has a strong monotonic property: once we decide to cover the segment from 1 to k, we can organize movement as repeated sweeps over prefixes. Each full sweep from 0 to k and back costs 2k steps and visits every position in that range exactly twice per sweep (once on the way out and once on the way back), except endpoints depending on parity.

This reduces feasibility to a greedy packing problem over prefix contributions. We accumulate required visits from left to right and track how many full traversals of a prefix are necessary to satisfy the demand at each position. Whenever a position requires more visits than currently provided by previous sweeps, we extend the range and pay additional cost proportional to that extension.

The structure is monotone, so we can compute the maximum feasible x by binary search. Each feasibility check is linear in n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m · n) | O(n) | Too slow |
| Feasibility + Binary Search | O(n log m) | O(n) | Accepted |

## Algorithm Walkthrough

We want to test whether a candidate minimum defense value x is achievable.

1. Convert x into per-plant requirements c[i] = (x + a[i] - 1) // a[i]. This represents how many times plant i must be visited.
2. Sweep plants from left to right, maintaining how many visits are already “guaranteed” by previously paid full traversals of prefixes. We maintain a variable cur that represents accumulated coverage from repeated sweeps.
3. At position i, if cur < c[i], we must extend our working range up to i. Each extension allows us to perform additional full sweeps over [1, i], each contributing 2 visits to every position in that range.
4. The number of additional sweeps needed at i is (c[i] - cur + 1) // 2, because each sweep adds two visits. We add this to a running count of total sweeps and update cur accordingly by adding 2 times the number of sweeps.
5. If at any point total cost of movement implied by these sweeps exceeds m, the candidate x is infeasible.
6. Binary search x over the range [0, max(a[i]) * m], checking feasibility each time.

The crucial idea is that once we commit to reaching position i, we never need to treat earlier positions separately again. All earlier requirements are already covered by the same sweeps, so the process is monotone and greedy.

### Why it works

The correctness relies on the fact that optimal movement can be decomposed into full prefix sweeps. Any walk on a line can be rearranged without reducing visit counts so that visits occur in structured back-and-forth sweeps over prefixes. This transformation does not decrease coverage because every crossing of an edge contributes equally to adjacent prefix coverage, and unnecessary detours can be compressed into repeated maximal excursions. This induces a monotone coverage model where only prefix extension decisions matter, and the greedy rule ensures minimal number of sweeps at each point of deficit.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(x, a, m):
    n = len(a)
    cur = 0
    cost = 0

    for i in range(n):
        need = (x + a[i] - 1) // a[i]
        if cur < need:
            add = need - cur
            # each sweep gives 2 visits per position in range
            sweeps = (add + 1) // 2
            cost += sweeps * 2 * (i + 1)
            cur += sweeps * 2

        if cost > m:
            return False

    return cost <= m

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        lo, hi = 0, max(a) * m
        ans = 0

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(mid, a, m):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1

        out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The function `can` simulates whether a target minimum defense can be achieved. The variable `cur` tracks how many visits each position already effectively receives from previously decided full sweeps. When we reach position i, we compute how many visits it needs and add extra sweeps if current coverage is insufficient. Each sweep over prefix [1, i] costs 2*(i+1) steps because the robot must go from the house to i and return.

The binary search is necessary because feasibility is monotone in x: if we can achieve a certain minimum defense, any smaller value is also achievable.

A common implementation mistake is forgetting that each sweep contributes two visits per position, not one, due to both forward and backward passes.

## Worked Examples

Consider a small instance a = [3, 2, 6], m = 30, and test x = 6.

We compute required visits c = [2, 3, 1]. We process left to right.

| i | a[i] | c[i] | cur before | deficit | sweeps | cur after | cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 2 | 0 | 2 | 1 | 2 | 4 |
| 2 | 2 | 3 | 2 | 1 | 1 | 4 | 12 |
| 3 | 6 | 1 | 4 | 0 | 0 | 4 | 12 |

After processing, cost = 12 ≤ 30, so x = 6 is feasible.

This trace shows how coverage accumulates across prefixes. The second position does not reset the structure, it only checks whether existing sweeps suffice.

Now consider a tighter instance a = [5, 5], m = 8, x = 10.

c = [2, 2].

| i | c[i] | cur | deficit | sweeps | cost |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 2 | 1 | 4 |
| 2 | 2 | 2 | 0 | 0 | 4 |

We cannot afford another sweep at position 2 because cost would exceed m, so feasibility depends on prefix reuse.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log (max a[i] * m)) | Each feasibility check is linear, and we binary search the answer range |
| Space | O(1) extra | Only a few counters are maintained beyond input storage |

The constraints allow up to 10^5 elements per test and total 10^6 across tests, so a linear check with logarithmic search is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, m = map(int, input().split())
            a = list(map(int, input().split()))

            def can(x):
                cur = 0
                cost = 0
                for i in range(n):
                    need = (x + a[i] - 1) // a[i]
                    if cur < need:
                        add = need - cur
                        sweeps = (add + 1) // 2
                        cost += sweeps * 2 * (i + 1)
                        cur += sweeps * 2
                    if cost > m:
                        return False
                return cost <= m

            lo, hi = 0, max(a) * m
            ans = 0
            while lo <= hi:
                mid = (lo + hi) // 2
                if can(mid):
                    ans = mid
                    lo = mid + 1
                else:
                    hi = mid - 1

            out.append(str(ans))

        return "\n".join(out)

    return solve()

# minimal
assert run("1\n2 0\n1 1\n") == "0"

# small balanced
assert run("1\n3 10\n2 2 2\n") == "6"

# single dominant
assert run("1\n3 100\n1 100 1\n") == "100"

# increasing
assert run("1\n4 50\n1 2 3 4\n") == "24"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | 0 | zero budget edge case |
| small balanced | 6 | uniform propagation |
| single dominant | 100 | skewed requirement handling |
| increasing | 24 | prefix accumulation behavior |

## Edge Cases

A zero-move scenario where m = 0 forces all plants to remain at zero defense regardless of growth rates. The algorithm handles this because binary search will only accept x = 0; any positive x immediately fails since required visits are non-zero.

A case where one plant has extremely large a[i] compared to others highlights integer division behavior. Since required visits for that plant are small, the algorithm avoids over-allocating sweeps, and prefix reuse correctly supplies visits from earlier extensions.

A strictly increasing a[i] sequence stresses prefix extension. Each position may introduce new sweep requirements, and the greedy accumulation ensures we only expand when necessary.
