---
title: "CF 103104F - Battery"
description: "We are given a collection of batteries and a collection of shooting locations. Each battery has a fixed amount of energy, and each location requires a fixed amount of energy to complete one recording session."
date: "2026-07-03T21:43:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103104
codeforces_index: "F"
codeforces_contest_name: "2021 Hubei Provincial Collegiate Programming Contest"
rating: 0
weight: 103104
solve_time_s: 49
verified: true
draft: false
---

[CF 103104F - Battery](https://codeforces.com/problemset/problem/103104/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of batteries and a collection of shooting locations. Each battery has a fixed amount of energy, and each location requires a fixed amount of energy to complete one recording session. Each battery can be used at most once, and once you start using a battery for a location, it must fully cover that location’s requirement without interruption or replacement.

The task is to choose a pairing strategy between batteries and locations so that the number of fully completed locations is maximized. Each battery can be assigned to at most one location, and each location can be assigned at most one battery. A location is satisfied if the chosen battery has capacity at least equal to its required duration.

The structure immediately suggests a bipartite matching-like problem, but the constraints are too large for any general matching algorithm. Instead, this is a greedy assignment problem over two multisets.

The constraints imply we need something close to O(N log N + M log M) or O(N + M log M). With N up to 100000 and M up to 300000, anything quadratic or even N times M is impossible. A solution that tries every battery-location pairing is clearly infeasible because it would reach up to 3 × 10^10 comparisons in the worst case.

The key structural detail is that all shooting durations are powers of two. This is a strong hint that grouping or bucket-based greedy matching will be effective, since we can process requirements in increasing order and handle repeated values efficiently.

A few edge cases matter:

A naive greedy that assigns the smallest battery that can satisfy a location without careful ordering can fail. For example, if batteries are [5, 6] and requirements are [4, 5], a careless assignment might give 5 → 5 and 6 → 4, which is fine, but if we reverse decisions greedily in the wrong order, we might waste the 6 on 5 and leave 4 unmatched incorrectly depending on implementation order. Another subtle failure arises when multiple identical requirements exist, since greedy choice must respect global optimality rather than local fit.

## Approaches

A brute-force view would try to assign batteries to locations in all possible ways and count the best matching. This corresponds to trying all matchings in a bipartite graph where an edge exists if ai ≥ bi. Even if we restrict ourselves to a greedy assignment, naive simulation would check every battery against every location, producing O(NM) time complexity, which is far beyond limits.

The key observation is that we do not need to preserve identities of locations beyond their required energy. Since requirements are just sizes, and we only care about how many we satisfy, the problem becomes a classic “maximize number of matches where capacity ≥ demand” problem. This is typically solved by sorting both arrays and greedily matching from smallest to largest.

However, the twist is that b_i are powers of two. This guarantees a very limited number of distinct requirement values (at most 31). Instead of treating M as large, we can compress requirements into frequency buckets indexed by exponent. Then we effectively match batteries against demand levels from small to large.

We sort batteries in increasing order and also process requirement buckets from smallest power to largest. For each requirement size, we try to assign the smallest possible battery that still satisfies it. This ensures we never waste a large battery on a small requirement unless necessary.

We maintain a pointer over batteries and greedily consume them as we satisfy demands. Because both sides are sorted and we only move forward, each element is processed once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching | O(NM) | O(1) | Too slow |
| Sorting + Greedy Matching | O((N + M) log N) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read all battery capacities and sort them in non-decreasing order. This allows us to always use the smallest available battery that can still satisfy a requirement, preserving larger batteries for later larger demands.
2. Count how many requests exist for each power of two value. Since bi = 2^j, we store frequencies in an array freq[j]. This compresses the input into at most 31 categories.
3. Initialize a pointer i at the beginning of the sorted battery array. This pointer represents the smallest unused battery.
4. Iterate over possible powers of two from smallest to largest, processing freq[j] in increasing order of required capacity. This ensures we always attempt to satisfy easier tasks first.
5. For each requirement level 2^j, attempt to assign batteries greedily. While freq[j] > 0 and i < N, advance i until we find a battery with capacity ≥ 2^j. If none exists, break because no further assignments at this level or higher will be possible for this battery range.
6. When a valid battery is found, assign it to one requirement, increment i, decrement freq[j], and increment the answer counter. This consumes both a battery and a location.
7. Continue until all requirement levels are processed or batteries are exhausted.

### Why it works

The algorithm maintains a greedy invariant: at any moment, the smallest remaining battery is either too small for the current requirement level or is the best possible choice for that level. Because both batteries and requirements are processed in increasing order, any deviation where we assign a larger battery to a smaller requirement would only reduce flexibility for future larger requirements without increasing the number of satisfied assignments. The monotonic structure ensures that once a battery is skipped for a requirement, it can never be useful for smaller requirements, and once requirements increase, earlier batteries cannot satisfy them anymore. This prevents any beneficial swap that could improve the total count.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    a.sort()

    freq = [0] * 31
    for x in b:
        freq[x.bit_length() - 1] += 1

    ans = 0
    i = 0

    for j in range(31):
        need = 1 << j
        while freq[j] > 0 and i < n:
            if a[i] >= need:
                ans += 1
                freq[j] -= 1
                i += 1
            else:
                i += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution starts by sorting batteries so that we can always consume them in increasing order. The frequency array compresses all shooting durations into power-of-two buckets, which is crucial because it removes dependence on M in the matching loop.

The pointer i is never reset backward. This is safe because once a battery is too small for a requirement level, it will never be useful for any later level. Each battery is considered at most once, ensuring linear scanning over the sorted array.

The inner loop either consumes a battery or discards it permanently, guaranteeing progress.

## Worked Examples

### Example 1

Input:

```
N = 2, M = 4
a = [3, 5]
b = [2, 2, 2, 2]
```

Buckets:

freq[1] = 4 since 2 = 2^1

| Step | i | Battery a[i] | freq[1] | Action | ans |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 4 | use 3 for 2 | 1 |
| 2 | 1 | 5 | 3 | use 5 for 2 | 2 |
| 3 | 2 | - | 2 | stop | 2 |

We match two locations, since only two batteries exist. The trace shows that once batteries are exhausted, remaining requirements cannot be satisfied.

### Example 2

Input:

```
N = 3, M = 3
a = [4, 6, 8]
b = [2, 4, 4]
```

Buckets:

freq[1] = 1, freq[2] = 2

| Step | i | Battery | Level | freq | Action | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 4 | 2 | 1 | use 4 | 1 |
| 2 | 1 | 6 | 4 | 2 | use 6 | 2 |
| 3 | 2 | 8 | 4 | 1 | use 8 | 3 |

This confirms that processing smaller requirements first prevents wasting larger batteries unnecessarily, while still allowing them to satisfy larger tasks later.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N + M + 31) | Sorting batteries dominates, frequency aggregation and scanning are linear |
| Space | O(1) extra | Only fixed-size frequency array and sorted input storage |

The constraints allow up to 4 × 10^5 total elements, and the algorithm performs only sorting plus a single linear scan over batteries, which comfortably fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import log2

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    a.sort()
    freq = [0] * 31
    for x in b:
        freq[x.bit_length() - 1] += 1

    ans = 0
    i = 0

    for j in range(31):
        need = 1 << j
        while freq[j] > 0 and i < n:
            if a[i] >= need:
                ans += 1
                freq[j] -= 1
                i += 1
            else:
                i += 1

    return str(ans)

# provided sample
assert run("2 4\n3 5\n2 2 2 2\n") == "2"

# all equal small
assert run("3 3\n1 1 1\n1 1 1\n") == "3"

# insufficient batteries
assert run("2 5\n10 20\n2 2 2 2 2\n") == "2"

# large battery single match
assert run("1 1\n100\n64\n") == "1"

# greedy ordering trap check
assert run("3 3\n3 5 10\n2 4 8\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal equal | 3 | basic full matching |
| insufficient batteries | 2 | exhaustion handling |
| single large match | 1 | threshold correctness |
| mixed ordering | 3 | greedy ordering safety |

## Edge Cases

One edge case is when all batteries are smaller than the smallest requirement. In that case, the pointer i advances through all batteries without any match, and the answer remains zero. The algorithm correctly skips all unusable batteries because the condition a[i] < need triggers only advancement.

Another edge case occurs when there are many identical requirement values. Because we process frequency counts, each match consumes exactly one unit of demand, and the loop continues until either batteries or demand are exhausted. There is no dependence on ordering within identical requirements, so no pathological behavior arises.

A final edge case is when a few very large batteries exist alongside many small ones. The sorting ensures that small batteries are used first where possible, but once requirements increase, the algorithm naturally shifts to larger batteries. Since the pointer never moves backward, large batteries are preserved automatically for larger requirements.
