---
title: "CF 1166B - All the Vowels Please"
description: "We are trying to construct a string of length $k$ that can be rearranged into a rectangular grid with $n$ rows and $m$ columns such that every row and every column contains all five vowels: a, e, i, o, u at least once."
date: "2026-06-12T02:13:04+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1166
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 561 (Div. 2)"
rating: 1100
weight: 1166
solve_time_s: 91
verified: true
draft: false
---

[CF 1166B - All the Vowels Please](https://codeforces.com/problemset/problem/1166/B)

**Rating:** 1100  
**Tags:** constructive algorithms, math, number theory  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are trying to construct a string of length $k$ that can be rearranged into a rectangular grid with $n$ rows and $m$ columns such that every row and every column contains all five vowels: a, e, i, o, u at least once.

The construction rule fixes how the string is mapped into the grid: we fill row by row from left to right. So the first $m$ characters form row 1, the next $m$ form row 2, and so on. Once placed into this grid, we are not allowed to rearrange the characters, so the final grid structure is fully determined by the string.

The key requirement is very strong: every row must contain all five vowels, and every column must also contain all five vowels. This immediately forces both dimensions $n$ and $m$ to be at least 5, otherwise a row or column cannot possibly contain all vowels.

The input is only the integer $k$, and we must decide whether such a grid exists for any factorization $k = n \cdot m$, and if it does, output any valid string that works. Otherwise, output -1.

The constraint $k \le 10^4$ means we can safely try all divisors of $k$ in $O(\sqrt{k})$, since at most about 100 candidates exist. Anything quadratic in $k$ would be unnecessary but still borderline acceptable; anything exponential is irrelevant.

The main subtlety is that the condition is not local to rows or columns independently. A naive attempt might ensure rows contain all vowels, but columns will fail unless the construction is carefully periodic.

A few edge cases highlight the structure:

When $k = 7$, no factorization produces both $n \ge 5$ and $m \ge 5$, so the answer is impossible even though $k$ is not small.

When $k = 25$, we can take $n = 5, m = 5$, and construct a valid grid.

The core challenge is to understand what structure guarantees both row-wise and column-wise completeness simultaneously.

## Approaches

A brute-force idea would be to try every factorization $k = n \cdot m$, and for each pair attempt to construct a grid. For each candidate grid, we could try filling it randomly or via backtracking to ensure every row and column contains all five vowels. However, even for a single fixed pair, the search space is enormous: each cell has 5 choices, so the number of grids is $5^{nm}$, which is completely infeasible even for moderate sizes.

The key observation is that the requirement “every row contains all vowels” already forces a strong structure: each row must contain at least 5 distinct characters, so $m \ge 5$. Similarly, each column must have height at least 5, so $n \ge 5$. This reduces the problem to finding a factorization $k = n \cdot m$ with both $n \ge 5$ and $m \ge 5$.

Once such a factorization exists, we can construct a periodic 5-by-5 pattern of vowels and tile it across the grid. A 5x5 Latin-style cyclic construction ensures each row and column contains all vowels exactly once, and repeating it across multiples of 5 preserves the property. The rest of the grid is just repetition of this base structure.

So the problem reduces entirely to number theory: does $k$ have a divisor $m$ such that both $m \ge 5$ and $k/m \ge 5$?

If yes, we construct the grid; otherwise, we output -1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (grid search) | Exponential $O(5^{k})$ | $O(k)$ | Too slow |
| Divisor + construction | $O(\sqrt{k})$ | $O(k)$ | Accepted |

## Algorithm Walkthrough

We want to find a valid rectangle size and then fill it in a structured way.

1. Iterate over all divisors $m$ of $k$. For each divisor, compute $n = k / m$. We only care about pairs where both $n \ge 5$ and $m \ge 5$, because smaller dimensions make it impossible to fit all five vowels in a row or column.
2. Once we find such a pair, we fix it as our grid dimensions. This step is justified because any valid solution must correspond to some factorization of $k$.
3. Build a 5x5 base pattern using a cyclic shift of vowels. The idea is to arrange vowels so that each row is a rotation of "aeiou", and each column also cycles through all vowels.
4. Extend this 5x5 block to an $n \times m$ grid by repeating rows and columns modulo 5. Concretely, cell $(i, j)$ is assigned vowel based on $(i \bmod 5, j \bmod 5)$.
5. Flatten the grid row by row into a string of length $k$.

If no valid factorization is found, we return -1.

### Why it works

The construction guarantees that every row consists of repeating a permutation of the five vowels in a cycle of length 5. Since each row is built from the same cyclic structure, every row contains all vowels at least once. The same applies to columns because the column pattern is identical up to cyclic shift. The periodicity ensures that extending the base 5x5 structure preserves both row-wise and column-wise completeness regardless of how many blocks are repeated.

The invariant is that every 5 consecutive positions in any row or column contain a permutation of the vowels, and this property is preserved under repetition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input().strip())
    
    vowels = "aeiou"
    
    # find valid factorization n x m
    n = m = -1
    for i in range(5, int(k**0.5) + 1):
        if k % i == 0:
            j = k // i
            if j >= 5:
                n, m = i, j
                break
            if i >= 5:
                n, m = j, i
    
    if n == -1:
        print(-1)
        return
    
    # build grid using cyclic pattern
    grid = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(vowels[(i + j) % 5])
        grid.append(row)
    
    # flatten
    res = []
    for i in range(n):
        res.extend(grid[i])
    
    print("".join(res))

if __name__ == "__main__":
    solve()
```

The code begins by selecting a valid factorization of $k$. It only accepts dimensions where both sides are at least 5, because smaller sizes immediately violate the requirement that a row or column must contain all five vowels.

The grid construction uses a diagonal cyclic shift: entry $(i, j)$ is determined by $(i + j) \bmod 5$. This ensures that moving right or down cycles through vowels in a fixed permutation, guaranteeing coverage in every row and column.

Finally, the grid is flattened in row-major order, matching the problem’s input-to-grid mapping.

## Worked Examples

### Example 1: k = 7

There is no factorization of 7 where both sides are at least 5. The only pairs are (1,7) and (7,1), both invalid.

| Step | n | m | Valid? | Action |
| --- | --- | --- | --- | --- |
| check 1×7 | 1 | 7 | no | row too small |
| check 7×1 | 7 | 1 | no | column too small |

The algorithm finds no valid grid and outputs -1. This matches the requirement since a single row or column cannot contain all five vowels.

### Example 2: k = 25

We can choose $n = 5, m = 5$.

| i | j | (i+j)%5 | letter |
| --- | --- | --- | --- |
| 0 | 0 | 0 | a |
| 0 | 1 | 1 | e |
| 0 | 2 | 2 | i |
| 0 | 3 | 3 | o |
| 0 | 4 | 4 | u |

Row 0 already contains all vowels. Every other row is a cyclic shift of this one.

The same pattern holds for columns because column $j$ is also a cyclic shift across rows.

The flattened string of length 25 is valid by construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{k})$ | We test divisor candidates up to $\sqrt{k}$ |
| Space | $O(k)$ | We explicitly build the resulting string of length $k$ |

The bound $k \le 10^4$ makes the divisor search trivial, and constructing a linear-size output is optimal since we must print $k$ characters anyway.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    
    # assuming solve() is defined above
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample
assert run("7\n") == "-1"

# k is valid square
assert len(run("25\n")) == 25

# smallest impossible
assert run("1\n") == "-1"

# prime > 5
assert run("11\n") == "-1"

# valid non-square factorization
assert len(run("30\n")) == 30
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 7 | -1 | impossible factorization |
| 25 | length 25 string | valid square construction |
| 1 | -1 | minimal edge case |
| 11 | -1 | prime case |
| 30 | length 30 string | rectangular valid case |

## Edge Cases

For $k = 1$, the algorithm immediately fails to find any divisor pair with both sides ≥ 5, so it returns -1. This is correct because a single character cannot satisfy even one row requirement.

For prime values like $k = 11$, the only factorizations are (1,11) and (11,1), both invalid. The divisor scan detects this cleanly.

For composite values like $k = 30$, we can choose $5 \times 6$. The construction uses a 5-cycle pattern, and both row and column completeness holds because both dimensions exceed or equal 5, allowing full cycles in both directions.
