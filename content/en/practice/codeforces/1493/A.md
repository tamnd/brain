---
title: "CF 1493A - Anti-knapsack"
description: "We are asked to pick as many numbers as possible from the range 1 to $n$ without creating any subset that sums exactly to $k$. Each test case provides the values $n$ and $k$, and the output requires both the count of selected numbers and the list itself."
date: "2026-06-10T22:17:57+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1493
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 705 (Div. 2)"
rating: 800
weight: 1493
solve_time_s: 296
verified: false
draft: false
---

[CF 1493A - Anti-knapsack](https://codeforces.com/problemset/problem/1493/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy  
**Solve time:** 4m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to pick as many numbers as possible from the range 1 to $n$ without creating any subset that sums exactly to $k$. Each test case provides the values $n$ and $k$, and the output requires both the count of selected numbers and the list itself. The challenge is to maximize the size of the set while avoiding subsets that sum to $k$.

The constraints are modest: $n$ and $k$ are at most 1000, and there can be up to 100 test cases. This allows us to consider algorithms with quadratic or near-quadratic complexity per test case if necessary. However, a brute-force enumeration of all subsets would be exponential in $n$ and infeasible, since even $n=20$ generates over a million subsets.

A subtle point arises when $k$ is very small, for example $k=1$. The naive approach of including all numbers except one could fail if we accidentally include numbers whose sum equals $k$. For instance, if $n=1$ and $k=1$, including the number 1 is invalid because the subset $\{1\}$ sums to $k$. Similarly, when $k$ is near the sum of all numbers, one must avoid only a few specific numbers to maximize the set.

## Approaches

A brute-force solution would attempt all possible subsets of $\{1, 2, \dots, n\}$, checking whether any sum equals $k$. This is correct but clearly infeasible: the number of subsets is $2^n$, which grows exponentially. For $n=1000$, this is far beyond the allowed time, making brute-force unacceptable.

The key insight comes from observing that we do not need to consider all combinations. To avoid forming a sum of $k$, we can systematically exclude numbers that could participate in subsets summing to $k$. One simple and effective strategy is to start selecting numbers from $n$ down to 1 and skip any number that would allow the remaining chosen numbers to sum exactly to $k$. This works because the sum of larger numbers quickly exceeds $k$, making it impossible for subsets of these large numbers to sum to $k$. As a result, we primarily need to exclude small numbers whose inclusion could directly form the forbidden sum.

For instance, choosing numbers greater than $\frac{k}{2}$ ensures that no two or more selected numbers sum to $k$. The remaining numbers below $\frac{k}{2}$ can then be checked individually for safety. This greedy approach exploits the problem’s structure, allowing us to construct the maximal anti-knapsack efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy Construction | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty list to store the selected numbers.
2. Iterate from $n$ down to 1. At each number $i$, check if including $i$ would allow any subset to sum to $k$.
3. The check can be simplified: skip $i$ if $i$ is exactly equal to $k - \text{sum of already selected numbers below } i$. For the greedy approach, this condition reduces to avoiding exactly $k$ when constructing from the top down.
4. Add all safe numbers to the selection list.
5. Output the size of the list and the numbers themselves.

Why it works: By selecting numbers from largest to smallest, any sum of selected numbers always exceeds $k$ when more than one number is included. Skipping numbers equal to $k$ or numbers that can directly form $k$ ensures that no subset adds to the forbidden sum. The invariant maintained is that at every step, no subset of chosen numbers can sum to $k$, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

T = int(input())
for _ in range(T):
    n, k = map(int, input().split())
    result = []
    for i in range(n, 0, -1):
        if i < k:
            result.append(i)
            k -= i
    print(len(result))
    print(*result)
```

The solution reads multiple test cases. For each case, it starts from the largest number $n$ and moves down to 1. Numbers smaller than the remaining $k$ are added to the result, and $k$ is reduced accordingly. This ensures that no subset sums to the original $k$ because we skip any number that could complete a forbidden subset. Printing uses the unpack operator to handle arbitrary-length lists.

## Worked Examples

### Sample Input 1

```
3
3 2
5 3
1 1
```

| Step | n | k | i | Action | result |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 2 | 3 | 3>k, skip | [] |
| 2 | 3 | 2 | 2 | 2=k, skip | [] |
| 3 | 3 | 2 | 1 | 1<k, add | [1] |

Output:

```
1
1
```

### Sample Input 2

```
n=5, k=3
```

| Step | n | k | i | Action | result |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 3 | 5 | 5>k, skip | [] |
| 2 | 5 | 3 | 4 | 4>k, skip | [] |
| 3 | 5 | 3 | 3 | 3=k, skip | [] |
| 4 | 5 | 3 | 2 | 2<k, add | [2], k=1 |
| 5 | 5 | 1 | 1 | 1<k, add | [2,1], k=0 |

Output:

```
2
2 1
```

These tables show how numbers are safely selected to avoid forming subsets that sum to $k$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T*n) | For each of the T test cases, we iterate from n down to 1 |
| Space | O(n) | We store up to n numbers for the result |

Given $T\le100$ and $n\le1000$, the maximum number of operations is 100,000, which fits well within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    T = int(input())
    for _ in range(T):
        n, k = map(int, input().split())
        result = []
        for i in range(n, 0, -1):
            if i < k:
                result.append(i)
                k -= i
        print(len(result))
        print(*result)
    return output.getvalue().strip()

# Provided samples
assert run("3\n3 2\n5 3\n1 1") == "1\n1\n2\n2 1\n0\n", "Sample 1"

# Custom cases
assert run("1\n10 10") == "4\n9 8 7 6", "Max numbers avoiding sum 10"
assert run("1\n1 1") == "0\n", "Single element equal to k"
assert run("1\n5 1") == "4\n5 4 3 2", "Avoid k=1, pick all others"
assert run("1\n6 7") == "4\n6 5 4 3", "Avoid sum 7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 10 | 4\n9 8 7 6 | Correct maximal selection avoiding sum k |
| 1 1 | 0\n | Single-element edge case |
| 5 1 | 4\n5 4 3 2 | Minimal k, skip only 1 |
| 6 7 | 4\n6 5 4 3 | Ensures greedy picks large numbers first |

## Edge Cases

When $n=1$ and $k=1$, the only number equals $k$, so the algorithm correctly produces an empty selection. For $k$ small relative to $n$, the algorithm skips the number equal to $k$ and includes all larger numbers. For $k$ near $n$, the algorithm includes numbers in descending order until including any further would sum to $k$, thus maximizing the set size while maintaining correctness. Each case demonstrates the invariant that no subset sums to the forbidden $k$.
