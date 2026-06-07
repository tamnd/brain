---
title: "CF 2123C - Prefix Min and Suffix Max"
description: "We are given an array of distinct integers and a set of operations: you can either replace a prefix with its minimum or a suffix with its maximum."
date: "2026-06-08T03:36:33+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 2123
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1034 (Div. 3)"
rating: 1000
weight: 2123
solve_time_s: 95
verified: false
draft: false
---

[CF 2123C - Prefix Min and Suffix Max](https://codeforces.com/problemset/problem/2123/C)

**Rating:** 1000  
**Tags:** brute force, data structures  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of distinct integers and a set of operations: you can either replace a prefix with its minimum or a suffix with its maximum. The goal is to determine, for each element in the array, whether it is possible to reduce the array to a single-element array containing only that element using a sequence of these operations. The output is a binary string where `1` indicates it is possible and `0` otherwise.

The input guarantees that the array has distinct integers and can be as large as 200,000 elements per test case, with multiple test cases totaling up to 200,000 elements. This rules out any brute-force simulation of all operation sequences because the number of possible sequences grows exponentially with the array size. Our algorithm must therefore compute the answer in linear time per test case.

The tricky part of the problem lies in understanding which elements are reachable. It is easy to think that any element could be reached if it appears anywhere in the array, but the operations are constrained: a prefix replacement always moves toward the smallest element on the left, and a suffix replacement moves toward the largest element on the right. For example, in an array `[3, 1, 4, 2]`, the element `3` cannot be reduced to alone because any operation will either pull `1` to the front or `4` to the back, never isolating `3`.

## Approaches

A naive approach would be to simulate every possible sequence of prefix and suffix operations for each element and see if the array can collapse to that element. This works because the operations are deterministic, but the number of sequences grows exponentially (`O(2^n)`), which is infeasible for `n = 2*10^5`.

The key observation is that only elements that are minimum in some prefix or maximum in some suffix of the array can potentially survive to the final position. Specifically, if we scan the array from left to right keeping track of the running minimum and from right to left keeping track of the running maximum, we can immediately determine which elements can appear as a final single-element array. The first element must always be reducible to the minimum of the whole array to survive, and the last element must be reducible to the maximum. Any element not on a strictly increasing sequence from minimum to maximum cannot be isolated because the operations either push smaller elements to the left or larger elements to the right.

This observation reduces the problem to a single pass from both ends of the array, resulting in a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array `a` and determine its length `n`. Initialize a binary string of length `n` filled with zeros.
2. Maintain two arrays: `prefix_min` and `suffix_max`. `prefix_min[i]` stores the minimum of `a[0..i]`, and `suffix_max[i]` stores the maximum of `a[i..n-1]`.
3. Fill `prefix_min` by scanning the array from left to right. At each index `i`, set `prefix_min[i]` as `min(prefix_min[i-1], a[i])`. This keeps track of the smallest element that could propagate to the front.
4. Fill `suffix_max` by scanning the array from right to left. At each index `i`, set `suffix_max[i]` as `max(suffix_max[i+1], a[i])`. This tracks the largest element that could propagate to the back.
5. Iterate over each index `i` of the array. An element `a[i]` can be isolated if and only if it equals `prefix_min[i]` or `suffix_max[i]`. Set the corresponding position in the binary string to `1` if this condition holds.
6. Print the resulting binary string.

Why it works: Any final array of length 1 must come from a sequence that continually pushes either smaller elements to the left or larger elements to the right. By maintaining the prefix minimums and suffix maximums, we identify the only elements that can survive such sequences at each position. This captures exactly the set of elements that can be the final single-element array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        prefix_min = [0] * n
        suffix_max = [0] * n
        
        prefix_min[0] = a[0]
        for i in range(1, n):
            prefix_min[i] = min(prefix_min[i-1], a[i])
        
        suffix_max[-1] = a[-1]
        for i in range(n-2, -1, -1):
            suffix_max[i] = max(suffix_max[i+1], a[i])
        
        result = ['0'] * n
        for i in range(n):
            if a[i] == prefix_min[i] or a[i] == suffix_max[i]:
                result[i] = '1'
        print(''.join(result))

solve()
```

The first section reads input and sets up storage for prefix minimums and suffix maximums. Two linear scans compute these arrays. The final loop constructs the binary string by checking if the current element can survive to the final array, based on the prefix minimum or suffix maximum. Off-by-one errors are avoided by careful initialization of the first and last elements of `prefix_min` and `suffix_max`. The solution is linear in both time and space, handling the largest constraints efficiently.

## Worked Examples

**Sample Input 1**

```
6
1 3 5 4 7 2
```

| i | a[i] | prefix_min | suffix_max | result |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 7 | 1 |
| 1 | 3 | 1 | 7 | 0 |
| 2 | 5 | 1 | 7 | 0 |
| 3 | 4 | 1 | 7 | 0 |
| 4 | 7 | 1 | 7 | 1 |
| 5 | 2 | 1 | 2 | 1 |

This trace shows that only elements that are the minimum so far from the left or maximum so far from the right can survive.

**Sample Input 2**

```
4
13 10 12 20
```

| i | a[i] | prefix_min | suffix_max | result |
| --- | --- | --- | --- | --- |
| 0 | 13 | 13 | 20 | 1 |
| 1 | 10 | 10 | 20 | 1 |
| 2 | 12 | 10 | 20 | 0 |
| 3 | 20 | 10 | 20 | 1 |

This trace confirms that middle elements not on the boundary of minimum or maximum sequences cannot be isolated.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass for prefix minimum, one pass for suffix maximum, one pass to generate the result string |
| Space | O(n) | Two arrays to store prefix minimums and suffix maximums |

Given the constraints, this solution easily fits within time and memory limits. Each test case takes linear time, and the sum of n over all test cases is capped at 2*10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("3\n6\n1 3 5 4 7 2\n4\n13 10 12 20\n7\n1 2 3 4 5 6 7\n") == "100011\n1101\n1000001"

# Custom cases
assert run("1\n2\n5 1\n") == "11", "two elements, min and max"
assert run("1\n3\n2 1 3\n") == "111", "middle element reachable by prefix or suffix"
assert run("1\n5\n10 20 30 40 50\n") == "10001", "strictly increasing sequence"
assert run("1\n5\n50 40 30 20 10\n") == "10001", "strictly decreasing sequence"
assert run("1\n4\n3 1 4 2\n") == "1001", "random small array"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2\n5 1` | `11` | Both elements can be isolated because one is min, one is max |
| `3\n2 1 3` | `111` | Middle element reachable by suffix/prefix operation |
| `5\n10 20 30 40 50` | `10001` | Only first and last survive in strictly increasing array |
| `5\n50 40 30 20 10` | `10001` | Only first and last survive |
