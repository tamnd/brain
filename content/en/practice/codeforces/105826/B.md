---
title: "CF 105826B - \u0417\u0430\u043a\u0440\u0430\u0441\u043a\u0430 \u0442\u043e\u0447\u0435\u043a"
description: "We have a regular polygon with n numbered vertices. Starting from the first vertex, we repeatedly move by a fixed step k around the polygon and draw the segments between the visited vertices. Every vertex reached by this process becomes painted."
date: "2026-06-25T14:57:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105826
codeforces_index: "B"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u043d\u0430 \u0412\u041a\u041e\u0428\u041f.Junior 2025"
rating: 0
weight: 105826
solve_time_s: 35
verified: true
draft: false
---

[CF 105826B - \u0417\u0430\u043a\u0440\u0430\u0441\u043a\u0430 \u0442\u043e\u0447\u0435\u043a](https://codeforces.com/problemset/problem/105826/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a regular polygon with `n` numbered vertices. Starting from the first vertex, we repeatedly move by a fixed step `k` around the polygon and draw the segments between the visited vertices. Every vertex reached by this process becomes painted. The task is to choose the smallest valid `k` so that the number of painted vertices is as small as possible.

The input contains only the number of vertices. The output is the step size that creates the smallest possible set of visited vertices, with the smallest step chosen among all optimal choices.

The important constraint is that `n` can be as large as `10^10`, so solutions that iterate over all possible steps or all vertices are impossible. Even an `O(n)` algorithm may perform up to ten billion operations, which is far beyond what a normal contest limit allows. We need to use number theory and work with divisors of `n` instead of the polygon itself.

A common mistake is to assume that a large step always paints fewer points. The number of painted vertices depends only on how the step interacts with `n`, not on the numeric size of `k`.

For example, if `n = 9`, choosing `k = 8` seems large, but the visited vertices are:

```
1, 9, 8, 7, 6, 5, 4, 3, 2
```

All 9 vertices are painted, so the answer is not 8. The correct answer is `3`, because it visits:

```
1, 4, 7
```

and paints only 3 vertices.

Another edge case is a prime number of vertices. For `n = 7`, every non-zero step is relatively prime to `7`, so every possible step reaches all vertices. The minimum valid step is simply `1`.

## Approaches

The direct approach is to try every possible `k` from `1` to `n - 1`. For each step, we can simulate the movement around the polygon until we return to the starting vertex and count how many distinct vertices were reached. This is correct because it follows the painting process exactly.

The problem is that one simulation can take up to `n` moves. Trying all `n - 1` possible values gives about `n^2` operations. With `n` reaching `10^10`, this is completely infeasible.

The key observation is that the visited vertices form a cycle. After `t` moves, the current vertex is:

```
1 + t * k (mod n)
```

Two positions in this sequence are the same when their difference is a multiple of `n`. The number of unique positions in this cycle is exactly:

```
n / gcd(n, k)
```

So instead of simulating the polygon, we only need to maximize `gcd(n, k)`. The painted count is smallest when this gcd is as large as possible.

The largest possible gcd between `n` and a proper positive `k` is the largest proper divisor of `n`. If `n` is composite and its smallest prime factor is `p`, this divisor is `n / p`. The smallest `k` with that gcd is also `n / p`.

If `n` is prime, there is no proper divisor greater than `1`, so every step paints all vertices. The smallest possible step is `1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(√n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and determine whether it is prime or find its smallest prime factor.
2. If `n` has no divisor smaller than itself, it is prime. Every possible step visits every vertex, so return `1`.
3. Otherwise, let `p` be the smallest prime factor of `n`. Return `n / p`, because this is the largest proper divisor and gives the maximum possible gcd with `n`.

Why it works: the movement always creates a cycle whose length is controlled by `gcd(n, k)`. A larger gcd means fewer vertices in the cycle. The maximum gcd is the largest divisor of `n` that is smaller than `n`, and the smallest step producing it is exactly that divisor.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    if n % 2 == 0:
        print(n // 2)
        return

    d = 3
    while d * d <= n:
        if n % d == 0:
            print(n // d)
            return
        d += 2

    print(1)

if __name__ == "__main__":
    solve()
```

The solution first handles even numbers because `2` is the smallest possible prime factor. For an even `n`, the best step is `n / 2`.

For odd numbers, we search for the smallest odd divisor starting from `3`. We only need to check up to the square root of `n`, because if `n` has a factor larger than its square root, the matching factor is smaller.

The first divisor found is the smallest prime factor. Returning `n / divisor` gives the largest proper divisor, which is the required step. If no divisor is found, `n` is prime and the answer is `1`.

There is no need for arrays or visited sets because the entire polygon structure is represented by the gcd relationship.

## Worked Examples

### Sample 1

Input:

```
9
```

The divisor search finds `3` as the smallest prime factor.

| Step | n | Current divisor | Action | Answer |
| --- | --- | --- | --- | --- |
| 1 | 9 | 2 | Not divisible | - |
| 2 | 9 | 3 | Divisor found | 9 / 3 = 3 |

Output:

```
3
```

The step `3` creates the cycle `1, 4, 7`, so only three vertices are painted.

### Sample 2

Input:

```
7
```

No divisor is found up to `sqrt(7)`.

| Step | n | Current divisor | Action | Answer |
| --- | --- | --- | --- | --- |
| 1 | 7 | 2, 3 | No divisor | 1 |

Output:

```
1
```

Because `7` is prime, every step reaches all seven vertices, and `1` is the smallest valid choice.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n) | We test possible factors only up to the square root of `n`. |
| Space | O(1) | The algorithm stores only a few integer variables. |

For `n ≤ 10^10`, checking up to `100000` possible divisors is easily fast enough.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve_case(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())

    if n % 2 == 0:
        return str(n // 2) + "\n"

    d = 3
    while d * d <= n:
        if n % d == 0:
            return str(n // d) + "\n"
        d += 2

    return "1\n"

# samples
assert solve_case("9\n") == "3\n", "sample 1"
assert solve_case("7\n") == "1\n", "sample 2"

# minimum size
assert solve_case("3\n") == "1\n", "prime triangle"

# composite with small factor
assert solve_case("12\n") == "6\n", "smallest factor is 2"

# prime near upper range
assert solve_case("9999999967\n") == "1\n", "large prime"

# odd composite
assert solve_case("25\n") == "5\n", "square number"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | `1` | Minimum prime case |
| `12` | `6` | Even numbers and largest proper divisor |
| `9999999967` | `1` | Large prime handling |
| `25` | `5` | Composite odd number |

## Edge Cases

For `n = 9`, a careless solution might choose the largest possible step and output `8`. The algorithm instead finds the smallest factor `3` and returns `9 / 3 = 3`. The gcd becomes `3`, producing the shortest possible cycle.

For `n = 7`, every non-zero step has gcd `1` with `7`. The number of painted vertices is always `7`, so minimizing the step itself gives answer `1`. The algorithm reaches the end of the divisor search and handles this prime case correctly.

For an even composite number such as `n = 12`, the movement should visit as few vertices as possible. The smallest prime factor is `2`, so the largest useful gcd is `6`. Choosing `k = 6` visits vertices `1` and `7` only, which is minimal.
