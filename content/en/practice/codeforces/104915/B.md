---
title: "CF 104915B - \u0410\u0431\u0441\u043e\u043b\u044e\u0442\u043d\u043e \u043e\u0442\u043d\u043e\u0441\u0438\u0442\u0435\u043b\u044c\u043d\u043e"
description: "We are given a route written in absolute compass directions, where each step is one of four values: North, East, South, or West. The platform executing the route starts with a fixed orientation, initially facing North."
date: "2026-06-28T18:05:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104915
codeforces_index: "B"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u0421\u0430\u043c\u0430\u0440\u0435 2023-2024 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104915
solve_time_s: 46
verified: true
draft: false
---

[CF 104915B - \u0410\u0431\u0441\u043e\u043b\u044e\u0442\u043d\u043e \u043e\u0442\u043d\u043e\u0441\u0438\u0442\u0435\u043b\u044c\u043d\u043e](https://codeforces.com/problemset/problem/104915/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a route written in absolute compass directions, where each step is one of four values: North, East, South, or West. The platform executing the route starts with a fixed orientation, initially facing North. As the route is executed, each new command is given in the global coordinate system, but what we want is to rewrite the same movement as a sequence of relative commands from the perspective of the moving platform.

The key transformation is that at every step, instead of interpreting a direction as an absolute vector, we interpret it relative to the current orientation of the platform. After each move, the platform’s orientation is updated to match the direction it just moved in, and the next command must be expressed relative to this updated orientation.

The output is therefore a sequence of the same length, but instead of absolute directions, it encodes whether the platform continues forward, turns right, turns around, or turns left relative to its current heading.

The constraints are small enough that a single linear scan over the string is sufficient. Any solution that attempts to recompute relative orientations from scratch for each position would still be linear, but anything involving pairwise recomputation or precomputing all transitions is unnecessary overhead. The natural target complexity is O(n).

A subtle edge case comes from handling wraparound in directional arithmetic. Since directions form a cycle of size four, naive subtraction can produce negative values. For example, moving from North to West gives a raw difference of -1, which must be normalized into the valid range [0, 3]. Any implementation that forgets modular normalization will silently produce incorrect relative commands in those wraparound transitions.

Another common pitfall is misunderstanding that the platform orientation changes after each step. For instance, if we incorrectly assume a fixed reference orientation (always North), we would compute relative directions consistently wrong after the first move.

## Approaches

A brute-force interpretation would simulate the platform step by step, and at each step recompute the relative direction by comparing the absolute direction of the current command with the current orientation. This is already close to optimal, but a careless implementation might recompute differences by scanning or mapping through pairs repeatedly, leading to redundant work.

The clean observation is that both absolute directions and relative transitions live in the same cyclic group of size four. If we encode directions as integers, North, East, South, West mapped to 0, 1, 2, 3, then the relative command is simply the modular difference between the target direction and the current orientation. After executing a step, we update the current orientation to that same target direction.

This reduces the problem to maintaining a single integer state and performing constant-time arithmetic per character. The brute-force idea works because it already follows the simulation structure, but it becomes unnecessarily complicated if we think in geometric vectors or string-based transformations. Once we recognize the cyclic structure, everything collapses into simple modular arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation with recomputation | O(n) | O(1) | Accepted but verbose |
| Optimal modular encoding | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Convert each direction character into an integer in a cycle: North becomes 0, East 1, South 2, West 3. This allows arithmetic operations to represent rotations.
2. Initialize the current orientation as 0, since the platform starts facing North.
3. For each command in the input sequence, compute the difference between the command direction and the current orientation using subtraction.
4. Normalize this difference using modulo 4. If the result is negative, add 4 implicitly through modulo arithmetic. This ensures we always stay within valid directional states.
5. Convert the resulting value back into a relative command: 0 means continue forward, 1 means turn right, 2 means turn around, 3 means turn left.
6. Update the current orientation to the absolute direction just executed, since the platform rotates to face its movement direction.
7. Append the relative command to the output sequence and proceed to the next input character.

The core idea is that at each step we are expressing the absolute direction as a rotation relative to the current heading, then updating the heading to that direction. The state evolution is fully captured by a single integer.

### Why it works

The algorithm maintains the invariant that the stored orientation always equals the last executed absolute direction. Because every relative command is computed as the difference between the next absolute direction and this stored orientation in a modulo-4 cycle, it exactly encodes the rotation required to transform one heading into another. Since rotations in four directions form a closed cyclic group under addition modulo 4, each transformation is uniquely represented and no ambiguity or drift accumulates across steps.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    mp = {
        'N': 0,
        'E': 1,
        'S': 2,
        'W': 3
    }

    rmp = {
        0: 'N',
        1: 'E',
        2: 'S',
        3: 'W'
    }

    cur = 0
    out = []

    for ch in s:
        nxt = mp[ch]
        diff = (nxt - cur) % 4
        out.append(rmp[diff])
        cur = nxt

    sys.stdout.write(''.join(out))

if __name__ == "__main__":
    solve()
```

The solution relies on maintaining a single variable `cur`, which represents the current absolute orientation of the platform. For each character, we convert it into its numeric encoding and compute the modular difference. The modulo operation handles both forward wraparound and negative subtraction cases uniformly, so no additional conditional logic is needed.

The update `cur = nxt` is essential because it reflects the physical rotation of the platform after executing each move. Without this update, all subsequent relative computations would incorrectly assume a fixed orientation.

## Worked Examples

### Example 1

Input:

```
NWES
```

We track the current orientation and computed relative moves.

| Step | Input | Current | Next | Difference | Output | New Current |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | N | 0 | 0 | 0 | N | 0 |
| 2 | W | 0 | 3 | 3 | W | 3 |
| 3 | E | 3 | 1 | 2 | S | 1 |
| 4 | S | 1 | 2 | 1 | E | 2 |

Output:

```
NWSE
```

This trace shows how the orientation continuously shifts, causing identical absolute moves to map to different relative commands depending on state.

### Example 2

Input:

```
NESW
```

| Step | Input | Current | Next | Difference | Output | New Current |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | N | 0 | 0 | 0 | N | 0 |
| 2 | E | 0 | 1 | 1 | E | 1 |
| 3 | S | 1 | 2 | 1 | E | 2 |
| 4 | W | 2 | 3 | 1 | E | 3 |

Output:

```
NEEE
```

This example highlights how repeated forward-relative motion can still correspond to changing absolute directions due to the rotating frame.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once with O(1) arithmetic operations |
| Space | O(1) | Only a constant-size mapping and output buffer are used |

The algorithm directly matches the input size, so even the largest possible input is handled comfortably within time limits. No recursion, no nested loops, and no auxiliary data structures that scale with input size are required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# simple cases
assert run("N") == "N"
assert run("NE") == "NE"

# sample-like case
assert run("NWES") == "NWSE"

# alternating turns
assert run("NESW") == "NEEE"

# all same direction
assert run("NNNN") == "NNNN"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| N | N | single-step identity case |
| NWES | NWSE | mixed rotations and state updates |
| NNNN | NNNN | no rotation accumulation |
| NESW | NEEE | consistent frame rotation |

## Edge Cases

One edge case is when the direction jumps backward in the cycle, such as transitioning from North to West. For input `NW`, the computation goes from cur = 0 to nxt = 3, producing (3 - 0) % 4 = 3, which correctly maps to a left turn. A naive subtraction without modulo handling would yield -1 and fail to map to a valid command.

Another case is repeated rotations that accumulate orientation changes. For input `NESW`, the current orientation evolves through all four states. The algorithm correctly updates `cur` at each step, so each difference is computed relative to the correct frame, preventing drift.

A final subtle case is long uniform sequences like `SSSSSS`. Since each step updates orientation to South repeatedly, every difference is zero after the first move, producing consistent forward commands. This confirms that the state update is idempotent when directions repeat.
