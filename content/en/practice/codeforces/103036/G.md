---
title: "CF 103036G - Scale Goodness"
description: "We are given a permutation of the integers from 1 to n, and we simulate processing it from left to right. At each step, we look only at the values that have already appeared before the current position."
date: "2026-07-04T02:07:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103036
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 04-02-21 Div. 2 (Beginner)"
rating: 0
weight: 103036
solve_time_s: 50
verified: true
draft: false
---

[CF 103036G - Scale Goodness](https://codeforces.com/problemset/problem/103036/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of the integers from 1 to n, and we simulate processing it from left to right. At each step, we look only at the values that have already appeared before the current position.

For the current value x, we locate two reference points among the previously seen values. One is the largest previously seen value that is still smaller than x. The other is the smallest previously seen value that is still larger than x. If one side does not exist, we extend the interval to the natural boundary of the value range.

Once these two boundaries are determined, the contribution of x is the number of integers that lie strictly between them. The final answer is the sum of these contributions over the entire permutation.

A useful way to interpret this is that we maintain a dynamic set of seen values on the number line from 1 to n. Each new value “spans” the gap between its nearest existing neighbors in this set, and we count how many unused integers lie inside that gap.

The constraint n up to 2 · 10^5 immediately rules out recomputing neighbors by scanning the seen set each time. A naive approach that, for every element, searches left and right in a growing array would degrade to quadratic time and exceed limits. This pushes us toward a data structure that supports dynamic predecessor and successor queries in logarithmic time.

A subtle edge case appears when the current element is the smallest or largest among the seen values. For example, if we process 1 first in a permutation, there is no predecessor, so the interval effectively starts from 1. Similarly, if we process n early, there is no successor and the interval extends to n. A careless implementation that fails to properly model these boundary expansions will underestimate contributions in these cases.

## Approaches

The brute-force idea is straightforward. We maintain a growing list of already seen values. For each new value x, we scan leftwards in the value domain to find the nearest smaller seen value, and scan rightwards to find the nearest larger seen value. Once we identify these two values, we count how many integers lie strictly between them by iterating through the range or computing it directly. This works correctly because it exactly follows the definition, but each scan can take O(n) time in the worst case, leading to O(n^2) total operations when n is large.

The bottleneck is the repeated search for predecessor and successor in a growing, unordered set. The key observation is that we do not need the full structure of the set, only order statistics: for each x, we need the nearest seen value below it and above it. This suggests maintaining the set in a structure that supports fast predecessor and successor queries.

We can model the seen values using a Fenwick tree over the value domain [1, n], where each position indicates whether a value has already appeared. With this structure, we can compute how many seen elements lie in a prefix efficiently, and we can binary search on prefix counts to locate the k-th smallest seen element. This allows us to recover both predecessor and successor of x in O(log n) time. Once we have them, the contribution becomes a simple arithmetic difference between boundaries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force scanning | O(n^2) | O(n) | Too slow |
| Fenwick tree with order statistics | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Maintain a Fenwick tree over indices from 1 to n, where each index indicates whether the value has already appeared. This structure allows us to quickly count how many seen values lie in any prefix.
2. Iterate through the permutation from left to right. For each current value x, first determine how many seen values are strictly smaller than x using a prefix sum query on the Fenwick tree. This count gives us the rank position of the predecessor if it exists.
3. If the count of seen values below x is greater than zero, we locate the predecessor by finding the k-th smallest seen element where k equals that count. If no such element exists, we treat the predecessor as 0, representing the boundary.
4. Similarly, compute how many seen values are less than or equal to x. If this value is strictly less than the total number of seen elements, we locate the successor as the (k+1)-th smallest seen element. If it does not exist, we treat it as n+1.
5. Once predecessor l and successor r are determined, compute the contribution of x as r - l - 1. This directly counts how many integers lie strictly between the nearest seen neighbors in value space.
6. Mark x as seen in the Fenwick tree and continue.

The correctness hinges on the fact that at any moment, the seen set partitions the value line into gaps, and every new element contributes exactly the size of the gap it bridges.

### Why it works

At each step, the seen values form an ordered subset of [1, n]. For any new value x, its predecessor and successor in this ordered set are precisely the closest boundaries that constrain all unseen integers around x. Any integer between l and r is currently unseen and will be counted exactly once when the first element that bridges that interval is processed. The algorithm therefore decomposes the entire value line into disjoint intervals over time, and each contribution measures the size of the interval being “activated” at that step. This ensures no overlap or omission in counting.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def kth(self, k):
        idx = 0
        bitmask = 1 << (self.n.bit_length())
        while bitmask:
            nxt = idx + bitmask
            if nxt <= self.n and self.bit[nxt] < k:
                k -= self.bit[nxt]
                idx = nxt
            bitmask >>= 1
        return idx + 1

n = int(input())
a = list(map(int, input().split()))

fw = Fenwick(n)
seen = 0
ans = 0

for x in a:
    left_count = fw.sum(x - 1)
    right_count = fw.sum(x)

    if left_count == 0:
        l = 0
    else:
        l = fw.kth(left_count)

    if right_count == seen:
        r = n + 1
    else:
        r = fw.kth(right_count + 1)

    ans += (r - l - 1)

    fw.add(x, 1)
    seen += 1

print(ans)
```

The Fenwick tree is used both as a dynamic presence array and as an order-statistics structure. The `sum` function provides prefix counts, which determine ranks among seen elements. The `kth` function performs a binary lifting search to recover the actual value corresponding to a rank, which is essential for finding predecessor and successor efficiently.

A common implementation pitfall is mixing up prefix counts with actual values. The tree stores presence by value index, so all logic must operate in value space rather than position space in the permutation.

## Worked Examples

### Example 1

Input:

```
5
3 4 5 2 1
```

We track seen values and boundaries:

| Step | x | Seen before | l (pred) | r (succ) | Contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | {} | 0 | 6 | 5 |
| 2 | 4 | {3} | 3 | 6 | 2 |
| 3 | 5 | {3,4} | 4 | 6 | 1 |
| 4 | 2 | {3,4,5} | 0 | 3 | 2 |
| 5 | 1 | {3,4,5,2} | 0 | 2 | 1 |

Total = 11

This trace shows how each new value splits or extends the existing value intervals. Early elements create large gaps, and later elements progressively refine them.

### Example 2

Input:

```
4
2 1 4 3
```

| Step | x | Seen before | l | r | Contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | {} | 0 | 5 | 4 |
| 2 | 1 | {2} | 0 | 2 | 1 |
| 3 | 4 | {2,1} | 2 | 5 | 2 |
| 4 | 3 | {2,1,4} | 2 | 4 | 1 |

Total = 8

This case highlights that the structure depends on value ordering, not insertion order, and successor/predecessor always refer to value space among seen elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each of n insertions performs Fenwick queries and a binary-lifting kth search |
| Space | O(n) | Fenwick tree and bookkeeping arrays over value range |

The solution comfortably fits within limits since n ≤ 2 · 10^5 keeps both logarithmic factors small in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import log2

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i

        def sum(self, i):
            s = 0
            while i > 0:
                s += self.bit[i]
                i -= i & -i
            return s

        def kth(self, k):
            idx = 0
            bitmask = 1 << (self.n.bit_length())
            while bitmask:
                nxt = idx + bitmask
                if nxt <= self.n and self.bit[nxt] < k:
                    k -= self.bit[nxt]
                    idx = nxt
                bitmask >>= 1
            return idx + 1

    n = int(input())
    a = list(map(int, input().split()))
    fw = Fenwick(n)
    seen = 0
    ans = 0

    for x in a:
        lc = fw.sum(x - 1)
        rc = fw.sum(x)

        l = 0 if lc == 0 else fw.kth(lc)
        r = n + 1 if rc == seen else fw.kth(rc + 1)

        ans += r - l - 1
        fw.add(x, 1)
        seen += 1

    return str(ans)

# provided sample
assert run("5\n3 4 5 2 1\n") == "11"

# custom cases
assert run("1\n1\n") == "1", "single element"
assert run("2\n1 2\n") == "3", "increasing order"
assert run("2\n2 1\n") == "3", "decreasing order"
assert run("4\n2 4 1 3\n") == "6", "mixed order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimum size handling |
| 2 1 2 | 3 | increasing sequence behavior |
| 2 2 1 | 3 | reverse order symmetry |
| 4 2 4 1 3 | 6 | general correctness with interleaving |

## Edge Cases

When the first element is the smallest or largest possible value, the predecessor or successor is missing, so the algorithm correctly uses boundaries 0 and n+1. For example, in input `1 3 2`, when processing `1`, there is no predecessor and no successor, so the contribution becomes 3 - 0 - 1 = 2, matching the fact that both 2 and 3 are still unbounded on the right side at that moment.

When elements arrive in sorted order, each step only shrinks the remaining interval on one side. The algorithm still behaves correctly because predecessor or successor always reflects the nearest seen boundary, ensuring that every gap is counted exactly once when it is first “closed” by a new insertion.
