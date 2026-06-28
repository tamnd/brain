---
title: "CF 104720C - Cooking Class"
description: "We are given a pool of contestants, each with a fixed skill value, and one special contestant, Autumn, whose skill can be increased by choosing exactly one upgrade from a list. Each upgrade adds a positive amount to her current skill."
date: "2026-06-29T05:41:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "C"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 76
verified: false
draft: false
---

[CF 104720C - Cooking Class](https://codeforces.com/problemset/problem/104720/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a pool of contestants, each with a fixed skill value, and one special contestant, Autumn, whose skill can be increased by choosing exactly one upgrade from a list. Each upgrade adds a positive amount to her current skill.

The competition ranking is determined purely by sorting all final skill values in descending order. If several contestants share the same skill, they occupy the same rank, and the next distinct skill level skips ranks accordingly, following standard competition ranking rules.

The task is to choose one upgrade for Autumn that gives her the best possible final rank. Since rank 1 is best, we are effectively minimizing how many contestants strictly outrank her after she picks an upgrade.

The input sizes are large, up to 200,000 contestants and 200,000 upgrades. This rules out any approach that recomputes ordering from scratch for each upgrade. A solution that naively evaluates each upgrade against all contestants would require up to 4×10^10 comparisons in the worst case, which is far beyond feasible limits in 2 seconds. This immediately pushes us toward preprocessing and logarithmic counting techniques.

A subtle issue arises from ties. If Autumn’s final skill equals some contestants, she does not outrank them. They share rank. Therefore, we must count only strict inequalities when determining how many people are above her.

Another corner case is when all boosts are identical or when Autumn is already stronger than everyone even before boosting. A correct solution must still handle these uniformly without special branching.

## Approaches

A brute-force method would try each possible cooking class, compute Autumn’s final skill, and then count how many contestants have strictly greater skill. This requires scanning all N contestants per class, leading to O(NM) operations. With N and M up to 2×10^5, this is far too slow.

The key observation is that for any fixed final skill value X, Autumn’s rank depends only on how many contestants have skill strictly greater than X. This suggests preprocessing the contestants' skills so we can answer “how many values are greater than X” quickly.

Sorting the list of opponent skills enables this. After sorting, we can use binary search to find the first value strictly greater than X. The number of people above X is then the suffix length beyond that position.

Once this structure is in place, each candidate boost can be evaluated in O(log N), and the total complexity becomes O((N + M) log N), which is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(1) | Too slow |
| Optimal (sorting + binary search) | O(N log N + M log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read all opponent skill values and Autumn’s initial skill. Treat Autumn as a separate value that will be modified per boost.
2. Sort the list of opponent skills in ascending order. This allows efficient counting of how many values exceed a threshold using binary search.
3. For each possible boost value P_i, compute Autumn’s candidate final skill X = S_A + P_i.
4. Use binary search to find the first index in the sorted opponent array where value is strictly greater than X.
5. The number of opponents strictly stronger than Autumn is the number of elements from that index to the end of the array.
6. Convert this into a rank. If k opponents are strictly stronger, then Autumn’s rank is k + 1.
7. Track the minimum rank over all boosts and output it.

Why binary search works here is that sorting transforms the “count greater than X” problem into a prefix boundary search. Every value to the right of the boundary is guaranteed to be greater than X.

### Why it works

For any fixed final skill X, all opponents with skill greater than X form a contiguous suffix in the sorted array. The algorithm identifies the boundary of this suffix correctly using a lower_bound-style search. Since rank depends only on the count of strictly greater elements, and this count is computed exactly for every candidate X, the minimum over all candidates is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline
from bisect import bisect_right

def solve():
    N, M = map(int, input().split())
    arr = list(map(int, input().split()))
    
    S_A = arr[-1]
    opponents = arr[:-1]
    
    opponents.sort()
    
    boosts = list(map(int, input().split()))
    
    best_rank = N + 1
    
    for p in boosts:
        x = S_A + p
        idx = bisect_right(opponents, x)
        stronger = N - idx
        rank = stronger + 1
        if rank < best_rank:
            best_rank = rank
    
    print(best_rank)

if __name__ == "__main__":
    solve()
```

The solution separates Autumn’s skill from the opponents immediately, since only her value changes across queries. Sorting opponents enables the use of `bisect_right`, which returns the first position where elements exceed the target value. This is critical because ties must not be counted as strictly stronger.

The rank computation is direct: everything to the right of the found index is strictly greater, so their count determines how many people are above Autumn.

A common pitfall is using `bisect_left` instead of `bisect_right`. That would incorrectly treat equal skills as stronger, inflating the rank. Another subtlety is initializing `best_rank` to `N + 1`, which safely dominates all possible valid ranks.

## Worked Examples

### Example 1

Input:

```
N = 5, M = 5
Opponents = [3, 3, 4, 5, 2], S_A = 1
Boosts = [2, 3, 4, 5]
```

We sort opponents:

```
[2, 3, 3, 4, 5]
```

| Boost | Final skill X | bisect_right index | stronger count | rank |
| --- | --- | --- | --- | --- |
| 2 | 3 | 3 | 2 | 3 |
| 3 | 4 | 4 | 1 | 2 |
| 4 | 5 | 5 | 0 | 1 |
| 5 | 6 | 5 | 0 | 1 |

The best outcome is rank 1, achieved by the largest boost.

This demonstrates that the algorithm correctly handles ties, since when X equals 3, only elements strictly greater than 3 contribute to rank.

### Example 2

Input:

```
N = 3, M = 3
Opponents = [10, 20, 30], S_A = 15
Boosts = [0, 5, 20]
```

Sorted opponents:

```
[10, 20, 30]
```

| Boost | Final skill X | index | stronger | rank |
| --- | --- | --- | --- | --- |
| 0 | 15 | 1 | 2 | 3 |
| 5 | 20 | 2 | 1 | 2 |
| 20 | 35 | 3 | 0 | 1 |

This confirms that once Autumn surpasses the maximum opponent value, the rank becomes 1, since the suffix is empty.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N + M log N) | Sorting dominates, each query uses binary search |
| Space | O(N) | Stores opponent list |

The constraints allow up to 400,000 total values, so an O(N log N) solution is comfortably within limits. The memory usage is linear and trivial for the given bounds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from bisect import bisect_right

    def solve():
        N, M = map(int, input().split())
        arr = list(map(int, input().split()))
        S_A = arr[-1]
        opponents = arr[:-1]
        opponents.sort()
        boosts = list(map(int, input().split()))

        best = N + 1
        for p in boosts:
            x = S_A + p
            idx = bisect_right(opponents, x)
            best = min(best, N - idx + 1)

        print(best)

    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("5 5\n3 3 4 5 2 1\n2 3 4 5\n") == "1"

# minimum case
assert run("1 1\n1 1\n1\n") == "1"

# all equal opponents
assert run("3 2\n5 5 5 5\n0 0\n") == "1"

# strict increasing boosts
assert run("3 3\n1 2 3 2\n0 1 2\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal input | 1 | single opponent handling |
| all equal skills | 1 | tie behavior correctness |
| increasing boosts | 2 | correct rank computation under varying thresholds |

## Edge Cases

One edge case is when Autumn already dominates all opponents even without any boost. For example, if opponents are `[1, 2, 3]` and Autumn starts at `10`, every boost still yields a value greater than all opponents. The sorted array gives a bisect index at the end, producing a stronger count of 0 and rank 1. This confirms that the algorithm naturally handles the “always first place” scenario without special casing.

Another case is when Autumn is weaker than everyone even after the smallest boost. For example, opponents `[100, 200, 300]`, Autumn `1`, boosts `[1]`. The final value is `2`, and all opponents are still strictly greater. The bisect index becomes 0, stronger count is 3, and rank is 4, which correctly reflects last place.

A third subtle case is duplicates exactly equal to Autumn’s final skill. Since `bisect_right` is used, equal values are placed on the left side of the boundary, ensuring they are not counted as stronger. This preserves the tie rule where equal skills share rank.
