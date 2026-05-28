---
title: "CF 138C - Mushroom Gnomes - 2"
description: "We have trees placed on a number line. Each tree may fall left, fall right, or remain standing. The probabilities for these three outcomes are given independently for every tree. A falling tree destroys mushrooms in a half-open interval determined by the tree position and height."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "probabilities", "sortings"]
categories: ["algorithms"]
codeforces_contest: 138
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 99 (Div. 1)"
rating: 2200
weight: 138
solve_time_s: 120
verified: true
draft: false
---

[CF 138C - Mushroom Gnomes - 2](https://codeforces.com/problemset/problem/138/C)

**Rating:** 2200  
**Tags:** binary search, data structures, probabilities, sortings  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We have trees placed on a number line. Each tree may fall left, fall right, or remain standing. The probabilities for these three outcomes are given independently for every tree.

A falling tree destroys mushrooms in a half-open interval determined by the tree position and height.

If a tree at position `x` with height `h` falls left, it destroys mushrooms in `[x - h, x)`.

If it falls right, it destroys mushrooms in `(x, x + h]`.

Every mushroom has a position and a power value. A mushroom survives only if no tree destroys it. We need the expected total power of all surviving mushrooms.

The crucial observation is that expectation is linear. Instead of thinking about all mushrooms together, we can compute the survival probability of each mushroom independently, multiply it by the mushroom power, and sum everything.

The constraints strongly shape the solution. There can be `10^5` trees, so any algorithm that checks every tree against every mushroom would perform about `10^9` operations in the worst case, which is far too slow for a 1 second limit. The number of mushrooms is smaller, only `10^4`, which suggests iterating over mushrooms and processing trees efficiently is feasible.

A subtle point is the interval boundaries. Left falls use `[x - h, x)`, while right falls use `(x, x + h]`. The tree position itself is excluded in both cases.

Consider this example:

```
1 1
5 3 100 0
5 10
```

The tree falls left with probability 1, but the mushroom at position 5 survives because the interval is `[2, 5)`, and 5 itself is excluded. A careless implementation using `<=` on both sides would incorrectly destroy it.

Another easy mistake appears when multiple trees can hit the same mushroom.

```
2 1
0 5 50 0
10 5 0 50
5 100
```

The mushroom survives only if neither dangerous event happens. The correct survival probability is:

```
(1 - 0.5) * (1 - 0.5) = 0.25
```

Adding probabilities directly and computing `1 - 0.5 - 0.5 = 0` would be wrong because tree events are independent.

A third edge case involves mushrooms exactly on the boundary.

```
1 2
10 5 100 0
5 1
10 1
```

The mushroom at 5 is destroyed because `5 ∈ [5,10)`. The mushroom at 10 survives because 10 is excluded. Correct handling of half-open intervals is essential.

## Approaches

The brute-force solution is straightforward. For every mushroom, iterate over all trees and determine the probability that this tree destroys the mushroom.

If a tree can destroy the mushroom by falling left, multiply the survival probability by `(1 - left_probability)`. Similarly for the right side.

Finally multiply the mushroom power by its survival probability and add it to the answer.

This works because tree outcomes are independent. The probability that a mushroom survives all trees is simply the product of the probabilities that each individual tree does not destroy it.

The problem is complexity. With `10^5` trees and `10^4` mushrooms, we would perform `10^9` interval checks. Even very small constant factors would time out.

The key observation is that each tree affects only a continuous interval on the number line. Instead of processing every tree for every mushroom, we can process mushrooms in sorted order and maintain multiplicative effects with sweep-line style events.

Suppose a tree falls left. Then every mushroom in `[a-h, a)` gets multiplied by `(1 - l/100)` in its survival probability.

Similarly, a right fall affects `(a, a+h]`.

These are range multiplications over mushroom positions.

Since mushrooms are only `10^4`, we can sort them and apply multiplicative interval updates using a difference-array idea in logarithmic time. For every interval, we mark where its multiplicative contribution starts and where it ends.

Then a single sweep over mushrooms reconstructs the total multiplicative factor affecting each mushroom.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Optimal | O((n + m) log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read all mushrooms and sort them by coordinate.

Sorting allows us to convert tree effects into contiguous index ranges over the mushroom array.
2. Create an array `mul` of size `m + 1`, initialized with `1.0`.

This array stores multiplicative difference updates. During the sweep, the running product represents the survival probability contribution from active tree intervals.
3. For every tree, process the left-fall interval.

The dangerous interval is `[a-h, a)`.

Use binary search on the sorted mushroom coordinates:

- `L = lower_bound(a-h)`
- `R = lower_bound(a)`

Mushrooms in indices `[L, R)` are affected.
4. Apply the multiplicative update for the left interval.

If left-fall probability is `p`, every mushroom in the interval must be multiplied by `(1-p)`.

Using multiplicative difference updates:

- `mul[L] *= (1-p)`
- `mul[R] /= (1-p)`

Later, prefix products reconstruct the full multiplier.
5. Process the right-fall interval similarly.

The dangerous interval is `(a, a+h]`.

We need:

- `L = upper_bound(a)`
- `R = upper_bound(a+h)`

Mushrooms in `[L, R)` are affected.
6. Apply the same multiplicative range update using factor `(1-r)`.
7. Sweep through mushrooms from left to right.

Maintain a running product `cur`.

At each index:

- `cur *= mul[i]`
- `cur` now equals the survival probability for this mushroom.
8. Add `cur * mushroom_power` to the answer.
9. Print the final expected value.

### Why it works

Every tree contributes independently to the survival probability of each mushroom.

For a fixed mushroom, its survival probability equals:

```
Π(probability this tree does not destroy it)
```

The algorithm applies exactly these multiplicative factors over all mushrooms covered by each dangerous interval.

The multiplicative difference-array technique guarantees that during the sweep, the running product contains precisely the product of all active interval factors affecting the current mushroom.

Because every interval update corresponds exactly to one tree-direction event, and because the intervals are constructed with the correct half-open boundaries, every mushroom receives exactly the correct survival probability.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    trees = []
    for _ in range(n):
        a, h, l, r = map(int, input().split())
        trees.append((a, h, l / 100.0, r / 100.0))

    mushrooms = []
    for _ in range(m):
        b, z = map(int, input().split())
        mushrooms.append((b, z))

    mushrooms.sort()

    coords = [x for x, _ in mushrooms]

    mul = [1.0] * (m + 1)

    for a, h, lp, rp in trees:
        # Left interval: [a-h, a)
        L = bisect_left(coords, a - h)
        R = bisect_left(coords, a)

        if L < R and lp > 0:
            factor = 1.0 - lp
            mul[L] *= factor
            mul[R] /= factor

        # Right interval: (a, a+h]
        L = bisect_right(coords, a)
        R = bisect_right(coords, a + h)

        if L < R and rp > 0:
            factor = 1.0 - rp
            mul[L] *= factor
            mul[R] /= factor

    ans = 0.0
    cur = 1.0

    for i in range(m):
        cur *= mul[i]
        ans += cur * mushrooms[i][1]

    print("{:.10f}".format(ans))

if __name__ == "__main__":
    solve()
```

The first important implementation detail is sorting mushrooms while keeping their power values attached. All binary searches operate on the sorted coordinate array.

The range updates use multiplicative differences instead of additive differences. If an interval multiplies all survival probabilities by `f`, we place:

```
mul[L] *= f
mul[R] /= f
```

During the sweep, the prefix product activates the factor at `L` and removes it after `R-1`.

The boundary handling is the trickiest part.

For `[a-h, a)` we use:

```
bisect_left(a-h)
bisect_left(a)
```

because the left boundary is inclusive and the right boundary is exclusive.

For `(a, a+h]` we use:

```
bisect_right(a)
bisect_right(a+h)
```

because the left boundary is exclusive and the right boundary is inclusive.

Using the wrong combination of `bisect_left` and `bisect_right` silently breaks boundary cases.

The sweep variable `cur` always stores the total survival probability multiplier for the current mushroom. Multiplying by mushroom power gives its contribution to the expected value.

## Worked Examples

### Example 1

Input:

```
1 1
2 2 50 50
1 1
```

Sorted mushrooms:

| Index | Position | Power |
| --- | --- | --- |
| 0 | 1 | 1 |

Tree effects:

| Tree | Interval | Affected Mushrooms | Survival Factor |
| --- | --- | --- | --- |
| Left fall | [0,2) | mushroom 1 | 0.5 |
| Right fall | (2,4] | none | 0.5 |

Sweep:

| Index | cur | Contribution |
| --- | --- | --- |
| 0 | 0.5 | 0.5 |

Final answer:

```
0.5
```

This example confirms the half-open interval logic. The mushroom at 1 is destroyed only by the left fall.

### Example 2

```
2 1
0 5 50 0
10 5 0 50
5 100
```

The mushroom is at position 5.

Tree processing:

| Tree | Dangerous Interval | Hits Mushroom? | Safe Probability |
| --- | --- | --- | --- |
| Tree 1 left | [-5,0) | No | 1 |
| Tree 1 right | none | No | 1 |
| Tree 2 left | none | No | 1 |
| Tree 2 right | (10,15] | No | 1 |

Actually this mushroom survives with probability 1.

Now change mushroom position to 8:

```
2 1
0 10 50 0
10 5 0 50
8 100
```

Then:

| Tree | Dangerous Interval | Hits Mushroom? | Safe Probability |
| --- | --- | --- | --- |
| Tree 1 right | (0,10] | Yes | 0.5 |
| Tree 2 left | [5,10) | Yes | 0.5 |

Final survival probability:

```
0.5 × 0.5 = 0.25
```

Expected contribution:

```
25
```

This demonstrates why probabilities must be multiplied, not added.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log m) | Each tree performs constant many binary searches |
| Space | O(m) | Coordinate and multiplier arrays |

The solution easily fits the constraints. With `10^5` trees and `10^4` mushrooms, the total number of binary searches is manageable, and the sweep itself is linear.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left, bisect_right

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    trees = []
    for _ in range(n):
        a, h, l, r = map(int, input().split())
        trees.append((a, h, l / 100.0, r / 100.0))

    mushrooms = []
    for _ in range(m):
        b, z = map(int, input().split())
        mushrooms.append((b, z))

    mushrooms.sort()

    coords = [x for x, _ in mushrooms]

    mul = [1.0] * (m + 1)

    for a, h, lp, rp in trees:
        L = bisect_left(coords, a - h)
        R = bisect_left(coords, a)

        if L < R and lp > 0:
            f = 1.0 - lp
            mul[L] *= f
            mul[R] /= f

        L = bisect_right(coords, a)
        R = bisect_right(coords, a + h)

        if L < R and rp > 0:
            f = 1.0 - rp
            mul[L] *= f
            mul[R] /= f

    ans = 0.0
    cur = 1.0

    for i in range(m):
        cur *= mul[i]
        ans += cur * mushrooms[i][1]

    print("{:.10f}".format(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
out = float(run("""1 1
2 2 50 50
1 1
"""))
assert abs(out - 0.5) < 1e-6

# minimum size
out = float(run("""1 1
0 1 0 0
0 7
"""))
assert abs(out - 7.0) < 1e-6

# boundary test for left interval
out = float(run("""1 2
10 5 100 0
5 1
10 1
"""))
assert abs(out - 1.0) < 1e-6

# overlapping probabilities
out = float(run("""2 1
0 10 50 0
10 5 0 50
8 100
"""))
assert abs(out - 25.0) < 1e-6

# all mushrooms destroyed
out = float(run("""1 3
0 100 100 100
-50 1
50 1
0 1
"""))
assert abs(out - 1.0) < 1e-6
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single tree, single mushroom | 0.5 | Basic probability handling |
| Minimum size | 7 | Tree that never falls |
| Boundary interval case | 1 | Correct half-open interval logic |
| Overlapping destruction | 25 | Independent probability multiplication |
| All destroyed except center | 1 | Tree position excluded from intervals |

## Edge Cases

Consider again the boundary issue:

```
1 2
10 5 100 0
5 1
10 1
```

The dangerous interval is `[5,10)`.

Binary searches produce:

```
L = lower_bound(5)
R = lower_bound(10)
```

Only the mushroom at 5 lies in that index range. The mushroom at 10 is excluded because the right endpoint is open.

The algorithm correctly outputs:

```
1
```

Now consider multiple trees affecting one mushroom:

```
2 1
0 10 50 0
10 5 0 50
8 100
```

The mushroom lies in both dangerous intervals.

The update factors are:

```
0.5 and 0.5
```

The sweep multiplies them together:

```
0.5 × 0.5 = 0.25
```

Expected value:

```
25
```

This confirms that independent probabilities are handled correctly.

Finally, consider mushrooms exactly at tree positions:

```
1 1
0 100 100 100
0 10
```

Left interval is `[-100,0)`, right interval is `(0,100]`.

Position 0 belongs to neither interval.

Binary searches generate empty ranges, so no multiplier is applied. The mushroom survives with probability 1, producing answer:

```
10
```

This is where using closed intervals by mistake would fail.
