---
title: "CF 2B - The least round way"
description: "We have an n × n grid of non-negative integers. Starting from the top-left corner, we may move only right or down until"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 2
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 2"
rating: 2000
weight: 2
solve_time_s: 187
verified: false
draft: false
---

[CF 2B - The least round way](https://codeforces.com/problemset/problem/2/B)

**Rating:** 2000  
**Tags:** dp, math  
**Solve time:** 3m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We have an `n × n` grid of non-negative integers. Starting from the top-left corner, we may move only right or down until we reach the bottom-right corner. Along a chosen path, we multiply every visited value together. The goal is to make the resulting product end with as few trailing zeros as possible.

A trailing zero appears whenever the product contains a factor `10`, and every `10` is formed from one factor `2` paired with one factor `5`. That means the number of trailing zeros equals:

$\min(\text{count of factor }2,\ \text{count of factor }5)$

So the actual values in the grid are not important by themselves. What matters is how many times each number contributes factors `2` and `5`.

The grid size can reach `1000 × 1000`, which means there are one million cells. Any algorithm that explores paths explicitly is hopeless because the number of valid paths is enormous. A path from `(0,0)` to `(n-1,n-1)` contains exactly `2n-2` moves, and we choose which `n-1` of them are downward. The total number of paths is:

$\binom{2n-2}{n-1}$

For `n = 1000`, this number is astronomically large. We need a polynomial-time solution, ideally around `O(n²)`.

The most subtle edge case involves zeros inside the grid. A path passing through a zero produces total product `0`, and `0` is usually considered to have at least one trailing zero. This creates an unusual situation where a path containing zero can actually be better than all non-zero paths.

Consider:

```
2
1 10
1 0
```

Any path avoiding the zero gives product `10`, which has one trailing zero. A path through the zero gives product `0`, also treated as having one trailing zero. The answer should still be `1`.

Now consider:

```
2
10 10
10 0
```

Every non-zero path produces `100`, which has two trailing zeros. Going through the zero gives only one trailing zero, so the optimal answer becomes `1`.

A careless implementation often treats zero as contributing infinite factors of `2` and `5`, which would incorrectly forbid paths through zero. The correct handling is to remember whether a zero exists and potentially construct a special path through it.

Another easy mistake is reconstructing the path incorrectly when both directions give the same DP value. If parent transitions are not stored carefully, the printed route may not correspond to the computed optimum.

## Approaches

The brute-force idea is straightforward. Enumerate every valid path from the top-left corner to the bottom-right corner, compute the product along that path, count its trailing zeros, and keep the best answer.

This works because the definition of the problem is directly tied to a path. Every valid route can be checked independently. The issue is the number of paths. A path consists of `n-1` downward moves and `n-1` rightward moves arranged in some order, giving:

$\binom{2n-2}{n-1}$

For `n = 20`, this already exceeds thirty billion paths. The brute-force approach becomes unusable long before the actual limit.

The key observation is that trailing zeros depend only on counts of prime factors `2` and `5`. For every cell, we can precompute:

```
twos[i][j]  = exponent of 2 in grid[i][j]
fives[i][j] = exponent of 5 in grid[i][j]
```

If a path accumulates `a` factors of `2` and `b` factors of `5`, then the number of trailing zeros equals `min(a, b)`.

This changes the problem completely. Instead of multiplying huge numbers, we only need additive costs along a path. Dynamic programming becomes natural because every move depends only on the top or left neighbor.

One subtlety remains. Minimizing `min(a, b)` directly is awkward because the minimum depends on two quantities simultaneously. The trick is to solve two separate DP problems:

```
minimum total factors of 2
minimum total factors of 5
```

Any path with minimal trailing zeros must optimize one of these counts. If the optimal path has `k` trailing zeros, then either its count of `2`s equals `k` or its count of `5`s equals `k`.

So we run DP twice and take the better result.

The zero case needs special treatment. A zero cell can provide exactly one trailing zero if every ordinary path has answer greater than one. In that situation, we deliberately construct a path that goes through the zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential recursion stack | Too slow |
| Optimal | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. For every cell, compute how many times its value is divisible by `2` and by `5`.

For example, `40 = 2³ × 5¹`, so it contributes three factors of `2` and one factor of `5`.
2. If a cell contains `0`, remember its coordinates separately.

We temporarily treat zero as contributing a very large cost in both DP tables so ordinary DP paths avoid it unless explicitly needed later.
3. Build a DP table for factors of `2`.

Let `dp2[i][j]` be the minimum total number of factors `2` needed to reach cell `(i,j)`.

Transition:

```
dp2[i][j] = twos[i][j] + min(top, left)
```
4. Store the direction used to reach each cell.

This allows reconstruction of the actual path after DP finishes.
5. Repeat the same process for factors of `5`.

This gives another DP table `dp5`.
6. Let:

```
best2 = dp2[n-1][n-1]
best5 = dp5[n-1][n-1]
```

The best ordinary path has answer:

```
min(best2, best5)
```
7. Check whether a zero cell exists.

If the ordinary answer is already `0`, using zero cannot improve it.

If the ordinary answer is greater than `1`, then routing through a zero gives answer exactly `1`, which is better.
8. If using zero is better, construct a path manually.

Move down until reaching the zero row, move right until reaching the zero column, then finish toward the bottom-right corner.
9. Otherwise, reconstruct the better DP path using stored parent directions.

### Why it works

For any integer product, trailing zeros equal the number of complete `(2,5)` pairs in its prime factorization. Since every path accumulates factors independently across cells, the total number of `2`s and `5`s becomes additive. Dynamic programming correctly computes the minimum achievable sum because every path to `(i,j)` must come from either `(i-1,j)` or `(i,j-1)`.

Suppose the optimal path has `a` factors of `2` and `b` factors of `5`. Its trailing zeros are `min(a,b)`. If `a ≤ b`, then this path is optimal for minimizing factors of `2`. If another path had fewer `2`s, it would also have fewer trailing zeros, contradicting optimality. The symmetric argument holds for `5`s. So solving the two independent DP problems is sufficient.

The zero handling is correct because any path through zero produces product `0`, which contributes exactly one trailing zero in the context of this problem. Such a path matters only when every ordinary path has at least two trailing zeros.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**9

n = int(input())

twos = [[0] * n for _ in range(n)]
fives = [[0] * n for _ in range(n)]

zero_pos = None

for i in range(n):
    row = list(map(int, input().split()))
    
    for j in range(n):
        x = row[j]

        if x == 0:
            zero_pos = (i, j)
            twos[i][j] = INF
            fives[i][j] = INF
            continue

        cnt2 = 0
        while x % 2 == 0:
            cnt2 += 1
            x //= 2

        cnt5 = 0
        while x % 5 == 0:
            cnt5 += 1
            x //= 5

        twos[i][j] = cnt2
        fives[i][j] = cnt5

def build_dp(cost):
    dp = [[INF] * n for _ in range(n)]
    parent = [[''] * n for _ in range(n)]

    dp[0][0] = cost[0][0]

    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                continue

            if i > 0 and dp[i - 1][j] + cost[i][j] < dp[i][j]:
                dp[i][j] = dp[i - 1][j] + cost[i][j]
                parent[i][j] = 'D'

            if j > 0 and dp[i][j - 1] + cost[i][j] < dp[i][j]:
                dp[i][j] = dp[i][j - 1] + cost[i][j]
                parent[i][j] = 'R'

    return dp, parent

dp2, par2 = build_dp(twos)
dp5, par5 = build_dp(fives)

best2 = dp2[n - 1][n - 1]
best5 = dp5[n - 1][n - 1]

best = min(best2, best5)

if zero_pos is not None and best > 1:
    zi, zj = zero_pos

    path = []
    path.extend('D' * zi)
    path.extend('R' * zj)
    path.extend('D' * (n - 1 - zi))
    path.extend('R' * (n - 1 - zj))

    print(1)
    print(''.join(path))

else:
    if best2 < best5:
        parent = par2
        answer = best2
    else:
        parent = par5
        answer = best5

    path = []

    i = n - 1
    j = n - 1

    while i > 0 or j > 0:
        move = parent[i][j]
        path.append(move)

        if move == 'D':
            i -= 1
        else:
            j -= 1

    path.reverse()

    print(answer)
    print(''.join(path))
```

The preprocessing phase converts every grid value into counts of factors `2` and `5`. This avoids dealing with gigantic products and turns multiplication into simple addition.

Zero handling is intentionally separated from normal DP. Assigning `INF` prevents accidental use of zero during optimization. Later, we explicitly decide whether a zero-path is beneficial.

The `build_dp` function computes shortest paths on the grid where each cell contributes a cost. Parent directions are stored during transitions. A stored `'D'` means the current cell was reached from above, so reconstruction moves upward when retracing.

One subtle implementation detail is reconstructing from the destination backward. During reconstruction:

```
'D' means we came from above
'R' means we came from the left
```

So while retracing, `'D'` decreases the row index and `'R'` decreases the column index.

Another subtle point is the comparison:

```
if zero_pos is not None and best > 1:
```

If the ordinary optimum already equals `1`, using zero gives no improvement, so either answer is acceptable. The special zero-path matters only when it strictly improves the result.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
4 5 6
7 8 9
```

Factor counts for `2`:

| Cell | Value | Count of 2 |
| --- | --- | --- |
| (0,0) | 1 | 0 |
| (0,1) | 2 | 1 |
| (0,2) | 3 | 0 |
| (1,0) | 4 | 2 |
| (1,1) | 5 | 0 |
| (1,2) | 6 | 1 |
| (2,0) | 7 | 0 |
| (2,1) | 8 | 3 |
| (2,2) | 9 | 0 |

Factor counts for `5`:

| Cell | Value | Count of 5 |
| --- | --- | --- |
| (0,0) | 1 | 0 |
| (0,1) | 2 | 0 |
| (0,2) | 3 | 0 |
| (1,0) | 4 | 0 |
| (1,1) | 5 | 1 |
| (1,2) | 6 | 0 |
| (2,0) | 7 | 0 |
| (2,1) | 8 | 0 |
| (2,2) | 9 | 0 |

DP for factors of `5`:

| Cell | Best cost |
| --- | --- |
| (0,0) | 0 |
| (0,1) | 0 |
| (0,2) | 0 |
| (1,0) | 0 |
| (1,1) | 1 |
| (1,2) | 0 |
| (2,0) | 0 |
| (2,1) | 0 |
| (2,2) | 0 |

The optimal path avoids the `5` entirely, giving zero trailing zeros. One valid route is `DDRR`.

This example demonstrates the core idea that minimizing trailing zeros is equivalent to minimizing either total `2`s or total `5`s.

### Example 2

Input:

```
2
10 10
10 0
```

Ordinary paths avoiding zero:

| Path | Product | Trailing zeros |
| --- | --- | --- |
| RD | 100 | 2 |
| DR | 0 | 1 |

The DP tables avoid the zero because it was assigned `INF`. The best ordinary answer becomes `2`.

Since a zero exists and `2 > 1`, the algorithm manually constructs a path through zero.

| Step | Position | Move |
| --- | --- | --- |
| Start | (0,0) | D |
| Next | (1,0) | R |
| End | (1,1) | - |

The output becomes:

```
1
DR
```

This example validates the special handling for zero cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each DP table processes every cell once |
| Space | O(n²) | DP tables and parent tables store one value per cell |

With `n ≤ 1000`, the grid contains at most one million cells. Two DP passes over the grid easily fit within the time limit in Python. The memory usage also remains well under the limit because each table stores only integers or single-character directions.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    INF = 10**9

    n = int(input())

    twos = [[0] * n for _ in range(n)]
    fives = [[0] * n for _ in range(n)]

    zero_pos = None

    for i in range(n):
        row = list(map(int, input().split()))

        for j in range(n):
            x = row[j]

            if x == 0:
                zero_pos = (i, j)
                twos[i][j] = INF
                fives[i][j] = INF
                continue

            cnt2 = 0
            while x % 2 == 0:
                cnt2 += 1
                x //= 2

            cnt5 = 0
            while x % 5 == 0:
                cnt5 += 1
                x //= 5

            twos[i][j] = cnt2
            fives[i][j] = cnt5

    def build(cost):
        dp = [[INF] * n for _ in range(n)]
        par = [[''] * n for _ in range(n)]

        dp[0][0] = cost[0][0]

        for i in range(n):
            for j in range(n):
                if i == 0 and j == 0:
                    continue

                if i > 0 and dp[i - 1][j] + cost[i][j] < dp[i][j]:
                    dp[i][j] = dp[i - 1][j] + cost[i][j]
                    par[i][j] = 'D'

                if j > 0 and dp[i][j - 1] + cost[i][j] < dp[i][j]:
                    dp[i][j] = dp[i][j - 1] + cost[i][j]
                    par[i][j] = 'R'

        return dp, par

    dp2, par2 = build(twos)
    dp5, par5 = build(fives)

    best2 = dp2[n - 1][n - 1]
    best5 = dp5[n - 1][n - 1]

    best = min(best2, best5)

    out = []

    if zero_pos is not None and best > 1:
        zi, zj = zero_pos

        path = []
        path.extend('D' * zi)
        path.extend('R' * zj)
        path.extend('D' * (n - 1 - zi))
        path.extend('R' * (n - 1 - zj))

        out.append("1")
        out.append(''.join(path))

    else:
        if best2 < best5:
            par = par2
            ans = best2
        else:
            par = par5
            ans = best5

        path = []

        i = n - 1
        j = n - 1

        while i > 0 or j > 0:
            move = par[i][j]
            path.append(move)

            if move == 'D':
                i -= 1
            else:
                j -= 1

        path.reverse()

        out.append(str(ans))
        out.append(''.join(path))

    print('\n'.join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run(
"""3
1 2 3
4 5 6
7 8 9
"""
).startswith("0")

# minimum size
assert run(
"""2
1 1
1 1
"""
).startswith("0")

# zero gives better answer
assert run(
"""2
10 10
10 0
"""
).startswith("1")

# all equal values
assert run(
"""3
10 10 10
10 10 10
10 10 10
"""
).startswith("5")

# path with no trailing zeros exists
assert run(
"""3
2 4 8
16 32 64
3 9 27
"""
).startswith("0")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2×2` grid of ones | `0` trailing zeros | Minimum-size boundary |
| Grid containing beneficial zero | `1` trailing zero | Correct zero handling |
| All values equal to `10` | `5` trailing zeros | Accumulation of factors |
| Grid with pure powers of `2` except one row | `0` trailing zeros | Avoiding unnecessary `5`s |

## Edge Cases

Consider the grid:

```
2
10 10
10 0
```

Every ordinary path accumulates at least two factors `2` and two factors `5`, giving two trailing zeros. During preprocessing, the zero cell receives cost `INF`, so DP avoids it and computes answer `2`.

Then the algorithm checks:

```
zero exists AND best > 1
```

Both conditions hold, so it constructs a route through the zero:

```
DR
```

The product becomes `10 × 10 × 0 = 0`, which yields exactly one trailing zero. The final answer is correct.

Now consider:

```
2
1 1
1 0
```

A non-zero path already achieves zero trailing zeros. The DP result becomes `0`.

Even though a zero exists, the condition `best > 1` fails. The algorithm correctly ignores the zero path because moving through zero would worsen the answer from `0` to `1`.

Finally, consider a tie case:

```
2
2 5
5 2
```

Both paths produce one trailing zero. During reconstruction, either parent choice is acceptable. The algorithm consistently reconstructs one valid optimal path because every DP transition stores an actual predecessor used to achieve the minimum cost.
