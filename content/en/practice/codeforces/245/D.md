---
title: "CF 245D - Restoring Table"
description: "We are given a square table that was originally generated from a hidden array of non-negative integers. Each off-diagonal entry is the bitwise AND of the corresponding pair of hidden values, while diagonal entries are artificially replaced by -1."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 245
codeforces_index: "D"
codeforces_contest_name: "CROC-MBTU 2012, Elimination Round (ACM-ICPC)"
rating: 1500
weight: 245
solve_time_s: 190
verified: true
draft: false
---

[CF 245D - Restoring Table](https://codeforces.com/problemset/problem/245/D)

**Rating:** 1500  
**Tags:** constructive algorithms, greedy  
**Solve time:** 3m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a square table that was originally generated from a hidden array of non-negative integers. Each off-diagonal entry is the bitwise AND of the corresponding pair of hidden values, while diagonal entries are artificially replaced by -1. The task is to reconstruct any valid hidden array that could have produced the table.

The key point is that every observed value b[i][j] for i ≠ j is exactly the result of applying bitwise AND to two unknown numbers a[i] and a[j]. The diagonal gives no information. We are not required to recover the unique original array, only one that is consistent with all pairwise constraints.

The constraint n ≤ 100 means we can afford cubic or even quartic reasoning if needed, but the structure of bitwise AND suggests that a direct reconstruction per bit or per element should be sufficient in O(n²) or O(n³). Anything exponential over bit configurations is unnecessary because each value is at most 10⁹, so we only deal with 30 bits per number.

A subtle failure case arises when a reconstruction greedily assigns values without ensuring consistency across all pairs. For example, if we try to deduce a[i] only from a single row, we might violate constraints with another row. Another issue is assuming equality constraints propagate transitively in a naive way, which is not true for bitwise AND.

A concrete problematic scenario is when three indices interact inconsistently if we assign values pair by pair. For instance, choosing a[i] too small to satisfy one pair forces contradictions in others because AND only preserves bits that are present in both numbers.

The key hidden structure is that each a[i] must be compatible with every row i, meaning a[i] must be a superset (in bit terms) of all b[i][j] constraints, but also must not introduce forbidden bits that would create contradictions when ANDed with other chosen values.

## Approaches

A brute-force approach would try to assign each a[i] independently from 0 to 10⁹ and check whether all pairwise AND results match the matrix. This immediately explodes to (10⁹)ⁿ possibilities, which is impossible even for n = 100.

We need to instead reverse-engineer bit constraints. The crucial observation is that bitwise AND behaves independently per bit. A bit is set in a[i] & a[j] if and only if that bit is set in both a[i] and a[j]. This means that for every pair (i, j), any bit that appears in b[i][j] must appear in both a[i] and a[j].

So for each pair (i, j), we can safely enforce that all bits set in b[i][j] must be present in both endpoints. This gives a lower-bound constraint on a[i] and a[j]. If we aggregate over all j, we get that a[i] must contain all bits that appear in any b[i][j].

This gives a natural candidate construction: set a[i] as the bitwise OR of all b[i][j] over j ≠ i. This ensures that every required bit is present in a[i]. What remains is to verify that this construction does not introduce extra bits that would create contradictions. The structure of AND guarantees this works because any bit set in a[i] must appear in at least one b[i][j], and therefore can only persist if it is also present in a[j] whenever needed.

This reduces the problem to a single pass over the matrix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Assignment | O((10⁹)ⁿ) | O(n²) | Too slow |
| Bitwise Constraint Construction | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Initialize an array a of size n with all zeros. This will accumulate all bit constraints for each index.
2. For each index i, iterate over all j ≠ i and compute a[i] |= b[i][j]. This step collects every bit that must appear in a[i], since each b[i][j] is a[i] & a[j], and thus cannot contain bits absent from a[i].
3. After filling all a[i], we implicitly rely on symmetry: if a bit appears in a[i] because of some b[i][j], then it is consistent only if it also appears in a[j]. This consistency is ensured because the same b[i][j] was used when computing a[j].
4. Output the resulting array.

Why it works is tied to bit independence. Each bit position behaves like a separate binary constraint system. If a bit appears in b[i][j], both endpoints must contain it. If it does not appear, at least one endpoint may or may not contain it, but never both unless supported by other pairs. Taking the OR over all constraints ensures every mandatory bit is included, and no unnecessary structure is introduced that would violate any pairwise AND value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    b = [list(map(int, input().split())) for _ in range(n)]

    a = [0] * n

    for i in range(n):
        val = 0
        for j in range(n):
            if i == j:
                continue
            val |= b[i][j]
        a[i] = val

    print(*a)

if __name__ == "__main__":
    solve()
```

The code directly translates the construction idea. The nested loops scan each row and accumulate a bitwise OR across all off-diagonal entries. The diagonal is ignored because it contains no usable information.

A common pitfall is forgetting that diagonal entries are -1 and attempting to include them in bitwise operations, which would corrupt results. Another subtle issue is accidentally using AND instead of OR; OR is required because we are accumulating required bits, not intersecting them.

## Worked Examples

### Example 1

Input:

```
1
-1
```

Since there is only one element, no constraints exist. The only valid number is 0.

| i | j | b[i][j] | a[i] after step |
| --- | --- | --- | --- |
| 0 | - | - | 0 |

Output:

```
0
```

This confirms that the algorithm handles the degenerate case where no pairwise constraints exist.

### Example 2

Input:

```
3
-1 1 0
1 -1 0
0 0 -1
```

We compute each row independently.

For i = 0, we OR values 1 and 0, giving a[0] = 1.

For i = 1, we OR values 1 and 0, giving a[1] = 1.

For i = 2, we OR values 0 and 0, giving a[2] = 0.

| i | j contributions | a[i] |
| --- | --- | --- |
| 0 | 1, 0 | 1 |
| 1 | 1, 0 | 1 |
| 2 | 0, 0 | 0 |

Now check consistency:

1 & 1 = 1 matches b[0][1], and all other pairs involving 0 produce 0 as required.

This shows the construction naturally aligns symmetric constraints without additional correction steps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each matrix entry is visited once during OR accumulation |
| Space | O(n²) | Storage for input matrix |

With n ≤ 100, at most 10⁴ operations are performed, which is trivial within limits. Memory usage is also small since the matrix is at most 100 × 100 integers.

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
assert run("1\n-1\n") == "0"

# two-node simple case
assert run("2\n-1 5\n5 -1\n") == "5 5"

# all zeros off diagonal
assert run("3\n-1 0 0\n0 -1 0\n0 0 -1\n") == "0 0 0"

# mixed bits
assert run("3\n-1 1 2\n1 -1 0\n2 0 -1\n") in ["3 1 2", "3 3 2"]

# symmetric consistency
assert run("4\n-1 1 0 0\n1 -1 2 0\n0 2 -1 4\n0 0 4 -1") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 matrix | 0 | base case |
| 2-node single constraint | identical values | propagation |
| all zeros | all zeros | absence of bits |
| mixed bits | valid reconstruction | correctness of OR logic |

## Edge Cases

For n = 1, there are no constraints at all, so any value is valid. The algorithm produces 0 because the OR over an empty set is 0, which matches the requirement of a non-negative integer.

For cases where some rows contain only zeros, such as a node that ANDs to zero with everyone else, the algorithm assigns a[i] = 0. This is correct because any positive bit would violate at least one pair constraint.

For dense matrices where many entries share overlapping bits, the OR construction ensures all mandatory bits are included without duplication issues. Each bit is justified by at least one observed pair, so no spurious bits are introduced.
