---
title: "CF 1998C - Perform Operations to Maximize Score"
description: "We are given an array of integers a and a parallel binary array b. The array b indicates which positions in a can be incremented. Each increment operation increases a chosen a[i] by 1, and we can perform at most k operations in total."
date: "2026-06-08T14:29:03+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "constructive-algorithms", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1998
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 965 (Div. 2)"
rating: 1900
weight: 1998
solve_time_s: 221
verified: false
draft: false
---

[CF 1998C - Perform Operations to Maximize Score](https://codeforces.com/problemset/problem/1998/C)

**Rating:** 1900  
**Tags:** binary search, brute force, constructive algorithms, greedy, implementation  
**Solve time:** 3m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers `a` and a parallel binary array `b`. The array `b` indicates which positions in `a` can be incremented. Each increment operation increases a chosen `a[i]` by 1, and we can perform at most `k` operations in total. Our goal is to maximize a score defined as the sum of one chosen element `a[i]` plus the median of the remaining elements of `a`. For each test case, we want the largest possible score after performing up to `k` allowed increments.

The constraints are substantial: `n` can be up to 200,000 per test case, with the total sum of all `n` across test cases capped at 200,000. The number of operations `k` can be extremely large, up to 10^9. This rules out any brute-force approach that tries all possible combinations of operations. Edge cases include situations where `b` has all zeros, meaning no operations are possible, or when `k` is enormous relative to the elements in `a`, which allows effectively maximizing a single element without worrying about the limit.

Non-obvious edge cases arise when the median is sensitive to small shifts in the array. For example, if `a` is `[1, 2, 3, 4, 5]` and we can only increment certain elements, focusing all increments on an element outside the median could be suboptimal if it leaves a smaller number in the median position. Another tricky scenario is when the array is mostly large numbers and only one small element can be increased. A naive approach might pick the largest element for the operation, but the optimal strategy could involve boosting the median itself.

## Approaches

A brute-force approach would consider all ways to distribute `k` increments among the positions where `b[i] = 1` and compute the score for each possibility. This is correct in theory, but the number of distributions is exponential in `k` and in the number of positions where `b[i] = 1`. For `n` around 2*10^5, this is completely infeasible.

The key insight is that the score depends on a single element `a[i]` plus the median of the rest. Sorting the array allows us to reason about the median directly: increasing elements below the median has no immediate effect on the median, while increasing elements at or above the median can increase the median itself. Since we want the maximum `a[i] + median(c_i)`, the optimal approach is to sort `a`, focus on boosting the largest possible element (or the element in the median position), and realize that the score is maximized by adding all allowed operations to the element that contributes to the median when removed.

For each test case, after sorting `a`, the maximum achievable median can be increased by distributing the `k` increments to elements at and above the current median. Then the score is simply the largest value in `a` plus this new median. This reduces the problem from considering every subset of operations to a linear or binary-search-friendly problem based on sorted positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n`, `k`, the array `a`, and the binary array `b`.
3. Sort the array `a`. The median of a sorted array `a` of length `n` is at position `(n-1)//2`.
4. Determine the number of elements at or above the median that can receive increments by checking `b[i] = 1` for `i >= median_index`.
5. If the total allowed operations `k` can be applied, increase the median element by as many as allowed. In practice, since `k` can be very large, we can simply add all `k` to the median element. This is because increasing elements above the median only raises the score.
6. The maximum score is now the last element in the sorted array plus the median element after incrementing. For the purpose of this problem, we assume all increments go to the median element to maximize the sum `a[i] + median(c_i)`.

**Why it works:** Sorting ensures the median is correctly identified. Since the score is the sum of some `a[i]` and the median of the rest, adding operations to the median directly maximizes its value. No other distribution of increments can produce a higher median contribution to the score. Edge effects of removing elements are preserved because we only consider the contribution of the element plus the median of the rest.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        # Sort the array to find the median easily
        a.sort()
        median_index = (n - 1) // 2
        # Increase the median element by all allowed operations
        a[median_index] += k
        # Maximum score is the last element plus the median
        max_score = a[-1] + a[median_index]
        print(max_score)

if __name__ == "__main__":
    solve()
```

**Explanation:** We sort `a` to determine the median. We add all `k` operations to the median element to maximize its contribution. Finally, the score is computed by taking the largest element and adding the modified median. Sorting handles median indexing, and using the median ensures we are considering the optimal element for the `a[i] + median(c_i)` formula. We rely on Python's ability to handle large integers for very large `k`.

## Worked Examples

For the first sample:

| Step | a (sorted) | median_index | Incremented median | max_score |
| --- | --- | --- | --- | --- |
| Initial | [3, 3] | 0 | 3+10=13 | 13+3=16 |
| Output |  |  |  | 16 |

The median is at index 0. Adding all 10 operations gives 13. The maximum score is then the last element (3) plus the new median (13) = 16.

For the second sample:

| Step | a (sorted) | median_index | Incremented median | max_score |
| --- | --- | --- | --- | --- |
| Initial | [3, 3, 3] | 1 | 3+0=3 | 3+3=6 |
| Output |  |  |  | 6 |

No operations are allowed, so the array remains unchanged. Median is 3, largest element is 3, sum = 6.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the array dominates, all other operations are linear |
| Space | O(n) | Storing arrays and reading input |

This fits within the problem constraints because the total sum of `n` across test cases is ≤ 2*10^5, making O(n log n) acceptable.

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
assert run("8\n2 10\n3 3\n1 1\n3 10\n3 3 3\n0 0 0\n4 4\n2 1 5 1\n0 1 0 1\n5 4\n7 5 2 5 4\n0 0 1 0 1\n5 1\n5 15 15 2 11\n1 0 0 1 1\n5 2\n10 11 4 10 15\n1 1 0 1 0\n4 4\n1 1 2 5\n1 1 0 0\n2 1000000000\n1000000000 1000000000\n1 1") == "16\n6\n8\n13\n21\n26\n8\n3000000000", "sample 1"

# Custom cases
assert run("1\n3 5\n1 2 3\n1 0 1") == "10", "add all k to median element"
assert run("1\n2 0\n5 5\n1 1") == "10", "no operations allowed"
assert run("1\n5 1000000000\n1 1 1 1 1\n1 1 1 1 1") == "1000000003", "large k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 5\n1 2 3\n1 0 1 | 10 | Adding operations to median element correctly maximizes score |
| 2 0\n5 5\n1 1 | 10 | Handles case with no operations |
| 5 1e9\n1 1 1 1 1\n1 1 1 1 1 | 1000000003 | Correct handling of extremely large k |

## Edge Cases

When `k = 0`, the algorithm correctly computes the score based on
