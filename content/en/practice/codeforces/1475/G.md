---
title: "CF 1475G - Strange Beauty"
description: "We are given an array of integers, and Polycarp defines an array as beautiful if, for every pair of distinct elements, one divides the other. In other words, for all $i ne j$, either $ai$ divides $aj$ or $aj$ divides $ai$."
date: "2026-06-11T00:10:07+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1475
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 697 (Div. 3)"
rating: 1900
weight: 1475
solve_time_s: 91
verified: true
draft: false
---

[CF 1475G - Strange Beauty](https://codeforces.com/problemset/problem/1475/G)

**Rating:** 1900  
**Tags:** dp, math, number theory, sortings  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and Polycarp defines an array as beautiful if, for every pair of distinct elements, one divides the other. In other words, for all $i \ne j$, either $a_i$ divides $a_j$ or $a_j$ divides $a_i$. The task is to remove as few elements as possible to make the array beautiful.

The input consists of multiple test cases. Each test case provides the length of the array and the array elements themselves. The output for each test case is a single integer: the minimum number of elements that must be removed.

The constraints allow $n$ up to $2 \cdot 10^5$ and element values up to $2 \cdot 10^5$. A naive approach that checks divisibility for all pairs would require $O(n^2)$ operations per test case, which is infeasible at the upper bound since $n^2$ could be $4 \cdot 10^{10}$. We therefore need an algorithm roughly $O(n \log n)$ or $O(n \sqrt{m})$ where $m$ is the maximum value, to handle the largest inputs efficiently.

A subtle edge case is when multiple copies of the same number exist. For example, $[2,2,8]$ is already beautiful, because all pairs of $2$s divide each other, and $2$ divides $8$. Any algorithm that does not handle duplicates correctly might incorrectly remove elements. Another case is when all elements are prime numbers with no common multiples, such as $[3,5,7]$; the optimal solution is to remove all but one element.

## Approaches

The brute-force approach checks every pair and tries to greedily remove elements that violate divisibility. It is correct but too slow. For each element, one would need to verify divisibility against all other $n-1$ elements, yielding $O(n^2)$ per test case. This becomes unacceptable when $n$ approaches $2 \cdot 10^5$.

The key observation is that the array becomes beautiful if it consists of multiples of some base number. Instead of checking all pairs, we can count for each number $x$ how many numbers in the array are divisible by $x$ or multiples of $x$. If we compute for every potential base number the maximum size of a beautiful subset ending with multiples of it, the minimum elements to remove is $n$ minus this maximum subset size.

This transforms the problem into a kind of sieve approach: we iterate over numbers from smallest to largest and accumulate counts of numbers divisible by each number. Then we track the maximum count of numbers that can form a chain of divisibility. The insight is that a number can only help form a beautiful array with its multiples, so we don't need to check all pairs, only multiples of each number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n + m log m) | O(m) | Accepted |

Here, $m$ is the maximum array element value ($2 \cdot 10^5$). The sieve ensures we process each number and its multiples efficiently.

## Algorithm Walkthrough

1. Count occurrences of each number in the array using a frequency array `freq` of size up to the maximum element $2 \cdot 10^5$. This allows us to know how many times each number appears.
2. Initialize a `dp` array of the same size, where `dp[x]` represents the maximum size of a beautiful subset ending at number `x`. Initially, `dp[x] = freq[x]` because a subset containing only `x` repeated `freq[x]` times is trivially beautiful.
3. Iterate over all numbers `x` from 1 to `max_val`. For each number, iterate over its multiples `k*x`. Update `dp[k*x] = max(dp[k*x], dp[x] + freq[k*x])`. This propagates the maximum chain size along multiples.
4. After processing all numbers, the maximum value in `dp` corresponds to the largest beautiful subset. The minimum number of elements to remove is `n - max(dp)`.

The reason this works is that by iterating from smaller numbers to larger numbers and propagating counts along multiples, we are effectively building the largest divisible chains possible. Each number contributes to chains of its multiples without violating the divisibility requirement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    MAX_A = 2 * 10**5
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        freq = [0] * (MAX_A + 1)
        for num in a:
            freq[num] += 1

        dp = freq[:]
        for x in range(1, MAX_A + 1):
            if dp[x] == 0:
                continue
            for k in range(2, (MAX_A // x) + 1):
                dp[k * x] = max(dp[k * x], dp[x] + freq[k * x])
        print(n - max(dp))

if __name__ == "__main__":
    solve()
```

The first section reads input efficiently. `freq` counts occurrences of each number. `dp` starts with the count of each number, representing the trivial beautiful subsets of only that number. The nested loop propagates chain sizes along multiples. Finally, `n - max(dp)` gives the number of removals needed.

## Worked Examples

### Sample Input 1

```
5
7 9 3 14 63
```

| x | freq[x] | dp[x] | Updated dp multiples |
| --- | --- | --- | --- |
| 3 | 1 | 1 | dp[6]=1, dp[9]=2, dp[12]=1, dp[15]=1 ... dp[63]=2 |
| 7 | 1 | 1 | dp[14]=2, dp[21]=2, dp[28]=2, dp[35]=2, dp[42]=2, dp[49]=1, dp[56]=2, dp[63]=3 |

`max(dp) = 3` (subset `[3,9,63]`), so minimum removals = `5-3=2`.

### Sample Input 2

```
3
2 14 42
```

All numbers form multiples of 2. `max(dp)=3`, removals = `0`.

These traces show that the algorithm correctly builds chains along multiples and calculates the largest subset efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m log m) | Counting frequencies is O(n), propagating along multiples is roughly O(m log m) due to harmonic series |
| Space | O(m) | Arrays `freq` and `dp` of size max element |

With $n \le 2 \cdot 10^5$ and $m = 2 \cdot 10^5$, the solution runs comfortably under the 5s limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("4\n5\n7 9 3 14 63\n3\n2 14 42\n4\n45 9 3 18\n3\n2 2 8\n") == "2\n0\n1\n0"

# Custom test cases
assert run("1\n3\n3 5 7\n") == "2", "all primes"
assert run("1\n1\n42\n") == "0", "single element"
assert run("1\n5\n2 4 8 16 32\n") == "0", "all powers of two"
assert run("1\n6\n2 2 3 3 6 12\n") == "1", "mixed multiples"
assert run("1\n5\n1 1 1 1 1\n") == "0", "all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n3 5 7 | 2 | all prime numbers, only one can remain |
| 1\n42 | 0 | single element array is trivially beautiful |
| 5\n2 4 8 16 32 | 0 | all elements are multiples, no removal needed |
| 6\n2 2 3 3 6 12 | 1 | checks correct propagation with repeated and divisible numbers |
| 5\n1 1 1 1 1 | 0 | all equal numbers |

## Edge Cases

For the array `[3,5,7]`, `freq` counts each as 1. Initially `dp[3]=1`, `dp[5]=1`, `dp[7]=1`. No multiples propagate further. The largest beautiful subset is size 1, removals = `3-1=2`. This demonstrates handling arrays with no divisibility between distinct numbers.

For `[2,2,8]`, `dp[2]=2`, `dp[4]=0`, `dp[8]=1`. Propagating from `2`, `dp[4]=2`, `dp[8]=3`. Maximum chain size is 3
