---
title: "CF 238A - Not Wool Sequences"
description: "We are counting arrays of length n where every element is chosen from the range [0, 2^m - 1]. A sequence is considered \"wool\" if some contiguous subarray has xor equal to 0. The task is to count the sequences that avoid this completely."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 238
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 148 (Div. 1)"
rating: 1300
weight: 238
solve_time_s: 93
verified: true
draft: false
---

[CF 238A - Not Wool Sequences](https://codeforces.com/problemset/problem/238/A)

**Rating:** 1300  
**Tags:** constructive algorithms, math  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are counting arrays of length `n` where every element is chosen from the range `[0, 2^m - 1]`. A sequence is considered "wool" if some contiguous subarray has xor equal to `0`. The task is to count the sequences that avoid this completely.

Another way to phrase the condition is through prefix xors. Define:

$$pref_i = a_1 \oplus a_2 \oplus \dots \oplus a_i$$

and let `pref_0 = 0`.

A subarray xor from `l` to `r` equals:

$$pref_r \oplus pref_{l-1}$$

This becomes `0` exactly when:

$$pref_r = pref_{l-1}$$

So a sequence is not wool precisely when all prefix xors are distinct.

That reformulation changes the problem from "check all subarrays" into "count sequences whose prefix xor values never repeat".

The constraints are large enough that brute force is impossible. Both `n` and `m` can reach `10^5`. The number of possible arrays is:

$$(2^m)^n = 2^{mn}$$

which is astronomically large even for moderate values. Any algorithm that tries to enumerate arrays or inspect all subarrays is ruled out immediately.

The target complexity should be close to linear or logarithmic in the input size. Since the answer only depends on combinatorial counting, the real challenge is finding the correct formula.

One subtle edge case appears when `n > 2^m`. There are only `2^m` possible xor states because every xor value fits in `m` bits. Since the prefix xor sequence includes `pref_0`, we would need `n + 1` distinct prefix xor values to avoid repetition. That becomes impossible once:

$$n + 1 > 2^m$$

For example:

```
Input:
4 1
```

Here the values are only `0` and `1`, so there are only two xor states. We would need five distinct prefix xors, which cannot happen. The correct answer is `0`.

Another easy mistake is forgetting that `pref_0 = 0` already exists before processing any elements. If some prefix xor later becomes `0`, then the subarray from the beginning has xor `0`. For example:

```
Input:
1 2
```

The allowed values are `0,1,2,3`. The single-element sequence `[0]` is wool because its xor is `0`. Only `[1]`, `[2]`, and `[3]` are valid, so the answer is `3`.

A careless implementation that only checks repeated prefix xors among positive indices would incorrectly count `[0]` as valid.

## Approaches

The brute-force idea is straightforward. Generate every possible sequence of length `n`, compute all subarray xors, and reject sequences containing a zero-xor segment.

There are `2^m` choices for each position, so the total number of arrays is:

$$(2^m)^n$$

Even if checking one sequence were free, this already explodes far beyond feasibility. With `n = 10^5`, brute force is completely impossible.

The key observation comes from the prefix xor interpretation. A sequence is valid exactly when all prefix xors are distinct.

Suppose we build the sequence from left to right.

Initially:

$$pref_0 = 0$$

When choosing `a_1`, the new prefix xor becomes:

$$pref_1 = pref_0 \oplus a_1$$

To remain valid, `pref_1` must differ from all previous prefix xors. Since only `pref_0` exists, we cannot choose `a_1 = 0`.

After choosing several elements, assume we already have `i` distinct prefix xor values:

$$pref_0, pref_1, \dots, pref_{i-1}$$

When selecting the next element, the next prefix xor is:

$$pref_i = pref_{i-1} \oplus a_i$$

Because xor with a fixed value is a bijection, every forbidden prefix xor corresponds to exactly one forbidden value of `a_i`.

There are exactly `i` forbidden xor states at step `i`, so there are exactly `i` forbidden choices for `a_i`.

Since the total number of possible values is `2^m`, the number of valid choices becomes:

$$2^m - i$$

Multiplying these choices across all positions gives:

$$(2^m - 1)(2^m - 2)\dots(2^m - n)$$

If `n \ge 2^m`, eventually one factor becomes zero, so the answer is zero automatically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{mn} \cdot n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`.
2. Compute:

$$k = 2^m$$

This is the total number of distinct xor states and also the number of possible element values.

1. If `n >= k`, print `0`.

A valid sequence requires `n + 1` distinct prefix xor values including `pref_0`. Since only `k` xor states exist, this becomes impossible once `n + 1 > k`.

1. Otherwise, initialize the answer as `1`.
2. For each `i` from `1` to `n`, multiply the answer by:

$$k - i$$

At step `i`, exactly `i` prefix xor states are already occupied, so exactly `i` choices would create a repeated prefix xor. The remaining `k - i` choices are valid.

1. Take every multiplication modulo `10^9 + 9`.
2. Print the final answer.

### Why it works

The invariant is that after processing `i - 1` elements, all prefix xors are distinct.

When choosing the next element, each previously seen prefix xor corresponds to exactly one forbidden value of the new element because:

$$a_i = pref_{i-1} \oplus target$$

for a desired next prefix xor `target`.

Since xor with a fixed value is bijective, different forbidden prefix xors produce different forbidden values. That means exactly `i` choices are invalid at step `i`.

Choosing any of the remaining values creates a brand new prefix xor, preserving the invariant. By induction, the counting formula counts exactly all valid sequences.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000009

n, m = map(int, input().split())

k = 1 << m

if n >= k:
    print(0)
else:
    ans = 1

    for i in range(1, n + 1):
        ans = (ans * (k - i)) % MOD

    print(ans)
```

The implementation follows the counting argument directly.

`k = 1 << m` computes `2^m` efficiently using bit shifting. Since `m ≤ 10^5` would normally make this enormous, many languages would overflow fixed-width integers. Python integers grow automatically, so this remains safe.

The condition `n >= k` is the impossibility check. We need `n + 1` distinct prefix xors, but only `k` exist. Rearranging gives the equivalent condition:

$$n \ge k$$

The loop multiplies all valid choices:

$$(k - 1)(k - 2)\dots(k - n)$$

The modulo operation is applied after every multiplication to keep numbers manageable.

A common off-by-one mistake is starting the loop at `0`. The first element has `k - 1` valid choices because choosing `0` would immediately repeat `pref_0`.

## Worked Examples

### Example 1

Input:

```
3 2
```

Here:

$$k = 2^2 = 4$$

| Step | Used Prefix XORs | Valid Choices | Answer |
| --- | --- | --- | --- |
| Start | `{0}` | - | 1 |
| i = 1 | 1 forbidden | 3 | 3 |
| i = 2 | 2 forbidden | 2 | 6 |
| i = 3 | 3 forbidden | 1 | 6 |

Final answer:

```
6
```

This trace shows how each new prefix xor consumes one xor state permanently. The number of available choices decreases by one at every step.

### Example 2

Input:

```
4 1
```

Here:

$$k = 2^1 = 2$$

We would need `5` distinct prefix xors:

$$pref_0, pref_1, pref_2, pref_3, pref_4$$

but only two xor states exist.

| Step | Value |
| --- | --- |
| k | 2 |
| n | 4 |
| Check | $4 \ge 2$ |

The algorithm immediately prints:

```
0
```

This example demonstrates the pigeonhole principle behind the impossibility condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One multiplication per position |
| Space | $O(1)$ | Only a few variables are stored |

The algorithm easily fits within the limits. Even for `n = 10^5`, the loop performs only one hundred thousand modular multiplications, which is trivial in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 1000000009

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    k = 1 << m

    if n >= k:
        print(0)
        return

    ans = 1

    for i in range(1, n + 1):
        ans = (ans * (k - i)) % MOD

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("3 2\n") == "6\n", "sample 1"

# minimum size
assert run("1 1\n") == "1\n", "minimum case"

# impossible because n >= 2^m
assert run("4 1\n") == "0\n", "impossible case"

# single element cannot be zero
assert run("1 2\n") == "3\n", "exclude zero"

# exact boundary before impossible
assert run("3 2\n") == "6\n", "boundary valid case"

# larger valid case
assert run("2 3\n") == "42\n", "8*7 reduced by first forbidden choice"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Smallest valid instance |
| `4 1` | `0` | Impossible when xor states run out |
| `1 2` | `3` | First element cannot be zero |
| `3 2` | `6` | Boundary where all xor states are consumed exactly |
| `2 3` | `42` | General multiplication formula |

## Edge Cases

Consider the input:

```
1 2
```

There are four possible values: `0,1,2,3`.

The algorithm computes:

$$k = 4$$

The first position has:

$$k - 1 = 3$$

valid choices.

Those are exactly `1,2,3`. Choosing `0` creates:

$$pref_1 = pref_0 = 0$$

which immediately forms a zero-xor subarray. The algorithm correctly excludes it.

Now consider:

```
4 1
```

The xor states are only `0` and `1`.

The algorithm checks:

$$n \ge k$$

which becomes:

$$4 \ge 2$$

so it outputs `0`.

To see why, observe that a valid sequence would require five distinct prefix xors:

$$pref_0, pref_1, pref_2, pref_3, pref_4$$

but only two states exist. Repetition becomes unavoidable, which means some subarray xor must become zero.

Finally, consider:

```
2 2
```

The algorithm computes:

$$(4 - 1)(4 - 2) = 3 \cdot 2 = 6$$

The first element has three valid choices because `0` is forbidden. After selecting one prefix xor, two xor states remain available for the next step.

The distinct-prefix invariant remains true throughout the construction, so every counted sequence is valid.
