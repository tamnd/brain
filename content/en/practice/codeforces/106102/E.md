---
title: "CF 106102E - Pencil"
description: "The box is an M × N grid. The cell at row i and column j contains a pencil whose length is i · N + j. Rows and columns are zero-indexed, so the top-left cell contains length 0. For each test case we are given M, N, and a target length L."
date: "2026-06-25T11:49:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106102
codeforces_index: "E"
codeforces_contest_name: "AGM 2025, Final Round, Day 1"
rating: 0
weight: 106102
solve_time_s: 65
verified: true
draft: false
---

[CF 106102E - Pencil](https://codeforces.com/problemset/problem/106102/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

The box is an `M × N` grid. The cell at row `i` and column `j` contains a pencil whose length is `i · N + j`. Rows and columns are zero-indexed, so the top-left cell contains length `0`.

For each test case we are given `M`, `N`, and a target length `L`. We may choose any axis-aligned subrectangle of the grid and join together all pencils inside it. The total length of the resulting pencil is the sum of all values inside that subrectangle.

The task is to find a subrectangle whose sum is exactly `L`. If several such rectangles exist, we must output the smallest possible area. If no rectangle has sum `L`, we output `-1`.

The dimensions can be as large as `10^6`, while `L` can reach `10^12`. A brute-force scan over positions or rectangle sizes is completely impossible. Even iterating over all rows or all columns would already be too large.

The key observation is that the grid values form a very regular arithmetic structure. Instead of searching through positions, we can derive a closed formula for the sum of any rectangle and convert the problem into a number-theoretic search over divisors of `2L`.

A common mistake is to assume that only the rectangle dimensions matter. Two rectangles with the same height and width can have different sums because their starting positions differ.

Consider:

```
M = 3, N = 3

0 1 2
3 4 5
6 7 8
```

A `1 × 2` rectangle can have sums `1`, `3`, `5`, `7`, `9`, `11`.

The dimensions alone do not determine the sum.

Another subtle case appears when the computed starting position lands outside the grid.

```
M = 2, N = 3, L = 8
```

The rectangle with area `4` exists and works, but some algebraically valid solutions correspond to a top-left corner beyond the allowed range. The geometric bounds must still be checked.

## Approaches

A brute-force solution would enumerate every subrectangle and compute its sum.

There are `O(M²N²)` subrectangles. With dimensions up to `10^6`, that is hopeless. Even storing the grid is impossible.

The structure of the grid is what saves us. Every value is

```
value(i, j) = iN + j
```

Suppose a rectangle starts at `(r, c)` and has height `h` and width `w`.

Its area is

```
A = h · w
```

Summing the arithmetic progressions gives

```
sum = A · ( N(2r + h - 1) + (2c + w - 1) ) / 2
```

Define

```
B = N(h - 1) + (w - 1)
x = Nr + c
```

Then

```
sum = A(2x + B)/2
```

For a target value `L`:

```
2L = A(2x + B)
```

This immediately implies that the area `A` must divide `2L`.

That changes the problem completely. Instead of searching over positions in a huge grid, we enumerate divisors of `2L`. The number of divisors of a number up to `2 · 10^12` is only a few thousand.

For a candidate area `A`, we try every factorization

```
A = h · w
```

with `h ≤ M` and `w ≤ N`.

Rearranging the equation gives

```
x = (2L/A - B)/2
```

If `x` is a non-negative integer, we recover

```
r = x // N
c = x % N
```

and simply verify that

```
r ≤ M - h
c ≤ N - w
```

If any factorization works, then area `A` is achievable. Since we test areas in increasing order, the first valid one is the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(M²N²) | O(1) | Too slow |
| Optimal | Roughly O(d²) where d is the number of divisors of 2L | O(d) | Accepted |

## Algorithm Walkthrough

1. Compute `S = 2L`.
2. Factorize `S`.
3. Generate all divisors of `S` and sort them in increasing order.
4. For each divisor `A` of `S`, treat it as a candidate rectangle area.
5. Enumerate every factorization `A = h · w`.
6. Skip any pair where `h > M` or `w > N`.
7. Compute

```
Q = S / A
B = N(h - 1) + (w - 1)
```
8. Check whether

```
Q - B
```

is non-negative and even.

Otherwise the corresponding starting position cannot be integral.
9. Recover

```
x = (Q - B)/2
r = x // N
c = x % N
```
10. Verify that the rectangle fits:

```
r ≤ M - h
c ≤ N - w
```
11. As soon as one valid rectangle is found, output `A`.
12. If no area works, output `-1`.

### Why it works

The sum formula

```
L = A(2x + B)/2
```

is an exact characterization of every rectangle.

For a fixed height and width, the quantity `B` is fixed. The only remaining freedom is the starting position, represented by `x = Nr + c`.

Rearranging the equation gives a unique candidate value of `x`. If that value is not a valid grid position, then no rectangle with those dimensions can produce the target sum. If it is valid, the corresponding rectangle produces exactly `L`.

The algorithm checks every possible area dividing `2L` and every possible factorization of that area. Since every valid rectangle must satisfy these conditions, no solution can be missed. Testing areas in ascending order guarantees that the first valid one has minimum area.

## Python Solution

```python
import sys
input = sys.stdin.readline

def factorize(x):
    fac = []
    d = 2

    while d * d <= x:
        if x % d == 0:
            cnt = 0
            while x % d == 0:
                x //= d
                cnt += 1
            fac.append((d, cnt))
        d += 1 if d == 2 else 2

    if x > 1:
        fac.append((x, 1))

    return fac

def gen_divisors(factors, idx=0, cur=1, out=None):
    if out is None:
        out = []

    if idx == len(factors):
        out.append(cur)
        return out

    p, e = factors[idx]
    val = 1

    for _ in range(e + 1):
        gen_divisors(factors, idx + 1, cur * val, out)
        val *= p

    return out

t = int(input())

for _ in range(t):
    M, N, L = map(int, input().split())

    S = 2 * L

    factors = factorize(S)
    divisors = gen_divisors(factors)
    divisors.sort()

    answer = -1

    for A in divisors:
        found = False

        for h in divisors:
            if h * h > A:
                break

            if A % h:
                continue

            w = A // h

            for hh, ww in ((h, w), (w, h) if h != w else ()):
                if hh > M or ww > N:
                    continue

                Q = S // A
                B = N * (hh - 1) + (ww - 1)

                diff = Q - B

                if diff < 0 or diff & 1:
                    continue

                x = diff // 2

                r = x // N
                c = x % N

                if r <= M - hh and c <= N - ww:
                    answer = A
                    found = True
                    break

            if found:
                break

        if found:
            break

    print(answer)
```

The first part factorizes `2L`. From that factorization we generate all divisors.

The outer loop tests candidate areas in increasing order. Since we only care about the smallest feasible area, the search can stop immediately when a valid rectangle is found.

For each area, we enumerate all factor pairs `(h, w)`. The algebra gives the unique possible starting index `x`. Converting

```
x = Nr + c
```

back into `(r, c)` is straightforward using integer division and remainder.

The most common implementation mistake is forgetting the geometric check

```
r ≤ M - h
c ≤ N - w
```

A value of `x` may satisfy the equation but still correspond to a rectangle extending outside the box.

## Worked Examples

### Example 1

Input:

```
M = 2, N = 3, L = 8
```

The smallest valid area is `4`.

| A | h | w | Q | B | x | r | c | Valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 16 | 0 | 8 | 2 | 2 | No |
| 2 | 1 | 2 | 8 | 1 | invalid | - | - | No |
| 4 | 2 | 2 | 4 | 4 | 0 | 0 | 0 | Yes |

The rectangle is:

```
0 1
3 4
```

whose sum is `8`.

### Example 2

Input:

```
M = 3, N = 3, L = 36
```

| A | h | w | Q | B | x | r | c | Valid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 72 | 0 | 36 | out | - | No |
| 3 | 1 | 3 | 24 | 2 | 11 | out | - | No |
| 9 | 3 | 3 | 8 | 8 | 0 | 0 | 0 | Yes |

The whole grid is selected:

```
0 1 2
3 4 5
6 7 8
```

and its sum is `36`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d²) | `d` is the number of divisors of `2L` |
| Space | O(d) | storing divisors |

For numbers up to `2 · 10^12`, the divisor count is only a few thousand in the worst case. This is tiny compared to the grid dimensions, which may reach `10^6`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def factorize(x):
        fac = []
        d = 2
        while d * d <= x:
            if x % d == 0:
                c = 0
                while x % d == 0:
                    x //= d
                    c += 1
                fac.append((d, c))
            d += 1 if d == 2 else 2
        if x > 1:
            fac.append((x, 1))
        return fac

    def gen(fac, i=0, cur=1, out=None):
        if out is None:
            out = []
        if i == len(fac):
            out.append(cur)
            return out
        p, e = fac[i]
        v = 1
        for _ in range(e + 1):
            gen(fac, i + 1, cur * v, out)
            v *= p
        return out

    t = int(input())
    ans = []

    for _ in range(t):
        M, N, L = map(int, input().split())
        S = 2 * L

        divs = gen(factorize(S))
        divs.sort()

        res = -1

        for A in divs:
            ok = False

            for h in divs:
                if h * h > A:
                    break
                if A % h:
                    continue

                w = A // h

                pairs = [(h, w)]
                if h != w:
                    pairs.append((w, h))

                for hh, ww in pairs:
                    if hh > M or ww > N:
                        continue

                    Q = S // A
                    B = N * (hh - 1) + (ww - 1)

                    diff = Q - B

                    if diff < 0 or diff % 2:
                        continue

                    x = diff // 2
                    r = x // N
                    c = x % N

                    if r <= M - hh and c <= N - ww:
                        res = A
                        ok = True
                        break

                if ok:
                    break

            if ok:
                break

        ans.append(str(res))

    return "\n".join(ans)

# sample-style cases
assert solve("1\n2 3 8\n") == "4"

# minimum grid
assert solve("1\n1 1 1\n") == "-1"

# whole grid
assert solve("1\n3 3 36\n") == "9"

# single cell exists
assert solve("1\n2 2 3\n") == "1"

# impossible target
assert solve("1\n3 3 10\n") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `-1` | Cell value 1 does not exist |
| `3 3 36` | `9` | Whole-grid solution |
| `2 2 3` | `1` | Single-cell rectangle |
| `3 3 10` | `-1` | No matching rectangle |

## Edge Cases

Consider:

```
1
1 1 1
```

The grid contains only one value:

```
0
```

The algorithm tests area `1`, computes the corresponding position, and finds that no rectangle can sum to `1`. It outputs `-1`.

Consider:

```
1
2 2 3
```

The cell `(1,0)` contains value `2`, and `(1,1)` contains value `3`.

For area `1`, the formula gives a valid starting position corresponding exactly to value `3`. The algorithm immediately returns `1`, which is optimal.

Consider:

```
1
2 3 8
```

A careless implementation might find an algebraic solution whose top-left corner lies outside the grid. The reconstruction step

```
r = x // N
c = x % N
```

followed by

```
r ≤ M - h
c ≤ N - w
```

eliminates those false positives and keeps only geometrically valid rectangles.
