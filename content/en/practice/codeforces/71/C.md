---
title: "CF 71C - Round Table Knights"
description: "The knights sit on a circle, equally spaced. Each position is marked either 1 for a knight in a good mood or 0 for a knight in a bad mood."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 71
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 65 (Div. 2)"
rating: 1600
weight: 71
solve_time_s: 100
verified: true
draft: false
---

[CF 71C - Round Table Knights](https://codeforces.com/problemset/problem/71/C)

**Rating:** 1600  
**Tags:** dp, math, number theory  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

The knights sit on a circle, equally spaced. Each position is marked either `1` for a knight in a good mood or `0` for a knight in a bad mood. We need to determine whether it is possible to choose some of the good-mood knights so that they form the vertices of a regular polygon with at least three vertices.

Because all knights are equally spaced around the circle, every regular polygon corresponds to taking positions with a fixed step size. For example, if `n = 12` and we choose every third knight, we get the vertices of a square. If we choose every second knight, we get a hexagon.

The task becomes: does there exist some step size such that repeatedly jumping by that step visits only positions containing `1`, and the cycle contains at least three distinct positions?

The constraint `n ≤ 10^5` immediately rules out anything close to cubic time. Even a full `O(n^2)` solution is risky in Python for Codeforces, especially with a very small time limit. We need something close to linear or `n log n`.

A subtle point is that not every subset of good knights forms a valid polygon. The vertices must be equally spaced around the circle. A careless solution might only count how many `1`s exist and conclude that at least three good knights are enough.

Consider:

```
6
1 1 1 0 0 0
```

The correct answer is `NO`.

Although there are three good knights, they are consecutive, not equally spaced. No regular polygon can be formed.

Another tricky case appears when the polygon uses all knights.

```
5
1 1 1 1 1
```

The answer is `YES`.

The entire pentagon is itself a regular polygon. Any implementation that only checks proper divisors of `n` would incorrectly miss this.

One more edge case involves cycles that are too small.

```
4
1 0 1 0
```

The answer is `NO`.

Choosing every second knight creates only two vertices, which is not a valid polygon because the polygon must contain at least three points.

## Approaches

The brute-force idea follows the geometry directly. For every possible polygon size `k`, we try every possible starting position and check whether all vertices of that polygon contain `1`.

Suppose the polygon has `k` vertices. Then the step between consecutive vertices is `n / k`, so `k` must divide `n`. For each divisor `k ≥ 3`, we can test all `n` starting positions and walk through the entire cycle.

This works because every regular polygon on equally spaced points corresponds exactly to one of these cycles.

The problem is the running time. In the worst case, we may examine many divisors, and for each one we may scan almost all positions. A naive implementation can drift toward `O(n^2)`, which is too slow for `n = 10^5`.

The key observation is that we do not actually care about polygon sizes directly. What matters is the jump distance.

If we jump by some step `d`, the visited positions form a cycle whose length is:

$$\frac{n}{\gcd(n,d)}$$

We only care about cycles of length at least `3`. Every valid regular polygon corresponds to one such cycle.

Now consider a divisor `k` of `n`, where `k ≥ 3`. The polygon vertices are exactly:

$$i,\ i + \frac{n}{k},\ i + 2\frac{n}{k},\dots$$

So instead of checking arbitrary subsets, we only need to test divisors of `n`.

For each divisor `k ≥ 3`, let:

$$step = \frac{n}{k}$$

Then we test every residue class modulo `step`. If every element in one residue class is `1`, we found a valid polygon.

Each position participates in only a limited number of divisor checks, so the total complexity stays efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of knights and the mood array.
2. Enumerate all divisors `k` of `n` such that `k ≥ 3`.

A regular polygon with `k` vertices is only possible if `k` divides `n`, because the vertices must be equally spaced around the circle.
3. For each valid `k`, compute:

```
step = n // k
```

Jumping by `step` moves from one polygon vertex to the next.
4. Try every possible starting offset from `0` to `step - 1`.

Each offset represents one cycle of equally spaced positions.
5. For a fixed offset, walk through the cycle:

```
offset, offset + step, offset + 2*step, ...
```

modulo `n`.
6. Check whether every position in that cycle contains `1`.

If even one cycle consists entirely of `1`s, print `YES` immediately.
7. If all divisor configurations fail, print `NO`.

### Why it works

A regular polygon on equally spaced circular points must use vertices separated by a constant angular distance. Since the knights are equally spaced, this translates directly into a fixed index jump.

If a polygon has `k` vertices, then consecutive vertices differ by exactly `n / k` positions. The algorithm checks every possible divisor `k` and every possible starting position for that spacing.

Every valid polygon appears in exactly one of these checks, and every checked cycle corresponds to a valid regular polygon. Because the algorithm accepts only when all vertices in a cycle contain `1`, it cannot produce a false positive.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    divisors = []

    d = 1
    while d * d <= n:
        if n % d == 0:
            if d >= 3:
                divisors.append(d)

            other = n // d
            if other != d and other >= 3:
                divisors.append(other)

        d += 1

    for k in divisors:
        step = n // k

        for start in range(step):
            ok = True

            for pos in range(start, n, step):
                if a[pos] == 0:
                    ok = False
                    break

            if ok:
                print("YES")
                return

    print("NO")

solve()
```

The first part computes all divisors of `n` that could represent polygon sizes. We ignore divisors smaller than `3` because polygons with fewer than three vertices are invalid.

For each divisor `k`, the code derives the spacing between polygon vertices using `step = n // k`. This is the crucial geometric translation from polygon structure into array indices.

The nested loop over `start` handles different rotations of the same polygon pattern. For example, with `step = 3`, the sequences starting at `0`, `1`, and `2` are distinct cycles.

The innermost loop checks one complete cycle. Using `range(start, n, step)` is enough because the positions naturally wrap around the circle structure through modular spacing. Every position in that residue class belongs to the same polygon.

The early return is important for performance. The moment we find one valid polygon, no further work is needed.

A common implementation mistake is checking divisors of `step` instead of divisors of `n`. Another easy bug is forgetting that polygons using all `n` vertices are valid.

## Worked Examples

### Example 1

Input:

```
3
1 1 1
```

| k | step | start | Checked positions | All ones |
| --- | --- | --- | --- | --- |
| 3 | 1 | 0 | 0,1,2 | Yes |

The algorithm immediately finds that all three positions form a valid regular triangle. Since every knight is in a good mood, the answer is `YES`.

### Example 2

Input:

```
6
1 0 1 0 1 0
```

| k | step | start | Checked positions | All ones |
| --- | --- | --- | --- | --- |
| 3 | 2 | 0 | 0,2,4 | Yes |

The positions `0`, `2`, and `4` are equally spaced and all contain `1`. These vertices form an equilateral triangle on the circle.

This trace demonstrates the core invariant: positions separated by a constant step correspond exactly to a regular polygon.

### Example 3

Input:

```
6
1 1 1 0 0 0
```

| k | step | start | Checked positions | All ones |
| --- | --- | --- | --- | --- |
| 3 | 2 | 0 | 0,2,4 | No |
| 3 | 2 | 1 | 1,3,5 | No |
| 6 | 1 | 0 | 0,1,2,3,4,5 | No |

No equally spaced cycle contains only `1`s, so the answer is `NO`.

This case shows why simply counting good knights is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each divisor check scans arithmetic progressions whose total size remains manageable |
| Space | O(1) | Only a few auxiliary variables besides the input array |

The solution comfortably fits the constraints. Even for `n = 10^5`, the number of divisors is small, and each array position is revisited only across divisor-based scans.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())
        a = list(map(int, input().split()))

        divisors = []

        d = 1
        while d * d <= n:
            if n % d == 0:
                if d >= 3:
                    divisors.append(d)

                other = n // d
                if other != d and other >= 3:
                    divisors.append(other)

            d += 1

        for k in divisors:
            step = n // k

            for start in range(step):
                ok = True

                for pos in range(start, n, step):
                    if a[pos] == 0:
                        ok = False
                        break

                if ok:
                    return "YES"

        return "NO"

    return solve()

# provided sample
assert run("3\n1 1 1\n") == "YES", "sample 1"

# minimum valid polygon
assert run("3\n1 0 1\n") == "NO", "minimum size failure"

# equally spaced triangle
assert run("6\n1 0 1 0 1 0\n") == "YES", "alternating pattern"

# consecutive ones are not enough
assert run("6\n1 1 1 0 0 0\n") == "NO", "non-regular subset"

# all knights good
assert run("5\n1 1 1 1 1\n") == "YES", "whole polygon"

# only two opposite points
assert run("4\n1 0 1 0\n") == "NO", "degenerate polygon"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 1 0 1` | `NO` | Minimum size handling |
| `6 / 1 0 1 0 1 0` | `YES` | Correct cycle detection |
| `6 / 1 1 1 0 0 0` | `NO` | Rejects consecutive but non-regular subsets |
| `5 / 1 1 1 1 1` | `YES` | Whole-circle polygon |
| `4 / 1 0 1 0` | `NO` | Rejects 2-point degenerate case |

## Edge Cases

Consider the input:

```
6
1 1 1 0 0 0
```

The algorithm checks divisor `k = 3`, giving `step = 2`.

The cycles are:

```
0,2,4
1,3,5
```

The first cycle contains a `0` at position `4`. The second cycle contains `0`s at positions `3` and `5`. No valid polygon exists.

This case verifies that the algorithm requires equal spacing, not merely enough good knights.

Now consider:

```
5
1 1 1 1 1
```

The divisor `k = 5` produces `step = 1`.

The only cycle is:

```
0,1,2,3,4
```

Every position contains `1`, so the algorithm correctly accepts the full pentagon.

Finally, examine:

```
4
1 0 1 0
```

A careless implementation might accept because positions `0` and `2` are equally spaced. The algorithm rejects this because the only divisors checked are `k ≥ 3`.

For `n = 4`, the valid divisor is only `4`, producing `step = 1`. Since not all positions are `1`, the answer becomes `NO`.
