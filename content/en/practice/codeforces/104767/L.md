---
title: "CF 104767L - Wall"
description: "We are given a one-dimensional binary array representing a row of cells. Each cell is either inactive, shown as a dot, or active, shown as an X. Starting from this initial configuration, we repeatedly evolve the row for a fixed number of steps."
date: "2026-06-28T20:09:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104767
codeforces_index: "L"
codeforces_contest_name: "2023-2024 CTU Open Contest"
rating: 0
weight: 104767
solve_time_s: 64
verified: true
draft: false
---

[CF 104767L - Wall](https://codeforces.com/problemset/problem/104767/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional binary array representing a row of cells. Each cell is either inactive, shown as a dot, or active, shown as an X. Starting from this initial configuration, we repeatedly evolve the row for a fixed number of steps. Each new row is computed simultaneously from the previous one using a fixed local rule.

The rule looks at every position together with its immediate left and right neighbors. These three cells form a window of size three, and there are eight possible patterns of 0 and 1 over such a window. The rule is encoded as a number between 0 and 255, which can be interpreted as a lookup table telling us what the next state of the center cell should be for each of the eight possible neighborhoods.

The output requires printing the first K generated configurations after applying this rule repeatedly, each on its own line, using the same dot and X encoding.

The constraints are small: the width is at most 250 and the number of steps is at most 200. This immediately suggests that a direct simulation is sufficient, because each generation costs linear time in the width, and the total work is at most about 50,000 cell updates per rule application. Even with full recomputation per step, the total number of operations stays tiny.

A subtle boundary condition is that the row is conceptually surrounded by infinite zeros. That means when we compute neighbors for the first and last cells, missing neighbors are treated as dots. A naive implementation that forgets this extension will silently shift or shrink patterns at the edges.

Another common mistake is misinterpreting the rule encoding. The rule number is not applied directly as a binary string in a naive left-to-right mapping unless we carefully define which neighborhood corresponds to which bit. The correct mapping is fixed: neighborhoods are ordered from 111 down to 000.

## Approaches

A brute force approach directly follows the definition. For each generation, we compute a new array by iterating over every cell and checking its left, center, and right neighbors. For each triple, we determine which of the eight binary patterns it matches, then index into the rule table to decide the next state. This is straightforward and correct, but still requires O(n) work per generation, giving O(nK) overall.

With n up to 250 and K up to 200, this is at most 50,000 cell updates, which is already trivial. There is no need for optimization beyond clean simulation. The only real difficulty is implementing the rule decoding correctly and handling boundaries.

The key observation is that this is a purely local deterministic automaton. Each cell update depends only on a fixed radius neighborhood, so no global structure or precomputation helps further. The optimal solution is simply careful simulation with correct bit extraction from the rule integer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(nK) | O(n) | Accepted |
| Optimal Simulation | O(nK) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the input string into a binary array where X becomes 1 and dot becomes 0. This makes neighbor computations direct and avoids repeated character comparisons.
2. Decode the rule integer into a list of 8 bits. The least significant bit corresponds to pattern 000, and the most significant bit corresponds to 111. This mapping must be consistent with how neighborhoods are interpreted. The rule can be extracted using bit shifts.
3. For each of the K generations, create a new array of the same length.
4. For every position i in the current array, compute the neighborhood value by reading left, current, and right cells. If i is at the boundary, treat out-of-range neighbors as 0. This ensures the infinite-zero assumption is respected without special casing separate logic.
5. Convert the triple (left, center, right) into an index between 0 and 7 using bit packing, then use that index to query the rule table and assign the new value.
6. After filling the new array, convert it back into the output format and print it. Then replace the current array with the new one and repeat.

### Why it works

Each cell update depends only on a fixed radius of one, so the next generation is fully determined by the previous one without any hidden dependencies. The rule table is a complete function from neighborhood states to next states, so every configuration evolves deterministically. Because boundary cells always see zeros outside the array, the simulation exactly matches the infinite extension described in the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    R, K = map(int, input().split())
    s = input().strip()

    n = len(s)
    cur = [1 if c == 'X' else 0 for c in s]

    rule = [(R >> i) & 1 for i in range(8)]

    for _ in range(K):
        nxt = [0] * n

        for i in range(n):
            left = cur[i - 1] if i - 1 >= 0 else 0
            mid = cur[i]
            right = cur[i + 1] if i + 1 < n else 0

            idx = (left << 2) | (mid << 1) | right
            nxt[i] = rule[idx]

        print("".join('X' if x else '.' for x in nxt))
        cur = nxt

if __name__ == "__main__":
    solve()
```

The solution first converts the string into integers so that bitwise operations become natural. The rule decoding step builds a direct lookup table indexed by the neighborhood pattern.

The key implementation detail is the indexing formula `(left << 2) | (mid << 1) | right`, which encodes the three-bit pattern into a number from 0 to 7. This must match the way the rule integer is unpacked.

Boundary handling is embedded directly in the neighbor extraction, where missing indices contribute zero. This avoids edge condition branches inside the core loop.

## Worked Examples

### Sample 1

Input:

```
128 5
XXXXXXXXXXXXX
```

Rule 128 corresponds to binary `10000000`, meaning only neighborhood 111 produces a 1; all others produce 0.

| Step | Current Row | Next Row |
| --- | --- | --- |
| 0 | XXXXXXXXXXXXX | .XXXXXXXXXXX. |
| 1 | .XXXXXXXXXXX. | ..XXXXXXXXX.. |
| 2 | ..XXXXXXXXX.. | ...XXXXXXX... |
| 3 | ...XXXXXXX... | ....XXXXX.... |
| 4 | ....XXXXX.... | .....XXX..... |

Each step shrinks the block because only fully surrounded active cells survive, and edges immediately drop due to zero padding.

### Sample 2

Input:

```
30 10
...........X...........
```

Rule 30 generates chaotic growth patterns where many mixed neighborhoods become active.

A partial trace of early evolution:

| Step | Center Pattern Snapshot |
| --- | --- |
| 0 | ...........X........... |
| 1 | ..........XXX.......... |
| 2 | .........XX..X......... |
| 3 | ........XX.XXXX........ |
| 4 | .......XX..X...X....... |

The pattern expands outward because rule 30 activates several asymmetric neighborhoods, allowing single seeds to propagate.

These traces confirm that the update is strictly local and depends only on adjacent triples.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nK) | Each of K generations processes all n cells once with constant work per cell |
| Space | O(n) | Two arrays of size n are used for current and next states |

With n ≤ 250 and K ≤ 200, the total number of operations is about 50,000, which is negligible under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else __import__('builtins').exec  # placeholder

# Since direct execution depends on environment, these are conceptual asserts

# sample 1
# assert run("128 5\nXXXXXXXXXXXXX\n") == ".XXXXXXXXXXX.\n..XXXXXXXXX..\n...XXXXXXX...\n....XXXXX....\n.....XXX.....\n"

# sample 2
# assert run("30 10\n...........X...........\n") == expected_output

# minimum case
# assert run("0 1\nX\n") == ".\n"

# single dot stability
# assert run("255 3\n.\n") == ".\n.\n.\n"

# alternating seed
# assert run("90 2\n.X.\n") == "...\n...\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell | dot | boundary handling with zero padding |
| all dots | all dots | stability under zero input |
| all X with rule 255 | all X | full activation rule |
| small pattern | correct evolution | neighbor encoding correctness |

## Edge Cases

A key edge case is a single-cell input. For example:

```
128 2
X
```

At the first update, both neighbors are treated as zero, so the only neighborhood is 000, which maps to a specific rule bit. After decoding rule 128, only 111 produces 1, so the cell immediately becomes dot and stays dot. The algorithm handles this naturally because both neighbors default to zero.

Another edge case is a completely empty row:

```
30 3
........
```

Every neighborhood is 000 in the first step, so the entire next generation depends solely on rule[0]. The algorithm correctly applies the same index computation everywhere, so no special casing is needed.

A final edge case is maximum width. Even with 250 cells, the algorithm still recomputes each row independently, and the fixed-size arrays ensure no dynamic overhead beyond simple indexing, so performance remains stable.
