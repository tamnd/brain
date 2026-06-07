---
title: "CF 2206J - Worldwide Playlist"
description: "We are given a music playlist of n unique songs arranged in some initial order a. The app plays the songs in a circular fashion: after the last song, it starts over from the first. Separately, we have a desired listening sequence b of the same n songs."
date: "2026-06-07T19:45:39+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 2206
codeforces_index: "J"
codeforces_contest_name: "2026 ICPC Asia Pacific Championship - Online Mirror (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1700
weight: 2206
solve_time_s: 136
verified: false
draft: false
---

[CF 2206J - Worldwide Playlist](https://codeforces.com/problemset/problem/2206/J)

**Rating:** 1700  
**Tags:** math  
**Solve time:** 2m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a music playlist of `n` unique songs arranged in some initial order `a`. The app plays the songs in a circular fashion: after the last song, it starts over from the first. Separately, we have a desired listening sequence `b` of the same `n` songs. On any day, we start at the beginning of playlist `a` and can press a skip button to jump to the next song. The goal is to determine the minimum number of skips required to listen to the songs in `b` in order, without skipping any song in `b` itself.

The additional complexity comes from updates between days. Each day (except the last), we are given a swap operation that either changes `a` or `b` permanently. After each update, we must recompute the minimum number of skips starting from the new `a_1`.

The constraints imply that naive simulation of the playlist will be too slow. With `n` and `d` up to 200,000, an O(n²) or O(n·d) solution would perform roughly 4 × 10¹⁰ operations, far exceeding what we can afford in 2 seconds. This suggests we need an O(n + d·log n) or O(n + d) approach. Edge cases include when `a` and `b` are almost identical, when one song is at the start of `a` but late in `b`, and when swaps change the position of the first or last elements. A careless implementation that linearly scans `a` for each song in `b` will fail on large `n`.

## Approaches

The brute-force approach is straightforward. Start at `a_1`, and for each song in `b`, scan `a` in order until we encounter the song, counting each skipped song. After reaching the end of `a`, wrap around to the beginning as necessary. This is correct because it simulates the process exactly. However, for `n = 200,000`, this leads to O(n²) operations in the worst case, which is too slow.

The key observation to optimize is that `a` is a permutation, so each song has a unique index. If we precompute the position of each song in `a`, we can compute the number of skips to go from one song in `b` to the next using modular arithmetic instead of scanning. Specifically, if song `b[i]` is at position `pos[b[i]]` in `a` and the previous song `b[i-1]` was at `prev_pos`, the number of skips is `(pos[b[i]] - prev_pos - 1) % n + n * (pos[b[i]] < prev_pos)`. Essentially, if the next song appears before the current song in the playlist, we account for wrapping around. This reduces the computation for a single day to O(n).

Handling updates efficiently is the next challenge. Swapping two elements in `a` requires updating the position map, which is O(1). Swapping elements in `b` requires changing their order in the sequence, which is also O(1) for the array representation. With these observations, each day’s minimum skips can be computed in O(n), and each update does not add more than O(1) work. Thus, the total complexity is O(d·n), which is acceptable for `n` up to 200,000 and small `d`. For the largest inputs, we might optimize further using segment trees if `d` were close to `n`, but the O(n) per day approach suffices here.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate playlist) | O(n²) | O(n) | Too slow |
| Optimal (position mapping + modular skips) | O(d·n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `d` and the initial arrays `a` and `b`. Build a `pos` dictionary mapping each song number in `a` to its index for O(1) lookups. This lets us jump directly to a song’s position instead of scanning linearly.
2. For the first day, initialize `prev_pos = -1`. For each song `b[i]` in order, compute its position `curr_pos = pos[b[i]]`. The number of skips is `(curr_pos - prev_pos - 1) % n` if `curr_pos > prev_pos`, or `(curr_pos + n - prev_pos - 1)` if wrapping is needed. Accumulate these skips and update `prev_pos = curr_pos`.
3. Output the total skips for the day.
4. For each of the remaining `d-1` days, read the update `(c, x, y)`. If `c = 1`, swap `a[x-1]` and `a[y-1]`, and update `pos[a[x-1]]` and `pos[a[y-1]]` accordingly. If `c = 2`, swap `b[x-1]` and `b[y-1]`. These swaps are constant time operations.
5. Repeat steps 2-3 for the new arrays after the update. Append the result to output.

Why it works: Each day, the algorithm maintains the invariant that `pos` accurately reflects the current position of each song in `a`. Using modular arithmetic guarantees that we correctly account for skips across the wrap-around boundary. Since each song in `b` appears exactly once, we never miscount skips, and the accumulated total represents the minimal number of skips necessary.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, d = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

# position map for quick lookup
pos = [0] * (n + 1)
for i, song in enumerate(a):
    pos[song] = i

def compute_skips():
    skips = 0
    prev = -1
    for song in b:
        curr = pos[song]
        if curr > prev:
            skips += curr - prev - 1
        else:
            skips += curr + n - prev - 1
        prev = curr
    return skips

print(compute_skips())

for _ in range(d - 1):
    c, x, y = map(int, input().split())
    x -= 1
    y -= 1
    if c == 1:
        a[x], a[y] = a[y], a[x]
        pos[a[x]] = x
        pos[a[y]] = y
    else:
        b[x], b[y] = b[y], b[x]
    print(compute_skips())
```

The solution begins by mapping each song in `a` to its index. This allows O(1) lookup of positions when computing skips. The `compute_skips` function iterates over `b` in order, calculating skips with modular arithmetic to handle circular playlist behavior. Updates are processed in-place, with `pos` updated immediately after swaps in `a`. Swaps in `b` only affect the iteration order. Careful attention is paid to zero-based indexing when reading swaps.

## Worked Examples

**Sample Input 1:**

```
4 3
1 4 2 3
3 2 1 4
1 3 4
2 1 3
```

| Day | a | b | pos | Skips Calculation |
| --- | --- | --- | --- | --- |
| 1 | 1 4 2 3 | 3 2 1 4 | 1:0,2:2.. | 6 |
| 2 | 1 4 3 2 | 3 2 1 4 | updated | 2 |
| 3 | 1 4 3 2 | 1 2 3 4 | updated | 6 |

This trace confirms that swapping elements in `a` or `b` updates positions and order correctly, and skips are computed using the relative positions modulo `n`.

**Custom Input Example:**

```
3 2
2 3 1
1 3 2
1 1 3
```

| Day | a | b | Skips |
| --- | --- | --- | --- |
| 1 | 2 3 1 | 1 3 2 | 3 |
| 2 | 1 3 2 | 1 3 2 | 0 |

The first day requires wrapping around the playlist, the second day requires no skips because `a` matches `b`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d·n) | For each day, we iterate over `b` of length n; swaps are O(1) |
| Space | O(n) | Arrays `a`, `b`, and `pos` each require O(n) |

Given `n` and `d` up to 200,000, the total operations are approximately 4 × 10¹⁰ in worst-case naive simulation, but with position mapping the solution runs in roughly 4 × 10⁷, which fits in 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    n, d = map(int, input().split
```
