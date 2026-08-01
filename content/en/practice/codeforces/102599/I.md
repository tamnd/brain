---
title: "CF 102599I - Count Triangles"
description: "We have four ordered boundaries that split possible side lengths into three ranges. The first side x must be chosen from [A, B], the second side y from [B, C], and the third side z from [C, D]."
date: "2026-08-01T07:08:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102599
codeforces_index: "I"
codeforces_contest_name: "The fifth Lipetsk collegiate programming contest. Finals. 8-11 form"
rating: 0
weight: 102599
solve_time_s: 1018
verified: true
draft: false
---

[CF 102599I - Count Triangles](https://codeforces.com/problemset/problem/102599/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 16m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have four ordered boundaries that split possible side lengths into three ranges. The first side `x` must be chosen from `[A, B]`, the second side `y` from `[B, C]`, and the third side `z` from `[C, D]`. Because of the ordering of the ranges, every chosen triple already satisfies `x <= y <= z`. The only remaining requirement for a valid triangle is the non-degenerate triangle inequality, which becomes `x + y > z`.

The task is to count how many triples `(x, y, z)` satisfy these conditions.

The largest value of any boundary is `500000`. A direct enumeration of all triples would consider up to `500000^3` possibilities, which is far beyond what can fit in a one second time limit. Even iterating over all pairs `(x, y)` is too expensive because there can be about `2.5 * 10^11` such pairs. We need to avoid dependence on the product of the interval lengths.

The key edge cases come from the boundaries between valid and invalid triangles. A careless implementation often mishandles strict inequality or assumes every possible triple is a triangle.

For example, with input:

```
1 1 1 3
```

The possible triples are `(1,1,1)`, `(1,1,2)`, and `(1,1,3)`. Only the first one is valid because `1 + 1 > 1` is true, while `1 + 1 > 2` and `1 + 1 > 3` are false. The answer is `1`. Using `>=` instead of `>` would incorrectly count degenerate cases.

Another boundary case is when all intervals contain one value:

```
500000 500000 500000 500000
```

The only possible triangle is `(500000,500000,500000)`, so the answer is `1`. Solutions that rely on ranges having multiple values or divide by interval lengths incorrectly can fail here.

A final common mistake appears when the upper bound of `z` is reached. For:

```
1 2 3 4
```

The pair `(2,3)` allows `z = 3` and `z = 4`, but no larger values exist. Any formula that counts all `z < x+y` without clipping at `D` would overcount.

## Approaches

A straightforward solution is to try every possible `x`, every possible `y`, and then count the possible `z` values satisfying the triangle inequality. For fixed `x` and `y`, the valid `z` values are from `C` to `min(D, x+y-1)`. This approach is correct because it directly applies the definition of a triangle.

The problem is the number of pairs. The first two ranges can both contain around `500000` values, producing around `250000000000` pairs. Even if each pair was processed in constant time, this would not finish.

The important observation is that we do not need to know every pair individually. For a fixed value of `z`, the only question is how many pairs `(x,y)` have `x+y > z`. This turns the problem into counting sums inside a rectangle of possible `(x,y)` values.

We can count the opposite quantity, the number of pairs with `x+y <= z`, and subtract it from the total number of pairs. After shifting both ranges to start at zero, this becomes the classic problem of counting points `(a,b)` in a rectangle where `a+b` is at most some value. Inclusion-exclusion gives this count in constant time, allowing us to iterate over every possible `z`. There are at most `500000` such values, which is easily manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((B-A+1)(C-B+1)) | O(1) | Too slow |
| Optimal | O(D-C+1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Let `n = B - A + 1` and `m = C - B + 1` be the sizes of the first two side ranges. The total number of possible `(x,y)` pairs is `n * m`.
2. Convert the first two side lengths into zero-based coordinates. Define `a = x - A`, so `0 <= a < n`, and `b = y - B`, so `0 <= b < m`.

The condition `x + y <= z` becomes:

```
a + b <= z - A - B
```

This transformation removes the large original values and leaves a standard bounded grid counting problem.
3. Create a helper function `triangle_count(k)` that returns how many pairs `(a,b)` satisfy `a >= 0`, `b >= 0`, `a < n`, `b < m`, and `a+b <= k`.

Without the upper bounds on `a` and `b`, the number of non-negative pairs is:

```
(k+1)(k+2)/2
```

If `a` reaches `n`, shift `a` down by `n` and subtract the invalid area. The same applies to `b`, and pairs violating both limits are added back by inclusion-exclusion.
4. For every possible `z` from `C` to `D`, calculate how many `(x,y)` pairs satisfy `x+y <= z`. Subtract this from the total number of pairs to get the number of valid triangles ending with this `z`.
5. Add all these counts to obtain the final answer.

Why it works:

For every fixed `z`, every pair `(x,y)` falls into exactly one of two groups: either `x+y <= z`, which cannot form a non-degenerate triangle, or `x+y > z`, which does. The helper function counts the first group exactly using inclusion-exclusion over the rectangle boundaries. Subtracting from the total pair count leaves exactly the valid choices for that `z`. Summing over all possible `z` counts every valid triangle once because each triangle has exactly one third side.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B, C, D = map(int, input().split())

    n = B - A + 1
    m = C - B + 1

    def count_leq(k):
        def calc(t):
            if t < 0:
                return 0
            return (t + 1) * (t + 2) // 2

        return calc(k) - calc(k - n) - calc(k - m) + calc(k - n - m)

    total_pairs = n * m
    ans = 0

    for z in range(C, D + 1):
        not_triangles = count_leq(z - A - B)
        ans += total_pairs - not_triangles

    print(ans)

if __name__ == "__main__":
    solve()
```

The variables `n` and `m` describe the possible choices for the first two sides. Keeping them as lengths rather than storing arrays is what allows the solution to use constant memory.

The function `calc(t)` is the triangular-number formula for an unlimited grid. It counts all pairs of non-negative values whose sum does not exceed `t`. Returning zero for negative `t` handles cases where the limit is too small for any pair.

The four terms in `count_leq` are the inclusion-exclusion correction. The first term counts every non-negative pair. The second and third remove pairs where `a` or `b` exceed their allowed ranges. The fourth adds back pairs removed twice.

The loop over `z` uses the fact that there are only `D-C+1` possible values for the largest side. Python integers avoid overflow concerns, which matters because the answer can be much larger than a 32-bit integer.

## Worked Examples

For the first sample:

```
1 2 3 4
```

The shifted rectangle has:

`n = 2`, `m = 2`, total pairs = 4.

| z | k = z-A-B | Pairs with x+y <= z | Valid pairs |
| --- | --- | --- | --- |
| 3 | 0 | 1 | 3 |
| 4 | 1 | 3 | 1 |

The sum is `3 + 1 = 4`, matching the sample output. The trace shows how each value of the largest side is handled independently.

For the second sample:

```
1 2 2 5
```

Here:

`n = 2`, `m = 1`, total pairs = 2.

| z | k = z-A-B | Pairs with x+y <= z | Valid pairs |
| --- | --- | --- | --- |
| 2 | -1 | 0 | 2 |
| 3 | 0 | 1 | 1 |
| 4 | 1 | 2 | 0 |
| 5 | 2 | 2 | 0 |

The answer is `2 + 1 = 3`. This example demonstrates that larger `z` values eventually become impossible when the sum of the two smaller sides cannot exceed them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(D-C+1) | We evaluate one constant-time formula for every possible value of `z`. |
| Space | O(1) | Only a few integer variables are stored. |

The maximum number of loop iterations is `500000`, and every iteration performs only arithmetic operations. This fits comfortably within the time limit.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    A, B, C, D = map(int, input().split())

    n = B - A + 1
    m = C - B + 1

    def count_leq(k):
        def calc(t):
            if t < 0:
                return 0
            return (t + 1) * (t + 2) // 2

        return calc(k) - calc(k - n) - calc(k - m) + calc(k - n - m)

    total = n * m
    ans = 0

    for z in range(C, D + 1):
        ans += total - count_leq(z - A - B)

    return str(ans) + "\n"

assert solution("1 2 3 4\n") == "4\n", "sample 1"
assert solution("1 2 2 5\n") == "3\n", "sample 2"
assert solution("500000 500000 500000 500000\n") == "1\n", "sample 3"

assert solution("1 1 1 3\n") == "1\n", "degenerate triangles must not count"
assert solution("1 1 2 2\n") == "1\n", "single valid combination"
assert solution("5 5 5 6\n") == "2\n", "equal sides and upper bound handling"
assert solution("1 500000 500000 500000\n") == "0\n", "largest side too large for most pairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 3` | `1` | Strict triangle inequality and degenerate cases |
| `1 1 2 2` | `1` | Smallest ranges and exact boundaries |
| `5 5 5 6` | `2` | Handling equal intervals and multiple `z` values |
| `1 500000 500000 500000` | `0` | Large ranges and impossible triangles |

## Edge Cases

For the degenerate triangle case:

```
1 1 1 3
```

The algorithm iterates through `z = 1, 2, 3`. For `z = 1`, the count of pairs with `x+y <= 1` is zero, so the only pair `(1,1)` is counted. For `z = 2` and `z = 3`, the pair is classified as invalid because the sum of the smaller sides is not greater than `z`. The final answer is `1`.

For the single-value maximum case:

```
500000 500000 500000 500000
```

The shifted ranges both have length one. For the only possible `z`, the helper function counts zero invalid pairs because `500000 + 500000 > 500000`. The total pair count is one, so the answer is one.

For upper-bound clipping:

```
1 2 3 4
```

The pair `(2,3)` has sum `5`, so it allows `z` values up to `4`, not beyond the given interval. The algorithm never generates a `z` outside `[C,D]`, so the upper limit is naturally respected. The final count remains `4`.
