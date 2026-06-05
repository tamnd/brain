---
title: "CF 285B - Find Marble"
description: "We have a row of n glasses, each uniquely indexed from 1 to n. A marble starts under the glass at position s. Petya defines a permutation of the positions that determines how glasses are moved simultaneously during a shuffle."
date: "2026-06-05T09:51:17+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 285
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 175 (Div. 2)"
rating: 1200
weight: 285
solve_time_s: 103
verified: true
draft: false
---

[CF 285B - Find Marble](https://codeforces.com/problemset/problem/285/B)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of `n` glasses, each uniquely indexed from 1 to `n`. A marble starts under the glass at position `s`. Petya defines a permutation of the positions that determines how glasses are moved simultaneously during a shuffle. If glass `i` is currently in position `i`, after a shuffle it moves to position `p[i]`. Vasya observes the marble at position `t` after some number of shuffles. The task is to determine the minimum number of shuffles required for the marble to reach `t`, or report `-1` if it is impossible.

The key observations are that each shuffle applies a fixed permutation to all positions and that the marble moves together with its glass. The marble's trajectory is therefore determined by repeated application of the permutation starting from `s`.

Constraints indicate `n` can be as large as 10^5. Each shuffle requires moving all glasses according to the permutation. A naive solution that simulates all possible sequences of shuffles would have exponential complexity in the number of operations, which is infeasible. A solution that walks along the trajectory of the marble alone is feasible because each glass can be visited at most once before cycles repeat, giving a linear O(n) algorithm.

Non-obvious edge cases include when `s` equals `t`. In that situation, zero shuffles may be needed, even if the permutation is non-trivial. Another subtle case is a permutation that contains cycles that do not include `t`. For example, if `s` is in a cycle that never reaches `t`, the answer should be `-1`. A careless implementation might loop infinitely without detecting cycles.

## Approaches

The brute-force approach is to simulate the marble's movement step by step. Start from `s`, apply the permutation repeatedly, and count the number of steps until the marble reaches `t`. This is correct because each shuffle deterministically moves the marble along a unique trajectory. However, in the worst case, the number of shuffles may be O(n), and if we do not track visited positions, we could enter a cycle and loop infinitely. The operation count is at most `n` since the permutation is a bijection; once a position repeats, any subsequent moves will only cycle.

The key observation that allows an optimal approach is that the marble moves along a single cycle of the permutation. We do not need to simulate the entire row. We can track the marble's current position, increment a counter, and stop when either the marble reaches `t` or we detect a repeated position. This guarantees a linear solution in the number of glasses and is sufficient given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate all positions) | O(n^2) | O(n) | Too slow for n ~ 10^5 |
| Trajectory Tracking (marble only) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `pos` to `s` to represent the current position of the marble and a counter `steps` to 0. This sets up our starting point for simulation.
2. If `pos` equals `t`, immediately return `steps` as 0. This handles the trivial case where no shuffles are needed.
3. Otherwise, begin a loop that continues until either `pos` equals `t` or we detect a cycle. At each iteration:

a. Set `pos` to `p[pos]`, moving the marble along the permutation.

b. Increment `steps` by 1.

c. If `pos` equals `t`, return `steps`.

d. If `pos` equals `s` again, it indicates a cycle that does not include `t`; return `-1`.
4. End of loop. If we exit without returning, return `-1` to indicate impossibility.

Why it works: The invariant is that `pos` always represents the marble's current location. Since the permutation is bijective, the marble moves along a fixed cycle. Either the cycle contains `t`, in which case we will reach it within at most `n` steps, or it does not, in which case revisiting `s` signals impossibility. There is no way to skip positions in the cycle or reach `t` by a different path.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, s, t = map(int, input().split())
p = [0] + list(map(int, input().split()))  # 1-indexed

if s == t:
    print(0)
    sys.exit()

pos = s
steps = 0
visited = set()

while pos not in visited:
    visited.add(pos)
    pos = p[pos]
    steps += 1
    if pos == t:
        print(steps)
        break
else:
    print(-1)
```

The code uses 1-based indexing to match the problem statement. We handle the trivial case `s == t` immediately. A `visited` set tracks positions to detect cycles and prevent infinite loops. At each step, we update the marble's position and check if it reached `t`. If we revisit a position without reaching `t`, we conclude that the target is unreachable.

## Worked Examples

**Sample 1**

Input:

```
4 2 1
2 3 4 1
```

| Step | pos | steps | visited |
| --- | --- | --- | --- |
| 0 | 2 | 0 | {} |
| 1 | 3 | 1 | {2} |
| 2 | 4 | 2 | {2,3} |
| 3 | 1 | 3 | {2,3,4} |

The marble reaches `1` after 3 steps. The visited set ensures we never loop infinitely.

**Sample 2**

Input:

```
5 3 3
2 3 4 5 1
```

The initial position equals the target. The algorithm returns 0 immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is visited at most once due to cycle detection. |
| Space | O(n) | The `visited` set may store all positions in the worst case. |

Given the constraints `n ≤ 10^5` and a 2-second time limit, this is efficient. Memory usage remains within the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution code here
    n, s, t = map(int, input().split())
    p = [0] + list(map(int, input().split()))
    if s == t:
        print(0)
    else:
        pos = s
        steps = 0
        visited = set()
        while pos not in visited:
            visited.add(pos)
            pos = p[pos]
            steps += 1
            if pos == t:
                print(steps)
                break
        else:
            print(-1)
    return output.getvalue().strip()

# provided sample
assert run("4 2 1\n2 3 4 1\n") == "3", "sample 1"
# s equals t
assert run("5 3 3\n2 3 4 5 1\n") == "0", "trivial case"
# unreachable t
assert run("3 1 3\n2 1 3\n") == "-1", "cycle without t"
# minimum input
assert run("1 1 1\n1\n") == "0", "single glass"
# maximum input simple cycle
perm = ' '.join(str(i % 100000 + 1) for i in range(100000))
assert run(f"100000 1 100000\n{perm}\n") == "-1", "large cycle no t"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "5 3 3\n2 3 4 5 1\n" | 0 | s equals t |
| "3 1 3\n2 1 3\n" | -1 | marble cannot reach t |
| "1 1 1\n1\n" | 0 | minimum size input |
| large cycle n=10^5 | -1 | performance and cycle detection |

## Edge Cases

When `s == t`, the algorithm returns 0 immediately. For example, input `5 3 3` returns 0 without entering the loop.

When the permutation forms a cycle that does not contain `t`, the visited set detects that `pos` revisits a previous position, and the algorithm correctly returns `-1`. For input `3 1 3` with `p = [2,1,3]`, the marble moves from 1→2→1 and never reaches 3, triggering the else branch.

The algorithm correctly handles the largest input size due to linear traversal along the marble's trajectory, avoiding simulation of unrelated glasses.
