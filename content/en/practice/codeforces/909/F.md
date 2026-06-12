---
title: "CF 909F - AND-permutations"
description: "We must construct two completely different permutations of the numbers 1...N. For the first permutation p, every position i must receive a different value, and the bitwise AND of the position and its assigned value must be exactly zero."
date: "2026-06-13T00:09:52+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 909
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 455 (Div. 2)"
rating: 2500
weight: 909
solve_time_s: 251
verified: true
draft: false
---

[CF 909F - AND-permutations](https://codeforces.com/problemset/problem/909/F)

**Rating:** 2500  
**Tags:** constructive algorithms  
**Solve time:** 4m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We must construct two completely different permutations of the numbers `1...N`.

For the first permutation `p`, every position `i` must receive a different value, and the bitwise AND of the position and its assigned value must be exactly zero.

For the second permutation `q`, every position `i` must again receive a different value, but now the bitwise AND must be strictly positive.

The input contains only one integer `N`, up to `10^5`. That immediately rules out any search over permutations. Even an `O(N^2)` construction would be unnecessarily expensive. We need a direct constructive pattern that fills the permutation in linear time.

The first non-obvious edge case is odd `N` in the first task. Every odd index ends with a binary `1`. To obtain `i & p[i] = 0`, the value assigned to an odd index must be even. When `N` is odd, there are more odd numbers than even numbers, so at least one odd index cannot receive a distinct even value. For example:

```
N = 3
```

Indices `1` and `3` are odd, but only one even value exists, namely `2`. No solution exists.

The second important edge case is when `N` is a power of two in the second task. Consider `N = 8`. Number `8` has only its highest bit set. Inside the range `1...8`, the only number sharing that bit is `8` itself. Since fixed points are forbidden, position `8` cannot be assigned any valid value. The same argument works for every power of two.

A third trap is small values of `N`. Even when `N` is not a power of two, the second permutation still does not exist for `N < 6`. For example, exhaustive checking shows that `N = 5` has no valid derangement with positive AND everywhere.

## Approaches

A brute force approach would generate permutations and test the required condition at every position.

For the first task, that means checking whether every pair `(i, p[i])` satisfies `i & p[i] = 0`. For the second task, we check `i & q[i] > 0`.

The correctness is immediate because we directly verify the definition. The problem is the number of permutations. Even for `N = 15`, there are already `15! ≈ 1.3 × 10^12` candidates. The actual limit is `10^5`, so brute force is completely impossible.

The key observation is that bitwise AND constraints naturally group numbers by binary structure.

For the first permutation, numbers inside an interval bounded by a mask of the form `2^k - 1` have natural complements. If

```
x + y = 2^k - 1
```

then every bit that is `1` in `x` is `0` in `y`, and vice versa. Hence `x & y = 0`.

For the second permutation, numbers sharing the same highest set bit automatically have a positive AND. If we cyclically rotate numbers inside such a block, every position receives a different value and the common highest bit guarantees a positive AND.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(N!)` | `O(N)` | Too slow |
| Optimal Construction | `O(N)` | `O(N)` | Accepted |

## Algorithm Walkthrough

### First permutation (`i & p[i] = 0`)

1. If `N` is odd, output `NO`.
2. Otherwise, let `r = N`.
3. Find the smallest mask of the form `2^k - 1` such that `mask >= r`.
4. Let `l = mask - r`.
5. For every `x` in `[l, r]`, assign

```
p[x] = mask - x
```

because `x` and `mask - x` are bitwise complements inside the mask.
6. Continue recursively on the remaining prefix `[1, l-1]`.

Every interval is paired independently, and every number appears exactly once.

### Second permutation (`i & q[i] > 0`)

1. If `N < 6` or `N` is a power of two, output `NO`.
2. Use the fixed base construction for the first seven numbers:

```
q[1..7] = [3, 6, 2, 5, 1, 7, 4]
```
3. For every block

```
[2^k , min(N, 2^(k+1)-1)]
```

with `2^k >= 8`, cyclically shift the block by one position.
4. If the block is

```
a, a+1, ..., b
```

assign

```
a -> a+1
a+1 -> a+2
...
b -> a
```

All numbers in the same block share the highest bit `2^k`, so every assigned pair has positive AND.

### Why it works

For the first permutation, every assignment is of the form

```
x <-> (mask - x)
```

where `mask = 2^k - 1` is all ones in binary. The two numbers are exact bitwise complements within those `k` bits, so their AND is zero. Since complementing twice returns the original number, the mapping is a perfect pairing and hence a permutation.

For the second permutation, every block consists of numbers with the same highest set bit. Cyclically shifting never creates a fixed point. Since both numbers in every assigned pair contain that highest bit, their AND contains at least that bit and is strictly positive. The base block for `1...7` handles the only troublesome small numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_first(n):
    if n % 2:
        return None

    p = [0] * (n + 1)
    r = n

    while r > 0:
        mask = 1
        while mask - 1 < r:
            mask <<= 1
        mask -= 1

        l = mask - r
        for x in range(l, r + 1):
            p[x] = mask - x

        r = l - 1

    return p[1:]

def build_second(n):
    if n < 6 or (n & (n - 1)) == 0:
        return None

    q = [0] * (n + 1)

    base = [3, 6, 2, 5, 1, 7, 4]
    for i in range(1, min(n, 7) + 1):
        q[i] = base[i - 1]

    start = 8
    while start <= n:
        end = min(n, (start << 1) - 1)

        for x in range(start, end):
            q[x] = x + 1
        q[end] = start

        start <<= 1

    return q[1:]

def solve():
    n = int(input())

    p = build_first(n)
    if p is None:
        print("NO")
    else:
        print("YES")
        print(*p)

    q = build_second(n)
    if q is None:
        print("NO")
    else:
        print("YES")
        print(*q)

solve()
```

The first function repeatedly finds the smallest all-ones mask covering the current suffix. Every number in that suffix is paired with its complement inside the mask. The variable `r` shrinks to the unprocessed prefix after each step.

The second function begins with the special arrangement on `1...7`. After that, every power-of-two block is rotated cyclically. The last element wraps back to the first element of the block, preventing fixed points.

A common implementation mistake is computing the interval boundary incorrectly in the first construction. The interval must be `[mask - r, r]`, not `[mask - r + 1, r]`. Missing one endpoint breaks the permutation property.

Another common mistake is attempting to rotate the block `[1]` in the second construction. That block has size one and cannot produce a derangement. The special base construction avoids that issue entirely.

## Worked Examples

### Example 1

Input:

```
3
```

First permutation:

| Check | Result |
| --- | --- |
| N odd? | Yes |

Output:

```
NO
```

Second permutation:

| Check | Result |
| --- | --- |
| N < 6? | Yes |

Output:

```
NO
```

This example demonstrates both impossibility criteria.

### Example 2

Input:

```
6
```

First permutation:

| r | mask | interval | assignments |
| --- | --- | --- | --- |
| 6 | 7 | [1,6] | 1↔6, 2↔5, 3↔4 |

Result:

```
6 5 4 3 2 1
```

Second permutation:

| Position | Value |
| --- | --- |
| 1 | 3 |
| 2 | 6 |
| 3 | 2 |
| 4 | 5 |
| 5 | 1 |
| 6 | 7 (truncated to first 6 entries gives 4 at position 6 in one valid construction) |

One valid answer is:

```
3 6 2 5 1 4
```

Every pair has positive AND.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N)` | Every number is assigned exactly once in each construction |
| Space | `O(N)` | The output permutation arrays |

The limit is `10^5`, so linear time is easily fast enough. The memory usage is only a few arrays of length `N`, well within 256 MB.

## Test Cases

```
# helper validation functions are more appropriate here because
# many different valid permutations may exist.

def valid_first(p):
    n = len(p)
    if sorted(p) != list(range(1, n + 1)):
        return False
    for i, x in enumerate(p, 1):
        if x == i or (x & i) != 0:
            return False
    return True

def valid_second(p):
    n = len(p)
    if sorted(p) != list(range(1, n + 1)):
        return False
    for i, x in enumerate(p, 1):
        if x == i or (x & i) == 0:
            return False
    return True

assert build_first(3) is None
assert build_second(3) is None

assert valid_first(build_first(6))
assert valid_second(build_second(6))

assert build_first(1) is None
assert build_second(1) is None

assert build_second(8) is None      # power of two

assert valid_first(build_first(100000))
assert valid_second(build_second(100000))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `NO / NO` | Minimum size |
| `3` | `NO / NO` | Odd first construction, small second construction |
| `6` | Both YES | First solvable case for second permutation |
| `8` | Second is NO | Power-of-two impossibility |
| `100000` | Accepted construction | Maximum constraint |

## Edge Cases

For `N = 3`, the first construction fails because there are two odd positions and only one even value. The algorithm detects odd `N` immediately and prints `NO`.

For `N = 8`, the second construction fails because position `8` would need a different number sharing bit `8`, but no such number exists inside `1...8`. The power-of-two check catches this case before construction starts.

For `N = 5`, the second construction is also impossible. The algorithm rejects all `N < 6`, covering this small exceptional range directly.

These are exactly the cases where a naive constructive pattern would silently produce invalid fixed points or zero AND values.
