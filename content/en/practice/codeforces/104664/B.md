---
title: "CF 104664B - Noodle Tug of War"
description: "We are given a sequence of positive integers representing strengths of participants arranged in a line. The task is to choose a single split position such that the array is divided into a left prefix and a right suffix."
date: "2026-06-29T10:02:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104664
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 10-06-23 Div. 2 (Beginner)"
rating: 0
weight: 104664
solve_time_s: 53
verified: true
draft: false
---

[CF 104664B - Noodle Tug of War](https://codeforces.com/problemset/problem/104664/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of positive integers representing strengths of participants arranged in a line. The task is to choose a single split position such that the array is divided into a left prefix and a right suffix. The score of a split is defined as the product of the total strength on the left side and the total strength on the right side. The goal is to find the split that maximizes this product.

In other words, if we denote a prefix sum up to index k as $S_k$, then the score at split k is $S_k \cdot (S_N - S_k)$. We want the maximum value over all valid k from 1 to N-1. The special case when N equals 1 is trivial because one side is empty and the product is zero.

The constraints allow up to $10^5$ elements, each up to $10^4$. This immediately rules out any quadratic approach over split positions combined with recomputation of sums. A solution that tries every split and recomputes both sides from scratch would do about $O(N^2)$ additions, which is too slow for the time limit.

A common edge case is when all elements are equal. For example, if the array is [1, 1, 1, 1], the best split is in the middle producing 2 and 2, giving 4. A naive approach that mismanages prefix sums might incorrectly recompute partial ranges or miss the optimal balanced split.

Another subtle case is N = 1. For input [x], any split is invalid in the usual sense, but the problem defines the answer as 0. A careless implementation that always evaluates k from 1 to N might attempt to compute both sides incorrectly or access an empty suffix without handling it explicitly.

## Approaches

The brute-force idea is straightforward. For every possible split position k, compute the sum of elements from 1 to k and the sum from k+1 to N, then multiply them. Each sum computation can be done by scanning the array, so each split costs $O(N)$. Since there are $O(N)$ splits, the total complexity becomes $O(N^2)$. With $N = 10^5$, this would involve around $10^{10}$ operations, which is far beyond feasible limits.

The key observation is that recomputing sums repeatedly is wasteful. Once we know the total sum of the array, the right side sum for a split can be derived from the left side sum in constant time. If we maintain a running prefix sum while iterating through the array, each split evaluation becomes $O(1)$. This reduces the problem from recomputing ranges to maintaining a single cumulative state.

So instead of recalculating sums, we compute the total sum once, then sweep through the array, updating a prefix sum. At each position, the right sum is simply total minus prefix. We compute the product and track the maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(1) | Too slow |
| Prefix Sum Sweep | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of all elements in the array. This represents the sum of both sides combined before any split is chosen.
2. Initialize a variable `prefix` to zero. This will store the sum of the left side as we move the split point from left to right.
3. Initialize a variable `best` to zero. This stores the maximum product found so far.
4. Iterate through the array from the first element to the second-to-last element. We stop before the last element because the right side must be non-empty for a meaningful split.
5. At each index i, add the current element to `prefix`. This extends the left group by including the current participant.
6. Compute the right side sum as `total - prefix`. This works because every element is either in the prefix or the suffix, so subtracting gives the exact remaining sum.
7. Compute the score `prefix * (total - prefix)` and update `best` if this value is larger than the current maximum.

After completing the iteration, `best` holds the maximum possible score.

The correctness relies on the fact that every valid split corresponds to exactly one prefix sum value. By iterating over all prefixes, we enumerate all possible partitions, and for each partition we compute the exact score without approximation or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    if n == 1:
        print(0)
        return

    total = sum(a)
    prefix = 0
    best = 0

    for i in range(n - 1):
        prefix += a[i]
        right = total - prefix
        best = max(best, prefix * right)

    print(best)

if __name__ == "__main__":
    solve()
```

The solution begins by handling the single-element case explicitly, since no valid split exists. The total sum is computed once and reused throughout the sweep. The loop stops at `n-1` to ensure the suffix is non-empty.

A subtle detail is the order of updates: we add the element to `prefix` before computing the product, which aligns index i with the split after including a[i]. Mixing this order would shift the split and produce incorrect results.

## Worked Examples

### Example 1

Input:

```
5
1 2 3 4 5
```

| i | prefix | right | product |
| --- | --- | --- | --- |
| 0 | 1 | 14 | 14 |
| 1 | 3 | 12 | 36 |
| 2 | 6 | 9 | 54 |
| 3 | 10 | 5 | 50 |

The maximum occurs when the split is after the third element. The prefix sum is 6 and the suffix sum is 9, giving 54. This shows that the best split tends to balance the two sides rather than favoring extreme partitions.

### Example 2

Input:

```
4
3 2 5 1
```

| i | prefix | right | product |
| --- | --- | --- | --- |
| 0 | 3 | 8 | 24 |
| 1 | 5 | 6 | 30 |
| 2 | 10 | 1 | 10 |

The best split is after the second element, producing prefix 5 and suffix 6, yielding 30. This confirms that the optimal split is not necessarily centered by index, but depends on cumulative sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | One pass to compute total sum and one pass to evaluate all splits |
| Space | O(1) | Only a few integer variables are maintained |

The linear complexity is sufficient for $N = 10^5$, since it performs only a single pass over the input array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    if n == 1:
        return "0\n"

    total = sum(a)
    prefix = 0
    best = 0

    for i in range(n - 1):
        prefix += a[i]
        best = max(best, prefix * (total - prefix))

    return str(best) + "\n"

# provided samples
assert run("5\n1 2 3 4 5\n") == "54\n"
assert run("4\n3 2 5 1\n") == "30\n"

# custom cases
assert run("1\n7\n") == "0\n", "single element"
assert run("2\n10 10\n") == "100\n", "minimal split"
assert run("5\n1 1 1 1 1\n") == "6\n", "uniform array"
assert run("6\n5 4 3 2 1 0\n") == "54\n", "descending with zero"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | single-element edge case |
| 10 10 | 100 | smallest meaningful split |
| all ones | 6 | balanced split correctness |
| descending + zero | 54 | handling of uneven distributions |

## Edge Cases

For the input `1 7`, there is no valid split. The algorithm detects `n == 1` and immediately returns 0 without entering the loop. This avoids any incorrect computation involving empty suffixes.

For `10 10`, total sum is 20. At i = 0, prefix becomes 10 and suffix is also 10, producing 100. Since there is only one split, the algorithm correctly evaluates exactly one candidate.

For `[1, 1, 1, 1, 1]`, total is 5. Prefix evolution produces products 1×4, 2×3, 3×2, 4×1. The maximum is 6 at the middle split, and the sweep evaluates every possible split exactly once, ensuring no missing case.

For `[5, 4, 3, 2, 1, 0]`, the presence of zero does not affect correctness. The optimal split occurs before the smaller suffix dominates. The prefix-suffix decomposition still holds because zero is included in the total sum, and the subtraction formula remains valid for every position.
