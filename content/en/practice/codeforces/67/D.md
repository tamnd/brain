---
title: "CF 67D - Optical Experiment"
description: "Each ray enters the box through one hole on the left side and exits through one hole on the right side. The order of holes on both sides matters."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 67
codeforces_index: "D"
codeforces_contest_name: "Manthan 2011"
rating: 1900
weight: 67
solve_time_s: 113
verified: true
draft: false
---

[CF 67D - Optical Experiment](https://codeforces.com/problemset/problem/67/D)

**Rating:** 1900  
**Tags:** binary search, data structures, dp  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

Each ray enters the box through one hole on the left side and exits through one hole on the right side. The order of holes on both sides matters. A ray is identified by its label, and the two input permutations describe where each ray appears on the entrance side and where it appears on the exit side.

Two rays intersect if their relative order changes between the two sides. Suppose ray `a` appears before ray `b` on the left side. If `a` appears after `b` on the right side, the two rays must cross somewhere inside the box.

The task asks for the largest subset of rays such that every pair inside the subset intersects. In graph language, we want the size of the largest clique in the intersection graph of rays, but the geometry gives us much more structure than a general graph problem.

The constraints are the main challenge. `n` can be as large as `10^6`, which rules out anything quadratic immediately. Even `O(n log^2 n)` needs careful implementation in Python at this scale. We need a clean `O(n log n)` solution with low constant factors and memory usage that stays linear where possible.

A subtle point is that the rays are given by labels, not directly by positions. We first need to reconstruct the position of every ray on both sides before we can reason about crossings.

Another easy mistake is confusing "pairwise intersecting" with "all intersect a common point". These are different conditions geometrically. For example:

```
3
1 2 3
3 1 2
```

All three rays do not pairwise intersect. Rays `(1,2)` intersect and `(1,3)` intersect, but `(2,3)` do not. The correct answer is `2`.

A careless implementation that only counts how many inversions each ray participates in could incorrectly conclude that all three belong to the same group.

Another dangerous edge case is already reversed order:

```
5
1 2 3 4 5
5 4 3 2 1
```

Every pair intersects, so the answer is `5`.

An algorithm that searches only for local patterns instead of the global structure might miss this complete reversal.

The smallest case also matters:

```
1
1
1
```

The answer is `1`, because a single ray trivially forms a valid group by itself.

## Approaches

The brute-force idea is straightforward. First compute the order of rays on the left side and the right side. Then for every pair of rays, check whether their order changes. This gives us an intersection graph. After that, we would need the largest subset where every pair intersects.

The pair checking alone already costs `O(n^2)`, which is impossible for `n = 10^6`. Even storing the graph would require trillions of edges in the worst case. General maximum clique algorithms are much worse than quadratic, so we need to exploit the special structure of this problem.

The key observation is that the geometry reduces everything to permutations.

Suppose we list rays in the order they appear on the left side. For each ray, write its position on the right side. We obtain a permutation:

```
p[i] = position on right side of the ray appearing at left position i
```

Two rays intersect exactly when their order reverses, which means:

```
i < j but p[i] > p[j]
```

Now think about a group where every pair intersects. For every pair inside the group, the earlier left-side ray must have a larger right-side position. That means the sequence of `p` values for the group is strictly decreasing.

So the problem becomes:

Find the longest decreasing subsequence of the permutation.

This is a classic problem. We can solve it in `O(n log n)` using the patience sorting technique used for LIS. A longest decreasing subsequence can be found by computing LIS on negated values, or by reversing the comparison logic directly.

At this point the geometric problem disappears completely. The entire challenge becomes a subsequence problem on permutations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the entrance order array and the exit order array.
2. Build an array `pos_right` where `pos_right[x]` stores the position of ray `x` on the right side.

This lets us quickly map any ray to its exit position.
3. Traverse the rays in left-side order and construct a permutation `p`.

For each ray `x` in the left-side array:

```
p.append(pos_right[x])
```

Now `p[i]` tells us where the `i`-th left-side ray appears on the right side.
4. Observe that two rays intersect exactly when their corresponding values form an inversion.

If `i < j` and `p[i] > p[j]`, the order reverses, so the rays cross.
5. A group where every pair intersects corresponds exactly to a strictly decreasing subsequence in `p`.

Inside such a subsequence, every earlier element is larger than every later element, so every pair forms an inversion.
6. Compute the length of the longest decreasing subsequence.

Instead of implementing LDS directly, negate the values and compute LIS on `-p[i]`.
7. Maintain an array `tails`.

`tails[k]` stores the smallest possible ending value for an increasing subsequence of length `k + 1`.
8. For each value `v = -p[i]`, binary search the first position in `tails` where `v` can replace an existing value.

If no such position exists, append `v`.
9. The final size of `tails` is the answer.

### Why it works

The critical invariant is the equivalence between pairwise intersections and inversions in the permutation.

After converting the geometry into permutation form, every valid group corresponds to indices where every pair satisfies:

```
i < j and p[i] > p[j]
```

That condition is exactly the definition of a strictly decreasing subsequence.

The LIS algorithm maintains the optimal ending value for every subsequence length. Replacing a larger tail with a smaller one never hurts future possibilities, because smaller endings are always more flexible for extension. By the standard correctness argument for patience sorting, the final length equals the maximum possible subsequence length.

Since we run LIS on negated values, we obtain the longest decreasing subsequence length in the original permutation, which equals the largest pairwise-intersecting group.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve():
    n = int(input())

    left = list(map(int, input().split()))
    right = list(map(int, input().split()))

    pos_right = [0] * (n + 1)

    for i, x in enumerate(right):
        pos_right[x] = i

    tails = []

    for x in left:
        v = -pos_right[x]

        idx = bisect_left(tails, v)

        if idx == len(tails):
            tails.append(v)
        else:
            tails[idx] = v

    print(len(tails))

solve()
```

The first step reconstructs the right-side positions of every ray. Since ray labels are unique and range from `1` to `n`, an array lookup is faster and lighter than a dictionary.

The permutation construction is implicit inside the main loop. For each ray in left-side order, we immediately fetch its right-side position and negate it. Negation converts the longest decreasing subsequence problem into a standard longest increasing subsequence problem.

The `tails` array is the standard patience sorting structure. Suppose `tails[2] = -7`. That means we have found an increasing subsequence of length `3` ending at value `-7`, and among all such subsequences this ending value is as small as possible.

Using `bisect_left` preserves strictness correctly. Since the permutation contains distinct values, strict increasing and non-decreasing behavior coincide cleanly after negation.

One easy mistake is using actual ray labels instead of positions. Intersections depend only on relative order, not on ray numbers themselves.

Another common bug is forgetting that positions are zero-indexed in the implementation while the mathematical description is usually one-indexed. The choice does not matter as long as ordering is preserved consistently.

## Worked Examples

### Example 1

Input:

```
5
1 4 5 2 3
3 4 2 1 5
```

First compute right-side positions:

| Ray | Right Position |
| --- | --- |
| 1 | 3 |
| 2 | 2 |
| 3 | 0 |
| 4 | 1 |
| 5 | 4 |

Now build the permutation in left-side order:

| Left Position | Ray | Right Position | Negated Value | tails |
| --- | --- | --- | --- | --- |
| 0 | 1 | 3 | -3 | [-3] |
| 1 | 4 | 1 | -1 | [-3, -1] |
| 2 | 5 | 4 | -4 | [-4, -1] |
| 3 | 2 | 2 | -2 | [-4, -2] |
| 4 | 3 | 0 | 0 | [-4, -2, 0] |

Final answer: `3`.

The corresponding decreasing subsequence in original positions is:

```
4, 2, 0
```

Those rays pairwise intersect.

### Example 2

Input:

```
5
1 2 3 4 5
5 4 3 2 1
```

Right-side positions:

| Ray | Right Position |
| --- | --- |
| 1 | 4 |
| 2 | 3 |
| 3 | 2 |
| 4 | 1 |
| 5 | 0 |

Permutation:

```
4 3 2 1 0
```

Trace:

| Step | Value | Negated | tails |
| --- | --- | --- | --- |
| 1 | 4 | -4 | [-4] |
| 2 | 3 | -3 | [-4, -3] |
| 3 | 2 | -2 | [-4, -3, -2] |
| 4 | 1 | -1 | [-4, -3, -2, -1] |
| 5 | 0 | 0 | [-4, -3, -2, -1, 0] |

Final answer: `5`.

This demonstrates the extreme case where every pair intersects, producing a completely decreasing permutation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each of the `n` elements performs one binary search in `tails` |
| Space | O(n) | Arrays for positions and LIS state |

With `n = 10^6`, quadratic algorithms are impossible. `O(n log n)` is fast enough in Python when implemented carefully with arrays and iterative processing. The memory usage also comfortably fits within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())

        left = list(map(int, input().split()))
        right = list(map(int, input().split()))

        pos_right = [0] * (n + 1)

        for i, x in enumerate(right):
            pos_right[x] = i

        tails = []

        for x in left:
            v = -pos_right[x]

            idx = bisect_left(tails, v)

            if idx == len(tails):
                tails.append(v)
            else:
                tails[idx] = v

        return str(len(tails))

    return solve() + "\n"

# provided sample
assert run(
"""5
1 4 5 2 3
3 4 2 1 5
""") == "3\n", "sample 1"

# minimum size
assert run(
"""1
1
1
""") == "1\n", "single ray"

# completely reversed
assert run(
"""5
1 2 3 4 5
5 4 3 2 1
""") == "5\n", "all pairs intersect"

# already aligned
assert run(
"""5
1 2 3 4 5
1 2 3 4 5
""") == "1\n", "no intersections"

# mixed ordering
assert run(
"""6
1 2 3 4 5 6
2 1 4 3 6 5
""") == "2\n", "multiple small inversions"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single ray | 1 | Smallest valid input |
| Completely reversed permutation | 5 | Every pair intersects |
| Identical permutations | 1 | No pair intersects |
| Alternating swaps | 2 | Correct handling of local inversions |

## Edge Cases

Consider the smallest possible input:

```
1
1
1
```

Right-side positions become:

```
pos_right[1] = 0
```

The generated sequence is:

```
[0]
```

The LIS on negated values has length `1`, so the algorithm outputs `1`. A single ray always forms a valid group because there are no conflicting pairs to check.

Now consider the case where no rays intersect:

```
5
1 2 3 4 5
1 2 3 4 5
```

The generated permutation is:

```
0 1 2 3 4
```

This sequence has no decreasing subsequence longer than `1`. During the LIS process on negated values:

```
0 -> [0]
-1 replaces 0
-2 replaces -1
-3 replaces -2
-4 replaces -3
```

The `tails` array never grows beyond length `1`, so the answer is correctly `1`.

Finally, consider the maximal intersection structure:

```
5
1 2 3 4 5
5 4 3 2 1
```

The permutation becomes:

```
4 3 2 1 0
```

Every pair forms an inversion, so every pair of rays intersects. The decreasing subsequence length is `5`, and the algorithm extends `tails` at every step, correctly returning the full size of the set.
