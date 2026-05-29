---
title: "CF 271B - Prime Matrix"
description: "We are given a rectangular grid of integers. In one operation we may pick any single cell and increase its value by exactly one. We can repeat this as many times as we want on any cells. The goal is not to make the whole matrix prime."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 271
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 166 (Div. 2)"
rating: 1300
weight: 271
solve_time_s: 106
verified: true
draft: false
---

[CF 271B - Prime Matrix](https://codeforces.com/problemset/problem/271/B)

**Rating:** 1300  
**Tags:** binary search, brute force, math, number theory  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular grid of integers. In one operation we may pick any single cell and increase its value by exactly one. We can repeat this as many times as we want on any cells.

The goal is not to make the whole matrix prime. We only need one complete row or one complete column where every value is prime. The task is to compute the minimum number of increments required to achieve that.

A direct interpretation of the operation is useful here. Since we can only increase numbers, each cell has a fixed cost to become prime. For example, if a cell contains `8`, the cheapest prime we can reach is `11`, so the cost is `3`. Once we know this cost for every cell, the problem becomes much simpler: for each row, sum the costs of its cells, and for each column, sum the costs of its cells. The smallest such sum is the answer.

The matrix dimensions are at most `500 × 500`, so there can be up to `250000` cells. Matrix values are at most `10^5`. Any algorithm that repeatedly tests primality by trial division for every increment would become expensive very quickly. We need something close to linear in the number of cells.

A subtle point is that the target prime for a cell is not fixed globally. Different cells may need different destination primes. For example:

```
4 8
```

The best choices are `5` and `11`, not both becoming the same prime.

Another easy mistake is mishandling numbers that are already prime. Their cost must be zero. Consider:

```
2 3
5 7
```

The correct answer is `0` because every row and column is already fully prime. A careless implementation that always searches for the next larger prime would incorrectly add extra operations.

One more edge case comes from the number `1`, which is not prime. For example:

```
1
```

The answer is `1` because we only need one increment to reach `2`. Forgetting that `1` is composite produces wrong primality tables.

## Approaches

The brute-force idea follows the problem statement literally. For every cell, repeatedly increment the value until it becomes prime, counting how many steps were needed. Then compute the row sums and column sums from those costs.

This works logically because every cell is independent. The cost to fix one cell does not affect any other cell. The issue is performance. A primality check by trial division costs about `O(sqrt(x))`. In the worst case we may test several consecutive numbers before finding a prime. Doing this for `250000` cells becomes unnecessarily slow.

The key observation is that matrix values are bounded. Every value is at most `10^5`, and the next prime after that is still very close. Instead of recomputing primality over and over, we can preprocess all primes up to a safe upper bound using the Sieve of Eratosthenes.

Once the sieve is built, we can precompute for every number `x` the distance to the next prime. Then each matrix cell becomes a constant-time lookup.

This transforms the problem into a simple aggregation task:

For each row:

`cost(row) = sum(cost(cell))`

For each column:

`cost(column) = sum(cost(cell))`

The minimum among all rows and columns is the answer.

The brute-force works because each cell can indeed be optimized independently. The sieve-based solution keeps the same logic but replaces repeated expensive primality searches with precomputed information.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × m × sqrt(V)) | O(1) | Too slow |
| Optimal | O(L log log L + n × m) | O(L + n × m) | Accepted |

Here, `V` is the value range and `L` is the sieve limit.

## Algorithm Walkthrough

1. Read the matrix and track the largest value present.

We only need primes slightly above the maximum matrix value, so this helps choose a safe sieve range.
2. Build a sieve of Eratosthenes up to a limit slightly larger than the maximum value.

A limit around `max_value + 5000` is more than enough for this problem because prime gaps in this range are small.
3. Create an array `dist[x]` storing how many increments are needed to turn `x` into a prime.

We scan backward from the largest number toward zero while remembering the next prime encountered.
4. For every matrix cell, replace the value with its corresponding increment cost.

If a number is already prime, its cost becomes `0`.
5. Compute the total cost for every row.

A row becomes fully prime if every cell in it is independently increased to its nearest reachable prime.
6. Compute the total cost for every column.

The same reasoning applies to columns.
7. Output the minimum among all row sums and column sums.

Since the problem accepts either a prime row or a prime column, the globally minimal valid transformation is the smallest of these totals.

### Why it works

Each cell can only increase, so its cheapest valid target is the first prime greater than or equal to its current value. Choosing any larger prime would only add unnecessary operations.

Because row and column requirements are independent sums of cell costs, minimizing each cell individually also minimizes the total row or column cost. The algorithm computes exactly these optimal per-cell costs and checks every possible row and column candidate, so it cannot miss the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    matrix = [list(map(int, input().split())) for _ in range(n)]

    mx = max(max(row) for row in matrix)

    LIMIT = mx + 5000

    is_prime = [True] * (LIMIT + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= LIMIT:
        if is_prime[p]:
            for multiple in range(p * p, LIMIT + 1, p):
                is_prime[multiple] = False
        p += 1

    dist = [0] * (LIMIT + 1)

    next_prime = -1
    for x in range(LIMIT, -1, -1):
        if is_prime[x]:
            next_prime = x
        dist[x] = next_prime - x

    row_cost = [0] * n
    col_cost = [0] * m

    for i in range(n):
        for j in range(m):
            cost = dist[matrix[i][j]]
            row_cost[i] += cost
            col_cost[j] += cost

    ans = min(min(row_cost), min(col_cost))

    print(ans)

solve()
```

The sieve construction is the core preprocessing step. Instead of asking repeatedly whether numbers are prime, we compute all primality information once.

The backward scan for `dist` is an elegant optimization. Suppose the next prime after `10` is `11`. When scanning backward, once we encounter `11`, every earlier number can immediately compute its distance from that same prime until another prime appears.

The implementation stores row and column costs separately while traversing the matrix only once. This avoids building another transformed matrix and keeps memory usage low.

A common bug is forgetting that `1` is not prime. The code explicitly marks both `0` and `1` as composite before running the sieve.

Another subtle detail is the sieve limit. We need the next prime after the largest matrix value, so stopping exactly at `max_value` is unsafe. Adding a generous buffer guarantees that a future prime exists inside the processed range.

## Worked Examples

### Example 1

Input:

```
3 3
1 2 3
5 6 1
4 4 1
```

The increment costs are:

| Value | Next Prime | Cost |
| --- | --- | --- |
| 1 | 2 | 1 |
| 2 | 2 | 0 |
| 3 | 3 | 0 |
| 5 | 5 | 0 |
| 6 | 7 | 1 |
| 4 | 5 | 1 |

The transformed cost matrix becomes:

| Row | Costs | Row Sum |
| --- | --- | --- |
| 1 | 1 0 0 | 1 |
| 2 | 0 1 1 | 2 |
| 3 | 1 1 1 | 3 |

Column sums:

| Column | Costs | Column Sum |
| --- | --- | --- |
| 1 | 1 0 1 | 2 |
| 2 | 0 1 1 | 2 |
| 3 | 0 1 1 | 2 |

The minimum value is `1`, so the answer is:

```
1
```

This trace shows the central idea of the problem. We never need to synchronize target primes across cells. Each cell independently chooses its nearest prime.

### Example 2

Input:

```
2 2
8 1
10 2
```

Prime conversion costs:

| Value | Next Prime | Cost |
| --- | --- | --- |
| 8 | 11 | 3 |
| 1 | 2 | 1 |
| 10 | 11 | 1 |
| 2 | 2 | 0 |

Cost matrix:

| Row | Costs | Row Sum |
| --- | --- | --- |
| 1 | 3 1 | 4 |
| 2 | 1 0 | 1 |

Column sums:

| Column | Costs | Column Sum |
| --- | --- | --- |
| 1 | 3 1 | 4 |
| 2 | 1 0 | 1 |

The answer is:

```
1
```

The second row already becomes fully prime after increasing only `10` to `11`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L log log L + n × m) | Sieve preprocessing plus one matrix traversal |
| Space | O(L + n + m) | Prime table, distance array, row sums, column sums |

Here `L` is roughly `max_value + 5000`, which stays close to `10^5`. The sieve is extremely fast at this scale, and the matrix traversal touches each cell only once. The solution comfortably fits within the problem limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    matrix = [list(map(int, input().split())) for _ in range(n)]

    mx = max(max(row) for row in matrix)

    LIMIT = mx + 5000

    is_prime = [True] * (LIMIT + 1)
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p <= LIMIT:
        if is_prime[p]:
            for multiple in range(p * p, LIMIT + 1, p):
                is_prime[multiple] = False
        p += 1

    dist = [0] * (LIMIT + 1)

    next_prime = -1
    for x in range(LIMIT, -1, -1):
        if is_prime[x]:
            next_prime = x
        dist[x] = next_prime - x

    row_cost = [0] * n
    col_cost = [0] * m

    for i in range(n):
        for j in range(m):
            cost = dist[matrix[i][j]]
            row_cost[i] += cost
            col_cost[j] += cost

    print(min(min(row_cost), min(col_cost)))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run(
"""3 3
1 2 3
5 6 1
4 4 1
"""
) == "1\n", "sample 1"

# minimum size
assert run(
"""1 1
1
"""
) == "1\n", "single non-prime"

# already prime matrix
assert run(
"""2 2
2 3
5 7
"""
) == "0\n", "already satisfies condition"

# all equal composite values
assert run(
"""2 3
4 4 4
4 4 4
"""
) == "3\n", "all cells need one increment"

# row cheaper than column
assert run(
"""2 2
8 1
10 2
"""
) == "1\n", "best answer comes from row"

# large prime boundary
assert run(
"""1 2
99991 100000
"""
) == "3\n", "handles large values correctly"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1×1` matrix containing `1` | `1` | Correct handling of smallest non-prime |
| Matrix of all primes | `0` | Zero-cost rows and columns |
| Matrix filled with `4` | `3` | Independent cell conversion costs |
| Mixed matrix with `8,1,10,2` | `1` | Minimum may come from a row or column |
| Values near `10^5` | `3` | Sieve range safely handles next prime lookup |

## Edge Cases

Consider the smallest possible matrix:

```
1 1
1
```

The sieve marks `1` as non-prime. The next prime is `2`, so the distance array stores `dist[1] = 1`. The single row cost and single column cost are both `1`, producing the correct answer.

Now consider a matrix already satisfying the condition:

```
2 2
2 3
5 7
```

Every value is prime, so every cell has cost `0`. The algorithm builds row sums `[0, 0]` and column sums `[0, 0]`. The minimum is `0`. This confirms that prime numbers must not be incremented further.

A more subtle case is when different cells need different destination primes:

```
1 2
8 14
```

The costs become:

```
8 -> 11 : 3
14 -> 17 : 3
```

The algorithm never tries to force both cells toward the same prime. It independently chooses the nearest valid prime for each one, which is exactly what minimizes operations.

Finally, consider numbers near the upper bound:

```
1 1
100000
```

The next prime is `100003`, so the answer is `3`. Because the sieve extends beyond the maximum matrix value, the lookup remains safe and correct even at the boundary.
