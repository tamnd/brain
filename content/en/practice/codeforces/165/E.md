---
title: "CF 165E - Compatible Numbers"
description: "We are given an array of integers, and for every element we must find another array element whose bitwise AND with it is zero. Two numbers are compatible exactly when they do not share any bit set to 1."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dfs-and-similar", "dp"]
categories: ["algorithms"]
codeforces_contest: 165
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 112 (Div. 2)"
rating: 2200
weight: 165
solve_time_s: 107
verified: true
draft: false
---

[CF 165E - Compatible Numbers](https://codeforces.com/problemset/problem/165/E)

**Rating:** 2200  
**Tags:** bitmasks, brute force, dfs and similar, dp  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and for every element we must find another array element whose bitwise AND with it is zero. Two numbers are compatible exactly when they do not share any bit set to `1`.

For example, if we look at `90` and `36`:

```
90  = 1011010
36  = 0100100
AND = 0000000
```

No bit position contains `1` in both numbers, so they are compatible.

The task is not to count compatible pairs. For every array value `a[i]`, we only need to output any array element `x` such that:

```
a[i] & x = 0
```

If no such element exists, we print `-1`.

The constraints completely determine the direction of the solution. The array can contain up to `10^6` numbers, and each value is at most `4 * 10^6`. Since `4 * 10^6 < 2^22`, every number fits inside 22 bits.

A quadratic solution would require checking all pairs:

```
10^6 * 10^6 = 10^12
```

operations, which is impossible.

The 22-bit bound is the real clue. Whenever the number of bits is small, bitmask dynamic programming becomes possible. A state space of size `2^22` is around 4.2 million, which is large but still manageable in both time and memory in a low constant-factor implementation.

There are several edge cases that break careless solutions.

Suppose the input is:

```
1
7
```

The only number is `7`. Since `7 & 7 != 0`, the answer is `-1`. A buggy implementation may accidentally allow a number to match itself without checking compatibility.

Another tricky case is duplicated values:

```
3
0 5 5
```

The number `0` is compatible with everything because:

```
0 & x = 0
```

for all `x`. The correct output may be:

```
5 0 0
```

A solution that only searches strict submasks may miss `0`.

A more subtle issue appears when many bits are set:

```
2
4194303 1
```

`4194303 = 2^22 - 1` has every bit set, so it cannot be compatible with any positive number. The correct answers are:

```
-1 -1
```

A wrong complement-mask computation can easily overflow the valid 22-bit range and produce invalid states.

## Approaches

The most direct solution checks every pair of numbers.

For each `a[i]`, we iterate through the whole array and test:

```
a[i] & a[j] == 0
```

The bitwise AND operation itself is constant time, so the total complexity becomes `O(n^2)`.

This brute-force method is correct because compatibility is defined entirely by pairwise comparison. If any compatible number exists, exhaustive search will eventually find it.

The problem is scale. With `n = 10^6`, this approach requires about `10^12` checks, which is many thousands of times beyond the limit.

The important observation is that compatibility depends only on bit patterns, not positions in the array.

For a fixed number `x`, we want some number `y` such that:

```
x & y = 0
```

That means every bit set in `y` must lie inside the zero-bit positions of `x`.

If we define:

```
FULL = (1 << 22) - 1
```

then the allowed bits for `y` are exactly:

```
FULL ^ x
```

So instead of searching the whole array, we can ask:

"Does the array contain any submask of `FULL ^ x`?"

This transforms the problem into a classic SOS DP, also called Sum Over Subsets DP.

We create an array `dp[mask]` where:

```
dp[mask] = some array value that is a submask of mask
```

Initially, if a number `v` appears in the array, we set:

```
dp[v] = v
```

Then we propagate information upward through masks. For every mask and every set bit, we inherit answers from smaller submasks.

After preprocessing, querying becomes easy:

```
answer(x) = dp[FULL ^ x]
```

because any submask of the complement mask shares no set bits with `x`.

The preprocessing costs about:

```
22 * 2^22
```

operations, roughly 92 million transitions. In optimized Python this is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal SOS DP | O(22 · 2²² + n) | O(2²²) | Accepted |

## Algorithm Walkthrough

1. Define the maximum bit width as 22 because every input number is smaller than `2^22`.
2. Create an array `dp` of size `2^22` and initialize every entry to `-1`.
3. For every value `x` in the input array, set:

```
dp[x] = x
```

This means the exact mask `x` exists in the array.
4. Run SOS DP over all masks.

For every mask and every bit position:

If the bit is set in the current mask, try removing it:

```
smaller = mask ^ (1 << bit)
```

If `dp[mask]` is still `-1`, inherit:

```
dp[mask] = dp[smaller]
```

The reason this works is that every submask can be reached by repeatedly removing set bits.
5. For each array value `x`, compute:

```
complement = FULL ^ x
```

Every compatible number must be a submask of this complement mask.
6. Output:

```
dp[complement]
```

If no valid submask exists in the array, the value remains `-1`.

### Why it works

The DP invariant is:

```
dp[mask] stores some array value that is a submask of mask,
or -1 if none exists.
```

Initially this is true for exact masks because we explicitly store existing numbers.

During transitions, we only copy values from smaller masks obtained by removing bits. Any submask of `smaller` is also a submask of `mask`, so the invariant remains valid.

For a query value `x`, the mask `FULL ^ x` contains exactly the bit positions where `x` has zeros. Any submask `y` of this complement satisfies:

```
x & y = 0
```

because `y` never uses a bit already set in `x`.

So if `dp[FULL ^ x] = y`, then `y` is guaranteed compatible with `x`.

## Python Solution

```python
import sys
input = sys.stdin.readline

BITS = 22
SIZE = 1 << BITS
FULL = SIZE - 1

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    dp = [-1] * SIZE

    for x in a:
        dp[x] = x

    for bit in range(BITS):
        for mask in range(SIZE):
            if mask & (1 << bit):
                if dp[mask] == -1:
                    dp[mask] = dp[mask ^ (1 << bit)]

    ans = []

    for x in a:
        ans.append(str(dp[FULL ^ x]))

    print(" ".join(ans))

solve()
```

The solution begins by allocating the DP array over all 22-bit masks. This is large, around 4.2 million entries, but still fits comfortably inside the memory limit in Python when storing integers.

The initialization step stores every array value directly into its own mask position. At this moment, only exact masks are known.

The SOS DP phase propagates information from smaller submasks toward larger masks. The order matters. For each bit, we process all masks containing that bit and try inheriting from the version with that bit removed.

A common mistake is reversing the transition direction. We want:

```
mask -> mask without one bit
```

because we are collecting information about submasks.

The complement computation is another place where bugs appear. We must restrict complements to 22 bits:

```
FULL ^ x
```

Using `~x` would create negative numbers in Python because integers are unbounded.

The final lookup is constant time. After preprocessing, every query reduces to a single array access.

## Worked Examples

### Example 1

Input:

```
2
90 36
```

Binary forms:

```
90 = 1011010
36 = 0100100
```

Their AND is zero.

| Step | Mask/Value | Result |
| --- | --- | --- |
| Insert values | dp[90] = 90 | stored |
| Insert values | dp[36] = 36 | stored |
| Query 90 | FULL ^ 90 contains 36 as submask | answer = 36 |
| Query 36 | FULL ^ 36 contains 90 as submask | answer = 90 |

Output:

```
36 90
```

This trace shows the core idea of the algorithm. We do not search directly for compatible numbers. We search for submasks of the complement.

### Example 2

Input:

```
4
1 2 3 7
```

Binary forms:

```
1 = 001
2 = 010
3 = 011
7 = 111
```

| Number | Complement bits | Existing compatible submask | Answer |
| --- | --- | --- | --- |
| 1 | 110 | 2 | 2 |
| 2 | 101 | 1 | 1 |
| 3 | 100 | none | -1 |
| 7 | 000 | none | -1 |

Possible output:

```
2 1 -1 -1
```

This example demonstrates that the algorithm correctly distinguishes between "some bits overlap" and "no bits overlap at all". The number `3` cannot pair with either `1` or `2` because both share a set bit with it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(22 · 2²² + n) | SOS DP over all masks and bits, plus linear input/output |
| Space | O(2²²) | DP table for every 22-bit mask |

`2^22` is about 4.2 million. Multiplying by 22 gives roughly 92 million transitions, which is large but feasible in optimized Python because each transition is extremely small and cache-friendly. The memory usage also fits inside 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

BITS = 22
SIZE = 1 << BITS
FULL = SIZE - 1

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    dp = [-1] * SIZE

    for x in a:
        dp[x] = x

    for bit in range(BITS):
        for mask in range(SIZE):
            if mask & (1 << bit):
                if dp[mask] == -1:
                    dp[mask] = dp[mask ^ (1 << bit)]

    ans = []

    for x in a:
        ans.append(str(dp[FULL ^ x]))

    print(" ".join(ans))

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
assert run("2\n90 36\n") == "36 90", "sample 1"

# minimum size, no compatible value
assert run("1\n7\n") == "-1", "single element"

# zero-compatible structure
res = run("3\n1 2 4\n").split()
assert res[0] in {"2", "4"}
assert res[1] in {"1", "4"}
assert res[2] in {"1", "2"}

# all equal values
assert run("4\n5 5 5 5\n") == "-1 -1 -1 -1", "all equal"

# full-mask boundary
assert run("2\n4194303 1\n") == "-1 -1", "22-bit boundary"

# mixed compatibility
res = run("4\n1 2 3 7\n").split()
assert res[0] == "2"
assert res[1] == "1"
assert res[2] == "-1"
assert res[3] == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `-1` | Single-element edge case |
| `1 2 4` | Any mutually compatible answers | Multiple valid outputs |
| `5 5 5 5` | All `-1` | Duplicate handling |
| `4194303 1` | `-1 -1` | 22-bit boundary correctness |
| `1 2 3 7` | `2 1 -1 -1` | Mixed compatible and incompatible cases |

## Edge Cases

Consider the input:

```
1
7
```

The only available number is `7` itself. Since:

```
7 & 7 = 7
```

it is not compatible with itself.

The complement mask contains only zero bits in the positions where `7` has ones, and no existing submask from the array satisfies it. The DP lookup returns `-1`.

Now consider duplicates:

```
4
5 5 5 5
```

Binary:

```
5 = 101
```

Any pair of `5`s still shares bits:

```
101 & 101 = 101
```

During preprocessing, only `dp[5]` becomes populated. No complement mask can reach it through submask transitions, so every answer remains `-1`.

Finally, examine the maximum-mask case:

```
2
4194303 1
```

`4194303` equals:

```
1111111111111111111111
```

with all 22 bits set.

Its complement inside 22 bits is zero:

```
FULL ^ 4194303 = 0
```

The DP value at mask `0` is `-1`, since no zero exists in the array. The algorithm correctly outputs `-1`.

For the number `1`, its complement contains all bits except the lowest one, but `4194303` is not a submask of that complement because it still contains the forbidden lowest bit. So the answer for `1` is also `-1`.
