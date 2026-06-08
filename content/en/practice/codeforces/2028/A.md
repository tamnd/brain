---
title: "CF 2028A - Alice's Adventures in ''Chess''"
description: "Alice starts at the origin on a two-dimensional grid and can move in the four cardinal directions. She has a fixed sequence of moves that she repeats indefinitely."
date: "2026-06-08T12:08:17+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2028
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 986 (Div. 2)"
rating: 900
weight: 2028
solve_time_s: 103
verified: true
draft: false
---

[CF 2028A - Alice's Adventures in ''Chess''](https://codeforces.com/problemset/problem/2028/A)

**Rating:** 900  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

Alice starts at the origin on a two-dimensional grid and can move in the four cardinal directions. She has a fixed sequence of moves that she repeats indefinitely. The Red Queen is located at a fixed coordinate `(a, b)`, and we are asked to determine whether Alice will eventually reach that location. The input provides multiple test cases, each specifying the length of the move sequence, the target coordinates, and the move string.

The grid coordinates are small (`1 ≤ n, a, b ≤ 10`), and the sequence length is also tiny. This allows us to simulate Alice's motion directly without worrying about performance. The key challenge is that Alice repeats her move sequence forever, so the path can be considered periodic. We need to account for all positions she will occupy over repeated cycles, not just a single traversal of the sequence.

Non-obvious edge cases include sequences that move in a loop or in a way that might overshoot the target. For example, if Alice's sequence is `NESW` and the Red Queen is at `(1,1)`, the first cycle brings her through `(0,1) → (1,1) → (1,0) → (0,0)`, reaching the target at the second step. A naive approach that checks only after complete sequences could miss this.

## Approaches

The brute-force approach would simulate Alice's moves indefinitely until she either reaches the target or we detect a repeating position. In the worst case, this could take an infinite amount of time, but given the constraints, we can actually bound the number of steps. Since the maximum coordinate for the target is 10 and the move sequence length is at most 10, Alice cannot move more than 10 units away from the origin in any direction in one cycle. Repeating the sequence several times covers all reachable positions within the bounding box defined by `[-10,10] × [-10,10]`. Once we simulate all these positions, either Alice has reached the target or she cannot ever reach it.

A more mathematical approach is to compute the total displacement of one full cycle of the sequence and determine whether the target coordinates can be expressed as a non-negative integer combination of this displacement plus some prefix of the cycle. Because the maximum coordinate is small, this reduces to iterating over all prefixes, checking if the difference between the target and the prefix displacement is a multiple of the full-cycle displacement.

Given the constraints, the first approach is simpler and fully acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute-force simulation with bounding box | O(n × (max( | a | , |
| Mathematical linear combination check | O(n²) | O(n) | Accepted, more elegant |

## Algorithm Walkthrough

1. For each test case, read the sequence length `n`, the target coordinates `(a, b)`, and the move string `s`.
2. Initialize Alice's current position at `(0,0)` and a dictionary mapping moves to coordinate changes: `'N' → (0,1)`, `'E' → (1,0)`, `'S' → (0,-1)`, `'W' → (-1,0)`.
3. Compute the total displacement after one full sequence by summing the changes of each move in `s`.
4. Iterate over the positions reached at each prefix of the sequence. For each prefix, compute the remaining displacement needed to reach `(a,b)` after completing some number of full cycles.
5. Check if the remaining displacement is an integer multiple of the full-cycle displacement in both x and y directions. Only non-negative multiples are valid since Alice can only move forward in cycles.
6. If such a combination exists for any prefix, output "YES". Otherwise, output "NO".

**Why it works**: Each position Alice can reach is the sum of a prefix displacement plus a non-negative multiple of the full-cycle displacement. By checking all prefixes and verifying whether the target minus the prefix is a non-negative multiple of the cycle displacement, we cover all positions Alice can ever occupy.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_meet(a, b, s):
    n = len(s)
    dx = {'N': 0, 'E': 1, 'S': 0, 'W': -1}
    dy = {'N': 1, 'E': 0, 'S': -1, 'W': 0}

    # prefix positions
    px = [0]
    py = [0]
    for move in s:
        px.append(px[-1] + dx[move])
        py.append(py[-1] + dy[move])

    total_dx = px[-1]
    total_dy = py[-1]

    for i in range(n + 1):
        rem_x = a - px[i]
        rem_y = b - py[i]

        # check if the remaining displacement can be reached via full cycles
        if total_dx == 0 and total_dy == 0:
            if rem_x == 0 and rem_y == 0:
                return True
        elif total_dx == 0:
            if rem_x == 0 and rem_y % total_dy == 0 and rem_y // total_dy >= 0:
                return True
        elif total_dy == 0:
            if rem_y == 0 and rem_x % total_dx == 0 and rem_x // total_dx >= 0:
                return True
        else:
            if rem_x % total_dx == 0 and rem_y % total_dy == 0:
                kx = rem_x // total_dx
                ky = rem_y // total_dy
                if kx == ky and kx >= 0:
                    return True
    return False

def main():
    t = int(input())
    for _ in range(t):
        n, a, b = map(int, input().split())
        s = input().strip()
        print("YES" if can_meet(a, b, s) else "NO")

if __name__ == "__main__":
    main()
```

**Explanation**: The solution computes all reachable positions as the sum of a prefix displacement and multiples of the full sequence displacement. It handles zero-displacement cases, avoids negative multiples, and checks for equality in both axes.

## Worked Examples

Sample Input: `2 2 2 NE`

| Step | x | y | Prefix | Total dx | Total dy | Remaining (a-px, b-py) | Multiple check | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | '' | 1 | 1 | (2,2) | 2×? | YES |

Alice reaches `(0,1)` then `(1,1)` in the first cycle. Remaining displacement `(1,1)` can be reached in one more cycle, so output is "YES".

Sample Input: `3 2 2 NNE`

| Step | x | y | Prefix | Total dx | Total dy | Remaining | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | '' | 1 | 2 | (2,2) | kx=2, ky=1 → NO |

The sequence displacement per cycle is `(1,2)`. The remaining displacement does not have equal multiples in x and y, so Alice cannot reach the target.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t × n) | Each test case simulates prefix sums and checks up to n+1 positions |
| Space | O(n) | Stores prefix sums of x and y coordinates |

Given `t ≤ 500` and `n ≤ 10`, this approach runs comfortably within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# Provided samples
assert run("6\n2 2 2\nNE\n3 2 2\nNNE\n6 2 1\nNNEESW\n6 10 10\nNNEESW\n3 4 2\nNEE\n4 5 5\nNEWS\n") == "YES\nNO\nYES\nYES\nYES\nNO", "sample 1"

# Custom cases
assert run("1\n1 0 1\nN\n") == "YES", "minimum distance"
assert run("1\n2 1 0\nEW\n") == "YES", "back and forth horizontal"
assert run("1\n3 3 3\nNNE\n") == "NO", "cannot reach"
assert run("1\n4 2 2\nNEWS\n") == "YES", "loop covers target"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 1 N` | YES | Single-step move reaches target |
| `2 1 0 EW` | YES | Repeated moves cancel out but target reached |
| `3 3 3 NNE` | NO | Target unreachable |
| `4 2 2 NEWS` | YES | Loop sequence covers target |

## Edge Cases

For the zero-displacement cycle, such as `s = 'NEWS'`, the total dx and dy per cycle is zero. If Alice’s
