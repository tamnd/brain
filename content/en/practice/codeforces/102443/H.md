---
title: "CF 102443H - Planet Nine"
description: "We have one decimal integer register. Starting from a, we may perform two kinds of operations. An addition operation increases the register by 9x for any positive integer x."
date: "2026-08-09T01:57:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102443
codeforces_index: "H"
codeforces_contest_name: "2019-2020 Russia Team Open, High School Programming Contest (VKOSHP 19)"
rating: 0
weight: 102443
solve_time_s: 867
verified: false
draft: false
---

[CF 102443H - Planet Nine](https://codeforces.com/problemset/problem/102443/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We have one decimal integer register. Starting from `a`, we may perform two kinds of operations. An addition operation increases the register by `9x` for any positive integer `x`. A deletion operation removes some positive number of leading decimal digits, but every removed digit must be `1`. The special case where the register is exactly `1` is included, because deleting that single digit produces `0`.

The task is constructive. Given `a` and `b`, we must print a sequence of at most `1000` operations that changes the register from `a` to `b`, or print `Broken` if no such sequence exists. Intermediate register values must stay at most `10^18`. The input values themselves are at most `10^9`, so they contain at most ten decimal digits.

The small number of digits is the key constraint. We do not need a shortest sequence, and we have a very generous limit of `1000` operations compared with the at most ten digits that need to be handled. This strongly suggests that the right solution should process the decimal representation digit by digit rather than search through possible register values.

A careless solution can also fail because leading zeroes disappear from the ordinary decimal representation. For example, consider `a = 100`. After handling the first digit, the remaining conceptual suffix is `00`, but the register stores it simply as `0`. A construction must reason about the position of the suffix using its digit count, rather than assuming that the register's current decimal length equals the number of unprocessed digits.

Another edge case is `a = 0` and `b = 0`. No operation is needed, so the correct output can simply be `Stable` followed by `0`. A construction that blindly tries to process the digit `0` as if it were a positive digit may produce an invalid operation.

The case `a = 1`, `b = 9` is also instructive. We can transform `1` into `0` by adding `9` and deleting the leading `1`, then transform `0` into `9` by adding another `9`. Thus a valid sequence is `+ 1`, `- 1`, `+ 1`. The sample uses a shorter sequence, `+ 2`, `- 1`, but minimality is irrelevant.

Finally, a solution must respect the `10^18` intermediate bound. Merely finding an algebraically correct construction is not enough if an addition creates a number larger than the allowed limit. The digit construction below creates numbers with at most eighteen decimal digits in the allowed input range, and its largest possible intermediate value remains below `10^18`.

## Approaches

A natural brute-force idea is to treat each register value as a state and search for a path from `a` to `b`. From a state we could try additions by increasing `x`, and we could also try every possible valid deletion. This is correct in principle because every legal operation would be represented as an edge in the state graph.

The problem is that the state space is enormous. Even if we restrict ourselves to values below `10^18`, there are up to `10^18 + 1` possible register values. Trying additions one by one is even worse for this particular construction. For example, when building a digit `1` at a sufficiently high decimal position, the required multiplier can be `12,345,679` times a power of ten. For a nine-digit target consisting entirely of ones, the largest required `x` is `1,234,567,900,000,000`, so a brute-force search that tests `x = 1, 2, 3, ...` can require more than `10^15` candidate checks at one position. The `1` second limit rules out such a search immediately.

The useful observation is that multiplication by `9` is tightly connected to decimal digit sums. If we want to turn a leading digit into a sequence of leading ones, we can choose an integer whose multiplication by `9` creates exactly those ones.

Suppose the current number starts with a digit `d`, followed by a suffix of exactly `k` decimal positions. For `d >= 1`, consider the number formed by writing `1, 2, ..., d`. For example, for `d = 4` this is `1234`. The identity

`4 + 9 * 1234 = 11110`

is the pattern we need. In general,

`d + 9 * 123...d = 11...110`

with exactly `d` leading ones. If the entire expression is multiplied by `10^k`, the suffix remains untouched after those leading ones are deleted. This lets us remove the first digit of `a`. Processing all digits from left to right eventually transforms `a` into zero.

Going in the opposite direction is slightly different. Suppose we already have a suffix of the target and want to prepend digit `d`. We can add a multiple of nine so that the result begins with several ones followed by the desired digit and the existing suffix. The number of leading ones is chosen so that the new number has the same remainder modulo nine as the existing suffix. Since a decimal number has the same remainder modulo nine as its digit sum, choosing `9 - d` leading ones for `1 <= d < 9` makes the added amount divisible by nine. For `d = 9`, no leading ones are needed.

This gives a direct construction from `0` to any `b`. Combining the two constructions gives

`a -> 0 -> b`.

Every digit takes at most two operations, so with at most ten digits in each number the whole sequence has at most forty operations, far below the limit of `1000`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Ω(10^15) candidate checks in a representative worst case | Potentially O(10^18) states | Too slow |
| Digit Construction | O(D^2), where D <= 10 | O(D) | Accepted |

## Algorithm Walkthrough

1. Read `a` and `b` as strings. Keeping the strings is useful because the construction depends on the original decimal positions, including zeroes that would otherwise disappear from the register representation.
2. Build a sequence that transforms `a` into `0`. Process the digits of `a` from left to right. Let `k` be the number of positions to the right of the current digit.
3. If the current digit is `0`, emit no operation. The current register already represents exactly the remaining suffix numerically, so there is nothing to remove.
4. If the current digit is `d >= 1`, construct the integer `123...d`. For example, `d = 1` gives `1`, `d = 2` gives `12`, and `d = 5` gives `12345`. Add `9 * 123...d * 10^k`, which is represented by the operation `+ (123...d * 10^k)`.
5. After this addition, the current leading digit and the added amount combine into exactly `d` leading ones, followed by the unchanged suffix. Delete those `d` leading ones using `- d`. The invariant after this operation is that the processed first digit has disappeared and the register equals the unprocessed suffix.
6. After all digits of `a` have been processed, the register is `0`. This handles leading zeroes automatically because zero digits require no operation.
7. Now construct `b` starting from zero. Process the digits of `b` from right to left. At every point, the register contains the suffix of `b` that has already been constructed.
8. If the new digit is `9`, add `9 * 10^k`, where `k` is the number of already constructed suffix digits. This directly changes the prefix from the current suffix `S` into `9S`, so no deletion is necessary.
9. If the new digit is `d`, where `1 <= d < 9`, choose exactly `9 - d` leading ones. Construct the integer `C` consisting of the digits `1, 2, ..., 8-d`, followed by `10-d`. For example, `d = 2` gives `C = 1234568`, while `d = 8` gives `C = 2`.
10. Add `C * 10^k` by printing `+ C * 10^k`. The resulting register consists of `9-d` leading ones, then the desired digit `d`, then the suffix already constructed. Delete the first `9-d` digits using `- (9-d)`. The register is now the correct longer suffix.
11. Concatenate the operations from the `a -> 0` phase and the `0 -> b` phase. Since each nonzero digit creates at most two operations and each number has at most ten digits, there are at most forty operations.

### Why it works

The invariant of the first phase is that after processing position `j`, the register contains exactly the decimal suffix beginning at position `j+1`. For a digit `d >= 1`, the identity

`d + 9 * 123...d = 11...110`

creates exactly `d` leading ones, so deleting those ones removes precisely the processed digit. Multiplication by `10^k` preserves the suffix positions. Thus every processed digit is removed without changing any unprocessed digit.

For the second phase, suppose the already constructed suffix is `S` and the next target digit is `d < 9`. We create a number of the form

`111...1 d S`

with `9-d` leading ones. Its digit sum exceeds that of `S` by exactly `9`, so it is congruent to `S` modulo nine. Consequently their difference is divisible by nine and can be produced by an addition operation. After deleting the `9-d` leading ones, the register becomes exactly `dS`. For `d = 9`, the direct addition of `9 * 10^k` gives `9S`. Hence every target digit can be prepended correctly.

The two phases are independent because the first always finishes at zero, and the second starts at zero. Since every operation is legal by construction and every intermediate value is bounded, the final register is exactly `b`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_to_zero(s):
    ops = []
    n = len(s)

    for i, ch in enumerate(s):
        d = ord(ch) - ord('0')

        if d == 0:
            continue

        # 123...d
        c = 0
        for x in range(1, d + 1):
            c = c * 10 + x

        k = n - 1 - i
        x = c * (10 ** k)

        ops.append(("+", x))
        ops.append(("-", d))

    return ops

def build_from_zero(s):
    ops = []
    n = len(s)

    for i in range(n - 1, -1, -1):
        d = ord(s[i]) - ord('0')
        k = n - 1 - i

        if d == 0:
            # A zero cannot be introduced by deleting leading ones,
            # but it is already represented by the positional suffix.
            continue

        if d == 9:
            # Add 9 * 10^k, which simply prepends digit 9.
            ops.append(("+", 10 ** k))
            continue

        # We want:
        #
        #   111...1 d S
        #
        # with 9-d leading ones.
        #
        # The difference from S must be divisible by 9.
        c = 0
        for x in range(1, 9 - d):
            c = c * 10 + x
        c = c * 10 + (10 - d)

        x = c * (10 ** k)

        ops.append(("+", x))
        ops.append(("-", 9 - d))

    return ops

def solve():
    a, b = input().split()

    ops = build_to_zero(a)
    ops.extend(build_from_zero(b))

    print("Stable")
    print(len(ops))
    for typ, value in ops:
        print(typ, value)

if __name__ == "__main__":
    solve()
```

The `build_to_zero` function implements the left-to-right invariant directly. The variable `k` is the number of decimal positions after the current digit, so multiplying the constructed value by `10^k` makes the newly created leading ones occur before the untouched suffix.

The loop constructing `c` deliberately uses the digits `1` through `d`. The resulting identity is the heart of the first phase. For example, with `d = 3`, `c = 123`, and `3 + 9 * 123 = 1110`.

The `build_from_zero` function reverses the direction. Its `k` counts how many target positions have already been constructed to the right. For digits from `1` through `8`, the value of `c` is chosen so that the number created after multiplication by nine contains exactly `9-d` leading ones. The subsequent deletion removes those ones and leaves the desired digit in front of the existing suffix.

The `d == 9` case is separate because `9-d` is zero. There is nothing to delete, and adding `9 * 10^k` simply inserts a `9` at the correct position.

Zeros need no explicit operation in the construction. They are handled by positional multiplication in later steps. This is why the original input must be retained as a string even though the register itself stores an integer.

Python integers do not overflow, but the construction also respects the problem's numerical bound. With inputs no larger than `10^9`, the only ten-digit input is `1000000000`, whose first digit is `1`; the constructed intermediate values therefore remain below `10^18`. The operation count is at most forty.

## Worked Examples

### Sample 1: `0 0`

The first phase has no digits that need processing, and the second phase also has no nonzero digit to construct.

| Phase | Position | Digit | Operation | Register |
| --- | --- | --- | --- | --- |
| Start |  |  |  | 0 |
| `a -> 0` |  |  | none | 0 |
| `0 -> b` |  |  | none | 0 |

The output is simply `Stable` followed by zero operations. This demonstrates the boundary case where both endpoints are already equal to zero.

### Sample 2: `1 9`

For `a = 1`, the first phase processes digit `1`. Here `k = 0` and `123...d = 1`, so we add `9` and obtain `10`. Removing one leading `1` leaves zero.

For `b = 9`, the second phase sees digit `9`. Since it is `9`, no leading ones are required. Adding `9` to zero produces the target directly.

| Phase | Digit | `k` | `+ x` | Register after `+` | `- y` | Register after `-` |
| --- | --- | --- | --- | --- | --- | --- |
| `1 -> 0` | 1 | 0 | 1 | 10 | 1 | 0 |
| `0 -> 9` | 9 | 0 | 1 | 9 | none | 9 |

The construction uses three operations, whereas the sample uses two. Both are valid because the problem asks for any valid sequence rather than a minimum-length sequence.

### A multi-digit example: `21 -> 21`

The first digit of `21` is `2`, with one digit to its right. We use `123 * 10 = 1230`, so the addition increases the register by `11070`, taking `21` to `11091`. Removing the first two ones leaves `91`, which is the remaining suffix `1` only if we inspect the arithmetic carefully. More directly, the construction should be interpreted through the identity on the full suffix:

`21 + 9 * (12 * 10) = 21 + 1080 = 1101`.

Deleting two leading ones leaves `1`.

The next digit is `1`, so adding `9` gives `10` and deleting its leading one gives zero.

For the reverse direction, process the final target digit `1` first. Starting from zero, adding `9 * 12345679` produces `111111111`, and deleting eight leading ones leaves `1`.

Then process digit `2`. The already built suffix is `1`, so we add `9 * 1234568 * 10`, producing `111111121`. Deleting seven leading ones leaves `21`.

| Phase | Current target digit | `k` | Addition multiplier `x` | Result before deletion | Deleted ones | Result |
| --- | --- | --- | --- | --- | --- | --- |
| `21 -> 0` | 2 | 1 | 120 | 1101 | 2 | 1 |
| `21 -> 0` | 1 | 0 | 1 | 10 | 1 | 0 |
| `0 -> 21` | 1 | 0 | 12345679 | 111111111 | 8 | 1 |
| `0 -> 21` | 2 | 1 | 12345680 | 111111121 | 7 | 21 |

This trace shows why the direction matters. To remove digits, we work from the most significant side first. To build digits, we work from the least significant side first because that suffix must already exist when a new digit is prepended.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(D^2) | For each of at most D digits, constructing the small decimal pattern takes O(D) time. |
| Space | O(D) | At most two operations are stored per digit. |

Here `D <= 10` because `a` and `b` are at most `10^9`. The resulting number of operations is at most `4D <= 40`, comfortably below the allowed `1000`, and the memory consumption is negligible compared with the `512 MB` limit.

## Test Cases

The following harness checks the produced operation sequence rather than comparing it with one fixed answer. That is necessary because the problem accepts any valid construction.

```python
# helper: run solution on input string, return output string
import sys
import io

def build_to_zero(s):
    ops = []
    n = len(s)

    for i, ch in enumerate(s):
        d = int(ch)

        if d == 0:
            continue

        c = 0
        for x in range(1, d + 1):
            c = c * 10 + x

        k = n - 1 - i
        ops.append(("+", c * (10 ** k)))
        ops.append(("-", d))

    return ops

def build_from_zero(s):
    ops = []
    n = len(s)

    for i in range(n - 1, -1, -1):
        d = int(s[i])
        k = n - 1 - i

        if d == 0:
            continue

        if d == 9:
            ops.append(("+", 10 ** k))
            continue

        c = 0
        for x in range(1, 9 - d):
            c = c * 10 + x
        c = c * 10 + (10 - d)

        ops.append(("+", c * (10 ** k)))
        ops.append(("-", 9 - d))

    return ops

def solve_string(inp):
    a, b = inp.strip().split()

    ops = build_to_zero(a)
    ops.extend(build_from_zero(b))

    out = ["Stable", str(len(ops))]
    out.extend(f"{typ} {value}" for typ, value in ops)
    return "\n".join(out) + "\n"

def run(inp: str) -> str:
    return solve_string(inp)

def validate(inp):
    a, b = map(int, inp.split())
    out = run(inp).strip().splitlines()

    assert out[0] == "Stable"

    n = int(out[1])
    assert 0 <= n <= 1000
    assert len(out) == n + 2

    value = a

    for line in out[2:]:
        typ, number = line.split()
        number = int(number)

        assert number > 0

        if typ == "+":
            value += 9 * number
        else:
            assert typ == "-"
            s = str(value)
            y = number
            assert y <= len(s)
            assert s[:y] == "1" * y
            value = int(s[y:]) if s[y:] else 0

        assert 0 <= value <= 10**18

    assert value == b

# Provided samples.
assert run("0 0") == "Stable\n0\n", "sample 1"

# Any valid construction is accepted, so validate the sample instead
# of requiring the sample's particular two-operation sequence.
validate("1 9")

# Minimum-size values.
validate("0 1")

# Both endpoints equal.
validate("123456789 123456789")

# Maximum allowed input value.
validate("1000000000 1000000000")

# Boundary digits and many zeroes.
validate("100000000 900000009")

# Every digit is nonzero, exercising both directions heavily.
validate("987654321 123456789")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `Stable`, `0` operations | Minimum-size and zero-to-zero boundary |
| `0 1` | Any valid `Stable` construction | Building a single digit from zero |
| `123456789 123456789` | Any valid `Stable` construction | Many consecutive nonzero digits |
| `1000000000 1000000000` | Any valid `Stable` construction | Maximum input value and positional zeroes |
| `100000000 900000009` | Any valid `Stable` construction | Leading digit, internal zeroes, and digit `9` |
| `987654321 123456789` | Any valid `Stable` construction | Both construction directions with all digits active |

## Edge Cases

For `a = 0` and `b = 0`, both construction functions return an empty operation list. The algorithm prints `Stable` and `0`, which is exactly the simplest valid transformation. No artificial `+` or `-` operation is needed.

For a number containing zeroes, consider `a = 100`. The first digit is `1`, so the algorithm adds `10^2` objects, meaning the register increases by `900`, changing `100` into `1000`. Removing the leading `1` leaves `0`. The two remaining zero digits generate no operations. This works because their positions have already been accounted for by the power of ten used while processing the first digit.

For a target containing zeroes, consider `b = 900000009`. The algorithm builds the final `9` first. The intervening zeroes require no explicit operation, because when the later leading `9` is inserted, its power of ten already places it nine positions away from the existing suffix. The construction therefore creates the zeroes as positional gaps rather than trying to manufacture them individually.

For digit `9`, the general deletion construction would require zero leading ones, which is not a valid deletion operation. The algorithm handles this case separately by adding `10^k` objects, producing an increase of `9 * 10^k`. This directly prepends the digit `9`, so no deletion is needed.

For digit `1`, the opposite extreme occurs. We need eight leading ones when constructing it from zero. For example, `0 + 9 * 12345679 = 111111111`; deleting eight leading ones leaves `1`. The number `12345679` is not arbitrary. Its digit sum is `37`, and the resulting product has exactly the required decimal structure.

For the maximum input `1000000000`, the first phase only performs the construction for its initial `1`. The operation uses `10^9`, producing `10^10`, and deleting the leading one gives zero. The remaining zeroes need no operations. This case also explains why the `10^18` bound is safe: the only ten-digit input allowed by the constraint has this special form, so we never encounter a ten-digit number beginning with a large nonzero digit.

The final subtlety is that the output sequence need not be minimal. For `1 -> 9`, the sample has a two-operation construction, while the simple `a -> 0 -> b` construction uses three. Rejecting the latter because it is longer would misunderstand the output requirement. The only limits that matter are legality, the `1000` operation bound, the `10^18` intermediate bound, and reaching the exact target.
