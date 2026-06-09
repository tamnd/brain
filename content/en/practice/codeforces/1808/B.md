---
title: "CF 1808B - Playing in a Casino"
description: "Each player receives a card containing m integers. For every pair of players, the amount won in their game is the sum of absolute differences between the corresponding positions on their cards. If player i has card values c[i][1...m] and player j has card values c[j][1..."
date: "2026-06-09T08:55:56+07:00"
tags: ["codeforces", "competitive-programming", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1808
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 861 (Div. 2)"
rating: 1200
weight: 1808
solve_time_s: 84
verified: true
draft: false
---

[CF 1808B - Playing in a Casino](https://codeforces.com/problemset/problem/1808/B)

**Rating:** 1200  
**Tags:** math, sortings  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

Each player receives a card containing `m` integers. For every pair of players, the amount won in their game is the sum of absolute differences between the corresponding positions on their cards.

If player `i` has card values `c[i][1...m]` and player `j` has card values `c[j][1...m]`, their contribution is:

$$\sum_{k=1}^{m} |c[i][k] - c[j][k]|$$

We need the total contribution over all unordered pairs of players.

A direct interpretation suggests comparing every pair of cards and every position inside the cards. With `n` players and `m` values per card, that would require examining all `n(n-1)/2` pairs and all `m` columns for each pair.

The constraint that matters is the total number of matrix entries across all test cases:

$$\sum (n \cdot m) \le 3 \cdot 10^5$$

This is small enough for algorithms around `O(nm log n)`, but far too large for `O(n^2 m)` when `n` is large. For example, if `n = 3 \cdot 10^5` and `m = 1`, then an `O(n^2)` approach would require roughly $9 \times 10^{10}$ operations.

The hidden structure is that the sum of absolute differences is separable by columns. Each column contributes independently to the final answer.

Several edge cases can easily cause mistakes.

Consider:

```
2 1
5
5
```

There is only one pair, and its contribution is `|5-5| = 0`. Any formula that assumes strictly increasing values after sorting would incorrectly add something positive.

Consider:

```
3 1
1
10
100
```

The answer is:

```
|1-10| + |1-100| + |10-100|
= 9 + 99 + 90
= 198
```

A careless implementation that only looks at adjacent differences after sorting would get `9 + 90 = 99`, which is only half of the required sum.

Consider:

```
1 4
7 8 9 10
```

There are no pairs of players at all. The answer must be `0`. Any solution that blindly applies pair formulas without considering `n = 1` may produce garbage values.

## Approaches

The brute-force idea is straightforward. For every pair of players, compare their cards coordinate by coordinate, compute the sum of absolute differences, and add it to the answer.

This works because it directly matches the definition of the winnings. The problem is the running time:

$$O(n^2 m)$$

If `n = 3 \cdot 10^5` and `m = 1`, this becomes completely infeasible.

The key observation is that the contribution from each column is independent.

Suppose we focus on a single column and collect all values from that column:

$$x_1, x_2, \dots, x_n$$

The total contribution of this column is:

$$\sum_{i<j} |x_i - x_j|$$

This is a classic expression. After sorting:

$$x_1 \le x_2 \le \cdots \le x_n$$

the absolute value disappears:

$$|x_j-x_i| = x_j-x_i \quad (j>i)$$

Now consider how often each sorted value appears positively and negatively.

For position `i`:

$$x_i$$

appears as the larger element exactly `i` times and as the smaller element exactly `n-1-i` times (using 0-based indexing).

Its net coefficient becomes:

$$i - (n-1-i)$$

Another way to compute the same sum is with prefix sums. While scanning the sorted array, for each value `x[i]`, all previous values are already known.

Its contribution against previous elements is:

$$i \cdot x[i] - \text{prefix}$$

where `prefix` is the sum of all earlier values.

This lets us compute the entire column contribution in linear time after sorting.

Since every column is processed independently, the complexity becomes:

$$O(m \cdot n \log n)$$

which easily fits the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²m) | O(1) | Too slow |
| Optimal | O(m·n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the matrix representing all cards.
2. For each column, collect its `n` values into an array.
3. Sort the column values.

After sorting, every pair contribution becomes a simple subtraction instead of an absolute value.
4. Initialize `prefix = 0`.
5. Scan the sorted column from left to right.

For the current value `x[i]`, all previous values are smaller or equal.
6. Add

$$i \cdot x[i] - prefix$$

to the answer.

This equals the sum of:

$$x[i]-x[0],\ x[i]-x[1],\ \dots,\ x[i]-x[i-1]$$

which is exactly the contribution of `x[i]` with all earlier elements.
7. Update

$$prefix += x[i]$$

so future elements can use it.
8. Repeat for every column.
9. Output the accumulated answer.

### Why it works

After sorting a column, every pair `(i,j)` with `i < j` contributes `x[j] - x[i]`. When processing `x[j]`, the quantity

$$j \cdot x[j] - \text{prefix}$$

adds exactly

$$(x[j]-x[0]) + (x[j]-x[1]) + \cdots + (x[j]-x[j-1])$$

which is the total contribution of all pairs ending at position `j`.

Every unordered pair appears exactly once, namely when its larger sorted endpoint is processed. No pair is omitted and no pair is counted twice. Summing this value over all positions and all columns gives exactly the required total winnings.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, m = map(int, input().split())

    a = [list(map(int, input().split())) for _ in range(n)]

    ans = 0

    for col in range(m):
        vals = [a[row][col] for row in range(n)]
        vals.sort()

        prefix = 0

        for i, x in enumerate(vals):
            ans += i * x - prefix
            prefix += x

    print(ans)
```

The matrix is read exactly once. For each column, we extract its values, sort them, and compute the sum of pairwise differences using a running prefix sum.

The expression:

```
ans += i * x - prefix
```

is the critical line. At index `i`, there are exactly `i` previous elements. Their total contribution against `x` is:

```
(x - v1) + (x - v2) + ... + (x - vi)
```

which simplifies to:

```
i * x - (v1 + v2 + ... + vi)
```

and that sum is stored in `prefix`.

Python integers automatically handle large values, so there is no overflow risk. In languages such as C++, a 64-bit integer would be required.

## Worked Examples

### Example 1

Input:

```
3 5
1 4 2 8 5
7 9 2 1 4
3 8 5 3 1
```

Column 1 values are `[1, 7, 3]`.

After sorting:

```
[1, 3, 7]
```

| i | x | prefix before | Added value | Running answer |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 |
| 1 | 3 | 1 | 2 | 2 |
| 2 | 7 | 4 | 10 | 12 |

Column 1 contributes `12`.

Column 2 values are `[4, 9, 8]`.

Sorted:

```
[4, 8, 9]
```

| i | x | prefix before | Added value | Column total |
| --- | --- | --- | --- | --- |
| 0 | 4 | 0 | 0 | 0 |
| 1 | 8 | 4 | 4 | 4 |
| 2 | 9 | 12 | 6 | 10 |

Column 2 contributes `10`.

Repeating for all five columns yields:

```
12 + 10 + 6 + 14 + 8 = 50
```

which matches the sample output.

This trace shows how each column is handled independently and how the prefix-sum formula reproduces all pairwise differences.

### Example 2

Input:

```
4 3
1 2 3
3 2 1
1 2 1
4 2 7
```

First column:

```
[1,3,1,4]
→ [1,1,3,4]
```

| i | x | prefix before | Added |
| --- | --- | --- | --- |
| 0 | 1 | 0 | 0 |
| 1 | 1 | 1 | 0 |
| 2 | 3 | 2 | 4 |
| 3 | 4 | 5 | 7 |

Contribution = `11`.

Second column:

```
[2,2,2,2]
```

| i | x | prefix before | Added |
| --- | --- | --- | --- |
| 0 | 2 | 0 | 0 |
| 1 | 2 | 2 | 0 |
| 2 | 2 | 4 | 0 |
| 3 | 2 | 6 | 0 |

Contribution = `0`.

Third column:

```
[3,1,1,7]
→ [1,1,3,7]
```

| i | x | prefix before | Added |
| --- | --- | --- | --- |
| 0 | 1 | 0 | 0 |
| 1 | 1 | 1 | 0 |
| 2 | 3 | 2 | 4 |
| 3 | 7 | 5 | 16 |

Contribution = `20`.

Final answer:

```
11 + 0 + 20 = 31
```

This example highlights that columns with all equal values naturally contribute zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m·n log n) | Each column of size `n` is sorted once |
| Space | O(n) | Temporary array storing one column |

The total number of matrix entries across all test cases is at most `3·10^5`. Sorting each column gives a total complexity comfortably within the limits, and the extra memory is only a single column array.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]

        ans = 0

        for col in range(m):
            vals = [a[row][col] for row in range(n)]
            vals.sort()

            pref = 0
            for i, x in enumerate(vals):
                ans += i * x - pref
                pref += x

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    res = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return res

# provided samples
assert run(
"""3
3 5
1 4 2 8 5
7 9 2 1 4
3 8 5 3 1
1 4
4 15 1 10
4 3
1 2 3
3 2 1
1 2 1
4 2 7
"""
) == "50\n0\n31"

# minimum size
assert run(
"""1
1 1
5
"""
) == "0"

# all equal
assert run(
"""1
3 2
7 7
7 7
7 7
"""
) == "0"

# single column
assert run(
"""1
3 1
1
10
100
"""
) == "198"

# off-by-one style check
assert run(
"""1
2 2
1 2
3 4
"""
) == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1x1` matrix | `0` | No player pairs exist |
| All values equal | `0` | Equal values contribute nothing |
| Single column `[1,10,100]` | `198` | Correct pairwise difference accumulation |
| Two rows `[[1,2],[3,4]]` | `4` | Every pair counted exactly once |

## Edge Cases

### Single Player

Input:

```
1
1 4
7 8 9 10
```

Each column contains only one value.

For every column, after sorting there is just one element:

| i | x | prefix | Added |
| --- | --- | --- | --- |
| 0 | x | 0 | 0 |

No pair exists, so every column contributes zero. The final answer is:

```
0
```

### All Values Equal

Input:

```
1
3 1
5
5
5
```

Sorted column:

```
[5,5,5]
```

| i | x | prefix before | Added |
| --- | --- | --- | --- |
| 0 | 5 | 0 | 0 |
| 1 | 5 | 5 | 0 |
| 2 | 5 | 10 | 0 |

The answer remains zero because every pair difference is zero.

### Large Gaps Between Values

Input:

```
1
3 1
1
10
100
```

Sorted column:

```
[1,10,100]
```

| i | x | prefix before | Added |
| --- | --- | --- | --- |
| 0 | 1 | 0 | 0 |
| 1 | 10 | 1 | 9 |
| 2 | 100 | 11 | 189 |

Total:

```
9 + 189 = 198
```

which equals:

```
|1-10| + |1-100| + |10-100|
= 9 + 99 + 90
= 198
```

This confirms that the prefix-sum formula captures every pairwise difference, not only adjacent differences in the sorted order.
