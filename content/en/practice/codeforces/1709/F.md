---
title: "CF 1709F - Multiset of Strings"
description: "Think of all binary strings of length at most n as the nodes of a complete binary trie of depth n. Every node except the root receives a capacity cs between 0 and k. A multiset of binary strings of length exactly n assigns some multiplicity to every leaf."
date: "2026-06-09T20:55:41+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dp", "fft", "flows", "graphs", "math", "meet-in-the-middle", "trees"]
categories: ["algorithms"]
codeforces_contest: 1709
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 132 (Rated for Div. 2)"
rating: 2500
weight: 1709
solve_time_s: 108
verified: true
draft: false
---

[CF 1709F - Multiset of Strings](https://codeforces.com/problemset/problem/1709/F)

**Rating:** 2500  
**Tags:** bitmasks, brute force, dp, fft, flows, graphs, math, meet-in-the-middle, trees  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of all binary strings of length at most `n` as the nodes of a complete binary trie of depth `n`.

Every node except the root receives a capacity `c_s` between `0` and `k`. A multiset of binary strings of length exactly `n` assigns some multiplicity to every leaf. For any trie node `s`, the total multiplicity inside its subtree cannot exceed `c_s`.

For a fixed assignment of capacities, define the maximum size of a beautiful multiset. The task is not to find that maximum. Instead, we must count how many capacity assignments produce maximum value exactly `f`.

The trie contains

$$2^1+2^2+\cdots+2^n=2^{n+1}-2$$

nodes with capacities. Even for `n = 15`, this is 65534 variables, so direct enumeration is hopeless.

The bound `n ≤ 15` is small, but `k` and `f` are as large as `2·10^5`. This strongly suggests that the interesting state is not the trie structure itself, but the value that each subtree can contribute. Any solution that keeps states for all capacity assignments is impossible, while a solution whose complexity is roughly polynomial in `k` and linear in `n` is feasible.

A subtle edge case appears when `f` exceeds every achievable answer.

For example:

```
n = 1
k = 1
f = 3
```

Each leaf capacity is at most `1`, so the maximum beautiful multiset size is at most `2`. The correct answer is `0`. A solution that only computes distributions up to `k` would incorrectly miss the fact that the root can reach values up to `2k`.

Another easy mistake is handling the equality case incorrectly in the transition.

Suppose a subtree's children can contribute exactly `j`. Then every capacity choice `c ≥ j` produces subtree value `j`. There are `k-j+1` such capacities, not `k-j`. Missing this extra possibility shifts the entire distribution.

## Approaches

The brute-force interpretation is straightforward.

Assign a value between `0` and `k` to every trie node. For each assignment, compute the maximum beautiful multiset size and check whether it equals `f`.

The trie contains `2^{n+1}-2` nodes, so the number of assignments is

$$(k+1)^{2^{n+1}-2}.$$

Even for `n=15` and `k=1`, this is astronomically large.

The key observation is that a subtree can be summarized by a single number.

Let `val(v)` be the maximum number of strings that can be placed inside the subtree rooted at node `v`.

For a leaf,

$$val(v)=c_v.$$

For an internal non-root node,

$$val(v)=\min(c_v,\; val(l)+val(r)).$$

The children together can supply at most `val(l)+val(r)` strings, but the node capacity may impose a tighter limit.

This means that the exact arrangement of capacities below a node is irrelevant once we know the resulting value of that subtree. We only need to count how many assignments produce each possible value.

If we know the distribution for a subtree of height `h-1`, then combining two children requires counting all pairs whose values sum to `t`. That is exactly a convolution.

Since `k` reaches `2·10^5`, naive quadratic convolution is too expensive. The problem becomes a sequence of polynomial convolutions, which can be accelerated with NTT.

The resulting dynamic programming runs in roughly `O(n k log k)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| DP + NTT | O(nk log k) | O(k) | Accepted |

## Algorithm Walkthrough

Let `dp[h][x]` denote the number of capacity assignments for a non-root complete binary subtree of height `h` whose maximum contribution equals exactly `x`.

Height `0` means a leaf.

### 1. Initialize leaf distributions

A leaf value equals its capacity.

For every `0 ≤ x ≤ k`:

$$dp[0][x]=1.$$

### 2. Combine two child subtrees

Assume we already know the distribution for height `h-1`.

Let

$$H[t] = \sum_{a+b=t} dp[h-1][a]\cdot dp[h-1][b].$$

`H[t]` counts assignments whose two children contribute total value `t`.

This is a polynomial convolution, computed using NTT.

### 3. Apply the node capacity

For a fixed child sum `t`, the parent value is

$$\min(c,t).$$

We need the number of ways to obtain each resulting value `j`.

If `t=j`, then any capacity `c≥j` works. There are `k-j+1` choices.

If `t>j`, then the only way to obtain value `j` is choosing `c=j`.

Hence

$$dp[h][j] = (k-j+1)H[j] + \sum_{t>j} H[t].$$

Rewriting:

$$dp[h][j] = (k-j)H[j] + \sum_{t\ge j} H[t].$$

The suffix sums of `H` allow this transition in linear time.

### 4. Repeat until reaching depth `n-1`

All non-root levels are processed using the previous transition.

### 5. Handle the root

The root has no capacity.

Its value is simply

$$val(root)=val(left)+val(right).$$

So the final answer distribution is just one more convolution of the height `n-1` distribution with itself.

The coefficient of `f` is the answer.

### Why it works

For every subtree, the only information needed by ancestors is the maximum number of strings that can be placed inside that subtree. The recursive formula

$$val(v)=\min(c_v,\; val(l)+val(r))$$

shows that the internal structure below a node influences higher levels only through this single value.

The DP counts exactly how many capacity assignments produce each possible subtree value. Convolution enumerates all pairs of child values. The capacity transition enumerates all capacities that transform a child sum into a given parent value. Since every assignment is counted once and only once at every level, the final distribution at the root is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
G = 3

def mod_pow(a, e):
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def ntt(a, invert):
    n = len(a)

    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        wlen = mod_pow(G, (MOD - 1) // length)
        if invert:
            wlen = mod_pow(wlen, MOD - 2)

        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD

                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD

                w = w * wlen % MOD

        length <<= 1

    if invert:
        inv_n = mod_pow(n, MOD - 2)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def convolution(a, b):
    need = len(a) + len(b) - 1
    n = 1
    while n < need:
        n <<= 1

    fa = a[:] + [0] * (n - len(a))
    fb = b[:] + [0] * (n - len(b))

    ntt(fa, False)
    ntt(fb, False)

    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD

    ntt(fa, True)

    return fa[:need]

def solve():
    n, k, f = map(int, input().split())

    dp = [1] * (k + 1)

    for level in range(1, n):
        h = convolution(dp, dp)

        m = len(h)
        suf = [0] * (m + 1)
        for i in range(m - 1, -1, -1):
            suf[i] = (suf[i + 1] + h[i]) % MOD

        ndp = [0] * (k + 1)
        for j in range(k + 1):
            ndp[j] = ((k - j) * h[j] + suf[j]) % MOD

        dp = ndp

    root = convolution(dp, dp)

    if f >= len(root):
        print(0)
    else:
        print(root[f] % MOD)

solve()
```

The base distribution corresponds to leaves. Each internal level first performs a convolution, producing the distribution of child sums. After that, the suffix-sum transition applies the parent capacity.

The expression

```
(k - j) * h[j] + suf[j]
```

implements

$$(k-j)H[j]+\sum_{t\ge j}H[t].$$

The root is treated separately because it has no capacity restriction.

One implementation detail that is easy to miss is the maximum value range. Internal subtree values never exceed `k`, but the root is the sum of two such values, so the final distribution extends up to `2k`. That is why we must check `f >= len(root)` before indexing.

## Worked Examples

### Example 1

Input

```
1 42 2
```

For `n=1`, there are only two leaves.

| Step | Distribution |
| --- | --- |
| Leaf values | `dp[x]=1` for `0≤x≤42` |
| Root convolution | coefficient of sum `2` equals `3` |

The pairs producing sum `2` are:

| Left | Right |
| --- | --- |
| 0 | 2 |
| 1 | 1 |
| 2 | 0 |

There are exactly `3` assignments.

Output:

```
3
```

This example shows that when `n=1`, the answer is simply the number of ordered pairs of leaf capacities summing to `f`.

### Example 2

Input

```
1 1 3
```

| Step | Result |
| --- | --- |
| Leaf values | `{0,1}` |
| Root sums | `{0,1,2}` |
| Value 3 present? | No |

The final polynomial has degree `2`.

Since `3 > 2k`, the answer is:

```
0
```

This demonstrates the importance of handling values beyond the support of the distribution.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk log k) | One NTT convolution per trie level |
| Space | O(k) | A few arrays of size proportional to the polynomial length |

With `n ≤ 15` and `k ≤ 2·10^5`, the largest polynomial size is about `4·10^5`. NTT handles such convolutions comfortably within the limits, and only a small number of levels are processed.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    MOD = 998244353

    # paste solve() implementation here
    return out

# provided sample
assert run("1 42 2\n") == "3\n"

# minimum values
assert run("1 1 0\n") == "1\n"

# impossible target
assert run("1 1 3\n") == "0\n"

# all pairs summing to 1
assert run("1 5 1\n") == "2\n"

# largest achievable value for n=1
assert run("1 3 6\n") == "1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 42 2` | `3` | Official sample |
| `1 1 0` | `1` | Smallest achievable answer |
| `1 1 3` | `0` | Target beyond maximum range |
| `1 5 1` | `2` | Ordered pair counting |
| `1 3 6` | `1` | Maximum root value |

## Edge Cases

Consider:

```
1 1 3
```

Each leaf capacity is at most `1`, so the root value is at most `2`. The final convolution has coefficients only for sums `0,1,2`. Since index `3` does not exist, the algorithm returns `0`.

Now consider:

```
2 2 1
```

Suppose a child sum equals exactly `1`. Every capacity choice `c=1` or `c=2` produces parent value `1`. The transition contributes `k-j+1 = 2` possibilities. Using `k-j` instead would count only one of them and produce an incorrect distribution. The suffix-sum formula correctly includes the equality case.

Finally, consider:

```
1 3 6
```

The only ordered pair summing to `6` is `(3,3)`. The root convolution coefficient at index `6` is exactly `1`, confirming that the algorithm correctly handles the upper boundary `2k`.
