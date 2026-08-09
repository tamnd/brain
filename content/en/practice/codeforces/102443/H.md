---
title: "CF 102443H - Planet Nine"
description: "The register starts at a and must end at b. There are only two kinds of events. An addition increases the register by a positive multiple of 9, while a deletion removes some leading decimal digits, and every removed digit must be 1."
date: "2026-08-09T18:09:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102443
codeforces_index: "H"
codeforces_contest_name: "2019-2020 Russia Team Open, High School Programming Contest (VKOSHP 19)"
rating: 0
weight: 102443
solve_time_s: 479
verified: true
draft: false
---

[CF 102443H - Planet Nine](https://codeforces.com/problemset/problem/102443/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The register starts at `a` and must end at `b`. There are only two kinds of events. An addition increases the register by a positive multiple of 9, while a deletion removes some leading decimal digits, and every removed digit must be `1`. The output is any valid sequence of at most 1000 such events. Every intermediate register value must stay at most 10 18.

The useful quantity is the remainder modulo 9. Adding 9x never changes it. If we delete `y` leading ones from a decimal number, the removed prefix is congruent to `y` modulo 9, and every power of 10 is also congruent to 1 modulo 9. Thus deleting `y` digits decreases the remainder by exactly `y` modulo 9. This is the central arithmetic property behind the construction.

The bounds on `a` and `b` are small enough that their decimal representations have at most 10 digits. The intermediate-value limit is much larger, 10 18, so we have room to temporarily create numbers with considerably more digits. The operation limit is 1000, which rules out any search through long operation sequences, but the construction below needs only a few dozen operations.

There are several edge cases that can make a seemingly reasonable construction fail. For `0 0`, the correct answer is simply `Stable` followed by `0`, because no event is needed. A program that always emits a positive addition would unnecessarily change the register.

For `1 9`, the two values have different remainders modulo 9. Merely adding nines cannot change `1` into `9`. One valid construction is the sample's `+ 2`, which changes `1` to `19`, followed by `- 1`, which removes the leading `1` and leaves `9`. A program that checks only whether `a <= b` and then adds `(b-a)/9` would incorrectly reject this case.

The case `0 1` is another useful boundary. There is no direct addition because 1 is not a multiple of 9. We can repeatedly create a leading `1` and remove it, changing the remainder one step at a time, eventually reaching 1. A construction is `0 -> 18 -> 8 -> 17 -> 7 -> ... -> 11 -> 1`. The temporary values are larger than the final value, but they are still far below 10 18.

Finally, values such as `1000000000` need care because they have 10 digits. A construction that creates a number with too many leading ones can exceed the 10 18 limit. The optimal construction deliberately uses a repunit of at most 18 digits, whose value is below 1.12⋅10 17.

## Approaches

A brute-force approach could model every possible register value as a state and try both operation types from every state. This fails immediately because an addition has a huge range of possible arguments. Even from zero, there are

⌊ 9 10 18 ​ ⌋=111111111111111111

possible positive additions that respect the intermediate-value bound. Searching operation sequences is even worse: if we artificially restricted ourselves to only two fixed choices at every step, a depth-1000 search would already contain 2 1000 sequences. The actual operation set is much larger, so brute force is not a meaningful option.

The brute force works conceptually because it would eventually discover a valid sequence if one exists. The useful observation is that we do not need to search for the additions at all. We can choose them algebraically.

Suppose the current value is `v`, and let it have `d` decimal digits. Define

t=(v−1)mod9.

Now consider

T=10 d +t.

The number `T` starts with the digit `1`, and

T≡1+t≡v(mod9).

Consequently `T-v` is a positive multiple of 9. We can reach `T` with one addition, delete its first digit, and obtain exactly `t`. Thus two operations transform any `v` into a number whose remainder modulo 9 is one smaller than the old remainder.

This gives us a deterministic way to adjust the modulo 9 remainder until it matches `b`. Once the remainder matches and the current value does not exceed `b`, a single addition reaches `b`.

There is one complication. If `a` is at least as large as `b`, the temporary remainder-adjustment process might pass through values larger than `b`, and the final addition could become negative. We avoid that completely by first sending `a` to zero. To do this, choose a decimal repunit

R L ​ =11…1

whose length `L` is congruent to `a` modulo 9 and whose value is at least `a`. Such an `L` always exists with L≤18. Since R L ​ ≡L(mod9), the difference `R_L-a` is divisible by 9. We add that difference, then delete all `L` leading ones, reaching zero. This is exactly the two-stage construction described in the official editorial.

From zero we can safely use the remainder-adjustment process to reach the residue of `b`, then add the remaining multiple of 9. The total number of events stays tiny.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the operation limit, with >10 17 possible first additions | Exponential | Too slow |
| Optimal | O(log 10 ​ max(a,b)) | O(log 10 ​ max(a,b)) for the output | Accepted |

## Algorithm Walkthrough

1. If `a == b`, output `Stable` and zero operations. No construction is necessary.
2. If `a < b`, keep the current value equal to `a` and repeatedly adjust its remainder modulo 9. For the current value `v`, compute its number of digits `d`, then set `t = (v - 1) % 9` and `T = 10^d + t`.
3. Add `(T-v)/9` nines. The result is exactly `T`, and `T` begins with `1`. The quotient is positive because `T > v`, while it is integral because `T` and `v` have the same remainder modulo 9.
4. Delete one leading digit. Since that digit is `1`, the operation is legal, and the register becomes `t`. Its remainder is one smaller than the previous remainder modulo 9.
5. Repeat the previous two steps until the current value has the same remainder modulo 9 as `b`. At most nine such transformations are needed because every transformation decreases the remainder by one modulo 9.
6. Add `(b-v)/9`. The remainders now match, so the quotient is an integer. Because `a < b`, after the remainder-adjustment phase the current value is at most 8, hence it is no greater than `b`. The final addition is consequently positive unless the values are already equal.
7. If `a > b`, first construct a repunit `R` with at most 18 digits such that `R >= a` and `R % 9 == a % 9`. Such a length can be found by checking lengths from 1 through 18.
8. Add `(R-a)/9` nines, unless `R == a`, in which case no addition is needed. The register is now exactly `R`.
9. Delete all `len(R)` leading digits. Every digit is `1`, so the deletion is valid and changes the register to zero.
10. Starting from zero, apply the same remainder-adjustment procedure toward `b`, then perform the final addition from the matching residue to `b`.

The invariant is simple. Every constructed addition changes the register by a multiple of 9, so it preserves the current remainder. Every deletion removes exactly one leading `1` in our construction, so it decreases the remainder by one modulo 9. The constructed number before each deletion is always `10^d+t`, meaning its first digit is guaranteed to be `1` and the deletion is legal. Once the remainder equals `b % 9`, the difference from the current value to `b` is a multiple of 9, so the final addition reaches `b` exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 10**18

def add_to_repunit(a, ops):
    """Transform a to zero using one repunit."""
    if a == 0:
        return 0

    # Find a repunit R >= a with R % 9 == a % 9.
    rep = 0
    chosen = None

    for length in range(1, 19):
        rep = rep * 10 + 1
        if rep >= a and rep % 9 == a % 9:
            chosen = rep
            chosen_len = length
            break

    # Such a repunit always exists for a <= 1e9.
    if chosen is None:
        raise RuntimeError("No suitable repunit")

    if chosen > a:
        x = (chosen - a) // 9
        ops.append(("+", x))

    ops.append(("-", chosen_len))
    return 0

def adjust_residue(cur, target_residue, ops):
    """
    Repeatedly decrease cur's residue modulo 9 until it equals
    target_residue. Each iteration uses +x, -1.
    """
    while cur % 9 != target_residue:
        d = len(str(cur))
        t = (cur - 1) % 9
        target = 10**d + t

        x = (target - cur) // 9
        if x <= 0:
            raise RuntimeError("Invalid positive addition")

        ops.append(("+", x))
        ops.append(("-", 1))

        cur = t

    return cur

def solve():
    a, b = map(int, input().split())

    if a == b:
        print("Stable")
        print(0)
        return

    ops = []

    if a >= b:
        # First reach zero.
        cur = add_to_repunit(a, ops)

        # Then construct b from zero.
        cur = adjust_residue(cur, b % 9, ops)

        if cur < b:
            x = (b - cur) // 9
            ops.append(("+", x))
            cur = b
    else:
        # a < b, so we can directly adjust the residue and then add.
        cur = adjust_residue(a, b % 9, ops)

        if cur < b:
            x = (b - cur) // 9
            ops.append(("+", x))
            cur = b

    assert cur == b
    assert len(ops) <= 1000

    print("Stable")
    print(len(ops))
    for typ, x in ops:
        print(typ, x)

if __name__ == "__main__":
    solve()
```

The `add_to_repunit` function implements the first half of the construction for `a >= b`. It searches only 18 possible repunit lengths. For each candidate, divisibility by 9 follows from `rep % 9 == a % 9`, so the required addition count is an integer.

The `adjust_residue` function implements the key two-operation transition. For `cur` with `d` digits, `10**d + t` has exactly `d+1` digits and starts with `1`. The addition count is computed before emitting the operation, which avoids any dependence on decimal carry behavior.

After `- 1`, the new value is exactly `t`, because removing the first digit from `10^d+t` leaves the decimal representation of `t`, including the possibility that `t` is zero.

The 18-digit repunit is safely below 10 18, and all other temporary values generated from inputs of at most 10 digits are at most 10 10 +8. Python integers also have arbitrary precision, so there is no arithmetic overflow during construction.

The operation order matters. The addition must come before the deletion because the deletion is only legal when the leading digit is `1`. The final addition is performed only after the modulo 9 residues agree, guaranteeing that its argument is an integer.

## Worked Examples

### Sample 1

For input `0 0`, the values already coincide.

| Current | Target | Action | New Current |
| --- | --- | --- | --- |
| 0 | 0 | none | 0 |

The algorithm immediately prints zero operations. This is the smallest possible construction and avoids producing an unnecessary positive operation.

### Sample 2

For input `1 9`, we have `1 < 9`, and the target remainder is `0`.

| Current | `current % 9` | `t = (current-1) % 9` | Constructed value | Action | New Current |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 10 | `+ 1`, `- 1` | 0 |
| 0 | 0 | 0 | 0 | `+ 1` | 9 |

The first pair changes the remainder from 1 to 0. The final addition changes 0 to 9. The sample uses a shorter construction, `+ 2`, `- 1`, but the problem accepts any valid sequence.

The trace demonstrates why minimizing the number of operations is unnecessary. The construction may use a few extra events, but it stays far below the limit of 1000.

### A boundary example

Consider `0 1`.

| Current | `current % 9` | `t` | Constructed value | New Current |
| --- | --- | --- | --- | --- |
| 0 | 0 | 8 | 18 | 8 |
| 8 | 8 | 7 | 17 | 7 |
| 7 | 7 | 6 | 16 | 6 |
| 6 | 6 | 5 | 15 | 5 |
| 5 | 5 | 4 | 14 | 4 |
| 4 | 4 | 3 | 13 | 3 |
| 3 | 3 | 2 | 12 | 2 |
| 2 | 2 | 1 | 11 | 1 |

The desired remainder is 1, so the process stops at 1. No final addition is needed.

This example exercises the case where the target is extremely small even though the construction temporarily creates two-digit numbers. The largest temporary value is only 18.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(logmax(a,b)) | At most 18 repunit checks and at most 9 residue-adjustment rounds, each using constant-size integers |
| Space | O(logmax(a,b)) | The operation list contains only a constant number of operations relative to the decimal digit count |

The actual operation count is at most 21 with this implementation. The initial repunit conversion uses at most two events, and the residue adjustment uses at most 18 events, followed by one final addition. Thus the required limit of 1000 operations is extremely loose. All temporary values are below 10 18, so the construction also satisfies the register bound.

## Test Cases

Because the output is not unique, tests should validate the produced operation sequence rather than compare it with one fixed output.

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

def verify(inp: str, out: str) -> bool:
    a, b = map(int, inp.split())
    lines = out.strip().splitlines()

    assert lines[0] == "Stable"
    n = int(lines[1])
    assert 0 <= n <= 1000
    assert len(lines) == n + 2

    cur = a

    for line in lines[2:]:
        parts = line.split()
        assert len(parts) == 2

        typ, x = parts
        x = int(x)
        assert x > 0

        if typ == "+":
            cur += 9 * x
            assert cur <= 10**18

        elif typ == "-":
            s = str(cur)
            y = x

            assert 1 <= y <= len(s)
            assert all(ch == "1" for ch in s[:y])

            s = s[y:]
            cur = int(s) if s else 0
            assert cur <= 10**18

        else:
            assert False, "unknown operation"

    assert cur == b
    return True

# Provided sample 1 has an exact canonical output.
assert run("0 0") == "Stable\n0\n", "sample 1"

# Provided sample 2 has many valid outputs, so verify its semantics.
assert verify("1 9", run("1 9")), "sample 2"

# Minimum-size input.
assert verify("0 0", run("0 0")), "minimum values"

# All-equal nonzero values.
assert verify("123456789 123456789", run("123456789 123456789")), "equal values"

# Maximum input values.
assert verify("1000000000 1000000000", run("1000000000 1000000000")), "maximum equal values"

# Large value going down to zero, exercising the repunit construction.
assert verify("1000000000 0", run("1000000000 0")), "repunit boundary"

# Different residues with a very small target.
assert verify("0 1", run("0 1")), "small target"

# Adjacent boundary near 1e9.
assert verify("999999999 1000000000", run("999999999 1000000000")), "large adjacent values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` | `Stable`, zero operations | Immediate equality and minimum values |
| `1 9` | Any valid `Stable` construction | Provided sample and residue change |
| `123456789 123456789` | `Stable`, zero operations | Equal nonzero values |
| `1000000000 1000000000` | `Stable`, zero operations | Maximum input boundary |
| `1000000000 0` | Any valid `Stable` construction | Repunit conversion and deletion of many leading ones |
| `0 1` | Any valid `Stable` construction | Small target with a different modulo 9 residue |
| `999999999 1000000000` | Any valid `Stable` construction | Large adjacent values and repeated residue adjustment |

## Edge Cases

For `0 0`, the equality check terminates before any arithmetic construction. The register remains zero, so the exact output is `Stable` followed by `0`.

For `1 9`, direct addition is impossible because the difference is 8, not a multiple of 9. The algorithm first changes the remainder from 1 to 0 by constructing 10 and deleting its leading `1`, obtaining zero. It then adds one multiple of 9 and reaches 9. The temporary value 10 is valid.

For `0 1`, the algorithm starts with remainder 0 while the target has remainder 1. Each `+x, -1` pair decreases the remainder by one modulo 9. The sequence of values after deletions is `8, 7, 6, 5, 4, 3, 2, 1`, so the target residue is reached after eight rounds. Every addition constructs `18`, `17`, ..., `11`, respectively, followed by deletion of the leading `1`.

For `1000000000 0`, the algorithm chooses the 10-digit repunit `1111111111`. It has the same remainder as `1000000000`, and it is larger, so the difference is divisible by 9. Adding that difference reaches the repunit, then deleting all ten `1` digits produces zero. The largest temporary value is only `1111111111`.

For `999999999 1000000000`, the initial value has remainder 0 while the target has remainder 1. The residue-adjustment procedure first produces 8, then 7, continuing until 1. From there, the difference to `1000000000` is divisible by 9, so one final addition reaches the target exactly. This demonstrates that the intermediate register value does not need to stay below the final target, only below the required 10 18 bound.
