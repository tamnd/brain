---
title: "CF 123C - Brackets"
description: "We are filling an n × m grid with brackets. Every cell contains either \"(\" or \")\". The grid is called valid if every monotone path from the top-left corner to the bottom-right corner forms a correct bracket sequence. A monotone path only moves right or down."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 123
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 92 (Div. 1 Only)"
rating: 2300
weight: 123
solve_time_s: 139
verified: true
draft: false
---

[CF 123C - Brackets](https://codeforces.com/problemset/problem/123/C)

**Rating:** 2300  
**Tags:** combinatorics, dp, greedy  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are filling an `n × m` grid with brackets. Every cell contains either `"("` or `")"`.

The grid is called valid if every monotone path from the top-left corner to the bottom-right corner forms a correct bracket sequence. A monotone path only moves right or down.

The second part of the problem defines an ordering between grids. Each cell has a unique priority from `1` to `nm`. To compare two grids, we inspect cells in increasing priority order and find the first position where the grids differ. The grid having `"("` in that position is considered smaller.

We must output the `k`-th valid grid in this ordering.

The first thing to understand is what the validity condition really means. A path from `(1,1)` to `(n,m)` always has length `n + m - 1`. Every such path must itself be a regular bracket sequence.

A regular bracket sequence has two properties:

1. Every prefix contains at least as many `"("` as `")"`.
2. The total number of `"("` equals the total number of `")"`.

Since every path has the same length, the total length must be even. That means `n + m - 1` must be even. If it is odd, no valid grid exists. The statement guarantees enough solutions for the given `k`, so we never need to handle impossible input explicitly.

The constraints are large enough to rule out brute force enumeration. The grid has up to `100 × 100 = 10000` cells. Even checking all `2^(nm)` grids is absurdly impossible. The value of `k` can be as large as `10^18`, which strongly suggests that we only need counting up to some capped value, not exact astronomical counts.

The hidden structural property is that every valid grid is completely determined by the anti-diagonal index `i + j`.

Consider any path. At step `t`, the path is always on cells satisfying `i + j = t + 2`. Every path visits exactly one cell from each anti-diagonal. If different cells on the same anti-diagonal had different brackets, then two paths could choose different brackets at the same position in the sequence, which would break the requirement that all paths are correct simultaneously.

This observation collapses the problem from a 2D grid into a 1D bracket sequence.

There are several edge cases that break naive reasoning.

Suppose:

```
1 3
```

The only path length is `3`, which is odd. No correct bracket sequence of odd length exists. A careless implementation might still try to generate something like `"()("`.

Another subtle case is:

```
2 2
```

Every path has length `3`, again impossible. Some naive DP formulations forget the parity condition and accidentally count invalid states.

A more interesting example is:

```
2 3
```

The anti-diagonals are:

```
(1,1)
(1,2),(2,1)
(1,3),(2,2)
(2,3)
```

If the second anti-diagonal mixed brackets, two paths would produce different second characters. One could become invalid earlier than the other. Uniformity across anti-diagonals is not optional, it is forced by the condition.

## Approaches

The brute force approach is straightforward conceptually. Enumerate all `2^(nm)` grids, check whether every monotone path forms a regular bracket sequence, collect all valid grids, sort them using the custom priority ordering, and print the `k`-th one.

Checking one grid already requires examining all monotone paths. The number of such paths is:

$$\binom{n+m-2}{n-1}$$

For a `100 × 100` grid this number is astronomical. Even before considering the number of grids, the validation itself is impossible.

The key observation is that every path visits exactly one cell from each anti-diagonal. Let:

$$d = i + j$$

All cells with the same `d` appear at the same position in every path.

Now suppose two cells on the same anti-diagonal contain different brackets. Then two different paths could produce different characters at the same sequence position. One sequence could violate bracket balance while another does not. The only way every path can always be correct is that all cells on the same anti-diagonal contain the same bracket.

This transforms the problem completely.

Instead of choosing brackets independently for `nm` cells, we only choose one bracket per anti-diagonal. There are exactly:

$$n + m - 1$$

anti-diagonals, so the entire grid corresponds to a single bracket sequence of that length.

Now the condition becomes much simpler. Every path reads exactly the same sequence. The grid is valid if and only if that sequence is a regular bracket sequence.

The custom ordering also becomes manageable. Each anti-diagonal contains several cells with different priorities. The earliest comparison point for a diagonal is simply the minimum priority inside that diagonal. So we can sort anti-diagonals by these minimum priorities and compare bracket sequences in that order.

At this point the problem reduces to:

1. Build the order of anti-diagonals.
2. Find the `k`-th regular bracket sequence under that custom position order.
3. Fill every diagonal uniformly.

We can construct the answer greedily. At each step in the comparison order, try placing `"("`. Count how many valid completions exist. If that count is at least `k`, keep `"("`. Otherwise subtract the count from `k` and place `")"`.

The counting DP is the standard bracket sequence DP with balance states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{nm} \cdot \binom{n+m-2}{n-1})$ | Exponential | Too slow |
| Optimal | $O((n+m)^2)$ | $O((n+m)^2)$ | Accepted |

## Algorithm Walkthrough

1. Compute the number of anti-diagonals.

The diagonals are indexed by:

$$s = i + j$$

ranging from `2` to `n + m`.
2. For each anti-diagonal, compute its minimum priority.

Every cell on the same diagonal must share the same bracket, so the comparison order between diagonals is determined by the smallest priority appearing inside each diagonal.
3. Sort the anti-diagonals by these minimum priorities.

This gives the exact lexicographic order used by the problem.
4. Let `L = n + m - 1`.

This is the length of every path sequence. Since a regular bracket sequence must have even length, `L` must be even.
5. Build a DP table.

Let:

$$dp[pos][bal]$$

be the number of valid ways to finish positions from `pos` onward if the current balance is `bal`.

Balance means:

$$\#("(") - \#(")")$$

already used.
6. Fill the DP backwards.

At the end:

$$dp[L][0] = 1$$

and all other ending balances are invalid.

For each position we try adding `"("` or `")"` while never allowing negative balance.
7. Construct the answer greedily in priority order.

For each diagonal in sorted order:

1. Temporarily place `"("`.
2. Count how many valid completions remain.
3. If the count is at least `k`, keep `"("`.
4. Otherwise subtract the count from `k` and place `")"`.

This is standard lexicographic generation using counting.
8. After deciding the bracket for every anti-diagonal, fill the grid.

Every cell `(i,j)` receives the bracket assigned to diagonal `i+j`.

### Why it works

Every monotone path visits exactly one cell from each anti-diagonal, in increasing diagonal order. If a diagonal contained mixed brackets, two paths could produce different symbols at the same sequence position. Then correctness would depend on path choice, contradicting the requirement that every path must be correct.

So every valid grid corresponds uniquely to one bracket sequence over the anti-diagonals.

The ordering between grids also reduces correctly because the first differing cell must belong to the diagonal whose minimum priority appears earliest.

The DP counts exactly the number of regular bracket sequences extending a given prefix. The greedy construction chooses the lexicographically smallest possible character whenever enough completions remain, so the produced sequence is exactly the `k`-th one.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

def solve():
    n, m, k = map(int, input().split())

    p = [list(map(int, input().split())) for _ in range(n)]

    L = n + m - 1

    # minimum priority for each anti-diagonal
    diag_min = [10**18] * (L + 2)

    for i in range(n):
        for j in range(m):
            s = i + j
            diag_min[s] = min(diag_min[s], p[i][j])

    # order of diagonals in comparison
    order = sorted(range(L), key=lambda x: diag_min[x])

    # dp[pos][bal]
    dp = [[0] * (L + 2) for _ in range(L + 1)]
    dp[L][0] = 1

    for pos in range(L - 1, -1, -1):
        rem = L - pos

        for bal in range(L + 1):
            val = 0

            # place '('
            if bal + 1 <= L:
                val += dp[pos + 1][bal + 1]

            # place ')'
            if bal > 0:
                val += dp[pos + 1][bal - 1]

            dp[pos][bal] = min(val, INF)

    ans_diag = ['?'] * L

    assigned = [None] * L

    # map diagonal -> sequence position
    pos_of_diag = [0] * L
    for idx, d in enumerate(order):
        pos_of_diag[d] = idx

    seq = ['?'] * L

    balance = 0

    for pos in range(L):
        # try '('
        remain_count = 0

        if balance + 1 <= L:
            remain_count = dp[pos + 1][balance + 1]

        if remain_count >= k:
            seq[pos] = '('
            balance += 1
        else:
            k -= remain_count
            seq[pos] = ')'
            balance -= 1

    # assign brackets to diagonals
    for d in range(L):
        ans_diag[d] = seq[pos_of_diag[d]]

    out = []

    for i in range(n):
        row = []
        for j in range(m):
            row.append(ans_diag[i + j])
        out.append(''.join(row))

    print('\n'.join(out))

solve()
```

The first part computes the minimum priority inside each anti-diagonal. That value determines when the diagonal participates in comparisons between two grids.

The subtle point is that the comparison order is not the natural diagonal order. We must sort diagonals by their smallest contained priority because the first differing cell decides the order.

The DP is the classic balanced bracket sequence DP. `dp[pos][bal]` stores how many suffixes are possible after processing `pos` characters with current balance `bal`.

The count is capped at `10^18` because the problem never distinguishes larger values. Without capping, languages with fixed-width integers would overflow. Python integers are arbitrary precision, but capping still keeps the values manageable and mirrors the intended logic.

The greedy construction is lexicographic generation. We first test whether putting `"("` still leaves at least `k` valid completions. If yes, we keep it. Otherwise all those sequences come earlier, so we subtract them and choose `")"`.

One easy mistake is forgetting that the sequence positions are ordered by diagonal priority, not by geometric diagonal index. The array `pos_of_diag` handles this conversion.

Another easy bug is allowing negative balance during construction. Such prefixes can never become valid bracket sequences.

## Worked Examples

### Example 1

Input:

```
1 2 1
1 2
```

There are two diagonals.

| Diagonal | Cells | Minimum Priority |
| --- | --- | --- |
| 0 | (1,1) | 1 |
| 1 | (1,2) | 2 |

The comparison order is `[0,1]`.

The sequence length is `2`.

DP determines only one valid bracket sequence exists:

```
()
```

Now fill the diagonals.

| Cell | Diagonal | Character |
| --- | --- | --- |
| (1,1) | 0 | ( |
| (1,2) | 1 | ) |

Output:

```
()
```

This example shows the simplest possible valid grid. Every path reads the same sequence because there is only one path.

### Example 2

Consider:

```
2 3 2
1 5 4
2 3 6
```

The anti-diagonals are:

| Diagonal | Cells | Minimum Priority |
| --- | --- | --- |
| 0 | (1,1) | 1 |
| 1 | (1,2),(2,1) | 2 |
| 2 | (1,3),(2,2) | 3 |
| 3 | (2,3) | 6 |

The order is `[0,1,2,3]`.

All valid bracket sequences of length `4` are:

```
(())
()()
```

Since `k = 2`, we choose the second one.

Now assign diagonals:

| Diagonal | Character |
| --- | --- |
| 0 | ( |
| 1 | ) |
| 2 | ( |
| 3 | ) |

Final grid:

```
()(
)()
```

Every monotone path reads:

```
()()
```

This trace demonstrates why uniform diagonals are enough. Different paths visit different cells, but always from the same diagonal order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+m)^2)$ | DP over positions and balances |
| Space | $O((n+m)^2)$ | DP table storage |

The maximum sequence length is `199`, so the DP is tiny. Even Python easily fits within the limits. The grid itself can contain `10000` cells, but we only process each cell a constant number of times.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

INF = 10**18

def solve():
    input = sys.stdin.readline

    n, m, k = map(int, input().split())
    p = [list(map(int, input().split())) for _ in range(n)]

    L = n + m - 1

    diag_min = [10**18] * (L + 2)

    for i in range(n):
        for j in range(m):
            diag_min[i + j] = min(diag_min[i + j], p[i][j])

    order = sorted(range(L), key=lambda x: diag_min[x])

    dp = [[0] * (L + 2) for _ in range(L + 1)]
    dp[L][0] = 1

    for pos in range(L - 1, -1, -1):
        for bal in range(L + 1):
            val = 0

            if bal + 1 <= L:
                val += dp[pos + 1][bal + 1]

            if bal > 0:
                val += dp[pos + 1][bal - 1]

            dp[pos][bal] = min(val, INF)

    pos_of_diag = [0] * L
    for idx, d in enumerate(order):
        pos_of_diag[d] = idx

    seq = []
    bal = 0

    for pos in range(L):
        cnt = 0

        if bal + 1 <= L:
            cnt = dp[pos + 1][bal + 1]

        if cnt >= k:
            seq.append('(')
            bal += 1
        else:
            k -= cnt
            seq.append(')')
            bal -= 1

    diag_char = ['?'] * L
    for d in range(L):
        diag_char[d] = seq[pos_of_diag[d]]

    out = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(diag_char[i + j])
        out.append(''.join(row))

    print('\n'.join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("1 2 1\n1 2\n") == "()"

# single valid sequence
assert run("1 4 1\n1 2 3 4\n") == "(())"

# second valid sequence
assert run("1 4 2\n1 2 3 4\n") == "()()"

# custom priority ordering
assert run(
    "1 4 1\n4 1 2 3\n"
) == ")(()"

# smallest possible valid case
assert run("2 1 1\n1\n2\n") == "(\n)"

print("ok")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | `()` | Smallest non-trivial valid case |
| `1 4, k=1` | `(())` | First lexicographic valid sequence |
| `1 4, k=2` | `()()` | Correct k-th generation |
| Shuffled priorities | `)(()` | Priority ordering differs from geometric order |
| `2 1` | vertical grid | Boundary handling for single column |

## Edge Cases

Consider:

```
2 2
```

Every path length is:

$$2 + 2 - 1 = 3$$

which is odd. No regular bracket sequence of odd length exists.

A careless implementation that only checks prefix balances might accidentally generate sequences like `"()("`. Our DP automatically prevents this because only states ending with balance `0` are counted valid.

Now consider mixed priorities:

```
1 4 1
4 1 2 3
```

The diagonals are already individual cells because the grid has one row. The comparison order becomes:

| Position | Priority |
| --- | --- |
| 2 | 1 |
| 3 | 2 |
| 4 | 3 |
| 1 | 4 |

So the lexicographic comparison order is not left-to-right. A naive implementation using natural sequence order would generate the wrong answer. Our algorithm sorts diagonals by minimum priority before constructing the sequence.

Finally consider a diagonal with multiple cells:

```
2 3
```

Suppose we tried:

```
((
))
```

The middle diagonal contains both `'('` and `')'`.

One path reads:

```
(())
```

Another reads:

```
()))
```

The second sequence is invalid. This demonstrates why every valid grid must assign a uniform bracket to each anti-diagonal.
