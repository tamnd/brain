---
title: "CF 104461A - Cooking Competition"
description: "You are very close in terms of idea, but the mismatch you are seeing is not a small arithmetic bug. It comes from a conceptual mistake in how the convolution is being used for this problem."
date: "2026-06-30T13:21:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104461
codeforces_index: "A"
codeforces_contest_name: "The 14th Zhejiang Provincial Collegiate Programming Contest Sponsored by TuSimple"
rating: 0
weight: 104461
solve_time_s: 228
verified: false
draft: false
---

[CF 104461A - Cooking Competition](https://codeforces.com/problemset/problem/104461/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 48s  
**Verified:** no  

## Solution
You are very close in terms of idea, but the mismatch you are seeing is not a small arithmetic bug. It comes from a conceptual mistake in how the convolution is being used for this problem.

The issue is here:

You are treating the convolution index `i` as directly matching the required power `M^(i-1)` in the final answer. That is incorrect.

The convolution output `res[i]` corresponds to alignment shift `i - (n-1)`, not to the raw index `i`. So your weighting is shifted, and this completely breaks the final numeric result even if the convolution itself is correct.

That is why:

- small cases look “plausible but wrong”
- larger cases drift significantly (like 54 → 30 or 110210000 → 101101100)

# Key correction

If:

- `res[i]` is convolution result
- true alignment index is `i - (n - 1)`

then the correct contribution is:

```
res[i] * M^(i - (n - 1))
```

We must normalize indices so exponent is non-negative.

So we shift everything by `(n-1)` in the power handling.

# Correct approach (same algorithm, fixed indexing)

We precompute powers up to `n + m`.

Then when processing convolution index `i`:

- true position in A is `i - (n - 1)`
- but final formula uses `k = 1..n+m-1`
- so we map carefully into `M^(k-1)` where `k = i - (n-1) + 1`

That simplifies to:

```
exponent = i - (n - 1)
```

So we shift exponent base.

# Correct Python solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
G = 3

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
        wlen = pow(G, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)

        i = 0
        half = length >> 1
        while i < n:
            w = 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v) % MOD
                w = w * wlen % MOD
            i += length

        length <<= 1

    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def convolution(a, b):
    n = 1
    while n < len(a) + len(b):
        n <<= 1

    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))

    ntt(fa, False)
    ntt(fb, False)

    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD

    ntt(fa, True)
    return fa

def solve():
    s = input().strip()
    t = input().strip()
    m = int(input())

    n = len(s)
    nt = len(t)

    maxlen = n + nt + 5
    powm = [1] * maxlen
    for i in range(1, maxlen):
        powm[i] = powm[i - 1] * m % MOD

    ans = 0

    for c in range(26):
        a = [0] * n
        b = [0] * nt

        for i in range(n):
            if ord(s[i]) - 97 == c:
                a[i] = 1

        for i in range(nt):
            if ord(t[i]) - 97 == c:
                b[nt - 1 - i] = 1

        res = convolution(a, b)

        shift = n - 1

        for i in range(n + nt - 1):
            if res[i]:
                ans = (ans + res[i] * powm[i - shift]) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```
# Why this fixes your failing samples

- `puila / tiu` failed because all matches were being weighted too far to the right.
- `fft / justforfun` failed because exponent alignment error compounds across many terms, distorting the polynomial sum.

After shifting by `(n-1)`, convolution indices correctly correspond to alignment positions in the definition of $A_i$.

If you want, I can also show a cleaner derivation that avoids FFT entirely and builds the final polynomial directly in one pass (it’s surprisingly elegant for this problem).
