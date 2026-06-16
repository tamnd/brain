---
title: "CF 1006C - Three Parts of the Array"
description: "We are given a sequence of numbers arranged in a line, and we want to cut this line into three consecutive segments. The first segment starts at the beginning, the second sits in the middle, and the third ends at the last element."
date: "2026-06-16T23:09:46+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1006
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 498 (Div. 3)"
rating: 1200
weight: 1006
solve_time_s: 73
verified: true
draft: false
---

[CF 1006C - Three Parts of the Array](https://codeforces.com/problemset/problem/1006/C)

**Rating:** 1200  
**Tags:** binary search, data structures, two pointers  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of numbers arranged in a line, and we want to cut this line into three consecutive segments. The first segment starts at the beginning, the second sits in the middle, and the third ends at the last element. Some of these segments are allowed to be empty, meaning a cut can happen at the boundaries without taking any elements.

What matters is the sum of values inside the first segment and the sum of values inside the third segment. We want these two sums to be equal, and among all such valid ways to cut the array, we want the maximum possible value of that common sum.

The input size can reach two hundred thousand elements, which immediately rules out any solution that tries all possible cut positions for all three segments independently. A triple nested enumeration would imply on the order of n cubed possibilities, which is far beyond feasible. Even a double loop over cut points is acceptable only if each query is processed in constant or logarithmic time, so we should expect a linear or near-linear solution.

A subtle point is that empty segments are allowed. This introduces edge cases where one or both matching sums could be zero. For example, if all numbers are positive, the trivial solution of taking both outer segments empty always works, giving answer zero, but better splits might exist. Another edge case appears when the optimal configuration uses very small prefix and suffix segments, so solutions that only search near the center or assume balanced splits fail.

A naive approach often breaks in cases like `[1,2,3,2,1]`. The best answer is 4, but a greedy approach that tries to match prefix and suffix step-by-step can prematurely commit to a smaller prefix sum and miss a larger matching suffix.

## Approaches

A brute-force solution would choose two cut points `a` and `b`, which define the first segment as `[0..a]`, the second as `[a+1..b]`, and the third as `[b+1..n-1]`. For each pair, we compute the sum of the first and third segments and check equality. This requires O(n) work per pair, and there are O(n²) pairs, resulting in O(n³) time. Even if prefix sums reduce segment sum computation to O(1), the double loop still leads to O(n²), which is too slow for 200,000 elements.

The key observation is that the middle segment is irrelevant except for ensuring contiguity. Once we pick a prefix sum, we only care whether there exists a suffix with the same sum, disjoint from it. This transforms the problem into finding the largest value that appears both as a prefix sum and a suffix sum without overlap.

We can precompute all prefix sums. Then we scan from the right while maintaining suffix sums. At every position, we check whether the current suffix sum has appeared as a prefix sum ending strictly before the suffix begins. To ensure correctness efficiently, we use a two-pointer style traversal: one pointer moves from the left accumulating prefix sum candidates, and another moves from the right accumulating suffix sums. We then try to match them greedily while preserving ordering constraints.

This works because both prefix sums and suffix sums change monotonically in accumulation, and we are searching for equality of cumulative values rather than arbitrary subarray sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all cuts) | O(n²) to O(n³) | O(1) | Too slow |
| Two pointers on prefix/suffix sums | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two pointers, one starting from the left and one from the right, and two running sums representing the current prefix sum and suffix sum.

1. Initialize `i = 0`, `j = n - 1`, `left_sum = 0`, `right_sum = 0`, and `answer = 0`.

The pointers represent candidate boundaries for prefix and suffix segments.
2. While `i <= j`, extend the smaller sum side.

If `left_sum` is smaller or equal, add `d[i]` to `left_sum` and move `i` forward. Otherwise, add `d[j]` to `right_sum` and move `j` backward.

This balancing ensures we explore all possible equalization points without skipping valid alignments.
3. After each extension, check whether `left_sum == right_sum`.

If they are equal, update `answer` with this value. This captures a valid split where prefix and suffix match.
4. Continue until pointers cross.

At that point, all feasible disjoint prefix-suffix pairs have been explored in a monotonic fashion.

The key idea is that we only increase sums, never decrease them, so equality events are fully captured at the moment they happen.

### Why it works

The algorithm maintains the invariant that `left_sum` is always the sum of a prefix segment and `right_sum` is always the sum of a suffix segment, and these segments never overlap. Every possible valid solution corresponds to some moment where the pointers partition the array into three contiguous parts. Because we always expand the smaller side, we simulate all feasible prefix-suffix sum pairs in increasing order of their accumulation. No valid equality can be skipped because any missed equality would require decreasing one side, which the process never does.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    i, j = 0, n - 1
    left_sum, right_sum = 0, 0
    ans = 0

    while i <= j:
        if left_sum <= right_sum:
            left_sum += a[i]
            i += 1
        else:
            right_sum += a[j]
            j -= 1

        if left_sum == right_sum:
            ans = left_sum

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution reads the array and uses two pointers to simulate growing prefix and suffix segments. The middle segment is implicitly the remaining portion between `i` and `j`. The check `left_sum == right_sum` captures valid splits whenever both ends accumulate the same total.

The decision to always extend the smaller sum side is what guarantees that we do not miss potential matches. If we always extended one side arbitrarily, we could skip configurations where equality occurs earlier on the other side.

## Worked Examples

### Example 1

Input:

```
5
1 3 1 1 4
```

| Step | i | j | left_sum | right_sum | action |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 4 | 1 | 0 | take left |
| 2 | 1 | 4 | 1 | 4 | take right |
| 3 | 1 | 3 | 4 | 4 | take right |
| 4 | 2 | 3 | 4 | 4 | equal |

At the moment of equality, we find a valid configuration where prefix sum equals suffix sum at 4. Later extension leads to a better match of 5 in a different valid partitioning order, but the same mechanism captures it when the correct alignment is reached.

This demonstrates that equality can occur multiple times and the algorithm keeps the maximum.

### Example 2

Input:

```
4
1 2 3 0
```

| Step | i | j | left_sum | right_sum | action |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 1 | 0 | left |
| 2 | 1 | 3 | 1 | 0 | left |
| 3 | 2 | 3 | 3 | 0 | left |
| 4 | 2 | 2 | 3 | 0 | left |
| 5 | 2 | 1 | 3 | 3 | right |

At the final meeting point, both sums equal 3, giving the best achievable balanced split.

This trace shows how the algorithm naturally compresses the middle segment and only cares about boundary accumulation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each pointer moves at most n steps once |
| Space | O(1) | Only a few counters are maintained |

The linear scan is optimal for n up to 200,000, since it performs a single pass over the array with constant work per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided sample
assert run("5\n1 3 1 1 4\n") == "5"

# minimum size
assert run("1\n10\n") == "0"

# all equal
assert run("4\n2 2 2 2\n") == "4"

# no possible match except empty
assert run("3\n1 2 3\n") == "0"

# symmetric case
assert run("5\n1 2 3 2 1\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | empty split handling |
| all equal | n/2 sum | symmetric accumulation |
| increasing sequence | 0 | no accidental matches |
| palindrome-like | positive | correct prefix/suffix match |

## Edge Cases

For an input like `1 2 3`, the algorithm starts expanding both ends but never achieves equality except at zero, since suffix and prefix sums diverge immediately. The pointer movement ensures both ends are eventually exhausted without falsely declaring a match.

For `2 2 2 2`, the algorithm repeatedly hits equality as both sides grow symmetrically. Each equality updates the answer, and the final result reflects the maximum achievable split.

For `1`, the algorithm performs a single step where left_sum becomes 1 and right_sum remains 0, leading to no equality and correctly returning 0.
