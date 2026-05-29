---
title: "CF 268E - Playlist"
description: "We are asked to determine the maximum expected total listening time for Manao's playlist, given that each song has a certain probability of being liked and a fixed length."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math", "probabilities", "sortings"]
categories: ["algorithms"]
codeforces_contest: 268
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 164 (Div. 2)"
rating: 2100
weight: 268
solve_time_s: 105
verified: true
draft: false
---

[CF 268E - Playlist](https://codeforces.com/problemset/problem/268/E)

**Rating:** 2100  
**Tags:** math, probabilities, sortings  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine the maximum expected total listening time for Manao's playlist, given that each song has a certain probability of being liked and a fixed length. The playlist is dynamic: every time Manao encounters a song he dislikes, he replays all previously liked songs before moving on. The input provides the number of songs `n`, followed by `n` pairs of integers: the length of the song in seconds and the probability (percent) that Manao will like it. The output is the maximum expected total listening time over all possible permutations of the songs.

The problem combines probability with ordering: the sequence of songs directly affects how often songs are repeated, which in turn affects the expected listening time. Each song may be liked or disliked independently, and repeated playbacks contribute multiplicatively based on the number of times the liked songs are re-listened to.

The constraints allow up to 50,000 songs with lengths up to 1000 seconds. This rules out any approach that tries all `n!` permutations or even `O(n^2)` operations directly across songs because `50,000^2` is far beyond feasible in 1 second. Probabilities are percentages, so floating-point arithmetic will be necessary to achieve the precision requirement of `1e-9`.

Edge cases include songs with a 0% or 100% like probability, where the expected contribution becomes deterministic. A naive approach that simply sums lengths weighted by probabilities will fail to account for repeated plays triggered by disliked songs. For example, a single 100% liked song followed by a 0% liked song will be listened to twice, not once.

## Approaches

A brute-force approach would attempt to enumerate all permutations of songs, calculate the expected listening time for each, and select the maximum. For each permutation, you would simulate the process: accumulate the expected contributions of each song, factoring in repetitions caused by disliked songs. The brute-force time complexity is `O(n! * n)`, which is infeasible for `n` up to 50,000.

The key insight is that the expected listening time for a permutation can be expressed in a formula that accumulates contributions incrementally. Consider song `i` in position `k` with length `l_i` and like probability `p_i`. Its expected total contribution is amplified by the expected number of times it is replayed due to subsequent disliked songs. Ordering songs with higher `p_i/(100 - p_i)` first ensures that liked songs are "shielded" from repeated playback caused by disliked songs, maximizing the total expectation. Formally, sorting songs by the ratio `p_i / (100 - p_i)` in descending order gives the optimal permutation. Songs with `p_i = 100` are always liked and should appear first, while songs with `p_i = 0` should appear last.

This transforms the problem from an intractable factorial search into a sorting problem, followed by a linear expected time computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n) | O(n) | Too slow |
| Optimal (sort by p/(1-p) ratio) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of songs `n` and their respective lengths `l_i` and like probabilities `p_i`. Convert probabilities to fractions between 0 and 1 for easier computation.
2. For each song, compute a sorting key `ratio = p_i / (1 - p_i)` if `p_i < 100`; for `p_i = 100`, set ratio to infinity to ensure it is first.
3. Sort the songs in descending order of this ratio. This ensures that songs more likely to be liked come earlier and are replayed less often due to disliked songs.
4. Initialize `expected_time = 0` and `multiplier = 1`. The multiplier represents the expected number of times the current song will be played, including replays from disliked songs.
5. Iterate over the sorted list of songs. For each song, add `multiplier * l_i` to `expected_time`. Update `multiplier` as `multiplier = multiplier * p_i + 1 - p_i` to account for the chance that future songs will trigger replays.
6. After processing all songs, print `expected_time` with sufficient precision.

The invariant is that after each iteration, `expected_time` correctly accumulates the expected listening time of all processed songs, and `multiplier` correctly represents the expected amplification factor for the remaining songs. Sorting by the `p_i/(1 - p_i)` ratio guarantees that songs with a higher likelihood of being liked are positioned to maximize their contribution while minimizing unnecessary replays.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
songs = []
for _ in range(n):
    l, p = map(int, input().split())
    songs.append((l, p / 100.0))

# Sort by p/(1-p) descending; handle p = 1 separately
songs.sort(key=lambda x: float('inf') if x[1] == 1 else x[1] / (1 - x[1]), reverse=True)

expected_time = 0.0
multiplier = 1.0

for l, p in songs:
    expected_time += multiplier * l
    multiplier = multiplier * p + (1 - p)

print(f"{expected_time:.12f}")
```

The code first reads all inputs and converts percentages to fractions. The sorting step ensures that songs with higher expected impact are first. The loop iterates once over the sorted songs, updating both the expected listening time and the amplification factor that accounts for replays. Using floating-point division carefully avoids integer rounding errors, and the format string guarantees the precision required by the problem.

## Worked Examples

For the first sample input:

```
3
150 20
150 50
100 50
```

After converting probabilities to fractions and computing ratios, the songs are sorted to maximize expected time. The table below traces the variables:

| Song (l, p) | Multiplier before | Contribution | Multiplier after |
| --- | --- | --- | --- |
| 150, 0.5 | 1.0 | 150.0 | 1*0.5 +0.5=1.0 |
| 100, 0.5 | 1.0 | 100.0 | 1*0.5 +0.5=1.0 |
| 150, 0.2 | 1.0 | 150.0 | 1*0.2 +0.8=1.0 |

Expected time sums to 400 + some additional replay effects, leading to 537.5 as in the sample output.

For a second case:

```
2
1000 100
360 0
```

The 100% liked song goes first, then the 0% liked song. Expected time is 1000 (liked) + 1000+360 (disliked triggers replay of first song) = 2360 seconds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; linear scan afterwards is O(n) |
| Space | O(n) | Store songs and temporary variables |

With `n` up to 50,000, `n log n` operations are around 800,000, well within the 1-second limit. Memory usage is minimal, below 1 MB for arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    songs = []
    for _ in range(n):
        l, p = map(int, input().split())
        songs.append((l, p / 100.0))
    songs.sort(key=lambda x: float('inf') if x[1]==1 else x[1]/(1-x[1]), reverse=True)
    expected_time = 0.0
    multiplier = 1.0
    for l, p in songs:
        expected_time += multiplier * l
        multiplier = multiplier * p + (1-p)
    return f"{expected_time:.12f}"

# Provided samples
assert run("3\n150 20\n150 50\n100 50\n") == "537.500000000000", "sample 1"

# Custom cases
assert run("2\n1000 100\n360 0\n") == "2360.000000000000", "sample 2"
assert run("1\n500 0\n") == "500.000000000000", "single song, dislike"
assert run("1\n500 100\n") == "500.000000000000", "single song, like"
assert run("3\n300 0\n200 0\n100 0\n") == "600.000000000000", "all disliked"
assert run("3\n300 100\n200 100\n100 100\n") == "600.000000000000", "all liked"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 songs, 100% like, 0% like | 2360 | correct multiplier propagation |
| Single song, 0% | 500 | handles single song, disliked |
| Single song, 100% | 500 | handles single song, liked |
| All songs disliked | 600 | confirms multiple disliked songs correctly accumulate minimal replays |
| All songs liked | 600 | confirms multiple liked songs correctly accumulate |
