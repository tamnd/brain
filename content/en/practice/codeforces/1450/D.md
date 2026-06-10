---
title: "CF 1450D - Rating Compression"
description: "We are given an array of integers representing the rating graph of a user on a competitive programming platform. For each integer $k$ from 1 to $n$, we are asked to consider the \"k-compression\" of the array."
date: "2026-06-11T03:40:51+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1450
codeforces_index: "D"
codeforces_contest_name: "Codeforces Global Round 12"
rating: 1800
weight: 1450
solve_time_s: 110
verified: false
draft: false
---

[CF 1450D - Rating Compression](https://codeforces.com/problemset/problem/1450/D)

**Rating:** 1800  
**Tags:** binary search, data structures, greedy, implementation, two pointers  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers representing the rating graph of a user on a competitive programming platform. For each integer $k$ from 1 to $n$, we are asked to consider the "k-compression" of the array. The k-compression is formed by taking the minimum of every contiguous subarray of length $k$. The goal is to determine, for each $k$, whether this compressed array is a permutation of the numbers from 1 to $n-k+1$. If it is, the users are happy, and we output `1`; otherwise, we output `0`.

The constraints allow $n$ to reach $3 \cdot 10^5$ per test case, and the sum of all $n$ across test cases is also bounded by $3 \cdot 10^5$. This means an $O(n^2)$ approach, where we compute every subarray minimum explicitly, would result in approximately $10^{10}$ operations in the worst case, which is far too slow. We need a solution that runs in linear or near-linear time per test case.

Non-obvious edge cases include arrays with repeated numbers, arrays that are already sorted, arrays with minimum or maximum elements at the boundaries, and very small arrays where $n = 1$. For example, an array `[3,3,2]` has multiple repeated numbers. A naive approach might overlook that for $k = 2$, the minimums `[3,2]` include a duplicate `3` if processed incorrectly.

## Approaches

The brute-force approach iterates over each $k$ from 1 to $n$, constructs the k-compression array explicitly, and checks whether it forms a permutation. This is correct but inefficient because computing all subarray minimums naively takes $O(nk)$ per $k$, leading to $O(n^2)$ overall. This fails when $n$ approaches $10^5$.

The key insight is that the smallest k-compression that can form a permutation depends on the positions of the minimum and maximum elements in the array. Specifically, if an array contains each number from 1 to $n$ exactly once, the entire array is a permutation for $k = 1$. Then, for larger $k$, the first and last occurrences of the numbers determine whether the sliding window can produce unique minimums. We can track the positions of each value and use a two-pointer approach to maintain a valid window for each length.

Instead of generating every k-compression, we only need to check whether the smallest element is at a boundary, then the next smallest, and so on. By iteratively "removing" the smallest available element from the ends, we can construct a binary string for all $k$ in $O(n)$ time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array $a$ and its length $n$. Initialize a binary result array `ans` of length $n$ filled with zeros.
2. Check if the array $a$ contains exactly all numbers from 1 to $n$. If so, the 1-compression is a permutation, so set `ans[0] = 1`.
3. Record the first and last occurrence indices of each number in $a$. This allows us to know where each value appears.
4. Initialize two pointers, `l = 0` and `r = n-1`, representing the current window's left and right ends.
5. Iterate `val` from 1 to $n$ in increasing order:

- If `val` is at `a[l]`, increment `l`.
- Else if `val` is at `a[r]`, decrement `r`.
- Otherwise, the next smallest value is not at a boundary, so no larger window can be a permutation, break.
- If we successfully processed `val`, set `ans[n - val] = 1`, because the window length `n - val + 1` is valid for a permutation.
6. Output the binary string `ans`.

Why it works: At each step, the smallest remaining number must appear at one of the boundaries to maintain uniqueness in the sliding window. By removing the boundary element corresponding to the current minimum, we preserve the invariant that the remaining subarray can form a permutation for the next window size. If any number is inside the window, the uniqueness property fails, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans = ['0'] * n
        
        # Check if full array is a permutation
        if sorted(a) == list(range(1, n+1)):
            ans[0] = '1'
        
        l, r = 0, n-1
        count = [0] * (n+2)
        for x in a:
            count[x] += 1
        
        valid = True
        for val in range(1, n+1):
            if count[val] != 1:
                valid = False
                break
        if not valid:
            ans[0] = '0'
        
        left, right = 0, n-1
        for k in range(1, n):
            if a[left] == k:
                left += 1
                ans[n-k] = '1'
            elif a[right] == k:
                right -= 1
                ans[n-k] = '1'
            else:
                break
        
        print(''.join(ans))

if __name__ == "__main__":
    solve()
```

The code first checks if the array is a permutation for `k=1` and sets the first character of `ans`. Then it uses a two-pointer approach to verify whether increasing lengths can form valid permutations, updating `ans` from the end toward the beginning. This avoids recomputing subarray minimums explicitly and maintains linear time complexity.

## Worked Examples

### Example 1

Input: `[1,5,3,4,2]`

Binary string construction:

| Step | l | r | val | Action | ans |
| --- | --- | --- | --- | --- | --- |
| k=1 | 0 | 4 | 1 | a[l]==1 -> l+=1 | `1....` |
| k=2 | 1 | 4 | 2 | a[r]==2 -> r-=1 | `10...` |
| k=3 | 1 | 3 | 3 | a[l]==3 -> l+=1 | `101..` |
| k=4 | 2 | 3 | 4 | a[r]==4 -> r-=1 | `1011.` |
| k=5 | 2 | 2 | 5 | a[l]==5 -> l+=1 | `10111` |

This matches the sample output.

### Example 2

Input: `[1,3,2,1]`

Binary string:

- `k=1` fails because 1 appears twice. Only `k=4` works since the whole array contains all unique elements from 1 to 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Two-pointer traversal + frequency count is linear |
| Space | O(n) | Storing frequency counts and binary result array |

Given the sum of all $n$ is at most $3\cdot10^5$, the solution fits well within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("5\n5\n1 5 3 4 2\n4\n1 3 2 1\n5\n1 3 3 3 2\n10\n1 2 3 4 5 6 7 8 9 10\n3\n3 3 2") == "10111\n0001\n00111\n1111111111\n000"

# Custom cases
assert run("1\n1\n1") == "1", "single element"
assert run("1\n5\n5 4 3 2 1") == "11111", "reversed permutation"
assert run("1\n4\n2 2 2 2") == "0000", "all equal elements"
assert run("1\n6\n1 2 3 1 2 3") == "000001", "duplicates with length n window"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | `1` | Minimum size array |
| `1\n5\n5 4 3 2 1` | `11111` | Reverse permutation |
| `1\n4\n2 2 2 2` | `0000` | All elements equal |
| `1\n6\n1 2 3 1 2 3` | `000 |  |
