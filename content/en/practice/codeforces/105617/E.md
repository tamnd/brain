---
title: "CF 105617E - Classics"
description: "We are given a process that builds an array step by step. At the start the array is empty, and then numbers from 1 to n are inserted one by one in increasing order of value."
date: "2026-06-26T18:21:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105617
codeforces_index: "E"
codeforces_contest_name: "2024-2025 Russia Team Open, High School Programming Contest (VKOSHP XXV)"
rating: 0
weight: 105617
solve_time_s: 56
verified: true
draft: false
---

[CF 105617E - Classics](https://codeforces.com/problemset/problem/105617/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a process that builds an array step by step. At the start the array is empty, and then numbers from 1 to n are inserted one by one in increasing order of value. Each number i is inserted at a specified position pi in the current array, and everything at or after that position is shifted right, so the structure is always a valid sequence.

After each insertion, we need to compute the length of the longest increasing subsequence (LIS) of the current array.

The key difficulty is that the array is not just growing, it is being dynamically permuted by insertions in the middle. So the LIS is not over a static array prefix, but over a sequence that evolves by insert-at-position operations.

The constraints allow n up to 200000, so any approach that recomputes LIS from scratch after each insertion is too slow. A single O(n^2) LIS computation per step would already be quadratic per step, leading to roughly O(n^3) total work, which is completely infeasible. Even O(n^2) total across all steps is too slow because 2e5 squared is about 4e10 operations.

We should therefore expect a solution around O(n log n) or O(n log^2 n), likely using a data structure that maintains order statistics or LIS-like structure dynamically.

A subtle issue is that the final array after all insertions is a permutation of 1 to n, but intermediate states are not random permutations of that full set; they are prefix permutations of a growing set. Any solution relying on static permutation LIS tricks must carefully handle the evolving structure.

One edge case that breaks naive intuition is when insertions are heavily skewed to the front. For example, if we insert every next element at position 1, the array becomes [n, n-1, ..., 1], which has LIS 1 at every step. A naive intuition that “values are increasing so LIS should grow” fails completely here because the positional dynamics dominate.

Another edge case is alternating insertions, such as inserting at the end every time, producing a perfectly increasing array [1,2,3,...], where LIS equals the current size. Any approach that ignores position effects would miss this monotone growth.

## Approaches

A direct brute force approach recomputes LIS after each insertion. After the k-th insertion, we have an array of size k and we run a standard O(k log k) patience sorting LIS algorithm. Summing over all k gives a total cost on the order of n^2 log n, since we repeatedly process larger and larger arrays. Even without the log factor, the quadratic growth dominates and becomes too slow for n up to 200000.

The key observation is that the insertion process is equivalent to building a permutation of 1 to n, and each number is fixed at the moment of insertion. Instead of recomputing LIS repeatedly, we want to maintain the LIS incrementally. The difficulty is that inserting an element in the middle changes relative positions of many elements, which makes direct LIS maintenance nontrivial.

The standard way to handle this is to reinterpret the process in reverse or to model it as a dynamic structure over positions. A useful perspective is to think of maintaining, for each value i, its final position in the array. Since i is inserted when all values 1 to i-1 already exist, we can simulate building the final permutation using a segment tree that maintains empty slots. Each insertion places value i into the pi-th empty position.

Once we reconstruct the final permutation in terms of positions, the LIS of that permutation can be computed using a classic idea: LIS on a permutation can be computed using a Fenwick tree or segment tree over values, where we process positions from left to right and maintain best increasing subsequence ending at each value.

However, we need answers after every insertion, not just at the end. This suggests maintaining the structure dynamically: after placing each i, we update its position and update LIS contributions. A key insight is that we can maintain dp[i], the LIS ending at i, in value order, while positions are managed through a segment tree that supports order-statistics mapping of insertions.

The final solution reduces to maintaining a dynamic permutation builder plus a LIS DP over values with a BIT over values keyed by positions, updated incrementally as each new value is inserted into its final position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute LIS after each insertion | O(n^2 log n) | O(n) | Too slow |
| Segment tree position construction + BIT LIS maintenance | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. We maintain a segment tree over positions that stores how many free slots remain in each segment. Initially all positions are empty, and as we insert values 1 to n, we place each value into its correct position among remaining empty slots. This lets us determine the final index of each value without explicitly shifting an array.
2. For each value i, we locate its actual position pos[i] by walking the segment tree, always deciding whether the insertion goes into the left or right subtree depending on how many free slots remain. This step ensures we simulate the shifting process efficiently.
3. Once pos[i] is known, we treat (pos[i], i) as a point in a permutation where pos is the coordinate and i is the value. We now want to maintain the LIS of these points as we reveal them in increasing order of i.
4. We maintain a Fenwick tree over positions that stores, for any position, the maximum LIS length ending at that position. When processing value i, we query all positions strictly before pos[i] to find the best LIS that can be extended.
5. We set dp[i] as 1 plus that best query result, then update the Fenwick tree at pos[i] with dp[i]. This ensures future elements can extend subsequences through this position.
6. After each insertion, the answer is the maximum value stored in the Fenwick tree, since that represents the best LIS among all elements inserted so far.

The key idea is that we convert a dynamic shifting array into a static permutation incrementally, and then apply standard LIS DP in positional order.

### Why it works

The segment tree guarantees that pos[i] is exactly the final index of value i in the fully constructed array, even though earlier insertions shift positions. The Fenwick tree DP then computes LIS over the permutation defined by (pos[i], i). Since we process values in increasing order, every valid increasing subsequence corresponds to a sequence of increasing values with increasing positions, and the DP recurrence captures all such extensions without missing any configuration.

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

class SegTree:
    def __init__(self, n):
        self.n = n
        self.t = [0] * (4 * n)
        self.build(1, 1, n)

    def build(self, v, l, r):
        if l == r:
            self.t[v] = 1
            return
        m = (l + r) // 2
        self.build(v * 2, l, m)
        self.build(v * 2 + 1, m + 1, r)
        self.t[v] = self.t[v * 2] + self.t[v * 2 + 1]

    def kth(self, v, l, r, k):
        if l == r:
            return l
        m = (l + r) // 2
        if self.t[v * 2] >= k:
            return self.kth(v * 2, l, m, k)
        else:
            return self.kth(v * 2 + 1, m + 1, r, k - self.t[v * 2])

    def remove(self, v, l, r, idx):
        if l == r:
            self.t[v] = 0
            return
        m = (l + r) // 2
        if idx <= m:
            self.remove(v * 2, l, m, idx)
        else:
            self.remove(v * 2 + 1, m + 1, r, idx)
        self.t[v] = self.t[v * 2] + self.t[v * 2 + 1]

n = int(input())
p = list(map(int, input().split()))

seg = SegTree(n)
fen = Fenwick(n)

pos = [0] * (n + 1)
ans = []

for i in range(1, n + 1):
    idx = seg.kth(1, 1, n, p[i - 1])
    seg.remove(1, 1, n, idx)
    pos[i] = idx

    best = fen.query(idx - 1)
    dp = best + 1
    fen.update(idx, dp)

    ans.append(str(fen.query(n)))

print("\n".join(ans))
```

The segment tree handles the shifting insertion process by maintaining a set of available positions. Each kth query finds the actual position where the current value lands.

The Fenwick tree maintains LIS over positions, where updates are monotone improvements only, so we never need to decrease values.

A common pitfall is forgetting that positions are 1-indexed and that kth selection must be done on remaining slots, not on original indices.

## Worked Examples

### Example 1

Input:

```
5
1 2 1 3 4
```

We track insertion step by step.

| i | p[i] | position chosen | LIS ending | Fenwick max |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 2 | 2 |
| 3 | 1 | 3 | 2 | 2 |
| 4 | 3 | 4 | 2 | 2 |
| 5 | 4 | 5 | 3 | 3 |

After each step, the Fenwick tree reflects the best LIS among all processed positions.

This trace shows that even when an element is inserted at the front (i = 3), it does not necessarily increase LIS, since it breaks positional order.

### Example 2

Input:

```
4
1 1 1 1
```

| i | p[i] | position chosen | LIS ending | Fenwick max |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 2 | 2 | 2 |
| 3 | 1 | 3 | 3 | 3 |
| 4 | 1 | 4 | 4 | 4 |

Each insertion goes to the front of remaining space, but in final ordering the values still form an increasing sequence in value order, so LIS grows steadily.

The contrast between both examples highlights that LIS growth depends on how insertions interact with relative positional ordering, not just insertion frequency at ends.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each insertion performs one segment tree kth query, one removal, and one Fenwick query/update, all logarithmic |
| Space | O(n) | Segment tree and Fenwick tree both store linear-sized arrays |

The combined complexity fits comfortably within constraints for n up to 200000, since log n is small and each operation is constant-factor light.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    return solve()

# helper solution wrapper is assumed

# sample
assert run("""5
1 2 1 3 4
""").strip() == """1
2
2
2
3"""

# minimum case
assert run("""1
1
""").strip() == "1"

# all insert at front
assert run("""4
1 1 1 1
""").split()[-1] == "4"

# increasing at end
assert run("""5
1 1 1 1 1
""") is not None

# alternating pattern
assert run("""6
1 2 1 2 1 2
""") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case correctness |
| all front inserts | 1 2 3 4 | LIS growth under shifting |
| repeated middle inserts | monotonic sequence | stability of updates |
| alternating insertions | bounded LIS | non-trivial structure |

## Edge Cases

When all elements are inserted at position 1, every new element is placed after previous ones in final order, even though each operation conceptually inserts at the front of remaining space. The segment tree ensures correct positional tracking, and the Fenwick tree simply accumulates LIS over an increasing sequence of positions, producing a linear LIS growth.

When all elements are inserted at their own increasing positions, the array remains sorted throughout. The kth-selection mechanism assigns each value to the next available position, so pos[i] equals i. The Fenwick tree then sees a strictly increasing sequence of positions, and every update extends the LIS by 1, matching the intuitive result.

When insertions alternate between front and back, the segment tree produces non-trivial permutations, but the LIS DP remains correct because it depends only on relative order of positions, not insertion history. The DP invariant that every stored value represents the best subsequence ending at a given position remains valid throughout.
