---
title: "CF 464C - Substitutes in Number"
description: "We start with a decimal string s. Then a sequence of replacement rules is applied in order. Each rule has the form d - t, meaning every occurrence of digit d is replaced by the string t."
date: "2026-06-07T17:11:27+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 464
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 265 (Div. 1)"
rating: 2100
weight: 464
solve_time_s: 75
verified: true
draft: false
---

[CF 464C - Substitutes in Number](https://codeforces.com/problemset/problem/464/C)

**Rating:** 2100  
**Tags:** dp  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a decimal string `s`. Then a sequence of replacement rules is applied in order. Each rule has the form `d -> t`, meaning every occurrence of digit `d` is replaced by the string `t`.

A crucial detail is that replacements are not performed on the current string one character at a time. Each rule transforms the entire current string. Since later rules may redefine digits that appear inside earlier replacement strings, the final expansion of a digit depends on all rules that come after it.

After all replacements have been applied, the resulting string is interpreted as a decimal number and we must compute its value modulo `10^9 + 7`. Leading zeroes remain part of the string representation, but they do not affect the numeric value.

The constraints immediately rule out any simulation of the final string. The original string can have length up to `10^5`, and there can be up to `10^5` replacement rules. Although the total length of all right-hand sides is only `10^5`, repeated substitutions can make the conceptual final string astronomically large. A single digit may expand into a long string, whose digits expand again, and so on. The actual result can easily have exponentially many characters.

This means we must never build the final string. We need a compressed representation that allows us to compute the resulting number modulo `10^9 + 7`.

Several edge cases are easy to mishandle.

Consider:

```
s = "3"
rule: 3->
```

The final string is empty. The problem defines the resulting number as `0`. Any approach that assumes every replacement produces at least one digit will fail here.

Consider:

```
s = "2"
rules:
2->00
```

The final string is `"00"`. Numerically this is still `0`. The algorithm must work with string lengths and modular values separately rather than trying to strip leading zeroes.

Consider:

```
s = "1"
rules:
1->23
2->4
```

The correct final result is `"43"`, not `"23"`. The second rule affects the digit `2` introduced by the first rule. This dependency between rules is the central difficulty of the problem.

## Approaches

The brute-force idea is straightforward. Maintain the current string and apply each replacement literally. For every character equal to the target digit, append the replacement string.

This is correct because it follows the problem statement exactly. The problem is size growth. Even a tiny chain such as

```
1->11
```

repeated many times doubles the length at every step. The final string can become exponentially large, far beyond memory limits.

The key observation is that we do not need the final string itself. To compute a decimal number modulo `M`, a string contributes only two pieces of information:

1. Its length.
2. Its numeric value modulo `M`.

Suppose a string `A` has value `val(A)` and length `len(A)`, and a string `B` has value `val(B)` and length `len(B)`.

For the concatenation `AB`:

$$val(AB)=val(A)\cdot 10^{len(B)}+val(B)$$

modulo `M`.

This means every expanded digit can be represented by a pair:

$$(value,\ length)$$

without ever storing the actual string.

Now look at the replacement rules. A digit's meaning depends on future rules, not past ones. That suggests processing the rules backwards.

Imagine we already know the final expansion of every digit after all later rules have been applied. Then for a rule

```
d -> t
```

we can compute the final expansion of `d` by concatenating the already-known expansions of the digits inside `t`.

Processing from the last rule toward the first gives exactly this situation.

Initially, before any rules are processed, each digit expands to itself. Then every backward step updates one digit using the current expansions of the digits appearing on the right-hand side.

After all rules have been processed, we know the final expansion of every digit in the original string. A final scan of `s` computes the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in worst case | Exponential | Too slow |
| Optimal | O( | s | + total replacement length) |

## Algorithm Walkthrough

1. Let `MOD = 10^9 + 7`.
2. Precompute powers of ten modulo `MOD` up to the maximum possible expansion length contribution. Since the total length of all replacement strings is at most `10^5`, computing powers up to that range is sufficient.
3. For each digit `0...9`, maintain:

`val[d]` = value of its final expansion modulo `MOD`.

`len[d]` = length of its final expansion modulo `MOD-1`.
4. Initialize each digit to represent itself:

`val[d] = d`

`len[d] = 1`
5. Read all rules and store them.
6. Process the rules from last to first.
7. For a rule `d -> t`, build the expansion of `d` by scanning `t` from left to right.
8. Maintain two variables:

`cur_val`

`cur_len`

Initially both are zero.
9. For each digit `x` in `t`, concatenate the already-computed expansion of `x`:

$$cur\_val = cur\_val \cdot 10^{len[x]} + val[x] \pmod{MOD}$$

$$cur\_len = cur\_len + len[x] \pmod{MOD-1}$$

1. After the entire right-hand side has been processed, assign:

$$val[d] = cur\_val$$

$$len[d] = cur\_len$$

1. After all rules have been handled, process the original string `s`.
2. Starting from zero, concatenate the final expansion of each digit in `s` using the same formula.
3. Output the resulting value modulo `MOD`.

The reason lengths are stored modulo `MOD-1` is that powers of ten are always taken modulo `MOD`, which is prime. By Fermat's theorem:

$$10^k \bmod MOD = 10^{k \bmod (MOD-1)} \bmod MOD$$

because `10` and `MOD` are coprime.

### Why it works

Process the rules in reverse order. After handling all rules from position `i+1` onward, the pair `(val[d], len[d])` describes exactly the string obtained from digit `d` after applying those later rules.

When processing rule `i`, every digit appearing in its right-hand side already has its final representation under all later substitutions. Concatenating those representations yields precisely the final representation of the left-hand-side digit after rule `i` and all subsequent rules.

By induction on the reverse processing order, every stored pair remains correct. After the first rule has been incorporated, each digit's pair equals its complete final expansion. A final concatenation over the original string reconstructs the value of the fully transformed number, modulo `10^9 + 7`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def solve():
    s = input().strip()
    n = int(input())

    rules = []
    for _ in range(n):
        line = input().strip()
        d = int(line[0])
        t = line[3:]
        rules.append((d, t))

    max_len = 100000
    pow10 = [1] * (max_len + 1)
    for i in range(1, max_len + 1):
        pow10[i] = (pow10[i - 1] * 10) % MOD

    val = [i for i in range(10)]
    length = [1] * 10

    for d, t in reversed(rules):
        cur_val = 0
        cur_len = 0

        for ch in t:
            x = ord(ch) - ord('0')
            cur_val = (cur_val * pow10[length[x]] + val[x]) % MOD
            cur_len = (cur_len + length[x]) % (MOD - 1)

        val[d] = cur_val
        length[d] = cur_len

    ans = 0
    for ch in s:
        x = ord(ch) - ord('0')
        ans = (ans * pow10[length[x]] + val[x]) % MOD

    print(ans)

solve()
```

The solution stores two quantities for every digit.

`val[d]` is the decimal value of the digit's complete expansion modulo `10^9+7`.

`length[d]` is the expansion length modulo `10^9+6`.

The reverse processing order is the core idea. When a rule is visited, every digit appearing on its right-hand side already knows its final expansion
