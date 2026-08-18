---
title: "CF 102192A - Character Encoding"
description: "A word of length m can be represented by an array of m encoded character values. Every position independently chooses an integer from 0 through n - 1. We need to count how many such arrays have total sum exactly k."
date: "2026-08-18T20:30:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102192
codeforces_index: "A"
codeforces_contest_name: "2018 Chinese Multi-University Training, Nanjing U Contest"
rating: 0
weight: 102192
solve_time_s: 162
verified: true
draft: false
---

[CF 102192A - Character Encoding](https://codeforces.com/problemset/problem/102192/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

A word of length `m` can be represented by an array of `m` encoded character values. Every position independently chooses an integer from `0` through `n - 1`. We need to count how many such arrays have total sum exactly `k`.

For example, with `n = 2` and `m = 3`, every position contains either `0` or `1`. The word `[0, 1, 1]` has sum `2`, while `[1, 1, 1]` has sum `3`. Different arrays represent different words because the character choices are ordered.

The answer is taken modulo `998244353`, since the number of valid arrays can become very large.

The bounds rule out ordinary dynamic programming over both the word length and the target sum for every test case. A DP with `O(mk)` operations could require around `10^10` operations for one test case when both `m` and `k` are `10^5`. The aggregate bounds, where the sums of all `n`, `m`, and `k` are each at most `5 * 10^6`, suggest that an algorithm roughly linear in `m + k` per test case, or better, is required. Since `k <= 10^5`, factorials and inverse factorials can also be precomputed globally, allowing binomial coefficients to be evaluated in constant time.

There are several boundary cases that a direct implementation can mishandle. With `n = 1`, every character must have value `0`, so for input `1 5 0` the answer is `1`, while `1 5 1` has answer `0`. A formula that assumes every value from `0` to `n - 1` gives at least two choices can get this case wrong.

The maximum possible sum is `m(n - 1)`. Thus `2 3 3` has answer `1`, because the only array is `[1,1,1]`, while `2 3 4` has answer `0`. An implementation that only checks whether `k` is nonnegative can accidentally count impossible sums.

The lower boundary behaves similarly. For every valid `n` and `m`, the only array with sum `0` is `[0,0,...,0]`. Hence `5 4 0` has answer `1`. This is also a useful test for off-by-one errors in the binomial coefficient formula.

## Approaches

The brute-force method directly enumerates every possible word. Each of the `m` positions has `n` choices, so there are `n^m` arrays to inspect. For every array we can calculate its sum in `O(m)` time, giving `O(m n^m)` work. Even if the sum is maintained incrementally, the enumeration itself still costs `O(n^m)`. For `n = m = 10^5`, this is not merely too slow, it is astronomically beyond any practical operation count.

A standard dynamic programming formulation is much better. Let `dp[i][s]` be the number of length-`i` arrays with sum `s`. Adding one character gives

`dp[i][s] = dp[i-1][s] + dp[i-1][s-1] + ... + dp[i-1][s-(n-1)]`.

A sliding window can reduce each transition to `O(1)`, making the whole DP `O(mk)`. That is already a substantial improvement, but the worst case still needs about `10^10` operations, so it does not fit.

The key observation is that the choices at every position are exactly the integers in the interval `[0,n-1]`. Without the upper bound, the number of nonnegative solutions to

`x1 + x2 + ... + xm = k`

is the stars-and-bars value

`C(k + m - 1, m - 1)`.

The upper bound `xi <= n-1` can be handled by inclusion-exclusion. For a chosen set of `j` positions that violate the upper bound, subtract `n` from each of them. If their original values are at least `n`, write `xi = yi + n`, where `yi >= 0`. The remaining variables are unrestricted nonnegative integers, and their new sum is `k - jn`.

There are `C(m,j)` ways to choose the violating positions, and the number of nonnegative solutions after subtracting `n` is

`C(k - jn + m - 1, m - 1)`.

Consequently, the answer is

`sum (-1)^j C(m,j) C(k - jn + m - 1, m - 1)`

over all `j` for which `jn <= k`. Terms with `j > m` do not exist because we cannot choose more than `m` violating positions.

The brute-force works because it considers every valid array individually, but fails because the number of arrays is exponential. The DP groups arrays by their partial sum, but still processes too many states. The inclusion-exclusion observation groups all arrays according to which positions exceed the allowed value, reducing the calculation to at most `min(m, floor(k/n)) + 1` binomial terms.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^m)` or `O(m n^m)` with explicit sum calculation | `O(m)` | Too slow |
| DP with sliding window | `O(mk)` | `O(k)` | Too slow in the worst case |
| Inclusion-Exclusion | `O(min(m, k/n))` per test case after preprocessing | `O(max(m+k))` | Accepted |

## Algorithm Walkthrough

1. Read every test case and determine the largest value of `m + k` that will be needed. Precompute factorials and inverse factorials up to this maximum. We need these arrays because every term contains binomial coefficients.
2. Before applying the formula, check whether `k > m(n-1)`. The largest possible sum is obtained when every character has value `n-1`, so such a target has no valid word and the answer is immediately `0`.
3. For the remaining cases, initialize the answer with the `j = 0` inclusion-exclusion term,

`C(k + m - 1, m - 1)`.

This counts all nonnegative arrays with sum `k`, without enforcing the upper bound.
4. For `j = 1, 2, ...`, stop when either `j > m` or `jn > k`. For each valid `j`, calculate

`C(m,j) * C(k - jn + m - 1, m - 1)`.

The first factor chooses which `j` positions violate the upper bound. The second factor counts assignments after subtracting `n` from each selected position.
5. Add the term when `j` is even and subtract it when `j` is odd. This is the inclusion-exclusion sign corresponding to the number of selected violating positions.
6. Reduce the running answer modulo `998244353` after each operation. Finally print the normalized result.

The binomial coefficient is computed using

`C(a,b) = fact[a] * invfact[b] * invfact[a-b] mod MOD`.

Factorials are computed once, and inverse factorials are obtained from one modular inverse followed by a backward recurrence.

### Why it works

Consider the set of all nonnegative integer arrays of length `m` whose sum is `k`. Stars and bars counts this set with `C(k+m-1,m-1)`. We need to remove arrays containing one or more positions whose value is at least `n`.

For any selected set of `j` violating positions, subtract `n` from each selected value. This creates a bijection with nonnegative arrays whose sum is `k-jn`. There are `C(k-jn+m-1,m-1)` such arrays, and there are `C(m,j)` choices for the selected positions.

Inclusion-exclusion adds sets with an even number of violations and subtracts sets with an odd number. Every invalid array with `r` violating positions contributes

`C(r,0) - C(r,1) + C(r,2) - ... + (-1)^r C(r,r) = 0`,

while every valid array has zero violations and contributes exactly once. Thus the final sum counts precisely the valid words.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    t = int(input())
    tests = [tuple(map(int, input().split())) for _ in range(t)]

    max_size = 0
    for n, m, k in tests:
        max_size = max(max_size, m + k)

    fact = [1] * (max_size + 1)
    for i in range(1, max_size + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (max_size + 1)
    invfact[max_size] = pow(fact[max_size], MOD - 2, MOD)
    for i in range(max_size, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(a, b):
        if b < 0 or b > a or a < 0:
            return 0
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

    out = []

    for n, m, k in tests:
        if k > m * (n - 1):
            out.append("0")
            continue

        if k == 0:
            out.append("1")
            continue

        ans = 0
        max_j = min(m, k // n)

        for j in range(max_j + 1):
            remaining = k - j * n
            ways = comb(m, j) * comb(
                remaining + m - 1, m - 1
            ) % MOD

            if j & 1:
                ans -= ways
            else:
                ans += ways

        out.append(str(ans % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first pass over the test cases finds the largest factorial index that will be required. The largest binomial argument is `k + m - 1`, so allocating factorials through `m + k` is sufficient and avoids a separate per-test-case allocation.

The `comb` function returns zero for invalid arguments. In the main loop its arguments are always valid because `remaining = k - jn` is nonnegative, but keeping the boundary checks makes the helper safe and prevents subtle negative-index behavior.

The maximum possible sum check is performed before the inclusion-exclusion loop. This avoids unnecessary work and handles impossible targets directly.

The loop includes `j = 0`. That term is the unrestricted stars-and-bars count. The loop limit is `min(m, k // n)`, because selecting more than `m` positions is impossible and selecting `j` positions requires at least `jn` total sum.

Python integers do not overflow, but all multiplication results are reduced modulo `MOD`. This keeps intermediate values small and matches the required arithmetic.

The inverse factorial array is generated from one modular exponentiation. Since `998244353` is prime, Fermat's little theorem gives

`fact[max_size]^(MOD-2)`

as its modular inverse. Every smaller inverse factorial then follows from `invfact[i-1] = invfact[i] * i`.

## Worked Examples

### Sample 1

Consider `n = 2`, `m = 3`, `k = 3`. Every position can contain only `0` or `1`. The maximum sum is `3`, so the target is exactly at the upper boundary.

| `j` | `remaining = k - jn` | `C(m,j)` | `C(remaining+m-1,m-1)` | Signed term | Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 1 | 10 | +10 | 10 |
| 1 | 1 | 3 | 3 | -9 | 1 |

For `j = 2`, `2n = 4 > k`, so the loop stops. The result is `1`, corresponding to `[1,1,1]`.

The unrestricted count starts at `10`, which includes arrays containing values greater than `1`. The `j = 1` term removes those invalid arrays, leaving exactly the single valid array.

### Sample 2

Consider `n = 2`, `m = 3`, `k = 4`. The maximum possible sum is only `3`, so the algorithm rejects the case before performing inclusion-exclusion.

| `n` | `m` | `k` | Maximum sum `m(n-1)` | Result |
| --- | --- | --- | --- | --- |
| 2 | 3 | 4 | 3 | 0 |

This demonstrates why the maximum-sum check must use `m(n-1)`, not merely compare `k` with `m` or `n`.

### Sample 3

For `n = 3`, `m = 3`, `k = 3`, the characters have values `0`, `1`, or `2`.

| `j` | `remaining` | `C(3,j)` | Stars-and-bars count | Signed term | Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 1 | 10 | +10 | 10 |
| 1 | 0 | 3 | 1 | -3 | 7 |

The result is `7`. The unrestricted count contains exactly three arrays where one position is at least `3`, and those are removed by the first correction term.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(M + Σ min(m, k/n))` | `M = max(m+k)` for factorial preprocessing, followed by one inclusion-exclusion loop per test case |
| Space | `O(M)` | Factorial and inverse-factorial arrays |

Across all test cases, `Σk <= 5 * 10^6` and `Σm <= 5 * 10^6`. Since `min(m, k/n) <= k` for every test case, the total number of inclusion-exclusion iterations is at most `5 * 10^6` up to the small `+1` contribution from each test case. The factorial preprocessing needs only about `max(m+k) <= 2 * 10^5`, so both the time and memory requirements fit comfortably within the limits.

## Test Cases

```python
import sys
import io

MOD = 998244353

def solve(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    input = sys.stdin.readline

    t = int(input())
    tests = [tuple(map(int, input().split())) for _ in range(t)]

    max_size = max(m + k for n, m, k in tests)

    fact = [1] * (max_size + 1)
    for i in range(1, max_size + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (max_size + 1)
    invfact[max_size] = pow(fact[max_size], MOD - 2, MOD)
    for i in range(max_size, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    def comb(a, b):
        if b < 0 or b > a or a < 0:
            return 0
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD

    out = []

    for n, m, k in tests:
        if k > m * (n - 1):
            out.append("0")
            continue

        if k == 0:
            out.append("1")
            continue

        ans = 0
        for j in range(min(m, k // n) + 1):
            remaining = k - j * n
            ways = comb(m, j) * comb(
                remaining + m - 1, m - 1
            ) % MOD

            if j & 1:
                ans -= ways
            else:
                ans += ways

        out.append(str(ans % MOD))

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided samples
sample = """4
2 3 3
2 3 4
3 3 3
128 3 340
"""
assert solve(sample) == "1\n0\n7\n903\n", "provided samples"

# Minimum alphabet and minimum target
assert solve("1\n1 1 0\n") == "1\n", "minimum-size valid case"

# n = 1 has only the all-zero word
assert solve("1\n1 5 1\n") == "0\n", "n=1 impossible positive sum"

# Maximum possible sum, exactly one word
assert solve("1\n2 5 5\n") == "1\n", "upper boundary"

# Just above the maximum possible sum
assert solve("1\n2 5 6\n") == "0\n", "above upper boundary"

# n=3, m=2, k=2:
# [0,2], [1,1], [2,0]
assert solve("1\n3 2 2\n") == "3\n", "small inclusion-exclusion case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0` | `1` | Minimum-size input and the unique zero-sum word |
| `1 5 1` | `0` | The special `n = 1` case |
| `2 5 5` | `1` | Exact maximum possible sum |
| `2 5 6` | `0` | Target just beyond the feasible range |
| `3 2 2` | `3` | Small case where the inclusion-exclusion correction is exercised |

## Edge Cases

When `n = 1`, every character is forced to value `0`. For `1 5 0`, the maximum possible sum is `5(1-1)=0`, so the target is feasible and the only array is `[0,0,0,0,0]`. The algorithm returns `1`. For `1 5 1`, the target exceeds the maximum sum `0`, so it returns `0` immediately. This prevents the inclusion-exclusion loop from relying on a nonexistent positive character value.

For a target exactly at the maximum, consider `2 3 3`. Each position is at most `1`, so reaching sum `3` forces `[1,1,1]`. The formula gives `C(5,2) - C(3,1)C(2,2) = 10 - 9 = 1`. The boundary is counted correctly because the `j = 1` correction removes every unrestricted solution containing a value at least `2`.

For a target above the maximum, `2 3 4` has maximum possible sum `3`. The algorithm detects `4 > 3` and returns `0` without evaluating any binomial coefficient. A DP or inclusion-exclusion implementation that does not explicitly account for this boundary can waste substantial work, and a formula with an incorrectly handled negative remainder can produce an invalid count.

For the zero target, consider `5 4 0`. Every character value is nonnegative, so a sum of zero forces every value to be zero. The `j = 0` term is `C(3,3)=1`, and `k // n = 0`, so there are no correction terms. The answer is exactly `1`.

For a small case that exposes the upper-bound correction, consider `3 2 2`. Without the restriction `xi <= 2`, there are `C(3,1)=3` solutions: `[0,2]`, `[1,1]`, and `[2,0]`, all of which are already valid. The inclusion-exclusion loop has `j = 0` and `j = 1`, but for `j = 1`, the remaining sum is negative because `k-n = -1`, so `j=1` is not reached at all. The result remains `3`. This confirms that the loop condition `j <= k/n` correctly stops before introducing an invalid negative remaining sum.
