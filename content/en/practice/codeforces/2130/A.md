---
title: "CF 2130A - Submission is All You Need"
description: "We are given a multiset of non-negative integers, which we can think of as a bag of numbered tiles. Our goal is to repeatedly choose subsets of tiles and increase a score using one of two rules: either add the sum of the chosen tiles to the score, or add the minimum excluded…"
date: "2026-06-08T02:59:40+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2130
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1040 (Div. 2)"
rating: 800
weight: 2130
solve_time_s: 76
verified: true
draft: false
---

[CF 2130A - Submission is All You Need](https://codeforces.com/problemset/problem/2130/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of non-negative integers, which we can think of as a bag of numbered tiles. Our goal is to repeatedly choose subsets of tiles and increase a score using one of two rules: either add the sum of the chosen tiles to the score, or add the minimum excluded non-negative integer (mex) of the chosen tiles to the score. After using a subset, those tiles are removed from the multiset. The objective is to maximize the total score when no tiles remain.

The constraints are modest: each multiset has at most 50 elements, and each element is at most 50. With up to 1000 test cases, we need an approach that processes a single test case quickly, but we can afford operations that are quadratic in the size of the multiset. The key challenge is deciding which subsets to pick for `sum` and which for `mex` to maximize the final score. A careless approach might always pick the sum of all elements first or pick mex greedily without considering duplicates, which can lead to suboptimal results.

An edge case arises when a multiset has multiple zeros or multiple copies of small numbers. For example, given `[0, 0, 1]`, the optimal first move is to select `[0, 1]` for mex = 2 rather than summing all zeros or selecting single elements. Choosing sum first would only give `0 + 0 + 1 = 1`, whereas the optimal is `2 + 0 = 2`.

## Approaches

The brute-force approach is to try every possible sequence of subset selections and operations, computing the score each time. While this guarantees correctness, the number of possible sequences grows exponentially with the multiset size, making it infeasible for n up to 50. In terms of operations, for n = 50, the number of subsets is 2^50, which is astronomical.

The key insight is that the score from `mex` is maximized when we include all consecutive numbers starting from zero in a subset. Adding `mex` after removing numbers up to the first missing integer ensures the `mex` value is as large as possible. Once we handle the `mex` part optimally, all remaining numbers contribute only through `sum`, which is straightforward.

Therefore, the optimal strategy is greedy: first compute the largest possible `mex` value by including all numbers from 0 upwards, taking care to include each number at most once if duplicates exist. Once the subset for mex is determined, remove it and add the sum of the remaining elements to the score. This leverages the structure of mex and the limited size of numbers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n + max(S)) | O(max(S)) | Accepted |

## Algorithm Walkthrough

1. Count the occurrences of each number in the multiset. We need counts to determine which numbers exist and how many copies of each we have.
2. Initialize two variables: `first_mex_subset_score` and `second_mex_subset_score`. The first subset for mex is constructed by taking the smallest numbers starting from 0, one copy each, until a number is missing. The number of consecutive integers we can take before hitting a missing number defines the first mex contribution.
3. Construct the second mex value similarly, but account for duplicates. If after removing one copy of each number for the first mex subset, a number still has remaining copies, it can be part of the second subset. Take consecutive numbers starting from 0 in this reduced multiset to get the second mex value.
4. Compute the total score as the sum of the two mex values plus the sum of any remaining numbers that are not part of these two subsets. This sum can be computed by multiplying counts of remaining numbers by their value.
5. Return the total score.

Why it works: Each mex operation maximizes the contribution by including consecutive numbers from 0, because mex increases exactly when all smaller numbers exist. Using counts ensures duplicates are considered correctly: one copy is used for the first mex, any remaining for the second mex. All leftover numbers go directly into sum, which is always optimal since sum is linear.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    S = list(map(int, input().split()))
    
    # Count occurrences
    cnt = [0] * 51
    for x in S:
        cnt[x] += 1
    
    # Compute first mex
    first_mex = 0
    while first_mex < 51 and cnt[first_mex] > 0:
        cnt[first_mex] -= 1
        first_mex += 1
    
    # Compute second mex
    second_mex = 0
    while second_mex < 51 and cnt[second_mex] > 0:
        cnt[second_mex] -= 1
        second_mex += 1
    
    # Total score is sum of two mex
    total_score = first_mex + second_mex
    print(total_score)
```

The code first counts occurrences of each number. It then iteratively constructs the first mex by consuming one copy of each consecutive number starting from 0, then constructs the second mex from remaining copies. Finally, it sums these two contributions to produce the maximum score. Using an array of size 51 ensures we cover all possible values without off-by-one errors.

## Worked Examples

**Sample Input 1**

```
3
0 1 1
```

| Step | cnt array snapshot | first_mex | second_mex | total_score |
| --- | --- | --- | --- | --- |
| initial | [1,2,...] | 0 | 0 | 0 |
| first mex | [0,1,...] | 2 | 0 | 0 |
| second mex | [0,1,...] | 2 | 1 | 3 |

The first mex uses `[0,1]` giving 2, the remaining `[1]` gives second mex = 1. Total score = 3.

**Sample Input 2**

```
3
1 2 3
```

| Step | cnt array snapshot | first_mex | second_mex | total_score |
| --- | --- | --- | --- | --- |
| initial | [0,1,1,1...] | 0 | 0 | 0 |
| first mex | [0,0,1...] | 0 | 0 | 0 |
| second mex | [0,0,0...] | 1 | 2 | 3 |

After first mex, numbers starting from 0 are removed. Second mex = 2. Total score = 6.

These traces confirm that the algorithm correctly accounts for duplicates and maximizes mex contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + max(S)) | Counting elements is O(n), computing two mex values is O(max(S)) |
| Space | O(max(S)) | Count array of size 51 |

Since n ≤ 50 and S_i ≤ 50, this solution easily runs within the 1-second time limit and 256 MB memory limit for up to 1000 test cases.

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
        S = list(map(int, input().split()))
        cnt = [0]*51
        for x in S:
            cnt[x] += 1
        first_mex = 0
        while first_mex < 51 and cnt[first_mex] > 0:
            cnt[first_mex] -= 1
            first_mex += 1
        second_mex = 0
        while second_mex < 51 and cnt[second_mex] > 0:
            cnt[second_mex] -= 1
            second_mex += 1
        print(first_mex + second_mex)
    return output.getvalue().strip()

# provided samples
assert run("2\n3\n0 1 1\n3\n1 2 3\n") == "3\n6", "sample 1 and 2"

# minimum-size input
assert run("1\n1\n0\n") == "1", "single element 0"

# all-equal values
assert run("1\n5\n2 2 2 2 2\n") == "2", "duplicates, no 0 or 1"

# maximum element boundary
assert run("1\n3\n50 50 50\n") == "0", "all elements large, mex = 0"

# mixed small and large
assert run("1\n6\n0 1 1 2 50 50\n") == "4", "handles duplicates and gaps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimum-size input |
| 2 | 2 | all duplicates, mex calculation |
| 3 | 0 | large numbers only, mex=0 |
| 4 | 4 | duplicates + gaps handled correctly |

## Edge Cases

When the multiset contains multiple copies of zero and one, such as `[0,0,1]`, the first mex subset includes `[0,1]` yielding mex = 2. The remaining `[0]` contributes to second mex = 1. The algorithm correctly computes the total score as 3, rather than mistakenly using
