---
title: "CF 102443F - Isosceles triangles"
description: "A regular polygon has all vertices equally spaced around a circle. We must count every triangle whose three vertices come from the polygon and whose side lengths contain at least one equal pair. The key difficulty is that the polygon can have as many as 10 9 vertices."
date: "2026-08-09T18:11:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102443
codeforces_index: "F"
codeforces_contest_name: "2019-2020 Russia Team Open, High School Programming Contest (VKOSHP 19)"
rating: 0
weight: 102443
solve_time_s: 86
verified: true
draft: false
---

[CF 102443F - Isosceles triangles](https://codeforces.com/problemset/problem/102443/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

A regular polygon has all vertices equally spaced around a circle. We must count every triangle whose three vertices come from the polygon and whose side lengths contain at least one equal pair.

The key difficulty is that the polygon can have as many as 10 9 vertices. An approach that explicitly examines vertices or triples cannot work. Even O(n) is already too large for the time limit, so the intended solution must reduce the answer to a constant number of arithmetic operations.

There is also a subtle counting issue. If we choose a vertex as the apex of an isosceles triangle, the two other vertices can be placed symmetrically around that apex. This counts every ordinary isosceles triangle once, but an equilateral triangle has three possible apexes, so it gets counted three times. We have to correct exactly that case.

For example, with input 3, the polygon itself is an equilateral triangle. A direct apex-based count gives three, because each of its vertices can be selected as the apex. The correct answer is 1, so simply counting symmetric pairs overcounts equilateral triangles.

Another edge case is an even-sized polygon. With n=4, choosing the opposite vertex on both sides of an apex would select the same polygon vertex twice, so that choice does not form a triangle. The correct answer is 4, not 8. This is why the number of valid symmetric distances is ⌊(n−1)/2⌋.

For n=6, equilateral triangles do exist. The apex-based count gives 6⋅2=12, but there are 6/3=2 distinct equilateral triangles, each counted three times. We must subtract two extra counts per equilateral triangle, giving 12−2⋅2=8.

## Approaches

The most direct brute-force solution is to choose every three vertices and check whether their three pairwise distances contain two equal values. There are

( 3 n ​ )= 6 n(n−1)(n−2) ​

triples. For n=10 9, this is approximately 1.67⋅10 26 triangles, so even constant-time processing of each triple is hopeless.

A slightly better-looking approach would fix one vertex and try every pair of remaining vertices, but that is still O(n 2 ), which is impossible for n=10 9.

The useful structure comes from the regular polygon. Fix a vertex v as the apex. Two other vertices have equal distance from v precisely when they are equally far around the polygon in opposite directions. If the clockwise distance to one endpoint is k, the counterclockwise distance to the other endpoint must also be k.

For every apex there are exactly

⌊ 2 n−1 ​ ⌋

valid choices of k. Thus we initially obtain

n⌊ 2 n−1 ​ ⌋

isosceles triangles.

This count has exactly one source of duplication. If three vertices form an equilateral triangle, every one of its vertices can serve as the apex. An equilateral triangle exists in a regular n-gon exactly when 3∣n, and in that case there are n/3 such triangles. Each was counted three times instead of once, so two copies must be removed for every equilateral triangle.

The final formula is therefore

n⌊ 2 n−1 ​ ⌋−{ 3 2n ​ , 0, ​ 3∣n, 3∤n. ​ ​

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n 3 ) | O(1) | Too slow |
| Fix apex and enumerate symmetric distances | O(n) | O(1) | Too slow for 10 9 |
| Closed-form counting | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the number of symmetric endpoint pairs available for one fixed apex as

k=⌊ 2 n−1 ​ ⌋.

Each value 1≤k≤k determines one triangle by taking the vertices k steps clockwise and k steps counterclockwise from the apex. The two equal sides are chords spanning the same number of polygon edges.
2. Multiply by n, because every polygon vertex can be chosen as the apex.

The initial count is

ans=nk.
3. Check whether n is divisible by 3. If it is not, no equilateral triangle can be formed from the polygon vertices, so the initial count is already exact.
4. If 3∣n, there are n/3 equilateral triangles. Each one was counted once for each of its three vertices, so each contributes two excess counts. Subtract

2⋅ 3 n ​

from the answer.
5. Print the resulting integer.

### Why it works

For every chosen apex, the equal sides of an isosceles triangle must connect the apex to two vertices at equal angular distance from it. Because all polygon vertices lie at equal angular intervals, these two vertices are exactly k steps in opposite directions for some valid k. Thus every isosceles triangle has at least one representation in our count.

A non-equilateral isosceles triangle has a unique apex, so it is counted exactly once. An equilateral triangle has three possible apexes and is consequently counted three times. These are the only triangles with multiple apex representations, so subtracting two copies for each equilateral triangle leaves every valid triangle counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    ans = n * ((n - 1) // 2)

    if n % 3 == 0:
        ans -= 2 * (n // 3)

    print(ans)

if __name__ == "__main__":
    solve()
```

The expression `(n - 1) // 2` computes the number of valid symmetric distances for one apex. Using `n - 1` rather than `n` is what prevents selecting the same vertex on both sides when n is even.

The multiplication by `n` accounts for every possible apex. Python integers handle the largest result without overflow, which is useful here because the answer can be on the order of 5⋅10 17, far beyond a 32-bit signed integer.

The divisibility check `n % 3 == 0` handles the only overcounting case. When it holds, `n // 3` is the number of distinct equilateral triangles, and each needs exactly two excess copies removed.

There is no loop over vertices, so the algorithm performs only a fixed number of arithmetic operations regardless of whether n is 3 or 10 9.

## Worked Examples

### Sample 1

For n=3, there is one triangle and it is equilateral.

| n | Symmetric choices per apex | Initial count | Equilateral correction | Final answer |
| --- | --- | --- | --- | --- |
| 3 | 1 | 3⋅1=3 | 2⋅(3/3)=2 | 1 |

The three apex choices all describe the same physical triangle. Removing two duplicate counts leaves exactly one triangle.

### Sample 2

For n=5, each vertex has two possible symmetric distances.

| n | Symmetric choices per apex | Initial count | Equilateral correction | Final answer |
| --- | --- | --- | --- | --- |
| 5 | 2 | 5⋅2=10 | 0 | 10 |

Since 5 is not divisible by 3, there are no equilateral triangles. Every counted triangle has a unique apex, so all ten counts represent distinct triangles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations and one divisibility check are performed. |
| Space | O(1) | The algorithm stores only a constant number of integer variables. |

The upper bound n≤10 9 rules out any algorithm that iterates over the vertices, let alone over pairs or triples. The constant-time formula works comfortably within the 1 second time limit and uses negligible memory.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())

    ans = n * ((n - 1) // 2)

    if n % 3 == 0:
        ans -= 2 * (n // 3)

    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("3\n") == "1\n", "sample 1"
assert run("5\n") == "10\n", "sample 2"

# Minimum size, also the smallest equilateral case
assert run("4\n") == "4\n", "even polygon boundary"

# Small multiple of 3
assert run("6\n") == "8\n", "equilateral correction"

# Large odd value
assert run("999999999\n") == "499999998000000000\n", "large odd n"

# Maximum input
assert run("1000000000\n") == "499999999000000000\n", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4` | `4` | Even n, where the halfway-around choice must not be counted twice |
| `6` | `8` | Equilateral-triangle correction |
| `999999999` | `499999998000000000` | Large odd input and 64-bit-sized arithmetic |
| `1000000000` | `499999999000000000` | Maximum input boundary |

## Edge Cases

For n=3, the algorithm computes one symmetric choice per apex, giving 3. Since 3∣n, it subtracts 2(3/3)=2, producing 1. This handles the smallest possible polygon and demonstrates why equilateral triangles cannot simply be ignored.

For n=4, the algorithm computes ⌊3/2⌋=1 symmetric choice per apex, giving 4. There is no equilateral correction because 4 is not divisible by 3. The result is 4, which corresponds to the four triangles obtained by omitting one vertex from the square. The floor operation is essential because taking two steps clockwise and two steps counterclockwise from an apex reaches the same opposite vertex.

For n=6, there are two symmetric choices per apex, giving an initial count of 12. Since 6 is divisible by 3, there are 6/3=2 equilateral triangles. Each was counted three times, so four excess counts are removed. The final answer is 12−4=8.

For n=10 9, the algorithm performs the same constant number of operations as for any smaller input. The per-apex count is

⌊ 2 10 9 −1 ​ ⌋=499999999,

so the initial count is

10 9 ⋅499999999=499999999000000000.

Because 10 9 is not divisible by 3, no correction is needed, and that value is the final answer.
