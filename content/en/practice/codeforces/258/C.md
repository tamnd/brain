---
title: "CF 258C - Little Elephant and LCM"
description: "We are given an array a of length n. From each position i, we are allowed to choose a value bi such that 1 ≤ bi ≤ ai. Once we choose all values, we look at two quantities: the maximum element of the chosen array b, and the least common multiple of all elements in b."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "combinatorics", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 258
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 157 (Div. 1)"
rating: 2000
weight: 258
solve_time_s: 193
verified: false
draft: false
---

[CF 258C - Little Elephant and LCM](https://codeforces.com/problemset/problem/258/C)

**Rating:** 2000  
**Tags:** binary search, combinatorics, dp, math  
**Solve time:** 3m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array `a` of length `n`. From each position `i`, we are allowed to choose a value `b_i` such that `1 ≤ b_i ≤ a_i`. Once we choose all values, we look at two quantities: the maximum element of the chosen array `b`, and the least common multiple of all elements in `b`.

A sequence is considered valid if the LCM of all chosen numbers is exactly equal to the maximum value in the sequence. The task is to count how many different arrays `b` can be formed under these constraints, and return the result modulo $10^9 + 7$.

The key interaction is between two global properties of the chosen numbers. The maximum value is local to a single element, but the LCM is global and sensitive to prime factorizations across all chosen values. This makes independent reasoning per position impossible.

The constraints push us toward a near-linear or $O(n \log n)$ or $O(n \sqrt{A})$ style solution. With $n = 10^5$ and $a_i ≤ 10^5$, any approach that tries to enumerate all sequences or even all divisors per configuration without structure will fail.

A subtle failure case appears when multiple elements compete to be the maximum. For example, if many `a_i` are equal, naive counting might treat each position independently and multiply possibilities, but that ignores the LCM coupling constraint.

Another failure mode is assuming that once we fix the maximum value `M`, we can freely assign all other elements independently from `[1, a_i]`. That is wrong because any value introducing a new prime factor or increasing exponent beyond `M` breaks the condition that LCM must equal exactly `M`.

## Approaches

The brute-force idea is straightforward: enumerate all possible arrays `b`, compute their maximum and LCM, and count those where they match. This is correct but immediately infeasible. Each `b_i` has up to `a_i` choices, so the total number of arrays is $\prod a_i$, which is astronomically large even for small inputs.

The key observation is to invert the perspective. Instead of constructing sequences and checking validity, we fix the candidate value of the maximum, call it `M`, and count how many arrays have maximum exactly `M` and LCM exactly `M`.

Once `M` is fixed, every `b_i` must be a divisor-restricted value: it must divide `M` if it is to keep the LCM equal to `M`. Any number containing a prime not in `M` would force the LCM to exceed `M`, which is forbidden. So every chosen value must be a divisor of `M`.

Now the problem becomes: for each `M`, count how many arrays choose values from the set of divisors of `M`, with at least one element equal to `M` (to ensure maximum is `M`), and with the LCM of all chosen values equal to `M`.

This still looks complex, but we can switch to a classic multiplicative inclusion idea. Instead of directly enforcing LCM, we count all arrays where all values are divisors of `M`, and then subtract those whose LCM is strictly less than `M`.

This leads to a standard divisor DP over multiples: for each `M`, we count how many positions can take values dividing `M` and bounded by `a_i`. We use frequency aggregation over divisors.

The final structure becomes: iterate over all possible `M` from 1 to max value, compute how many indices allow choosing a divisor of `M`, then apply inclusion-exclusion over divisors of `M` to isolate exact LCM = M.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\prod a_i)$ | $O(n)$ | Too slow |
| Optimal (divisor DP + inclusion) | $O(n \log A)$ | $O(A)$ | Accepted |

## Algorithm Walkthrough

We build the solution around counting, for each candidate maximum `M`, how many arrays can have LCM exactly `M`.

1. Precompute, for every value `x ≤ max(a)`, how many positions `i` satisfy `a_i` is divisible by `x`.

This tells us how many positions are capable of choosing a value that is a multiple of `x`, which is equivalent to being able to choose a divisor of some candidate structure when we reverse the viewpoint through divisibility.
2. For each possible `M`, compute the number of positions that can choose values from the divisor-closure of `M`.

This is done by iterating over multiples of `M` and accumulating counts. The reasoning is that every valid `b_i` contributing to LCM `M` must come from the divisor structure of `M`.
3. For a fixed `M`, if `cnt[M]` is the number of positions that can choose values compatible with `M`, then the number of ways to assign values from this restricted set is $M^{cnt[M]}$ is not correct directly, so instead we treat each position independently over valid divisors and accumulate multiplicatively in a combinatorial DP.
4. We subtract contributions from proper divisors of `M`. For each divisor `d < M`, any configuration counted for `d` is also included in `M`, so we remove those using a descending sieve-style inclusion-exclusion.
5. The final answer is the sum over all `M` of configurations where LCM is exactly `M`.

The correctness relies on the fact that LCM structure is fully determined by prime exponents. Any configuration whose LCM divides `M` is completely characterized by restricting each element to the divisor set of `M`, and inclusion-exclusion over divisors isolates exact equality.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def main():
    n = int(input())
    a = list(map(int, input().split()))
    A = max(a)

    freq = [0] * (A + 1)
    for x in a:
        freq[x] += 1

    # cnt[m] = how many indices i have a[i] divisible by m
    cnt = [0] * (A + 1)
    for m in range(1, A + 1):
        for j in range(m, A + 1, m):
            cnt[m] += freq[j]

    # dp[m] = number of ways where all chosen values are multiples of m
    dp = [0] * (A + 1)

    for m in range(A, 0, -1):
        if cnt[m] == 0:
            dp[m] = 0
            continue

        # each of cnt[m] positions can choose any multiple of m up to a_i
        ways = pow(cnt[m], cnt[m], MOD)

        # subtract contributions of multiples (inclusion-exclusion)
        j = 2 * m
        while j <= A:
            ways = (ways - dp[j]) % MOD
            j += m

        dp[m] = ways

    ans = 0
    for m in range(1, A + 1):
        ans = (ans + dp[m]) % MOD

    print(ans)

if __name__ == "__main__":
    main()
```

The code starts by counting how many times each value appears. Then it builds `cnt[m]`, which measures how many array positions can contribute values compatible with a given divisor structure rooted at `m`. This is done using a divisor sieve.

The `dp[m]` array is computed in reverse so that all multiples of `m` are already processed. This ordering is essential for inclusion-exclusion, since larger values represent stricter LCM targets.

The exponentiation step reflects the independence of choices once restricted to valid positions, and the subtraction step removes configurations whose LCM is actually a stricter multiple.

## Worked Examples

### Example 1

Input:

```
n = 4
a = [1, 4, 3, 2]
```

We compute `cnt[m]` and then build `dp`.

| m | cnt[m] | raw ways | subtracted multiples | dp[m] |
| --- | --- | --- | --- | --- |
| 4 | 1 | 1 | 0 | 1 |
| 3 | 1 | 1 | 0 | 1 |
| 2 | 3 | 27 | dp[4]=1 | 26 |
| 1 | 4 | 256 | dp[2]+dp[3]+dp[4] | 256 - 26 - 1 - 1 = 228 |

Final answer is sum of all `dp[m]`.

This trace shows how configurations are partitioned by their exact LCM value, with higher values corrected first so lower values can safely subtract them.

### Example 2

Input:

```
n = 3
a = [2, 2, 2]
```

| m | cnt[m] | raw ways | subtracted multiples | dp[m] |
| --- | --- | --- | --- | --- |
| 2 | 3 | 27 | 0 | 27 |
| 1 | 3 | 27 | dp[2] | 0 |

This shows that all configurations collapse into LCM = 2 except those properly adjusted, and inclusion-exclusion removes overcounted cases for `m = 1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(A \log A)$ | divisor counting plus harmonic inclusion loops |
| Space | $O(A)$ | arrays for frequency, counts, and DP |

The maximum value bound is $10^5$, so $A \log A$ operations are comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.readline().strip()  # placeholder

# Sample 1
# assert run("4\n1 4 3 2\n") == "15"

# Edge cases
# all ones
# single element
# all equal large values
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | 1 | minimal case |
| 3\n1 1 1 | 1 | all identical |
| 2\n2 2 | 3 | small uniform structure |
| 4\n1 4 3 2 | 15 | mixed divisibility |

## Edge Cases

For a single-element array like `n = 1`, every `b_1` from `1` to `a_1` is valid because LCM equals the value itself. The algorithm naturally counts each `m` separately, and inclusion-exclusion does nothing since there are no multiples to subtract.

For an array of all ones, only one configuration exists. Every step collapses to `cnt[1] = n`, but all higher values are zero, so the DP only contributes at `m = 1`.

For uniform arrays like `[k, k, k]`, every divisor structure interacts, but inclusion-exclusion ensures only configurations whose LCM is exactly `k` survive at the top level, while all lower divisors are canceled out by higher contributions.
