---
title: "CF 266B - Queue at the School"
description: "We are given a line of children represented as a string where each character is either a boy or a girl. The line evolves over time in discrete steps. During each second, every adjacent pair where a boy stands immediately before a girl swaps positions simultaneously."
date: "2026-06-04T18:12:53+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graph-matchings", "implementation", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 266
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 163 (Div. 2)"
rating: 800
weight: 266
solve_time_s: 72
verified: true
draft: false
---

[CF 266B - Queue at the School](https://codeforces.com/problemset/problem/266/B)

**Rating:** 800  
**Tags:** constructive algorithms, graph matchings, implementation, shortest paths  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of children represented as a string where each character is either a boy or a girl. The line evolves over time in discrete steps. During each second, every adjacent pair where a boy stands immediately before a girl swaps positions simultaneously. In other words, all valid “BG” patterns become “GB” in the same second, and all swaps happen in parallel rather than one after another from left to right.

The task is to determine the configuration of the line after exactly t seconds of applying this transformation rule.

The constraints are very small, with n and t both at most 50. This immediately tells us that even a straightforward simulation is acceptable because the worst-case number of operations is on the order of n multiplied by t, which is at most 2500 swap checks per run. Even if we repeat character scans for each second, the total work is trivial under a 2-second limit.

A subtle edge case arises from the simultaneous nature of swaps. If we process left to right and immediately swap characters in place, we can accidentally reuse updated information in the same second. For example, consider “BGBG”. If we greedily swap the first pair “BG”, we get “GBBG”, and then the next pair is evaluated incorrectly because the structure has already changed mid-step. The correct interpretation requires all swaps for a second to be based on the same snapshot of the string.

Another edge case is when swaps overlap. In a pattern like “BGB”, only the first pair swaps in a single step, and the middle character participates in at most one swap per second. This prevents double movement within a single time unit.

## Approaches

The most direct way to model the process is to literally simulate each second. For each time step, we scan the string from left to right and whenever we see a “BG” pattern, we swap it into “GB” and skip the next position since it has already moved as part of the swap. This approach matches the problem definition exactly and preserves correctness because we simulate one full second at a time using a fresh pass over the current state.

This brute-force simulation already performs well enough because each second requires a single pass over the string, giving O(n) work per second. Over t seconds, the total work is O(n·t), which is bounded by 2500 operations.

There is no need for a more advanced optimization because the constraints do not push us toward asymptotic improvements. The key insight is not about speeding up computation, but about correctly modeling simultaneous swaps by ensuring we do not chain updates inside a single second.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Step-by-step simulation | O(n·t) | O(n) | Accepted |
| Optimized global movement model | O(n) | O(n) | Accepted but unnecessary |

## Algorithm Walkthrough

1. Start with the initial queue as a mutable list of characters. This allows efficient swapping.
2. Repeat the process for t seconds. Each iteration represents one full synchronized transformation step.
3. During each second, scan from left to right using an index i starting at 0.
4. If the current position i and the next position i+1 form the pattern “B” followed by “G”, swap them.
5. After performing a swap, increment i by 2 to avoid reprocessing the newly swapped character.
6. If no swap occurs at position i, move i forward by 1.
7. After finishing the full scan, the resulting list represents the queue after one second.
8. Continue until all t seconds are simulated.

The key reasoning behind skipping indices after a swap is that a swapped “GB” pair should not be reconsidered in the same second. If we did not skip, the same girl could be involved in multiple swaps in a single time step, which violates the simultaneous swap rule.

### Why it works

The correctness rests on the invariant that at the start of each second, the array represents the state after exactly that many full transformations. Within a single second, each swap is applied based only on the original configuration of that second, because we scan left to right and ensure that once a swap occurs, both positions are consumed for that step. This prevents cascading effects inside the same second and ensures all swaps correspond exactly to disjoint “BG” pairs in the current snapshot.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, t = map(int, input().split())
s = list(input().strip())

for _ in range(t):
    i = 0
    while i < n - 1:
        if s[i] == 'B' and s[i + 1] == 'G':
            s[i], s[i + 1] = s[i + 1], s[i]
            i += 2
        else:
            i += 1

print("".join(s))
```

The solution stores the queue as a list so swaps are O(1). Each second is simulated independently. The inner loop carefully enforces the rule that swaps are based on a single frozen configuration per second by scanning once and advancing the index appropriately.

A common mistake is updating the string left-to-right without skipping indices after swaps. That leads to double-processing a character that has just moved, which violates the simultaneous nature of the transformation.

## Worked Examples

### Example 1

Input:

```
5 1
BGGBG
```

We simulate one second.

| i | pair checked | action | state |
| --- | --- | --- | --- |
| 0 | BG | swap | GBGBG |
| 2 | GB | none | GBGBG |
| 3 | BG | swap | GBGGB |

Final result is `GBGGB`.

This shows that swaps are independent and based only on the initial configuration of that second.

### Example 2

Input:

```
4 2
BGBG
```

We track two seconds.

After second 1:

| i | pair | action | state |
| --- | --- | --- | --- |
| 0 | BG | swap | GBGB |
| 2 | BG | swap | GGBB |

After second 2:

| i | pair | action | state |
| --- | --- | --- | --- |
| 0 | GG | none | GGBB |
| 1 | GB | none | GGBB |
| 2 | BB | none | GGBB |

Final result is `GGBB`.

This demonstrates how movement naturally saturates when all girls are already ahead of boys.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·t) | Each of t seconds performs a single linear scan over the string |
| Space | O(n) | We store the queue as a mutable list of characters |

Given n, t ≤ 50, the maximum number of operations is tiny, far below any practical limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, t = map(int, input().split())
    s = list(input().strip())

    for _ in range(t):
        i = 0
        while i < n - 1:
            if s[i] == 'B' and s[i + 1] == 'G':
                s[i], s[i + 1] = s[i + 1], s[i]
                i += 2
            else:
                i += 1

    return "".join(s)

# provided sample
assert run("5 1\nBGGBG\n") == "GBGGB"

# all same
assert run("4 3\nGGGG\n") == "GGGG"

# all boys
assert run("4 2\nBBBB\n") == "BBBB"

# alternating pattern
assert run("6 1\nBGBGBG\n") == "GBGBGB"

# multiple steps
assert run("5 2\nBGGBG\n") == run("5 1\n" + "GBGGB\n")

# max small stress
assert run("1 50\nB\n") == "B"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 3 / GGGG | GGGG | No swaps occur |
| 4 2 / BBBB | BBBB | No valid BG pairs |
| 6 1 / BGBGBG | GBGBGB | Multiple independent swaps |
| 1 50 / B | B | Minimum boundary size |

## Edge Cases

A key edge case is when swaps are adjacent, such as “BGB”. During a single second, only the first “BG” should swap, producing “GBB”. The algorithm handles this correctly because after swapping indices 0 and 1, the pointer jumps to index 2, preventing the second character from participating in another swap within the same second.

Another edge case is a fully alternating string like “BGBGBG”. The algorithm ensures that swaps happen independently for each disjoint pair, and skipping after swaps prevents overlap corruption.

Finally, a no-op case such as all “G” or all “B” strings confirms stability. Since no “BG” patterns exist, the scan performs no swaps in any second, and the invariant state is preserved across all iterations.
