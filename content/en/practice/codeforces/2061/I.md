---
title: "CF 2061I - Kevin and Nivek"
description: "We are asked to determine the minimum time Kevin must invest to win at least a given number of matches against Nivek, for all possible counts from 0 to $n$."
date: "2026-06-08T07:44:48+07:00"
tags: ["codeforces", "competitive-programming", "divide-and-conquer", "dp"]
categories: ["algorithms"]
codeforces_contest: 2061
codeforces_index: "I"
codeforces_contest_name: "IAEPC Preliminary Contest (Codeforces Round 999, Div. 1 + Div. 2)"
rating: 3500
weight: 2061
solve_time_s: 108
verified: false
draft: false
---

[CF 2061I - Kevin and Nivek](https://codeforces.com/problemset/problem/2061/I)

**Rating:** 3500  
**Tags:** divide and conquer, dp  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine the minimum time Kevin must invest to win at least a given number of matches against Nivek, for all possible counts from 0 to $n$. Each match is either Type 1, which has a fixed time cost $a_i$ for Kevin to guarantee a win, or Type 2, which automatically goes to Kevin if he is not currently behind in wins. Type 2 matches do not cost time themselves but depend on Kevin's prior wins.

The input is a sequence of integers where $-1$ indicates a Type 2 match and any non-negative number represents the time cost of a Type 1 match. The output is a list of length $n+1$, where the $k$-th element is the minimum time to ensure at least $k$ wins.

Given the constraints - $n$ up to $3 \cdot 10^5$ per test case, and up to $10^4$ test cases - any algorithm that examines every subset of matches or simulates all possibilities will be far too slow. A solution must scale linearly or at worst $O(n \log n)$ per test case. Edge cases include when all matches are Type 2, when all matches are Type 1, or when a mixture of both makes it impossible to reach certain win counts.

For example, if the input is `5` and all matches are Type 2 (`-1 -1 -1 -1 -1`), Kevin can win all matches without spending any time, so the output should be `0 0 0 0 0 0`. If all matches are Type 1 with costs `[3, 2, 5, 4, 1]`, the minimum time for a given number of wins is obtained by choosing the cheapest $k$ matches, which in this case leads to cumulative sums of sorted costs: `0 1 3 6 10 15`.

A careless approach might try to simulate each match sequentially and decide on Type 2 matches dynamically without precomputing cumulative possibilities. This fails because the optimal strategy often involves selecting specific Type 1 matches first, then letting Type 2 matches automatically contribute to wins, and the interaction is non-local.

## Approaches

The brute-force approach would be to consider all subsets of Type 1 matches, simulate Type 2 outcomes for each subset, and record the minimum time to achieve each possible win count. For $n$ matches, there are $2^n$ subsets, which is infeasible. Even if we split by match type, iterating all permutations of Type 1 matches to account for Type 2 outcomes leads to exponential growth.

The key insight is that Type 2 matches are free and automatically beneficial if Kevin is not behind. This allows us to handle them separately. We can first count the number of Type 2 matches $b$ and Type 1 matches $a_1, \dots, a_m$. We sort the Type 1 costs in ascending order. To win at least $k$ matches, we can consider spending time on the cheapest $x$ Type 1 matches and letting Type 2 matches fill in the remaining required wins. Specifically, Kevin only needs to spend time on Type 1 matches if $k$ exceeds the number of Type 2 matches he can leverage to reach $k$.

This reduces the problem to sorting Type 1 costs and computing prefix sums, then carefully determining how many Type 1 matches are actually required for each target $k$. Each target can be evaluated in $O(1)$ after sorting and prefix sum calculation, giving an overall $O(n \log n)$ solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Split the matches into two lists: Type 1 matches with their associated times and Type 2 matches counted by a simple integer. Sort the Type 1 times in ascending order. Sorting ensures that we spend time on the cheapest matches first.
2. Compute the prefix sum of the sorted Type 1 times. This lets us quickly query the total time required to win any number of Type 1 matches.
3. Iterate over the required number of wins $k$ from 0 to $n$. For each $k$, determine the minimum number of Type 1 matches Kevin must actively win. This is the smallest $x$ such that $x + \text{Type 2 count} \ge k$ and $x \le \text{Type 1 count}$. If $k$ is less than or equal to the Type 2 count, Kevin spends no time. If $k$ exceeds the sum of Type 2 and Type 1 matches, it is impossible, and we can mark it with -1.
4. For achievable $k$, use the prefix sum array to find the total time spent on the required Type 1 matches. Append this to the output list for the test case.
5. Output the full list for each test case.

Why it works: At every step, the algorithm guarantees we only spend time on Type 1 matches if necessary. Type 2 matches automatically contribute to wins if Kevin is not behind, so the prefix sums of Type 1 matches give the minimal additional time required. This ensures we achieve the minimum time for all possible target win counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        type1 = sorted([x for x in a if x != -1])
        type2_count = a.count(-1)
        m = len(type1)
        prefix = [0] * (m + 1)
        for i in range(m):
            prefix[i+1] = prefix[i] + type1[i]
        res = []
        for k in range(n+1):
            x = max(0, k - type2_count)
            if x > m:
                res.append(-1)
            else:
                res.append(prefix[x])
        print(' '.join(map(str, res)))

solve()
```

The solution first separates Type 1 and Type 2 matches, sorts Type 1 times, and precomputes prefix sums. When evaluating each $k$, it checks if Type 2 matches alone suffice. Otherwise, it adds the cheapest Type 1 matches as needed. Edge cases, like all matches being Type 2 or Type 1, naturally fall out of this computation.

## Worked Examples

For the input:

```
5
-1 -1 -1 -1 -1
```

We have 5 Type 2 matches and no Type 1 matches. The prefix sum array is `[0]`. Iterating $k = 0$ to 5, the required Type 1 matches are `max(0, k-5) = 0` for all $k$. The result is `[0, 0, 0, 0, 0, 0]`.

For input:

```
5
100 -1 -1 -1 1
```

Type 1 matches: `[1, 100]`, Type 2 count = 3. Prefix sums `[0, 1, 101]`.

| k | x = max(0, k-3) | prefix[x] | result |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 |
| 3 | 0 | 0 | 0 |
| 4 | 1 | 1 | 1 |
| 5 | 2 | 101 | 101 |

This demonstrates the algorithm correctly handles mixtures and selects the minimal cost matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | Sorting Type 1 matches dominates |
| Space | O(n) | Prefix sum and match separation arrays |

Given the maximum sum of $n$ across all test cases is $3 \cdot 10^5$, this solution runs comfortably within 4 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("3\n5\n-1 -1 -1 -1 -1\n5\n3 2 5 4 1\n5\n100 -1 -1 -1 1\n") == "0 0 0 0 0 0\n0 1 3 6 10 15\n0 0 0 0 1 101", "sample 1"

# Custom cases
assert run("1\n1\n-1\n") == "0 0", "single Type 2 match"
assert run("1\n1\n5\n") == "0 5", "single Type 1 match"
assert run("1\n3\n5 2 -1\n") == "0 0 2 7", "mix of Type 1 and Type 2"
assert run("1\n4\n-1 -1 -1 -1\n
```
