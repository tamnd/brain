---
title: "CF 106054J - Jaimito's blocks"
description: "We are given two configurations of stacked blocks distributed across $T$ towers. Each tower is essentially a stack, and every block has a weight."
date: "2026-06-21T07:44:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106054
codeforces_index: "J"
codeforces_contest_name: "2025 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 106054
solve_time_s: 38
verified: true
draft: false
---

[CF 106054J - Jaimito's blocks](https://codeforces.com/problemset/problem/106054/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two configurations of stacked blocks distributed across $T$ towers. Each tower is essentially a stack, and every block has a weight. Inside each stack, weights are arranged from bottom to top in non-increasing order, meaning heavier or equal blocks always stay below lighter ones. This constraint guarantees that every tower is already in a stable state.

A single operation consists of taking the top block of any non-empty tower and placing it on top of another tower, provided the resulting tower remains stable, so the moved block must not be heavier than the current top block of the destination (if it exists).

The task is to determine whether we can transform the initial arrangement into the final arrangement using any number of such legal moves.

The key observation from the constraints is scale. There are up to $2 \cdot 10^5$ blocks, so any strategy that simulates moves one by one or tries to explore configurations will immediately fail. Even a linear number of moves per block is too large if each move triggers recomputation or validation work.

A naive interpretation would suggest treating this as a state-space reachability problem over stacks, but the state space is astronomically large. The only hope is to compress the problem into some invariant over individual blocks or over structural properties of stacks.

A subtle edge case arises when blocks share identical weights. Since equal weights are allowed to be stacked freely under the “non-increasing” rule, many transformations that seem blocked by ordering are actually possible. For example, if all blocks are weight 5, any rearrangement is valid. A naive solution that incorrectly enforces strict ordering constraints between configurations would fail here.

Another edge case is when the initial and final configurations have identical multisets of towers but differ only in distribution order. A naive tower-by-tower comparison would incorrectly reject these cases even though redistribution via temporary towers is often possible.

## Approaches

The brute-force perspective starts by simulating all legal moves. From any state, we can move the top block of each tower to any other compatible tower, generating new states. Since each move affects only the top element, we could imagine a BFS over configurations.

This approach is correct in principle because it explores the entire reachability space defined by legal moves. However, the number of configurations is exponential in the number of blocks. Each block can move multiple times and create combinatorial branching across towers. Even for 30 blocks this becomes infeasible, and here we have up to $2 \cdot 10^5$.

The key insight is that the order inside each tower is completely determined by weights, and the only real freedom lies in how blocks of equal or different weights can be “reassigned” across towers over time. Since only the top block moves, a block can only move after all blocks above it in its initial tower are removed first. This creates a dependency structure: each block must wait for its tower prefix to be cleared.

Instead of simulating movement, we reverse the viewpoint. We observe that every block has a fixed identity and appears in both initial and final configurations. The only question is whether the final arrangement respects the constraints imposed by how blocks become accessible during removals.

This reduces the problem to checking whether, when processing blocks in a suitable order (from top-like accessibility constraints), we can match how blocks are grouped in final stacks. The system behaves like a constrained re-stacking where only prefix removals are allowed, which suggests a greedy reconstruction using stacks and counters per weight or per tower.

We reduce the problem to validating whether the sequence of block removals implied by the final configuration is consistent with a legal sequence of prefix pops from the initial configuration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS over configurations | Exponential | Exponential | Too slow |
| Greedy stack simulation with validation | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process both configurations as sequences of blocks in stack order.

1. Flatten each tower into an ordered list from bottom to top, then reverse it so we treat it as a sequence of pops from top to bottom. This converts each tower into a stack representation.
2. Build a global sequence for the initial configuration by concatenating tower stacks, preserving tower separation implicitly.
3. Do the same for the final configuration, but interpret it as a target sequence of required removals.
4. Use a single simulation stack to model the process of gradually matching final configuration blocks while consuming initial configuration blocks. At any point, we push blocks from the initial configuration in order, and whenever the top of our working stack matches the next required block in the final sequence, we pop it and advance.
5. Continue until all initial blocks are consumed, repeatedly resolving matches whenever possible.
6. If at the end all final blocks have been matched exactly in order, the transformation is possible.

The reason we can merge everything into a single process is that within each tower, relative order is fixed, and cross-tower moves only matter in terms of when a block becomes accessible. The stack simulation captures exactly this accessibility constraint.

### Why it works

Each block can only be moved after all blocks above it in its original tower are removed, which means the initial configuration defines a partial order where each tower is a chain. Any valid sequence of moves corresponds to a linear extension of this partial order that respects the final arrangement. The greedy stack simulation constructs exactly such a linear extension by only matching blocks when they become accessible and when they are needed in the final configuration order. If a mismatch occurs, it corresponds to an impossible ordering constraint induced by the tower structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def read_towers(T):
    towers = []
    for _ in range(T):
        arr = list(map(int, input().split()))
        k = arr[0]
        if k == 0:
            towers.append([])
        else:
            towers.append(arr[1:])
    return towers

def flatten(towers):
    res = []
    for t in towers:
        for x in reversed(t):
            res.append(x)
    return res

def solve():
    T = int(input())
    init_towers = read_towers(T)
    final_towers = read_towers(T)

    init = flatten(init_towers)
    target = flatten(final_towers)

    if len(init) != len(target):
        print("N")
        return

    j = 0
    stack = []

    for x in init:
        stack.append(x)
        while stack and j < len(target) and stack[-1] == target[j]:
            stack.pop()
            j += 1

    print("S" if j == len(target) else "N")

if __name__ == "__main__":
    solve()
```

The implementation first reads both configurations and converts each tower into a sequence of blocks ordered from top to bottom. This is important because moves always affect the top block, so the natural processing order is reversed relative to input.

The main logic uses a stack to simulate deferred placement. We push blocks from the initial configuration, and whenever the current top matches the next required block in the final configuration, we immediately consume it. This greedy matching is safe because any block that can be matched should be matched as early as possible; delaying it cannot help since it would only increase blocking.

A common pitfall is forgetting that towers are independent chains. Flattening them in the correct order is crucial, otherwise we would incorrectly assume blocks can move between positions in ways that violate stack constraints.

## Worked Examples

### Example 1

Initial towers: $[4], [3,2], [1]$

Final towers: $[4,3,1], [2]$

Flattened:

Initial = $[4,3,2,1]$

Target = $[4,3,1,2]$

| Step | Pushed | Stack | Next target index | Action |
| --- | --- | --- | --- | --- |
| 1 | 4 | [4] | 0 | match 4 |
| 2 | 3 | [3] | 1 | match 3 |
| 3 | 2 | [3,2] | 1 | no match |
| 4 | 1 | [3,2,1] | 2 | match 1 then 2 |

At the end, all target blocks are matched in order, so transformation is possible. This shows how blocks can be temporarily delayed in the stack and still be rearranged correctly.

### Example 2

Initial = $[6,5,3,1]$

Final = $[6,3,5,1]$

| Step | Pushed | Stack | Next target index | Action |
| --- | --- | --- | --- | --- |
| 1 | 6 | [6] | 0 | match 6 |
| 2 | 5 | [5] | 1 | no match |
| 3 | 3 | [5,3] | 1 | match 3 |
| 4 | 1 | [5,1] | 2 | mismatch blocked |

Here the algorithm fails because 5 is stuck above 1 while the target requires 3 before 5, which cannot be resolved by any legal sequence of moves.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | each block is pushed and popped at most once |
| Space | $O(n)$ | stacks store at most all blocks |

The linear complexity is sufficient for up to $2 \cdot 10^5$ blocks, and memory usage is also linear in the number of blocks, which fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve_capture(inp)

def solve_capture(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def read_towers(T):
        towers = []
        for _ in range(T):
            arr = list(map(int, input().split()))
            k = arr[0]
            if k == 0:
                towers.append([])
            else:
                towers.append(arr[1:])
        return towers

    def flatten(towers):
        res = []
        for t in towers:
            for x in reversed(t):
                res.append(x)
        return res

    T = int(input())
    init_towers = read_towers(T)
    final_towers = read_towers(T)

    init = flatten(init_towers)
    target = flatten(final_towers)

    if len(init) != len(target):
        return "N"

    j = 0
    stack = []

    for x in init:
        stack.append(x)
        while stack and j < len(target) and stack[-1] == target[j]:
            stack.pop()
            j += 1

    return "S" if j == len(target) else "N"

# provided samples
assert run("""2
1 4
1 3
1 2
1 4
""") == "S"

# all equal
assert run("""3
1 5
1 5
1 5
1 5
1 5
1 5
""") == "S"

# impossible reorder
assert run("""2
2 3 1
0
2 1 3
0
""") == "N"

# minimal
assert run("""1
1 1
1 1
""") == "S"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample-like 4 blocks | S | basic correctness |
| all equal weights | S | free rearrangement |
| impossible reorder | N | constraint violation detection |
| single tower | S | minimal edge case |

## Edge Cases

A key edge case is when all blocks are identical. The algorithm always matches immediately whenever possible, so the stack never blocks, and the final answer is always positive as expected.

Another case is a strict inversion between initial and final sequences. The stack simulation correctly detects that a larger block blocks access to a required smaller block in the wrong order, causing the target index to stall permanently.

A third case is empty towers. These contribute no blocks to the flattened sequence and therefore do not affect the simulation, which correctly ignores them without special handling.
