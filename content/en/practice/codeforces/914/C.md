---
title: "CF 914C - Travelling Salesman and Special Numbers"
description: "We are given an upper bound n, but n is not provided as a decimal integer. Instead, it is given directly as a binary string whose length can be as large as 1000 bits."
date: "2026-06-13T01:23:47+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "dp"]
categories: ["algorithms"]
codeforces_contest: 914
codeforces_index: "C"
codeforces_contest_name: "Codecraft-18 and Codeforces Round 458 (Div. 1 + Div. 2, combined)"
rating: 1800
weight: 914
solve_time_s: 240
verified: true
draft: false
---

[CF 914C - Travelling Salesman and Special Numbers](https://codeforces.com/problemset/problem/914/C)

**Rating:** 1800  
**Tags:** brute force, combinatorics, dp  
**Solve time:** 4m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an upper bound `n`, but `n` is not provided as a decimal integer. Instead, it is given directly as a binary string whose length can be as large as 1000 bits. We consider the following operation on a positive integer:

Take the number and replace it with the number of `1` bits in its binary representation.

For example:

`13 → 3 → 2 → 1`

because `13 = 1101₂` has three set bits, `3 = 11₂` has two set bits, and `2 = 10₂` has one set bit.

A number is called special if the minimum number of such operations needed to reach `1` equals `k`.

The task is to count how many positive integers `x` satisfy `1 ≤ x ≤ n` and require exactly `k` operations to reach `1`.

The unusual part of the constraints is that `n` can contain up to 1000 binary digits. That means the numeric value of `n` can be around `2^1000`, far beyond what can be enumerated. Any solution that iterates through numbers up to `n` is immediately impossible.

The length limit of 1000 bits suggests that algorithms proportional to the bit length are acceptable. Dynamic programming on the binary representation, often called digit DP, becomes a natural candidate.

Several edge cases are easy to mishandle.

Consider:

```
1
0
```

The only number not exceeding `1` is `1` itself. Since `1` is already equal to `1`, it needs zero operations. The correct answer is `1`. A solution that blindly applies the general recurrence for positive operation counts will miss this case.

Consider:

```
1
1
```

No number `≤ 1` requires exactly one operation. Number `1` requires zero operations. The correct answer is `0`.

Another subtle case is:

```
10
1
```

Here `n = 2`. The only special number is `2`, because `2 → 1` in one step. Number `1` must not be counted. Many implementations count all numbers having one set bit and accidentally include `1`.

A final trap is that the number of set bits may be zero during the DP. The value `0` is not a positive integer and should never contribute to the answer.

## Approaches

A brute-force solution is conceptually straightforward. For every integer `x` from `1` to `n`, repeatedly replace it by its popcount until reaching `1`, count how many steps were needed, and check whether that count equals `k`.

The operation chain is short because popcount collapses large numbers very quickly. For numbers below `2^1000`, one application produces a value at most `1000`, and after that the values become tiny. The problem is not the chain length, it is the number of starting values. When `n` itself may be close to `2^1000`, iterating over all candidates is hopeless.

The key observation is that after the first operation, the future behavior depends only on the number of set bits of the original number.

Suppose a number `x` contains exactly `s` ones in its binary representation.

After one operation:

```
x → s
```

From that point onward, the process is completely determined by `s`.

Define:

```
f(v) = minimum operations needed to reduce v to 1
```

for ordinary integers `v`.

If `x` has `s` set bits and `x > 1`, then:

```
f(x) = 1 + f(s)
```

So instead of reasoning about enormous numbers, we only need to know how many set bits they contain. Since the binary length is at most 1000, the number of set bits is at most 1000 as well.

This transforms the problem into two separate pieces.

First, precompute `f(s)` for all `s ≤ 1000`.

Second, for every possible set-bit count `s`, count how many numbers `x ≤ n` contain exactly `s` ones. This is a classic combinatorial digit-DP problem on a binary string.

The numbers contributing to the answer are exactly those whose set-bit count `s` satisfies:

```
1 + f(s) = k
```

except for the special handling of `x = 1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) | O(1) | Too slow |
| Optimal | O(L²) | O(L²) | Accepted |

Here `L` is the binary length of `n`, at most `1000`.

## Algorithm Walkthrough

1. Read the binary string `n` and let `L` be its length.
2. Handle the special case `k = 0`.

The only number requiring zero operations is `1` itself. If `1 ≤ n`, which is always true because `n` is positive, the answer is `1`.
3. Precompute the operation counts for all values from `1` to `1000`.

Let:

```
steps[1] = 0
steps[i] = 1 + steps[popcount(i)]
```

for `i > 1`.

Since `popcount(i) < i` for every `i > 1`, the values can be computed in increasing order.
4. Determine all set-bit counts `s` satisfying:

```
1 + steps[s] = k
```

Any number with exactly `s` ones will require exactly `k` operations, provided the number itself is greater than `1`.
5. Precompute binomial coefficients `C(n,r)` modulo `10^9+7` for all `0 ≤ n,r ≤ 1000`.

These coefficients allow us to count how many binary strings of a certain remaining length contain a given number of ones.
6. For each valid set-bit count `s`, count how many numbers `x ≤ n` have exactly `s` ones.

Scan the bits of `n` from left to right.

Whenever a position contains `1`, we may place `0` there and make the resulting number strictly smaller than `n`. The remaining positions can then be filled arbitrarily.

If we have already used `used` ones so far and there are `rem` positions left, then choosing `0` at the current position contributes:

```
C(rem, s - used)
```

whenever `s - used` is feasible.

Then continue the scan assuming we match `n` and place `1`, increasing `used`.
7. After the scan finishes, if the number `n` itself contains exactly `s` ones, add one more count.
8. Sum the counts over all valid `s`.
9. When `k = 1`, subtract one from the answer.

The reason is that `s = 1` satisfies:

```
1 + steps[1] = 1
```

and the counting procedure includes the number `1`. But `1` actually requires zero operations, not one.
10. Output the result modulo `10^9+7`.

### Why it works

For every positive integer `x > 1`, the first operation sends it to `popcount(x)`. After that moment, the future sequence depends only on that popcount value. If `x` contains `s` ones, then the total number of operations equals `1 + steps[s]`.

The algorithm enumerates all possible values of `s` that lead to exactly `k` operations. For each such `s`, the digit-DP counting procedure counts every number `≤ n` with exactly `s` set bits exactly once. The combinatorial transitions correspond to the first position where the constructed number becomes smaller than `n`.

Since every valid number has a unique set-bit count and every counted number satisfies the required operation count, the final sum is exactly the desired answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

n = input().strip()
k = int(input())

L = len(n)

if k == 0:
    print(1)
    sys.exit()

# steps[i] = operations needed for i -> 1
steps = [0] * (L + 1)
steps[1] = 0

for i in range(2, L + 1):
    steps[i] = steps[i.bit_count()] + 1

# binomial coefficients
C = [[0] * (L + 1) for _ in range(L + 1)]
for i in range(L + 1):
    C[i][0] = C[i][i] = 1
    for j in range(1, i):
        C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD

def count_with_ones(target):
    used = 0
    res = 0

    for i, ch in enumerate(n):
        if ch == '1':
            rem = L - i - 1
            need = target - used

            if 0 <= need <= rem:
                res = (res + C[rem][need]) % MOD

            used += 1

    if used == target:
        res = (res + 1) % MOD

    return res

ans = 0

for ones in range(1, L + 1):
    if 1 + steps[ones] == k:
        ans = (ans + count_with_ones(ones)) % MOD

if k == 1:
    ans = (ans - 1) % MOD

print(ans % MOD)
```

The `steps` array stores the number of operations needed for small integers up to 1000. This works because after one popcount operation every relevant number becomes at most the bit length of `n`.

The binomial table supports the counting phase. When the scan encounters a `1` bit in `n`, we can choose a smaller digit `0` and freely distribute the remaining required ones among the remaining positions. The number of such distributions is exactly a binomial coefficient.

The function `count_with_ones(target)` performs the digit-DP counting. Rather than storing states in a DP table, it uses the standard combinatorial counting trick for binary upper bounds.

The subtraction for `k = 1` is the most delicate part of the implementation. Numbers with one set bit satisfy the condition `1 + steps[1] = 1`, but the number `1` itself should not belong to that category because it already equals `1` before any operation.

## Worked Examples

### Example 1

Input:

```
110
2
```

Here `n = 6`.

The valid set-bit counts satisfy:

```
1 + steps[s] = 2
```

Only `s = 2` works because:

```
2 -> 1
```

in one step.

Counting numbers ≤ 110₂ with exactly two ones:

| Position | Bit of n | used before | Contribution |
| --- | --- | --- | --- |
| 0 | 1 | 0 | C(2,2)=1 |
| 1 | 1 | 1 | C(1,1)=1 |
| 2 | 0 | 2 | 0 |

The final number itself also has two ones, so add one.

| Source | Count |
| --- | --- |
| 011₂ = 3 | 1 |
| 101₂ = 5 | 1 |
| 110₂ = 6 | 1 |
| Total | 3 |

Output:

```
3
```

This example shows how the counting process enumerates all numbers with a fixed popcount without explicitly generating them.

### Example 2

Input:

```
10
1
```

Here `n = 2`.

Valid set-bit counts satisfy:

```
1 + steps[s] = 1
```

Only `s = 1`.

Counting numbers with one set bit:

| Number | Ones |
| --- | --- |
| 1 | 1 |
| 2 | 1 |

The counting routine returns `2`.

However, `1` requires zero operations:

```
1
```

So we subtract it.

| Quantity | Value |
| --- | --- |
| Raw count | 2 |
| Remove number 1 | -1 |
| Final answer | 1 |

The remaining valid number is `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L²) | Building combinations dominates |
| Space | O(L²) | Binomial coefficient table |

With `L ≤ 1000`, the table contains roughly one million entries. This easily fits within the memory limit, and the quadratic preprocessing is comfortably fast in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    MOD = 10 ** 9 + 7

    n = input().strip()
    k = int(input())

    L = len(n)

    if k == 0:
        print(1)
        return

    steps = [0] * (L + 1)
    for i in range(2, L + 1):
        steps[i] = steps[i.bit_count()] + 1

    C = [[0] * (L + 1) for _ in range(L + 1)]
    for i in range(L + 1):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD

    def count(target):
        used = 0
        res = 0

        for i, ch in enumerate(n):
            if ch == '1':
                rem = L - i - 1
                need = target - used

                if 0 <= need <= rem:
                    res += C[rem][need]

                used += 1

        if used == target:
            res += 1

        return res % MOD

    ans = 0
    for s in range(1, L + 1):
        if 1 + steps[s] == k:
            ans += count(s)

    if k == 1:
        ans -= 1

    print(ans % MOD)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("110\n2\n") == "3", "sample 1"

# minimum value
assert run("1\n0\n") == "1", "only number 1"

# number 1 is not special for k=1
assert run("1\n1\n") == "0", "special handling of 1"

# boundary where only 2 qualifies
assert run("10\n1\n") == "1", "remove number 1"

# numbers <= 3 needing exactly one operation: only 2
assert run("11\n1\n") == "1", "small boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `1` | Zero-operation special case |
| `1 / 1` | `0` | Number 1 must not be counted for k=1 |
| `10 / 1` | `1` | Correct subtraction of number 1 |
| `11 / 1` | `1` | Inclusive upper-bound counting |
| `110 / 2` | `3` | Sample scenario |

## Edge Cases

Consider:

```
1
0
```

The algorithm immediately triggers the dedicated `k = 0` branch and returns `1`. No DP is needed. This matches the fact that only the number `1` already equals the target state.

Consider:

```
1
1
```

The general popcount-counting logic would identify numbers with one set bit. That includes `1`. The correction for `k = 1` removes exactly this unwanted contribution, leaving answer `0`.

Consider:

```
10
1
```

The counting routine finds two numbers with one set bit, namely `1` and `2`. After subtracting the contribution of `1`, only `2` remains. The final answer becomes `1`, which is correct because:

```
2 -> 1
```

takes exactly one operation.

Consider:

```
1000
2
```

Here `n = 8`. The valid set-bit count is `2`. The digit-DP counts exactly the numbers:

```
3, 5, 6
```

Each has two ones, and:

```
3 -> 2 -> 1
5 -> 2 -> 1
6 -> 2 -> 1
```

No larger number not exceeding `8` has two set bits. The answer is `3`, confirming that the combinatorial counting handles exact upper-bound restrictions correctly.
