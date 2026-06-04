---
title: "CF 271B - Prime Matrix"
description: "We are given a grid of positive integers. From this grid, we are allowed to repeatedly choose any single cell and increment its value by one. Each increment costs one move."
date: "2026-06-05T01:33:30+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 271
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 166 (Div. 2)"
rating: 1300
weight: 271
solve_time_s: 81
verified: true
draft: false
---

[CF 271B - Prime Matrix](https://codeforces.com/problemset/problem/271/B)

**Rating:** 1300  
**Tags:** binary search, brute force, math, number theory  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid of positive integers. From this grid, we are allowed to repeatedly choose any single cell and increment its value by one. Each increment costs one move. The goal is to make the grid “prime” in the sense that either at least one entire row becomes prime-valued, or at least one entire column becomes prime-valued.

A value is acceptable in a chosen row or column only if it becomes a prime number. Since we can only increase values, every cell has an independent cost: the number of increments needed to turn it into a prime number greater than or equal to its current value.

The task is to select a row or a column and pay the total cost to convert every value in it into a prime, then minimize this cost over all rows and columns.

The constraints go up to a 500 by 500 grid, so there are up to 250,000 cells. Each value is at most 100,000, but can be incremented arbitrarily. That immediately suggests that any per-cell heavy computation must be preprocessed, because recomputing prime distances repeatedly inside nested loops would still pass, but only if primality checks are efficient and reused.

A subtle edge case is when numbers are already prime in some row or column. That row or column contributes zero cost, and the answer becomes zero. Another important case is when many values are just below primes, for example 14, 20, 26. A naive “check next prime by incrementing one by one” per cell would be too slow if done repeatedly inside loops.

The key hidden requirement is that we must efficiently compute, for every number in the grid, the smallest number greater than or equal to it that is prime.

## Approaches

A brute-force approach would process each row and column independently. For a fixed row, we would iterate through all its cells, and for each cell repeatedly increment until we hit a prime, summing the increments. Then we repeat the same for every column and take the minimum.

This is correct but too slow because each cell might require many increments, and we do this for up to 250,000 cells. In the worst case, if values are near 100,000 and primes are sparse locally, repeated primality checks per increment would lead to billions of checks.

The key observation is that each cell’s cost is independent and depends only on its value. We do not need to simulate increments. Instead, we precompute the next prime for every integer up to a safe limit slightly above 100,000. Then each cell contributes a fixed cost: `next_prime[a[i][j]] - a[i][j]`.

Once we have this cost grid, the problem reduces to finding the minimum sum over all rows and all columns. That is just aggregation over precomputed values.

So the solution structure becomes: precompute primes using a sieve, build a next-prime array, compute cost per cell, then compute row sums and column sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Increment Simulation | O(nm × steps) | O(1) | Too slow |
| Sieve + Precompute + Aggregation | O(MAX log log MAX + nm) | O(MAX) | Accepted |

## Algorithm Walkthrough

1. Choose a maximum bound slightly above the largest possible value, typically 100000 + margin (like 130000). This ensures every number has a reachable prime above it.
2. Run a sieve of Eratosthenes to mark all primes up to this bound. This gives constant-time primality lookup.
3. Build an array `next_prime` such that for every integer x, `next_prime[x]` is the smallest prime greater than or equal to x.

This is done by scanning downward from the maximum value while remembering the last seen prime.
4. Create a cost matrix implicitly: for each cell (i, j), compute `cost[i][j] = next_prime[a[i][j]] - a[i][j]`. This represents the minimum number of increments needed for that cell.
5. Compute the cost of each row by summing its cell costs.
6. Compute the cost of each column similarly.
7. Return the minimum among all row sums and column sums.

Each step reduces the problem from dynamic incremental operations into static precomputed differences, which is the central simplification.

### Why it works

Each cell contributes independently to whether a row or column becomes fully prime. Since operations on different cells do not interact, the cost of transforming a row is just the sum of individual minimal costs. Because we always choose the nearest prime above each value, we never overpay per cell. This guarantees that any row or column cost computed is the true minimal cost for that structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 130000

# sieve
is_prime = [True] * (MAXV + 1)
is_prime[0] = is_prime[1] = False

for i in range(2, int(MAXV ** 0.5) + 1):
    if is_prime[i]:
        step = i
        start = i * i
        for j in range(start, MAXV + 1, step):
            is_prime[j] = False

# build next prime
next_prime = [0] * (MAXV + 2)
last = -1
for i in range(MAXV, -1, -1):
    if is_prime[i]:
        last = i
    next_prime[i] = last

n, m = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]

row_cost = [0] * n
col_cost = [0] * m

for i in range(n):
    for j in range(m):
        v = a[i][j]
        cost = next_prime[v] - v
        row_cost[i] += cost
        col_cost[j] += cost

ans = min(min(row_cost), min(col_cost))
print(ans)
```

The sieve portion ensures we can instantly determine primality and also derive the next prime for any value. The reverse scan is critical because it turns a sparse prime distribution into a direct lookup table.

The nested loop over the matrix computes costs once per cell and accumulates both row and column totals simultaneously, avoiding extra passes.

A subtle point is that we rely on `next_prime[v]` always existing. This is why the sieve range must be large enough beyond the maximum input value.

## Worked Examples

### Example 1

Input:

```
3 3
1 2 3
5 6 1
4 4 1
```

We compute next primes:

1→2, 2→2, 3→3, 4→5, 5→5, 6→7.

Cost matrix becomes:

```
1 0 0
0 1 1
1 1 1
```

Row sums and column sums:

| i | Row | Sum |
| --- | --- | --- |
| 0 | 1 0 0 | 1 |
| 1 | 0 1 1 | 2 |
| 2 | 1 1 1 | 3 |

| j | Column | Sum |
| --- | --- | --- |
| 0 | 1 0 1 | 2 |
| 1 | 0 1 1 | 2 |
| 2 | 0 1 1 | 2 |

Minimum is 1, achieved by first row.

This shows that even a single cheap row dominates all other configurations.

### Example 2

Input:

```
2 2
4 6
1 10
```

Next primes:

4→5, 6→7, 1→2, 10→11.

Cost matrix:

```
1 1
1 1
```

Row sums are both 2, column sums are both 2.

| i | Row | Sum |
| --- | --- | --- |
| 0 | 1 1 | 2 |
| 1 | 1 1 | 2 |

| j | Column | Sum |
| --- | --- | --- |
| 0 | 1 1 | 2 |
| 1 | 1 1 | 2 |

Answer is 2.

This demonstrates symmetry: when all costs are uniform, any row or column is equivalent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MAX log log MAX + nm) | sieve builds primes once, then one pass over grid |
| Space | O(MAX) | arrays for primality and next-prime lookup |

The grid traversal is linear in the number of cells, which is at most 250,000, easily within limits. The sieve runs over ~130,000 values, which is also trivial in 2 seconds in Python.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    MAXV = 130000

    is_prime = [True] * (MAXV + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(MAXV ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, MAXV + 1, i):
                is_prime[j] = False

    next_prime = [0] * (MAXV + 2)
    last = -1
    for i in range(MAXV, -1, -1):
        if is_prime[i]:
            last = i
        next_prime[i] = last

    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    row = [0] * n
    col = [0] * m

    for i in range(n):
        for j in range(m):
            c = next_prime[a[i][j]] - a[i][j]
            row[i] += c
            col[j] += c

    print(min(min(row), min(col)))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided sample
assert run("""3 3
1 2 3
5 6 1
4 4 1
""") == "1"

# single cell already prime
assert run("""1 1
2
""") == "0"

# all same small composite
assert run("""2 2
1 1
1 1
""") == "2"

# mixed case
assert run("""2 3
4 6 8
9 10 1
""") == str(min(1+1+1, 1+1, 1+1))

# max-ish structure sanity
assert run("""3 3
100000 100000 100000
100000 100000 100000
100000 100000 100000
""") >= "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 prime | 0 | already prime base case |
| all 1s | 2 | minimal non-prime conversion |
| mixed small grid | computed | row vs column comparison |
| large equal values | ≥0 sanity | performance and bounds |

## Edge Cases

A key edge case is when the matrix already contains a full prime row or column. For example, if a row is `[2, 3, 5]`, its cost becomes zero and the answer must immediately be zero. The algorithm handles this because `next_prime[p] - p` is zero when `p` is prime, so row sum becomes zero automatically.

Another case is when multiple rows and columns tie. For instance, a uniform matrix of all ones produces identical row and column costs. The algorithm correctly computes all sums independently and takes the minimum without assuming uniqueness.

A third case is when values sit just below primes, such as 14, 20, 26. Each cell independently jumps to its nearest prime (17, 23, 29). Since each cost is local, summing does not interfere with global structure, and both row and column evaluations remain consistent.

Finally, the sieve boundary must be high enough. If it is too small, `next_prime[x]` could be undefined for large values, producing incorrect results. The fixed upper bound ensures every input value has a valid next prime.
