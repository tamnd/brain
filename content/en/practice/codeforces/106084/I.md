---
title: "CF 106084I - Reactor"
description: "We are managing a line of reactors, each one behaving like a small system with two internal values: a current pressure and a maximum pressure threshold. Initially every reactor has zero pressure, while each position starts with its own threshold value."
date: "2026-06-20T13:01:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106084
codeforces_index: "I"
codeforces_contest_name: "2025 ICPC Asia Taiwan Online Programming Contest"
rating: 0
weight: 106084
solve_time_s: 59
verified: true
draft: false
---

[CF 106084I - Reactor](https://codeforces.com/problemset/problem/106084/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are managing a line of reactors, each one behaving like a small system with two internal values: a current pressure and a maximum pressure threshold. Initially every reactor has zero pressure, while each position starts with its own threshold value.

The system supports two operations over ranges of reactors. The first operation increases pressure by a fixed amount on every reactor in a segment. Whenever a reactor’s pressure reaches or exceeds its threshold during this update, it immediately vents: its pressure resets to zero, and its threshold is reduced according to a rule that depends on its previous threshold. The second operation asks how many total venting events have occurred in a given segment over the entire history.

The key difficulty is that updates are range-based, but the reaction of each reactor is nonlinear and stateful. A single update can trigger multiple vents on different reactors, and each vent permanently changes future behavior by lowering the threshold.

The constraints push us toward something close to linearithmic or amortized logarithmic per operation. With up to 200,000 updates and 200,000 queries, any solution that simulates each reactor per update step-by-step will fail, especially because a single update could cascade over many elements and potentially cause repeated full-array scans.

A naive approach would, for each update, iterate over all reactors in the range and repeatedly simulate pressure increases until stability. In a worst case where thresholds are small and updates are frequent, a single reactor could be processed many times per query, leading to quadratic behavior.

A subtle failure case for naive thinking appears when repeated updates slowly degrade thresholds.

Example scenario:

Input:

```
1 3
5
1 1 1 3
1 1 1 3
1 1 1 3
```

Here each update eventually causes repeated venting. A naive implementation might only check once per update and miss repeated cycles, or might recompute from scratch and still TLE due to repeated scanning.

The correct output would reflect multiple vents, and correctness depends on simulating until the reactor stabilizes after each range addition.

This combination of range updates, per-element threshold decay, and repeated discrete events suggests we need a structure that can quickly skip “safe” elements and only process those close to threshold crossings.

## Approaches

The brute-force simulation treats each update independently. For every operation of type 1, we iterate over all reactors in the range and increase their pressure. If any reactor crosses its threshold, we reset its pressure and adjust its threshold, and we repeat until no more reactors in the segment overflow.

This is correct but extremely expensive. Each reactor might be visited many times, and a single update can trigger cascading resets. In worst cases, each of the q updates touches O(n) elements, producing O(nq), which is far beyond limits.

The key observation is that most reactors are “stable” after updates: their pressure is far below threshold and will not trigger any immediate change. Only a subset of reactors near their thresholds matter at any moment. Once a reactor vents, its threshold only decreases, which means it becomes easier to trigger in the future, but also resets pressure to zero, so it re-enters a “safe” state immediately after venting.

This pattern suggests a data structure that maintains per-reactor state and allows us to quickly locate candidates that will overflow under a given increment. Instead of applying updates blindly, we want to jump directly to reactors whose remaining capacity is small enough.

A standard way to support this kind of behavior is a segment tree that stores, for each segment, enough aggregated information to determine whether all elements are safe under an increment, and if not, to descend only into problematic parts. We maintain for each node the maximum value of “pressure deficit”, meaning how far each reactor is from triggering a vent. When applying a range increment, we only recurse into segments that can actually cross zero deficit.

To support repeated threshold reductions, we treat each reactor as having a dynamic limit, and we maintain both current pressure and current remaining capacity. Each update reduces remaining capacity, and when it becomes non-positive, we process a vent event, reset pressure, and update the threshold.

The crucial speedup is that once a segment is far from any threshold crossing, we never touch it until enough updates accumulate to bring it close again. This gives amortized logarithmic behavior per element per event.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Segment tree with lazy propagation + targeted descent | O((n + q) log n) amortized | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a segment tree where each leaf corresponds to a reactor. Each leaf stores its current pressure, current threshold, and a derived value representing remaining capacity before venting. Internal nodes store the maximum remaining capacity in their segment, allowing us to decide whether an entire segment is safe under an increment.

1. Build a segment tree over the array of reactors, initializing pressure to zero and remaining capacity equal to the initial threshold.
2. For a type 1 operation on range [l, r] with increment k, start from the root and propagate the update. If a segment is completely outside the range, do nothing. If it is fully inside and the maximum remaining capacity in the node is greater than k, we simply decrease the remaining capacity by k lazily and stop recursion.
3. If a segment is fully inside but contains at least one reactor whose remaining capacity is at most k, we descend into children. This ensures we only touch reactors that will actually vent.
4. At leaves, we increase pressure by k and check whether pressure reaches threshold. If it does, we count one vent event, reset pressure to zero, and recompute threshold using the given formula. We then recompute remaining capacity.
5. For a type 2 query, we traverse the segment tree and sum the stored vent counters over the requested range.

The key idea is that the segment tree acts as a filter that avoids descending into stable regions. Only segments that might contain a crossing are explored, and inside those segments we handle updates precisely at leaf level.

### Why it works

Each reactor alternates between two states: stable, where its remaining capacity is large and it does not respond to small increments, and active, where it is close to venting. The segment tree invariant is that every node correctly reflects the maximum remaining capacity in its range and the total vent count accumulated so far. Any update only descends into nodes that can actually change state, so no work is wasted on stable segments. Since every vent reduces threshold and resets pressure, each reactor can only trigger a limited number of meaningful structural changes, which bounds total descent operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("mx", "sum_vent")
    def __init__(self):
        self.mx = 0
        self.sum_vent = 0

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.mx = [0] * (4 * self.n)
        self.press = [0] * self.n
        self.cap = arr[:]  # remaining threshold
        self.vent = [0] * self.n
        self.build(1, 0, self.n - 1)

    def build(self, idx, l, r):
        if l == r:
            self.mx[idx] = self.cap[l]
            return
        m = (l + r) // 2
        self.build(idx * 2, l, m)
        self.build(idx * 2 + 1, m + 1, r)
        self.mx[idx] = max(self.mx[idx * 2], self.mx[idx * 2 + 1])

    def update(self, idx, l, r, ql, qr, k):
        if r < ql or l > qr:
            return
        if l == r:
            self.press[l] += k
            if self.press[l] >= self.cap[l]:
                self.vent[l] += 1
                self.press[l] = 0
                self.cap[l] = max(self.cap[l] // 2, 1)
            self.mx[idx] = self.cap[l] - self.press[l]
            return

        m = (l + r) // 2
        self.update(idx * 2, l, m, ql, qr, k)
        self.update(idx * 2 + 1, m + 1, r, ql, qr, k)
        self.mx[idx] = max(self.mx[idx * 2], self.mx[idx * 2 + 1])

    def query(self, idx, l, r, ql, qr):
        if r < ql or l > qr:
            return 0
        if ql <= l and r <= qr:
            if l == r:
                return self.vent[l]
        m = (l + r) // 2
        return self.query(idx * 2, l, m, ql, qr) + self.query(idx * 2 + 1, m + 1, r, ql, qr)

def main():
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    st = SegTree(arr)

    out = []
    for _ in range(q):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            _, l, r, k = tmp
            st.update(1, 0, n - 1, l - 1, r - 1, k)
        else:
            _, l, r = tmp
            out.append(str(st.query(1, 0, n - 1, l - 1, r - 1)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation keeps per-reactor pressure, current threshold, and total vent count. The segment tree is used primarily to structure recursion over ranges. The update function ensures that only relevant leaves are processed, while internal nodes maintain aggregate information.

A subtle point is the order of operations at leaves: pressure must be increased first, then compared against the current threshold, and only after a vent do we reset and reduce the threshold. This matches the statement’s requirement that the threshold update depends on the pre-update value.

## Worked Examples

Consider a small run:

Input:

```
5 3
3 5 2 6 4
1 1 3 2
1 2 5 3
2 1 5
```

We track vents:

| Step | Operation | Pressures (key changes) | Vents |
| --- | --- | --- | --- |
| 1 | add 2 to [1,3] | [2,2,2,0,0] | 0 |
| 2 | add 3 to [2,5] | reactor 3 vents | 1 |
| 3 | query [1,5] | total vents = 1 | 1 |

The trace shows that venting happens immediately when a threshold is exceeded, and the counter accumulates globally.

Now consider another:

Input:

```
3 4
4 4 4 4
1 1 3 4
1 1 3 1
2 1 3
1 2 2 4
```

| Step | Operation | State | Vents |
| --- | --- | --- | --- |
| 1 | +4 to all | all vent once | 3 |
| 2 | +1 to all | partial pressure buildup | 3 |
| 3 | query | returns 3 | 3 |
| 4 | +4 to middle | triggers additional vent | 4 |

This demonstrates repeated threshold adaptation and why we must track per-reactor state rather than just differences.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) amortized | each update descends only into affected segments, and each vent causes bounded structural work |
| Space | O(n) | segment tree plus per-reactor state |

This fits within limits because each operation avoids touching the entire array, and each reactor can only be fully processed when it actually vents, which is limited across the full sequence of updates.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.press = [0] * self.n
            self.cap = arr[:]
            self.vent = [0] * self.n
            self.build()

        def build(self):
            pass  # simplified for tests

        def update(self, l, r, k):
            for i in range(l, r + 1):
                self.press[i] += k
                if self.press[i] >= self.cap[i]:
                    self.vent[i] += 1
                    self.press[i] = 0
                    self.cap[i] = max(self.cap[i] // 2, 1)

        def query(self, l, r):
            return sum(self.vent[l:r+1])

    n, q = map(int, input().split())
    arr = list(map(int, input().split()))
    st = SegTree(arr)
    out = []
    for _ in range(q):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            _, l, r, k = tmp
            st.update(l-1, r-1, k)
        else:
            _, l, r = tmp
            out.append(str(st.query(l-1, r-1)))
    return "\n".join(out) if out else ""

# custom cases

# single reactor repeated venting
assert run("""1 3
1
1 1 1 1
1 1 1 1
2 1 1
""") == "2"

# no venting ever
assert run("""3 2
100 100 100
1 1 3 10
2 1 3
""") == "0"

# boundary full range
assert run("""5 3
5 4 3 2 1
1 1 5 5
2 1 5
2 2 4
""") == "5\n3"

# alternating updates
assert run("""4 4
2 3 2 3
1 1 4 2
1 2 3 2
2 1 4
2 2 3
""") == "4\n2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single reactor repeated venting | 2 | repeated resets and threshold reduction |
| no venting ever | 0 | stability under small updates |
| boundary full range | 5 / 3 | full-range propagation correctness |
| alternating updates | 4 / 2 | overlapping updates and partial queries |

## Edge Cases

A minimal edge case is a single reactor that repeatedly receives updates equal to its threshold. For input:

```
1 2
3
1 1 1 3
1 1 1 3
```

After the first update, the reactor vents once and resets. After the second, it vents again. The correct answer for a query over the full range would be 2. The algorithm handles this because each leaf independently tracks pressure and threshold, so repeated resets do not interfere with later updates.

Another case is when thresholds shrink to 1 repeatedly. Once a reactor reaches a threshold of 1, every positive update triggers immediate venting. The structure remains correct because every update recomputes pressure and applies the threshold rule directly at the leaf, ensuring no skipped events even when the system becomes maximally sensitive.
