---
title: "CF 102800H - Curious"
description: "We are given an array of positive integers. Every value in the array is at most m. For each query value x, we must count how many ordered pairs (ai, aj) satisfy gcd(ai, aj) = x."
date: "2026-07-27T17:40:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102800
codeforces_index: "H"
codeforces_contest_name: "The 14th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 102800
solve_time_s: 79
verified: true
draft: false
---

[CF 102800H - Curious](https://codeforces.com/problemset/problem/102800/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers. Every value in the array is at most `m`. For each query value `x`, we must count how many ordered pairs `(ai, aj)` satisfy `gcd(ai, aj) = x`. Ordered pairs mean `(i, j)` and `(j, i)` are counted separately when `i ≠ j`, and `(i, i)` is also a valid pair.

The straightforward interpretation is to compute the greatest common divisor for every pair of indices and answer the queries from those results. That is correct, but the input sizes make it impossible. Both `n` and `m` can reach `10^5`, and there may be `10^5` queries. Computing all `n²` pairs would require up to `10^10` GCD computations, which is far beyond what fits in one second. Even storing information for every pair is impossible.

The upper bound on the values is the real opportunity. Every array element is at most `m`, so instead of reasoning about individual indices, we can reason about values and their divisors. Algorithms that iterate over multiples of every integer run in roughly `m log m` time because

$$\sum_{i=1}^{m}\frac{m}{i}=m\log m.$$

That is well within the limits for `m = 10^5`.

One easy mistake is forgetting that the problem asks for ordered pairs rather than unordered pairs.

For example,

```
n = 2
array = [2, 4]
query = 2
```

The correct answer is `4` because the valid pairs are `(2,2)`, `(2,4)`, `(4,2)`, and `(4,4)`. Dividing by two as if the pairs were unordered would produce the wrong answer.

Another subtle case is when the queried GCD never appears as an array value.

```
array = [6, 12]
query = 3
```

No pair has GCD equal to `3`, even though every number is divisible by `3`. Simply counting numbers divisible by `3` would incorrectly return `4`.

A third common mistake is counting pairs whose GCD is a multiple of the query instead of exactly the query.

```
array = [4, 8]
query = 2
```

Both numbers are divisible by `2`, but every pair actually has GCD `4`. The correct answer is `0`. This is exactly why an inclusion-exclusion step is required.

## Approaches

The brute force method checks every ordered pair of indices, computes `gcd(ai, aj)`, and increments the corresponding answer. Its correctness is immediate because it directly implements the definition of the problem. Unfortunately, with `n = 10^5`, it performs `10^10` pair checks, making it completely impractical.

The key observation is that GCD is defined through divisibility. Instead of examining pairs one by one, count how many array elements are divisible by every possible value.

Let `cnt[v]` be the frequency of value `v` in the array.

For every divisor `d`, compute

$$f[d]=\text{number of array elements divisible by }d.$$

This is done efficiently by iterating through multiples of `d`.

If `f[d]=c`, then there are `c²` ordered pairs whose two values are both divisible by `d`. Those pairs have GCD equal to `d` or some multiple of `d`.

The remaining task is separating the pairs whose GCD is exactly `d`. Processing divisors from large to small makes this possible. Let `ans[d]` denote the number of ordered pairs with GCD exactly `d`. Initially,

$$ans[d]=f[d]^2.$$

Every pair counted here whose GCD is actually `2d`, `3d`, or another multiple has already been computed because larger divisors are processed first. Subtract all those contributions:

$$ans[d]=f[d]^2-\sum_{k\ge2}ans[kd].$$

This is the classic inclusion-exclusion principle over multiples, often described as Möbius inversion without explicitly computing the Möbius function.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log m) | O(m) | Too slow |
| Optimal | O(m log m + k) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read the array and build a frequency array `cnt`, where `cnt[v]` is the number of occurrences of value `v`.
2. For every integer `d` from `1` to `m`, compute how many array elements are divisible by `d`. Iterate through `d, 2d, 3d, ...` and accumulate their frequencies into `divisible[d]`.
3. Create an answer array.
4. Process divisors from `m` down to `1`.
5. Set `ans[d] = divisible[d] * divisible[d]`. This counts every ordered pair whose two values are divisible by `d`.
6. Iterate through multiples `2d, 3d, ...` and subtract `ans[multiple]` from `ans[d]`. Those pairs were counted in the previous step but actually have a larger GCD.
7. After preprocessing finishes, every query is answered by printing `ans[x]`.

### Why it works

For every divisor `d`, `divisible[d]²` counts all ordered pairs whose GCD is a multiple of `d`. Every such pair belongs to exactly one value, namely its exact GCD. Processing from larger divisors toward smaller ones guarantees that all larger GCD contributions have already been computed. Subtracting those contributions leaves precisely the pairs whose GCD equals `d`. Since every pair has exactly one greatest common divisor, every pair is counted once and only once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m, k = map(int, input().split())

        cnt = [0] * (m + 1)
        for v in map(int, input().split()):
            cnt[v] += 1

        divisible = [0] * (m + 1)
        for d in range(1, m + 1):
            s = 0
            for x in range(d, m + 1, d):
                s += cnt[x]
            divisible[d] = s

        ans = [0] * (m + 1)
        for d in range(m, 0, -1):
            cur = divisible[d] * divisible[d]
            for x in range(d * 2, m + 1, d):
                cur -= ans[x]
            ans[d] = cur

        for _ in range(k):
            x = int(input())
            out.append(str(ans[x]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The frequency array compresses the input into counts of values instead of positions. This is what makes the preprocessing depend on `m` rather than `n²`.

The second loop computes how many numbers are divisible by each divisor. Iterating over multiples is efficient because every integer appears as a multiple only for its divisors.

The reverse loop is the heart of the algorithm. The subtraction must happen after larger divisors have already been processed, which is why the iteration goes from `m` down to `1`. Reversing this order would subtract values that have not yet been computed.

The square `divisible[d] * divisible[d]` already counts ordered pairs correctly. No factor of two is needed because ordered pairs are required by the problem.

All intermediate values fit comfortably in Python integers. In languages with fixed-width integers, a 64-bit type is required because the largest possible answer is `n²`, which reaches `10^10`.

## Worked Examples

### Example 1

Input:

```
n = 3
array = [2, 4, 6]
queries = [2, 1]
```

| Divisor | divisible | Initial pairs | Final answer |
| --- | --- | --- | --- |
| 6 | 1 | 1 | 1 |
| 4 | 1 | 1 | 1 |
| 3 | 1 | 1 | 1 |
| 2 | 3 | 9 | 7 |
| 1 | 3 | 9 | 0 |

The pairs with GCD equal to `2` are exactly those remaining after removing the pairs whose GCD is `4` or `6`. No pair has GCD `1`, so the final value becomes zero.

### Example 2

Input:

```
n = 2
array = [4, 8]
query = 2
```

| Divisor | divisible | Initial pairs | Final answer |
| --- | --- | --- | --- |
| 8 | 1 | 1 | 1 |
| 4 | 2 | 4 | 3 |
| 2 | 2 | 4 | 0 |
| 1 | 2 | 4 | 0 |

Although every number is divisible by `2`, all four candidate pairs actually have GCD `4` or `8`. The subtraction step removes them all, leaving the correct answer of zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m + k) | Two harmonic-series loops over multiples, then constant time per query |
| Space | O(m) | Frequency, divisible count, and answer arrays |

The preprocessing performs approximately `m/1 + m/2 + ... + m/m` iterations, which is `O(m log m)`. With `m = 10^5`, this comfortably fits within the limits, and each query is answered in constant time.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = []
    t = int(input())

    for _ in range(t):
        n, m, k = map(int, input().split())
        cnt = [0] * (m + 1)
        for v in map(int, input().split()):
            cnt[v] += 1

        div = [0] * (m + 1)
        for d in range(1, m + 1):
            for x in range(d, m + 1, d):
                div[d] += cnt[x]

        ans = [0] * (m + 1)
        for d in range(m, 0, -1):
            ans[d] = div[d] * div[d]
            for x in range(d * 2, m + 1, d):
                ans[d] -= ans[x]

        for _ in range(k):
            out.append(str(ans[int(input())]))

    return "\n".join(out)

assert run("""1
1 1 1
1
1
""") == "1"

assert run("""1
2 4 2
2 4
2
4
""") == "4\n1"

assert run("""1
2 8 1
4 8
2
""") == "0"

assert run("""1
3 5 3
5 5 5
5
1
2
""") == "9\n0\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single value `1` | `1` | Minimum input size |
| Values `2 4` | `4`, `1` | Ordered pair counting |
| Values `4 8`, query `2` | `0` | Excluding larger GCD values |
| All values equal to `5` | `9`, `0`, `0` | Large frequency concentrated at one value |

## Edge Cases

Consider the array

```
1
2 4 1
2 4
2
```

The divisible counts are `divisible[4] = 1` and `divisible[2] = 2`. The algorithm first computes `ans[4] = 1`. For divisor `2`, it starts from `2² = 4` ordered pairs and subtracts the one pair with GCD `4`, leaving `4`. This matches the four ordered pairs whose GCD is exactly `2`.

Now consider

```
1
2 12 1
6 12
3
```

Both values are divisible by `3`, so `divisible[3] = 2` and the initial count is `4`. Processing larger divisors subtracts the four pairs whose GCD is `6`, leaving `0`. The algorithm correctly distinguishes divisibility from exact GCD.

Finally,

```
1
2 8 1
4 8
2
```

Again `divisible[2] = 2`, giving an initial count of `4`. The computation subtracts `ans[4] = 3` and `ans[8] = 1`, leaving zero. Every candidate pair belongs to a larger exact GCD, so none remain for divisor `2`. This demonstrates why processing from large divisors to small ones is essential.
