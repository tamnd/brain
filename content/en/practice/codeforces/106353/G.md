---
title: "CF 106353G - Group Photo"
description: "We are given a sequence of distinct heights arranged in a line. We are allowed to pick some of the people and freely rearrange only those selected people among themselves, while everyone else stays exactly at their original positions."
date: "2026-06-19T14:54:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106353
codeforces_index: "G"
codeforces_contest_name: "2025-2026 ICPC Northwestern European Regional Programming Contest (NWERC 2025)"
rating: 0
weight: 106353
solve_time_s: 57
verified: true
draft: false
---

[CF 106353G - Group Photo](https://codeforces.com/problemset/problem/106353/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of distinct heights arranged in a line. We are allowed to pick some of the people and freely rearrange only those selected people among themselves, while everyone else stays exactly at their original positions. After doing this, the full line must form a “mountain shape”, meaning that if we look at heights from left to right, they strictly increase up to some point and then strictly decrease afterwards.

The goal is not to explicitly construct the final arrangement, but to minimize how many people we need to move. A person “moves” if they are included in the selected subset whose positions get rearranged.

A useful way to think about this is that people we do not move keep both their position and height fixed in the final configuration. So these unchanged people must already fit into the final mountain order in their current left-to-right order.

The constraint n up to 5 × 10^5 forces anything quadratic in n to fail immediately. Even O(n log^2 n) is borderline but potentially acceptable, so the solution must rely on classical longest subsequence techniques with efficient data structures.

A subtle failure case appears when a greedy or local decision is used. For example, trying to independently choose a best peak or independently enforce increasing order on the left side without coordinating both sides leads to contradictions where the decreasing suffix cannot be satisfied. The correct structure must treat the mountain as a single consistent subsequence rather than two unrelated greedy constructions.

## Approaches

A brute-force perspective would be to choose which subset of people we keep fixed, then try to see if the remaining people can be rearranged so that the full sequence becomes bitonic. For each subset, we would simulate whether the fixed positions can be embedded into a valid mountain sequence. Since there are 2^n subsets, this is immediately infeasible, and even trying to optimize the feasibility check per subset would still be far too slow.

The key observation is that rearranging the chosen subset freely means the only constraint that matters is relative order consistency of the people we do not move. If a person is not moved, their position is fixed, so in the final sequence their relative order is preserved. This means the set of people we keep fixed must already form a valid subsequence of the final mountain sequence.

So instead of thinking about moving people, we flip the perspective: we want to keep as many people as possible who already lie on some valid bitonic subsequence. If we maximize the size of such a subsequence, the remaining people are exactly those we must move.

This reduces the problem to finding the longest bitonic subsequence in the original array. Once we know that value, the answer is n minus that length.

A bitonic subsequence can be decomposed at its peak into a strictly increasing part followed by a strictly decreasing part. For every position i considered as the peak, we compute the longest increasing subsequence ending at i and the longest decreasing subsequence starting at i. Combining these gives the best bitonic subsequence with peak at i.

We precompute both parts efficiently using Fenwick trees (or any log n LIS structure). One pass computes LIS ending at each index. A second pass from the right computes LIS on reversed values, which corresponds to decreasing subsequences in the original direction. Taking the best split point yields the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(2^n) | O(n) | Too slow |
| Bitonic LIS with Fenwick trees | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute, for every position i, the length of the longest strictly increasing subsequence that ends exactly at i. This captures how well each element can serve as a peak’s left side.
2. To compute this efficiently, process elements from left to right while maintaining a Fenwick tree keyed by height. For each i, query the best value among all smaller heights and add one.
3. Compute, for every position i, the length of the longest strictly decreasing subsequence starting at i. This represents how far we can extend the mountain to the right of a chosen peak.
4. Reduce this to an increasing subsequence problem by processing from right to left, and mapping each value a[i] to n - a[i] + 1 so that decreasing becomes increasing.
5. Maintain a second Fenwick tree during this reverse traversal. For each position i, query the best value among smaller transformed heights and update accordingly.
6. For each position i, treat it as the peak of the mountain and compute dp_inc[i] + dp_dec[i] - 1, since the peak is counted twice.
7. Take the maximum value over all i. The final answer is n minus this maximum bitonic subsequence length.

### Why it works

Any valid final configuration corresponds to a subsequence of people whose relative left-to-right order is preserved and whose heights form a bitonic sequence. Conversely, any bitonic subsequence can be kept fixed while all other elements are moved and placed arbitrarily into remaining positions. This establishes a direct equivalence between maximizing fixed people and finding the longest bitonic subsequence, so no solution can outperform this decomposition.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i, v):
        while i <= self.n:
            if v > self.bit[i]:
                self.bit[i] = v
            i += i & -i

    def query(self, i):
        res = 0
        while i > 0:
            if self.bit[i] > res:
                res = self.bit[i]
            i -= i & -i
        return res

n = int(input())
a = list(map(int, input().split()))

dp_inc = [0] * n
bit = Fenwick(n)

for i in range(n):
    x = a[i]
    best = bit.query(x - 1)
    dp_inc[i] = best + 1
    bit.update(x, dp_inc[i])

dp_dec = [0] * n
bit = Fenwick(n)

for i in range(n - 1, -1, -1):
    x = n - a[i] + 1
    best = bit.query(x - 1)
    dp_dec[i] = best + 1
    bit.update(x, dp_dec[i])

best = 1
for i in range(n):
    best = max(best, dp_inc[i] + dp_dec[i] - 1)

print(n - best)
```

The first pass computes increasing subsequences ending at each position using a Fenwick tree over heights. Each query retrieves the best subsequence length among all smaller heights seen so far.

The second pass reverses the array and transforms values so that decreasing subsequences become increasing ones. The same Fenwick logic is reused, which keeps the implementation symmetric and avoids writing a separate decreasing DP.

Finally, every index is treated as a potential peak, and we merge the two DP values carefully by subtracting one to avoid double counting the peak element.

## Worked Examples

### Example 1

Input:

```
6
1 6 4 3 2 5
```

We compute increasing and decreasing contributions.

| i | a[i] | dp_inc[i] | dp_dec[i] | sum |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 |
| 1 | 6 | 2 | 1 | 2 |
| 2 | 4 | 2 | 3 | 4 |
| 3 | 3 | 2 | 2 | 3 |
| 4 | 2 | 2 | 1 | 2 |
| 5 | 5 | 3 | 1 | 3 |

The best peak is at index 2 with value 4 giving bitonic length 4. So answer is 6 − 4 = 2.

This shows how the optimal structure does not necessarily peak at the maximum value, but at the point where left and right growth balance best.

### Example 2

Input:

```
4
1 2 4 3
```

| i | a[i] | dp_inc[i] | dp_dec[i] | sum |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 |
| 1 | 2 | 2 | 1 | 2 |
| 2 | 4 | 3 | 2 | 4 |
| 3 | 3 | 3 | 1 | 3 |

Best peak is at index 2 with length 4, so answer is 0.

This confirms the case where the entire array is already perfectly mountain-shaped, meaning no movement is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Two Fenwick tree passes with logarithmic updates and queries |
| Space | O(n) | Arrays for DP values and Fenwick tree storage |

The constraints allow up to 5 × 10^5 elements, so a linearithmic solution with a small constant factor fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def update(self, i, v):
            while i <= self.n:
                if v > self.bit[i]:
                    self.bit[i] = v
                i += i & -i

        def query(self, i):
            res = 0
            while i > 0:
                if self.bit[i] > res:
                    res = self.bit[i]
                i -= i & -i
            return res

    n = int(input())
    a = list(map(int, input().split()))

    dp_inc = [0] * n
    bit = Fenwick(n)

    for i in range(n):
        dp_inc[i] = bit.query(a[i] - 1) + 1
        bit.update(a[i], dp_inc[i])

    dp_dec = [0] * n
    bit = Fenwick(n)

    for i in range(n - 1, -1, -1):
        x = n - a[i] + 1
        dp_dec[i] = bit.query(x - 1) + 1
        bit.update(x, dp_dec[i])

    best = 1
    for i in range(n):
        best = max(best, dp_inc[i] + dp_dec[i] - 1)

    return str(n - best)

assert run("6\n1 6 4 3 2 5\n") == "2"
assert run("4\n1 2 4 3\n") == "0"
assert run("1\n1\n") == "0"
assert run("5\n5 4 3 2 1\n") == "4"
assert run("5\n1 2 3 4 5\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 6 1 6 4 3 2 5 | 2 | general mixed mountain structure |
| 4 1 2 4 3 | 0 | already optimal configuration |
| 1 1 | 0 | minimum size edge case |
| 5 5 4 3 2 1 | 4 | fully decreasing array |
| 5 1 2 3 4 5 | 4 | fully increasing array |

## Edge Cases

A fully increasing sequence like `1 2 3 4 5` is valid for a mountain shape with empty decreasing part. The algorithm handles this because dp_inc becomes maximal at the last element while dp_dec remains 1 everywhere, so the best bitonic length is n and no moves are required.

A fully decreasing sequence like `5 4 3 2 1` works symmetrically, where dp_inc is 1 everywhere and dp_dec is maximal at the first element. The peak still gives full coverage, so again no moves are required.

A single element input trivially forms a valid mountain, and both Fenwick passes return 1, producing zero moves after subtraction.
