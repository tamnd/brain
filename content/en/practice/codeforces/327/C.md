---
title: "CF 327C - Magic Five"
description: "We are given a digit string a and an integer k. The actual plate is not a itself, but the string obtained by concatenating a with itself k times. From this long string, we may delete any subset of positions, except that we are not allowed to delete every digit."
date: "2026-06-06T09:00:50+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 327
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 191 (Div. 2)"
rating: 1700
weight: 327
solve_time_s: 97
verified: true
draft: false
---

[CF 327C - Magic Five](https://codeforces.com/problemset/problem/327/C)

**Rating:** 1700  
**Tags:** combinatorics, math  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a digit string `a` and an integer `k`. The actual plate is not `a` itself, but the string obtained by concatenating `a` with itself `k` times.

From this long string, we may delete any subset of positions, except that we are not allowed to delete every digit. The remaining digits keep their original relative order and form a number, possibly with leading zeros.

We must count how many different deletion choices produce a number divisible by `5`. Two choices are considered different if they delete different sets of positions.

The length of `a` is at most `10^5`, but the final string has length `|a| · k`, and `k` can be as large as `10^9`. Constructing the full string is impossible. In the worst case it would contain `10^14` digits. Any algorithm that touches every digit of the expanded string is immediately ruled out.

The answer is required modulo `10^9+7`, which is a strong hint that the number of valid deletion sets grows exponentially and that modular arithmetic will be involved throughout the solution.

The key edge cases come from the fact that we are counting subsequences, not substrings.

Consider:

```
a = "1256"
k = 1
```

The valid numbers are `5`, `15`, `25`, and `125`. The subsequence `5` is valid even though all digits before it are deleted. A substring-based interpretation would miss several answers.

Another subtle case is:

```
a = "0"
k = 1
```

The only non-empty subsequence is `"0"`, which is divisible by `5`, so the answer is `1`. A careless solution might exclude leading-zero numbers and incorrectly return `0`.

A more interesting example is:

```
a = "5"
k = 2
```

The expanded string is `"55"`.

The valid subsequences are:

```
first 5
second 5
55
```

The answer is `3`. Counting only positions containing `5` would give `2`, forgetting that multiple digits can be kept.

Finally, when every digit is either `0` or `5`, every non-empty subsequence is divisible by `5`.

For example:

```
a = "55"
k = 1
```

The valid subsequences are:

```
first 5
second 5
55
```

giving `2² - 1 = 3`. Any solution must correctly count all possible choices of earlier digits.

## Approaches

The brute-force idea is straightforward. Construct the full string `s`, enumerate every non-empty subset of positions, build the corresponding subsequence, and test whether its value is divisible by `5`.

A number is divisible by `5` exactly when its last digit is `0` or `5`, so the divisibility test itself is easy. The problem is the number of subsequences. A string of length `n` has `2^n - 1` non-empty subsequences. Even for `n = 60`, this already exceeds `10^18`. The actual problem can reach lengths around `10^14`, so brute force is hopeless.

The observation that changes everything is that divisibility by `5` depends only on the last digit.

Suppose we decide that position `i` of the final string is the last kept digit. For the resulting number to be divisible by `5`, digit `i` must be either `0` or `5`.

Once position `i` is chosen as the last digit, every position after `i` must be deleted. Every position before `i` may be either kept or deleted independently.

If there are `i` positions before it, there are exactly `2^i` ways to choose which of them remain.

This means each occurrence of `0` or `5` contributes a power of two.

If positions are numbered from `0`, the contribution of a valid ending position is:

```
2^position
```

Thus the answer for a string `s` is

```
Σ 2^i
```

over all positions `i` whose digit is `0` or `5`.

Now we exploit the repeated structure.

Let `m = |a|`.

Position `j` inside a copy of `a` appears globally at positions

```
j,
j + m,
j + 2m,
...
j + (k-1)m
```

If `a[j]` is neither `0` nor `5`, it contributes nothing.

Otherwise its total contribution is

```
2^j (1 + 2^m + 2^(2m) + ... + 2^((k-1)m))
```

The second factor is a geometric series.

Let

```
r = 2^m
```

Then the answer becomes

```
(Σ valid positions j of 2^j)
×
(1 + r + r² + ... + r^(k-1))
```

All arithmetic is modulo `10^9+7`.

The geometric sum can be computed as

```
(r^k - 1) / (r - 1)
```

modulo `MOD`, using a modular inverse.

### Approach Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(n) | Too slow |
| Optimal | O( | a | + log k) |

## Algorithm Walkthrough

1. Read `a` and `k`.
2. Let `m = len(a)`.
3. Traverse `a` from left to right and compute

```
base = Σ 2^j
```

over all positions `j` where the digit is `0` or `5`.

Each such position represents all subsequences whose last kept digit comes from that position inside a copy.
4. Compute

```
r = 2^m mod MOD
```

because shifting by one whole copy increases the exponent by `m`.
5. Compute

```
geom = 1 + r + r² + ... + r^(k-1)
```

modulo `MOD`.

Using the geometric-series formula:

```
geom = (r^k - 1) * inverse(r - 1)
```

modulo `MOD`.
6. Multiply:

```
answer = base * geom mod MOD
```
7. Output the result.

### Why it works

Every valid subsequence has a unique last kept position. That last position must contain either `0` or `5`, otherwise the resulting number is not divisible by `5`.

Fix such a position `i`. Every position after `i` must be deleted, while each position before `i` can independently be kept or deleted. This gives exactly `2^i` subsequences ending at `i`.

Different ending positions generate disjoint sets of subsequences, since every subsequence has exactly one last position.

Summing `2^i` over all positions containing `0` or `5` counts every valid subsequence exactly once.

The repeated structure of the string allows grouping equal offsets across copies into a geometric series, producing the formula used by the algorithm.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def solve():
    a = input().strip()
    k = int(input())

    base = 0
    p2 = 1

    for ch in a:
        if ch == '0' or ch == '5':
            base = (base + p2) % MOD
        p2 = (p2 * 2) % MOD

    m = len(a)
    r = pow(2, m, MOD)

    geom = (pow(r, k, MOD) - 1) % MOD
    geom = geom * pow(r - 1, MOD - 2, MOD) % MOD

    ans = base * geom % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

The variable `base` stores the contribution from one copy of `a`. While scanning the string, `p2` always equals `2^j` modulo `MOD`, where `j` is the current position.

For every occurrence of `0` or `5`, we add the corresponding power of two. This implements the count of subsequences ending at that position.

The value `r = 2^m` represents the multiplicative factor obtained when moving one full copy to the right. Positions with the same offset inside different copies contribute a geometric progression.

The geometric sum is computed modulo `MOD` using Fermat's little theorem:

```
inverse(x) = x^(MOD-2)
```

because `MOD` is prime.

A common mistake is attempting to compute the geometric sum with ordinary integer division. All operations must remain in modular arithmetic.

Another easy bug is forgetting the modulo before multiplying by the modular inverse. The expression

```
(pow(r, k, MOD) - 1) % MOD
```

avoids negative intermediate values.

## Worked Examples

### Sample 1

Input:

```
1256
1
```

Positions containing `0` or `5`:

| Position j | Digit | 2^j | base |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 |
| 1 | 2 | 2 | 0 |
| 2 | 5 | 4 | 4 |
| 3 | 6 | 8 | 4 |

Now:

| Quantity | Value |
| --- | --- |
| m | 4 |
| r = 2^m | 16 |
| k | 1 |
| geom | 1 |
| answer | 4 |

Output:

```
4
```

The four counted subsequences are exactly `5`, `15`, `25`, and `125`.

### Sample 2

Input:

```
105
2
```

The expanded string is:

```
105105
```

For one copy:

| Position j | Digit | 2^j | Contribution |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 2 | 2 |
| 2 | 5 | 4 | 4 |

Thus:

| Quantity | Value |
| --- | --- |
| base | 6 |
| m | 3 |
| r | 8 |
| geom = 1 + 8 | 9 |
| answer | 54 |

Output:

```
54
```

This trace shows how contributions from corresponding positions in different copies form a geometric progression.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | a |
| Space | O(1) | Only a few integer variables are stored |

The string `a` contains at most `10^5` characters, so a single linear scan is trivial. Modular exponentiation takes logarithmic time in `k`, which remains tiny even when `k = 10^9`. The solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 1000000007

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    a = input().strip()
    k = int(input())

    base = 0
    p2 = 1

    for ch in a:
        if ch in "05":
            base = (base + p2) % MOD
        p2 = (p2 * 2) % MOD

    r = pow(2, len(a), MOD)
    geom = (pow(r, k, MOD) - 1) % MOD
    geom = geom * pow(r - 1, MOD - 2, MOD) % MOD

    return str(base * geom % MOD)

# provided sample
assert run("1256\n1\n") == "4", "sample 1"

# custom cases
assert run("0\n1\n") == "1", "single valid digit"
assert run("1\n1\n") == "0", "no valid ending digit"
assert run("5\n2\n") == "3", "subsequences of 55"
assert run("55\n1\n") == "3", "all non-empty subsequences valid"
assert run("05\n1\n") == "3", "leading zero subsequences allowed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0, 1` | `1` | Single valid digit |
| `1, 1` | `0` | No valid ending position |
| `5, 2` | `3` | Repeated-copy contribution |
| `55, 1` | `3` | Every non-empty subsequence valid |
| `05, 1` | `3` | Leading zeros must be counted |

## Edge Cases

Consider:

```
0
1
```

Scanning the string gives `base = 1`. The geometric factor is `1`, so the answer is `1`. The only subsequence is `"0"`, which is divisible by `5`. The algorithm naturally includes it because divisibility depends only on the last digit.

Consider:

```
1
1
```

There is no position containing `0` or `5`, so `base = 0`. Every subsequence ends with digit `1`, hence none are divisible by `5`. The answer becomes `0`.

Consider:

```
5
2
```

The expanded string is `"55"`.

The first position contributes `2^0 = 1`. The second contributes `2^1 = 2`.

Total:

```
1 + 2 = 3
```

corresponding to subsequences:

```
first 5
second 5
55
```

The geometric-series formulation reproduces exactly the same count.

Consider:

```
05
1
```

Valid subsequences are:

```
0
5
05
```

The answer is `3`.

A solution that rejects leading zeros would incorrectly count only `0` and `5`. Since the algorithm only cares about the last digit, it correctly includes `"05"` as well.
