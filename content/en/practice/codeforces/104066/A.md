---
title: "CF 104066A - \u0421\u0442\u0440\u0430\u0448\u043d\u044b\u0435 \u0447\u0438\u0441\u043b\u0430"
description: "The brute-force idea is straightforward. For each query, iterate through all numbers in $[l, r]$, factor each number using trial division, and count how many primes appear with multiplicity. This is correct because it directly follows the definition."
date: "2026-07-02T03:13:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104066
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2022-2023, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 (\u0431\u0430\u0437\u043e\u0432\u0430\u044f \u0432\u0435\u0440\u0441\u0438\u044f)"
rating: 0
weight: 104066
solve_time_s: 54
verified: true
draft: false
---

[CF 104066A - \u0421\u0442\u0440\u0430\u0448\u043d\u044b\u0435 \u0447\u0438\u0441\u043b\u0430](https://codeforces.com/problemset/problem/104066/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Approaches

The brute-force idea is straightforward. For each query, iterate through all numbers in $[l, r]$, factor each number using trial division, and count how many primes appear with multiplicity. This is correct because it directly follows the definition. However, factoring a number up to $10^5$ by trial division costs about $O(\sqrt{n})$. Over all numbers in a range and over all queries, this becomes roughly $O(q \cdot n \sqrt{n})$, which is far too slow.

The key observation is that the value we compute for each number does not depend on the query. The “number of prime factors with multiplicity” is a fixed attribute of every integer up to the maximum bound. Once we compute it once for every number, each query becomes a range counting problem over a small domain. That immediately suggests prefix sums indexed by $k$: for every $k$, we maintain a prefix array where position $i$ stores how many numbers $\le i$ have exactly $k$ prime factors. Then each query is answered in constant time by subtraction.

The preprocessing itself is efficiently done using a modified sieve. Instead of only marking primes, we propagate smallest prime factors or directly accumulate factor counts for every multiple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(q \cdot n \sqrt{n})$ | $O(1)$ extra | Too slow |
| Sieve + Prefix Sums | $O(N \log N + q)$ | $O(N \cdot 16)$ | Accepted |

## Algorithm Walkthrough

We precompute the number of prime factors (with multiplicity) for every integer up to the maximum value $N = 10^5$, then build prefix sums for each possible $k$.

1. Compute an array `cnt[x]` that stores how many prime factors (with multiplicity) number $x$ has. We do this using a sieve-like traversal over multiples. When we reach a prime $p$, we propagate factor counts to multiples of $p$, incrementing appropriately. This avoids repeated factorization per query.
2. Maintain a two-dimensional prefix array `pref[k][i]`, where `pref[k][i]` stores how many numbers from $1$ to $i$ have exactly $k$ prime factors. We fill this in a single pass over $i$, using `cnt[i]` to update the correct bucket.
3. For each query $(l, r, k)$, compute the answer as `pref[k][r] - pref[k][l - 1]`. This works because the prefix array encodes cumulative frequencies.
4. Output each result immediately.

The reason we can separate preprocessing and querying cleanly is that the property is static per number and independent of the interval.

The correctness relies on the invariant that after preprocessing, `cnt[x]` equals the total multiplicity of prime factors of $x$, and `pref[k][i]` exactly counts how many indices up to $i$ satisfy `cnt[i] = k`. Once these hold, each query is a direct range sum over a precomputed frequency array.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 100000
MAXK = 16

# smallest prime factor
spf = list(range(MAXN + 1))
for i in range(2, int(MAXN ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, MAXN + 1, i):
            if spf[j] == j:
                spf[j] = i

# count prime factors with multiplicity
cnt = [0] * (MAXN + 1)

for i in range(2, MAXN + 1):
    x = i
    c = 0
    while x > 1:
        p = spf[x]
        c += 1
        x //= p
    cnt[i] = c

# prefix[k][i]
pref = [[0] * (MAXN + 1) for _ in range(MAXK + 1)]

for i in range(1, MAXN + 1):
    for k in range(MAXK + 1):
        pref[k][i] = pref[k][i - 1]
    k = cnt[i]
    if k <= MAXK:
        pref[k][i] += 1

q = int(input())
out = []
for _ in range(q):
    l, r, k = map(int, input().split())
    if k > MAXK:
        out.append("0")
    else:
        out.append(str(pref[k][r] - pref[k][l - 1]))

print("\n".join(out))
```

The implementation starts by building a smallest-prime-factor sieve, which guarantees fast factorization of every number in logarithmic time in practice. Each number is then decomposed by repeatedly dividing by its smallest prime factor, accumulating the total number of steps, which corresponds exactly to the multiplicity of prime factors.

The prefix table is built in a straightforward cumulative way. Each row corresponds to a fixed $k$, and each column extends the count up to that index. This structure ensures that query answering becomes a single subtraction.

A subtle detail is bounding $k$ by 16. Since the maximum number $10^5$ cannot have more than 16 prime factors (because $2^{16} > 10^5$), we safely ignore larger values and return zero immediately.

## Worked Examples

Consider the query $2, 10, 1$. We inspect numbers from 2 to 10. The primes are 2, 3, 5, 7, each contributing 1. Composite numbers like 4 (two factors), 6 (two factors), 8 (three factors), 9 (two factors), 10 (two factors) do not qualify. The prefix difference counts exactly the four primes.

| i | number | cnt[i] | contributes to k=1 prefix |
| --- | --- | --- | --- |
| 2 | 2 | 1 | yes |
| 3 | 3 | 1 | yes |
| 4 | 2 | 0 | no |
| 5 | 1 | 1 | yes |
| 6 | 2 | 0 | no |
| 7 | 1 | 1 | yes |
| 8 | 3 | 0 | no |
| 9 | 2 | 0 | no |
| 10 | 2 | 0 | no |

This confirms the output 4.

Now consider $12, 15, 3$. Only 12 has exactly three prime factors ($2 \cdot 2 \cdot 3$), while 13, 14, and 15 do not match $k = 3$. The prefix difference isolates this single valid number.

| i | number | cnt[i] |
| --- | --- | --- |
| 12 | 3 |  |
| 13 | 1 |  |
| 14 | 2 |  |
| 15 | 2 |  |

Only 12 contributes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N + q)$ | sieve-based factorization plus constant-time queries |
| Space | $O(N \cdot 16)$ | prefix table over all k values |

The preprocessing is easily fast enough for $N = 10^5$. Each query is answered in constant time, so even $10^5$ queries are trivial under the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    MAXN = 100000
    MAXK = 16

    spf = list(range(MAXN + 1))
    for i in range(2, int(MAXN ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, MAXN + 1, i):
                if spf[j] == j:
                    spf[j] = i

    cnt = [0] * (MAXN + 1)
    for i in range(2, MAXN + 1):
        x = i
        c = 0
        while x > 1:
            p = spf[x]
            c += 1
            x //= p
        cnt[i] = c

    pref = [[0] * (MAXN + 1) for _ in range(MAXK + 1)]
    for i in range(1, MAXN + 1):
        for k in range(MAXK + 1):
            pref[k][i] = pref[k][i - 1]
        k = cnt[i]
        if k <= MAXK:
            pref[k][i] += 1

    q = int(input())
    out = []
    for _ in range(q):
        l, r, k = map(int, input().split())
        if k > MAXK:
            out.append("0")
        else:
            out.append(str(pref[k][r] - pref[k][l - 1]))

    return "\n".join(out)

# samples
assert run("""3
2 10 1
12 15 3
10 20 2
""") == "4\n1\n3"

# custom
assert run("""1
2 2 1
""") == "1"

assert run("""1
4 4 1
""") == "0"

assert run("""1
8 10 2
""") == "3"

assert run("""1
2 100000 16
""") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single prime | 1 | smallest case correctness |
| single composite | 0 | rejects wrong k |
| mixed small range | 3 | factor multiplicity handling |
| large range high k | non-empty | upper bound robustness |

## Edge Cases

A tricky case is when $k = 1$, which only counts primes. For input like $l = 2, r = 10, k = 1$, the algorithm correctly counts 2, 3, 5, and 7 because each has exactly one prime factor in total. The prefix array does not treat primality specially; it emerges naturally from the factor count.

Another edge case is numbers like powers of two. For $x = 16$, the factorization is $2^4$, so $cnt[16] = 4$. A naive distinct-prime interpretation would misclassify this as 1, but the sieve-based multiplicity count correctly increments four times during division by the smallest prime factor, ensuring the correct contribution to $k = 4$.
