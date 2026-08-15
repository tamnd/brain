---
title: "CF 102348C - Marbles"
description: "We have a row of (n) marbles, where each marble has one of at most 20 colors. We may swap neighboring marbles, and the goal is to make every color occupy one contiguous block. The blocks themselves may appear in any order."
date: "2026-08-16T01:38:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "C"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 1338
verified: false
draft: false
---

[CF 102348C - Marbles](https://codeforces.com/problemset/problem/102348/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 22m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We have a row of (n) marbles, where each marble has one of at most 20 colors. We may swap neighboring marbles, and the goal is to make every color occupy one contiguous block. The blocks themselves may appear in any order.

The key difficulty is that the final order of the colors is not specified. Once that order is fixed, the problem becomes a standard minimum adjacent-swap problem. The real task is to choose the best permutation of the distinct colors.

Let the distinct colors be (k) colors. Since every color is between 1 and 20, (k\leq20), even though (n) can be as large as (4\cdot10^5). This small bound on the number of colors is the reason a subset dynamic programming solution is possible. A solution polynomial in (n) and exponential only in (k) is practical, while anything exponential in (n) is completely impossible.

The bound (n\leq4\cdot10^5) also rules out repeatedly simulating swaps. A single transformation can require (\frac{n(n-1)}2) adjacent swaps, which at the maximum (n) is

[
\frac{400000\cdot399999}{2}=79,999,800,000.
]

So even handling one particularly bad target arrangement by explicit swaps is far beyond the time limit.

There are several edge cases that are easy to mishandle. If all marbles already form blocks, the answer is zero even when the colors are not numerically sorted. For example,

```
4
2 2 1 1
```

has answer (0). A solution that assumes the blocks must be ordered by color value would incorrectly pay for changing (2,1) into (1,2).

If only one color occurs, no operation is needed regardless of (n). For example,

```
4
20 20 20 20
```

has answer (0). A solution that blindly allocates states for all 20 possible colors may waste substantial time, while a correct implementation should compress the colors that actually occur.

Repeated colors are also significant. For

```
4
1 2 1 2
```

the answer is (1), because swapping the middle two marbles gives (1,1,2,2). Treating individual marbles as independently ordered objects can count unnecessary swaps between marbles of the same color.

Finally, color values are not limited to a small consecutive range such as (1,\dots,k). For

```
4
20 1 20 1
```

the answer is again (1). The implementation should compress the actually occurring colors rather than using their numerical values as DP indices.

## Approaches

A direct brute-force approach starts by observing that a final valid arrangement is completely determined by the order of its color blocks. If the distinct colors are (c_1,c_2,\ldots,c_k), there are (k!) possible orders.

For one fixed order, we can assign every color its desired block rank and scan the original array. Every pair of marbles whose relative order differs from the desired block order contributes exactly one adjacent swap. This is the usual inversion interpretation of adjacent swaps. Thus a fixed order can be evaluated in (O(n)), giving (O(k!,n)) time for all possible orders.

At (k=20), this is hopeless. There are

[
20! = 2,432,902,008,176,640,000
]

possible orders. Even scanning the (4\cdot10^5) marbles once for every order would require roughly

[
20!\cdot4\cdot10^5 \approx 9.73\cdot10^{23}
]

element visits.

The useful observation is that the cost of an order can be decomposed pairwise. Suppose color (x) is placed before color (y) in the final sequence. Every occurrence of (y) that originally appears before an occurrence of (x) forms a pair whose order must be reversed. Each such pair costs exactly one adjacent swap.

Define

[
cost[x][y]
]

as the number of pairs where an (x) occurs before a (y) in the original array.

Now imagine constructing the final color order from left to right. If we append color (c) after a set (S) of already chosen colors, then every color (x\in S) is required to appear before (c). The swaps introduced by placing (c) after all of them are exactly

[
\sum_{x\in S} cost[c][x].
]

The important part is that this depends only on (S) and (c), not on the order in which the colors of (S) were previously arranged. That gives us the optimal-substructure needed for subset DP.

We use a bitmask to represent the set of colors already placed. The DP state records the minimum cost of arranging exactly that set as a prefix. Appending one new color gives the transition.

The comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(k!,n)) | (O(k+n)) | Too slow |
| Optimal | (O(nk+k2^k)) | (O(k2^k)) | Accepted |

Here (k\leq20), so the exponential part is bounded by roughly (20\cdot2^{20}), which is manageable.

## Algorithm Walkthrough

1. Compress the colors that actually occur in the array into indices (0,1,\ldots,k-1). Only these colors can appear as final blocks, and (k\leq20).
2. Build the pairwise cost matrix. For every pair of colors (x,y), let (cost[x][y]) be the number of pairs of positions (i<j) such that (a_i=x) and (a_j=y). During a left-to-right scan, when the current color is (y), every previously seen (x) contributes one to (cost[x][y]). Since there are at most 20 colors, this preprocessing costs (O(nk)).
3. Consider a final order of the colors and focus on the moment when its last color (c) is appended. All other colors form a set (S), and (c\notin S). The extra cost caused by appending (c) is

[
add(c,S)=\sum_{x\in S}cost[c][x].
]

This formula counts exactly the pairs that are in the wrong relative order when (c) is required to come after every color in (S).

1. Define (dp[mask]) as the minimum number of adjacent swaps needed to arrange exactly the colors represented by `mask` into one valid prefix of the final row. The colors in the mask may appear in whichever order gives the minimum cost.
2. For every nonempty mask, try each color (c) contained in it as the last color of that prefix. If `prev = mask` without (c), the transition is

\min_{c\in mask}
\left(
dp[prev]
+
\sum_{x\in prev}cost[c][x]
\right).
]

The predecessor is already optimal by the definition of the DP, and the added term accounts for every pair involving the newly appended color.

1. To keep the Python implementation fast, precompute the subset sum

[
sum_c[S]=\sum_{x\in S}cost[c][x]
]

for every color (c) and every subset (S) that does not contain (c). Each such table has (2^{k-1}) entries, so all of them together contain (k2^{k-1}) values. The subset sums themselves are computed by removing one set bit:

[
sum_c[S]=sum_c[S\setminus{x}]+cost[c][x].
]

The implementation stores these values in compact 64-bit arrays.

1. Iterate through all masks and apply the transition for every possible last color. The answer is `dp[(1 << k) - 1]`, because that mask contains every distinct color.

Why it works: fix any final ordering of the colors. Every pair of marbles of different colors either keeps its relative order or reverses it. A pair whose original order disagrees with the final block order must cross exactly once, and an adjacent swap can change the relative order of only the two swapped marbles. Hence the number of such reversed pairs is exactly the minimum number of adjacent swaps for that final ordering.

The DP considers every possible final ordering implicitly. When color (c) is appended, its contribution depends only on which colors are already before it, not on their internal order. Thus every ordering is represented by a sequence of DP transitions, and every transition adds exactly the swaps involving the newly appended block. Taking the minimum over all possible last colors consequently gives the minimum cost over all valid block orders.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve_case(a):
    # Compress the colors that actually occur.
    colors = sorted(set(a))
    k = len(colors)
    index = {x: i for i, x in enumerate(colors)}
    b = [index[x] for x in a]

    # cost[x][y] = number of pairs (x before y) in the original array.
    cost = [[0] * k for _ in range(k)]
    seen = [0] * k

    for y in b:
        for x in range(k):
            cost[x][y] += seen[x]
        seen[y] += 1

    if k == 1:
        return 0

    # For every color c, store subset sums for subsets not containing c.
    # Such a subset has k-1 bits, hence 2^(k-1) entries.
    half = 1 << (k - 1)
    total_sum_entries = k * half
    subset_sum = array('q', [0]) * total_sum_entries

    for c in range(k):
        base = c * half

        others = []
        for x in range(k):
            if x != c:
                others.append(x)

        row = cost[c]

        for mask in range(1, half):
            lb = mask & -mask
            bit = lb.bit_length() - 1
            prev = mask ^ lb
            subset_sum[base + mask] = (
                subset_sum[base + prev] + row[others[bit]]
            )

    size = 1 << k
    inf = 10**30
    dp = [inf] * size
    dp[0] = 0

    lower_mask = [(1 << c) - 1 for c in range(k)]

    for mask in range(1, size):
        bits = mask
        best = inf

        while bits:
            lb = bits & -bits
            c = lb.bit_length() - 1
            prev = mask ^ lb

            # Remove bit c from prev to obtain its compressed
            # (k-1)-bit representation.
            compressed = (
                (prev & lower_mask[c])
                | ((prev >> (c + 1)) << c)
            )

            value = dp[prev] + subset_sum[c * half + compressed]

            if value < best:
                best = value

            bits ^= lb

        dp[mask] = best

    return dp[-1]

def main():
    n = int(input())
    a = list(map(int, input().split()))
    print(solve_case(a))

if __name__ == "__main__":
    main()
```

The first part of `solve_case` compresses the colors. This avoids allocating DP states for colors that never occur and also handles values such as 20 without treating them specially.

The `cost` matrix stores directional pair counts. When the current color is `y`, every previously seen color `x` gives one pair with `x` before `y`, so `cost[x][y]` is incremented by `seen[x]`. This orientation matters. When `y` is appended after `x`, the problematic pairs are the ones where `y` originally appeared before `x`, which are stored as `cost[y][x]`.

The subset-sum table is indexed separately for each possible last color. Since the last color (c) cannot be present in its predecessor mask, only (k-1) bits are needed. This cuts the storage from (k2^k) entries to (k2^{k-1}) entries.

The compressed mask removes bit `c`. Its lower bits can stay where they are, while every bit above `c` is shifted down by one. The expression

```
(prev & lower_mask[c]) | ((prev >> (c + 1)) << c)
```

performs exactly that conversion.

The DP starts with `dp[0] = 0`, because an empty prefix requires no swaps. For every nonempty mask, each set bit is considered as the color of the last block. The predecessor is obtained with `mask ^ lb`, and the precomputed subset sum supplies the cost of putting the chosen color after all predecessor colors.

Python integers have arbitrary precision, so there is no overflow concern even though the answer can be much larger than (2^{31}). The compact `array('q')` is used for the subset sums because Python's normal integers carry substantial per-object memory overhead.

## Worked Examples

### Sample 1

The input is

```
7
3 4 2 3 4 2 2
```

The distinct colors are (3,4,2). After compression, call them (0,1,2) respectively.

Some relevant pair costs are

[
cost[4][3]=1,
\qquad
cost[2][3]=1,
\qquad
cost[2][4]=1.
]

These are exactly the three pairs that must cross if the final order is (3,4,2).

The optimal DP path can be shown as follows.

| Mask | Last color | Previous mask | Added cost | DP value |
| --- | --- | --- | --- | --- |
| `001` | 3 | `000` | 0 | 0 |
| `011` | 4 | `001` | (cost[4][3]=1) | 1 |
| `111` | 2 | `011` | (cost[2][3]+cost[2][4]=2) | 3 |

The resulting block order is (3,4,2), giving the final arrangement

```
3 3 4 4 2 2 2
```

and the minimum is (3).

This trace demonstrates why the cost is attached to the color being appended. When 4 is appended after 3, only pairs where 4 originally precedes 3 matter. When 2 is appended, it must cross the earlier 3 and 4 exactly where those pairs occur in the wrong order.

### Sample 2

The input is

```
5
20 1 14 10 2
```

Every color occurs exactly once. Since each color already forms a segment of length one, any order of the five singleton blocks is valid, and the original arrangement requires zero swaps.

All pair costs are irrelevant to the optimum because the original sequence itself is already a valid block ordering.

| Mask | Last color | Previous mask | Added cost | DP value |
| --- | --- | --- | --- | --- |
| `00001` | 20 | `00000` | 0 | 0 |
| `00011` | 1 | `00001` | 0 | 0 |
| `00111` | 14 | `00011` | 0 | 0 |
| `01111` | 10 | `00111` | 0 | 0 |
| `11111` | 2 | `01111` | 0 | 0 |

Every DP state remains at zero, so the final answer is (0).

This exercises the case where every color appears once. A correct solution must recognize that singleton colors are already contiguous.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nk+k2^k)) | Building pair costs takes (O(nk)), subset sums and DP take (O(k2^k)) |
| Space | (O(k2^k)) | The DP has (2^k) states and the compact subset-sum table has (k2^{k-1}) entries |

With (k\leq20), the DP contains at most (2^{20}=1,048,576) states. The transition examines at most 20 possible last colors per state. The preprocessing scans at most 20 color counters for each of the (4\cdot10^5) marbles. These bounds are designed around the small color alphabet, so the algorithm remains feasible even at the maximum (n).

## Test Cases

```python
import sys
import io
from array import array

def solve(inp: str) -> str:
    reader = io.StringIO(inp).readline
    n = int(reader())
    a = list(map(int, reader().split()))

    colors = sorted(set(a))
    k = len(colors)
    index = {x: i for i, x in enumerate(colors)}
    b = [index[x] for x in a]

    cost = [[0] * k for _ in range(k)]
    seen = [0] * k

    for y in b:
        for x in range(k):
            cost[x][y] += seen[x]
        seen[y] += 1

    if k == 1:
        return "0"

    half = 1 << (k - 1)
    subset_sum = array('q', [0]) * (k * half)

    for c in range(k):
        base = c * half
        others = [x for x in range(k) if x != c]
        row = cost[c]

        for mask in range(1, half):
            lb = mask & -mask
            bit = lb.bit_length() - 1
            prev = mask ^ lb
            subset_sum[base + mask] = (
                subset_sum[base + prev] + row[others[bit]]
            )

    size = 1 << k
    inf = 10**30
    dp = [inf] * size
    dp[0] = 0

    lower_mask = [(1 << c) - 1 for c in range(k)]

    for mask in range(1, size):
        bits = mask
        best = inf

        while bits:
            lb = bits & -bits
            c = lb.bit_length() - 1
            prev = mask ^ lb

            compressed = (
                (prev & lower_mask[c])
                | ((prev >> (c + 1)) << c)
            )

            value = dp[prev] + subset_sum[c * half + compressed]

            if value < best:
                best = value

            bits ^= lb

        dp[mask] = best

    return str(dp[-1])

# Provided samples
assert solve("""7
3 4 2 3 4 2 2
""") == "3", "sample 1"

assert solve("""5
20 1 14 10 2
""") == "0", "sample 2"

assert solve("""13
5 5 4 4 3 5 7 6 5 4 4 6 5
""") == "21", "sample 3"

# Minimum-size input
assert solve("""2
1 1
""") == "0", "minimum size, all equal"

assert solve("""2
1 2
""") == "0", "minimum size, two singleton blocks"

# Repeated colors requiring exactly one swap
assert solve("""4
1 2 1 2
""") == "1", "one crossing pair"

# Boundary color value and non-consecutive colors
assert solve("""4
20 1 20 1
""") == "1", "color value 20"

# Already grouped, but block order is not numerical
assert solve("""6
3 3 1 1 2 2
""") == "0", "arbitrary valid block order"

# Maximum-size input, all marbles have one color
maximum_case = "400000\n" + "20 " * 399999 + "20\n"
assert solve(maximum_case) == "0", "maximum n, all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 1` | `0` | Minimum size and single distinct color |
| `2 / 1 2` | `0` | Minimum size with two singleton blocks |
| `4 / 1 2 1 2` | `1` | Exactly one required crossing |
| `4 / 20 1 20 1` | `1` | Boundary color value and color compression |
| `6 / 3 3 1 1 2 2` | `0` | Valid block order does not need to be numerically sorted |
| `400000 / all 20` | `0` | Maximum (n), single-color handling |

## Edge Cases

If every marble has the same color, there is already exactly one contiguous segment. For

```
4
20 20 20 20
```

the compression produces (k=1). The algorithm returns immediately with zero instead of constructing a large DP. This avoids both unnecessary work and the common mistake of assuming that at least two colors exist.

If every color occurs once, every marble is already its own contiguous block. For

```
5
20 1 14 10 2
```

there are five singleton blocks, so the original row is already valid and the answer is zero. The pair costs do not force any particular order because the original order itself is one of the allowed final orders.

If colors are interleaved, the pair-count formulation captures exactly the required swaps. For

```
4
1 2 1 2
```

the final order (1,2) requires the second marble and third marble to cross. There is exactly one pair where a 2 occurs before a later 1, so the DP assigns cost (1) to the order (1,2). The reverse block order would cost more, and the answer is (1).

If the color values are sparse or at their boundary, compression prevents array-index errors. For

```
4
20 1 20 1
```

the colors are compressed to two DP indices even though their original values are 20 and 1. One crossing is required, so the answer is (1).

If the existing blocks are in an arbitrary order, that order must be accepted. For

```
6
3 3 1 1 2 2
```

each color is already contiguous, so no swap is necessary. The DP is not tied to numerical color order. It is free to select (3,1,2) as the final block order and obtains zero.

The largest input size is also safe when one color dominates. With (400000) copies of color 20, there is only one distinct color, so the algorithm exits after compression. This case is useful because an implementation that always builds a (2^{20})-state DP would perform unnecessary work despite the actual instance having only one state.
