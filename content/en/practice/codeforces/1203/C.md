---
title: "CF 1203C - Common Divisors"
description: "We are asked to find the number of positive integers that evenly divide every number in a given array. The array can contain up to 400,000 elements, each of which can be as large as $10^{12}$. Conceptually, we are looking for the set of common divisors of all array elements."
date: "2026-06-11T23:42:03+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1203
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 579 (Div. 3)"
rating: 1300
weight: 1203
solve_time_s: 99
verified: true
draft: false
---

[CF 1203C - Common Divisors](https://codeforces.com/problemset/problem/1203/C)

**Rating:** 1300  
**Tags:** implementation, math  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find the number of positive integers that evenly divide every number in a given array. The array can contain up to 400,000 elements, each of which can be as large as $10^{12}$. Conceptually, we are looking for the set of common divisors of all array elements.

The output is a single integer: the count of these divisors. For instance, in an array like `[2, 4, 6, 2, 10]`, the numbers `1` and `2` divide all elements, so the answer is `2`.

The constraints immediately inform our approach. Since `n` can be 4·10^5 and each number up to 10^12, we cannot afford to iterate over all numbers up to the maximum element and check divisibility. A naive solution would require iterating up to `10^12` for each array element, which is infeasible. We need an approach whose complexity depends on the number of divisors of a number rather than the number itself.

A subtle edge case arises when the array contains `1`. If any element is `1`, the only common divisor is `1`. Similarly, if all elements are the same, the answer is the number of divisors of that number. Arrays with large prime numbers also pose a challenge because their divisors are limited. Careless solutions might iterate over a range based on the array size rather than the greatest common divisor, producing incorrect or inefficient behavior.

## Approaches

The brute-force approach would attempt to check every integer from `1` up to the minimum element in the array, counting those that divide all elements. This is correct because any common divisor cannot exceed the smallest number. However, in the worst case, the smallest number can be up to $10^{12}$, and testing divisibility for each number is too slow. The operation count could be roughly $10^{12} \cdot n$, which will never fit in 2 seconds.

The key observation is that the set of common divisors of the array is exactly the set of divisors of the greatest common divisor (GCD) of all elements. This is because any number dividing the GCD automatically divides each element of the array, and conversely, any number that divides all array elements divides their GCD. Computing the GCD of all numbers can be done efficiently with the Euclidean algorithm, even for very large numbers. Once the GCD is known, we only need to count its divisors. Counting divisors up to $\sqrt{g}$ ensures that we consider all divisor pairs without iterating beyond the square root.

This observation reduces the problem from a potentially huge search space to something manageable, where the operations are roughly proportional to $n \log(\text{max element})$ for the GCD computation and $O(\sqrt{g})$ for counting divisors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * min(a)) | O(1) | Too slow |
| GCD + Divisor Count | O(n log max(a) + √g) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array from input and store the elements in a list. This is necessary to compute the GCD over all elements.
2. Initialize a variable `g` with the first element. This will store the running GCD.
3. Iterate through the remaining elements of the array. For each element `a[i]`, update `g` as the GCD of `g` and `a[i]` using the Euclidean algorithm. This step ensures that at the end of the loop, `g` is the GCD of the entire array.
4. Initialize a counter `count` to zero. This will track the number of divisors of `g`.
5. Iterate over all integers `d` from `1` to the integer square root of `g`. For each `d`, check if `g % d == 0`. If true, increment `count` by 1 because `d` is a divisor.
6. For each divisor `d` that is not equal to `g // d`, increment `count` by 1 to account for the paired divisor. This step ensures we do not double-count perfect squares.
7. Print the value of `count`, which is the number of positive integers that divide all elements of the array.

Why it works: The invariant here is that any divisor of the GCD divides all numbers in the array. Conversely, any number that divides all elements divides the GCD. By iterating up to the square root of `g` and counting each divisor pair, we ensure that every common divisor is counted exactly once.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

g = a[0]
for num in a[1:]:
    g = math.gcd(g, num)

count = 0
sqrt_g = int(g**0.5)
for d in range(1, sqrt_g + 1):
    if g % d == 0:
        count += 1
        if d != g // d:
            count += 1

print(count)
```

The code reads the input efficiently using `sys.stdin.readline` and computes the GCD using Python's built-in `math.gcd`. We loop through the divisors up to the square root to efficiently count all divisors without duplication. The check `d != g // d` ensures we handle perfect squares correctly.

## Worked Examples

### Sample 1

Input:

```
5
1 2 3 4 5
```

| Step | g | Divisor Count | Notes |
| --- | --- | --- | --- |
| Initial | 1 | 0 | Start with g = a[0] = 1 |
| GCD loop | 1 | 0 | gcd(1,2)=1, gcd(1,3)=1, gcd(1,4)=1, gcd(1,5)=1 |
| Divisor loop | 1 | 1 | Only divisor is 1 |

Output: `1`. Correct, since only 1 divides all numbers.

### Custom Example 2

Input:

```
4
2 4 6 8
```

| Step | g | Divisor Count | Notes |
| --- | --- | --- | --- |
| Initial | 2 | 0 | g = a[0] = 2 |
| GCD loop | 2 | 0 | gcd(2,4)=2, gcd(2,6)=2, gcd(2,8)=2 |
| Divisor loop | 2 | 2 | divisors are 1 and 2 |

Output: `2`. Correct, divisors of 2 divide all elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log max(a) + √g) | GCD computation is O(n log max(a)), counting divisors is O(√g) |
| Space | O(n) | Storing the array |

The algorithm easily fits within the constraints: n ≤ 4·10^5 and numbers up to 10^12. The divisor count loop is bounded by √(10^12) ≈ 10^6, which is acceptable within the time limit.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    g = a[0]
    for num in a[1:]:
        g = math.gcd(g, num)
    count = 0
    sqrt_g = int(g**0.5)
    for d in range(1, sqrt_g + 1):
        if g % d == 0:
            count += 1
            if d != g // d:
                count += 1
    return str(count)

# Provided sample
assert run("5\n1 2 3 4 5\n") == "1", "sample 1"

# All equal numbers
assert run("4\n6 6 6 6\n") == "4", "all equal"

# Single element
assert run("1\n10\n") == "4", "single element divisors"

# Large prime numbers
assert run("3\n17 34 51\n") == "2", "common divisors of 17,34,51"

# Perfect squares
assert run("3\n16 32 48\n") == "5", "divisors of 16"

# Mixed small and large numbers
assert run("5\n1 1000000000000 500000000000 250000000000 125000000000\n") == "1", "only 1 divides all"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 6 6 6 6 | 4 | Handling all equal elements |
| 1 10 | 4 | Single element case |
| 17 34 51 | 2 | GCD with prime numbers |
| 16 32 48 | 5 | Perfect square handling |
| 1 1000000000000 500000000000 250000000000 125000000000 | 1 | Large numbers with only 1 common divisor |

## Edge Cases

When the array contains `1` alongside larger numbers, like `[1, 2, 3,
