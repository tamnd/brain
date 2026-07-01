---
title: "CF 104493F - New Board Game"
description: "We are given an $n times n$ grid filled with integers from $1$ to $n$. Each value appears exactly $n$ times in total, so the grid is perfectly balanced in terms of frequency, but otherwise arbitrary. We are allowed to apply two global operations any number of times."
date: "2026-06-30T12:23:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104493
codeforces_index: "F"
codeforces_contest_name: "2023 ICPC HIAST Collegiate Programming Contest"
rating: 0
weight: 104493
solve_time_s: 50
verified: true
draft: false
---

[CF 104493F - New Board Game](https://codeforces.com/problemset/problem/104493/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times n$ grid filled with integers from $1$ to $n$. Each value appears exactly $n$ times in total, so the grid is perfectly balanced in terms of frequency, but otherwise arbitrary.

We are allowed to apply two global operations any number of times. One operation shifts every row one step to the right in a cyclic manner, and the other shifts every column one step down in a cyclic manner. These operations affect the entire board uniformly, so they do not modify rows or columns independently, only by global cyclic translations of the grid.

The goal is to determine whether it is possible, after some sequence of these operations, to obtain a “beautiful” grid. A grid is beautiful if every row contains each number from $1$ to $n$ exactly once, and every column also contains each number from $1$ to $n$ exactly once.

The constraints allow $n$ up to 1000, which means the grid can contain up to one million cells. This immediately rules out any approach that tries to simulate many sequences of operations or explore different transformation states. Any correct solution must inspect the grid in essentially linear time with respect to its size.

A key subtlety is that the operations might suggest a complex transformation space, but they are actually very structured: they only perform global cyclic shifts. A common mistake is to assume we can “rearrange” the grid more freely than we actually can.

A few edge cases clarify the structure:

If the grid is already a valid Latin square, then the answer should be YES, since any number of shifts preserves the property.

If all rows are identical, for example:

```
1 2 3 4
1 2 3 4
1 2 3 4
1 2 3 4
```

then no amount of global shifting will make columns valid permutations, so the answer is NO.

A naive misunderstanding would be to think we can align rows and columns independently using shifts. That is not possible because both operations apply globally and uniformly.

## Approaches

A brute-force interpretation would try to simulate all possible sequences of row and column shifts. Each operation changes the grid state, and we might try to test whether any reachable state becomes a Latin square. However, even though there are only $n$ possible shifts in each direction, combining them leads to $n^2$ states, and each check costs $O(n^2)$, resulting in $O(n^4)$ behavior, which is completely infeasible for $n = 1000$.

The key insight is to understand what these operations actually do. A right shift applied to all rows simultaneously is equivalent to a cyclic horizontal translation of the entire grid. A down shift applied to all columns is a cyclic vertical translation. Combining them, any sequence of operations results in a uniform toroidal shift of the grid: every cell is moved by the same offset $(\Delta r, \Delta c)$ modulo $n$.

This means the structure of each row and each column, in terms of which values appear and whether duplicates exist, is invariant under all allowed operations. Shifting cannot introduce or remove duplicates inside a row or column; it only reorders positions.

Therefore, if we ever hope to obtain a grid where every row and column is a permutation, those properties must already hold in the original grid. The operations are too weak to fix any violation of the Latin square conditions.

So the problem reduces to a simple validation: check whether every row contains all numbers from $1$ to $n$ exactly once, and every column also satisfies the same condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over shifts | $O(n^4)$ | $O(n^2)$ | Too slow |
| Check rows and columns | $O(n^2)$ | $O(1)$ or $O(n)$ | Accepted |

## Algorithm Walkthrough

We reduce the problem to verifying a Latin square property.

### Steps

1. Read the grid of size $n \times n$.

We store it as a 2D array because we need direct access to both row-wise and column-wise values.
2. For each row, check whether it contains all integers from $1$ to $n$ exactly once.

This is done using a frequency array or a visited marker array of size $n$.

If any number is missing or duplicated, the grid can never be made valid, because shifts cannot repair row structure.
3. For each column, perform the same check.

This ensures that no value repeats in a column and no value is missing.
4. If both row checks and column checks pass for all indices, output YES. Otherwise output NO.

The important observation is that we never simulate any operation. We only verify whether the grid already satisfies the invariant required by the final state.

### Why it works

The allowed operations are global cyclic shifts. Such shifts only permute positions; they do not change the multiset structure inside any row or column. A row that contains duplicates will always contain duplicates after any sequence of operations, because shifting preserves equality relationships between elements within the same row. The same applies to columns.

Conversely, if every row and every column already forms a permutation, then the grid is already a Latin square, and any cyclic shift preserves that property, so a valid configuration exists trivially.

Thus the condition is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_perm(arr, n):
    seen = [False] * (n + 1)
    for x in arr:
        if x < 1 or x > n:
            return False
        if seen[x]:
            return False
        seen[x] = True
    return True

def main():
    n = int(input())
    a = [list(map(int, input().split())) for _ in range(n)]

    for i in range(n):
        if not is_perm(a[i], n):
            print("NO")
            return

    for j in range(n):
        col = [a[i][j] for i in range(n)]
        if not is_perm(col, n):
            print("NO")
            return

    print("YES")

if __name__ == "__main__":
    main()
```

The row validation is done first because it is slightly cheaper to access memory sequentially, improving cache behavior. The column validation constructs each column explicitly; this is still $O(n^2)$ overall and fits comfortably in the constraints.

A subtle point is that we explicitly check both range validity and duplication. Even though the problem statement guarantees values are in $1$ to $n$, keeping the check makes the logic self-contained and avoids hidden assumption errors.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
3 1 2
2 3 1
```

| Step | Row Check | Column Check | Decision |
| --- | --- | --- | --- |
| 1 | all rows valid | pending | continue |
| 2 | all columns valid | all valid | YES |

This grid is already a Latin square, so every row and column contains a permutation. Any shifts only rotate structure, so validity is preserved.

### Example 2

Input:

```
4
1 2 3 4
1 2 3 4
1 2 3 4
1 2 3 4
```

| Step | Row Check | Column Check | Decision |
| --- | --- | --- | --- |
| 1 | rows valid | pending | continue |
| 2 | column 1 fails | detected | NO |

Each column contains repeated values, so even though rows are permutations, the column condition fails immediately. Since shifts cannot change equality patterns inside a column, there is no way to fix this configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each cell is visited once for row checks and once for column checks |
| Space | $O(1)$ auxiliary (besides input) | Only a fixed-size visited array of size $n$ is used per check |

The grid size reaches up to one million cells, and this solution processes each cell a constant number of times, which fits easily within typical time limits for 1 second constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def is_perm(arr, n):
        seen = [False] * (n + 1)
        for x in arr:
            if x < 1 or x > n:
                return False
            if seen[x]:
                return False
            seen[x] = True
        return True

    n = int(input())
    a = [list(map(int, input().split())) for _ in range(n)]

    for i in range(n):
        if not is_perm(a[i], n):
            return "NO"

    for j in range(n):
        col = [a[i][j] for i in range(n)]
        if not is_perm(col, n):
            return "NO"

    return "YES"

# provided sample
assert run("""3
1 2 3
3 1 2
2 3 1
""") == "YES"

assert run("""4
1 2 3 4
1 2 3 4
1 2 3 4
1 2 3 4
""") == "NO"

# custom cases
assert run("""1
1
""") == "YES", "minimum size"

assert run("""2
1 2
2 1
""") == "YES", "already valid"

assert run("""3
1 1 1
2 2 2
3 3 3
""") == "NO", "row duplicates"

assert run("""3
1 2 3
1 2 3
3 1 2
""") == "NO", "mixed column failure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid | YES | minimum boundary |
| 2x2 swap | YES | simple valid Latin square |
| repeated rows | NO | row duplication detection |
| mixed grid | NO | column failure propagation |

## Edge Cases

A minimal grid of size $1 \times 1$ always passes, since the only row and column trivially contain a permutation of length 1. The algorithm handles this naturally because the frequency check succeeds immediately.

A grid where rows are correct but columns are not, such as identical rows stacked vertically, fails in the column validation phase. The algorithm explicitly constructs each column and detects duplicates, so no transformation is needed to expose the issue.

A grid where columns are correct but rows are not is symmetric and fails in the row validation step first. This early exit prevents unnecessary computation.

A fully valid Latin square remains valid under all checks, confirming that the algorithm does not reject correct configurations.
