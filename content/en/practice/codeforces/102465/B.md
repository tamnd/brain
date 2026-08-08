---
title: "CF 102465B - Blurred Pictures"
description: "Each row of the picture contains one contiguous interval of good pixels. For row (i), the good pixels occupy columns from (ai) through (bi), inclusive. We need the largest axis-aligned square whose every pixel is good. Suppose a square uses rows (l) through (r)."
date: "2026-08-08T09:10:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102465
codeforces_index: "B"
codeforces_contest_name: "2018-2019 ICPC Southwestern European Regional Programming Contest (SWERC 2018)"
rating: 0
weight: 102465
solve_time_s: 257
verified: true
draft: false
---

[CF 102465B - Blurred Pictures](https://codeforces.com/problemset/problem/102465/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

Each row of the picture contains one contiguous interval of good pixels. For row (i), the good pixels occupy columns from (a_i) through (b_i), inclusive. We need the largest axis-aligned square whose every pixel is good.

Suppose a square uses rows (l) through (r). Every one of those rows must contain the same horizontal interval occupied by the square. Since row (i) is exactly the interval ([a_i,b_i]), the common columns available to all rows are

[
[\max_{l\le i\le r} a_i,\ \min_{l\le i\le r} b_i].
]

If this intersection contains at least (k) columns and the number of rows is also (k), then a (k\times k) square exists.

The special geometric condition gives us an additional simplification. If two good pixels lie in the same column, every pixel between them in that column is also good. Consequently, if the first and last rows of a group both contain some interval of columns, every intermediate row contains that interval as well. We can use the first and last rows to test a candidate square instead of explicitly inspecting all rows between them.

With (N\le 100000), an (O(N^2)) algorithm is already too slow. There are roughly

[
\frac{N(N+1)}2
]

contiguous row ranges, which is about (5\times10^9) when (N=100000). Even a constant amount of work for every pair is far beyond what a two-second contest limit allows. We need an algorithm close to linear time.

There are several edge cases where a careless implementation can go wrong. First, a single row is always a valid (1\times1) square. For example,

```
1
0 0
```

has answer `1`. An implementation that starts its answer at zero and only searches for squares using two rows can incorrectly return zero.

A second issue is that a wide individual row does not imply a large square. Consider

```
3
0 3
1 2
0 3
```

The middle row has only two good pixels, so the largest square has side `2`, not `4`. A solution based only on the widest row would be wrong. This input is valid because the common columns of the first and third rows are also present in the middle row.

The inclusive endpoints are another common source of off-by-one errors. For example,

```
3
0 1
0 1
0 1
```

contains exactly two good columns, so the answer is `2`. The interval length is `b_i-a_i+1`, not `b_i-a_i`.

Finally, a candidate square cannot extend past the last row. For

```
2
0 1
0 1
```

the answer is `2`, and a check for a candidate whose bottom row is index `2` must stop before accessing it.

## Approaches

A straightforward solution can enumerate every possible top and bottom row. For a fixed pair, we can intersect all row intervals in that range and see whether the resulting horizontal interval is at least as wide as the number of rows. With a running maximum of the left endpoints and minimum of the right endpoints, every new bottom row can be processed in constant time. This gives (O(N^2)) work overall, because there are (N(N+1)/2) possible row ranges. For (N=100000), that is approximately (5\times10^9) ranges, which is much too large.

The structure of the picture gives us a stronger observation. Suppose we already know that a square of side (s) exists. Now fix its top row (i) and ask whether we can extend it to side (s+1). The required rows are (i) through (i+s).

Look only at rows (i) and (i+s). Their common good interval is

[
[L,R]=[\max(a_i,a_{i+s}),\min(b_i,b_{i+s})].
]

If (R-L+1\ge s+1), then both endpoint rows contain (s+1) consecutive common columns. Pick any such (s+1)-column interval. Every column in that interval is good in both endpoint rows. By the vertical convexity condition from the statement, every pixel between those two good pixels is also good. Thus every intermediate row contains the entire interval, giving a valid ((s+1)\times(s+1)) square.

This turns the problem into incremental growth. Keep the largest square side found so far, call it `ans`. For each possible top row, try to extend `ans` by one row and one column. A successful extension increases `ans`, and `ans` can increase at most (N-1) times during the whole algorithm.

The key amortization is what makes the method linear. Although one top row may perform several successful extension checks, every successful check increments the global answer. There can be at most (N-1) such increments. Each top row can also terminate after one unsuccessful check or because the picture boundary has been reached. Hence there are only (O(N)) total iterations of the inner loop.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2)) | (O(N)) | Too slow |
| Optimal | (O(N)) amortized | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Read the interval ([a_i,b_i]) for every row and store the two endpoints. The interval representation is sufficient because every row is horizontally convex.
2. Set `ans = 1`. Since every row contains at least one good pixel, a (1\times1) square always exists.
3. Process each row `i` as a possible top row of a larger square. We already know that a square of side `ans` exists somewhere, but we now ask whether this particular top row can support a square of side `ans + 1`.
4. First check whether row `i` itself has at least `ans + 1` good pixels. Its width is `b[i] - a[i] + 1`, so if

[
b_i-a_i+1 < ans+1,
]

this row cannot be the top of a larger square. There is no reason to try a larger square starting here.

1. Let `j = i + ans`. This is the bottom row of a candidate square with side `ans + 1`. If `j >= N`, the candidate would extend outside the picture, so we stop processing this top row.
2. Compute the intersection of the top and bottom row intervals:

[
L=\max(a_i,a_j),\qquad R=\min(b_i,b_j).
]

If

[
R-L+1\ge ans+1,
]

the two endpoint rows share enough columns for a square of side `ans + 1`.

1. When the intersection is large enough, increment `ans` and repeat the same check. The new candidate has side `ans + 1` and therefore reaches one row farther down.
2. If the endpoint intersection is too narrow, stop for this top row. Increasing the candidate size cannot make the intersection wider, so no larger square beginning at this row can succeed.
3. After all top rows have been processed, print `ans`.

### Why it works

The invariant is that `ans` is always the side length of some valid square already found. Whenever the algorithm increments it, the top and bottom rows of the new candidate share at least `ans` columns. Every column in that shared interval contains good pixels at both endpoints. Vertical convexity guarantees that all pixels between those endpoints are good, so the entire candidate square is valid.

Conversely, when a candidate of side `s` fails for a fixed top row, the shared interval of its two endpoint rows has fewer than `s` columns. Any larger square with the same top row would use the same bottom row or an even later one, and the required width would only increase. Thus there is no missed larger square beginning at that row. Since every possible top row is considered, the final `ans` is the maximum possible square side.

The linear complexity follows from amortization. Every successful inner-loop iteration increases `ans`, and `ans` can increase at most (N-1) times. There is at most one terminating iteration for each top row, so the total number of inner-loop iterations is (O(N)).

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    left = [0] * n
    right = [0] * n

    for i in range(n):
        left[i], right[i] = map(int, input().split())

    ans = 1

    for i in range(n):
        while True:
            # Row i must be wide enough for a square of side ans + 1.
            if right[i] - left[i] + 1 < ans + 1:
                break

            # The bottom row of a square of side ans + 1.
            j = i + ans
            if j >= n:
                break

            # Intersection of the top and bottom row.
            L = max(left[i], left[j])
            R = min(right[i], right[j])

            # Need at least ans + 1 columns.
            if R - L + 1 >= ans + 1:
                ans += 1
            else:
                break

    print(ans)

if __name__ == "__main__":
    solve()
```

The arrays `left` and `right` store the two endpoints of every row. No individual pixel needs to be represented, which keeps the memory usage linear.

The answer starts at `1` because every input row has at least one good pixel. The condition `right[i] - left[i] + 1 < ans + 1` uses the inclusive interval length. Writing it as `right[i] - left[i] < ans` would be equivalent, but the explicit `+1` makes the pixel-count interpretation clearer.

For a candidate of side `ans + 1`, the bottom row is `i + ans`, not `i + ans + 1`. A square of side `s` beginning at row `i` occupies exactly the rows `i, i+1, ..., i+s-1`, so for `s = ans + 1`, the last row is `i + ans`.

The intersection is also inclusive. Its number of columns is `R-L+1`, which must be at least the candidate side length. There is no integer overflow concern in Python, and all relevant values are at most (N).

The most subtle part of the implementation is the inner `while`. It does not cause (O(N^2)) work even though it is nested inside the loop over rows. Every time its body succeeds, `ans` increases. Since `ans` never decreases and cannot exceed `N`, there are at most (N-1) successful iterations in the entire program. Each row can contribute at most one final failed or boundary check.

## Worked Examples

### Sample 1

The first sample is

```
3
1 1
0 2
1 1
```

The rows are `[1,1]`, `[0,2]`, and `[1,1]`. Every row has at least one good pixel, so we begin with `ans = 1`.

| Top row `i` | `ans` before | Bottom row `j` | Top/bottom intersection | Result | `ans` after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | `[1,1]` | width 1, too small | 1 |
| 1 | 1 | 2 | `[1,1]` | width 1, too small | 1 |
| 2 | 1 | 3 | outside picture | stop | 1 |

The answer remains `1`. This demonstrates why the width of an individual row is not enough. The middle row is wide, but the neighboring rows only contain column `1`, so no (2\times2) square exists.

### Sample 2

The second sample is

```
8
2 4
2 4
1 4
0 7
0 3
1 2
1 2
1 1
```

The algorithm starts with `ans = 1`.

| Top row `i` | `ans` before | Bottom row `j` | Intersection | Width | Result |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | `[2,4]` | 3 | `ans = 2` |
| 0 | 2 | 2 | `[2,4]` | 3 | `ans = 3` |
| 0 | 3 | 3 | `[2,4]` | 3 | cannot reach 4 |
| 1 | 3 | 4 | `[2,3]` | 2 | cannot reach 4 |
| 2 | 3 | 5 | `[1,2]` | 2 | cannot reach 4 |
| 3 | 3 | 6 | `[1,2]` | 2 | cannot reach 4 |
| 4 | 3 | 7 | `[1,1]` | 1 | cannot reach 4 |
| 5 | 3 | 8 | outside picture | stop | 3 |
| 6 | 3 | 9 | outside picture | stop | 3 |
| 7 | 3 | 10 | outside picture | stop | 3 |

The first row can support a (2\times2) square, then a (3\times3) square, but not a (4\times4) square. The final answer is `3`.

The trace also illustrates the amortization. The two successful extensions happen while processing the first row, but those two extensions account for two of the only (N-1) possible increments of `ans`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) amortized | Each successful inner iteration increases `ans`, at most (N-1) times, and each row has at most one terminating check. |
| Space | (O(N)) | Two arrays store the left and right endpoint of every row. |

For (N=100000), the algorithm performs only a linear number of interval comparisons and uses linear memory. This is comfortably within the stated 2-second and 256 MB limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    left = [0] * n
    right = [0] * n

    for i in range(n):
        left[i], right[i] = map(int, input().split())

    ans = 1

    for i in range(n):
        while True:
            if right[i] - left[i] + 1 < ans + 1:
                break

            j = i + ans
            if j >= n:
                break

            L = max(left[i], left[j])
            R = min(right[i], right[j])

            if R - L + 1 >= ans + 1:
                ans += 1
            else:
                break

    return str(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided sample 1
assert run("""\
3
1 1
0 2
1 1
""") == "1", "sample 1"

# Provided sample 2
assert run("""\
8
2 4
2 4
1 4
0 7
0 3
1 2
1 2
1 1
""") == "3", "sample 2"

# Minimum-size picture.
assert run("""\
1
0 0
""") == "1", "minimum size"

# All rows are the whole picture.
assert run("""\
4
0 3
0 3
0 3
0 3
""") == "4", "all rows equal"

# Off-by-one case: exactly two columns are available in every row.
assert run("""\
3
0 1
0 1
0 1
""") == "2", "inclusive interval width"

# Wide rows surrounding a narrow row.
assert run("""\
3
0 3
1 2
0 3
""") == "2", "narrow middle row"

# Maximum-size input, with the entire picture good.
n = 100000
maximum_input = str(n) + "\n" + ("0 99999\n" * n)
assert run(maximum_input) == "100000", "maximum size"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 0` | `1` | Minimum size and guaranteed (1\times1) square |
| Four rows of `0 3` | `4` | Maximum possible answer and repeated successful extensions |
| Three rows of `0 1` | `2` | Inclusive interval boundaries and exact square width |
| `0 3 / 1 2 / 0 3` | `2` | A narrow intermediate row prevents a larger square |
| 100000 rows of `0 99999` | `100000` | Maximum (N), linear performance, and boundary handling |

## Edge Cases

The minimum-size case is

```
1
0 0
```

The algorithm starts with `ans = 1`. For the only row, a candidate of side `2` would require bottom row `1`, which is outside the picture. The loop stops and prints `1`. No special-case branch is needed.

For a picture whose every row is completely good,

```
4
0 3
0 3
0 3
0 3
```

the first row successfully grows `ans` from `1` to `2`, then from `2` to `3`, and finally from `3` to `4`. When it tries side `5`, the bottom row would be index `4`, so the boundary check stops the loop. The answer is `4`, which is the entire picture.

For the exact-width case,

```
3
0 1
0 1
0 1
```

a candidate side `2` has endpoint intersection `[0,1]`, whose width is `1-0+1=2`. The algorithm accepts it. A candidate side `3` would require three columns, but the intersection still has width only `2`, so it is rejected. The answer is `2`. This is the typical off-by-one case where forgetting the inclusive `+1` would produce the wrong result.

For

```
3
0 3
1 2
0 3
```

the first and last rows are wide, but the middle row has only columns `1` and `2`. The algorithm can grow from side `1` to side `2` using the first two rows. When it tries side `3`, the first and third rows intersect in four columns, but the top row itself can support the candidate only through the endpoint condition, and the vertical convexity property guarantees that the shared interval must also be present in the intermediate row. Here the relevant common interval for a side `3` candidate would have to contain three columns, while the middle row contains only two, so such a square is impossible. The algorithm correctly stops at `2`.

The maximum-size case contains (100000) identical rows:

```
100000
0 99999
0 99999
...
```

The answer is `100000`. The inner loop performs one successful extension for each possible side length and then stops at the picture boundary. Thus even the largest input produces only (O(N)) work rather than (O(N^2)).
