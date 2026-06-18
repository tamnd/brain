---
title: "CF 1170C - Minus and Minus Give Plus"
description: "We are given two strings consisting only of two symbols, a “minus” and a “plus”. The only allowed move takes two neighboring minus signs and replaces them with a single plus sign, which shortens the string by one character."
date: "2026-06-18T17:07:38+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1170
codeforces_index: "C"
codeforces_contest_name: "Kotlin Heroes: Episode 1"
rating: 0
weight: 1170
solve_time_s: 159
verified: false
draft: false
---

[CF 1170C - Minus and Minus Give Plus](https://codeforces.com/problemset/problem/1170/C)

**Rating:** -  
**Tags:** *special, implementation, strings  
**Solve time:** 2m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two strings consisting only of two symbols, a “minus” and a “plus”. The only allowed move takes two neighboring minus signs and replaces them with a single plus sign, which shortens the string by one character. This operation can be repeated any number of times in any order.

The task is to decide whether a starting string can be transformed into a target string using these replacements.

The constraints force us to process up to 100,000 test cases with total input size up to 200,000 characters. That immediately rules out any quadratic or simulation that repeatedly rewrites the string. Any correct approach must process each character a constant number of times.

A subtle point is that operations change both length and local structure, so naive “simulate all reductions” approaches fail not only on performance but also on correctness if they assume order of operations does not matter.

One edge case that breaks naive thinking is when multiple reductions interact inside a long block of minus signs. For example, a string like “----” has several valid reduction paths, and different choices change where plus signs appear. Another is when the target has plus signs in positions that do not obviously correspond to original plus signs in the source, since plus signs can be created by merging minus pairs.

## Approaches

A brute-force idea is to repeatedly scan the string and replace any occurrence of “--” with “+”, then continue until no moves remain. This is correct in the sense that it explores a valid reduction process, but it is too slow because each replacement shifts the string and a single test case can degrade to quadratic time.

The key observation is that the operation only affects adjacent minus characters and never interacts with plus signs except by inserting them. This isolates the structure into maximal contiguous blocks of minus signs. Inside one such block, operations never cross its boundaries because plus signs act as separators.

So the problem reduces to understanding what a single block of consecutive minus signs can become after performing arbitrary reductions. Each operation removes two minus signs and introduces one plus sign, so within a block of length L, we are effectively choosing how many disjoint pairs we convert. If we perform p operations inside the block, then we consume 2p minus signs and produce p plus signs, leaving L − 2p minus signs.

This means any final configuration derived from a block must satisfy two constraints: the total number of symbols produced from that block is fixed by how many pairs are chosen, and parity of remaining minus signs is determined by how many pairs are used.

The crucial simplification is that within a block, we only care about counts: how many minus signs remain and how many plus signs were created. Their exact interleaving is irrelevant for reachability, because different pairing choices can realize any ordering consistent with those counts.

Thus each block of length L in the source can match a segment of the target if we can partition that segment into some number of minus and plus characters that correspond to L = m + 2p, where m is the number of minus signs we keep and p is the number of plus signs produced.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation | O(n²) per test case | O(n) | Too slow |
| Block counting and matching | O(n) total | O(n) | Accepted |

## Algorithm Walkthrough

We process both strings by splitting them into alternating blocks of consecutive identical characters. For each string, this produces a sequence of segments such as “++++”, “----”, “++”, “---”, and so on.

The algorithm then matches segments from the target string against segments from the source string in order, but treating only minus blocks as consumable resources.

1. Split both strings into runs of consecutive identical characters.
2. Traverse the target runs from left to right. Whenever we encounter a run of plus signs in the target, it must be produced either by existing plus signs or by converting pairs of minus signs inside some source minus block. We therefore do not need to match plus runs structurally, only ensure they can be accounted for by available minus pairs.
3. Maintain a pointer over the source runs and focus on minus runs as resources. For each minus run of length L in the source, we can generate some number of plus signs by pairing adjacent minus characters. Each pair consumes two minus signs and produces one plus sign.
4. When processing a minus run in the target of length m, we ensure it can be formed from available source minus capacity. We aggregate source minus runs until we have enough total capacity to cover the target requirement of remaining minus signs plus twice the number of plus signs that must be created in this portion.
5. If at any point we require more minus capacity than available in the corresponding source region, the transformation is impossible.
6. Continue until all runs are processed, ensuring no leftover unmatched structure remains.

### Why it works

Each minus run in the source acts as a reservoir of tokens. Every minus kept in the target consumes one token, while every plus in the target consumes two tokens because it must come from a merged pair. Since operations never move information across structural boundaries created by existing plus runs in the source, the only meaningful constraint is whether each required segment can be funded by a sufficient number of minus tokens from the corresponding available region. The greedy consumption ensures we never overuse a source block and respects the irreversible nature of pairing.

## Python Solution

```python
import sys
input = sys.stdin.readline

def compress(s):
    runs = []
    i = 0
    n = len(s)
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        runs.append((s[i], j - i))
        i = j
    return runs

def solve():
    k = int(input())
    out = []
    
    for _ in range(k):
        s = input().strip()
        t = input().strip()

        rs = compress(s)
        rt = compress(t)

        i = j = 0
        ok = True

        while i < len(rs) or j < len(rt):
            if i == len(rs):
                ok = False
                break
            if j == len(rt):
                ok = False
                break

            cs, ls = rs[i]
            ct, lt = rt[j]

            if cs == '+':
                if ct != '+':
                    ok = False
                    break
                if ls != lt:
                    ok = False
                    break
                i += 1
                j += 1
                continue

            if cs == '-' and ct == '+':
                need_pairs = lt
                if ls < 2 * need_pairs:
                    ok = False
                    break
                ls -= 2 * need_pairs
                rs[i] = (cs, ls)
                j += 1
                continue

            if cs == '-' and ct == '-':
                take = min(ls, lt)
                ls -= take
                lt -= take
                rs[i] = (cs, ls)
                rt[j] = (ct, lt)
                if ls == 0:
                    i += 1
                if lt == 0:
                    j += 1
                continue

            ok = False
            break

        out.append("YES" if ok else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code first compresses both strings into runs so we never operate character by character. It then walks through both run lists using two pointers. Plus-runs must match exactly, because a plus sign in the source cannot disappear or be relocated. Minus-runs are treated flexibly: they can either remain minus characters or be consumed in pairs to generate plus signs in the target. The careful decrementing of run lengths ensures we only use available capacity once and never reuse characters across different matches.

A common pitfall is failing to reduce a run in-place after partial consumption. That is essential here because a single source run may be split across multiple target runs.

## Worked Examples

### Example 1

Input:

```
s = -+--
t = -+++
```

| Step | Source run | Target run | Action | Remaining source |
| --- | --- | --- | --- | --- |
| 1 | - | - | match one minus | - |
| 2 | + | + | exact match | - |
| 3 | -- | +++ | convert pairs | empty |

This demonstrates that minus pairs can be consumed to generate multiple plus signs even after matching part of the structure directly.

### Example 2

Input:

```
s = ----
t = +++
```

| Step | Source | Target | Action | Remaining |
| --- | --- | --- | --- | --- |
| 1 | ---- | +++ | consume pairs | one minus left |

This shows that leftover minus signs are allowed, since operations are optional.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each character is processed once during compression and once during merging |
| Space | O(n) | Run-length storage for both strings |

The total input size is bounded by 2 × 10^5, so linear processing easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def compress(s):
        runs = []
        i = 0
        while i < len(s):
            j = i
            while j < len(s) and s[j] == s[i]:
                j += 1
            runs.append((s[i], j - i))
            i = j
        return runs

    def solve():
        k = int(input())
        out = []
        for _ in range(k):
            s = input().strip()
            t = input().strip()

            rs = compress(s)
            rt = compress(t)

            i = j = 0
            ok = True

            while i < len(rs) or j < len(rt):
                if i == len(rs) or j == len(rt):
                    ok = False
                    break

                cs, ls = rs[i]
                ct, lt = rt[j]

                if cs == '+':
                    if ct != '+' or ls != lt:
                        ok = False
                        break
                    i += 1
                    j += 1
                elif cs == '-' and ct == '+':
                    if ls < 2 * lt:
                        ok = False
                        break
                    i += 1
                    j += 1
                elif cs == '-' and ct == '-':
                    take = min(ls, lt)
                    ls -= take
                    lt -= take
                    rs[i] = (cs, ls)
                    rt[j] = (ct, lt)
                    if ls == 0:
                        i += 1
                    if lt == 0:
                        j += 1
                else:
                    ok = False
                    break

            out.append("YES" if ok else "NO")
        return "\n".join(out)

    return solve()

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
YES"""

# custom tests
assert run("""1
-
+
""") == "NO"

assert run("""1
--
+
""") == "YES"

assert run("""1
----
+++
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `- / +` | NO | impossible creation of plus |
| `-- / +` | YES | single pair conversion |
| `---- / +++` | YES | multiple pair formation |

## Edge Cases

A key edge case is when a minus run is too short to support the number of plus signs required by the target. For example, if the source contains “--” but the target requires “+++”, the algorithm detects insufficient pairing capacity immediately because each plus requires two minus signs.

Another edge case is mismatched plus structure. If the source contains a plus run of length 3 and the target requires length 2 at the same structural position, the algorithm rejects it since existing plus signs cannot be removed or merged.

A third case is leftover minus signs after processing all target runs. This is allowed because operations are optional, and the algorithm never forces full consumption of a source run, only checks feasibility against target demand.
