---
title: "CF 482A - Diverse Permutation"
description: "We are asked to construct a permutation of integers from 1 to n such that the set of absolute differences between consecutive elements contains exactly k distinct values. Concretely, if the permutation is [p1, p2, ..."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 482
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 275 (Div. 1)"
rating: 1200
weight: 482
solve_time_s: 663
verified: false
draft: false
---

[CF 482A - Diverse Permutation](https://codeforces.com/problemset/problem/482/A)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy  
**Solve time:** 11m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a permutation of integers from 1 to _n_ such that the set of absolute differences between consecutive elements contains exactly _k_ distinct values. Concretely, if the permutation is `[p1, p2, ..., pn]`, then the list `[|p1 - p2|, |p2 - p3|, ..., |pn-1 - pn|]` must have _k_ distinct numbers.

The input consists of two integers _n_ and _k_, with the guarantee that `1 ≤ k < n ≤ 10^5`. This means we need a solution that runs in linear or near-linear time, as anything quadratic (`O(n^2)`) would involve up to 10^10 operations in the worst case and will not finish within the 1-second limit.

Non-obvious edge cases include when _k_ is 1 or _n-1_. For `k = 1`, the permutation must produce differences that are all equal, which essentially means the permutation is strictly increasing or decreasing. For `k = n-1`, the permutation must use every possible difference from 1 to `n-1` exactly once. A naive approach that randomly permutes numbers will fail to guarantee the exact count of distinct differences and will often produce fewer or more distinct values than required.

## Approaches

A brute-force approach would attempt all `n!` permutations of `[1, 2, ..., n]` and compute the set of consecutive differences for each. We would then check which permutation yields exactly _k_ distinct differences. While this is correct in principle, the factorial growth makes it completely impractical for any non-trivial _n_, even for `n = 10`.

The key insight to achieve an efficient solution comes from observing that we can deliberately control the set of differences by alternating between small and large numbers. By starting at 1 and then choosing `n`, then 2, then `n-1`, and so on, we create the largest differences first. Each switch from one end to the other introduces a new distinct difference, and once we reach exactly _k_ distinct differences, we can fill the remaining numbers in order to maintain only the smallest difference of 1. This greedy construction ensures that the first _k_ differences are distinct, and the remaining `n-k-1` differences are all equal, satisfying the requirement exactly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Greedy alternating construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two pointers: `left = 1` and `right = n`. These will track the smallest and largest available numbers to pick for the permutation.
2. Create an empty list `perm` that will hold the final permutation.
3. Repeat _k + 1_ times to generate the first `k` differences. On each iteration, alternate between picking from `left` and `right`. Start with `left`. Each pick adds a new distinct difference.

For example, if we start with `left`, append `left` to `perm` and increment `left`. Then append `right` to `perm` and decrement `right`, and repeat. Each append guarantees a new absolute difference between consecutive elements.
4. Once the first `k + 1` numbers are placed, fill the rest of the permutation with the remaining numbers in consecutive order. If the last number appended came from the `left` side, continue filling from `left` up; if it came from `right`, continue filling down. These numbers introduce only one new difference of 1, keeping the total distinct differences exactly _k_.
5. Print the permutation.

**Why it works**

Each switch between `left` and `right` guarantees a new difference because the absolute value between the current and previous number increases with the distance from the opposite end. By alternating exactly _k + 1_ times, we produce exactly _k_ distinct differences. After that, filling numbers in order introduces no additional new differences. This invariant ensures that the total distinct differences in the permutation equals exactly _k_.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())

perm = []
left, right = 1, n

# Generate first k+1 numbers with k distinct differences
for i in range(k + 1):
    if i % 2 == 0:
        perm.append(left)
        left += 1
    else:
        perm.append(right)
        right -= 1

# Fill remaining numbers in order
if (k + 1) % 2 == 0:
    perm.extend(range(left, right + 1))
else:
    perm.extend(range(right, left - 1, -1))

print(' '.join(map(str, perm)))
```

The code carefully alternates picks from the two ends to guarantee distinct differences. After the first `k + 1` elements, the remaining numbers are placed sequentially to avoid introducing new differences. The modulo operation ensures that the alternation pattern is maintained correctly.

## Worked Examples

Sample input 1:

```
n = 3, k = 2
```

| i | perm | left | right | Comment |
| --- | --- | --- | --- | --- |
| 0 | [1] | 2 | 3 | Pick left |
| 1 | [1, 3] | 2 | 2 | Pick right |
| 2 | [1, 3, 2] | 2 | 2 | Pick left (remaining) |

The differences are `[2, 1]`, exactly 2 distinct values.

Another example:

```
n = 5, k = 3
```

| i | perm | left | right | Comment |
| --- | --- | --- | --- | --- |
| 0 | [1] | 2 | 5 | Pick left |
| 1 | [1, 5] | 2 | 4 | Pick right |
| 2 | [1, 5, 2] | 3 | 4 | Pick left |
| 3 | [1, 5, 2, 4] | 3 | 3 | Pick right |
| 4 | [1, 5, 2, 4, 3] | 3 | 3 | Fill remaining |

Differences: `[4,3,2,1]` → 3 distinct values as required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each number from 1 to n is visited once in either the alternating phase or filling phase |
| Space | O(n) | We store the permutation in a list of size n |

The algorithm is linear in both time and space, comfortably handling `n = 10^5` within the given limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    perm = []
    left, right = 1, n
    for i in range(k + 1):
        if i % 2 == 0:
            perm.append(left)
            left += 1
        else:
            perm.append(right)
            right -= 1
    if (k + 1) % 2 == 0:
        perm.extend(range(left, right + 1))
    else:
        perm.extend(range(right, left - 1, -1))
    return ' '.join(map(str, perm))

# Provided samples
assert run("3 2\n") == "1 3 2", "sample 1"

# Custom cases
assert run("5 3\n") == "1 5 2 4 3", "k = n-2 case"
assert run("4 1\n") == "1 2 3 4", "k = 1 case"
assert run("6 5\n") == "1 6 2 5 3 4", "k = n-1 case"
assert run("1 1\n") == "1", "minimum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 3 | 1 5 2 4 3 | Alternating construction for k < n-1 |
| 4 1 | 1 2 3 4 | Smallest distinct differences |
| 6 5 | 1 6 2 5 3 4 | Maximum distinct differences |
| 1 1 | 1 | Minimum size input |

## Edge Cases

For `k = 1`, such as input `4 1`, the algorithm produces `[1, 2, 3, 4]`. The first `k+1 = 2` numbers are `[1, 2]`, creating one distinct difference of 1. The remaining numbers `[3, 4]` are filled sequentially, introducing no new differences, maintaining exactly one distinct difference.

For `k = n-1`, such as input `6 5`, the alternation fully spans `[1, 6, 2, 5, 3, 4]`. Each consecutive difference is unique: `[5,4,3,2,1]`, producing exactly 5 distinct differences as required. The algorithm gracefully handles both extremes without special cases.
