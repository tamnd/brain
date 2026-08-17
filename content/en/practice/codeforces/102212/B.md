---
title: "CF 102212B - Racetrack"
description: "Alice scores exactly a points every time she plays, while Bob scores exactly b points every time he plays. After some number of games, their total scores are equal. The task is to find the smallest positive score that both players can have."
date: "2026-08-18T00:25:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102212
codeforces_index: "B"
codeforces_contest_name: "Amazalgo Uni 2019 Practice Contest"
rating: 0
weight: 102212
solve_time_s: 180
verified: false
draft: false
---

[CF 102212B - Racetrack](https://codeforces.com/problemset/problem/102212/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m  
**Verified:** no  

## Solution
## Problem Understanding

Alice scores exactly `a` points every time she plays, while Bob scores exactly `b` points every time he plays. After some number of games, their total scores are equal. The task is to find the smallest positive score that both players can have.

If Alice plays `x` times, her score is `a * x`. If Bob plays `y` times, his score is `b * y`. We need the smallest positive integer `c` for which both `a` and `b` divide `c`. In other words, the problem is asking for the least common multiple of `a` and `b`.

Both input values are at most `10,000`. A direct search through every possible score could reach `100,000,000`, which is large enough to make a linear search undesirable under a 1 second limit. The structure of the problem gives us a constant-time arithmetic solution instead. The answer itself also fits comfortably in the stated limit, since the largest possible least common multiple for two values in this range is at most `10,000 * 9,999 = 99,990,000`.

There are a few small cases that can expose careless implementations. For input `1 1`, the answer is `1`, because both players already gain one point per game. An implementation that starts searching from `a + b` would miss the minimum. For input `1 10000`, the answer is `10000`, because every positive multiple of `10000` is also divisible by `1`; treating the two values symmetrically through an incorrect formula could produce a larger result. For input `4 6`, the answer is `12`, not `24`, because `12` is already divisible by both values. This catches approaches that simply multiply the inputs instead of removing their shared factor.

## Approaches

A straightforward brute-force solution can generate possible scores until it finds one divisible by both `a` and `b`. For example, starting with `1`, we could test whether each integer `c` satisfies `c % a == 0` and `c % b == 0`. The first such value is necessarily the answer because every smaller positive value has already been rejected.

The problem with this version is that the search range can be very large. For `a = 10000` and `b = 9999`, the answer is `99,990,000`, so checking every integer from `1` through the answer requires `99,990,000` iterations. Even though each iteration is simple, this is far more work than necessary.

We can make the search smaller by considering only multiples of one input. If we test `a`, `2a`, `3a`, and so on, the first multiple that is also divisible by `b` is the least common multiple. Since the answer is at most `100,000,000` and `a` is at least `1`, this can still require up to about `100,000,000` iterations when `a = 1`, so it is not the cleanest solution either.

The key observation is that the common part of `a` and `b` must not be counted twice. Let `g = gcd(a, b)`. The product `a * b` contains every factor of `a` and `b`, but the factors represented by `g` appear in both. Dividing their product by `g` removes exactly that duplicated part, giving the least common multiple:

`lcm(a, b) = a * b / gcd(a, b)`.

The brute-force works because it searches for the first number having both divisibility properties, but fails because it ignores the arithmetic relationship between the two inputs. The observation that their shared factors can be identified with the greatest common divisor lets us compute the same answer directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(lcm(a, b)) | O(1) | Too slow in the worst case |
| Optimal | O(log(min(a, b))) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `a` and `b`, the number of points Alice and Bob gain per game.
2. Compute `g = gcd(a, b)` using the Euclidean algorithm. The gcd contains exactly the factors shared by both scoring values.
3. Compute `a * b // g`. This is the least common multiple because multiplying `a` and `b` combines all their factors, while dividing by the gcd removes the factors that were included twice.
4. Print the resulting value. It is the smallest positive score divisible by both `a` and `b`, so both players can reach it using an integer number of games.

### Why it works

Let `g = gcd(a, b)`. We can write `a = g * x` and `b = g * y`, where `x` and `y` are coprime. Since `x` and `y` have no common factors, the smallest number containing all factors needed for both inputs is `g * x * y`. Substituting `x = a / g` and `y = b / g` gives `(a / g) * b`, which is exactly `a * b / g`. This value is divisible by both `a` and `b`, and any common multiple must contain the same required factors, so no smaller positive common multiple exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

a, b = map(int, input().split())

g = gcd(a, b)
answer = a * b // g

print(answer)
```

The `gcd` function implements the Euclidean algorithm. At each iteration, the pair `(a, b)` is replaced by `(b, a % b)`. The set of common divisors does not change under this transformation, and the second value eventually becomes zero. The remaining first value is the gcd.

After computing the gcd, the code evaluates `a * b // g`. Integer division is exact here because `g` divides both `a` and `b`, so it necessarily divides their product. Python integers also do not overflow, although the largest intermediate product here is only `100,000,000` anyway.

There is no loop over possible scores, so there are no boundary conditions involving the answer itself and no off-by-one issue. The inputs are guaranteed to be positive, so the gcd is also positive and division by zero cannot occur.

## Worked Examples

### Sample 1

For `a = 2` and `b = 3`, the two values have no common factor other than `1`.

| a | b | gcd(a, b) | a * b | Answer |
| --- | --- | --- | --- | --- |
| 2 | 3 | 1 | 6 | 6 |

The gcd is `1`, so no duplicated factor needs to be removed from the product. The smallest score divisible by both `2` and `3` is `6`. Alice reaches it after `3` games, while Bob reaches it after `2` games.

### Sample 2

For `a = 4` and `b = 6`, the values share a factor of `2`.

| a | b | gcd(a, b) | a * b | Answer |
| --- | --- | --- | --- | --- |
| 4 | 6 | 2 | 24 | 12 |

The product `24` counts the shared factor `2` twice. Dividing by the gcd removes that duplication, producing `12`. Alice reaches `12` after `3` games and Bob reaches it after `2` games.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(min(a, b))) | The Euclidean algorithm repeatedly replaces the pair with smaller remainders. |
| Space | O(1) | Only a constant number of integer variables are stored. |

With both inputs at most `10,000`, the Euclidean algorithm takes only a handful of iterations. The solution is easily within the 1 second time limit and uses negligible memory compared with the 64 MB limit.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    data = inp.split()
    a, b = map(int, data)

    x, y = a, b
    while y:
        x, y = y, x % y

    return str(a * b // x) + "\n"

def run(inp: str) -> str:
    return solve(inp)

# Provided samples
assert run("2 3") == "6\n", "sample 1"
assert run("4 6") == "12\n", "sample 2"

# Minimum-size inputs
assert run("1 1") == "1\n", "minimum values"

# One value divides the other
assert run("1 10000") == "10000\n", "one divides the other"

# Equal values
assert run("10000 10000") == "10000\n", "equal maximum values"

# Maximum answer in the allowed input range
assert run("9999 10000") == "99990000\n", "maximum LCM"

# Shared factors, catches incorrect multiplication
assert run("12 18") == "36\n", "shared factors"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum-size input and the smallest possible answer |
| `1 10000` | `10000` | A value equal to `1` and a case where one input divides the other |
| `10000 10000` | `10000` | Equal values, including the largest allowed input |
| `9999 10000` | `99990000` | Largest-answer boundary within the constraints |
| `12 18` | `36` | Correctly removes shared factors instead of returning the product |

## Edge Cases

For `1 1`, the gcd is `1`, so the formula gives `1 * 1 / 1 = 1`. The algorithm does not assume that the answer must be greater than either input, and correctly returns the smallest possible positive score.

For `1 10000`, the Euclidean algorithm computes `gcd(1, 10000) = 1`. The result is `1 * 10000 / 1 = 10000`. This works because every integer is divisible by `1`, so the first positive score that Bob can reach is already a valid score for Alice.

For `4 6`, the gcd is `2`. The formula gives `4 * 6 / 2 = 12`. A careless implementation using only `a * b` would return `24`, which is a common multiple but not the smallest one. Dividing by the gcd is precisely what removes the duplicated factor.

For `9999 10000`, the gcd is `1`, so there is no factor to remove. The product is `99,990,000`, which is the least common multiple and also demonstrates that the answer can be close to the stated upper bound of `100,000,000`. The algorithm handles this boundary directly without iterating through the millions of smaller candidate scores.
