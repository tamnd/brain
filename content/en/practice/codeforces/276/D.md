---
title: "CF 276D - Little Girl and Maximum XOR"
description: "We are given two integers, l and r. We may choose any two numbers a and b such that both lie inside the interval [l, r] and a ≤ b. Among all such pairs, we must compute the maximum possible value of a XOR b. The XOR operation compares bits position by position."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 276
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 169 (Div. 2)"
rating: 1700
weight: 276
solve_time_s: 84
verified: true
draft: false
---

[CF 276D - Little Girl and Maximum XOR](https://codeforces.com/problemset/problem/276/D)

**Rating:** 1700  
**Tags:** bitmasks, dp, greedy, implementation, math  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integers, `l` and `r`. We may choose any two numbers `a` and `b` such that both lie inside the interval `[l, r]` and `a ≤ b`. Among all such pairs, we must compute the maximum possible value of `a XOR b`.

The XOR operation compares bits position by position. A bit in the result becomes `1` when the corresponding bits of the two numbers differ, and `0` otherwise. Because higher bits contribute more to the final value, the best XOR comes from making the most significant differing bit as large as possible, then maximizing all smaller bits as well.

The bounds are extremely large, up to `10^18`. That immediately rules out checking all pairs. Even iterating over all numbers in the range may be impossible because the interval length itself can approach `10^18`. A quadratic solution would require roughly `(r - l + 1)^2` operations, which is completely infeasible.

The problem is really about binary structure, not enumeration. Since `10^18` fits inside 60 bits, any algorithm that processes bits directly in `O(log r)` time is easily fast enough.

Several edge cases are easy to mishandle if the reasoning is incomplete.

Consider the interval where both ends are equal:

```
l = 8, r = 8
```

The only possible pair is `(8, 8)`, so the answer is:

```
8 XOR 8 = 0
```

A careless implementation that assumes there is always some differing bit may incorrectly return a positive value.

Another tricky case is when the numbers differ only in low bits:

```
l = 10   -> 1010
r = 15   -> 1111
```

The highest differing bit is the third bit from the right. Once that bit differs, every smaller bit can also be made different, producing:

```
1111 = 15
```

A naive greedy attempt that only compares endpoints directly gives:

```
10 XOR 15 = 5
```

which is not optimal.

One more subtle case appears when the interval crosses a power of two:

```
l = 7    -> 0111
r = 8    -> 1000
```

The most significant bits already differ, which means the answer becomes:

```
1111 = 15
```

Many incorrect solutions underestimate the result here because they only look at existing values instead of reasoning about what pairs inside the interval are achievable.

## Approaches

The brute-force solution is straightforward. Iterate through every pair `(a, b)` such that `l ≤ a ≤ b ≤ r`, compute `a XOR b`, and keep the maximum.

This works because it directly checks all valid possibilities. The problem is the running time. If the interval length is `n = r - l + 1`, then the number of pairs is roughly:

```
n * (n + 1) / 2
```

When `n` can be close to `10^18`, this approach is hopeless.

The key observation comes from how XOR behaves in binary.

Suppose we compare `l` and `r` bit by bit from left to right. Eventually we reach the first position where they differ. Let that position be bit `k`.

Above bit `k`, every number inside the interval shares the same prefix. Those higher bits can never contribute to the XOR result because both chosen numbers must have identical values there.

At bit `k`, one endpoint has `0` and the other has `1`. Since the interval spans both possibilities, we can choose two numbers whose bits differ at that position. That contributes `1` at bit `k`.

Even more importantly, once the highest differing bit is fixed, every lower bit can also be made different. That means all bits from `k` down to `0` can become `1` in the final XOR.

So if the highest differing bit is `k`, the maximum XOR is:

```
2^(k+1) - 1
```

Another way to obtain this value is:

1. Compute `x = l XOR r`
2. Find the position of the highest set bit in `x`
3. Set all bits below it to `1`

For example:

```
l = 10  -> 1010
r = 15  -> 1111

l XOR r = 0101
```

The highest set bit is at position `2`, so the answer becomes:

```
111 = 7
```

Actually the interval allows an even larger XOR:

```
1000 XOR 1111 = 0111
```

Wait, this reveals the real structure more clearly. The correct transformation is:

If the highest differing bit is at position `k`, then the answer is:

```
(1 << (k + 1)) - 1
```

Here `k = 2`, giving:

```
111 = 7
```

But for the actual interval `[10,15]`, the highest differing bit between `10` and `15` is bit `2`, and the optimal pair is:

```
10 XOR 13 = 7
```

The formula matches perfectly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((r - l + 1)^2) | O(1) | Too slow |
| Optimal | O(log r) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers `l` and `r`.
2. Compute `x = l XOR r`.

This identifies exactly which bit positions differ between the interval endpoints.
3. Find the most significant set bit in `x`.

This bit is the highest position where numbers inside the interval can differ.
4. Construct the answer with all bits from that position downward set to `1`.

If the highest differing bit is position `k`, the answer becomes:

```
(1 << (k + 1)) - 1
```
5. Output the constructed value.

### Why it works

Let the first differing bit between `l` and `r` be position `k`.

All bits above `k` are identical across the entire interval. No pair of numbers inside `[l, r]` can differ there, so those bits in the XOR result must be `0`.

At bit `k`, the interval contains numbers with both `0` and `1` in that position. We can choose two such numbers, making bit `k` equal to `1` in the XOR result.

Once bit `k` differs, the lower bits become unrestricted. We can independently choose them to maximize XOR, which means every lower bit can also become `1`.

So the maximum XOR consists of `k + 1` consecutive `1` bits, exactly:

```
2^(k+1) - 1
```

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    l, r = map(int, input().split())

    x = l ^ r
    ans = 1

    while ans <= x:
        ans <<= 1

    print(ans - 1)

solve()
```

The solution starts by computing `l XOR r`. Every set bit in this value marks a position where the endpoints differ.

The loop finds the smallest power of two strictly greater than `x`. Suppose the highest set bit in `x` is position `k`. Then after the loop finishes, `ans` equals:

```
2^(k+1)
```

Subtracting one produces:

```
2^(k+1) - 1
```

which is a binary number containing exactly `k + 1` ones.

The implementation avoids any overflow issues because Python integers automatically expand as needed. In languages with fixed-width integers, 64-bit types are necessary since the input may reach `10^18`.

One subtle detail is the loop condition:

```
while ans <= x:
```

Using `<` instead would fail when `x` itself is already a power of two.

## Worked Examples

### Example 1

Input:

```
1 2
```

Binary forms:

```
1 = 01
2 = 10
```

| Step | Value |
| --- | --- |
| `l XOR r` | `01 XOR 10 = 11` |
| `x` | `3` |
| Powers checked | `1 -> 2 -> 4` |
| First power greater than `x` | `4` |
| Final answer | `4 - 1 = 3` |

The answer becomes `3`, which is binary `11`. Both bits can differ inside the interval.

### Example 2

Input:

```
10 15
```

Binary forms:

```
10 = 1010
15 = 1111
```

| Step | Value |
| --- | --- |
| `l XOR r` | `1010 XOR 1111 = 0101` |
| `x` | `5` |
| Highest differing bit | Position `2` |
| Powers checked | `1 -> 2 -> 4 -> 8` |
| First power greater than `x` | `8` |
| Final answer | `8 - 1 = 7` |

This trace shows the central invariant. Once the highest differing bit is identified, every smaller bit can also become `1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log r) | The loop processes at most 60 bits |
| Space | O(1) | Only a few integer variables are used |

Since `10^18` fits within 60 binary digits, the loop executes only a tiny number of iterations. The solution comfortably fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    l, r = map(int, input().split())

    x = l ^ r
    ans = 1

    while ans <= x:
        ans <<= 1

    print(ans - 1)

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
assert run("1 2\n") == "3\n", "sample 1"

# minimum range
assert run("1 1\n") == "0\n", "single value"

# all equal large value
assert run("1000000 1000000\n") == "0\n", "same endpoints"

# crossing power of two
assert run("7 8\n") == "15\n", "highest bit changes"

# nearby values
assert run("10 15\n") == "7\n", "lower bits become all ones"

# large boundary
assert run("1 1000000000000000000\n") == "1152921504606846975\n", "large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | Single-number interval |
| `1000000 1000000` | `0` | Large equal endpoints |
| `7 8` | `15` | Crossing a power of two |
| `10 15` | `7` | Lower bits become all ones |
| `1 1000000000000000000` | `1152921504606846975` | Large 64-bit behavior |

## Edge Cases

Consider the input:

```
8 8
```

We compute:

```
8 XOR 8 = 0
```

So `x = 0`. The loop never runs because `ans = 1` is already greater than `0`. The algorithm prints:

```
1 - 1 = 0
```

which is correct because only one pair exists.

Now consider:

```
7 8
```

Binary representations:

```
7 = 0111
8 = 1000
```

The highest differing bit is the most significant bit itself. Computing:

```
7 XOR 8 = 1111
```

gives `15`. The algorithm recognizes that every lower bit can also vary and correctly outputs:

```
15
```

Finally examine:

```
10 11
```

Binary forms:

```
10 = 1010
11 = 1011
```

Only the lowest bit differs:

```
10 XOR 11 = 0001
```

The algorithm returns:

```
1
```

This confirms that when only one bit position can vary, the maximum XOR contains exactly one set bit.
