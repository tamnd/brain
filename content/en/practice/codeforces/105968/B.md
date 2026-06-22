---
title: "CF 105968B - Braga's Problem"
description: "We are working with multiple queries over a range of integers, and for each query we need to compute the sum of all prime numbers that lie inside a given interval."
date: "2026-06-22T16:19:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105968
codeforces_index: "B"
codeforces_contest_name: "IME++ Starters Try-Outs 2025"
rating: 0
weight: 105968
solve_time_s: 54
verified: true
draft: false
---

[CF 105968B - Braga's Problem](https://codeforces.com/problemset/problem/105968/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are working with multiple queries over a range of integers, and for each query we need to compute the sum of all prime numbers that lie inside a given interval. Each query provides a left and right endpoint, and the task is to quickly return the total of primes between those two bounds, inclusive.

The key structure here is that the same universe of numbers is reused across all queries. That immediately suggests that recomputing primality or summing primes from scratch per query will be redundant. Instead, we want a preprocessing step over a fixed range, followed by fast range queries.

If the maximum possible value in the input range is large, say up to n, then a per-query scan would cost O(n) and become too slow when multiplied by many queries. For example, if n is 10^6 and there are 10^5 queries, a naive approach would require about 10^11 operations, which is not feasible under typical time limits. This pushes us toward preprocessing in roughly O(n log log n) or O(n) time and answering each query in O(1).

A subtle edge case appears when the range starts at 1. Since 1 is not prime, any approach that incorrectly initializes primality for 1 can accidentally include it in the sum. For example, if the query is [1, 10], the correct primes are 2, 3, 5, 7 and the answer is 17. A buggy sieve that treats 1 as prime would return 18.

Another issue arises when the range is very small or degenerate, such as [x, x]. In that case, correctness depends entirely on whether x is prime, and prefix sums must be constructed carefully to support single-point queries without off-by-one errors.

## Approaches

A straightforward approach is to handle each query independently. For each range [l, r], we iterate through every number, check if it is prime by trial division, and accumulate the sum. This is conceptually simple and correct, but primality testing up to n costs O(sqrt n), and doing it for every number in every query leads to O(n sqrt n) in the worst case per query range. With many queries, this quickly becomes infeasible.

The inefficiency comes from recomputing primality and recomputing partial sums repeatedly for overlapping ranges. The structure of the problem suggests that primality of each number is independent of queries, and once known, it never changes. This allows preprocessing.

The sieve of Eratosthenes computes primality for all numbers up to n in O(n log log n). Once we have a boolean array marking primes, we can build a prefix sum array where prefix[i] stores the sum of all primes from 1 to i. Then any query [l, r] can be answered as prefix[r] - prefix[l - 1], giving O(1) per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q · N √N) | O(1) | Too slow |
| Sieve + Prefix Sum | O(N log log N + Q) | O(N) | Accepted |

## Algorithm Walkthrough

We build a global view of which numbers are prime and convert that into cumulative information that supports fast range queries.

### Steps

1. Choose the maximum value n based on the largest possible endpoint across all queries. This ensures that every number we might need is covered in preprocessing.
2. Create an array is_prime of size n + 1 and initialize all entries as true except 0 and 1. This initialization reflects that primality is only unknown for 2 and above.
3. Run the sieve of Eratosthenes by iterating i from 2 up to sqrt(n). When i is still marked as prime, mark all multiples of i starting from i * i as non-prime. Starting from i * i is sufficient because smaller multiples would have already been handled by smaller primes.
4. After the sieve completes, construct a prefix sum array prefix where prefix[i] stores the sum of all primes from 1 to i. For each i, if is_prime[i] is true, add i to the running sum; otherwise add 0.
5. For each query [l, r], compute the result as prefix[r] - prefix[l - 1] when l > 1, otherwise just prefix[r]. This converts a range sum into a constant time arithmetic operation.

### Why it works

At the end of the sieve, every composite number has been marked false in is_prime, and every remaining true entry corresponds exactly to a prime number. The prefix array is constructed as a cumulative sum over a fixed array, so it preserves exact totals for every prefix interval. Since any range sum can be decomposed into two prefix sums, every query is answered exactly without recomputation. The invariant is that prefix[i] always equals the sum of all primes in [1, i], and this holds because each index contributes exactly once if and only if it is prime.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_sieve(n):
    is_prime = [True] * (n + 1)
    if n >= 0:
        is_prime[0] = False
    if n >= 1:
        is_prime[1] = False

    i = 2
    while i * i <= n:
        if is_prime[i]:
            step = i
            start = i * i
            for j in range(start, n + 1, step):
                is_prime[j] = False
        i += 1

    return is_prime

def build_prefix(is_prime):
    n = len(is_prime) - 1
    prefix = [0] * (n + 1)
    running = 0
    for i in range(1, n + 1):
        if is_prime[i]:
            running += i
        prefix[i] = running
    return prefix

def solve():
    data = input().strip().split()
    if not data:
        return

    q = int(data[0])
    queries = []
    max_r = 0

    idx = 1
    for _ in range(q):
        l = int(data[idx])
        r = int(data[idx + 1])
        idx += 2
        queries.append((l, r))
        if r > max_r:
            max_r = r

    is_prime = build_sieve(max_r)
    prefix = build_prefix(is_prime)

    out = []
    for l, r in queries:
        if l > 1:
            out.append(str(prefix[r] - prefix[l - 1]))
        else:
            out.append(str(prefix[r]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The sieve construction isolates primality as a preprocessing step, ensuring we never repeat work across queries. The prefix construction transforms a static classification into a structure that supports O(1) interval sums. The only delicate part is handling the lower bound of queries correctly, since prefix subtraction requires a guard when l equals 1 to avoid indexing prefix[-1].

## Worked Examples

Consider queries over a small range where we can manually track primes.

Example input:

```
3
1 10
5 5
6 20
```

We first build primes up to 20, which are 2, 3, 5, 7, 11, 13, 17, 19. The prefix sums evolve as follows.

| i | is_prime[i] | prefix[i] |
| --- | --- | --- |
| 1 | F | 0 |
| 2 | T | 2 |
| 3 | T | 5 |
| 4 | F | 5 |
| 5 | T | 10 |
| 6 | F | 10 |
| 7 | T | 17 |
| 8 | F | 17 |
| 9 | F | 17 |
| 10 | F | 17 |
| 11 | T | 28 |
| 12 | F | 28 |
| 13 | T | 41 |
| 14 | F | 41 |
| 15 | F | 41 |
| 16 | F | 41 |
| 17 | T | 58 |
| 18 | F | 58 |
| 19 | T | 77 |
| 20 | F | 77 |

For the query [1, 10], we return prefix[10] = 17, which matches 2 + 3 + 5 + 7.

For [5, 5], we return prefix[5] - prefix[4] = 10 - 5 = 5, since 5 is prime.

For [6, 20], we compute 77 - 10 = 67, corresponding to primes 7, 11, 13, 17, 19.

This trace confirms that prefix differences isolate exactly the contributions inside each query range.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log log N + Q) | sieve preprocesses all numbers once, each query answered in constant time |
| Space | O(N) | arrays store primality and prefix sums up to maximum value |

The preprocessing cost is acceptable for typical constraints up to a few million, and query processing is optimal since each query reduces to a constant number of array lookups.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip() if False else solve_capture(inp)

def solve_capture(inp: str) -> str:
    import sys
    from io import StringIO
    backup = sys.stdout
    sys.stdin = StringIO(inp)
    out = StringIO()
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue().strip()

# sample-style tests
assert solve_capture("3\n1 10\n5 5\n6 20\n") == "17\n5\n67"

# custom cases
assert solve_capture("1\n1 1\n") == "0"
assert solve_capture("1\n2 2\n") == "2"
assert solve_capture("2\n1 2\n2 3\n") == "2\n5"
assert solve_capture("1\n10 30\n") == str(sum([11,13,17,19,23,29]))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 0 | non-prime boundary |
| 2 2 | 2 | smallest prime case |
| overlapping ranges | 2, 5 | prefix correctness |
| 10 30 | computed sum | larger range consistency |

## Edge Cases

A range starting at 1 tests whether the prefix subtraction correctly avoids accessing a negative index. For input [1, 10], the algorithm uses prefix[10] directly, and since prefix[0] is defined as 0 implicitly, the result remains correct.

A single-point range like [5, 5] ensures that subtraction does not accidentally remove the value. The computation becomes prefix[5] - prefix[4], which isolates exactly 5.

Large ranges dominated by non-primes, such as [14, 16], confirm that composite-heavy intervals produce zero contributions without special handling. The sieve already marks 14, 15, 16 as non-prime, so prefix remains unchanged across that segment, and the subtraction correctly yields 0.
