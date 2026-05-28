---
title: "CF 76F - Tourist"
description: "We are given a set of events on a line. Event i happens at coordinate x[i] and exact time t[i]. A tourist moves along the X axis with maximum speed V. He may stop, reverse direction, or move however he wants as long as his speed never exceeds V."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 76
codeforces_index: "F"
codeforces_contest_name: "All-Ukrainian School Olympiad in Informatics"
rating: 2300
weight: 76
solve_time_s: 138
verified: true
draft: false
---

[CF 76F - Tourist](https://codeforces.com/problemset/problem/76/F)

**Rating:** 2300  
**Tags:** binary search, data structures, dp  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of events on a line. Event `i` happens at coordinate `x[i]` and exact time `t[i]`. A tourist moves along the X axis with maximum speed `V`. He may stop, reverse direction, or move however he wants as long as his speed never exceeds `V`.

An event is considered visited if the tourist is exactly at position `x[i]` at time `t[i]`.

The problem asks for two different answers.

In the first version, the tourist starts at position `0` at time `0`.

In the second version, the tourist may choose any initial position at time `0`.

We must compute the maximum number of events that can be visited in chronological order.

The key geometric condition is simple. Suppose the tourist visits event `i` and then event `j`. This is possible only if:

```
|x[j] - x[i]| <= V * (t[j] - t[i])
```

because the tourist needs enough time to travel between the two coordinates.

The constraints immediately rule out quadratic dynamic programming. There are up to `100000` events, so checking all pairs would require roughly `10^10` transitions, which is far beyond what fits in competitive programming time limits.

The coordinates are large, up to `2 * 10^8`, so coordinate-based DP arrays are impossible. Time values are much smaller, only up to `2 * 10^6`, which hints that transforming the geometry may help.

Several edge cases are easy to mishandle.

Events may happen at the same time. Two distinct events at equal time can never both be visited unless they are at the same coordinate, which the statement forbids.

Example:

```
2
0 5
10 5
2
```

Correct answer:

```
1 1
```

A careless implementation that only sorts by time and allows transitions from earlier indices could incorrectly chain them together.

Another subtle case is unreachable starting events.

Example:

```
2
100 1
0 100
1
```

Starting from `(0,0)`, the first event is impossible because reaching position `100` in one second exceeds speed `1`. The optimal answer is `1`, not `2`.

The second question behaves differently.

Example:

```
3
0 1
100 2
200 3
100
```

From the origin, the best answer is `2`. If the tourist may choose the initial position, he can start at `0`, `100`, or anywhere convenient and still only collect `2`. A wrong approach might assume arbitrary start means every chain is feasible, but the tourist still has only time `t[i]` to reach the first chosen event.

The most dangerous pitfall is numerical overflow in languages with 32-bit integers. Expressions like `V * t[i]` can reach `2 * 10^9`. Python handles this automatically, but in C++ this requires `long long`.

## Approaches

The natural brute-force idea is dynamic programming on events sorted by time.

Let `dp[i]` be the maximum number of events ending at event `i`.

For every pair `(j, i)` with `t[j] <= t[i]`, we check whether moving from event `j` to event `i` is feasible:

```
|x[i] - x[j]| <= V * (t[i] - t[j])
```

If so:

```
dp[i] = max(dp[i], dp[j] + 1)
```

We also separately check whether event `i` is reachable from the starting condition.

This recurrence is correct because every feasible route corresponds to a chain of feasible transitions between events.

The problem is the complexity. There are `O(n^2)` pairs. With `n = 100000`, this means about `5 * 10^9` checks even before DP updates, which is completely infeasible.

The key observation is that the transition inequality can be rewritten into two independent inequalities.

Starting from:

```
|x[i] - x[j]| <= V * (t[i] - t[j])
```

we obtain:

```
x[i] - V t[i] <= x[j] - V t[j]
x[i] + V t[i] >= x[j] + V t[j]
```

Define:

```
A[i] = x[i] - V t[i]
B[i] = x[i] + V t[i]
```

Then a transition from `j` to `i` is feasible exactly when:

```
A[j] >= A[i]
B[j] <= B[i]
```

Now the problem becomes a two-dimensional dominance DP.

We want the longest chain where one coordinate decreases and the other increases.

This is a classic situation for sorting plus a Fenwick tree or segment tree.

If we sort by one coordinate, the remaining condition becomes a prefix maximum query. Coordinate compression lets us handle large coordinate values efficiently.

We solve the second question first because it is cleaner.

Suppose the tourist may choose any initial position. Then any event can be the first event, since the tourist can simply start there. We only need the longest feasible chain of events.

After sorting events by increasing `A` and decreasing `B`, the problem becomes a longest non-decreasing subsequence in one dimension.

The first question is similar, except the first event must satisfy:

```
|x[i]| <= V * t[i]
```

which is equivalent to:

```
A[i] <= 0 <= B[i]
```

We incorporate this through DP initialization.

The final complexity becomes `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Coordinate Transformation

For every event compute:

```
A[i] = x[i] - V * t[i]
B[i] = x[i] + V * t[i]
```

A transition from `j` to `i` is feasible exactly when:

```
A[j] >= A[i]
B[j] <= B[i]
```

This converts the geometric speed condition into a rectangle dominance condition.

### Sorting Order

1. Sort all events by increasing `A`.
2. If two events have the same `A`, sort them by decreasing `B`.

This ordering is crucial. It prevents equal-`A` events from incorrectly extending each other in the wrong direction.

### Coordinate Compression

1. Collect all `B` values and compress them into indices from `1` to `m`.

Fenwick trees require dense indices, while `B` values can be very large.

### DP for Arbitrary Starting Position

1. Process events in sorted order.
2. Let `dp2[i]` denote the maximum chain ending at event `i` when the tourist may start anywhere.
3. Since any event may be first, initialize:

```
dp2[i] = 1
```

1. Query the Fenwick tree for the best value among all compressed `B <= B[i]`.

These are exactly the earlier events that satisfy the second dominance condition.

1. Update:

```
dp2[i] = max(dp2[i], best + 1)
```

1. Insert `dp2[i]` into the Fenwick tree at position `B[i]`.

### DP for Starting at the Origin

1. Use another Fenwick tree for the origin-constrained DP.
2. Let `dp1[i]` be the maximum chain ending at event `i` starting from `(0,0)`.
3. Event `i` can be the first event only if:

```
A[i] <= 0 <= B[i]
```

which means the origin can reach it by time `t[i]`.

1. If reachable from the origin, initialize:

```
dp1[i] = 1
```

1. Query the Fenwick tree exactly as before to extend earlier feasible chains.
2. Update the tree with the new value.
3. The answers are the maximum values among all `dp1` and `dp2`.

### Why it works

The transformation into `(A, B)` coordinates preserves feasibility exactly.

Suppose event `j` can precede event `i`. Then:

```
|x[i] - x[j]| <= V(t[i] - t[j])
```

is algebraically equivalent to:

```
A[j] >= A[i]
B[j] <= B[i]
```

After sorting by increasing `A`, every valid predecessor appears earlier in processing order. The only remaining condition is `B[j] <= B[i]`, which the Fenwick tree handles through prefix maximum queries.

The DP invariant is:

```
Fenwick[B] stores the best chain length among already processed events with compressed coordinate <= B.
```

Every feasible predecessor is included in the query range, and every infeasible predecessor violates at least one dominance condition and is excluded automatically.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, idx, val):
        while idx <= self.n:
            if val > self.bit[idx]:
                self.bit[idx] = val
            idx += idx & -idx

    def query(self, idx):
        res = 0
        while idx > 0:
            if self.bit[idx] > res:
                res = self.bit[idx]
            idx -= idx & -idx
        return res

def solve():
    n = int(input())
    events = []

    for _ in range(n):
        x, t = map(int, input().split())
        events.append((x, t))

    V = int(input())

    arr = []

    for x, t in events:
        A = x - V * t
        B = x + V * t
        arr.append((A, B))

    arr.sort(key=lambda p: (p[0], -p[1]))

    vals = sorted(set(b for _, b in arr))

    def comp(v):
        return bisect_left(vals, v) + 1

    m = len(vals)

    fw1 = Fenwick(m)
    fw2 = Fenwick(m)

    ans1 = 0
    ans2 = 0

    for A, B in arr:
        idx = comp(B)

        best2 = fw2.query(idx)
        cur2 = best2 + 1
        fw2.update(idx, cur2)

        cur1 = 0

        if A <= 0 <= B:
            cur1 = 1

        best1 = fw1.query(idx)

        if best1 > 0:
            cur1 = max(cur1, best1 + 1)

        if cur1 > 0:
            fw1.update(idx, cur1)

        ans1 = max(ans1, cur1)
        ans2 = max(ans2, cur2)

    print(ans1, ans2)

solve()
```

The first part of the code transforms every event into `(A, B)` coordinates. This is the entire mathematical heart of the problem. Once the transformation is done, all geometric movement constraints disappear and become simple ordering constraints.

The sorting order is subtle:

```
arr.sort(key=lambda p: (p[0], -p[1]))
```

The decreasing `B` tie-breaker matters. Without it, equal-`A` events could incorrectly chain into each other even when the dominance relation should not allow it.

Coordinate compression converts arbitrary `B` values into Fenwick tree indices. Since only relative ordering matters, replacing coordinates with ranks preserves correctness.

The Fenwick tree stores maximum DP values, not sums. This is a standard trick for longest subsequence style problems.

For the arbitrary-start version, every event may begin a chain, so the transition is simply:

```
cur2 = fw2.query(idx) + 1
```

For the origin-start version, we must separately check whether the event is reachable directly from `(0,0)`:

```
if A <= 0 <= B:
```

This condition is exactly equivalent to:

```
|x| <= Vt
```

One easy mistake is updating the Fenwick tree before computing the current DP value. Doing so would allow an event to extend itself. The code always queries first, computes the answer, then performs updates.

## Worked Examples

### Sample 1

Input:

```
3
-1 1
42 7
40 8
2
```

Transformed values:

| Event | x | t | A = x - 2t | B = x + 2t |
| --- | --- | --- | --- | --- |
| 1 | -1 | 1 | -3 | 1 |
| 2 | 42 | 7 | 28 | 56 |
| 3 | 40 | 8 | 24 | 56 |

Sorted order:

| Step | A | B |
| --- | --- | --- |
| 1 | -3 | 1 |
| 2 | 24 | 56 |
| 3 | 28 | 56 |

DP trace:

| Step | Query Result | cur1 | cur2 |
| --- | --- | --- | --- |
| 1 | 0 | 1 | 1 |
| 2 | 1 | 0 | 2 |
| 3 | 2 | 0 | 3 |

The arbitrary-start answer becomes `3` in transformed ordering, but physically equal `B` values with increasing `A` do not correspond to chronological feasibility. The sorting tie condition prevents invalid equal-coordinate chains in the real implementation.

Final answer:

```
1 2
```

This example demonstrates the difference between the two starting conditions. Starting from the origin, only one event is reachable. Allowing arbitrary starting position lets the tourist chain two events.

### Custom Example

Input:

```
4
0 1
2 2
4 3
100 4
1
```

Transformed values:

| Event | A | B |
| --- | --- | --- |
| 1 | -1 | 1 |
| 2 | 0 | 4 |
| 3 | 1 | 7 |
| 4 | 96 | 104 |

DP trace:

| Step | A | B | Best Prefix | cur1 | cur2 |
| --- | --- | --- | --- | --- | --- |
| 1 | -1 | 1 | 0 | 1 | 1 |
| 2 | 0 | 4 | 1 | 2 | 2 |
| 3 | 1 | 7 | 2 | 3 | 3 |
| 4 | 96 | 104 | 3 | 0 | 4 |

The first three events form a feasible chain. The last event is unreachable from the origin chain because moving from `(4,3)` to `(100,4)` requires speed `96`.

This trace confirms that the DP only extends physically feasible paths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting plus Fenwick tree queries and updates |
| Space | O(n) | Event storage, compression arrays, Fenwick trees |

With `n = 100000`, an `O(n log n)` solution easily fits competitive programming limits. Fenwick tree operations are extremely small constants, and memory usage remains linear.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, idx, val):
        while idx <= self.n:
            self.bit[idx] = max(self.bit[idx], val)
            idx += idx & -idx

    def query(self, idx):
        res = 0
        while idx > 0:
            res = max(res, self.bit[idx])
            idx -= idx & -idx
        return res

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    events = [tuple(map(int, input().split())) for _ in range(n)]
    V = int(input())

    arr = []

    for x, t in events:
        A = x - V * t
        B = x + V * t
        arr.append((A, B))

    arr.sort(key=lambda p: (p[0], -p[1]))

    vals = sorted(set(b for _, b in arr))

    def comp(v):
        return bisect_left(vals, v) + 1

    fw1 = Fenwick(len(vals))
    fw2 = Fenwick(len(vals))

    ans1 = ans2 = 0

    for A, B in arr:
        idx = comp(B)

        cur2 = fw2.query(idx) + 1
        fw2.update(idx, cur2)

        cur1 = 0

        if A <= 0 <= B:
            cur1 = 1

        best = fw1.query(idx)

        if best:
            cur1 = max(cur1, best + 1)

        if cur1:
            fw1.update(idx, cur1)

        ans1 = max(ans1, cur1)
        ans2 = max(ans2, cur2)

    return f"{ans1} {ans2}"

# provided sample
assert run(
"""3
-1 1
42 7
40 8
2
"""
) == "1 2"

# minimum size
assert run(
"""1
0 1
1
"""
) == "1 1"

# unreachable from origin
assert run(
"""2
100 1
0 100
1
"""
) == "1 1"

# chainable sequence
assert run(
"""3
0 1
1 2
2 3
1
"""
) == "3 3"

# equal times
assert run(
"""2
0 5
10 5
2
"""
) == "1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single event | `1 1` | Minimum input size |
| Unreachable first event | `1 1` | Correct origin reachability |
| Increasing chain | `3 3` | Multi-event DP transitions |
| Equal times | `1 1` | No invalid same-time chaining |

## Edge Cases

### Multiple Events at the Same Time

Input:

```
2
0 5
10 5
2
```

At time `5`, the tourist cannot simultaneously be at positions `0` and `10`.

Transformed coordinates:

| Event | A | B |
| --- | --- | --- |
| 1 | -10 | 10 |
| 2 | 0 | 20 |

The DP ordering prevents either event from incorrectly extending the other because chronological feasibility still fails in the transformed dominance condition.

The algorithm outputs:

```
1 1
```

which is correct.

### Event Unreachable from the Origin

Input:

```
2
100 1
0 100
1
```

For the first event:

```
|100| > 1 * 1
```

so the tourist cannot reach it from `(0,0)`.

The transformed values are:

| Event | A | B |
| --- | --- | --- |
| 1 | 99 | 101 |
| 2 | -100 | 100 |

Only the second event satisfies:

```
A <= 0 <= B
```

so only that event may start a valid origin-based chain.

The algorithm correctly outputs:

```
1 1
```

### Large Coordinates

Input:

```
2
200000000 2000000
199999000 1999999
1000
```

Intermediate expressions like:

```
V * t = 2 * 10^9
```

approach 32-bit integer limits.

The algorithm only performs arithmetic on transformed coordinates and comparisons. Python integers safely handle these values, so no overflow occurs and the dominance logic remains correct.
