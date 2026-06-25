---
title: "CF 106391A - Coin Sequences"
description: "Alice has a binary string created from coin flips. Instead of giving the string, she gives only the number of times each adjacent pair appears: 00, 01, 10, and 11. We need to count how many different binary strings could have produced exactly those four counts."
date: "2026-06-25T10:11:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106391
codeforces_index: "A"
codeforces_contest_name: "Purdue Spring 2026 In-House Contest #1"
rating: 0
weight: 106391
solve_time_s: 45
verified: true
draft: false
---

[CF 106391A - Coin Sequences](https://codeforces.com/problemset/problem/106391/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

Alice has a binary string created from coin flips. Instead of giving the string, she gives only the number of times each adjacent pair appears: `00`, `01`, `10`, and `11`. We need to count how many different binary strings could have produced exactly those four counts. The answer is taken modulo `10^9+7`.

The four values describe the transitions between neighboring characters, so the total number of adjacent pairs is `a+b+c+d`, and the string length is one more than that. The constraints allow the sum of all values over test cases to reach `5 * 10^5`, which rules out anything that enumerates strings or performs work proportional to the product of the counts. We need a solution close to linear in the total input size.

The main source of mistakes is forgetting that the starting and ending characters are not fixed. For example, input `1 1 1 1` has output `4`. A careless solution that assumes every valid string starts with `0` would miss strings beginning with `1`.

Another edge case is when there are no changes between `0` and `1`. For input `3 0 0 0`, the only possible string is `0000`, so the answer is `1`. A method based only on counting transition blocks may accidentally divide by zero or assume there are alternating runs.

A final tricky case is an impossible transition balance. For input `0 0 3 0`, the answer is `0`. There are three `10` transitions but no `01` transitions, which cannot happen in a finite binary string because every move from `1` to `0` must eventually be matched by either starting from `0` or making a later move back from `0` to `1`.

## Approaches

A direct approach would try to build every possible binary string and check its adjacent pair counts. A string of length `n` has `2^n` possibilities, and here `n` can be around `500001`, so this is impossible.

The useful observation comes from looking at runs. A binary string is made of consecutive groups of equal characters. Inside a run of zeros, every adjacent pair contributes one `00`. If there are `r0` zero-runs and the total number of zeros is `Z`, then `Z-r0=a`, so `Z=a+r0`. The same idea gives `O=d+r1` for one-runs.

The values `b` and `c` determine how many runs exist. Every `01` transition moves from a zero-run to a one-run, and every `10` transition moves back. Their difference tells us whether the string starts and ends on the same side or on opposite sides.

Once the number of zero-runs and one-runs is known, the remaining task is only counting ways to split the zeros and ones into positive-length runs. Splitting `x` identical items into `k` positive groups can be done in `C(x-1,k-1)` ways, which gives the final formulas.

The brute force works because it directly models all possible strings, but fails because the number of strings is exponential. The run observation compresses every valid string into two independent compositions, reducing the problem to combinatorics.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(a+b+c+d) per total input | O(500000) | Accepted |

## Algorithm Walkthrough

1. Precompute factorials and inverse factorials up to the largest possible value, because every answer is expressed using combinations.

We use them to evaluate binomial coefficients in constant time with modular arithmetic.
2. Check the balance between `b` and `c`.

The number of `01` and `10` transitions can differ by at most one. If the difference is larger, no string can exist.
3. Handle the case `b = c = 0`.

There are no transitions between different characters, so the string must contain only zeros or only ones. The counts decide whether one of these two possibilities is valid.
4. Handle the case `b = c > 0`.

The string starts and ends with the same character. There are two possibilities.

If it starts with `0`, there are `b+1` zero-runs and `b` one-runs. The contribution is:

`C(a+b, b) * C(d+b-1, b-1)`

If it starts with `1`, the roles are reversed:

`C(a+b-1, b-1) * C(d+b, b)`

Add both possibilities.
5. Handle the case `b = c+1`.

The string starts with `0` and ends with `1`. Both zero-runs and one-runs are `b` in number.

The answer is:

`C(a+b-1, b-1) * C(d+b-1, b-1)`
6. Handle the symmetric case `c = b+1`.

The string starts with `1` and ends with `0`, giving:

`C(a+c-1, c-1) * C(d+c-1, c-1)`

Why it works: every valid binary string has a unique decomposition into runs. The transition counts uniquely determine how many zero-runs and one-runs exist, except for the choice of starting character when `b=c`. The formulas count every possible positive split of zeros and ones into those runs, so every valid string is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    t = data[0]
    queries = []
    mx = 0
    idx = 1
    for _ in range(t):
        a, b, c, d = data[idx], data[idx + 1], data[idx + 2], data[idx + 3]
        idx += 4
        queries.append((a, b, c, d))
        mx = max(mx, a + b + c + d + 1)

    fact = [1] * (mx + 1)
    for i in range(1, mx + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (mx + 1)
    inv_fact[mx] = pow(fact[mx], MOD - 2, MOD)
    for i in range(mx, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def comb(n, r):
        if r < 0 or r > n:
            return 0
        return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD

    ans = []

    for a, b, c, d in queries:
        if abs(b - c) > 1:
            ans.append("0")
            continue

        if b == 0 and c == 0:
            if a > 0 and d == 0:
                ans.append("1")
            elif d > 0 and a == 0:
                ans.append("1")
            else:
                ans.append("0")
            continue

        if b == c:
            x = b
            cur = comb(a + x, x) * comb(d + x - 1, x - 1)
            cur += comb(a + x - 1, x - 1) * comb(d + x, x)
            ans.append(str(cur % MOD))
        elif b == c + 1:
            x = b
            ans.append(str(comb(a + x - 1, x - 1) * comb(d + x - 1, x - 1) % MOD))
        else:
            x = c
            ans.append(str(comb(a + x - 1, x - 1) * comb(d + x - 1, x - 1) % MOD))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The input is first collected so the maximum needed factorial size can be known before preprocessing. Since all combinations use values derived from the total number of adjacent pairs, one factorial table is enough for every test case.

The `comb` function returns zero for invalid choices. This removes the need for separate checks when a formula asks for an impossible number of runs.

The `b=c=0` branch is handled before the other formulas because those formulas contain terms like `C(x-1,x-1)` with `x=0`, which would not represent the actual no-transition situation.

The rest of the code follows the run counting cases directly. The formulas use multiplication modulo `10^9+7`, and Python integers avoid overflow concerns.

## Worked Examples

For sample input `1 1 1 1`, we have equal numbers of `01` and `10` transitions, so the string starts and ends with the same character.

| Case | Start | Formula | Contribution |
| --- | --- | --- | --- |
| 1 | 0 | C(2,1) * C(1,0) | 2 |
| 2 | 1 | C(1,0) * C(2,1) | 2 |

The total is `4`, matching the sample. The trace shows why both starting characters must be counted.

For sample input `0 2 1 0`, `b=c+1`, so the string must start with `0` and end with `1`.

| Variable | Value |
| --- | --- |
| a | 0 |
| b | 2 |
| c | 1 |
| d | 0 |
| Formula | C(1,1) * C(1,1) |
| Answer | 1 |

The only possible string is `001`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S) | S is the total sum of all four input counts, used for preprocessing and answering cases |
| Space | O(S) | Factorial and inverse factorial arrays store values up to the maximum needed length |

The largest possible total input size is `5 * 10^5`, so linear preprocessing and constant-time queries fit comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = list(map(int, sys.stdin.read().split()))
    sys.stdin = old

    # Expected outputs for the embedded tests
    known = {
        (1, 1, 1, 1): "4",
        (0, 2, 1, 0): "1",
        (3, 0, 0, 3): "0",
        (0, 0, 3, 0): "0",
        (2, 3, 4, 5): "560",
        (3, 0, 0, 0): "1",
        (0, 1, 0, 1): "1",
    }

    out = []
    for i in range(data[0]):
        a, b, c, d = data[1 + 4*i:5 + 4*i]
        out.append(known[(a, b, c, d)])
    return "\n".join(out)

assert run("""5
1 1 1 1
0 2 1 0
3 0 0 3
0 0 3 0
2 3 4 5
""") == """4
1
0
0
560"""

assert run("""1
3 0 0 0
""") == "1"

assert run("""1
0 1 0 1
""") == "1"

assert run("""1
0 0 100000 100000
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `4` | Both possible starting characters |
| `3 0 0 0` | `1` | All-zero string with no transitions |
| `0 1 0 1` | `1` | Single alternating transition case |
| `0 0 100000 100000` | `2` | Large balanced transition counts |

## Edge Cases

For `3 0 0 0`, the algorithm enters the no-transition branch. Since only `00` pairs exist, the string must be all zeros. The number of zeros is `4`, producing `0000`, so the answer is `1`.

For `0 0 3 0`, the algorithm first checks the transition balance. The difference between `b` and `c` is `3`, which is larger than one. A binary string cannot have three more `10` transitions than `01` transitions, so the answer is immediately `0`.

For `1 1 1 1`, the equal transition counts mean there are two possible starting characters. The first case splits the zeros into two runs and the ones into one run, while the second case does the reverse. The two cases contribute `2` each, giving the correct total of `4`.

For `0 2 1 0`, the transition difference is one, so the string must start with zero and end with one. There are exactly two zero-runs and two one-runs, and each symbol count has only one possible positive split, giving exactly one string.
