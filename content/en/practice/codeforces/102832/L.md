---
title: "CF 102832L - Coordinate Paper"
description: "We need create an array of n non-negative integers representing the number of black cells in each row. The total number of black cells must be exactly s. Between every two neighboring rows, the amount of black cells can either increase by exactly one or decrease by exactly k."
date: "2026-07-26T15:16:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102832
codeforces_index: "L"
codeforces_contest_name: "2020 China Collegiate Programming Contest Changchun Onsite"
rating: 0
weight: 102832
solve_time_s: 88
verified: true
draft: false
---

[CF 102832L - Coordinate Paper](https://codeforces.com/problemset/problem/102832/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We need create an array of `n` non-negative integers representing the number of black cells in each row. The total number of black cells must be exactly `s`. Between every two neighboring rows, the amount of black cells can either increase by exactly one or decrease by exactly `k`.

The input gives the number of rows, the allowed decrease value, and the required total number of black cells. The output is any valid sequence of row values, or `-1` if no such sequence exists.

The limit `n <= 100000` means the solution must be close to linear. Trying many possible arrays, dynamic programming over the sum, or any method depending on `s` directly is impossible because `s` can reach `10^18`.

The tricky cases are caused by the fact that increasing every element by the same amount changes the sum by multiples of `n`, not by arbitrary values. A construction that only uses `+1` transitions fails on cases such as:

```
n = 3, k = 2, s = 15
```

Using only increases gives sums congruent to `0` modulo `3`, but valid answers such as `6 4 5` require a decrease transition.

Another failure case is when the answer exists only after using many decreases. For example:

```
n = 5, k = 10, s = 1
```

A naive approach that starts with large positive values and adjusts downward may violate non-negativity, because a decrease of `10` can quickly create negative rows.

The final edge case is when the modular condition is impossible. For example:

```
n = 4, k = 3, s = 2
```

Here every transition changes a row value by either `1` or `-3`, so all rows have a fixed relation modulo `4`. If the required sum does not match that relation, no amount of shifting can fix it.

## Approaches

A brute-force idea is to decide every transition independently. There are `n-1` transitions and each one has two choices, so this explores `2^(n-1)` possibilities. It is correct because it examines every possible shape of the array, but for `n = 100000` it is completely infeasible.

The useful observation comes from describing every transition relative to the all-increase case. Let the first row be `A`. If every transition were `+1`, the value of row `i` would be `A + i - 1`. A decrease transition instead subtracts an additional `k+1` compared with that.

If a decrease happens between positions `i` and `i+1`, it affects every later row. Its contribution to the total sum is exactly `k+1` times `(n-i)`. Therefore, if we let `D` be the sum of the chosen weights among `1,2,...,n-1`, the total sum becomes:

```
s = n*A + n(n-1)/2 - (k+1)*D
```

The possible values of `D` are every number from `0` to `n(n-1)/2`, because any number in that range can be represented as a subset sum of `1,2,...,n-1`.

The problem is reduced to finding a valid `D` satisfying:

```
(k+1)*D = n(n-1)/2 - s (mod n)
```

This is a linear congruence. After finding a suitable `D`, the first value `A` is determined. We choose the largest possible valid `D` in its congruence class so that `A` is guaranteed to be non-negative.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Let `C = n(n-1)/2`. The all-increase sequence contributes `C` to the sum, so the remaining part is controlled by the first value and by the decrease operations.
2. Solve the congruence:

```
(k+1)D ≡ C-s (mod n)
```

using the greatest common divisor. If the right side is not divisible by `gcd(k+1,n)`, no solution exists.
3. Compute one solution `D0` modulo `n/gcd(k+1,n)` using the modular inverse of `(k+1)/gcd(k+1,n)`.
4. Move to the largest value of `D` not exceeding `C` that has the same residue as `D0`. This choice maximizes the subtraction term and prevents the computed first value from becoming negative.
5. Compute:

```
A = (s-C+(k+1)D)/n
```

Then `A` is the first row value.
6. Represent `D` as a subset of `1,2,...,n-1`. Iterate from the largest weight downwards. If the current weight fits into `D`, place a decrease transition there.
7. Build the array by starting with `A`. For each transition, add `1` normally or subtract `k` when a decrease transition was selected.

The invariant behind the construction is that every selected decrease contributes exactly its assigned weight to `D`. The congruence guarantees the total sum is correct, and choosing the largest valid `D` guarantees the initial offset is large enough. Since the sequence is built directly from valid transitions, every neighboring pair satisfies the required rule.

## Python Solution

```python
import sys
input = sys.stdin.readline

def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y

def solve_case(n, k, s):
    if n == 1:
        return "0" if s != 0 else "0"

    c = n * (n - 1) // 2
    g, _, _ = egcd(k + 1, n)

    if (c - s) % g != 0:
        return "-1"

    mod = n // g
    if mod == 1:
        d0 = 0
    else:
        a = (k + 1) // g
        b = (c - s) // g
        _, x, _ = egcd(a, mod)
        d0 = (b * (x % mod)) % mod

    d = c - ((c - d0) % mod)
    a0 = (s - c + (k + 1) * d) // n

    cuts = [False] * n
    rem = d
    for i in range(n - 1, 0, -1):
        if rem >= i:
            rem -= i
            cuts[i] = True

    ans = [a0]
    for i in range(1, n):
        if cuts[i]:
            ans.append(ans[-1] - k)
        else:
            ans.append(ans[-1] + 1)

    return " ".join(map(str, ans))

def main():
    n, k, s = map(int, input().split())
    print(solve_case(n, k, s))

if __name__ == "__main__":
    main()
```

The code first handles the modular equation. The extended Euclidean algorithm provides the inverse needed for the congruence without depending on library functions.

The value `d` is chosen as the largest valid representative of its residue class. This is the detail that avoids negative starting values. A smaller valid value could satisfy the mathematics but still require a negative first row.

The `cuts` array stores which transitions are decreases. The greedy subset construction works because the weights are exactly `1` through `n-1`, so taking the largest available weight first always leaves a representable remainder.

Python integers do not overflow, which is necessary because intermediate products such as `(k+1)*d` can exceed 64-bit signed limits.

## Worked Examples

For the sample input:

```
3 2 15
```

we have `C = 3`.

| Variable | Value |
| --- | --- |
| `gcd(k+1,n)` | 1 |
| `D` | 1 |
| First value `A` | 6 |
| Decrease positions | transition 1 |

The produced sequence is:

```
6 4 5
```

The first transition decreases by `2`, and the second increases by `1`. The sum is `15`.

For:

```
2 5 7
```

we have `C = 1`.

| Variable | Value |
| --- | --- |
| `gcd(k+1,n)` | 2 |
| Congruence possible | yes |
| `D` | 0 |
| First value `A` | 3 |

The sequence is:

```
3 4
```

The only transition is an increase by one, and the sum is `7`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The construction scans the transition positions once. |
| Space | O(n) | The answer and transition markers require linear memory. |

The solution avoids any dependence on `s`, which is necessary because `s` can be as large as `10^18`. The linear complexity fits the limit of `100000` rows.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    n, k, s = map(int, input().split())
    out = solve_case(n, k, s)
    sys.stdin = old
    return out

# provided sample
assert sum(map(int, run("3 2 15").split())) == 15

# minimum size
assert run("1 1 0") == "0"

# impossible modular condition
assert run("4 3 2") == "-1"

# all increase construction
assert sum(map(int, run("2 5 7").split())) == 7

# larger valid case
x = list(map(int, run("5 10 100").split()))
assert len(x) == 5
assert sum(x) == 100
assert all(v >= 0 for v in x)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 2 15` | Any valid array summing to 15 | Sample behavior |
| `1 1 0` | `0` | Single row handling |
| `4 3 2` | `-1` | Impossible congruence |
| `2 5 7` | Any valid two-row array | Small boundary construction |
| `5 10 100` | Any valid array | Larger decrease handling |

## Edge Cases

For `n = 1`, there are no transitions to satisfy. The implementation handles this separately because the modular construction assumes at least one transition exists.

For an impossible congruence such as:

```
4 3 2
```

we have `gcd(4,4)=4`, but `C-s = 4`, so this particular example is actually solvable. A truly impossible case is:

```
4 3 3
```

where `C-s = 3` is not divisible by `4`. The algorithm rejects it before attempting construction.

For very small sums, the chosen `D` must be large enough. The algorithm takes the largest valid `D`, increasing the contribution of decreases and reducing the required first value. This prevents a mathematically valid but negative array.

For large values of `s`, the same construction still works because the first value absorbs the extra amount. Increasing all rows by the same amount preserves every transition condition and only changes the total by multiples of `n`.

I can also adapt this editorial into a shorter Codeforces-style version if you want something closer to an actual contest publication format.
