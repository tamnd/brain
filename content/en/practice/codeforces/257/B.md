---
title: "CF 257B - Playing Cubes"
description: "We are asked to simulate a game between two players arranging colored cubes in a line. Petya wants to maximize the number of consecutive cubes of the same color, while Vasya wants to maximize the number of consecutive cubes of different colors."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 257
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 159 (Div. 2)"
rating: 1300
weight: 257
solve_time_s: 83
verified: true
draft: false
---

[CF 257B - Playing Cubes](https://codeforces.com/problemset/problem/257/B)

**Rating:** 1300  
**Tags:** games, greedy, implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a game between two players arranging colored cubes in a line. Petya wants to maximize the number of consecutive cubes of the same color, while Vasya wants to maximize the number of consecutive cubes of different colors. Petya moves first, and the total number of moves equals the total number of cubes, _n_ red and _m_ blue. The final score is the number of same-color neighbor pairs for Petya and the number of different-color neighbor pairs for Vasya.

The key constraints are that both _n_ and _m_ can go up to 100,000. This means any algorithm iterating through all possible cube arrangements is hopeless, because there are factorially many permutations. We need an approach that computes the optimal outcome directly without simulating every sequence.

The edge cases to watch include situations where one color dominates the other. For instance, if _n = 1_ and _m = 3_, naive reasoning might suggest alternating as much as possible, but since Petya starts and wants consecutive colors, he can force a block of the majority color to maximize his points. Another subtle case occurs when _n = m_, where the scores are almost balanced, but the first move can slightly tip the total points in Petya's favor. These cases show that the order of moves and the color choice for the first move is critical.

## Approaches

The brute-force approach is straightforward: try every possible ordering of the cubes, simulate the moves, and count the scores. This works correctly because it exhaustively explores all sequences. However, with up to 2 × 10^5 cubes, the number of permutations is astronomical, so this approach is infeasible.

The key observation for an optimal solution is that the game reduces to a simple property of the counts: the player who wants consecutive colors benefits by choosing the color with the largest remaining block when possible, while the player who wants alternation benefits by forcing a switch. Petya moves first and prefers grouping the majority color at the start. Vasya reacts by alternating if possible. The total points for Petya are simply the count of the largest color minus one, because the longest possible contiguous block yields maximum same-color pairs. The points for Vasya are the minimum of _n_ and _m_, which represents the maximum number of alternations achievable.

This insight lets us skip any detailed simulation and compute the result in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n+m)!) | O(n+m) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Identify the color with more cubes. Let _max_color_ = max(n, m) and _min_color_ = min(n, m). This ensures Petya can start with the majority color and maximize consecutive pairs.
2. Petya's score is _max_color - 1_. Placing the first cube of the larger color allows him to build a contiguous block. Each additional cube of the same color creates one more same-color neighbor pair.
3. Vasya's score is _min_color_. After Petya builds his block, the remaining cubes of the minority color will inevitably alternate with the tail of the majority color. Each such alternation gives Vasya a point.
4. Print the results as two integers: Petya's score followed by Vasya's score.

The reasoning hinges on the invariant that, with optimal play, Petya can always front-load the majority color, producing the maximum possible consecutive pairs, and Vasya can only score as many alternations as the minority color allows. No sequence can yield more points for either player because any deviation reduces the number of consecutive pairs for Petya or alternations for Vasya.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

petya_score = max(n, m) - 1
vasya_score = min(n, m)

print(f"{petya_score} {vasya_score}")
```

The code first reads the counts of red and blue cubes. We immediately calculate Petya's score as the larger of the two counts minus one. Vasya's score is the smaller count. Using `max` and `min` avoids any need to distinguish red or blue by name. Printing the results in the required order matches the expected output format. There are no tricky off-by-one errors because the first cube does not create a neighbor pair, so we subtract one from the maximum count to get Petya's score.

## Worked Examples

**Sample 1**

Input: 3 1

| Step | n | m | max_color | min_color | Petya | Vasya |
| --- | --- | --- | --- | --- | --- | --- |
| initial | 3 | 1 | 3 | 1 | - | - |
| compute scores | - | - | - | - | 2 | 1 |

Explanation: Petya starts with red, creating a block of 3 reds. He scores 2 points for the two consecutive red pairs. Vasya scores 1 point from the alternation when the single blue cube is placed.

**Custom Example**

Input: 2 2

| Step | n | m | max_color | min_color | Petya | Vasya |
| --- | --- | --- | --- | --- | --- | --- |
| initial | 2 | 2 | 2 | 2 | - | - |
| compute scores | - | - | - | - | 1 | 2 |

Explanation: With equal counts, Petya can only create one consecutive pair. Vasya gets two points because each color change between the two pairs counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a couple of arithmetic operations and comparisons. |
| Space | O(1) | Only storing a few integers for counts and scores. |

With n and m up to 10^5, this constant-time solution easily fits within the 2-second limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    petya_score = max(n, m) - 1
    vasya_score = min(n, m)
    return f"{petya_score} {vasya_score}"

# provided samples
assert run("3 1\n") == "2 1", "sample 1"

# custom cases
assert run("2 2\n") == "1 2", "equal cubes"
assert run("1 1\n") == "0 1", "minimum size"
assert run("100000 1\n") == "99999 1", "maximum size, extreme imbalance"
assert run("5 5\n") == "4 5", "all equal values"
assert run("1 100000\n") == "99999 1", "opposite extreme imbalance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 | 1 2 | Equal counts, balance of points |
| 1 1 | 0 1 | Minimum input size |
| 100000 1 | 99999 1 | Large numbers, extreme imbalance |
| 5 5 | 4 5 | Small equal numbers, basic calculation |
| 1 100000 | 99999 1 | Reverse extreme imbalance, first move advantage |

## Edge Cases

For n = 1 and m = 1, Petya cannot form any consecutive pair, so his score is 0. Vasya can score 1 from the single alternation. The algorithm computes max(1, 1) - 1 = 0 and min(1, 1) = 1, exactly correct. For a highly unbalanced case like n = 100000, m = 1, Petya's strategy is to start with the majority color, creating a block of 100,000 cubes and scoring 99999, while Vasya can only insert the single blue cube to get 1 point. The formula correctly handles these extremes without iteration.
