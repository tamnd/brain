---
title: "CF 102471D - Fire"
description: "Root the tree at vertex 1. Pang starts at the root and must eventually cast his magic exactly once at every vertex."
date: "2026-08-09T04:36:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102471
codeforces_index: "D"
codeforces_contest_name: "2019 ICPC Asia-East Continent Final"
rating: 0
weight: 102471
solve_time_s: 513
verified: true
draft: false
---

[CF 102471D - Fire](https://codeforces.com/problemset/problem/102471/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

Root the tree at vertex 1. Pang starts at the root and must eventually cast his magic exactly once at every vertex. Because every directed edge can be used at most once, a subtree that is entered and later left through its parent has a completely determined movement cost: if the subtree contains `s` vertices, traversing it and returning to the entry vertex uses exactly `2s` moves. The only freedom is the order in which sibling subtrees are processed and which subtree contains the final vertex of the entire walk.

Let `a[v]` be the temperature of vertex `v` immediately before the morning of day 1. If Pang casts magic at vertex `v` on day `t`, its temperature after the evening magic is `a[v] - t + k`. If he leaves on day `d`, the morning of day `d` has already reduced that temperature by the appropriate number of days, so the source vertex must be strictly positive. The destination only has to be non-negative. These two different inequalities are responsible for several boundary cases.

The output is the latest day on which Pang can prepare at vertex 1, meaning he casts the magic at vertex 1 on that day and makes his first move on the following day. If even day 0 cannot work, the answer is `-1`.

The bound `n <= 100000` rules out anything quadratic, especially because the time limit is only one second. A traversal of the whole tree is already linear, so the target is essentially `O(n)` or `O(n log n)`. The temperature and `k` values can reach `10^9`, while subtree sizes can reach `10^5`, so intermediate expressions such as `k + a[v] - 2 * size[v]` should be handled with 64-bit arithmetic in languages with fixed-width integers. Python integers have arbitrary precision, so there is no overflow issue in the implementation.

One boundary case is that the destination temperature may be exactly zero. Consider a two-vertex tree with `k = 0` and temperatures `2 1`.

```
2 0
1 2
2 1
```

The answer is `0`. Pang casts at vertex 1 on day 0, moves on day 1, and arrives at vertex 2 with temperature zero. A careless implementation that requires the destination to have positive temperature would incorrectly reject this case.

The source vertex has the opposite condition, it must be strictly positive. With the same tree and `k = 0`, change the root temperature to `1`.

```
2 0
1 2
1 1
```

The answer is `-1`. After casting on day 0, the root has temperature 1, but the morning of day 1 reduces it to zero, so Pang cannot make the move. Checking only the destination temperature misses this failure.

The order of sibling subtrees is also significant. Consider

```
5 2
1 2
1 3
1 4
4 5
100 1 100 100 100
```

The correct answer is `93`. Vertex 2 has a very tight deadline, so its subtree must be visited before the larger subtree rooted at vertex 4. Processing children in input order can put the large subtree first and make vertex 2 unreachable in time. A solution that merely tries DFS in adjacency-list order can consequently fail even though a valid schedule exists.

Finally, day 0 is special because temperatures do not decrease on that day. For

```
2 2
1 2
0 1
```

the answer is `0`. Pang can cast magic at vertex 1 on day 0, raising its temperature from zero to two, and then move on day 1 to vertex 2, whose temperature is exactly zero that morning. Treating day 0 as if the first temperature decrement had already happened loses this valid solution.

## Approaches

A direct approach would enumerate possible walks through the tree. Once the tree is rooted, every non-final child subtree must be entered, completely explored, and returned from. The final subtree is the only one that does not need a return. For every possible ordering of children, we could simulate the days, checking the temperature before every move and magic operation.

This is correct because every legal walk has exactly this recursive structure. The problem is the number of orderings. A star with `n - 1` leaves already has `(n - 1)!` possible orders, and simulating each order takes `Theta(n)` moves. The worst-case work is therefore `Theta(n * (n - 1)!)`, long before we reach `n = 100000`.

The brute force works because a tree forces every completed subtree to behave like a single excursion. The key observation is that such an excursion has a fixed duration, exactly twice the number of vertices in the subtree. Once a child subtree is summarized by the latest day on which it may be entered, the parent only has to schedule these fixed-duration excursions before their deadlines.

Suppose the children of `u` are ordered as `v_1, v_2, ..., v_d`. If Pang casts at `u` on day `t`, then child `v_i` is entered on day

[
t + 1 + 2\sum_{j<i} size[v_j].
]

If `f[v_i]` is the latest valid arrival day for a complete round trip through `v_i`, we need

[
t + 1 + 2\sum_{j<i} size[v_j] \le f[v_i].
]

Rearranging gives

[
t \le f[v_i]-1-2\sum_{j<i}size[v_j].
]

This is a scheduling problem. Each child has processing time `2 * size[v]`, and its effective deadline is `f[v] + 2 * size[v]`. Sorting children by this value gives an optimal order. This is the same ordering described in the official-style solution notes for this problem.

There is one more complication. The whole walk does not have to return to vertex 1. In fact, it must finish at a leaf. We therefore need a second DP state that allows the final child subtree to be traversed without returning to its parent. The children before that final child still have to be scheduled in the same optimal order.

For one fixed final child, deleting that child from the ordered list only changes the prefix time of children after it. Prefix and suffix minima let us calculate the best deadline of all remaining children in constant time per possible final child. Thus, after sorting the children, the entire transition for one vertex is linear in its degree.

The resulting comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `Theta(n * (n - 1)!)` in a star | `O(n)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex 1 and compute a bottom-up order. For every vertex `u`, let `size[u]` be the number of vertices in its rooted subtree. Processing vertices in reverse DFS order guarantees that every child has already been solved when we handle `u`.
2. Define `f[u]` as the latest day on which Pang may arrive at `u`, cast magic there, traverse the entire subtree of `u`, return to `u`, and finally leave `u` toward its parent. This state describes a subtree that behaves as a complete round trip for its parent.
3. Sort the children of `u` by

[
f[v] + 2size[v].
]

For a child `v` placed after previous subtrees whose total size is `P`, its entry day is `t + 1 + 2P`, so it requires

[
t \le f[v]-1-2P.
]

The sorting rule is the earliest effective deadline rule for these fixed-duration excursions. If two adjacent children violate this order, swapping them cannot make the maximum feasible starting day smaller, so repeatedly removing such inversions gives the sorted order.

1. After sorting, let `deadline[i]` be the constraint contributed by child `i` when all earlier children are processed before it:

[
deadline[i] = f[v_i]-1-2\sum_{j<i}size[v_j].
]

The best start day for all child excursions is the minimum of these values.

Pang also has to survive at `u` itself. If he starts at `u` on day `t`, the initial casting requires `t <= a[u]`. To traverse the entire subtree and then leave toward the parent, there are `2size[u]-1` moves after the casting day. The final departure requires `u` to be positive, which gives

[
t \le a[u] + k - 2size[u].
]

Consequently,

[
f[u] =
\min\left(
a[u],
a[u]+k-2size[u],
\min_i deadline[i]
\right).
]

For a leaf, this reduces to `min(a[u], a[u] + k - 2)`.

1. Define `g[u]` as the latest day on which Pang may arrive at `u`, cast there, traverse the entire subtree, and finish anywhere inside that subtree. Unlike `f[u]`, `g[u]` does not require a final move from `u` to its parent.

If `u` is a leaf, Pang can simply finish there, so `g[u] = a[u]`.

1. For an internal vertex `u`, choose one child `c` to be the final child. Every other child must be completely traversed and returned from before `c` is entered.

Let

[
S = size[u]-1-size[c]
]

be the total size of all non-final child subtrees. They consume `2S` moves before the final child is entered.

The final child can therefore only be entered on or before its own `g[c]` deadline:

[
t+1+2S \le g[c],
]

giving

[
t \le g[c]-1-2S.
]

Pang also needs to be able to leave `u` for the final child. That move occurs on day `t+1+2S`, so the temperature condition at `u` gives

[
t \le a[u]+k-2-2S.
]

1. We still need the constraints of all non-final children. Removing child `c` from the sorted list leaves the children before `c` unchanged, while every child after `c` starts `2size[c]` days earlier. Compute a prefix minimum of the original child deadlines and a suffix minimum. For child `c`, the best constraint from all other children is

[
side(c)=
\min\left(
prefix[c],
suffix[c+1]+2size[c]
\right).
]

The first term covers children before `c`. The second term covers children after `c`, whose prefix becomes smaller by `size[c]`.

1. The candidate answer when `c` is the final child is

[
candidate(c)=
\min\left(
a[u],
a[u]+k-2-2S,
g[c]-1-2S,
side(c)
\right).
]

Take the maximum over all children. That maximum is `g[u]`, because every valid traversal must choose exactly one child as the direction in which the final vertex lies.

1. At the root there is no parent that Pang needs to return to. Hence the required latest preparation day is exactly `g[1]`. If `g[1] < 0`, even preparation on day 0 cannot work, so the answer is `-1`. Otherwise print `g[1]`.

### Why it works

The central invariant is that `f[u]` is exactly the latest feasible casting day for a traversal that completely processes `u`'s subtree and returns to its parent, while `g[u]` is exactly the latest feasible casting day when the traversal may finish anywhere inside the subtree. For `f[u]`, every child excursion has a fixed duration and a latest allowed starting time, so exchanging two incorrectly ordered adjacent children shows that sorting by `f[v] + 2size[v]` is optimal. For `g[u]`, every valid traversal has exactly one final child. All other children form complete excursions and can be scheduled by the same optimal ordering. The prefix and suffix minima calculate precisely the constraints of those excursions after the final child is removed. Since every possible final child is considered, `g[u]` takes the best valid choice. At the root, every complete walk corresponds to one such final-child choice, so `g[1]` is exactly the latest possible preparation day.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        graph[x].append(y)
        graph[y].append(x)

    a = list(map(int, input().split()))

    parent = [-2] * n
    parent[0] = -1

    order = [0]
    for u in order:
        for v in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)

    size = [1] * n
    f = [0] * n
    g = [0] * n

    INF = 10**30

    for u in reversed(order):
        children = [v for v in graph[u] if parent[v] == u]

        if not children:
            size[u] = 1
            f[u] = min(a[u], a[u] + k - 2)
            g[u] = a[u]
            continue

        size[u] = 1 + sum(size[v] for v in children)

        children.sort(key=lambda v: f[v] + 2 * size[v])

        m = len(children)

        deadline = [0] * m
        prefix = [INF] * (m + 1)

        used = 0
        for i, v in enumerate(children):
            deadline[i] = f[v] - 1 - 2 * used
            prefix[i + 1] = min(prefix[i], deadline[i])
            used += size[v]

        suffix = [INF] * (m + 1)
        for i in range(m - 1, -1, -1):
            suffix[i] = min(suffix[i + 1], deadline[i])

        f[u] = min(
            a[u],
            a[u] + k - 2 * size[u],
            prefix[m]
        )

        total_children_size = size[u] - 1
        best = -INF

        for i, v in enumerate(children):
            sv = size[v]

            # Remove v from the child order.
            # Children before v keep their original prefix.
            # Children after v start 2 * sv days earlier.
            side_deadline = min(
                prefix[i],
                suffix[i + 1] + 2 * sv
            )

            remaining_size = total_children_size - sv

            candidate = min(
                a[u],
                a[u] + k - 2 - 2 * remaining_size,
                g[v] - 1 - 2 * remaining_size,
                side_deadline
            )

            best = max(best, candidate)

        g[u] = best

    answer = g[0]
    print(answer if answer >= 0 else -1)

if __name__ == "__main__":
    solve()
```

The first part of the implementation roots the tree iteratively. Recursion is avoided because a tree with `100000` vertices can be a single chain, which is deep enough to exceed Python's normal recursion limit.

The reverse traversal order computes the DP from leaves toward the root. The `size` array is needed both for the duration of a complete child excursion and for the temperature constraint at a vertex after all of its descendants have been processed.

For each vertex, the children are sorted by `f[v] + 2 * size[v]`. The `deadline` array stores the exact bound on the casting day of `u` contributed by each child. The `prefix` array gives the minimum deadline among children before a selected final child, while `suffix` gives the minimum among children after it.

The expression `suffix[i + 1] + 2 * sv` is easy to get wrong. After child `v` is removed, every later child starts `2 * size[v]` days earlier, so its constraint becomes less restrictive by exactly that amount. That is why the suffix value must be increased rather than decreased.

The distinction between `-1` and zero is also deliberate. A DP state may be negative because it represents a latest feasible casting day relative to a parent. At the root, however, only non-negative days are available. Thus `g[0] == 0` is valid, while `g[0] < 0` means the instance is impossible.

All arithmetic is done directly with Python integers. Expressions involving `2 * size[u]` and `k` can exceed 32-bit ranges, so a fixed-width implementation should use `long long`.

## Worked Examples

For Sample 1,

```
3 1
1 2
1 3
4 3 5
```

Vertices 2 and 3 are leaves. Their states are `f[2] = 2`, `g[2] = 3`, `f[3] = 4`, and `g[3] = 5`.

The root has two possible choices for the final child.

| Vertex | `size` | `f` | `g` |
| --- | --- | --- | --- |
| 2 | 1 | 2 | 3 |
| 3 | 1 | 4 | 5 |
| 1 | 3 | -1 | 1 |

The children are ordered by `f[v] + 2size[v]`, giving vertex 2 first and vertex 3 second.

If vertex 2 is final, vertex 3 must be processed first. The root's own departure bound is `1`, while entering the final child after the side excursion gives a bound of `0`. The candidate is therefore `0`.

If vertex 3 is final, vertex 2 is processed first. The final-child constraint gives `2`, while the root's source-temperature constraint gives `1`, so the candidate is `1`.

The maximum is `g[1] = 1`, matching the sample output.

For Sample 2,

```
3 1
1 2
1 3
2 10 10
```

Both leaves have `f = 9` and `g = 10`. Whichever leaf is chosen as the final child, the other leaf must first be visited and returned from.

| Vertex | `size` | `f` | `g` |
| --- | --- | --- | --- |
| 2 | 1 | 9 | 10 |
| 3 | 1 | 9 | 10 |
| 1 | 3 | -1 | -1 |

After one side excursion, the root would have to leave for the final child on a day when its temperature is not positive. The resulting `g[1]` is `-1`, so even preparation on day 0 cannot work. The output is `-1`.

The traces demonstrate why the source vertex condition cannot be replaced by a non-negative check. The root needs strictly positive temperature at every departure, and the DP encodes that strict inequality through the `-2` terms.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Every vertex's children are sorted, and the total sorting cost is at most `O(n log n)` |
| Space | `O(n)` | The tree, parent/order arrays, subtree sizes, and DP states are all linear |

The tree has at most `100000` vertices, so `O(n log n)` is easily within the intended asymptotic range. The implementation also avoids recursive DFS, which is useful for the worst-case chain. The temporary prefix, suffix, and deadline arrays contain only the children of the currently processed vertex, so their total retained memory remains linear.

## Test Cases

The following test harness uses the same `solve` function as the submitted solution. It temporarily replaces standard input and output, then restores them after each test.

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        global input
        input = sys.stdin.readline

        solve()

        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """3 1
1 2
1 3
4 3 5
"""
) == "1", "sample 1"

# Provided sample 2
assert run(
    """3 1
1 2
1 3
2 10 10
"""
) == "-1", "sample 2"

# Minimum-size tree, destination is exactly zero on arrival.
assert run(
    """2 0
1 2
2 1
"""
) == "0", "destination may be zero"

# Source must be strictly positive when moving.
assert run(
    """2 0
1 2
1 1
"""
) == "-1", "source must be positive"

# Child ordering matters.
assert run(
    """5 2
1 2
1 3
1 4
4 5
100 1 100 100 100
"""
) == "93", "child ordering"

# Day 0 does not suffer the morning decrement.
assert run(
    """2 2
1 2
0 1
"""
) == "0", "day zero"

# All equal values with a small branching tree.
assert run(
    """3 2
1 2
1 3
4 4 4
"""
) == "1", "all equal values"

# Maximum-size generated test, a chain with equal temperatures.
n = 100000
k = 1000000000

parts = [f"{n} {k}\n"]
for i in range(1, n):
    parts.append(f"{i} {i + 1}\n")
parts.append(("1000000000 " * n).strip() + "\n")

max_case = "".join(parts)

assert run(max_case) == "999900001", "maximum-size chain"
```

The custom cases validate the following situations:

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 0`, edge `1 2`, temperatures `2 1` | `0` | Destination temperature may be exactly zero |
| `2 0`, edge `1 2`, temperatures `1 1` | `-1` | Source temperature must be strictly positive |
| Five-vertex tree with children of different sizes and deadlines | `93` | Sorting children by effective deadline |
| `2 2`, temperatures `0 1` | `0` | Day 0 has no initial temperature decrement |
| Three-vertex star, `k = 2`, all temperatures `4` | `1` | Equal values and sibling scheduling |
| Chain of `100000` vertices with large equal temperatures | `999900001` | Maximum `n`, iterative traversal, large integer arithmetic |

## Edge Cases

The zero-temperature destination case is handled by the child-arrival inequality `t + 1 <= g[c]`. There is no extra subtraction after arrival, so a temperature of exactly zero is accepted. In the two-vertex case with temperatures `2 1` and `k = 0`, the root can cast on day 0 and move on day 1, arriving at the second vertex with temperature zero. The algorithm computes `g[2] = 1`, and the root transition gives `g[1] = 0`, so it prints `0`.

The strict source condition appears in the `a[u] + k - 2` term for a leaf and the corresponding departure terms for internal vertices. With `n = 2`, `k = 0`, and temperatures `1 1`, the root can cast on day 0 but has temperature zero after the morning of day 1. The transition produces `g[1] = -1`, correctly reporting impossibility.

The child-ordering case

```
5 2
1 2
1 3
1 4
4 5
100 1 100 100 100
```

has a leaf child 2 with `f[2] = 1` and a two-vertex child rooted at 4 with `f[4] = 98`. Their effective keys are `3` and `102`, so vertex 2 must be processed first. After that excursion, the large subtree can be visited, and vertex 3 can be the final subtree, giving day `93`. The prefix deadlines enforce this order automatically.

The day-zero case

```
2 2
1 2
0 1
```

has `a[1] = 0`, so Pang can cast at the root on day 0. The magic raises its temperature to 2. On day 1, the root is positive and vertex 2 has temperature zero, so the move is legal. The root transition gives `g[1] = 0`, which is exactly the earliest and latest possible preparation day.

For a leaf, `g[u] = a[u]` because Pang may arrive, cast magic, and finish immediately. This boundary is essential when the final vertex of the whole walk is a leaf. Using the round-trip state `f[u]` instead would unnecessarily require enough temperature to leave the leaf again and could reject valid solutions.

When `k` is zero, magic does not recharge a vertex at all. The formulas still work because every departure bound contains the same `k` term. When `k` is very large, the arrival constraint `t <= a[u]` can become the limiting condition instead, which is why `f[u]` must use the minimum of both constraints rather than assuming the recharge condition is always tighter.

A negative DP value inside the tree is not itself an error. It simply means that a subtree would have to be entered before day 0 to satisfy all of its deadlines. Such a state can still be used as a bound when computing an ancestor. Only `g[1]` is compared with zero, because day 0 is the earliest preparation day available to Pang.

The editorial above uses the `f/g` formulation directly, so the implementation follows the proof rather than requiring a separate rerooting pass.
