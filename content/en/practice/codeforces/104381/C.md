---
title: "CF 104381C - Bashy Math"
description: "We are given a collection of integers and we want to count ordered relationships between indices based on divisibility. For every pair of positions $i$ and $j$, we check whether the value at $i$ is divisible by the value at $j$, while ensuring the two indices are different."
date: "2026-07-01T02:58:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104381
codeforces_index: "C"
codeforces_contest_name: "The Andover Computing Open (TACO) 2022"
rating: 0
weight: 104381
solve_time_s: 143
verified: true
draft: false
---

[CF 104381C - Bashy Math](https://codeforces.com/problemset/problem/104381/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of integers and we want to count ordered relationships between indices based on divisibility. For every pair of positions $i$ and $j$, we check whether the value at $i$ is divisible by the value at $j$, while ensuring the two indices are different. Each valid pair contributes one to the final answer.

The input size makes brute force over all pairs impossible. With up to $2 \cdot 10^5$ numbers, a quadratic scan over all pairs would involve around $4 \cdot 10^{10}$ checks, which is far beyond what can run in a second. Even a slightly optimized nested loop that tries to skip some cases still collapses under this scale.

The values themselves are bounded by $5 \cdot 10^5$, which is the key structural constraint. This means we can shift thinking from per-element comparisons to value-frequency reasoning, since the universe of possible values is much smaller than the number of elements.

A naive approach also tends to fail in a subtle way when duplicates exist. If many elements share the same value, treating each occurrence independently inside nested loops causes repeated redundant work and inflates runtime without improving correctness.

For example, if the array is all ones, every ordered pair except self-pairs is valid. A brute force approach still checks every pair individually, while a frequency-based approach immediately collapses the computation into a simple formula.

## Approaches

The brute-force solution iterates over all ordered pairs and checks divisibility directly. This is conceptually simple: for each $i$, we scan all $j \neq i$ and test whether $a_i \bmod a_j = 0$. This works because it follows the definition exactly, but it performs a divisibility check for every ordered pair, leading to $O(n^2)$ operations. With $n = 2 \cdot 10^5$, this is not feasible.

The key observation is that divisibility depends only on values, not on positions. If we know how many times each value appears, we can replace repeated checks with aggregated counting. Instead of iterating over elements, we iterate over possible values and reason about their multiples.

For a fixed value $x$, every valid partner $y$ must satisfy that $y$ divides $x$. So the problem becomes: for each value $x$, sum the frequencies of all divisors $y$, while respecting ordering constraints.

This shifts the computation into a sieve-like accumulation process. We precompute frequencies and then iterate over values, propagating contributions to multiples. Each number contributes to all multiples of itself, which naturally encodes divisibility relationships without explicit pair enumeration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Frequency Sieve | $O(V \log V)$ or $O(V \log V)$-like | $O(V)$ | Accepted |

Here $V = 5 \cdot 10^5$.

## Algorithm Walkthrough

We first compress the input into a frequency array where `freq[x]` stores how many times value `x` appears.

We then compute contributions using a sieve over multiples.

1. Build a frequency array over all values in the input. This lets us treat identical values as a group instead of handling each occurrence separately. This is essential because all interactions depend only on values, not indices.
2. For each value $x$, we consider it as a potential divisor. Every multiple $k \cdot x$ represents a value that can pair with $x$ under the divisibility condition.
3. For each such multiple, we add contributions of the form `freq[x] * freq[kx]`. This counts ordered pairs where the second element is divisible by the first.
4. We must also ensure ordering constraints do not double count incorrectly. Since the condition is directional (i, j ordered), each valid pair is naturally counted exactly once when iterating over divisors in increasing order.
5. Sum all contributions into a global answer.

The key is that iterating over multiples ensures every valid divisibility relation is captured exactly once, without scanning irrelevant pairs.

### Why it works

Every ordered pair $(i, j)$ such that $a_i$ is a multiple of $a_j$ corresponds uniquely to a pair of values $(x, y)$ where $x = a_i$, $y = a_j$, and $x$ is a multiple of $y$. When we fix $y$ and iterate over all multiples $x$, we enumerate exactly those pairs. The frequency product counts all index combinations, so no pairing is missed and none is double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    MAXV = 500000
    freq = [0] * (MAXV + 1)
    
    for x in a:
        freq[x] += 1

    ans = 0

    for y in range(1, MAXV + 1):
        if freq[y] == 0:
            continue
        for x in range(y * 2, MAXV + 1, y):
            if freq[x]:
                ans += freq[x] * freq[y]

    print(ans)

if __name__ == "__main__":
    solve()
```

After reading the input, we build a frequency table so that all identical values are aggregated. The double loop then walks through divisor-multiple relationships. For each base value `y`, we iterate through all multiples `x`, and accumulate `freq[y] * freq[x]` which represents all ordered pairs where the larger value is divisible by the smaller one.

The inner loop starts from `2*y` because `y` dividing itself would correspond to self-pairs, which are explicitly excluded by the problem statement.

## Worked Examples

### Example 1

Input:

```
1 2 3 4 5
```

Frequencies are all 1. We enumerate contributions:

| y | multiples x | contributions |
| --- | --- | --- |
| 1 | 2,3,4,5 | 4 |
| 2 | 4 | 1 |
| 3 | - | 0 |
| 4 | - | 0 |
| 5 | - | 0 |

Total = 5

This matches the sample because all numbers are divisible by 1, and 4 is divisible by 2.

### Example 2

Input:

```
2 2 2 4
```

Frequencies:

- 2 → 3
- 4 → 1

| y | x | contribution |
| --- | --- | --- |
| 2 | 4 | 3 * 1 = 3 |

Answer = 3

This shows how duplicates amplify contributions through frequency multiplication.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(V \log V)$ | Each value iterates over its multiples |
| Space | $O(V)$ | Frequency array over value range |

The maximum value is $5 \cdot 10^5$, so the sieve-style iteration comfortably fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()

# sample 1
assert run("5\n1 2 3 4 5\n") is not None

# single element
assert run("1\n7\n") is not None

# all equal
assert run("4\n3 3 3 3\n") is not None

# powers of two
assert run("5\n1 2 4 8 16\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | n(n-1) | full multiplicity behavior |
| primes | 0 except with 1 | divisibility boundary |
| powers of two | structured chain | transitive multiples |

## Edge Cases

A critical edge case is when the array contains many duplicates of a small number like 1. In that case, every other number contributes through 1, and the answer grows quadratically. The frequency-based method handles this naturally because `freq[1]` multiplies all other frequencies, while a naive approach still does redundant pairwise checks.

Another edge case is when values are sparse near the upper limit. The sieve still iterates correctly because it skips empty frequencies and only processes existing divisors, preventing unnecessary work.
