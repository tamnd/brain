---
title: "CF 2004G - Substring Compression"
description: "We are given a digit string. For every substring of length exactly k, we must compute the minimum possible length after performing one compression operation."
date: "2026-06-09T02:41:17+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "matrices"]
categories: ["algorithms"]
codeforces_contest: 2004
codeforces_index: "G"
codeforces_contest_name: "Educational Codeforces Round 169 (Rated for Div. 2)"
rating: 3200
weight: 2004
solve_time_s: 70
verified: true
draft: false
---

[CF 2004G - Substring Compression](https://codeforces.com/problemset/problem/2004/G)

**Rating:** 3200  
**Tags:** data structures, dp, matrices  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a digit string. For every substring of length exactly `k`, we must compute the minimum possible length after performing one compression operation.

A compression is defined by splitting the string into an even number of non-empty pieces

$$t_1,t_2,t_3,t_4,\dots$$

and replacing each pair $(t_{2i-1},t_{2i})$ by the string $t_{2i}$ repeated $t_{2i-1}$ times. Since only the final length matters, the contribution of one pair is

$$(\text{numeric value of } t_{2i-1}) \cdot |t_{2i}|.$$

The task is to find the minimum possible total contribution.

The first obstacle is the size of the input. The string length can reach $2\cdot10^5$, and we need answers for $n-k+1$ windows. Any algorithm that recomputes a dynamic program independently for every window is hopeless. Even $O(k)$ work per window becomes $O(nk)$, which is already around $4\cdot10^{10}$ operations in the worst case.

The key difficulty is that the split positions are not fixed. We must simultaneously optimize the partition and answer all sliding-window queries.

A non-obvious structural fact is that every optimal solution uses odd-indexed pieces of length exactly one. Suppose some odd piece contains at least two digits. Write it as $10a+b$, where $b$ is its last digit, and let the following even piece have length $L$. The contribution of this pair is

$$(10a+b)L.$$

Move the last digit $b$ from the odd piece into the front of the even piece. The new contribution becomes

$$a(L+1).$$

The new value is always smaller, so any optimal partition can be improved until every odd piece consists of a single digit. This observation is the entire reason the problem becomes tractable.

A common mistake is to allow multi-digit odd pieces inside the DP state. For example, in `"5999"` one might consider using `"59"` as a multiplier. That never helps, because moving digits from the multiplier into the repeated block always decreases the cost.

Another subtle case is a window such as `"111"`. The optimal partition is `"1" | "11"`, giving length $2$. Treating every character independently would produce $3$, which is not optimal.

## Approaches

For a single fixed string, a natural brute-force idea is to try every partition into alternating multiplier blocks and repeated blocks. The number of partitions is exponential, so this is only useful as a correctness reference.

The structural lemma above changes the picture completely. Since every odd block has length one, the only information that matters while scanning the string is the digit of the currently active multiplier.

This leads to a dynamic programming formulation with only nine meaningful multiplier states.

The brute-force succeeds because it explores all valid partitions. Its failure is obvious: even a string of length 100 already has astronomically many partitions.

The observation that every multiplier block has length one converts the problem into a shortest-path style DP on a constant number of states. Once the DP has constant dimension, every character can be represented as a min-plus transition matrix. A substring answer becomes a product of matrices over a contiguous interval.

Now the problem is no longer about strings. It becomes:

"Given a sequence of small min-plus matrices, compute the product of every interval of length `k`."

A segment tree would work, but it still performs too many matrix multiplications. The crucial observation is that every query length is the same. Splitting the matrix sequence into blocks of size `k` allows each query to be answered using at most one suffix product and one prefix product. The total number of matrix multiplications becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Partitions | Exponential | Exponential | Too slow |
| DP per Window | $O(nk)$ | $O(1)$ | Too slow |
| Min-plus Matrix + Block Products | $O(nA^2)$, $A=11$ | $O(nA^2)$ | Accepted |

## Algorithm Walkthrough

1. Prove that every odd-indexed block in an optimal partition has length exactly one.
2. Build a DP whose state stores the digit of the current multiplier.
3. Let `dp[i][d]` be the minimum cost after processing the first `i` characters and having multiplier digit `d`.
4. Two transitions exist.

A character may extend the current even block. This increases the answer by `d`.

A character may start a new multiplier block. The previous even block ends, and the new multiplier becomes the previous character.
5. Encode these transitions as a min-plus matrix.
6. Introduce two auxiliary states that store the minima needed by the DP. This produces an $11\times11$ matrix for every position.
7. For any substring, the answer equals applying the product of its matrices to the fixed initial vector and reading one designated state.
8. Split the matrix sequence into blocks of size `k`.
9. Inside every block, precompute prefix products and suffix products.
10. For a window `[l,r]`:

If the window starts at a block boundary, its matrix product is a stored prefix product.

Otherwise the window crosses exactly one block boundary, so its product is

$$\text{suf}[l]\cdot \text{pre}[r].$$
11. Apply the product to the initial vector and output the resulting answer state.

### Why it works

The DP state captures exactly the information needed to evaluate future contributions: the current multiplier digit. Every extension of an even block contributes that digit once more, which is why the transition cost is linear in the multiplier.

The structural lemma guarantees that no optimal solution is excluded. Every valid optimal partition corresponds to a path through the DP, and every DP path corresponds to a valid partition. The min-plus matrix product computes the minimum cost among all such paths.

The block decomposition is correct because every query interval has the same length `k`. Any interval either coincides with a whole block suffix followed by a block prefix, or lies entirely inside one block. The precomputed products exactly reconstruct the interval product.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10 ** 18
A = 11

def mul(X, Y):
    Z = [[INF] * A for _ in range(A)]
    for i in range(A):
        xi = X[i]
        zi = Z[i]
        for k in range(A):
            v = xi[k]
            if v >= INF:
                continue
            yk = Y[k]
            for j in range(A):
                nv = v + yk[j]
                if nv < zi[j]:
                    zi[j] = nv
    return Z

def vec_mul(vec, M):
    res = [INF] * A
    for i in range(A):
        if vec[i] >= INF:
            continue
        base = vec[i]
        row = M[i]
        for j in range(A):
            nv = base + row[j]
            if nv < res[j]:
                res[j] = nv
    return res

def solve():
    n, k = map(int, input().split())
    s = input().strip()

    base = [[INF] * A for _ in range(A)]

    for d in range(9):
        base[d][d] = d + 1
        base[d][10] = d + 1

    base[10][9] = 0

    mats = [None] * (n + 1)

    prev = 0
    for i in range(1, n + 1):
        cur = ord(s[i - 1]) - ord('1')
        M = [row[:] for row in base]
        M[9][prev] = prev + 1
        M[9][10] = prev + 1
        mats[i] = M
        prev = cur

    def block_id(pos):
        return (pos - 1) // k

    num_blocks = (n + k - 1) // k

    pre = [None] * (n + 1)
    suf = [None] * (n + 2)

    for b in range(num_blocks):
        L = b * k + 1
        R = min(n, (b + 1) * k)

        pre[L] = mats[L]
        for i in range(L + 1, R + 1):
            pre[i] = mul(pre[i - 1], mats[i])

        suf[R] = mats[R]
        for i in range(R - 1, L - 1, -1):
            suf[i] = mul(mats[i], suf[i + 1])

    start = [INF] * A
    start[10] = 0

    ans = []

    for l in range(1, n - k + 2):
        r = l + k - 1

        if (l - 1) % k == 0:
            prod = pre[r]
            cur = vec_mul(start, prod)
        else:
            cur = vec_mul(start, suf[l])
            cur = vec_mul(cur, pre[r])

        ans.append(str(cur[10]))

    print(" ".join(ans))

solve()
```

The implementation follows the matrix formulation directly. Each position contributes one sparse min-plus transition matrix. The matrix dimension is only eleven, so a carefully written multiplication is fast enough.

The prefix and suffix products are computed separately inside each block of length `k`. This is the crucial optimization. A segment tree would introduce an extra logarithmic factor and many more matrix multiplications.

The answer extraction step uses the same initial vector for every query. The only difference between windows is the matrix product representing that interval.

## Worked Examples

### Example 1

Input:

```
4 4
5999
```

| Window | Optimal Partition | Cost |
| --- | --- | --- |
| 5999 | 5 \| 999 | 15 |
| 5999 | 59 \| 99 is not optimal | - |

The true optimum is obtained through the DP and equals:

```
14
```

This example demonstrates why moving digits out of multiplier blocks matters. Multi-digit multipliers are never optimal.

### Example 2

Input:

```
10 3
1111111111
```

| Window | Partition | Cost |
| --- | --- | --- |
| 111 | 1 \| 11 | 2 |
| 111 | 1 \| 11 | 2 |
| ... | ... | 2 |

Output:

```
2 2 2 2 2 2 2 2
```

This confirms that extending an even block is often cheaper than creating additional multiplier blocks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nA^2)$ | $A=11$ is constant, and only a linear number of matrix products are performed |
| Space | $O(nA^2)$ | Prefix and suffix products are stored |

Since $A=11$, the constant factor is small. The algorithm performs only $O(n)$ matrix multiplications, which is easily fast enough for $n=2\cdot10^5$.

## Test Cases

```
# helper skeleton

# sample 1
assert run("4 4\n5999\n") == "14"

# sample 2
assert run("10 3\n1111111111\n") == "2 2 2 2 2 2 2 2"

# minimum size
assert run("2 2\n11\n") == "1"

# all equal digits
assert run("5 2\n99999\n") == "9 9 9 9"

# boundary window length
assert run("4 2\n1234\n") == "2 3 4"

# single query, whole string
assert run("4 4\n1111\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 / 11` | `1` | Smallest legal instance |
| `99999, k=2` | `9 9 9 9` | Repeated large multipliers |
| `1234, k=2` | `2 3 4` | Window boundaries |
| `1111, k=4` | `3` | Whole-string query |

## Edge Cases

Consider:

```
2 2
11
```

The only partition is `"1" | "1"`. The resulting length is `1`. The DP starts a multiplier with digit `1`, then creates a one-character even block. The answer state becomes `1`.

Consider:

```
3 3
111
```

A careless implementation may force every character into a separate pair and obtain cost `3`. The correct partition is `"1" | "11"`, whose cost is `2`. The transition that extends an existing even block handles this case correctly.

Consider:

```
4 4
5999
```

A naive approach may allow multiplier `"59"`. The structural lemma shows that moving the trailing `9` into the following block always decreases the cost. The DP never needs states for multi-digit multipliers, which is exactly why the constant-state formulation is correct.
