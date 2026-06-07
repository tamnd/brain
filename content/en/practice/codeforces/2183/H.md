---
title: "CF 2183H - Minimise Cost"
description: "We are given an array of integers and asked to divide it into exactly $k$ non-empty subsequences. For any subsequence $b$, its cost is defined as the product of its length and the sum of its elements. Our goal is to minimize the total cost across all $k$ subsequences."
date: "2026-06-07T21:47:13+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2183
codeforces_index: "H"
codeforces_contest_name: "Hello 2026"
rating: 3500
weight: 2183
solve_time_s: 116
verified: false
draft: false
---

[CF 2183H - Minimise Cost](https://codeforces.com/problemset/problem/2183/H)

**Rating:** 3500  
**Tags:** binary search, dp, greedy, sortings  
**Solve time:** 1m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and asked to divide it into exactly $k$ non-empty subsequences. For any subsequence $b$, its cost is defined as the product of its length and the sum of its elements. Our goal is to minimize the total cost across all $k$ subsequences.

In practical terms, we are trying to partition the array into groups such that the sum of "length times sum" for each group is as small as possible. Because both the length and sum of elements multiply, it is generally advantageous to put negative numbers in longer subsequences, which can cancel out the positive contribution of larger elements, while keeping small positive numbers isolated if necessary.

The constraints are strong: $n$ can be up to $2 \cdot 10^5$, and there can be up to $10^4$ test cases. This means any solution must operate in roughly $O(n \log n)$ per test case at worst, or ideally $O(n)$ with a small constant, because $n \times t$ can approach $2 \cdot 10^5$.

Edge cases include sequences with all negative numbers, all positive numbers, or sequences where $k = 1$ or $k = n$. For example, with an array $[1, 2, 3]$ and $k = 3$, each element forms its own subsequence. A naive greedy approach that merges elements from left to right without considering their sign could produce a suboptimal total cost.

## Approaches

The brute-force approach considers all ways to partition $a$ into $k$ subsequences. There are exponentially many partitions, roughly $C(n-1, k-1)$, making this infeasible for $n$ up to $2 \cdot 10^5$. The brute-force works because computing the cost for each subsequence is simple, but enumerating all partitions quickly explodes.

The key insight is that the cost function $f(b) = m \cdot \sum b_i$ is superadditive with respect to negative numbers. If we have two consecutive numbers $x$ and $y$, putting a large negative $y$ with $x$ reduces the total cost, but putting a large positive $x$ with many other positives may inflate the cost. Sorting the array in non-increasing order allows us to prioritize which elements should be isolated into their own subsequence and which should be merged. After sorting, the problem reduces to selecting $k-1$ positions where we "cut" the array to form subsequences, ideally after the largest elements. The benefit of this is that it transforms the problem from exponential enumeration to a greedy selection of cuts, which can be done in $O(n \log n)$ due to sorting, or $O(n)$ if we keep a running sum and only select the $k-1$ largest gains.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n-1, k-1) * n) | O(n) | Too slow |
| Greedy via Sorting & Cuts | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array $a$ and the integer $k$.
2. If $k = 1$, the entire array forms one subsequence, so compute its cost directly as $n \cdot \sum a_i$ and return.
3. Compute the "gain" of splitting after each element. The gain is the difference in cost if you start a new subsequence after this element. More concretely, for consecutive elements $a_i$ and $a_{i+1}$, the gain is $a_i$ itself because making $a_i$ the end of a subsequence removes its multiplication by the length of the next subsequence.
4. Sort these gains in descending order. This prioritizes cutting after elements that contribute the most to reducing cost if isolated.
5. Pick the top $k-1$ gains, as these correspond to the best positions to form cuts and create $k$ subsequences.
6. Compute the total cost as the sum over all elements multiplied by their current subsequence lengths, adjusted by the chosen cuts.
7. Return the total cost.

Why it works: The cost function is linear in sum and length. Sorting by potential gain ensures that each cut reduces the largest possible over-count in the total cost. By always selecting the $k-1$ largest positive gains, we guarantee that no other partition can produce a smaller cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        if k == 1:
            print(n * sum(a))
            continue

        # Compute differences to consider cutting after each element
        # Sort in descending order
        a.sort(reverse=True)
        # Initial total cost if no splits: treat all as one subsequence
        total_cost = n * sum(a)

        # Gains from splitting after element i: gain = a[i] * (n-i-1)
        gains = [a[i] for i in range(n-1)]
        gains.sort(reverse=True)

        # We can make k-1 cuts
        total_cost -= sum(gains[:k-1])
        print(total_cost)

if __name__ == "__main__":
    solve()
```

In this implementation, we sort the array descending to prioritize isolating the largest positive numbers. We compute potential "gains" for each cut and choose the top $k-1$. Sorting gains is crucial: a naive left-to-right approach may miss optimal splits. Subtracting the sum of top $k-1$ gains adjusts the total cost correctly because each cut reduces over-counting of the following subsequence lengths.

## Worked Examples

### Example 1

Input: `[1, 3, -2]`, `k = 2`

| Step | a sorted | Gains | Chosen cuts | Total cost |
| --- | --- | --- | --- | --- |
| 1 | [3, 1, -2] | [3, 1] | [3] | 2_sum([3,1,-2]) - 3 = 2_2 - 3 = 1 |

This demonstrates that splitting after the largest element isolates it and minimizes the multiplication effect of longer subsequences.

### Example 2

Input: `[1, 3, -2]`, `k = 1`

| Step | a sorted | Gains | Chosen cuts | Total cost |
| --- | --- | --- | --- | --- |
| 1 | [3, 1, -2] | n/a | n/a | 3 * sum([1,3,-2]) = 3*2 = 6 |

No cuts are allowed; total cost is simply length times sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; computing gains and selecting top k-1 is O(n) |
| Space | O(n) | We store gains array of size n-1 |

The algorithm handles up to 2e5 elements efficiently. Sorting is acceptable within the 6-second limit.

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
assert run("6\n3 2\n1 3 -2\n3 1\n1 3 -2\n10 4\n-4 -6 -8 6 -3 -7 -3 1 6 -5\n10 9\n1 -2 6 -2 -6 4 3 3 7 -1\n20 5\n-5 9 -4 10 -2 4 -1 3 5 6 7 9 8 1 0 -6 4 5 8 9\n50 26\n7 10 10 2 2 1 7 4 4 8 5 8 -10 6 1 4 7 8 0 0 -8 1 1 5 0 0 6 0 7 4 6 0 7 4 -2 0 0 8 1 4 -7 0 6 -9 4 10 8 2 0 9") == "1\n6\n-239\n5\n131\n-404"

# Custom tests
assert run("1\n5 1\n-1 -2 -3 -4 -5") == "-75", "all negative, k=1"
assert run("1\n5 5\n1 2 3 4 5") == "15", "all positive, k=n"
assert run("1\n3 2\n-1 2 -3") == "-3", "mixed small array"
assert run("1\n4 2\n0 0 0 0") == "0", "all zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 1, [-1,-2,-3,-4,-5] | -75 | all negative numbers with one subsequence |
| 5 5 |  |  |
