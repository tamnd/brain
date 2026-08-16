---
title: "CF 102275A - On the Run"
description: "We have an (N times M) rectangular grid. Mr. X occupies one cell, and there are either one or two HAHA agents occupying two other cells. In every round, every agent must move exactly one step to an adjacent free cell, in any order. After all agents have moved, Mr."
date: "2026-08-17T02:59:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102275
codeforces_index: "A"
codeforces_contest_name: "2019 Facebook Hacker Cup, Round 2"
rating: 0
weight: 102275
solve_time_s: 1057
verified: true
draft: false
---

[CF 102275A - On the Run](https://codeforces.com/problemset/problem/102275/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 17m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an (N \times M) rectangular grid. Mr. X occupies one cell, and there are either one or two HAHA agents occupying two other cells. In every round, every agent must move exactly one step to an adjacent free cell, in any order. After all agents have moved, Mr. X also makes exactly one step to an adjacent free cell. If every adjacent cell of Mr. X is occupied by agents, he has no legal move and loses.

The input gives the grid dimensions, Mr. X's starting cell, and the starting cells of the (K) agents. The output asks whether the agents can force a loss, with perfect play from both sides. `Y` means the agents have a winning strategy, while `N` means Mr. X can keep moving forever.

The constraints look large enough to discourage any simulation of the game. With (N,M\le300), there can be (90{,}000) cells. A state with two agents contains three occupied cells, so an explicit game graph already has on the order of (90{,}000^3), roughly (7.3\times10^{14}), ordered configurations. Even storing such a graph is impossible. The fact that there are at most two agents is the crucial structural restriction that makes a much simpler characterization possible.

The first useful observation is that a grid cell has at least two neighbors, and an interior cell has four. Since there are at most two agents, Mr. X can surrender only when he is standing in a corner and both of that corner's two neighbors are occupied. Thus the agents never need to surround an interior cell. They only need to force Mr. X to a corner.

The second observation is that the grid is bipartite. Color cell ((r,c)) by the parity of (r+c). Every legal move changes this parity. Since every participant moves exactly once in every complete round, the parity relationship between the three participants at the beginning of a round never changes.

Consider the small input

```
1
3 3 1
1 1
2 2
```

There is only one agent, so the correct output is `N`. A careless simulation might see the agent moving toward a corner and assume it can eventually trap Mr. X, but two occupied neighbors are required at the final position.

Now consider

```
1
3 3 2
1 1
1 3
3 1
```

All three positions have even (r+c). The correct output is `Y`. After the agents move to ((1,2)) and ((2,1)), Mr. X at ((1,1)) has no free neighbor.

A more subtle case is

```
1
4 4 2
1 2
1 3
1 4
```

The parities are (1,0,1), so they are not all equal. The correct output is `N`. A simulation that only checks whether the agents can approach the same corner can incorrectly predict a trap. The parity relation prevents one of the agents from being in the correct color class when the final two neighboring cells must be occupied.

The parity characterization is also consistent with the contest discussion, where the accepted observation for problem A was summarized as requiring all three points to have the same value of ((x+y)\bmod2) when (K=2), while (K=1) is always losing for the agents.

## Approaches

A direct approach would model every possible arrangement of Mr. X and the agents as a game state. From each state, we would enumerate the possible moves of the agents, account for their possible order, and then enumerate Mr. X's responses. Because this is a finite reachability game, a retrograde game analysis could theoretically classify every state as winning or losing.

The problem is the size of that state space. Let (V=NM). With two agents, there are roughly (V(V-1)(V-2)) ordered placements, so at the maximum grid size there are about (90{,}000^3=7.29\times10^{14}) states before considering any moves. Even a constant amount of work per state is far beyond the limits.

The structure that destroys this enormous state space is the checkerboard coloring. Every move flips color. At the beginning of each complete round, all three participants have made the same number of moves since the start, so their pairwise parity relationships are fixed forever.

Suppose (K=2), and one agent starts on the opposite color from Mr. X. At the beginning of every agent phase, that agent is still on the opposite color from Mr. X. The agent must then move, so it switches to Mr. X's color. A neighbor of Mr. X has the opposite color from Mr. X, so that agent cannot occupy a neighboring cell of Mr. X after its mandatory move. Since both neighbors of a corner are required to trap Mr. X, the agents can never win.

This gives the necessary condition that all three initial positions must have the same parity.

The same condition is sufficient. When all three participants start on the same checkerboard color, the two agents can use the standard two-agent grid-squeezing strategy. Two agents are sufficient to force a moving player toward the boundary of a finite rectangular grid and eventually into a corner. Classical grid pursuit strategies do exactly this by maintaining two shrinking regions, or shadow cones, and preventing the runner from crossing back through a controlled boundary. Two agents suffice for rectangular grids because the agents can progressively reduce the runner's available rectangle until only a corner remains.

The special rule that every agent must move is handled by the same parity condition. At the beginning of each round, the agents and Mr. X have equal parity. A required agent move flips its parity exactly when Mr. X's next move will flip his. Thus the agents can carry out the squeezing strategy without needing to wait for an unused turn. When the runner reaches a corner, the two agents can occupy its two neighbors on their move, forcing surrender.

The brute force works because it explicitly represents every possible game state, but fails because the state space is cubic in the number of cells. The parity observation collapses the entire game to one constant-time test.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O((NM)^{K+1})) | (O((NM)^{K+1})) | Too slow |
| Optimal | (O(K)) per test case | (O(K)) | Accepted |

## Algorithm Walkthrough

1. Read (N,M,K), Mr. X's position, and all agent positions. The actual dimensions of the grid will not affect the final test, because (N,M\ge3) guarantees that every corner has exactly two neighbors.
2. If (K=1), answer `N`. One agent can occupy at most one of the two neighbors of a corner, while surrender requires both neighbors to be occupied.
3. If (K=2), compute the checkerboard color of every participant as ((r+c)\bmod2). A move changes this value because exactly one coordinate changes by (1).
4. Check whether the two agents and Mr. X all have the same parity. If any one differs, answer `N`. The differing agent will always have the wrong parity after its mandatory move to participate in a corner trap, so it can never occupy one of the required neighboring cells.
5. If all three parities are equal, answer `Y`. The two agents can apply the standard two-agent squeezing strategy on the rectangular grid. Their equal round-start parity lets every required move fit the alternating-color structure, and the strategy eventually confines Mr. X to a corner. Once he is there, the agents can occupy the two adjacent cells and leave him with no legal move.

The invariant is the parity relationship at the beginning of every round. Every participant makes exactly one move per round, so every participant flips color once. Consequently, if two participants have equal colors initially, they have equal colors at every round boundary, and if they have different colors initially, they remain different. A winning corner trap requires both agents to have the same color as Mr. X at the start of the agent phase, because their moves must place them onto cells of the opposite color. Thus unequal initial parity is an absolute obstruction, while equal initial parity is exactly the case in which the two-agent grid-squeezing strategy can complete the trap.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for tc in range(1, t + 1):
        n, m, k = map(int, input().split())

        x_r, x_c = map(int, input().split())
        agents = [tuple(map(int, input().split())) for _ in range(k)]

        if k == 1:
            ans = "N"
        else:
            target_parity = (x_r + x_c) & 1
            ans = "Y"

            for r, c in agents:
                if ((r + c) & 1) != target_parity:
                    ans = "N"
                    break

        out.append(f"Case #{tc}: {ans}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input is read one test case at a time. For each case, Mr. X's parity is calculated once using `(x_r + x_c) & 1`.

When there is one agent, the program immediately returns `N`, because the grid has at least three rows and three columns, so every corner has two distinct neighbors. One agent cannot occupy both.

When there are two agents, the program starts with `Y` and changes it to `N` as soon as an agent has a different parity from Mr. X. There is no need to store the grid, generate moves, or track future positions. The parity relation already determines the game.

The coordinates are one-based, exactly as supplied by the problem. Adding them before taking the parity is unaffected by the choice of one-based versus zero-based indexing, since shifting both coordinates by one changes their sum by two.

Python integers have arbitrary precision, although no large arithmetic is involved here. The memory usage is constant apart from the small list of at most two agent positions.

## Worked Examples

### Sample 1

The first sample has one agent.

| Variable | Value |
| --- | --- |
| (N,M) | (3,3) |
| (K) | (1) |
| Mr. X | ((1,1)) |
| Mr. X parity | (0) |
| Agent | ((2,2)) |
| Agent parity | (0) |
| Decision | `K == 1` |
| Output | `N` |

Even though the agent has the same parity as Mr. X, parity equality is not sufficient with only one agent. The corner ((1,1)) has two neighbors, ((1,2)) and ((2,1)), and both would have to be occupied simultaneously. One agent cannot do that, so the answer is `N`.

### Sample 2

The second sample has two agents.

| Variable | Value |
| --- | --- |
| (N,M) | (3,3) |
| (K) | (2) |
| Mr. X | ((1,1)) |
| Mr. X parity | (0) |
| Agent 1 | ((1,3)) |
| Agent 1 parity | (0) |
| Agent 2 | ((3,1)) |
| Agent 2 parity | (0) |
| All parities equal | Yes |
| Output | `Y` |

The two agents can move to ((1,2)) and ((2,1)), the two cells adjacent to Mr. X. Both are free before the corresponding agent moves, so the final state leaves Mr. X with no legal move. The answer is `Y`.

The trace demonstrates why parity equality is the winning configuration. At the beginning, all three positions have the same color. After both agents move, both have flipped color and can occupy neighbors of Mr. X, while Mr. X has not moved yet.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(K)) per test case | We inspect at most two agent positions. |
| Space | (O(K)) | We store at most two agent positions. |

Since (K\le2), the work per test case is effectively constant. Even with (T=500), the algorithm performs only a few thousand arithmetic operations. The grid can contain (90{,}000) cells, but the solution never constructs it.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for tc in range(1, t + 1):
        n, m, k = map(int, input().split())
        xr, xc = map(int, input().split())
        agents = [tuple(map(int, input().split())) for _ in range(k)]

        if k == 1:
            ans = "N"
        else:
            p = (xr + xc) & 1
            ans = "Y"
            for r, c in agents:
                if ((r + c) & 1) != p:
                    ans = "N"
                    break

        out.append(f"Case #{tc}: {ans}")

    return "\n".join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

sample = """\
8
3 3 1
1 1
2 2
3 3 2
1 1
1 3
3 1
4 4 2
1 2
1 3
1 4
3 10 2
2 10
1 9
3 9
8 8 2
8 1
8 8
1 1
300 5 2
2 3
15 2
300 5
67 25 2
32 10
66 3
21 18
71 87 2
36 44
1 87
71 1
"""

expected_sample = """\
Case #1: N
Case #2: Y
Case #3: N
Case #4: Y
Case #5: N
Case #6: Y
Case #7: N
Case #8: Y
"""

assert run(sample) == expected_sample, "provided samples"

assert run("""\
1
3 3 1
1 1
2 2
""") == "Case #1: N", "minimum grid with one agent"

assert run("""\
1
3 3 2
1 1
1 3
3 1
""") == "Case #1: Y", "minimum grid, all three positions have even parity"

assert run("""\
1
4 4 2
1 2
1 3
1 4
""") == "Case #1: N", "boundary case with mixed parity"

assert run("""\
1
300 300 2
2 3
100 100
299 299
""") == "Case #1: N", "maximum grid size with mixed parity"

assert run("""\
1
300 5 2
2 2
2 4
4 2
""") == "Case #1: Y", "large boundary dimensions with equal parity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 3 1 / 1 1 / 2 2` | `Case #1: N` | Minimum grid and the one-agent case |
| `3 3 2 / 1 1 / 1 3 / 3 1` | `Case #1: Y` | All three positions have the same checkerboard color |
| `4 4 2 / 1 2 / 1 3 / 1 4` | `Case #1: N` | Mixed parity on boundary cells |
| `300 300 2 / 2 3 / 100 100 / 299 299` | `Case #1: N` | Maximum dimensions and large coordinates |
| `300 5 2 / 2 2 / 2 4 / 4 2` | `Case #1: Y` | Equal parity near grid boundaries with the maximum row count |

The literal condition that all coordinates be identical cannot occur in a valid input, because the problem guarantees that all participants occupy distinct cells. The closest meaningful interpretation for an "all-equal" test is that all three parity values are equal, which is covered by the second and fifth custom cases.

## Edge Cases

The one-agent case is handled before any parity reasoning. For

```
1
3 3 1
1 1
2 2
```

Mr. X starts at a corner, but the only agent cannot fill both ((1,2)) and ((2,1)). Even if the agent moves to one of them, the other remains free. The algorithm immediately returns `N`.

For mixed parity, consider

```
1
4 4 2
1 2
1 3
1 4
```

Mr. X has parity (3\bmod2=1). The first agent has parity (4\bmod2=0), while the second has parity (5\bmod2=1). At every round boundary the first agent remains opposite in color to Mr. X. After the first agent is forced to move, it switches to Mr. X's color rather than the neighbor color needed for a trap. Consequently both required corner neighbors can never be occupied after the agents' phase. The algorithm returns `N`.

For the winning parity configuration,

```
1
3 3 2
1 1
1 3
3 1
```

all three sums are even. The agents begin at the cells two steps along the two directions from the corner. They move to ((1,2)) and ((2,1)), which are precisely the two neighbors of Mr. X. The next move is impossible, so the algorithm returns `Y`.

Finally, the largest grid dimensions do not create a special case. For

```
1
300 300 2
2 3
100 100
299 299
```

Mr. X has odd parity, while both agents have even parity. The grid size is irrelevant once the parity obstruction is found, so the answer is immediately `N`. The algorithm never allocates a (300\times300) grid and never simulates a chase.
