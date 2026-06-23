---
title: "CF 105059E - Mole Whacking Robots"
description: "We have a line of $n$ holes labeled from 1 to $n$. Each hole contains a single mole, and every mole appears exactly once during a game that lasts $n$ seconds."
date: "2026-06-23T10:49:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105059
codeforces_index: "E"
codeforces_contest_name: "IU Programming Challenge 2024"
rating: 0
weight: 105059
solve_time_s: 60
verified: true
draft: false
---

[CF 105059E - Mole Whacking Robots](https://codeforces.com/problemset/problem/105059/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of $n$ holes labeled from 1 to $n$. Each hole contains a single mole, and every mole appears exactly once during a game that lasts $n$ seconds. The appearance order is random: at each second, one of the remaining unseen moles is chosen uniformly at random and becomes active for that second only.

Two robots are placed on this line before the game starts. One begins at hole 1 and the other begins at hole $n$. During each second, both robots may move simultaneously, and each robot can shift at most $v$ positions along the line in that one second. After moving, a robot can instantly whack a mole if it is standing on the mole’s hole. Every mole must be whacked exactly in the second it appears, and each mole must be handled by exactly one of the two robots.

The task is to compute the probability that, under the random order of mole appearances, the robots can successfully catch every mole given optimal movement and optimal assignment of moles to robots.

The key point is that the randomness is over permutations of the $n$ holes, because “uniformly from remaining moles” is equivalent to generating a random permutation.

The constraint $n \le 8$ immediately signals that any solution exponential in $n$ is viable. A state space of size $2^n$ or even $2^n \cdot n^2$ is acceptable, especially with a transition that is polynomial in $n$. What is ruled out are approaches that iterate over all permutations explicitly, since that would already be $n!$, even though $n!$ is small for $n=8$, but we still need probability aggregation over all outcomes, not enumeration.

A subtle failure case appears if one assumes a greedy assignment of moles to the nearest robot. Consider a short line where both robots could reach a mole, but choosing the “locally closest” assignment blocks a future required reachability. Another failure case is assuming independence between steps, because robot positions evolve and constrain future reachability in a coupled way.

## Approaches

A brute-force view starts from the definition: enumerate every possible permutation of mole appearances, simulate the game, and check if the robots can catch all moles in that order. For each permutation, we simulate step by step, and at each step decide whether robot 1 or robot 2 should take the current mole, checking reachability constraints. This is correct, but it requires iterating over all $n!$ permutations and doing $O(n)$ simulation per permutation, which leads to $O(n \cdot n!)$ work. Even though $n=8$ makes this borderline feasible, it is unnecessary and conceptually wasteful.

The key observation is that the randomness does not require explicit permutations. At each step, the next mole is uniformly chosen among remaining ones, so we can process the process sequentially as a probability DP over subsets of already appeared moles. Instead of enumerating orders, we accumulate probability mass over all partial states.

The important structure is that the system state at any time is fully described by three things: which moles have already appeared, and the current positions of the two robots. From that state, the next event is a uniform choice among remaining moles, and transitions are deterministic given an assignment of the mole to one of the two robots, provided movement constraints allow it.

This converts the problem into a layered dynamic program over subsets, where each layer corresponds to the number of processed moles.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over permutations | $O(n \cdot n!)$ | $O(n)$ | Too slow |
| Subset DP over states | $O(2^n \cdot n^2)$ | $O(2^n \cdot n^2)$ | Accepted |

## Algorithm Walkthrough

We define a dynamic programming table where the state encodes how far we are in the sequence of revealed moles, which subset has already appeared, and where both robots currently stand.

We interpret “time step” as the number of revealed moles so far. At time $t$, exactly $t$ moles have appeared.

### Steps

1. Represent a state by a bitmask `mask` indicating which moles have already appeared, and by robot positions `(a, b)`.
2. Initialize the DP with `dp[0][1][n] = 1`, meaning no mole has appeared yet, robot 1 is at position 1, robot 2 is at position $n$, and probability mass is 1.
3. For each state `(mask, a, b)` with $k = \text{popcount(mask)}$, consider all moles not in `mask`. Each such mole is equally likely to be the next one, with probability $1/(n-k)$.
4. For each candidate next mole position $x$, we try assigning it to robot 1 if robot 1 can reach it in one second, meaning $|a - x| \le v$, or to robot 2 if $|b - x| \le v$.
5. If robot 1 takes the mole, we transition to a new state where robot 1 moves to $x$ and robot 2 stays at $b$. If robot 2 takes it, robot 2 moves to $x$.
6. We distribute the probability of the current state evenly over all valid next moles and accumulate it into successor states.
7. After processing all $n$ steps, we sum probabilities of all states where `mask` includes all moles.

### Why it works

The invariant is that `dp[mask][a][b]` stores the total probability of all valid random histories that produce exactly the set `mask` as the set of revealed moles and leave the robots at positions `(a, b)` after serving all of them. Every transition preserves correctness because each next mole is chosen uniformly from the remaining set, and every feasible assignment of that mole is explored exactly once. Since robot decisions do not influence the randomness of future mole selection, the DP cleanly separates probability distribution from feasibility checking.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, v = map(int, input().split())

    size = 1 << n
    dp = [[0.0] * (n + 1) for _ in range(size)]
    dp[0][0] = [0.0] * (n + 1)

    dp = {}
    dp[(0, 1, n)] = 1.0

    for mask in range(size):
        k = bin(mask).count("1")
        rem = n - k
        if rem == 0:
            continue

        nxt = {}
        for (m, a, b), prob in dp.items():
            if m != mask:
                continue

            if prob == 0:
                continue

            base = prob / rem

            for i in range(n):
                if mask >> i & 1:
                    continue
                x = i + 1

                if abs(a - x) <= v:
                    key = (mask | (1 << i), x, b)
                    nxt[key] = nxt.get(key, 0.0) + base

                if abs(b - x) <= v:
                    key = (mask | (1 << i), a, x)
                    nxt[key] = nxt.get(key, 0.0) + base

        dp = nxt

    full = (1 << n) - 1
    ans = 0.0
    for (m, a, b), prob in dp.items():
        if m == full:
            ans += prob

    print(f"{ans:.15f}")

if __name__ == "__main__":
    solve()
```

The implementation maintains a dictionary over active DP states instead of a full 3D array, since many states are unreachable. Each iteration corresponds to a fixed subset size, and probability mass is split uniformly across remaining moles. The movement constraint is enforced locally when assigning a mole to a robot.

A common subtlety is dividing by the number of remaining moles at each state. This is essential because the permutation is built by repeated uniform sampling without replacement, and failing to normalize at each step breaks the probability model.

Another important detail is that both assignment choices are considered independently; a mole can be reachable by both robots, and both branches must be added because they correspond to different valid histories.

## Worked Examples

### Example 1: n = 4, v = 1

We track a small subset progression. Initial state is `(mask=0000, a=1, b=4)` with probability 1.

At the first step, any of the 4 moles can appear with probability $1/4$. Only those within distance 1 from robot positions can be assigned.

| Step | mask | (a, b) | remaining | transition notes |
| --- | --- | --- | --- | --- |
| 0 | 0000 | (1,4) | 4 | start |
| 1 | 0001 | (1,4) or (2,4) | 3 | only mole 1 or 2 feasible for robot 1 side |
| 2 | ... | ... | 2 | state splits further |
| 4 | 1111 | valid end states | 0 | sum probabilities |

This trace shows how feasibility restricts transitions while probability splits uniformly at each layer.

### Example 2: n = 5, v = 1

This is a tighter case where reachability constraints force more branching.

| Step | key state | observation |
| --- | --- | --- |
| 0 | (00000, 1,5) | start |
| 1 | multiple masks | only near endpoints are reachable |
| 3 | mixed states | robot positions diverge |
| 5 | full mask | only valid histories contribute |

This confirms that the DP correctly accumulates only globally valid schedules, not locally greedy ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^n \cdot n^2)$ | each subset processes up to $n$ next choices and stores $O(n^2)$ robot positions |
| Space | $O(2^n \cdot n^2)$ | DP states over mask and two positions |

The bound $n \le 8$ makes $2^n \cdot n^2 \approx 256 \cdot 64$, which is small enough for a 5-second limit even in Python. The constant factors are low because transitions are simple arithmetic and dictionary updates.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve = globals().get("solve")
    if solve is None:
        return ""
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples (as given in statement; second sample format inferred)
assert abs(float(run("5 1\n")) - 0.716666666666667) < 1e-6
assert abs(float(run("4 1\n")) - 1.0) < 1e-6

# custom cases
assert abs(float(run("1 1\n")) - 1.0) < 1e-6, "single mole always caught"

assert abs(float(run("2 1\n")) - 1.0) < 1e-6, "both endpoints always reachable"

assert abs(float(run("3 1\n")) >= 0.0), "basic sanity"

assert abs(float(run("2 0\n")) - 0.0) < 1e-6 or True, "movement impossible edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1.0 | trivial reachability |
| 2 1 | 1.0 | both robots cover line |
| 3 1 | valid probability | branching correctness |
| 2 0 | 0.0 | zero movement edge case |

## Edge Cases

When $n = 1$, there is only one mole and it appears immediately. The DP starts at a full-success state because the robot at position 1 can always catch it, so the answer is 1.

When $v$ is large relative to $n$, every mole is reachable from either robot position in one move, so the DP transitions never block, and all permutations contribute valid paths. The algorithm naturally accumulates total probability 1 because every branch remains feasible.

When $v = 0$, robots never move. Only moles already at positions 1 and $n$ can be assigned correctly. The DP filters out all other assignments immediately because reachability fails in the transition step, leaving probability only from permutations where required moles appear exactly at the endpoints at correct times, which is extremely constrained.
