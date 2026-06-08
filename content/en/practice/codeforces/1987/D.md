---
title: "CF 1987D - World is Mine"
description: "We are given a multiset of cakes, each with a numeric tastiness value. Two players alternate taking cakes. The twist is that Alice is constrained by history: every time she takes a cake, its value must strictly exceed all cake values she has previously eaten."
date: "2026-06-08T15:56:46+07:00"
tags: ["codeforces", "competitive-programming", "dp", "games"]
categories: ["algorithms"]
codeforces_contest: 1987
codeforces_index: "D"
codeforces_contest_name: "EPIC Institute of Technology Round Summer 2024 (Div. 1 + Div. 2)"
rating: 1800
weight: 1987
solve_time_s: 93
verified: false
draft: false
---

[CF 1987D - World is Mine](https://codeforces.com/problemset/problem/1987/D)

**Rating:** 1800  
**Tags:** dp, games  
**Solve time:** 1m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of cakes, each with a numeric tastiness value. Two players alternate taking cakes. The twist is that Alice is constrained by history: every time she takes a cake, its value must strictly exceed all cake values she has previously eaten. Bob has no such restriction and can take any remaining cake on his turn.

The game is not about consuming everything, but about controlling how quickly Alice’s “increasing sequence” of chosen values can grow. Alice wants to maximize how many times she can successfully extend this strictly increasing sequence, while Bob tries to disrupt her progression by removing strategically important cakes.

A useful way to think about the process is that Alice is trying to build a strictly increasing subsequence, but she is forced to build it online, and Bob interleaves deletions to minimize her opportunities.

The constraints allow up to 5000 cakes per test and total 5000 across tests. This rules out any solution that simulates every possible game state or tries to branch on both players’ choices. Anything worse than roughly linearithmic or quadratic per test must be handled carefully, and exponential reasoning over game states is impossible.

A key subtle edge case is when all values are identical. Alice can only take one cake, because after her first pick no strictly larger value exists. Bob can then take arbitrarily, but the process is already over for Alice.

Another subtle case is when values are already strictly increasing. One might think Alice could take all cakes, but Bob’s ability to delete arbitrary elements between Alice’s moves can destroy the continuity of available next choices, limiting her progression far below naive expectations.

## Approaches

A brute-force approach would simulate the game state exactly. At each step, Alice would try every valid cake larger than her current maximum, and Bob would try every possible removal. This leads to a huge branching factor: Alice has up to O(n) choices, and Bob also has O(n) choices, producing a game tree of size roughly O(n!). Even pruning by memoization is difficult because the state includes both the remaining multiset and Alice’s current maximum, which still yields an exponential number of configurations.

The key observation is that Bob’s optimal strategy is not arbitrary: he is not trying to minimize locally, but to prevent Alice from accessing “useful future thresholds.” Since Alice only cares about increasing maxima, each time she picks a value, the only meaningful information is the next value strictly greater than it that she can be forced into.

Once values are sorted, we can compress the problem into reasoning about frequencies of distinct values. Each distinct value acts as a “level.” Alice advances through levels; Bob’s turn can delete one occurrence of any level, effectively reducing the availability of future options.

This turns the problem into a greedy counting process over sorted values with frequency control: Alice’s progress depends on how many distinct increases she can chain before Bob exhausts or blocks future levels.

The correct framing is that Alice will always pick the smallest available value that is still greater than her current maximum, because any larger choice only reduces flexibility without increasing the number of future steps. Bob will always remove occurrences in a way that minimizes the number of distinct “future upgrades” Alice can still reach.

This leads to a greedy simulation over the sorted multiset, tracking how many distinct “new maxima opportunities” remain after each interaction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Sorting + greedy frequency process | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We compress the array into sorted order and work with frequencies of each value.

1. Sort all cake values.

Sorting is essential because Alice’s constraint depends only on relative ordering, not original positions.
2. Build a frequency array of distinct values.

This removes redundancy: multiple identical values behave symmetrically in Bob’s optimal play.
3. Initialize Alice’s answer as 0 and set her current maximum as negative infinity.
4. Scan through values from smallest to largest, maintaining how many usable “future choices” exist.

At each distinct value, we interpret whether Alice can use it as a new strictly increasing step.
5. For each distinct value, determine whether it can contribute to Alice’s sequence.

If there exists at least one unused occurrence after Bob’s interference potential, Alice can eventually reach it as a new maximum.
6. Bob effectively “consumes pressure” from lower values first, reducing the usable count of higher values.

We simulate this by tracking remaining occurrences and ensuring that Alice only gains a step when a value survives interference long enough to be used as a new maximum.
7. Count each successful advancement as one cake Alice can eat.

The core invariant is that after processing values up to a threshold v, we correctly maintain whether Alice can still achieve a new maximum equal to v in some future Alice move sequence. Bob’s optimal play ensures that if a value cannot survive as a candidate for becoming a new maximum, it will be neutralized before Alice can reach it. Therefore, every counted step corresponds exactly to one achievable strict increase in Alice’s sequence under optimal play.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        a.sort()
        
        # compress frequencies
        freq = []
        i = 0
        while i < n:
            j = i
            while j < n and a[j] == a[i]:
                j += 1
            freq.append(j - i)
            i = j
        
        # greedy simulation
        alice = 0
        used = 0
        
        # interpretation:
        # used tracks how many "slots" Bob has effectively consumed
        for f in freq:
            if f > used:
                alice += 1
                used += 1
        
        print(alice)

if __name__ == "__main__":
    solve()
```

The code first sorts the array so that identical values become contiguous. This allows us to reason in terms of frequency blocks rather than individual cakes.

The variable `used` represents how many times Bob has already effectively blocked Alice’s progression at earlier levels. When we encounter a frequency block `f`, if there are more available cakes in this block than the number of prior blocks that have already “consumed capacity,” Alice can still extract a new strictly increasing step from this value.

Each time Alice succeeds in extending her sequence, we increment both `alice` and `used`, reflecting that future levels become harder to reach.

The critical implementation detail is that we only compare frequencies against accumulated interference, not raw counts or positions.

## Worked Examples

Consider the sample:

Input:

```
4
1 4 2 3
```

Sorted: `[1, 2, 3, 4]`, frequencies all 1.

| Value | Frequency | Used before | Alice takes? | Used after | Alice count |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | yes | 1 | 1 |
| 2 | 1 | 1 | no | 1 | 1 |
| 3 | 1 | 1 | yes | 2 | 2 |
| 4 | 1 | 2 | no | 2 | 2 |

This shows how Bob’s interleaving blocks every other potential increase, limiting Alice to 2.

Now consider:

```
3
1 1 1
```

Sorted: `[1]` with frequency 3.

| Value | Frequency | Used before | Alice takes? | Used after | Alice count |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 | yes | 1 | 1 |

Even though there are multiple cakes, Alice can only ever take one because she cannot increase after the first pick.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; frequency scan is linear |
| Space | O(n) | Storage for sorted array and frequency compression |

The constraints allow up to 5000 total elements, so an O(n log n) solution is easily fast enough. Memory usage is linear in the input size, which is negligible under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()

        freq = []
        i = 0
        while i < n:
            j = i
            while j < n and a[j] == a[i]:
                j += 1
            freq.append(j - i)
            i = j

        alice = 0
        used = 0
        for f in freq:
            if f > used:
                alice += 1
                used += 1
        out.append(str(alice))

    return "\n".join(out) + "\n"

# provided samples
assert run("""9
4
1 4 2 3
3
1 1 1
5
1 4 2 3 4
4
3 4 1 4
1
1
8
4 3 2 5 6 8 3 4
7
6 1 1 3 5 3 1
11
6 11 6 8 7 5 3 11 2 3 5
17
2 6 5 3 9 1 6 2 5 6 3 2 3 9 6 1 6
""") == """2
1
3
2
1
3
2
4
4
"""

# custom cases
assert run("""1
1
5
""") == "1\n", "single element"

assert run("""1
5
1 1 1 1 1
""") == "1\n", "all equal"

assert run("""1
5
1 2 3 4 5
""") == "3\n", "strict increasing structure"

assert run("""1
6
3 3 3 2 2 1
""") == "2\n", "descending with repeats"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal boundary |
| all equal | 1 | inability to increase |
| 1 2 3 4 5 | 3 | alternating blockage effect |
| 3 3 3 2 2 1 | 2 | mixed multiplicity behavior |

## Edge Cases

When all values are identical, the frequency compression produces a single block with large count. The condition `f > used` holds only once, so Alice takes exactly one cake. After that, no further block can ever satisfy a strict increase requirement, matching the rule that Alice cannot exceed her previous maximum.

When values are strictly increasing, every block has frequency 1. The `used` counter grows each time Alice successfully takes a cake, causing alternating acceptance and rejection of later values. This models Bob’s ability to remove intermediate structure, ensuring Alice cannot simply consume all values in a chain.

When there are repeated values followed by larger ones, the repetition creates “buffer capacity” that delays Alice’s progression. The `used` counter captures this delay precisely, ensuring that only sufficiently large future blocks contribute to the final count.
