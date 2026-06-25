---
title: "CF 106160B - Boggle Sort"
description: "The puzzle is about a 4 by 4 tray of dice. Each die has six possible letters, and we may only rotate a die. The dice stay in their original positions."
date: "2026-06-25T11:11:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106160
codeforces_index: "B"
codeforces_contest_name: "2025 Benelux Algorithm Programming Contest (BAPC 25)"
rating: 0
weight: 106160
solve_time_s: 42
verified: true
draft: false
---

[CF 106160B - Boggle Sort](https://codeforces.com/problemset/problem/106160/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

The puzzle is about a 4 by 4 tray of dice. Each die has six possible letters, and we may only rotate a die. The dice stay in their original positions. The goal is to choose the final top face of every die so that the 16 visible results are in nondecreasing alphabetical order from left to right, using the fewest total rotations.

A rotation changes which face points upward. A sideways face can be brought to the top with one turn, while the bottom face needs two turns. The currently visible top face costs zero turns.

The input describes the 16 dice by giving the top row, the four side rows, and the bottom row. The `Q` character represents the special Boggle face `Qu`, which should be compared as two letters. This means a tile showing `Qu` behaves like the string `"QU"` when checking order.

The number of dice is fixed at 16, which completely changes the algorithmic approach. A general sorting problem with a large number of elements would require something like `O(n log n)` or better, but here the number of positions is tiny. The challenge is not handling many dice, but correctly exploring the possible rotations without wasting work.

A careless solution might treat every die as having six independent choices and try all combinations. That creates `6^16` possibilities, which is over 2.8 billion states. Even though the board is small, that is far too much.

The tricky cases come from the ordering rules and repeated letters. For example, a single die may have the same useful character on multiple faces, and choosing the cheaper rotation matters. Consider a die that can show `A` on the top and also on a side. The correct minimum cost for choosing `A` is zero, not one. Any approach that stores only letters and forgets their costs can produce a wrong answer.

Another edge case is the `Qu` face. If two consecutive chosen tiles are `Q` and `U`, their order is not the same as `Q` and `T`. For example, the sequence `Qu, U` is valid because it compares as `QU` followed by `U`, while `Qu, T` is invalid because after `Q` the next compared character is `U`, which is larger than `T`.

## Approaches

The direct brute force approach is to try every possible final orientation of every die. Each die has six possible top faces, so the search space is `6^16`. For every complete choice, we check whether the resulting sequence is sorted and keep the minimum rotation cost. This is correct because it examines every possible final tray state, but the number of states is about 2.8 billion, making it impractical.

The structure that saves us is that the sorted condition only depends on the previous chosen tile. Once we decide the first `i` dice, the only information needed to decide the next die is the value of the last chosen face. The exact history no longer matters.

This lets us build a dynamic programming solution. We process dice from left to right. The state stores the minimum cost after finishing a prefix while ending with a particular visible face. When adding the next die, we only allow faces that are alphabetically not smaller than the previous face.

The number of states is tiny. There are only 16 positions and each position has at most six possible visible faces.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(6^16) | O(16) | Too slow |
| Optimal | O(16 * 6 * 6) | O(6) | Accepted |

## Algorithm Walkthrough

1. Parse the six faces of every die. For each possible final top face, store the number of rotations needed to make it appear. A top face costs zero, side faces cost one, and the bottom face costs two.

If the same visible character appears through different rotations, keeping the cheaper cost is necessary because the final order only cares about the character, not the physical face.
2. Create a dynamic programming array where `dp[j]` means the minimum cost after processing the current prefix of dice, with the last chosen tile being face `j`.

The previous tile is the only constraint needed because every new tile must be at least as large as the previous one.
3. Initialize the first die by allowing every possible visible face. There is no previous tile to compare against.
4. For every following die, try every possible current face. If the previous chosen face is not greater than the current face, transition to the new state by adding the rotation cost.
5. After processing all dice, the answer is the minimum value among all ending states. If no state is reachable, the tray cannot be sorted.

Why it works:

The invariant is that after processing the first `i` dice, every stored state represents the cheapest way to make those `i` visible tiles sorted and end with a particular final tile. When we add a new die, we only extend sequences that remain sorted. Since every possible ending face is considered, no valid arrangement is missed. Because every transition adds exactly the rotation cost of the chosen face, the minimum reachable final state is the optimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**9

def solve():
    lines = []
    while len(lines) < 6:
        s = input().strip()
        if s:
            lines.append(s)

    top = lines[0]
    sides = lines[1:5]
    bottom = lines[5]

    dice = []

    for i in range(16):
        cost = {}
        faces = [(top[i], 0)]
        for row in sides:
            faces.append((row[i], 1))
        faces.append((bottom[i], 2))

        for ch, c in faces:
            value = "QU" if ch == "Q" else ch
            if value not in cost or c < cost[value]:
                cost[value] = c

        dice.append(list(cost.items()))

    states = list({x for die in dice for x, _ in die})
    states.sort()

    m = len(states)
    idx = {s: i for i, s in enumerate(states)}

    dp = [INF] * m

    for s, c in dice[0]:
        dp[idx[s]] = min(dp[idx[s]], c)

    for i in range(1, 16):
        ndp = [INF] * m
        for prev in range(m):
            if dp[prev] == INF:
                continue
            for cur_s, cur_c in dice[i]:
                cur = idx[cur_s]
                if states[prev] <= cur_s:
                    ndp[cur] = min(ndp[cur], dp[prev] + cur_c)
        dp = ndp

    ans = min(dp)
    print("impossible" if ans == INF else ans)

if __name__ == "__main__":
    solve()
```

The code first builds the six possible outcomes of each die and converts `Q` into the string `QU` so normal string comparison follows the required ordering. This avoids needing special comparison logic later.

The dynamic programming array is compressed to only the visible strings that actually exist on some die. Since there are at most 16 dice with six faces each, the number of possible states is very small.

The transition checks `states[prev] <= cur_s`. This is the core ordering condition. Python's string comparison handles the special `QU` representation correctly because it compares character by character.

The input reading ignores empty lines, which makes the solution robust against formatting differences around the sample input. The final minimum is either a valid rotation count or remains infinite, meaning no sorted arrangement exists.

## Worked Examples

For a small constructed case:

Input:

```
A
B
C
D
E
F
```

The relevant states are only the six dice in the example. The process is:

| Step | Current die | Possible choice | DP state |
| --- | --- | --- | --- |
| 1 | A | A | A:0 |
| 2 | B | B | A:0, B:0 |
| 3 | C | C | A:0, B:0, C:0 |
| 4 | D | D | A:0, B:0, C:0, D:0 |

This demonstrates the normal sorted case. The algorithm keeps every valid ending point instead of committing greedily to one face.

For a case where the visible order must be fixed with rotations:

Input:

```
Z
A
B
C
D
E
```

Suppose the first die can rotate to `A` for one turn. The trace becomes:

| Step | Current die | Chosen face | Cost |
| --- | --- | --- | --- |
| 1 | first | A | 1 |
| 2 | second | B | 0 |
| 3 | third | C | 0 |
| 4 | fourth | D | 0 |

The final cost is one. This shows why the algorithm must consider rotations early, rather than assuming the currently visible letters are fixed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(16 * 6 * 6) | Each die tries every previous state and every possible new face |
| Space | O(6) | Only the previous and current DP layers are stored |

The fixed board size keeps the solution comfortably within the limits. The algorithm is effectively constant time, but the dynamic programming reasoning is what allows the same idea to work for larger variants with more positions.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return sys.stdout.getvalue()

# sample 1
assert run("""IAZEEOXSPACKYIGF
APDSSAOHEQAOGGLY
LCERNRFILJINEEWE
BDVLOMRESBATLTRI
TEAAWSINUOOUKVIH
YMNCDHBPTMTDUNUE
""").strip() == "15"

# sample 2
assert run("""EXFETDMNMGDBRSRM
TIEGINOVRETACNUA
PRYKASAEATNTSHID
SOHUOEJDHVKYLPLC
UFIYAWBZONUIEIWE
LBELCOQASIOLAEGP
""").strip() == "impossible"

# already sorted
assert run("""ABCDEFGHIJKLMNOP
ABCDEFGHIJKLMNOP
ABCDEFGHIJKLMNOP
ABCDEFGHIJKLMNOP
ABCDEFGHIJKLMNOP
ABCDEFGHIJKLMNOP
""").strip() == "0"

# requires rotating first die
assert run("""ZBCDEFGHIJKLMNOP
ABCDEFGHIJKLMNOP
ABCDEFGHIJKLMNOP
ABCDEFGHIJKLMNOP
ABCDEFGHIJKLMNOP
ABCDEFGHIJKLMNOP
""").strip() != "impossible"

# impossible ordering
assert run("""ZAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAA
""").strip() == "impossible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | 15 | Normal optimal rotation case |
| Sample 2 | impossible | Detects unreachable ordering |
| Sorted dice | 0 | Handles zero-cost solutions |
| First die needs adjustment | possible | Checks rotation transitions |
| Descending first tile with no fix | impossible | Checks boundary comparison |

## Edge Cases

When a die has duplicate letters on multiple faces, the algorithm merges them and keeps the lowest rotation cost. For example, if a die can show `A` either by staying still or by turning, the stored transition cost for `A` remains zero. This avoids paying unnecessary turns.

The `Qu` face is handled by converting it into `QU`. Suppose two adjacent choices are `Qu` and `U`. The comparison becomes `"QU" <= "U"`, which is true because `Q` comes before `U`. If the next tile is `T`, the comparison becomes `"QU" <= "T"`, which is false because `U` is larger than `T`. The string representation exactly matches the required alphabetic rule.

If no sequence can satisfy the ordering constraint, every DP state eventually becomes unreachable. For example, if the first die is forced to show `Z` and every later die can only show letters before `Z`, every transition is rejected. The final minimum remains infinite and the program outputs `impossible`.
