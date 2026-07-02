---
title: "CF 103666B - \u0422\u0440\u043e\u0439\u043d\u043e\u0439 \u0424\u0438\u0431\u043e\u043d\u0430\u0447\u0447\u0438"
description: "We are given a Fibonacci-like sequence where the first two terms are fixed as $F1 = 1$ and $F2 = 2$, and every later term is the sum of the previous two. This produces a deterministic infinite sequence of integers."
date: "2026-07-02T21:06:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103666
codeforces_index: "B"
codeforces_contest_name: "\u0422\u0443\u0440\u043d\u0438\u0440 \u0410\u0440\u0445\u0438\u043c\u0435\u0434\u0430 2016"
rating: 0
weight: 103666
solve_time_s: 51
verified: true
draft: false
---

[CF 103666B - \u0422\u0440\u043e\u0439\u043d\u043e\u0439 \u0424\u0438\u0431\u043e\u043d\u0430\u0447\u0447\u0438](https://codeforces.com/problemset/problem/103666/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a Fibonacci-like sequence where the first two terms are fixed as $F_1 = 1$ and $F_2 = 2$, and every later term is the sum of the previous two. This produces a deterministic infinite sequence of integers. The task is not to compute large values directly, but to focus on a segment of this sequence indexed from $L$ to $R$, and count how many of those indexed Fibonacci numbers are divisible by 3.

The input gives two integers $L$ and $R$, describing a contiguous block of indices in the Fibonacci sequence. The output is a single integer representing how many Fibonacci numbers in that index range have remainder zero when divided by 3.

The constraints allow $L, R \le 10^5$, which immediately suggests that any solution that recomputes Fibonacci values naively up to each query endpoint is already fine in terms of raw iteration count, since generating $10^5$ Fibonacci numbers is trivial. However, the real issue is not computing Fibonacci numbers themselves, but efficiently checking divisibility and recognizing structure in that property.

A subtle pitfall appears when trying to compute large Fibonacci values directly. Even though $n \le 10^5$, Fibonacci numbers grow exponentially and exceed standard integer ranges very quickly. A naive implementation using big integers is still possible in Python, but unnecessary. More importantly, recomputing full values is wasted effort because we only care about divisibility by 3, which depends only on the sequence modulo 3.

No tricky edge cases arise from input formatting or ranges, but there is a conceptual one: if someone computes Fibonacci values directly and then checks divisibility, they may assume Python handles it safely. It does, but it hides the fact that the structure of the problem allows a constant-time per index solution after preprocessing.

## Approaches

A direct approach is to generate Fibonacci numbers one by one from $F_1$ up to $F_R$, check each value, and count how many in the range $[L, R]$ are divisible by 3. This is correct because it follows the definition directly. The cost is linear in $R$, with each step performing an addition and a modulo check. In Python this is still feasible for $10^5$ terms, but it is doing unnecessary work.

The key observation is that we never need the full Fibonacci values. We only need them modulo 3. Once we reduce the recurrence modulo 3, we get a small state machine: each term depends only on the previous two residues modulo 3. Since each residue is in $\{0,1,2\}$, the entire process must eventually repeat. In fact, this sequence has a very short periodic structure, so the divisibility pattern by 3 becomes periodic in the index.

Once we know this pattern, the problem reduces to counting how many indices in $[L, R]$ fall into positions where the Fibonacci residue is zero. This can be answered either by precomputing the first period and using arithmetic counting, or by building a prefix sum over the periodic pattern up to $10^5$.

A simpler and equally safe approach is to precompute the residue sequence up to $R$, build a prefix sum of positions where $F_i \bmod 3 = 0$, and answer the query in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Fibonacci + check | $O(R)$ | $O(1)$ | Accepted |
| Modulo + prefix sum | $O(R)$ preprocessing, $O(1)$ query | $O(R)$ | Accepted |

## Algorithm Walkthrough

We construct the Fibonacci sequence only modulo 3, since divisibility depends solely on the remainder.

1. Compute an array `f[i]` storing $F_i \bmod 3$ for all $i \le R$. Each value is computed using the recurrence $f[i] = (f[i-1] + f[i-2]) \bmod 3$. This keeps numbers small and avoids overflow entirely.
2. Build a prefix sum array `pref[i]` where `pref[i]` counts how many indices $1 \le j \le i$ satisfy $f[j] = 0$. This converts the problem into range counting, which is why prefix sums are useful here.
3. Answer the query $[L, R]$ by computing `pref[R] - pref[L-1]`. This works because prefix sums encode cumulative frequency, so subtraction isolates exactly the range we care about.

Why it works: the Fibonacci recurrence modulo 3 defines a deterministic sequence of residues, so every index has a fixed value in advance. The prefix array stores an exact count of positions satisfying the divisibility condition up to any index. Since the sequence is fully precomputed without approximation, subtracting prefix values exactly isolates the number of valid elements in any interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

L = int(input().strip())
R = int(input().strip())

n = R

f = [0] * (n + 1)
pref = [0] * (n + 1)

if n >= 1:
    f[1] = 1 % 3
    pref[1] = 1 if f[1] == 0 else 0

if n >= 2:
    f[2] = 2 % 3
    pref[2] = pref[1] + (1 if f[2] == 0 else 0)

for i in range(3, n + 1):
    f[i] = (f[i - 1] + f[i - 2]) % 3
    pref[i] = pref[i - 1] + (1 if f[i] == 0 else 0)

ans = pref[R] - (pref[L - 1] if L > 1 else 0)
print(ans)
```

The implementation directly mirrors the recurrence, but reduces every Fibonacci value modulo 3 immediately, preventing unnecessary growth. The prefix array is updated in the same loop to avoid a second pass.

A subtle detail is the handling of $L = 1$, since `pref[0]` does not exist in the array. This is handled explicitly by treating it as zero.

## Worked Examples

Consider the example where $L = 3$ and $R = 7$.

We compute the sequence:

| i | F_i | F_i mod 3 | prefix count |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 0 |
| 2 | 2 | 2 | 0 |
| 3 | 3 | 0 | 1 |
| 4 | 5 | 2 | 1 |
| 5 | 8 | 2 | 1 |
| 6 | 13 | 1 | 1 |
| 7 | 21 | 0 | 2 |

Query result is $pref[7] - pref[2] = 2 - 0 = 2$.

This trace shows that once residues are tracked, the problem reduces to simple counting.

Now consider $L = 1, R = 5$:

| i | F_i mod 3 | prefix |
| --- | --- | --- |
| 1 | 1 | 0 |
| 2 | 2 | 0 |
| 3 | 0 | 1 |
| 4 | 2 | 1 |
| 5 | 2 | 1 |

Answer is $pref[5] - pref[0] = 1$, confirming that only one Fibonacci number in this range is divisible by 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(R)$ | Each Fibonacci residue and prefix value is computed once |
| Space | $O(R)$ | Arrays store values up to index $R$ |

The constraint $R \le 10^5$ makes this solution comfortably fast, since both memory and time usage are linear and small in absolute terms.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    return __import__('builtins').print.__self__  # placeholder to avoid execution issues

# Since full harness is not executable here, illustrative asserts:

# provided sample
# assert run("3\n7\n") == "2"

# edge: smallest range
# assert run("1\n1\n") == "0"

# edge: first divisible case
# assert run("3\n3\n") == "1"

# small range
# assert run("1\n6\n") == "1"

# larger range
# assert run("1\n10\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 0 | single element non-divisible |
| 3 3 | 1 | first divisible Fibonacci term |
| 1 6 | 1 | small range correctness |
| 1 10 | 2 | multiple periods of pattern |

## Edge Cases

The case $L = 1$ is the only structural edge condition because it forces handling of a missing prefix index. For example, with input:

```
1
1
```

We compute only $F_1 = 1$, which is not divisible by 3, so the correct answer is 0. The algorithm handles this by treating `pref[0]` as zero explicitly.

For a second case:

```
2
3
```

We have $F_2 = 2$, $F_3 = 3$. Only index 3 contributes, so the answer is 1. The prefix subtraction `pref[3] - pref[1]` correctly isolates this single valid index without needing special-case logic beyond the boundary handling.
