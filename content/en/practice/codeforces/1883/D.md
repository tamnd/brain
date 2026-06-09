---
title: "CF 1883D - In Love"
description: "We are asked to maintain a dynamic multiset of segments on the number line, processing additions and deletions one by one. After each operation, we must determine whether the multiset contains at least two segments that do not overlap."
date: "2026-06-08T22:29:43+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1883
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 905 (Div. 3)"
rating: 1500
weight: 1883
solve_time_s: 135
verified: true
draft: false
---

[CF 1883D - In Love](https://codeforces.com/problemset/problem/1883/D)

**Rating:** 1500  
**Tags:** data structures, greedy  
**Solve time:** 2m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to maintain a dynamic multiset of segments on the number line, processing additions and deletions one by one. After each operation, we must determine whether the multiset contains at least two segments that do not overlap. A pair of segments does not intersect if no point on the number line belongs to both segments.

The input consists of up to $10^5$ operations, each adding or removing a segment defined by its endpoints $l$ and $r$, where $1 \le l \le r \le 10^9$. After each operation, we must output "YES" if there exists a pair of non-intersecting segments and "NO" otherwise.

Because $q$ can be as large as $10^5$, any algorithm that examines all pairs of segments after each operation would require $O(q^2)$ time in the worst case, which is $10^{10}$ operations and far too slow. This forces us to maintain only the information necessary to answer the query efficiently, rather than re-scanning all segments repeatedly.

Non-obvious edge cases include situations where multiple identical segments exist. For example, if the multiset contains two copies of segment $(2, 4)$ and one segment $(5, 6)$, the answer must still be "YES" because $(2, 4)$ and $(5, 6)$ do not intersect, even though $(2, 4)$ itself appears twice. Another edge case is when the multiset contains only identical or overlapping segments; any algorithm that does not consider the maximal left and minimal right endpoints may incorrectly conclude that non-intersecting segments exist.

## Approaches

The brute-force approach is straightforward: after every addition or removal, check all pairs of segments to see whether they intersect. This is correct but requires $O(n^2)$ per operation in the worst case. With up to $10^5$ segments, this results in up to $10^{10}$ operations, which is infeasible.

The key insight is that we do not need to examine every pair of segments. To determine whether a pair of segments does not intersect, it suffices to know the segment with the smallest left endpoint and the segment with the largest right endpoint. If the segment with the maximum left endpoint is greater than the segment with the minimum right endpoint, then these two segments do not intersect.

To implement this efficiently, we maintain the current minimal left endpoint, maximal left endpoint, minimal right endpoint, and maximal right endpoint across all segments, along with their counts to handle duplicate segments. With this approach, each addition or deletion updates these four values in $O(\log n)$ time using a balanced data structure or a `SortedDict`/`SortedList` from Python's `sortedcontainers`. Then, we can check for non-intersecting segments in constant time by comparing `max_left` and `min_right`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * n) | O(n) | Too slow |
| Maintain extremes | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize four data structures: one multiset or counter for left endpoints, one for right endpoints. Track `min_left`, `max_left`, `min_right`, `max_right` dynamically with counts for duplicates.
2. For each operation:

- If it is an addition, insert the segment's left and right endpoints into the respective multisets.
- If it is a removal, remove one occurrence of the segment's endpoints from the multisets.
3. After each operation, calculate the current `min_left`, `max_left`, `min_right`, and `max_right`.
4. If `max_left` > `min_right`, output "YES" since there exists at least one pair of segments that do not intersect. Otherwise, output "NO".
5. Repeat for all operations.

Why it works: By keeping track of the extreme endpoints, we guarantee that we consider the segments most likely to be non-overlapping. The invariant is that `min_right` is the rightmost point any segment starts to the left, and `max_left` is the leftmost point any segment extends to the right. If `max_left` exceeds `min_right`, there is a gap between segments, guaranteeing non-intersection.

## Python Solution

```python
import sys
from collections import Counter
import bisect

input = sys.stdin.readline

class Multiset:
    def __init__(self):
        self.counter = Counter()
        self.sorted = []

    def add(self, x):
        if self.counter[x] == 0:
            bisect.insort(self.sorted, x)
        self.counter[x] += 1

    def remove(self, x):
        self.counter[x] -= 1
        if self.counter[x] == 0:
            idx = bisect.bisect_left(self.sorted, x)
            self.sorted.pop(idx)

    def min(self):
        return self.sorted[0]

    def max(self):
        return self.sorted[-1]

q = int(input())
lefts = Multiset()
rights = Multiset()
segments = Counter()

for _ in range(q):
    op, l, r = input().split()
    l = int(l)
    r = int(r)
    if op == '+':
        segments[(l,r)] += 1
        lefts.add(l)
        rights.add(r)
    else:
        segments[(l,r)] -= 1
        lefts.remove(l)
        rights.remove(r)
    if len(segments) < 2:
        print("NO")
        continue
    if lefts.max() > rights.min():
        print("YES")
    else:
        print("NO")
```

The `Multiset` class uses a `Counter` for duplicates and a sorted list for fast retrieval of minimum and maximum. Each addition and removal keeps the data consistent. This avoids scanning all segments, and `max_left` and `min_right` comparisons answer the query in constant time.

## Worked Examples

For the sample input:

```
+ 1 2
+ 3 4
+ 2 3
```

| Operation | Segments | min_right | max_left | Output |
| --- | --- | --- | --- | --- |
| + 1 2 | {(1,2)} | 2 | 1 | NO |
| + 3 4 | {(1,2),(3,4)} | 2 | 3 | YES |
| + 2 3 | {(1,2),(3,4),(2,3)} | 2 | 3 | YES |

This trace confirms the invariant: `max_left` > `min_right` indicates a gap.

For another example:

```
+ 2 2
+ 3 4
- 2 2
```

| Operation | Segments | min_right | max_left | Output |
| --- | --- | --- | --- | --- |
| + 2 2 | {(2,2)} | 2 | 2 | NO |
| + 3 4 | {(2,2),(3,4)} | 2 | 3 | YES |
| - 2 2 | {(3,4)} | 4 | 3 | NO |

It demonstrates correct handling of segment removal and updates to extremes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each insertion/removal in `Multiset` is O(log n) due to `bisect`. Maximum q = 10^5 makes 10^5 * log 10^5 ≈ 2*10^6 operations. |
| Space | O(n) | Each segment stored in Counter and two multisets, at most q segments exist. |

This fits comfortably in the 2-second, 256MB limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open('solution.py').read())
    return out.getvalue().strip()

# provided sample
assert run("""12
+ 1 2
+ 3 4
+ 2 3
+ 2 2
+ 3 4
- 3 4
- 3 4
- 1 2
+ 3 4
- 2 2
- 2 3
- 3 4
""") == """NO
YES
YES
YES
YES
YES
NO
NO
YES
NO
NO
NO"""

# minimal input
assert run("""1
+ 1 1
""") == "NO", "single segment cannot have non-intersecting pair"

# identical segments
assert run("""3
+ 1 2
+ 1 2
+ 1 2
""") == "NO", "all identical, no non-intersecting pair"

# non-intersecting multiple
assert run("""4
+ 1 2
+ 3 4
+ 5 6
- 1 2
""") == """NO
YES
YES
YES""", "after removal, non-intersecting still exists"

# edge large numbers
assert run("""2
+ 1 1000000000
+ 500000000 1000000000
""") == """NO
NO""", "overlapping
```
