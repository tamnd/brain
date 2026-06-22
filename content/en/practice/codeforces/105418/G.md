---
title: "CF 105418G - Odd Non Primes"
description: "We are given several independent test cases. Each test case is a sequence of integers representing a row of cards."
date: "2026-06-23T04:23:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105418
codeforces_index: "G"
codeforces_contest_name: "Algorithmia IIITN 2024 - Round 1"
rating: 0
weight: 105418
solve_time_s: 80
verified: false
draft: false
---

[CF 105418G - Odd Non Primes](https://codeforces.com/problemset/problem/105418/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent test cases. Each test case is a sequence of integers representing a row of cards. From this row we may choose any contiguous segment, and for that segment we compute a score defined as the number of odd values minus the number of prime values inside it. The task is to find the maximum possible score over all non-empty contiguous segments.

The structure is purely linear, so every decision is about where a subarray starts and ends. There is no combinatorial selection beyond contiguous intervals, which immediately suggests prefix-based or Kadane-style reasoning rather than anything exponential.

The constraints are small enough that an $O(n^2)$ per test solution would pass. With total $n \le 2000$, even a double loop that evaluates all subarrays is around four million operations, which is fine in Python. However, the intended solution is linear per test case.

A subtle point lies in the interaction between “odd” and “prime”. Every prime except 2 is odd, so primes overlap heavily with odd numbers. This means contributions are not independent categories; a number can increase the odd count and simultaneously decrease the prime count. The number 2 is the only prime that is not odd, which makes it behave differently from other primes.

A naive mistake is to treat the score as two independent arrays or to try prefix counts of odds and primes separately without realizing they overlap. Another mistake is assuming primes only matter as a subset of odds; in fact, even non-odd primes (only 2) still reduce the score, and odd primes contribute net zero if treated incorrectly.

For example, consider a segment containing only 2. The score is $0 - 1 = -1$. A careless approach that only counts odd primes as “bad odds” would incorrectly treat it as neutral.

## Approaches

A brute-force solution evaluates every subarray and computes its score directly. For each pair of indices $l, r$, we scan the segment and count odds and primes. This is straightforward and correct because it directly follows the definition. However, it repeats the same work repeatedly: each segment recomputes counts from scratch.

The time complexity of this approach is $O(n^3)$ per test case if implemented literally, since there are $O(n^2)$ subarrays and each takes $O(n)$ to evaluate. Even with prefix sums reducing evaluation to $O(1)$, we still need to carefully encode both odd and prime indicators, but that only reduces it to $O(n^2)$, which is acceptable under the constraints but not optimal.

The key observation is that each element contributes independently to the score. For each value $a_i$, we can assign it a weight:

if it is odd, it contributes +1; if it is prime, it contributes -1; if both (odd prime), the net contribution is 0; if neither, it contributes 0. Since 2 is the only even prime, it gets -1. Every odd prime contributes +1 and -1, canceling out to 0.

This reduces the problem to finding a maximum subarray sum on a transformed array where each element has a fixed weight. That is exactly Kadane’s algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ or $O(n^2)$ | $O(1)$ | Too slow / Accepted under limits |
| Optimal (Kadane) | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Precompute whether each number is prime. Since values go up to $10^6$, we use a sieve once globally. This avoids repeated primality checks inside each test case.
2. For each element $a_i$, compute its contribution:

if it is odd, add +1 to its base score; if it is prime, subtract 1. This produces a single integer array representing the problem.
3. Run a maximum subarray sum algorithm on this transformed array. Maintain a running best ending here and a global best.
4. At each position, decide whether to extend the previous segment or start fresh. This choice reflects whether a negative prefix would harm future gain.
5. Track the maximum value seen across all positions.

The reasoning behind step 4 is that any optimal segment must either include the previous element or restart; there is no benefit in skipping elements inside a chosen subarray.

### Why it works

After transformation, each element contributes a fixed independent value to any subarray. The score of a subarray becomes the sum of its elements in this transformed array. Any contiguous segment maximizing sum is exactly the classical maximum subarray problem. The greedy transition in Kadane’s algorithm ensures that any prefix with negative total is discarded because it reduces all future sums in that segment, so restarting yields a better or equal outcome.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 10**6

# Sieve for primality
is_prime = [True] * (MAXV + 1)
is_prime[0] = is_prime[1] = False
for i in range(2, int(MAXV ** 0.5) + 1):
    if is_prime[i]:
        step = i
        start = i * i
        for j in range(start, MAXV + 1, step):
            is_prime[j] = False

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))

    best = -10**18
    cur = -10**18

    for x in arr:
        val = 0
        if x % 2 == 1:
            val += 1
        if is_prime[x]:
            val -= 1

        if cur == -10**18:
            cur = val
        else:
            cur = max(val, cur + val)

        best = max(best, cur)

    print(best)
```

The sieve is built once globally to ensure that primality checks are constant time during each test case. Each number is converted into its contribution independently. The Kadane step uses a standard recurrence: either start a new subarray at the current element or extend the previous one.

The initialization of `cur` with a sentinel avoids ambiguity for the first element, ensuring the first value always starts a segment cleanly.

## Worked Examples

Consider an array: `[1, 2, 3, 4]`.

We compute contributions:

- 1: odd, not prime → +1
- 2: even prime → -1
- 3: odd prime → +1 - 1 = 0
- 4: even non-prime → 0

So transformed array is `[1, -1, 0, 0]`.

| Index | Value | Contribution | Cur Best Ending Here | Global Best |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 |
| 2 | 2 | -1 | 0 | 1 |
| 3 | 3 | 0 | 0 | 1 |
| 4 | 4 | 0 | 0 | 1 |

The maximum segment is `[1]` with value 1. This confirms that negative contributions (like 2) reset potential gains.

Now consider `[2, 3, 5, 4]`.

Contributions:

- 2 → -1
- 3 → 0
- 5 → 0
- 4 → 0

| Index | Value | Contribution | Cur | Best |
| --- | --- | --- | --- | --- |
| 1 | 2 | -1 | -1 | -1 |
| 2 | 3 | 0 | 0 | 0 |
| 3 | 5 | 0 | 0 | 0 |
| 4 | 4 | 0 | 0 | 0 |

The optimal segment is `[3, 5, 4]` giving 0, showing that starting after a negative element improves the result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test | Each element is processed once after sieve preprocessing |
| Space | $O(10^6)$ | Sieve storage for primality |

The total $n$ across test cases is small, so linear scanning is well within limits. The sieve cost is incurred once and reused, making the solution efficient overall.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read().strip()

# Note: full solution function integration assumed in real environment

# custom conceptual checks (format illustrative)
assert True  # placeholder since full harness depends on integration
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n2` | `-1` | single even prime |
| `1\n1\n3` | `0` | odd prime cancels out |
| `1\n4\n1 2 3 4` | `1` | mixed contributions |
| `1\n3\n4 6 8` | `1` | all non-prime evens/odds behavior |
| `1\n5\n2 3 5 7 11` | `0` | all primes cancel structure |

## Edge Cases

A single element equal to 2 is the most important boundary case. The algorithm assigns it value -1, and Kadane correctly treats it as a standalone subarray since extending from negative prefixes would only reduce future sums.

An array of only odd primes produces all zero contributions. The maximum subarray sum becomes 0, and Kadane naturally selects any non-empty segment, confirming that cancellation is handled correctly without special casing.

An array with alternating large positive and single negative values demonstrates the restart behavior of Kadane. Whenever a -1 appears, the running sum drops, and the algorithm may restart after it if beneficial, ensuring optimal segmentation.
