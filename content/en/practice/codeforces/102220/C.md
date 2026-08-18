---
title: "CF 102220C - Line-line Intersection"
description: "We have n infinite straight lines in the plane. Each line is described by two distinct points, so the input gives four integers for every line. We need to count pairs of lines that have at least one common point. Two non-parallel infinite lines always intersect exactly once."
date: "2026-08-19T00:18:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102220
codeforces_index: "C"
codeforces_contest_name: "The 13th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102220
solve_time_s: 196
verified: true
draft: false
---

[CF 102220C - Line-line Intersection](https://codeforces.com/problemset/problem/102220/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We have n infinite straight lines in the plane. Each line is described by two distinct points, so the input gives four integers for every line. We need to count pairs of lines that have at least one common point.

Two non-parallel infinite lines always intersect exactly once. Two parallel lines normally never intersect, but there is one exception: if they are actually the same geometric line, they have infinitely many common points and the pair must be counted.

The official problem has n≤10 5 per test case and ∑n≤10 6. The official limits are 6 seconds and 512 MB.  A direct comparison of every pair takes O(n 2 ) operations. At n=10 5, that is

2 100000⋅99999 ​ =4,999,950,000

pairs, which is far beyond what we can process in a typical contest time limit. The total bound of 10 6 input lines also means the solution should be close to O(nlogn), or preferably expected O(n), over all test cases.

The first subtle case is overlapping lines. Consider

```
1
2
0 0 1 1
0 0 2 2
```

Both descriptions represent y=x, so the answer is `1`. A solution that treats every pair of parallel lines as non-intersecting would incorrectly output `0`.

The second subtle case is two distinct parallel lines. For example,

```

```

These are x=0 and x=1, so the answer is `0`. A solution that only checks whether the direction vectors are equal without distinguishing the actual line would count this pair incorrectly.

The third subtle case is that the same geometric line can be given with its two endpoints reversed. For example,

```

```

Both lines are y=x, so the answer is `1`. A raw representation such as (dx,dy,c) without fixing its sign can represent these two copies using opposite triples and fail to recognize that they are identical.

## Approaches

The brute-force solution considers every pair of lines and determines whether they intersect. Two lines intersect if their direction vectors are not proportional, or if they are proportional and both equations describe the same line. This is correct because the only way two infinite lines fail to share a point is for them to be distinct and parallel.

The problem is the number of pairs. With 10 5 lines there are almost five billion pairs, so even a constant-time geometric test per pair is too slow. The brute-force method has O(n 2 ) time and cannot exploit the fact that many pairs have the same geometric relationship.

The key observation is that every pair of non-parallel lines contributes to the answer. The only pairs we need to exclude are pairs of distinct parallel lines. This changes the problem from checking every pair of lines into grouping lines by direction.

For one direction, suppose there are k lines. There are ( 2 k ​ ) pairs among them. Every such pair would be excluded because the lines are parallel, except pairs that are actually the same geometric line. If a particular geometric line occurs c times in the input, its ( 2 c ​ ) copies should be added back.

We can process this incrementally. When the current line is the i-th line, there are i−1 previous lines, and initially we pretend that it intersects all of them. If p previous lines have the same direction, while q of those are actually the same geometric line, then p−q previous lines are distinct and parallel, so exactly those pairs must be removed. The current line contributes

(i−1)−(p−q)

new intersecting pairs.

The remaining task is representing a line canonically with integers. For points (x 1 ​ ,y 1 ​ ) and (x 2 ​ ,y 2 ​ ), we can write

Ax+By=C

where

A=y 1 ​ −y 2 ​ ,B=x 2 ​ −x 1 ​ ,C=Ax 1 ​ +By 1 ​ .

We divide A,B,C by gcd(∣A∣,∣B∣), then choose a fixed sign for (A,B,C). The pair (A,B) identifies a direction family, while (A,B,C) identifies one exact geometric line.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n 2 ) | O(1) | Too slow |
| Optimal | Expected O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the two input points of the current line into an equation Ax+By=C. The coefficients A and B are obtained directly from the coordinate differences, so no floating-point slope is needed.
2. Divide all three coefficients by gcd(∣A∣,∣B∣). This removes arbitrary scaling, so equations such as 2x+2y=4 and x+y=2 receive the same normalized representation.
3. Fix the sign of the normalized coefficients. If A<0, multiply all three by −1. If A=0, require B>0, again multiplying by −1 when necessary. This makes reversed endpoints produce exactly the same representation.
4. Use (A,B) as the key of a direction-frequency map. Every line with this key is parallel to every other line with the key, including copies of the same line.
5. Use (A,B,C) as the key of an exact-line-frequency map. Two lines have the same key precisely when they are the same geometric line.
6. Before inserting the current line into either map, let `same_direction` be the number of previous lines with the same (A,B), and let `same_line` be the number of previous copies of the exact (A,B,C).
7. Add

(i−1)−same_direction+same_line

to the answer, where i is the current one-based index. The first term assumes the current line intersects every previous line. The second removes previous lines that are parallel and distinct. The third restores previous copies that lie on exactly the same geometric line.

1. Increment both frequency maps. After processing all lines, the accumulated value is the required number of intersecting pairs.

### Why it works

At the moment a line is processed, every previous line either intersects it or is distinct and parallel to it. The number of previous lines is i−1. Among them, `same_direction` lines are parallel to the current line, but `same_line` of those are actually the same geometric line and therefore do intersect. Thus exactly `same_direction - same_line` previous lines fail to intersect. The algorithm adds all other pairs and never counts a non-intersecting pair, so every pair is counted exactly once.

## Python Solution

```
Python
```

The first part of the loop constructs the implicit equation of the line. Using A=y 1 ​ −y 2 ​ and B=x 2 ​ −x 1 ​ gives a normal vector to the line, so the equation is valid for vertical and horizontal lines without special cases.

The greatest common divisor removes the common scale factor. Because A and B are already a normal vector, dividing by gcd(∣A∣,∣B∣) is sufficient to make the direction primitive. The same divisor also has to be applied to C.

The sign normalization is essential. Without it, the input

```

```

would produce coefficients with the opposite sign from

```

```

even though both describe the same line.

The two dictionaries serve different purposes. `direction_count` tells us how many previous lines are parallel to the current one. `line_count` tells us how many of those parallel lines are actually identical to it.

The expression

```
Python
```

uses zero-based `i`. At iteration `i`, exactly `i` lines have already been processed. We remove all `same_direction` parallel lines and restore the `same_line` coincident copies.

Python integers have arbitrary precision, so products such as `A * x1` do not overflow. This matters because the coordinates can have absolute value up to 10 9, making the intermediate value for C as large as roughly 2⋅10 18.

The dictionaries are recreated for every test case. Since each test case has at most 10 5 lines, this keeps memory proportional to the largest individual test case rather than the full 10 6 lines across all cases.

## Worked Examples

The official sample contains three test cases: two crossing diagonal lines, two distinct vertical lines, and two identical diagonal lines.

For the first test case,

```

```

the normalized lines are x−y=0 and x+y=1.

| Current line | Direction key | Exact line key | Same direction | Same line | Added pairs | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| y=x | `(1, -1)` | `(1, -1, 0)` | 0 | 0 | 0 | 0 |
| x+y=1 | `(1, 1)` | `(1, 1, 1)` | 0 | 0 | 1 | 1 |

The direction keys differ, so the second line is not parallel to the first. The pair is counted, producing `1`.

For the second test case,

```

```

the lines are x=0 and x=1.

| Current line | Direction key | Exact line key | Same direction | Same line | Added pairs | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| x=0 | `(1, 0)` | `(1, 0, 0)` | 0 | 0 | 0 | 0 |
| x=1 | `(1, 0)` | `(1, 0, 1)` | 1 | 0 | 0 | 0 |

The second line has the same direction but a different exact-line key. It is parallel and distinct, so the potential pair is removed.

For the third test case,

```

```

both inputs describe exactly the same line.

| Current line | Direction key | Exact line key | Same direction | Same line | Added pairs | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| y=x | `(1, -1)` | `(1, -1, 0)` | 0 | 0 | 0 | 0 |
| y=x | `(1, -1)` | `(1, -1, 0)` | 1 | 1 | 1 | 1 |

The pair first appears to be parallel, but `same_line` restores it because coincident lines share infinitely many points.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | Expected O(n) per test case | Each line performs constant expected-time dictionary operations and one GCD computation |
| Space | O(n) | The two frequency dictionaries contain at most n distinct direction and line keys |

Across all test cases, the expected running time is O(∑n), apart from the logarithmic cost of the integer GCD operations, and ∑n≤10 6. The largest individual test case has only 10 5 lines, so the two dictionaries remain manageable under the official 512 MB memory limit.

## Test Cases

```
Python
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 0 0 1 1` | `0` | Minimum input and absence of self-pairs |
| Four copies of y=x | `6` | Every coincident pair must be counted |
| Four distinct vertical lines | `0` | Parallel but non-coincident lines must be excluded |
| Reversed endpoints plus other directions | `5` | Canonical sign normalization and mixed relationships |
| Coordinates of magnitude 10 9 | `3` | Large integer arithmetic and boundary coordinates |

## Edge Cases

For coincident lines, consider

```

```

The first line produces one normalized equation key. The second line produces the same key after sign normalization, despite its endpoints being reversed. Before processing the second line, `same_direction = 1` and `same_line = 1`, so the contribution is 1−1+1=1. The final answer is `1`.

For distinct parallel lines, consider

```

```

Both lines have direction key `(1, 0)`, but their exact keys have different values of C. The second line sees `same_direction = 1` and `same_line = 0`, giving a contribution of 1−1=0. The final answer is `0`.

For several copies of the same line mixed with parallel lines, consider

```

```

The first two lines are the same geometric line, the third is parallel to them but distinct, and the fourth is vertical. When the second line arrives, its contribution is 1−1+1=1, because it coincides with the first. When the third arrives, there are two previous lines with the same direction but only one exact-line copy, so its contribution is 2−2+0=0. The fourth line has a different direction and intersects all three previous lines, contributing `3`. The final answer is `4`.

The sign normalization also handles vertical lines correctly. For a vertical line, A is nonzero and B=0, so the canonical form is simply Ax=C with A>0. There is no division by zero because the two input points are guaranteed to be distinct, so A and B cannot both be zero.
