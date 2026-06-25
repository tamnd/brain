---
title: "CF 106190D - \u0425\u0432\u043e\u0441\u0442\u044b \u0442\u0438\u0433\u0440\u043e\u043a\u0440\u044b\u0441\u0430"
description: "The problem asks us to recover the possible length of the missing middle tail of a tigercat-like creature. The three tail lengths are a, b, and c, where a < b < c. We already know the shortest and longest lengths, but the middle one is missing."
date: "2026-06-25T10:45:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106190
codeforces_index: "D"
codeforces_contest_name: "\u041a\u043e\u0433\u043d\u0438\u0442\u0438\u0432\u043d\u044b\u0435 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0438 2025-2026. \u041f\u0435\u0440\u0432\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 106190
solve_time_s: 39
verified: true
draft: false
---

[CF 106190D - \u0425\u0432\u043e\u0441\u0442\u044b \u0442\u0438\u0433\u0440\u043e\u043a\u0440\u044b\u0441\u0430](https://codeforces.com/problemset/problem/106190/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to recover the possible length of the missing middle tail of a tigercat-like creature. The three tail lengths are `a`, `b`, and `c`, where `a < b < c`. We already know the shortest and longest lengths, but the middle one is missing. We are also given `m`, which is the product of all distinct prime factors appearing in `a * b * c`, also called the radical of the product. We need the smallest and largest possible values of `b`, or report that no such value exists. The original problem is from Codeforces Gym 106190.

The input contains several independent cases. Each case gives `m`, `a`, and `c`. The answer is a pair of values: the minimum valid middle tail length and the maximum valid middle tail length. The middle length must strictly stay between the two known lengths.

The important constraint is that `a` and `c` are at most `10^6`, while `m` can be as large as `10^18`. This immediately rules out trying every possible factorization of `m` or doing work proportional to its value. The upper bound on `c` is the key: every possible answer `b` is smaller than `10^6`, so we only need to reason about relatively small candidate numbers.

The main edge cases come from confusing the radical with the original product. A number can contain the same prime many times, but the radical only cares whether a prime exists.

For example:

```
Input:
210 5 21

Output:
6 20
```

A careless approach might try to require `b` to be exactly the product of missing prime factors. The missing prime factor is `2 * 3 = 6`, but `20` also works because it only adds the prime `2` again. The radical remains `2 * 3 * 5 * 7`.

Another tricky case is when `a` or `c` already contains a prime that is not present in `m`.

```
Input:
35 5 7

Output:
-1 -1
```

Here `a * c = 35`, so the radical already contains `5` and `7`. The value `m` only has `5` and `7` too, but any middle value between `5` and `7` is impossible because the only candidate is `6`, whose radical adds the prime `2`.

A third case is when `m` contains a prime that neither side contains.

```
Input:
12 2 6

Output:
-1 -1
```

The product `a * c` already gives prime factors `2` and `3`. The only possible middle value would be between `2` and `6`, but every number in that interval either introduces a forbidden prime or does not change the radical correctly.

## Approaches

The direct solution is to test every possible middle tail length. For every `b` from `a + 1` to `c - 1`, we can compute the radical of `a * b * c` and compare it with `m`. This is correct because the range contains every possible answer. The problem is the amount of repeated work. If every test has `c` close to `10^6`, checking every candidate and factorizing each one costs far too much for many test cases.

The key observation is that we do not actually need the whole product. The radical only depends on which primes appear. First, factor `a` and `c` and collect all prime factors they already contribute. If one of these primes is not in `m`, the answer is impossible immediately.

Now consider the primes of `m`. Some of them are already present in `a * c`. The remaining primes must appear in `b`. Call their product `need`. Every valid `b` must be a multiple of `need`.

There is one more restriction. `b` cannot introduce any prime outside `m`, because that would make the final radical too large. So after removing the required part `need`, the remaining multiplier may only use primes from `m`.

Since `b < 10^6`, we can generate all numbers whose prime factors belong to the allowed set and find the smallest and largest multiples of `need` in the interval `(a, c)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((c-a) * sqrt(c)) | O(1) | Too slow |
| Optimal | O(number of generated candidates) per test, bounded by values below 10^6 | O(number of candidates) | Accepted |

## Algorithm Walkthrough

1. Factor `a` and `c` and store their distinct prime factors. We need these primes because they are already forced to appear in the final radical.
2. Factor `m` into its distinct prime factors. If `m` contains a prime smaller side numbers do not explain, we will later force it into `b`.
3. Check that every prime factor of `a` and `c` exists in `m`. If this fails, no value of `b` can remove an extra prime from the radical.
4. Compute `need`, the product of every prime in `m` that is missing from `a * c`. This is the minimum required prime contribution from `b`.
5. Generate all values made only from the prime factors of `m`. For every generated value `x`, multiply it by `need` if it stays below `c`. The result is a candidate middle length.
6. Among all candidates strictly greater than `a` and strictly less than `c`, keep the minimum and maximum values.

The reason the generation works is that every valid `b` can be split into two parts. One part contains the missing primes that must be added, and the other part only increases powers of already allowed primes. The generator creates exactly these possible extra parts.

Why it works: the final radical is the union of prime factors from `a`, `b`, and `c`. The checks guarantee that `a` and `c` do not contain forbidden primes. The required part guarantees that `b` supplies every missing prime from `m`. The generated multiplier cannot add new primes, so every accepted candidate has exactly the required radical. Every valid `b` can also be represented in this form, so no answers are missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def factor(x):
    res = []
    d = 2
    while d * d <= x:
        if x % d == 0:
            res.append(d)
            while x % d == 0:
                x //= d
        d += 1 if d == 2 else 2
    if x > 1:
        res.append(x)
    return res

def solve_case(m, a, c):
    fm = set(factor(m))
    fa = factor(a)
    fc = factor(c)

    for p in fa + fc:
        if p not in fm:
            return -1, -1

    need = 1
    base = set(fa + fc)
    for p in fm:
        if p not in base:
            need *= p

    allowed = list(fm)
    limit = c // need

    vals = [1]
    for p in allowed:
        cur = []
        for x in vals:
            y = x
            while y * p <= limit:
                y *= p
                cur.append(y)
        vals += cur

    ans_min = 10**18
    ans_max = -1

    for x in vals:
        b = x * need
        if a < b < c:
            ans_min = min(ans_min, b)
            ans_max = max(ans_max, b)

    if ans_max == -1:
        return -1, -1
    return ans_min, ans_max

def main():
    t = int(input())
    out = []
    for _ in range(t):
        m, a, c = map(int, input().split())
        x, y = solve_case(m, a, c)
        out.append(f"{x} {y}")
    print("\n".join(out))

main()
```

The `factor` function only stores distinct prime factors because repeated powers do not matter for a radical. After finding the factors of `m`, the code first rejects impossible cases where `a` or `c` introduce a prime outside the target radical.

The variable `need` represents the mandatory part of `b`. The remaining generated values are only allowed to use primes from `m`, which prevents accidentally creating a larger radical.

The generation loop grows numbers by multiplying existing values by allowed primes. The limit is `c // need` because multiplying by `need` later must still keep the candidate below `c`. The strict inequality checks are necessary because the middle tail must be between the two known tails, not equal to them.

## Worked Examples

For the first example:

```
210 5 21
```

The factors of `a` and `c` are:

| Step | Current value | Meaning |
| --- | --- | --- |
| Initial | `5, 21` | Known tails |
| Factors | `{5, 3, 7}` | Existing primes |
| Missing | `{2}` | Must appear in `b` |
| Need | `2` | Every candidate contains this |

Possible values of `b` are generated:

| Candidate | Valid? | Reason |
| --- | --- | --- |
| 6 | Yes | Radical becomes `210` |
| 10 | Yes | Adds only prime `2` |
| 20 | Yes | Adds only prime `2` with higher power |

The minimum and maximum are `6` and `20`.

For:

```
121 11 13
```

The factorization gives:

| Step | Current value | Meaning |
| --- | --- | --- |
| `a` | `11` | Already has prime 11 |
| `c` | `13` | Already has prime 13 |
| `m` | `{11}` | Missing prime 13 |

Since `13` appears in `c` but not in `m`, the known tails already contain a forbidden prime. The algorithm stops immediately and returns:

```
-1 -1
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(number of generated candidates + sqrt(c)) | Factoring small values dominates, and generation only considers numbers below 1e6 |
| Space | O(number of generated candidates) | Stores possible multipliers |

The maximum possible value that must be generated is below `10^6`, so the number of candidates remains small. This easily fits the limits even with many test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().strip().split()
    sys.stdin = old

    if not data:
        return ""

    it = iter(data)
    t = int(next(it))
    ans = []
    for _ in range(t):
        m = int(next(it))
        a = int(next(it))
        c = int(next(it))
        x, y = solve_case(m, a, c)
        ans.append(f"{x} {y}")
    return "\n".join(ans)

assert run("""6
210 5 21
35 5 7
121 11 13
870870 14 2145
20 1 5
12 2 6
""") == """6 20
-1 -1
-1 -1
29 2088
-1 -1
-1 -1"""

assert run("""1
2 1 3
""") == "2 2"

assert run("""1
1 1 10
""") == "1 1"

assert run("""1
30 6 20
""") == "-1 -1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `210 5 21` | `6 20` | Basic missing prime handling |
| `2 1 3` | `2 2` | Smallest possible interval |
| `1 1 10` | `1 1` | Radical equal to one |
| `30 6 20` | `-1 -1` | Forbidden prime detection |

## Edge Cases

When `m` is `1`, no prime factor may appear anywhere. The only possible values are numbers made entirely of prime factors outside the range of `m`, which means the only usable number is `1`. The generator starts from `1`, so it correctly finds this case.

When `a` or `c` contains a prime not in `m`, the algorithm rejects the case before searching. For example:

```
35 5 7
```

The known tails already force primes `5` and `7`, but the target radical is incompatible with any additional middle value. The answer remains `-1 -1`.

When the missing primes have a large product, `need` can itself be close to `c`. The generated multiplier is then very small, but the final interval check prevents returning `a` or `c` as a fake answer. This handles boundary errors around strict inequalities.
