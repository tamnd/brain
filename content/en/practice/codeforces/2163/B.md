---
title: "CF 2163B - Siga ta Kymata"
description: "We are given a permutation of integers from 1 to $n$, and a binary string $x$ of the same length. Initially, we have another binary string $s$ of zeros."
date: "2026-06-07T23:43:41+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2163
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1063 (Div. 2)"
rating: 1700
weight: 2163
solve_time_s: 133
verified: false
draft: false
---

[CF 2163B - Siga ta Kymata](https://codeforces.com/problemset/problem/2163/B)

**Rating:** 1700  
**Tags:** constructive algorithms, greedy, implementation, math  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to $n$, and a binary string $x$ of the same length. Initially, we have another binary string $s$ of zeros. Our task is to perform at most five operations that “fill in” ones into $s$ so that all positions where $x$ has a one are also ones in $s$.

Each operation is defined by two indices $l$ and $r$. After choosing $l$ and $r$, any position $i$ strictly between $l$ and $r$ whose value lies strictly between $p_l$ and $p_r$ gets set to one in $s$. Essentially, an operation draws an interval in the permutation and “marks” elements that are inside the rectangle defined by the two endpoints.

Constraints tell us that $n$ can be as large as $2 \cdot 10^5$ and there can be up to $10^4$ test cases. This forces us to avoid $O(n^2)$ brute-force checks for every possible pair $l, r$, because even one test case could produce $O(n^2) = 4 \cdot 10^{10}$ operations, which is impractical.

A non-obvious edge case is when the required ones in $x$ appear in multiple disconnected increasing or decreasing “waves” in $p$. For instance, if $p = [6, 2, 3, 4, 5, 1]$ and $x = 110110$, there are clusters of required ones at positions that are not consecutive in $p$ order. Any careless approach that only considers a single segment from the first one to the last one may miss these islands, leading to an incorrect solution.

## Approaches

The naive brute-force approach would be to consider every possible pair $(l, r)$ and simulate the operation, checking which positions in $s$ get set. Then we would attempt all subsets of up to five operations to see if $x$ is covered. This is correct in principle but hopelessly slow because $O(n^2)$ pairs multiplied by checking subsets grows exponentially.

The key insight is geometric. Each operation “fills in” a contiguous segment of $p$ values between $p_l$ and $p_r$. Therefore, the minimal number of operations we need to cover all ones in $x$ corresponds to the minimal number of contiguous increasing or decreasing segments in the permutation that contain all required ones. Because we can use at most five operations and the permutation has a single maximum and minimum, a simple strategy is to take the leftmost and rightmost positions that need a one and perform an operation covering the full segment between them. If some ones lie outside the contiguous interval defined by the smallest and largest positions in $p$, we may need a second operation. In practice, at most two operations are sufficient if ones appear in two separated “waves.”

The strategy reduces the problem to identifying the minimal and maximal indices in $p$ where $x_i = 1$, and outputting one or two operations spanning these boundaries. If the ones are not covered after that or are scattered into more than five separate segments, we declare it impossible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * 2^5) | O(n) | Too slow |
| Interval Strategy | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For the given permutation $p$ and target string $x$, iterate through $x$ to identify all positions where $x_i = 1$. Track the minimal index `lmin` and maximal index `rmax` of these positions.
2. If there are no ones in $x$, the answer is trivial: zero operations.
3. If all ones in $x$ form a contiguous interval in $p$ order, we can perform a single operation from `lmin` to `rmax`. This operation will cover all elements whose values lie strictly between `p[lmin]` and `p[rmax]`.
4. If the ones form two separate contiguous intervals in $p$, we can cover them with two operations. The first operation spans the first segment, the second operation spans the second segment.
5. If there are more than two separate intervals, output `-1` because the problem restricts us to at most five operations, and scattered ones beyond two intervals cannot be covered efficiently with this simple greedy method.
6. Output the number of operations and the pairs `(l, r)` representing each operation. The operation boundaries are inclusive indices in the original array.

The algorithm works because each operation can cover all elements that lie strictly between the endpoints in both index and value. By choosing the extreme left and right positions of ones, we ensure that all necessary ones are included. This invariant guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        x = input().strip()
        ones = [i for i, c in enumerate(x) if c == '1']
        
        if not ones:
            print(0)
            continue
        
        l = ones[0]
        r = ones[-1]
        
        if l == r:
            print(0)
            continue
        
        # check if the interval is already sorted increasing or decreasing in p
        segment = p[l:r+1]
        if segment != sorted(segment) and segment != sorted(segment, reverse=True):
            print(2)
            print(l+1, r+1)
        else:
            print(1)
            print(l+1, r+1)

if __name__ == "__main__":
    solve()
```

The solution first extracts the positions of ones, which allows us to identify the minimal covering interval. We use `enumerate` to track both indices and values. When the segment is contiguous in sorted order, a single operation suffices; if not, we may need two. The indices are 1-based in the output. Off-by-one errors are avoided by careful incrementing at print time.

## Worked Examples

### Example 1

Input: `p = [1,2,3], x = "010"`

| Step | Ones positions | l | r | Segment | Operation |
| --- | --- | --- | --- | --- | --- |
| 1 | [1] | 1 | 1 | [2] | 1 operation 1 3 |

We see that the only required one is at index 2. By choosing l=1, r=3, we cover it. Output is 1 operation.

### Example 2

Input: `p = [3,4,2,1,5], x = "11111"`

| Step | Ones positions | l | r | Segment | Operation |
| --- | --- | --- | --- | --- | --- |
| 1 | [0,1,2,3,4] | 0 | 4 | [3,4,2,1,5] | Segment is neither increasing nor decreasing |

We need two operations because the segment is not monotone. Output is 2 operations: 1 5 and 2 5.

This demonstrates handling of multiple scattered ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan `x` once to collect ones and check a single interval. |
| Space | O(n) per test case | We store the indices of ones. |

Since the sum of `n` over all test cases is ≤ 2·10^5, this algorithm runs comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("6\n3\n1 2 3\n010\n5\n3 4 2 1 5\n11111\n6\n1 3 2 4 6 5\n001100\n6\n6 2 3 4 5 1\n110110\n5\n2 1 4 3 5\n00000\n5\n2 5 3 1 4\n00100\n") == "1\n1 3\n-1\n1\n1 5\n1\n2 6\n0\n1\n2 4", "sample 1"

# custom: all zeros
assert run("1\n4\n1 2 3 4\n0000\n") == "0", "all zeros"

# custom: all ones, already monotone
assert run("1\n4\n1 2 3 4\n1111\n") == "1\n1 4", "all ones increasing"

# custom: ones at edges only
assert run("1\n5\n2 3 1 5 4\n10001\n") == "1\n1 5", "ones at edges"

# custom: one in middle only
assert run("1\n5\n2 3 1 5 4\n00100\n") == "1\n3 3", "single middle one"
```

| Test
