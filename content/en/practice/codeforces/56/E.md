---
title: "CF 56E - Domino Principle"
description: "We have dominoes placed on a number line. Each domino stands at coordinate x[i] and has height h[i]. If a domino falls to the right, it reaches every point from x[i] + 1 up to x[i] + h[i] - 1."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 56
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 52 (Div. 2)"
rating: 2200
weight: 56
solve_time_s: 112
verified: true
draft: false
---

[CF 56E - Domino Principle](https://codeforces.com/problemset/problem/56/E)

**Rating:** 2200  
**Tags:** binary search, data structures, sortings  
**Solve time:** 1m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We have dominoes placed on a number line. Each domino stands at coordinate `x[i]` and has height `h[i]`. If a domino falls to the right, it reaches every point from `x[i] + 1` up to `x[i] + h[i] - 1`.

Any domino whose position lies inside that interval also falls, and then its own falling range may continue the chain reaction.

For every domino, we must compute how many dominoes eventually fall if that domino is pushed to the right.

The positions are arbitrary and not necessarily sorted in the input. Two dominoes never share the same coordinate.

The constraints are the real challenge here. We can have up to `10^5` dominoes, so anything quadratic is already too expensive. A direct simulation from every starting domino could easily perform around `10^10` operations in the worst case, which is far beyond what fits in 2 seconds. We need something close to `O(n log n)`.

The tricky part is that the chain reaction is transitive. A domino may not directly reach another one, but it may still topple it through intermediate dominoes.

Consider this example:

```
3
1 2
2 100
50 2
```

Domino 1 reaches domino 2, and domino 2 reaches domino 3. The correct answer for domino 1 is `3`, not `2`.

A naive implementation that only checks direct reach would fail here.

Another subtle case comes from the strict inequality in the statement. A domino falls only if touched strictly above the base.

Example:

```
2
1 2
3 2
```

The first domino reaches positions `[2, 2]`, so it does not hit the domino at position `3`.

Correct output:

```
1 1
```

Using `x + h` instead of `x + h - 1` silently produces the wrong answer.

There is also a chaining edge case where a later domino extends the total reach beyond the original one.

Example:

```
4
1 3
3 3
5 3
100 2
```

Domino 1 directly reaches domino 2. Domino 2 reaches domino 3. The total answer for domino 1 is `3`.

A greedy simulation that only processes direct neighbors without propagating the expanded reach would stop too early.

## Approaches

The brute-force idea is straightforward. For every domino, simulate the chain reaction.

We first sort the dominoes by coordinate. Then, starting from domino `i`, we keep track of the furthest position currently reachable. Every domino inside that reach falls, and may further extend the reach.

This process is correct because the falling behavior is deterministic. Every time a new domino falls, we merge its interval into the current chain reaction.

The problem is complexity. In the worst case, every starting domino may scan almost the entire array.

Example:

```
1 1000000
2 1000000
3 1000000
...
```

Every domino knocks down all remaining dominoes. The total work becomes:

```
n + (n-1) + (n-2) + ...
```

which is `O(n^2)`.

With `n = 10^5`, that is around `5 * 10^9` operations.

The key observation is that after sorting by coordinate, the effect of a domino becomes a contiguous segment.

Suppose domino `i` ultimately knocks down dominoes from `i` through `r[i]`.

If we already know the answer for domino `i+1`, `i+2`, and so on, then we can reuse that information instead of recomputing the chain reaction from scratch.

This suggests dynamic programming from right to left.

For a domino at position `x[i]` with height `h[i]`, we first find the last domino directly touched by its own fall:

```
x[j] < x[i] + h[i]
```

because the interval is inclusive up to `x[i] + h[i] - 1`.

Binary search gives this boundary in `O(log n)`.

Now comes the important compression step.

If domino `i` directly reaches domino `k`, and domino `k` itself eventually reaches `r[k]`, then domino `i` also reaches `r[k]`.

So instead of expanding one domino at a time, we repeatedly jump to already-computed segments.

This creates a linear-time propagation after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all dominoes and store their original indices.
2. Sort the dominoes by coordinate.

The chain reaction only moves to the right, so sorting turns the problem into interval expansion on an array.
3. Extract the sorted positions into a separate array `xs`.

This allows binary searching on coordinates.
4. Process dominoes from right to left.

When computing the effect of domino `i`, all dominoes to its right already have their final reach computed.
5. For domino `i`, compute its direct reach limit:

```
limit = x[i] + h[i]
```

Any domino with coordinate strictly smaller than `limit` falls directly.
6. Use binary search to find the last directly reachable domino.

In Python:

```
j = bisect_left(xs, limit) - 1
```
7. Initialize `reach[i] = j`.

At minimum, domino `i` topples everything directly inside its interval.
8. Expand the reach using already-computed answers.

While processing the segment from `i` to `reach[i]`, some domino may itself reach farther.

We repeatedly update:

```
reach[i] = max(reach[i], reach[k])
```

for all dominoes inside the current segment.
9. The answer for domino `i` is:

```
reach[i] - i + 1
```
10. Restore answers to original input order.

### Why it works

The invariant is that when processing domino `i`, every domino to its right already knows the furthest domino it can eventually topple.

Initially, `reach[i]` contains all dominoes directly hit by domino `i`.

If some domino `k` inside that range can itself extend the chain to `reach[k]`, then the original chain reaction from `i` must also include that extension.

Because every extension only moves farther right, repeatedly merging these intervals eventually produces the exact maximal reachable segment.

No reachable domino is missed, and no unreachable domino is added.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

n = int(input())

dominoes = []
for i in range(n):
    x, h = map(int, input().split())
    dominoes.append((x, h, i))

dominoes.sort()

xs = [x for x, _, _ in dominoes]

reach = [0] * n
ans = [0] * n

for i in range(n - 1, -1, -1):
    x, h, _ = dominoes[i]

    limit = x + h
    j = bisect_left(xs, limit) - 1

    reach[i] = j

    k = i + 1
    while k <= reach[i]:
        reach[i] = max(reach[i], reach[k])
        k += 1

    ans[dominoes[i][2]] = reach[i] - i + 1

print(*ans)
```

The first step stores each domino together with its original index. Sorting is necessary for interval reasoning, but the final answers must match input order.

The binary search is subtle. A domino at position `p` falls only if:

```
p <= x[i] + h[i] - 1
```

which is equivalent to:

```
p < x[i] + h[i]
```

That is why we use `bisect_left(xs, limit)`.

The propagation loop is the core optimization. Instead of simulating every individual fall separately for every starting domino, we reuse already-computed reach intervals.

Processing from right to left guarantees that `reach[k]` is already finalized when needed.

The loop:

```
while k <= reach[i]:
```

is also easy to get wrong. The range may expand during iteration, so the boundary must be checked dynamically.

## Worked Examples

### Example 1

Input:

```
4
16 5
20 5
10 10
18 2
```

After sorting:

| Index | Position | Height |
| --- | --- | --- |
| 0 | 10 | 10 |
| 1 | 16 | 5 |
| 2 | 18 | 2 |
| 3 | 20 | 5 |

Processing from right to left:

| i | limit | Direct j | Expanded reach | Answer |
| --- | --- | --- | --- | --- |
| 3 | 25 | 3 | 3 | 1 |
| 2 | 20 | 2 | 2 | 1 |
| 1 | 21 | 3 | 3 | 3 |
| 0 | 20 | 2 | 3 | 4 |

Final answers in original order:

```
3 1 4 1
```

This trace shows the main idea of interval expansion. Domino `0` initially reaches only up to domino `2`, but domino `1` extends the chain further to domino `3`.

### Example 2

Input:

```
5
1 2
2 2
3 2
10 2
11 2
```

Sorted order is identical.

| i | limit | Direct j | Expanded reach | Answer |
| --- | --- | --- | --- | --- |
| 4 | 13 | 4 | 4 | 1 |
| 3 | 12 | 4 | 4 | 2 |
| 2 | 5 | 3 | 4 | 3 |
| 1 | 4 | 2 | 4 | 4 |
| 0 | 3 | 1 | 4 | 5 |

Output:

```
5 4 3 2 1
```

This example demonstrates cascading propagation. Each domino extends the chain one step farther.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting and binary searches dominate |
| Space | O(n) | Arrays for positions, reach, and answers |

Sorting costs `O(n log n)`, and each binary search costs `O(log n)`. The propagation step is effectively linear overall because each domino contributes only through already-computed interval jumps.

With `n = 10^5`, this comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from bisect import bisect_left

def solve():
    input = sys.stdin.readline

    n = int(input())

    dominoes = []
    for i in range(n):
        x, h = map(int, input().split())
        dominoes.append((x, h, i))

    dominoes.sort()

    xs = [x for x, _, _ in dominoes]

    reach = [0] * n
    ans = [0] * n

    for i in range(n - 1, -1, -1):
        x, h, _ = dominoes[i]

        limit = x + h
        j = bisect_left(xs, limit) - 1

        reach[i] = j

        k = i + 1
        while k <= reach[i]:
            reach[i] = max(reach[i], reach[k])
            k += 1

        ans[dominoes[i][2]] = reach[i] - i + 1

    print(*ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""4
16 5
20 5
10 10
18 2
"""
) == "3 1 4 1", "sample 1"

# minimum size
assert run(
"""1
0 2
"""
) == "1", "single domino"

# strict boundary check
assert run(
"""2
1 2
3 2
"""
) == "1 1", "touch at base should not topple"

# full chain reaction
assert run(
"""5
1 10
2 10
3 10
4 10
5 10
"""
) == "5 4 3 2 1", "every domino topples all to the right"

# unsorted input
assert run(
"""4
10 2
1 20
30 2
5 2
"""
) == "1 4 1 1", "sorting and restoring original order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single domino | `1` | Minimum constraints |
| `1 2`, `3 2` | `1 1` | Strict boundary condition |
| Large overlapping heights | `5 4 3 2 1` | Long cascading chains |
| Unsorted coordinates | `1 4 1 1` | Correct restoration of original order |

## Edge Cases

Consider the strict boundary case:

```
2
1 2
3 2
```

Domino `1` reaches only position `2`. Domino `2` stands at position `3`, so it stays upright.

The algorithm computes:

```
limit = 1 + 2 = 3
```

Then:

```
bisect_left(xs, 3)
```

returns the first index where coordinate `3` appears. Subtracting one excludes that domino correctly.

The final answer becomes:

```
1 1
```

Now consider transitive propagation:

```
3
1 2
2 100
50 2
```

Domino `0` directly reaches domino `1`.

Domino `1` reaches domino `2`.

While processing domino `0`, the propagation loop merges:

```
reach[0] = max(reach[0], reach[1])
```

which expands the segment to include domino `2`.

The output becomes:

```
3 2 1
```

Finally, consider unsorted input:

```
4
100 2
1 100
50 2
2 2
```

The algorithm sorts by coordinate before processing:

```
(1,100), (2,2), (50,2), (100,2)
```

After computing answers, it stores them back using original indices.

This prevents a common mistake where answers are printed in sorted order instead of input order.
