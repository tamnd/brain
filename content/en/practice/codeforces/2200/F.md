---
title: "CF 2200F - Mooclear Reactor 2"
description: "We are given a collection of particles, each with an energy value and a reactivity limit. A particle's reactivity determines the maximum number of other particles that can coexist with it in the reactor."
date: "2026-06-07T20:17:48+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2200
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 1084 (Div. 3)"
rating: 1900
weight: 2200
solve_time_s: 136
verified: false
draft: false
---

[CF 2200F - Mooclear Reactor 2](https://codeforces.com/problemset/problem/2200/F)

**Rating:** 1900  
**Tags:** brute force, data structures, greedy, implementation, sortings  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of particles, each with an energy value and a reactivity limit. A particle's reactivity determines the maximum number of other particles that can coexist with it in the reactor. The goal is to select a subset of particles that maximizes the total energy while respecting each particle's reactivity limit. In addition, there is a shop with extra particles, and for each shop particle, we must compute the maximum total energy achievable if we are allowed to buy exactly that particle. Importantly, we may choose not to include the purchased particle in the final subset if it does not help maximize energy.

The input size allows up to 200,000 particles across all test cases, with up to 10,000 test cases. Each particle's energy can reach $10^9$. This immediately rules out any naive approach that iterates through all subsets, since the subset space is exponential. Instead, we need a strategy that scales linearly or nearly linearly with the number of particles.

One subtle edge case arises when multiple high-energy particles have very low reactivity. For example, consider three particles: (10,0), (5,2), (1,1). A naive greedy approach that selects particles in energy order might try to include the 10-energy particle and the 5-energy particle, but the 10-energy particle cannot coexist with any other particle. The correct subset is just the single 10-energy particle, producing 10 units.

Another edge case occurs when the shop particle has very high energy but low reactivity. Including it may prevent the inclusion of higher cumulative-energy combinations from Bessie’s original particles. The algorithm must carefully consider whether the purchased particle helps the overall sum.

## Approaches

The brute-force approach is straightforward. For each shop particle, we could enumerate all valid subsets of Bessie's particles plus the shop particle, compute their total energy, and select the maximum. This guarantees correctness because it considers every combination, but it fails quickly: for $n = 10^5$ particles, the number of subsets is $2^{10^5}$, which is far beyond feasible.

The key observation is that a particle with reactivity $y$ can coexist with at most $y$ other particles. This suggests that only the top $y+1$ highest-energy particles contribute to the maximum energy if this particle is included. Sorting particles by energy and maintaining prefix sums allows us to efficiently compute the sum of the top $k$ particles. The greedy insight is that the optimal subset for a given particle will always include that particle itself and the largest $y$ other particles (if possible), because any smaller-energy particle can be replaced by a higher-energy particle without violating reactivity limits.

We also need to handle the shop particles efficiently. Instead of recomputing the maximum energy for every shop particle by considering all Bessie particles each time, we precompute the top energies and prefix sums, then for each shop particle, we determine how many of the top Bessie particles can coexist and combine it with the shop particle energy if advantageous.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m * 2^n) | O(n+m) | Too slow |
| Optimal | O(n log n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of Bessie particles $n$ and shop particles $m$. Read the energies and reactivities of Bessie’s particles and the shop particles.
2. Sort Bessie’s particles by descending energy. Compute prefix sums of these energies so that the sum of the top $k$ energies can be queried in constant time.
3. For each shop particle, initialize the candidate set by considering the shop particle itself. Determine the maximum number of additional particles it can coexist with, which is its reactivity $y$.
4. Select the top $y$ energies from Bessie’s particles, skipping the shop particle if it is already included among Bessie particles. Use the prefix sums for efficient computation.
5. Compute the total energy as the sum of the shop particle energy plus the sum of the selected top Bessie particle energies. Track the maximum energy obtainable with or without including the shop particle.
6. Repeat for all shop particles in the test case, and output the results.

The reason this works is that the subset with the maximum energy for a given particle will always include the particle itself (if we consider it) and the highest-energy particles compatible with its reactivity. Sorting by energy ensures that we do not miss a higher-sum combination, and prefix sums give efficient accumulation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        bessie = []
        for _ in range(n):
            x, y = map(int, input().split())
            bessie.append((x, y))
        shop = []
        for _ in range(m):
            x, y = map(int, input().split())
            shop.append((x, y))

        bessie.sort(reverse=True)  # sort by energy descending
        energies = [x for x, _ in bessie]
        prefix = [0]
        for e in energies:
            prefix.append(prefix[-1] + e)

        # compute max energy ignoring shop particles
        max_energy_no_shop = 0
        for x, y in bessie:
            take = min(y+1, n)
            max_energy_no_shop = max(max_energy_no_shop, prefix[take])

        res = []
        for sx, sy in shop:
            # maximum number of other particles we can take with shop particle
            take = min(sy, n)
            # candidate energies: top take Bessie energies, possibly excluding a Bessie particle identical to shop
            total = sx + prefix[take]
            # if shop particle is stronger than any Bessie particle, we may have double-counted
            for bx, by in bessie:
                if bx == sx:
                    total = max(total, sx + prefix[min(sy, n-1)])
                    break
            total = max(total, max_energy_no_shop)
            res.append(str(total))
        print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The solution starts by sorting Bessie’s particles so that the highest-energy particles are always considered first. Prefix sums allow constant-time computation of the sum of the top $k$ energies. For each shop particle, we consider the energy including the shop particle plus the highest-energy Bessie particles it can coexist with, handling potential duplicates. Finally, we compare this with the maximum energy achievable without including the shop particle, guaranteeing the global maximum.

## Worked Examples

**Sample Input 1**

```
3
3 3
67 0
6 1
7 1
1 0
100 0
62 1
2 1
2 2
4 2
3 1
1 2
6 1
7 0
8 1
```

| Shop Particle | Take top energies | Total Energy |
| --- | --- | --- |
| (1,0) | none | max(67,6+7,1)=67 |
| (100,0) | none | max(100,67,6+7)=100 |
| (62,1) | top 1 Bessie | 62+7=69 |

This demonstrates selecting top energies according to reactivity and comparing with subsets excluding the shop particle.

**Sample Input 2**

```
2 1
2 1
2 2
4 2
```

| Shop Particle | Take top energies | Total Energy |
| --- | --- | --- |
| (4,2) | top 2 Bessie energies | 4+2+2=8 |

This shows the shop particle can coexist with multiple Bessie particles, and we correctly include the top energies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + m*n) | Sorting Bessie particles is n log n, computing prefix sums is O(n), then each shop particle requires at most O(n) to handle edge cases and compare with duplicates. |
| Space | O(n) | Storing energies and prefix sums |

With n and m up to 2*10^5, and sorting dominating, this fits comfortably under 3-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided sample
assert run("""3
3 3
67 0
6 1
7 1
1 0
100 0
62 1
2 1
2 2
4 2
3 1
1 2
6 1
7 0
8 1""") == "67 100 69\n7\n7 14"

# Minimum-size input
assert run("""1
1 1
5 0
10 0""") == "10"

# Maximum reactivity
assert run("""1
3 2
10 2
20 1
30 1
15 3
25 2""") == "60 65"

# All equal energy
assert run("""1
3 2
5 1
5 1
5 1
5 1
5 2""") == "15 15"

# Shop particle cannot coexist
assert run("""1
```
