---
title: "CF 236B - Easy Number Challenge"
description: "We need to compute the sum of the number of divisors of every product i j k, where i ranges from 1 to a, j ranges from 1 to b, and k ranges from 1 to c. For each triple (i, j, k), we evaluate d(i j k), where d(x) means the number of positive divisors of x."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 236
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 146 (Div. 2)"
rating: 1300
weight: 236
solve_time_s: 105
verified: true
draft: false
---

[CF 236B - Easy Number Challenge](https://codeforces.com/problemset/problem/236/B)

**Rating:** 1300  
**Tags:** implementation, number theory  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to compute the sum of the number of divisors of every product `i * j * k`, where `i` ranges from `1` to `a`, `j` ranges from `1` to `b`, and `k` ranges from `1` to `c`.

For each triple `(i, j, k)`, we evaluate `d(i * j * k)`, where `d(x)` means the number of positive divisors of `x`. The final answer is the sum of all these divisor counts, taken modulo `2^30 = 1073741824`.

The constraints are small enough that iterating over all triples is completely reasonable. Since each variable is at most `100`, the total number of triples is at most:

$$100 \times 100 \times 100 = 10^6$$

One million iterations is fine in Python within a 2 second limit. The real challenge is how we compute the divisor count for each product.

The maximum possible product is:

$$100 \times 100 \times 100 = 10^6$$

A naive divisor-count routine that checks all integers from `1` to `n` would require about `10^6` operations per query in the worst case. Repeating that for another million products would explode to roughly `10^{12}` operations, which is far beyond the limit.

The important observation is that many products repeat. For example, `2 * 3 * 4` and `1 * 6 * 4` both produce `24`. If we compute the divisor count for `24` once and store it, every future occurrence becomes an O(1) lookup.

There are also subtle edge cases that can quietly break careless implementations.

Consider the smallest input:

```
1 1 1
```

The only product is `1`, and `d(1) = 1`. Some divisor-count implementations accidentally return `0` for `1` because they assume every number has a prime factor.

Another easy mistake appears when counting divisors using square root iteration. For example:

```
1 1 4
```

The products are `1, 2, 3, 4`, whose divisor counts are `1, 2, 2, 3`.

If we count divisors by iterating up to `sqrt(n)` and add `2` for every divisor pair, we must treat perfect squares carefully. For `4`, the divisor pair `(2,2)` should only contribute once. Forgetting this produces `4` instead of `3`.

A different pitfall is recomputing divisor counts every time the same product appears. With input:

```
100 100 100
```

many products repeat heavily. A solution without memoization still performs millions of expensive divisor computations and risks timing out.

## Approaches

The most direct solution is to iterate over every triple `(i, j, k)`, compute the product `x = i * j * k`, then calculate `d(x)` by checking every integer from `1` to `x`.

This works logically because the definition of divisors is straightforward: every integer dividing `x` contributes one to the count. The problem is scale. There are up to one million products, and each divisor computation may scan up to one million numbers. The worst case becomes roughly:

$$10^6 \times 10^6 = 10^{12}$$

which is hopeless.

We can improve divisor counting by using the square root property. Divisors come in pairs. If `d` divides `n`, then `n/d` also divides `n`. We only need to test numbers up to `sqrt(n)`.

For example, divisors of `36` appear as:

$$(1,36), (2,18), (3,12), (4,9), (6,6)$$

Checking only up to `6` is enough.

This reduces one divisor computation from `O(n)` to `O(sqrt(n))`. Since the largest product is `10^6`, each divisor count now costs about `1000` iterations. Across one million triples, this becomes about `10^9` operations, still too slow in Python.

The key observation is that the number of distinct products is limited. Every product lies between `1` and `10^6`. Instead of recomputing divisor counts repeatedly, we cache them.

When we encounter a product for the first time, we compute its divisor count using square root iteration and store the result. Every future occurrence becomes a constant-time lookup.

This transforms the expensive repeated work into a one-time preprocessing effect. Since divisor counting for numbers up to `10^6` is cheap enough when done only once per distinct value, the solution easily passes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(abc × n) | O(1) | Too slow |
| Optimal | O(abc + U√U) | O(U) | Accepted |

Here, `U` is the maximum possible product, at most `10^6`.

## Algorithm Walkthrough

1. Read integers `a`, `b`, and `c`.
2. Create a dictionary or array to memoize divisor counts.

The same product appears many times, so caching avoids repeated work.
3. Iterate through all triples `(i, j, k)`.

Since each bound is at most `100`, the total number of iterations is manageable.
4. Compute the product:

$$x = i \times j \times k$$
5. If `x` has not been processed before, compute its divisor count.

Iterate `d` from `1` to `⌊√x⌋`.

If `d` divides `x`, then:

- add `2` if `d` and `x/d` are different
- add `1` if `d*d == x`

This correctly counts divisor pairs without double-counting perfect squares.
6. Store the divisor count for `x` in the cache.
7. Add the cached divisor count to the running answer.
8. After all triples are processed, print the answer modulo `1073741824`.

### Why it works

For every triple `(i, j, k)`, the algorithm computes exactly the value required by the problem, namely `d(i*j*k)`.

The divisor-count routine is correct because every divisor below `sqrt(n)` corresponds to a paired divisor above `sqrt(n)`. Perfect squares contribute one unpaired divisor at the square root itself.

Memoization does not change correctness. It only avoids recomputing values for products already seen earlier. Every lookup returns the same divisor count that would have been recomputed manually.

Since every triple is processed exactly once and contributes exactly its divisor count, the final sum is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1073741824

a, b, c = map(int, input().split())

cache = {}
answer = 0

for i in range(1, a + 1):
    for j in range(1, b + 1):
        for k in range(1, c + 1):
            x = i * j * k

            if x not in cache:
                divisors = 0
                d = 1

                while d * d <= x:
                    if x % d == 0:
                        if d * d == x:
                            divisors += 1
                        else:
                            divisors += 2
                    d += 1

                cache[x] = divisors

            answer += cache[x]

print(answer % MOD)
```

The three nested loops enumerate every valid triple exactly once. Since the bounds are only `100`, one million iterations are acceptable.

The cache stores divisor counts keyed by product value. This is the critical optimization. Without it, the same divisor count would be recomputed many times.

The divisor-count loop uses the square root method. The condition `d * d <= x` guarantees we inspect all possible divisor pairs.

The perfect-square branch is easy to get wrong. For example, when `x = 36`, divisor `6` pairs with itself. We should count it once, not twice.

The modulo is applied only at the end. Python integers do not overflow, so intermediate sums are safe. Applying modulo during accumulation would also work.

## Worked Examples

### Example 1

Input:

```
2 2 2
```

| i | j | k | Product | Divisors | Running Sum |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 2 | 2 | 2 | 3 |
| 1 | 2 | 1 | 2 | 2 | 5 |
| 1 | 2 | 2 | 4 | 3 | 8 |
| 2 | 1 | 1 | 2 | 2 | 10 |
| 2 | 1 | 2 | 4 | 3 | 13 |
| 2 | 2 | 1 | 4 | 3 | 16 |
| 2 | 2 | 2 | 8 | 4 | 20 |

Final answer:

```
20
```

This example shows repeated products clearly. The value `2` appears three times, and `4` appears three times. Memoization avoids recomputing their divisor counts repeatedly.

### Example 2

Input:

```
1 2 3
```

| i | j | k | Product | Divisors | Running Sum |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 2 | 2 | 2 | 3 |
| 1 | 1 | 3 | 3 | 2 | 5 |
| 1 | 2 | 1 | 2 | 2 | 7 |
| 1 | 2 | 2 | 4 | 3 | 10 |
| 1 | 2 | 3 | 6 | 4 | 14 |

Final answer:

```
14
```

This trace demonstrates both repeated products and non-square products with divisor pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(abc + U√U) | Triple iteration plus one divisor computation per distinct product |
| Space | O(U) | Cache may store divisor counts for all products up to `10^6` |

The largest possible number of triples is `10^6`, which is completely manageable in Python. The divisor-count cache prevents repeated expensive computations, keeping the runtime comfortably within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 1073741824

def solve():
    input = sys.stdin.readline

    a, b, c = map(int, input().split())

    cache = {}
    answer = 0

    for i in range(1, a + 1):
        for j in range(1, b + 1):
            for k in range(1, c + 1):
                x = i * j * k

                if x not in cache:
                    divisors = 0
                    d = 1

                    while d * d <= x:
                        if x % d == 0:
                            if d * d == x:
                                divisors += 1
                            else:
                                divisors += 2
                        d += 1

                    cache[x] = divisors

                answer += cache[x]

    print(answer % MOD)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue().strip()

# provided sample
assert run("2 2 2\n") == "20", "sample 1"

# minimum input
assert run("1 1 1\n") == "1", "minimum case"

# small asymmetric case
assert run("1 2 3\n") == "14", "mixed ranges"

# perfect square products appear
assert run("1 1 4\n") == "8", "perfect square divisor counting"

# all equal small values
assert run("2 2 1\n") == "8", "duplicate products"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | Correct handling of divisor count for `1` |
| `1 2 3` | `14` | Mixed ranges and repeated products |
| `1 1 4` | `8` | Perfect-square divisor counting |
| `2 2 1` | `8` | Duplicate products and cache reuse |

## Edge Cases

Consider the smallest possible input:

```
1 1 1
```

The algorithm processes only one triple:

| Product | Divisors |
| --- | --- |
| 1 | 1 |

The divisor loop runs with `d = 1`. Since `1 * 1 == 1`, the algorithm correctly adds only one divisor instead of two.

Final answer:

```
1
```

Now consider a perfect square case:

```
1 1 4
```

The products are `1, 2, 3, 4`.

For `4`, the divisor loop behaves as follows:

| d | d*d <= 4 | 4 % d == 0 | Contribution |
| --- | --- | --- | --- |
| 1 | Yes | Yes | +2 |
| 2 | Yes | Yes | +1 |

Total divisor count becomes `3`, corresponding to `{1,2,4}`.

A careless implementation that always adds `2` for divisor pairs would incorrectly return `4`.

Finally, consider repeated products:

```
2 2 2
```

The product `4` appears three times. The first occurrence computes its divisor count and stores:

```
cache[4] = 3
```

The next two occurrences immediately reuse the cached value. This avoids repeated square root scans and keeps the runtime fast enough for the largest inputs.
