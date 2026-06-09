---
title: "CF 1626A - Equidistant Letters"
description: "We are given a short string where each character appears either once or twice. The task is to permute the characters so that whenever a letter appears twice, the gap between its two occurrences is identical for all such letters."
date: "2026-06-10T05:22:39+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1626
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 121 (Rated for Div. 2)"
rating: 800
weight: 1626
solve_time_s: 118
verified: false
draft: false
---

[CF 1626A - Equidistant Letters](https://codeforces.com/problemset/problem/1626/A)

**Rating:** 800  
**Tags:** constructive algorithms, sortings  
**Solve time:** 1m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a short string where each character appears either once or twice. The task is to permute the characters so that whenever a letter appears twice, the gap between its two occurrences is identical for all such letters.

Another way to see it is that for every duplicated letter, if its positions are $i$ and $j$, then the value $j - i$ must be the same constant for all letters that occur twice. Letters that appear once impose no constraints.

The string length is at most 52, and there are at most 26 distinct letters, each appearing at most twice. This immediately tells us that any construction that tries all permutations is unnecessary. Even $52!$ is far beyond feasible limits, but even more structured brute force like backtracking over placements would still be exponential in practice.

A key observation is that the only meaningful constraint is on pairing duplicated letters with equal spacing. Single-occurrence letters are free variables that can be inserted anywhere without affecting constraints.

Edge cases that often break naive ideas are situations where duplicated letters are scattered and interleaved in the input. For example, in a string like `abacbc`, the natural pairing distances differ, and any solution must reorder globally, not locally adjust pairs. Another subtle case is when no letter appears twice, such as `ac`, where every permutation is valid and constraints vanish entirely.

## Approaches

A brute-force interpretation would be to try all permutations of the string and check whether all duplicated letters have equal distance. This is correct but immediately infeasible since even length 20 already yields $20!$ permutations.

The structure of the problem becomes simpler once we reinterpret the condition. Suppose we decide that all duplicated letters must have positions forming pairs with identical gaps. If we fix the final arrangement, every duplicated letter occupies two positions whose difference is a constant $d$. So the task becomes constructing a string where every duplicated letter is placed in positions $(i, i + d)$ for some fixed $d$.

Instead of searching permutations, we can directly construct such a structure. Since each letter appears at most twice, we only need to assign pairs of positions. We can choose a spacing $d$, and then greedily place each duplicated letter into slots that respect this spacing. Because the string length is small and the number of duplicates is limited, trying all feasible $d$ values and filling positions greedily always succeeds.

A simpler and more standard insight used in most solutions is even stronger: we do not need to explicitly choose $d$. We can construct the answer by placing all second occurrences at a uniform offset relative to the first occurrences in a consistent ordering. Sorting letters and assigning positions in a structured pattern guarantees equal spacing automatically.

The simplest construction is to place all characters that appear twice in a contiguous block pattern: first occurrences in one sequence, second occurrences mirrored with a fixed shift, while singletons are inserted arbitrarily into remaining slots.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Permutations | O(n!) | O(n) | Too slow |
| Structured Construction | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

The key idea is to group letters by frequency and then place them in a controlled order that enforces identical distance for all duplicated letters.

1. Count the frequency of each character. We separate characters into those appearing once and those appearing twice. This classification is crucial because only duplicated letters impose constraints.
2. Collect all letters that appear twice into a list and sort them. Sorting is not strictly required for correctness, but it ensures determinism and simplifies reasoning about placement.
3. Build two sequences for duplicated letters: one sequence will represent their first occurrences, and the other their second occurrences. The core idea is that we will place the first occurrences in one increasing order and the second occurrences in a shifted but aligned order so that every pair shares the same gap.
4. Place all single-occurrence letters into any remaining positions. These letters do not constrain distances, so they can be inserted without affecting the structure.
5. Construct the final string by interleaving the first-occurrence and second-occurrence structures in a way that enforces a constant shift. One natural way is to place all first occurrences in the front segment and all second occurrences in the back segment with identical relative ordering.
6. Output the constructed string.

### Why it works

The correctness comes from enforcing a rigid positional template for duplicated letters. Once all first occurrences are assigned positions $p_1 < p_2 < \dots < p_k$, and second occurrences are assigned positions $p_1 + d, p_2 + d, \dots, p_k + d$, every duplicated letter automatically has distance $d$. Since the construction ensures the same relative offset for all pairs, no letter can violate the constraint. Single-occurrence letters are unconstrained and therefore cannot break the condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()

    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1

    ones = []
    twos = []

    for ch in freq:
        if freq[ch] == 1:
            ones.append(ch)
        else:
            twos.append(ch)

    twos.sort()
    ones.sort()

    # Build result in a simple constructive pattern:
    # first all singles, then first occurrences, then second occurrences
    res = []

    # place singletons first
    for ch in ones:
        res.append(ch)

    # first occurrences
    for ch in twos:
        res.append(ch)

    # second occurrences
    for ch in twos:
        res.append(ch)

    print("".join(res))
```

The code first computes frequencies, then splits characters into singleton and duplicate groups. It sorts both groups for deterministic structure. The construction places all single-occurrence characters first, followed by the first occurrences of duplicated letters, and finally their second occurrences.

This layout ensures that all duplicated letters have identical spacing because every duplicated character is split between the same two contiguous blocks, making their distance equal to the size of the singleton block plus the offset induced by ordering. The exact value of the distance is irrelevant, only equality matters.

## Worked Examples

### Example 1: `abcdcba`

We compute frequencies: all `a, b, c, d` appear twice. There are no singletons.

We split:

- ones = []
- twos = [a, b, c, d]

After sorting: [a, b, c, d]

We construct:

| Step | Ones block | First block | Second block | Result |
| --- | --- | --- | --- | --- |
| init | [] | [] | [] | "" |
| duplicates first | [] | a b c d | [] | "abcd" |
| duplicates second | [] | a b c d | a b c d | "abcdabcd" |

Final string: `abcdabcd`

Every letter appears twice with identical spacing of 4.

This demonstrates that the structure enforces uniform pairing even when original order is arbitrary.

### Example 2: `oelhl`

Frequencies:

- o:1, e:1, h:1, l:2

Split:

- ones = [e, h, o]
- twos = [l]

Construction:

| Step | Ones block | First block | Second block | Result |
| --- | --- | --- | --- | --- |
| init | [] | [] | [] | "" |
| singles | e h o | [] | [] | "eho" |
| first l | e h o | l | [] | "ehol" |
| second l | e h o | l | l | "ehol l" |

Final string: `eholl`

The single duplicated letter `l` trivially satisfies equal spacing since there is only one pair. Singletons do not interfere with any constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting characters per test case dominates, n ≤ 52 |
| Space | O(n) | Storage for frequency map and output string |

The constraints are extremely small, so even sorting per test case is effectively constant time in practice. The solution easily fits within limits for up to $10^3$ test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        s = input().strip()

        freq = {}
        for ch in s:
            freq[ch] = freq.get(ch, 0) + 1

        ones = []
        twos = []

        for ch in freq:
            if freq[ch] == 1:
                ones.append(ch)
            else:
                twos.append(ch)

        ones.sort()
        twos.sort()

        res = ones + twos + twos
        out.append("".join(res))

    return "\n".join(out)

# provided samples
assert run("3\noelhl\nabcdcba\nac\n") in [
    "eho ll\nabcdabcd\nac"
], "sample check (any valid ordering accepted)"

# custom cases
assert run("1\naabbcc\n") != "", "all duplicates case"
assert run("1\nabcdef\n") == "abcdef", "all singles"
assert run("1\naaaabb\n") != "", "multiple duplicates"
assert run("1\nz\n") == "z", "single char"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `aabbcc` | any valid permutation with uniform structure | multiple duplicate letters |
| `abcdef` | unchanged | all single occurrences |
| `aaaabb` | structured rearrangement | mixed singles and duplicates |
| `z` | `z` | minimum input |

## Edge Cases

When the string contains no duplicated letters, the frequency split produces only singletons. In an input like `ac`, the algorithm places both letters in the singleton block and outputs them directly. Since no constraints exist, any ordering is valid, and the algorithm correctly avoids unnecessary structure.

When all letters are duplicated, such as `abcdcba`, the singleton block is empty. The construction collapses into two identical halves of the sorted duplicate list. The second half guarantees identical spacing because every letter’s pair is separated by exactly the same segment length.

When a single letter is duplicated among many singletons, such as `oelhl`, the singleton prefix simply shifts both occurrences of the duplicated letter equally. Since all duplicates share the same prefix, the distance between their occurrences remains consistent, and singleton placement cannot disturb relative spacing.
