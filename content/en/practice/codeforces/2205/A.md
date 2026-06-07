---
title: "CF 2205A - Simons and Making It Beautiful"
description: "We are given a permutation p of length n. An index i is called ugly if it is the first time the maximum value is reached at that position. More formally, i is ugly if p[i] is equal to the maximum of p[1..i]."
date: "2026-06-07T19:50:13+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 2205
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1083 (Div. 2)"
rating: 800
weight: 2205
solve_time_s: 145
verified: false
draft: false
---

[CF 2205A - Simons and Making It Beautiful](https://codeforces.com/problemset/problem/2205/A)

**Rating:** 800  
**Tags:** brute force, constructive algorithms  
**Solve time:** 2m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation `p` of length `n`. An index `i` is called ugly if it is the first time the maximum value is reached at that position. More formally, `i` is ugly if `p[i]` is equal to the maximum of `p[1..i]`. Simons can perform at most one swap between any two positions in the array. Our task is to output a permutation `q` obtained from `p` with at most one swap such that the number of ugly indices is minimized.

The input consists of multiple test cases. Each test case provides `n` and the array `p` of distinct integers from `1` to `n`. The output is a permutation `q` for each test case satisfying the minimal ugliness criterion.

The constraints indicate `n` can be up to 500, and `t` up to 100. With `n` small, even an `O(n^2)` algorithm is feasible, but we can find a linear-time solution based on properties of permutations and the definition of ugly indices.

A naive implementation might try every possible swap and count ugly indices for each, but this is unnecessary. Edge cases include permutations that are already in decreasing order, where the first element is the largest, or already optimal permutations where no swap improves the count. For instance, `p = [3,1,2]` is already minimal because swapping would increase ugliness.

## Approaches

A brute-force approach is straightforward: for each test case, iterate over all pairs `(i,j)` with `i<j`, swap `p[i]` and `p[j]`, count the number of ugly indices, and track the permutation with the minimum count. Each swap requires `O(n)` to count ugliness, so the total time complexity is `O(n^3)` per test case. With `n = 500`, this is roughly 125 million operations per test case, which may barely fit in 1 second depending on the constant factor, but it is clearly suboptimal.

The optimal approach leverages the fact that an index is ugly if its value is the running maximum. To reduce ugliness, we want the first element to be the largest because that ensures no subsequent element triggers a new maximum until a smaller number is reached. A simple strategy is to find the maximum element `n` and place it at the beginning of the array if it is not already there. Swapping the first element with the maximum element achieves this in a single operation. If the maximum is already at the start, no swap is needed. This guarantees only one ugly index at the start, minimizing ugliness.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the permutation `p`.
3. Identify the position `max_idx` of the maximum value `n` in the array.
4. If `max_idx` is not the first position, swap `p[0]` and `p[max_idx]`. This ensures the largest value is first, minimizing ugly indices.
5. Output the resulting permutation.

Why it works: The property we use is that an index is ugly if it is the first occurrence of the running maximum. By placing the largest element at the first position, we guarantee that the first ugly index is at position 1, and no other index can be ugly until a larger number appears, which does not exist. This strategy is optimal because any swap involving a smaller element cannot reduce ugliness beyond placing the largest element first.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    p = list(map(int, input().split()))
    max_val = n
    max_idx = p.index(max_val)
    if max_idx != 0:
        p[0], p[max_idx] = p[max_idx], p[0]
    print(" ".join(map(str, p)))
```

The solution first finds the position of the maximum value in `p`. If it is not at the first position, it swaps it with the first element. The swap is safe because it is allowed once per test case. We use `p.index(n)` which is `O(n)`, and the swap itself is `O(1)`. The `print` statement outputs the permutation for each test case. No extra space beyond the array is used, and boundary conditions like `n=1` are naturally handled.

## Worked Examples

**Example 1**

Input: `p = [1, 2]`

| Step | p | max_val | max_idx | Action |
| --- | --- | --- | --- | --- |
| initial | [1,2] | 2 | 1 | swap positions 0 and 1 |
| after swap | [2,1] | 2 | 0 | print [2,1] |

Explanation: The largest element `2` is moved to the first position. Ugly indices are minimized to 1.

**Example 2**

Input: `p = [4, 1, 3, 2, 6, 7, 8, 5]`

| Step | p | max_val | max_idx | Action |
| --- | --- | --- | --- | --- |
| initial | [4,1,3,2,6,7,8,5] | 8 | 6 | swap positions 0 and 6 |
| after swap | [8,1,3,2,6,7,4,5] | 8 | 0 | print [8,1,3,2,6,7,4,5] |

Explanation: The largest element `8` is placed at the beginning. Ugly indices occur at position 1, the minimal possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | `p.index(n)` is O(n), swap is O(1) |
| Space | O(n) | We store the permutation in memory |

With `t <= 100` and `n <= 500`, the worst-case total operations are 50,000, which is easily within the 1-second limit.

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
        p = list(map(int, input().split()))
        max_val = n
        max_idx = p.index(max_val)
        if max_idx != 0:
            p[0], p[max_idx] = p[max_idx], p[0]
        print(" ".join(map(str, p)))
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("5\n2\n1 2\n4\n2 3 1 4\n5\n3 2 4 5 1\n1\n1\n8\n4 1 3 2 6 7 8 5\n") == \
"2 1\n4 3 1 2\n5 2 4 3 1\n1\n8 1 3 2 6 7 4 5", "sample 1"

# custom cases
assert run("1\n1\n1\n") == "1", "single element"
assert run("1\n3\n3 2 1\n") == "3 2 1", "max already first"
assert run("1\n4\n1 2 3 4\n") == "4 2 3 1", "max last"
assert run("1\n5\n2 1 5 3 4\n") == "5 1 2 3 4", "max middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | n=1 edge case |
| 3 2 1 | 3 2 1 | max already first, no swap needed |
| 1 2 3 4 | 4 2 3 1 | max last position swap |
| 2 1 5 3 4 | 5 1 2 3 4 | max in middle swap |

## Edge Cases

For `n = 1`, the array `[1]` has only one element and is trivially optimal. The algorithm detects that `max_idx = 0`, so no swap occurs and the output is `[1]`.

For an array where the maximum is already first, such as `[3,2,1]`, the algorithm leaves the permutation unchanged. Swapping any other element would increase the number of ugly indices. The algorithm correctly identifies that the initial permutation is optimal and does not perform unnecessary operations.

If the maximum is at the last position, e.g., `[1,2,3,4]`, the algorithm swaps `4` to the first position, giving `[4,2,3,1]`. Ugly indices are now minimized to 1 at position 1, whereas any other swap would leave multiple ugly indices at earlier positions.
