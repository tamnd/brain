---
title: "CF 76D - Plus and xor"
description: "We are given two non-negative integers, A and B. We need to construct two other non-negative integers, X and Y, such that: - their sum equals A - their bitwise xor equals B Among all valid pairs, we must output the one with the smallest possible X."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 76
codeforces_index: "D"
codeforces_contest_name: "All-Ukrainian School Olympiad in Informatics"
rating: 1700
weight: 76
solve_time_s: 106
verified: true
draft: false
---

[CF 76D - Plus and xor](https://codeforces.com/problemset/problem/76/D)

**Rating:** 1700  
**Tags:** dp, greedy, math  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two non-negative integers, `A` and `B`. We need to construct two other non-negative integers, `X` and `Y`, such that:

- their sum equals `A`
- their bitwise xor equals `B`

Among all valid pairs, we must output the one with the smallest possible `X`.

The interesting part is that addition and xor interact through carries. If we only look at xor, every bit behaves independently. Addition is different because a carry from a lower bit changes the next bit. The entire problem is really about understanding how these two operations fit together.

The numbers can be as large as `2^64 - 1`, so brute force over all possible values is impossible. Even iterating over all candidates for `X` would require up to `2^64` operations, which is completely infeasible. We need something that works in roughly constant time, or at worst proportional to the number of bits. Since a 64-bit integer has only 64 positions, an `O(64)` solution is effectively instantaneous.

Several edge cases are easy to mishandle.

Consider:

```
A = 5
B = 6
```

We know that:

```
X + Y >= X xor Y
```

because carries increase the sum. Here `B > A`, so no solution exists. A careless implementation that only manipulates bits without checking feasibility may incorrectly produce negative intermediate values.

Another subtle case is parity mismatch:

```
A = 10
B = 3
```

Using the identity:

```
A = (X xor Y) + 2 * (X & Y)
```

we get:

```
A - B = 7
```

which is odd. Since `2 * (X & Y)` must always be even, this is impossible. Missing this parity condition causes incorrect answers.

There is also the overlap condition:

```
A = 2
B = 2
```

Then:

```
(A - B) / 2 = 0
```

which is valid, giving:

```
X = 0
Y = 2
```

But for:

```
A = 10
B = 8
```

we get:

```
C = (A - B) / 2 = 1
```

Now `C & B = 0`, so the construction works.

Compare that with:

```
A = 14
B = 10
```

Then:

```
C = 2
B = 1010
C = 0010
```

They overlap on bit 1. That means one bit would need to simultaneously create a carry and differ in xor, which is impossible. A naive reconstruction can silently generate invalid numbers here.

## Approaches

The most direct brute-force idea is to try every possible value of `X`, compute:

```
Y = A - X
```

and check whether:

```
X xor Y == B
```

This is correct because every valid pair must satisfy the equation. The problem is the search space. Since `A` can be close to `2^64`, the brute-force approach may require around `10^19` iterations. Even a billion operations per second would take centuries.

The key observation comes from a standard identity involving sum and xor:

$X+Y=(X\oplus Y)+2(X\&Y)$

The xor counts positions where bits differ. The `AND` counts positions where both bits are `1`, which create carries during addition. Every carry contributes twice its bit value to the final sum.

Since `B = X xor Y`, we can rewrite:

```
A = B + 2 * (X & Y)
```

Let:

```
C = X & Y = (A - B) / 2
```

Now the problem becomes:

- construct two numbers whose xor is `B`
- whose and is `C`

At each bit:

- if a bit in `B` is `1`, then the bits of `X` and `Y` must differ
- if a bit in `C` is `1`, then both bits must be `1`

These two conditions cannot happen simultaneously on the same bit. So:

```
B & C == 0
```

must hold.

Once this condition is satisfied, reconstruction becomes easy:

- every `1` bit of `C` goes into both numbers
- every `1` bit of `B` must go into exactly one of the numbers

To minimize `X`, we assign all xor-only bits to `Y` instead of `X`.

That gives:

```
X = C
Y = C + B
```

provided the overlap condition is valid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^64) | O(1) | Too slow |
| Optimal | O(64) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `A` and `B`.
2. Check whether `A < B`.

Since:

```
X + Y >= X xor Y
```

the sum can never be smaller than the xor.
3. Compute:

```
D = A - B
```

If `D` is odd, no solution exists.

The quantity:

```
D = 2 * (X & Y)
```

must always be even.
4. Compute:

```
C = D // 2
```

This represents the common `1` bits shared by both numbers.
5. Check whether:

```
C & B != 0
```

If this happens, output `-1`.

A bit cannot simultaneously belong to the xor and the carry structure. A xor bit requires the two numbers to differ, while an and bit requires both to be `1`.
6. Construct the answer:

```
X = C
Y = C + B
```

All shared bits stay inside `C`. All differing bits from `B` are assigned to `Y` to keep `X` as small as possible.
7. Output `X` and `Y`.

### Why it works

The construction is based on the exact decomposition of binary addition into xor and carries:

```
X + Y = (X xor Y) + 2 * (X & Y)
```

The value `C = (A - B) / 2` uniquely determines all carry-producing bits. If any bit belongs to both `B` and `C`, we would need the same bit position to both differ and match simultaneously, which is impossible.

When `B & C == 0`, the roles of bits are completely separated:

- bits of `C` are `1` in both numbers
- bits of `B` are `1` in exactly one number

Assigning every xor-only bit to `Y` minimizes `X`, because adding any of those bits to `X` would only increase it.

## Python Solution

```python
import sys
input = sys.stdin.readline

A = int(input())
B = int(input())

if A < B:
    print(-1)
    sys.exit()

D = A - B

if D % 2:
    print(-1)
    sys.exit()

C = D // 2

if C & B:
    print(-1)
    sys.exit()

X = C
Y = C + B

print(X, Y)
```

The first condition checks the basic inequality between sum and xor. Any valid pair must satisfy:

```
X + Y >= X xor Y
```

because carries only increase the sum.

Next, the code computes `D = A - B`. This value must equal twice the shared-bit structure:

```
D = 2 * (X & Y)
```

If `D` is odd, reconstruction is impossible.

The overlap check:

```
if C & B:
```

is the core correctness condition. A set bit in `C` means both numbers contain `1` there. A set bit in `B` means the numbers differ there. One bit position cannot satisfy both requirements simultaneously.

The final construction is intentionally asymmetric:

```
X = C
Y = C + B
```

Every xor-only bit goes into `Y`, which keeps `X` minimal. Using addition instead of bitwise or is safe because `C` and `B` never overlap.

Python integers automatically handle 64-bit values safely, so there is no overflow risk.

## Worked Examples

### Example 1

Input:

```
A = 142
B = 76
```

First compute:

```
D = A - B = 66
C = 33
```

Binary forms:

```
B = 1001100
C = 0100001
```

No overlapping bits exist.

| Variable | Value |
| --- | --- |
| A | 142 |
| B | 76 |
| D = A - B | 66 |
| C = D / 2 | 33 |
| C & B | 0 |
| X | 33 |
| Y | 109 |

Verification:

| Expression | Result |
| --- | --- |
| X + Y | 142 |
| X xor Y | 76 |

This trace shows the clean separation between carry bits and xor bits. The shared bits form `33`, while xor-only bits are added into `Y`.

### Example 2

Input:

```
A = 10
B = 3
```

| Variable | Value |
| --- | --- |
| A | 10 |
| B | 3 |
| D = A - B | 7 |

Since `D` is odd, reconstruction stops immediately.

This demonstrates the parity condition. Shared carry bits always contribute an even amount to the sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(64) | Only a constant number of bitwise operations on 64-bit integers |
| Space | O(1) | No extra data structures are used |

The solution performs only a few arithmetic and bitwise operations, independent of the magnitude of the numbers. This easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    A = int(input())
    B = int(input())

    if A < B:
        print(-1)
        return

    D = A - B

    if D % 2:
        print(-1)
        return

    C = D // 2

    if C & B:
        print(-1)
        return

    print(C, C + B)

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
assert run("142\n76\n") == "33 109", "sample 1"

# minimum values
assert run("0\n0\n") == "0 0", "both zero"

# impossible because A < B
assert run("5\n6\n") == "-1", "sum smaller than xor"

# impossible because parity fails
assert run("10\n3\n") == "-1", "odd difference"

# valid boundary-style case
assert run("2\n2\n") == "0 2", "xor without shared bits"

# overlap conflict
assert run("14\n10\n") == "-1", "and/xor overlap"

# large values
assert run("18446744073709551614\n0\n") == \
       "9223372036854775807 9223372036854775807", "64-bit range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `0 0` | Smallest possible input |
| `5 6` | `-1` | Sum cannot be smaller than xor |
| `10 3` | `-1` | Odd difference detection |
| `2 2` | `0 2` | Pure xor case with minimal X |
| `14 10` | `-1` | Overlap between xor bits and carry bits |
| Large 64-bit case | valid large pair | Correct handling near integer limits |

## Edge Cases

Consider:

```
A = 5
B = 6
```

The algorithm first checks:

```
A < B
```

which is true. Since xor can never exceed the sum, the algorithm correctly prints:

```
-1
```

without attempting reconstruction.

Now consider:

```
A = 10
B = 3
```

The algorithm computes:

```
D = 10 - 3 = 7
```

Since `7` is odd, it is impossible for:

```
D = 2 * (X & Y)
```

The algorithm terminates immediately with `-1`.

Finally, consider the overlap conflict:

```
A = 14
B = 10
```

We compute:

```
D = 4
C = 2
```

Binary:

```
B = 1010
C = 0010
```

Now:

```
C & B = 0010
```

which is nonzero.

Bit 1 would need to be:

- different between `X` and `Y` because it belongs to xor
- equal to `1` in both numbers because it belongs to and

That contradiction makes the instance impossible, and the algorithm correctly outputs `-1`.
