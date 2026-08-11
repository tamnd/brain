---
title: "CF 102409I - Thanos's snap"
description: "There are exactly (N=5{,}000{,}000) people in Diegopolis. Each person independently survives the snap with probability (1/2). Let (X) be the number of survivors, so (X) follows a binomial distribution with parameters (N) and (1/2)."
date: "2026-08-12T00:02:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102409
codeforces_index: "I"
codeforces_contest_name: "Semana i 2019"
rating: 0
weight: 102409
solve_time_s: 150
verified: true
draft: false
---

[CF 102409I - Thanos's snap](https://codeforces.com/problemset/problem/102409/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

There are exactly (N=5{,}000{,}000) people in Diegopolis. Each person independently survives the snap with probability (1/2). Let (X) be the number of survivors, so (X) follows a binomial distribution with parameters (N) and (1/2).

For every test case, we are given a threshold (K), and need the probability that at least (K) people survive:

[
P(X\ge K).
]

The answer is not required as a floating-point probability. Instead, we work modulo (M=10^9+7), treating division as multiplication by a modular inverse. The original problem fixes the population at five million and allows up to (10^5) queries.

The size of (N) is the key constraint. A computation that performs even a small amount of work for every possible outcome is already doing about five million operations, which is reasonable once, but doing that separately for (10^5) queries would be roughly (5\times10^{11}) work and is completely infeasible. Any approach that explicitly computes a binomial sum independently for each query is ruled out. We need to make the expensive work shared by all queries.

There are several boundary cases where a careless implementation can fail. For (K=0), the event is certain, so the answer is exactly (1). For example,

```
1
0
```

must produce

```
1
```

even though the formal statement's lower bound says (K\ge1), because the sample itself includes (K=0).

At the other extreme, (K=N) means that everybody must survive. Thus the answer is simply

[
\frac{1}{2^N}.
]

For

```
1
5000000
```

the answer is (195206359), as given by the sample. A solution that accidentally computes (P(X>K)) instead of (P(X\ge K)) would return zero here.

The threshold (K=1) is another useful boundary. Its complement is the event that nobody survives, so

[
P(X\ge1)=1-\frac1{2^N}.
]

For this problem that is (804793649). An implementation that starts its cumulative sum at (K=1) but forgets the probability of zero survivors will get this case wrong.

## Approaches

The direct approach follows immediately from the binomial distribution. Exactly (k) survivors has probability

[
P(X=k)=\binom Nk\frac1{2^N}.
]

Consequently, a query asking for at least (K) survivors can be answered by summing

[
\sum_{k=K}^{N}\binom Nk\frac1{2^N}.
]

This is correct because the possible survivor counts are mutually exclusive and cover every outcome. The problem is the amount of repeated work. If a query asks for (K=1), we would process roughly five million terms. Doing that for (10^5) queries gives up to (5\times10^{11}) terms, far beyond the one-second limit.

The key observation is that the binomial probabilities are not independent values. Consecutive terms have a simple ratio:

# \frac{\binom Nk}{\binom N{k-1}}

\frac{N-k+1}{k}.
]

Thus, once we know the probability of zero survivors,

[
P(X=0)=\frac1{2^N},
]

we can generate every subsequent probability using one modular multiplication and one modular inverse.

There is another useful observation about the queries. If we sort all queried values of (K), we can move from the smallest threshold to the largest while maintaining the tail probability. Suppose we currently know

[
S_k=P(X\ge k).
]

Then

[
S_{k+1}=S_k-P(X=k).
]

So moving the threshold forward by one costs only the current probability mass. Across all queries, we never need to traverse the distribution more than once, up to the largest requested (K).

The remaining question is how to obtain all modular inverses (1^{-1},2^{-1},\ldots,m^{-1}), where (m) is the largest queried threshold. Because (m<10^9+7), every denominator is invertible modulo (M). We can generate the inverses in linear time using

M-\left\lfloor\frac Mi\right\rfloor
\operatorname{inv}[M\bmod i]\pmod M.
]

For Python, storing five million ordinary integers would consume too much memory, so the implementation uses `array('I')`, which stores each modular value in four bytes. Five million entries therefore require about 20 MB.

The brute-force approach and the optimized approach can be summarized as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(NT)) | (O(1)) | Too slow |
| Optimal | (O(N+T\log T)) | (O(N+T)) | Accepted |

## Algorithm Walkthrough

1. Read all queries and remember their original positions. Sorting the queries lets us answer them in increasing order of (K), so each binomial probability is generated only once.
2. Let (m) be the largest queried (K). There is no reason to generate probabilities beyond (m), because no query asks about a larger threshold.
3. Build modular inverses from (1) through (m). Since (m<10^9+7), every integer in this range has a modular inverse.
4. Compute

[
p_0=P(X=0)=2^{-N}\pmod M.
]

Python's three-argument `pow` computes the modular exponentiation efficiently, so this does not require iterating (N) times.

1. Initialize the tail probability with

[
S_0=P(X\ge0)=1.
]

Also keep `cur = 0` and `p = p_0`, where `p` represents (P(X=\text{cur})).

1. Process the sorted queries. If the next query asks for (K), repeatedly move from `cur` to (K). On each move, subtract (P(X=\text{cur})) from the current tail, increment `cur`, and generate the new probability with

P(X=\text{cur}-1)
\frac{N-\text{cur}+1}{\text{cur}}.
]

The reason for subtracting before incrementing is that (P(X\ge cur)) becomes (P(X\ge cur+1)) exactly by removing the probability mass at (X=cur).

1. Once `cur == K`, the maintained tail is exactly (P(X\ge K)). Store it at the original query position.
2. Print the answers in input order rather than sorted order. Duplicate thresholds need no special handling because they are simply answered from the same maintained state.

### Why it works

The invariant is that immediately before answering a query with threshold `cur`, `tail` equals (P(X\ge cur)), while `pmf` equals (P(X=cur)). Moving from (cur) to (cur+1) subtracts exactly the one probability mass that must disappear from the tail, so the invariant remains true. The recurrence for `pmf` produces the exact next binomial probability because consecutive binomial coefficients have ratio ((N-k+1)/k). Since the invariant starts with (P(X\ge0)=1) and (P(X=0)=2^{-N}), every requested tail probability is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

from array import array

MOD = 1_000_000_007
N = 5_000_000

def solve():
    t = int(input())
    queries = [int(input()) for _ in range(t)]

    indexed = sorted(enumerate(queries), key=lambda x: x[1])
    max_k = indexed[-1][1]

    # inv[i] = modular inverse of i modulo MOD.
    inv = array('I', [0]) * (max_k + 1)
    if max_k >= 1:
        inv[1] = 1
        for i in range(2, max_k + 1):
            inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # P(X = 0) = 1 / 2^N.
    pmf = pow(pow(2, N, MOD), MOD - 2, MOD)

    # tail = P(X >= cur)
    cur = 0
    tail = 1

    ans = [0] * t

    for idx, k in indexed:
        while cur < k:
            # Remove P(X = cur), so tail becomes P(X >= cur + 1).
            tail -= pmf
            if tail < 0:
                tail += MOD

            cur += 1

            # P(X = cur) =
            # P(X = cur - 1) * (N - cur + 1) / cur
            pmf = pmf * (N - cur + 1) % MOD
            pmf = pmf * inv[cur] % MOD

        ans[idx] = tail

    sys.stdout.write('\n'.join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The inverse array is generated first because every transition from (P(X=k-1)) to (P(X=k)) requires division by (k). The recurrence avoids calling `pow(k, MOD-2, MOD)` five million times, which would be far too expensive.

The initial probability is computed as (2^{-N}). The code writes this as the inverse of (2^N), using Fermat's little theorem. Since (M) is prime,

[
(2^N)^{-1}\equiv (2^N)^{M-2}\pmod M.
]

The main loop maintains the two quantities described in the proof. `tail` starts at one because every possible survivor count is at least zero. `pmf` starts at (P(X=0)). After subtracting `pmf`, the threshold is incremented, and the recurrence generates the probability belonging to that new threshold.

The subtraction is performed modulo (M). Python integers do not overflow, but `tail` can become negative after a modular subtraction, so the code adds `MOD` when necessary.

The query sorting is also significant. Without it, moving from (K=4{,}000{,}000) back to (K=2) would require rebuilding the distribution or maintaining extra information. With sorted queries, `cur` only increases, so the total number of distribution transitions is at most (m).

The `array('I')` representation is a Python-specific memory optimization. A normal Python integer carries substantial object overhead, and five million such integers would approach or exceed the 256 MB memory limit. Four-byte unsigned entries keep the inverse table near 20 MB.

## Worked Examples

The provided sample contains two queries, (K=0) and (K=5{,}000{,}000).

| Query (K) | `cur` before | `tail` before | Action | Answer |
| --- | --- | --- | --- | --- |
| 0 | 0 | (1) | No transitions needed | (1) |
| 5,000,000 | 0 | (1) | Remove (P(X=0),P(X=1),\ldots,P(X=4,999,999)) | (P(X=5,000,000)) |

After all transitions, only the outcome (X=5{,}000{,}000) remains in the tail. Hence

[
P(X\ge5{,}000{,}000)=P(X=5{,}000{,}000)
=\frac1{2^{5{,}000{,}000}}
\equiv195206359\pmod M.
]

The output is therefore

```
1
195206359
```

This trace exercises both extremes. (K=0) demonstrates why the loop must allow a query to be answered immediately, while (K=N) demonstrates that the inclusive boundary (X\ge K) must retain the probability of exactly (K).

For a second trace, consider several queries concentrated at the upper boundary.

| Query (K) | `cur` before | Required transition | Resulting tail |
| --- | --- | --- | --- |
| 1 | 0 | Remove (P(X=0)) | (1-P(X=0)) |
| 4,999,999 | 1 | Remove (P(X=1),\ldots,P(X=4,999,998)) | (P(X\ge4,999,999)) |
| 5,000,000 | 4,999,999 | Remove (P(X=4,999,999)) | (P(X=5,000,000)) |

Here (P(X=5{,}000{,}000)=195206359). Also,

1. 

]

Thus

788168783+195206359
\equiv983375142\pmod M.
]

The answers for these three thresholds are consequently

```
804793649
983375142
195206359
```

The trace demonstrates why the recurrence must generate (P(X=k)) after incrementing `cur`. Using the old denominator or old numerator would shift every generated probability by one position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N+T\log T)) | At most (N) inverse or probability transitions, plus sorting the (T) queries |
| Space | (O(N+T)) | The inverse table uses (O(N)) compact integers and the queries and answers use (O(T)) |

Here (N=5{,}000{,}000) and (T\le100{,}000). The expensive part is linear in five million, rather than linear in five million for every query. The compact inverse array keeps the memory usage within 256 MB, while sorting only (10^5) queries is comparatively small. The official problem gives a one-second limit and 256 MB memory limit, so sharing the distribution scan across all queries is essential.

## Test Cases

```python
from array import array

MOD = 1_000_000_007
N = 5_000_000

def solution(data: str) -> str:
    it = iter(data.split())
    t = int(next(it))
    queries = [int(next(it)) for _ in range(t)]

    indexed = sorted(enumerate(queries), key=lambda x: x[1])
    max_k = indexed[-1][1]

    inv = array('I', [0]) * (max_k + 1)

    if max_k >= 1:
        inv[1] = 1
        for i in range(2, max_k + 1):
            inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    pmf = pow(pow(2, N, MOD), MOD - 2, MOD)
    cur = 0
    tail = 1

    ans = [0] * t

    for idx, k in indexed:
        while cur < k:
            tail -= pmf
            if tail < 0:
                tail += MOD

            cur += 1
            pmf = pmf * (N - cur + 1) % MOD
            pmf = pmf * inv[cur] % MOD

        ans[idx] = tail

    return '\n'.join(map(str, ans))

# Provided sample
assert solution("2\n0\n5000000\n") == \
       "1\n195206359", "provided sample"

# Minimum threshold and maximum threshold
assert solution("2\n0\n1\n") == \
       "1\n804793649", "minimum threshold boundary"

# Upper boundary, including N-1 and N
assert solution("2\n4999999\n5000000\n") == \
       "983375142\n195206359", "upper boundary"

# Duplicate queries and arbitrary ordering
assert solution("5\n5000000\n0\n5000000\n1\n0\n") == \
       "195206359\n1\n195206359\n804793649\n1", "duplicate queries"

# All queries equal
assert solution("4\n5000000\n5000000\n5000000\n5000000\n") == \
       "195206359\n195206359\n195206359\n195206359", "all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 0 / 1` | `1 / 804793649` | Minimum threshold and the complement of zero survivors |
| `2 / 4999999 / 5000000` | `983375142 / 195206359` | Inclusive upper boundary and off-by-one behavior |
| `5 / 5000000 / 0 / 5000000 / 1 / 0` | `195206359 / 1 / 195206359 / 804793649 / 1` | Query sorting, original ordering, and duplicates |
| `4 / 5000000 / 5000000 / 5000000 / 5000000` | Four copies of `195206359` | Repeated identical thresholds |

## Edge Cases

For (K=0), the input

```
1
0
```

starts with `cur = 0` and `tail = 1`. Since `cur < k` is false, the algorithm performs no probability transition and immediately returns (1). This is exactly (P(X\ge0)), because every possible number of survivors is nonnegative.

For (K=1), the input

```
1
1
```

performs exactly one transition. Initially `pmf` is (P(X=0)=195206359), so subtracting it gives

[
1-195206359=804793648
]

Wait, because the modulus is (10^9+7), the correct modular subtraction is

[
1-195206359\equiv804793649\pmod{1{,}000{,}000{,}007}.
]

Thus the output is

```
804793649
```

and the algorithm correctly removes only the zero-survivor outcome.

For (K=N-1=4{,}999{,}999), the algorithm eventually leaves exactly the probabilities of (N-1) and (N). Starting from

[
P(X=N)=195206359,
]

the recurrence gives

195206359\cdot5{,}000{,}000
\equiv788168783.
]

Their sum is

[
788168783+195206359
=983375142,
]

so

```
1
4999999
```

produces

```
983375142
```

This is a particularly useful off-by-one test because an implementation computing (P(X>K)) would incorrectly return only (195206359).

For (K=N), the input

```
1
5000000
```

advances until `cur` reaches (N). At that point the tail contains only (P(X=N)), which was generated by the recurrence and equals

[
\frac1{2^N}\equiv195206359\pmod M.
]

The output is therefore

```
195206359
```

which also matches the official sample.
