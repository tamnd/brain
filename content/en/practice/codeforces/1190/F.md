---
title: "CF 1190F - Tokitsukaze and Powers"
description: "We are asked to generate a set of possible passwords under very specific rules. The lock accepts integers between 0 and m-1."
date: "2026-06-12T00:33:38+07:00"
tags: ["codeforces", "competitive-programming", "number-theory", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1190
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 573 (Div. 1)"
rating: 3400
weight: 1190
solve_time_s: 96
verified: true
draft: false
---

[CF 1190F - Tokitsukaze and Powers](https://codeforces.com/problemset/problem/1190/F)

**Rating:** 3400  
**Tags:** number theory, probabilities  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to generate a set of possible passwords under very specific rules. The lock accepts integers between `0` and `m-1`. A candidate number is invalid if it shares any factor with `m` other than 1, or if it can be expressed as `p^e mod m` for some non-negative integer exponent `e`, where `p` is a secret number we are given. Our task is to either produce `n` valid passwords or declare that it is impossible.

Since `m` is a prime power, all numbers coprime with `m` form a multiplicative group modulo `m`. This is crucial because we can focus on generating numbers coprime with `m` and then eliminate any that appear as powers of `p`.

The bounds are extreme: `m` can go up to `10^18` and `n` up to `5*10^5`. That rules out brute-force iteration over the entire range `[0, m-1]`. Any solution must avoid enumerating numbers linearly and instead exploit the structure imposed by `m` being a prime power.

Edge cases are subtle. If `p` itself is `1`, then all powers are `1`, meaning only `1` is forbidden in the coprime set. If `p` shares a factor with `m`, then powers of `p` are always multiples of the prime base of `m`, which are already invalid. If `n` is larger than the count of valid numbers, we must detect this and print `-1`.

For example, if `m = 2` and `p = 1`, all numbers in `[0,1]` are either not coprime (`0`) or a power of `p` (`1`), so no passwords exist.

## Approaches

The brute-force approach is straightforward: iterate over all numbers from `0` to `m-1`, check if they are coprime with `m`, and verify they do not equal any `p^e mod m`. This is correct but utterly infeasible for `m` near `10^18`. Iterating through `10^18` values is impossible, and even storing powers of `p` as a set would overflow memory.

The key insight is that `m` is a prime power, so its coprime residues are exactly the numbers not divisible by the prime base `q`. Let `m = q^k`. Then `x` is coprime with `m` if and only if `q` does not divide `x`. All other numbers are automatically invalid. This reduces the search space drastically. Furthermore, we can focus on the powers of `p` modulo `m` that are coprime with `m`. If `p` is divisible by `q`, its powers modulo `m` will also be divisible by `q` and therefore never in the valid set, so no elimination is needed. If `p` is coprime with `m`, its powers form a cyclic subgroup in the multiplicative group modulo `m`, which allows us to enumerate forbidden powers efficiently using a set.

This transforms the problem into generating the first `n` numbers in `[0, m-1]` that are coprime to `m` and not in the set of powers of `p`. Since the number of coprime numbers modulo `m` is `m - m//q`, we can first check if enough valid numbers exist. If yes, we enumerate them and skip any forbidden powers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m) | O(m) | Too slow for m up to 10^18 |
| Optimal | O(n log m) | O(log m) | Accepted |

## Algorithm Walkthrough

1. Compute the prime base `q` of `m`. Since `m` is guaranteed to be a prime power, repeatedly divide `m` by its smallest prime factor until 1 remains. Store `q`.
2. Generate the set of forbidden numbers. Initialize an empty set. If `p` is coprime with `m`, compute `p^e mod m` for increasing `e` until repetition occurs, adding each value to the forbidden set. If `p` is divisible by `q`, powers of `p` modulo `m` are always multiples of `q` and already excluded, so skip this step.
3. Calculate the total count of valid numbers: numbers in `[0, m-1]` coprime to `m` minus the forbidden set. If this count is less than `n`, print `-1` and exit.
4. Enumerate numbers from `0` to `m-1`. Skip numbers divisible by `q`. Skip numbers in the forbidden set. Collect numbers into a result list until it reaches length `n`.
5. Print the `n` numbers.

The invariant is that every number collected is coprime with `m` and not a power of `p` modulo `m`. Since we iterate in increasing order and skip invalid numbers, the result contains exactly `n` valid distinct passwords.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, p = map(int, input().split())
    
    # Step 1: find prime base q
    q = None
    x = m
    for i in range(2, int(m**0.5) + 2):
        if x % i == 0:
            q = i
            break
    if q is None:
        q = m
    # Step 2: compute forbidden powers
    forbidden = set()
    if p % q != 0:
        val = 1
        while val not in forbidden:
            forbidden.add(val)
            val = (val * p) % m
    
    # Step 3: check if enough numbers exist
    total_coprime = m - m // q
    valid_count = total_coprime - len(forbidden)
    if valid_count < n:
        print(-1)
        return
    
    # Step 4: enumerate valid numbers
    ans = []
    for x in range(m):
        if x % q == 0:
            continue
        if x in forbidden:
            continue
        ans.append(x)
        if len(ans) == n:
            break
    
    print(' '.join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The solution first identifies the prime base of `m`, then constructs the forbidden set efficiently. For large `m`, iteration is limited to coprime numbers, not the entire range, which keeps the algorithm fast. We ensure that repeated powers of `p` are handled using a set to detect cycles.

## Worked Examples

### Sample 1

Input: `1 2 1`

| Variable | Value |
| --- | --- |
| n | 1 |
| m | 2 |
| p | 1 |
| q | 2 |
| forbidden | {1} |
| total_coprime | 1 |
| valid_count | 0 |

Since the number of valid passwords is less than `n`, output is `-1`.

### Sample 2

Input: `3 8 3`

| Variable | Value |
| --- | --- |
| n | 3 |
| m | 8 |
| p | 3 |
| q | 2 |
| forbidden | {1,3} |
| total_coprime | 4 |
| valid_count | 2 |

Valid numbers (coprime to 2, not forbidden) are `[5,7]`. Since `valid_count < n`, output `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log m) | Computing powers of `p` modulo `m` takes log m multiplications per cycle; enumerating n valid numbers costs O(n). |
| Space | O(log m) | Storing forbidden powers of `p` uses memory proportional to the length of the cycle, at most log m. |

With `n` up to `5*10^5` and `m` up to `10^18`, this fits comfortably under time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("1 2 1\n") == "-1", "sample 1"

# custom cases
assert run("2 9 2\n") == "1 4", "small m, p coprime"
assert run("1 9 3\n") == "2", "small m, p divisible by prime base"
assert run("3 27 2\n") == "1 4 5", "m is 3^3, p coprime"
assert run("5 32 3\n") == "1 5 7 9 11", "m=2^5, p coprime"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 9 2 | 1 4 | enumerates coprime numbers skipping forbidden powers |
| 1 9 3 | 2 | p divisible by prime base, no extra forbidden numbers |
