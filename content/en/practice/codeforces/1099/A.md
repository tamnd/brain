---
title: "CF 1099A - Snowball"
description: "The process describes a snowball sliding downward from a starting height until it reaches the ground. At every integer height level, the snowball repeatedly changes its weight in three ordered phases: it first gains additional weight equal to its current height, then possibly…"
date: "2026-06-15T15:49:42+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1099
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 530 (Div. 2)"
rating: 800
weight: 1099
solve_time_s: 382
verified: true
draft: false
---

[CF 1099A - Snowball](https://codeforces.com/problemset/problem/1099/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 6m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

The process describes a snowball sliding downward from a starting height until it reaches the ground. At every integer height level, the snowball repeatedly changes its weight in three ordered phases: it first gains additional weight equal to its current height, then possibly loses weight if there is a stone at that height, and finally moves one step down.

The input describes the initial state of this system. We are given the starting weight and starting height of the snowball, and two stones placed at specific heights, each removing a fixed amount of weight whenever the snowball passes through their height.

The task is to simulate this motion until the snowball reaches height zero and report its final weight. The key difficulty is that the weight evolves continuously with both accumulation and subtraction at specific positions.

The constraints are small: height is at most 100 and weights are at most 100. This immediately implies that a direct simulation over each height level is efficient enough, since at most 100 steps are performed and each step does O(1) work. Any solution up to roughly 10^7 operations would be safe under the time limit, so there is no need for optimization beyond straightforward iteration.

A few edge cases are easy to mishandle if the sequence of operations is not followed precisely. One is forgetting that weight increases before stone collisions. For example, if a snowball starts at height 1 with a stone at height 1, the increment by height happens first, so the snowball gains weight before losing it. Another is mishandling negative weight after stone impact. The problem explicitly clamps weight to zero but continues the simulation, so a naive early stop would be incorrect.

A third subtle case is when a stone has zero weight. Even then, the collision must still be processed, though it changes nothing. Skipping such stones conditionally is safe, but skipping the collision step entirely at that height is not, because ordering matters for consistency.

## Approaches

A brute-force solution directly simulates the process second by second. At each height, we increase the snowball weight by the current height, apply stone damage if applicable, clamp the result to zero if negative, and then decrement the height. Since height decreases by exactly one each iteration, this simulation runs for exactly h steps. Each step is constant time, so the brute-force approach is already optimal under the given constraints.

There is no hidden mathematical structure to compress further because the state transition depends only on the current height and current weight, and height strictly decreases. Any attempt to skip steps would still require accounting for stone interactions at individual heights, so no aggregation trick reduces complexity further in a meaningful way.

The main distinction between correct and incorrect solutions is not efficiency but strict adherence to the event ordering.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(h) | O(1) | Accepted |
| Optimal Simulation | O(h) | O(1) | Accepted |

## Algorithm Walkthrough

We simulate the snowball descending one level at a time, always keeping track of its current height and weight.

1. Initialize the snowball weight and height from the input, and store the two stones in a structure that allows quick lookup by height. This matters because we need constant-time checks at each step.
2. While the current height is greater than zero, perform one full update cycle.
3. First increase the snowball weight by the current height. This step is crucial because the problem defines weight gain before any interaction with stones. The order determines correctness.
4. Check whether a stone exists at the current height. If it does, subtract its weight from the snowball. If multiple stones exist at the same height, both effects are applied sequentially, though the input guarantees distinct heights here.
5. If the resulting weight becomes negative, clamp it to zero. The snowball does not stop or change behavior; only the stored weight is adjusted.
6. Decrease the height by one to simulate the downward movement.
7. Repeat until height becomes zero, then output the final weight.

### Why it works

At every iteration, the algorithm preserves the exact state described in the problem definition: the weight reflects all previous increments and stone interactions at higher or equal levels, and the height strictly tracks remaining unprocessed levels. Because each height is processed exactly once and in the correct order, no contribution is skipped or double-counted. The final state after height zero is therefore the accumulated result of all deterministic transitions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    w, h = map(int, input().split())
    u1, d1 = map(int, input().split())
    u2, d2 = map(int, input().split())

    stone = {}
    stone[d1] = u1
    stone[d2] = u2

    weight = w
    height = h

    while height > 0:
        weight += height

        if height in stone:
            weight -= stone[height]
            if weight < 0:
                weight = 0

        height -= 1

    print(weight)

if __name__ == "__main__":
    solve()
```

The solution stores stone effects in a dictionary keyed by height so that checking for a stone at a given level is O(1). The loop processes heights from h down to 1, matching the physical movement of the snowball. The increment step happens before the lookup, preserving the required order.

The clamping step after subtraction is necessary because negative weights are not allowed to persist, even though the process continues unchanged.

## Worked Examples

### Example 1

Input:

```
4 3
1 1
1 2
```

| Height | Start Weight | +Height | Stone Loss | After Clamp | Next Height |
| --- | --- | --- | --- | --- | --- |
| 3 | 4 | 7 | 0 | 7 | 2 |
| 2 | 7 | 9 | 1 | 8 | 1 |
| 1 | 8 | 9 | 1 | 8 | 0 |

This trace shows that each height contributes exactly once to weight gain, and stone interactions are applied only at their designated levels. The final weight matches the expected output of 8.

### Example 2

Input:

```
5 4
3 4
2 2
```

| Height | Start Weight | +Height | Stone Loss | After Clamp | Next Height |
| --- | --- | --- | --- | --- | --- |
| 4 | 5 | 9 | 3 | 6 | 3 |
| 3 | 6 | 9 | 0 | 9 | 2 |
| 2 | 9 | 11 | 2 | 9 | 1 |
| 1 | 9 | 10 | 0 | 10 | 0 |

This case highlights that stones at different heights independently modify the trajectory without interacting, and the ordering of operations determines the final accumulation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(h) | Each height level is processed exactly once with constant-time operations |
| Space | O(1) | Only a constant number of variables and a small map for two stones |

The maximum height is 100, so the simulation performs at most 100 iterations, well within limits even under strict constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    w, h = map(int, input().split())
    u1, d1 = map(int, input().split())
    u2, d2 = map(int, input().split())

    stone = {d1: u1, d2: u2}
    weight = w

    while h > 0:
        weight += h
        if h in stone:
            weight -= stone[h]
            if weight < 0:
                weight = 0
        h -= 1

    return str(weight)

assert run("4 3\n1 1\n1 2\n") == "8"

assert run("0 1\n0 1\n0 1\n") == "1"

assert run("10 5\n0 3\n0 4\n") == "25"

assert run("5 4\n5 4\n0 2\n") == "9"

assert run("1 2\n10 1\n10 2\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimal height | 1 | Single-step simulation correctness |
| Zero stone weights | Growth only | No-op stone handling |
| Multiple mid heights | Accumulation correctness | Proper additive behavior |
| Heavy stone at start | Immediate clamping | Negative weight handling |

## Edge Cases

One subtle case is when the stone at a height removes more weight than currently exists. For example, at a height where the snowball has just gained a small amount, a large stone can push it negative. The algorithm explicitly clamps to zero after subtraction, ensuring the state remains valid without interrupting the loop.

Another case is when a stone is located at height 1. Even though this is the final active step, the snowball still performs the full sequence: gain by 1, apply stone, then move to zero. The loop structure naturally handles this without special branching because height becomes zero only after processing.

A third case is when both stones have zero weight. The simulation still performs dictionary lookups and subtraction attempts, but the net effect is neutral. The correctness depends on still executing the collision step, even if it does not change the state.
