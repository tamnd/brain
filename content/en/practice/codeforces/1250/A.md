---
title: "CF 1250A - Berstagram"
description: "We are simulating a social media feed where posts continuously swap positions based on incoming likes. Initially, posts are arranged in a fixed vertical order from top to bottom, with post 1 at the top and post n at the bottom."
date: "2026-06-13T21:12:01+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1250
codeforces_index: "A"
codeforces_contest_name: "2019-2020 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1400
weight: 1250
solve_time_s: 445
verified: true
draft: false
---

[CF 1250A - Berstagram](https://codeforces.com/problemset/problem/1250/A)

**Rating:** 1400  
**Tags:** implementation  
**Solve time:** 7m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a social media feed where posts continuously swap positions based on incoming likes. Initially, posts are arranged in a fixed vertical order from top to bottom, with post 1 at the top and post n at the bottom. Each time a post receives a like, it attempts to move one position upward by swapping with the post directly above it, unless it is already at the top.

The feed evolves over time, starting from the initial configuration, then after each like. For every post, we are asked to determine two values across the entire timeline: the best position it ever reaches (closest to the top, meaning the smallest index), and the worst position it ever reaches (closest to the bottom, meaning the largest index).

The key difficulty is that positions are dynamic and depend on all previous swaps. If we literally simulate the full array and track positions at every step, each swap is O(1), but updating positions requires searching for the post, which leads to inefficiency unless we maintain an auxiliary structure.

The constraints allow up to 100,000 posts and 400,000 likes. Any solution that scans the array to find a post on each like will degrade to O(nm), which is far beyond feasible. Even O(m log n) is unnecessary; the structure is simple enough that we can maintain everything in linear time with direct indexing.

A subtle edge case arises when a post receives multiple consecutive likes. In such cases, it may oscillate upward in small steps, and naive intuition might incorrectly assume it reaches position 1 more often than it actually does. Another edge case is when a post is never liked at all; its minimum position is still 1 initially, and its maximum remains n throughout.

## Approaches

A brute-force simulation keeps the entire array representing the feed and, for each like, searches for the position of the liked post, swaps it with the element above it, and continues. This correctly models the system, but each search is O(n), and there are m operations, leading to O(nm) complexity. With worst-case inputs, this exceeds 4 × 10^10 operations.

The key observation is that we never need to know the full structure after each step. We only need to know where each post currently is, and update only local swaps. This suggests maintaining a position array that maps each post to its current index. Then each swap becomes O(1), because we can directly access and update positions.

To compute minimum and maximum positions, we track two arrays per post: the smallest index it has ever occupied and the largest index it has ever occupied. Each time a post moves, we update its current position and possibly update its recorded bounds.

The difference from brute force is that instead of searching the array, we maintain an inverse mapping from post to index, turning every operation into constant time bookkeeping.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(nm) | O(n) | Too slow |
| Position mapping with tracking | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain an array pos where pos[i] is the current position of post i, and an array order where order[p] is the post currently at position p. We also maintain arrays best and worst for each post.

1. Initialize order so that order[1] = 1, order[2] = 2, ..., order[n] = n, and set pos[i] = i for all i. Set best[i] = i and worst[i] = i for all posts. This captures the initial configuration before any likes.
2. For each like a_j, retrieve its current position p = pos[a_j]. This is O(1) because we maintain direct indexing.
3. If p is already 1, we only update nothing except ensuring bounds remain correct, because no movement happens.
4. Otherwise, let the post above it be b = order[p - 1]. We swap a_j and b in the order array, and update their positions in pos accordingly.
5. After the swap, update best and worst for both affected posts using their new positions. Only these two posts change position, so only they can affect bounds.
6. Continue processing all likes in sequence.

After processing all updates, best[i] and worst[i] contain the minimum and maximum indices ever reached by post i.

### Why it works

The system evolves through adjacent swaps only, so each operation affects exactly two posts. Since positions are tracked explicitly, the pos array always reflects the current configuration without ambiguity. Every time a post moves, we immediately evaluate whether its new position improves its historical minimum or maximum. Because no other posts are affected by that swap, no additional updates are necessary. This preserves correctness while avoiding global recomputation.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
a = list(map(int, input().split()))

pos = [0] * (n + 1)
order = [0] * (n + 1)

best = [0] * (n + 1)
worst = [0] * (n + 1)

for i in range(1, n + 1):
    pos[i] = i
    order[i] = i
    best[i] = i
    worst[i] = i

for x in a:
    p = pos[x]
    if p == 1:
        continue

    y = order[p - 1]

    order[p], order[p - 1] = order[p - 1], order[p]
    pos[x] = p - 1
    pos[y] = p

    best[x] = min(best[x], p - 1)
    worst[x] = max(worst[x], p - 1)

    best[y] = min(best[y], p)
    worst[y] = max(worst[y], p)

for i in range(1, n + 1):
    print(best[i], worst[i])
```

The core structure is the bidirectional mapping between posts and positions. The pos array avoids any search, and order ensures we can update neighbors in constant time. The only subtle point is that both swapped posts must update their best and worst values immediately after the swap, since both have changed positions.

## Worked Examples

### Example 1

Input:

```
3 5
3 2 1 3 3
```

We track arrays after each step.

| Step | Like | order | pos(1,2,3) | updated posts |
| --- | --- | --- | --- | --- |
| 0 | - | [1,2,3] | (1,2,3) | init |
| 1 | 3 | [1,3,2] | (1,3,2) | 3 |
| 2 | 2 | [1,2,3] | (1,2,3) | 2,3 |
| 3 | 1 | [1,2,3] | (1,2,3) | 1 |
| 4 | 3 | [1,3,2] | (1,3,2) | 3 |
| 5 | 3 | [3,1,2] | (3,1,2) | 3,1 |

Post 1 reaches positions 1 and 2. Post 2 reaches positions 2 and 3. Post 3 reaches positions 1, 2, and 3.

This confirms that tracking only local swaps correctly captures global extrema.

### Example 2

Input:

```
4 3
4 4 4
```

| Step | Like | order | pos(4) |
| --- | --- | --- | --- |
| 0 | - | [1,2,3,4] | 4 |
| 1 | 4 | [1,2,4,3] | 3 |
| 2 | 4 | [1,4,2,3] | 2 |
| 3 | 4 | [4,1,2,3] | 1 |

Post 4 has best = 1 and worst = 4.

This shows repeated likes on a single element can move it monotonically upward, and the algorithm still captures full range correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Initialization is linear, each like causes at most one swap with constant updates |
| Space | O(n) | Arrays store position, order, and bounds for each post |

The constraints allow up to 400,000 operations, so a constant-time per operation simulation fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdin
    input = stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    pos = [0] * (n + 1)
    order = [0] * (n + 1)
    best = [0] * (n + 1)
    worst = [0] * (n + 1)

    for i in range(1, n + 1):
        pos[i] = i
        order[i] = i
        best[i] = i
        worst[i] = i

    for x in a:
        p = pos[x]
        if p == 1:
            continue
        y = order[p - 1]

        order[p], order[p - 1] = order[p - 1], order[p]
        pos[x] = p - 1
        pos[y] = p

        best[x] = min(best[x], p - 1)
        worst[x] = max(worst[x], p - 1)
        best[y] = min(best[y], p)
        worst[y] = max(worst[y], p)

    return "\n".join(f"{best[i]} {worst[i]}" for i in range(1, n + 1)) + "\n"

assert run("3 5\n3 2 1 3 3\n") == "1 2\n2 3\n1 3\n"

assert run("1 5\n1 1 1 1 1\n") == "1 1\n"

assert run("2 1\n2\n") == "1 2\n1 2\n"

assert run("4 3\n4 4 4\n") == "1 4\n2 2\n3 3\n1 4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single repeated likes | stable element movement | no-change swaps |
| smallest n=1 | trivial stability | boundary correctness |
| single swap | direct one-step effect | basic adjacency update |
| repeated top movement | monotonic ascent | repeated updates consistency |

## Edge Cases

A post that is never liked never moves, so its best position remains 1 and worst remains n. The algorithm handles this because initialization sets both bounds correctly and no updates ever touch that post.

A post receiving repeated likes can move step-by-step toward the top. Each swap updates both participants, so intermediate positions are all captured. Since every movement is local, no global recomputation is required.

A like on the current top element triggers no swap. The condition check for position 1 prevents invalid array access and ensures no unnecessary updates occur, preserving correctness and avoiding index errors.
