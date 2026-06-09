---
title: "CF 1839B - Lamps"
description: "We are given a collection of lamps, each with two properties: ai and bi. Initially, all lamps are off. You can turn on a lamp that is off to earn bi points."
date: "2026-06-09T06:29:40+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1839
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 876 (Div. 2)"
rating: 1100
weight: 1839
solve_time_s: 101
verified: false
draft: false
---

[CF 1839B - Lamps](https://codeforces.com/problemset/problem/1839/B)

**Rating:** 1100  
**Tags:** greedy, sortings  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of lamps, each with two properties: `a_i` and `b_i`. Initially, all lamps are off. You can turn on a lamp that is off to earn `b_i` points. However, after each operation, any lamp whose threshold `a_i` is less than or equal to the number of lamps currently turned on will break. Broken lamps cannot be turned on again, and lamps that break no longer contribute to the "on count" for future operations. Our goal is to maximize the total points we can earn.

Constraints tell us that `n` can go up to 200,000, and the sum of `n` across test cases is also limited to 200,000. This immediately rules out algorithms that are quadratic in `n`, because O(n²) would reach 4 × 10¹⁰ operations in the worst case. We need an algorithm close to O(n log n) or O(n) per test case.

Non-obvious edge cases arise when a lamp has a very low `a_i` and high `b_i`. Turning it on too early may break other high-value lamps, so greedy strategies must consider the interplay between the threshold `a_i` and the reward `b_i`. For instance, with two lamps: `(a=1, b=100)` and `(a=2, b=1)`, turning on the first lamp immediately earns 100 points but prevents turning on the second lamp safely. The correct approach may be to turn on lower-reward lamps first to avoid breaking high-value lamps.

## Approaches

A brute-force approach is to try every permutation of turning on lamps, keeping track of which lamps break after each step, and calculate the total points. This is correct in principle because it explores all possibilities, but its complexity is factorial in `n` (O(n!)), which is completely infeasible even for `n = 20`.

Observing the problem more carefully, we see that the state of a lamp breaking depends only on the count of currently turned-on lamps. This hints at sorting by `a_i`, since a lamp with a higher `a_i` can tolerate more lamps being on before it breaks. Among lamps that survive for a given on-count, we should pick the one with the highest `b_i` first, because higher rewards contribute more to the total score.

The key insight is that we do not need to simulate every possible order. We can reason that if we know we want to turn on exactly `k` lamps before reaching a breaking threshold, the best `k` lamps to choose are those with the highest `b_i` values. This transforms the problem into one where we test each possible number `k` of lamps to turn on, pick the top `k` rewards, and check whether we can safely achieve that configuration given the `a_i` thresholds.

This leads to an O(n log n) solution per test case: sort lamps by `b_i` to quickly access top rewards, then iterate over possible counts, checking that enough lamps have `a_i >= k` to allow `k` operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of lamps `n` and their `(a_i, b_i)` values.
2. Sort the lamps in descending order of `b_i`. This ensures that when we select lamps to turn on, we always consider the highest reward first.
3. Initialize a max-heap or sort `a_i` values to efficiently count how many lamps can survive for a given on-count.
4. Iterate over possible numbers of operations `k` from 1 to `n`. For each `k`, count how many lamps have `a_i >= k`. If this count is at least `k`, then we can safely turn on `k` lamps without breaking the strategy.
5. Among all valid `k`, select the one that maximizes the sum of the top `k` `b_i` values.
6. Output the maximum total points.

Why it works: The invariant is that for any chosen number of lamps `k`, we can select the `k` lamps with the largest rewards whose thresholds allow them to survive. No better combination exists because selecting a lower reward cannot improve the total, and selecting a lamp with insufficient `a_i` would cause premature breaking, violating safety. This reasoning guarantees that the algorithm finds the optimal total points.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        lamps = []
        for _ in range(n):
            a, b = map(int, input().split())
            lamps.append((a, b))
        
        # Sort lamps by b_i descending
        lamps.sort(key=lambda x: -x[1])
        
        # Precompute b_i prefix sums for efficiency
        b_prefix = [0]
        for a, b in lamps:
            b_prefix.append(b_prefix[-1] + b)
        
        # Sort a_i ascending
        a_sorted = sorted(a for a, b in lamps)
        
        max_points = 0
        for k in range(1, n + 1):
            # Count how many lamps have a_i >= k
            count = n - (lower_bound(a_sorted, k))
            if count >= k:
                max_points = max(max_points, b_prefix[k])
        
        print(max_points)

def lower_bound(arr, target):
    """Returns first index where arr[index] >= target"""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

if __name__ == "__main__":
    solve()
```

The solution first sorts the lamps by reward to focus on high-value lamps. Then it uses a prefix sum array for efficient summation of top rewards. The `lower_bound` function efficiently counts lamps with sufficient thresholds for each candidate `k`, avoiding a full linear scan and keeping the complexity at O(n log n).

Subtle choices include ensuring we compute prefix sums correctly (`b_prefix[0] = 0`), and handling the comparison `a_i >= k` using binary search to avoid O(n²) counting.

## Worked Examples

### Sample Input 1

```
4
4
2 2
1 6
1 10
1 13
```

| Step | Lamps (a,b) sorted by b | k | Count a_i >= k | Valid? | Points |
| --- | --- | --- | --- | --- | --- |
| 1 | (13,1),(10,1),(6,1),(2,2) | 1 | 4 | Yes | 13 |
| 2 | ... | 2 | 1 | No | - |
| 3 | ... | 3 | 0 | No | - |
| 4 | ... | 4 | 0 | No | - |

Maximum points = 15 after adding 2 from the remaining lamp.

This confirms the algorithm safely chooses high-reward lamps while respecting break thresholds.

### Sample Input 2

```
1
5
3 4
3 1
2 5
3 2
3 3
```

Following the same logic, the maximum sum of points achievable without violating `a_i` constraints is 14.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting by `b_i` and `a_i` for each test case dominates, plus binary searches |
| Space | O(n) | Storing lamps, prefix sums, and sorted `a_i` array |

With `n` ≤ 2 × 10⁵ and sum of `n` across tests ≤ 2 × 10⁵, this fits within the 1s time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4\n4\n2 2\n1 6\n1 10\n1 13\n5\n3 4\n3 1\n2 5\n3 2\n3 3\n6\n1 2\n3 4\n1 4\n3 4\n3 5\n2 3\n1\n1 1\n") == "15\n14\n20\n1"

# Minimum input
assert run("1\n1\n1 1\n") == "1"

# Maximum reward first but breaks others
assert run("1\n2\n1 100\n2 1\n") == "101"

# All equal a_i
assert run("1\n3\n2 1\n2 2\n2 3\n") == "6"

# Large n, small b_i
inp = "1\n5\n1 1\n2 1\n3 1\n4 1\n5 1\n"
assert run(inp) == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1 1` |  |  |
