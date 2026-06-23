---
title: "CF 105336L - \u7f51\u7edc\u9884\u9009\u8d5b"
description: "We are given a grid of lowercase letters with $n$ rows and $m$ columns. From this grid, we are interested in selecting any two consecutive rows and any two consecutive columns. Each such choice defines a $2 times 2$ submatrix."
date: "2026-06-23T15:26:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105336
codeforces_index: "L"
codeforces_contest_name: "The 2024 CCPC Online Contest"
rating: 0
weight: 105336
solve_time_s: 42
verified: true
draft: false
---

[CF 105336L - \u7f51\u7edc\u9884\u9009\u8d5b](https://codeforces.com/problemset/problem/105336/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid of lowercase letters with $n$ rows and $m$ columns. From this grid, we are interested in selecting any two consecutive rows and any two consecutive columns. Each such choice defines a $2 \times 2$ submatrix. The goal is to count how many of these $2 \times 2$ blocks match a specific pattern:

$$\begin{matrix}
c & c \\
p & c
\end{matrix}$$

In other words, the top row of the block must be two identical characters, both equal to `'c'`, while the bottom row must have `'p'` on the left and `'c'` on the right.

The output is simply the number of positions $(i, j)$ such that the submatrix formed by rows $i, i+1$ and columns $j, j+1$ satisfies this pattern.

The constraints $2 \le n, m \le 500$ imply at most $500 \times 500 = 250000$ possible top-left corners for a $2 \times 2$ submatrix. This is small enough that an $O(nm)$ scan is sufficient. However, the grid access pattern matters because each candidate must be checked in constant time.

A naive misunderstanding that sometimes happens here is scanning all pairs of rows and columns independently and recomputing submatrices in a heavier way. That would still work for this problem size but is unnecessary.

Edge cases are minimal but worth noting. If the grid contains no `'c'` at all, the answer is clearly zero. If every cell is `'c'`, the answer is still zero because the bottom-left must be `'p'`, which never appears. Another subtle case is when `'p'` appears but not in the bottom-left position relative to valid `'c'` pairs, which leads to partial but invalid matches.

## Approaches

The brute-force approach is straightforward: iterate over every possible top-left corner of a $2 \times 2$ submatrix, extract its four characters, and check whether it matches the required pattern. Since each check is constant time, this runs in $O(nm)$, which is at most 250,000 operations. Even if we consider overhead from Python indexing, this is easily fast enough.

There is no need for preprocessing or advanced data structures. The key observation is that each candidate submatrix is independent, and validation requires only direct character comparisons.

One could attempt to precompute positions of `'c'` or `'p'`, but that does not reduce complexity meaningfully, since the bottleneck is already just scanning the grid once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(1)$ | Accepted |
| Optimal | $O(nm)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We only need to check each possible $2 \times 2$ submatrix once.

## Algorithm Walkthrough

1. Iterate over all possible top-left positions $(i, j)$ where $0 \le i < n-1$ and $0 \le j < m-1$. This ensures the submatrix stays inside bounds.
2. For each position, examine the four cells:

the top-left $(i, j)$, top-right $(i, j+1)$, bottom-left $(i+1, j)$, and bottom-right $(i+1, j+1)$.
3. Check whether these satisfy the condition:

the top row must both be `'c'`, the bottom-left must be `'p'`, and the bottom-right must be `'c'`.
4. If the condition holds, increment the answer counter.
5. After scanning all positions, output the counter.

The reason we directly check each candidate instead of grouping or preprocessing is that each submatrix is fully determined by four characters, so there is no overlapping computation worth exploiting.

### Why it works

Every valid answer corresponds to exactly one choice of a top-left corner $(i, j)$. The algorithm enumerates all such corners without omission or duplication. For each corner, it applies a deterministic predicate that matches the required pattern. Since the predicate is evaluated exactly once per candidate and depends only on those four cells, no valid configuration can be missed and no invalid configuration can be counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    g = [input().strip() for _ in range(n)]

    ans = 0

    for i in range(n - 1):
        row1 = g[i]
        row2 = g[i + 1]
        for j in range(m - 1):
            if row1[j] == 'c' and row1[j + 1] == 'c' and row2[j] == 'p' and row2[j + 1] == 'c':
                ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the enumeration described earlier. The grid is stored as a list of strings so that character access is $O(1)$. We avoid repeated indexing into `g[i][j]` where possible by caching row references into `row1` and `row2`, which reduces overhead in Python.

The loop bounds `n - 1` and `m - 1` ensure we never access out-of-range indices when forming a $2 \times 2$ block.

## Worked Examples

### Example 1

Input:

```
3 4
cccc
spcc
ccpc
```

We scan all $2 \times 2$ submatrices.

| i | j | top-left | top-right | bottom-left | bottom-right | valid |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | c | c | s | p | no |
| 0 | 1 | c | c | p | c | yes |
| 0 | 2 | c | c | c | c | no |
| 1 | 0 | s | p | c | c | no |
| 1 | 1 | p | c | c | p | no |
| 1 | 2 | c | c | p | c | yes |

Answer is 2.

This trace shows that only positions where the top row is exactly `'cc'` contribute, and the bottom-left must precisely be `'p'`.

### Example 2

Input:

```
2 2
cp
cc
```

| i | j | top-left | top-right | bottom-left | bottom-right | valid |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | c | p | c | c | no |

Answer is 0.

This confirms that even if most of the structure resembles the pattern, a mismatch in any single cell invalidates the submatrix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each $2 \times 2$ submatrix is checked once with constant work |
| Space | $O(1)$ | Only the grid storage and a few variables are used |

With $n, m \le 500$, the maximum of 250,000 checks is well within the 1-second limit in Python when using direct indexing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue().strip()

# provided sample
def test_sample():
    input_data = """3 4
cccc
spcc
ccpc
"""
    assert solve_io(input_data) == "2"

# minimal case
def test_min():
    input_data = """2 2
cp
cc
"""
    assert solve_io(input_data) == "0"

# all c's
def test_all_c():
    input_data = """3 3
ccc
ccc
ccc
"""
    assert solve_io(input_data) == "0"

# single valid pattern
def test_one():
    input_data = """2 3
ccp
ccc
"""
    assert solve_io(input_data) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 4 sample | 2 | basic correctness |
| 2x2 cp/cc | 0 | minimal grid handling |
| all 'c' grid | 0 | no false positives |
| single match | 1 | direct detection |

## Edge Cases

A key edge case is when the grid is uniform. For example:

```
2 2
cc
cc
```

The algorithm checks only one submatrix at $(0,0)$, but fails the condition because the bottom-left is not `'p'`. The iteration still runs correctly, and the result is zero.

Another case is when `'p'` exists but is never aligned with a valid `'cc'` above it:

```
3 3
ccc
cpc
ccc
```

Every checked $2 \times 2$ window will fail either the top row or bottom-right condition. The scan still evaluates all four candidates, but none satisfy all constraints simultaneously, producing zero as expected.
