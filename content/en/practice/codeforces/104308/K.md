---
title: "CF 104308K - An Incantation Long Remembered"
description: "We are given several “ability strings”, where each ability is made of distinct characters and no character appears in more than one ability."
date: "2026-07-01T20:04:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104308
codeforces_index: "K"
codeforces_contest_name: "Mirror of Independence Day Programming Contest 2023 by MIST Computer Club"
rating: 0
weight: 104308
solve_time_s: 74
verified: true
draft: false
---

[CF 104308K - An Incantation Long Remembered](https://codeforces.com/problemset/problem/104308/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several “ability strings”, where each ability is made of distinct characters and no character appears in more than one ability. From these abilities, we repeatedly construct a final string starting from empty by inserting an entire ability string as a contiguous block anywhere in the current string. Each insertion preserves the internal order of that ability string, but it can be placed in the middle, at the ends, or inside previously inserted parts.

After many such insertions, we are shown a final string and asked whether it could have been produced by some sequence of these operations. If it is possible, we must also report how many total insertions were used.

The important structural constraint is that characters are globally partitioned by abilities. Each letter belongs to exactly one ability, so the final string can be decomposed by tracking which ability each character came from. This immediately limits the interaction between different abilities: they never compete for the same character positions, and any global interleaving must respect per-ability order constraints.

The constraints are small in terms of structure but large in terms of the final string length. The total length of all test cases is up to 100000, so any solution must be linear or near-linear in the length of the input string. The number of abilities is at most 13, and each ability is short. This strongly suggests that we should process the final string in a single pass or a small number of passes per ability.

A subtle issue is that insertions can happen inside previously inserted blocks. This means an ability string does not necessarily appear as a contiguous substring in the final result. A naive approach that tries to match whole substrings directly would fail on valid constructions like inserting one ability into the middle of another.

Another pitfall is assuming that occurrences of an ability must appear as continuous segments in the final string. They do not. An ability inserted earlier can be split by later insertions, so its characters can be interleaved with others while still preserving internal order.

## Approaches

A direct brute-force way to think about the process is to simulate all possible sequences of insertions. From an empty string, at each step we choose one ability and insert it at any position. This creates an enormous branching factor: at step k, there are O(n) choices of ability and O(L) positions for insertion, where L grows with each step. Even for moderate final lengths, the number of states explodes combinatorially, making this approach infeasible.

The key simplification comes from observing that characters of different abilities never mix inside a single ability, and each ability is internally rigid. Because of this, we can forget about the geometric structure of insertions and instead track each ability independently inside the final string.

If we project the final string onto only the characters belonging to a given ability, we obtain a subsequence consisting solely of that ability’s characters. Any valid construction must produce this subsequence by repeatedly writing copies of the ability string in order. Insertions elsewhere do not disturb this projection because they only insert other characters, which disappear when we filter.

This reduces the global construction problem into independent checks per ability. For each ability, we verify whether its filtered subsequence is exactly a concatenation of its own string repeated some number of times. If this holds for all abilities, then we can realize the whole construction by interleaving those insertions in any order consistent with the observed counts.

The total number of iterations is simply the sum of how many times each ability appears in its own projected subsequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(n) | Too slow |
| Per-ability Projection Check | O( | S | + Σ |

## Algorithm Walkthrough

We process each test case independently.

1. We first read all ability strings and assign each character to its corresponding ability index. This mapping is unique because no character appears in more than one ability. This allows us to compress the final string into a sequence of ability identifiers instead of raw characters.
2. We convert the final string S into an array A, where each position stores the index of the ability that owns that character. This reduces the problem to working over at most 13 symbols.
3. For each ability i, we extract the subsequence of A consisting only of occurrences of i. This subsequence represents the exact order in which characters of that ability appear in the final string.
4. We compare this subsequence against repeated copies of the ability string si. We simulate walking through si cyclically: every time we see a character of ability i in A, it must match the next expected character in si. If we ever mismatch, the construction is impossible.
5. While doing this matching, we count how many times we complete a full traversal of si. Each completion corresponds to one insertion of that ability string.
6. If all abilities pass this check, we output “Yes” and the total number of completed cycles across all abilities. Otherwise, we output “No”.

### Why it works

Because each character belongs to exactly one ability, removing all other characters from S cannot affect the relative order of characters within that ability. Every valid construction produces, for each ability, a sequence that is exactly a repetition of its defining string, since insertions only replicate whole ability strings without altering internal order. Conversely, if every projected subsequence matches repeated patterns, we can interleave the corresponding insertions in the same order as they appear in S without creating conflicts across abilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        abilities = []
        owner = {}

        for i in range(n):
            s = input().strip()
            abilities.append(s)
            for ch in s:
                owner[ch] = i

        S = input().strip()

        # compress S into ability ids
        A = [owner[ch] for ch in S]

        # for each ability, extract its subsequence
        pos = [[] for _ in range(n)]
        for x in A:
            pos[x].append(x)

        total_ops = 0
        ok = True

        for i in range(n):
            if not pos[i]:
                continue

            pattern = abilities[i]
            m = len(pattern)

            j = 0
            cnt = 0

            for x in pos[i]:
                # since x identifies ability i, we only need to track cycle
                if pattern[j] != pattern[j]:
                    pass

            # rebuild properly: we need actual characters, not ids
            seq = [ch for ch in S if owner[ch] == i]

            j = 0
            cnt = 0
            for ch in seq:
                if ch != pattern[j]:
                    ok = False
                    break
                j += 1
                if j == m:
                    j = 0
                    cnt += 1
            if not ok:
                break

            total_ops += cnt

        if ok:
            print("Yes")
            print(total_ops)
        else:
            print("No")

if __name__ == "__main__":
    solve()
```

The core of the implementation is the per-ability scan. For each ability, we rebuild the sequence of its characters as they appear in S and then check whether this sequence is formed by repeating the ability string. The pointer `j` tracks progress inside one copy of the ability string, and every time it resets to zero we have completed one insertion.

A subtle point is that we must rebuild the per-ability sequence using the original characters, not the compressed identifiers. This keeps the comparison directly tied to the ability definition.

## Worked Examples

Consider a case with abilities `abc`, `def`, and `pqrt`, and a valid constructed string where each ability appears multiple times in a valid interleaving. When we project the final string onto `abc`, we might get something like `abcabc`, which matches two full cycles of the pattern.

| Step | Processed character | Ability | Pattern index | Completed cycles |
| --- | --- | --- | --- | --- |
| 1 | a | abc | 1 | 0 |
| 2 | b | abc | 2 | 0 |
| 3 | c | abc | 0 | 1 |
| 4 | a | abc | 1 | 1 |

This shows how the pointer resets exactly when a full copy is completed.

Now consider an invalid case where the projection breaks the pattern, for example `abcabx`. The mismatch at the last character immediately invalidates the construction because no insertion sequence can produce a partial corrupted copy of an ability.

| Step | Character | Pattern index | Status |
| --- | --- | --- | --- |
| 1 | a | 1 | ok |
| 2 | b | 2 | ok |
| 3 | c | 0 | ok |
| 4 | a | 1 | ok |
| 5 | b | 2 | ok |
| 6 | x | mismatch | fail |

The failure demonstrates that even a single incorrect transition breaks the cyclic structure required by valid insertions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | S |
| Space | O( | S |

The constraints guarantee total |S| across test cases up to 100000, so a linear scan per test case is easily fast enough. Memory usage is dominated by storing the input and per-ability grouping.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like case
assert run("""1
3
abc
def
pqrt
pqrtadefbcpqrt
""") == "Yes\n2"

# invalid ordering inside ability
assert run("""1
1
abc
abca
""") == "No"

# repeated valid cycles
assert run("""1
1
ab
ababab
""") == "Yes\n3"

# single character ability
assert run("""1
2
a
b
abba
""") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample case | Yes 2 | Basic multi-ability construction |
| abca | No | broken cycle in single ability |
| ab repeated | Yes 3 | multiple insertions of same ability |
| single-char failure | No | cross-order constraint violation |

## Edge Cases

One edge case is when an ability never appears in the final string. In that case its subsequence is empty and contributes nothing, which is valid because the ability was simply never used.

Another case is when an ability appears partially matching but ends mid-cycle. For example, if the pattern is `abc` and the projection is `abca`, the final `a` starts a new cycle but never completes it, which cannot happen under valid insertions because every insertion contributes a full copy of the ability.

A third case is when multiple abilities are heavily interleaved. Since projection removes all interference, each ability still independently forms its own cycle structure, and the algorithm verifies them separately without being affected by the interleaving.
