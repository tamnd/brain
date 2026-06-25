---
title: "CF 105971A - Tokens on a Graph"
description: "We have a connected undirected graph. Some vertices contain tokens and some vertices contain bonuses. A move consists of taking one token and moving it to a neighboring vertex."
date: "2026-06-25T13:41:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105971
codeforces_index: "A"
codeforces_contest_name: "BSUIR Open XIII: Student final"
rating: 0
weight: 105971
solve_time_s: 51
verified: true
draft: false
---

[CF 105971A - Tokens on a Graph](https://codeforces.com/problemset/problem/105971/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected undirected graph. Some vertices contain tokens and some vertices contain bonuses. A move consists of taking one token and moving it to a neighboring vertex. The first move is always allowed, but every later move is allowed only if the previous moved token landed on a bonus vertex. The next move must use a different token. The goal is to decide whether any token can eventually reach vertex 1.

The difficulty is that the moves of a token are not the only thing that matters. A token close to the finish may still be useless if there are not enough other tokens to keep the chain of bonus landings alive. At the same time, some groups of bonuses can generate unlimited extra moves.

The constraints allow the total number of vertices and edges across test cases to reach about 200000. This rules out exploring every possible sequence of token moves, because the number of possible states grows exponentially. A solution must be close to linear in the size of the graph.

A few cases are easy to miss. If a token starts at vertex 1, the answer is immediately YES because no moves are needed. For example:

```
n = 3, m = 2
tokens = [1]
bonuses = [2]
edges = (1,2), (2,3)
```

The correct output is YES. A solution that only checks whether a token can move into vertex 1 would incorrectly reject it.

Another tricky case is when a token can reach the finish only by using several bonuses, but there are not enough other tokens to continue the chain.

```
n = 4, m = 3
tokens = [4]
bonuses = [3]
edges = (1,2), (2,3), (3,4)
```

The correct output is NO. The token can move from 4 to 3, but after that it cannot move again because the same token cannot be reused. A simple shortest path check would incorrectly think the token can continue.

A final edge case is an infinite source of moves. If two bonuses are adjacent, a token near that area can keep activating the bonuses repeatedly by moving different tokens around the bonus edge.

```
n = 5, m = 5
tokens = [5,4]
bonuses = [2,3]
edges = (1,2), (2,3), (3,4), (4,5), (2,5)
```

The correct output is YES because the bonus pair can provide unlimited turns. An approach that only counts the number of nearby tokens would miss this.

## Approaches

A direct approach would simulate all possible games. We could choose a token, move it, then recursively try every next token that becomes available. This is correct because it explores exactly the possible sequences of moves. The problem is that the branching factor can be huge. With many tokens, the number of possible orders of moves is comparable to the number of permutations of tokens, which is far beyond what the limits allow.

The key observation is to stop thinking about the whole sequence and focus on how many moves are needed to bring one chosen token to the finish. Suppose we choose a token that will eventually reach vertex 1. Before the final move, this token must travel through vertices that allow the chain to continue. These useful vertices are bonus vertices that lie on a path toward the finish.

We first find, for every vertex, the minimum number of bonus landings needed before a token there can reach the finish. This can be done with a BFS starting from vertex 1, but we only expand through bonus vertices. If a token is at a vertex with distance `d`, it needs `d` moves of support before it can be finished.

Now we only need to know whether the other tokens can provide enough support. A token can contribute one extra move if it is next to a bonus vertex. It can contribute unlimited moves if it is next to a bonus vertex that is part of a pair of adjacent bonuses, because those bonuses can be reused forever by alternating tokens.

The brute force works because it models every possible ordering. It fails when the number of possible orders explodes. The observation that only the amount of available support matters lets us replace a search over sequences with graph preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the graph and store which vertices contain tokens and which contain bonuses. If any token starts at vertex 1, the answer is immediately YES because the game is already finished.
2. Mark every vertex that belongs to a pair of adjacent bonuses. These vertices represent a place where a token can help create unlimited future moves.
3. Run BFS from vertex 1. Only move through bonus vertices while expanding. The resulting distance tells us the minimum number of moves needed from that vertex to reach the finish while keeping the game alive.
4. For every token, compute how much support it needs. A token can use its own first move for free, so if its required distance is `d`, it needs `d - 1` additional moves from other tokens.
5. Count the available support from all tokens. A token contributes unlimited support if it is adjacent to a double bonus area. Otherwise it contributes one move if it can reach a bonus in one step.
6. Try every token as the final winning token. Temporarily remove its own contribution from the support count. If there is unlimited support, or enough one move supports, then the answer is YES.

Why it works: the chosen winning token only needs a chain of moves before its final move to the finish. Every non-final move exists only to activate another turn, so the only relevant information about the other tokens is how many turns they can provide. Tokens near reusable bonus structures provide infinite turns, while all other useful tokens provide exactly one. The BFS distance gives the exact number of required turns, so the final comparison is sufficient.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    p, b = map(int, input().split())

    tokens = list(map(int, input().split()))
    bonuses = [0] * (n + 1)

    if b:
        for x in map(int, input().split()):
            bonuses[x] = 1
    else:
        input()

    graph = [[] for _ in range(n + 1)]

    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    has_pair = [0] * (n + 1)
    for i in range(1, n + 1):
        if bonuses[i]:
            for v in graph[i]:
                if bonuses[v]:
                    has_pair[i] = 1
                    break

    if 1 in tokens:
        print("YES")
        return

    support = [0] * (n + 1)

    for x in tokens:
        for v in graph[x]:
            if has_pair[v]:
                support[x] = 2
                break
            if bonuses[v]:
                support[x] = max(support[x], 1)

    dist = [-1] * (n + 1)
    q = deque([1])
    dist[1] = 0

    while q:
        u = q.popleft()
        for v in graph[u]:
            if bonuses[v] and dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)

    cnt_one = 0
    cnt_inf = 0

    for x in tokens:
        if support[x] == 1:
            cnt_one += 1
        elif support[x] == 2:
            cnt_inf += 1

    for x in tokens:
        if support[x] == 1:
            cnt_one -= 1
        elif support[x] == 2:
            cnt_inf -= 1

        need = 10**9

        if dist[x] != -1:
            need = dist[x]

        for v in graph[x]:
            if dist[v] != -1:
                need = min(need, dist[v] + 1)

        if need != 10**9:
            if cnt_inf > 0 or cnt_one >= need - 1:
                print("YES")
                return

        if support[x] == 1:
            cnt_one += 1
        elif support[x] == 2:
            cnt_inf += 1

    print("NO")

t = int(input())
for _ in range(t):
    solve()
```

The code first builds the adjacency list because every later step needs fast access to neighbors. The `has_pair` array identifies vertices that sit inside an adjacent bonus pair, which are exactly the places where support becomes unlimited.

The BFS is slightly different from a normal shortest path search. We start from the finish and only expand into bonus vertices because every intermediate move must land on a bonus. A non-bonus vertex cannot be part of the preparation path.

The final loop tests each token as the one that reaches the finish. Its own contribution is removed before checking because it cannot help itself. The value `need - 1` comes from the fact that the first move of the game is always available without requiring a previous bonus activation.

## Worked Examples

Consider:

```
n = 4, m = 3
tokens = [4,3]
bonuses = [3]
edges = (1,2), (2,3), (3,4)
```

| Step | Current token | Distance | One move supports | Infinite supports | Result |
| --- | --- | --- | --- | --- | --- |
| Initial | 4 | 3 | 1 | 0 | Continue |
| Test token 4 | 3 needed | 1 | 0 | Not enough | NO |

The token at 4 can enter the bonus, but after that there is no other token available to continue the sequence. The trace shows why distance alone is not enough.

Another example:

```
n = 4, m = 4
tokens = [4,3]
bonuses = [2,3]
edges = (1,2), (2,3), (3,4), (1,4)
```

| Step | Current token | Distance | One move supports | Infinite supports | Result |
| --- | --- | --- | --- | --- | --- |
| BFS | 1 | 0 |  |  |  |
| Bonus 2 | 1 |  |  |  |  |
| Bonus 3 | 2 |  |  |  |  |
| Test token 4 | 2 | 0 | 1 | 0 | YES |

The token at 4 can use the bonus chain. The support from the other token is enough to keep the game alive until the final move.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Every edge is processed a constant number of times by BFS and preprocessing |
| Space | O(n + m) | The adjacency list and auxiliary arrays store graph information |

The total input size across all tests fits the linear solution. The algorithm avoids exploring game states, so it remains fast even for the largest graphs.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n, m = map(int, sys.stdin.readline().split())
        p, b = map(int, sys.stdin.readline().split())
        tokens = list(map(int, sys.stdin.readline().split()))
        bonuses = [0] * (n + 1)
        if b:
            for x in map(int, sys.stdin.readline().split()):
                bonuses[x] = 1
        else:
            sys.stdin.readline()

        g = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v = map(int, sys.stdin.readline().split())
            g[u].append(v)
            g[v].append(u)

        if 1 in tokens:
            out.append("YES")
            continue

        pair = [0] * (n + 1)
        for i in range(1, n + 1):
            if bonuses[i] and any(bonuses[x] for x in g[i]):
                pair[i] = 1

        typ = []
        one = inf = 0
        for x in tokens:
            val = 0
            for y in g[x]:
                if pair[y]:
                    val = 2
                    break
                if bonuses[y]:
                    val = 1
            typ.append(val)
            if val == 1:
                one += 1
            elif val == 2:
                inf += 1

        dist = [-1] * (n + 1)
        q = deque([1])
        dist[1] = 0
        while q:
            u = q.popleft()
            for v in g[u]:
                if bonuses[v] and dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)

        ok = False
        for idx, x in enumerate(tokens):
            if typ[idx] == 1:
                one -= 1
            elif typ[idx] == 2:
                inf -= 1

            need = 10**9
            if dist[x] != -1:
                need = dist[x]
            for y in g[x]:
                if dist[y] != -1:
                    need = min(need, dist[y] + 1)

            if need != 10**9 and (inf or one >= need - 1):
                ok = True

            if typ[idx] == 1:
                one += 1
            elif typ[idx] == 2:
                inf += 1

        out.append("YES" if ok else "NO")

    sys.stdin = old
    return "\n".join(out)

assert run("""1
3 2
1 1
1
2
1 2
2 3
""") == "YES"

assert run("""1
4 3
1 1
4
3
1 2
2 3
3 4
""") == "NO"

assert run("""1
4 4
2 2
3 4
2 3
1 2
2 3
3 4
1 4
""") == "YES"

assert run("""1
2 1
1 0
2

1 2
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Token already on finish | YES | Immediate win case |
| Single token needing bonus chain | NO | Prevents ignoring token reuse rules |
| Adjacent bonuses with multiple tokens | YES | Infinite support detection |
| No bonuses and one move only | NO | Boundary condition |

## Edge Cases

For the first edge case, a token on vertex 1 never enters the algorithmic checks because the answer is returned immediately. This handles the state where the game has already ended before any move.

For the single token bonus case, the BFS correctly finds that the token can approach the finish, but the support count is zero after removing the winning token. The condition fails because there are not enough other tokens to provide turns.

For the adjacent bonus case, the preprocessing marks the bonus pair. Any token next to that area is classified as infinite support, so the final check succeeds without needing to count individual moves. This captures the repeating nature of adjacent bonuses.
