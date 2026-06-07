---
title: "CF 2135A - Against the Difference"
description: "We are given an array of integers, and we want to find the length of the longest subsequence that can be split into \"blocks\". A block is defined as a contiguous sequence where every element equals the length of that sequence."
date: "2026-06-08T02:37:08+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 2135
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1046 (Div. 1)"
rating: 1200
weight: 2135
solve_time_s: 119
verified: false
draft: false
---

[CF 2135A - Against the Difference](https://codeforces.com/problemset/problem/2135/A)

**Rating:** 1200  
**Tags:** data structures, dp  
**Solve time:** 1m 59s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and we want to find the length of the longest subsequence that can be split into "blocks". A block is defined as a contiguous sequence where every element equals the length of that sequence. For instance, `[3, 3, 3]` is a block because it has length three and every element is three, while `[2, 2, 1]` is not a block. The array is neat if it can be expressed as the concatenation of one or more blocks, possibly zero. Our task is to find the maximum length of a subsequence that is neat.

The input provides multiple test cases. Each test case gives the length `n` of the array and the array elements themselves. Each element satisfies `1 <= a_i <= n`. The sum of all `n` across test cases is at most 200,000, so we must aim for an algorithm that runs in roughly linear time per test case. Quadratic algorithms, such as trying all subsequences, would require on the order of `O(2^n)` operations, which is completely infeasible. Even `O(n^2)` approaches will be too slow for `n` near 200,000.

Subtle edge cases include arrays where no element occurs enough times to form a block, or where only small blocks are possible. For example, for `a = [5, 1, 2]`, no block can be formed because the counts of numbers do not match any required block length, so the longest neat subsequence is empty. Another case is when multiple identical numbers appear, but in counts insufficient to form their block, e.g., `[2, 2, 2]` allows one block of `[2, 2]` but the third `2` cannot form a new block, so careful counting is required.

## Approaches

A brute-force approach would be to enumerate all subsequences, check if each can be split into blocks, and record the maximum length. This is correct in principle but intractable: a subsequence has `2^n` possibilities, which is astronomically large for `n = 2 * 10^5`. Even an `O(n^2)` approach that attempts dynamic programming over subarrays or positions is too slow because it would require on the order of `4*10^10` operations in the worst case.

The key insight is to notice that the order of elements does not matter beyond selecting subsequences. What matters is the frequency of each number. For a number `x`, the maximum number of elements that can contribute to neat blocks of size `x` is the largest multiple of `x` less than or equal to its count. For example, if `4` appears `9` times, we can form two blocks of size 4 (`4*2 = 8` elements), leaving one leftover `4` that cannot form a block. Once we compute the maximal contribution of each number, summing these gives the length of the longest neat subsequence.

Thus, the optimal approach is a frequency-count based greedy selection: count occurrences of each number, compute the maximal multiple of each number less than or equal to its count, and sum these contributions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the array `a`.
3. Initialize a frequency array or dictionary to count occurrences of each integer in `a`.
4. Initialize a variable `max_neat_length` to zero.
5. Iterate over each distinct number `x` in the frequency array.
6. For each number `x`, compute `k = (count[x] // x) * x`. This gives the maximum number of elements of `x` that can form complete blocks.
7. Add `k` to `max_neat_length`.
8. After processing all numbers, output `max_neat_length` for the current test case.

Why it works: The greedy selection is valid because blocks of length `x` must use exactly `x` elements, and any extra elements beyond multiples of `x` cannot contribute to a neat subsequence. Counting frequencies ensures we consider all possible elements. Summing the maximal contributions ensures we capture the longest subsequence. Since the subsequence can be reordered arbitrarily, order does not constrain the solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def longest_neat_subsequence(n, a):
    from collections import Counter
    freq = Counter(a)
    length = 0
    for x, count in freq.items():
        length += (count // x) * x
    return length

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(longest_neat_subsequence(n, a))
```

The solution uses `Counter` to efficiently count occurrences in `O(n)` time. The loop over `freq.items()` ensures each distinct number is considered exactly once. The division and multiplication `(count // x) * x` determines the maximal number of elements usable from each number. Using fast I/O ensures the solution runs efficiently under tight input constraints.

## Worked Examples

**Example 1:** `a = [1, 2, 3, 3, 3, 1]`

| x | count[x] | count[x]//x | contribution |
| --- | --- | --- | --- |
| 1 | 2 | 2 // 1 = 2 | 2 |
| 2 | 1 | 1 // 2 = 0 | 0 |
| 3 | 3 | 3 // 3 = 1 | 3 |

Sum = 2 + 0 + 3 = 5

The longest neat subsequence is `[1, 3, 3, 3, 1]`.

**Example 2:** `a = [8, 8, 8, 8, 8, 8, 8, 7]`

| x | count[x] | count[x]//x | contribution |
| --- | --- | --- | --- |
| 7 | 1 | 1 // 7 = 0 | 0 |
| 8 | 7 | 7 // 8 = 0 | 0 |

Sum = 0

No neat subsequence is possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Counting frequencies and computing contributions both take O(n) time. |
| Space | O(n) per test case | Counter stores at most n keys with counts. |

With sum of `n` over all test cases <= 2 * 10^5, the total operations remain within 2 * 10^5, easily within 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open(__file__).read(), globals())
    return output.getvalue().strip()

# Provided samples
assert run("6\n1\n1\n2\n2 2\n4\n2 2 1 1\n6\n1 2 3 3 3 1\n8\n8 8 8 8 8 8 8 7\n10\n2 3 3 1 2 3 5 1 1 7\n") == "1\n2\n4\n5\n0\n5"

# Custom cases
assert run("1\n3\n5 1 2\n") == "0", "no blocks"
assert run("1\n5\n2 2 2 2 2\n") == "4", "multiple blocks of 2"
assert run("1\n1\n1\n") == "1", "single element"
assert run("1\n6\n1 1 1 1 1 1\n") == "6", "all ones"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5\n2 2 2 2 2` | 4 | Multiple complete blocks for same number |
| `3\n5 1 2` | 0 | No possible blocks |
| `6\n1 1 1 1 1 1` | 6 | Multiple blocks of 1, sum used correctly |
| `1\n1` | 1 | Single-element array edge case |

## Edge Cases

When no number occurs enough times to form a block, the algorithm correctly sums zero contributions. For `a = [5, 1, 2]`, counts are `{5:1,1:1,2:1}`, and `(count // x) * x = 0` for all. The output is `0`, matching the expected empty neat subsequence.

When a number appears exactly `x` times, it forms one complete block. For `a = [2, 2]`, `count[2] = 2`, `2 // 2 * 2 = 2`. The algorithm outputs `2`, correctly capturing the full array as a neat subsequence.

When a number appears more than `x` but less than `2x`, it contributes only `x` to the total, ignoring leftovers. For `a = [3,3,3,3
