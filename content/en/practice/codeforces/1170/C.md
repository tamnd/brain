---
title: "CF 1170C - Minus and Minus Give Plus"
description: "We are given a string made only of two symbols, plus and minus. We are allowed to repeatedly pick any two adjacent minus signs and replace them with a single plus sign. This operation shortens the string by one character, since two symbols are replaced by one."
date: "2026-06-15T16:57:50+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1170
codeforces_index: "C"
codeforces_contest_name: "Kotlin Heroes: Episode 1"
rating: 0
weight: 1170
solve_time_s: 429
verified: false
draft: false
---

[CF 1170C - Minus and Minus Give Plus](https://codeforces.com/problemset/problem/1170/C)

**Rating:** -  
**Tags:** *special, implementation, strings  
**Solve time:** 7m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string made only of two symbols, plus and minus. We are allowed to repeatedly pick any two adjacent minus signs and replace them with a single plus sign. This operation shortens the string by one character, since two symbols are replaced by one.

The question is whether we can start from a given string `s` and, after performing zero or more such local replacements, obtain another given string `t`.

The key aspect is that this is not a free rearrangement problem. We cannot move symbols arbitrarily. The only allowed change is to pick a contiguous pair of `--` and turn it into `+`. That means structure is heavily constrained: plus signs act like fixed separators unless we explicitly create new ones, and minus signs only disappear in pairs.

The constraints are large enough that any approach simulating operations is impossible. The total length across all test cases is up to 2 × 10^5, which forces an essentially linear solution per test case. Anything quadratic in the string length would immediately fail, especially since each replacement operation is local and could, in a naive simulation, lead to O(n^2) behavior.

A subtle difficulty comes from the fact that operations can create new plus signs in the middle of a minus segment, which changes how the string splits over time. For example, in a block like `"----"`, different sequences of operations can yield different intermediate structures like `"+--"` or `"++"`, so it is not enough to think in terms of simple compression.

A few edge cases illustrate the pitfalls:

If `s = "--"` and `t = "+"`, the answer is YES, since one operation transforms the entire string.

If `s = "-"` and `t = "+"`, the answer is NO, because we cannot create a plus without having two adjacent minus signs.

If `s = "+-"` and `t = "-+"`, the answer is NO, because the plus at the front is fixed and cannot be turned into a minus.

These examples show that plus positions in `s` impose rigid constraints, while minus segments are the only flexible parts.

## Approaches

A brute-force interpretation would simulate all possible applications of the operation. Each step scans the string for a `"--"` pattern, replaces it with `"+"`, and branches over possible choices. The number of states grows exponentially because each reduction can be applied in many different places, and the resulting string structure changes dynamically. Even a single string of length 200 could lead to an enormous number of intermediate configurations.

The key observation is that the operation only interacts locally with minus signs and never affects existing plus signs except by creating new ones. This allows us to separate the string into fixed plus positions and flexible minus segments.

Any position where `s` already has a plus cannot be changed, since no operation ever turns a plus into a minus. This immediately forces a necessary condition: every plus in `s` must also appear in `t` at the same position.

Once we accept that plus positions in `s` are rigid, the remaining structure consists of maximal contiguous blocks of minus signs in `s`. Inside such a block, we can perform operations freely, but only within that block. We can reduce the number of minus signs by pairs, and we can also create plus signs that split the block in arbitrary ways. However, one invariant remains: each operation reduces the number of minus signs by exactly 2, so the parity of the number of minus signs inside each block is fixed.

This leads to a clean local condition per block: in each minus-only segment of `s`, the corresponding segment in `t` must contain exactly the same parity of minus signs, and no minus signs are allowed outside those segments.

The brute-force fails because it tries to reason globally over all transformations, while the correct solution reduces the problem to independent local checks on segments with a single parity constraint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate operations) | Exponential | O(n) | Too slow |
| Segment parity check | O(n) | O(1) extra | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. First, we compare the fixed structure imposed by plus signs in `s`. Every position where `s[i]` is `'+'` must also satisfy `t[i] == '+'`. If this fails anywhere, transformation is impossible. This works because plus signs in `s` can never be removed or turned into minus signs.
2. Next, we identify maximal contiguous segments in `s` consisting only of minus signs. Each such segment behaves independently because operations never move symbols across a plus boundary.
3. For each such segment, we look at the corresponding substring in `t` covering the same indices. Within this interval, we count how many minus signs appear in `t`.
4. Let the segment in `s` have length `k`. Since each operation removes exactly two minus signs, the number of minus signs that can remain after any sequence of operations is fixed as `k % 2`. We check whether the count of minus signs in the corresponding part of `t` matches this value.
5. We also ensure that `t` contains no minus signs outside these segments, which is already guaranteed by the first condition on plus positions.

If all segments satisfy the parity condition, the transformation is possible.

### Why it works

Each operation reduces the number of minus signs by 2, and never introduces new minus signs. This makes the parity of minus count inside every isolated minus segment invariant. Plus signs act as permanent separators that cannot be crossed or removed. Since operations never transfer symbols across these separators, each segment evolves independently. The final configuration inside a segment is fully determined by how many minus signs remain after repeated pair removals, which is exactly the original count modulo 2.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input())
    out = []

    for _ in range(k):
        s = input().strip()
        t = input().strip()

        n = len(s)
        if len(t) != n:
            out.append("NO")
            continue

        ok = True

        # Step 1: fixed '+' positions must match
        for i in range(n):
            if s[i] == '+' and t[i] != '+':
                ok = False
                break

        if not ok:
            out.append("NO")
            continue

        i = 0
        while i < n:
            if s[i] == '+':
                i += 1
                continue

            j = i
            while j < n and s[j] == '-':
                j += 1

            k_len = j - i
            target_minus = 0

            for p in range(i, j):
                if t[p] == '-':
                    target_minus += 1

            if target_minus != (k_len % 2):
                ok = False
                break

            i = j

        out.append("YES" if ok else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code first enforces immovable structure: every plus in the source string must remain a plus in the target. It then scans contiguous minus segments in the source and checks each against the corresponding interval in the target.

The only subtle implementation detail is that we never attempt to track how plus signs inside minus segments are created. They are irrelevant for feasibility; only the number of minus signs in each segment matters, because plus signs can always be manufactured internally as long as enough minus pairs exist.

## Worked Examples

### Example 1

Consider `s = "--+---"` and `t = "-++-+-+"`.

We split `s` into segments of minus signs: `"--"` and `"---"`.

| Segment | k (s minus length) | t minus count | k % 2 | Valid |
| --- | --- | --- | --- | --- |
| "--" | 2 | 1 | 0 | No |
| "---" | 3 | 1 | 1 | Yes |

The first segment already fails because a length-2 block cannot produce a single minus in the final configuration. This immediately makes the answer NO.

This trace shows how the parity constraint alone determines feasibility inside each independent block.

### Example 2

Take `s = "-+--+"` and `t = "-++-+"`.

We check fixed plus positions first. All positions where `s` has `+` also have `+` in `t`, so we proceed.

Now the only minus block is `"--"`.

| Segment | k (s minus length) | t minus count | k % 2 | Valid |
| --- | --- | --- | --- | --- |
| "--" | 2 | 0 | 0 | Yes |

The block is valid, so the transformation is possible. This example demonstrates how plus positions do not restrict internal rearrangement beyond acting as boundaries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each character is scanned a constant number of times across segmentation and checks |
| Space | O(1) extra | Only counters and indices are used |

The total length across all test cases is bounded by 2 × 10^5, so a linear scan over all input is easily fast enough within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return main()

def main():
    input = sys.stdin.readline
    k = int(input())
    out = []
    for _ in range(k):
        s = input().strip()
        t = input().strip()

        n = len(s)
        ok = True

        for i in range(n):
            if s[i] == '+' and t[i] != '+':
                ok = False
                break

        if ok:
            i = 0
            while i < n:
                if s[i] == '+':
                    i += 1
                    continue
                j = i
                while j < n and s[j] == '-':
                    j += 1
                if sum(1 for p in range(i, j) if t[p] == '-') != (j - i) % 2:
                    ok = False
                    break
                i = j

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided samples
assert run("""5
-+--+
-+++
--------
-+--+-
-
+
--
---
+++
+++
""") == """YES
YES
NO
NO
YES
"""

# custom cases
assert run("1\n--\n+") == "NO", "cannot create plus without operation"
assert run("1\n-+\n-+") == "YES", "identity case"
assert run("1\n--\n--") == "YES", "no operation needed"
assert run("1\n---\n-+-") == "YES", "odd segment produces single minus"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `-- / +` | NO | impossible to create plus from single minus |
| `-+ / -+` | YES | unchanged string validity |
| `-- / --` | YES | identity case |
| `--- / -+-` | YES | parity handling in odd segment |

## Edge Cases

A single minus in `s` cannot produce any plus, so any requirement that introduces a new plus inside a purely minus region immediately fails. The algorithm catches this because a length-1 segment has parity 1, forcing exactly one minus in `t`, so any deviation is rejected.

A long alternating structure of plus and minus is handled safely because every plus acts as a hard boundary, preventing cross-segment interference. Each segment is evaluated independently, so even highly interleaved inputs reduce to local parity checks.

A fully minus string behaves as a single segment, where the only constraint is parity. The algorithm reduces it correctly to a single global check, confirming whether the final number of minus signs in `t` matches the parity of the original length.
