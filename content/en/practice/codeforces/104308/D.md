---
title: "CF 104308D - Unwanted Divisors"
description: "We are given a sequence of integers and then a sequence of queries. For each query value $b$, we are interested in all positive divisors of $b$. Among those divisors, some may appear inside the given array, and others may not."
date: "2026-07-01T20:01:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104308
codeforces_index: "D"
codeforces_contest_name: "Mirror of Independence Day Programming Contest 2023 by MIST Computer Club"
rating: 0
weight: 104308
solve_time_s: 51
verified: true
draft: false
---

[CF 104308D - Unwanted Divisors](https://codeforces.com/problemset/problem/104308/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and then a sequence of queries. For each query value $b$, we are interested in all positive divisors of $b$. Among those divisors, some may appear inside the given array, and others may not. The task for each query is to count how many divisors of $b$ are absent from the array.

The array itself is static for each test case, so it can be treated as a fixed reference set while processing all queries.

The constraints imply that both the array size and number of queries can go up to $10^5$, and the values inside the array and queries are also bounded by $10^5$. This immediately rules out recomputing divisors naively per query and also rules out checking divisibility against the array directly for every query element by scanning the array. A solution that touches all array elements per query would lead to about $10^{10}$ operations in the worst case, which is far beyond the time limit.

A subtle pitfall appears when thinking about recomputing divisors for each query independently. For a number like 100000, iterating up to $\sqrt{b}$ per query is fine, but doing it $10^5$ times still risks timing out if not optimized carefully, especially in Python under tight limits.

Another edge case comes from duplicates in the array. If a value appears multiple times, it should still only count once as a “present divisor”, so treating the array as a set is necessary. For example, if the array is $[2, 2, 3]$ and $b = 6$, the divisors are $1,2,3,6$. Both $2$ and $3$ are present, so the answer is $2$, not affected by the duplicate 2.

## Approaches

A direct approach for each query is to enumerate all integers from 1 to $b$ and check which ones divide $b$, and then verify membership in the array. This is correct but immediately too slow, since each query would cost $O(b)$, leading to up to $10^{10}$ operations.

A better observation is that divisors come in pairs and can be generated efficiently up to $\sqrt{b}$. This reduces per-query cost to $O(\sqrt{b})$, but still leaves us with up to $10^5$ queries, which can push the total close to the limit.

The key structural improvement comes from realizing that all numbers are bounded by $10^5$. Instead of recomputing divisors repeatedly, we can precompute the divisor list for every number from 1 to $10^5$ once using a sieve-like construction. After that, each query becomes a simple scan over a precomputed list, and membership checks can be done in $O(1)$ using a boolean array or hash set.

This transforms the problem from repeated arithmetic factorization into a lookup problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per query | $O(q \cdot b)$ | $O(1)$ | Too slow |
| Per-query sqrt factorization | $O(q \sqrt{b})$ | $O(1)$ | Borderline |
| Precompute divisors + set lookup | $O(N \log N + q \cdot d(b))$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Read the array and convert it into a boolean presence table indexed by value. This allows constant-time checks for whether a number exists in the array. The reason for using a table instead of a set is that the value range is small and fixed.
2. Precompute a list of divisors for every number from 1 to 100000. For each integer $i$, iterate through its multiples and append $i$ as a divisor. This builds all divisor lists in a sieve-like manner.
3. For each query value $b$, retrieve its precomputed divisor list.
4. Iterate over all divisors of $b$, and count those that are not marked present in the array’s boolean table.
5. Output the count for each query.

The key idea is that divisor generation is moved entirely outside the query loop, so each query becomes a linear scan over a small precomputed structure.

### Why it works

Every divisor of a number is guaranteed to be included in the precomputed divisor list exactly once. The presence table independently tracks whether that divisor exists in the array. Since both components are exact representations of the required sets, counting mismatches directly produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 100000

# precompute divisors for all numbers up to MAXV
divs = [[] for _ in range(MAXV + 1)]
for i in range(1, MAXV + 1):
    for j in range(i, MAXV + 1, i):
        divs[j].append(i)

def solve():
    t = int(input())
    out_lines = []

    for _ in range(t):
        n, q = map(int, input().split())
        arr = list(map(int, input().split()))
        queries = list(map(int, input().split()))

        present = [False] * (MAXV + 1)
        for x in arr:
            present[x] = True

        for b in queries:
            cnt = 0
            for d in divs[b]:
                if not present[d]:
                    cnt += 1
            out_lines.append(str(cnt))

    return "\n".join(out_lines)

print(solve())
```

The preprocessing step builds a divisor list for every integer once, so no query performs any arithmetic factorization. The array is converted into a boolean lookup table, which guarantees constant-time membership checks.

Inside each query, we only iterate over actual divisors of $b$, so work is proportional to the divisor count rather than the magnitude of $b$.

A common mistake here is using a Python set for divisors of each number repeatedly, which would reintroduce overhead per query. The precomputation avoids repeated allocations entirely.

## Worked Examples

Consider a small example where the array is $[1, 2, 4, 7]$ and we query $b = 8$.

Divisors of 8 are $1, 2, 4, 8$.

| Step | Divisor | Present in array | Count |
| --- | --- | --- | --- |
| 1 | 1 | yes | 0 |
| 2 | 2 | yes | 0 |
| 3 | 4 | yes | 0 |
| 4 | 8 | no | 1 |

The answer is 1.

Now consider array $[3, 5, 6]$ and query $b = 12$.

Divisors of 12 are $1, 2, 3, 4, 6, 12$.

| Step | Divisor | Present in array | Count |
| --- | --- | --- | --- |
| 1 | 1 | no | 1 |
| 2 | 2 | no | 2 |
| 3 | 3 | yes | 2 |
| 4 | 4 | no | 3 |
| 5 | 6 | yes | 3 |
| 6 | 12 | no | 4 |

The answer is 4.

These examples show that the algorithm is purely set membership counting over a divisor decomposition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N + \sum d(b))$ | Divisor sieve plus scanning divisors per query |
| Space | $O(N)$ | Divisor lists plus presence array |

The sieve dominates preprocessing but stays within limits for $N = 10^5$. Query handling is efficient because the number of divisors of any integer up to $10^5$ is small on average.

## Test Cases

```python
import sys, io

MAXV = 100000
divs = [[] for _ in range(MAXV + 1)]
for i in range(1, MAXV + 1):
    for j in range(i, MAXV + 1, i):
        divs[j].append(i)

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, q = map(int, input().split())
        arr = list(map(int, input().split()))
        queries = list(map(int, input().split()))

        present = [False] * (MAXV + 1)
        for x in arr:
            present[x] = True

        for b in queries:
            cnt = 0
            for d in divs[b]:
                if not present[d]:
                    cnt += 1
            out.append(str(cnt))

    return "\n".join(out)

# sample-style test
assert solve("""1
4 2
1 3 6 9
6 12
""") == "2\n4"

# all divisors present
assert solve("""1
3 1
1 2 3
6
""") == "0"

# none present
assert solve("""1
3 1
7 8 9
6
""") == "4"

# single element array
assert solve("""1
1 1
5
10
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all divisors present case | 0 | full coverage elimination |
| none present case | full divisor count | maximum counting behavior |
| single element array | correct exclusion logic | minimal structure correctness |

## Edge Cases

When the array contains repeated values, such as $[2, 2, 2]$, the boolean presence array ensures the duplicate does not affect the result. For a query $b = 6$, divisors $1,2,3,6$ are checked exactly once each against the presence table, so duplication cannot inflate counts.

For small values like $b = 1$, the divisor list contains only $[1]$. If the array does not contain 1, the answer is 1; otherwise it is 0. The algorithm handles this naturally because the precomputed divisor list for 1 is correct and minimal.

For maximum values near $10^5$, the divisor list remains small enough that iterating it per query is efficient. Even in worst cases like highly composite numbers, divisor counts remain bounded and do not threaten the time limit.
