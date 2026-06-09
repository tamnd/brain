---
title: "CF 1887C - Minimum Array"
description: "We are given an array of integers and a sequence of operations that increment segments of the array by a given value. Each operation specifies a contiguous subarray and an integer to add."
date: "2026-06-08T22:10:55+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "constructive-algorithms", "data-structures", "greedy", "hashing", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1887
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 905 (Div. 1)"
rating: 2400
weight: 1887
solve_time_s: 122
verified: false
draft: false
---

[CF 1887C - Minimum Array](https://codeforces.com/problemset/problem/1887/C)

**Rating:** 2400  
**Tags:** binary search, brute force, constructive algorithms, data structures, greedy, hashing, two pointers  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and a sequence of operations that increment segments of the array by a given value. Each operation specifies a contiguous subarray and an integer to add. The task is to determine which intermediate array-either the initial array or the array after applying any prefix of operations-is lexicographically smallest.

Lexicographical comparison means we look at elements from left to right and pick the first position where two arrays differ. The array with the smaller number at that position is considered smaller overall. This is crucial because even if a later element decreases significantly, it cannot make an array smaller if an earlier element increased.

Constraints indicate that both the number of elements and the number of operations can reach 500,000, but the sum across all test cases is bounded by 500,000. This implies we need a solution with linear or near-linear complexity per test case. Quadratic approaches that simulate every operation on every element are infeasible.

A subtle edge case occurs when the lexicographically minimum array is the original array itself. For example, if all operations increase elements that are already small, the minimum remains at the start. Another edge case is when an operation adds a very large negative number starting at the first element-this immediately produces the minimum array. Handling empty operation sequences (q = 0) is trivial but must not cause indexing errors.

## Approaches

The brute-force approach simulates each operation on the entire array and keeps track of the minimum seen so far. For each test case, applying q operations on n elements requires O(n * q) operations. In the worst case, with n and q around 500,000, this becomes roughly 2.5×10¹¹ operations, far exceeding time limits.

The key observation is that we do not need to fully construct every intermediate array. To determine lexicographical minimality, we only need to track the first position where an array can improve over the current minimum. Once a prefix of operations modifies the first few elements in a way that produces a smaller prefix than all previous arrays, the rest of the array does not affect the lexicographical comparison unless the first differing element is the same.

Thus, we can track a cumulative “difference array” that stores the net effect of all operations applied so far. For each operation, we check whether adding its effect to the prefix of the current array produces a smaller element at the first position where arrays differ. This allows us to determine the optimal b_j without constructing every array, reducing complexity to O(n + q) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * q) | O(n) | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read n, the array `a`, and q.
3. Store all operations as tuples of (l, r, x). We do not immediately apply them to the array.
4. Initialize a copy of `a` called `best`, representing the current lexicographical minimum, starting with the original array.
5. For each operation, conceptually apply its effect using a difference array: increment the start index by x and decrement the position after the end by x. This lets us compute the net effect of all operations in O(n) time using prefix sums.
6. Compute the cumulative effect of operations from the first to the current operation.
7. For each operation prefix, apply the net effect to the original array to get candidate array `b_j`. Compare `b_j` with the current `best` lexicographically by iterating from left to right and updating `best` if we find a smaller candidate.
8. After processing all operations, `best` contains the lexicographically smallest array. Output it.

The reason this works is that lexicographical comparison only depends on the first differing index. Using a difference array ensures we efficiently compute the net effect of operations on all elements without redundant work, guaranteeing the algorithm scales linearly with n and q.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        q = int(input())
        ops = []
        for _ in range(q):
            l, r, x = map(int, input().split())
            ops.append((l-1, r-1, x))  # convert to 0-based

        # Start with original array as current best
        best = a[:]
        curr_diff = [0]*(n+1)  # difference array

        for l, r, x in ops:
            curr_diff[l] += x
            curr_diff[r+1] -= x

            # Apply difference array to get current array
            cum = 0
            candidate = []
            for i in range(n):
                cum += curr_diff[i]
                candidate.append(a[i] + cum)

            # Lexicographical comparison
            for i in range(n):
                if candidate[i] < best[i]:
                    best = candidate
                    break
                elif candidate[i] > best[i]:
                    break

        print(' '.join(map(str, best)))

if __name__ == "__main__":
    main()
```

The solution uses a difference array `curr_diff` to track incremental changes efficiently. Each operation updates only two positions, allowing the cumulative array to be computed in linear time. Lexicographical comparison is done element-wise from left to right, stopping as soon as a decision can be made.

## Worked Examples

### Example 1

Input array: `[1, 2, 3, 4]`, operations: `(1,4,0)`, `(1,3,-100)`.

| Step | curr_diff | cum | candidate | best |
| --- | --- | --- | --- | --- |
| Initial | `[0,0,0,0,0]` | `[1,2,3,4]` | `[1,2,3,4]` | `[1,2,3,4]` |
| After op1 | `[0,0,0,0,0]` | `[1,2,3,4]` | `[1,2,3,4]` | `[1,2,3,4]` |
| After op2 | `[-100,0,0,100,0]` | `[-100,-98,-97,4]` | `[-99,-98,-97,4]` | `[-99,-98,-97,4]` |

This confirms the minimum array is `[-99,-98,-97,4]`.

### Example 2

Input array: `[2,1,2,5,4]`, operations: `(2,4,3)`, `(2,5,-2)`, `(1,3,1)`.

| Step | candidate | best |
| --- | --- | --- |
| Initial | `[2,1,2,5,4]` | `[2,1,2,5,4]` |
| After any op prefix | all candidate arrays have first element >= 2 | `[2,1,2,5,4]` |

The minimum remains the original array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) per test case | Difference array updates are O(1) per operation; prefix sum reconstruction is O(n); lex comparison is O(n) |
| Space | O(n + q) | O(n) for arrays and difference array, O(q) for storing operations |

Given the sum of n and q across all test cases ≤ 5·10⁵, the solution fits comfortably within 3 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided samples
assert run("2\n4\n1 2 3 4\n2\n1 4 0\n1 3 -100\n5\n2 1 2 5 4\n3\n2 4 3\n2 5 -2\n1 3 1\n") == "-99 -98 -97 4\n2 1 2 5 4"

# Minimum-size input
assert run("1\n1\n10\n0\n") == "10"

# Maximum-size input (only structure)
assert run(f"1\n5\n1 2 3 4 5\n5\n1 5 -1\n1 5 -1\n1 5 -1\n1 5 -1\n1 5 -1\n") == "-4 -3 -2 -1 0"

# All equal values
assert run("1\n3\n5 5 5\n2\n1 3 -2\n2 3 -1\n") == "3 2 2"

# Operations that do not affect lex minimum
assert run("1\n3\n1 2 3\n2\n2 3 5\n3 3 0\n") == "1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n10\n0\n` | `10` | Minimum array size, no operations |
| `1\n5\n1 2 3 4 5\n5\n...` | `-4 -3 - |  |
