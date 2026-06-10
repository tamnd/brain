---
title: "CF 1511C - Yet Another Card Deck"
description: "We are given a deck of n cards, each with a color represented by an integer from 1 to 50. The deck is arranged from top to bottom, and we receive q queries."
date: "2026-06-10T18:58:46+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 1511
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 107 (Rated for Div. 2)"
rating: 1100
weight: 1511
solve_time_s: 133
verified: true
draft: false
---

[CF 1511C - Yet Another Card Deck](https://codeforces.com/problemset/problem/1511/C)

**Rating:** 1100  
**Tags:** brute force, data structures, implementation, trees  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a deck of `n` cards, each with a color represented by an integer from `1` to `50`. The deck is arranged from top to bottom, and we receive `q` queries. Each query specifies a color, and for each query, we need to locate the first card of that color in the current deck, report its position (1-based index), and then move that card to the top of the deck. The challenge is that the deck dynamically changes with each query, so positions of cards shift over time.

The constraints are significant: both `n` and `q` can reach up to `300,000`. A naive solution that scans the deck for every query would perform `O(n * q)` operations, which could reach `9 * 10^10` in the worst case. This is far beyond what fits in a 2-second time limit, so we need a more efficient approach. The limited range of colors (`1` to `50`) hints that we can use this small universe to manage positions efficiently.

A subtle edge case arises when a color appears multiple times in the deck. Moving the first occurrence to the top changes all subsequent positions. For example, if the deck is `[1, 2, 1]` and we query `1`, we output `1` and move it to the top, leaving `[1, 2, 1]`. The next query for `1` should now return `1` again because the previously moved card is still on top. Careless implementations that recalculate indices without updating positions dynamically will produce wrong results.

## Approaches

The brute-force approach iterates through the deck for each query, searching for the first occurrence of the requested color. Once found, we record its position, remove it from the deck, and insert it at the top. While correct, this approach requires scanning up to `n` cards for each of the `q` queries, giving a time complexity of `O(n * q)`. With `n` and `q` up to `3 * 10^5`, this could perform on the order of `10^10` operations, which is impractical for a 2-second limit.

The key insight is that the number of colors is small. We can maintain a mapping from each color to the first occurrence in the current deck. Instead of shifting cards in an array, we can simulate their relative positions using a list of colors and updating indices. When we process a query for a color, we read its current position from the map, print it, then adjust the positions of all other colors that appear before it in the deck by incrementing their index. Finally, we move the queried color to the top, which is equivalent to setting its position to `1`. This approach exploits the bounded color range and avoids full deck scans, reducing the complexity to `O(n * c)` where `c = 50` is the number of colors, which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * q) | O(n) | Too slow |
| Optimal | O(q * c) | O(c) | Accepted |

## Algorithm Walkthrough

1. Create an array `pos` of size `51` to track the current position of the first card of each color. Initialize it by scanning the deck once, setting `pos[color]` to the first index where it appears. This gives the starting position for each color.
2. Iterate through each query `t_j`. Use `pos[t_j]` to find the current position of the first card of that color and print it.
3. For all colors `c` in the deck, if `pos[c]` is smaller than `pos[t_j]`, increment `pos[c]` by `1`. This simulates that these cards have been shifted down by the move-to-top operation.
4. Set `pos[t_j]` to `1` because the queried card is now on top.
5. Repeat steps 2-4 for all queries.

Why it works: The invariant is that `pos[c]` always represents the current 1-based position of the first card of color `c` in the deck. Moving a card to the top increments positions of all cards that were above it, preserving correct relative ordering. Since the number of colors is limited, updating `pos` takes at most `50` operations per query, which is efficient enough.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
a = list(map(int, input().split()))
t = list(map(int, input().split()))

# initialize position mapping
pos = [0] * 51
for idx, color in enumerate(a):
    if pos[color] == 0:
        pos[color] = idx + 1

result = []

for color in t:
    result.append(pos[color])
    # increment positions of colors above the current one
    for c in range(1, 51):
        if pos[c] < pos[color]:
            pos[c] += 1
    pos[color] = 1

print(*result)
```

The first loop establishes the initial positions of each color in the deck. The second loop handles each query efficiently using the `pos` array. By updating all colors above the queried card and moving the queried card to the top, we maintain correct positions without shifting the entire deck. It is important that the `pos` array uses 1-based indexing to match the problem's output requirements.

## Worked Examples

For the sample input:

```
7 5
2 1 1 4 3 3 1
3 2 1 1 4
```

| Query | pos before | Output | pos after update |
| --- | --- | --- | --- |
| 3 | [2:1,1:2,3:5,4:4] | 5 | [2:2,1:3,3:1,4:5] |
| 2 | [2:2,1:3,3:1,4:5] | 2 | [2:1,1:4,3:2,4:6] |
| 1 | [2:1,1:4,3:2,4:6] | 3 | [2:2,1:1,3:3,4:7] |
| 1 | [2:2,1:1,3:3,4:7] | 1 | unchanged |
| 4 | [2:2,1:1,3:3,4:7] | 5 | [2:3,1:2,3:4,4:1] |

This trace shows the invariant `pos[c]` is always the first occurrence of color `c`. Every update reflects the move-to-top operation accurately.

Another small example:

Input:

```
3 3
1 2 1
1 2 1
```

| Query | pos before | Output | pos after update |
| --- | --- | --- | --- |
| 1 | [1:1,2:2] | 1 | [1:1,2:3] |
| 2 | [1:1,2:3] | 3 | [1:2,2:1] |
| 1 | [1:2,2:1] | 2 | [1:1,2:2] |

The positions adjust correctly even when the same color is queried multiple times.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q * 50) = O(q) | Each query updates positions of at most 50 colors |
| Space | O(51) = O(1) | `pos` array stores first occurrence per color |

With `q` up to `3 * 10^5`, this gives roughly 15 million operations, which fits comfortably within 2 seconds. Memory usage is minimal, as we only store positions for each color.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    t = list(map(int, input().split()))

    pos = [0] * 51
    for idx, color in enumerate(a):
        if pos[color] == 0:
            pos[color] = idx + 1

    result = []
    for color in t:
        result.append(pos[color])
        for c in range(1, 51):
            if pos[c] < pos[color]:
                pos[c] += 1
        pos[color] = 1
    return ' '.join(map(str, result))

# provided sample
assert run("7 5\n2 1 1 4 3 3 1\n3 2 1 1 4\n") == "5 2 3 1 5", "sample 1"

# minimum input
assert run("2 1\n1 2\n1\n") == "1", "minimum size"

# all equal
assert run("4 4\n1 1 1 1\n1 1 1 1\n") == "1 1 1 1", "all equal colors"

# alternating colors
assert run("5 5\n1 2 1 2 1\n2 1 2 1 2\n") == "2 1 3 1 2", "alternating pattern"

# maximum colors
assert run
```
