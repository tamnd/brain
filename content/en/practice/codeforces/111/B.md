---
title: "CF 111B - Petya and Divisors"
description: "We are asked to process a sequence of queries, each defined by two integers, x and y. For each query, we need to count how many positive divisors of x do not divide any of the y numbers immediately preceding x in the sequence, that is, the numbers x-y, x-y+1, ..., x-1."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 111
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 85 (Div. 1 Only)"
rating: 1900
weight: 111
solve_time_s: 170
verified: true
draft: false
---

[CF 111B - Petya and Divisors](https://codeforces.com/problemset/problem/111/B)

**Rating:** 1900  
**Tags:** binary search, data structures, number theory  
**Solve time:** 2m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to process a sequence of queries, each defined by two integers, x and y. For each query, we need to count how many positive divisors of x do **not** divide any of the y numbers immediately preceding x in the sequence, that is, the numbers x-y, x-y+1, ..., x-1. If y is zero, the answer is simply the number of divisors of x, because there are no preceding numbers to check.

The input allows up to 100,000 queries, and x can be as large as 100,000. This means any solution that naively iterates over all divisors of x and checks them against up to x numbers per query will be too slow. A brute-force approach of iterating every divisor for each query against all relevant previous numbers could approach 10^10 operations, which is unmanageable. We need a solution that precomputes or reduces work using number-theoretic properties.

Non-obvious edge cases include queries with y = 0, which is a shortcut situation, and small x values, particularly x = 1 or prime numbers, where divisors are trivial but boundary conditions could fail if we don’t handle them correctly. Another edge case is when y exceeds x, but the constraints guarantee 0 ≤ y ≤ i-1, so we will never access negative indices of previous x values.

## Approaches

The brute-force approach would enumerate all divisors of x for each query and then check each divisor against the y previous numbers to see if it divides any of them. For each query, this could involve up to O(sqrt(x)) divisors times up to O(y) previous numbers, which in the worst case reaches O(n * sqrt(x) * n) ≈ 10^10 operations. This is clearly too slow.

The key observation is that we only need to know whether a divisor d of x appears as a divisor of any of the previous y numbers. Instead of testing each divisor against every previous number individually, we can maintain for each divisor d a record of the last query index where it appeared as a divisor. Then for the current query, we simply check whether this last occurrence is within the last y queries. If it is, we skip counting d; if not, we count d. This reduces the work to enumerating the divisors of x and performing a simple lookup per divisor, which is feasible because each x has at most O(sqrt(x)) divisors.

This approach leverages precomputation and caching, effectively transforming a potentially quadratic check into a set of constant-time checks per divisor. It is a classic application of number-theoretic preprocessing combined with clever state tracking.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * sqrt(x) * n) | O(n) | Too slow |
| Divisor Tracking | O(n * sqrt(x)) | O(max_x) | Accepted |

## Algorithm Walkthrough

1. Precompute divisors of all numbers up to the maximum possible x. We can do this by iterating from 1 to max_x and adding i as a divisor to all multiples of i. This gives O(max_x * log(max_x)) preprocessing. For each query, we can then retrieve divisors of x instantly.
2. Initialize an array or dictionary, `last_seen`, to store the last query index in which each divisor appeared.
3. Process queries sequentially. For query i with values x and y, iterate through all divisors d of x.
4. For each divisor d, check `last_seen[d]`. If it is less than i-y, this means d did not appear in the previous y numbers, and we increment the count.
5. Update `last_seen[d]` to i for all divisors of x, recording the current query index.
6. Print the count for the current query.

This works because the invariant that `last_seen[d]` always stores the most recent query index in which d was a divisor ensures that any divisor appearing in the range x-y to x-1 will be skipped correctly. By tracking indices instead of the full previous numbers, we avoid repeated divisor checks.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX_X = 100000

# Precompute divisors for all numbers up to MAX_X
divisors = [[] for _ in range(MAX_X + 1)]
for i in range(1, MAX_X + 1):
    for j in range(i, MAX_X + 1, i):
        divisors[j].append(i)

def main():
    n = int(input())
    last_seen = [0] * (MAX_X + 1)
    
    for idx in range(1, n + 1):
        x_str, y_str = input().split()
        x = int(x_str)
        y = int(y_str)
        
        count = 0
        for d in divisors[x]:
            if last_seen[d] <= idx - y - 1:
                count += 1
            last_seen[d] = idx
        print(count)

if __name__ == "__main__":
    main()
```

The `divisors` array lets us instantly retrieve all divisors of x, avoiding recomputation. We use 1-based query indexing so that `idx - y - 1` correctly identifies whether the last occurrence of a divisor falls outside the y previous queries. Updating `last_seen[d]` after checking ensures correctness for the next queries.

## Worked Examples

Using the sample input:

```
6
4 0
3 1
5 2
6 2
18 4
10000 3
```

| Query | x | y | Divisors of x | Counted | last_seen after query |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 0 | 1,2,4 | 3 | 1→1, 2→1, 4→1 |
| 2 | 3 | 1 | 1,3 | 1 | 1→2, 3→2 |
| 3 | 5 | 2 | 1,5 | 1 | 1→3, 5→3 |
| 4 | 6 | 2 | 1,2,3,6 | 2 | 1→4,2→4,3→4,6→4 |
| 5 | 18 | 4 | 1,2,3,6,9,18 | 2 | 1→5,2→5,3→5,6→5,9→5,18→5 |
| 6 | 10000 | 3 | 1,2,4,5,... | 22 | updated accordingly |

This trace demonstrates that `last_seen` correctly skips divisors that appeared too recently, and counts all others.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * sqrt(MAX_X)) | Each query processes divisors of x, at most O(sqrt(x)) per query. |
| Space | O(MAX_X) | Storing `last_seen` and divisor lists for all numbers up to MAX_X. |

With n ≤ 10^5 and x ≤ 10^5, O(n * sqrt(MAX_X)) ≈ 10^7 operations, which is well within 5-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided sample
assert run("6\n4 0\n3 1\n5 2\n6 2\n18 4\n10000 3\n") == "3\n1\n1\n2\n2\n22", "sample 1"

# minimum x
assert run("1\n1 0\n") == "1", "minimum x"

# all primes
assert run("3\n2 0\n3 1\n5 2\n") == "2\n1\n1", "primes"

# y=0 edge
assert run("2\n12 0\n7 0\n") == "6\n2", "y zero case"

# large x
assert run("1\n100000 0\n") == "36", "large x with all divisors counted"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 0 | 1 | smallest x value, trivial divisor |
| 3\n2 0\n3 1\n5 2 | 2\n1\n1 | primes and y > 0 skipping |
| 2\n12 0\n7 0 | 6\n2 | y = 0 shortcut handling |
| 1\n100000 0 | 36 | correctness on large x |

## Edge Cases

For a query where y = 0, for example `x = 12, y = 0`, the algorithm retrieves all divisors [1,2,3,4,6,12] and counts them without checking previous queries. `last_seen` updates to the current query index. This produces output 6, which is correct.

For queries with y > 0, for example `x = 5, y = 2` after previous queries 4 and 3, `last_seen[1] = 3` and `last_seen[5] = 2`. Since `idx - y - 1 = 3 - 2 - 1 =
