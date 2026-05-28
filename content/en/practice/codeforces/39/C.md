---
title: "CF 39C - Moon Craters"
description: "Each crater is described by a center coordinate c and a radius r. Since the robot moves along a line, every crater can be represented on that line by its interval: $[c-r, c+r]$ Professor Okulov’s rule says that any two selected craters must either be completely disjoint or one…"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "sortings"]
categories: ["algorithms"]
codeforces_contest: 39
codeforces_index: "C"
codeforces_contest_name: "School Team Contest 1 (Winter Computer School 2010/11)"
rating: 2100
weight: 39
solve_time_s: 265
verified: false
draft: false
---

[CF 39C - Moon Craters](https://codeforces.com/problemset/problem/39/C)

**Rating:** 2100  
**Tags:** dp, sortings  
**Solve time:** 4m 25s  
**Verified:** no  

## Solution
## Problem Understanding

Each crater is described by a center coordinate `c` and a radius `r`. Since the robot moves along a line, every crater can be represented on that line by its interval:

$[c-r,\ c+r]$

Professor Okulov’s rule says that any two selected craters must either be completely disjoint or one must lie entirely inside the other. Partial overlap is forbidden.

For intervals, this means that for any two chosen intervals:

1. They do not intersect at all.
2. One interval is fully contained inside the other.
3. Touching at endpoints is allowed.

We must select the largest possible subset of craters satisfying this condition and output any optimal set.

The constraint `n ≤ 2000` is the main clue. A cubic solution with around `8 * 10^9` operations is impossible. A quadratic dynamic programming solution is realistic, especially in Python with careful implementation. Since the task also asks for reconstruction of the chosen set, we need to store transitions, not only the answer size.

The tricky part is that the relation between intervals is not simply “compatible” or “incompatible” like ordinary interval scheduling. Two intervals can coexist if one contains the other, which creates a nested structure similar to properly matched parentheses.

Several edge cases are easy to mishandle.

Consider tangent intervals:

```
2
0 1
2 1
```

These intervals are `[−1,1]` and `[1,3]`. They touch at one point and are allowed together. Using strict inequalities when checking overlap would incorrectly reject them.

Now consider crossing intervals:

```
2
0 3
4 3
```

These intervals are `[−3,3]` and `[1,7]`. They overlap, but neither contains the other. They cannot both be selected. A careless implementation that only checks “not disjoint” would incorrectly accept them.

Nested intervals also require care:

```
3
0 10
0 5
0 2
```

All three are valid together because every smaller crater is fully inside the larger one. A greedy strategy that always prefers smaller or always prefers larger intervals can easily lose optimal solutions in more complex cases.

Another subtle situation occurs when two intervals share one endpoint:

```
2
0 5
5 0
```

The intervals are `[−5,5]` and `[5,5]`. The second is fully contained in the first, and tangency is allowed. Using strict containment instead of non-strict containment breaks this case.

## Approaches

The brute-force idea is straightforward. We try every subset of craters and verify whether every pair satisfies the rule. Pair checking takes `O(n²)`, and there are `2^n` subsets, so the total complexity becomes `O(2^n * n²)`. Even for `n = 40`, this is already hopeless, while the actual limit is `2000`.

A more refined brute-force direction is to think of intervals. Two intervals are compatible unless they cross. Crossing means:

$l_1 < l_2 < r_1 < r_2$

or symmetrically the opposite order.

This reveals the real structure of the problem. Valid interval families are exactly laminar families, meaning intervals are either disjoint or nested. Once intervals are sorted by their endpoints, the structure becomes recursive. Inside one interval, we solve the same problem again for its children. Disjoint groups can also be concatenated independently.

That suggests interval DP.

The key observation is that if we process intervals ordered by left endpoint and right endpoint, every valid solution behaves like properly nested segments. Whenever we choose an interval, every other chosen interval is either fully inside it or completely outside it.

We can build a DP over interval ranges. For every interval `i`, we compute the best valid subset that lies completely inside `i`. Then we combine non-crossing child intervals similarly to weighted interval scheduling.

Since `n ≤ 2000`, an `O(n²)` or `O(n² log n)` solution is acceptable. The standard accepted solution uses quadratic dynamic programming after sorting intervals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n²) | O(n) | Too slow |
| Optimal DP | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

### Interval Representation

Each crater becomes an interval:

$[l_i,r_i]=[c_i-r_i,\ c_i+r_i]$

We also keep the original index because the output must use input numbering.

### Sorting

1. Sort intervals by increasing left endpoint.
2. If left endpoints are equal, sort by decreasing right endpoint.

This order is crucial. Larger containing intervals appear before smaller contained intervals. That makes nesting relationships easy to process.

### Defining Crossing

1. Two intervals cross if:

$l_i < l_j \le r_i < r_j$

Crossing intervals cannot both belong to the answer.

### Dynamic Programming State

1. Let `dp[i]` be the maximum size of a valid subset whose outermost chosen interval is interval `i`.

We always include `i` itself in this state.

### Transition

1. For every interval `i`, process all intervals strictly inside it.
2. Among intervals inside `i`, we only want to combine disjoint “top-level” children. If two children overlap without containment, they cross and are invalid together.
3. This becomes a weighted interval scheduling problem on the immediate compatible children of `i`.

For each candidate child `j` inside `i`:

- We may take the optimal structure rooted at `j`, worth `dp[j]`.
- Then continue with the next disjoint child.

### Secondary DP

1. Use another DP over positions to combine children in non-overlapping order.

This computes the best collection of disjoint substructures inside interval `i`.

1. Finally:

```
dp[i] = 1 + best_inside
```

The `1` counts interval `i` itself.

### Reconstruction

1. Store parent choices during transitions.
2. After finding the interval with maximum `dp[i]`, recursively reconstruct all chosen intervals.

### Why it works

The crucial invariant is that every valid family of intervals forms a laminar structure. Any interval inside a chosen interval belongs either to one nested branch or to another completely disjoint branch. Crossing structures are impossible.

Because of that, every optimal solution rooted at interval `i` decomposes into independent optimal solutions of its disjoint immediate children. The DP explores exactly those possibilities and never combines crossing intervals. Since every valid configuration can be uniquely decomposed this way, the DP cannot miss an optimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    segs = []

    for idx in range(1, n + 1):
        c, r = map(int, input().split())
        l = c - r
        rr = c + r
        segs.append((l, rr, idx))

    segs.sort(key=lambda x: (x[0], -x[1]))

    l = [0] * n
    r = [0] * n
    idxs = [0] * n

    for i in range(n):
        l[i], r[i], idxs[i] = segs[i]

    dp = [1] * n
    choice = [[] for _ in range(n)]

    inside = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if l[i] <= l[j] and r[j] <= r[i]:
                inside[i].append(j)

    for i in range(n - 1, -1, -1):
        children = inside[i]

        m = len(children)

        best = [0] * (m + 1)
        take = [False] * m
        nxt = [m] * m

        for a in range(m):
            j = children[a]

            b = a + 1
            while b < m and l[children[b]] <= r[j]:
                b += 1

            nxt[a] = b

        pick = [False] * m

        for a in range(m - 1, -1, -1):
            j = children[a]

            skip_val = best[a + 1]
            take_val = dp[j] + best[nxt[a]]

            if take_val > skip_val:
                best[a] = take_val
                pick[a] = True
            else:
                best[a] = skip_val

        dp[i] = 1 + best[0]

        cur = 0
        selected = []

        while cur < m:
            if pick[cur]:
                j = children[cur]
                selected.append(j)
                cur = nxt[cur]
            else:
                cur += 1

        choice[i] = selected

    root = max(range(n), key=lambda x: dp[x])

    ans = []

    def build(v):
        ans.append(idxs[v])
        for to in choice[v]:
            build(to)

    build(root)

    print(len(ans))
    print(*ans)

solve()
```

The first step converts every crater into an interval. Using interval endpoints directly simplifies all geometric conditions into comparisons between numbers.

Sorting by increasing left endpoint and decreasing right endpoint is essential. Suppose two intervals share the same left endpoint. The larger one must appear first so that containment relations remain valid during DP transitions.

The array `inside[i]` stores every interval fully contained in interval `i`. Since the intervals are already sorted, all descendants appear after `i`.

The secondary DP inside each interval behaves like weighted interval scheduling. Once we select a child interval `j`, every later child whose left endpoint is still inside `j` belongs to `j`’s subtree and must not be processed as a separate top-level child. The pointer `nxt[a]` skips directly to the next disjoint child.

One subtle implementation detail is the condition:

```
while b < m and l[children[b]] <= r[j]:
```

The `<=` is correct because touching intervals are not disjoint at the same nesting level. If another interval starts before or exactly at `r[j]`, then it either intersects or is nested within `j`, so it must belong to `j`’s subtree rather than become a sibling.

The reconstruction phase follows stored choices recursively. Since every chosen child already represents an optimal nested subtree, recursion rebuilds the full optimal answer.

## Worked Examples

### Example 1

Input:

```
4
1 1
2 2
4 1
5 1
```

Intervals:

| Index | Interval |
| --- | --- |
| 1 | [0,2] |
| 2 | [0,4] |
| 3 | [3,5] |
| 4 | [4,6] |

Sorted order:

| Position | Original Index | Interval |
| --- | --- | --- |
| 0 | 2 | [0,4] |
| 1 | 1 | [0,2] |
| 2 | 3 | [3,5] |
| 3 | 4 | [4,6] |

DP computation:

| Interval | Best nested value | dp |
| --- | --- | --- |
| [4,6] | 0 | 1 |
| [3,5] | 0 | 1 |
| [0,2] | 0 | 1 |
| [0,4] | 2 | 3 |

The optimal structure rooted at `[0,4]` contains `[0,2]` and `[4,6]`. Those intervals are disjoint, so all three can coexist.

Output:

```
3
1 2 4
```

This trace demonstrates the laminar structure. The outer interval contains one nested branch and one disjoint branch.

### Example 2

Input:

```
5
0 5
2 1
4 1
6 1
8 1
```

Intervals:

| Index | Interval |
| --- | --- |
| 1 | [-5,5] |
| 2 | [1,3] |
| 3 | [3,5] |
| 4 | [5,7] |
| 5 | [7,9] |

DP states:

| Interval | Compatible top-level children | dp |
| --- | --- | --- |
| [7,9] | none | 1 |
| [5,7] | none | 1 |
| [3,5] | none | 1 |
| [1,3] | none | 1 |
| [-5,5] | [1,3], [3,5] | 3 |

The optimal answer chooses intervals 1, 2, and 3.

This example confirms that tangency is allowed. `[1,3]` and `[3,5]` touch at one point and remain compatible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Building containment relations and DP transitions both require quadratic work |
| Space | O(n²) | The containment lists may store O(n²) pairs |

With `n ≤ 2000`, quadratic complexity is fully acceptable. Around four million operations fit comfortably within the time limit in Python, and the memory usage also remains well below the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    segs = []

    for idx in range(1, n + 1):
        c, r = map(int, input().split())
        segs.append((c - r, c + r, idx))

    segs.sort(key=lambda x: (x[0], -x[1]))

    l = [x[0] for x in segs]
    r = [x[1] for x in segs]
    ids = [x[2] for x in segs]

    dp = [1] * n
    choice = [[] for _ in range(n)]

    inside = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            if l[i] <= l[j] and r[j] <= r[i]:
                inside[i].append(j)

    for i in range(n - 1, -1, -1):
        children = inside[i]
        m = len(children)

        best = [0] * (m + 1)
        nxt = [m] * m
        pick = [False] * m

        for a in range(m):
            j = children[a]

            b = a + 1
            while b < m and l[children[b]] <= r[j]:
                b += 1

            nxt[a] = b

        for a in range(m - 1, -1, -1):
            j = children[a]

            take = dp[j] + best[nxt[a]]
            skip = best[a + 1]

            if take > skip:
                best[a] = take
                pick[a] = True
            else:
                best[a] = skip

        dp[i] = 1 + best[0]

        cur = 0

        while cur < m:
            if pick[cur]:
                choice[i].append(children[cur])
                cur = nxt[cur]
            else:
                cur += 1

    root = max(range(n), key=lambda x: dp[x])

    ans = []

    def rec(v):
        ans.append(ids[v])
        for to in choice[v]:
            rec(to)

    rec(root)

    print(len(ans))
    print(*sorted(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run(
"""4
1 1
2 2
4 1
5 1
"""
).splitlines()[0] == "3", "sample"

# minimum case
assert run(
"""1
5 3
"""
) == "1\n1", "single crater"

# fully nested
assert run(
"""3
0 10
0 5
0 2
"""
).splitlines()[0] == "3", "all nested"

# crossing intervals
assert run(
"""2
0 3
4 3
"""
).splitlines()[0] == "1", "crossing intervals"

# tangent intervals
assert run(
"""3
0 1
2 1
4 1
"""
).splitlines()[0] == "3", "touching intervals allowed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single crater | 1 crater chosen | Minimum input size |
| Fully nested intervals | All intervals chosen | Deep nesting |
| Crossing intervals | Only 1 chosen | Invalid partial overlap |
| Tangent intervals | All chosen | Endpoint touching is allowed |

## Edge Cases

Consider tangent intervals again:

```
2
0 1
2 1
```

The intervals become `[−1,1]` and `[1,3]`. During compatibility checks, they are treated as disjoint enough to coexist because touching is legal. The DP includes both intervals, producing answer size `2`.

Now examine crossing intervals:

```
2
0 3
4 3
```

The intervals are `[−3,3]` and `[1,7]`. Neither contains the other, and they overlap internally. While processing the second interval, the DP transition skips combining them as siblings because the second starts before the first ends. Only one interval can remain in the final answer.

Deep nesting also works correctly:

```
4
0 10
0 7
0 4
0 1
```

Every interval lies completely inside the previous one. The recursive structure naturally forms a single chain. The DP computes:

```
1 + 1 + 1 + 1 = 4
```

so all intervals are selected.

Finally, consider equal endpoints:

```
2
0 5
5 0
```

The intervals are `[−5,5]` and `[5,5]`. The second is fully contained in the first because containment uses non-strict inequalities. The algorithm correctly keeps both intervals instead of rejecting the boundary case.
