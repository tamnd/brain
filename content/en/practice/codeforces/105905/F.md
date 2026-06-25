---
title: "CF 105905F - \u0422\u0443\u043d \u0442\u0443\u043d \u0442\u0443\u043d \u0442\u0443\u043d \u0421\u0430\u0445\u0443\u0440"
description: "We have two strings describing drum events. The first string p is the actual sequence of hits: each character is one hit on either the left drum (L) or the right drum (R). The second string s is what was heard."
date: "2026-06-25T14:14:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105905
codeforces_index: "F"
codeforces_contest_name: "Ural championship 2025"
rating: 0
weight: 105905
solve_time_s: 35
verified: true
draft: false
---

[CF 105905F - \u0422\u0443\u043d \u0442\u0443\u043d \u0442\u0443\u043d \u0442\u0443\u043d \u0421\u0430\u0445\u0443\u0440](https://codeforces.com/problemset/problem/105905/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two strings describing drum events. The first string `p` is the actual sequence of hits: each character is one hit on either the left drum (`L`) or the right drum (`R`). The second string `s` is what was heard. A single hit does not always create a single character in the recording: an `L` hit can appear as either `L` or `LL`, and an `R` hit can appear as either `R` or `RR`.

The task is to decide whether the recorded string `s` could have been produced from the hit sequence `p`.

The input contains multiple test cases. For each case, the lengths of all strings across the whole input are large enough that solutions doing repeated searching or backtracking will not fit. With total length around `2 * 10^5`, we need a linear or near-linear algorithm. Anything quadratic would perform around `4 * 10^10` operations in the worst case, which is far beyond what a normal Codeforces time limit allows.

The tricky part is that equal consecutive characters can be stretched. A careless solution might only check whether `p` is a subsequence of `s`, but that ignores the grouping rules. For example, if `p = "LR"` and `s = "LLLR"`, a subsequence check succeeds because we can find `L` and `R`, but the answer is actually `NO`. The first hit can create at most two `L` characters, so three `L` characters before the `R` cannot come from the same original hit.

Another edge case is when the number of characters is correct but the groups are wrong. For `p = "LL"` and `s = "L"`, the output is `NO`. Each character in `p` represents a separate hit, so both hits must appear in the recording. A solution that only compares the final counts of letters might incorrectly accept this.

A final boundary case is a single character. For `p = "R"` and `s = "RR"`, the output is `YES` because one hit can sound twice. For `p = "RR"` and `s = "R"`, the output is `NO` because two hits cannot shrink into one sound.

## Approaches

The direct approach is to simulate all possible expansions of `p`. Each character has two choices, so a string of length `n` can produce up to `2^n` possible recordings. This is correct because it tries every valid transformation, but it becomes useless even for moderate lengths. With `n = 200000`, the number of possibilities is impossible to enumerate.

The structure of the problem gives us a much smaller view. Consecutive equal characters in `p` must correspond to one consecutive block of equal characters in `s`. If we split both strings into maximal blocks, every block from `p` can grow independently by a factor of either one or two. A block of length `x` in `p` can become a block of length `x` or `2x` in `s`.

This observation removes the need to try choices. We only need to compare the compressed forms of both strings. If the letters of corresponding blocks differ, the transformation is impossible. If a block from `s` is shorter than the matching block from `p`, it is impossible because sounds cannot disappear. If it is longer than twice the original block, it is impossible because every hit contributes at most two copies.

The brute force works because every valid answer is an expansion of the original string, but fails because it explores many equivalent possibilities. The block comparison works because all characters inside a block behave identically, so the only information that matters is the block length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Block Compression | O( | p | + |

## Algorithm Walkthrough

1. Split both strings into groups of equal consecutive characters. For example, `"LLLRR"` becomes blocks `("L", 3)` and `("R", 2)`. These blocks represent individual hits of the same drum type that appear next to each other.
2. Compare the number of blocks in the two strings. If they are different, the answer is immediately `NO`. Each block in `p` must match exactly one block in `s`, because the only allowed change is repeating the same character.
3. For every pair of matching blocks, check that their characters are equal. A left hit cannot turn into a right sound, and a right hit cannot turn into a left sound.
4. Compare the lengths of each pair of blocks. If the recorded block length is smaller than the original block length, the recording lost sounds and is invalid. If it is larger than twice the original length, there are too many sounds for the available hits. Otherwise this block is valid.
5. If every block passes the checks, print `YES`.

The reason this works is that the compression preserves exactly the information relevant to the transformation. Inside one block, every original hit is the same type of drum hit. The only possible change is adding one extra copy, so the entire block can only scale by a factor between one and two. Different blocks cannot merge or split because that would change the order of drum hits.

## Python Solution

```python
import sys
input = sys.stdin.readline

def compress(s):
    res = []
    i = 0
    n = len(s)
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        res.append((s[i], j - i))
        i = j
    return res

def solve():
    t = int(input())
    ans = []
    for _ in range(t):
        p = input().strip()
        s = input().strip()

        a = compress(p)
        b = compress(s)

        if len(a) != len(b):
            ans.append("NO")
            continue

        ok = True
        for (c1, x), (c2, y) in zip(a, b):
            if c1 != c2 or y < x or y > 2 * x:
                ok = False
                break

        ans.append("YES" if ok else "NO")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `compress` function walks through the string once and builds the consecutive blocks. It uses two pointers: `i` marks the start of a block and `j` moves until the character changes. This avoids repeated slicing and keeps the total work linear.

The main loop first compares the number of blocks. This catches cases where a block boundary is missing, such as an original `"LR"` trying to become `"LRL"`. After that, the paired blocks are checked. The condition `y > 2 * x` is the most common place for an off-by-one mistake because a block is allowed to double, but not more.

Python integers do not overflow here because the only arithmetic involves string lengths, which are at most a few hundred thousand.

## Worked Examples

For `p = "LR"` and `s = "LRR"`:

| Step | p blocks | s blocks | Result |
| --- | --- | --- | --- |
| Compress strings | (L,1), (R,1) | (L,1), (R,2) | continue |
| Check L block | L, 1 to 1 | valid | continue |
| Check R block | R, 1 to 2 | valid | YES |

This shows the case where the recording contains an extra sound. The second drum hit was allowed to become two `R` characters.

For `p = "LR"` and `s = "LLLR"`:

| Step | p blocks | s blocks | Result |
| --- | --- | --- | --- |
| Compress strings | (L,1), (R,1) | (L,3), (R,1) | continue |
| Check L block | L, original length 1 | recorded length 3 | invalid |

The first block is too large. A single `L` hit can only create one or two `L` characters, so three of them cannot be produced.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | p |
| Space | O( | p |

The total length of all strings is bounded by the input limits, so the linear solution easily fits. The memory usage is also proportional to the input size and stays within typical Codeforces limits.

## Test Cases

```python
import sys
import io

def compress(s):
    res = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        res.append((s[i], j - i))
        i = j
    return res

def solve(inp):
    data = inp.strip().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        p = data[idx]
        s = data[idx + 1]
        idx += 2
        a = compress(p)
        b = compress(s)
        ok = len(a) == len(b)
        if ok:
            for (c1, x), (c2, y) in zip(a, b):
                if c1 != c2 or y < x or y > 2 * x:
                    ok = False
                    break
        out.append("YES" if ok else "NO")
    return "\n".join(out)

assert solve("""5
R
RR
LRLR
LRLR
LR
LLLR
LLLLLRL
LLLLRRLL
LLRLRLRRL
LLLRLRRLLRRRL
""") == """YES
YES
NO
NO
YES"""

assert solve("""2
L
L
RR
R
""") == """YES
NO"""

assert solve("""3
LL
LL
LL
LLLL
LL
L
""") == """YES
YES
NO"""

assert solve("""2
LR
LLRR
LR
LRR
""") == """YES
YES"""

assert solve("""1
LLLL
LLLLLLLL
""") == """YES"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single `R` becoming `RR` | YES | A block may double in size. |
| Two `R` hits becoming one `R` | NO | Sounds cannot disappear. |
| Four equal hits becoming eight | YES | Maximum expansion is handled. |
| Mixed blocks with valid expansion | YES | Different drum blocks stay aligned. |

## Edge Cases

For `p = "LR"` and `s = "LLLR"`, compression gives `(L,1),(R,1)` and `(L,3),(R,1)`. The first pair fails because the recorded length is larger than twice the original length. The algorithm returns `NO`, avoiding the mistake of treating `p` as a subsequence.

For `p = "LL"` and `s = "L"`, the compressed forms are `(L,2)` and `(L,1)`. The second string is too short because two separate hits need to produce at least two sounds. The length comparison catches this immediately.

For `p = "R"` and `s = "RR"`, the blocks are `(R,1)` and `(R,2)`. The recorded size is exactly the allowed maximum, so the algorithm accepts it. This verifies the upper boundary condition.

For `p = "LR"` and `s = "LRL"`, the compressed form of the second string has three blocks while the first has two. Since a single original block cannot split into another block of a different drum, the algorithm rejects it before doing any length checks.
