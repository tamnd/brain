---
title: "CF 252A - Little Xor"
description: "We are asked to find a segment of consecutive elements in a small array of non-negative integers such that the bitwise XOR of all numbers in that segment is as large as possible. The input consists of the size of the array, $n$, followed by $n$ integers each less than $2^{30}$."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 252
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 153 (Div. 2)"
rating: 1100
weight: 252
solve_time_s: 52
verified: true
draft: false
---

[CF 252A - Little Xor](https://codeforces.com/problemset/problem/252/A)

**Rating:** 1100  
**Tags:** brute force, implementation  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find a segment of consecutive elements in a small array of non-negative integers such that the bitwise XOR of all numbers in that segment is as large as possible. The input consists of the size of the array, $n$, followed by $n$ integers each less than $2^{30}$. The output is a single integer representing the maximum XOR achievable among all contiguous subarrays.

Given that $n \le 100$, the array is small enough that algorithms with up to roughly $10^6$ operations are feasible in a 2-second time limit. The numbers themselves can be large (up to roughly $10^9$), but this primarily affects storage and XOR computation, which is fast.

A subtle edge case arises when all elements are zero. For example, with input:

```
3
0 0 0
```

the maximum XOR of any segment is 0. A naive implementation that assumes a segment must contain at least one non-zero element could mistakenly output an incorrect positive number. Another case is when the maximal XOR comes from a single element rather than combining multiple elements, such as:

```
4
1 2 3 4
```

where the maximum XOR is 7 from the segment `[3,4]`. Any approach must consider single-element segments explicitly.

## Approaches

The brute-force approach is conceptually straightforward. We can iterate over every possible subarray, calculate the XOR for that subarray, and track the maximum encountered. This works because XOR is associative, meaning the order of grouping does not change the result. The complexity for this method is $O(n^3)$ if we compute the XOR from scratch for every segment, but we can reduce it to $O(n^2)$ by computing XOR incrementally. Specifically, for a starting index $i$, we can initialize `current_xor` to 0 and iterate the ending index $j$ from $i$ to $n-1$, updating `current_xor` by XORing with `a[j]`. This eliminates recomputation and keeps the complexity manageable given the constraints, since $n^2 = 10,000$ is well within the allowed operations.

The key insight is that the array is small, so there is no need for advanced techniques like trie-based XOR maximization. XOR is fast, and $O(n^2)$ covers all possible segments. Trying to optimize further would be overkill and risk adding complexity without practical gain.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Accepted |
| Optimal | O(n^2) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `max_xor` to zero. This will store the maximum XOR found so far. We start with zero because XOR values are non-negative.
2. Loop over every starting index `i` of the array from 0 to `n-1`. Each `i` represents the beginning of a candidate segment.
3. For each starting index, initialize a variable `current_xor` to zero. This variable accumulates the XOR for the segment starting at `i`.
4. Loop over every ending index `j` from `i` to `n-1`. XOR the element `a[j]` into `current_xor`. After each XOR, compare `current_xor` with `max_xor` and update `max_xor` if it is larger. This ensures we consider every contiguous segment starting at `i`.
5. After both loops complete, print `max_xor`. It now holds the maximal XOR among all segments.

Why it works: XOR is associative and commutative, so we can compute the XOR incrementally from left to right for each starting index. By considering every possible starting index and extending the segment to the right, we guarantee that every contiguous subarray is evaluated exactly once. The invariant is that after processing index `i`, all segments starting at `i` and ending at any index `j >= i` have been considered, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

max_xor = 0
for i in range(n):
    current_xor = 0
    for j in range(i, n):
        current_xor ^= a[j]
        if current_xor > max_xor:
            max_xor = current_xor

print(max_xor)
```

We first read the size of the array and the array itself. We initialize `max_xor` to zero, which works for the edge case of all zeros. The nested loops ensure that every contiguous segment is checked. Updating `current_xor` incrementally avoids recalculating XORs repeatedly. The comparison `current_xor > max_xor` handles segments of length one as well as longer segments.

## Worked Examples

Sample 1 input:

```
5
1 2 1 1 2
```

| i | j | current_xor | max_xor |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 1 |
| 0 | 1 | 3 | 3 |
| 0 | 2 | 2 | 3 |
| 0 | 3 | 3 | 3 |
| 0 | 4 | 1 | 3 |
| 1 | 1 | 2 | 3 |
| 1 | 2 | 3 | 3 |
| 1 | 3 | 2 | 3 |
| 1 | 4 | 0 | 3 |
| 2 | 2 | 1 | 3 |
| 2 | 3 | 0 | 3 |
| 2 | 4 | 2 | 3 |
| 3 | 3 | 1 | 3 |
| 3 | 4 | 3 | 3 |
| 4 | 4 | 2 | 3 |

The trace confirms that the segment `[1,2]` gives the maximal XOR of 3.

Sample 2 input:

```
3
1 2 3
```

| i | j | current_xor | max_xor |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 1 |
| 0 | 1 | 3 | 3 |
| 0 | 2 | 0 | 3 |
| 1 | 1 | 2 | 3 |
| 1 | 2 | 1 | 3 |
| 2 | 2 | 3 | 3 |

The maximal XOR of 3 occurs with the single element segment `[2]` and confirms the algorithm handles single-element segments correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Two nested loops over the array, each index pair evaluated once. |
| Space | O(1) | Only a few integer variables are used, no additional arrays. |

Given $n \le 100$, $n^2 = 10,000$ operations are well below the 2-second limit. Memory usage is trivial, far below the 256 MB allowed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    max_xor = 0
    for i in range(n):
        current_xor = 0
        for j in range(i, n):
            current_xor ^= a[j]
            if current_xor > max_xor:
                max_xor = current_xor
    return str(max_xor)

# provided samples
assert run("5\n1 2 1 1 2\n") == "3", "sample 1"
assert run("3\n1 2 3\n") == "3", "sample 2"

# custom cases
assert run("1\n0\n") == "0", "single zero element"
assert run("4\n7 7 7 7\n") == "7", "all equal values"
assert run("5\n0 1 0 1 0\n") == "1", "alternating zeros and ones"
assert run("100\n" + " ".join(str(i) for i in range(100)) + "\n") == "127", "maximum-size array"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element 0 | 0 | Minimal size, zero value |
| 4 elements all 7 | 7 | All equal numbers, single-element maximum |
| Alternating 0/1 | 1 | Handling segments of length 1 vs longer |
| 100 elements 0..99 | 127 | Maximum allowed array size |

## Edge Cases

For the single-element zero array `1\n0`, the inner loop runs once, `current_xor` is 0, and `max_xor` remains 0. This correctly handles an array where the maximum XOR is zero. For arrays where the maximum XOR comes from a single element, such as `4\n1 2 3 4`, the inner loop ensures that each element is considered independently as a segment of length one.
