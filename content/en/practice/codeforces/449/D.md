---
title: "CF 449D - Jzzhu and Numbers"
description: "We are given an array of n non-negative integers. A group is any non-empty subset of array indices. For a chosen group, we take the bitwise AND of all values at those indices. The task is to count how many non-empty groups have bitwise AND equal to 0."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "dp"]
categories: ["algorithms"]
codeforces_contest: 449
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 257 (Div. 1)"
rating: 2400
weight: 449
solve_time_s: 114
verified: true
draft: false
---

[CF 449D - Jzzhu and Numbers](https://codeforces.com/problemset/problem/449/D)

**Rating:** 2400  
**Tags:** bitmasks, combinatorics, dp  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of `n` non-negative integers. A group is any non-empty subset of array indices. For a chosen group, we take the bitwise AND of all values at those indices.

The task is to count how many non-empty groups have bitwise AND equal to `0`. The answer must be reported modulo `1000000007`.

The key detail is that we are choosing indices, not values. If the same number appears multiple times, different index selections count as different groups.

The constraints completely determine the kind of solution we need. The array length can be as large as `10^6`, which immediately rules out anything that examines subsets directly. There are `2^n - 1` non-empty groups, an astronomically large number.

The more interesting constraint is the value range. Every `a[i]` is at most `10^6`, which fits within 20 bits because:

$$2^{20} = 1048576$$

This means every number can be viewed as a mask of at most 20 bits. A state space of size `2^20 ≈ 10^6` is large but manageable. Whenever a problem has huge `n` but small bit width, it is often a signal that we should work in mask space rather than subset space.

Several edge cases are easy to mishandle.

Consider:

```
1
0
```

The only non-empty group is `{0}` and its AND equals `0`, so the answer is `1`. A solution that forgets to exclude the empty subset at the correct moment can produce the wrong count.

Consider:

```
2
1 1
```

The possible groups are `{1}`, `{1}`, and `{1,1}`. Every group's AND equals `1`, never `0`, so the answer is `0`. Counting masks instead of index subsets can accidentally merge duplicate values and undercount or overcount.

Consider:

```
3
0 7 7
```

Any group containing the zero element has AND equal to `0`. There are four such groups:

```
{0}
{0,7(first)}
{0,7(second)}
{0,7(first),7(second)}
```

The correct answer is `4`. This illustrates why index multiplicities matter.

Another subtle situation is when no individual number is zero but some combination produces zero:

```
2
1 2
```

The singleton groups have AND values `1` and `2`, but the pair has:

```
1 & 2 = 0
```

The answer is `1`. Looking only at individual values is insufficient.

## Approaches

The most direct solution is to enumerate every non-empty subset of indices, compute the AND of all selected numbers, and count how many results are zero.

This is correct because it checks exactly the definition of a valid group. Unfortunately, there are `2^n - 1` non-empty groups. Even for `n = 50`, this is already infeasible. With `n = 10^6`, the approach is completely impossible.

To find a better solution, we need to think about what it means for the AND of a subset to contain certain bits.

Suppose we fix a mask `m`. Let us count how many array elements contain all bits of `m`. In other words:

```
(a[i] & m) = m
```

If a subset's AND contains all bits of `m`, then every element in that subset must contain all bits of `m`.

This transforms the problem into counting subsets drawn from numbers that are supersets of a mask.

Let:

```
cnt[m]
```

be the number of array elements whose masks are supersets of `m`.

Then the number of non-empty subsets whose AND contains `m` equals:

```
2^(cnt[m]) - 1
```

because any non-empty selection of those `cnt[m]` elements preserves every bit of `m`.

Now we have a classic inclusion-exclusion situation.

Define:

```
F(m) = number of non-empty subsets whose AND contains m
```

We want:

```
G(0) = number of non-empty subsets whose AND is exactly 0
```

Using Möbius inversion on the subset lattice:

```
G(0) = Σ (-1)^(popcount(m)) * F(m)
```

where the sum runs over all masks.

The remaining challenge is computing `cnt[m]` for every mask. This is exactly the SOS DP (Sum Over Subsets DP) problem. Starting from frequency counts of exact values, we compute for every mask the number of array elements whose values are supersets of that mask.

The entire solution becomes a combination of:

1. Frequency counting of masks.
2. SOS DP to obtain superset counts.
3. Inclusion-exclusion over all masks.

### Approach Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · n) | O(1) | Too slow |
| Optimal | O(20 · 2^20 + n) | O(2^20) | Accepted |

## Algorithm Walkthrough

### 1. Count occurrences of every exact mask

Create an array `freq` of size `2^20`.

For every input number `x`, increment:

```
freq[x]
```

This records how many times each exact mask appears.

### 2. Build superset counts using SOS DP

Create:

```
dp = freq
```

Initially `dp[m]` counts elements equal to `m`.

We want:

```
dp[m] = number of elements whose masks are supersets of m
```

For each bit from `0` to `19`, and for every mask:

If the bit is not set in the mask, add the count of the mask with that bit turned on.

Formally:

```
dp[mask] += dp[mask | (1 << bit)]
```

After all 20 passes, `dp[m]` becomes the number of array elements satisfying:

```
(value & m) = m
```

### 3. Precompute powers of two

For every `i` from `0` to `n` compute:

```
pow2[i] = 2^i mod MOD
```

We will frequently need:

```
2^(dp[m]) - 1
```

which is the number of non-empty subsets formed from those elements.

### 4. Apply inclusion-exclusion

For every mask:

```
ways = 2^(dp[mask]) - 1
```

This counts non-empty subsets whose AND contains all bits of `mask`.

If the mask has an even number of set bits, add `ways`.

If the mask has an odd number of set bits, subtract `ways`.

Mathematically:

```
answer += (-1)^(popcount(mask)) * ways
```

All operations are performed modulo `1000000007`.

### 5. Normalize the result

The inclusion-exclusion sum may become negative during computation.

Return:

```
(answer % MOD + MOD) % MOD
```

### Why it works

After SOS DP, `dp[m]` counts exactly the array elements whose masks contain every bit of `m`. Any non-empty subset chosen from those elements has an AND that also contains every bit of `m`, giving `2^(dp[m]) - 1` subsets.

Each subset whose AND equals some mask `A` contributes to every `F(m)` where `m` is a submask of `A`. Inclusion-exclusion on the Boolean lattice removes overcounting and isolates subsets whose AND is exactly zero. This is precisely the Möbius inversion formula on subset masks, which guarantees the final sum equals the number of groups whose AND is `0`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007
BITS = 20
MAX_MASK = 1 << BITS

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    freq = [0] * MAX_MASK
    for x in arr:
        freq[x] += 1

    dp = freq[:]

    for bit in range(BITS):
        for mask in range(MAX_MASK):
            if (mask & (1 << bit)) == 0:
                dp[mask] += dp[mask | (1 << bit)]

    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    ans = 0

    for mask in range(MAX_MASK):
        ways = pow2[dp[mask]] - 1

        if mask.bit_count() & 1:
            ans -= ways
        else:
            ans += ways

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The first section builds the frequency table of exact masks. Since values never exceed `10^6`, allocating an array of size `2^20` is feasible.

The SOS DP transforms exact frequencies into superset frequencies. When processing a bit, every mask receives contributions from masks that contain one additional required bit. After all 20 dimensions are processed, each state contains the count of array elements that are supersets of that mask.

The power table allows constant time evaluation of `2^k`. Since `k` can be as large as `n`, precomputing once is much faster than repeated exponentiation.

The final loop performs the Möbius inversion. Even parity masks contribute positively and odd parity masks contribute negatively. The resulting sum is exactly the count of non-empty groups whose AND equals zero.

A common implementation mistake is attempting to use inclusion-exclusion on exact frequencies instead of superset counts. The inversion formula only works after computing the SOS DP values.

## Worked Examples

### Sample 1

Input:

```
3
2 3 3
```

The masks are:

```
2 = 10
3 = 11
3 = 11
```

Relevant states:

| Mask | Binary | dp[mask] |
| --- | --- | --- |
| 0 | 00 | 3 |
| 1 | 01 | 2 |
| 2 | 10 | 3 |
| 3 | 11 | 2 |

Now compute contributions:

| Mask | Popcount | 2^(dp)-1 | Sign | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 0 | 7 | + | +7 |
| 1 | 1 | 3 | - | -3 |
| 2 | 1 | 7 | - | -7 |
| 3 | 2 | 3 | + | +3 |

Total:

```
7 - 3 - 7 + 3 = 0
```

Answer:

```
0
```

This demonstrates that every non-empty subset has a positive AND value, so inclusion-exclusion cancels everything.

### Example 2

Input:

```
2
1 2
```

Masks:

```
1 = 01
2 = 10
```

SOS results:

| Mask | Binary | dp[mask] |
| --- | --- | --- |
| 0 | 00 | 2 |
| 1 | 01 | 1 |
| 2 | 10 | 1 |
| 3 | 11 | 0 |

Contributions:

| Mask | Popcount | 2^(dp)-1 | Sign | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 0 | 3 | + | +3 |
| 1 | 1 | 1 | - | -1 |
| 2 | 1 | 1 | - | -1 |
| 3 | 2 | 0 | + | 0 |

Total:

```
3 - 1 - 1 = 1
```

The only valid subset is:

```
{1, 2}
```

whose AND equals zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + 20 · 2^20) | Frequency counting plus SOS DP and inclusion-exclusion |
| Space | O(2^20) | Frequency and DP arrays |

The dominant cost is the SOS DP. There are 20 bit positions and `2^20` masks, yielding roughly twenty million transitions. This comfortably fits within typical Codeforces limits in optimized Python. Memory usage is also acceptable because arrays of size about one million are well within the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

MOD = 1000000007

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    arr = list(map(int, input().split()))

    BITS = 20
    MAX_MASK = 1 << BITS

    freq = [0] * MAX_MASK
    for x in arr:
        freq[x] += 1

    dp = freq[:]

    for bit in range(BITS):
        for mask in range(MAX_MASK):
            if (mask & (1 << bit)) == 0:
                dp[mask] += dp[mask | (1 << bit)]

    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    ans = 0
    for mask in range(MAX_MASK):
        ways = pow2[dp[mask]] - 1
        if mask.bit_count() & 1:
            ans -= ways
        else:
            ans += ways

    return str(ans % MOD)

# provided sample
assert run("3\n2 3 3\n") == "0", "sample 1"

# single zero
assert run("1\n0\n") == "1", "single element equal to zero"

# single non-zero
assert run("1\n5\n") == "0", "single non-zero element"

# pair whose AND becomes zero
assert run("2\n1 2\n") == "1", "only the pair works"

# all zeros
assert run("3\n0 0 0\n") == "7", "every non-empty subset works"

# duplicate values
assert run("2\n1 1\n") == "0", "duplicates with non-zero AND"

# mixed case
assert run("3\n0 7 7\n") == "4", "all subsets containing zero"
```

### Test Summary

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `1` | Smallest valid positive answer |
| `1 / 5` | `0` | Single non-zero element |
| `2 / 1 2` | `1` | AND becomes zero only after combining |
| `3 / 0 0 0` | `7` | Every non-empty subset valid |
| `2 / 1 1` | `0` | Duplicate values handled by indices |
| `3 / 0 7 7` | `4` | Correct counting with repeated values and zero |

## Edge Cases

### A single zero

Input:

```
1
0
```

The SOS DP gives:

```
dp[0] = 1
```

All other masks have count zero. Inclusion-exclusion evaluates to:

```
2^1 - 1 = 1
```

The algorithm outputs `1`, corresponding to the only possible group.

### Duplicate values

Input:

```
2
1 1
```

There are three non-empty groups:

```
{first}
{second}
{first, second}
```

Every group's AND equals `1`. The frequency table stores multiplicity, so the SOS DP counts both occurrences separately. Inclusion-exclusion ultimately produces `0`, which is correct.

### Zero produced only by combining elements

Input:

```
2
1 2
```

Neither singleton group has AND equal to zero:

```
1
2
```

The pair gives:

```
1 & 2 = 0
```

The algorithm counts subsets through superset frequencies rather than checking individual values. Inclusion-exclusion isolates exactly one subset whose AND equals zero, producing the correct answer `1`.

### All elements are zero

Input:

```
3
0 0 0
```

Every non-empty subset has AND equal to zero. There are:

```
2^3 - 1 = 7
```

such subsets. Since every value already equals zero, `dp[0] = 3` and all other masks have count zero. The inclusion-exclusion sum evaluates to `7`, matching the combinatorial count exactly.
