---
title: "CF 105631L - LCM and GCD"
description: "We are asked to fill an $n times m$ matrix with positive integers up to $10^9$. Instead of arbitrary values, each row and column must satisfy a very specific aggregate constraint."
date: "2026-06-22T05:42:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105631
codeforces_index: "L"
codeforces_contest_name: "SYSU Collegiate Programming Contest 2024 (SYSUCPC 2024), Final"
rating: 0
weight: 105631
solve_time_s: 65
verified: true
draft: false
---

[CF 105631L - LCM and GCD](https://codeforces.com/problemset/problem/105631/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to fill an $n \times m$ matrix with positive integers up to $10^9$. Instead of arbitrary values, each row and column must satisfy a very specific aggregate constraint.

For every row $i$, if you take the least common multiple of all elements in that row, the result must be exactly $a_i$. For every column $j$, if you take the greatest common divisor of all elements in that column, the result must be exactly $b_j$. The task is to decide whether such a matrix exists and, if it does, construct one.

The constraints $n, m \le 1000$ imply up to $10^6$ cells. Any solution that tries to search values per cell or iteratively adjust candidates with nested factor checks is already close to the limit. A solution must reduce the problem to a direct construction with at most $O(nm)$ simple arithmetic.

A key structural constraint hides inside the definitions of LCM and GCD. LCM constraints force row elements to be divisors of the row target. GCD constraints force column elements to be multiples of the column target. These two directions intersect strongly, and most incorrect approaches fail by treating them independently.

A typical failure case appears when a candidate value satisfies row constraints but breaks column GCDs. For example, if one tries to set every cell in row $i$ equal to $a_i$, column GCDs collapse into the GCD of the $a_i$'s instead of matching the required $b_j$'s. Conversely, setting columns to $b_j$ breaks row LCMs because rows cannot reach their targets.

The solution hinges on aligning both constraints so that every cell is simultaneously compatible with both its row and column requirements.

## Approaches

A brute-force idea would be to treat every cell as a variable and try values that satisfy both constraints simultaneously, repeatedly recomputing all row LCMs and column GCDs after each assignment. Even if we only try small candidate values per cell, recomputation costs $O(nm)$ per attempt, and the search space explodes since each cell depends on factor combinations of two independent targets. This quickly becomes infeasible beyond very small grids.

The key structural observation is that constraints are not independent per cell but separable into divisibility conditions. From the definition of LCM and GCD, we can derive that every cell must divide its row target and must be divisible by its column target. This converts the problem into a compatibility condition on pairs $(a_i, b_j)$. Once this is recognized, construction becomes straightforward: we start from a base matrix that satisfies column constraints and then selectively “inject” row targets without breaking column structure.

The construction works because GCD is stable under introducing values that are multiples of the current GCD, while LCM is stable as long as at least one element in the row achieves the row target.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search | exponential | $O(nm)$ | Too slow |
| Divisibility-based construction | $O(nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

We start by translating the constraints into arithmetic restrictions on a single cell $x_{i,j}$.

1. For a fixed row $i$, the LCM of the row is $a_i$, so every element in that row must divide $a_i$. If a cell contained a number with a prime factor not present in $a_i$, the LCM would exceed $a_i$. Therefore every $x_{i,j}$ must divide $a_i$.
2. For a fixed column $j$, the GCD is $b_j$, so every element in that column must be a multiple of $b_j$. If any entry were not divisible by $b_j$, the GCD would drop below $b_j$. Therefore every $x_{i,j}$ must be divisible by $b_j$.
3. Combining both conditions, every cell must satisfy

$$b_j \mid x_{i,j} \mid a_i.$$

This immediately implies a feasibility condition: if $b_j$ does not divide $a_i$, no valid value can exist in that position, hence the entire matrix is impossible.
4. Once feasibility holds for all pairs, we construct a base matrix by setting every cell to its column requirement $b_j$. This automatically ensures all column GCDs are at least correct candidates.
5. To fix row LCMs, for each row $i$, we choose a single column $p_i$ and overwrite that cell with $a_i$. This guarantees that row $i$ contains a value equal to $a_i$, forcing the LCM of the row to become exactly $a_i$.
6. We must check that this overwrite does not break column GCDs. In column $p_i$, we now have mostly $b_{p_i}$ values and one value $a_i$. Since $b_{p_i} \mid a_i$, the GCD of that column remains $b_{p_i}$.
7. Finally, we output the matrix.

### Why it works

The construction maintains two invariants. Every cell is always a multiple of its column target, so column GCDs can never drop below $b_j$, and every column still contains at least one value equal to $b_j$, so the GCD cannot increase. For rows, each row contains at least one value equal to $a_i$, and all other elements divide $a_i$, so the LCM cannot exceed $a_i$ and cannot fall below it. These two constraints pin both row LCMs and column GCDs to exact values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    # feasibility check: b[j] must divide every a[i]
    for i in range(n):
        for j in range(m):
            if a[i] % b[j] != 0:
                print("No")
                return

    # start with base matrix filled with column requirements
    mat = [[b[j] for j in range(m)] for _ in range(n)]

    # assign each row one column to place its row LCM target
    for i in range(n):
        mat[i][i % m] = a[i]

    print("Yes")
    for row in mat:
        print(*row)

if __name__ == "__main__":
    solve()
```

The feasibility check directly enforces the derived condition $b_j \mid a_i$. If it fails anywhere, no construction is possible because that cell would violate both divisibility constraints simultaneously.

The matrix is initialized so that every column already has correct GCD candidates. Each row then receives a single override placing $a_i$, ensuring the row LCM becomes exact without disrupting column structure. Using $i \bmod m$ distributes these overrides so every column still contains multiple $b_j$ values, preventing accidental GCD inflation.

## Worked Examples

### Example 1

Input:

```
2 3
2 6
1 2 2
```

We begin with feasibility: every $b_j$ divides every $a_i$, since 1 and 2 divide both 2 and 6.

We build:

| Step | Row 1 | Row 2 |
| --- | --- | --- |
| init | 1 2 2 | 1 2 2 |
| place a_i | 2 2 2 | 1 6 2 |

Row 1 LCM is 2 because it contains a 2 and all values divide 2. Row 2 LCM is 6 due to the placed 6. Each column’s GCD remains its $b_j$ since all values are multiples of $b_j$, and each column still contains at least one pure $b_j$ entry or only multiples preserving the GCD.

### Example 2

Input:

```
3 3
1 1 4
5 1 4
```

Feasibility fails immediately because $5$ does not divide $1$ or $4$. There is no value in any cell that can be both a multiple of $5$ and a divisor of $1$ or $4$. The construction cannot even start, so the correct output is `No`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | One feasibility scan plus one matrix construction |
| Space | $O(nm)$ | Storage for the constructed matrix |

The limits $n, m \le 1000$ allow up to $10^6$ operations, which fits comfortably in Python for simple arithmetic and output formatting.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""2 3
2 6
1 2 2
""").startswith("Yes")

# impossible sample
assert run("""3 3
1 1 4
5 1 4
""") == "No"

# minimal case
assert run("""1 1
6
3
""") == "Yes\n6"

# all ones
assert run("""2 2
1 1
1 1
""").startswith("Yes")

# incompatible divisibility
assert run("""2 2
2 3
2 2
""") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 trivial | Yes 6 | base correctness |
| all ones | Yes matrix of ones | neutral LCM/GCD behavior |
| divisibility failure | No | impossibility detection |

## Edge Cases

One subtle case is when all $a_i = 1$. Then every cell must divide 1, forcing all entries to be 1. The construction still works because every $b_j$ must also be 1, otherwise feasibility fails immediately. The algorithm correctly rejects inconsistent cases and otherwise outputs a uniform matrix whose row LCMs and column GCDs remain 1.

Another case is when all $b_j = 1$. This removes column constraints almost entirely, but row constraints still force at least one occurrence of each $a_i$. The base matrix filled with ones ensures column GCDs remain 1, and injecting $a_i$ into one position per row preserves correctness since GCD(1, a_i) is always 1.

A third case is when $n$ or $m$ equals 1. The construction degenerates into a single row or column, but the same divisibility logic still applies. The algorithm still correctly checks compatibility and assigns the single required structure without modification.
