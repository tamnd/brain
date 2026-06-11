---
title: "CF 1136C - Nastya Is Transposing Matrices"
description: "We are given two matrices of the same size, A and B. The allowed operation is surprisingly powerful: we may choose any square submatrix inside A and transpose it. Transposition swaps positions relative to the square's main diagonal."
date: "2026-06-12T04:00:41+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1136
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 546 (Div. 2)"
rating: 1500
weight: 1136
solve_time_s: 109
verified: true
draft: false
---

[CF 1136C - Nastya Is Transposing Matrices](https://codeforces.com/problemset/problem/1136/C)

**Rating:** 1500  
**Tags:** constructive algorithms, sortings  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two matrices of the same size, `A` and `B`.

The allowed operation is surprisingly powerful: we may choose any square submatrix inside `A` and transpose it. Transposition swaps positions relative to the square's main diagonal. We may perform this operation any number of times and on any square sizes.

The task is to determine whether matrix `A` can be transformed into matrix `B`.

The matrix dimensions are at most `500 × 500`, so there can be up to 250,000 cells. Any solution that explicitly simulates sequences of transpositions is immediately suspicious because the number of possible square submatrices is enormous. Even checking all possible operations once would already be too expensive.

The key challenge is understanding what property of the matrix remains unchanged under every allowed operation.

A common mistake is to compare rows or columns independently. Transposition moves elements between rows and columns, so neither row contents nor column contents are preserved.

Another easy trap is assuming that the whole matrix can be rearranged arbitrarily. The operation is flexible, but it still preserves certain structural constraints.

Consider:

```
A:
1 2
3 4

B:
1 3
2 4
```

Output:

```
YES
```

The entire matrix can be transposed once.

Now consider:

```
A:
1 2
3 4

B:
1 4
3 2
```

Output:

```
NO
```

The multisets of matrix elements are identical, but no sequence of allowed transpositions can move elements between arbitrary diagonals. A solution that only compares global frequencies would incorrectly answer YES.

A more subtle example is:

```
A:
1 2 3
4 5 6

B:
1 2 3
4 6 5
```

Output:

```
NO
```

Only the last two elements differ. Since they belong to different preserved diagonal groups, they cannot be exchanged.

Understanding exactly what is preserved is the entire problem.

## Approaches

A brute-force approach would attempt to model transpositions and search for a sequence of operations that transforms `A` into `B`.

This is theoretically correct because every valid transformation could eventually be discovered. Unfortunately, the state space is astronomical. A matrix may contain up to 250,000 elements, and there are roughly `O(nm · min(n,m))` different square submatrices. Exploring operation sequences is completely infeasible.

The breakthrough comes from studying what a transpose actually does to matrix coordinates.

Take a square submatrix whose top-left corner is `(r,c)`. Inside that square, a cell at local coordinates `(x,y)` moves to `(y,x)` after transposition.

Before the move:

```
global row    = r + x
global column = c + y
```

After the move:

```
global row    = r + y
global column = c + x
```

Now examine the value:

```
(row - column)
```

Before:

```
(r + x) - (c + y)
= (r - c) + (x - y)
```

After:

```
(r + y) - (c + x)
= (r - c) + (y - x)
```

Instead of looking at `row - column`, it is easier to look at:

```
row + column
```

Before:

```
(r + x) + (c + y)
= r + c + x + y
```

After:

```
(r + y) + (c + x)
= r + c + x + y
```

The sum `row + column` never changes.

That means every element always stays on the same anti-diagonal.

Every allowed operation merely permutes elements inside one anti-diagonal. It can never move an element to another anti-diagonal.

Now we need one more observation. A transpose of a `2 × 2` square swaps the two off-diagonal elements. Repeated local transpositions allow us to realize arbitrary permutations within a fixed anti-diagonal. Thus the only thing that matters for each anti-diagonal is the multiset of values it contains.

So the problem becomes:

For every anti-diagonal `i + j`, collect all values from `A` and all values from `B`. If the multisets match for every anti-diagonal, the answer is YES. Otherwise it is NO.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / state-space search | Huge | Too slow |
| Optimal | O(nm log(nm)) | O(nm) | Accepted |

## Algorithm Walkthrough

1. For every cell `(i,j)` in matrix `A`, place its value into a container corresponding to anti-diagonal `i + j`.
2. For every cell `(i,j)` in matrix `B`, place its value into another container corresponding to anti-diagonal `i + j`.
3. For each anti-diagonal index from `0` to `n + m - 2`, sort the collected values from `A`.
4. Sort the collected values from `B` for the same anti-diagonal.
5. Compare the two sorted lists.
6. If any anti-diagonal differs, output `"NO"` immediately because some value would need to leave its anti-diagonal, which is impossible.
7. If all anti-diagonals match, output `"YES"`.

### Why it works

Every transpose preserves the quantity `row + column`, so an element never leaves its anti-diagonal. Consequently, the multiset of values on each anti-diagonal is invariant under every allowed operation.

The remaining question is whether matching anti-diagonal multisets are sufficient. They are. Transpositions of square submatrices generate swaps between neighboring positions on the same anti-diagonal, and neighboring swaps generate arbitrary permutations. Any arrangement of values within a fixed anti-diagonal can be reached.

Thus two matrices are mutually reachable exactly when every anti-diagonal contains the same multiset of values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    da = [[] for _ in range(n + m - 1)]
    db = [[] for _ in range(n + m - 1)]

    for i in range(n):
        row = list(map(int, input().split()))
        for j, x in enumerate(row):
            da[i + j].append(x)

    for i in range(n):
        row = list(map(int, input().split()))
        for j, x in enumerate(row):
            db[i + j].append(x)

    for k in range(n + m - 1):
        da[k].sort()
        db[k].sort()
        if da[k] != db[k]:
            print("NO")
            return

    print("YES")

solve()
```

The implementation mirrors the proof directly.

The array index `i + j` identifies an anti-diagonal. Since the largest possible value is

```
(n - 1) + (m - 1) = n + m - 2
```

we need exactly `n + m - 1` containers.

While reading each matrix, every element is appended into the list corresponding to its anti-diagonal. No matrix storage is required after insertion, which keeps the implementation simple.

Sorting converts each anti-diagonal multiset into a canonical representation. Two multisets are equal if and only if their sorted sequences are equal.

The early return after detecting a mismatch avoids unnecessary work.

## Worked Examples

### Example 1

Input:

```
2 2
1 1
6 1
1 6
1 1
```

Anti-diagonals of `A`:

| Cell | i+j | Value |
| --- | --- | --- |
| (0,0) | 0 | 1 |
| (0,1) | 1 | 1 |
| (1,0) | 1 | 6 |
| (1,1) | 2 | 1 |

Anti-diagonals of `B`:

| Cell | i+j | Value |
| --- | --- | --- |
| (0,0) | 0 | 1 |
| (0,1) | 1 | 6 |
| (1,0) | 1 | 1 |
| (1,1) | 2 | 1 |

After sorting:

| Diagonal | A | B |
| --- | --- | --- |
| 0 | [1] | [1] |
| 1 | [1,6] | [1,6] |
| 2 | [1] | [1] |

All match, so the answer is:

```
YES
```

This example shows that values may move within the same anti-diagonal.

### Example 2

```
3 3
1 2 3
4 5 6
7 8 9

1 2 3
4 6 5
7 8 9
```

Collected diagonals:

| Diagonal | A | B |
| --- | --- | --- |
| 0 | [1] | [1] |
| 1 | [2,4] | [2,4] |
| 2 | [3,5,7] | [3,6,7] |
| 3 | [6,8] | [5,8] |
| 4 | [9] | [9] |

Diagonal `2` already differs.

Output:

```
NO
```

This demonstrates that having the same overall set of matrix values is not enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm log(nm)) | Sorting all anti-diagonals together costs at most this much |
| Space | O(nm) | Every matrix element is stored once inside a diagonal list |

There are at most 250,000 elements. Sorting that many values spread across the anti-diagonals easily fits within the 1 second limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())

    da = [[] for _ in range(n + m - 1)]
    db = [[] for _ in range(n + m - 1)]

    for i in range(n):
        row = list(map(int, input().split()))
        for j, x in enumerate(row):
            da[i + j].append(x)

    for i in range(n):
        row = list(map(int, input().split()))
        for j, x in enumerate(row):
            db[i + j].append(x)

    ans = "YES"
    for k in range(n + m - 1):
        if sorted(da[k]) != sorted(db[k]):
            ans = "NO"
            break

    return ans + "\n"

# provided sample
assert run(
"""2 2
1 1
6 1
1 6
1 1
"""
) == "YES\n", "sample 1"

# minimum size
assert run(
"""1 1
5
5
"""
) == "YES\n", "1x1 matrix"

# minimum size mismatch
assert run(
"""1 1
5
7
"""
) == "NO\n", "single cell differs"

# same values globally but wrong diagonal
assert run(
"""2 2
1 2
3 4
1 4
3 2
"""
) == "NO\n", "global multiset equal"

# all values equal
assert run(
"""3 3
7 7 7
7 7 7
7 7 7
7 7 7
7 7 7
7 7 7
"""
) == "YES\n", "all equal"

# rectangular matrix
assert run(
"""2 3
1 2 3
4 5 6
1 4 3
2 5 6
"""
) == "YES\n", "anti-diagonals preserved"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 identical matrices | YES | Smallest possible input |
| 1×1 different matrices | NO | Direct mismatch |
| Same global multiset, different diagonals | NO | Catches incorrect frequency-only solutions |
| All values equal | YES | Duplicate handling |
| Rectangular matrix | YES | Correct indexing of anti-diagonals |

## Edge Cases

### Single-cell matrix

Input:

```
1 1
42
42
```

There is only one anti-diagonal, containing `[42]` in both matrices.

The algorithm builds:

```
diag[0] = [42]
```

for both matrices and returns `YES`.

### Equal global frequencies but impossible transformation

Input:

```
2 2
1 2
3 4

1 4
3 2
```

The anti-diagonals are:

```
A:
0 -> [1]
1 -> [2,3]
2 -> [4]

B:
0 -> [1]
1 -> [4,3]
2 -> [2]
```

After sorting:

```
[2,3] != [3,4]
```

The algorithm returns `NO`.

A solution that only compared the four values `{1,2,3,4}` would incorrectly return `YES`.

### Rectangular matrices

Input:

```
2 3
1 2 3
4 5 6

1 4 3
2 5 6
```

Anti-diagonals:

```
0 -> [1]
1 -> [2,4]
2 -> [3,5]
3 -> [6]
```

The corresponding multisets match exactly.

The algorithm outputs `YES`, showing that the argument depends only on anti-diagonals and does not require the matrix to be square.

### Many duplicate values

Input:

```
3 3
1 1 1
1 2 1
1 1 1

1 1 1
1 2 1
1 1 1
```

Sorting preserves multiplicities. The algorithm compares full sorted lists rather than sets, so repeated values are counted correctly and the answer is `YES`.
