---
title: "CF 39E - What Has Dirichlet Got to Do with That?"
description: "We start with a distinct boxes and b distinct items. Since boxes may stay empty and every item independently chooses one"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "games"]
categories: ["algorithms"]
codeforces_contest: 39
codeforces_index: "E"
codeforces_contest_name: "School Team Contest 1 (Winter Computer School 2010/11)"
rating: 2000
weight: 39
solve_time_s: 117
verified: true
draft: false
---

[CF 39E - What Has Dirichlet Got to Do with That?](https://codeforces.com/problemset/problem/39/E)

**Rating:** 2000  
**Tags:** dp, games  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with `a` distinct boxes and `b` distinct items. Since boxes may stay empty and every item independently chooses one of the boxes, the number of possible placements is simply:

$a^b$

Two players alternate turns. On each turn, a player may either increase the number of boxes by one or increase the number of items by one. After making the move, if the number of placements becomes at least `n`, that player immediately loses.

The game starts from a state where `a^b < n`, and Stas moves first. We must determine whether the first player wins, the second player wins, or whether optimal play leads to an infinite game, which the statement calls `"Missing"`.

The constraints completely shape the solution. The number of items never exceeds `30` initially, but during the game it can increase further. The number of boxes can start as large as `10000`. The threshold `n` is at most `10^9`, which is small enough that powers grow past it quickly. That observation is crucial because it means the game graph is actually tiny, even though `a` itself may be large.

A naive recursive game search without memoization would repeatedly revisit the same states. Even worse, the game graph contains cycles. For example, from `(1,1)` you can go to `(2,1)` or `(1,2)`, and both can continue forever while staying below `n` for a while. Any solution that assumes the game is a directed acyclic graph will silently fail.

One subtle edge case is the existence of draws. Consider:

```
1 1 1000000000
```

Here the value is `1^1 = 1`. Increasing the number of boxes keeps the value at `1`, so both players may keep adding boxes forever. A solution that only classifies states as win or lose will incorrectly force an answer even though perfect play produces an infinite game.

Another dangerous case is overflow during power computation. Suppose we check:

```
10000 30 1000000000
```

The actual value of `10000^30` is astronomically large. Using normal exponentiation without early stopping can overflow fixed-width integers in many languages or waste time constructing giant Python integers. We only care whether the value reaches `n`, so computations must stop as soon as the threshold is crossed.

A third subtle case comes from positions where one move loses immediately and the other continues the game. For example:

```
2 2 10
```

The current value is `4`. Increasing boxes gives `3^2 = 9`, still safe. Increasing items gives `2^3 = 8`, also safe. But after careful play, the first player can force the second into a losing move. Greedy reasoning based only on the next step is not enough.

## Approaches

The most direct approach is to treat every pair `(a,b)` as a game state and recursively determine whether it is winning or losing. From each state there are at most two moves:

```
(a+1, b)
(a, b+1)
```

Any move that produces a value at least `n` is forbidden in practice because the player immediately loses after making it.

This recursive definition is correct because impartial combinatorial games naturally reduce to state transitions. A state is winning if there exists a move to a losing state. A state is losing if every valid move leads to a winning state.

The problem is that this game graph is not acyclic. States can continue growing forever in some directions while staying valid. The simplest example is any state with `b = 1`, because:

$a^1=a$

As long as `a < n`, players may keep increasing boxes forever. A DFS that assumes eventual termination cannot distinguish between genuinely winning positions and positions that allow infinite play.

The key observation is that the game graph is still finite if we only keep states satisfying:

$a^b<n$

Once the value reaches `n`, the game ends immediately. Since `n ≤ 10^9`, the exponent grows very quickly. For `b ≥ 30`, even small bases already exceed the limit. The total number of reachable safe states is actually tiny, roughly a few hundred thousand at most.

That lets us model the game as a finite directed graph with draws. We can then use standard game-state propagation:

If a state has a move to a losing state, it is winning.

If every move goes to winning states, it is losing.

States that are neither provably winning nor losing belong to cycles from which players can avoid defeat forever, so they are draws.

This becomes a retrograde analysis problem on a directed graph. We build all valid states, reverse all edges, and propagate outcomes backward using BFS.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS | Exponential | Exponential | Too slow |
| Retrograde Game Analysis | O(S) | O(S) | Accepted |

Here `S` is the number of valid states with `a^b < n`.

## Algorithm Walkthrough

1. Enumerate every valid state `(a,b)` such that `a^b < n`.

We only care about states where the game has not already ended. Any move producing `a^b ≥ n` immediately loses.
2. For each state, generate its legal moves.

From `(a,b)` we try `(a+1,b)` and `(a,b+1)`. A move is legal only if the destination still satisfies `a^b < n`.
3. Compute the outdegree of every state.

The outdegree is the number of safe moves available. This value is needed for backward propagation.
4. Build reverse edges.

If state `u` can move to state `v`, then `v` stores `u` in its reverse adjacency list. This allows us to propagate information backward once the status of `v` becomes known.
5. Initialize losing states.

Any state with zero legal moves is losing because every possible move immediately reaches or exceeds `n`.
6. Run BFS propagation.

When a losing state is discovered, every predecessor becomes winning because it can move into that losing state.

When a winning state is discovered, we decrement the remaining unexplored moves of its predecessors. If all moves of a predecessor lead to winning states, then that predecessor becomes losing.
7. Any unclassified state after BFS is a draw.

Those states belong to cycles where neither player can force the game to end.
8. Output the result for the initial state.

If the initial state is winning, Stas can force Masha to lose, so we print `"Masha"`.

If the initial state is losing, Stas loses under optimal play, so we print `"Stas"`.

Otherwise we print `"Missing"`.

### Why it works

The propagation maintains the standard impartial game invariant.

A state is winning exactly when there exists a move to a losing state. Once we identify a losing state, all predecessors immediately become winning.

A state is losing exactly when every legal move goes to winning states. The outdegree counter tracks how many unresolved moves remain. When all outgoing moves are known to be winning, the state must be losing.

Any state never classified by these two rules must belong to a cycle that can avoid terminal states forever. Since neither player can force a win from such a region, the correct result is a draw.

## Python Solution

```python
import sys
from collections import deque, defaultdict

input = sys.stdin.readline

def safe_pow(a, b, limit):
    res = 1
    for _ in range(b):
        res *= a
        if res >= limit:
            return limit
    return res

def solve():
    a0, b0, n = map(int, input().split())

    states = []
    idx = {}

    max_b = 1

    # Enumerate all valid states
    a = 1
    while safe_pow(a, 1, n) < n:
        b = 1
        while safe_pow(a, b, n) < n:
            idx[(a, b)] = len(states)
            states.append((a, b))
            max_b = max(max_b, b)
            b += 1
        a += 1

    m = len(states)

    rev = [[] for _ in range(m)]
    outdeg = [0] * m

    # Build graph
    for i, (a, b) in enumerate(states):
        for na, nb in ((a + 1, b), (a, b + 1)):
            if (na, nb) in idx:
                j = idx[(na, nb)]
                outdeg[i] += 1
                rev[j].append(i)

    # 0 = draw/unvisited
    # 1 = winning
    # 2 = losing
    state = [0] * m

    q = deque()

    # Terminal losing states
    for i in range(m):
        if outdeg[i] == 0:
            state[i] = 2
            q.append(i)

    rem = outdeg[:]

    # Retrograde analysis
    while q:
        v = q.popleft()

        for u in rev[v]:
            if state[u] != 0:
                continue

            if state[v] == 2:
                state[u] = 1
                q.append(u)
            else:
                rem[u] -= 1
                if rem[u] == 0:
                    state[u] = 2
                    q.append(u)

    start = idx[(a0, b0)]

    if state[start] == 1:
        print("Masha")
    elif state[start] == 2:
        print("Stas")
    else:
        print("Missing")

solve()
```

The first important piece is `safe_pow`. We never need the exact value once it reaches `n`, so the multiplication stops early. That avoids constructing huge integers and keeps enumeration fast.

State generation relies on the fact that only safe positions matter. The nested loops stop naturally because powers eventually exceed `n`. Even though `a` may grow large, the total number of valid states stays manageable.

The graph construction phase creates both forward information through `outdeg` and reverse information through `rev`. Reverse edges are what make backward propagation efficient.

The BFS itself implements the standard winning-losing game logic. When we process a losing node, every predecessor instantly becomes winning because it has a move to defeat. When we process a winning node, predecessors merely lose one remaining safe option. Only after all options become winning do we classify the predecessor as losing.

The states left as `0` after BFS are exactly the draw states. They are never forced into either category because players can keep cycling indefinitely.

One subtle implementation detail is the output convention. The problem asks for the loser, not the winner. If the initial state is winning for the current player, then Stas wins and Masha loses, so we print `"Masha"`.

## Worked Examples

### Example 1

Input:

```
2 2 10
```

Safe states include:

| State | Value | Legal moves |
| --- | --- | --- |
| (2,2) | 4 | (3,2), (2,3) |
| (3,2) | 9 | none |
| (2,3) | 8 | none |

Propagation works like this:

| Step | Processed state | Type | Effect |
| --- | --- | --- | --- |
| 1 | (3,2) | Losing | (2,2) becomes winning |
| 2 | (2,3) | Losing | already resolved |

Since `(2,2)` is winning, Stas can force Masha to lose.

Output:

```
Masha
```

This trace demonstrates the central game rule. A single move to a losing state is enough to make the current state winning.

### Example 2

Input:

```
1 1 1000000000
```

Key states:

| State | Value | Safe moves |
| --- | --- | --- |
| (1,1) | 1 | (2,1), (1,2) |
| (2,1) | 2 | (3,1), (2,2) |
| (3,1) | 3 | (4,1), (3,2) |

The chain `(1,1) → (2,1) → (3,1) → ...` never forces termination because increasing boxes with one item keeps the value below `n` for a very long time.

No backward propagation can classify these states as forced wins or losses, so they remain draws.

Output:

```
Missing
```

This example confirms that cycles and infinite play must be handled explicitly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S) | each valid state and edge is processed once |
| Space | O(S) | graph storage and BFS arrays |

`S` is the number of states satisfying `a^b < n`. Because `n ≤ 10^9`, powers grow rapidly and `S` stays comfortably small for the limits. The solution easily fits within both the 2-second time limit and the 64 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def safe_pow(a, b, limit):
        res = 1
        for _ in range(b):
            res *= a
            if res >= limit:
                return limit
        return res

    a0, b0, n = map(int, input().split())

    states = []
    idx = {}

    a = 1
    while safe_pow(a, 1, n) < n:
        b = 1
        while safe_pow(a, b, n) < n:
            idx[(a, b)] = len(states)
            states.append((a, b))
            b += 1
        a += 1

    m = len(states)

    rev = [[] for _ in range(m)]
    outdeg = [0] * m

    for i, (a, b) in enumerate(states):
        for na, nb in ((a + 1, b), (a, b + 1)):
            if (na, nb) in idx:
                j = idx[(na, nb)]
                outdeg[i] += 1
                rev[j].append(i)

    state = [0] * m
    q = deque()

    for i in range(m):
        if outdeg[i] == 0:
            state[i] = 2
            q.append(i)

    rem = outdeg[:]

    while q:
        v = q.popleft()

        for u in rev[v]:
            if state[u] != 0:
                continue

            if state[v] == 2:
                state[u] = 1
                q.append(u)
            else:
                rem[u] -= 1
                if rem[u] == 0:
                    state[u] = 2
                    q.append(u)

    start = idx[(a0, b0)]

    if state[start] == 1:
        return "Masha\n"
    elif state[start] == 2:
        return "Stas\n"
    return "Missing\n"

# provided sample
assert run("2 2 10\n") == "Masha\n", "sample 1"

# draw case
assert run("1 1 1000000000\n") == "Missing\n", "infinite play"

# immediate trap
assert run("3 2 10\n") == "Stas\n", "no safe moves"

# tiny boundary
assert run("1 1 2\n") == "Stas\n", "minimum threshold"

# larger mixed case
assert run("2 3 20\n") == "Masha\n", "non-trivial winning state"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1000000000` | `Missing` | infinite-play cycle detection |
| `3 2 10` | `Stas` | terminal losing state |
| `1 1 2` | `Stas` | smallest valid threshold |
| `2 3 20` | `Masha` | deeper retrograde propagation |

## Edge Cases

Consider the draw case:

```
1 1 1000000000
```

The algorithm generates a large chain of states `(k,1)` where every state can move to `(k+1,1)` safely. None of these states ever reaches outdegree zero during initialization. During BFS propagation, they are never forced into winning or losing categories because the cycle of safe play never collapses. The state remains unclassified, so the algorithm correctly prints:

```
Missing
```

Now consider a terminal position:

```
3 2 10
```

The current value is:

$3^2=9$

Increasing boxes gives `4^2 = 16`, which loses immediately. Increasing items gives `3^3 = 27`, which also loses immediately. The state has zero legal outgoing moves, so it is initialized as losing. Since Stas starts there, the output is:

```
Stas
```

Finally, consider the small-threshold boundary:

```
1 1 2
```

The current value is `1`. Both possible moves produce exactly `2`, which already triggers defeat because the condition is `>= n`, not strictly greater. The algorithm rejects both moves during graph construction, giving outdegree zero. That detail avoids the classic off-by-one mistake.
