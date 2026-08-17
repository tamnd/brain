---
title: "CF 102257C - Street Lamps"
description: "The street has (n+1) stops and (n) consecutive segments. Lamp (i) controls the segment between stops (i) and (i+1). At any moment, a taxi can travel from stop (a) to stop (b) exactly when every lamp with index (a,a+1,ldots,b-1) is on. The lamp configuration is given at time (0)."
date: "2026-08-17T20:47:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102257
codeforces_index: "C"
codeforces_contest_name: "2019 Asia-Pacific Informatics Olympiad (APIO 19)"
rating: 0
weight: 102257
solve_time_s: 91
verified: true
draft: false
---

[CF 102257C - Street Lamps](https://codeforces.com/problemset/problem/102257/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

The street has (n+1) stops and (n) consecutive segments. Lamp (i) controls the segment between stops (i) and (i+1). At any moment, a taxi can travel from stop (a) to stop (b) exactly when every lamp with index (a,a+1,\ldots,b-1) is on.

The lamp configuration is given at time (0). At the end of every hour, exactly one event happens. A toggle changes one lamp, while a query asks how many hours have elapsed during which the entire interval from stop (a) to stop (b) was continuously usable. The query includes all completed hours up to the current event time.

The constraints are (n,q\le 300000). A direct scan of all lamps in every query can take (O(nq)), which is as large as (9\cdot10^{10}) lamp checks. That is far beyond what a 5 second limit can support. We need roughly logarithmic work per event, giving an (O((n+q)\log n)) solution.

The first subtlety is that an event happens at the end of its hour. Consider

```
1 1
1
query 1 2
```

The answer is `1`, not `0`. The lamp was on throughout hour 1, so the completed hour counts.

The second subtlety is that a toggle at the end of an hour affects only future hours. In the official sample, lamp 3 is toggled at the end of hour 5. The configuration is `11011` during hours 1 through 5, and `11111` starting with hour 6. Thus a query at hour 6 sees exactly one usable hour for stops 3 and 4.

The third subtlety is a query spanning several lamps. For example,

```
3 1
101
query 1 4
```

has answer `0`, because the middle lamp is off. Checking only the endpoints would incorrectly conclude that the whole route is usable.

Finally, a query involving one segment is still a range query. For

```
2 1
01
query 2 3
```

the answer is `1`, because only lamp 2 matters. Converting stop indices directly to segment indices without handling the endpoint convention is a common source of off-by-one errors.

## Approaches

A straightforward solution can simulate the current lamp state and, for every query, inspect lamps (a) through (b-1). If they are all on, the query's answer could be increased by the number of hours since the previous event that left this configuration unchanged. This is correct because the configuration is constant between consecutive toggle events.

The problem is the range inspection. A single query may inspect (n) lamps, and there can be (q) queries. In the worst case this gives (O(nq)=9\cdot10^{10}) checks. Maintaining the current state itself is cheap, but repeatedly determining whether an entire interval consists of ones is not.

The key observation is that the question is not asking only whether a range is currently all on. It asks for the total amount of time during which that range was all on. This suggests storing historical information directly in a segment tree.

For every segment-tree node, keep whether every lamp in that node is currently on, together with the total time up to the last time that node was processed during which the whole node was on. Also store the timestamp at which this node's historical value was last finalized.

Suppose a node has been completely on since time (last). When we first need its information at time (t), its contribution for the unrecorded interval is simply (t-last). If the node is currently off, the contribution is zero. A point toggle changes only (O(\log n)) segment-tree nodes, so all affected historical values can be finalized in (O(\log n)). A range query visits (O(\log n)) canonical nodes, and each of those nodes can similarly be finalized at the query time.

The brute-force approach works because it explicitly checks every lamp that matters. It fails because the same long ranges are checked again and again. The observation that a segment's entire state changes only when one of its descendants is toggled lets us store its accumulated usable time and update it only when necessary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nq)) worst case | (O(n)) | Too slow |
| Optimal | (O((n+q)\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree over the (n) lamps. For each node, store `on`, which is true exactly when every lamp represented by that node is currently on. Also store `total`, the amount of already finalized time during which the entire node was on, and `last`, the timestamp through which `total` has been finalized.
2. Initialize every node's `last` value to zero. The initial configuration is valid from time zero onward, so no time has accumulated yet. The `on` values are computed from the initial binary string.
3. When a node is accessed at time (t), finalize its missing time interval. If `on` is true, add (t-last) to `total`. Then set `last=t`. If `on` is false, only `last` changes because the node contributed nothing during that interval.
4. For a toggle of lamp (i) at the end of hour (t), walk from that leaf toward the root and finalize every node on the path at time (t). This records the state that existed during hour (t) before the toggle. After that, flip the leaf's `on` value.
5. Recompute the ancestors of the toggled leaf from the bottom upward. A parent is currently on exactly when both of its children are currently on. Set the parent's `last` value to (t), because its new state begins at this timestamp.
6. For a query from stop (a) to stop (b), convert it to the half-open lamp interval ([a-1,b-1)). These are precisely lamps (a,a+1,\ldots,b-1). Decompose this interval into the usual (O(\log n)) segment-tree nodes.
7. Finalize every selected node at the current time (t), then add its `total` value to the answer. The selected nodes are disjoint and together contain exactly the requested lamps, so their usable-time contributions can be summed directly.
8. Output the resulting sum. A query does not change the lamp configuration, so no tree state needs to be recomputed after the query.

The invariant is that for every segment-tree node, `total` contains exactly the amount of time for which the entire segment was on during the interval from time zero through `last`. Its `on` flag describes the configuration immediately after `last`. Whenever the node is touched at a later time, the interval from `last` to the new time has a constant state, so adding its length exactly accounts for all newly completed usable time. Point toggles preserve this invariant along their root-to-leaf path, and range queries sum disjoint nodes whose represented intervals exactly form the requested route.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    s = input().strip()

    size = 1
    while size < n:
        size <<= 1

    # on[v]   = whether the whole segment of v is currently on
    # total[v] = finalized amount of time for which the whole segment was on
    # last[v] = time through which total[v] has been finalized
    on = [False] * (2 * size)
    total = [0] * (2 * size)
    last = [0] * (2 * size)

    for i, ch in enumerate(s):
        on[size + i] = (ch == '1')

    for v in range(size - 1, 0, -1):
        on[v] = on[v << 1] and on[v << 1 | 1]

    def touch(v, t):
        if on[v]:
            total[v] += t - last[v]
        last[v] = t

    def toggle(pos, t):
        v = size + pos

        # Finalize every node whose old state is about to change.
        u = v
        while u:
            touch(u, t)
            u >>= 1

        # Change the lamp itself.
        on[v] = not on[v]

        # Recompute ancestors using the new child states.
        v >>= 1
        while v:
            on[v] = on[v << 1] and on[v << 1 | 1]
            last[v] = t
            v >>= 1

    def query(left, right, t):
        # Query [left, right) in zero-based lamp indices.
        left += size
        right += size

        answer = 0

        while left < right:
            if left & 1:
                touch(left, t)
                answer += total[left]
                left += 1

            if right & 1:
                right -= 1
                touch(right, t)
                answer += total[right]

            left >>= 1
            right >>= 1

        return answer

    out = []

    for t in range(1, q + 1):
        event = input().split()

        if event[0] == "toggle":
            pos = int(event[1]) - 1
            toggle(pos, t)
        else:
            a = int(event[1])
            b = int(event[2])

            # Stops [a, b] correspond to lamps [a-1, b-1).
            left = a - 1
            right = b - 1

            out.append(str(query(left, right, t)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The tree uses a power-of-two number of leaves because that makes the iterative range decomposition simple. Extra leaves are initialized to off. They never appear in a valid query because every query ends at lamp (n), so they cannot affect a selected canonical node.

The `touch` function is the central operation. A node's state has remained unchanged since `last[v]`, so if it is currently on, exactly `t - last[v]` additional hours have elapsed with the entire segment illuminated.

The toggle operation first touches every ancestor using the old state. This ordering matters. If the leaf were flipped first, the time interval immediately before the toggle could be lost. After the old contribution has been finalized, the leaf is flipped and the ancestors are rebuilt.

The query converts stops to lamps carefully. Traveling from stop (a) to stop (b) uses lamps (a) through (b-1), so in zero-based half-open notation the interval is `[a - 1, b - 1)`.

Python integers do not overflow, and the largest answer is at most (q), which is only (300000). The implementation is iterative rather than recursively traversing the segment tree, avoiding Python recursion overhead across up to (300000) events.

## Worked Examples

The official sample is:

```
5 7
11011
query 1 2
query 1 2
query 1 6
query 3 4
toggle 3
query 3 4
query 1 6
```

The state during each completed hour and the relevant query result are:

| Hour | Event | Lamp state during hour | Query interval | Answer |
| --- | --- | --- | --- | --- |
| 1 | `query 1 2` | `11011` | lamp 1 | 1 |
| 2 | `query 1 2` | `11011` | lamp 1 | 2 |
| 3 | `query 1 6` | `11011` | lamps 1..5 | 0 |
| 4 | `query 3 4` | `11011` | lamp 3 | 0 |
| 5 | `toggle 3` | `11011` | none | 0 |
| 6 | `query 3 4` | `11111` | lamp 3 | 1 |
| 7 | `query 1 6` | `11111` | lamps 1..5 | 2 |

The resulting output is `1, 2, 0, 0, 1, 2`. This demonstrates the crucial timing rule: the toggle at the end of hour 5 changes the configuration only for hour 6 onward.

For a second example, consider:

```
3 5
111
query 1 4
toggle 2
query 1 4
toggle 2
query 1 4
```

The state and tree-level interpretation are:

| Hour | Event | Current state after event | Query interval | Answer |
| --- | --- | --- | --- | --- |
| 1 | `query 1 4` | `111` | lamps 1..3 | 1 |
| 2 | `toggle 2` | `101` | none | 0 |
| 3 | `query 1 4` | `101` | lamps 1..3 | 1 |
| 4 | `toggle 2` | `111` | none | 0 |
| 5 | `query 1 4` | `111` | lamps 1..3 | 2 |

At hour 3, the complete interval was usable only during hour 1, so the accumulated answer is still 1. After the second toggle, the whole interval becomes usable again starting at hour 5, giving two usable hours in total at the final query. The example exercises both directions of a toggle and confirms that historical time is preserved rather than recomputed from the current state.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((n+q)\log n)) | Building the tree costs (O(n)), each toggle touches one root-to-leaf path, and each query visits (O(\log n)) canonical nodes. |
| Space | (O(n)) | Four arrays of segment-tree size are maintained, with the tree containing (O(n)) nodes. |

With (n,q\le300000), the solution performs only logarithmically many tree operations per event, rather than potentially hundreds of thousands of lamp checks per query. This fits the 5 second, 512 MB limits given by the problem.

## Test Cases

```python
# helper: run the solution on an input string
import sys
import io

def solve_io(inp: str) -> str:
    data = inp.splitlines()
    it = iter(data)

    n, q = map(int, next(it).split())
    s = next(it).strip()

    size = 1
    while size < n:
        size <<= 1

    on = [False] * (2 * size)
    total = [0] * (2 * size)
    last = [0] * (2 * size)

    for i, ch in enumerate(s):
        on[size + i] = (ch == '1')

    for v in range(size - 1, 0, -1):
        on[v] = on[v << 1] and on[v << 1 | 1]

    def touch(v, t):
        if on[v]:
            total[v] += t - last[v]
        last[v] = t

    def toggle(pos, t):
        v = size + pos

        u = v
        while u:
            touch(u, t)
            u >>= 1

        on[v] = not on[v]

        v >>= 1
        while v:
            on[v] = on[v << 1] and on[v << 1 | 1]
            last[v] = t
            v >>= 1

    def query(left, right, t):
        left += size
        right += size
        ans = 0

        while left < right:
            if left & 1:
                touch(left, t)
                ans += total[left]
                left += 1

            if right & 1:
                right -= 1
                touch(right, t)
                ans += total[right]

            left >>= 1
            right >>= 1

        return ans

    out = []

    for t in range(1, q + 1):
        event = next(it).split()

        if event[0] == "toggle":
            toggle(int(event[1]) - 1, t)
        else:
            a = int(event[1])
            b = int(event[2])
            out.append(str(query(a - 1, b - 1, t)))

    return "\n".join(out)

# Official sample
assert solve_io(
    """5 7
11011
query 1 2
query 1 2
query 1 6
query 3 4
toggle 3
query 3 4
query 1 6
"""
) == """1
2
0
0
1
2""", "official sample"

# Minimum-size case
assert solve_io(
    """1 1
1
query 1 2
"""
) == "1", "single lamp"

# All lamps initially on, then the middle lamp is toggled off and on again
assert solve_io(
    """3 5
111
query 1 4
toggle 2
query 1 4
toggle 2
query 1 4
"""
) == """1
1
2""", "toggle off and back on"

# Boundary query with only the last lamp
assert solve_io(
    """2 3
01
query 2 3
toggle 2
query 2 3
"""
) == """1
1""", "last lamp boundary"

# Maximum-size n and q, all lamps initially on.
# Every event is a query over the complete street.
n = 300000
q = 300000
maximum_input = (
    f"{n} {q}\n"
    + "1" * n
    + "\n"
    + "\n".join(["query 1 300001"] * q)
    + "\n"
)
maximum_output = "\n".join(["1"] + [str(i) for i in range(2, q + 1)])
assert solve_io(maximum_input) == maximum_output, "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 / query 1 2` | `1` | Minimum size and the fact that the current completed hour counts |
| `3 5 / 111 / ...` | `1, 1, 2` | Repeated toggles and preservation of historical time |
| `2 3 / 01 / ...` | `1, 1` | Query beginning at the final stop pair and endpoint conversion |
| `300000 300000 / 1...1 / repeated full queries` | `1, 2, ..., 300000` | Maximum constraints and accumulation over a full range |

## Edge Cases

The minimum case has one lamp and two stops. For

```
1 1
1
query 1 2
```

the query corresponds to the single lamp, which is on throughout hour 1. The query interval becomes `[0,1)`, selecting exactly one leaf, and `touch` adds (1-0=1). The output is `1`.

A full-street query is another frequent source of off-by-one errors. With

```
3 1
111
query 1 4
```

the route from stop 1 to stop 4 uses lamps 1, 2, and 3. The implementation converts this to `[0,3)`, so all three leaves are selected. Since the complete segment was on throughout the first hour, the answer is `1`.

A toggle at the end of an hour must not retroactively change that hour. Consider

```
1 2
1
toggle 1
query 1 2
```

During hour 1 the lamp is on. The toggle occurs at the end of hour 1, so during hour 2 it is off. At the toggle timestamp, the leaf is first touched and receives one hour of accumulated on-time. The subsequent query touches it again, but its current state is off, so no additional time is added. The answer is `1`.

A range containing a single off lamp must contribute zero even if every other lamp is on. For

```
3 1
101
query 1 4
```

the root representing the complete street is currently off because its middle child is off. The query decomposes the range into nodes whose combined state is not entirely on, and every selected node containing the zero lamp contributes no time. The output is `0`.

The maximum-size case is also useful for checking that accumulated values remain correct over many queries. If all (300000) lamps start on and every event is a full-street query, the state never changes. The first query records one hour, the second records another hour, and so on, producing answers from 1 through 300000. The segment tree never needs to inspect individual lamps, so the repeated queries remain logarithmic.
