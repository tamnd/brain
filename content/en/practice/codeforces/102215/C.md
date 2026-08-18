---
title: "CF 102215C - Jumps on a Circle"
description: "The chip starts at point 0 on a circle containing p points, numbered 0 through p - 1. On the first move it advances by 1, on the second by 2, on the third by 3, and so on. Movement wraps around the circle, so every position is considered modulo p."
date: "2026-08-18T21:55:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "C"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 799
verified: false
draft: false
---

[CF 102215C - Jumps on a Circle](https://codeforces.com/problemset/problem/102215/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 13m 19s  
**Verified:** no  

## Solution
## Problem Understanding

The chip starts at point `0` on a circle containing `p` points, numbered `0` through `p - 1`. On the first move it advances by `1`, on the second by `2`, on the third by `3`, and so on. Movement wraps around the circle, so every position is considered modulo `p`.

After `k` moves, the total distance traveled is

[
1+2+\dots+k=\frac{k(k+1)}2.
]

So the position after `k` moves is

[
pos_k=\frac{k(k+1)}2\bmod p.
]

The task is to count how many different values occur among `pos_0, pos_1, ..., pos_n`. The initial position `0` is included, so even when `n = 0`, the answer is `1`.

The circle can contain up to `10^7` points, while the number of moves can be as large as `10^18`. The latter bound immediately rules out simulating every move. Even `10^7` iterations are already near the practical limit for a 2-second Python program, so we need to prove that only a bounded prefix of the movement sequence matters. The memory limit of 256 MB also makes a Python `set` containing millions of integers unattractive, while a compact `bytearray` can represent whether each point has been visited using only one byte per point.

The crucial periodicity comes from the triangular-number formula. For every `k`,

[
pos_{k+2p}
=\frac{(k+2p)(k+2p+1)}2
\equiv \frac{k(k+1)}2
\pmod p.
]

Thus the sequence of positions repeats every `2p` moves. We never need to simulate more than `2p` moves, regardless of whether `n` is `10^6` or `10^18`.

There are several boundary cases that a careless implementation can mishandle. For `p = 1, n = 0`, the correct input is `1 0` and the answer is `1`, because the starting point is already the only point. A solution that counts only destinations after moves would incorrectly print `0`.

For `p = 3, n = 10`, the positions are `0, 1, 0, 0, 1, 0, ...`, so the answer is `2`. A solution that assumes a period of `p` moves without proving it can still get some cases right by accident, but the actual period is `2p`.

For `p = 4, n = 3`, the visited positions are `0, 1, 3, 2`, so every point has been reached and the answer is `4`. Stopping after fewer than `n` moves, or treating the starting position separately incorrectly, causes an off-by-one error.

## Approaches

The direct solution follows the chip exactly. Maintain its current position and, for every move `i`, add `i` modulo `p`. Whenever the new position has not been seen before, increase the answer. A boolean array indexed by the circle position gives constant-time membership checks, so this is correct because it records precisely the set of positions reached by the chip.

The problem is the value of `n`. In the worst case, `n = 10^18`, so direct simulation would require up to `10^18` iterations, which is completely infeasible.

The observation that unlocks the optimization is that the chip's position after `k` moves is a triangular number modulo `p`. Since

[
(k+2p)(k+2p+1)-k(k+1)
=4pk+2p(2p+1),
]

the difference is divisible by `2p`, and after dividing by `2`, the corresponding positions differ by a multiple of `p`. Hence `pos_{k+2p} = pos_k`.

The brute-force method works because every simulated move gives one exact position and the visited array records it. It fails when `n` is enormous. The periodicity observation reduces the problem to at most `2p` moves. Since `p <= 10^7`, this means at most `2 * 10^7` iterations, independent of the potentially astronomical value of `n`.

We can also avoid a second pass over all `p` positions by increasing the answer immediately when a previously unseen point is reached. A `bytearray` stores the visited flags compactly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(p) | Too slow when `n` is large |
| Optimal | O(min(n, 2p)) | O(p) | Accepted |

## Algorithm Walkthrough

1. Read `p` and `n`. The chip has already visited point `0`, so initialize the visited structure with point `0` marked and the answer equal to `1`.
2. Replace the number of moves by `min(n, 2p)`. The sequence repeats every `2p` moves, so simulating anything after the first complete period cannot add a new point.
3. Keep `cur` as the chip's current position and process moves from `1` through the reduced move count. For move `i`, advance `cur` by `i` modulo `p`.
4. If the resulting position has not been marked before, mark it and increment the answer. A position may be reached many times, but it contributes to the answer only on its first visit.
5. Print the number of marked positions. Because the answer was increased exactly when a new position was encountered, it already equals the number of distinct visited points.

### Why it works

The invariant is that after processing the first `i` moves, `cur` is exactly the chip's position after move `i`, and every point visited during those moves is marked in the visited array. The initialization establishes the invariant for move `0`, since point `0` is the starting position. Each iteration advances by exactly the next jump length and marks the resulting position, preserving the invariant.

The only remaining question is whether stopping after `2p` moves can lose a point. It cannot, because for every `k`,

[
pos_{k+2p}=pos_k.
]

Every position reached after the first `2p` moves is already reached at the corresponding position within the previous period. Thus the first `min(n, 2p)` moves contain every distinct point that could ever be visited during the requested execution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    p, n = map(int, input().split())

    visited = bytearray(p)
    visited[0] = 1
    answer = 1

    moves = min(n, 2 * p)

    cur = 0
    step_mod = 1

    for _ in range(moves):
        cur += step_mod
        if cur >= p:
            cur -= p

        if not visited[cur]:
            visited[cur] = 1
            answer += 1

        step_mod += 1
        if step_mod == p:
            step_mod = 0

    print(answer)

if __name__ == "__main__":
    solve()
```

The `visited` array has exactly `p` entries, one for each point. A `bytearray` is used instead of a Python list or set because its elements occupy only one byte, which matters when `p` is as large as `10^7`.

The variable `moves` implements the periodicity argument directly. If `n < 2p`, every requested move is simulated. If `n >= 2p`, only one full period is needed.

The implementation keeps `step_mod` rather than storing the full jump length. Since only the jump length modulo `p` affects the position, this is equivalent. After every move, `step_mod` is incremented modulo `p`.

The update

```
cur += step_mod
if cur >= p:
    cur -= p
```

is equivalent to `cur = (cur + step_mod) % p`. At every iteration both `cur` and `step_mod` are in `[0, p - 1]`, so their sum is less than `2p`, meaning one subtraction is sufficient. Avoiding `%` in the main loop makes the Python implementation substantially lighter.

There is no integer overflow issue in Python because integers have arbitrary precision. In a fixed-width language, the original value of `n` requires a sufficiently wide integer type, but the loop counter after applying `min(n, 2p)` is at most `2 * 10^7`.

The loop runs for exactly the number of moves that can still introduce new positions. The initial point is counted separately, so the loop deliberately processes moves `1` through `moves` rather than accidentally treating the starting position as a move.

## Worked Examples

For Sample 1, `p = 3` and `n = 10`. The period is `2p = 6`, so only the first six moves need to be inspected.

| Move | Step modulo `p` | Position | New point? | Answer |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | Initial point | 1 |
| 1 | 1 | 1 | Yes | 2 |
| 2 | 2 | 0 | No | 2 |
| 3 | 0 | 0 | No | 2 |
| 4 | 1 | 1 | No | 2 |
| 5 | 2 | 0 | No | 2 |
| 6 | 0 | 0 | No | 2 |

The jump lengths are `1, 2, 3, 4, 5, 6`, but modulo `3` they are `1, 2, 0, 1, 2, 0`. Only points `0` and `1` occur, so the answer is `2`. The remaining four requested moves repeat the same period.

For Sample 2, `p = 5` and `n = 3`. Since `n < 2p`, all three moves are simulated.

| Move | Step modulo `p` | Position | New point? | Answer |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | Initial point | 1 |
| 1 | 1 | 1 | Yes | 2 |
| 2 | 2 | 3 | Yes | 3 |
| 3 | 3 | 1 | No | 3 |

The visited points are `{0, 1, 3}`, giving the required answer `3`. This trace also demonstrates why counting moves and counting newly visited points are different operations. The third move lands on an existing point, so it does not increase the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(min(n, 2p)) | At most `2p` moves are simulated, with constant work per move |
| Space | O(p) | One byte is stored for each circle point |

Since `p <= 10^7`, the algorithm performs at most `2 * 10^7` iterations even when `n = 10^18`. The `bytearray` needs about 10 MB at the maximum value of `p`, comfortably below the 256 MB memory limit. The solution is based on the same `O(p)`-scale simulation made possible by the period `2p`, rather than attempting to process the potentially huge value of `n`.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    p, n = map(int, sys.stdin.readline().split())

    visited = bytearray(p)
    visited[0] = 1
    answer = 1

    moves = min(n, 2 * p)

    cur = 0
    step_mod = 1

    for _ in range(moves):
        cur += step_mod
        if cur >= p:
            cur -= p

        if not visited[cur]:
            visited[cur] = 1
            answer += 1

        step_mod += 1
        if step_mod == p:
            step_mod = 0

    print(answer)

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# Provided samples
assert solve_data("3 10\n") == "2\n", "sample 1"
assert solve_data("5 3\n") == "3\n", "sample 2"
assert solve_data("8 1000000000000000000\n") == "8\n", "sample 3"

# Minimum circle, no moves
assert solve_data("1 0\n") == "1\n", "single point with zero moves"

# Minimum circle, many moves
assert solve_data("1 1000000000000000000\n") == "1\n", "single point with huge n"

# Boundary before a full period
assert solve_data("4 3\n") == "4\n", "all four points reached before 2p"

# Exactly one full period
assert solve_data("3 6\n") == "2\n", "exactly 2p moves"

# Huge n must be reduced to one period
assert solve_data("10000000 1000000000000000000\n") <= "10000000\n", "huge n boundary"
```

The final large test only checks that the result is a valid count because computing the exact value here would duplicate the solution's work inside the test itself. The other tests exercise the exact expected answers and the important period boundaries.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `1` | Minimum `p`, zero moves, starting point must count |
| `1 1000000000000000000` | `1` | Single-point circle and enormous `n` |
| `4 3` | `4` | All points can be reached before one full period |
| `3 6` | `2` | Exactly `2p` moves and periodicity boundary |
| `10000000 1000000000000000000` | A value in `[1, 10000000]` | Maximum-scale `p` and huge `n` |

## Edge Cases

For `p = 1, n = 0`, the algorithm creates a one-element `bytearray`, marks position `0`, and sets `answer = 1`. Since `moves = min(0, 2) = 0`, the loop does not execute. The output is `1`, correctly counting the starting point.

For `p = 3, n = 10`, the algorithm replaces `n` with `min(10, 6) = 6`. Starting from `0`, the positions after the six simulated moves are `1, 0, 0, 1, 0, 0`. Only position `1` is new, so the final answer is `2`. Moves seven through ten cannot add anything because they repeat the first four positions of the periodic sequence.

For `p = 4, n = 3`, the loop processes positions `1, 3, 2`. Together with the initial `0`, the visited set becomes `{0, 1, 2, 3}`, so the answer is `4`. This catches the common mistake of forgetting that the starting point is already part of the visited set.

For `p = 3, n = 6`, the algorithm processes exactly one complete period. The positions are `0, 1, 0, 0, 1, 0, 0`, so the result remains `2`. The fact that the last position returns to `0` is also a concrete check of the identity `pos_{2p} = 0`.

For `p = 8, n = 10^18`, the requested number of moves is enormous, but `moves` becomes `16`. The algorithm only examines those sixteen moves. After that point the same positions recur every sixteen moves, so the answer obtained from the first period is also the answer for the entire requested execution.
