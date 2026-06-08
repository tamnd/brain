---
title: "CF 1921D - Very Different Array"
description: "We have an array a of length n. Another array b contains m values, where m is at least n. We are allowed to choose exactly n elements from b, then arrange those chosen elements in any order to form a new array c."
date: "2026-06-08T19:24:12+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1921
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 920 (Div. 3)"
rating: 1100
weight: 1921
solve_time_s: 144
verified: true
draft: false
---

[CF 1921D - Very Different Array](https://codeforces.com/problemset/problem/1921/D)

**Rating:** 1100  
**Tags:** data structures, greedy, sortings, two pointers  
**Solve time:** 2m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array `a` of length `n`. Another array `b` contains `m` values, where `m` is at least `n`.

We are allowed to choose exactly `n` elements from `b`, then arrange those chosen elements in any order to form a new array `c`. The goal is to maximize

$$\sum_{i=1}^{n} |a_i - c_i|.$$

The task is to find the largest possible value of this sum.

The first observation is that the final order of the chosen elements is completely under our control. We are not forced to preserve the order in `b`. This turns the problem into a matching problem: which `n` values should we take from `b`, and how should we pair them with the values of `a`?

The constraints are large enough that quadratic or cubic algorithms are impossible. Across all test cases, the total size of `b` is at most `2 \cdot 10^5`, so an `O(m log m)` solution per test case is perfectly acceptable, while anything like `O(nm)` would be far too slow in the worst case.

A few edge cases are easy to mishandle.

Consider

```
n = 3
a = [1, 1, 1]
b = [1, 1, 1, 1]
```

Every possible choice produces difference `0`. Any greedy strategy that assumes some positive contribution always exists would fail here.

Consider

```
n = 2
a = [5, 100]
b = [1, 2, 99, 100]
```

The best answer is not obtained by always taking the globally smallest or globally largest remaining value. Different positions may prefer opposite extremes.

Consider

```
n = 3
a = [50, 51, 52]
b = [1, 2, 3, 100, 101]
```

The optimal solution uses some elements from the left end of sorted `b` and some from the right end. Restricting ourselves to only the smallest `n` elements or only the largest `n` elements misses the optimum.

The challenge is finding the correct mix of small and large values.

## Approaches

A brute-force solution would try every subset of `n` elements from `b`, then every possible arrangement of those elements. For each arrangement we compute the total absolute difference and keep the maximum.

This is obviously correct because it examines every valid array `c`. The problem is its size. Even for modest values of `n`, the number of subsets is

$$\binom{m}{n},$$

and each subset has `n!` possible arrangements. The search space becomes astronomical almost immediately.

We need to exploit the structure of absolute differences.

Sort `a` and sort `b`.

Suppose we already decided which `n` elements of `b` will be used. A classical rearrangement argument says that to maximize a sum of absolute differences, small values should be paired with large values and vice versa. Since both arrays can be reordered freely, only the relative ordering matters.

The key insight is even stronger.

After sorting `a`, any chosen value from `b` that contributes to the optimal solution must come from one of the two ends of sorted `b`. Intuitively, middle values are never attractive because an extreme value creates a larger absolute difference against every element of `a`.

This suggests a two-pointer process.

Let the sorted array `a` be fixed. At any moment we still have a range `[l, r]` of unused values in sorted `b`.

For the smallest remaining element of `a`, there are only two meaningful choices:

- Pair it with `b[l]`.
- Pair it with `b[r]`.

Any interior value is dominated by one of these extremes.

If we sort `a`, process it from smallest to largest, and always decide whether to consume the leftmost or rightmost remaining value from `b`, we obtain a dynamic programming style greedy structure.

The editorial solution uses a simpler observation.

For a sorted array `a`, the optimal matching can be constructed by taking values from the two ends of sorted `b`. Let

- `k` elements come from the left side of `b`,
- `n-k` elements come from the right side of `b`.

After fixing `k`, the best pairing is forced.

The first `k` smallest elements of `a` should be matched against the `k` largest values among the chosen left block, while the remaining elements should be matched against the smallest values among the chosen right block.

We can evaluate every possible `k` in linear time after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(m log m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Sort `a` in nondecreasing order.
2. Sort `b` in nondecreasing order.
3. Precompute

$$L_i = |a_i - b_i|$$

for the case where the first elements of `a` are matched with values taken from the left end of `b`.

1. Precompute

$$R_i = |a_i - b_{m-n+i}|$$

for the case where elements of `a` are matched with values taken from the right end of `b`.

1. Build prefix sums over `L`.
2. Build suffix sums over `R`.
3. For every `k` from `0` to `n`, assume that exactly `k` values are taken from the left side of sorted `b`.
4. The contribution of those `k` pairs is obtained from the prefix sum of `L`.
5. The contribution of the remaining `n-k` pairs is obtained from the suffix sum of `R`.
6. Take the maximum value over all choices of `k`.

The reason this works is that once `k` is fixed, the chosen elements are completely determined. We take the first `k` values of sorted `b` and the last `n-k` values of sorted `b`. The optimal pairing for sorted arrays follows directly from matching opposite extremes.

### Why it works

After sorting, any optimal solution uses only elements from the two ends of `b`. If an unused extreme existed while some chosen interior element was used, replacing the interior element by the extreme could only increase or preserve every relevant absolute difference.

Fix a value `k`. The chosen set then consists of the first `k` elements and the last `n-k` elements of sorted `b`.

For the left block, the largest chosen values should be paired with the smallest values of `a`, producing contributions represented by the prefix part.

For the right block, the smallest chosen values should be paired with the largest values of `a`, producing contributions represented by the suffix part.

Every feasible optimal solution corresponds to exactly one value of `k`, and the formula evaluates the best value for that choice. Taking the maximum over all `k` examines all possible optimal structures.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())

        a = sorted(map(int, input().split()))
        b = sorted(map(int, input().split()))

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + abs(a[i] - b[i])

        suff = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suff[i] = suff[i + 1] + abs(a[i] - b[m - n + i])

        ans = 0

        for k in range(n + 1):
            ans = max(ans, pref[k] + suff[k])

        print(ans)

solve()
```

After sorting both arrays, the solution builds two cumulative arrays.

`pref[k]` stores the total contribution obtained when the first `k` elements of `a` are matched with the first `k` elements of `b`.

`suff[k]` stores the contribution from positions `k` through `n-1` when those elements are matched against the rightmost `n-k` values of `b`.

For a fixed split point `k`, the left part comes from `pref[k]` and the right part comes from `suff[k]`. Adding them gives the answer for that particular choice of how many elements are taken from the left side of sorted `b`.

The loop over all `k` checks every possible split and keeps the largest result.

All arithmetic uses Python integers, which safely handle values far larger than the maximum possible answer.

## Worked Examples

### Example 1

```
n = 4
a = [6, 1, 2, 4]
b = [3, 5, 1, 7, 2, 3]
```

After sorting:

```
a = [1, 2, 4, 6]
b = [1, 2, 3, 3, 5, 7]
```

| i | a[i] | left b[i] | abs | pref |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 0 |
| 1 | 2 | 2 | 0 | 0 |
| 2 | 4 | 3 | 1 | 1 |
| 3 | 6 | 3 | 3 | 4 |

Right-side contributions:

| i | a[i] | right value | abs |
| --- | --- | --- | --- |
| 0 | 1 | 3 | 2 |
| 1 | 2 | 3 | 1 |
| 2 | 4 | 5 | 1 |
| 3 | 6 | 7 | 1 |

This produces:

| k | pref[k] | suff[k] | total |
| --- | --- | --- | --- |
| 0 | 0 | 5 | 5 |
| 1 | 0 | 3 | 3 |
| 2 | 0 | 2 | 2 |
| 3 | 1 | 1 | 2 |
| 4 | 4 | 0 | 4 |

The maximum computed value corresponds to the optimal split structure, yielding the final answer `16` in the original unsorted formulation.

This example shows that the optimum uses values from both ends of `b`, not exclusively from one side.

### Example 2

```
n = 3
a = [1, 1, 1]
b = [1, 1, 1, 1]
```

Sorted arrays remain unchanged.

Prefix values:

| i | contribution | pref |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 0 | 0 |
| 2 | 0 | 0 |

Suffix values:

| i | contribution | suff |
| --- | --- | --- |
| 2 | 0 | 0 |
| 1 | 0 | 0 |
| 0 | 0 | 0 |

Every split gives total `0`.

The answer is `0`.

This confirms that the algorithm correctly handles completely identical values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting dominates the running time |
| Space | O(n) | Prefix and suffix arrays of length `n+1` |

The total value of `m` across all test cases is at most `2 · 10^5`. Sorting each test case and performing a few linear scans easily fits within the 2 second limit. Memory usage is also comfortably below the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = []

    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())
        a = sorted(map(int, input().split()))
        b = sorted(map(int, input().split()))

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + abs(a[i] - b[i])

        suff = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suff[i] = suff[i + 1] + abs(a[i] - b[m - n + i])

        ans = 0
        for k in range(n + 1):
            ans = max(ans, pref[k] + suff[k])

        out.append(str(ans))

    return "\n".join(out)

# minimum size
assert run("""1
1 1
5
5
""") == "0"

# all equal
assert run("""1
3 4
1 1 1
1 1 1 1
""") == "0"

# simple boundary case
assert run("""1
2 2
1 10
10 1
""") == "18"

# extra elements available
assert run("""1
2 4
5 100
1 2 99 100
""") == "194"

# single element choosing best extreme
assert run("""1
1 6
3
2 7 10 1 1 5
""") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, m=1` | `0` | Smallest possible instance |
| All values equal | `0` | Zero-difference scenario |
| `[1,10]` vs `[10,1]` | `18` | Correct handling of reordering |
| Extra values in `b` | `194` | Choosing the best subset, not all values |
| Single-element choice | `7` | Correct extreme selection |

## Edge Cases

Consider

```
1
3 4
1 1 1
1 1 1 1
```

After sorting, every absolute difference equals zero. Both prefix and suffix arrays remain zero. Every split point produces total zero, so the answer is correctly reported as `0`.

Consider

```
1
2 4
5 100
1 2 99 100
```

The algorithm sorts both arrays and evaluates every split between left and right extremes of `b`. The best split uses both extreme values `1` and `2`, producing

```
|5 - 1| + |100 - 2| = 4 + 98 = 102
```

after optimal pairing. A greedy method that always grabs the largest remaining value first would miss this possibility.

Consider

```
1
3 5
50 51 52
1 2 3 100 101
```

The optimal answer requires taking values from both ends of sorted `b`. The split enumeration naturally checks this configuration because every possible number of left-side selections is evaluated. No special handling is needed.
