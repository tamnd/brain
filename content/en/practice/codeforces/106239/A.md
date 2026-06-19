---
title: "CF 106239A - \u6781\u5dee\u6700\u5927\u7684\u533a\u95f4"
description: "We are given a sequence of integers and asked to choose a contiguous segment so that the difference between the largest and smallest element inside that segment is as large as possible."
date: "2026-06-19T16:26:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106239
codeforces_index: "A"
codeforces_contest_name: "2025\u5e7f\u4e1c\u5de5\u4e1a\u5927\u5b66\u65b0\u751f\u8d5b(\u51b3\u8d5b)"
rating: 0
weight: 106239
solve_time_s: 56
verified: true
draft: false
---

[CF 106239A - \u6781\u5dee\u6700\u5927\u7684\u533a\u95f4](https://codeforces.com/problemset/problem/106239/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and asked to choose a contiguous segment so that the difference between the largest and smallest element inside that segment is as large as possible. Along with the value of this maximum difference, we must also output one segment that achieves it.

The input is a single array of length up to 100, with each value between 0 and 100. A valid answer is any pair of indices $l, r$ such that the subarray $A[l..r]$ has the maximum possible value of $\max(A[l..r]) - \min(A[l..r])$.

The constraint $n \le 100$ already signals that a cubic or even quadratic solution is acceptable. A linear or linearithmic solution would also be fine, but unnecessary. The key observation is that the problem is not asking for a unique structure like a special monotonic property or dynamic state, only a global optimum over all subarrays.

A subtle point is that the optimal segment is not necessarily unique, and multiple segments may achieve the same maximum difference. Any one valid segment is acceptable, which means we do not need tie-breaking rules beyond correctness.

A naive but common mistake is to assume the optimal segment must include either the global minimum or global maximum of the entire array. That is correct for this problem but needs justification through enumeration logic rather than assumption.

For example, consider:

```
A = [2, 3, 4, 1]
```

The best segment is the whole array, giving max 4 and min 1, difference 3. A mistake would be to pick a segment like [2, 3, 4], which has difference 2, missing the fact that extending to include 1 improves the result.

Another edge case is when all elements are equal:

```
A = [5, 5, 5]
```

Every segment has difference 0, so any single element segment is valid. A naive solution might still return a longer segment unnecessarily, but correctness is unaffected.

## Approaches

The most direct solution is to enumerate every possible subarray. For each pair of indices $l, r$, we scan the subarray to compute its minimum and maximum, then update the best answer if this difference improves the current best.

This works because it explicitly evaluates the objective function for every candidate segment. The correctness is immediate: no subarray is missed.

However, the cost is high. There are $O(n^2)$ subarrays, and computing min and max for each takes $O(n)$, leading to $O(n^3)$ total operations. While $n = 100$ makes this borderline but still acceptable, it is unnecessarily slow.

We can improve this by reusing computation. If we fix the left endpoint $l$, we can extend the right endpoint $r$ incrementally while maintaining the current minimum and maximum in constant time. Each expansion updates the answer in $O(1)$, reducing the overall complexity to $O(n^2)$.

The key idea is that recomputing min and max from scratch for every segment is redundant. Since segments with the same left endpoint form a growing sequence, we can maintain state as we extend.

This turns the problem into a two-layer loop where the outer loop fixes the start and the inner loop extends the end while maintaining running extrema.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Acceptable but slow |
| Expand with running min/max | O(n²) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize variables to store the best answer found so far: best difference, best left index, and best right index. We start with a very small best difference so that any real segment improves it.
2. Fix a left endpoint $l$ from 1 to $n$. This represents the start of a candidate subarray. Every valid subarray must begin somewhere, so we systematically try all possibilities.
3. For each $l$, initialize two variables `cur_min` and `cur_max` to $A[l]$. This represents the state of the subarray consisting only of the single element at position $l$.
4. Extend the right endpoint $r$ from $l$ to $n$, updating `cur_min = min(cur_min, A[r])` and `cur_max = max(cur_max, A[r])`. This maintains the correct extrema of the current subarray without recomputation.
5. Compute the current difference `cur_max - cur_min`. If this is larger than the best difference so far, update the stored answer to $(l, r)$ and the new difference.
6. Continue expanding until all $r$ values for this $l$ are processed, then move to the next $l$.
7. After all iterations, output the stored best segment and its difference.

### Why it works

At every step of extending $r$, the algorithm maintains the exact minimum and maximum of the current subarray $[l, r]$. This is an invariant preserved by the update rule: adding one element only requires comparing it with previous extrema. Since every subarray is uniquely represented by some pair $(l, r)$, and each such pair is evaluated exactly once, the algorithm considers all candidates without duplication or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    best_diff = -1
    best_l, best_r = 0, 0
    
    for l in range(n):
        cur_min = a[l]
        cur_max = a[l]
        
        for r in range(l, n):
            if r > l:
                cur_min = min(cur_min, a[r])
                cur_max = max(cur_max, a[r])
            
            diff = cur_max - cur_min
            if diff > best_diff:
                best_diff = diff
                best_l = l
                best_r = r
    
    print(best_l + 1, best_r + 1, best_diff)

if __name__ == "__main__":
    solve()
```

The code directly implements the two-layer enumeration strategy. The outer loop fixes the left boundary, and the inner loop expands the right boundary while maintaining running minimum and maximum values. The +1 shift at output is required because the problem uses 1-based indexing while Python arrays are 0-based.

A common implementation pitfall is reinitializing `cur_min` and `cur_max` incorrectly inside the inner loop, which would destroy the incremental optimization. Another subtle issue is updating extrema before computing the difference, which must happen in the correct order to ensure the current element is included.

## Worked Examples

### Example 1

Input:

```
4
2 3 4 1
```

| l | r | cur_min | cur_max | diff | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 2 | 0 | (1,1,0) |
| 0 | 1 | 2 | 3 | 1 | (1,2,1) |
| 0 | 2 | 2 | 4 | 2 | (1,3,2) |
| 0 | 3 | 1 | 4 | 3 | (1,4,3) |

This trace shows how extending the interval eventually captures both global extrema 4 and 1, producing the maximum possible difference.

### Example 2

Input:

```
5
1 5 3 5 2
```

| l | r | cur_min | cur_max | diff | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1 | 0 | (1,1,0) |
| 0 | 1 | 1 | 5 | 4 | (1,2,4) |
| 0 | 4 | 1 | 5 | 4 | (1,2,4) |
| 2 | 4 | 2 | 5 | 3 | (1,2,4) |

The optimal segments here are multiple, including [1,2] and [1,4], both giving difference 4. The algorithm correctly keeps the first best found but would also accept others if they appear later.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Two nested loops over all subarray endpoints, with O(1) updates per step |
| Space | O(1) | Only a few scalar variables are maintained |

With $n \le 100$, the total number of iterations is at most 10,000, which is trivial under typical limits. Even a cubic solution would be acceptable, but the quadratic version is clean and efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().split()))
    
    best_diff = -1
    best_l, best_r = 0, 0
    
    for l in range(n):
        cur_min = a[l]
        cur_max = a[l]
        
        for r in range(l, n):
            if r > l:
                cur_min = min(cur_min, a[r])
                cur_max = max(cur_max, a[r])
            
            diff = cur_max - cur_min
            if diff > best_diff:
                best_diff = diff
                best_l = l
                best_r = r
    
    return f"{best_l+1} {best_r+1} {best_diff}"

# provided sample-style cases
assert run("4\n2 3 4 1\n") == "1 4 3"

# minimum size
assert run("1\n7\n") == "1 1 0"

# all equal
assert run("3\n5 5 5\n") == "1 1 0"

# increasing sequence
assert run("5\n1 2 3 4 5\n") == "1 5 4"

# decreasing sequence
assert run("4\n9 7 5 3\n") == "1 4 6"

# mixed
assert run("5\n1 5 3 5 2\n") == "1 2 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 1 0 | minimum size correctness |
| all equal | 1 1 0 | zero variance handling |
| increasing | 1 5 4 | global min/max span |
| decreasing | 1 4 6 | order independence |
| mixed | 1 2 4 | early optimal subarray detection |

## Edge Cases

For a single-element array like `A = [7]`, the algorithm sets `cur_min = cur_max = 7` and immediately evaluates a difference of 0. Since no other segments exist, it correctly outputs `(1, 1, 0)`.

For an all-equal array like `A = [3, 3, 3, 3]`, every iteration maintains `cur_min = cur_max = 3` regardless of expansion. The difference never exceeds 0, so the first segment `(1, 1)` remains the stored answer.

For a strictly increasing array like `A = [1, 2, 3, 4]`, the first outer loop already discovers that extending to the full range produces the maximum difference. The invariant ensures that once both extremes are included, no later segment can exceed that value, since all future subarrays are subsets or equal-range variants.
