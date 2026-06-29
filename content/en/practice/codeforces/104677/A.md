---
title: "CF 104677A - Pizza"
description: "The task describes a simple division scenario. A person has a fixed number of pizza slices and a group of friends. The slices are distributed as evenly as possible among all friends, and anything that cannot be evenly distributed remains unused."
date: "2026-06-29T09:11:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104677
codeforces_index: "A"
codeforces_contest_name: "Sugar Sweet \u2764\ufe0f"
rating: 0
weight: 104677
solve_time_s: 56
verified: true
draft: false
---

[CF 104677A - Pizza](https://codeforces.com/problemset/problem/104677/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a simple division scenario. A person has a fixed number of pizza slices and a group of friends. The slices are distributed as evenly as possible among all friends, and anything that cannot be evenly distributed remains unused.

The input consists of two integers, where the first represents how many pizza slices are available and the second represents how many friends will share them. The output must describe two quantities. The first is how many slices each friend receives after an equal split, and the second is how many slices remain undistributed.

The constraints go up to 10^9 for both values, which immediately signals that any approach simulating distribution slice by slice would be too slow. A loop over up to 10^9 iterations would not finish in time under a 1 second limit. The solution must compute the result in constant time using arithmetic operations.

A subtle edge case appears when the number of slices is smaller than the number of friends. For example, if there are 2 slices and 5 friends, each friend gets zero slices and all slices remain unused. Another corner case is when slices divide evenly, such as 9 slices among 3 friends, where nothing is left over. Both cases must be handled correctly without special branching beyond integer arithmetic.

## Approaches

A direct simulation approach would assign one slice at a time in round-robin fashion among friends. This would keep distributing until no slices remain. While conceptually straightforward, its worst case requires iterating once per slice, leading to up to 10^9 operations, which is far beyond feasible limits.

The key observation is that the distribution is purely uniform. Every friend receives exactly the integer part of dividing total slices by the number of friends. Any remainder is what cannot be evenly assigned. This transforms the process from repeated simulation into a single arithmetic division.

The brute-force works because it explicitly models the distribution process, but it fails when the number of slices becomes large. The observation that only the quotient and remainder matter reduces the problem to integer division and modulo operations, both computable in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(x) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read two integers, the number of slices and the number of friends. These represent the total resource and the number of equal partitions we want to form.
2. Compute how many slices each friend receives using integer division. This captures the largest equal allocation possible without exceeding the available slices.
3. Compute the leftover slices using the modulo operation. This directly represents the remainder after equal distribution.
4. Output the quotient and remainder as the final result.

The reasoning behind each step is tied to the mathematical structure of division. Integer division naturally encodes equal splitting, and modulo captures what cannot be evenly split.

### Why it works

The invariant is that after distributing `x` slices equally among `N` friends, the total assigned slices must be the largest multiple of `N` that does not exceed `x`. Integer division produces exactly this multiple when multiplied back by `N`. The remainder is whatever is left after subtracting this maximum divisible portion, which is precisely what modulo computes. Since both operations are exact decompositions of the original number, the result cannot deviate from a correct distribution.

## Python Solution

```python
import sys
input = sys.stdin.readline

x, n = map(int, input().split())

each = x // n
leftover = x % n

print(each, leftover)
```

The solution reads the input once and immediately performs two arithmetic operations. The integer division operator `//` ensures that fractional parts are discarded, which matches the idea of only distributing whole slices. The modulo operator `%` computes what remains after this allocation.

No loops or conditional branches are needed because the arithmetic fully encodes the distribution logic. The order of operations is straightforward, and there are no boundary issues beyond ensuring integer arithmetic, which Python handles naturally for large values.

## Worked Examples

### Example 1

Input:

```
5 2
```

| Step | x | N | each = x // N | leftover = x % N |
| --- | --- | --- | --- | --- |
| Start | 5 | 2 | - | - |
| Compute division | 5 | 2 | 2 | - |
| Compute remainder | 5 | 2 | 2 | 1 |

Output:

```
2 1
```

This shows that each friend receives two slices, and one slice remains unused because 5 is not fully divisible by 2.

### Example 2

Input:

```
9 3
```

| Step | x | N | each = x // N | leftover = x % N |
| --- | --- | --- | --- | --- |
| Start | 9 | 3 | - | - |
| Compute division | 9 | 3 | 3 | - |
| Compute remainder | 9 | 3 | 3 | 0 |

Output:

```
3 0
```

This confirms that when the division is exact, no slices remain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time arithmetic operations are performed |
| Space | O(1) | No additional data structures are used |

The computation consists of a fixed number of operations regardless of input size, which makes it easily within limits even for maximum constraints of 10^9.

## Test Cases

```python
import sys, io

def solve():
    x, n = map(int, sys.stdin.readline().split())
    print(x // n, x % n)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as _io
    out = _io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("5 2\n") == "2 1", "sample 1"
assert run("9 3\n") == "3 0", "sample 2"

# custom cases
assert run("1 2\n") == "0 1", "fewer slices than friends"
assert run("10 1\n") == "10 0", "single friend gets everything"
assert run("1000000000 2\n") == "500000000 0", "large equal split"
assert run("7 3\n") == "2 1", "general remainder case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 | 0 1 | fewer slices than friends |
| 10 1 | 10 0 | single recipient edge case |
| 1000000000 2 | 500000000 0 | maximum input size |
| 7 3 | 2 1 | general non-divisible case |

## Edge Cases

When the number of slices is smaller than the number of friends, such as input `1 5`, integer division yields zero, meaning no friend receives any slice. The modulo operation returns the original number, which correctly reflects that nothing was distributed.

When the number of friends is one, such as `10 1`, the division yields all slices for that single friend, and the remainder is zero. This confirms that the entire resource is allocated correctly without special handling.

When slices divide evenly, such as `8 4`, integer division produces the exact per-friend share and modulo returns zero. This shows that no leftover handling is needed beyond the arithmetic decomposition itself.

When values are large, such as `10^9 2`, the operations still behave correctly because Python handles arbitrary-size integers. The computation remains constant time and does not degrade with input magnitude.
