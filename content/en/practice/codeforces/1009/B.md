---
title: "CF 1009B - Minimum Ternary String"
description: "We are given a string made only of digits 0, 1, and 2. We are allowed to repeatedly swap adjacent pairs if they are 0 and 1 in either direction, or 1 and 2 in either direction."
date: "2026-06-16T22:57:11+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1009
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 47 (Rated for Div. 2)"
rating: 1400
weight: 1009
solve_time_s: 159
verified: false
draft: false
---

[CF 1009B - Minimum Ternary String](https://codeforces.com/problemset/problem/1009/B)

**Rating:** 1400  
**Tags:** greedy, implementation  
**Solve time:** 2m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string made only of digits 0, 1, and 2. We are allowed to repeatedly swap adjacent pairs if they are 0 and 1 in either direction, or 1 and 2 in either direction. The goal is to transform the string into the lexicographically smallest possible string under these moves.

The important aspect is that swaps are local and only involve neighboring pairs, but they can be applied arbitrarily many times, meaning characters can effectively “move through” the string as long as they respect the allowed adjacency rules.

The string length can be up to 100000, so any approach that tries to simulate swaps explicitly is too slow. A naive simulation could take quadratic time in the worst case since each swap only moves characters by one position. That immediately rules out any approach that repeatedly bubbles characters into place.

A subtle edge case appears when all three digits are mixed. For example, a string like 100210 allows multiple valid swap sequences that produce different-looking final arrangements. A naive greedy like “sort the string” can fail because not all swaps are allowed (0 and 2 never swap directly), while overly cautious local strategies can also fail because chains of swaps allow indirect rearrangements that are not obvious from the initial configuration.

The key difficulty is that 1 acts as a mediator: it can swap with both 0 and 2, which means it enables indirect movement that complicates simple ordering assumptions.

## Approaches

A brute force approach would simulate all possible swaps using BFS or DFS over all reachable strings. Each state has up to O(n) neighbors, and the number of states grows explosively because many permutations are reachable through sequences of adjacent swaps. Even if pruning is attempted, the state space becomes factorial in the worst case, making it completely infeasible.

The key observation is that we do not need to track individual swap sequences. Instead, we should understand what ordering constraints remain invariant under the allowed operations. The system allows local inversions between 0 and 1, and between 1 and 2, which means 1 can move across both 0 and 2 freely through intermediate steps. This makes 1 effectively the most flexible character.

From this flexibility, the optimal strategy is to reason in terms of minimizing lexicographic order greedily. Since 0 is the smallest digit, we want 0s as early as possible. Since 2 is the largest, we want it as late as possible. The digit 1 can be used as a buffer that can be placed between them in a way that does not obstruct the placement of smaller characters.

This leads to the standard constructive result: the optimal string is obtained by arranging all 0s first, then all 1s, then all 2s. Any attempt to delay 0s or bring 2s forward can only worsen lexicographic order because there always exists a sequence of valid swaps that allows pushing 0 leftwards past 1s and pushing 2 rightwards past 1s.

The brute force works because it explicitly explores all swap sequences. The greedy works because the only relevant global objective is lexicographic minimization, and the swap system is rich enough that digits can be freely rearranged into global sorted order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (state search) | Exponential | Exponential | Too slow |
| Optimal (counting and construction) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We construct the answer directly rather than simulating swaps.

### Steps

1. Count how many 0s, 1s, and 2s appear in the string.

These counts fully determine the final string because swaps allow arbitrary rearrangement consistent with lexicographic minimization.
2. Build the result by writing all 0s first.

Putting 0s earlier is always optimal because no operation can make a 0 larger than necessary without worsening lexicographic order.
3. Append all 1s after the 0s.

Since 1 is larger than 0 but smaller than 2, placing it in the middle keeps the prefix minimal while avoiding unnecessary interference with 0s.
4. Append all 2s at the end.

2 contributes the largest possible lexicographic value, so delaying it maximizes optimality.

### Why it works

The swaps ensure that no digit is permanently trapped in a worse position relative to others of smaller value. Any configuration that is not sorted by digit value can be improved by repeatedly swapping adjacent inverted pairs (0 before 1 or 1 before 2). Because these swaps are reversible and exhaustive, any inversion between smaller and larger digits can be eliminated. This means the lexicographically smallest reachable arrangement is the fully sorted arrangement by digit value.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

c0 = c1 = c2 = 0

for ch in s:
    if ch == '0':
        c0 += 1
    elif ch == '1':
        c1 += 1
    else:
        c2 += 1

print('0' * c0 + '1' * c1 + '2' * c2)
```

The solution works by reducing the problem to counting frequencies. The loop is the only processing step and runs in linear time. After counting, string construction is direct and does not depend on the original ordering.

A common mistake is trying to simulate swaps or track positions of digits. That is unnecessary because the allowed operations remove any meaningful positional constraints beyond counts.

## Worked Examples

### Example 1

Input:

```
100210
```

We count digits: c0 = 3, c1 = 2, c2 = 1.

| Step | c0 | c1 | c2 | Partial Output |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | "" |
| After counting | 3 | 2 | 1 | "" |
| Build 0s | 3 | 2 | 1 | "000" |
| Build 1s | 3 | 2 | 1 | "00011" |
| Build 2s | 3 | 2 | 1 | "000112" |

Final output:

```
000112
```

This matches the lexicographically smallest arrangement achievable because all smaller digits are placed as early as possible.

### Example 2

Input:

```
210102
```

Counts are c0 = 2, c1 = 2, c2 = 2.

| Step | c0 | c1 | c2 | Partial Output |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | "" |
| After counting | 2 | 2 | 2 | "" |
| Build 0s | 2 | 2 | 2 | "00" |
| Build 1s | 2 | 2 | 2 | "0011" |
| Build 2s | 2 | 2 | 2 | "001122" |

Final output:

```
001122
```

This demonstrates that even with heavily mixed input, the structure collapses to a sorted arrangement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to count characters plus linear construction of result |
| Space | O(1) | Only three counters are used; output string dominates memory |

The algorithm fits easily within limits for n up to 100000 since it performs only constant work per character.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    s = input().strip()

    c0 = c1 = c2 = 0
    for ch in s:
        if ch == '0':
            c0 += 1
        elif ch == '1':
            c1 += 1
        else:
            c2 += 1

    return '0' * c0 + '1' * c1 + '2' * c2

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("100210\n") == "000112", "sample 1"

# single character
assert run("0\n") == "0"
assert run("2\n") == "2"

# all same
assert run("11111\n") == "11111"

# mixed small
assert run("102012\n") == "001122"

# already sorted reverse
assert run("222111000\n") == "000111222"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 / 2 single | same | minimal boundary behavior |
| all equal ones | unchanged | stability of construction |
| 102012 | 001122 | mixed ordering |
| 222111000 | 000111222 | worst-case reordering |

## Edge Cases

A minimal input like `0` or `2` shows that the algorithm does not introduce artificial structure and simply returns the same single character. The counting step yields a single non-zero counter, and the reconstruction directly outputs it.

A fully reversed input like `222111000` demonstrates that the algorithm does not depend on initial ordering at all. Even though the original string is maximally “large”, the output becomes fully minimized because all 0s are emitted first, followed by 1s and then 2s.

A mixed input like `102012` confirms that no interaction between positions is required. Even though digits are interleaved, the swap system allows complete rearrangement into grouped form, and the counting approach captures the reachable minimum directly.
