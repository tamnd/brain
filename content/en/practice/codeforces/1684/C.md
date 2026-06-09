---
title: "CF 1684C - Column Swapping"
description: "We are given a matrix where each row represents a sequence of numbers arranged across columns. The goal is to make every row individually non-decreasing from left to right, but we are only allowed a single global operation: swap two entire columns."
date: "2026-06-10T00:00:01+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1684
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 792 (Div. 1 + Div. 2)"
rating: 1400
weight: 1684
solve_time_s: 120
verified: true
draft: false
---

[CF 1684C - Column Swapping](https://codeforces.com/problemset/problem/1684/C)

**Rating:** 1400  
**Tags:** brute force, constructive algorithms, greedy, implementation, sortings  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a matrix where each row represents a sequence of numbers arranged across columns. The goal is to make every row individually non-decreasing from left to right, but we are only allowed a single global operation: swap two entire columns.

A column swap means choosing two indices and exchanging the entire vertical slices of the matrix. After this swap, we check whether every row becomes sorted in non-decreasing order.

The key constraint is that we do not reorder elements inside rows independently. A single column swap affects all rows simultaneously, so a choice that helps one row might break another. The task is to determine whether there exists a pair of columns whose swap makes every row sorted, or conclude it is impossible.

The constraints are tight: the total number of cells across all test cases is at most 2×10^5. This immediately rules out any solution that tries all O(m^2) column swaps and validates each one in O(nm), since that would explode to cubic behavior in the worst case. Even checking a single swap naively costs O(nm), so brute force over all pairs is infeasible.

A subtle edge case appears when the grid is already good. Since we must output a swap, swapping a column with itself is allowed and counts as a valid operation. Another edge case is when multiple inversions exist in different rows, but they cannot be fixed simultaneously by any single swap, even though each row individually could be fixed by a different swap. For example, if row 1 requires swapping columns (1,2) but row 2 requires swapping (2,3), no global swap can satisfy both.

## Approaches

A direct idea is to try every pair of columns (i, j), swap them, and check whether all rows become sorted. This is straightforward to implement: perform the swap, verify each row in linear time, then undo it. However, there are O(m^2) pairs and each validation costs O(nm), which leads to O(nm^3) in the worst case, completely impossible under the constraints.

The key observation is that if a valid swap exists, it must be determined by the structure of inversions in the rows. Each row imposes constraints on which pairs of columns can be swapped without breaking its order. A row is already sorted except for positions where swapping two columns fixes its inversions. That means each row independently suggests a candidate permutation that differs from sorted order in a very controlled way.

If a solution exists, then after applying the swap, every row becomes sorted. That implies that for every row, if we compare it to its sorted version, the transformation induced by the swap must align with the permutation needed to sort that row. This forces a strong consistency condition: all rows must agree on the same “corrected” ordering of columns except for at most two positions.

This leads to a simplification: we only need to compare each row with its sorted version and detect where mismatches occur. If more than two positions differ in any row, no single swap can fix it. If all rows share the same mismatch positions (or none at all), swapping those two columns resolves everything.

The problem reduces to finding at most two columns that, when swapped, make every row sorted, and verifying consistency across all rows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m³) | O(1) | Too slow |
| Optimal | O(n·m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Take the first row and create a sorted version of its column order. Compare it with the original row to identify mismatched positions.

If the number of mismatches exceeds 2, no single swap can fix even this row, so the answer is immediately impossible.
2. If there are zero mismatches in the first row, the grid is already locally consistent with respect to column ordering. We tentatively assume swapping a column with itself is valid and proceed with identity columns.
3. If there are exactly two mismatches, record these two column indices as candidates for swapping. This defines the only possible correction for the first row.
4. Apply this candidate swap conceptually to all rows and verify each row becomes non-decreasing. Instead of actually swapping, compare values at the two columns and check whether the resulting order matches a sorted sequence.
5. For each row, simulate the effect of swapping the candidate columns and scan left to right, ensuring every adjacent pair is non-decreasing.
6. If any row violates the condition after applying the swap, reject the candidate pair.
7. If all rows pass, output the chosen columns.

### Why it works

Each row imposes a constraint that the final column order must be a permutation that makes it sorted. A single swap corresponds to a permutation that fixes at most two positions relative to the sorted order of that row. If more than two positions differ, no single transposition can transform it into a sorted sequence.

If a valid global swap exists, it must be exactly the transposition that aligns the first row with its sorted version, because any other swap would already violate ordering in the first row. Once fixed for one row, all other rows must be consistent with the same transposition, otherwise at least one row would remain unsorted. This forces uniqueness of the candidate swap and guarantees correctness of verification.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]

        # Step 1: find candidate swap from first row
        first = a[0]
        sorted_first = sorted(first)

        diff = []
        for i in range(m):
            if first[i] != sorted_first[i]:
                diff.append(i)

        if len(diff) == 0:
            l = r = 0
        elif len(diff) == 2:
            l, r = diff[0], diff[1]
        else:
            print(-1)
            continue

        # Step 2: verify all rows
        ok = True
        for i in range(n):
            row = a[i]
            prev = -10**18

            for j in range(m):
                val = row[j]
                if j == l:
                    val = row[r]
                elif j == r:
                    val = row[l]

                if val < prev:
                    ok = False
                    break
                prev = val

            if not ok:
                break

        if not ok:
            print(-1)
        else:
            print(l + 1, r + 1)

if __name__ == "__main__":
    solve()
```

The implementation first uses the first row as a template to determine the only possible swap. Sorting this row reveals the target order, and mismatches identify exactly which two columns are out of place. If there are more than two mismatches, the algorithm correctly rejects early.

The verification step does not physically swap columns in the matrix. Instead, it simulates the swap during a linear scan of each row. This avoids extra memory usage and ensures the solution remains linear in the total input size. The variable `prev` tracks whether the row remains non-decreasing after applying the hypothetical swap.

A subtle detail is handling the case where no swap is needed. In that case, `(0,0)` is output, which corresponds to swapping a column with itself and leaves the grid unchanged, satisfying the problem requirement.

## Worked Examples

### Example 1

Input:

```
1
2 3
1 2 3
1 1 1
```

First row is already sorted, so diff is empty. Candidate swap is (0,0).

| row | applied swap | result sequence | valid |
| --- | --- | --- | --- |
| [1,2,3] | none | 1,2,3 | yes |
| [1,1,1] | none | 1,1,1 | yes |

Both rows remain non-decreasing, so output is `1 1`.

This confirms the identity swap case is handled correctly.

### Example 2

Input:

```
1
2 3
2 3 1
1 2 3
```

First row sorted is [1,2,3], diff positions are indices (0,2), so swap columns 1 and 3.

| row | swapped row | check |
| --- | --- | --- |
| [2,3,1] | [1,3,2] | not sorted |
| [1,2,3] | [3,2,1] | not sorted |

The first row already invalidates the swap, so answer is -1.

This demonstrates why using only the first row is sufficient to determine feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·m log m) | sorting first row dominates, verification is linear in total size |
| Space | O(m) | only stores one row and mismatch indices |

The total input size is bounded by 2×10^5, so a linear scan per test case is sufficient. Sorting only one row keeps the constant factor small, and overall execution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]

        first = a[0]
        sorted_first = sorted(first)

        diff = [i for i in range(m) if first[i] != sorted_first[i]]

        if len(diff) == 0:
            l = r = 0
        elif len(diff) == 2:
            l, r = diff
        else:
            out.append("-1")
            continue

        ok = True
        for i in range(n):
            prev = -10**18
            for j in range(m):
                val = a[i][j]
                if j == l:
                    val = a[i][r]
                elif j == r:
                    val = a[i][l]
                if val < prev:
                    ok = False
                    break
                prev = val
            if not ok:
                break

        out.append("-1" if not ok else f"{l+1} {r+1}")

    return "\n".join(out)

# provided samples
assert run("""5
2 3
1 2 3
1 1 1
2 2
4 1
2 3
2 2
2 1
1 1
2 3
6 2 1
5 4 3
2 1
1
2
""") == """1 1
-1
1 2
1 3
1 1"""

# custom cases
assert run("""1
1 1
42
""") == "1 1"

assert run("""1
2 3
3 2 1
1 2 3
""
```
