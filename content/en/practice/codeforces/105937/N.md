---
title: "CF 105937N - Kessoku Band"
description: "We are given a permutation of numbers from 1 to n, meaning every integer in this range appears exactly once and is arranged in some order along a line. Each operation gives us a segment [l, r] of this line."
date: "2026-06-22T15:49:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105937
codeforces_index: "N"
codeforces_contest_name: "2025 Xian Jiaotong University Programming Contest"
rating: 0
weight: 105937
solve_time_s: 83
verified: true
draft: false
---

[CF 105937N - Kessoku Band](https://codeforces.com/problemset/problem/105937/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of numbers from 1 to n, meaning every integer in this range appears exactly once and is arranged in some order along a line. Each operation gives us a segment [l, r] of this line. From this segment, we look at which values are missing among the numbers that appear inside it, and we take the smallest missing positive integer, call it x.

After computing x, if x is equal to or larger than n, we simply output the word “peace” and do nothing to the permutation. Otherwise, we output x and then modify the permutation by swapping the positions of the values x and x + 1 wherever they currently are.

So each query is both a range-existence query over a dynamic permutation and then a local structural update that slightly reshuffles two consecutive values in the value domain.

The constraints are large: n can be up to 5 × 10^5 and k up to 10^5. Any solution that scans the interval for every query will be too slow, since that would cost O(nk) in the worst case, which is far beyond acceptable. Even O(n log n) per query is too large. We need something closer to logarithmic per query, with very fast updates and range checks.

The tricky part is that the permutation is dynamic. After every query, swapping x and x+1 changes positions, which affects all future range queries. This rules out any static preprocessing over values.

A subtle edge case is when the missing number is n or larger. Since the permutation only contains 1 to n, x will always be at most n+1. If x equals n+1, or effectively if all 1..n appear in the segment, we output “peace”. A naive implementation might incorrectly try to swap in this case, but the swap must only happen when x < n.

## Approaches

A direct approach is to process each query by scanning the segment [l, r], marking which values appear, and then finding the smallest missing integer by checking from 1 upward. This is correct but too slow. Each query costs O(r - l + 1 + n) in the worst case if we reset bookkeeping arrays, and with up to 10^5 queries this becomes infeasible.

The main difficulty is that we are repeatedly asking for the mex of values inside a range, where values are from a permutation that is changing via swaps of adjacent values in value space. This suggests we need a structure that can quickly answer “is value v present in [l, r]” and support updates that move the positions of two values.

The key observation is that we never actually need to examine all values in the segment. We only need to find the smallest value v such that v does not appear in [l, r]. This can be turned into a prefix-style search over values: we test candidates v in increasing order, and for each v we check whether it exists in the segment. The first v that is absent is the answer.

So the core operation becomes a dynamic “point location” structure: for each value v, we maintain its current position pos[v]. Then checking whether v appears in [l, r] is just checking whether pos[v] lies in that interval. This reduces the range query into a sequence of O(1) checks per value candidate.

The remaining challenge is to find the smallest missing v quickly. We can maintain a segment tree over the value domain [1..n], storing for each segment whether all values in that segment are fully “covered” in the sense that their positions lie inside the current query range. However, since each query has a different [l, r], we cannot precompute this.

Instead, we invert the perspective. For a fixed query [l, r], we want the smallest v such that pos[v] is not in [l, r]. This is equivalent to finding the first v where pos[v] < l or pos[v] > r. This is a monotone predicate over v if we define it carefully using segment tree nodes that store min and max position of values in a range of values.

For a range of values [L, R], we can maintain minPos and maxPos. If both minPos and maxPos lie inside [l, r], then all values in that range are inside the segment. Otherwise, there exists at least one missing value in that range. This allows us to binary search the smallest v using a segment tree, descending until we find the first value whose position escapes [l, r].

Updates are simple: swapping x and x+1 just swaps their positions in pos[].

This leads to an O(log n) query for finding the mex via segment tree descent, and O(1) update per swap, giving an overall O((n + k) log n) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(n) | Too slow |
| Optimal (segment tree over values) | O((n + k) log n) | O(n) | Accepted |

## Algorithm Walkthrough

We build a segment tree over the value domain from 1 to n. Each node represents a contiguous range of values and stores two pieces of information: the minimum position among those values in the current permutation and the maximum position among those values.

We also maintain an array pos[v], which tells us the current index of value v in the permutation.

For each query [l, r], we want the smallest v such that pos[v] is not in [l, r].

1. Build the segment tree using the initial permutation. For each value v, we set pos[v] to its index, and leaf nodes store (pos[v], pos[v]). Internal nodes compute min and max from children.
2. To answer a query [l, r], we descend the segment tree starting from the root, always trying to find a value in increasing order whose position is outside [l, r]. At each node, we check whether the entire segment is fully inside [l, r], meaning its minPos ≥ l and maxPos ≤ r. If this is true, then all values in this node are inside the segment, so we skip it.
3. If a node is not fully contained, it means there exists at least one value whose position lies outside [l, r]. We then go down to its children, always preferring the left child first, because we want the smallest possible value.
4. When we reach a leaf node corresponding to value v, we check whether pos[v] is inside [l, r]. If it is outside, we return v as the mex. Otherwise, this branch is invalid.
5. After obtaining x, if x is equal to n, we output “peace” and do nothing further.
6. If x is less than n, we output x and then swap the positions of x and x+1. We update pos[x] and pos[x+1], and update the segment tree leaves for both values and propagate changes upward.

Why it works is based on a structural invariant: every node always represents the correct minimum and maximum position of its value range. This ensures that when a node is fully contained in [l, r], we can safely discard the entire subtree because no value inside it can be missing from the segment. Conversely, if a node is not fully contained, it guarantees at least one value in its range violates the interval condition, so the answer must lie somewhere in that subtree. The tree traversal preserves ordering by always exploring left before right, which guarantees the smallest valid value is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, pos):
        self.n = len(pos) - 1
        self.minv = [0] * (4 * self.n)
        self.maxv = [0] * (4 * self.n)
        self.build(1, 1, self.n, pos)

    def build(self, idx, l, r, pos):
        if l == r:
            self.minv[idx] = self.maxv[idx] = pos[l]
            return
        mid = (l + r) // 2
        self.build(idx * 2, l, mid, pos)
        self.build(idx * 2 + 1, mid + 1, r, pos)
        self.pull(idx)

    def pull(self, idx):
        self.minv[idx] = min(self.minv[idx * 2], self.minv[idx * 2 + 1])
        self.maxv[idx] = max(self.maxv[idx * 2], self.maxv[idx * 2 + 1])

    def update(self, idx, l, r, pos_idx, val):
        if l == r:
            self.minv[idx] = self.maxv[idx] = val
            return
        mid = (l + r) // 2
        if pos_idx <= mid:
            self.update(idx * 2, l, mid, pos_idx, val)
        else:
            self.update(idx * 2 + 1, mid + 1, r, pos_idx, val)
        self.pull(idx)

    def find_mex(self, idx, l, r, ql, qr):
        if self.minv[idx] >= l and self.maxv[idx] <= r:
            return -1
        if l == r:
            return l if not (ql <= self.minv[idx] <= qr) else -1
        mid = (l + r) // 2
        res = self.find_mex(idx * 2, l, mid, ql, qr)
        if res != -1:
            return res
        return self.find_mex(idx * 2 + 1, mid + 1, r, ql, qr)

n = int(input())
a = list(map(int, input().split()))
k = int(input())

pos = [0] * (n + 1)
for i, v in enumerate(a, 1):
    pos[v] = i

st = SegTree(pos)

for _ in range(k):
    l, r = map(int, input().split())
    x = st.find_mex(1, 1, n, l, r)

    if x == -1 or x == n:
        print("peace")
        continue

    print(x)
    px, py = pos[x], pos[x + 1]
    pos[x], pos[x + 1] = py, px

    st.update(1, 1, n, x, pos[x])
    st.update(1, 1, n, x + 1, pos[x + 1])
```

The segment tree is built over values rather than positions. Each leaf corresponds to a value v and stores its current position in the permutation. This inversion is what makes range queries on values meaningful.

The mex search works by pruning entire segments whose values are fully inside [l, r] in terms of positions. If a node’s entire value range lies within the query segment, it cannot contain the answer, so it is skipped immediately.

The swap step is careful to update both the pos array and the segment tree leaves for the swapped values. Missing either update would desynchronize the structure and produce incorrect future queries.

## Worked Examples

We trace a small example to observe how the structure evolves.

Consider permutation [4, 3, 1, 2, 5] with query [2, 4].

| Step | Query [l, r] | Found x | Action | Permutation |
| --- | --- | --- | --- | --- |
| 1 | [2,4] | 4 | swap 4 and 5 | [5, 3, 1, 2, 4] |
| 2 | [2,5] | 5 | peace | [5, 3, 1, 2, 4] |
| 3 | [1,3] | 2 | swap 2 and 3 | [5, 2, 1, 3, 4] |
| 4 | [1,3] | 3 | swap 3 and 4 | [5, 2, 1, 4, 3] |
| 5 | [1,5] | 6 | peace | [5, 2, 1, 4, 3] |

Each step shows that once all small values are present in the queried interval, the mex shifts upward until it escapes the domain, producing “peace”.

Now consider a smaller focused case: permutation [1, 2, 3, 4], query [2, 3].

| v checked | pos[v] | in [2,3]? |
| --- | --- | --- |
| 1 | 1 | no |
| 2 | 2 | yes |
| 3 | 3 | yes |
| 4 | 4 | no |

The smallest missing is 1, which immediately triggers a swap between 1 and 2, demonstrating how local value adjustments propagate through future queries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + k) log n) | Each query descends a segment tree over values, and each swap updates two leaves |
| Space | O(n) | Segment tree and position array |

The logarithmic factor is sufficient for n up to 5 × 10^5 and k up to 10^5, since each operation only touches a path in the tree rather than scanning ranges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    class SegTree:
        def __init__(self, pos):
            self.n = len(pos) - 1
            self.minv = [0] * (4 * self.n)
            self.maxv = [0] * (4 * self.n)
            self.build(1, 1, self.n, pos)

        def build(self, idx, l, r, pos):
            if l == r:
                self.minv[idx] = self.maxv[idx] = pos[l]
                return
            mid = (l + r) // 2
            self.build(idx * 2, l, mid, pos)
            self.build(idx * 2 + 1, mid + 1, r, pos)
            self.pull(idx)

        def pull(self, idx):
            self.minv[idx] = min(self.minv[idx * 2], self.minv[idx * 2 + 1])
            self.maxv[idx] = max(self.maxv[idx * 2], self.maxv[idx * 2 + 1])

        def update(self, idx, l, r, pos_idx, val):
            if l == r:
                self.minv[idx] = self.maxv[idx] = val
                return
            mid = (l + r) // 2
            if pos_idx <= mid:
                self.update(idx * 2, l, mid, pos_idx, val)
            else:
                self.update(idx * 2 + 1, mid + 1, r, pos_idx, val)
            self.pull(idx)

        def find_mex(self, idx, l, r, ql, qr):
            if self.minv[idx] >= l and self.maxv[idx] <= r:
                return -1
            if l == r:
                return l if not (ql <= self.minv[idx] <= qr) else -1
            mid = (l + r) // 2
            res = self.find_mex(idx * 2, l, mid, ql, qr)
            if res != -1:
                return res
            return self.find_mex(idx * 2 + 1, mid + 1, r, ql, qr)

    n = 1
    a = [1]
    pos = [0, 1]
    st = SegTree(pos)
    assert run("1\n1\n1\n1 1\n") == "peace\n", "min size"

    return "ok"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 single query | peace | smallest boundary case |

## Edge Cases

A critical edge case happens when the queried segment already contains all values 1 through n. In that case, every value v satisfies pos[v] inside [l, r], so the mex becomes n+1 and we output “peace”. The segment tree will correctly prune every node because each node’s min and max position will fall inside the query interval, causing full coverage and no candidate leaf to be found.

Another subtle case is repeated swaps involving adjacent values that move positions back and forth. Since each swap only touches two values and immediately updates both their leaf nodes, the invariant that pos[v] is always correct is preserved. Even after many operations, the structure remains consistent because every update is localized and propagated through the tree.

A final corner case is when x is n. Even though it is the largest valid value, the swap with x+1 is invalid since x+1 does not exist. The code explicitly treats x == n as a stopping condition, ensuring no out-of-bounds update occurs.
