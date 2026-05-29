---
title: "CF 250B - Restoring IPv6"
description: "An IPv6 address in its full form is a fixed structure made of eight blocks. Each block represents 16 bits and is written as exactly four hexadecimal characters, including leading zeros when necessary."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 250
codeforces_index: "B"
codeforces_contest_name: "CROC-MBTU 2012, Final Round (Online version, Div. 2)"
rating: 1500
weight: 250
solve_time_s: 65
verified: true
draft: false
---

[CF 250B - Restoring IPv6](https://codeforces.com/problemset/problem/250/B)

**Rating:** 1500  
**Tags:** implementation, strings  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

An IPv6 address in its full form is a fixed structure made of eight blocks. Each block represents 16 bits and is written as exactly four hexadecimal characters, including leading zeros when necessary. The blocks are separated by colons, so a fully expanded address always has the same length pattern and always contains seven colons.

The input we receive is a shortened version of such an address. Two independent compressions may have been applied. First, within each block, leading zeros may have been removed, so a block like `00ea` might appear as `ea`. Second, a single contiguous run of blocks that were all zero may have been replaced by a double colon `::`, which stands for one or more full zero blocks. Importantly, this replacement can only be used once per address.

The task is to reconstruct the original full eight-block representation. That means we must recover both the missing zero blocks from `::` and restore each block to exactly four hexadecimal digits by adding leading zeros.

The constraints are small, with at most 100 addresses, so even a straightforward parsing approach is easily fast enough. The main difficulty is not performance but correctness in handling the ambiguous structure of `::`, especially distinguishing where the omitted zero blocks belong and how many there are.

A few edge situations tend to break naive solutions. If the input is exactly `::`, it represents eight zero blocks, and many implementations incorrectly treat it as empty or a single block. If `::` appears at the beginning or end, one side of the split becomes empty, which must still be interpreted correctly. Another subtle case is ensuring that when expanding `::`, the total number of blocks becomes exactly eight, not more or less, regardless of how many explicit blocks appear around it.

## Approaches

A full IPv6 expansion problem is mostly about reversing a lossy encoding. A brute-force idea would be to try all possible placements of zero blocks for every `::` and validate which reconstruction yields exactly eight blocks and matches the visible parts. This would involve splitting the string around `::`, guessing how many zero blocks were compressed, and checking consistency. While conceptually simple, it introduces unnecessary combinatorial reasoning even though the structure actually determines the answer uniquely.

The key observation is that the non-`::` blocks are already fixed. Once we split the string at `::`, the number of missing blocks is completely determined by how many blocks are already present. Since the final address must contain exactly eight blocks, the number of inserted zero blocks is simply `8 - (left_blocks + right_blocks)`.

This removes any ambiguity. We no longer search, we only compute how many zero blocks are needed and insert them in the correct position.

After reconstructing the full list of eight blocks, each block is independently expanded to four hexadecimal digits by padding with leading zeros. There is no interaction between blocks at this stage.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force guessing zero placement | O(exponential per `::`) | O(1) | Too slow / unnecessary |
| Direct parsing and reconstruction | O(1) per address | O(1) | Accepted |

## Algorithm Walkthrough

We process each address independently.

1. Check whether the string contains `::`. If it does not, the address already has all eight blocks explicitly listed. We only need to split by `:` and pad each block to four characters.
2. If `::` exists, split the string into two parts: everything before `::` and everything after it. Each part may be empty.
3. Split both parts by `:` into lists of blocks. Empty parts produce empty lists, which is important for cases like leading or trailing `::`.
4. Count how many blocks are already present in both lists combined. Let this be `k`.
5. Compute how many zero blocks must be inserted as `z = 8 - k`. This value is always non-negative because the input is guaranteed valid.
6. Construct the full block list as: left blocks, then `z` zero blocks, then right blocks. The zero blocks are represented as `"0"` or empty strings but will be normalized in the next step.
7. Convert every block into a 4-character hexadecimal string using zero padding. This is done uniformly for both original and inserted blocks.
8. Join all eight blocks using colons to form the final expanded IPv6 address.

The correctness comes from the fact that the full structure size is fixed. Once we know how many blocks are explicitly present, the remainder must be zero blocks introduced by `::`, and there is no freedom in their placement beyond the single gap.

The invariant maintained is that after step 6, the constructed block list always has exactly eight logical positions filled either by original values or inferred zero blocks. Padding in step 7 only changes formatting, not structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def expand_ipv6(s: str) -> str:
    if "::" in s:
        left, right = s.split("::")

        left_blocks = left.split(":") if left else []
        right_blocks = right.split(":") if right else []

        # remove empty strings caused by edge cases like ":" splitting artifacts
        left_blocks = [b for b in left_blocks if b]
        right_blocks = [b for b in right_blocks if b]

        k = len(left_blocks) + len(right_blocks)
        z = 8 - k

        blocks = left_blocks + (["0"] * z) + right_blocks
    else:
        blocks = s.split(":")

    # pad each block to 4 hex digits
    res = []
    for b in blocks:
        res.append(b.zfill(4))

    return ":".join(res)

def main():
    n = int(input())
    out = []
    for _ in range(n):
        s = input().strip()
        out.append(expand_ipv6(s))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation mirrors the reconstruction logic directly. The most delicate part is handling `::` correctly when it appears at the start or end of the string, because splitting produces empty strings that must not be treated as real blocks. The use of filtering ensures we only count actual hexadecimal tokens when determining how many zero blocks are missing.

The padding step with `zfill(4)` is sufficient because every block is guaranteed to be valid hexadecimal and at most four characters long after compression.

## Worked Examples

### Example 1: `a56f::0124:0001:0000:1234:0ff0`

We split around `::`, giving left = `a56f`, right = `0124:0001:0000:1234:0ff0`.

| Step | Left blocks | Right blocks | k | z | Final blocks |
| --- | --- | --- | --- | --- | --- |
| Parse | [a56f] | [0124, 0001, 0000, 1234, 0ff0] | 6 | 2 | [a56f, 0, 0, 0124, 0001, 0000, 1234, 0ff0] |

After padding, `a56f` becomes `a56f`, zeros become `0000`, and the rest remain normalized. The result matches the requirement of eight blocks.

This confirms that the computed gap size correctly restores the missing structure.

### Example 2: `::`

Here the entire address is compressed.

| Step | Left blocks | Right blocks | k | z | Final blocks |
| --- | --- | --- | --- | --- | --- |
| Parse | [] | [] | 0 | 8 | [0,0,0,0,0,0,0,0] |

After padding, every block becomes `0000`, producing the fully zero IPv6 address.

This demonstrates that empty splits correctly translate into zero-length lists and that the algorithm naturally fills the entire structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each address is parsed and padded in constant time since it always has at most 8 blocks |
| Space | O(1) | Only a fixed number of blocks are stored per address |

The input size is small enough that even multiple string operations per test case are negligible, and the solution easily fits within both limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout

    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

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

# all zeros edge
assert run("1\n::\n") == "0000:0000:0000:0000:0000:0000:0000:0000"

# no compression
assert run("1\na:b:c:d:e:f:1:2\n") == "000a:000b:000c:000d:000e:000f:0001:0002"

# leading ::
assert run("1\n::1:2:3:4:5:6:7\n") == "0000:0001:0002:0003:0004:0005:0006:0007"

# trailing ::
assert run("1\n1:2:3:4:5:6:7::\n") == "0001:0002:0003:0004:0005:0006:0007:0000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `::` | all zeros | full compression |
| no `::` | padded blocks | basic formatting |
| leading `::` | left-empty split | prefix gap handling |
| trailing `::` | right-empty split | suffix gap handling |

## Edge Cases

For the input `::`, the algorithm splits into empty left and right lists. The computed missing block count becomes eight, so eight zero blocks are inserted. After padding, all become `0000`, producing a valid full IPv6 address.

For `::1:2:3:4:5:6:7`, the left side is empty and the right side contains seven blocks. The algorithm inserts one zero block at the beginning, ensuring the total reaches eight blocks. Padding then produces the correct full representation.

For `1:2:3:4:5:6:7::`, the opposite happens: the right side is empty, and one zero block is appended at the end. This shows that the placement of `::` naturally determines whether zeros are inserted at the start or end without special casing.
