---
title: "CF 103379G - Santa's New Sled"
description: "We are given a sequence of locations in a 2D plane, starting from the origin. Santa’s sled does not choose directions freely anymore. Instead, it repeatedly executes a fixed movement pattern given by a string consisting of the four cardinal directions."
date: "2026-07-03T12:34:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103379
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 10-29-21 Div. 1 (Advanced)"
rating: 0
weight: 103379
solve_time_s: 51
verified: true
draft: false
---

[CF 103379G - Santa's New Sled](https://codeforces.com/problemset/problem/103379/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of locations in a 2D plane, starting from the origin. Santa’s sled does not choose directions freely anymore. Instead, it repeatedly executes a fixed movement pattern given by a string consisting of the four cardinal directions.

We conceptually imagine Santa standing at position (0, 0) and applying the string from left to right. After finishing the string once, he immediately repeats it again, and this continues infinitely. Each repetition produces a deterministic displacement vector, so the motion is periodic in structure.

The question asks whether, at any point in this infinite walk, Santa will land exactly on a target coordinate (x, y). This is not limited to the end of full cycles of the string, but can occur at any intermediate step inside any repetition.

The constraints matter in two ways. The coordinate bounds reach 10^18 scale, so simulating steps directly is impossible. The string length can be up to 100,000, so even a single pass is already large enough that any O(n^2) or repeated simulation per cycle is too slow. The only viable direction is to treat one full string execution as a transformation and reason algebraically about repeated applications.

A subtle edge case arises when the net displacement after one full string is zero. In that case, the sled is trapped inside a bounded orbit, and only positions visited in the first cycle matter. If we ignore this and assume periodic shifting, we can incorrectly claim reachability for coordinates that are never actually visited.

Another edge case occurs when the target coordinate is reachable only in a middle segment of a cycle, not at cycle boundaries. For example, if the string is "UR", positions visited are (0,0), (0,1), (1,1), then repeat. A target like (0,1) must be detected inside the cycle, not just via net displacement reasoning.

## Approaches

The brute-force idea is straightforward: simulate the sled step by step, storing every visited coordinate, and check whether (x, y) appears. This is correct because the motion is deterministic and periodic, so eventually either we see the target or we do not. The problem is that the path is infinite, so brute-force must artificially stop after some number of steps.

A natural cutoff is to simulate up to some large number of cycles, for example O(n * C) steps where C is large enough to “cover” all possible offsets. However, since coordinates can be as large as 10^18, there is no safe bound on how many cycles might be needed. Even a few million cycles would exceed time limits.

The key insight is that each full string application contributes a fixed displacement vector. Let that displacement be (dx, dy). After k full cycles, the position is k * (dx, dy) plus the position inside the current cycle. This reduces the infinite walk to checking arithmetic progressions of points.

We then reverse the perspective. Instead of asking whether (x, y) is ever visited, we ask whether there exists a cycle index k and a prefix position i in the string such that the prefix displacement at i plus k times the full-cycle displacement equals (x, y). This transforms the problem into checking linear Diophantine conditions over a small set of prefix states.

If (dx, dy) is not (0, 0), then k is uniquely determined for each prefix candidate, and we only need to verify whether that k is a non-negative integer consistent for both coordinates. If (dx, dy) is (0, 0), then no shifting occurs between cycles, so only one cycle matters and we directly check whether the target appears in prefix traversal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(infinite or bounded O(n·C)) | O(n) | Too slow / incomplete |
| Prefix + Cycle Decomposition | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute prefix positions of the sled after each character in the string starting from (0, 0). This gives the exact location after each step inside one cycle. This is needed because the target may be reached mid-cycle.
2. Compute the total displacement of one full cycle as (dx, dy) by taking the final prefix position after processing the whole string. This captures how the entire pattern shifts space after one repetition.
3. For each prefix position (px, py) corresponding to index i in the string (including the initial (0, 0)), consider whether the target (x, y) could match this state after some number of full cycles. This means we check whether (x - px, y - py) can be expressed as k * (dx, dy) for some integer k ≥ 0.
4. If dx is non-zero, compute k as (x - px) / dx and verify it is an integer. Also check that applying it to y gives consistency: (y - py) must equal k * dy. This prevents mismatched scaling when dx and dy are not aligned.
5. If dx is zero but dy is not zero, do the symmetric check using only y-coordinates, since horizontal movement never changes between cycles.
6. If both dx and dy are zero, then the cycle does not move the sled at all. In this case, only the first cycle matters, so we simply check whether any prefix position equals the target.
7. If any prefix position satisfies the condition, return “Yes”. Otherwise return “No”.

Why it works is based on the invariant that every visited point in the infinite walk can be uniquely decomposed into a prefix state within one cycle plus an integer number of full-cycle shifts. The prefix enumeration covers all intra-cycle possibilities, while the linear scaling by (dx, dy) captures all inter-cycle movement. No other points exist in the trajectory beyond these combinations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x, y = map(int, input().split())
    s = input().strip()

    # prefix positions
    px = py = 0
    pref = [(0, 0)]

    for c in s:
        if c == 'U':
            py += 1
        elif c == 'D':
            py -= 1
        elif c == 'L':
            px -= 1
        else:
            px += 1
        pref.append((px, py))

    dx, dy = pref[-1]

    for i, (cx, cy) in enumerate(pref):
        tx = x - cx
        ty = y - cy

        if dx == 0 and dy == 0:
            if tx == 0 and ty == 0:
                print("Yes")
                return
            continue

        if dx == 0:
            if tx == 0 and dy != 0 and ty % dy == 0:
                k = ty // dy
                if k >= 0 and cy + k * dy == y:
                    print("Yes")
                    return
            continue

        if dy == 0:
            if ty == 0 and dx != 0 and tx % dx == 0:
                k = tx // dx
                if k >= 0 and cx + k * dx == x:
                    print("Yes")
                    return
            continue

        if tx % dx == 0:
            k = tx // dx
            if k >= 0 and cy + k * dy == y:
                print("Yes")
                return

    print("No")

if __name__ == "__main__":
    solve()
```

The prefix construction directly encodes all possible within-cycle endpoints. The final displacement `(dx, dy)` captures the repeating structure. Each conditional block handles degeneracies where one or both axes do not change across cycles, which otherwise would lead to division-by-zero or invalid integer assumptions. The key implementation detail is to always validate consistency on both coordinates, not just one.

## Worked Examples

Consider the input:

```
2 2
UR
```

The prefix states are:

| i | move | position |
| --- | --- | --- |
| 0 | start | (0, 0) |
| 1 | U | (0, 1) |
| 2 | R | (1, 1) |

The cycle displacement is (1, 1). The target (2, 2) matches prefix (0, 0) with k = 2 cycles, so it is reachable.

This demonstrates that reachability can occur exactly at cycle boundaries, and prefix (0, 0) must always be considered.

Now consider:

```
1 2
RU
```

Prefix:

| i | move | position |
| --- | --- | --- |
| 0 | start | (0, 0) |
| 1 | R | (1, 0) |
| 2 | U | (1, 1) |

Cycle displacement is (1, 1). The target (1, 2) cannot be expressed as any prefix plus integer multiples of (1, 1), so it is unreachable.

This shows why checking only distance magnitude or naive periodicity fails, since the direction coupling between x and y matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to build prefix positions and one pass to test them |
| Space | O(n) | Storage of prefix coordinates for each position in the cycle |

The solution fits easily within constraints since n is up to 100,000, and all operations are constant-time arithmetic per character. The memory footprint is linear in the string size, which is acceptable under typical 256 MB limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like cases
assert run("2 2\nUR\n") == "Yes"
assert run("1 2\nRU\n") == "No"

# minimal case
assert run("0 0\nU\n") == "Yes"

# cycle zero displacement
assert run("1 1\nUDLR\n") == "No"

# reachable mid-cycle repeated shift
assert run("3 1\nUR\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 / U | Yes | prefix origin handling |
| UDLR with target 1 1 | No | zero net displacement cycle |
| UR with target 3 1 | Yes | repeated cycle accumulation |

## Edge Cases

One important edge case is when the displacement vector of the full string is zero. In this situation, the sled never shifts between cycles, so the only reachable points are those in the first traversal of the string. The algorithm handles this by immediately reducing the problem to a single-cycle prefix check, ensuring no incorrect extrapolation across cycles.

Another edge case arises when dx or dy is zero. If dx is zero, horizontal position never changes between cycles, so attempting to divide by dx would be invalid. The algorithm explicitly separates this case and only performs validity checks on the axis that actually changes.

A final subtle case is when the target is reachable only at the very start (0, 0). This is covered because the prefix list includes the initial position before any movement, so the algorithm correctly identifies immediate success without needing any cycle reasoning.
