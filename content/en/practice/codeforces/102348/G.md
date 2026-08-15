---
title: "CF 102348G - Swap Letters"
description: "We have two strings s and t of the same length. Every position contains either a or b. One operation chooses any position in s and any position in t, then swaps the two characters."
date: "2026-08-15T17:31:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "G"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 224
verified: false
draft: false
---

[CF 102348G - Swap Letters](https://codeforces.com/problemset/problem/102348/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We have two strings `s` and `t` of the same length. Every position contains either `a` or `b`. One operation chooses any position in `s` and any position in `t`, then swaps the two characters. The goal is to make the two entire strings identical using as few operations as possible, while also printing one optimal sequence of swaps.

The useful way to look at a position is to compare the two characters occupying it. If they already agree, that position needs no attention. If they disagree, the position is either of type `ab`, meaning `s[i] = a` and `t[i] = b`, or type `ba`, meaning `s[i] = b` and `t[i] = a`.

The length can reach `2 * 10^5`, so an algorithm with quadratic work can perform around `4 * 10^10` iterations in the worst case, far beyond what a 2-second contest limit allows. We need a solution whose work is essentially linear in `n`, with only a small amount of bookkeeping per position. Since the alphabet contains only two characters, the mismatch types give us exactly the structure needed to achieve that.

There are several edge cases that can make a seemingly reasonable implementation fail. First, an odd number of mismatches is impossible. For example,

```
1
a
b
```

has one `ab` mismatch. There is only one `a` among the two characters, and every final equal pair contains either zero or two `a` characters. No sequence of swaps can change the total number of `a` characters, so the correct output is `-1`. A careless implementation that simply pairs mismatches without checking parity may leave one position unresolved.

A second edge case occurs when both mismatch types have odd counts. For example,

```
2
ab
ba
```

has one `ab` position and one `ba` position. A direct one-swap pairing cannot fix them because their orientations are opposite. However, two swaps are enough. Swap `s[1]` with `t[1]`, turning the first mismatch from `ab` into `ba`, then swap `s[1]` with `t[2]`. Both positions become equal. A solution that only pairs equal mismatch types would incorrectly conclude that this case is impossible.

A third edge case is when there are no mismatches at all:

```
3
aba
aba
```

The correct answer is `0`, with no operation lines. Implementations that assume there is at least one mismatch can accidentally access an empty list or print an unnecessary operation.

## Approaches

A direct approach is to repeatedly find a mismatch and search for another position that can be fixed with it. For example, after finding an `ab` position, we can scan the remaining positions looking for another `ab` position and use one cross-string swap to resolve both. If no such position exists, we can handle the special case involving a `ba` position with two swaps.

This strategy is logically sound, because every search is looking for a valid partner and each successful operation reduces the number of mismatches. The problem is the repeated scanning. In the worst case, there can be `Θ(n)` mismatches, and finding each partner may inspect `Θ(n)` positions. The total number of character comparisons can reach `Θ(n²)`, which is about `4 * 10^10` for `n = 2 * 10^5`. That is far too much for the time limit.

The key observation is that we do not need to search for partners dynamically. The only information relevant to an incorrect position is whether it is `ab` or `ba`. We can collect all positions of each type in one pass.

Two `ab` positions can always be fixed together with one operation. Suppose positions `x` and `y` are both `ab`. Swapping `s[x]` with `t[y]` exchanges `a` and `b`. At `x`, `s[x]` changes from `a` to `b`, matching `t[x]`. At `y`, `t[y]` changes from `b` to `a`, matching `s[y]`. The same argument works for two `ba` positions.

This immediately handles every pair of equal mismatch types. The only remaining situation is when both mismatch lists contain one unpaired position. Since the total number of mismatches must be even, these two lists either both have even size or both have odd size. In the odd case, let `x` be the remaining `ab` position and `y` the remaining `ba` position. First swap `s[x]` with `t[x]`. This changes position `x` from `ab` into `ba`. Now both `x` and `y` are `ba`, so a second swap between `s[x]` and `t[y]` fixes both.

The lower bound on the number of operations is also simple. One operation can fix at most two currently mismatched positions, so pairing two equal mismatches requires at least one operation and is optimal. When one `ab` and one `ba` remain, one operation cannot solve both, because their orientations are opposite. The two-operation construction above is consequently optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated search for partners | `O(n²)` | `O(n)` | Too slow |
| Store mismatch positions and pair them | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Scan every position from left to right. If `s[i] == t[i]`, ignore it. If `s[i] == 'a'` and `t[i] == 'b'`, append `i` to the `ab` list. Otherwise append `i` to the `ba` list. This separates every problematic position according to the only two possible mismatch orientations.
2. Check the parity of the two lists. The total number of `a` characters in both strings is preserved by every swap, and a final equal pair contains either zero or two `a` characters. Thus the total number of `a` characters must be even. Equivalently, the total number of mismatches must be even. Since the two mismatch counts have the same parity whenever their sum is even, it is enough to reject when `len(ab) + len(ba)` is odd.
3. Pair consecutive positions in `ab`. For every pair `ab[2j]` and `ab[2j + 1]`, output a swap between `s[ab[2j]]` and `t[ab[2j + 1]]`. One operation fixes both positions, so this is optimal for that pair.
4. Pair consecutive positions in `ba` in exactly the same way. For positions `x = ba[2j]` and `y = ba[2j + 1]`, swap `s[x]` with `t[y]`. Both mismatches become equal positions after the operation.
5. If both mismatch lists have odd length, one position remains in each list. Let those positions be `x = ab[-1]` and `y = ba[-1]`. First output `(x, x)`, which swaps the two characters at position `x` and changes its type from `ab` to `ba`. Then output `(x, y)`. The two remaining `ba` mismatches are now paired and become equal.
6. Convert every stored zero-based index to one-based indexing when printing. The output count is simply the length of the generated operation list.

### Why it works

After the initial scan, every mismatch belongs to exactly one of the two lists. A swap between two positions of the same mismatch type fixes both of them without affecting any already-fixed position. Thus all even-sized portions of the two lists can be removed optimally in pairs.

If both lists are odd, exactly one position remains in each. The first extra swap changes the remaining `ab` mismatch into a `ba` mismatch, after which the two remaining mismatches have the same type and can be fixed by one more swap. If the total mismatch count is odd, no solution exists because every operation preserves the parity condition required for the two strings to become identical.

Every operation used on two equal mismatch types fixes two mismatches, which is the maximum possible. The only unavoidable exception is the final opposite pair, where two operations are necessary. Hence the constructed sequence has the minimum possible length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()
    t = input().strip()

    ab = []
    ba = []

    for i in range(n):
        if s[i] == t[i]:
            continue
        if s[i] == 'a':
            ab.append(i)
        else:
            ba.append(i)

    if (len(ab) + len(ba)) % 2:
        print(-1)
        return

    operations = []

    for i in range(0, len(ab) - 1, 2):
        operations.append((ab[i] + 1, ab[i + 1] + 1))

    for i in range(0, len(ba) - 1, 2):
        operations.append((ba[i] + 1, ba[i + 1] + 1))

    if len(ab) % 2 == 1:
        x = ab[-1] + 1
        y = ba[-1] + 1
        operations.append((x, x))
        operations.append((x, y))

    out = [str(len(operations))]
    out.extend(f"{x} {y}" for x, y in operations)
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first loop only records mismatches, so equal positions never enter the later logic. This is useful because every operation generated afterward can be reasoned about entirely in terms of the mismatch lists.

The parity check is performed before constructing operations. Since each operation only exchanges existing characters, it cannot change the total number of `a` characters in the two strings. A final state with equal strings necessarily has an even total number of `a` characters, so an odd mismatch count proves impossibility.

The two pairing loops use `range(0, len(list) - 1, 2)`. The upper bound deliberately stops before the final element when the list has odd length. That final element is reserved for the special two-operation construction.

The special case uses the same index twice in the first operation, such as `(x, x)`. This is legal because the first index belongs to `s` and the second belongs to `t`, so the operation swaps `s[x]` and `t[x]`. It is not a no-op. For an `ab` mismatch, it changes the position into `ba`.

All internal indices are zero-based because Python strings use zero-based indexing. They are increased by one only when stored in the output, matching the one-based positions required by the problem.

No mutation of `s` or `t` is necessary. The operations are derived from the original mismatch classification, and each generated operation is known mathematically to fix its intended positions. This also avoids accidental changes to later classification decisions.

## Worked Examples

### Sample 1

The input is:

```
4
abab
aabb
```

The mismatch classification is:

| Index | `s[i]` | `t[i]` | Type | `ab` list | `ba` list |
| --- | --- | --- | --- | --- | --- |
| 0 | a | a | equal | [] | [] |
| 1 | b | a | `ba` | [] | [1] |
| 2 | a | b | `ab` | [2] | [1] |
| 3 | b | b | equal | [2] | [1] |

There is one `ab` and one `ba`, so both lists are odd. The algorithm uses the special case:

| Step | Operation, zero-based | Purpose |
| --- | --- | --- |
| 1 | `(2, 2)` | Change position 2 from `ab` to `ba` |
| 2 | `(2, 1)` | Pair the two `ba` mismatches |

Converted to one-based indexing, the output is:

```
2
3 3
3 2
```

The first operation changes the strings from `abab` and `aabb` to `abbb` and `aaab`. The second operation makes both strings `abab`. The two operations are necessary because the original mismatches have opposite orientations.

### Sample 2

The input is:

```
1
a
b
```

The trace is:

| Index | `s[i]` | `t[i]` | Type | `ab` | `ba` | Total mismatches |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | a | b | `ab` | [0] | [] | 1 |

The mismatch count is odd, so the algorithm immediately prints:

```
-1
```

There cannot be a valid sequence because the only two characters contain exactly one `a`, while two equal strings would contain an even number of `a` characters across both strings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Each position is scanned once, and each mismatch is processed once when operations are generated. |
| Space | `O(n)` | The two mismatch lists and the resulting operation list contain at most `O(n)` entries. |

With `n <= 2 * 10^5`, the algorithm performs only a few linear passes over the strings. Its worst-case work is proportional to roughly `n`, rather than the tens of billions of inspections produced by a quadratic search, so it comfortably fits the 2-second limit. The memory usage is also linear and well within 256 MB.

## Test Cases

Because optimal operation sequences are not unique, a robust test harness should not compare a successful output character-for-character with the sample output. Instead, it should verify that the output has the correct minimum number of operations and that applying those operations really produces equal strings.

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    t = input().strip()

    ab = []
    ba = []

    for i in range(n):
        if s[i] == t[i]:
            continue
        if s[i] == 'a':
            ab.append(i)
        else:
            ba.append(i)

    if (len(ab) + len(ba)) % 2:
        print(-1)
        return

    operations = []

    for i in range(0, len(ab) - 1, 2):
        operations.append((ab[i] + 1, ab[i + 1] + 1))

    for i in range(0, len(ba) - 1, 2):
        operations.append((ba[i] + 1, ba[i + 1] + 1))

    if len(ab) % 2 == 1:
        x = ab[-1] + 1
        y = ba[-1] + 1
        operations.append((x, x))
        operations.append((x, y))

    print(len(operations))
    for x, y in operations:
        print(x, y)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

def validate(inp: str, out: str):
    data = inp.strip().splitlines()
    n = int(data[0])
    original_s = data[1]
    original_t = data[2]

    lines = out.strip().splitlines()

    if not lines:
        raise AssertionError("empty output")

    if lines[0].strip() == "-1":
        mismatches = sum(a != b for a, b in zip(original_s, original_t))
        assert mismatches % 2 == 1, "reported impossible for a solvable case"
        return

    k = int(lines[0])
    assert len(lines) == k + 1, "wrong number of operation lines"

    ab = []
    ba = []

    for i in range(n):
        if original_s[i] == original_t[i]:
            continue
        if original_s[i] == 'a':
            ab.append(i)
        else:
            ba.append(i)

    expected = len(ab) // 2 + len(ba) // 2
    if len(ab) % 2:
        expected += 2

    assert k == expected, f"not minimum: got {k}, expected {expected}"

    s = list(original_s)
    t = list(original_t)

    for line in lines[1:]:
        x, y = map(int, line.split())
        assert 1 <= x <= n
        assert 1 <= y <= n
        x -= 1
        y -= 1
        s[x], t[y] = t[y], s[x]

    assert s == t, "operations did not make strings equal"

# Provided samples.
sample1 = """4
abab
aabb
"""
validate(sample1, run(sample1))

sample2 = """1
a
b
"""
validate(sample2, run(sample2))

sample3 = """8
babbaabb
abababaa
"""
validate(sample3, run(sample3))

# Minimum-size solvable case: already equal.
case1 = """1
a
a
"""
validate(case1, run(case1))
assert run(case1).strip() == "0"

# Minimum-size impossible case: one mismatch.
case2 = """1
a
b
"""
assert run(case2).strip() == "-1"

# Opposite mismatch types. This catches the special two-operation case.
case3 = """2
ab
ba
"""
validate(case3, run(case3))

# Maximum-size input, with all positions equal.
case4 = "200000\n" + "a" * 200000 + "\n" + "a" * 200000 + "\n"
assert run(case4).strip() == "0"

# Boundary case with two equal mismatch types.
case5 = """4
aabb
bbaa
"""
validate(case5, run(case5))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / a / a` | `0` | Minimum size and already-equal strings |
| `1 / a / b` | `-1` | Minimum impossible case and odd mismatch count |
| `2 / ab / ba` | `2` operations | The special case where both mismatch types occur once |
| `n = 200000`, both strings all `a` | `0` | Maximum input size and linear-time behavior |
| `4 / aabb / bbaa` | `2` operations | Pairing multiple mismatches of the same type |

The validator applies every printed swap to mutable copies of the strings, then checks equality at the end. It also computes the theoretical minimum from the mismatch counts. This catches solutions that happen to make the strings equal but use unnecessary operations, as well as solutions that print invalid indices or an incorrect special-case sequence.

## Edge Cases

When the two strings are already equal, there are no mismatch positions. For example,

```
3
aba
aba
```

produces empty `ab` and `ba` lists. Both pairing loops execute zero times, the special case is skipped, and the answer is `0`. No operation is needed or allowed in an optimal answer.

When there is an odd total number of mismatches, the answer is impossible. For

```
1
a
b
```

the `ab` list is `[0]` and the `ba` list is empty. The total is one, so the algorithm prints `-1` before trying to access a partner. This is the parity condition caused by preservation of the total number of `a` characters.

When both mismatch types have odd size, the total mismatch count is even, so the instance is solvable but requires the special construction. For

```
2
ab
ba
```

the lists are `ab = [0]` and `ba = [1]`. The operation `(1, 1)` changes the first position from `ab` to `ba`. The operation `(1, 2)` then pairs the two `ba` positions. Exactly two operations are used, and one operation cannot solve the original opposite orientations.

When a mismatch list has an even size greater than zero, every position in it can be handled independently in pairs. For

```
4
aabb
bbaa
```

the mismatches are `ab` at positions `1` and `2`, and `ba` at positions `3` and `4`. The algorithm swaps `(1, 2)` for the first pair and `(3, 4)` for the second pair. Each operation fixes two mismatches, giving the minimum of two operations.

The one-based indexing boundary is also handled explicitly. Internally, position `0` represents the first character, but every stored operation adds one before printing. Thus a mismatch at the first character is printed using index `1`, while a mismatch at the final character of a length-`n` string is printed using index `n`. The test harness checks both bounds for every generated operation.
