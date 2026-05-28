---
title: "CF 158D - Ice Sculptures"
description: "We have n ice sculptures placed evenly on a circle. Each sculpture has a value, which may be positive or negative. We may remove some sculptures, but the remaining ones must still form a regular polygon."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "brute-force", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 158
codeforces_index: "D"
codeforces_contest_name: "VK Cup 2012 Qualification Round 1"
rating: 1300
weight: 158
solve_time_s: 98
verified: true
draft: false
---

[CF 158D - Ice Sculptures](https://codeforces.com/problemset/problem/158/D)

**Rating:** 1300  
**Tags:** *special, brute force, number theory  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` ice sculptures placed evenly on a circle. Each sculpture has a value, which may be positive or negative. We may remove some sculptures, but the remaining ones must still form a regular polygon.

Because the sculptures cannot move, the remaining vertices must be equally spaced along the original circle. That means if we keep `k` sculptures, then `k` must divide `n`, and the kept sculptures are obtained by repeatedly jumping by a fixed step size.

For example, if `n = 12` and we keep 4 sculptures, then the spacing between consecutive kept sculptures must be `12 / 4 = 3`. Starting from any position and repeatedly adding 3 modulo 12 produces one valid polygon.

The task is to maximize the sum of the kept sculpture values, while keeping at least 3 sculptures.

The constraints are small enough to allow trying many divisors of `n`, but too large for anything quadratic in `n`. Since `n ≤ 20000`, an `O(n^2)` solution would perform around 400 million operations in the worst case, which is too slow in Python. A solution around `O(n * d(n))`, where `d(n)` is the number of divisors, easily fits.

There are several easy mistakes in this problem.

One common mistake is checking only contiguous segments. The remaining sculptures are not required to stay adjacent on the circle.

Consider:

```
8
1 2 -3 4 -5 5 2 3
```

The best answer is obtained by keeping every second sculpture:

```
2 + 4 + 5 + 3 = 14
```

A contiguous-subarray approach would completely miss this structure.

Another mistake is forgetting that the remaining polygon must have at least 3 vertices.

Example:

```
6
100 -1 100 -1 100 -1
```

Keeping only the three `100`s is valid and gives `300`. Keeping two vertices would give `200`, but a 2-gon is not allowed.

A subtler bug appears when handling circular stepping. Suppose:

```
5
1 2 3 4 5
```

Since 5 is prime, the only valid polygon uses all sculptures. Any attempt to use step size 2 or 3 still visits every vertex because those steps are coprime with 5. The correct answer is `15`.

Careless implementations sometimes count such cycles multiple times or incorrectly assume every step creates a smaller polygon.

## Approaches

The brute-force idea is straightforward. We can try every subset of sculptures and check whether the chosen positions form a regular polygon. A subset is valid if the gaps between consecutive chosen vertices are equal around the circle.

This works conceptually because the definition of a regular polygon is very rigid. Unfortunately, there are `2^n` subsets, which becomes impossible even for `n = 30`, let alone `20000`.

A more structured brute force observes that every valid polygon corresponds to repeatedly taking jumps of fixed size around the circle.

Suppose the jump size is `d`. Starting from position `s`, we visit:

```
s, s+d, s+2d, ...
```

modulo `n`.

This forms a cycle. The number of distinct vertices visited equals:

```
n / gcd(n, d)
```

For the polygon to be valid, we need at least 3 vertices.

Now the search space becomes manageable. For every possible step size, we can simulate every starting position and compute the sum along its cycle.

The key observation is that cycles produced by the same step size partition the circle into disjoint groups. If `g = gcd(n, d)`, then there are exactly `g` different cycles, each of length `n / g`.

Instead of thinking in terms of arbitrary polygons, we only need to consider divisors of `n`.

Let `k` be the number of vertices kept. Then `k` must divide `n`. The step size becomes:

```
step = n / k
```

For every divisor `k ≥ 3`, we compute sums of all arithmetic progressions modulo `n` with that step size and keep the maximum.

The number of divisors of a number up to `20000` is small, so the total work stays near linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | O(2^n) | O(n) | Too slow |
| Cycle Enumeration by Divisors | O(n × d(n)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array of sculpture values.
2. Initialize the answer as the sum of all sculptures.

This already corresponds to keeping the entire polygon, which is always allowed.

1. Enumerate all divisors `k` of `n` such that `k ≥ 3`.

Here, `k` represents the number of vertices in the remaining polygon.

1. For each valid `k`, compute:

```
step = n / k
```

If we repeatedly move by `step`, we visit exactly `k` vertices before returning to the start.

1. For every starting position from `0` to `step - 1`, compute the sum of the cycle formed by repeatedly adding `step`.

Each starting position generates one distinct polygon configuration for this divisor.

1. Update the global maximum with the cycle sum.
2. Print the best value found.

### Why it works

A valid remaining polygon must consist of equally spaced vertices on the original circle. If the polygon has `k` vertices, then the spacing between consecutive kept vertices must be exactly `n / k`.

Starting from any vertex and repeatedly adding this spacing modulo `n` generates precisely the vertices of that polygon.

Conversely, every cycle generated this way forms a valid regular polygon because all gaps are equal.

The algorithm enumerates every possible divisor `k` and every possible starting position for that spacing, so every valid polygon is checked exactly once. Since we compute the exact sum for each candidate and keep the maximum, the final answer is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    ans = sum(a)

    for k in range(3, n + 1):
        if n % k != 0:
            continue

        step = n // k

        for start in range(step):
            cur = 0
            pos = start

            for _ in range(k):
                cur += a[pos]
                pos += step

            ans = max(ans, cur)

    print(ans)

solve()
```

The solution directly follows the mathematical structure of valid polygons.

The outer loop iterates over all possible polygon sizes `k`. Only divisors of `n` are valid because equally spaced vertices must wrap around the circle perfectly.

For a fixed `k`, the jump size is `step = n // k`. Starting from any index and repeatedly adding `step` visits exactly the vertices of one candidate polygon.

The range `0 .. step-1` is enough for starting positions because larger starts would repeat the same cycles. This is a subtle optimization that avoids duplicate work.

Inside the innermost loop, we collect exactly `k` elements. Since `k * step = n`, we return to the starting position after exactly `k` jumps.

Another detail is that modulo arithmetic is unnecessary here. Because `pos` increases by `step` exactly `k` times, the largest accessed index is:

```
start + (k - 1) * step < n
```

So every access stays within bounds.

## Worked Examples

### Example 1

Input:

```
8
1 2 -3 4 -5 5 2 3
```

Valid divisors `k ≥ 3` are `4` and `8`.

For `k = 4`:

```
step = 8 / 4 = 2
```

| Start | Visited Values | Sum |
| --- | --- | --- |
| 0 | 1, -3, -5, 2 | -5 |
| 1 | 2, 4, 5, 3 | 14 |

For `k = 8`:

| Start | Visited Values | Sum |
| --- | --- | --- |
| 0 | all values | 9 |

The maximum is `14`.

This trace shows why non-contiguous selections matter. The best polygon skips every other sculpture.

### Example 2

Input:

```
6
100 -1 100 -1 100 -1
```

Valid divisors are `3` and `6`.

For `k = 3`:

```
step = 2
```

| Start | Visited Values | Sum |
| --- | --- | --- |
| 0 | 100, 100, 100 | 300 |
| 1 | -1, -1, -1 | -3 |

For `k = 6`:

| Start | Visited Values | Sum |
| --- | --- | --- |
| 0 | all values | 297 |

The answer is `300`.

This example demonstrates why checking smaller valid polygons is necessary even when keeping all sculptures already gives a large sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × d(n)) | We process every divisor and traverse at most `n` elements for each |
| Space | O(1) | Only a few integer variables are used |

The number of divisors of integers up to `20000` is very small, so the practical runtime is close to linear. The solution comfortably fits within the 3-second limit in Python.

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

        ans = sum(a)

        for k in range(3, n + 1):
            if n % k != 0:
                continue

            step = n // k

            for start in range(step):
                cur = 0
                pos = start

                for _ in range(k):
                    cur += a[pos]
                    pos += step

                ans = max(ans, cur)

        return str(ans)

    return solve()

# provided sample
assert run("8\n1 2 -3 4 -5 5 2 3\n") == "14", "sample 1"

# minimum size
assert run("3\n1 2 3\n") == "6", "minimum n"

# all negative
assert run("4\n-1 -2 -3 -4\n") == "-10", "must keep at least 3"

# alternating large values
assert run("6\n100 -1 100 -1 100 -1\n") == "300", "every second element"

# prime n
assert run("5\n1 2 3 4 5\n") == "15", "only full polygon possible"

# all equal
assert run("12\n7 7 7 7 7 7 7 7 7 7 7 7\n") == "84", "uniform values"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 1 2 3` | `6` | Minimum allowed size |
| `4 / -1 -2 -3 -4` | `-10` | Must keep at least 3 sculptures |
| `6 / 100 -1 100 -1 100 -1` | `300` | Best solution skips elements |
| `5 / 1 2 3 4 5` | `15` | Prime `n` allows only full cycle |
| `12 / all 7s` | `84` | Uniform arrays and divisor handling |

## Edge Cases

Consider the case where all values are negative:

```
4
-1 -2 -3 -4
```

A careless solution might try to keep only one sculpture with value `-1`, but polygons with fewer than 3 vertices are invalid.

The algorithm checks only divisors `k ≥ 3`.

For `k = 4`:

```
sum = -10
```

No other valid polygon exists, so the answer is `-10`.

Now consider a prime number of sculptures:

```
5
1 2 3 4 5
```

The only divisors of 5 are 1 and 5. Since we require at least 3 vertices, only `k = 5` is considered.

The algorithm computes:

```
1 + 2 + 3 + 4 + 5 = 15
```

This correctly handles the fact that every nonzero step size modulo a prime traverses the entire circle.

Finally, consider repeated cycles:

```
8
1 2 -3 4 -5 5 2 3
```

For `k = 4`, the step size is 2.

Starting positions larger than 1 would repeat existing cycles:

```
0 -> 2 -> 4 -> 6
1 -> 3 -> 5 -> 7
```

The algorithm iterates only over starts in `[0, step-1]`, so every distinct polygon is processed exactly once.
