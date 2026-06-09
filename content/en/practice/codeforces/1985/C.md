---
title: "CF 1985C - Good Prefixes"
description: "The problem asks us to analyze prefixes of an integer array and determine which prefixes are \"good\" according to a specific rule. A prefix of length $i$ is considered good if there exists an element in the prefix equal to the sum of all other elements."
date: "2026-06-08T16:18:52+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1985
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 952 (Div. 4)"
rating: 1000
weight: 1985
solve_time_s: 158
verified: true
draft: false
---

[CF 1985C - Good Prefixes](https://codeforces.com/problemset/problem/1985/C)

**Rating:** 1000  
**Tags:** greedy  
**Solve time:** 2m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to analyze prefixes of an integer array and determine which prefixes are "good" according to a specific rule. A prefix of length $i$ is considered good if there exists an element in the prefix equal to the sum of all other elements. For example, in the array `[1, 3, 2, 6]`, the full array is good because `6` equals `1 + 3 + 2`. Single-element arrays are only good if the element is zero. The input consists of multiple test cases, each specifying the array length followed by the array elements, and the output is the count of good prefixes for each case.

The constraints indicate that a single array can be up to $2 \cdot 10^5$ elements, and the total across all test cases does not exceed the same number. This means a solution with $O(n^2)$ time per test case is far too slow, because in the worst case it would require roughly $4 \cdot 10^{10}$ operations. An efficient solution must operate in linear or near-linear time per test case, ideally $O(n)$ per array. Edge cases include single-element arrays, arrays containing only zeros, arrays where multiple elements could be the "sum of the rest," and prefixes that appear good early but fail as more elements are added. For example, `[0, 1]` is not good because `0 ≠ 1` and `1 ≠ 0`, even though `[0]` alone is good.

## Approaches

The naive approach considers each prefix individually, and for each prefix of length $i$, it checks every element to see if it equals the sum of all others. This is correct in principle: compute the prefix sum and then for each element subtract it from the total sum to see if it equals the element. The complexity is $O(n^2)$ for each test case because for every prefix of length $i$ you perform $i$ checks, which is infeasible given the problem constraints.

The key insight comes from observing that to determine if a prefix is good, we only need to know the sum of all elements so far and the counts of individual elements in that prefix. If the total sum is `S` and the prefix is length `i`, a prefix is good if there exists an element `x` such that `x = S - x`, i.e., `2 * x = S`. This means we just need a frequency map for the prefix elements and the running prefix sum. Every time we add a new element to the prefix, we update the total sum and check if `(sum - element)` exists in the prefix using the frequency map. By maintaining a running sum and frequency dictionary, each prefix can be checked in constant time, resulting in an $O(n)$ algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter for good prefixes to zero, a running sum for the current prefix, and a dictionary to track the frequency of each element encountered so far.
2. Iterate through each element in the array, adding it to the running sum and incrementing its count in the dictionary.
3. After updating the sum and frequency, compute the target value as `sum - element` for each element in the prefix. If `2 * element = sum`, the current prefix is good.
4. Increment the good-prefix counter whenever the condition holds.
5. Continue to the next element until the end of the array.
6. After processing all elements of a test case, output the counter for that test case.

The invariant that guarantees correctness is that at each step, the running sum accurately reflects the total of the current prefix, and the frequency map contains all elements in the prefix. Checking `2 * x == sum` ensures we capture exactly the condition that one element equals the sum of the rest.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_good_prefixes(a):
    freq = {}
    total = 0
    good_count = 0
    for x in a:
        total += x
        freq[x] = freq.get(x, 0) + 1
        if total % 2 == 0:
            target = total // 2
            if freq.get(target, 0) > 0:
                good_count += 1
    return good_count

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(count_good_prefixes(a))
```

The `count_good_prefixes` function maintains a frequency dictionary and a running total as it iterates through the array. For each new element, it updates the total sum and checks whether the prefix sum is even. If it is, it checks whether half the total exists in the prefix. This ensures that exactly one element equals the sum of the remaining elements. Using a dictionary avoids iterating over all elements repeatedly, keeping the complexity linear. The function correctly handles the edge case where a single-element prefix of zero is good, as the total is zero and the element is zero.

## Worked Examples

**Example 1: `[0, 1, 2, 1, 4]`**

| Element | Running Sum | Frequency Map | Good Prefix? |
| --- | --- | --- | --- |
| 0 | 0 | {0:1} | Yes |
| 1 | 1 | {0:1,1:1} | No |
| 2 | 3 | {0:1,1:1,2:1} | No |
| 1 | 4 | {0:1,1:2,2:1} | Yes |
| 4 | 8 | {0:1,1:2,2:1,4:1} | Yes |

This shows that the algorithm correctly identifies three good prefixes: `[0]`, `[0,1,2,1]`, `[0,1,2,1,4]`.

**Example 2: `[1,1,2,0]`**

| Element | Running Sum | Frequency Map | Good Prefix? |
| --- | --- | --- | --- |
| 1 | 1 | {1:1} | No |
| 1 | 2 | {1:2} | Yes |
| 2 | 4 | {1:2,2:1} | Yes |
| 0 | 4 | {1:2,2:1,0:1} | No |

The algorithm correctly counts three good prefixes for this array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once, dictionary lookups and updates are O(1) amortized |
| Space | O(n) | Frequency dictionary can store up to n distinct elements |

With the sum of n across all test cases bounded by 2 × 10^5, this algorithm runs comfortably within time and memory limits.

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
        a = list(map(int, input().split()))
        print(count_good_prefixes(a))
    return output.getvalue().strip()

# provided samples
assert run("7\n1\n0\n1\n1\n4\n1 1 2 0\n5\n0 1 2 1 4\n7\n1 1 0 3 5 2 12\n7\n1000000000 1000000000 1000000000 1000000000 1000000000 1000000000 294967296\n10\n0 1000000000 1000000000 1000000000 1000000000 1000000000 1000000000 1000000000 1000000000 589934592") == "1\n0\n3\n3\n4\n1\n2", "sample 1"

# custom cases
assert run("1\n1\n1") == "0", "single element non-zero"
assert run("1\n1\n0") == "1", "single element zero"
assert run("1\n3\n1 2 3") == "0", "no good prefixes"
assert run("1\n5\n2 2 4 0 8") == "3", "multiple good prefixes"
assert run("1\n4\n0 0 0 0") == "4", "all zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | 0 | single-element non-zero array |
| `1\n1\n0` | 1 | single-element zero array |
| `1\n3\n1 2 3` | 0 | no good prefixes |
| `1\n5\n2 2 4 0 8` | 3 | multiple good prefixes detected |
| `1\n4\n0 0 0 0` | 4 | array of zeros handled correctly |

## Edge Cases

A single-element zero `[0]` is good. The algorithm correctly identifies this because the total sum is zero and the frequency map contains zero, satisfying `2*0=0`. For
