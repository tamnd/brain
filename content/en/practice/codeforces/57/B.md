---
title: "CF 57B - Martian Architecture"
description: "Each construction describes a staircase placed on a one-dimensional line of cells. A staircase starts at cell l, ends at cell r, and adds heights in an arithmetic progression."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 57
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 53"
rating: 1600
weight: 57
solve_time_s: 97
verified: true
draft: false
---

[CF 57B - Martian Architecture](https://codeforces.com/problemset/problem/57/B)

**Rating:** 1600  
**Tags:** implementation  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

Each construction describes a staircase placed on a one-dimensional line of cells. A staircase starts at cell `l`, ends at cell `r`, and adds heights in an arithmetic progression. If the starting height is `x`, then the added stones are:

`x` at `l`

`x + 1` at `l + 1`

`x + 2` at `l + 2`

and so on until `x + (r - l)` at `r`.

Several staircases may overlap, and their contributions accumulate.

We are not asked to reconstruct the whole road. Instead, only `k` specific cells matter. We need the total number of stones present in those queried cells after all staircases are applied.

The input gives:

- the number of cells,
- the list of staircase constructions,
- the set of interesting cells whose final stone counts must be summed.

The largest values are around `10^5`, which immediately rules out anything quadratic. A direct simulation that updates every affected cell for every staircase may perform around `10^10` operations in the worst case, far beyond a 2 second limit.

The interesting detail is that `k ≤ 100`. Only a small number of cells are queried. That changes the direction completely. Instead of updating every cell touched by every staircase, we can process only the queried positions.

A few edge cases are easy to mishandle.

Suppose a staircase starts before a queried cell and ends after it.

```
5 1 1
1 5 3
4
```

The queried cell is `4`. The staircase contributes:

`3 4 5 6 7`

Cell `4` receives `6`, not `3` and not `7`. A careless implementation that only stores the starting value would fail to account for the offset from the staircase start.

Another subtle case appears when queried cells are outside the staircase interval.

```
5 1 2
2 4 1
1 5
```

The staircase affects only cells `2,3,4`. The correct answer is `0`. Off-by-one mistakes in interval checks often incorrectly include boundary cells.

Overlapping staircases also matter.

```
5 2 1
1 3 1
2 5 2
3
```

The first staircase contributes `3` to cell `3`.

The second staircase contributes `3` to cell `3`.

The final value is `6`.

A naive overwrite instead of accumulation gives the wrong result.

Finally, the answer may exceed 32-bit integer range. Even though each staircase starts with at most `1000`, there can be `10^5` staircases. The implementation must use 64-bit arithmetic.

## Approaches

The most direct solution builds the entire road explicitly.

For every staircase `(l, r, x)`, we iterate through all affected cells and add the proper arithmetic progression value:

```
cell l     += x
cell l + 1 += x + 1
cell l + 2 += x + 2
...
```

After processing all staircases, we sum the queried cells.

This works logically because every staircase contribution is applied exactly once to every covered position. The problem is cost. A single staircase may cover `10^5` cells, and there may be `10^5` staircases. That leads to roughly `10^10` updates in the worst case.

The key observation is that we never need the values of all cells. Only at most `100` positions matter.

Instead of iterating through all cells inside a staircase, we can iterate through all queried positions and check whether the staircase affects them.

Suppose we process a queried cell `p`.

A staircase `(l, r, x)` contributes to `p` only if:

```
l ≤ p ≤ r
```

If the staircase covers `p`, then the added value is:

```
x + (p - l)
```

because each step to the right increases the height by one.

Now the total work becomes:

```
m × k
```

Since `m ≤ 100000` and `k ≤ 100`, the maximum is only `10^7` checks, which is completely acceptable in Python.

The brute-force works because it literally simulates every added stone. The optimized solution works because the query set is tiny, so checking only relevant positions is much cheaper than constructing the whole road.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal | O(mk) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read all queried positions and store them in a list.

Since only these positions matter, no other cells need to be tracked.
2. Create an array `ans` of length `k`.

`ans[i]` will store the total stones accumulated at the `i-th` queried position.
3. Process each staircase `(l, r, x)` one by one.

Every staircase is independent, so we can immediately add its contribution to all relevant queried cells.
4. For every queried position `p`:

Check whether `l ≤ p ≤ r`.

If false, this staircase contributes nothing to `p`.
5. If the staircase covers `p`, add:

```
x + (p - l)
```

to the corresponding answer entry.

The term `(p - l)` represents how many steps to the right the queried cell is from the staircase start.
6. After all staircases are processed, sum all entries of `ans`.

This gives the total number of stones across all queried cells.

### Why it works

For every staircase and every queried position, the algorithm considers exactly one of two possibilities.

If the queried cell lies outside the staircase interval, the staircase contributes nothing.

If the queried cell lies inside the interval, the staircase contributes exactly the arithmetic progression value corresponding to its distance from the start cell.

Because every staircase contribution is added independently and accumulation is linear, the final stored value for each queried cell equals the true total number of stones in that cell. Summing those values produces the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    roads = [tuple(map(int, input().split())) for _ in range(m)]
    queries = list(map(int, input().split()))

    ans = [0] * k

    for l, r, x in roads:
        for i in range(k):
            p = queries[i]

            if l <= p <= r:
                ans[i] += x + (p - l)

    print(sum(ans))

solve()
```

The solution keeps only the queried positions instead of building an array of size `n`.

The outer loop iterates through staircases. The inner loop checks all queried cells. Since `k` is at most `100`, this remains efficient even when `m` reaches `100000`.

The expression:

```
x + (p - l)
```

is the core of the solution. If the staircase starts at `l` with height `x`, then moving one cell to the right increases the added stones by one. A queried position `p` is exactly `p - l` steps away from the start.

The interval check:

```
if l <= p <= r:
```

is critical. Forgetting either boundary creates incorrect contributions at the edges.

The final answer is the sum of all queried cell values, not the individual values themselves. The problem asks for one combined total.

Python integers automatically handle large values, so overflow is not an issue.

## Worked Examples

### Example 1

Input:

```
5 2 1
1 5 1
2 4 1
3
```

Queried cell is `3`.

| Staircase | Covers 3? | Contribution to 3 | Running Total |
| --- | --- | --- | --- |
| (1, 5, 1) | Yes | 1 + (3 - 1) = 3 | 3 |
| (2, 4, 1) | Yes | 1 + (3 - 2) = 2 | 5 |

Final answer:

```
5
```

This trace shows how overlapping staircases accumulate independently.

### Example 2

Input:

```
6 3 2
1 3 2
2 5 1
4 6 3
2 5
```

Queried cells are `2` and `5`.

| Staircase | Query Cell | Covers? | Contribution | Running Value |
| --- | --- | --- | --- | --- |
| (1, 3, 2) | 2 | Yes | 3 | 3 |
| (1, 3, 2) | 5 | No | 0 | 0 |
| (2, 5, 1) | 2 | Yes | 1 | 4 |
| (2, 5, 1) | 5 | Yes | 4 | 4 |
| (4, 6, 3) | 2 | No | 0 | 4 |
| (4, 6, 3) | 5 | Yes | 4 | 8 |

Final queried values are:

```
cell 2 = 4
cell 5 = 8
```

Total answer:

```
12
```

This example demonstrates both uncovered cells and arithmetic progression growth inside intervals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(mk) | Each staircase checks all queried positions |
| Space | O(k) | Only queried cell totals are stored |

With `m ≤ 100000` and `k ≤ 100`, the total number of iterations is at most `10^7`. That comfortably fits within the time limit in Python. Memory usage is tiny because the algorithm stores only the queried cells instead of the entire road.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, m, k = map(int, input().split())

        roads = [tuple(map(int, input().split())) for _ in range(m)]
        queries = list(map(int, input().split()))

        ans = [0] * k

        for l, r, x in roads:
            for i in range(k):
                p = queries[i]

                if l <= p <= r:
                    ans[i] += x + (p - l)

        return str(sum(ans))

    return solve()

# provided sample
assert run(
"""5 2 1
1 5 1
2 4 1
3
"""
) == "5", "sample 1"

# minimum-size input
assert run(
"""1 1 1
1 1 7
1
"""
) == "7", "minimum case"

# queried cells outside all ranges
assert run(
"""5 1 2
2 4 3
1 5
"""
) == "0", "outside intervals"

# overlapping staircases
assert run(
"""5 2 1
1 3 1
2 5 2
3
"""
) == "6", "overlap accumulation"

# boundary check
assert run(
"""5 1 2
2 4 1
2 4
"""
) == "4", "inclusive boundaries"

# large arithmetic progression
assert run(
"""10 1 1
1 10 5
10
"""
) == "14", "progression growth"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single cell and single staircase | 7 | Minimum constraints |
| Queries outside intervals | 0 | Correct interval exclusion |
| Two overlapping staircases | 6 | Proper accumulation |
| Query exactly at interval boundaries | 4 | Inclusive endpoints |
| Query at far end of staircase | 14 | Correct arithmetic progression offset |

## Edge Cases

Consider a queried cell inside a staircase but far from its start.

```
5 1 1
1 5 3
4
```

The staircase adds:

```
3 4 5 6 7
```

When processing query `4`, the algorithm computes:

```
3 + (4 - 1) = 6
```

which matches the true contribution. This confirms the offset formula is correct.

Now consider queried cells completely outside all staircases.

```
5 1 2
2 4 1
1 5
```

For query `1`, the condition `2 ≤ 1 ≤ 4` fails.

For query `5`, the condition `2 ≤ 5 ≤ 4` also fails.

No contribution is added, so both queried cells remain zero and the final answer is `0`.

Overlapping staircases are another common source of bugs.

```
5 2 1
1 3 1
2 5 2
3
```

The first staircase contributes:

```
1 + (3 - 1) = 3
```

The second contributes:

```
2 + (3 - 2) = 3
```

The algorithm adds both values into the same accumulator:

```
3 + 3 = 6
```

which matches the expected result.

Finally, consider interval boundaries.

```
5 1 2
2 4 1
2 4
```

At query `2`, the contribution is:

```
1 + (2 - 2) = 1
```

At query `4`, the contribution is:

```
1 + (4 - 2) = 3
```

The final answer is `4`.

This confirms the interval check is inclusive on both ends.
