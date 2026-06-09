---
title: "CF 1979B - XOR Sequences"
description: "We are given two integers, x and y. Using them, we define two infinite sequences: $$an=noplus x$$ and $$bn=noplus y.$$ The indices start from 1. Every element is obtained by XORing the index with a fixed value."
date: "2026-06-08T17:00:54+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1979
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 951 (Div. 2)"
rating: 1000
weight: 1979
solve_time_s: 123
verified: true
draft: false
---

[CF 1979B - XOR Sequences](https://codeforces.com/problemset/problem/1979/B)

**Rating:** 1000  
**Tags:** bitmasks, greedy  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers, `x` and `y`. Using them, we define two infinite sequences:

$$a_n=n\oplus x$$

and

$$b_n=n\oplus y.$$

The indices start from `1`. Every element is obtained by XORing the index with a fixed value.

The task is to find the maximum length of a contiguous block that appears in both sequences. The block may start at different positions in the two sequences, but once the starting positions are chosen, the elements must match one by one for the entire length.

The constraints are small in terms of test count but the values of `x` and `y` can be as large as $10^9$. The sequences themselves are infinite, so any solution that tries to generate terms explicitly is impossible. Even examining the first few million elements would not be enough because the answer can be as large as $2^{25}$, as shown by the sample.

The problem is really about understanding how XOR transforms consecutive integers. Once we find the underlying bit pattern, the answer can be computed in constant time per test case.

A subtle edge case appears when `x` and `y` differ only in the least significant bit.

For example:

```
x = 0
y = 1
```

Then:

```
d = x xor y = 1
```

The answer is `1`. A common mistake is to think the answer should be `2` because XOR only changes one bit. The carry behavior of consecutive integers immediately breaks any longer matching segment.

Another easy mistake occurs when `x xor y` is a power of two.

For example:

```
x = 12
y = 4
```

Then:

```
x xor y = 8
```

The answer is `8`, not `4`. The length depends on the position of the lowest differing bit, not on the number of differing bits.

## Approaches

A brute-force idea is to generate large prefixes of both sequences and search for the longest common subarray. This is correct because the definition is literally asking for a common contiguous segment.

The problem is that the sequences are infinite. Even if we generated the first million elements, there would be no guarantee that the optimal segment occurs there. The answer itself can exceed thirty million, so any direct simulation is hopeless.

The key observation comes from rewriting the equality condition.

Suppose a common segment starts at positions `i` and `j`. Then for every offset `t` inside the segment,

$$(i+t)\oplus x=(j+t)\oplus y.$$

Applying XOR with `x` on both sides gives

$$(i+t) \oplus (j+t)=x\oplus y.$$

Let

$$d=x\oplus y.$$

The problem becomes:

Find the longest interval of consecutive values of `t` such that

$$(i+t)\oplus(j+t)=d.$$

Now we only need to study how XOR behaves when two numbers increase simultaneously.

The crucial fact is that the maximum possible length depends only on the lowest set bit of `d`.

If the lowest set bit of `d` is at position `k`, then the answer is

$$2^k.$$

Equivalently,

$$\text{answer}=d\ \&\ (-d).$$

This quantity is the value of the least significant set bit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Unbounded | Unbounded | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute

$$d=x\oplus y.$$

Since `x ≠ y`, we know `d > 0`.
2. Find the least significant set bit of `d`.

In binary arithmetic this is

$$d\ \&\ (-d).$$
3. Output that value.

The entire solution consists of these three steps.

### Why it works

Let the lowest set bit of `d` be at position `k`.

All bits below position `k` are zero in `d`. This means that for any matching pair of numbers `u` and `v` satisfying

$$u\oplus v=d,$$

their lower `k` bits must be identical.

As we increment both numbers simultaneously, those lower `k` bits evolve identically for exactly `2^k` consecutive values before a carry reaches bit `k`.

When that carry occurs, bit `k` changes in one side differently from the other because `d` contains a `1` at that position. The equality

$$(u+t)\oplus(v+t)=d$$

can no longer continue.

So no segment can be longer than `2^k`.

This bound is achievable by choosing suitable starting values whose lower `k` bits begin at zero. Then the XOR remains equal to `d` for exactly `2^k` consecutive steps.

Hence the longest possible common segment has length

$$2^k=d\&(-d).$$

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        x, y = map(int, input().split())
        d = x ^ y
        ans.append(str(d & -d))

    sys.stdout.write("\n".join(ans))

solve()
```

The implementation follows the mathematical result directly.

The expression `x ^ y` computes the mask of differing bits. Since the numbers are distinct, this value is always positive.

The expression `d & -d` isolates the lowest set bit. In two's-complement arithmetic, `-d` flips all bits above the lowest set bit and preserves exactly that bit when ANDed with `d`.

There are no overflow concerns because Python integers have arbitrary precision. The values are at most about `2^30`, so even fixed-width 64-bit integers would be sufficient.

## Worked Examples

### Example 1

Input:

```
x = 12
y = 4
```

| Quantity | Value |
| --- | --- |
| x | 12 |
| y | 4 |
| d = x xor y | 8 |
| Binary d | 1000 |
| Lowest set bit | 8 |
| Answer | 8 |

The lowest set bit is already the highest and only set bit. The longest common segment has length `8`.

### Example 2

Input:

```
x = 57
y = 37
```

| Quantity | Value |
| --- | --- |
| x | 57 |
| y | 37 |
| d = x xor y | 28 |
| Binary d | 11100 |
| Lowest set bit | 4 |
| Answer | 4 |

The least significant set bit is `4`, so the answer is `4`, matching the sample.

This example demonstrates that only the lowest differing bit matters. Higher differing bits do not affect the maximum length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | One XOR and one bit operation |
| Space | O(1) | Only a few variables are used |

Each test case requires a constant number of arithmetic operations. With up to `10^4` test cases, the running time is negligible compared to the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        x, y = map(int, input().split())
        d = x ^ y
        out.append(str(d & -d))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    res = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return res.strip()

# provided sample
assert run(
"""4
0 1
12 4
57 37
316560849 14570961
"""
) == "\n".join([
    "1",
    "8",
    "4",
    "33554432"
])

# adjacent values
assert run(
"""1
10 11
"""
) == "1"

# power-of-two difference
assert run(
"""1
0 16
"""
) == "16"

# single low differing bit among many high bits
assert run(
"""1
123456 123460
"""
) == "4"

# large values
assert run(
"""1
1000000000 0
"""
) == "512"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `10 11` | `1` | Lowest bit difference only |
| `0 16` | `16` | Pure power of two |
| `123456 123460` | `4` | Multiple differing bits, lowest one dominates |
| `1000000000 0` | `512` | Large values near limit |

## Edge Cases

Consider:

```
x = 7
y = 6
```

Then

$$x\oplus y = 1.$$

The lowest set bit is `1`, so the answer is `1`.

A mistaken intuition is that very similar numbers should allow a long common segment. The carry generated after a single increment immediately reaches the differing bit, so the segment cannot extend beyond one element.

Now consider:

```
x = 0
y = 32
```

Then

$$x\oplus y=32.$$

The lowest set bit is `32`, and the answer is `32`. All lower five bits are identical in the XOR mask, allowing exactly `32` consecutive positions before a carry reaches the first differing bit.

Finally consider:

```
x = 13
y = 9
```

Then

$$x\oplus y=4.$$

Even though several higher bits may differ, the first differing position from the bottom is bit `2`, giving answer `4`. The algorithm ignores every higher bit because they do not influence when the first unavoidable carry breaks the equality.
