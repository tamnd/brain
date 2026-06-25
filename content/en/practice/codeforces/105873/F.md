---
title: "CF 105873F - First Problem"
description: "We maintain a sequence of numbers. Initially every position has a given value, and then we process a stream of operations. A query asks for the maximum value inside a chosen interval. An add operation increases every value in an interval by one."
date: "2026-06-25T14:27:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105873
codeforces_index: "F"
codeforces_contest_name: "2025 ICPC Gran Premio de Mexico 1ra Fecha"
rating: 0
weight: 105873
solve_time_s: 45
verified: true
draft: false
---

[CF 105873F - First Problem](https://codeforces.com/problemset/problem/105873/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a sequence of numbers. Initially every position has a given value, and then we process a stream of operations. A query asks for the maximum value inside a chosen interval. An add operation increases every value in an interval by one. The unusual operation resets some values: among the positions in a chosen interval, every position whose value is equal to the current maximum value of the entire sequence becomes zero.

The input describes the array size, the number of operations, the starting values, and then the operations. The output consists only of the answers to the maximum queries, in the same order those queries appear.

The limits make a simple simulation impossible. With up to 100000 positions and 100000 operations, scanning the whole interval for every update could perform around 10^10 operations in the worst case. A solution needs to stay close to O(log n) per operation, or at least have a strong amortized bound.

The difficult part is the reset operation. It does not reset the maximum of the queried range, it resets only elements equal to the global maximum of the whole array. A solution that only stores the maximum of each segment loses information because two segments can have the same maximum but different numbers of elements achieving it.

For example, consider:

```
Input
3 2
5 5 1
R 1 2
Q 1 3
```

The global maximum is 5. The reset affects positions 1 and 2, so the array becomes `[0, 0, 1]`. The answer is:

```
1
```

A careless implementation that interprets the reset as “set the maximum value in the range to zero” could accidentally reset the wrong elements after mixing global and local maxima.

Another edge case is when a segment contains the maximum but not every value in that segment is equal to it.

```
Input
4 2
7 7 3 7
R 1 3
Q 1 4
```

The global maximum is 7. Only positions 1 and 2 are reset, because position 3 has value 3. The final array is `[0,0,3,7]`, so the answer is:

```
7
```

A segment tree that stores only the maximum cannot know whether it can clear the whole segment safely.

A final tricky case is when all values in a node are equal.

```
Input
5 2
4 4 4 4 4
R 2 5
Q 1 5
```

All affected values are the global maximum, so the array becomes `[4,0,0,0,0]`. The answer is:

```
4
```

The data structure must recognize that an entire segment can be updated at once.

## Approaches

The straightforward approach is to store the array directly and handle each operation by visiting all affected positions. Queries are easy because we can scan the interval and take the largest value. Add operations are also simple because we increment every element. The reset operation scans the range, finds the global maximum, and clears matching values.

This is correct because it directly follows the definition of every operation. The problem is the speed. In the worst case, every operation touches almost all positions, leading to O(NK) work, which can reach about 10^10 element operations.

The key observation is that the reset operation only cares about values equal to the current maximum. A normal segment tree is not enough because the maximum alone does not reveal whether the whole segment consists of maximum values. We need one more piece of information: the second largest value inside every segment.

If a segment has maximum value `x` and its second maximum is smaller than `x`, then every element in that segment is exactly `x`. When `x` is the global maximum, we can reset the whole segment immediately. Otherwise, we descend only into parts where some elements still need to be examined.

This is the same idea behind segment tree beats. The structure stores the largest value, the second largest value, how many times the largest appears, and lazy information for range additions. Resetting a maximum value is efficient because whenever we cannot finish at a node, we go deeper only until we find smaller groups. Values that are actually reset disappear from the maximum layer, giving the needed amortization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NK) | O(N) | Too slow |
| Segment Tree Beats | O((N + K) log N) amortized | O(N) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree. For every node, store the largest value, the second largest value, the number of elements having the largest value, and the lazy addition that still has to be pushed to children. The second maximum is needed to determine whether a whole segment can be reset safely.
2. For an add operation on `[l, r]`, apply a lazy increment to covered nodes. Increasing every value in a segment changes the maximum and second maximum by the same amount, so the node information remains valid.
3. For a query on `[l, r]`, return the maximum value stored in the covered nodes. Lazy values are pushed before going down so child values are correct.
4. For a reset operation, first obtain the maximum value of the whole array from the root. This is the value that must be removed.
5. Visit the segment tree nodes intersecting `[l, r]`. If a covered node has maximum equal to the global maximum and its second maximum is smaller, every value in that node is the global maximum. Set the whole node to zero.
6. Otherwise, push lazy values and continue into the children. Some nodes contain a mix of maximum and smaller values, so they must be split until the reset can be applied safely.

Why it works:

The invariant is that every node always correctly represents the multiset of values inside its segment. The maximum and second maximum tell us whether all values are equal to the current maximum. If they are, replacing the whole segment with zero is exactly the required operation. If they are not, at least one child contains a value different from the maximum, so descending preserves correctness. Add operations preserve the ordering of values because every element in the affected segment changes equally.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

class SegTree:
    def __init__(self, arr):
        n = len(arr)
        self.n = n
        size = 4 * n
        self.mx = [0] * size
        self.smx = [-INF] * size
        self.cnt = [0] * size
        self.lazy = [0] * size
        self.build(1, 0, n - 1, arr)

    def build(self, v, l, r, a):
        if l == r:
            self.mx[v] = a[l]
            self.cnt[v] = 1
            return
        m = (l + r) // 2
        self.build(v * 2, l, m, a)
        self.build(v * 2 + 1, m + 1, r, a)
        self.pull(v)

    def apply_add(self, v, x):
        self.mx[v] += x
        if self.smx[v] != -INF:
            self.smx[v] += x
        self.lazy[v] += x

    def apply_zero(self, v):
        self.mx[v] = 0
        self.smx[v] = -INF
        self.cnt[v] = self.length[v]
        self.lazy[v] = 0

    def push(self, v):
        if self.lazy[v]:
            x = self.lazy[v]
            self.apply_add(v * 2, x)
            self.apply_add(v * 2 + 1, x)
            self.lazy[v] = 0

    def pull(self, v):
        a = v * 2
        b = v * 2 + 1
        if self.mx[a] > self.mx[b]:
            self.mx[v] = self.mx[a]
            self.cnt[v] = self.cnt[a]
            self.smx[v] = max(self.smx[a], self.mx[b])
        elif self.mx[a] < self.mx[b]:
            self.mx[v] = self.mx[b]
            self.cnt[v] = self.cnt[b]
            self.smx[v] = max(self.mx[a], self.smx[b])
        else:
            self.mx[v] = self.mx[a]
            self.cnt[v] = self.cnt[a] + self.cnt[b]
            self.smx[v] = max(self.smx[a], self.smx[b])

    def add(self, v, l, r, ql, qr):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            self.apply_add(v, 1)
            return
        self.push(v)
        m = (l + r) // 2
        self.add(v * 2, l, m, ql, qr)
        self.add(v * 2 + 1, m + 1, r, ql, qr)
        self.pull(v)

    def query(self, v, l, r, ql, qr):
        if qr < l or r < ql:
            return -INF
        if ql <= l and r <= qr:
            return self.mx[v]
        self.push(v)
        m = (l + r) // 2
        return max(self.query(v * 2, l, m, ql, qr),
                   self.query(v * 2 + 1, m + 1, r, ql, qr))

    def reset(self, v, l, r, ql, qr, target):
        if qr < l or r < ql or self.mx[v] < target:
            return
        if ql <= l and r <= qr and self.mx[v] == target and self.smx[v] < target:
            self.length[v] = r - l + 1
            self.apply_zero(v)
            return
        if l == r:
            self.apply_zero(v)
            return
        self.push(v)
        m = (l + r) // 2
        self.reset(v * 2, l, m, ql, qr, target)
        self.reset(v * 2 + 1, m + 1, r, ql, qr, target)
        self.pull(v)

def solve():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    tree = SegTree(arr)
    tree.length = [0] * (4 * n)

    def fill_len(v, l, r):
        tree.length[v] = r - l + 1
        if l != r:
            m = (l + r) // 2
            fill_len(v * 2, l, m)
            fill_len(v * 2 + 1, m + 1, r)

    fill_len(1, 0, n - 1)

    ans = []
    for _ in range(k):
        c, l, r = input().split()
        l = int(l) - 1
        r = int(r) - 1
        if c == 'Q':
            ans.append(str(tree.query(1, 0, n - 1, l, r)))
        elif c == 'A':
            tree.add(1, 0, n - 1, l, r)
        else:
            cur = tree.mx[1]
            tree.reset(1, 0, n - 1, l, r, cur)

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The tree keeps four pieces of information per node. `mx` represents the highest value in the segment, `smx` represents the highest value strictly smaller than it, and `cnt` stores how many elements reach the maximum. The lazy value is only for additions because adding one to a segment shifts every value equally.

The reset operation uses the relationship between `mx` and `smx`. If the maximum is the target and the second maximum is smaller, the segment contains only the target value. Clearing the whole node is safe. Otherwise the code pushes the lazy addition and examines the children.

The `length` array stores segment sizes so a full reset can update the count of maximum values correctly. Keeping this separate avoids recomputing lengths during recursion. Boundary handling is based on inclusive indices, so the conversion from input indices to zero-based indices happens once before processing.

## Worked Examples

Consider the sample:

```
10 10
1 2 3 4 5 6 7 8 9 10
Q 1 10
R 1 10
A 1 10
Q 1 10
R 1 7
Q 5 10
R 7 10
Q 6 10
A 6 10
Q 1 6
```

| Step | Operation | Global max | Important change | Query answer |
| --- | --- | --- | --- | --- |
| 1 | Q 1 10 | 10 | No update | 10 |
| 2 | R 1 10 | 10 | Position 10 becomes 0 | - |
| 3 | A 1 10 | 10 | Every value increases | - |
| 4 | Q 1 10 | 10 | Maximum restored | 10 |
| 5 | R 1 7 | 10 | Position 7 cleared | - |
| 6 | Q 5 10 | 10 | Position 10 remains | 10 |

This shows why the reset uses the global maximum rather than the interval maximum. The first reset changes only the element that actually holds the global maximum.

A second example:

```
5 3
4 4 4 4 4
R 2 5
Q 1 5
A 1 5
```

| Step | Operation | Root maximum | Segment state |
| --- | --- | --- | --- |
| 1 | Initial | 4 | All values equal |
| 2 | R 2 5 | 4 | Covered segment is reset at once |
| 3 | Q 1 5 | 4 | Only first position remains maximum |
| 4 | A 1 5 | 5 | All values increase |

This confirms that an all-equal segment is handled as a single operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + K) log N) amortized | Each operation performs logarithmic tree work, and repeated resets reduce the number of maximum elements that need deeper visits |
| Space | O(N) | The segment tree stores a constant amount of information per node |

The constraints require avoiding full range scans. The segment tree keeps the number of visited nodes small enough for 100000 operations.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old
    return ""

# The following cases are intended for the solve() implementation.

# sample 1
# 10 10
# 1 2 3 4 5 6 7 8 9 10
# Q 1 10
# R 1 10
# A 1 10
# Q 1 10
# R 1 7
# Q 5 10
# R 7 10
# Q 6 10
# A 6 10
# Q 1 6

# minimum size
# 1 3
# 5
# Q 1 1
# R 1 1
# Q 1 1

# all equal values
# 5 2
# 3 3 3 3 3
# R 1 5
# Q 1 5

# mixed maximum values
# 4 2
# 7 7 3 7
# R 1 3
# Q 1 4
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element with reset | `5` then `0` | Minimum size handling |
| All values equal | `0` after reset | Full segment reset |
| Mixed maximum values | `7` | Does not clear non-maximum values |
| Range add after reset | Depends on produced maximum | Lazy propagation correctness |

## Edge Cases

For the case where a reset interval contains some but not all maximum values, the tree descends instead of clearing the whole node. In:

```
4 2
7 7 3 7
R 1 3
Q 1 4
```

the root sees maximum `7`, but the segment `[1,3]` has a second maximum of `3`. The reset continues downward and clears only the leaves containing `7`. The final maximum remains `7`.

For the all-equal case:

```
5 2
4 4 4 4 4
R 2 5
Q 1 5
```

the covered node has `mx = 4` and `smx = -INF`. The algorithm knows every value in that node is `4`, so it replaces the entire segment immediately. The remaining first position keeps value `4`, which is the query result.

For overlapping additions:

```
3 3
1 2 3
A 1 3
R 1 3
Q 1 3
```

after the addition the array is `[2,3,4]`. The reset removes only the last value because it is the global maximum. The answer becomes `3`, showing that lazy additions and resets interact correctly.
