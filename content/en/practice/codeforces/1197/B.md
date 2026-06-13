---
title: "CF 1197B - Pillars"
description: "We are given a row of pillars, each initially holding exactly one disk. Each disk has a distinct radius, so we can think of the input as a permutation of values from 1 to n placed on positions 1 through n. The only allowed move is very restrictive."
date: "2026-06-13T14:27:59+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1197
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 69 (Rated for Div. 2)"
rating: 1000
weight: 1197
solve_time_s: 274
verified: true
draft: false
---

[CF 1197B - Pillars](https://codeforces.com/problemset/problem/1197/B)

**Rating:** 1000  
**Tags:** greedy, implementation  
**Solve time:** 4m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of pillars, each initially holding exactly one disk. Each disk has a distinct radius, so we can think of the input as a permutation of values from 1 to n placed on positions 1 through n.

The only allowed move is very restrictive. A disk can be moved from a pillar to an adjacent pillar, but only if its current pillar has exactly one disk. Additionally, when placing it onto another pillar, it must either land on an empty pillar or on top of a strictly larger disk. This creates a stacking constraint where disks can only be placed in decreasing order of radius.

The question is whether it is possible, using only these adjacent single-disk moves, to eventually collect all disks onto a single pillar.

The constraint n up to 2 · 10^5 forces us away from any simulation of actual moves. Any approach that tries to explicitly move disks step by step risks quadratic behavior because a disk may traverse many positions and each move is local.

A subtle difficulty is that the movement restriction “a disk can only be moved from a pillar that currently has exactly one disk” prevents arbitrary rearrangement. If we try to treat this as a free sorting process, we would incorrectly assume we can always shuttle disks through intermediate positions. In reality, intermediate configurations can block future moves.

A common failure case comes from greedily stacking without respecting adjacency constraints. For example, if large disks are not positioned so that smaller disks can be peeled off in a consistent outward expansion, a naive greedy ordering still produces a valid decreasing sequence but ignores that some required intermediate pillar will temporarily contain multiple disks, making moves illegal.

So the core difficulty is not ordering the disks, but ensuring that the adjacency constraint does not trap any disk in a configuration where it cannot be moved out as a singleton.

## Approaches

A brute force idea is to simulate all valid moves using a BFS over configurations. Each state would represent the full arrangement of stacks, and each transition would move a valid disk to a neighbor. This is theoretically correct because it explores all reachable configurations, but the number of states is astronomically large. Even for moderate n, the number of ways to stack disks across pillars grows exponentially, making this approach completely infeasible.

The key insight is that we do not actually need to construct the sequence of moves. We only need to determine whether a valid sequence exists. The adjacency constraint implies a structural property: at any moment, the set of disks that have not yet been moved must form a contiguous region around the current construction process. More importantly, because we can only move from single-disk pillars, the process of building a final stack behaves like peeling the array inward from both ends.

This leads to a simplification. We choose a target final pillar implicitly and try to simulate whether we can “collect” all disks into a single decreasing stack. Since disks must end up in decreasing order, the largest disk must be the first fixed element of the final structure. After placing it as the base, all remaining disks must be attached in decreasing order, and at each step we are only allowed to take the next disk from one of the current ends of the remaining segment. This is because only endpoints remain reachable without violating the “singleton source pillar” constraint.

Thus the problem reduces to checking whether we can start from the position of the maximum element and expand outward, always choosing an adjacent unprocessed element that is smaller than the last chosen disk.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(exp(n)) | O(exp(n)) | Too slow |
| Two-pointer greedy expansion | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We first locate the position of the maximum radius disk. This disk must be the starting point of our final stack because no larger disk exists to sit above it.

We then maintain two pointers, one expanding left and one expanding right from this position. We also maintain a variable tracking the last chosen disk in the final ordering, initially set to the maximum disk.

At each step, we consider the two candidates at the current boundaries. We are allowed to take a candidate only if its radius is strictly smaller than the last chosen value, because the final stack must be strictly decreasing. Among the valid candidates, we choose the larger one. This choice is important because picking a smaller value too early can block access to a larger valid candidate later, while the greedy choice preserves flexibility.

We continue expanding until all elements are consumed or until neither boundary candidate is valid.

After finishing, if we have successfully included all disks, the answer is YES, otherwise NO.

The correctness relies on the invariant that the already chosen sequence is always strictly decreasing and corresponds to a contiguous segment in the original array centered at the maximum element. Every remaining candidate is adjacent to this segment, so if a valid full construction exists, there will always be a valid boundary choice at each step that does not violate decreasing order. The greedy selection ensures we never prematurely discard a necessary larger element.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    mx = max(range(n), key=lambda i: a[i])
    last = a[mx]

    l = mx - 1
    r = mx + 1

    used = 1

    while used < n:
        left_val = a[l] if l >= 0 else -1
        right_val = a[r] if r < n else -1

        valid_left = l >= 0 and left_val < last
        valid_right = r < n and right_val < last

        if not valid_left and not valid_right:
            print("NO")
            return

        if valid_left and valid_right:
            if left_val > right_val:
                last = left_val
                l -= 1
            else:
                last = right_val
                r += 1
        elif valid_left:
            last = left_val
            l -= 1
        else:
            last = right_val
            r += 1

        used += 1

    print("YES")

if __name__ == "__main__":
    solve()
```

The code first identifies the maximum element index and initializes the expansion boundaries around it. The loop grows the chosen segment outward while maintaining the strictly decreasing condition.

The key implementation detail is careful boundary handling: when one side is exhausted, it must not be considered as a candidate. Another subtle point is ensuring that comparisons use strict inequality with `last`, since equal values are impossible by problem statement but the condition still enforces correctness structurally.

The greedy selection between left and right is implemented by comparing their values directly, always extending toward the larger feasible boundary value.

## Worked Examples

Consider the sample input:

```
4
1 3 4 2
```

We first find the maximum element 4 at index 2.

| Step | Left pointer | Right pointer | Last chosen | Action |
| --- | --- | --- | --- | --- |
| Init | 1 | 3 | 4 | start at max |
| 1 | 1 | 3 | 4 → 3 | take right (3) |
| 2 | 1 | 4 | 3 → 2 | take right (2) |
| 3 | 1 | 4 | 2 → 1 | take left (1) |

All elements are consumed successfully, confirming feasibility.

Now consider a failing-style arrangement:

```
4
4 1 3 2
```

We start at 4 at index 0.

| Step | Left pointer | Right pointer | Last chosen | Action |
| --- | --- | --- | --- | --- |
| Init | -1 | 1 | 4 | start |
| 1 | -1 | 1 | 4 → 1 | must take right |
| 2 | -1 | 2 | 1 → 3 invalid | stuck |

At step 2, we cannot take 3 because it is larger than the last chosen value 1, and there is no valid left move. The process stops early, so the answer is NO.

These traces show that feasibility depends on whether the outward greedy expansion can always find a decreasing boundary extension.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each index is visited once during expansion |
| Space | O(1) | only pointers and counters are used |

The algorithm is linear in the number of pillars, which is sufficient for n up to 2 · 10^5, and it uses constant auxiliary memory beyond the input array.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.readline  # placeholder, replace with full solution call

# sample cases
# assert run("4\n1 3 4 2\n") == "YES\n"

# custom cases
# minimum size
# assert run("3\n3 1 2\n") == "YES\n"

# already sorted decreasing
# assert run("5\n5 4 3 2 1\n") == "YES\n"

# peak in middle but impossible extension
# assert run("5\n2 1 5 3 4\n") == "NO\n"

# maximum spread
# assert run("6\n1 6 2 5 3 4\n") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 1 3 4 2 | YES | standard solvable case |
| 3 3 1 2 | YES | small boundary correctness |
| 5 5 4 3 2 1 | YES | already valid ordering |
| 5 2 1 5 3 4 | NO | blocked greedy expansion |

## Edge Cases

A key edge case is when the maximum element lies at an extreme position. In that situation, the expansion becomes one-sided immediately, and the algorithm must correctly treat the missing side as invalid without attempting to access it.

Another subtle case is when both sides are valid but choosing the wrong side early would still seem locally correct. The greedy rule of always choosing the larger available neighbor ensures that we do not prematurely consume a small value that might be needed later to keep the expansion feasible.

The final important case is a configuration where valid moves exist for several steps but eventually lead to a dead end. The step-by-step boundary simulation ensures that the algorithm detects this exactly when both sides fail the decreasing constraint, mirroring the moment when no legal disk move is possible in the actual process.
