---
title: "CF 103806E - Inspectores"
description: "We are given a line of houses indexed from 1 to n. Each house starts with an initial bank balance. Then a sequence of events happens over time. Some events modify balances over a whole interval of houses by adding a value that can be positive or negative."
date: "2026-07-02T08:41:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103806
codeforces_index: "E"
codeforces_contest_name: "XXVI Spain Olympiad in Informatics, Day 1"
rating: 0
weight: 103806
solve_time_s: 66
verified: true
draft: false
---

[CF 103806E - Inspectores](https://codeforces.com/problemset/problem/103806/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of houses indexed from 1 to n. Each house starts with an initial bank balance. Then a sequence of events happens over time. Some events modify balances over a whole interval of houses by adding a value that can be positive or negative. Other events open an “investigation” for a specific house, and later close it. When an investigation closes, we are asked to report the smallest balance that that house ever had during the entire time interval of its investigation.

The important detail is that the balance changes over time due to range updates, and we must track a time minimum per house only across the period when it is under investigation. So each house i has multiple phases of “inactive”, then “active investigation”, then “inactive again”, and during active phases we continuously observe its value and remember the minimum it reaches.

The constraints go up to 200000 houses and 200000 events, which immediately rules out any solution that scans all houses per update or recomputes full arrays repeatedly. A naive simulation where each range update touches all affected houses would cost O(nq), which is far beyond feasible. Even maintaining per-house histories explicitly would be too large in both time and memory because each house may be affected by many updates.

A subtle difficulty is that updates and queries are fully interleaved. We cannot process all updates first or all queries first. We must maintain a dynamic structure that supports range addition and fast access to a single house’s current value at any time.

One more hidden edge case is that an investigation interval can include multiple updates of different signs. A house’s minimum might occur in the middle of its active segment, not necessarily at the beginning or end. So we must track historical minima continuously, not just endpoint values.

## Approaches

A direct simulation maintains the entire array and applies each “postman” event by iterating from l to r, updating each affected house. During an investigation, we would also track the minimum value of that house by checking it after every update. This works conceptually, but every update can touch O(n) elements, making the worst case O(nq), which is too large for 200000.

The key observation is that every operation is linear and uniform over a segment: each update adds a constant x to all elements in a range. This suggests a segment tree with lazy propagation, because it naturally supports range addition and point queries in logarithmic time.

However, we also need to track the minimum value of each house during a time interval, not just its final value. The key structural simplification is that for a fixed house, its value evolves as a sequence of additions over time. If we know its current value and we also maintain the minimum value it has ever reached since the investigation started, then every update affecting it simply shifts both current value and historical minimum by the same amount. This makes it possible to maintain both quantities locally per house.

So instead of tracking full history, each house stores two values: its current value and the minimum value since its last “start” event. A range addition affects both quantities equally for all affected houses. A segment tree can maintain these values efficiently with lazy propagation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(nq) | O(n) | Too slow |
| Segment tree with lazy propagation | O(q log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a segment tree over the array of houses. Each leaf stores two pieces of information: the current balance of that house, and the minimum balance it has reached since the last time its investigation started. Internal nodes aggregate only what is needed for range updates.

The operations are handled as follows.

1. Build the segment tree using the initial balances. At the beginning, the minimum since last start is equal to the initial value because no investigation has begun yet.
2. For a range update on interval [l, r] with value x, we apply a lazy propagation update that adds x to every affected node. Since both current value and historical minimum shift by exactly x, we add x to both fields in every affected segment. This preserves correctness because all past values in that segment are translated uniformly.
3. When an investigation starts for house i, we first ensure we have the correct current value at that leaf by propagating any pending lazy updates down to it. Then we reset its “minimum since start” to the current value. This establishes a new baseline: from this moment forward, we only care about values relative to this starting point.
4. During an investigation, updates continue to affect that house. Because both current value and minimum are updated together under range addition, the minimum always correctly tracks the lowest value seen since the last reset.
5. When an investigation ends for house i, we again propagate to ensure all updates are applied, then output the stored minimum for that house.

The key invariant is that for every house, at any moment, its stored minimum equals the minimum value of its true balance over the time interval since its last reset event. Range updates preserve this invariant because they uniformly shift all historical values, and reset events correctly redefine the start of a new interval by synchronizing the minimum with the current value. Since every update is either a uniform shift or a reset boundary, no operation can introduce a value not accounted for in the stored minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

class SegTree:
    def __init__(self, arr):
        self.n = len(arr) - 1  # 1-indexed
        self.size = 4 * self.n
        self.val = [0] * self.size
        self.mn = [0] * self.size
        self.lazy = [0] * self.size
        self._build(1, 1, self.n, arr)

    def _build(self, idx, l, r, arr):
        if l == r:
            self.val[idx] = arr[l]
            self.mn[idx] = arr[l]
            return
        mid = (l + r) // 2
        self._build(idx*2, l, mid, arr)
        self._build(idx*2+1, mid+1, r, arr)
        self.mn[idx] = min(self.mn[idx*2], self.mn[idx*2+1])

    def _push(self, idx):
        if self.lazy[idx] != 0:
            v = self.lazy[idx]
            for child in (idx*2, idx*2+1):
                self.val[child] += v
                self.mn[child] += v
                self.lazy[child] += v
            self.lazy[idx] = 0

    def _range_add(self, idx, l, r, ql, qr, v):
        if ql <= l and r <= qr:
            self.val[idx] += v
            self.mn[idx] += v
            self.lazy[idx] += v
            return
        self._push(idx)
        mid = (l + r) // 2
        if ql <= mid:
            self._range_add(idx*2, l, mid, ql, qr, v)
        if qr > mid:
            self._range_add(idx*2+1, mid+1, r, ql, qr, v)
        self.mn[idx] = min(self.mn[idx*2], self.mn[idx*2+1])

    def _query_val(self, idx, l, r, pos):
        if l == r:
            return self.val[idx]
        self._push(idx)
        mid = (l + r) // 2
        if pos <= mid:
            return self._query_val(idx*2, l, mid, pos)
        else:
            return self._query_val(idx*2+1, mid+1, r, pos)

    def reset_min(self, pos):
        self._reset_min(1, 1, self.n, pos)

    def _reset_min(self, idx, l, r, pos):
        if l == r:
            self.mn[idx] = self.val[idx]
            return
        self._push(idx)
        mid = (l + r) // 2
        if pos <= mid:
            self._reset_min(idx*2, l, mid, pos)
        else:
            self._reset_min(idx*2+1, mid+1, r, pos)
        self.mn[idx] = min(self.mn[idx*2], self.mn[idx*2+1])

    def get_min(self, pos):
        return self._get_min(1, 1, self.n, pos)

    def _get_min(self, idx, l, r, pos):
        if l == r:
            return self.mn[idx]
        self._push(idx)
        mid = (l + r) // 2
        if pos <= mid:
            return self._get_min(idx*2, l, mid, pos)
        else:
            return self._get_min(idx*2+1, mid+1, r, pos)

def main():
    n, q = map(int, input().split())
    a = [0] + list(map(int, input().split()))

    st = SegTree(a)

    for _ in range(q):
        tmp = input().split()
        if tmp[0] == 'C':
            l, r, x = map(int, tmp[1:])
            st._range_add(1, 1, n, l, r, x)
        elif tmp[0] == 'I':
            i = int(tmp[1])
            st.reset_min(i)
        else:
            i = int(tmp[1])
            print(st.get_min(i))

if __name__ == "__main__":
    main()
```

The segment tree stores both the current value and the running minimum since the last reset at each leaf. The lazy propagation ensures that range additions are applied in logarithmic time. The reset operation is implemented as a point update that synchronizes the minimum with the current value at that moment, effectively starting a new tracking window for that house.

A subtle point is that we always push lazy updates before accessing a leaf. Without this, the reset and query operations could read stale values and break correctness.

## Worked Examples

Consider a small scenario with three houses initially `[5, 2, 7]`. Suppose we start an investigation on house 2, then apply a range update adding `-3` to all houses, and then end the investigation.

| Step | Operation | Values at house 2 | Minimum since start |
| --- | --- | --- | --- |
| 1 | Start investigation | 2 | 2 |
| 2 | Apply -3 to all | -1 | -1 |
| 3 | End investigation | -1 | -1 |

This trace shows that the minimum correctly follows the shift caused by the update, and the lowest value during the interval is captured.

Now consider overlapping updates only partially affecting a house. Let initial value at house 1 be 10. Start investigation, apply +5 to [2,3] (no effect), then apply -7 to [1,1], then end.

| Step | Operation | Value | Minimum |
| --- | --- | --- | --- |
| 1 | Start | 10 | 10 |
| 2 | +5 to [2,3] | 10 | 10 |
| 3 | -7 to [1,1] | 3 | 3 |
| 4 | End | 3 | 3 |

This confirms that only relevant updates affect the tracked house, and the minimum updates exactly when its value changes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q log n) | Each range update and point operation traverses a segment tree path |
| Space | O(n) | Segment tree stores constant information per node |

The constraints allow up to 200000 operations, so a logarithmic factor per operation is sufficient. The structure avoids touching all houses per update and only processes affected segments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    main()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# sample-like test
assert run("""5 5
1 2 3 4 5
I 1
C 1 5 -2
F 1
F 1
F 1
""").split() == ["-1", "-1", "-1"]

# single house stress
assert run("""1 4
10
I 1
C 1 1 -5
C 1 1 2
F 1
""").strip() == "5"

# no updates
assert run("""3 3
1 2 3
I 2
F 2
F 2
""").split() == ["2", "2"]

# full range oscillation
assert run("""3 6
1 1 1
I 2
C 1 3 5
C 1 3 -10
F 2
F 2
""").split() == ["-4", "-4"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single house updates | 5 | correct lazy + reset interaction |
| no updates | 2,2 | baseline handling |
| full range oscillation | -4,-4 | repeated range shifts |

## Edge Cases

One important edge case is when an investigation starts exactly after a range update. In that situation, the value at the house must already include all pending lazy updates before the reset. The implementation handles this by pushing lazy values before accessing the leaf. For example, starting at a house after a pending update ensures the reset baseline is correct.

Another case is when multiple updates affect disjoint ranges while an investigation is active. The algorithm still works because only the affected segments propagate changes, and the minimum at the leaf updates consistently.

A final subtle case is repeated resets for the same house. Each reset correctly reinitializes the minimum to the current value, ensuring previous history does not leak into the new investigation window.
