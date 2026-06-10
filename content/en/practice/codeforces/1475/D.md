---
title: "CF 1475D - Cleaning the Phone"
description: "We are given a phone with a list of installed apps. Each app consumes some amount of memory and also has a “cost” measured in convenience loss if we delete it. Every app contributes either 1 or 2 convenience points."
date: "2026-06-11T00:08:30+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1475
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 697 (Div. 3)"
rating: 1800
weight: 1475
solve_time_s: 102
verified: true
draft: false
---

[CF 1475D - Cleaning the Phone](https://codeforces.com/problemset/problem/1475/D)

**Rating:** 1800  
**Tags:** binary search, dp, sortings, two pointers  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a phone with a list of installed apps. Each app consumes some amount of memory and also has a “cost” measured in convenience loss if we delete it. Every app contributes either 1 or 2 convenience points.

The task is to remove a subset of apps so that the total freed memory is at least a required threshold $m$, while minimizing the total convenience lost. If it is impossible to free enough memory, we must report that fact.

So the input gives us two parallel arrays: one describing memory sizes, one describing how “important” each app is. We are selecting a subset that satisfies a knapsack-like constraint on total size, but the cost is unusually simple because it only takes two possible values.

The key constraint shaping the solution is the total number of apps across all test cases, which is at most $2 \cdot 10^5$. This immediately rules out any solution that tries all subsets or uses quadratic dynamic programming over memory values. A full knapsack over $m$ is also impossible since $m$ can reach $10^9$.

A common failure mode comes from treating this like a standard knapsack or greedy-by-ratio problem. For example, choosing apps with best memory-to-cost ratio can fail:

Input:

```
3 10
6 5 4
2 1 1
```

Greedy ratio might pick (6,2) and (5,1) for total memory 11 cost 3. But optimal is (6,2)+(4,1)=10 cost 3 as well, so ties can hide mistakes; worse examples exist where greedy fails because cost is only 1 or 2, not continuous.

Another subtle edge case is when the best solution uses many cheap-cost apps (b = 1), but a naive approach exhausts b = 2 apps first and stops too early.

The structure of costs being only 1 or 2 is what makes the problem tractable.

## Approaches

A brute-force approach would enumerate all subsets of apps, compute total memory and total cost, and take the best valid subset. This works conceptually because every subset is checked, but it requires $2^n$ evaluations, which is far beyond feasible even for $n = 40$.

A more structured brute-force is to try all subsets using recursion or DP over index and memory sum, but the memory dimension is up to $10^9$, making any DP state space explosion immediate.

The key observation is that costs are binary: every app belongs to one of two groups. This suggests separating apps into two lists based on their cost. If we sort apps in each group by memory descending, then any optimal solution will take some number of largest-memory items from cost-1 group and cost-2 group.

However, picking them independently is not enough because the trade-off is global: sometimes taking a slightly smaller cost-2 app is better if it frees more memory.

The crucial insight is to sort all apps by memory descending, but process them in a way that allows incremental choice of how many cost-2 apps we include. We precompute prefix sums of memory for both groups after sorting. Then we try all possible counts of taking the best $k$ cost-2 apps, and fill the remaining memory requirement using cost-1 apps.

This reduces the problem to combining two sorted sequences with prefix sums, instead of searching subsets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal (sorting + greedy + prefix sums) | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We split applications into two groups: those with cost 1 and those with cost 2.

1. Separate all apps into two lists based on their cost. This isolates the two “pricing tiers” that we will trade off against each other.
2. Sort both lists in descending order of memory size. This ensures that whenever we take $k$ apps from a group, we are always taking the most efficient ones in terms of memory gain.
3. Build prefix sum arrays for both groups. The prefix sum at index $i$ gives the maximum memory obtainable by taking the best $i$ apps of that type.
4. Compute total available memory. If even taking all apps is insufficient, immediately output -1.
5. For each possible number $i$ of cost-2 apps taken (from 0 to len(b2)), compute the memory gained. If it already reaches $m$, record cost $2i$.
6. If not enough, compute remaining memory needed and determine how many cost-1 apps are required using binary search on prefix sums.
7. Track the minimum total cost over all valid splits.

The reason this works is that cost-2 apps are strictly worse in cost but potentially better in memory per item, so the only meaningful decision is how many of them to include. Once fixed, the rest reduces to a single greedy fill from cost-1 apps.

### Why it works

Any optimal solution can be rearranged so that within each cost group, the selected apps are the ones with largest memory. If a solution uses a smaller-memory app while a larger one is unused in the same group, swapping improves or preserves feasibility without increasing cost. This exchange argument ensures that considering only prefix selections inside each group never misses an optimal configuration. Once both groups are reduced to prefix choices, the only remaining degree of freedom is how many items are taken from the cost-2 group.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        ones = []
        twos = []
        
        total = 0
        
        for ai, bi in zip(a, b):
            total += ai
            if bi == 1:
                ones.append(ai)
            else:
                twos.append(ai)
        
        if total < m:
            print(-1)
            continue
        
        ones.sort(reverse=True)
        twos.sort(reverse=True)
        
        pre1 = [0]
        for x in ones:
            pre1.append(pre1[-1] + x)
        
        pre2 = [0]
        for x in twos:
            pre2.append(pre2[-1] + x)
        
        ans = float('inf')
        
        j = len(ones)
        
        for i in range(len(twos) + 1):
            mem2 = pre2[i]
            cost = 2 * i
            
            if mem2 >= m:
                ans = min(ans, cost)
                continue
            
            need = m - mem2
            
            # smallest j such that pre1[j] >= need
            l, r = 0, len(ones)
            while l <= r:
                mid = (l + r) // 2
                if pre1[mid] >= need:
                    j = mid
                    r = mid - 1
                else:
                    l = mid + 1
            
            if pre1[j] >= need:
                ans = min(ans, cost + j)
        
        print(ans if ans != float('inf') else -1)

if __name__ == "__main__":
    solve()
```

The implementation first partitions apps into two arrays and sorts each. The prefix sums allow constant-time evaluation of taking a fixed number from each group. The binary search finds the minimum number of cost-1 apps needed after fixing a choice of cost-2 apps. This avoids recomputing sums repeatedly and keeps the solution within logarithmic time per iteration over the second group.

A subtle point is that we must recompute the binary search for each choice of cost-2 count, because the remaining requirement changes. Another important detail is handling the case where cost-2 apps alone already satisfy the requirement.

## Worked Examples

### Example 1

Input:

```
n=5, m=7
a=[5,3,2,1,4]
b=[2,1,1,2,1]
```

We split:

| Group | Values |
| --- | --- |
| cost 1 | [3,2,4] |
| cost 2 | [5,1] |

Sorted:

cost 1 → [4,3,2]

cost 2 → [5,1]

Prefix sums:

cost 1: [0,4,7,9]

cost 2: [0,5,6]

We try choices:

| cost2 count | mem2 | remaining | best cost1 | total cost |
| --- | --- | --- | --- | --- |
| 0 | 0 | 7 | 2 (3+4) | 2 |
| 1 | 5 | 2 | 1 | 3 |
| 2 | 6 | 1 | 0 | 4 |

Minimum is 2.

This confirms that skipping expensive cost-2 apps entirely can be optimal.

### Example 2

Input:

```
n=4, m=10
a=[5,1,3,4]
b=[1,2,1,2]
```

cost 1: [5,3]

cost 2: [4,1]

Prefix sums:

cost 1: [0,5,8]

cost 2: [0,4,5]

Try:

| cost2 | mem2 | remaining | cost1 needed | total |
| --- | --- | --- | --- | --- |
| 0 | 0 | 10 | impossible | inf |
| 1 | 4 | 6 | 2 | 4 |
| 2 | 5 | 5 | 1 | 5 |

Best is 4.

This shows the trade-off between taking more cost-2 items versus relying on cost-1 heavy hitters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; each test also does a linear scan over cost-2 items with binary search over cost-1 prefix |
| Space | $O(n)$ | Storing two groups and prefix sums |

The total complexity is safe because the sum of $n$ across tests is bounded by $2 \cdot 10^5$, and each operation is at most logarithmic or linear in that total.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        ones, twos = [], []
        total = 0
        
        for ai, bi in zip(a, b):
            total += ai
            if bi == 1:
                ones.append(ai)
            else:
                twos.append(ai)
        
        if total < m:
            out.append("-1")
            continue
        
        ones.sort(reverse=True)
        twos.sort(reverse=True)
        
        pre1 = [0]
        for x in ones:
            pre1.append(pre1[-1] + x)
        
        pre2 = [0]
        for x in twos:
            pre2.append(pre2[-1] + x)
        
        ans = float('inf')
        
        for i in range(len(twos) + 1):
            mem2 = pre2[i]
            cost = 2 * i
            
            if mem2 >= m:
                ans = min(ans, cost)
                continue
            
            need = m - mem2
            l, r = 0, len(ones)
            j = len(ones)
            
            while l <= r:
                mid = (l + r) // 2
                if pre1[mid] >= need:
                    j = mid
                    r = mid - 1
                else:
                    l = mid + 1
            
            if pre1[j] >= need:
                ans = min(ans, cost + j)
        
        out.append(str(ans if ans != float('inf') else -1))
    
    return "\n".join(out)

# provided samples
assert run("""5
5 7
5 3 2 1 4
2 1 1 2 1
1 3
2
1
5 10
2 3 2 3 2
1 2 1 2 1
4 10
5 1 3 4
1 2 1 2
4 5
3 2 1 2
2 1 2 1
""") == """2
-1
6
4
3"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal impossible case | -1 | total memory insufficient |
| all cost-1 apps | greedy prefix correctness | cost-2 group empty |
| mixed heavy cost-2 | trade-off correctness | balance between groups |
| edge high m | boundary behavior | large requirement handling |
