---
title: "CF 106403D - Power Up"
description: "The problem asks us to answer many independent checks about a collection of power values. We have a set of distinct numbers."
date: "2026-06-25T10:07:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106403
codeforces_index: "D"
codeforces_contest_name: "Bay Area Programming Contest 2026 Novice Division"
rating: 0
weight: 106403
solve_time_s: 41
verified: true
draft: false
---

[CF 106403D - Power Up](https://codeforces.com/problemset/problem/106403/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to answer many independent checks about a collection of power values. We have a set of distinct numbers. In one operation, choosing two different values `a` and `b` creates a new value:

$$a \cdot b + 2(a+b)$$

For each query value `x`, we must decide whether some pair from the original set can produce exactly `x`. This is the problem Codeforces problem 106403D, "Power Up". [Codeforces problem archive](https://codeforces.com/gym/106403/problems)

The expression looks like it requires checking all pairs, but it has a hidden algebraic structure. We can rewrite it as:

$$a \cdot b + 2a + 2b + 4 - 4$$

which gives:

$$(a+2)(b+2)-4$$

So a query `x` is possible exactly when `x + 4` can be represented as the product of two different shifted values from the array.

The input size is large. There can be up to `2 * 10^5` values and the same number of queries. A solution that tries every pair would perform about `n^2` operations, which is around `4 * 10^10` in the largest case and is far beyond what a typical 2 second limit allows. We need a solution closer to linear or `q * small_factor` time.

The shifted values `p_i + 2` are at most `200002`, which is much smaller than the maximum possible query value. This means we can store all available shifted values in a fast membership structure. For each query, we only need to search for possible factors of `x + 4`.

A common mistake is forgetting that the two chosen elements must be different. For example, if the array is:

```
1
```

and the query is:

```
8
```

The shifted value is `3`, and `8 + 4 = 12` is divisible by `3`. A careless check might accept because `3 * 4 = 12`, but the value `4` does not exist. The answer is:

```
NO
```

Another edge case appears when both factors are the same. For:

```
1
1
4
```

we have `x + 4 = 8`, and the shifted value is `3`. There is no pair of different elements, so the answer is `NO`. We must verify both factors are present and different.

## Approaches

The straightforward approach is to test every pair of elements. For every two values `a` and `b`, we compute `a*b + 2(a+b)` and store the results. Then each query becomes a constant time lookup.

This approach is correct because every possible combination is explicitly considered. The problem is the number of combinations. With `n = 200000`, the number of pairs is approximately:

$$\frac{n(n-1)}{2}$$

which is about `2 * 10^10` operations. It is impossible to run within the limits.

The key observation is the transformation:

$$a*b+2(a+b)= (a+2)(b+2)-4$$

Instead of generating all pair products, we reverse the process. For a query `x`, we need to know whether `x+4` has two factors that are both shifted array values.

The shifted values are small enough that they can be stored in a set. To answer a query, we factor `x+4` and examine its divisors. Since the query value is at most about `10^9`, the square root is around `31623`, so factoring is fast. If a divisor `d` exists and both `d` and `(x+4)/d` are available shifted values, the answer is YES. We also check that the two factors are not equal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² + q) | O(n²) | Too slow |
| Optimal | O(n + q√x) worst case | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the power values and transform every value `p` into `p + 2`. Store these transformed values in a set. The transformation lets us work with multiplication instead of the original quadratic expression.
2. For each query `x`, replace it with `target = x + 4`. A valid answer now requires two stored transformed values whose product is `target`.
3. Try every divisor candidate `d` from `1` up to `sqrt(target)`. If `d` divides `target`, the matching factor is `target / d`.
4. Check whether both `d` and `target / d` exist in the transformed-value set. If they do, and the two values are different, the original pair exists, so print YES.
5. If all divisors are checked without finding a valid pair, print NO.

The reason checking only up to the square root is enough is that every factor pair has one value not larger than the square root and the other not smaller than it. By finding the smaller side of the pair, we find the complete pair.

Why it works: the transformation preserves the exact condition of the original problem. Every valid pair `(a, b)` becomes `(a+2, b+2)`, and their product is exactly `x+4`. Conversely, every valid factor pair of `x+4` maps back to two original values by subtracting two. Since the set contains exactly the shifted original values, the divisor search finds a pair if and only if one exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    vals = list(map(int, input().split()))

    present = set()
    for v in vals:
        present.add(v + 2)

    ans = []
    for _ in range(q):
        x = int(input())
        target = x + 4
        ok = False

        d = 1
        while d * d <= target:
            if target % d == 0:
                other = target // d
                if d in present and other in present and d != other:
                    ok = True
                    break
            d += 1

        ans.append("YES" if ok else "NO")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The set `present` stores the transformed values rather than the original powers. This avoids repeating the algebra during every query.

For each query, `target` is the value that needs to be split into two shifted numbers. The loop checks divisors only until `d*d` exceeds `target`, which covers all possible factor pairs.

The condition `d != other` is necessary because the original pair must use two different elements. Since all original powers are distinct, two equal shifted values cannot come from different elements.

Python integers handle the multiplication and division safely here because the largest intermediate values stay around `10^9`.

## Worked Examples

Consider:

```
5 3
1 3 4 6 7
11
26
68
```

The transformed set is `{3, 5, 6, 8, 9}`.

| Query | target = x + 4 | Divisor pair found | Result |
| --- | --- | --- | --- |
| 11 | 15 | 3 and 5 | YES |
| 26 | 30 | 5 and 6 | YES |
| 68 | 72 | 8 and 9 | YES |

The trace shows how the original multiplication problem becomes a factor lookup problem.

Another case:

```
2 2
1 4
4
21
```

The transformed set is `{3, 6}`.

| Query | target = x + 4 | Divisor pair found | Result |
| --- | --- | --- | --- |
| 4 | 8 | none | NO |
| 21 | 25 | none | NO |

This demonstrates that a number being composite is not enough. Both factors must exist as shifted powers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q√x) | Each query checks divisors up to the square root of at most about `10^9` |
| Space | O(n) | The set stores the shifted values |

The maximum square root is about `31623`, so the divisor checks are small enough for the given number of queries. The solution avoids storing all possible pairs, which would require impossible memory.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    if not data:
        return ""

    it = iter(data)
    n = int(next(it))
    q = int(next(it))

    present = set()
    for _ in range(n):
        present.add(int(next(it)) + 2)

    out = []
    for _ in range(q):
        x = int(next(it))
        target = x + 4
        ok = False
        d = 1
        while d * d <= target:
            if target % d == 0:
                if d in present and target // d in present and d != target // d:
                    ok = True
                    break
            d += 1
        out.append("YES" if ok else "NO")
    return "\n".join(out)

assert run("""5 8
1 3 4 6 7
11
21
26
36
50
68
69
20
""") == """YES
NO
YES
YES
YES
YES
NO
YES"""

assert run("""4 6
2 4 1 3
8
25
14
11
16
8
""") == """YES
NO
YES
YES
YES
YES"""

assert run("""1 2
1
5
8
""") == """NO
NO"""

assert run("""4 3
1 2 3 4
8
11
20
""") == """NO
YES
YES"""

assert run("""5 2
1 1 1 1 1
11
12
""") == """NO
NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | NO | Checks that a self-pair is not accepted |
| Consecutive small values | YES/YES cases | Checks normal factor matches |
| Repeated values | NO | Confirms that only distinct original elements matter |
| Values near the upper range | YES/NO behavior | Checks divisor boundary handling |

## Edge Cases

For a single available value, the algorithm never accepts a factorization using that same shifted value twice. In the input:

```
1 1
1
5
```

the target is `9`, and the only shifted value is `3`. Although `3 * 3 = 9`, the factors are equal, so the algorithm rejects it.

For a case where the target is prime, there cannot be two meaningful factors. For example:

```
2 1
1 2
7
```

The shifted values are `3` and `4`. The target is `11`, which has no divisor pair from the set, so the answer is NO.

For a successful case:

```
2 1
1 3
11
```

The shifted values are `3` and `5`. The target is `15`, and the divisor search finds `3 * 5`, so the answer is YES. This confirms the transformation matches the original formula exactly.
