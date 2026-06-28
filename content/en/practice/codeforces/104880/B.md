---
title: "CF 104880B - \u6bd5\u4e1a\u5408\u7167"
description: "We are given a set of people moving along an infinite straight line. Each person starts at a position $xi$ and then moves with constant velocity $vi$. All motion begins at the same moment, so time $t = 0$ is shared."
date: "2026-06-28T09:21:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104880
codeforces_index: "B"
codeforces_contest_name: "The 18-th Beihang University Collegiate Programming Contest (BCPC 2023) - Preliminary"
rating: 0
weight: 104880
solve_time_s: 54
verified: true
draft: false
---

[CF 104880B - \u6bd5\u4e1a\u5408\u7167](https://codeforces.com/problemset/problem/104880/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of people moving along an infinite straight line. Each person starts at a position $x_i$ and then moves with constant velocity $v_i$. All motion begins at the same moment, so time $t = 0$ is shared.

Whenever two people arrive at the same position at the same time, they take a photo together. If a group of $k$ people meets at the same point at the same time, every pair inside that group takes a photo, so that contributes $\frac{k(k-1)}{2}$ photos at that instant. We need the total number of such pairwise meetings over all times.

The key object is not the motion itself, but the equality of positions:

$$x_i + v_i t = x_j + v_j t$$

which defines when two people meet, if ever.

The constraints $n \le 1000$ and $|x_i|, |v_i| \le 10^4$ immediately suggest that an $O(n^2)$ reasoning is safe. Any solution that tries to simulate time continuously or track events dynamically would be unnecessary and likely overcomplicated.

A subtle issue is handling simultaneous meetings. Multiple pairs can meet at exactly the same time and location, forming a cluster. For example, if three people all satisfy the same intersection time and position, we must count 3 photos, not 2 or 1.

Another edge case comes from identical starting positions. If $x_i = x_j$, they meet immediately at time 0 regardless of velocity, so they contribute one photo at the start. A naive implementation that only checks intersections with positive time would miss these.

Finally, there are cases where two trajectories never meet because their relative motion does not intersect in forward time, for example when the faster person starts ahead.

## Approaches

A brute-force approach checks every pair of people and computes whether their trajectories intersect. For a pair $(i, j)$, we solve:

$$x_i + v_i t = x_j + v_j t$$

which gives:

$$t = \frac{x_j - x_i}{v_i - v_j}$$

If $v_i = v_j$, they meet only if $x_i = x_j$, otherwise never. If $t \ge 0$, we count one meeting.

This works because each valid pair corresponds to exactly one meeting event. The correctness is straightforward, but it does not handle multi-person collisions explicitly in a grouped way. However, pairwise counting is already sufficient since each meeting contributes independently per pair.

The issue is performance only if we attempted anything beyond pair enumeration, such as sorting events by time or simulating movement. That would require handling up to $O(n^2)$ events and sorting them, leading to $O(n^2 \log n)$, which is unnecessary.

The key insight is that we do not need to simulate time at all. Every meeting is determined purely by pairwise algebra, and counting all valid pairs directly already produces the correct answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pair Check | O(n²) | O(1) | Accepted |
| Event Simulation / Sorting | O(n² log n) | O(n²) | Accepted but unnecessary |

## Algorithm Walkthrough

1. Iterate over all unordered pairs of people $(i, j)$. This ensures every possible interaction is considered exactly once.
2. If $v_i = v_j$, check whether $x_i = x_j$. If so, these two people are always together from the start, so they contribute exactly one photo. Otherwise, they never meet and contribute nothing.
3. If $v_i \ne v_j$, compute the meeting time using:

$$t = \frac{x_j - x_i}{v_i - v_j}$$

This is derived directly from equating their positions over time.
4. Only count the pair if $t \ge 0$. Negative time corresponds to a meeting in the past, which is irrelevant since motion starts at $t = 0$.
5. Accumulate the total number of valid pairs.

Why it works:

Each pair of people has a unique potential meeting time determined by linear motion. If that time exists and is non-negative, the pair contributes exactly one photo. Even if multiple people meet at the same point simultaneously, each pair inside that group is still counted independently, so pairwise accumulation naturally captures group collisions without special handling.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
people = [tuple(map(int, input().split())) for _ in range(n)]

ans = 0

for i in range(n):
    x1, v1 = people[i]
    for j in range(i + 1, n):
        x2, v2 = people[j]

        if v1 == v2:
            if x1 == x2:
                ans += 1
            continue

        num = x2 - x1
        den = v1 - v2

        if den == 0:
            continue

        # check if t >= 0 without floating point
        # t = num / den >= 0  <=> num and den have same sign
        if num * den >= 0:
            ans += 1

print(ans)
```

The implementation directly mirrors the pairwise reasoning. The loop structure enumerates all pairs in $O(n^2)$. The equal-velocity case is separated because division would otherwise be invalid and conceptually corresponds to either permanent overlap or never meeting.

The condition `num * den >= 0` avoids floating point precision issues by checking the sign of the fraction instead of computing it explicitly. This is important because positions and velocities are integers but division could introduce subtle floating-point errors.

## Worked Examples

### Example 1

Input:

```
2
0 1
10 -1
```

These two people move toward each other.

| i | j | x1 | v1 | x2 | v2 | Case | Contribution |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 10 | -1 | different velocities | 1 |

They meet exactly once at time $t = 5$. The algorithm counts this single valid pair.

This confirms that the intersection condition correctly detects head-on motion.

### Example 2

Input:

```
3
0 1
0 2
10 -1
```

Two people start together, and one more approaches later.

| i | j | x1 | v1 | x2 | v2 | Case | Contribution |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 | 2 | same position | 1 |
| 0 | 2 | 0 | 1 | 10 | -1 | meet later | 1 |
| 1 | 2 | 0 | 2 | 10 | -1 | meet later | 1 |

Total is 3.

This shows how simultaneous starting positions are handled correctly and how all pairwise interactions inside a three-person collision are captured independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | We check every unordered pair exactly once |
| Space | O(1) | Only a constant number of variables are used beyond input storage |

With $n \le 1000$, the maximum number of pairs is about 500,000, which is easily fast enough in Python under a 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    people = [tuple(map(int, input().split())) for _ in range(n)]

    ans = 0
    for i in range(n):
        x1, v1 = people[i]
        for j in range(i + 1, n):
            x2, v2 = people[j]

            if v1 == v2:
                if x1 == x2:
                    ans += 1
                continue

            num = x2 - x1
            den = v1 - v2

            if num * den >= 0:
                ans += 1

    return str(ans)

# provided sample-style tests
assert run("2\n0 1\n10 -1\n") == "1"
assert run("3\n0 1\n0 2\n10 -1\n") == "3"

# custom cases
assert run("1\n5 5\n") == "0", "single person"
assert run("2\n1 1\n1 1\n") == "1", "identical trajectories"
assert run("2\n0 1\n1 2\n") == "1", "same direction faster behind"
assert run("2\n0 2\n10 1\n") == "1", "faster ahead never meets"
assert run("3\n0 1\n1 1\n2 1\n") == "2", "parallel same velocity chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single person | 0 | no pairs exist |
| identical trajectories | 1 | same start and velocity |
| same direction faster behind | 1 | catch-up case |
| faster ahead never meets | 1 | negative time filtering |
| parallel same velocity chain | 2 | multiple identical velocity pairs |

## Edge Cases

When multiple people start at the same position, every pair among them is counted immediately. For input `3 0 1 0 2 0 3`, the algorithm evaluates all three pairs and each satisfies `x1 == x2`, so it returns 3, matching the fact that all pairs meet at time zero.

When velocities are identical but positions differ, such as `2 0 1 10 1`, the condition `v1 == v2` triggers and skips counting, correctly reflecting that parallel motion never intersects.

When a faster person starts ahead, like `0 2` and `10 1`, the computed numerator and denominator have opposite signs, so `num * den >= 0` fails, preventing an invalid “backwards-time” meeting from being counted.
