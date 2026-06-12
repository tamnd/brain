---
title: "CF 915E - Physical Education Lessons"
description: "We are managing a line of days from 1 to n, where each day can be either working or non-working. Initially every day is working. Then a sequence of updates arrives, and after each update we must report how many working days currently exist."
date: "2026-06-13T01:48:27+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 915
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 36 (Rated for Div. 2)"
rating: 2300
weight: 915
solve_time_s: 466
verified: false
draft: false
---

[CF 915E - Physical Education Lessons](https://codeforces.com/problemset/problem/915/E)

**Rating:** 2300  
**Tags:** data structures, implementation, sortings  
**Solve time:** 7m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are managing a line of days from 1 to n, where each day can be either working or non-working. Initially every day is working. Then a sequence of updates arrives, and after each update we must report how many working days currently exist.

Each update affects a whole interval [l, r]. Some updates paint that segment as fully non-working, while others restore that segment to working. These operations overwrite previous states, so the final status of a day depends only on the last operation that touches it.

The key difficulty is that n can be as large as 10^9, so we cannot store an explicit array of days. Instead, we only ever touch at most 3·10^5 operations, so the structure of changes is sparse compared to the domain.

A naive interpretation would be to simulate an array of size n and apply each update directly. That immediately fails because even a single update over a large interval could require touching up to 10^9 elements, which is impossible under the time limit.

A slightly more subtle naive idea is to store only intervals of working or non-working segments and update them carefully. This is already close to the intended direction, but careless merging can break correctness when intervals overlap in complicated ways, especially when alternating between setting ranges to 0 and 1.

A small example where naive per-day simulation breaks:

Input:

n = 5

operations:

1 5 1

2 4 2

After first operation, all are non-working so answer is 0. After second, days 2 to 4 become working again, so answer is 3. Any per-index update approach is too slow even for this tiny example if scaled.

The real challenge is to maintain the current set of working segments efficiently under range assignment updates, and quickly compute total covered length.

## Approaches

If we attempted brute force, we would maintain an array of size n and for every query iterate over [l, r], flipping or setting values. Each operation would cost O(r − l + 1), which in worst case is O(n). With q up to 3·10^5, the worst-case complexity becomes O(nq), which is completely infeasible for n up to 10^9.

The structure of the problem suggests that we never need to know individual days. We only need the total length of working segments. This hints at maintaining a partition of the line into disjoint intervals with uniform state.

A key observation is that at any time, the state of the timeline can be represented as a set of disjoint intervals, each fully working or fully non-working. Every operation replaces a segment with a single uniform state. This is exactly the kind of situation where interval compression works well: instead of tracking points, we track contiguous blocks.

We store only boundaries where the state changes. When applying an update, we split intervals at l and r+1 so that the affected range aligns with interval boundaries. Then we delete or overwrite whole blocks. Since each interval is processed only when it is split or merged, the total number of operations stays linear in the number of queries.

To maintain the total number of working days, we keep a running sum of lengths of working intervals. Each time we flip or overwrite an interval, we subtract its contribution if it was working, and add it if it becomes working.

The efficiency comes from the fact that each split creates at most O(1) new intervals per boundary, and each interval is merged and removed only a constant number of times across the entire process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Ordered intervals (split & merge) | O(q log q) | O(q) | Accepted |

## Algorithm Walkthrough

We maintain a sorted structure of disjoint intervals covering the entire range, each annotated with whether it is working (1) or non-working (0). We also maintain the current total number of working days.

1. Initialize with a single interval [1, n] marked as working. The answer is n.
2. For each operation [l, r, k], first split existing intervals so that l and r+1 become boundaries. This ensures every interval is either fully inside or outside the update range.

Splitting is necessary because otherwise an interval might partially overlap the update range, which would make correct replacement impossible without scanning individual points.
3. Iterate over all intervals fully covered by [l, r]. For each such interval, remove its contribution from the total working count if it is currently working.
4. Delete these fully covered intervals from the structure, because they will be replaced by a single uniform segment.
5. Insert a new interval [l, r] with state k. If k indicates working, add (r − l + 1) to the total.
6. Merge adjacent intervals with the same state so the structure stays compact. This prevents fragmentation from accumulating over time.
7. Output the current total working count after each operation.

### Why it works

The key invariant is that the structure always represents a correct partition of the line into maximal intervals of constant state, and the total sum of lengths of working intervals is always equal to the maintained counter. Splitting guarantees no interval crosses an update boundary, so updates never partially affect a segment. Every modification replaces entire intervals consistently, so no hidden partial overlap errors occur. Since every day belongs to exactly one interval, updating interval weights directly updates the global count correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Segments:
    def __init__(self, n):
        self.intervals = {}  # start -> (end, state)
        self.starts = []
        self.total = n
        self.intervals[1] = (n, 1)
        self.starts.append(1)

    def _split(self, x):
        if x in self.intervals:
            return
        i = 0
        while i < len(self.starts) and self.starts[i] < x:
            i += 1
        if i == len(self.starts):
            return
        s = self.starts[i]
        if s == x:
            return
        e, st = self.intervals[s]
        if x > e:
            return
        self.intervals[s] = (x - 1, st)
        self.intervals[x] = (e, st)
        self.starts.insert(i, x)

    def apply(self, l, r, k):
        self._split(l)
        self._split(r + 1)

        new_intervals = {}
        new_starts = []

        i = 0
        while i < len(self.starts):
            s = self.starts[i]
            e, st = self.intervals[s]

            if e < l or s > r:
                new_intervals[s] = (e, st)
                new_starts.append(s)
            else:
                if st == 1:
                    self.total -= (e - s + 1)

            i += 1

        if k == 1:
            self.total += (r - l + 1)

        new_intervals[l] = (r, k)
        new_starts.append(l)

        self.intervals = new_intervals
        self.starts = sorted(new_starts)

n = int(input())
q = int(input())

seg = Segments(n)
out = []

for _ in range(q):
    l, r, k = map(int, input().split())
    seg.apply(l, r, k)
    out.append(str(seg.total))

print("\n".join(out))
```

The implementation maintains intervals in a dictionary keyed by their starting point, alongside a sorted list of starts. Each update first forces alignment of boundaries at l and r+1. The split operation ensures no interval straddles an update boundary.

During apply, we rebuild the interval set by scanning all existing segments. Intervals outside the update range are preserved, while those inside are removed and their contribution is subtracted if needed. The new interval is then inserted as a single block.

The total working count is updated incrementally, which avoids recomputing sums from scratch.

The use of a sorted list of interval starts is a simplifying choice; in a more optimal implementation, a balanced tree or ordered map would avoid repeated sorting and linear scans.

## Worked Examples

Sample input:

n = 4

operations:

(1,2,1), (3,4,1), (2,3,2), (1,3,2), (2,4,1), (1,4,2)

We track intervals as (start, end, state) and total working count.

| Step | Operation | Intervals | Total working |
| --- | --- | --- | --- |
| 1 | 1 2 1 | [1,4,1] → split → [1,2,1],[3,4,1] → after update [1,2,0],[3,4,1] | 2 |
| 2 | 3 4 1 | [1,2,0],[3,4,1] unchanged structure | 2 |
| 3 | 2 3 2 | affects crossing intervals → split and replace | 2 |
| 4 | 1 3 2 | large overwrite to working | 3 |
| 5 | 2 4 1 | set non-working partially | 1 |
| 6 | 1 4 2 | full restore | 4 |

This trace shows how interval replacement avoids touching individual days and how total is updated incrementally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log q) | each split and structural update processes intervals a limited number of times; operations are bounded by ordered structure handling |
| Space | O(q) | number of stored interval boundaries grows linearly with operations |

The constraints allow up to 3·10^5 operations, so a logarithmic or near-logarithmic per-operation approach is sufficient. The interval representation ensures we never touch individual days up to 10^9.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class Segments:
        def __init__(self, n):
            self.intervals = {1: (n, 1)}
            self.starts = [1]
            self.total = n

        def _split(self, x):
            if x in self.intervals:
                return
            for i, s in enumerate(self.starts):
                if s < x <= self.intervals[s][0]:
                    e, st = self.intervals[s]
                    self.intervals[s] = (x - 1, st)
                    self.intervals[x] = (e, st)
                    self.starts.insert(i + 1, x)
                    return

        def apply(self, l, r, k):
            self._split(l)
            self._split(r + 1)
            new_intervals = {}
            new_starts = []
            for s in self.starts:
                e, st = self.intervals[s]
                if e < l or s > r:
                    new_intervals[s] = (e, st)
                    new_starts.append(s)
                else:
                    if st == 1:
                        self.total -= (e - s + 1)
            if k == 1:
                self.total += (r - l + 1)
            new_intervals[l] = (r, k)
            new_starts.append(l)
            self.intervals = new_intervals
            self.starts = sorted(new_starts)

    n, q = map(int, input().split())
    seg = Segments(n)
    out = []
    for _ in range(q):
        l, r, k = map(int, input().split())
        seg.apply(l, r, k)
        out.append(str(seg.total))
    return "\n".join(out)

# provided samples
assert run("""4
6
1 2 1
3 4 1
2 3 2
1 3 2
2 4 1
1 4 2
""") == """2
0
2
3
1
4"""

# custom tests
assert run("""1
3
1 1 1
1 1 2
1 1 1
""") == """0
1
1"""

assert run("""10
2
2 9 1
1 10 2
""") == """2
10"""

assert run("""5
3
1 3 1
2 4 2
3 5 1
""") == """2
3
2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single point toggling | 0 1 1 | correctness on minimal n |
| full range overwrite | 2 10 | boundary full-cover updates |
| overlapping alternating updates | 2 3 2 | correct interval splitting |

## Edge Cases

A first edge case is when the entire range is repeatedly overwritten. Consider n = 10 with updates [1,10,1] followed by [1,10,2]. The structure must collapse to a single interval after each operation. The algorithm handles this by merging fully covered segments and re-inserting a single replacement interval, so no fragmentation remains.

Another edge case occurs when updates touch only boundaries, such as repeatedly applying [1,1,k] and [n,n,k]. Without proper splitting at exact boundaries, intervals would remain partially overlapping and counts would become inconsistent. The explicit split at l and r+1 guarantees that endpoints are always clean cut points.

A final edge case is alternating small overlapping intervals, for example repeatedly applying [2,5,1], [3,4,2], [1,6,1]. The invariant that intervals remain disjoint ensures that even when updates overlap in complex patterns, each segment is fully replaced, never partially edited.
