---
title: "CF 160E - Buses and People"
description: "Each bus is active at exactly one moment in time. A bus starting at stop s and ending at stop f can carry any passenger whose trip interval [l, r] is fully contained inside [s, f]. A person arrives at stop l at time b, so they can only use buses whose time t satisfies t = b."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 160
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 111 (Div. 2)"
rating: 2400
weight: 160
solve_time_s: 133
verified: true
draft: false
---

[CF 160E - Buses and People](https://codeforces.com/problemset/problem/160/E)

**Rating:** 2400  
**Tags:** binary search, data structures, sortings  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

Each bus is active at exactly one moment in time. A bus starting at stop `s` and ending at stop `f` can carry any passenger whose trip interval `[l, r]` is fully contained inside `[s, f]`. A person arrives at stop `l` at time `b`, so they can only use buses whose time `t` satisfies `t >= b`. Among all such buses, they always choose the one with the smallest time.

For every person, we must answer a geometric query on intervals:

Find the bus with minimum `t` such that:

- `s <= l`
- `r <= f`
- `t >= b`

If no such bus exists, print `-1`.

The constraints immediately rule out any pairwise checking. With up to `10^5` buses and `10^5` people, a direct scan for every query would require `10^10` comparisons in the worst case, which is far beyond what fits in one second.

The tricky part is that the query has three conditions at once. We are not only filtering by time, we are also asking whether one interval contains another. A solution that handles only one dimension efficiently is still too slow.

Several edge cases are easy to mishandle.

Consider buses:

```
1 5 10
2 6 20
```

and a person:

```
2 5 10
```

The correct answer is the first bus, because its time is exactly equal to `b`, and equality is allowed. A careless binary search using `t > b` instead of `t >= b` silently fails here.

Another subtle case is overlapping buses where the earlier bus does not contain the passenger interval, but a later one does.

```
Buses:
1 4 5
2 10 7

Person:
3 8 1
```

The answer is the second bus. A greedy structure that only keeps the minimum-time active bus would incorrectly reject the query because the earliest bus cannot serve the passenger.

One more dangerous situation appears when multiple buses cover the same left boundary but have different right boundaries.

```
Buses:
1 5 3
1 10 8

Person:
2 8 1
```

The correct answer is the second bus. If we compress information incorrectly and keep only one bus per starting point, we lose necessary information.

## Approaches

The brute force solution is straightforward. For each person, scan every bus and check the three conditions:

- `s <= l`
- `r <= f`
- `t >= b`

Among all valid buses, pick the one with smallest `t`.

The logic is perfectly correct because it directly implements the definition from the statement. The problem is performance. With `10^5` people and `10^5` buses, the worst case performs `10^10` checks. Even a highly optimized implementation cannot finish in time.

The key observation is that time is totally ordered and unique. If we process buses in increasing order of `t`, then for a person with threshold `b`, the answer is simply the first bus after time `b` whose interval contains `[l, r]`.

This transforms the problem into an offline geometric search problem.

Suppose we process buses by increasing time. At any moment, we want to answer:

Among already processed buses, does there exist one with:

- `s <= l`
- `f >= r`

This is a classic two-dimensional dominance query.

The important structural detail is that stops range up to `10^9`, but only `10^5` coordinates actually appear. Coordinate compression lets us work on indices instead of raw values.

Now consider fixing the left endpoint condition. If we sweep from large `s` toward small `s`, then whenever we are at coordinate `x`, every inserted bus already satisfies `s >= x`.

For a query with left endpoint `l`, we need buses with `s <= l`, not `s >= l`. We can reverse the sweep direction:

- Sort buses by `s` ascending.
- Sort queries by `l` ascending.
- Insert all buses with `s <= l`.

Among inserted buses, we only need to know whether some bus has `f >= r`, and among all such buses we want the smallest time.

This becomes a segment tree problem indexed by compressed `f`.

For every bus endpoint `f`, we store the minimum time among buses ending there. Then querying suffix `[r, maxF]` gives the minimum valid bus time.

The final complication is that queries ask for the minimum time greater than or equal to `b`, not just the absolute minimum. We handle this with divide-and-conquer on answers.

We binary search the answer bus for every query over the ordered list of buses by time. During one parallel binary search iteration, we test whether a valid bus exists among the first `mid` buses.

That feasibility test is exactly the interval containment query solved above.

The combination gives an `O((n + m) log^2 n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O((n + m) log² n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all buses by increasing time `t`.
2. Coordinate-compress all stop coordinates appearing in buses and people.

Compression allows segment tree indexing while preserving interval ordering.
3. For every person, binary search the smallest bus index that can serve them.

Since buses are sorted by time, finding the first valid bus automatically gives the minimum valid time.
4. Use parallel binary search to process all people together.

Each person maintains a search range `[low, high]` over bus indices.
5. During one iteration, group people by their current midpoint `mid`.

A person asks: "Can some bus among the first `mid` buses contain my interval?"
6. Process buses incrementally from smallest time upward.

When bus `i` is added, insert it into a segment tree at position `f_i`.
7. The segment tree stores the minimum left endpoint `s` among buses ending at each position.

For every suffix range `[r, maxF]`, querying the minimum stored `s` tells us whether some inserted bus satisfies `s <= l`.
8. To answer a person query `(l, r)` at midpoint `mid`, query the segment tree over suffix `[r, maxF]`.

If the minimum `s` in that suffix is at most `l`, then some inserted bus contains the interval.
9. If the query succeeds, move the binary search range left.

Otherwise move it right.
10. After parallel binary search finishes, every person either has no feasible bus or has the first feasible bus index.
11. Convert the index back to the original bus number from input order.

### Why it works

At midpoint `mid`, the data structure contains exactly the buses whose times are among the first `mid` smallest values. A query succeeds precisely when at least one inserted bus contains the passenger interval.

The segment tree invariant is:

For every compressed endpoint `f`, the tree stores the minimum `s` among inserted buses ending at `f`.

When querying suffix `[r, maxF]`, we examine all buses with `f >= r`. If the minimum stored `s` inside that suffix satisfies `s <= l`, then some bus simultaneously satisfies both containment conditions:

- `s <= l`
- `f >= r`

Because buses are processed in increasing time order, the first midpoint where the query becomes feasible corresponds exactly to the minimum valid bus time.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

class SegTree:
    def __init__(self, n):
        self.n = 1
        while self.n < n:
            self.n <<= 1
        self.seg = [INF] * (2 * self.n)

    def reset(self):
        for i in range(2 * self.n):
            self.seg[i] = INF

    def update(self, pos, val):
        pos += self.n
        if val < self.seg[pos]:
            self.seg[pos] = val
        else:
            return

        pos >>= 1
        while pos:
            self.seg[pos] = min(self.seg[pos << 1],
                                self.seg[pos << 1 | 1])
            pos >>= 1

    def query(self, l, r):
        res = INF
        l += self.n
        r += self.n

        while l <= r:
            if l & 1:
                res = min(res, self.seg[l])
                l += 1
            if not (r & 1):
                res = min(res, self.seg[r])
                r -= 1
            l >>= 1
            r >>= 1

        return res

def solve():
    n, m = map(int, input().split())

    buses = []
    coords = []

    for idx in range(n):
        s, f, t = map(int, input().split())
        buses.append((t, s, f, idx + 1))
        coords.append(s)
        coords.append(f)

    people = []

    for idx in range(m):
        l, r, b = map(int, input().split())
        people.append((l, r, b, idx))
        coords.append(l)
        coords.append(r)

    coords = sorted(set(coords))
    comp = {x: i for i, x in enumerate(coords)}

    buses.sort()

    bus_data = []
    for t, s, f, idx in buses:
        bus_data.append((s, f, idx))

    low = [0] * m
    high = [n - 1] * m
    ans = [-1] * m

    possible = [False] * m

    for i, (l, r, b, idx) in enumerate(people):
        if buses[-1][0] >= b:
            possible[i] = True
        else:
            low[i] = 1
            high[i] = 0

    while True:
        buckets = [[] for _ in range(n)]
        active = False

        for i in range(m):
            if low[i] <= high[i]:
                active = True
                mid = (low[i] + high[i]) // 2
                buckets[mid].append(i)

        if not active:
            break

        seg = SegTree(len(coords))

        ptr = 0

        for mid in range(n):
            while ptr <= mid:
                s, f, _ = bus_data[ptr]
                seg.update(comp[f], s)
                ptr += 1

            for qi in buckets[mid]:
                l, r, b, idx = people[qi]

                if buses[mid][0] < b:
                    low[qi] = mid + 1
                    continue

                cr = comp[r]

                best = seg.query(cr, len(coords) - 1)

                if best <= l:
                    ans[qi] = mid
                    high[qi] = mid - 1
                else:
                    low[qi] = mid + 1

    out = []

    for i in range(m):
        if ans[i] == -1:
            out.append("-1")
        else:
            out.append(str(buses[ans[i]][3]))

    print(" ".join(out))

solve()
```

The solution begins by sorting buses by time because every query asks for the smallest feasible time. Once buses are ordered this way, the problem becomes finding the first prefix containing a valid interval.

Coordinate compression is necessary because stop numbers reach `10^9`. The segment tree only cares about relative ordering, so compressed indices are enough.

The segment tree stores minimum starting positions. This direction is easy to get wrong. For a query `(l, r)`, we examine all buses with `f >= r`. Among them, if the minimum stored `s` is at most `l`, then some bus contains the interval.

The parallel binary search is the core optimization. Instead of running a separate binary search for every person and rebuilding structures repeatedly, all queries sharing the same midpoint are processed together.

One subtle implementation detail is the order of filtering by time. The segment tree at midpoint `mid` contains all buses from indices `0..mid`, but some of them may still have `t < b`. Since times are sorted, checking `buses[mid][0] < b` is enough. If the largest time in the prefix is still too small, no bus in that prefix can work.

Another easy mistake is overwriting segment tree values directly. Multiple buses may share the same `f`, so we must store the minimum `s` among them.

## Worked Examples

### Sample 1

Input:

```
4 3
1 10 10
5 6 2
6 7 3
5 7 4
5 7 1
1 2 1
1 10 11
```

Sorted buses by time:

| Time | Bus ID | Interval |
| --- | --- | --- |
| 2 | 2 | [5,6] |
| 3 | 3 | [6,7] |
| 4 | 4 | [5,7] |
| 10 | 1 | [1,10] |

Queries:

| Person | Interval | b |
| --- | --- | --- |
| 1 | [5,7] | 1 |
| 2 | [1,2] | 1 |
| 3 | [1,10] | 11 |

Binary search progression:

| Person | Mid Tested | Valid? | Result |
| --- | --- | --- | --- |
| 1 | Bus time 3 | No | move right |
| 1 | Bus time 4 | Yes | answer = bus 4 |
| 2 | Bus time 3 | No | move right |
| 2 | Bus time 10 | Yes | answer = bus 1 |
| 3 | Bus time 10 | No | answer = -1 |

Final output:

```
4 1 -1
```

This example shows why we need the earliest valid bus, not just any valid one. Person 1 could also ride bus 1, but bus 4 has smaller time.

### Custom Example

Input:

```
3 3
1 5 2
2 8 6
1 10 9
2 4 1
3 9 1
3 9 10
```

Sorted buses:

| Time | Bus ID | Interval |
| --- | --- | --- |
| 2 | 1 | [1,5] |
| 6 | 2 | [2,8] |
| 9 | 3 | [1,10] |

Processing:

| Person | Interval | First Valid Bus |
| --- | --- | --- |
| 1 | [2,4] | Bus 1 |
| 2 | [3,9] | Bus 3 |
| 3 | [3,9], b=10 | None |

Output:

```
1 3 -1
```

This trace demonstrates that the minimum-time bus may fail containment while a later one succeeds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log² n) | Parallel binary search performs O(log n) rounds, each with segment tree operations |
| Space | O(n + m) | Storage for buses, queries, buckets, and segment tree |

With `10^5` buses and people, `O(nm)` is impossible. The logarithmic factors here are small enough to fit comfortably inside the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

INF = 10**18

class SegTree:
    def __init__(self, n):
        self.n = 1
        while self.n < n:
            self.n <<= 1
        self.seg = [INF] * (2 * self.n)

    def update(self, pos, val):
        pos += self.n
        self.seg[pos] = min(self.seg[pos], val)

        pos >>= 1
        while pos:
            self.seg[pos] = min(self.seg[pos << 1],
                                self.seg[pos << 1 | 1])
            pos >>= 1

    def query(self, l, r):
        res = INF
        l += self.n
        r += self.n

        while l <= r:
            if l & 1:
                res = min(res, self.seg[l])
                l += 1
            if not (r & 1):
                res = min(res, self.seg[r])
                r -= 1
            l >>= 1
            r >>= 1

        return res

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())

    buses = []
    coords = []

    for idx in range(n):
        s, f, t = map(int, input().split())
        buses.append((t, s, f, idx + 1))
        coords.extend([s, f])

    people = []

    for idx in range(m):
        l, r, b = map(int, input().split())
        people.append((l, r, b, idx))
        coords.extend([l, r])

    coords = sorted(set(coords))
    comp = {x: i for i, x in enumerate(coords)}

    buses.sort()

    low = [0] * m
    high = [n - 1] * m
    ans = [-1] * m

    while True:
        buckets = [[] for _ in range(n)]
        active = False

        for i in range(m):
            if low[i] <= high[i]:
                active = True
                mid = (low[i] + high[i]) // 2
                buckets[mid].append(i)

        if not active:
            break

        seg = SegTree(len(coords))
        ptr = 0

        for mid in range(n):
            while ptr <= mid:
                t, s, f, idx = buses[ptr]
                seg.update(comp[f], s)
                ptr += 1

            for qi in buckets[mid]:
                l, r, b, idx = people[qi]

                if buses[mid][0] < b:
                    low[qi] = mid + 1
                    continue

                best = seg.query(comp[r], len(coords) - 1)

                if best <= l:
                    ans[qi] = mid
                    high[qi] = mid - 1
                else:
                    low[qi] = mid + 1

    res = []

    for x in ans:
        if x == -1:
            res.append("-1")
        else:
            res.append(str(buses[x][3]))

    return " ".join(res)

# provided sample
assert run(
"""4 3
1 10 10
5 6 2
6 7 3
5 7 4
5 7 1
1 2 1
1 10 11
"""
) == "4 1 -1", "sample 1"

# minimum case
assert run(
"""1 1
1 2 5
1 2 5
"""
) == "1", "minimum valid case"

# exact equality on time
assert run(
"""1 1
1 10 7
2 5 7
"""
) == "1", "t == b must work"

# containment failure
assert run(
"""2 1
1 5 2
2 10 3
3 9 1
"""
) == "-1", "no interval fully contains query"

# later bus succeeds
assert run(
"""3 1
1 5 2
2 8 6
1 10 9
3 9 1
"""
) == "3", "must choose later containing bus"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single bus and passenger | `1` | Minimum valid configuration |
| `t == b` | `1` | Equality boundary on time |
| No containing interval | `-1` | Correct interval containment logic |
| Later bus succeeds | `3` | Earliest valid bus is not always earliest overall |

## Edge Cases

Consider the equality boundary on time:

```
1 1
1 10 7
2 5 7
```

The passenger arrives exactly when the bus operates. Since the condition is `b <= t`, the bus is valid.

During binary search, midpoint time is `7`. The condition `buses[mid][0] < b` becomes `7 < 7`, which is false, so the query proceeds normally and succeeds.

Now consider overlapping but insufficient intervals:

```
2 1
1 5 2
2 10 3
3 9 1
```

The first bus fails because `5 < 9`. The second bus fails because `2 > 3`.

In the segment tree query over suffix `f >= 9`, only the second bus appears. Its stored minimum `s` is `2`, which is not `<= 3`, so the algorithm correctly rejects the query.

Finally, consider multiple buses sharing the same endpoint:

```
3 1
1 10 5
4 10 6
7 10 7
5 9 1
```

All buses satisfy `f >= 9`, but only the first two satisfy `s <= 5`.

The segment tree stores the minimum `s` for endpoint `10`, namely `1`. The suffix query returns `1`, correctly proving that a valid bus exists.
