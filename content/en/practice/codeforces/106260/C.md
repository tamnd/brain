---
title: "CF 106260C - backpack"
description: "We are given a directed graph of caverns and tunnels. We start in cavern 1 with zero rocks in the backpack and want to reach cavern n. A tunnel adds a rocks when we enter it, then removes b rocks when we leave it."
date: "2026-06-25T07:24:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106260
codeforces_index: "C"
codeforces_contest_name: "2025 SiChuan University for new student"
rating: 0
weight: 106260
solve_time_s: 76
verified: true
draft: false
---

[CF 106260C - backpack](https://codeforces.com/problemset/problem/106260/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph of caverns and tunnels. We start in cavern `1` with zero rocks in the backpack and want to reach cavern `n`.

A tunnel adds `a` rocks when we enter it, then removes `b` rocks when we leave it. If we have fewer than `b` rocks available, the tunnel removes everything. If the current number of rocks is `r`, then after traversing a tunnel the new amount is

```
max(0, r + a - b)
```

It is convenient to define

```
w = a - b
```

so every tunnel applies

```
r -> max(0, r + w)
```

The task is to find the minimum number of rocks that can be present when we first arrive at cavern `n`. If cavern `n` is unreachable, the answer is `-1`.

The graph has at most 300 vertices, but can be very dense, up to `n(n-1)` directed edges. The tunnel parameters satisfy `0 ≤ a, b ≤ 10`, so every edge changes the rock count by at most 10 before the floor-at-zero operation is applied.

The small edge weights are the key observation. A simple path contains at most `n - 1` edges, so along any simple path the total decrease is at most

```
10 * (n - 1) ≤ 2990
```

This immediately suggests that only a bounded range of rock counts needs to be represented explicitly.

A subtle edge case appears when cycles exist.

Example:

```
1 -> 2 : +10
2 -> 3 : -9
3 -> 2 : 0
```

A shortest-path style solution fails because revisiting vertices changes the rock count and may improve the final answer.

Another important case is when a path requires temporarily accumulating many rocks before later reducing them.

Example:

```
1 -> 2 : +10
2 -> 2 : +10
2 -> n : -10
```

The optimal walk may use the positive cycle several times before leaving. Any solution that only considers simple paths misses such walks.

Finally, the graph may contain reachable positive cycles that allow arbitrarily large rock counts. We cannot store every possible value explicitly, so the state space must be compressed carefully.

## Approaches

A brute-force search treats a state as `(vertex, rocks)` and explores all reachable states.

This is correct because the transition is deterministic:

```
r -> max(0, r + w)
```

The problem is that the rock count is theoretically unbounded. A reachable positive cycle can increase the number of rocks forever, producing infinitely many states.

The crucial observation is that edge weights are bounded by 10 and the graph contains only 300 vertices.

Let

```
B = 10 * (n - 1)
```

For this problem,

```
B ≤ 2990
```

Suppose we currently have more than `B` rocks. No simple path can decrease the count by more than `B`, because every edge contributes at least `-10`.

That means once the count becomes sufficiently large, the exact value is no longer important. Every value above a fixed threshold behaves similarly. We can store all counts up to a limit explicitly and merge everything larger into a single special state.

A convenient choice is

```
LIMIT = B + 10 = 3000
```

If we ever have more than 3000 rocks, then after traversing any edge we still have more than 2990 rocks. The floor-at-zero operation can never become relevant while we stay in this region.

This converts the infinite state space into a finite one:

```
(vertex, 0..3000)
```

plus one extra "large" state per vertex.

The remaining challenge is efficiency. Instead of storing reachable counts individually, we store them as bitsets. A bitset of length 3001 fits comfortably into a Python integer, and every edge transformation becomes a few bit operations.

The resulting algorithm is a monotone reachability propagation on a finite graph and converges to the complete set of reachable states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over exact rock counts | Unbounded | Unbounded | Too slow |
| Bitset reachability with compressed large states | O(m · LIMIT / word_size) in practice | O(n · LIMIT) | Accepted |

## Algorithm Walkthrough

1. For every tunnel compute

```
w = a - b
```

since the transition only depends on this value.
2. Let

```
LIMIT = 3000
```

Counts `0..3000` are represented explicitly.
3. For every vertex maintain:

```
bits[v]
```

where bit `k` is set if rock count `k` is reachable at vertex `v`.

Also maintain

```
big[v]
```

which means some count greater than 3000 is reachable at vertex `v`.
4. Initialize

```
bits[1] = {0}
```

because we start at cavern 1 with zero rocks.
5. Repeatedly propagate information along outgoing edges.

For a nonnegative weight `w`:

```
k -> k + w
```

Counts that exceed 3000 generate the `big` state.
6. For a negative weight `-d`:

```
k -> max(0, k - d)
```

This is implemented with a right shift of the bitset, plus setting bit 0 if any count below `d` was reachable.
7. If `big[u]` is true and there is an edge `u -> v`, then `big[v]` also becomes true.

Any count above 3000 remains above 2990 after one transition, so the exact value is irrelevant.
8. Use a queue. Whenever a vertex receives new reachable states, push it into the queue so its outgoing edges are processed again.
9. After the fixed point is reached, inspect the bitset of vertex `n`.

The smallest set bit is the minimum reachable rock count.
10. If neither the bitset nor the large state is reachable at vertex `n`, output `-1`.

### Why it works

The algorithm computes the least fixed point of the reachability relation.

Every reachable state is generated because we begin from the initial state and repeatedly apply all valid transitions. No reachable state is omitted.

The compression is safe because values greater than 3000 can never return directly to the explicit range in a single step. The maximum decrease of one edge is 10, so a count larger than 3000 always remains larger than 2990 after a transition. The exact value is irrelevant once we enter this region, and the single `big` state captures all such possibilities.

Since the finite state space is explored exhaustively and every transition is modeled exactly, the set of reachable rock counts at cavern `n` is correct. Taking the smallest reachable count gives the required answer.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

LIMIT = 3000
MASK = (1 << (LIMIT + 1)) - 1

def transform(bits, w):
    if bits == 0:
        return 0, False

    if w >= 0:
        shifted = bits << w

        low = shifted & MASK
        high = shifted >> (LIMIT + 1)

        return low, high != 0

    d = -w

    low_part = bits & ((1 << d) - 1) if d <= LIMIT else bits
    res = bits >> d

    if low_part:
        res |= 1

    return res, False

def solve():
    n, m = map(int, input().split())

    g = [[] for _ in range(n)]

    for _ in range(m):
        x, y, a, b = map(int, input().split())
        g[x - 1].append((y - 1, a - b))

    bits = [0] * n
    big = [False] * n

    bits[0] = 1  # rock count 0

    q = deque([0])
    inq = [False] * n
    inq[0] = True

    while q:
        u = q.popleft()
        inq[u] = False

        cur_bits = bits[u]
        cur_big = big[u]

        for v, w in g[u]:
            add_bits, make_big = transform(cur_bits, w)

            changed = False

            new_bits = bits[v] | add_bits
            if new_bits != bits[v]:
                bits[v] = new_bits
                changed = True

            if cur_big or make_big:
                if not big[v]:
                    big[v] = True
                    changed = True

            if changed and not inq[v]:
                inq[v] = True
                q.append(v)

    target = bits[n - 1]

    if target == 0 and not big[n - 1]:
        print(-1)
        return

    answer = (target & -target).bit_length() - 1
    print(answer)

solve()
```

The solution stores all reachable counts up to 3000 inside one Python integer. Bit `k` corresponds to rock count `k`.

For nonnegative edge weights we shift the bitset left. Any bits that move beyond position 3000 indicate counts larger than the explicit range, so the destination vertex receives the `big` flag.

For negative edge weights we shift right. Counts smaller than the magnitude of the negative weight collapse to zero because of the `max(0, ...)` operation. That is why bit 0 must be added whenever one of those small counts was reachable.

The queue-based propagation is a standard monotone data-flow process. A vertex is processed again only when its reachable-state set grows.

The expression

```
(target & -target).bit_length() - 1
```

returns the index of the lowest set bit, which is exactly the smallest reachable rock count.

## Worked Examples

### Example 1

Input:

```
4 4
1 2 10 0
2 4 2 1
4 3 0 5
3 2 3 3
```

The effective edge weights are:

```
1 -> 2 : +10
2 -> 4 : +1
4 -> 3 : -5
3 -> 2 : 0
```

| Step | Vertex | Rocks |
| --- | --- | --- |
| Start | 1 | 0 |
| 1 -> 2 | 2 | 10 |
| 2 -> 4 | 4 | 11 |
| 4 -> 3 | 3 | 6 |
| 3 -> 2 | 2 | 6 |
| 2 -> 4 | 4 | 7 |
| 4 -> 3 | 3 | 2 |
| 3 -> 2 | 2 | 2 |
| 2 -> 4 | 4 | 3 |
| 4 -> 3 | 3 | 0 |
| 3 -> 2 | 2 | 0 |
| 2 -> 4 | 4 | 1 |

The minimum reachable value at cavern 4 is 1.

### Example 2

Input:

```
3 2
1 2 5 0
2 3 0 10
```

Effective weights:

```
1 -> 2 : +5
2 -> 3 : -10
```

| Step | Vertex | Rocks |
| --- | --- | --- |
| Start | 1 | 0 |
| 1 -> 2 | 2 | 5 |
| 2 -> 3 | 3 | 0 |

The second edge removes all available rocks, so the answer is 0.

This example demonstrates why the transition is not ordinary addition. Negative values are never allowed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m · LIMIT / word_size) in practice | Bitset operations process many rock counts simultaneously |
| Space | O(n · LIMIT) | One bitset of length 3001 per vertex |

With `n ≤ 300` and `LIMIT = 3000`, the total state representation is under one million bits. The bitset-based propagation easily fits within the memory limit and is fast enough for the graph sizes in this problem.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    LIMIT = 3000
    MASK = (1 << (LIMIT + 1)) - 1

    def transform(bits, w):
        if bits == 0:
            return 0, False

        if w >= 0:
            shifted = bits << w
            return shifted & MASK, (shifted >> (LIMIT + 1)) != 0

        d = -w
        low_part = bits & ((1 << d) - 1)
        res = bits >> d
        if low_part:
            res |= 1
        return res, False

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())

    g = [[] for _ in range(n)]

    for _ in range(m):
        x, y, a, b = map(int, input().split())
        g[x - 1].append((y - 1, a - b))

    from collections import deque

    bits = [0] * n
    big = [False] * n

    bits[0] = 1

    q = deque([0])
    inq = [False] * n
    inq[0] = True

    while q:
        u = q.popleft()
        inq[u] = False

        for v, w in g[u]:
            add_bits, make_big = transform(bits[u], w)

            changed = False

            nb = bits[v] | add_bits
            if nb != bits[v]:
                bits[v] = nb
                changed = True

            if big[u] or make_big:
                if not big[v]:
                    big[v] = True
                    changed = True

            if changed and not inq[v]:
                inq[v] = True
                q.append(v)

    target = bits[n - 1]

    if target == 0 and not big[n - 1]:
        return "-1\n"

    ans = (target & -target).bit_length() - 1
    return str(ans) + "\n"

# sample
assert run(
"""4 4
1 2 10 0
2 4 2 1
4 3 0 5
3 2 3 3
"""
) == "1\n"

# minimum graph
assert run(
"""1 1
1 1 0 0
"""
) == "0\n"

# unreachable target
assert run(
"""3 1
1 2 1 0
"""
) == "-1\n"

# saturation at zero
assert run(
"""3 2
1 2 5 0
2 3 0 10
"""
) == "0\n"

# positive cycle
assert run(
"""3 3
1 2 10 0
2 2 10 0
2 3 0 10
"""
) == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex graph | 0 | Start equals destination |
| Unreachable destination | -1 | Reachability handling |
| Large negative edge | 0 | Correct floor-at-zero behavior |
| Positive cycle | 0 | Infinite-state compression |
| Sample graph | 1 | Full problem logic |

## Edge Cases

Consider:

```
3 2
1 2 5 0
2 3 0 10
```

The transition from 5 rocks through the second edge is

```
max(0, 5 - 10) = 0
```

The algorithm handles this through the negative-weight transformation. Any count below the required decrease contributes to bit 0 in the destination bitset.

Now consider an unreachable destination:

```
3 1
1 2 1 0
```

No state is ever propagated into vertex 3. Its bitset remains empty and its `big` flag remains false, so the algorithm correctly outputs `-1`.

Finally, consider a reachable positive cycle:

```
3 3
1 2 10 0
2 2 10 0
2 3 0 10
```

The self-loop at vertex 2 can increase the rock count without bound. Once the count exceeds the explicit limit, the algorithm switches to the compressed `big` representation. Reachability remains correct without storing infinitely many values.
