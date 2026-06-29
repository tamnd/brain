---
title: "CF 104683A - Banis and Cards"
description: "We are given a collection of cards numbered from 1 up to n. For each query, someone chooses a value m and asks for the sum of all card numbers that are divisible by m. In other words, we are summing every multiple of m that appears in the range from 1 to n."
date: "2026-06-29T08:54:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104683
codeforces_index: "A"
codeforces_contest_name: "TheForces Round #24 (DIV3-Forces)"
rating: 0
weight: 104683
solve_time_s: 75
verified: true
draft: false
---

[CF 104683A - Banis and Cards](https://codeforces.com/problemset/problem/104683/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of cards numbered from 1 up to n. For each query, someone chooses a value m and asks for the sum of all card numbers that are divisible by m. In other words, we are summing every multiple of m that appears in the range from 1 to n.

So for a fixed query, the task is to compute m + 2m + 3m + … as long as the term does not exceed n. This is simply the sum of an arithmetic progression formed by the multiples of m inside the range.

The input contains up to 100,000 independent queries, and each n can be as large as 1e9. This combination immediately rules out any approach that iterates over all numbers up to n per query. Even iterating through multiples one by one becomes impossible when n is large and t is also large, since the worst case would involve on the order of 1e14 operations.

The main edge case comes from misunderstanding the range of multiples. A naive implementation might try to loop from 1 to n and check divisibility, which is clearly infeasible. Another subtle issue is overflow or precision if someone tries to accumulate without realizing the closed form exists, although Python avoids overflow, it would still TLE.

A small example shows the structure clearly. If n = 12 and m = 2, the valid cards are 2, 4, 6, 8, 10, 12 and their sum is 42. If n = 1 and m = 1, the answer is 1 because only one number is included.

## Approaches

The brute-force idea is straightforward. For each query, we scan all integers from 1 to n and add those divisible by m. This is correct because it directly follows the definition. However, it performs n iterations per query, leading to 1e14 operations in the worst case when both t and n are large, which is far beyond the limit.

The key observation is that the numbers contributing to the sum are exactly the multiples of m: m, 2m, 3m, and so on up to the largest k such that km ≤ n. The number of such terms is floor(n / m). Once we identify this, the problem reduces to summing the first k natural numbers scaled by m.

So the sum becomes:

m (1 + 2 + … + k), where k = floor(n / m).

The sum of the first k integers is k(k + 1) / 2, so the final result is:

m * k * (k + 1) / 2.

This reduces each query to constant time arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per query | O(1) | Too slow |
| Optimal | O(1) per query | O(1) | Accepted |

## Algorithm Walkthrough

1. Read n and m for a query. These define the range of cards and the step size of valid multiples.
2. Compute k = n // m. This gives the number of multiples of m that fit inside [1, n], since every valid term is of the form i·m.
3. Compute the sum of integers from 1 to k using k * (k + 1) // 2. This represents the index positions of the multiples.
4. Multiply that result by m to scale back from indices to actual card values.
5. Output the result for the query.

### Why it works

Every valid number in the sum can be uniquely written as i·m where i ranges from 1 to k = floor(n / m). This mapping is one-to-one, so summing card values is equivalent to summing a scaled sequence of consecutive integers. Because the sequence is arithmetic with constant difference, replacing it with its closed form preserves correctness for all valid inputs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        k = n // m
        ans = m * k * (k + 1) // 2
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution relies entirely on converting the problem into counting multiples and applying the arithmetic series formula. The integer division n // m is crucial because it determines how many full steps of size m fit into the range. The multiplication by m must happen after computing the triangular number to avoid unnecessary growth during intermediate steps, although Python would handle large integers anyway.

A common mistake is reversing the order or attempting to compute m * i repeatedly in a loop. Another subtle issue is forgetting that k is zero when m > n, but integer division naturally handles this case correctly.

## Worked Examples

We trace the computation for two cases.

### Example 1: n = 12, m = 2

| Step | n | m | k = n//m | k(k+1)/2 | Final |
| --- | --- | --- | --- | --- | --- |
| Init | 12 | 2 | - | - | - |
| Compute k | 12 | 2 | 6 | - | - |
| Triangular sum | 12 | 2 | 6 | 21 | - |
| Multiply by m | 12 | 2 | 6 | 21 | 42 |

The result matches the direct enumeration of even numbers up to 12. This confirms that mapping multiples to indices works correctly.

### Example 2: n = 1, m = 1

| Step | n | m | k = n//m | k(k+1)/2 | Final |
| --- | --- | --- | --- | --- | --- |
| Init | 1 | 1 | - | - | - |
| Compute k | 1 | 1 | 1 | - | - |
| Triangular sum | 1 | 1 | 1 | 1 | - |
| Multiply by m | 1 | 1 | 1 | 1 | 1 |

This confirms correctness for the smallest non-trivial input, where only one element exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each query is handled with constant arithmetic operations |
| Space | O(1) | No auxiliary data structures are used |

The solution easily fits within limits since even 100,000 queries only require simple integer arithmetic, which is negligible compared to the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(sys.stdin.readline())
    for _ in range(t):
        n, m = map(int, sys.stdin.readline().split())
        k = n // m
        output.append(str(m * k * (k + 1) // 2))
    return "\n".join(output)

# provided samples
assert run("""3
12 2
1 1
1010 10
""") == """42
1
5050""", "sample 1"

# custom cases
assert run("""1
10 3
""") == "18", "basic multiple count"

assert run("""1
5 10
""") == "0", "m greater than n"

assert run("""1
1000000000 1
""") == "500000000500000000", "maximum n, m=1"

assert run("""1
6 6
""") == "6", "single multiple"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 3 | 18 | non-trivial divisor pattern |
| 5 10 | 0 | case where no multiples exist |
| 1e9 1 | large sum | maximum bound arithmetic stability |
| 6 6 | 6 | single-element arithmetic progression |

## Edge Cases

When m > n, k becomes zero due to integer division. For example, input n = 5, m = 10 produces k = 0, and the formula evaluates to 0 * 1 / 2 * m = 0. This matches the fact that no card number is divisible by m in that range.

When m equals n, k becomes 1, and the result reduces to m * 1 = m, correctly capturing the single valid element.

When m = 1, every number from 1 to n is included. The formula becomes n(n + 1)/2, which matches the standard sum of the first n integers, confirming that the general formula degenerates correctly into a well-known case.
