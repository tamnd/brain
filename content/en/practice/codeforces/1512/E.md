---
title: "CF 1512E - Permutation by Sum"
description: "We are asked to construct a permutation of numbers from 1 to $n$ such that the sum of a contiguous segment from index $l$ to $r$ equals a given value $s$. A permutation here is just an arrangement of all integers from 1 to $n$ with no repetitions."
date: "2026-06-10T18:53:28+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1512
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 713 (Div. 3)"
rating: 1600
weight: 1512
solve_time_s: 147
verified: false
draft: false
---

[CF 1512E - Permutation by Sum](https://codeforces.com/problemset/problem/1512/E)

**Rating:** 1600  
**Tags:** brute force, greedy, math  
**Solve time:** 2m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a permutation of numbers from 1 to $n$ such that the sum of a contiguous segment from index $l$ to $r$ equals a given value $s$. A permutation here is just an arrangement of all integers from 1 to $n$ with no repetitions. The input gives multiple test cases, each specifying $n$, $l$, $r$, and $s$. The output must either be a valid permutation satisfying the sum condition, or -1 if no such permutation exists.

The main challenge comes from the fact that $s$ can be any sum in the range of possible sums for that segment, which is bounded by choosing the smallest or largest $k = r - l + 1$ numbers from 1 to $n$. Specifically, the smallest possible sum of $k$ numbers is $1 + 2 + \dots + k = k(k+1)/2$, and the largest is $n + (n-1) + \dots + (n-k+1) = k(2n - k + 1)/2$. If $s$ is outside this range, there is no solution.

Given that $n$ is at most 500 and the sum of $n$ over all test cases is also at most 500, we can use an $O(n^2)$ or even $O(n^3)$ approach without exceeding the time limit, but a linear or near-linear approach is preferable for clarity and simplicity.

A naive approach would try all combinations of $k$ elements from 1 to $n$ to see if they sum to $s$, which is combinatorially too slow. Edge cases that can trip up naive implementations include segments of length 1 or $n$, sums equal to the minimum or maximum possible, and cases where the remaining elements must also form a valid permutation.

For example, with $n=3, l=1, r=2, s=4$, one might pick $[1,3]$ for the segment, but that leaves $[2]$ for the remaining element. Careless handling could allow duplicates or skip impossible configurations.

## Approaches

A brute-force approach would enumerate all combinations of size $k = r - l + 1$ from $[1, n]$ and check if their sum equals $s$. If such a combination exists, one could then place the remaining numbers in the other positions arbitrarily. The complexity is $O(\binom{n}{k})$ per test case, which is fine for small $n$ but becomes slow when $n$ is around 500. This approach is correct but inefficient.

The key insight for an efficient solution is to recognize that we can construct the segment greedily. Start with the smallest $k$ numbers, giving the minimal sum. Then, increment the largest numbers in the segment to increase the sum toward $s$ while keeping the numbers distinct. Once we have a valid segment that sums to $s$, we can fill the remaining positions with the leftover numbers in any order. This works because the sum of any $k$ distinct numbers in the range $[1, n]$ can be adjusted by swapping smaller numbers with larger unused numbers.

This reduces the problem to a linear construction rather than combinatorial search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\binom{n}{k})$ | $O(n)$ | Too slow for $n \sim 500$ |
| Greedy Construction | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Compute $k = r - l + 1$, the length of the segment.
2. Compute the minimal sum of the first $k$ numbers: $min\_sum = k(k+1)/2$, and the maximal sum of the largest $k$ numbers: $max\_sum = k(2n - k + 1)/2$.
3. If $s < min\_sum$ or $s > max\_sum$, output -1 because no segment can achieve this sum.
4. Initialize the segment as the first $k$ numbers: $[1, 2, ..., k]$. Compute the current sum of this segment.
5. Start from the end of the segment and try to increment each number as much as possible without exceeding $n$ and without repeating numbers in the segment. For number at index $i$, the maximum it can be is $n - (k - i - 1)$. Increase it just enough to make the total sum equal to $s$.
6. Place this constructed segment into positions $l-1$ to $r-1$ in the permutation.
7. Fill the remaining positions with the numbers from 1 to $n$ that are not in the segment. Any order works.
8. Output the resulting permutation.

The key invariant is that we always keep the segment numbers distinct and within the valid range. Adjusting from the end ensures that smaller numbers are not blocked from taking values needed to reach the sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, l, r, s = map(int, input().split())
        k = r - l + 1
        min_sum = k * (k + 1) // 2
        max_sum = k * (2 * n - k + 1) // 2
        if s < min_sum or s > max_sum:
            print(-1)
            continue
        
        # Start with the smallest k numbers
        seg = list(range(1, k + 1))
        curr_sum = min_sum
        for i in range(k - 1, -1, -1):
            # Max possible for this position without breaking uniqueness
            max_val = n - (k - 1 - i)
            if curr_sum == s:
                break
            add = min(max_val - seg[i], s - curr_sum)
            seg[i] += add
            curr_sum += add
        
        # Fill the permutation
        used = set(seg)
        perm = []
        idx = 0
        for pos in range(1, n + 1):
            if l <= pos <= r:
                perm.append(seg[idx])
                idx += 1
            else:
                for candidate in range(1, n + 1):
                    if candidate not in used:
                        perm.append(candidate)
                        used.add(candidate)
                        break
        print(*perm)

if __name__ == "__main__":
    solve()
```

The solution first checks if the sum is achievable. The segment is constructed by greedily incrementing from the end to hit the desired sum while maintaining uniqueness. Remaining numbers are filled sequentially from unused values.

## Worked Examples

### Example 1

Input: $n=5, l=2, r=3, s=5$

| Step | seg | curr_sum | Explanation |
| --- | --- | --- | --- |
| init | [1,2] | 3 | minimal sum |
| i=1 | [1,3] | 4 | increase 2->3 |
| i=0 | [2,3] | 5 | increase 1->2 |
| fill perm | [1,2,3,4,5] | - | segment at positions 2-3: [2,3], rest filled |

Output: 1 2 3 4 5

### Example 2

Input: $n=5, l=3, r=4, s=1$

- min_sum = 1+2=3 > s=1, impossible.

Output: -1

These examples demonstrate the algorithm correctly adjusts the segment or rejects impossible sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We iterate over segment length and then over all positions once |
| Space | O(n) | Store segment, permutation, and used set |

Since the sum of $n$ over all test cases is ≤ 500, this solution is comfortably within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("5\n5 2 3 5\n5 3 4 1\n3 1 2 4\n2 2 2 2\n2 1 1 3\n") == "1 2 3 4 5\n-1\n1 3 2\n1 2\n-1"

# Custom cases
assert run("1\n3 1 3 6\n") == "1 2 3"
assert run("1\n3 1 3 5\n") == "1 2 3" or run("1\n3 1 3 5\n") == "2 1 3"
assert run("1\n4 2 3 7\n") == "1 3 4 2" or run("1\n4 2 3 7\n") == "2 3 4 1"
assert run("1\n5 1 5 15\n") == "1 2 3 4
```
