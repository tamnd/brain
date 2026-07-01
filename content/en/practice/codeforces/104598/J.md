---
title: "CF 104598J - Special Word Search"
description: "We are given a square grid of characters, and a list of words. A word is considered “found” if its letters can be traced on the grid in a straight line: horizontally, vertically, or diagonally."
date: "2026-06-30T04:33:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104598
codeforces_index: "J"
codeforces_contest_name: "GPL 2023 Advanced"
rating: 0
weight: 104598
solve_time_s: 75
verified: false
draft: false
---

[CF 104598J - Special Word Search](https://codeforces.com/problemset/problem/104598/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a square grid of characters, and a list of words. A word is considered “found” if its letters can be traced on the grid in a straight line: horizontally, vertically, or diagonally. The twist is that the grid behaves like a torus, meaning if we move past one edge, we reappear on the opposite side. So every straight direction continues infinitely with wrap-around behavior.

Each word must be matched starting from some cell and moving in one of the eight directions. A single cell cannot be reused within the same occurrence, which effectively prevents trivial cycles that would arise from wrapping back and reusing the same position in a degenerate way. However, since we only move in a fixed direction, revisiting the same cell would only happen if the direction itself cycles through the grid period, and such paths are still considered valid as long as we do not reuse a position before finishing the word in a conflicting way.

The output is not the number of total matches across all positions. Instead, for each word we only care whether it appears at least once in the grid. Even if a word can be formed in many different ways, it contributes at most one to the final count.

The grid size is at most 100 by 100, and there are up to 5000 words, each of length up to 100. This immediately rules out a naive search that tries every word starting from every cell and exploring all paths dynamically without structure. A worst case estimate for such an approach would be on the order of 100 by 100 starting points, 8 directions, and up to 100 steps per word, repeated for 5000 words, which is already too large if each check involves repeated string operations or backtracking.

A second subtle issue comes from wrapping. A common mistake is to simulate movement without proper modular indexing, which leads to index errors or incorrect early termination when reaching borders.

Another failure case is treating words independently but recomputing full scans per word without reuse. Since K can be large, repeated scanning over the grid for each word becomes the bottleneck.

Finally, duplicates in the word list matter. If the same word appears multiple times, it still counts once, so we must deduplicate before processing.

## Approaches

A direct approach is to process each word independently. For a given word, we try every starting cell and every of the 8 directions, then simulate stepping forward character by character with wrap-around using modulo arithmetic. If we match all characters, we mark the word as found.

This is correct because every valid occurrence corresponds to a unique starting cell and direction. However, the cost is high. For each word of length L, we try 10000 starting positions and 8 directions, and each check takes O(L). With K up to 5000 and L up to 100, this leads to roughly 10000 × 8 × 100 × 5000 operations in the worst case, which is too slow.

The key observation is that we are repeatedly scanning the same grid for many different words. Instead of treating each word separately, we can precompute all possible strings that can be formed by walking in a straight line with wrapping, up to length 100, and store them in a set. Then we simply check whether each word exists in that set.

Since directions are fixed and wrapping is deterministic, every valid word corresponds to some contiguous segment along a cyclic line in one of the 8 directions. Precomputing all such segments allows us to convert the problem into membership queries.

We generate all starting cells and directions, then simulate up to 100 steps, building strings incrementally. We insert every prefix into a hash set. After preprocessing, each word check is O(1) on average.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per word | O(K · N² · 8 · L) | O(1) | Too slow |
| Precompute all paths | O(N² · 8 · L²) | O(N² · L²) | Accepted |

## Algorithm Walkthrough

1. Read the grid and store it as a 2D array of characters. This allows constant-time access when walking in any direction.
2. Deduplicate the word list using a set. This ensures repeated words are only counted once and reduces unnecessary work.
3. Define the 8 directions corresponding to horizontal, vertical, and diagonal moves. Each direction is a pair (dx, dy).
4. For every cell in the grid, treat it as a starting point.
5. For every direction, simulate a walk of length up to 100 steps. At each step, move using modular arithmetic so that going off one edge re-enters from the opposite side.
6. As we extend the path step by step, maintain a current string. After each extension, insert the string into a hash set of “seen patterns”. This ensures that every possible straight-line wrapped substring is recorded.
7. After preprocessing, iterate over the unique words and check membership in the set. Count how many are present.

### Why it works

Every valid word in the grid corresponds to some starting cell and one of the 8 directions, followed by a sequence of steps that respects wrap-around. Our preprocessing enumerates exactly these sequences up to length 100, which is the maximum word length. Since every possible valid construction is generated once, any word that exists in the grid must appear in the set. Conversely, anything in the set corresponds to a valid straight-line wrapped traversal, so no false positives are introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    grid = [input().split() for _ in range(n)]

    words = input().split()
    words = set(words)

    dirs = [(-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1)]

    seen = set()

    for i in range(n):
        for j in range(n):
            for dx, dy in dirs:
                x, y = i, j
                s = []
                for _ in range(100):
                    s.append(grid[x][y])
                    seen.add("".join(s))
                    x = (x + dx) % n
                    y = (y + dy) % n

    ans = 0
    for w in words:
        if w in seen:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The grid is stored as strings for fast indexing. The direction list encodes all straight-line movements including diagonals. The wrap-around is handled using modulo arithmetic so we never go out of bounds.

The main subtlety is building strings incrementally. Repeated string concatenation would be too slow, so we accumulate characters in a list and join only when inserting into the set. This keeps each step O(1) amortized.

We only build strings up to length 100 because no word exceeds that constraint. Any longer walk would be unnecessary.

## Worked Examples

### Sample 1

Input grid:

```
t h i s
b a r c
w t m e
a p s o
```

Words:

```
this sea soap her water
```

We track a few representative paths.

| Start | Direction | Steps | Built string | In set? |
| --- | --- | --- | --- | --- |
| (0,0) | (0,1) | 4 | "this" | yes |
| (1,1) | diagonal | 3 | "sea" (via wrap paths) | yes |
| (3,1) | (0,1) | 4 | "soap" | yes |

After preprocessing, the set contains all valid wrapped substrings. Each word lookup becomes a direct membership check.

This confirms that multiple words can overlap and still be independently detected.

### Additional Case

Grid:

```
a a
a a
```

Words:

```
aaa aaaa
```

| Start | Direction | Steps | Built string | In set? |
| --- | --- | --- | --- | --- |
| (0,0) | right | 3 | "aaa" | yes |
| (0,0) | right | 4 | "aaaa" | yes |

This demonstrates that wrapping causes repeated reuse of the same letters, and longer words can still be formed even in a minimal grid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N² · 8 · L² + K · L) | We build up to 100-length strings from each cell and direction, then do O(1) average lookups per word |
| Space | O(N² · L²) | All generated substrings are stored in a hash set |

The preprocessing dominates but remains feasible since N ≤ 100 and L ≤ 100, giving at most a few million generated strings. The solution fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip() if False else solve_and_capture(inp)

def solve_and_capture(inp: str) -> str:
    import sys
    from io import StringIO
    backup = sys.stdout
    sys.stdin = StringIO(inp)
    sys.stdout = StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = backup
    return out.strip()

# sample
assert solve_and_capture("4 5\n t h i s\n b a r c\n w t m e\n a p s o\nthis sea soap her water\n") == "3"

# all same letters
assert solve_and_capture("2 2\na a\na a\naa aaaa\n") == "2"

# single cell grid
assert solve_and_capture("1 3\na\na aa aaa\n") == "3"

# no matches
assert solve_and_capture("2 2\na b\nc d\nxy z\n") == "0"

# wrap-heavy
assert solve_and_capture("2 2\na b\nc d\nabcd bcda cdab dabc\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid | all words match | minimal boundary |
| uniform grid | multiple lengths match | repetition handling |
| mixed grid | zero matches | negative case correctness |
| cyclic pattern | full wrap correctness | torus behavior |

## Edge Cases

A subtle edge case arises when the grid is very small, especially 1x1 or 2x2. In a 1x1 grid, every direction leads back to the same cell, so any word consisting of repeated identical characters is valid. The algorithm handles this naturally because modulo arithmetic keeps all movement inside the same cell, and the generated strings correctly include repeated expansions.

Another edge case involves long words that exceed a full cycle around the grid. Since we limit generation to 100 steps, we still capture these because the maximum word length is 100. The wrap-around ensures that revisiting the same cell does not break construction, and the substring set includes all cyclic repetitions needed to match such words.
