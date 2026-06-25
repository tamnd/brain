---
title: "CF 105757H - Klein Moretti's Riddle"
description: "We are given an array of length n and a fixed subsequence size k. For every query value x, we must count how many subsequences containing exactly k elements have bitwise OR equal to x."
date: "2026-06-25T23:22:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105757
codeforces_index: "H"
codeforces_contest_name: "Insomnia 2025"
rating: 0
weight: 105757
solve_time_s: 50
verified: true
draft: false
---

[CF 105757H - Klein Moretti's Riddle](https://codeforces.com/problemset/problem/105757/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length `n` and a fixed subsequence size `k`. For every query value `x`, we must count how many subsequences containing exactly `k` elements have bitwise OR equal to `x`.

A subsequence here is determined by the chosen positions, so if the same value appears multiple times, different occurrences are counted separately.

The constraints are the main challenge. Both `n` and the number of queries can reach one million, and every array value as well as every query value is at most one million. Since `10^6 < 2^20`, every value fits inside 20 bits. A solution that processes each query independently is immediately ruled out. Even an `O(q log n)` approach is too expensive when `q = 10^6`. The only realistic direction is to preprocess answers for every possible 20-bit mask once, then answer each query in constant time.

A common mistake is to think directly about OR values of subsequences. The number of possible subsequences is enormous.

Consider:

```
n = 3, k = 2
a = [1, 2, 4]
```

The subsequences are:

```
{1,2} -> 3
{1,4} -> 5
{2,4} -> 6
```

Trying to generate OR values explicitly clearly does not scale.

Another subtle case appears when multiple values are identical:

```
n = 4, k = 2
a = [1,1,1,1]
```

The OR is always `1`, but the answer is not `1`. It is:

```
C(4,2) = 6
```

We count position choices, not distinct value sets.

A third edge case occurs when a query mask contains a bit that never appears in any chosen element:

```
n = 3, k = 2
a = [1,2,2]
query = 7
```

No subsequence can produce bit `4`, so the answer is `0`. Any approach that only tracks subsets of query masks without respecting actual frequencies can incorrectly produce a nonzero result.

## Approaches

The brute-force idea is straightforward. Enumerate every subsequence of size `k`, compute its OR, and count how many times each OR value appears.

This is correct because every valid subsequence is examined exactly once.

The problem is the number of subsequences:

```
C(n,k)
```

Even for moderate values of `n`, this becomes astronomically large. With `n` up to one million, brute force is completely impossible.

The key observation comes from reversing the question.

Instead of asking:

```
How many subsequences have OR exactly x?
```

ask:

```
How many subsequences have OR contained inside x?
```

A subsequence has OR contained inside `x` if every selected element uses only bits already present in `x`.

For a mask `x`, let:

```
g[x] = number of array elements whose bit set is a subset of x
```

Every size-`k` subsequence chosen from these `g[x]` elements has OR at most `x`.

Hence:

```
F[x] = C(g[x], k)
```

counts subsequences whose OR is a subset of `x`.

Now let:

```
ans[x] = number of subsequences whose OR equals x
```

Every subsequence counted in `F[x]` contributes to exactly one OR value `y` with `y ⊆ x`.

So:

```
F[x] = Σ ans[y]
       y⊆x
```

This is a classic subset zeta transform relationship.

Once all `F[x]` values are known, we recover the exact answers using subset Möbius inversion.

The remaining task is computing `g[x]`.

Let `freq[v]` be the frequency of value `v` in the array.

Then:

```
g[x] = Σ freq[s]
       s⊆x
```

which is exactly the subset-sum SOS DP.

Since there are only `2^20 = 1,048,576` masks, a 20-dimensional SOS transform is feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n,k) · k) | O(number of OR values) | Too slow |
| Optimal | O(20 · 2^20 + n + q) | O(2^20) | Accepted |

## Algorithm Walkthrough

1. Read the array and build a frequency array `freq`, where `freq[v]` stores how many times value `v` appears.
2. Precompute factorials and inverse factorials modulo `10^9+7` up to `n`, allowing constant-time computation of combinations.
3. Copy `freq` into an array `g`.
4. Run the subset SOS transform on `g`.

After this transform:

```
g[x] = Σ freq[s]
       s⊆x
```

which equals the number of array elements whose masks are subsets of `x`.
5. For every mask `x`, compute:

```
F[x] = C(g[x], k)
```

If `g[x] < k`, the value is zero.
6. Apply subset Möbius inversion to `F`.

After inversion:

```
F[x] = Σ ans[y]
       y⊆x
```

becomes

```
ans[x]
```

directly.
7. For each query value `x`, output `ans[x]`.

### Why it works

For a fixed mask `x`, the only elements that can participate in a subsequence whose OR is contained inside `x` are elements whose own masks are subsets of `x`. The SOS transform computes exactly how many such elements exist.

Choosing any `k` of those elements gives a subsequence whose OR is also a subset of `x`, so `F[x] = C(g[x],k)` counts all subsequences with OR at most `x`.

Every subsequence contributes to exactly one OR value. Consequently, `F[x]` is the sum of exact OR counts over all masks contained in `x`. Subset Möbius inversion is precisely the inverse operation of this summation, so it recovers the exact number of subsequences whose OR equals each mask.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MOD = 1000000007
B = 20
M = 1 << B

def main():
    n, k = map(int, input().split())

    freq = array('I', [0]) * M
    arr = list(map(int, input().split()))
    for x in arr:
        freq[x] += 1

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    ifact = [1] * (n + 1)
    ifact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        ifact[i - 1] = ifact[i] * i % MOD

    def comb(nn, rr):
        if nn < rr:
            return 0
        return fact[nn] * ifact[rr] % MOD * ifact[nn - rr] % MOD

    g = array('I', freq)

    for bit in range(B):
        step = 1 << bit
        for mask in range(M):
            if mask & step:
                g[mask] += g[mask ^ step]

    dp = [0] * M
    for mask in range(M):
        dp[mask] = comb(g[mask], k)

    for bit in range(B):
        step = 1 << bit
        for mask in range(M):
            if mask & step:
                dp[mask] -= dp[mask ^ step]
                dp[mask] %= MOD

    q = int(input())
    out = []
    for _ in range(q):
        x = int(input())
        out.append(str(dp[x]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The frequency array stores how many times each value appears in the input. Since all values are below `2^20`, every possible mask has a dedicated slot.

The SOS transform converts frequencies into subset counts. After it finishes, `g[x]` contains the number of array elements that can appear in a subsequence whose OR does not exceed `x`.

Combination values are computed using factorials and inverse factorials. Since the modulus is prime, Fermat's theorem provides modular inverses.

The array `dp` initially stores `F[x] = C(g[x],k)`. The second SOS-style pass performs Möbius inversion. The subtraction step is the exact inverse of subset accumulation and turns "OR is contained inside x" counts into "OR equals x" counts.

The modulo operation after each subtraction is necessary because intermediate values may become negative.

## Worked Examples

### Example 1

```
n = 3, k = 2
a = [1, 2, 3]
```

Relevant masks:

| Mask | g[mask] | F[mask] = C(g,k) |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 1 | 0 |
| 2 | 1 | 0 |
| 3 | 3 | 3 |

After Möbius inversion:

| Mask | Exact OR count |
| --- | --- |
| 1 | 0 |
| 2 | 0 |
| 3 | 3 |

The three subsequences are:

```
{1,2} -> 3
{1,3} -> 3
{2,3} -> 3
```

All contribute to mask `3`.

### Example 2

```
n = 4, k = 2
a = [1,1,1,1]
```

| Mask | g[mask] | F[mask] |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 4 | 6 |

After inversion:

| Mask | Exact OR count |
| --- | --- |
| 0 | 0 |
| 1 | 6 |

This example demonstrates that subsequences are counted by positions. Even though there is only one distinct value, there are six different ways to choose two positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(20 · 2^20 + n + q) | Two SOS-style transforms dominate |
| Space | O(2^20) | Frequency and DP arrays over all masks |

`2^20` is about one million, so each SOS transform performs roughly twenty million updates. This comfortably fits within the limits for a 2-second C++ solution and is also the intended complexity of the problem.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    MOD = 1000000007
    B = 20
    M = 1 << B

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    from array import array

    freq = array('I', [0]) * M
    for x in arr:
        freq[x] += 1

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    ifact = [1] * (n + 1)
    ifact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        ifact[i - 1] = ifact[i] * i % MOD

    def C(nn, rr):
        if nn < rr:
            return 0
        return fact[nn] * ifact[rr] % MOD * ifact[nn - rr] % MOD

    g = array('I', freq)

    for bit in range(B):
        b = 1 << bit
        for mask in range(M):
            if mask & b:
                g[mask] += g[mask ^ b]

    dp = [0] * M
    for mask in range(M):
        dp[mask] = C(g[mask], k)

    for bit in range(B):
        b = 1 << bit
        for mask in range(M):
            if mask & b:
                dp[mask] = (dp[mask] - dp[mask ^ b]) % MOD

    q = int(input())
    ans = []
    for _ in range(q):
        ans.append(str(dp[int(input())]))
    return "\n".join(ans)

# custom cases
assert run("1 1\n1\n2\n1\n2\n") == "1\n0"
assert run("4 2\n1 1 1 1\n2\n1\n3\n") == "6\n0"
assert run("3 2\n1 2 4\n4\n3\n5\n6\n7\n") == "1\n1\n1\n0"
assert run("3 3\n7 7 7\n2\n7\n1\n") == "1\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | `1, 0` | Minimum size case |
| All values equal | `6, 0` | Correct combinatorial counting |
| Distinct powers of two | `1,1,1,0` | Exact OR reconstruction |
| `k = n` | `1,0` | Boundary where only one subsequence exists |

## Edge Cases

Consider:

```
n = 4
k = 2
a = [1,1,1,1]
query = 1
```

The SOS transform gives:

```
g[1] = 4
```

so:

```
F[1] = C(4,2) = 6
```

Möbius inversion leaves `ans[1] = 6`. The algorithm counts position choices rather than distinct values, which is exactly what the problem requires.

Consider:

```
n = 3
k = 2
a = [1,2,2]
query = 7
```

No array value contains bit `4`, so every subsequence OR is contained inside `3`.

The SOS stage computes valid counts only from existing masks. During inversion, mask `7` receives no contribution, leaving:

```
ans[7] = 0
```

which is correct.

Consider:

```
n = 3
k = 3
a = [1,2,4]
query = 7
```

Only one subsequence exists, using all positions.

The algorithm obtains:

```
g[7] = 3
F[7] = C(3,3) = 1
```

and inversion produces:

```
ans[7] = 1
```

while every other mask receives zero. This confirms correct handling of the extreme case `k = n`.
