---
title: "CF 238A - Not Wool Sequences"
description: "We work with arrays of length n, where every element is an integer from 0 to 2^m - 1. A sequence is called \"wool\" if there exists some contiguous subarray whose xor is 0. We are asked to count how many sequences are not wool, meaning every contiguous subarray has non-zero xor."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 238
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 148 (Div. 1)"
rating: 1300
weight: 238
solve_time_s: 318
verified: true
draft: false
---

[CF 238A - Not Wool Sequences](https://codeforces.com/problemset/problem/238/A)

**Rating:** 1300  
**Tags:** constructive algorithms, math  
**Solve time:** 5m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We work with arrays of length `n`, where every element is an integer from `0` to `2^m - 1`.

A sequence is called "wool" if there exists some contiguous subarray whose xor is `0`. We are asked to count how many sequences are _not_ wool, meaning every contiguous subarray has non-zero xor.

The answer must be computed modulo `10^9 + 9`.

The first thing to notice is that xor over a subarray is naturally connected to prefix xors. If we define

$$p_i = a_1 \oplus a_2 \oplus \cdots \oplus a_i$$

with `p_0 = 0`, then the xor of subarray `[l, r]` equals

$$p_r \oplus p_{l-1}$$

A subarray xor becomes zero exactly when two prefix xors are equal.

So the problem is secretly asking:

"How many arrays produce pairwise distinct prefix xors `p_0, p_1, ..., p_n`?"

That reformulation is the whole problem.

The constraints are large enough that brute force enumeration is impossible. Both `n` and `m` can reach `10^5`. The number of arrays is

$$(2^m)^n = 2^{mn}$$

which is astronomically large even for moderate values. Any solution that iterates over arrays, subsets, or xor states per position in quadratic fashion will fail.

The target complexity is roughly linear or logarithmic in `n` and `m`.

There are several easy-to-miss edge cases.

If `n >= 2^m`, the answer is automatically zero. There are only `2^m` possible prefix xor values, but we need `n + 1` distinct values because of `p_0`. By the pigeonhole principle, repetition is unavoidable.

For example:

```
n = 2, m = 1
```

Allowed values are `{0, 1}`.

There are only two possible prefix xors, but we need three distinct values:

$$p_0, p_1, p_2$$

Impossible, so the correct answer is `0`.

A careless implementation may try to compute a falling factorial with negative terms and accidentally produce garbage instead of zero.

Another subtle case is arrays containing zero. Any element `a_i = 0` immediately creates a zero-xor subarray of length one.

For example:

```
n = 1, m = 3
```

Allowed numbers are `0..7`.

Only value `0` is forbidden, so the answer is `7`.

A buggy derivation that forgets about `p_i != p_{i-1}` would incorrectly count all `8` arrays.

## Approaches

The brute force approach is straightforward. Generate every array of length `n`, compute xor for every subarray, and check whether any xor equals zero.

There are `2^{mn}` arrays. Even if we optimize subarray xor computation using prefix xors, each array still requires checking all `O(n^2)` subarrays.

The total complexity becomes

$$O(2^{mn} \cdot n^2)$$

which is hopeless even for tiny inputs.

The problem becomes manageable once we rewrite the condition using prefix xors.

Define:

$$p_0 = 0$$

$$p_i = a_1 \oplus a_2 \oplus \cdots \oplus a_i$$

Then:

$$a_i = p_i \oplus p_{i-1}$$

Every choice of prefix xors uniquely determines the array.

A subarray `[l, r]` has xor zero exactly when:

$$p_r = p_{l-1}$$

So a sequence is not wool precisely when all prefix xors are distinct.

Now the problem becomes combinatorial.

There are `2^m` possible xor values.

We already fixed `p_0 = 0`.

To choose `p_1`, we may use any value except `0`, giving:

$$2^m - 1$$

choices.

For `p_2`, we must avoid the two used values:

$$2^m - 2$$

choices.

Continuing this process:

$$(2^m - 1)(2^m - 2)\cdots(2^m - n)$$

This is just a falling factorial.

If `n >= 2^m`, one factor becomes zero, so the answer is zero.

The entire problem reduces to modular multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^{mn} \cdot n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n + \log m)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`.
2. Compute

$$K = 2^m \pmod{10^9+9}$$

using fast modular exponentiation.

1. If `n >= K` in ordinary integer arithmetic, the answer must be zero because we need `n + 1` distinct prefix xor values but only `K` values exist.

Since `2^m` may be huge, we do not compute it directly. We only need to know whether `2^m <= n`.

Because `n ≤ 10^5`, we can safely check:

- if `m >= 17`, then `2^m > 10^5`, so `n < 2^m` automatically
- otherwise compute `1 << m`

1. Initialize `answer = 1`.
2. For every `i` from `1` to `n`, multiply:

$$answer \gets answer \times (K - i)$$

modulo `10^9 + 9`.

This corresponds to choosing a new distinct prefix xor at each step.

1. Print the final answer.

### Why it works

The invariant is that after processing position `i`, the prefix xor values

$$p_0, p_1, \dots, p_i$$

are all distinct.

At step `i`, exactly `i` xor values are already used, so there are:

$$2^m - i$$

valid choices for `p_i`.

Every valid sequence of distinct prefix xors corresponds to exactly one array because:

$$a_i = p_i \oplus p_{i-1}$$

and every array produces exactly one prefix xor sequence.

So counting valid arrays is identical to counting ways to choose distinct prefix xor values step by step.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 9

def solve():
    n, m = map(int, input().split())

    # Check whether 2^m <= n without overflow
    if m < 17 and (1 << m) <= n:
        print(0)
        return

    total = pow(2, m, MOD)

    ans = 1

    for i in range(1, n + 1):
        ans = (ans * (total - i)) % MOD

    print(ans)

solve()
```

The first important detail is the early zero check.

The mathematical condition is:

$$n \ge 2^m$$

but directly computing `2^m` can become unnecessarily large. Since `n` is at most `100000`, any `m >= 17` automatically satisfies:

$$2^m > 100000$$

so the answer cannot become zero from the pigeonhole principle. Only small `m` values need explicit checking.

The variable `total` stores:

$$2^m \bmod MOD$$

which is enough for all later multiplications because every operation is modulo `MOD`.

The loop multiplies:

$$(2^m - 1)(2^m - 2)\cdots(2^m - n)$$

exactly matching the combinatorial derivation.

The subtraction must happen before modulo multiplication. Forgetting parentheses here is a common source of bugs.

## Worked Examples

### Example 1

Input:

```
3 2
```

We have:

$$2^m = 4$$

The computation proceeds as follows.

| Step | Factor | Answer |
| --- | --- | --- |
| Start | - | 1 |
| i = 1 | 4 - 1 = 3 | 3 |
| i = 2 | 4 - 2 = 2 | 6 |
| i = 3 | 4 - 3 = 1 | 6 |

Final answer:

```
6
```

This matches the sample.

The trace demonstrates the core counting idea. At each step we choose a new prefix xor that has not appeared earlier.

### Example 2

Input:

```
2 1
```

Allowed xor values are `{0, 1}`.

We need three distinct prefix xors:

$$p_0, p_1, p_2$$

which is impossible.

| Step | Value |
| --- | --- |
| $2^m$ | 2 |
| Required distinct prefix xors | 3 |
| Possible? | No |

Final answer:

```
0
```

This example demonstrates the pigeonhole principle edge case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + \log m)$ | modular exponentiation plus one loop over `n` |
| Space | $O(1)$ | only a few integer variables are stored |

The loop runs at most `100000` iterations, which is trivial within the time limit. Memory usage is constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 10**9 + 9

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    if m < 17 and (1 << m) <= n:
        print(0)
        return

    total = pow(2, m, MOD)

    ans = 1

    for i in range(1, n + 1):
        ans = (ans * (total - i)) % MOD

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run("3 2\n") == "6", "sample 1"

# minimum input
assert run("1 1\n") == "1", "single nonzero value"

# impossible because n >= 2^m
assert run("2 1\n") == "0", "pigeonhole principle"

# another small manual case
assert run("1 3\n") == "7", "all values except zero"

# boundary where n = 2^m - 1
assert run("3 2\n") == "6", "largest possible nonzero case"

# large m where zero condition should not trigger
res = int(run("100000 100000\n"))
assert 0 <= res < MOD, "large limits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | smallest nontrivial case |
| `2 1` | `0` | impossible distinct-prefix scenario |
| `1 3` | `7` | zero element must be excluded |
| `3 2` | `6` | falling factorial computation |
| `100000 100000` | valid modulo value | performance at maximum limits |

## Edge Cases

Consider:

```
2 1
```

There are only two xor states: `0` and `1`.

The algorithm checks:

$$2^1 = 2$$

Since `n = 2`, we need `3` distinct prefix xors, which is impossible. The early condition returns `0`.

This avoids accidentally computing:

$$(2-1)(2-2)=0$$

through modular arithmetic after many unnecessary operations.

Now consider:

```
1 3
```

Allowed values are `0..7`.

The algorithm computes:

| Step | Factor | Answer |
| --- | --- | --- |
| Start | - | 1 |
| i = 1 | 8 - 1 = 7 | 7 |

The only forbidden array is `(0)` because a single zero already forms a zero-xor subarray.

The algorithm handles this automatically because `p_1` cannot equal `p_0 = 0`.

Finally consider:

```
3 1
```

Here:

$$2^1 = 2$$

but we would need four distinct prefix xors.

The early check immediately returns `0`.

Without that check, a careless implementation might continue multiplying negative values modulo `MOD`, producing a meaningless nonzero answer.
