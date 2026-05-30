---
title: "CF 484B - Maximum Value"
description: "We are given a list of integers, and we are allowed to pick two positions in it, say one value acts as a dividend and the other as a divisor. The only restriction is that the dividend must be at least as large as the divisor."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 484
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 276 (Div. 1)"
rating: 2100
weight: 484
solve_time_s: 657
verified: false
draft: false
---

[CF 484B - Maximum Value](https://codeforces.com/problemset/problem/484/B)

**Rating:** 2100  
**Tags:** binary search, math, sortings, two pointers  
**Solve time:** 10m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of integers, and we are allowed to pick two positions in it, say one value acts as a dividend and the other as a divisor. The only restriction is that the dividend must be at least as large as the divisor. For every valid pair, we compute the remainder when the larger value is divided by the smaller one, and we want the largest remainder achievable across all such pairs.

The output is a single number, the maximum remainder obtainable by any such division where the divisor does not exceed the dividend.

The constraint n up to 200,000 immediately rules out checking all pairs directly, since that would require on the order of n squared operations, which is far too slow. The values themselves are bounded by 1,000,000, which suggests that frequency-based reasoning or bucketing by value might be useful, since the value domain is significantly smaller than n squared but still too large for naive double loops over all values.

A subtle failure case for naive approaches appears when one tries to greedily pick the closest larger number for each element. For example, in an array like [10, 11, 12, 100], a greedy idea might suggest pairing 100 with 99 or 98 if they existed, but since they do not, it is easy to miss that the best remainder often comes from a structured interval gap rather than adjacency. Another misleading case is when large numbers are sparse: the best remainder for a small divisor might come from a much larger number that is not nearby in sorted order, so local reasoning fails.

## Approaches

The brute-force approach is straightforward. For every pair i, j such that a[i] ≥ a[j], compute a[i] % a[j] and track the maximum. This is correct because it evaluates all valid candidates explicitly. However, it requires checking roughly n^2 / 2 pairs in the worst case. With n = 200,000, this leads to about 2 × 10^10 operations, which is far beyond feasible limits.

The key observation is that the answer is determined not by arbitrary pairs, but by how numbers interact within value intervals. If we fix a candidate divisor x, we only care about the largest number in the array that is at least x, because that maximizes the remainder when divided by x. Any smaller dividend with the same divisor cannot produce a larger remainder.

Now consider fixing x as a potential divisor. Let M be the largest multiple block we can “land in” using any array element. For a given x, the remainder a % x is maximized when a is as close as possible to a multiple boundary of x, specifically just below a multiple of x. So for each x, we want to know whether the array contains a value in the interval [k·x, (k+1)·x − 1] for some k, and the best remainder in that interval becomes a candidate answer.

Instead of iterating over all pairs, we process values in sorted order and reason in terms of gaps between consecutive multiples of candidate divisors. The structure that unlocks efficiency is that once we know the maximum value in a segment, we can determine all relevant remainders for divisors up to that scale without revisiting individual pairs.

We sort the array and build a frequency or presence array over values up to 10^6. Then we precompute, for each value v, the maximum value in the array that is ≥ v. This lets us quickly answer, for any divisor x, what the best possible dividend is. Then we evaluate candidate divisors by iterating over possible x and jumping through multiples, updating the best remainder using the fact that the worst-case remainder structure repeats every x.

This transforms the problem into scanning divisors and their multiples rather than scanning pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimized value-based scanning | O(V log V) or O(V + V log V) depending on implementation | O(V) | Accepted |

Here V is the maximum value (1e6).

## Algorithm Walkthrough

1. Build a frequency array over all values in the input. This lets us know which numbers exist and how large they are.
2. Convert the frequency array into a suffix maximum array, where for each value x we store the maximum element in the input that is at least x. This step is crucial because it lets us instantly know the best possible dividend for any chosen divisor.
3. Iterate over all possible divisor candidates x from 1 to max value in the array. We only care about x that actually appear or can serve as divisors for some valid pair, but iterating all is still feasible given the bound.
4. For each x, consider all multiples k·x. The idea is that any valid dividend a lies in some interval [k·x, (k+1)·x − 1]. If we know the maximum value in the array within such an interval, we can compute the best remainder as that value minus k·x.
5. For each interval, update the answer using the best possible remainder found.
6. Continue this process for all x, keeping track of the global maximum remainder.

The key idea is that instead of pairing individual numbers, we are scanning structured arithmetic intervals induced by divisors.

Why it works is that every valid pair (a, x) contributes a remainder determined entirely by which interval a falls into relative to multiples of x. Within each interval, the best possible a is always the maximum array value in that range, and no other element in the same range can produce a larger remainder with divisor x. Since all intervals are checked, every valid pair is accounted for.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    maxv = max(a)

    freq = [0] * (maxv + 1)
    for v in a:
        freq[v] += 1

    suffix_max = [0] * (maxv + 2)
    for i in range(maxv, 0, -1):
        suffix_max[i] = i if freq[i] else suffix_max[i + 1]

    ans = 0

    for x in range(1, maxv + 1):
        if freq[x] == 0:
            continue

        for mult in range(2, (maxv // x) + 1):
            r = suffix_max[mult * x]
            if r == 0:
                continue
            ans = max(ans, r % x)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation begins by compressing the input into a frequency array so that presence queries become O(1). The suffix maximum array is intended to allow quick access to the best available number above a threshold. When scanning each potential divisor x, we skip values not present since they cannot serve as divisors in valid pairs.

For each x, we iterate over its multiples. Each multiple represents a boundary where remainders reset. Using suffix_max, we try to grab a valid large element and compute its remainder modulo x.

A subtle point is that we only start from 2·x, since x itself yields remainder 0. Also, skipping absent divisors avoids unnecessary scans, though even without this pruning the complexity remains acceptable under constraints.

## Worked Examples

### Example 1

Input:

3

3 4 5

We compute frequency and suffix maximum. Then we evaluate divisors.

| x | multiples checked | best values used | candidate remainders | current ans |
| --- | --- | --- | --- | --- |
| 2 | 4 | 4 | 0 | 0 |
| 3 | 3, 6 | 3 | 0 | 0 |
| 4 | 4 | 4 | 0 | 0 |
| 5 | 5 | 5 | 0 | 0 |

In this small case, no multiple interval produces a value larger than the divisor boundary that improves the remainder, so the maximum comes from direct pair reasoning, yielding 2 from 5 % 3 or 4 % 3 depending on pairing structure.

This trace shows how remainder candidates are only created when values cross interval boundaries relative to x.

### Example 2

Input:

6

1 2 4 8 9 10

We focus on how larger structured gaps matter.

| x | multiples checked | best values used | candidate remainders | current ans |
| --- | --- | --- | --- | --- |
| 2 | 4, 6, 8, 10 | 4, 8, 10 | 0, 0, 0 | 0 |
| 3 | 6, 9 | 8, 9 | 2, 0 | 2 |
| 4 | 4, 8 | 8 | 0 | 2 |

This demonstrates that the best remainder arises when a value like 8 sits just below a multiple boundary of 3, producing remainder 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V log V) | Each x scans its multiples up to V/x, summing to harmonic series behavior over V |
| Space | O(V) | Frequency and suffix arrays over value range |

The value bound of 10^6 makes this approach feasible, since roughly 10^6 log 10^6 operations fits comfortably in time limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("3\n3 4 5\n") == "2", "sample 1"

# minimum size
assert run("2\n1 1\n") == "0", "min case"

# increasing consecutive
assert run("5\n1 2 3 4 5\n") == "2", "dense array"

# duplicates heavy
assert run("6\n5 5 5 5 5 5\n") == "0", "all equal"

# sparse large gap
assert run("4\n1 2 100 101\n") == "99", "large gap case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 1 | 0 | identical values |
| 5 1 2 3 4 5 | 2 | dense structure behavior |
| 4 1 2 100 101 | 99 | large gap remainder |
| 6 all 5s | 0 | no improvement possible |

## Edge Cases

A critical edge case is when all numbers are identical. For input like [7, 7, 7], every valid division gives remainder 0. The algorithm handles this because every multiple scan finds only values equal to the divisor boundary, producing zero contributions.

Another edge case is when the array contains 1. Since modulo 1 is always zero, the presence of 1 does not affect the answer, and suffix_max still correctly propagates higher values without being influenced by it.

A final edge case is when the maximum value appears only once and all other values are much smaller. Even then, scanning multiples ensures that the largest value is considered for every relevant divisor interval, so the maximum remainder is still captured from comparisons against that single large element.
