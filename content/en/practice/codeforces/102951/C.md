---
title: "CF 102951C - LCS on Permutations"
description: "We are given two sequences that contain the same elements in different orders, typically two permutations of length $n$."
date: "2026-07-04T07:22:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102951
codeforces_index: "C"
codeforces_contest_name: "USACO Guide Problem Submission"
rating: 0
weight: 102951
solve_time_s: 44
verified: true
draft: false
---

[CF 102951C - LCS on Permutations](https://codeforces.com/problemset/problem/102951/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences that contain the same elements in different orders, typically two permutations of length $n$. The task is to determine the length of the longest sequence of values that appears in both permutations in the same relative order, without requiring the values to be contiguous.

Concretely, imagine you have a list of labels arranged in one order on a shelf, and another shelf with the same labels but rearranged. You are allowed to pick some labels from the first shelf, preserving left to right order, and you want the longest possible sequence that can also be picked in the same order from the second shelf.

The output is a single integer, the maximum number of elements that can be matched in this way.

The key constraint that drives the solution is that the inputs are permutations, meaning every value appears exactly once in each array. With $n$ up to around $10^5$, any quadratic approach that compares all pairs of positions would require on the order of $10^{10}$ operations in the worst case, which is far beyond feasible limits in a 2-second runtime. This immediately rules out dynamic programming solutions that explicitly compute LCS in $O(n^2)$.

A few edge situations are easy to mishandle.

If the two permutations are identical, for example:

Input:

$A = [1, 2, 3, 4]$, $B = [1, 2, 3, 4]$

The correct answer is 4, since the entire sequence matches. A naive approach that only checks equality of positions instead of order would still work here, which can falsely reassure a wrong solution.

If one permutation is reversed:

Input:

$A = [1, 2, 3, 4]$, $B = [4, 3, 2, 1]$

The correct answer is 1, since no two elements preserve relative order. Solutions that assume matching indices or forget ordering constraints often overcount here.

Another subtle failure case appears when values are correct but positions are misaligned:

Input:

$A = [2, 3, 1, 4]$, $B = [1, 2, 3, 4]$

The correct answer is 2, not 3, because only some subsequences preserve order in both arrays.

## Approaches

A direct way to think about the problem is to try all subsequences of the first permutation and check whether each subsequence appears in the second permutation in the same order. This is correct in principle, because it explicitly tests every candidate sequence that could be part of a common subsequence. However, the number of subsequences of an $n$-element array is $2^n$, and even checking each one against the second array costs linear time, leading to an exponential explosion that becomes impossible even for moderate $n$.

The structural breakthrough comes from recognizing that the second permutation defines a fixed position for every value. Instead of comparing values directly, we can translate the first permutation into a sequence of indices representing where each element appears in the second permutation. Once this transformation is done, the problem changes character completely: we are no longer matching two permutations, but finding the longest increasing subsequence in a single array of indices.

This works because preserving relative order in both permutations is equivalent to preserving increasing order of positions in the second permutation. Any subsequence of the first permutation corresponds to a sequence of indices in the second, and that subsequence is valid if and only if those indices are strictly increasing.

The LIS problem can be solved in $O(n \log n)$ using a greedy construction with binary search, which is efficient enough for $n = 10^5$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsequences | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Map + LIS | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

## Steps

1. Build a position map for the second permutation, storing for each value its index. This allows constant-time lookup of where any element lands in the second sequence.
2. Replace each element in the first permutation with its corresponding index from the second permutation, producing a new array of positions.
3. Compute the length of the longest strictly increasing subsequence of this transformed array.
4. Maintain an array `dp` where `dp[i]` stores the smallest possible ending value of an increasing subsequence of length `i + 1`.
5. For each position value in the transformed array, use binary search to find where it fits in `dp`. If it extends the longest subsequence, append it; otherwise, replace the first element in `dp` that is greater than or equal to it.
6. The final length of `dp` is the answer.

The replacement step is the key idea that preserves flexibility. Even if we overwrite values in `dp`, we are only keeping the best possible tail for subsequences of a given length, not committing to a specific subsequence.

### Why it works

At any point, `dp[k]` represents the smallest possible ending position of an increasing subsequence of length `k + 1`. This invariant ensures that if a longer increasing subsequence exists, it can always be built on top of these minimal endings. Since we always replace with smaller valid candidates, we never lose the possibility of extending to an optimal solution, and we never artificially inflate subsequence length by using incompatible elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

from bisect import bisect_left

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, v in enumerate(b):
        pos[v] = i

    seq = [pos[v] for v in a]

    dp = []
    for x in seq:
        i = bisect_left(dp, x)
        if i == len(dp):
            dp.append(x)
        else:
            dp[i] = x

    print(len(dp))

if __name__ == "__main__":
    solve()
```

The first part of the code constructs a direct lookup table so that each value in the first permutation can be mapped to its position in the second permutation in constant time. This avoids repeated scanning.

The transformation step creates a single numeric sequence that encodes ordering constraints. Once this is done, the original problem structure disappears and we only reason about monotonicity.

The LIS computation uses a greedy strategy with binary search. The `dp` array does not store an actual subsequence, but maintains minimal possible endings for each length, which is sufficient to recover the correct length.

## Worked Examples

### Example 1

Input:

$A = [2, 3, 1, 4]$, $B = [1, 2, 3, 4]$

Positions in $B$:

$1 \to 0, 2 \to 1, 3 \to 2, 4 \to 3$

Transformed sequence:

$[1, 2, 0, 3]$

| Step | x | dp before | dp after | explanation |
| --- | --- | --- | --- | --- |
| 1 | 1 | [] | [1] | start new subsequence |
| 2 | 2 | [1] | [1, 2] | increasing extension |
| 3 | 0 | [1, 2] | [0, 2] | replace first element |
| 4 | 3 | [0, 2] | [0, 2, 3] | extend longest |

Final answer is 3.

This demonstrates how replacements allow recovery from earlier large values and still build a longer subsequence later.

### Example 2

Input:

$A = [1, 2, 3]$, $B = [3, 2, 1]$

Positions:

$3 \to 0, 2 \to 1, 1 \to 2$

Transformed:

$[2, 1, 0]$

| Step | x | dp before | dp after |
| --- | --- | --- | --- |
| 1 | 2 | [] | [2] |
| 2 | 1 | [2] | [1] |
| 3 | 0 | [1] | [0] |

Final answer is 1.

This shows the algorithm correctly handles completely reversed orderings where no increasing subsequence longer than 1 exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | each of $n$ elements does a binary search in LIS structure |
| Space | $O(n)$ | position map and transformed sequence |

The transformation and LIS computation both scale linearly or near-linearly, which fits comfortably within constraints up to $10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import log
    import sys
    input = sys.stdin.readline

    from bisect import bisect_left

    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        pos = [0] * (n + 1)
        for i, v in enumerate(b):
            pos[v] = i

        seq = [pos[v] for v in a]

        dp = []
        for x in seq:
            i = bisect_left(dp, x)
            if i == len(dp):
                dp.append(x)
            else:
                dp[i] = x

        print(len(dp))

    solve()
    return sys.stdout.getvalue().strip()

# sample-like tests
assert run("4\n2 3 1 4\n1 2 3 4") == "3"
assert run("3\n1 2 3\n3 2 1") == "1"

# custom tests
assert run("1\n1\n1") == "1", "single element"
assert run("5\n1 2 3 4 5\n1 2 3 4 5") == "5", "identical permutations"
assert run("5\n5 4 3 2 1\n1 2 3 4 5") == "1", "fully reversed"
assert run("6\n2 4 6 1 3 5\n1 2 3 4 5 6") == "3", "mixed ordering"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-element case | 1 | minimal boundary |
| identical permutations | n | full match correctness |
| reversed permutations | 1 | strict ordering failure |
| alternating structure | 3 | non-trivial LIS behavior |

## Edge Cases

A single-element permutation is the simplest sanity check. The algorithm constructs a position map of size one and produces a single-element LIS, since there is no alternative structure to compare against.

Identical permutations test whether the LIS implementation preserves full increasing structure without unnecessary replacements. Every element extends `dp`, so the length grows linearly to $n$, which matches the correct answer.

Reversed permutations stress the strict ordering requirement. Every new element is smaller than the previous in the transformed array, so the LIS structure keeps collapsing back to length one, demonstrating correct handling of non-increasing sequences.

Mixed patterns confirm that local decreases do not break global subsequence discovery. Even when elements are scattered, the replacement strategy ensures that earlier suboptimal tails do not block later valid extensions.
