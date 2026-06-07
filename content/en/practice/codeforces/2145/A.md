---
title: "CF 2145A - Candies for Nephews"
description: "Monocarp wants to divide a certain number of candies evenly among his three nephews. He starts with n candies and needs to figure out how many more, if any, he must buy to make the total divisible by three."
date: "2026-06-08T01:31:06+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 2145
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 183 (Rated for Div. 2)"
rating: 800
weight: 2145
solve_time_s: 79
verified: true
draft: false
---

[CF 2145A - Candies for Nephews](https://codeforces.com/problemset/problem/2145/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

Monocarp wants to divide a certain number of candies evenly among his three nephews. He starts with `n` candies and needs to figure out how many more, if any, he must buy to make the total divisible by three. The input consists of multiple test cases, each giving a single integer `n`. The output for each test case is the smallest non-negative integer `k` such that `n + k` is divisible by three.

The constraints are small: `n` can go up to 100, and there are at most 100 test cases. This means we can afford very simple arithmetic operations per test case without worrying about performance. No complex data structures or algorithms are needed.

The non-obvious edge cases arise when `n` is already divisible by three, in which case Monocarp does not need to buy any extra candies. For example, if `n = 24`, the correct answer is `0`. If `n = 7`, Monocarp needs `2` additional candies because `7 + 2 = 9`, which is divisible by three. A careless solution that blindly adds a fixed number or forgets to handle the case `n % 3 == 0` would produce wrong answers.

## Approaches

The brute-force approach is conceptually simple. For each `n`, we could start from zero additional candies and incrementally test `n + k` until it is divisible by three. This works because eventually we will reach a number divisible by three, but even with small constraints this is unnecessary. It involves up to two extra checks per test case, which is trivial for this problem, but the arithmetic insight allows us to solve it directly.

The key observation is that to make `n` divisible by three, we only need to consider the remainder `r = n % 3`. If `r` is zero, no candies are needed. If `r` is one, we need `2` more candies, and if `r` is two, we need `1` more candy. This comes from simple modular arithmetic: we are essentially solving `(n + k) % 3 == 0` for the smallest non-negative `k`.

The optimal approach is therefore to compute the remainder of `n` modulo three and subtract it from three, except when the remainder is zero. This avoids unnecessary looping entirely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) per test case | O(1) | Accepted but unnecessary |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n`, the number of candies Monocarp currently has.
3. Compute the remainder `r = n % 3`.
4. If `r` is zero, print `0`. Otherwise, print `3 - r`. This gives the minimum number of candies to add to make the total divisible by three.
5. Repeat for all test cases.

Why it works: the invariant is that we always want the total candy count divisible by three. The modulo operation directly measures how far we are from the nearest multiple of three. Adding `3 - r` corrects the remainder without overshooting. This guarantees that the total becomes divisible by three in the minimal number of extra candies.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    r = n % 3
    print(0 if r == 0 else 3 - r)
```

The code first reads the number of test cases. For each test case, it computes the remainder of `n` divided by three. If the remainder is zero, it outputs zero; otherwise, it outputs `3 - r`. There are no off-by-one issues because `n % 3` always produces 0, 1, or 2. Using `3 - r` ensures we always add the minimal number of candies needed.

## Worked Examples

For the input `7`:

| n | n % 3 | r | 3 - r | Output |
| --- | --- | --- | --- | --- |
| 7 | 1 | 1 | 2 | 2 |

Adding 2 candies gives `9` candies, divisible by three, so each nephew gets `3`.

For the input `24`:

| n | n % 3 | r | 3 - r | Output |
| --- | --- | --- | --- | --- |
| 24 | 0 | 0 | - | 0 |

No candies are needed because `24` is already divisible by three.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires a single modulo operation and a conditional check. |
| Space | O(1) | Only a few integer variables are used. |

Given that `t` is at most 100 and `n` is at most 100, this solution easily runs within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    for _ in range(t):
        n = int(input())
        r = n % 3
        print(0 if r == 0 else 3 - r)
    
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("2\n7\n24\n") == "2\n0", "sample 1"

# custom cases
assert run("3\n1\n2\n3\n") == "2\n1\n0", "small numbers"
assert run("2\n100\n99\n") == "2\n0", "large divisible cases"
assert run("1\n0\n") == "0", "zero candies"
assert run("1\n5\n") == "1", "remainder 2 case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 2, 3 | 2, 1, 0 | small numbers and remainder logic |
| 100, 99 | 2, 0 | correctness for large numbers |
| 0 | 0 | zero candies case |
| 5 | 1 | remainder 2 correction |

## Edge Cases

For `n = 0`, `0 % 3` is zero, so the algorithm correctly outputs `0`. For `n = 1` or `n = 2`, the algorithm computes `3 - r` as `2` and `1` respectively, which matches the minimal extra candies needed. No special handling is required beyond the simple modulo computation. For `n` already divisible by three, the algorithm outputs zero, ensuring we never overshoot. Each of these edge cases confirms that the modulo-based solution is robust.
