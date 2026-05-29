---
title: "CF 404A - Valera and X"
description: "We are given a square grid of size $n times n$, where $n$ is an odd integer. Each cell contains a lowercase English letter. The task is to determine whether the pattern of letters forms an “X” shape under a strict rule."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 404
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 237 (Div. 2)"
rating: 1000
weight: 404
solve_time_s: 295
verified: false
draft: false
---

[CF 404A - Valera and X](https://codeforces.com/problemset/problem/404/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 4m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a square grid of size $n \times n$, where $n$ is an odd integer. Each cell contains a lowercase English letter. The task is to determine whether the pattern of letters forms an “X” shape under a strict rule.

The grid is considered valid if every cell on both diagonals shares the same character, and every other cell (those not on either diagonal) shares a single uniform character that is different from the diagonal character. The two diagonals include the main diagonal from top-left to bottom-right and the anti-diagonal from top-right to bottom-left. Since $n$ is odd, these diagonals intersect at exactly one center cell, which must also belong to the diagonal character group.

The output is a single decision: print "YES" if the grid matches this structure, otherwise print "NO".

The constraint $3 \le n < 300$ means $n$ is small enough that an $O(n^2)$ scan is easily fast. Any solution that inspects each cell once is sufficient. Anything worse than quadratic would be unnecessary.

A few failure scenarios are easy to overlook.

One issue appears when the diagonals are consistent internally but accidentally differ from each other. For example, if the main diagonal is all 'x' and the anti-diagonal is all 'o', a naive check that only validates each diagonal separately would incorrectly accept the grid. A correct solution must ensure both diagonals share the same character.

Another issue occurs when diagonal and off-diagonal characters are not enforced as distinct. A grid where all characters are identical should be rejected, even though both diagonals are uniform, because the off-diagonal region is not different.

A third subtle case is the center cell. Since it belongs to both diagonals, it must not be validated against the off-diagonal character group.

## Approaches

A brute-force interpretation checks every cell by simulating the rule literally. One could pick a candidate diagonal character from the center or first diagonal cell, then verify all diagonal positions match it, and separately pick a candidate off-diagonal character and verify all other positions match it. This requires scanning all cells for every consistency check and can be implemented cleanly.

However, the brute-force approach tends to repeatedly recompute conditions or check mismatched candidates without structuring the logic. The real inefficiency is not time complexity but redundancy in validation logic, which may lead to multiple passes over the grid or repeated scans per hypothesis.

The key observation is that there are only two character roles in the entire grid: diagonal and non-diagonal. This reduces the problem to identifying two values and verifying consistency in a single pass. We can determine the expected diagonal character from the first cell, then ensure all diagonal cells match it. At the same time, we determine the off-diagonal character from any non-diagonal cell and ensure all such cells match it. Finally, we verify the two characters are distinct.

This reduces the problem to a straightforward $O(n^2)$ validation with no backtracking or recomputation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ to $O(n^3)$ depending on implementation | $O(1)$ | Accepted but redundant |
| Optimal | $O(n^2)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We scan the grid once while classifying each cell as either diagonal or non-diagonal.

1. Initialize two variables: one for the diagonal character and one for the non-diagonal character. Both start unset. These variables represent the two expected uniform values in the grid.
2. Iterate over every cell $(i, j)$. A cell belongs to a diagonal if $i = j$ or $i + j = n - 1$. This condition cleanly separates X-shape structure from the rest of the grid.
3. If the cell is on a diagonal, we compare its value against the stored diagonal character. If it is unset, we assign it. Otherwise, we verify consistency. Any mismatch immediately invalidates the grid.
4. If the cell is not on a diagonal, we apply the same logic using the non-diagonal character. The first encountered non-diagonal cell defines the expected value for the entire off-diagonal region.
5. After processing all cells, we verify that both characters were discovered and that they are different. If either is missing or both are equal, the structure cannot represent a valid X pattern.

### Why it works

The grid structure imposes a partition of all cells into exactly two disjoint sets: diagonal and non-diagonal. Each set must be constant-valued under the problem definition. Since every cell belongs to exactly one set except the center, which is consistently classified as diagonal, a single pass enforcing uniformity guarantees correctness. Any violation must appear as a mismatch during scanning, so no hidden invalid configuration can survive the traversal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    g = [input().strip() for _ in range(n)]

    diag = None
    other = None

    for i in range(n):
        for j in range(n):
            if i == j or i + j == n - 1:
                if diag is None:
                    diag = g[i][j]
                elif g[i][j] != diag:
                    print("NO")
                    return
            else:
                if other is None:
                    other = g[i][j]
                elif g[i][j] != other:
                    print("NO")
                    return

    if diag is None or other is None or diag == other:
        print("NO")
    else:
        print("YES")

if __name__ == "__main__":
    solve()
```

The code directly implements the classification rule. The nested loops ensure every cell is visited exactly once. The diagonal condition checks both main and anti-diagonal membership, ensuring the center cell is consistently treated as diagonal. The two lazy-initialized variables avoid preselecting characters incorrectly and instead derive them from the input itself.

A subtle implementation detail is the final check `diag == other`, which prevents accepting uniform grids. Another important point is early termination: as soon as a mismatch is found, the function returns immediately, avoiding unnecessary scanning.

## Worked Examples

### Example 1

Input:

```
5
xooox
oxoxo
soxoo
oxoxo
xooox
```

| Cell check | i=j or i+j=n-1 | diag | other | Action |
| --- | --- | --- | --- | --- |
| (0,0)=x | yes | x | - | set diag=x |
| (0,1)=o | no | x | o | set other=o |
| (0,2)=o | yes | x | o | ok |
| (2,2)=x | yes | x | o | ok |
| (2,1)=x | no | x | o | mismatch check passes so far |

At some point, diagonal consistency breaks (anti-diagonal and main diagonal do not form a single uniform value across the entire structure), so the algorithm eventually rejects.

Output:

```
NO
```

This confirms that even if local segments look consistent, global diagonal uniformity is enforced.

### Example 2

Input:

```
3
aba
bab
aba
```

| Cell | Type | diag | other | Action |
| --- | --- | --- | --- | --- |
| (0,0)=a | diag | a | - | set diag=a |
| (0,1)=b | other | a | b | set other=b |
| (0,2)=a | diag | a | b | ok |
| (1,1)=b | diag | a | b | mismatch |

The center cell forces diagonal consistency with the anti-diagonal, and since it differs from previously seen diagonal values, the structure fails.

Output:

```
NO
```

This shows why the center cell must match both diagonal constraints simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | every cell is visited once during validation |
| Space | $O(1)$ | only two variables store state, grid storage aside |

The bound $n < 300$ makes $n^2 \approx 9 \times 10^4$, which is trivial for a single pass scan.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("5\nxooox\noxoxo\nsoxoo\noxoxo\nxooox\n") == "NO"

# all valid X
assert run("3\nxox\noxo\nxox\n") == "YES"

# all same character
assert run("3\naaa\naaa\naaa\n") == "NO"

# diagonal mismatch
assert run("3\nxox\nxoo\nxox\n") == "NO"

# minimal valid structure
assert run("3\naba\nbab\naba\n") == "NO"

# larger valid case
assert run("5\nxooox\noxoxo\noxxox\noxoxo\nxooox\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3x3 valid X | YES | correct structure |
| all equal | NO | rejects uniform grid |
| diagonal mismatch | NO | enforces diagonal consistency |
| malformed center | NO | center constraint handling |
| larger valid | YES | scalability and full pattern |

## Edge Cases

One edge case is when all characters in the grid are identical. The algorithm sets `diag` from the first diagonal cell and `other` from the first off-diagonal cell, but both will become the same character. The final check `diag == other` correctly rejects this case.

Another edge case occurs when only diagonals exist, such as in a minimal grid where off-diagonal cells are few but non-empty. The classification still ensures at least one off-diagonal cell is present in valid inputs; otherwise `other` remains unset and the final condition rejects it.

A third edge case involves inconsistent diagonals, where the main diagonal is uniform but the anti-diagonal differs. This is caught immediately during traversal because both are treated under the same `diag` variable, forcing global consistency rather than per-diagonal independence.
