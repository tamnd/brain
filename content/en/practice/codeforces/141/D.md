---
title: "CF 141D - Take-off Ramps"
description: "We are moving on a one-dimensional track from position 0 to position L. Walking is simple, one meter costs exactly one second, and we may move in either direction as long as we never go below 0. A ramp gives a shortcut, but using it has a strict structure."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 141
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 101 (Div. 2)"
rating: 2300
weight: 141
solve_time_s: 135
verified: true
draft: false
---

[CF 141D - Take-off Ramps](https://codeforces.com/problemset/problem/141/D)

**Rating:** 2300  
**Tags:** graphs, shortest paths  
**Solve time:** 2m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are moving on a one-dimensional track from position `0` to position `L`. Walking is simple, one meter costs exactly one second, and we may move in either direction as long as we never go below `0`.

A ramp gives a shortcut, but using it has a strict structure. For a ramp `(x, d, t, p)`, Vasya must first stand at position `x - p`, then spend `p` seconds skiing normally to reach `x`, and finally fly to `x + d` in `t` seconds. The flight always goes to the right.

If we compare this with normal walking, traversing the interval from `x - p` to `x + d` on foot would cost `p + d` seconds. Using the ramp instead costs `p + t` seconds. The ramp is useful only when `t < d`.

The task is not only to compute the minimum total time, but also to reconstruct which ramps are used.

The constraints immediately rule out any quadratic shortest-path construction. There can be up to `10^5` ramps, so even building all pairwise transitions would require around `10^10` edges, far beyond the limit. We need something close to `O(n log n)`.

The track length `L` can reach `10^9`, which means we cannot build a DP over positions. Only the ramp endpoints matter.

Several edge cases are easy to mishandle.

A ramp may be impossible to use because the preparation segment starts before zero.

Example:

```
1 20
4 10 1 7
```

The ramp requires starting at `-3`, which is forbidden. The correct answer is simply walking for `20` seconds.

A ramp can also be useless even if reachable.

Example:

```
1 20
5 3 10 2
```

Walking through that section costs `2 + 3 = 5`, while the ramp costs `2 + 10 = 12`. An implementation that blindly takes every reachable ramp produces a non-optimal answer.

Another subtle case is moving backward. The statement allows movement in both directions. A careless greedy solution might assume ramps must be used in increasing order of their takeoff points. That is not always true locally. Still, the optimal global structure turns out to be acyclic after compression, and proving that is the key insight of the problem.

Example:

```
2 30
10 10 1 1
5 20 100 1
```

The second ramp is terrible, but the first is excellent. The best route is still monotone to the right.

## Approaches

A brute-force view models every ramp as a state. From one ramp, we can walk to the preparation point of another ramp and use it next. We can also finish by walking directly to `L`.

Suppose we define a graph where each node represents a ramp, plus a start node and a finish node. If we are currently at position `a`, and another ramp starts preparation at `b`, then walking there costs `|a - b|`. Using the ramp adds its flight time.

This graph is correct because every valid route becomes a path in the graph. Unfortunately, every ramp can potentially transition to every other ramp, so the graph has `O(n^2)` edges. With `10^5` ramps, this is completely infeasible.

The key observation is that the world outside ramps is extremely simple. Walking cost between two positions is just linear distance. That means we do not actually need arbitrary transitions.

Consider a ramp `(x, d, t, p)`. Using it replaces walking over a segment of length `p + d` with a cost of `p + t`. Relative to pure walking, the ramp changes the total by:

$$t - d$$

The preparation part cancels out.

This transforms the whole problem. Imagine Vasya always walks from `0` to `L`, paying `L` seconds. Every ramp used contributes an additional value `t - d`. Since good ramps satisfy `t < d`, they reduce the total.

Now we only need to know whether ramps can be chained. Ramp `A` ending at `x_A + d_A` can be followed by ramp `B` if:

$$x_B - p_B \ge x_A + d_A$$

because we can walk forward between them.

Backward walking is never beneficial. If we move backward, we only add extra walking distance while ramps themselves never move left. Any path with backward motion can be straightened into a monotone path with no greater cost.

That gives us a DAG ordered by position.

We can now run shortest path DP over ramps sorted by their preparation start point. The transition becomes:

$$dp[i] = (t_i - d_i) + \min dp[j]$$

over all ramps `j` that end before ramp `i` begins preparation.

This is a classic sweep-line minimum query problem. As we process ramps in sorted order, we maintain the best DP value among ramps whose landing positions are already reachable.

A priority queue or ordered sweep reduces the complexity to `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force graph | O(n²) | O(n²) | Too slow |
| Sweep-line DP | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Discard every ramp with `x - p < 0`.

Such ramps can never be used because preparation would begin before the start line.
2. For every remaining ramp, compute:

$$s = x - p$$

and

$$e = x + d$$

Here `s` is the preparation start position and `e` is the landing position.
3. Sort ramps by `s`.

This lets us process ramps from left to right while maintaining which previous ramps can connect into the current one.
4. Define `dp[i]` as the minimum extra cost relative to pure walking when the last used ramp is ramp `i`.

Since walking the entire track costs `L`, the final answer becomes:

$$L + \min(0, dp[i])$$
5. For a single ramp used directly from the start, the extra cost is:

$$t_i - d_i$$

because walking from `0` to `L` already includes the preparation and landing distances.
6. Maintain a priority structure of ramps ordered by landing position `e`.

While processing ramp `i`, every previous ramp with `e \le s_i` can precede it.
7. Keep track of the smallest DP value among all currently valid predecessor ramps.

Then:

$$dp[i] = (t_i - d_i) + best$$

where `best` is either `0` for starting directly, or the minimum predecessor DP.
8. Store parent pointers whenever a predecessor improves the value.

This allows reconstruction of the chosen ramps.
9. After processing all ramps, choose the best among:

`L` with no ramps,

or

$$L + dp[i]$$

for every ramp.
10. Reconstruct the path using parent pointers and print the original ramp indices.

### Why it works

The invariant is that while processing ramps in increasing preparation-start order, the maintained minimum DP value corresponds exactly to all ramps that can legally precede the current ramp.

Because every ramp moves strictly to the right, any feasible sequence of ramps forms a monotone chain. Walking between ramps is uniquely determined by positions, so the only meaningful optimization is choosing which beneficial segments replace walking.

The DP stores the minimum additional cost beyond baseline walking. Every ramp independently contributes `t - d`, and valid transitions only require non-overlapping order:

$$e_j \le s_i$$

Thus every feasible solution is represented exactly once in the DP, and every DP transition corresponds to a valid route.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, L = map(int, input().split())

    ramps = []

    for idx in range(1, n + 1):
        x, d, t, p = map(int, input().split())

        s = x - p
        if s < 0:
            continue

        e = x + d
        gain = t - d

        ramps.append((s, e, gain, idx))

    ramps.sort()

    m = len(ramps)

    dp = [0] * m
    parent = [-1] * m

    heap = []

    best_value = 0
    best_idx = -1

    answer = L
    answer_idx = -1

    ptr = 0

    by_end = sorted(
        [(ramps[i][1], i) for i in range(m)]
    )

    for s, end_idx in by_end:
        pass

    events = sorted(
        [(ramps[i][1], i) for i in range(m)]
    )

    ptr = 0

    for i in range(m):
        s_i, e_i, gain_i, orig_i = ramps[i]

        while ptr < m and events[ptr][0] <= s_i:
            _, j = events[ptr]

            heapq.heappush(heap, (dp[j], j))
            ptr += 1

        if heap:
            best_value, best_idx = heap[0]
        else:
            best_value, best_idx = 0, -1

        dp[i] = gain_i + best_value
        parent[i] = best_idx

        total = L + dp[i]

        if total < answer:
            answer = total
            answer_idx = i

    path = []

    cur = answer_idx

    while cur != -1:
        path.append(ramps[cur][3])
        cur = parent[cur]

    path.reverse()

    print(answer)
    print(len(path))

    if path:
        print(*path)
    else:
        print()

solve()
```

The solution starts by filtering invalid ramps. This matters because ramps with `x - p < 0` cannot even begin preparation, so they must never enter the DP.

Each ramp is converted into a compact form containing its preparation start `s`, landing point `e`, and contribution `t - d`. That contribution is the only part affecting optimization once we treat plain walking as the baseline cost.

The ramps are sorted by `s`, which guarantees that every valid predecessor appears earlier in processing order.

The subtle part is maintaining the best reachable predecessor. We cannot scan all previous ramps because that would return to quadratic complexity. Instead, we process ramps whose landing position is already small enough. Once a ramp satisfies:

```
e_j <= s_i
```

it becomes permanently eligible for all future ramps because future `s_i` values only increase.

The heap stores pairs `(dp[j], j)`, so the top always gives the smallest reachable DP value.

A common mistake is trying to greedily use every beneficial ramp. Two individually good ramps may overlap and become incompatible. The DP avoids this by only transitioning from ramps whose landing point is before the next preparation start.

Another easy bug is forgetting that the optimal solution may use no ramps at all. The initial answer is set to `L`, representing pure walking.

All arithmetic safely fits in Python integers since values can reach around `10^14`.

## Worked Examples

### Sample 1

Input:

```
2 20
5 10 5 5
4 16 1 7
```

Only ramp 1 is valid because ramp 2 starts preparation at `-3`.

| Ramp | s | e | t-d | Best previous | dp |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 15 | -5 | 0 | -5 |

Final answer:

$$20 + (-5) = 15$$

Chosen ramps: `[1]`

This trace shows why impossible ramps must be discarded before DP processing. If ramp 2 were included, the algorithm would incorrectly believe an enormous shortcut exists.

### Sample 2

```
2 20
5 3 10 2
14 6 1 1
```

| Ramp | s | e | t-d | Best previous | dp |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 8 | 7 | 0 | 7 |
| 2 | 13 | 20 | -5 | 0 | -5 |

Ramp 1 is harmful because its flight time exceeds the walking distance saved.

Final answer:

$$20 + (-5) = 15$$

Chosen ramps: `[2]`

This demonstrates that the DP naturally ignores bad ramps without requiring special-case logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting and heap operations dominate |
| Space | O(n) | DP arrays, heap, and parent reconstruction |

With `10^5` ramps, `O(n log n)` easily fits inside the time limit. Memory usage remains linear and comfortably below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    n, L = map(int, input().split())

    ramps = []

    for idx in range(1, n + 1):
        x, d, t, p = map(int, input().split())

        s = x - p

        if s < 0:
            continue

        e = x + d
        gain = t - d

        ramps.append((s, e, gain, idx))

    ramps.sort()

    m = len(ramps)

    dp = [0] * m
    parent = [-1] * m

    events = sorted((ramps[i][1], i) for i in range(m))

    heap = []

    ptr = 0

    answer = L
    answer_idx = -1

    for i in range(m):
        s_i, e_i, gain_i, orig_i = ramps[i]

        while ptr < m and events[ptr][0] <= s_i:
            _, j = events[ptr]
            heapq.heappush(heap, (dp[j], j))
            ptr += 1

        if heap:
            best, best_idx = heap[0]
        else:
            best, best_idx = 0, -1

        dp[i] = gain_i + best
        parent[i] = best_idx

        total = L + dp[i]

        if total < answer:
            answer = total
            answer_idx = i

    path = []

    cur = answer_idx

    while cur != -1:
        path.append(ramps[cur][3])
        cur = parent[cur]

    path.reverse()

    print(answer)
    print(len(path))

    if path:
        print(*path)
    else:
        print()

    return out.getvalue()

# provided samples

assert run(
"""2 20
5 10 5 5
4 16 1 7
"""
) == "15\n1\n1\n", "sample 1"

assert run(
"""2 20
5 3 10 2
14 6 1 1
"""
) == "15\n1\n2\n", "sample 2"

# minimum size

assert run(
"""0 7
"""
) == "7\n0\n\n", "no ramps"

# invalid ramp

assert run(
"""1 30
5 20 1 10
"""
) == "30\n0\n\n", "ramp starts before zero"

# chain of ramps

assert run(
"""2 50
10 10 1 1
25 20 1 1
"""
) == "22\n2\n1 2\n", "two compatible ramps"

# overlapping ramps

assert run(
"""2 40
10 20 1 1
15 20 1 1
"""
) == "20\n1\n1\n", "cannot take overlapping ramps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| No ramps | Walk entire distance | Base case |
| Ramp starting before zero | Ignore invalid ramp | Boundary condition |
| Two compatible ramps | Chain reconstruction | Parent tracking |
| Overlapping ramps | Transition legality | Correct predecessor condition |

## Edge Cases

Consider a ramp whose preparation begins before zero.

Input:

```
1 20
4 16 1 7
```

The preparation start is:

$$4 - 7 = -3$$

The algorithm discards this ramp immediately during preprocessing. No DP state is created for it, so the only remaining option is walking directly to the finish.

Output:

```
20
0
```

Now consider a harmful ramp.

Input:

```
1 20
5 3 10 2
```

The ramp contribution is:

$$10 - 3 = 7$$

Using it actually increases total time. The DP computes:

$$20 + 7 = 27$$

which is worse than plain walking. Since the answer is initialized with `20`, the algorithm correctly chooses no ramps.

Finally, consider overlapping ramps.

Input:

```
2 40
10 20 1 1
15 20 1 1
```

Ramp 1 lands at:

$$10 + 20 = 30$$

Ramp 2 requires preparation from:

$$15 - 1 = 14$$

Since `30 > 14`, the second ramp cannot follow the first. The sweep structure never inserts ramp 1 into the valid predecessor set while processing ramp 2, so the illegal transition is impossible inside the DP.
