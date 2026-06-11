---
title: "CF 1364A - XXXXX"
description: "We are given an array of integers and a number $x$ that Ehab dislikes. The goal is to find the length of the longest contiguous subarray whose sum is not divisible by $x$. Each test case gives a new array and a new $x$."
date: "2026-06-11T12:23:36+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "number-theory", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1364
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 649 (Div. 2)"
rating: 1200
weight: 1364
solve_time_s: 114
verified: true
draft: false
---

[CF 1364A - XXXXX](https://codeforces.com/problemset/problem/1364/A)

**Rating:** 1200  
**Tags:** brute force, data structures, number theory, two pointers  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a number $x$ that Ehab dislikes. The goal is to find the length of the longest contiguous subarray whose sum is not divisible by $x$. Each test case gives a new array and a new $x$. If no subarray satisfies the condition, the output should be $-1$.

The input arrays can be up to $10^5$ elements long, and values in the array and $x$ can go up to $10^4$. With up to 5 test cases per run, this means our solution must be at worst linear in $n$ per test case, because a naive quadratic approach examining all subarrays would involve roughly $5 \times 10^5 \times 10^5 / 2$ operations in the worst case, which is too slow for a 1-second time limit.

Subtle edge cases include arrays where all elements are multiples of $x$. For example, for $a = [2, 4, 6]$ and $x = 2$, any subarray sum is divisible by 2, so the output should be $-1$. Another edge case is when the sum of the entire array is already not divisible by $x$; in that case, the longest subarray is the whole array. Arrays with zeros or a single element equal to $x$ can also behave differently and need careful handling to avoid off-by-one mistakes.

## Approaches

A brute-force approach would check all subarrays explicitly, compute their sums, and test divisibility by $x$. This works logically, but the number of subarrays is $O(n^2)$, and computing each sum takes $O(1)$ with prefix sums. The total operations are still $O(n^2)$, which is infeasible for $n = 10^5$.

The key insight is that the property of divisibility is global. If the sum of the entire array is not divisible by $x$, then the full array is already the answer. If the sum is divisible by $x$, then we must remove at least one element to break this divisibility. Because the subarray must remain contiguous, removing either a prefix or a suffix until the first element not divisible by $x$ is reached gives the longest possible subarray. We do not need to check all subarrays; we only need the first and last elements that are not divisible by $x$. This observation reduces the solution from quadratic to linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$ and $x$ and then read the array $a$.
2. Compute the total sum of the array. If this sum is not divisible by $x$, immediately return $n$, the full length of the array.
3. If the total sum is divisible by $x$, scan the array from the left to find the first element whose value is not divisible by $x$. Store its index as `left`.
4. Scan the array from the right to find the first element whose value is not divisible by $x$. Store its index as `right`.
5. If no such element exists, all elements are divisible by $x$ and no subarray can have a sum not divisible by $x$; return $-1$.
6. Otherwise, compute two candidate subarray lengths: removing the prefix up to `left` yields `n - left - 1`, and removing the suffix after `right` yields `right`. The answer is the maximum of these two lengths.

The invariant here is that removing elements from one end of an array with sum divisible by $x$ until reaching a non-divisible element guarantees that the remaining subarray has a sum not divisible by $x$. This is the longest possible because removing more elements would only shorten the subarray unnecessarily.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    
    total = sum(a)
    if total % x != 0:
        print(n)
        continue
    
    left = 0
    while left < n and a[left] % x == 0:
        left += 1
    right = n - 1
    while right >= 0 and a[right] % x == 0:
        right -= 1
    
    if left == n:  # all elements divisible by x
        print(-1)
    else:
        print(max(n - left - 1, right))
```

The implementation follows the algorithm directly. We handle the full-array case first. The left and right scans are simple linear passes that stop at the first non-divisible element. The max calculation considers both options for the longest subarray. Boundary conditions, such as all elements divisible by $x$, are handled explicitly with a separate check.

## Worked Examples

Trace Sample 1:

Input: `3 3` `1 2 3`

- Total sum = 6, divisible by 3.
- Scan left: first element 1 % 3 != 0 at index 0.
- Scan right: last element 3 % 3 == 0, second to last 2 % 3 != 0 at index 1.
- Candidate lengths: `n - left - 1 = 3 - 0 - 1 = 2`, `right = 1`. Maximum = 2.

Input: `3 4` `1 2 3`

- Total sum = 6, not divisible by 4.
- Answer = 3, the full array length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each array is scanned at most twice, once left-to-right and once right-to-left. |
| Space | O(1) | Only a few indices and the total sum are stored. |

For the given constraints, this guarantees completion well under 1 second even at maximum input sizes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution code inline
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        
        total = sum(a)
        if total % x != 0:
            print(n)
            continue
        
        left = 0
        while left < n and a[left] % x == 0:
            left += 1
        right = n - 1
        while right >= 0 and a[right] % x == 0:
            right -= 1
        
        if left == n:
            print(-1)
        else:
            print(max(n - left - 1, right))
    return output.getvalue().strip()

# provided samples
assert run("3\n3 3\n1 2 3\n3 4\n1 2 3\n2 2\n0 6\n") == "2\n3\n-1", "sample 1"

# custom cases
assert run("1\n1 1\n1\n") == "-1", "single element divisible by x"
assert run("1\n1 2\n1\n") == "1", "single element not divisible by x"
assert run("1\n5 2\n2 4 6 8 10\n") == "-1", "all even, x = 2"
assert run("1\n5 3\n3 3 3 3 1\n") == "5", "last element breaks divisibility"
assert run("1\n6 5\n5 5 5 5 5 1\n") == "6", "last element not divisible by x"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | -1 | Single element divisible by x |
| 1 2 1 | 1 | Single element not divisible by x |
| 5 2 2 4 6 8 10 | -1 | All elements divisible by x |
| 5 3 3 3 3 3 1 | 5 | Last element breaks divisibility |
| 6 5 5 5 5 5 5 1 | 6 | Last element not divisible by x |

## Edge Cases

When all elements are divisible by $x$, the algorithm correctly identifies this by the `left == n` check. For arrays with only one element not divisible by $x$, the algorithm calculates `n - left - 1` and `right` correctly, choosing the maximum contiguous subarray that satisfies the condition. For arrays where the sum is already not divisible, the algorithm avoids unnecessary scanning and returns the full array length.
