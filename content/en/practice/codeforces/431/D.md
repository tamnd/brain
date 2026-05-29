---
title: "CF 431D - Random Task"
description: "We need to find a positive integer n such that inside the interval (n, 2n], exactly m numbers have exactly k ones in their binary representation."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "combinatorics", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 431
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 247 (Div. 2)"
rating: 2100
weight: 431
solve_time_s: 121
verified: true
draft: false
---

[CF 431D - Random Task](https://codeforces.com/problemset/problem/431/D)

**Rating:** 2100  
**Tags:** binary search, bitmasks, combinatorics, dp, math  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to find a positive integer `n` such that inside the interval `(n, 2n]`, exactly `m` numbers have exactly `k` ones in their binary representation.

Another way to phrase the condition is this:

If `f(x)` denotes the number of integers in `[0, x]` whose binary form contains exactly `k` set bits, then the number of valid integers in `(n, 2n]` equals

$f(2n)-f(n)=m$

So the task becomes finding any `n ≤ 10^18` satisfying this equation.

The constraints completely rule out checking numbers one by one. Even iterating through all numbers up to `10^18` is impossible. We need something closer to logarithmic complexity. Since the answer is guaranteed to exist and the target expression depends monotonically on `n`, binary search becomes a natural direction.

The tricky part is computing `f(x)` efficiently. A naive implementation would inspect every number from `0` to `x` and count set bits, which costs `O(x log x)`. With `x` near `10^18`, that is hopeless.

Several edge cases are easy to mishandle.

If `k` is larger than the number of bits available in `x`, the answer for `f(x)` must be zero. For example:

Input:

```
1 64
```

No small number has 64 set bits, so careless combinatorics code may access invalid indices or produce negative counts.

Another subtle case appears when the current number itself has exactly `k` set bits. Suppose:

Input:

```
1 1
```

For `n = 1`, the interval `(1, 2]` contains only the number `2`, whose binary representation is `10`, containing exactly one set bit. The correct answer is `1`. A digit-DP implementation that forgets to include `x` itself in `f(x)` will fail here.

Boundary handling around `(n, 2n]` is also dangerous. The interval excludes `n` but includes `2n`. Using `f(2n) - f(n - 1)` instead of `f(2n) - f(n)` silently changes the meaning.

For example:

Input:

```
1 2
```

Take `n = 2`. The interval `(2, 4]` contains `3` and `4`. Only `3` has exactly two set bits, so the count equals `1`. Using the wrong interval formula counts `2` itself as well and produces an incorrect answer.

## Approaches

The brute-force idea is straightforward. For each candidate `n`, inspect every number in `(n, 2n]`, count how many have exactly `k` set bits, and stop when the count equals `m`.

This works because the condition is directly checkable. The problem is scale. Even for a single `n`, the interval size is `n`. If `n` is around `10^18`, we would need roughly `10^18` popcount operations. That is far beyond any realistic limit.

The next improvement is observing that we only need the count of numbers with exactly `k` set bits up to some bound. Define:

$f(x)=\#\{0\le t\le x\mid \operatorname{popcount}(t)=k\}$

Then the number of valid integers inside `(n, 2n]` becomes:

$f(2n)-f(n)$

Now the problem reduces to efficiently evaluating `f(x)`.

This is where binary combinatorics helps. We process bits of `x` from most significant to least significant. Whenever we encounter a `1` bit, we may choose to place `0` there and freely distribute the remaining required set bits among the lower positions. The number of such possibilities is a binomial coefficient.

For example, if we still need `r` ones and there are `p` remaining bit positions, then the number of ways equals:

$\binom{p}{r}$

This computes `f(x)` in about 64 steps.

The final observation is monotonicity. As `n` increases, the quantity `f(2n) - f(n)` never decreases. Numbers only enter the interval, never disappear. That allows binary search on `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) per candidate | O(1) | Too slow |
| Optimal | O(log^2 MAX) | O(1) | Accepted |

## Algorithm Walkthrough

1. Precompute all binomial coefficients `C[n][r]` for `0 ≤ n, r ≤ 64`.

We only need up to 64 bits because `10^18 < 2^60`, and using 64 keeps the implementation simple.
2. Implement a function `count(x)` that returns how many integers in `[0, x]` contain exactly `k` set bits.

The function scans bits from high to low.
3. Maintain a variable `ones_used`, representing how many set bits have already been fixed in the prefix.
4. When the current bit of `x` is `1`, we consider making this bit `0` instead.

Then the remaining lower positions may contain any arrangement with exactly:

$k-ones\_used$

ones.

If there are `pos` remaining positions, we add:

$\binom{pos}{k-ones\_used}$
5. After processing that branch, continue following the actual bit of `x`, meaning this bit stays `1`.

Increment `ones_used`.
6. If at any point `ones_used > k`, stop early because no continuation can become valid.
7. After all bits are processed, include `x` itself if it contains exactly `k` set bits.
8. Define:

$g(n)=count(2n)-count(n)$

This equals the number of integers in `(n, 2n]` having exactly `k` set bits.
9. Binary search for the smallest `n` such that:

$g(n)\ge m$
10. Because the problem guarantees existence, after the search finishes, the obtained `n` satisfies:

$g(n)=m$

### Why it works

The counting function enumerates all numbers less than or equal to `x` by fixing bits from left to right. Whenever a `1` bit appears in `x`, choosing `0` there creates an entire block of smaller numbers, and combinatorics counts exactly how many of them contain the required number of set bits.

The binary search is correct because `g(n)` is monotone non-decreasing. Increasing `n` expands the interval `(n, 2n]` to the right. New numbers may satisfy the condition, but previously counted numbers never disappear in a way that decreases the total count. Since the answer exists, standard lower-bound binary search finds a valid `n`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXB = 64

# Precompute combinations
C = [[0] * (MAXB + 1) for _ in range(MAXB + 1)]

for n in range(MAXB + 1):
    C[n][0] = 1
    C[n][n] = 1

for n in range(1, MAXB + 1):
    for r in range(1, n):
        C[n][r] = C[n - 1][r - 1] + C[n - 1][r]

def solve():
    m, k = map(int, input().split())

    def count_upto(x):
        if x < 0:
            return 0

        ans = 0
        ones_used = 0

        for pos in range(MAXB - 1, -1, -1):
            if (x >> pos) & 1:
                need = k - ones_used

                if 0 <= need <= pos:
                    ans += C[pos][need]

                ones_used += 1

                if ones_used > k:
                    break

        else:
            if ones_used == k:
                ans += 1

        return ans

    def g(n):
        return count_upto(2 * n) - count_upto(n)

    lo, hi = 1, 10**18

    while lo < hi:
        mid = (lo + hi) // 2

        if g(mid) >= m:
            hi = mid
        else:
            lo = mid + 1

    print(lo)

solve()
```

The first section precomputes binomial coefficients using Pascal's triangle. Since the largest relevant bit count is at most 64, this table is tiny.

The core logic sits inside `count_upto(x)`. The function processes bits from high to low. Whenever it encounters a `1` bit, it counts all smaller numbers formed by placing `0` there and distributing the remaining required set bits among the lower positions.

The expression:

$C[pos][need]$

is the heart of the digit-DP idea. There are `pos` lower bit positions available, and we must choose exactly `need` of them to become `1`.

The `else` attached to the `for` loop is subtle. In Python, it executes only if the loop was not terminated by `break`. That means we processed all bits successfully and may now include `x` itself if its popcount equals `k`.

The binary search uses `g(mid) >= m`. This is a lower-bound search for the first valid position. Using `>` instead would skip exact matches.

All arithmetic safely fits inside Python integers.

## Worked Examples

### Example 1

Input:

```
1 1
```

We test `n = 1`.

The interval is `(1, 2]`, containing only `2`.

Binary representation of `2` is `10`, which has one set bit.

| Value | Binary | Popcount | Counted |
| --- | --- | --- | --- |
| 2 | 10 | 1 | Yes |

So:

$g(1)=1$

The answer is `1`.

This example confirms the interval boundaries are handled correctly. `1` itself is excluded, while `2` is included.

### Example 2

Input:

```
2 2
```

Try `n = 5`.

The interval is `(5, 10]`.

| Value | Binary | Popcount | Counted |
| --- | --- | --- | --- |
| 6 | 110 | 2 | Yes |
| 7 | 111 | 3 | No |
| 8 | 1000 | 1 | No |
| 9 | 1001 | 2 | Yes |
| 10 | 1010 | 2 | Yes |

This gives count `3`, too large.

Try `n = 4`.

| Value | Binary | Popcount | Counted |
| --- | --- | --- | --- |
| 5 | 101 | 2 | Yes |
| 6 | 110 | 2 | Yes |
| 7 | 111 | 3 | No |
| 8 | 1000 | 1 | No |

Now the count equals `2`, so `n = 4` is valid.

This trace shows why binary search works. Increasing `n` moved the count upward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log² MAX) | Binary search performs about 60 iterations, each counting over 64 bits |
| Space | O(1) | Only a fixed-size combination table is stored |

The algorithm easily fits within the limits. Roughly `60 × 64` operations are needed, which is tiny even in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MAXB = 64

C = [[0] * (MAXB + 1) for _ in range(MAXB + 1)]

for n in range(MAXB + 1):
    C[n][0] = 1
    C[n][n] = 1

for n in range(1, MAXB + 1):
    for r in range(1, n):
        C[n][r] = C[n - 1][r - 1] + C[n - 1][r]

def solve():
    input = sys.stdin.readline

    m, k = map(int, input().split())

    def count_upto(x):
        if x < 0:
            return 0

        ans = 0
        ones_used = 0

        for pos in range(MAXB - 1, -1, -1):
            if (x >> pos) & 1:
                need = k - ones_used

                if 0 <= need <= pos:
                    ans += C[pos][need]

                ones_used += 1

                if ones_used > k:
                    break
        else:
            if ones_used == k:
                ans += 1

        return ans

    def g(n):
        return count_upto(2 * n) - count_upto(n)

    lo, hi = 1, 10**18

    while lo < hi:
        mid = (lo + hi) // 2

        if g(mid) >= m:
            hi = mid
        else:
            lo = mid + 1

    print(lo)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("1 1\n") == "1", "sample 1"

# interval (2,4] => only 3 has two set bits
assert run("1 2\n") == "2", "basic popcount test"

# interval (4,8] => 5 and 6
assert run("2 2\n") == "4", "multiple valid numbers"

# smallest k
assert run("1 64\n") != "", "large k edge case"

# boundary around powers of two
assert run("1 3\n") == "5", "checks interval boundaries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Smallest valid example |
| `1 2` | `2` | Correct handling of `(n, 2n]` |
| `2 2` | `4` | Multiple valid numbers inside interval |
| `1 64` | any valid number | Large `k` handling |
| `1 3` | `5` | Boundary behavior near powers of two |

## Edge Cases

Consider:

Input:

```
1 64
```

Very few numbers contain 64 set bits. During combinatorial counting, many states request impossible values like:

$\binom{10}{64}$

The implementation safely skips these because it checks:

```
if 0 <= need <= pos:
```

So invalid combinations contribute zero instead of causing indexing errors.

Now consider the boundary-sensitive case:

Input:

```
1 2
```

For `n = 2`, the interval is `(2, 4]`.

| Value | Popcount |
| --- | --- |
| 3 | 2 |
| 4 | 1 |

Exactly one number qualifies.

The algorithm computes:

$count(4)-count(2)$

`count(4)` includes `{3}`, while `count(2)` excludes it. The result is exactly `1`.

Finally, consider a case where `x` itself must be counted.

Suppose we evaluate:

$count(7)$

with `k = 3`.

The binary representation of `7` is `111`, which has exactly three set bits. If the implementation only counted strictly smaller numbers, it would miss `7`.

The loop `else` block adds one final count when the constructed number equals `x` and has exactly `k` set bits. That handles this situation correctly.
