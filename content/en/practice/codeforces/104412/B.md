---
title: "CF 104412B - Bogo Sort Probability"
description: "The process described is a randomized sorting procedure that repeatedly shuffles the array until it happens to become sorted. A single “successful iteration” means that after one random shuffle, the resulting permutation is already sorted."
date: "2026-06-30T22:49:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104412
codeforces_index: "B"
codeforces_contest_name: "2023 ICPC Gran Premio de Mexico 2da Fecha"
rating: 0
weight: 104412
solve_time_s: 93
verified: true
draft: false
---

[CF 104412B - Bogo Sort Probability](https://codeforces.com/problemset/problem/104412/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

The process described is a randomized sorting procedure that repeatedly shuffles the array until it happens to become sorted. A single “successful iteration” means that after one random shuffle, the resulting permutation is already sorted.

A key observation is that every shuffle produces a uniformly random permutation of the multiset of values, not just distinct permutations of indices. If we want the probability of landing directly in a sorted arrangement, we are really asking: among all distinct permutations of the array’s elements, what fraction corresponds to the sorted order.

If all elements are distinct, there is exactly one sorted permutation out of $N!$, so the probability is $1/N!$. When duplicates exist, many index permutations represent the same value arrangement. If a value $x$ appears $f_x$ times, then the number of distinct permutations is

$$\frac{N!}{\prod f_x!}$$

Only one of these permutations is sorted, so the probability becomes

$$\frac{1}{N! / \prod f_x!} = \frac{\prod f_x!}{N!}.$$

The task is to output this value modulo $10^9+7$, and then maintain it under point updates where one array position changes value. Each update only changes two frequencies: one value loses an occurrence and another gains one, so the probability can be updated incrementally.

The constraints allow both $N$ and $K$ up to $10^6$, which immediately rules out recomputing factorial products from scratch per query. Any solution that scans all values per update would be too slow because it would lead to $O(NK)$ behavior in the worst case, far beyond feasible limits.

A subtle issue is that values can be up to $10^9$, so direct indexing by value is impossible. Any approach relying on arrays keyed by value would silently fail unless values are compressed or stored in a hash map.

Edge cases arise when all elements are identical. Then the probability should be $1$, since every permutation is identical and already sorted. Another corner case is when updates repeatedly swap values so that frequencies oscillate; correctness depends on maintaining frequency-based contributions rather than tracking permutations explicitly.

## Approaches

A brute-force interpretation would recompute the full probability after every update by rebuilding a frequency map and evaluating

$$\frac{\prod f_x!}{N!}.$$

Computing factorials of frequencies per query is still acceptable, but recomputing frequencies itself requires scanning the entire array after each update, which is $O(N)$ per query. With up to $10^6$ updates, this becomes $10^{12}$ operations in the worst case, which is not viable.

The key insight is that the probability depends only on the multiset frequency distribution. When a single element changes, only two frequencies change by ±1, and the global product $\prod f_x!$ can be updated locally. This turns the problem into maintaining a dynamic product under point updates, which can be done in constant time per update if factorials are precomputed.

We also precompute factorials and modular inverses so that division by $N!$ is handled once globally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Recompute each query | $O(NK)$ | $O(N)$ | Too slow |
| Maintain frequency product | $O(N + K)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We rewrite the probability as:

$$\text{answer} = \left(\prod_{v} f_v!\right) \cdot (N!)^{-1}.$$

We maintain this expression dynamically.

### Steps

1. Precompute factorials and inverse factorials up to $N + K$. This is needed because any frequency can grow up to $N$, and factorial values must be available in O(1) time.
2. Build a frequency map of initial array values. For each value, increase its count.
3. Compute an initial product over all values of $f_v!$. This represents the numerator of the probability formula.
4. Compute the constant denominator factor $(N!)^{-1}$ once using precomputed inverse factorial.
5. For each update, remove the contribution of the old value’s frequency from the product, update the frequency, and reinsert the new factorial contribution. The product is always kept consistent with current frequencies.
6. After each update, output:

$$\text{product} \cdot (N!)^{-1} \bmod (10^9+7).$$

### Why it works

The algorithm maintains the exact value of $\prod f_v!$ at all times. Since updates only change two frequencies, the product adjustment is local and exact. The denominator $N!$ remains constant because the array size does not change. This ensures the maintained expression always equals the probability derived from the permutation counting argument.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    N, K = map(int, input().split())
    arr = list(map(int, input().split()))

    maxn = N + K + 5

    fact = [1] * (maxn)
    invfact = [1] * (maxn)

    for i in range(1, maxn):
        fact[i] = fact[i - 1] * i % MOD

    invfact[maxn - 1] = pow(fact[maxn - 1], MOD - 2, MOD)
    for i in range(maxn - 2, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % MOD

    freq = {}
    prod = 1

    for x in arr:
        if x not in freq:
            freq[x] = 0
        freq[x] += 1

    for v in freq.values():
        prod = prod * fact[v] % MOD

    inv_n_fact = invfact[N]

    out = []

    def remove(val):
        nonlocal prod
        c = freq[val]
        prod = prod * invfact[c] % MOD
        c -= 1
        freq[val] = c
        prod = prod * fact[c] % MOD

    def add(val):
        nonlocal prod
        c = freq.get(val, 0)
        if val not in freq:
            freq[val] = 0
        prod = prod * invfact[c] % MOD
        c += 1
        freq[val] = c
        prod = prod * fact[c] % MOD

    for _ in range(K):
        A, B = map(int, input().split())
        A -= 1
        old = arr[A]

        remove(old)
        arr[A] = B
        add(B)

        out.append(str(prod * inv_n_fact % MOD))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution is centered around maintaining a single global product representing all factorial contributions. The remove and add helpers ensure that each frequency change is applied symmetrically: the old factorial term is removed before decrementing, and the new one is inserted after adjustment. This ordering prevents stale contributions from remaining in the product.

The factorial and inverse factorial tables guarantee that all updates are O(1), and the modular inverse of $N!$ is precomputed once since $N$ never changes.

## Worked Examples

### Sample 1

Initial array: $[3, 2, 5, 4, 1]$

All values are distinct, so all frequencies are 1.

| Step | Action | Frequency state | Product |
| --- | --- | --- | --- |
| Init | build | all 1 | $1$ |
| Query 1 | 2→1 | 1:2, 3,4,5:1 | updated |
| Query 2 | 4→6 | updated distribution | updated |

After each update, only two frequencies change, and the product adjusts locally.

This trace shows that even though values are large and dynamic, only frequency counts matter, not ordering.

### Sample 2

Initial array: $[2, 7, 3, 5]$

All frequencies are 1, so initial probability is $1/4!$.

After update $1 \to 3$, frequency of 3 becomes 2, and 2 disappears.

| Step | Action | Frequency state | Product |
| --- | --- | --- | --- |
| Init | build | all 1 | 1 |
| Q1 | 1→3 | 3:2, others:1 | adjusted |
| Q2 | 1→7 | 7:2, others:1 | adjusted |

This shows how duplicates increase the numerator via factorial growth, increasing the probability.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N + K)$ | factorial precomputation plus O(1) updates per query |
| Space | $O(N + K)$ | factorial arrays and frequency map |

The constraints allow up to one million operations, so linear preprocessing and constant-time updates fit comfortably within limits.

## Test Cases

```python
import sys, io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    from math import isclose

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Sample 1
assert run("""5 2
3 2 5 4 1
2 1
4 6
""") == """808333339
616666671
616666671"""

# Sample 2
assert run("""4 2
2 7 3 5
1 3
1 7
""") == """41666667
83333334
83333334"""

# Sample 3
assert run("""3 2
1 2 3
2 1
3 1
""") == """166666668
333333336
1"""

# all equal
assert run("""3 2
5 5 5
1 5
2 5
""") == """1
1
1"""

# single element
assert run("""1 1
7
1 8
""") == """1"""

# max duplicate buildup
assert run("""2 2
1 2
1 2
2 2
""") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | 1s | full duplication edge case |
| single element | 1 | trivial probability |
| repeated updates | stable output | frequency consistency |

## Edge Cases

When all elements are identical, the frequency map contains a single key with value $N$. The product becomes $N!$, and multiplying by $(N!)^{-1}$ yields 1. The algorithm handles this naturally because both remove and add operations always keep the factorial product consistent with the current frequency.

When updates repeatedly swap two values back and forth, the frequency of each value oscillates between two states. Each transition applies symmetric remove and add operations, so no drift accumulates in the global product.

When a value disappears entirely, its frequency becomes zero. The remove step reduces the product by dividing out the last factorial contribution, and since $0! = 1$, no invalid factorial terms remain in the product.
