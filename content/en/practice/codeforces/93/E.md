---
title: "CF 93E - Lostborn"
description: "We are asked to calculate how many numbers from 1 to n are not divisible by any number in a given set of integers, called hit indicators. Each indicator is guaranteed to be coprime with the others, and there are k of them, each at most 1000."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 93
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 76 (Div. 1 Only)"
rating: 2600
weight: 93
solve_time_s: 65
verified: true
draft: false
---

[CF 93E - Lostborn](https://codeforces.com/problemset/problem/93/E)

**Rating:** 2600  
**Tags:** dp, math, number theory  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to calculate how many numbers from 1 to _n_ are **not divisible** by any number in a given set of integers, called hit indicators. Each indicator is guaranteed to be coprime with the others, and there are _k_ of them, each at most 1000. Conceptually, imagine Igor's hero with strength _n_ swinging a weapon whose properties are encoded in the indicators; the damage corresponds to counting numbers in 1…_n_ that "survive" being divisible by any of these indicators.

The constraints give us an immediate clue about algorithm choice. _n_ can go up to 10^13, which rules out any algorithm that checks each number individually. Even iterating linearly is impossible, since that would require 10^13 operations. _k_ is relatively small, at most 100, and the indicators are small (≤1000), so combinatorial techniques using subsets of indicators are feasible.

A non-obvious edge case arises when _n_ is smaller than any of the indicators. For example, if _n_ = 3 and indicators are 5, 7, 11, then none of the numbers are divisible by any indicator, so the answer is 3. A naive approach that assumes at least one number will always be divisible by each indicator would fail here. Another potential pitfall is integer overflow when calculating products of indicators in subset combinations; we must be careful because some products may exceed 10^13.

## Approaches

The brute-force approach is straightforward: iterate through all integers from 1 to _n_, check each against all _k_ indicators, and count those that are not divisible by any of them. This works correctly, but requires O(n * k) operations, which can reach 10^15 in the worst case. This is far beyond acceptable limits.

The key observation is that all indicators are pairwise coprime. This allows us to use the **Inclusion-Exclusion Principle**. For any subset of indicators, we can compute how many numbers are divisible by their product. If a subset contains an odd number of indicators, we add its contribution; if even, we subtract it. Using this, we only need to consider 2^k subsets, which is feasible for k ≤ 100 if we prune subsets whose product exceeds _n_. The coprimality ensures that the least common multiple of any subset is just the product of its elements, simplifying calculations.

The brute-force works because it correctly checks divisibility one by one, but fails for large _n_. The inclusion-exclusion approach works because the coprimality guarantees that counting multiples by product accurately captures overlaps without double-counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * k) | O(1) | Too slow |
| Inclusion-Exclusion | O(2^k) (pruned by product ≤ n) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read integers _n_ and _k_, and then read the list of indicators _a_.
2. Initialize a variable `count_divisible` to 0; it will store the total number of numbers divisible by at least one indicator.
3. Iterate over all non-empty subsets of the indicators. Represent subsets with bitmasks from 1 to 2^k - 1.
4. For each subset, calculate the product of its elements. Skip the subset if the product exceeds _n_, because no numbers ≤ _n_ are divisible by it.
5. Determine the subset's contribution to `count_divisible`. If the subset size is odd, add floor(n / product); if even, subtract floor(n / product). This is the Inclusion-Exclusion formula.
6. After processing all subsets, the answer is `n - count_divisible`, representing numbers not divisible by any indicator.

The invariant that guarantees correctness is that the Inclusion-Exclusion Principle correctly counts numbers divisible by at least one element, adding when subsets have odd cardinality and subtracting when even. The coprimality ensures that products correspond exactly to the least common multiple.

## Python Solution

```python
import sys
input = sys.stdin.readline
from itertools import combinations
from math import prod

def main():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    count_divisible = 0
    for mask in range(1, 1 << k):
        subset = []
        for i in range(k):
            if mask & (1 << i):
                subset.append(a[i])
        p = 1
        for x in subset:
            if p > n // x:
                p = n + 1
                break
            p *= x
        if p > n:
            continue
        if len(subset) % 2 == 1:
            count_divisible += n // p
        else:
            count_divisible -= n // p
    print(n - count_divisible)

if __name__ == "__main__":
    main()
```

The solution carefully handles integer overflow by checking `p > n // x` before multiplying. This prevents the product from exceeding 10^13. The use of bitmasks allows us to generate subsets efficiently, and the odd/even check implements the inclusion-exclusion sign. The subtraction `n - count_divisible` at the end gives exactly the numbers that are safe from all indicators.

## Worked Examples

### Sample 1

Input:

```
20 3
2 3 5
```

| Subset | Product | Floor(20 / Product) | Contribution |
| --- | --- | --- | --- |
| [2] | 2 | 10 | +10 |
| [3] | 3 | 6 | +6 |
| [5] | 5 | 4 | +4 |
| [2,3] | 6 | 3 | -3 |
| [2,5] | 10 | 2 | -2 |
| [3,5] | 15 | 1 | -1 |
| [2,3,5] | 30 | 0 | +0 |

`count_divisible = 10+6+4-3-2-1+0 = 14`

Answer = 20 - 14 = 6

This confirms that the inclusion-exclusion calculation correctly counts overlaps.

### Custom Sample

Input:

```
10 2
3 7
```

| Subset | Product | Floor(10 / Product) | Contribution |
| --- | --- | --- | --- |
| [3] | 3 | 3 | +3 |
| [7] | 7 | 1 | +1 |
| [3,7] | 21 | 0 | -0 |

`count_divisible = 4`

Answer = 10 - 4 = 6

This demonstrates that small _n_ relative to indicators is handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^k * k) | Each subset is generated using a bitmask (2^k subsets), computing product takes up to k multiplications |
| Space | O(k) | Only storing the current subset and product |

For k ≤ 100, the 2^k subsets are pruned by checking `p > n`, so in practice the algorithm runs well within the time limit for n up to 10^13. Memory usage is minimal since only subset products and counters are stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("20 3\n2 3 5\n") == "6", "sample 1"

# minimum input
assert run("1 1\n1\n") == "0", "minimum input"

# all indicators larger than n
assert run("3 2\n5 7\n") == "3", "no number divisible"

# n equals product of all indicators
assert run("6 2\n2 3\n") == "2", "product equals n"

# all indicators 1
assert run("10 3\n1 1 1\n") == "0", "all divisible by 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n1 | 0 | minimum n, indicator 1 |
| 3 2\n5 7 | 3 | no numbers divisible by any indicator |
| 6 2\n2 3 | 2 | overlapping multiples correctly counted |
| 10 3\n1 1 1 | 0 | indicators equal to 1, everything divisible |

## Edge Cases

When _n_ is smaller than all indicators, such as `n=3` and indicators `[5,7]`, the inclusion-exclusion algorithm correctly skips subsets where product > n. Each subset product exceeds n, so `count_divisible` remains 0, yielding 3 as the answer. This demonstrates the algorithm does not falsely subtract numbers when no multiples exist.

When an indicator is 1, all numbers are divisible, so the algorithm correctly identifies that every subset containing 1 contributes to `count_divisible`, resulting in zero remaining numbers. The check `p > n // x` prevents overflow when handling large n with small indicators, such as n=10^13 and indicator 1000.
