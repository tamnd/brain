---
title: "CF 1506D - Epic Transformation"
description: "We are given an array of integers, and we are allowed to repeatedly remove pairs of elements that are different from each other. Our task is to determine the smallest size the array can have after applying this operation any number of times."
date: "2026-06-10T20:18:40+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1506
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 710 (Div. 3)"
rating: 1400
weight: 1506
solve_time_s: 141
verified: true
draft: false
---

[CF 1506D - Epic Transformation](https://codeforces.com/problemset/problem/1506/D)

**Rating:** 1400  
**Tags:** constructive algorithms, data structures, greedy  
**Solve time:** 2m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we are allowed to repeatedly remove pairs of elements that are different from each other. Our task is to determine the smallest size the array can have after applying this operation any number of times. The input consists of multiple test cases, each with its own array. The output is simply the minimal possible length for each array after optimal pair removals.

Looking at the constraints, the array can be as large as 2×10^5 elements in a single test case, and the total across all test cases is capped at 2×10^5. This immediately rules out any solution that tries to simulate every possible pair removal explicitly, because that could involve O(n^2) operations in the worst case. We need a linear or near-linear approach per test case. Each element value can be very large, up to 10^9, so any solution that relies on creating a frequency array indexed by the value itself is infeasible. We need to work with counts, not value ranges.

Edge cases that require careful attention include arrays where all elements are equal. For example, `[1, 1, 1]` cannot have any pair removed, so the result is 3. Another tricky scenario is when the counts of the most frequent number dominate the array. For instance, `[1, 1, 1, 2, 3]` allows only two pairs to be removed (`1-2` and `1-3`), leaving one `1` behind. A naive approach that removes pairs arbitrarily could produce a suboptimal final size if it doesn't consider the distribution of counts.

## Approaches

The brute-force approach is to simulate removing any two different numbers repeatedly. You would pick pairs, remove them, and repeat until no more pairs are possible. This is guaranteed to produce a correct answer if implemented carefully, but the worst-case complexity is O(n^2), which is too slow for n = 2×10^5.

The key insight is that we only need to know the frequency of each number. Suppose the most frequent number occurs `max_count` times, and the rest of the elements total `rest_count = n - max_count`. If `rest_count` is greater than or equal to `max_count`, then we can pair every occurrence of the most frequent number with some different element and reduce the array to either 0 or 1 element depending on parity. If `rest_count` is less than `max_count`, then even after pairing every other element with the most frequent element, there will be `max_count - rest_count` elements left, which cannot be removed. Therefore, the minimal array size is `max(1, max_count - rest_count)` if `max_count > rest_count` and `n % 2` otherwise.

This observation allows us to solve each test case in O(n) time using a frequency map.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Frequency Analysis | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read the array length `n` and the array `a`.
3. Count the occurrences of each number in the array. This can be done using a dictionary or `collections.Counter`.
4. Identify the largest frequency `max_count`.
5. Compute the sum of all other frequencies `rest_count = n - max_count`.
6. If `max_count` is greater than `rest_count`, the minimal array size is `max_count - rest_count` because these elements cannot be paired with anything different.
7. If `max_count` is less than or equal to `rest_count`, then we can remove pairs optimally until 0 or 1 element remains, so the minimal size is `n % 2`.
8. Print the minimal size for each test case.

The invariant here is that the maximal frequency element determines the lower bound on the remaining elements. If other elements suffice to pair with it, they can all be removed. Otherwise, the excess remains.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    freq = Counter(a)
    max_count = max(freq.values())
    rest_count = n - max_count
    if max_count > rest_count:
        print(max_count - rest_count)
    else:
        print(n % 2)
```

The code first reads all inputs efficiently. `Counter` builds the frequency map, which allows us to quickly determine the most common element. `max_count` and `rest_count` capture the two critical quantities needed for deciding the minimal array size. We then apply the reasoning from the algorithm directly: if the most frequent element dominates, we output the excess; otherwise, we output parity of the array size after maximal pairing.

## Worked Examples

### Sample Input 1

```
6
1 6 1 1 4 4
```

| Variable | Value |
| --- | --- |
| freq | {1:3, 6:1, 4:2} |
| max_count | 3 |
| rest_count | 3 |
| output | n % 2 = 6 % 2 = 0 |

Explanation: We can pair `1-6`, `1-4`, `1-4` to remove all elements. The minimal array size is 0.

### Sample Input 2

```
5
4 5 4 5 4
```

| Variable | Value |
| --- | --- |
| freq | {4:3, 5:2} |
| max_count | 3 |
| rest_count | 2 |
| output | max_count - rest_count = 3 - 2 = 1 |

Explanation: Only two pairs can be removed: `4-5` and `4-5`, leaving one `4` behind. Minimal array size is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Counting frequencies is linear, finding max in a small dictionary is linear in unique elements, total ≤ n. |
| Space | O(n) | We store the array and frequency map; the frequency map has at most n keys. |

With n ≤ 2×10^5 in total across all test cases, this fits well within 2-second time limit and 256 MB memory.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        freq = Counter(a)
        max_count = max(freq.values())
        rest_count = n - max_count
        if max_count > rest_count:
            output.append(str(max_count - rest_count))
        else:
            output.append(str(n % 2))
    return "\n".join(output)

# provided samples
assert run("5\n6\n1 6 1 1 4 4\n2\n1 2\n2\n1 1\n5\n4 5 4 5 4\n6\n2 3 2 1 3 1\n") == "0\n0\n2\n1\n0"

# custom cases
assert run("1\n1\n42\n") == "1"  # single element
assert run("1\n4\n7 7 7 7\n") == "4"  # all equal
assert run("1\n5\n1 2 3 4 5\n") == "1"  # all unique odd
assert run("1\n6\n1 1 2 2 3 3\n") == "0"  # all paired perfectly
assert run("1\n7\n1 1 1 2 2 2 3\n") == "1"  # one excess
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n42` | 1 | Single element cannot be paired |
| `1\n4\n7 7 7 7` | 4 | All elements identical |
| `1\n5\n1 2 3 4 5` | 1 | All unique odd number of elements |
| `1\n6\n1 1 2 2 3 3` | 0 | All elements can be paired exactly |
| `1\n7\n1 1 1 2 2 2 3` | 1 | Excess element remains after maximal pairing |

## Edge Cases

For arrays with all equal elements, the algorithm computes `max_count = n`, `rest_count = 0`, and outputs `max_count - rest_count = n`. For example, `[7, 7, 7, 7]` correctly outputs 4. For arrays with exactly two different elements appearing in equal number, like `[1, 1, 2, 2]`, `max_count = 2`, `rest_count = 2`, output is `n % 2 = 4 % 2 = 0`, confirming that all can be removed. The solution correctly handles single-element arrays, arrays with one dominant number, and arrays with perfect pairing opportunities.
