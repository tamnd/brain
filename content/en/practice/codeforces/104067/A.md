---
title: "CF 104067A - \u0421\u0442\u0440\u0430\u0448\u043d\u044b\u0435 \u0447\u0438\u0441\u043b\u0430"
description: "We are given multiple independent queries over a small integer range. Each query provides an interval $[l, r]$ and a number $k$. For every integer $x$, we factorize it into primes and count how many prime factors appear in that factorization, counting multiplicity."
date: "2026-07-02T03:09:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104067
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2022-2023, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 (\u043f\u0440\u043e\u0434\u0432\u0438\u043d\u0443\u0442\u0430\u044f \u0432\u0435\u0440\u0441\u0438\u044f)"
rating: 0
weight: 104067
solve_time_s: 63
verified: true
draft: false
---

[CF 104067A - \u0421\u0442\u0440\u0430\u0448\u043d\u044b\u0435 \u0447\u0438\u0441\u043b\u0430](https://codeforces.com/problemset/problem/104067/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple independent queries over a small integer range. Each query provides an interval $[l, r]$ and a number $k$. For every integer $x$, we factorize it into primes and count how many prime factors appear in that factorization, counting multiplicity. So $12 = 2^2 \cdot 3$ contributes $3$ factors, while $18 = 2 \cdot 3^2$ also contributes $3$.

A number is called $k$-“scary” if this count of prime factors is exactly $k$. For each query, we must count how many integers in the given segment have exactly $k$ prime factors.

The input constraints already shape the solution strongly. The values of $l$ and $r$ are at most $10^5$, so the universe of numbers is small enough that we can preprocess properties for every integer once. However, the number of queries is large, up to $10^5$, so recomputing factorization per query would be too slow. A naive approach that factorizes every number in every query leads to roughly $10^5 \times 10^5$ operations, which is far beyond acceptable limits.

The parameter $k$ is also small, bounded by 16, which hints that the distribution of prime factor counts is shallow and can be precomputed efficiently.

A subtle edge case comes from small numbers like 1. The number 1 has zero prime factors. If a query asks for $k = 0$, it should be counted, but many naive implementations ignore 1 entirely because it has no prime decomposition. Another issue is counting multiplicity correctly. For example, 8 should contribute 3, not 1, because $8 = 2^3$. A mistake here leads to systematic undercounting.

## Approaches

A brute-force solution directly processes each query by factoring every number in $[l, r]$ using trial division. This is conceptually straightforward: for each number, repeatedly divide by primes and count factors. It is correct, but its cost is driven by repeated factorization. Even with a sieve, doing this $10^5$ times over ranges of size $10^5$ results in about $10^{10}$ operations in the worst case, which cannot pass.

The key observation is that all numbers are within a fixed small bound, so their prime factor counts can be precomputed once. Instead of recomputing factorization per query, we compute a function $f[x]$ equal to the number of prime factors of $x$. Once this array is known, each query becomes a range counting problem over a static array.

Range counting over many queries is efficiently handled using prefix sums. For every possible value of $k$, we build a prefix array $pref[k][x]$ that stores how many numbers up to $x$ have exactly $k$ prime factors. Each query then reduces to a constant-time subtraction.

This transforms the problem from repeated number theory computations into a preprocessing step plus fast lookups.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(q \cdot (r-l+1)\sqrt{n})$ | $O(1)$ | Too slow |
| Optimal (sieve + prefix sums) | $O(N \log \log N + q)$ | $O(NK)$ | Accepted |

## Algorithm Walkthrough

We preprocess all numbers up to $N = 10^5$.

1. Build an array `spf` or directly compute smallest primes using a sieve-like method, so that each number can be factorized quickly. This avoids recomputing divisibility checks from scratch for every number.
2. For each integer $x$ from 2 to $N$, compute its total number of prime factors with multiplicity. We repeatedly divide $x$ by its smallest prime factor and accumulate the count. This produces a value `cnt[x]`.
3. Since $k$ is at most 16, we build prefix sums for each possible $k$. We maintain `pref[k][i]`, which stores how many numbers in $[1, i]$ have exactly $k$ prime factors. We fill it incrementally by propagating previous values and adding 1 when `cnt[i] == k`.
4. For each query $(l, r, k)$, we answer in constant time using:

$$pref[k][r] - pref[k][l-1]$$
5. Output the result for each query.

The main implementation concern is keeping factorization linear or near-linear. Using smallest prime factor preprocessing ensures that each number is decomposed in logarithmic time in practice.

### Why it works

The correctness relies on two invariants. First, `cnt[x]` is exactly the total number of prime factors of $x$, because each step of division removes exactly one prime factor and all factors are accounted for through repeated division by smallest primes. Second, the prefix array maintains a cumulative count of occurrences of each $k$-class. Since each integer contributes independently to exactly one $k$, prefix differences precisely isolate counts over any segment without overlap or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

N = 100000

spf = list(range(N + 1))

for i in range(2, int(N ** 0.5) + 1):
    if spf[i] == i:
        for j in range(i * i, N + 1, i):
            if spf[j] == j:
                spf[j] = i

cnt = [0] * (N + 1)

for i in range(2, N + 1):
    x = i
    c = 0
    while x > 1:
        p = spf[x]
        while x % p == 0:
            x //= p
            c += 1
    cnt[i] = c

MAXK = 16
pref = [[0] * (N + 1) for _ in range(MAXK + 1)]

for i in range(1, N + 1):
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

The solution first builds smallest prime factors so that factorization becomes deterministic and fast. Each number is then reduced to its prime components, accumulating multiplicities correctly rather than just distinct primes. The prefix table is built in a way that each row corresponds to a fixed $k$, so queries never require scanning ranges.

A common implementation pitfall is forgetting that 1 contributes 0 factors. Here it is naturally handled since `cnt[1]` remains zero and is included in the prefix for $k = 0$.

Another subtle issue is updating prefix arrays efficiently. Recomputing full counts for every $k$ independently per index would be too slow; instead, we copy previous prefix values and update only the relevant $k$ bucket per index.

## Worked Examples

Consider a small segment where we can see factor counts clearly.

### Example 1

Input:

```
l = 2, r = 10, k = 2
```

We compute prime factor counts:

| x | factorization | cnt[x] |
| --- | --- | --- |
| 2 | 2 | 1 |
| 3 | 3 | 1 |
| 4 | 2^2 | 2 |
| 5 | 5 | 1 |
| 6 | 2·3 | 2 |
| 7 | 7 | 1 |
| 8 | 2^3 | 3 |
| 9 | 3^2 | 2 |
| 10 | 2·5 | 2 |

Counting those with $k = 2$ gives 4 numbers: 4, 6, 9, 10.

This matches what the prefix difference would return: `pref[2][10] - pref[2][1]`.

### Example 2

Input:

```
l = 12, r = 15, k = 3
```

| x | factorization | cnt[x] |
| --- | --- | --- |
| 12 | 2^2·3 | 3 |
| 13 | 13 | 1 |
| 14 | 2·7 | 2 |
| 15 | 3·5 | 2 |

Only 12 satisfies $k = 3$, so the answer is 1.

This demonstrates how multiplicity matters, since 12 accumulates three factors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log \log N + q)$ | sieve-like preprocessing plus constant-time queries |
| Space | $O(NK)$ | prefix table for each $k \le 16$ |

The preprocessing is linearithmic in a small bound $10^5$, and each query is answered in constant time, which fits comfortably within limits even for $10^5$ queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isclose

    N = 100000
    spf = list(range(N + 1))
    for i in range(2, int(N ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, N + 1, i):
                if spf[j] == j:
                    spf[j] = i

    cnt = [0] * (N + 1)
    for i in range(2, N + 1):
        x = i
        c = 0
        while x > 1:
            p = spf[x]
            while x % p == 0:
                x //= p
                c += 1
        cnt[i] = c

    MAXK = 16
    pref = [[0] * (N + 1) for _ in range(MAXK + 1)]

    for i in range(1, N + 1):
        for k in range(MAXK + 1):
            pref[k][i] = pref[k][i - 1]
        k = cnt[i]
        if k <= MAXK:
            pref[k][i] += 1

    q = int(_sys.stdin.readline())
    out = []
    for _ in range(q):
        l, r, k = map(int, _sys.stdin.readline().split())
        if k > MAXK:
            out.append("0")
        else:
            out.append(str(pref[k][r] - pref[k][l - 1]))
    return "\n".join(out)

# sample-style sanity checks
assert run("1\n2 10 2\n") == "4"
assert run("1\n12 15 3\n") == "1"
assert run("1\n1 1 0\n") == "1"
assert run("1\n1 10 10\n") == "0"
assert run("3\n2 10 1\n12 15 3\n10 20 2\n") == "4\n1\n3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1 1 0\n` | `1` | handling of number 1 as zero prime factors |
| `1\n1 10 10\n` | `0` | k larger than possible factor counts |
| `3 queries sample` | `4\n1\n3` | correctness across multiple queries |

## Edge Cases

For the value 1, the algorithm assigns `cnt[1] = 0` implicitly through initialization. When a query asks for $k = 0$, the prefix array correctly includes 1, since it contributes exactly once to the zero-class bucket.

For large $k$ values such as 15 or 16, many numbers in the range do not reach that factor count. The prefix table still handles them safely because those buckets remain zero throughout preprocessing, so subtraction yields zero without special-case logic.

Queries with $l = 1$ rely on accessing `pref[k][0]`. The prefix arrays are initialized with zero at index 0, so the subtraction `pref[k][r] - pref[k][0]` correctly returns the full range count without underflow or indexing errors.
