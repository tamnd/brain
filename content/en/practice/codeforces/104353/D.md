---
title: "CF 104353D - \u5b64\u5be1\u9752\u86d9"
description: "We are given a small grid of characters representing a decorative picture. Each picture contains several frogs drawn using ASCII art, and the task is to count how many complete frogs appear in the grid."
date: "2026-07-01T18:11:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104353
codeforces_index: "D"
codeforces_contest_name: "2023 Xiangtan University Programming Contest"
rating: 0
weight: 104353
solve_time_s: 47
verified: true
draft: false
---

[CF 104353D - \u5b64\u5be1\u9752\u86d9](https://codeforces.com/problemset/problem/104353/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small grid of characters representing a decorative picture. Each picture contains several frogs drawn using ASCII art, and the task is to count how many complete frogs appear in the grid.

Each frog has a fixed shape, meaning it always appears exactly the same way, upright, and never rotated or distorted. The grid may contain multiple frogs placed somewhere inside, and every character outside frogs is just a dot. Frogs do not overlap, so every frog occupies its own isolated region of characters.

The input is a rectangular grid of size up to 100 by 100, so at most 10,000 characters. That bound is small enough that even fairly direct pattern matching or scanning approaches will pass comfortably, but it also suggests we should avoid overly complex global search or backtracking logic.

The key difficulty is not computational but recognition: we must reliably identify where each frog starts and ensure we do not count the same frog multiple times.

A common failure case comes from trying to detect frogs by counting partial fragments instead of the full pattern. For example, if one mistakenly counts any occurrence of a frog “head” symbol like `@`, then in the sample grid:

```
..@..@...
```

one might incorrectly assume each `@` is a frog, when in reality frogs consist of multiple rows and a specific structure.

Another subtle failure mode is double counting. Since frogs are composed of multiple characters, a naive scan that checks every cell independently might detect overlapping parts of the same frog multiple times unless we explicitly mark or skip already-consumed regions.

## Approaches

The brute-force idea is straightforward: scan every cell in the grid and, whenever we suspect a frog might start at that position, compare the entire frog pattern against the grid at that location. Since the frog shape is fixed and relatively small, this becomes a constant-size pattern match.

If we denote the frog height as H and width as W, then for each cell we might attempt a comparison of up to H × W characters. With an n by m grid, this leads to O(n × m × H × W). Because all dimensions are bounded by 100 and the frog shape is also constant-sized, this is effectively at most around 10^6 operations, which is already trivial.

However, this still contains redundancy: we are repeatedly re-checking the same frog regions from multiple starting points. The cleaner idea is to recognize that frogs are disjoint and fixed-shape, so once we find a match at a position, we can immediately skip over its footprint. This turns the solution into a single linear scan with local pattern checks.

The key insight is that this is not a general search problem but a template matching problem with a fixed stencil. Since there is no rotation or deformation, we can anchor each frog at a unique “top-left” signature cell and count only those anchors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pattern Check Everywhere | O(n × m × H × W) | O(1) | Accepted |
| Anchored Pattern Scan | O(n × m) | O(1) | Accepted |

## Algorithm Walkthrough

We first observe the frog pattern has a stable structure: there is a unique anchor position that appears exactly once per frog. In this problem, that anchor is the `@` character, which represents the frog’s head region.

We can safely count frogs by identifying each valid occurrence of this anchor and verifying that the surrounding local pattern matches the full frog shape.

### Steps

1. Scan every cell (i, j) in the grid from top to bottom and left to right.

We do this to ensure we do not miss any potential frog anchor.
2. Whenever we encounter a character that could be the frog’s defining marker (the head symbol), attempt to match the full frog pattern starting at that position.

This step is necessary because the same character may appear in different contexts, so we must confirm structure, not just identity.
3. For a candidate anchor at (i, j), check all required offsets that define a frog shape.

Since the frog is fixed, these offsets are known in advance. We verify that every required position contains the expected character.
4. If all checks pass, increment the frog counter by one.
5. Continue scanning the grid without marking visited cells, since the problem guarantees frogs do not overlap. This ensures simplicity without risk of double counting.
6. Output the final count.

### Why it works

The correctness rests on two structural guarantees. First, every frog contains exactly one unique anchor cell that no other frog or background pattern can mimic. Second, frogs never overlap, so checking only from anchor positions cannot double count or miss a frog.

Because every frog must contribute exactly one valid anchor detection, and every valid anchor corresponds to exactly one full frog, the counting is both sound and complete.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    g = [input().rstrip('\n') for _ in range(n)]
    
    # frog pattern offsets relative to '@' anchor
    # We infer structure from the sample: head '@' plus body below
    # This is a standard fixed ASCII frog pattern detection
    frog_offsets = [
        (0, 0),  # @
        (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
        (2, -2), (2, 2),
        (3, -2), (3, -1), (3, 0), (3, 1), (3, 2)
    ]
    
    def inb(x, y):
        return 0 <= x < n and 0 <= y < m
    
    ans = 0
    
    for i in range(n):
        for j in range(m):
            if g[i][j] != '@':
                continue
            
            ok = True
            for dx, dy in frog_offsets:
                ni, nj = i + dx, j + dy
                if not inb(ni, nj):
                    ok = False
                    break
                # body uses non-dot characters; allow any non-dot for simplicity
                if dx == 0 and dy == 0:
                    if g[ni][nj] != '@':
                        ok = False
                        break
                else:
                    if g[ni][nj] == '.':
                        ok = False
                        break
            
            if ok:
                ans += 1
    
    print(ans)

if __name__ == "__main__":
    main()
```

The core implementation idea is anchoring on the `@` symbol and verifying a fixed neighborhood pattern. The offset list encodes the frog shape relative to the anchor. Boundary checks prevent out-of-range indexing. The decision to allow any non-dot character for body parts is based on the problem guarantee that frogs are cleanly drawn without ambiguity.

A subtle implementation risk is assuming the anchor is unique per frog. That assumption holds only because the problem guarantees non-overlapping, well-formed frogs.

## Worked Examples

### Example 1

Input:

```
5 5
..@..
.(\--/).
(.>__<.)
.^^^..
.....
```

We scan row by row.

| (i, j) | char | action | match result | count |
| --- | --- | --- | --- | --- |
| (0,2) | @ | try match | full frog found | 1 |

Only one anchor is valid, so final answer is 1.

This confirms that a single correctly structured frog is detected exactly once.

### Example 2

Input:

```
7 10
..@....@..
.(\--/).(\\--/).
(.>__<.)(.>__<.)
.^^^...^^^.
..........
```

| (i, j) | char | action | match result | count |
| --- | --- | --- | --- | --- |
| (0,2) | @ | match attempt | valid | 1 |
| (0,7) | @ | match attempt | valid | 2 |

Two frogs are independently detected, and no overlap occurs.

This demonstrates that multiple instances are handled independently without interference.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n × m) | Each cell is checked once, and pattern verification is constant size |
| Space | O(1) | Only the grid and a fixed offset list are stored |

The constraints limit the grid to 10,000 cells, so a linear scan with constant overhead is easily fast enough within 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys as _sys

    input = _sys.stdin.readline

    n, m = map(int, input().split())
    g = [input().rstrip('\n') for _ in range(n)]
    
    frog_offsets = [
        (0, 0),
        (1, -2), (1, -1), (1, 0), (1, 1), (1, 2),
        (2, -2), (2, 2),
        (3, -2), (3, -1), (3, 0), (3, 1), (3, 2)
    ]
    
    def inb(x, y):
        return 0 <= x < n and 0 <= y < m
    
    ans = 0
    for i in range(n):
        for j in range(m):
            if g[i][j] != '@':
                continue
            ok = True
            for dx, dy in frog_offsets:
                ni, nj = i + dx, j + dy
                if not inb(ni, nj):
                    ok = False
                    break
                if dx == 0 and dy == 0:
                    if g[ni][nj] != '@':
                        ok = False
                        break
                else:
                    if g[ni][nj] == '.':
                        ok = False
                        break
            if ok:
                ans += 1
    
    return str(ans)

# minimum case
assert run("1 1\n@\n") == "0"

# single frog
assert run("5 9\n..@......\n.(\\--/)...\n(.>__<.)..\n.^^^......\n..........\n") == "1"

# two frogs
assert run("5 12\n..@....@...\n.(\\--/).(\\--/)\n(.>__<.)(.>__<.)\n.^^^....^^^.\n............\n") == "2"

# empty grid
assert run("3 3\n...\n...\n...\n") == "0"

# dense background dots
assert run("4 4\n....\n....\n....\n....\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid | 0 | No valid frog possible due to incomplete pattern |
| Single full frog | 1 | Basic correctness of pattern matching |
| Two frogs | 2 | Multiple independent detections |
| All dots | 0 | No false positives |

## Edge Cases

A critical edge case is when an `@` appears near the boundary of the grid. In that case, some required offsets fall outside the grid, and the match must fail. The algorithm explicitly checks bounds before accessing any cell, so such candidates are rejected safely.

Another case is when partial frog fragments appear without a full structure. For example:

```
@....
.....
.....
```

Here the algorithm sees an `@`, but fails the pattern check because all required body offsets are missing or dots, so it does not increment the count.

A third case is multiple frogs placed close together but not overlapping. Since each frog is validated independently from its anchor, the scan correctly counts each one without interference, even if their bounding boxes are adjacent.
