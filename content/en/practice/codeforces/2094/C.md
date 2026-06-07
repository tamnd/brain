---
title: "CF 2094C - Brr Brrr Patapim"
description: "We are given an $n times n$ grid that was generated from an unknown permutation $p$ of length $2n$. The construction rule is simple: the value in cell $(i,j)$ is $p{i+j}$."
date: "2026-06-08T05:34:04+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 2094
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1017 (Div. 4)"
rating: 900
weight: 2094
solve_time_s: 138
verified: false
draft: false
---

[CF 2094C - Brr Brrr Patapim](https://codeforces.com/problemset/problem/2094/C)

**Rating:** 900  
**Tags:** math  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an $n \times n$ grid that was generated from an unknown permutation $p$ of length $2n$.

The construction rule is simple: the value in cell $(i,j)$ is $p_{i+j}$. Since $i$ and $j$ are 1-based, every cell on the same anti-diagonal has the same value because they share the same sum $i+j$.

Our task is to reconstruct the entire permutation $p_1,p_2,\dots,p_{2n}$.

The key observation is that the grid contains information only about indices $2$ through $2n$. The value $p_1$ never appears because the smallest possible sum is $1+1=2$.

The constraints are very small. The sum of all $n$ across test cases is at most $800$, so even reading the input dominates the work. Any solution that scans the grid once is easily fast enough. There is no need for sophisticated data structures or optimization.

A non-obvious edge case is $n=1$.

Input:

```
1
1
1
```

The grid contains only $p_2=1$. Since the permutation must contain the numbers $1$ and $2$, the missing value is $2$. The answer is:

```
2 1
```

A careless solution might assume every permutation position appears somewhere in the grid and forget to reconstruct $p_1$.

Another subtle case is when the missing value is neither the smallest nor the largest number.

Input:

```
1
2
2 3
3 4
```

From the grid we recover $p_2=2$, $p_3=3$, $p_4=4$. The only number from $\{1,2,3,4\}$ that does not appear is $1$, so:

```
1 2 3 4
```

Any approach that guesses $p_1$ from grid structure instead of using the permutation property would fail here.

## Approaches

A brute-force way to think about the problem is to reconstruct every position $p_k$ by examining all cells whose indices satisfy $i+j=k$. Since the grid is guaranteed to be valid, every such cell contains the same value. After collecting $p_2$ through $p_{2n}$, we determine the remaining number and place it at position $1$.

This already works within the constraints. The grid contains only $n^2$ cells, and $n \le 800$.

The real insight is that we do not need to inspect every anti-diagonal separately.

For any sum $s$ between $2$ and $2n$, there is always at least one valid cell with $i+j=s$. Since all cells on that anti-diagonal contain $p_s$, a single representative cell is enough.

For $s \le n+1$, we can use cell $(1,s-1)$.

For $s > n+1$, we can use cell $(s-n,n)$.

This immediately gives all values $p_2,p_3,\dots,p_{2n}$. Since $p$ is a permutation of $1$ through $2n$, exactly one number is missing from those recovered values. That missing number must be $p_1$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Accepted |
| Optimal | $O(n^2)$ | $O(n)$ | Accepted |

The asymptotic complexity is the same because reading the grid already costs $O(n^2)$, but the optimal approach extracts each permutation value directly.

## Algorithm Walkthrough

1. Read the grid.
2. Create an array `p` of length `2n + 1` using 1-based indexing.
3. For every sum `s` from `2` to `2n`, recover `p[s]`.

If `s <= n + 1`, use `grid[0][s - 2]`, which corresponds to cell `(1, s-1)`.

Otherwise, use `grid[s - n - 1][n - 1]`, which corresponds to cell `(s-n, n)`.

Both cells lie on the anti-diagonal with sum `s`, so they contain exactly `p[s]`.
4. Mark all recovered values `p[2] ... p[2n]`.
5. Among the numbers `1 ... 2n`, find the one that was never marked.
6. Set that number as `p[1]`.
7. Output `p[1] ... p[2n]`.

### Why it works

Every anti-diagonal corresponds to exactly one permutation position. The anti-diagonal with sum $s$ contains only the value $p_s$, so taking any cell from that anti-diagonal recovers the correct permutation element.

The grid covers sums $2$ through $2n$, which means it reveals every permutation position except $p_1$. Since the sequence is guaranteed to be a permutation of $1$ through $2n$, exactly one number is absent from the recovered values. That missing number must be $p_1$. No other choice is possible, which is why the reconstruction is unique.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    g = [list(map(int, input().split())) for _ in range(n)]

    p = [0] * (2 * n + 1)

    for s in range(2, 2 * n + 1):
        if s <= n + 1:
            p[s] = g[0][s - 2]
        else:
            p[s] = g[s - n - 1][n - 1]

    seen = [False] * (2 * n + 1)
    for i in range(2, 2 * n + 1):
        seen[p[i]] = True

    for x in range(1, 2 * n + 1):
        if not seen[x]:
            p[1] = x
            break

    print(*p[1:])
```

The first part reads the grid exactly as given.

The loop over `s` reconstructs positions `2` through `2n`. The indexing is the only slightly tricky part. The input grid is stored with 0-based indices, so cell `(1, s-1)` becomes `g[0][s-2]`, while cell `(s-n, n)` becomes `g[s-n-1][n-1]`.

After recovering all visible permutation values, the code marks them in the `seen` array. Since the permutation contains every number from `1` to `2n` exactly once, scanning for the unmarked number immediately yields `p[1]`.

No integer-overflow concerns exist because all values are at most `1600`.

## Worked Examples

### Example 1

Input:

```
n = 3

1 6 2
6 2 4
2 4 3
```

Recovered values:

| s | Chosen cell | Value | p[s] |
| --- | --- | --- | --- |
| 2 | (1,1) | 1 | 1 |
| 3 | (1,2) | 6 | 6 |
| 4 | (1,3) | 2 | 2 |
| 5 | (2,3) | 4 | 4 |
| 6 | (3,3) | 3 | 3 |

After reconstruction:

| Position | Value |
| --- | --- |
| p2 | 1 |
| p3 | 6 |
| p4 | 2 |
| p5 | 4 |
| p6 | 3 |

The numbers present are `{1,2,3,4,6}`. The missing number from `1..6` is `5`, so `p1 = 5`.

Final answer:

```
5 1 6 2 4 3
```

This example shows that every anti-diagonal directly reveals one permutation position.

### Example 2

Input:

```
n = 2

2 3
3 4
```

Recovered values:

| s | Chosen cell | Value | p[s] |
| --- | --- | --- | --- |
| 2 | (1,1) | 2 | 2 |
| 3 | (1,2) | 3 | 3 |
| 4 | (2,2) | 4 | 4 |

The recovered set is `{2,3,4}`.

| Number | Present? |
| --- | --- |
| 1 | No |
| 2 | Yes |
| 3 | Yes |
| 4 | Yes |

The missing value is `1`, so:

```
1 2 3 4
```

This example demonstrates the reconstruction of the hidden first position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Reading the grid dominates the work |
| Space | $O(n^2)$ | The stored grid contains $n^2$ values |

The total sum of $n$ over all test cases is at most $800$, so at most $640{,}000$ grid cells are processed. This is far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        g = [list(map(int, input().split())) for _ in range(n)]

        p = [0] * (2 * n + 1)

        for s in range(2, 2 * n + 1):
            if s <= n + 1:
                p[s] = g[0][s - 2]
            else:
                p[s] = g[s - n - 1][n - 1]

        seen = [False] * (2 * n + 1)
        for i in range(2, 2 * n + 1):
            seen[p[i]] = True

        for x in range(1, 2 * n + 1):
            if not seen[x]:
                p[1] = x
                break

        out.append(" ".join(map(str, p[1:])))

    return "\n".join(out)

# provided samples
assert run(
"""3
3
1 6 2
6 2 4
2 4 3
1
1
2
2 3
3 4
"""
) == (
"""5 1 6 2 4 3
2 1
1 2 3 4"""
)

# minimum size
assert run(
"""1
1
1
"""
) == "2 1"

# missing value is largest
assert run(
"""1
2
1 2
2 3
"""
) == "4 1 2 3"

# missing value in the middle
assert run(
"""1
2
1 4
4 2
"""
) == "3 1 4 2"

# larger case
assert run(
"""1
3
2 5 1
5 1 6
1 6 4
"""
) == "3 2 5 1 6 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1` | `2 1` | Smallest possible instance |
| `[[1,2],[2,3]]` | `4 1 2 3` | Missing value is the maximum |
| `[[1,4],[4,2]]` | `3 1 4 2` | Missing value lies in the middle |
| 3×3 custom case | `3 2 5 1 6 4` | Correct extraction of all anti-diagonals |

## Edge Cases

Consider the smallest valid input:

```
1
1
1
```

The algorithm recovers only `p2 = 1`. The permutation must contain the numbers `{1,2}`. The missing value is `2`, so it outputs:

```
2 1
```

The reconstruction remains valid even though the grid consists of a single cell.

Now consider:

```
1
2
2 3
3 4
```

Recovery gives:

```
p2 = 2
p3 = 3
p4 = 4
```

The missing number from `{1,2,3,4}` is `1`, producing:

```
1 2 3 4
```

This confirms that the algorithm does not rely on any special position for the missing value.

Finally, consider:

```
1
2
1 4
4 2
```

Recovery yields:

```
p2 = 1
p3 = 4
p4 = 2
```

The only unused number is `3`, so:

```
3 1 4 2
```

This verifies that the hidden first element can be any value in the permutation range, not just an endpoint.
