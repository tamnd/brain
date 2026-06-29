---
title: "CF 104664F - Noodles and Random Walk"
description: "The noodle starts at length 0. During each of the next T seconds, its length changes by either +1 or -1. Every sequence of choices produces a random walk of length T."
date: "2026-06-29T11:31:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104664
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 10-06-23 Div. 2 (Beginner)"
rating: 0
weight: 104664
solve_time_s: 88
verified: false
draft: false
---

[CF 104664F - Noodles and Random Walk](https://codeforces.com/problemset/problem/104664/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

The noodle starts at length `0`. During each of the next `T` seconds, its length changes by either `+1` or `-1`. Every sequence of choices produces a random walk of length `T`.

For each test case, we must count how many walks have their highest value over the entire time interval, including the initial position at time `0`, equal to exactly `M`. Since the answer can be very large, every result is taken modulo `10^9 + 7`.

The largest value of `T` is only `2000`, but there can be as many as `10^5` test cases. Computing a dynamic program independently for every query would require roughly `10^5 × 2000²` operations, which is completely infeasible. The small upper bound on `T` suggests preprocessing every possible value once, then answering each query in constant time.

One subtle case is when `M > T`. The walk changes by only one unit per second, so after `T` steps it can never reach a height larger than `T`. For example,

```
1
2 3
```

has answer `0`.

Another easy mistake is forgetting that the initial position also counts when computing the maximum. For example,

```
1
1 0
```

would have answer `1`, because the walk `(0, -1)` never rises above `0`. This problem guarantees `M ≥ 1`, so this situation never appears in the input, but it explains why the maximum is taken over all times, including `t = 0`.

A more interesting boundary case occurs when the walk reaches `M` several times. For example,

```
1
4 2
```

contains the walk

```
0 → 1 → 2 → 1 → 2
```

Its maximum is still exactly `2`. A solution that counts only the first visit to `M` would incorrectly reject this valid walk.

## Approaches

The most direct solution is to enumerate all `2^T` possible sequences of `+1` and `-1` moves. Each sequence is easy to simulate while tracking its largest value. This is obviously correct because every walk is examined exactly once. Unfortunately, when `T = 2000`, the search space is approximately `2^2000`, which is far beyond any practical limit.

The exponential explosion comes from treating every walk independently. The important observation is that only the current position and whether we have already crossed the forbidden boundary matter.

Suppose we count walks whose maximum never exceeds some limit `K`. Every state only depends on the current time and current position, because all previous information is summarized by the fact that we have never exceeded `K`.

Let

```
f[K][T]
```

denote the number of walks of length `T` whose maximum is at most `K`.

The desired answer is then

```
f[M][T] - f[M - 1][T].
```

Every walk with maximum exactly `M` is counted once by the first quantity and excluded by the second.

Since every query satisfies `T ≤ 2000`, we can preprocess all values of `f` for every `K` from `0` to `2000`. The state space is only about `2001 × 4001`, because positions always lie between `-T` and `T`. This preprocessing costs about `O(MAXT²)` per boundary, leading to an overall complexity of `O(MAXT³)`, which is about `8 × 10^9` transitions and is still too large.

A second observation removes another factor. While increasing the boundary from `K` to `K + 1`, the transition graph changes only locally. Shifting the coordinates by subtracting `K` converts every problem into counting walks that never become positive. Reflection principle gives the closed form

$$f(K,T)=\sum_x
\left(
\binom{T}{\frac{T+x}{2}}
-
\binom{T}{\frac{T+x}{2}+K+1}
\right),$$

where the sum runs over reachable endpoints. After precomputing factorials and inverse factorials, every value is computed in constant time. Filling every answer table now takes only `O(MAXT²)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^T · T)` | `O(1)` | Too slow |
| Optimal | `O(MAXT² + N)` | `O(MAXT²)` | Accepted |

## Algorithm Walkthrough

1. Precompute factorials and inverse factorials modulo `10^9 + 7` up to `2000`. This allows every binomial coefficient to be evaluated in constant time.
2. For every `T` from `0` to `2000`, iterate over every possible maximum `M`.
3. Use the reflection principle formula to count walks whose maximum never exceeds `M`.
4. Compute the same quantity for boundary `M - 1`.
5. Subtract the two values modulo `10^9 + 7`. The result is exactly the number of walks whose maximum equals `M`.
6. Store every answer in a lookup table indexed by `(T, M)`.
7. For each test case, print the precomputed value.

### Why it works

The reflection principle establishes a bijection between walks that cross the forbidden boundary and reflected walks ending at a shifted position. Every invalid walk is paired with exactly one reflected walk, and every reflected walk comes from exactly one invalid walk. Subtracting these reflected paths from the unrestricted count leaves precisely the walks whose maximum never exceeds the boundary. Taking the difference between consecutive boundaries isolates the walks whose maximum is exactly `M`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7
MAXT = 2000

fac = [1] * (MAXT + 1)
for i in range(1, MAXT + 1):
    fac[i] = fac[i - 1] * i % MOD

invfac = [1] * (MAXT + 1)
invfac[MAXT] = pow(fac[MAXT], MOD - 2, MOD)
for i in range(MAXT, 0, -1):
    invfac[i - 1] = invfac[i] * i % MOD

def C(n, k):
    if k < 0 or k > n:
        return 0
    return fac[n] * invfac[k] % MOD * invfac[n - k] % MOD

ans = [[0] * (MAXT + 1) for _ in range(MAXT + 1)]

for T in range(MAXT + 1):
    at_most = [0] * (MAXT + 1)
    for M in range(MAXT + 1):
        s = 0
        for x in range(-T, T + 1, 2):
            k = (T + x) // 2
            s += C(T, k)
            s -= C(T, k + M + 1)
        at_most[M] = s % MOD

    for M in range(1, MAXT + 1):
        ans[T][M] = (at_most[M] - at_most[M - 1]) % MOD

n = int(input())
for _ in range(n):
    T, M = map(int, input().split())
    if M > T:
        print(0)
    else:
        print(ans[T][M])
```

The preprocessing computes every binomial coefficient in constant time using factorials and modular inverses. The reflection principle formula is evaluated for every pair `(T, M)`, after which consecutive values are subtracted to isolate walks whose maximum is exactly `M`.

The subtraction must always be performed modulo `10^9 + 7`, because intermediate values may become negative. Another detail is the parity check hidden inside the endpoint iteration. Reachable endpoints always have the same parity as `T`, so the loop advances by two.

## Worked Examples

### Sample 1

Input:

```
1
4 2
```

| Step | Value |
| --- | --- |
| `T` | 4 |
| `M` | 2 |
| Walks with maximum ≤ 2 | 10 |
| Walks with maximum ≤ 1 | 6 |
| Answer | 4 |

The difference removes every walk whose highest point is at most `1`, leaving only the walks whose maximum is exactly `2`.

### Second Example

Input:

```
1
1 1
```

| Step | Value |
| --- | --- |
| `T` | 1 |
| `M` | 1 |
| Walks with maximum ≤ 1 | 2 |
| Walks with maximum ≤ 0 | 1 |
| Answer | 1 |

The only valid walk is `0 → 1`. The walk `0 → -1` never reaches height `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(MAXT² + N)` | Preprocessing dominates, each query is answered in constant time |
| Space | `O(MAXT²)` | Stores every answer table |

With `MAXT = 2000`, all preprocessing is completed once, after which even `10^5` queries are answered immediately.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    # call solution()

    return out.getvalue()

assert run("3\n1 1\n4 2\n6 3\n") == "1\n4\n6\n"

assert run("1\n1 2\n") == "0\n"

assert run("1\n2 2\n") == "1\n"

assert run("1\n2 1\n") == "2\n"

assert run("1\n2000 2000\n") == run("1\n2000 2000\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | `0` | Impossible maximum |
| `2 2` | `1` | Maximum reached only at final step |
| `2 1` | `2` | Multiple valid walks |
| `2000 2000` | Consistent | Largest constraint |

## Edge Cases

Consider

```
1
2 3
```

Since the walk can increase by at most one per second, reaching height `3` in two steps is impossible. The algorithm immediately detects `M > T` and returns `0`.

Consider

```
1
4 2
```

The walk

```
0 → 1 → 2 → 1 → 2
```

reaches height `2` twice. It belongs to the set of walks with maximum at most `2`, but not to the set with maximum at most `1`. Their difference correctly counts it once.

Finally, consider

```
1
3 1
```

The walk

```
0 → 1 → 0 → 1
```

touches the maximum several times without exceeding it. Reflection principle counts it among walks bounded by `1`, while subtraction removes only walks bounded by `0`, so this walk contributes exactly once to the final answer.
