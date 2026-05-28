---
title: "CF 15C - Industrial Nim"
description: "Each quarry contributes a consecutive range of heap sizes to a standard Nim game. If a quarry gives us values (x, m), th"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "games"]
categories: ["algorithms"]
codeforces_contest: 15
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 15"
rating: 2000
weight: 15
solve_time_s: 145
verified: true
draft: false
---

[CF 15C - Industrial Nim](https://codeforces.com/problemset/problem/15/C)

**Rating:** 2000  
**Tags:** games  
**Solve time:** 2m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

Each quarry contributes a consecutive range of heap sizes to a standard Nim game.

If a quarry gives us values `(x, m)`, then its dumpers contain:

$$x,\ x+1,\ x+2,\ \dots,\ x+m-1$$

All dumpers from all quarries together form one large Nim position. Since ordinary Nim is played, the winner depends only on the xor of all heap sizes. If the total xor is non-zero, the first player wins. Otherwise the second player wins.

The direct interpretation of the task is:

$$(x) \oplus (x+1) \oplus \dots \oplus (x+m-1)$$

for every quarry, then xor all those results together.

The constraints completely rule out iterating through heaps individually. A single quarry may contain up to $10^{16}$ dumpers, and there may be $10^5$ quarries. Even storing all heaps is impossible, let alone processing them one by one.

This forces us to look for a mathematical shortcut for xor over consecutive integers.

The tricky part is that many programmers remember formulas for sums of ranges, but xor behaves differently. A naive adaptation often fails on boundary conditions.

Consider this input:

```
1
1 4
```

The heaps are:

```
1 2 3 4
```

Their xor is:

$$1 \oplus 2 \oplus 3 \oplus 4 = 4$$

A careless implementation that tries to derive patterns manually may easily produce `0` here.

Another easy mistake is mishandling ranges starting at zero. The standard prefix-xor formula uses:

$$0 \oplus 1 \oplus 2 \oplus \dots \oplus n$$

Suppose we process:

```
1
2 1
```

The answer is simply `2`, since there is only one heap. If we compute:

$$f(r) \oplus f(l)$$

instead of:

$$f(r) \oplus f(l-1)$$

we get the wrong result immediately.

Large values also matter. With numbers up to $10^{16}$, any fixed-width 32-bit integer logic would overflow in many languages. Python handles this automatically, but the algorithm still must remain logarithmic or constant time per quarry.

## Approaches

The brute-force idea is completely straightforward. For every quarry, generate all heap sizes in the interval:

$$[x,\ x+m-1]$$

and xor them together.

That works because Nim positions combine through xor. If the final xor is non-zero, the first player wins. Otherwise the second player loses.

The problem is scale. A single quarry can contain $10^{16}$ heaps. Even processing one billion operations per second would still be hopelessly slow. In the worst case, brute force would require roughly:

$$10^5 \times 10^{16} = 10^{21}$$

operations.

The key observation is that xor over consecutive integers has a repeating structure.

Define:

$$pref(n)=0 \oplus 1 \oplus 2 \oplus \dots \oplus n$$

Then xor over any interval becomes:

$$l \oplus (l+1) \oplus \dots \oplus r
=
pref(r)\oplus pref(l-1)$$

because every value before `l` appears twice and cancels itself.

Now we only need a fast way to compute `pref(n)`.

If we write out several values:

| n | pref(n) |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 3 |
| 3 | 0 |
| 4 | 4 |
| 5 | 1 |
| 6 | 7 |
| 7 | 0 |

a cycle of length 4 appears:

$$pref(n)=
\begin{cases}
n & n \bmod 4 = 0 \\
1 & n \bmod 4 = 1 \\
n+1 & n \bmod 4 = 2 \\
0 & n \bmod 4 = 3
\end{cases}$$

That reduces each quarry from up to $10^{16}$ operations to constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\sum m_i)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the number of quarries.
2. Maintain a variable `nim_sum`, initially `0`.

This stores the xor of all heaps across all quarries.
3. For each quarry, compute:

$$l = x$$

$$r = x+m-1$$

The quarry contributes every integer in the interval `[l, r]`.

1. Compute the xor of the interval using prefix xor:

$$range\_xor = pref(r) \oplus pref(l-1)$$

Every number below `l` appears in both prefix xors and cancels out.

1. Xor this interval contribution into `nim_sum`.
2. After processing all quarries, check `nim_sum`.

If it is non-zero, the first player has a winning Nim position, so print `"tolik"`.

Otherwise print `"bolik"`.

### Why it works

The correctness comes from two standard Nim properties.

First, independent heaps combine through xor. The entire game is winning for the first player exactly when the xor of all heap sizes is non-zero.

Second, xor is self-canceling:

$$a \oplus a = 0$$

So:

$$pref(r)\oplus pref(l-1)$$

removes all numbers below `l`, leaving only the xor of the interval `[l, r]`.

The `pref(n)` formula is correct because xor over consecutive integers repeats every four numbers. Appending four consecutive integers always restores the same pattern, which produces the closed-form cases based on `n % 4`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def pref_xor(n):
    if n % 4 == 0:
        return n
    if n % 4 == 1:
        return 1
    if n % 4 == 2:
        return n + 1
    return 0

n = int(input())
nim_sum = 0

for _ in range(n):
    x, m = map(int, input().split())

    l = x
    r = x + m - 1

    nim_sum ^= pref_xor(r) ^ pref_xor(l - 1)

print("tolik" if nim_sum else "bolik")
```

The helper function `pref_xor(n)` computes:

$$0 \oplus 1 \oplus \dots \oplus n$$

in constant time using the repeating modulo-4 pattern.

For each quarry, the code converts `(x, m)` into an actual interval `[x, x+m-1]`. The `-1` matters. Forgetting it shifts the range and breaks every answer.

The expression:

```
pref_xor(r) ^ pref_xor(l - 1)
```

extracts xor over the interval exactly the same way prefix sums extract arithmetic sums.

Python integers automatically handle values above $2^{63}$, so the $10^{16}$ limits are completely safe.

The final decision matches standard Nim theory. A zero xor means every move can be mirrored into another zero xor state, so the first player loses under optimal play.

## Worked Examples

### Example 1

Input:

```
2
2 1
3 2
```

Processing trace:

| Quarry | Interval | Interval xor | nim_sum after update |
| --- | --- | --- | --- |
| (2,1) | [2,2] | 2 | 2 |
| (3,2) | [3,4] | 7 | 5 |

Final xor is `5`, which is non-zero.

Output:

```
tolik
```

This example shows how different quarries simply combine through xor. The algorithm never needs to simulate moves.

### Example 2

Input:

```
1
1 3
```

The heaps are:

```
1 2 3
```

Trace:

| Quarry | Interval | pref(r) | pref(l-1) | Interval xor | nim_sum |
| --- | --- | --- | --- | --- | --- |
| (1,3) | [1,3] | 0 | 0 | 0 | 0 |

Output:

```
bolik
```

Indeed:

$$1 \oplus 2 \oplus 3 = 0$$

This demonstrates the cancellation property behind the prefix-xor technique.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each quarry is processed in constant time |
| Space | $O(1)$ | Only a few integer variables are stored |

With $10^5$ quarries, linear time is easily fast enough. The algorithm performs only a handful of arithmetic and xor operations per quarry, well within the 2-second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    def pref_xor(n):
        if n % 4 == 0:
            return n
        if n % 4 == 1:
            return 1
        if n % 4 == 2:
            return n + 1
        return 0

    n = int(input())
    nim_sum = 0

    for _ in range(n):
        x, m = map(int, input().split())

        l = x
        r = x + m - 1

        nim_sum ^= pref_xor(r) ^ pref_xor(l - 1)

    print("tolik" if nim_sum else "bolik")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run(
"""2
2 1
3 2
""") == "tolik", "sample 1"

# minimum-size input
assert run(
"""1
1 1
""") == "tolik", "single heap"

# xor becomes zero
assert run(
"""1
1 3
""") == "bolik", "1 xor 2 xor 3 = 0"

# catches off-by-one in interval end
assert run(
"""1
5 1
""") == "tolik", "single-value interval"

# large values
assert run(
"""1
10000000000000000 2
""") == "tolik", "large integers"

# multiple ranges cancelling each other
assert run(
"""2
1 1
1 1
""") == "bolik", "same heaps cancel"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1` | `tolik` | Minimum valid input |
| `1 / 1 3` | `bolik` | Zero xor position |
| `1 / 5 1` | `tolik` | Correct interval boundary handling |
| `1 / 10^16 2` | `tolik` | Large integer safety |
| `2 / 1 1 / 1 1` | `bolik` | Xor cancellation across quarries |

## Edge Cases

A common mistake is mishandling a quarry containing exactly one heap.

Input:

```
1
5 1
```

The interval is `[5,5]`.

The algorithm computes:

$$pref(5)\oplus pref(4)$$

Using the modulo-4 rule:

$$pref(5)=1$$

$$pref(4)=4$$

So:

$$1 \oplus 4 = 5$$

The final xor is non-zero, so the answer is `"tolik"`.

If we accidentally used `r = x + m` instead of `x + m - 1`, we would process `[5,6]` instead and get the wrong answer.

Another subtle case is when the total xor cancels completely.

Input:

```
1
1 3
```

The heaps are:

```
1 2 3
```

The algorithm computes:

$$pref(3)\oplus pref(0)
=
0 \oplus 0
=
0$$

So the output is `"bolik"`.

This validates the prefix-xor cancellation logic. A buggy implementation of the modulo-4 pattern usually fails on this exact range.

Large values are another danger point.

Input:

```
1
10000000000000000 1
```

The interval contains a single heap with value $10^{16}$.

The algorithm still performs only constant-time arithmetic:

$$pref(10^{16}) \oplus pref(10^{16}-1)$$

No iteration depends on heap magnitude, so the solution remains efficient even at maximum limits.
