---
title: "CF 250B - Restoring IPv6"
description: "We are given several IPv6 addresses in a shortened human-readable form. Each address originally represents exactly 8 blocks, and each block corresponds to 16 bits written as 4 hexadecimal digits. The shortening rules allow two independent compressions."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 250
codeforces_index: "B"
codeforces_contest_name: "CROC-MBTU 2012, Final Round (Online version, Div. 2)"
rating: 1500
weight: 250
solve_time_s: 139
verified: true
draft: false
---

[CF 250B - Restoring IPv6](https://codeforces.com/problemset/problem/250/B)

**Rating:** 1500  
**Tags:** implementation, strings  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several IPv6 addresses in a shortened human-readable form. Each address originally represents exactly 8 blocks, and each block corresponds to 16 bits written as 4 hexadecimal digits.

The shortening rules allow two independent compressions. First, within each block, leading zeros may be removed, so a block like `000a` may appear as `a`, and `00ff` may appear as `ff`. Second, one contiguous segment of blocks that are all zero can be replaced by the marker `::`, but this marker can appear at most once in a valid shortened address. The task is to reconstruct the original fully expanded 8-block representation for each input string.

The output must restore every block to exactly 4 lowercase hexadecimal characters, including leading zeros, and ensure there are exactly 8 blocks separated by single colons.

The constraints are small, with at most 100 addresses and each string being short. This means even a linear scan per string is trivial in terms of complexity, and the real difficulty is purely in correct parsing of the compression rules, especially handling `::`.

A naive but incorrect approach is to simply split the string by `:` and expect 8 parts. This fails immediately when `::` appears. For example, input `::` would produce empty tokens, and something like `a::b` would not preserve how many zero blocks were compressed.

Another common mistake is miscounting zero blocks when `::` appears in the middle versus at the ends. For example, `a::b` could mean different expansions depending on how many blocks exist on each side. The correct interpretation depends on ensuring the final count is always exactly 8 blocks.

## Approaches

A direct brute-force idea would be to attempt to reconstruct the original address by guessing how many zero blocks `::` represents and inserting them, checking whether the final length becomes 8 blocks and whether all constraints are satisfied. Since the input guarantees validity, this would always succeed for one configuration, but brute-forcing possibilities is unnecessary and awkward. Even though the number of possibilities is small, the logic becomes messy because the placement of zero blocks interacts with splitting on colons in non-uniform ways.

The key observation is that `::` is the only ambiguous construct. Everything else is already explicitly given as blocks, possibly with missing leading zeros. Once we locate whether `::` exists, the structure becomes deterministic: everything to the left and right of `::` are fixed blocks, and the number of missing blocks is exactly `8 - (left_blocks + right_blocks)`.

This turns the problem into simple string parsing with a single special case. We only need to split the string into left and right parts around `::`, expand both sides, and insert the correct number of `"0000"` blocks in between.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force guessing zero placement | O(8 · n) per string | O(1) | Too slow and unnecessary |
| Direct parsing with `::` handling | O(n) per string | O(n) | Accepted |

## Algorithm Walkthrough

We process each address independently.

1. Check whether the string contains `::`. This determines whether we have a compressed zero block segment or a fully explicit structure. If no `::` exists, the string already contains exactly 8 blocks separated by single colons.
2. If there is no `::`, split the string by `:` into 8 tokens. Each token is a hexadecimal block that may have fewer than 4 characters. Pad each token on the left with zeros until it becomes length 4. Join them back with colons.
3. If `::` exists, split the string into two parts: everything before `::` and everything after `::`.
4. Split both parts by `:` independently, but carefully handle empty strings, since `::` at the start or end produces empty left or right parts. Each resulting token list represents explicitly written blocks.
5. Compute how many blocks are already present: the number of left tokens plus the number of right tokens.
6. The number of missing blocks is `8 - (left_count + right_count)`. These correspond exactly to the compressed zero segment.
7. Construct the final list as: left blocks, then the required number of `"0000"` blocks, then right blocks.
8. Pad every block in the final list to 4 characters and join them with `:`.

The crucial reasoning step is that `::` represents a contiguous sequence of zero blocks whose length is not encoded explicitly but is fully determined by the requirement that the final structure must contain exactly 8 blocks.

### Why it works

The representation is uniquely determined by the rule that exactly one zero-sequence compression is allowed and the final expanded address must have exactly 8 blocks. Once we fix the non-zero blocks on the left and right of `::`, the missing count of blocks is forced. No other interpretation can produce a valid 8-block reconstruction, so the construction is deterministic and consistent.

## Python Solution

```python
import sys
input = sys.stdin.readline

def pad(block: str) -> str:
    return block.rjust(4, '0')

def solve_one(s: str) -> str:
    if "::" not in s:
        parts = s.split(":")
        parts = [pad(p) for p in parts]
        return ":".join(parts)

    left, right = s.split("::")

    left_parts = [] if left == "" else left.split(":")
    right_parts = [] if right == "" else right.split(":")

    # handle single empty string case from split
    if left_parts == [""]:
        left_parts = []
    if right_parts == [""]:
        right_parts = []

    used = len(left_parts) + len(right_parts)
    zeros = 8 - used

    mid = ["0000"] * zeros

    res = [pad(x) for x in left_parts] + mid + [pad(x) for x in right_parts]
    return ":".join(res)

def main():
    n = int(input())
    for _ in range(n):
        s = input().strip()
        print(solve_one(s))

if __name__ == "__main__":
    main()
```

The function `solve_one` isolates the logic for a single address. The key branching is whether `::` exists. The padding function ensures each block becomes exactly four hexadecimal characters, preserving correctness even for single-digit blocks.

Care must be taken when splitting around `::`, since Python produces empty strings when the compression is at the boundaries. Those cases are normalized into empty lists so that counting logic remains consistent.

## Worked Examples

### Example 1: `a56f::0124:0001:0000:1234:0ff0`

| Step | Left blocks | Right blocks | Missing | Result construction |
| --- | --- | --- | --- | --- |
| Parse | a56f | 0124,0001,0000,1234,0ff0 | - | - |
| Count | 1 | 5 | 2 | - |
| Fill | - | - | 2 | insert 0000,0000 |
| Final | a56f,0000,0000 | 0124,0001,0000,1234,0ff0 | - | join |

This shows how the missing block count is derived purely from the requirement of 8 total blocks.

### Example 2: `::`

| Step | Left blocks | Right blocks | Missing | Result construction |
| --- | --- | --- | --- | --- |
| Parse | empty | empty | - | - |
| Count | 0 | 0 | 8 | insert 8 zeros |
| Final | - | - | - | 0000 × 8 |

This demonstrates that even the fully compressed zero address is handled uniformly by the same rule.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per string | Each address has constant maximum size and we process at most 8 blocks |
| Space | O(1) | Only stores up to 8 fixed-size blocks per string |

The constraints allow up to 100 strings, so the total work is negligible. The solution is entirely bounded by constant-factor string operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def pad(block: str) -> str:
        return block.rjust(4, '0')

    def solve_one(s: str) -> str:
        if "::" not in s:
            parts = s.split(":")
            return ":".join([pad(p) for p in parts])

        left, right = s.split("::")
        left_parts = [] if left == "" else left.split(":")
        right_parts = [] if right == "" else right.split(":")

        used = len(left_parts) + len(right_parts)
        zeros = 8 - used

        res = [pad(x) for x in left_parts] + ["0000"] * zeros + [pad(x) for x in right_parts]
        return ":".join(res)

    n = int(input())
    out = []
    for _ in range(n):
        out.append(solve_one(input().strip()))
    return "\n".join(out)

# provided samples
assert run("""6
a56f:d3:0:0124:01:f19a:1000:00
a56f:00d3:0000:0124:0001::
a56f::0124:0001:0000:1234:0ff0
a56f:0000::0000:0001:0000:1234:0ff0
::
0ea::4d:f4:6:0
""") == """a56f:00d3:0000:0124:0001:f19a:1000:0000
a56f:00d3:0000:0124:0001:0000:0000:0000
a56f:0000:0000:0124:0001:0000:1234:0ff0
a56f:0000:0000:0000:0001:0000:1234:0ff0
0000:0000:0000:0000:0000:0000:0000:0000
00ea:0000:0000:0000:004d:00f4:0006:0000"""

# custom cases
assert run("1\n0:0:0:0:0:0:0:0\n") == "0000:0000:0000:0000:0000:0000:0000:0000"
assert run("1\nabcd::1\n") == "abcd:0000:0000:0000:0000:0000:0000:0001"
assert run("1\n::1\n") == "0000:0000:0000:0000:0000:0000:0000:0001"
assert run("1\n1::\n") == "0001:0000:0000:0000:0000:0000:0000:0000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `::` | all zeros | full compression case |
| `abcd::1` | padded middle zeros | center expansion |
| `::1` | leading compression | empty left side handling |
| `1::` | trailing compression | empty right side handling |

## Edge Cases

The most delicate case is when `::` appears at the beginning or end of the string. For input like `::1`, splitting produces an empty left side, and the algorithm correctly interprets this as zero explicit blocks before the compression. The remaining blocks determine exactly how many zeros to insert so that the total reaches 8.

For `1::`, the right side is empty. The same logic applies symmetrically: only the left block is present, so seven zero blocks must be inserted after it.

The fully compressed `::` case removes all blocks. The algorithm computes used blocks as zero, so all eight positions are filled with `"0000"`, which matches the definition of a fully zero IPv6 address.

Each of these cases works because the algorithm never depends on position heuristics, only on the invariant that the final expanded form must contain exactly 8 blocks.
