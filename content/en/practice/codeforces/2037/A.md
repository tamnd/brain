---
title: "CF 2037A - Twice"
description: "We are given a small array of integers. Kinich can score points by repeatedly selecting two distinct indices containing equal values, with the restriction that each index can be used at most once. The task is to determine the maximum number of such pairings for each test case."
date: "2026-06-08T10:12:40+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2037
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 988 (Div. 3)"
rating: 800
weight: 2037
solve_time_s: 139
verified: true
draft: false
---

[CF 2037A - Twice](https://codeforces.com/problemset/problem/2037/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small array of integers. Kinich can score points by repeatedly selecting two distinct indices containing equal values, with the restriction that each index can be used at most once. The task is to determine the maximum number of such pairings for each test case.

The input consists of multiple test cases. Each test case specifies the length of the array and the array elements themselves. The output is the maximum score Kinich can achieve in that test case. Since each operation consumes exactly two elements of the same value, the score is determined entirely by how many pairs of identical numbers exist.

The constraints are very tight: the array length $n$ is at most 20, and each element is between 1 and $n$. This implies that even brute-force approaches are feasible because the total number of combinations we might check is bounded by $n \choose 2$ repeatedly, which is very small for $n \le 20$.

The non-obvious edge cases occur when all elements are distinct or all elements are identical. For instance, if the array is [1,2,3,4], no operations are possible, so the score should be 0. Conversely, if the array is [2,2,2,2], there are two disjoint pairs we can make, yielding a score of 2. A careless implementation that counts only unique numbers or forgets to prevent reuse of indices could produce incorrect results in these scenarios.

## Approaches

A brute-force approach would try every possible pair of equal numbers, mark them as used, and recurse to maximize the score. This is correct because it explores all possible sequences of pairings. However, even with $n=20$, this recursive method has a factorial growth, which is unnecessary for this problem.

The key observation is that we do not need to consider the positions of numbers, only their frequency. Each number can contribute at most $\lfloor \text{frequency} / 2 \rfloor$ points to the score because every pair requires two occurrences. Summing $\lfloor \text{frequency} / 2 \rfloor$ over all distinct numbers directly gives the maximum score. This reduces the problem to counting occurrences, which is trivial for the given constraints.

The brute-force works because it explicitly enumerates all valid pairings, but it fails when $n$ grows larger because the number of combinations explodes. The observation about counting frequencies converts the problem into simple arithmetic, avoiding any combinatorial explosion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow / unnecessary |
| Frequency Count | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read the array length $n$ and the array elements.
3. Initialize a frequency array of size $n+1$ to zero. This will store the number of occurrences of each integer from 1 to $n$.
4. Traverse the array and increment the frequency of each number.
5. Initialize the score to 0.
6. For each number in the frequency array, compute how many pairs can be formed by integer division of the frequency by 2. Add this to the score.
7. Output the score for the test case.

This works because the maximum number of non-overlapping pairs for any number is exactly half its occurrences. Summing across all numbers gives the maximum achievable score without the need to track individual indices.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    freq = [0] * (n + 1)
    for x in a:
        freq[x] += 1
    
    score = 0
    for count in freq:
        score += count // 2
    
    print(score)
```

The solution reads input efficiently using `sys.stdin.readline`, counts the occurrences of each number, and computes the maximum number of non-overlapping pairs. The frequency array is sized `n+1` for 1-based indexing convenience, and integer division ensures only complete pairs are counted.

## Worked Examples

### Example 1

Input: `4 1 2 3 1`

| Number | Frequency | Pairs | Score |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |
| 2 | 1 | 0 | 1 |
| 3 | 1 | 0 | 1 |

The score is 1, corresponding to the pair of 1s.

### Example 2

Input: `6 1 2 3 1 2 3`

| Number | Frequency | Pairs | Score |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |
| 2 | 2 | 1 | 2 |
| 3 | 2 | 1 | 3 |

The score is 3, representing one pair for each value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Counting frequencies and summing pairs for each test case |
| Space | O(n) | Frequency array to store counts of each integer |

Given the constraints $t \le 500$ and $n \le 20$, the solution easily executes well within time and memory limits.

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
        a = list(map(int, input().split()))
        freq = [0] * (n + 1)
        for x in a:
            freq[x] += 1
        score = sum(count // 2 for count in freq)
        print(score)
    
    return output.getvalue().strip()

# Provided samples
assert run("5\n1\n1\n2\n2 2\n2\n1 2\n4\n1 2 3 1\n6\n1 2 3 1 2 3\n") == "0\n1\n0\n1\n3", "sample 1"

# Custom test cases
assert run("1\n4\n1 1 1 1\n") == "2", "all equal elements"
assert run("1\n4\n1 2 3 4\n") == "0", "all distinct"
assert run("1\n5\n1 2 2 3 3\n") == "2", "multiple pairs"
assert run("1\n1\n1\n") == "0", "single element"
assert run("1\n6\n1 1 2 2 2 2\n") == "3", "mixed frequencies"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 1 | 2 | Correctly counts multiple pairs of the same value |
| 1 2 3 4 | 0 | No pairs possible for distinct numbers |
| 1 2 2 3 3 | 2 | Correctly counts multiple different numbers with pairs |
| 1 | 0 | Single-element edge case |
| 1 1 2 2 2 2 | 3 | Mixed frequency handling |

## Edge Cases

For a single-element array like `[1]`, the algorithm initializes the frequency array, counts `1` once, divides by 2 to get 0 pairs, and outputs 0. For arrays with all equal elements such as `[2,2,2,2]`, the frequency is 4, integer division by 2 gives 2 pairs, which is exactly the maximum score. Mixed cases like `[1,1,2,2,2,2]` yield frequency counts `[0,2,4,...]`, producing 1+2=3 points, showing that the algorithm correctly handles varying frequencies across different numbers.
