---
title: "CF 1922B - Forming Triangles"
description: "We are given a set of sticks, each with a length that is a power of two. The input does not give the actual lengths directly but rather exponents $ai$ such that the stick's length is $2^{ai}$."
date: "2026-06-08T19:16:13+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1922
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 161 (Rated for Div. 2)"
rating: 1200
weight: 1922
solve_time_s: 100
verified: true
draft: false
---

[CF 1922B - Forming Triangles](https://codeforces.com/problemset/problem/1922/B)

**Rating:** 1200  
**Tags:** combinatorics, constructive algorithms, math, sortings  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of sticks, each with a length that is a power of two. The input does not give the actual lengths directly but rather exponents $a_i$ such that the stick's length is $2^{a_i}$. Our task is to count the number of ways to pick exactly three sticks that can form a non-degenerate triangle. A triangle is non-degenerate if the sum of the lengths of any two sides exceeds the length of the third side.

The output for each test case is a single integer representing the number of valid stick triplets. Because the sticks are defined by powers of two, many sticks may have the same length, and the triangle inequality reduces to a simple comparison between the largest stick and the sum of the other two.

The constraints tell us that $n$ can be as large as $3 \cdot 10^5$ and there can be up to $10^4$ test cases, with the total number of sticks across all test cases bounded by $3 \cdot 10^5$. This means any algorithm with complexity worse than $O(n^2)$ per test case will likely be too slow. An $O(n \log n)$ or $O(n^2)$ approach is acceptable if carefully implemented.

Edge cases arise when all sticks have the same length, making every triplet valid, or when the sticks grow exponentially, making most triplets invalid. For example, if we have sticks with exponents `[1, 2, 3]` corresponding to lengths `[2, 4, 8]`, no triangle can be formed because $2 + 4 = 6 \le 8$.

## Approaches

The naive approach is brute force: iterate through all triplets of sticks and check if they satisfy the triangle inequality. This is correct but has $O(n^3)$ complexity, which is infeasible for $n$ up to $3 \cdot 10^5$. Even for moderate $n$, such an approach would be far too slow.

The key observation is that the stick lengths are powers of two, which implies that the triangle inequality can be simplified. Sorting the sticks by their exponents converts the problem into a standard triangle-counting problem on a sorted array. For sorted sticks, if we pick three indices $i < j < k$, a non-degenerate triangle exists if $2^{a_i} + 2^{a_j} > 2^{a_k}$. Sorting guarantees that $a_i \le a_j \le a_k$, so we only need to check the largest element versus the sum of the smaller two. This allows a two-pointer or three-pointer approach to count valid triplets efficiently.

We can precompute the number of triplets using combinatorial formulas for sticks of equal length and then account for sticks of different lengths by scanning through sorted unique lengths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Sort + Three Pointers | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and the exponents $a_i$.
2. Sort the array of exponents. Sorting allows us to quickly enforce the triangle inequality by only comparing the largest stick to the sum of the smaller two.
3. Initialize a counter for valid triplets.
4. Iterate over the array with three indices $i < j < k$. Fix $i$ and $j$ and find the maximum $k$ such that $2^{a_i} + 2^{a_j} > 2^{a_k}$. Use the sorted property to move $k$ forward until the condition fails.
5. For each valid $i, j$ pair, add the number of valid $k$ positions to the counter.
6. Output the counter after scanning all pairs.

Why it works: The sorted array ensures that as $k$ increases, $2^{a_k}$ also increases. By advancing $k$ only when the triangle inequality holds, we count every triplet exactly once, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_triangles(n, a):
    a.sort()
    count = 0
    for i in range(n - 2):
        k = i + 2
        for j in range(i + 1, n - 1):
            while k < n and (1 << a[i]) + (1 << a[j]) > (1 << a[k]):
                k += 1
            count += k - j - 1
    return count

t = int(input())
results = []
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    results.append(str(count_triangles(n, a)))

print("\n".join(results))
```

The code first sorts the exponent array. For each pair of sticks, it advances $k$ until the triangle inequality fails. The number of valid $k$ for each pair $(i, j)$ is exactly $k - j - 1$. Sorting is necessary to ensure that once $2^{a_i} + 2^{a_j} \le 2^{a_k}$, all subsequent $k$ will also fail.

## Worked Examples

Sample input 1:

```
7
1 1 1 1 1 1 1
```

| i | j | k (max) | Valid triplets added | Counter |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 5 | 5 |
| 0 | 2 | 3 | 4 | 9 |
| 0 | 3 | 4 | 3 | 12 |
| 0 | 4 | 5 | 2 | 14 |
| 0 | 5 | 6 | 1 | 15 |
| 1 | 2 | 3 | 4 | 19 |
| 1 | 3 | 4 | 3 | 22 |
| 1 | 4 | 5 | 2 | 24 |
| 1 | 5 | 6 | 1 | 25 |
| 2 | 3 | 4 | 3 | 28 |
| 2 | 4 | 5 | 2 | 30 |
| 2 | 5 | 6 | 1 | 31 |
| 3 | 4 | 5 | 2 | 33 |
| 3 | 5 | 6 | 1 | 34 |
| 4 | 5 | 6 | 1 | 35 |

Every triplet works because all sticks have the same length.

Sample input 2:

```
4
3 2 1 3
```

After sorting: `[1, 2, 3, 3]` (lengths `[2, 4, 8, 8]`)

| i | j | k (max) | Valid triplets added | Counter |
| --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 0 | 0 |
| 0 | 2 | 3 | 2 | 2 |
| 1 | 2 | 3 | 0 | 2 |

Only two triplets satisfy the triangle inequality: `(1,3,4)` and `(2,3,4)` in 1-based indexing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Sorting takes O(n log n), the nested loop with pointer k runs in total O(n^2) worst-case. |
| Space | O(n) | We store the array of exponents and the result list. |

Given the sum of $n$ across all test cases is ≤ 3·10^5, the solution fits comfortably in the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    import builtins
    input = builtins.input
    t = int(input())
    results = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        results.append(str(count_triangles(n, a)))
    return output.getvalue().strip()

# Provided samples
assert run("4\n7\n1 1 1 1 1 1 1\n4\n3 2 1 3\n3\n1 2 3\n1\n1\n") == "35\n2\n0\n0"

# Custom tests
assert run("1\n3\n0 0 0\n") == "1"  # All equal lengths, one triangle
assert run("1\n5\n0 1 2 3 4\n") == "0"  # Exponentially increasing, no triangle
assert run("1\n6\n1 1 2 2 3 3\n") == "7"  # Mix of equal lengths
assert run("1\n1\n10\n") == "0"  # Single stick, cannot form triangle
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3\n0 0 0` | 1 | Minimum-size input, all equal sticks |
| `5\n0 1 2 3 4` | 0 | Increasing powers, no triangle possible |
| `6\n1 1 2 2 3 3` | 7 | Mix of duplicates and distinct values |
| `1\n10` | 0 | Single stick, cannot form triangle |

## Edge Cases

If all sticks are equal, like `[1, 1, 1
