---
title: "CF 1469B - Red and Blue"
description: "We are given two sequences of integers, one representing red-painted elements and the other representing blue-painted elements of an original sequence."
date: "2026-06-11T01:08:42+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1469
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 101 (Rated for Div. 2)"
rating: 1000
weight: 1469
solve_time_s: 110
verified: true
draft: false
---

[CF 1469B - Red and Blue](https://codeforces.com/problemset/problem/1469/B)

**Rating:** 1000  
**Tags:** dp, greedy  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences of integers, one representing red-painted elements and the other representing blue-painted elements of an original sequence. The order within each color is preserved, but we do not know how to interleave red and blue elements to reconstruct the original sequence. The task is to find an ordering of these two subsequences that maximizes the largest prefix sum, where the prefix sum is defined as the sum of the first element, the sum of the first two elements, and so on. We only care about the maximum among these sums and zero.

The input sizes are small, with each color sequence containing at most 100 elements and up to 1000 test cases. This means an O(n + m) solution per test case is acceptable, but any algorithm that tries all possible interleavings would be infeasible because the number of interleavings is combinatorial and can be extremely large.

A subtle edge case is when all elements are negative. In that case, the maximum prefix sum is zero, because taking any element would decrease the sum. Another is when one sequence has all negative values and the other has positive values. The algorithm must be careful to possibly skip negative prefixes entirely.

## Approaches

The brute-force approach would attempt to generate every valid interleaving of the red and blue sequences and compute the maximum prefix sum for each. Since a sequence of length $n + m$ has $\binom{n+m}{n}$ interleavings, even the largest constraints (n = m = 100) make this approach completely impractical, as it would require $10^{58}$ computations.

The key insight is that the maximum prefix sum depends only on the sum of prefixes within each color sequence independently. Since we can place all elements of one color before elements of the other, we only need to consider taking the best prefix sum of the red sequence and the best prefix sum of the blue sequence separately. Placing the prefix with the largest positive sum first does not hurt, and the sums are additive. Therefore, the solution reduces to computing the maximum prefix sum of the red sequence, the maximum prefix sum of the blue sequence, and summing them, but ensuring we do not take negative contributions (we use max with zero).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n+m)) | O(n+m) | Too slow |
| Optimal | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `max_red` and `max_blue` to zero. These will store the maximum prefix sums for the red and blue sequences, respectively.
2. Iterate over the red sequence. Maintain a running sum. After adding each element, update `max_red` if the running sum exceeds it. This finds the largest sum obtainable by taking a prefix of the red sequence.
3. Repeat step 2 for the blue sequence, storing the result in `max_blue`.
4. The maximum possible value of `f(a)` is `max_red + max_blue`. Both prefix sums contribute positively if they are positive; negative sums are ignored.

The reason this works is that adding any additional elements after the maximum prefix sum of one sequence cannot increase the maximum beyond the sum of the best red and blue prefixes. The ordering within the color is fixed, so the only decision is how to interleave sequences. By taking the maximum positive contribution from each independently, we guarantee the global maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    r = list(map(int, input().split()))
    m = int(input())
    b = list(map(int, input().split()))
    
    max_red = max_blue = 0
    curr_sum = 0
    for val in r:
        curr_sum += val
        if curr_sum > max_red:
            max_red = curr_sum
    
    curr_sum = 0
    for val in b:
        curr_sum += val
        if curr_sum > max_blue:
            max_blue = curr_sum
    
    print(max_red + max_blue)
```

The solution reads input efficiently using `sys.stdin.readline`. For each sequence, we maintain a running sum and update the maximum prefix sum, ensuring that negative prefixes do not reduce the result. The sum of the best red prefix and the best blue prefix gives the answer for each test case. Care must be taken to reset the running sum before processing the blue sequence.

## Worked Examples

**Example 1**

Red: [6, -5, 7, -3]

Blue: [2, 3, -4]

| Step | Running Sum Red | Max Red | Running Sum Blue | Max Blue |
| --- | --- | --- | --- | --- |
| 1 | 6 | 6 | 2 | 2 |
| 2 | 1 | 6 | 5 | 5 |
| 3 | 8 | 8 | 1 | 5 |
| 4 | 5 | 8 | -3 | 5 |

Max prefix sum red = 8

Max prefix sum blue = 5

Total = 13

**Example 2**

Red: [1, 1]

Blue: [10, -3, 2, 2]

| Step | Running Sum Red | Max Red | Running Sum Blue | Max Blue |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 10 | 10 |
| 2 | 2 | 2 | 7 | 10 |

Max prefix sum red = 2

Max prefix sum blue = 10

Total = 12

These traces confirm that the algorithm correctly accumulates positive contributions while ignoring sequences that would reduce the sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | Each element is visited exactly once to compute the running sum |
| Space | O(1) extra | Only running sums and max values are stored; input arrays are given |

With up to 1000 test cases, the total number of operations is at most $1000 \times (100 + 100) = 2 \times 10^5$, which easily fits in the 2-second time limit. Memory usage is negligible compared to the 512 MB limit.

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
        r = list(map(int, input().split()))
        m = int(input())
        b = list(map(int, input().split()))
        
        max_red = max_blue = 0
        curr_sum = 0
        for val in r:
            curr_sum += val
            max_red = max(max_red, curr_sum)
        
        curr_sum = 0
        for val in b:
            curr_sum += val
            max_blue = max(max_blue, curr_sum)
        
        print(max_red + max_blue)
    
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("4\n4\n6 -5 7 -3\n3\n2 3 -4\n2\n1 1\n4\n10 -3 2 2\n5\n-1 -2 -3 -4 -5\n1\n0\n1\n0\n") == "13\n13\n0\n0", "samples"

# Custom cases
assert run("1\n1\n-10\n1\n-5\n") == "0", "all negative"
assert run("1\n3\n1 2 3\n2\n-1 -2\n") == "6", "positive and negative mix"
assert run("1\n5\n0 0 0 0 0\n5\n1 1 1 1 1\n") == "5", "zeros and positives"
assert run("1\n1\n100\n1\n100\n") == "200", "single large positives"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 -10 -5 | 0 | all negative numbers produce zero |
| 3 1 2 3 -1 -2 | 6 | positive contributions from red and blue sums |
| 5 zeros, 5 ones | 5 | ignores zero contribution correctly |
| 1 100, 1 100 | 200 | handles large single-element positive sums correctly |

## Edge Cases

When all elements are negative, for example red = [-10], blue = [-5], the running sums never exceed zero. The algorithm initializes `max_red` and `max_blue` as zero, so the final output is correctly 0. This avoids erroneously selecting a negative prefix.

When sequences contain zeros, these do not decrease the sum, so they are included naturally if beneficial. For example, red = [0, 0], blue = [1, 2], max_red = 0, max_blue = 3, total = 3, which matches the optimal interleaving.
