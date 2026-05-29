---
title: "CF 245D - Restoring Table"
description: "We are given an n x n matrix where every off-diagonal value represents the bitwise AND of two unknown numbers. For every pair of indices i != j: $$b[i][j] = a[i] & a[j]$$ The diagonal entries are all -1 and carry no information."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 245
codeforces_index: "D"
codeforces_contest_name: "CROC-MBTU 2012, Elimination Round (ACM-ICPC)"
rating: 1500
weight: 245
solve_time_s: 93
verified: true
draft: false
---

[CF 245D - Restoring Table](https://codeforces.com/problemset/problem/245/D)

**Rating:** 1500  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an `n x n` matrix where every off-diagonal value represents the bitwise AND of two unknown numbers.

For every pair of indices `i != j`:

$$b[i][j] = a[i] \& a[j]$$

The diagonal entries are all `-1` and carry no information.

Our task is to reconstruct any valid array `a` whose pairwise AND values match the matrix. Multiple answers may exist, and every value must stay within `10^9`.

The constraints are small enough that we can afford quadratic work. With `n <= 100`, even an `O(n^2 * 30)` solution is tiny, since there are only about 300,000 bit operations. A cubic algorithm would also pass, but there is no need for anything heavier.

The tricky part is understanding what information each row gives us about a number.

Suppose we look at some fixed index `i`. Every value `b[i][j]` contains only bits that are present in both `a[i]` and `a[j]`. That means every bit appearing anywhere in row `i` must definitely belong to `a[i]`.

This immediately suggests taking the bitwise OR of the whole row.

For example:

```
a[i] = OR of all b[i][j], j != i
```

Why does this work?

If some bit is present in `a[i]`, then because the original array is guaranteed to exist, there must be at least one other number sharing that bit, otherwise the bit would never appear in any AND result and we could freely remove it from `a[i]`. Since any valid answer is acceptable, keeping exactly the bits visible from pairwise ANDs is enough.

The main edge case is `n = 1`.

Input:

```
1
-1
```

There are no off-diagonal values, so no information exists about the number. Any non-negative integer works. The smallest valid answer is:

```
0
```

A careless implementation that blindly ORs the row would produce an empty OR and may accidentally leave the value uninitialized.

Another subtle case is when many entries are zero.

Example:

```
3
-1 0 0
0 -1 0
0 0 -1
```

A valid answer is:

```
0 0 0
```

If we incorrectly assume every number must contain some bit from another row, we could invent unnecessary bits and break the matrix.

One more important situation is asymmetric bit distribution.

Example:

```
3
-1 1 0
1 -1 0
0 0 -1
```

A correct reconstruction is:

```
1 1 0
```

The third number cannot accidentally inherit bit `1`, because then `a[1] & a[3]` would become nonzero and violate the matrix.

The reconstruction must preserve every pairwise AND exactly, not just approximately.

## Approaches

The brute-force mindset is to reconstruct every bit independently.

For each position `i` and each bit `k`, we try to determine whether bit `k` belongs to `a[i]`. If any matrix entry `b[i][j]` contains bit `k`, then `a[i]` must also contain it. Otherwise the bit is optional.

This already leads to a workable solution because integers only use about 30 bits. We scan every row and accumulate all visible bits.

The brute-force interpretation is still useful conceptually because it explains the exact logical requirement for a bit to exist in a number.

The key observation is that all mandatory bits for `a[i]` are precisely the union of bits appearing in row `i`.

Bitwise OR computes exactly this union.

So instead of reasoning about bits separately, we can directly build:

$$a[i] = b[i][1] \;|\; b[i][2] \;|\; \dots$$

excluding the diagonal.

Now we must justify that this reconstruction preserves every AND value.

Take any bit that appears in `b[i][j]`. Since that bit belongs to both row ORs, it will exist in both `a[i]` and `a[j]`, so it survives in `a[i] & a[j]`.

Take any bit absent from `b[i][j]`. At least one of the original numbers lacked that bit, so the corresponding row never forces it into both reconstructed values simultaneously. The bit cannot appear in the reconstructed AND.

Thus every pairwise AND remains exactly correct.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force bit-by-bit reconstruction | O(n² · 30) | O(n) | Accepted |
| Optimal row-OR construction | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the matrix `b`.
2. Create an array `a` of length `n`, initially filled with `0`.
3. For every row `i`, iterate through every column `j`.
4. Skip the diagonal because `b[i][i] = -1` is not part of the construction.
5. OR every off-diagonal value into `a[i]`.

This collects every bit that must belong to `a[i]`.
6. After processing all rows, print the array `a`.

### Why it works

For every pair `(i, j)`, the value `b[i][j]` contains exactly the bits shared by the original numbers.

When we OR all values from row `i`, every bit that ever participated in an AND with `a[i]` becomes part of the reconstructed `a[i]`.

Now consider a specific bit `k`.

If bit `k` exists in `b[i][j]`, then both reconstructed numbers receive that bit from their row ORs, so the bit appears in `a[i] & a[j]`.

If bit `k` does not exist in `b[i][j]`, then at least one of the two rows never forces that bit into its reconstructed value. The bit cannot appear in both numbers simultaneously, so it stays absent from the AND.

Thus every reconstructed pair satisfies:

$$a[i] \& a[j] = b[i][j]$$

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    b = [list(map(int, input().split())) for _ in range(n)]

    if n == 1:
        print(0)
        return

    a = [0] * n

    for i in range(n):
        for j in range(n):
            if i != j:
                a[i] |= b[i][j]

    print(*a)

solve()
```

The special handling for `n = 1` is necessary because there are no off-diagonal entries to OR together. Any non-negative number would work, and `0` is the simplest choice.

The main loop follows the mathematical construction directly. Each row accumulates all visible bits through the OR operation.

The implementation uses integers directly because Python handles bit operations efficiently and safely within the required range.

One subtle point is skipping the diagonal. If we accidentally OR `-1`, every bit would become set due to two's complement representation, completely corrupting the reconstruction.

## Worked Examples

### Example 1

Input:

```
1
-1
```

Since there are no pairwise relationships, we can output any valid number.

| Step | Action | a |
| --- | --- | --- |
| 1 | Handle `n = 1` | `[0]` |

Output:

```
0
```

This demonstrates the degenerate case where the matrix provides no information.

### Example 2

Input:

```
3
-1 1 3
1 -1 1
3 1 -1
```

### Row construction

| Row i | Values used | OR result |
| --- | --- | --- |
| 0 | `1, 3` | `3` |
| 1 | `1, 1` | `1` |
| 2 | `3, 1` | `3` |

So:

```
a = [3, 1, 3]
```

### Verification

| Pair | Computation | Result |
| --- | --- | --- |
| `(0,1)` | `3 & 1` | `1` |
| `(0,2)` | `3 & 3` | `3` |
| `(1,2)` | `1 & 3` | `1` |

All values match the matrix.

This example shows how a row OR reconstructs exactly the bits needed for every relationship.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | We scan every matrix entry once |
| Space | O(n) | Only the reconstructed array is stored |

With `n <= 100`, the total number of operations is tiny. The solution easily fits within the 2-second limit and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    b = [list(map(int, input().split())) for _ in range(n)]

    if n == 1:
        print(0)
        return

    a = [0] * n

    for i in range(n):
        for j in range(n):
            if i != j:
                a[i] |= b[i][j]

    print(*a)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("1\n-1\n") == "0", "sample 1"

# all zeros
assert run(
    "3\n"
    "-1 0 0\n"
    "0 -1 0\n"
    "0 0 -1\n"
) == "0 0 0", "all zero matrix"

# asymmetric visible bits
assert run(
    "3\n"
    "-1 1 3\n"
    "1 -1 1\n"
    "3 1 -1\n"
) == "3 1 3", "mixed bit structure"

# two elements
assert run(
    "2\n"
    "-1 5\n"
    "5 -1\n"
) == "5 5", "smallest nontrivial case"

# larger repeated values
assert run(
    "4\n"
    "-1 7 7 7\n"
    "7 -1 7 7\n"
    "7 7 -1 7\n"
    "7 7 7 -1\n"
) == "7 7 7 7", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element matrix | `0` | Degenerate case with no constraints |
| All off-diagonal zeros | `0 0 0` | Correct handling of absent bits |
| Mixed bit structure | `3 1 3` | Proper OR reconstruction |
| Two-element matrix | `5 5` | Smallest meaningful AND relationship |
| All values equal | `7 7 7 7` | Stable propagation of shared bits |

## Edge Cases

Consider the single-node case:

```
1
-1
```

The algorithm immediately triggers the special case and outputs:

```
0
```

No AND relationships exist, so any value is valid.

Now consider an all-zero matrix:

```
3
-1 0 0
0 -1 0
0 0 -1
```

Processing rows:

```
Row 0 OR = 0
Row 1 OR = 0
Row 2 OR = 0
```

So the reconstructed array becomes:

```
0 0 0
```

Checking:

```
0 & 0 = 0
```

for every pair, which matches perfectly.

Finally, consider a case where bits are unevenly distributed:

```
3
-1 1 0
1 -1 0
0 0 -1
```

The row ORs are:

```
a[0] = 1
a[1] = 1
a[2] = 0
```

Verification:

```
1 & 1 = 1
1 & 0 = 0
```

The third value correctly remains zero because no row ever forced bit `1` into it. This confirms the reconstruction never invents shared bits that do not exist in the matrix.
