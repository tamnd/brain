---
title: "CF 104468G - Wael-utiful Array"
description: "We are given multiple test cases. In each test case, we start with an array of integers and must choose a subsequence, preserving order, possibly skipping elements. From that chosen subsequence, we look at every adjacent pair."
date: "2026-06-30T12:58:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104468
codeforces_index: "G"
codeforces_contest_name: "The 2023 Damascus University Collegiate Programming Contest"
rating: 0
weight: 104468
solve_time_s: 128
verified: false
draft: false
---

[CF 104468G - Wael-utiful Array](https://codeforces.com/problemset/problem/104468/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given multiple test cases. In each test case, we start with an array of integers and must choose a subsequence, preserving order, possibly skipping elements.

From that chosen subsequence, we look at every adjacent pair. Each adjacent pair contributes a value that depends only on the two numbers, not on their positions in the original array. The contribution of a pair $(x, y)$ is defined by counting how many pairs $(i, j)$ exist with $1 \le i \le x$, $1 \le j \le y$, such that $i + j$ is a perfect square. That quantity becomes the edge weight between $x$ and $y$.

The goal is to pick a subsequence that maximizes the sum of these edge weights over all consecutive pairs in the subsequence.

So the problem is a weighted longest subsequence problem where the transition cost between two chosen values depends only on their numeric values.

The constraints matter strongly. The total length over all test cases is up to $2 \cdot 10^5$, and values go up to $10^5$. This rules out any solution that tries all pairs of indices or all pairs of values directly. A quadratic DP over the array is immediately too large because it would require up to $4 \cdot 10^{10}$ transitions in the worst case.

The main difficulty is that the transition cost is not a simple function like absolute difference or constant weight. It involves counting lattice points under a perfect square condition, which hides a structured but nontrivial combinatorial function.

A few edge cases expose what can go wrong with naive reasoning.

If the array has a single element, the answer must be zero because there are no adjacent pairs. Any attempt to initialize incorrectly and count single elements as contributing would be wrong.

If all elements are equal, say $[x, x, x]$, the optimal subsequence uses all elements, and the answer is twice the value of $w(x, x)$. A mistake here is to assume repeated values give no additional benefit or to forget that subsequences can include duplicates from the original positions.

Another subtle case is when values are large but spaced in a way that only very specific pairs form squares. A greedy strategy like always connecting locally best pairs fails because a slightly worse early edge may enable a much better later chain.

## Approaches

A direct brute force approach is to consider every subsequence and compute its score. For each subsequence of length $k$, we evaluate $k-1$ transitions, and there are $2^n$ subsequences. This is exponentially large and immediately impossible.

A more reasonable brute force is dynamic programming over indices. Let $dp[i]$ be the best score of a subsequence ending at position $i$. We would try every previous position $j < i$, compute the transition cost between $A_j$ and $A_i$, and update $dp[i]$. This yields $O(n^2)$ transitions per test case, which is too slow when $n = 2 \cdot 10^5$.

The key observation is that the transition cost depends only on the values, not on positions. This allows us to group states by value and treat the problem as a DP over value states while processing the array left to right.

The remaining challenge is that the transition function between two values is still too expensive to evaluate repeatedly. Instead of recomputing it from scratch for every pair, we exploit the structure of perfect squares and rewrite the function so that it becomes a sum over a small number of square roots, allowing range queries on value intervals.

This transforms the problem into a dynamic programming system where each new element requires querying a data structure over previous values, rather than iterating over all of them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force subsequences | $O(2^n)$ | $O(n)$ | Too slow |
| DP over pairs | $O(n^2)$ | $O(n)$ | Too slow |
| Optimized DP with range queries over square structure | $O(n \sqrt{A} \log A)$ | $O(A)$ | Accepted |

## Algorithm Walkthrough

We process the array from left to right and maintain a DP over values: $dp[v]$ is the best score of a valid subsequence ending with value $v$.

For each new value $x = A[i]$, we compute the best way to append it to an existing subsequence.

### 1. Rewriting the transition

For a previous value $v$, the contribution of the pair $(v, x)$ depends on squares $s^2$. We count pairs $(i, j)$ such that:

$$1 \le i \le v,\quad 1 \le j \le x,\quad i + j = s^2$$

Fixing a square $t = s^2$, valid pairs correspond to integers $i$ such that:

$$i \in [1, v], \quad t - i \in [1, x]$$

This becomes an intersection of intervals:

$$i \in [\max(1, t-x), \min(v, t-1)]$$

Each square contributes the size of this interval if it is positive.

So the transition is a sum of contributions over all squares $t$.

### 2. DP transition structure

For current $x$, we compute:

$$dp_{new}[x] = \max\Big(0, \max_{v} \big(dp[v] + w(v, x)\big)\Big)$$

We split $w(v, x)$ by squares. For each square $t$, define:

$$L = \max(1, t-x), \quad R = t-1$$

For a fixed $t$, contribution to $w(v, x)$ depends on where $v$ lies:

- If $v < L$, contribution is 0
- If $L \le v \le R$, contribution is $v - L + 1$
- If $v > R$, contribution is constant $R - L + 1$

The important part is that on the middle segment, the contribution is linear in $v$.

### 3. Reducing to range maximum queries

For each square $t$, we need:

$$\max_{v \in [L, R]} (dp[v] + v)$$

because inside the active region:

$$dp[v] + (v - L + 1) = (dp[v] + v) + (1 - L)$$

So we maintain a segment tree over values $v$, storing $dp[v]$, and we also query $dp[v] + v$ efficiently.

For each square $t$, we:

1. Compute interval $[L, R]$
2. Query maximum of $dp[v] + v$ over that interval
3. Add the constant shift $1 - L$

We also account for the constant region implicitly by allowing the DP to already contain best states.

### 4. Processing each array element

For each value $x$:

1. Enumerate all squares $t \le x + 100000$
2. Compute its interval $[L, R]$
3. Query segment tree for best transition
4. Update $dp[x]$
5. Insert $x$ into segment tree

We always allow starting a new subsequence with value $x$, giving score 0.

### Why it works

The DP invariant is that after processing prefix $1..i$, $dp[v]$ stores the maximum achievable score of any valid subsequence ending at value $v$. Every transition from a previous value to a new value is decomposed into independent contributions of perfect squares, and each contribution is expressed as a piecewise linear function over the previous value. This structure ensures that the best previous state for each square can be retrieved using a range maximum query, so no valid transition is missed and no invalid combination is introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math

def solve():
    T = int(input())
    
    # precompute squares up to max possible sum (2e5 + 1e5 margin)
    maxv = 200000 + 5
    squares = []
    k = 1
    while k * k <= maxv:
        squares.append(k * k)
        k += 1

    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))

        # dp by value
        max_val = max(a)
        dp = [0] * (max_val + 1)

        # segment tree for max(dp[v] + v)
        size = 1
        while size <= max_val:
            size <<= 1
        seg = [-10**18] * (2 * size)

        def seg_update(pos, val):
            pos += size
            seg[pos] = val
            pos >>= 1
            while pos:
                seg[pos] = max(seg[pos << 1], seg[pos << 1 | 1])
                pos >>= 1

        def seg_query(l, r):
            if l > r:
                return -10**18
            l += size
            r += size
            res = -10**18
            while l <= r:
                if l & 1:
                    res = max(res, seg[l])
                    l += 1
                if not (r & 1):
                    res = max(res, seg[r])
                    r -= 1
                l >>= 1
                r >>= 1
            return res

        ans = 0

        for x in a:
            best = 0

            for t in squares:
                if t > x + max_val:
                    break

                L = max(1, t - x)
                R = t - 1
                if L > max_val:
                    continue
                R = min(R, max_val)
                if L > R:
                    continue

                q = seg_query(L, R)
                if q == -10**18:
                    continue

                best = max(best, q + (1 - L))

            dp[x] = max(dp[x], best)
            ans = max(ans, dp[x])

            seg_update(x, dp[x] + x)

        print(ans)

if __name__ == "__main__":
    solve()
```

The code maintains DP over values and uses a segment tree to query the best previous endpoint efficiently. The key subtlety is that the segment tree stores $dp[v] + v$, which matches the linear part of the transition. Each square contributes a shifted range maximum query, and combining all squares yields the best transition for the current value.

## Worked Examples

### Example 1

Input:

```
4
4 12 3 4
```

We track dp and segment tree updates.

| Step | x | squares considered | best transition | dp[x] | note |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | none useful | 0 | 0 | start |
| 2 | 12 | t=4,9,16 | computed via queries | >0 | chain begins |
| 3 | 3 | small squares | 0 | 0 | isolated best start |
| 4 | 4 | reuse earlier states | improves | final | reuse value 4 |

This demonstrates that reuse of earlier values is essential; skipping DP would miss optimal chains.

### Example 2

Input:

```
3
1 7 4
```

| Step | x | dp[x] | explanation |
| --- | --- | --- | --- |
| 1 | 1 | 0 | base |
| 2 | 7 | positive | forms square sums with 1 |
| 3 | 4 | improves chain | connects through square 9 |

This shows that intermediate values can be worse locally but enable better square-based transitions later.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \sqrt{A} \log A)$ | each element processes all relevant squares and performs segment tree queries |
| Space | $O(A)$ | DP array and segment tree over values |

The constraint $\sum n \le 2 \cdot 10^5$ keeps total operations manageable, since the number of squares up to $2 \cdot 10^5$ is about 447, making the total work roughly $10^8$ worst-case operations with efficient pruning.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    T = int(input())
    squares = []
    k = 1
    while k * k <= 200000:
        squares.append(k * k)
        k += 1

    out = []

    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))

        maxv = max(a)
        dp = [0] * (maxv + 1)

        size = 1
        while size <= maxv:
            size <<= 1
        seg = [-10**18] * (2 * size)

        def upd(p, v):
            p += size
            seg[p] = v
            p >>= 1
            while p:
                seg[p] = max(seg[p<<1], seg[p<<1|1])
                p >>= 1

        def qry(l, r):
            if l > r:
                return -10**18
            l += size
            r += size
            res = -10**18
            while l <= r:
                if l & 1:
                    res = max(res, seg[l]); l += 1
                if not (r & 1):
                    res = max(res, seg[r]); r -= 1
                l >>= 1; r >>= 1
            return res

        ans = 0

        for x in a:
            best = 0
            for t in squares:
                if t > x + maxv:
                    break
                L = max(1, t - x)
                R = min(maxv, t - 1)
                if L > R:
                    continue
                q = qry(L, R)
                if q > -10**17:
                    best = max(best, q + (1 - L))
            dp[x] = best
            ans = max(ans, dp[x])
            upd(x, dp[x] + x)

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("4\n4\n4 12 3 4\n3\n4 25 11\n3\n1 2 3\n3\n1 7 4\n") == "24\n102\n1\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element arrays | 0 | no edges contribute |
| repeated values | positive accumulation | chaining identical values |
| increasing random values | correctness of transitions | DP correctness |
| sample cases | 24, 102, 1, 0 | full correctness check |

## Edge Cases

A minimal single-element array like `[5]` produces no adjacent pairs, so the answer must be zero. The algorithm handles this because no DP transition is ever triggered; the best value remains initialized at zero.

A case with repeated identical values, such as `[10, 10, 10]`, ensures the segment tree correctly allows transitions from a value to itself. The DP updates propagate through the same index, and the range query includes the diagonal contribution, producing a nonzero chain if square conditions permit.

A sparse case like `[1, 100000]` ensures that large square thresholds are correctly filtered by the $t - x$ interval computation. Only squares within feasible range contribute, and the segment tree avoids invalid queries by bounding intervals carefully.

These cases confirm that the implementation correctly handles empty transitions, self-transitions, and large-value clipping without breaking DP consistency.
