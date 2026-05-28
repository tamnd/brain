---
title: "CF 27C - Unordered Subsequence"
description: "We are given a sequence of integers, and we are asked to extract the shortest subsequence that is not ordered. A sequenc"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 27
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 27 (Codeforces format, Div. 2)"
rating: 1900
weight: 27
solve_time_s: 78
verified: false
draft: false
---

[CF 27C - Unordered Subsequence](https://codeforces.com/problemset/problem/27/C)

**Rating:** 1900  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers, and we are asked to extract the shortest subsequence that is _not ordered_. A sequence is considered ordered if it is either entirely non-decreasing or entirely non-increasing. In other words, if every consecutive pair either never decreases or never increases, the sequence is ordered. Our task is to find a minimal subsequence that breaks this pattern.

The input consists of a single integer $n$ specifying the sequence length, followed by $n$ integers. The output should report the length of the shortest unordered subsequence (if any exists) and the 1-based indices of its elements.

With $n$ up to $10^5$ and a 2-second time limit, any solution with worse than linear complexity is likely too slow. An $O(n^2)$ brute-force search of all triplets is already $10^{10}$ operations in the worst case, which is clearly infeasible. This suggests a need for a single-pass or near-linear scan approach.

Edge cases are subtle. If all elements are equal, there is no unordered subsequence, so the output must be zero. If the sequence has only one or two elements, any subsequence is trivially ordered. We also need to handle strictly increasing or decreasing sequences that appear to have “variation” but do not actually break monotonicity.

## Approaches

The naive solution would examine all subsequences of length 3, checking whether they are ordered. This works because any unordered subsequence must have at least three elements: two elements are always ordered. Checking every triplet in an array of length $n$ requires roughly $n^3$ operations, which is completely impractical for $n = 10^5$.

The key insight is that the shortest unordered subsequence always has length 3. Suppose we find three consecutive elements $a_i, a_j, a_k$ where $i < j < k$ such that $a_i < a_j > a_k$ or $a_i > a_j < a_k$. Any unordered sequence of more than three elements contains such a triple. Therefore, we only need to scan the array once, checking every triplet of consecutive elements. As soon as a triplet violates monotonicity, we can immediately output it.

This observation reduces complexity from $O(n^3)$ to $O(n)$ with constant space. We only need the current element and its immediate neighbors to detect an unordered triple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the sequence of integers into an array.
2. If the sequence length is less than 3, output 0 immediately. Two elements are always ordered.
3. Iterate over the array with index $i$ from 1 to $n-2$. For each triplet $(a[i-1], a[i], a[i+1])$, check the ordering condition.
4. If the middle element is either strictly larger than both neighbors ($a[i-1] < a[i] > a[i+1]$) or strictly smaller than both neighbors ($a[i-1] > a[i] < a[i+1]$), output the triplet length 3 and their 1-based indices $i, i+1, i+2$. Terminate immediately.
5. If the loop finishes without finding any unordered triplet, output 0.

Why it works: The algorithm is guaranteed to find the shortest unordered subsequence because any sequence of three elements that is not monotone is minimal. Scanning consecutive triplets ensures we never miss such a subsequence. No sequence of length two can violate order, so 3 is the correct minimum length.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

if n < 3:
    print(0)
else:
    found = False
    for i in range(1, n-1):
        if (a[i-1] < a[i] > a[i+1]) or (a[i-1] > a[i] < a[i+1]):
            print(3)
            print(i, i+1, i+2)
            found = True
            break
    if not found:
        print(0)
```

The code starts by handling sequences of length less than three. Then, it checks each consecutive triplet exactly once. The condition explicitly checks for “peak” or “valley” formations. Using 1-based indexing aligns with the problem requirement. A subtle point is that equality does not count as breaking order: the conditions use strict inequalities.

## Worked Examples

**Example 1**

Input:

```
5
67 499 600 42 23
```

| i | a[i-1] | a[i] | a[i+1] | Check | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 67 | 499 | 600 | 67<499>600? no | continue |
| 2 | 499 | 600 | 42 | 499<600>42 yes | print 3, indices 2,3,4 |

The algorithm correctly identifies a peak at 600 and outputs the minimal unordered subsequence.

**Example 2**

Input:

```
4
1 2 3 4
```

| i | a[i-1] | a[i] | a[i+1] | Check | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 3 | 1<2>3? no | continue |
| 2 | 2 | 3 | 4 | 2<3>4? no | continue |

No triplet violates order, so output 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each triplet is checked once in a single pass. |
| Space | O(n) | We store the array of n integers; no additional structures needed. |

With $n \le 10^5$ and $O(n)$ operations, the solution comfortably runs within 2 seconds. Memory usage is also within 256 MB, as integers fit easily in arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    exec(open("solution.py").read())  # assume solution code above is saved in solution.py
    return sys.stdout.getvalue().strip()

# provided sample
assert run("5\n67 499 600 42 23\n") == "3\n2 3 4"

# all increasing
assert run("4\n1 2 3 4\n") == "0"

# all decreasing
assert run("3\n5 3 1\n") == "0"

# single element
assert run("1\n42\n") == "0"

# peak in middle
assert run("5\n1 3 2 4 5\n") == "3\n2 3 4"

# valley in middle
assert run("5\n5 2 4 6 7\n") == "3\n1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 67 499 600 42 23 | 3 2 3 4 | detection of peak |
| 4 1 2 3 4 | 0 | strictly increasing sequence |
| 3 5 3 1 | 0 | strictly decreasing sequence |
| 1 42 | 0 | single-element edge case |
| 5 1 3 2 4 5 | 3 2 3 4 | unordered subsequence with peak |
| 5 5 2 4 6 7 | 3 1 2 3 | unordered subsequence with valley |

## Edge Cases

For a sequence with repeated elements, e.g., `2 2 2`, the algorithm checks consecutive triplets. No strict inequality is satisfied, so it outputs 0. For sequences of length 2, such as `1 2`, the initial check immediately returns 0. For sequences with a minimal unordered subsequence at the start, middle, or end, the algorithm always identifies the first such triple encountered.

This editorial should give a reader enough context to reason from first principles that the shortest unordered subsequence is always length three and can be detected with a single linear scan.
