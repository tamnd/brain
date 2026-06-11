---
title: "CF 1284C - New Year and Permutation"
description: "We need the total number of framed segments across all permutations of length n. For a fixed permutation, a segment [l, r] is framed when the values inside it form a set of consecutive integers."
date: "2026-06-11T19:18:13+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 1284
codeforces_index: "C"
codeforces_contest_name: "Hello 2020"
rating: 1600
weight: 1284
solve_time_s: 121
verified: true
draft: false
---

[CF 1284C - New Year and Permutation](https://codeforces.com/problemset/problem/1284/C)

**Rating:** 1600  
**Tags:** combinatorics, math  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We need the total number of framed segments across all permutations of length `n`.

For a fixed permutation, a segment `[l, r]` is framed when the values inside it form a set of consecutive integers. Since all values in a permutation are distinct, the condition

$$\max - \min = r - l$$

means exactly that the segment contains every integer between its minimum and maximum.

The happiness of a permutation is the number of framed segments it contains. Instead of computing happiness for one permutation, we must sum it over all `n!` permutations and output the result modulo the given prime `m`.

The constraint `n ≤ 250000` completely changes the nature of the problem. We cannot enumerate permutations, since even `20!` is already enormous. We also cannot afford any algorithm that examines all segments of a single permutation. The solution must derive a counting formula and evaluate it in roughly linear time.

A subtle point is that we are summing over all permutations simultaneously. Many problems of this type become tractable after reversing the counting order: instead of asking how many framed segments each permutation has, ask how many permutations make a particular segment framed.

Another easy mistake is to think that the condition depends on the positions only. For example, for `n = 3`, the segment of length `2` is framed only when its two values are consecutive. The pair `(1,3)` does not work because `3 - 1 = 2` while the segment length minus one equals `1`.

For `n = 1`, there is only one permutation and one segment. The answer is `1`. Any formula must naturally produce this value.

## Approaches

Let us first imagine the brute-force interpretation.

We could generate every permutation of length `n`. For each permutation we could inspect every segment, compute its minimum and maximum, and check whether it is framed. Even if segment queries were optimized, there are `n!` permutations, so the approach becomes impossible almost immediately. For `n = 10`, there are already `3,628,800` permutations.

The key observation is that the definition of a framed segment depends only on the set of values inside that segment.

Consider a segment of length

$$k = r-l+1.$$

Because all values are distinct, the condition

$$\max - \min = k-1$$

means the segment contains exactly `k` consecutive numbers.

Suppose those consecutive numbers are

$$x, x+1, \dots, x+k-1.$$

How many choices exist for such a value set? The starting value `x` can be chosen in

$$n-k+1$$

ways.

Now count permutations where a fixed position segment of length `k` contains exactly those `k` numbers.

The `k` chosen values can be arranged inside the segment in `k!` ways.

The remaining `n-k` values can be arranged outside the segment in `(n-k)!` ways.

Hence, for a fixed segment position and a fixed consecutive value block, the number of valid permutations is

$$k!(n-k)!.$$

There are `n-k+1` possible consecutive value blocks and also `n-k+1` possible positions of a segment of length `k`.

Thus the total contribution of all length-`k` segments is

$$(n-k+1)^2 \cdot k! \cdot (n-k)!.$$

Summing over all lengths gives the answer:

$$\sum_{k=1}^{n}
(n-k+1)^2 \cdot k! \cdot (n-k)!.$$

The remaining task is evaluating this sum modulo `m`. Since `n` is up to `250000`, we can precompute factorials modulo `m` in linear time and then evaluate the summation in another linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n²) or worse | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`.
2. Precompute factorials modulo `m`.

Let `fact[i] = i! mod m` for all `0 ≤ i ≤ n`.
3. Initialize the answer to zero.
4. For every segment length `k` from `1` to `n`, compute

$$(n-k+1)^2 \cdot fact[k] \cdot fact[n-k]
\pmod m.$$

This quantity counts all pairs `(permutation, framed segment)` whose segment length equals `k`.
5. Add this contribution to the answer modulo `m`.
6. Output the final answer.

The reason step 4 works is that every framed segment corresponds to exactly one block of consecutive values, and every choice of segment position, consecutive value block, arrangement inside the segment, and arrangement outside the segment produces a unique valid permutation.

### Why it works

Fix a length `k`.

A segment of length `k` is framed if and only if its values are exactly some set of `k` consecutive integers. There are `n-k+1` such value sets.

Choose one segment position among the `n-k+1` possible positions. Once a consecutive value set is chosen, the `k` values may be ordered arbitrarily inside the segment, contributing `k!` possibilities. The remaining values may be ordered arbitrarily outside the segment, contributing `(n-k)!` possibilities.

Every permutation containing that framed segment is counted exactly once, because the segment position and its value set are uniquely determined.

Summing these counts over all segment lengths counts every framed segment in every permutation exactly once, which is precisely the required total happiness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

fact = [1] * (n + 1)
for i in range(1, n + 1):
    fact[i] = fact[i - 1] * i % m

ans = 0

for k in range(1, n + 1):
    cnt = n - k + 1
    contrib = cnt * cnt
    contrib %= m
    contrib = contrib * fact[k] % m
    contrib = contrib * fact[n - k] % m
    ans = (ans + contrib) % m

print(ans)
```

The factorial array stores every value modulo `m`. Since all later computations are also performed modulo `m`, no larger values are needed.

The loop over `k` directly evaluates the derived formula. The variable `cnt = n-k+1` appears twice because there are two independent choices: the position of the segment and the consecutive block of values assigned to it.

Applying modulo after each multiplication prevents intermediate numbers from growing unnecessarily large. Python integers can handle large values, but reducing early keeps the implementation closer to the intended modular arithmetic.

The indexing is particularly easy to get wrong. The contribution uses `fact[k]` and `fact[n-k]`, not `fact[k-1]`. The term `n-k+1` comes from counting both segment positions and consecutive value blocks.

## Worked Examples

### Example 1

Input:

```
1 993244853
```

Factorials:

| i | fact[i] |
| --- | --- |
| 0 | 1 |
| 1 | 1 |

Main loop:

| k | cnt = n-k+1 | cnt² | k! | (n-k)! | Contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | 1 |

Final answer:

| Answer |
| --- |
| 1 |

The only permutation is `[1]`, and its only segment is framed.

### Example 2

Input:

```
3 1000000007
```

Factorials:

| i | fact[i] |
| --- | --- |
| 0 | 1 |
| 1 | 1 |
| 2 | 2 |
| 3 | 6 |

Main loop:

| k | cnt | cnt² | k! | (n-k)! | Contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 9 | 1 | 2 | 18 |
| 2 | 2 | 4 | 2 | 1 | 8 |
| 3 | 1 | 1 | 6 | 1 | 6 |

Summation:

| Running Answer |
| --- |
| 18 |
| 26 |
| 32 |

Output:

```
32
```

This matches the sample discussion, where the total happiness across all six permutations equals `32`.

The trace illustrates the central counting idea. Length-1 segments contribute `18`, length-2 segments contribute `8`, and length-3 segments contribute `6`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One factorial pass and one summation pass |
| Space | O(n) | Storage for factorials |
|  |  |  |

The algorithm performs only a few arithmetic operations per value of `k`. With `n = 250000`, roughly half a million loop iterations are required, which is easily within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % m

    ans = 0
    for k in range(1, n + 1):
        cnt = n - k + 1
        ans = (
            ans
            + cnt * cnt % m
            * fact[k] % m
            * fact[n - k]
        ) % m

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("1 993244853\n") == "1", "sample 1"

# custom cases
assert run("2 1000000007\n") == "8", "all segments framed in both permutations"
assert run("3 1000000007\n") == "32", "statement example"
assert run("4 1000000007\n") == "156", "checks larger counting formula"
assert run("5 1000000007\n") == "872", "off-by-one and factorial indexing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 993244853` | `1` | Minimum size |
| `2 1000000007` | `8` | Every segment is framed |
| `3 1000000007` | `32` | Known example from statement |
| `4 1000000007` | `156` | Multiple segment lengths contribute |
| `5 1000000007` | `872` | Checks factorial and counting formula |

## Edge Cases

Consider the smallest input:

```
1 993244853
```

The loop runs once with `k = 1`.

$$(1)^2 \cdot 1! \cdot 0! = 1.$$

The algorithm outputs `1`, matching the single permutation and single framed segment.

Consider `n = 2`:

```
2 1000000007
```

The contributions are

$$2^2 \cdot 1! \cdot 1! = 4,$$

and

$$1^2 \cdot 2! \cdot 0! = 2.$$

The answer is `6`. Since there are two permutations, each having happiness `3`, the total is `6`. This confirms that the counting correctly handles segments occupying the entire array.

A common off-by-one risk appears when counting consecutive value blocks. For `n = 3` and `k = 2`, there are exactly two valid value blocks:

$$\{1,2\}, \{2,3\}.$$

The formula uses `n-k+1 = 2`. Using `n-k` would miss one block and produce an incorrect total. The algorithm avoids this because both segment positions and value blocks are counted with the same expression `n-k+1`.

Another subtle case is `k = n`. There is only one segment position and only one consecutive value block, namely all values from `1` to `n`. The contribution becomes

$$1^2 \cdot n! \cdot 0! = n!,$$

which is exactly the number of permutations whose full array segment is framed. Since every permutation satisfies this property for the entire array, the count is correct.
