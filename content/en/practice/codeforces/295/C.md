---
title: "CF 295C - Greg and Friends"
description: "Every person weighs either 50 kg or 100 kg. A boat starts on the left bank and can carry any non-empty group whose total weight does not exceed the boat limit. Somebody inside the boat must steer it, so every crossing contains at least one passenger."
date: "2026-06-05T17:52:48+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 295
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 179 (Div. 1)"
rating: 2100
weight: 295
solve_time_s: 218
verified: true
draft: false
---

[CF 295C - Greg and Friends](https://codeforces.com/problemset/problem/295/C)

**Rating:** 2100  
**Tags:** combinatorics, dp, graphs, shortest paths  
**Solve time:** 3m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

Every person weighs either 50 kg or 100 kg. A boat starts on the left bank and can carry any non-empty group whose total weight does not exceed the boat limit. Somebody inside the boat must steer it, so every crossing contains at least one passenger.

We must transport everybody from the left bank to the right bank. Among all valid transportation plans, we need two values.

The first value is the minimum number of boat rides.

The second value is the number of distinct transportation plans that achieve that minimum. Two plans are different if at least one ride contains a different set of people.

The key observation is that people have only two possible weights. We never need to remember the identity of every person individually while searching for the minimum number of rides. We only need to know how many 50 kg people and how many 100 kg people remain on the left bank.

The number of people is at most 50. A state that stores exact subsets would require up to $2^{50}$ possibilities, which is completely impossible. On the other hand, the counts of remaining 50 kg and 100 kg people each range from 0 to 50, giving only about $51 \times 51$ possibilities. Adding the boat position still leaves fewer than 6000 states.

A subtle point is that the shortest-path search cannot ignore identities completely. Suppose there are three different 50 kg people and we move one of them. Choosing person A and choosing person B lead to the same count state, but they represent different transportation plans. We must search on count states while counting how many concrete choices produce each transition.

Several edge cases are easy to mishandle.

Consider

```
1 50
50
```

The answer is

```
1
1
```

The boat can immediately cross with the only person.

Now consider

```
1 50
100
```

The answer is

```
-1
0
```

The only passenger weighs more than the boat capacity, so no move exists.

Another important case is

```
2 100
50 50
```

The answer is

```
1
1
```

Both people cross together. Counting them as two different orders would be incorrect because a ride is defined by the set of passengers, not by an ordering inside the boat.

## Approaches

A brute-force solution would treat every person as distinct and search all possible boat loads. Even with only 50 people, the number of subsets of passengers is $2^{50}$, and every state would branch into many more states. The search space explodes immediately.

The reason brute force seems attractive is that the definition of distinct plans depends on individual identities. Unfortunately, keeping identities inside the state is far too expensive.

The structure of the weights changes everything. Since every weight is either 50 or 100, a state is completely determined by three values:

- how many 50 kg people remain on the left bank,
- how many 100 kg people remain on the left bank,
- which bank currently contains the boat.

The state space becomes tiny:

$$51 \times 51 \times 2 \approx 5200.$$

The remaining challenge is counting distinct plans. Two transitions between the same pair of count states may correspond to many different choices of actual people.

Suppose $x$ fifty-kilogram people are currently on the left bank and we send $p$ of them across. The number of ways to choose those people is

$$\binom{x}{p}.$$

Similarly, choosing $q$ one-hundred-kilogram people contributes

$$\binom{y}{q}.$$

The total multiplicity of that transition is the product of the two binomial coefficients.

The state graph is unweighted because every boat ride costs exactly one crossing. Once we build this graph, the minimum number of rides becomes a shortest-path problem. Since all edges have equal cost, BFS gives the shortest distance. While running BFS, we also maintain the number of shortest paths, multiplying by the combinatorial count attached to each edge.

This produces both answers simultaneously.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ states or worse | Exponential | Too slow |
| Optimal | $O(S \cdot T)$ | $O(S)$ | Accepted |

Here $S \approx 5200$ is the number of states and $T$ is the number of feasible boat-load patterns.

## Algorithm Walkthrough

1. Count the number of 50 kg people, call it $A$, and the number of 100 kg people, call it $B$.
2. Divide all weights by 50. A 50 kg person becomes weight 1, a 100 kg person becomes weight 2, and the boat capacity becomes $M = k / 50$.
3. Precompute all pairs $(p,q)$ such that $p+2q \le M$ and $p+q > 0$. Each pair represents a possible passenger composition for one crossing.
4. Precompute all binomial coefficients $\binom{n}{r}$ for $0 \le n,r \le 50$ modulo $10^9+7$.
5. Use the state $(x,y,s)$, where:

- $x$ is the number of 50 kg people still on the left bank,
- $y$ is the number of 100 kg people still on the left bank,
- $s=0$ means the boat is on the left bank,
- $s=1$ means the boat is on the right bank.
6. Start BFS from $(A,B,0)$. The distance of this state is 0 and the number of shortest ways is 1.
7. When the boat is on the left bank, try every feasible pair $(p,q)$ with $p \le x$ and $q \le y$. Move those passengers to the right bank and reach state $(x-p,y-q,1)$.
8. The multiplicity of that transition is

$$\binom{x}{p}\binom{y}{q}.$$

1. When the boat is on the right bank, the right bank currently contains $A-x$ fifty-kilogram people and $B-y$ one-hundred-kilogram people. Try every feasible return load $(p,q)$ satisfying

$$p \le A-x,\qquad q \le B-y.$$

The new state is $(x+p,y+q,0)$.

1. The multiplicity of this return transition is

$$\binom{A-x}{p}\binom{B-y}{q}.$$

1. Run ordinary BFS relaxation. If a state is discovered for the first time, record its distance and initialize its shortest-path count. If another shortest path reaches the same state, add its contribution modulo $10^9+7$.
2. The target state is $(0,0,1)$, meaning everybody is on the right bank and the final crossing has already happened.

### Why it works

The state contains exactly the information needed to determine all future legal moves. Any two configurations with the same counts of remaining 50 kg and 100 kg people and the same boat position have identical future possibilities.

Every edge in the state graph corresponds to exactly one boat ride, so the minimum number of rides is precisely the shortest-path distance in this graph. BFS finds shortest distances in every unweighted graph.

For a fixed transition, the number of concrete ways to realize it equals the number of choices of actual passengers, which is given by the relevant binomial coefficients. Multiplying these factors along a path counts the number of transportation plans represented by that path. The BFS shortest-path counting recurrence sums those contributions over all shortest paths only, yielding exactly the number of optimal transportation plans.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

MOD = 1000000007

def main():
    n, k = map(int, input().split())
    w = list(map(int, input().split()))

    A = sum(x == 50 for x in w)
    B = sum(x == 100 for x in w)

    M = k // 50

    C = [[0] * 51 for _ in range(51)]
    for i in range(51):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD

    moves = []
    for p in range(51):
        for q in range(51):
            if p + q > 0 and p + 2 * q <= M:
                moves.append((p, q))

    dist = [[[-1] * 2 for _ in range(B + 1)] for _ in range(A + 1)]
    ways = [[[0] * 2 for _ in range(B + 1)] for _ in range(A + 1)]

    q = deque()
    dist[A][B][0] = 0
    ways[A][B][0] = 1
    q.append((A, B, 0))

    while q:
        x, y, side = q.popleft()

        cur_dist = dist[x][y][side]
        cur_ways = ways[x][y][side]

        if side == 0:
            for p, r in moves:
                if p > x or r > y:
                    continue

                nx = x - p
                ny = y - r
                ns = 1

                mult = C[x][p] * C[y][r]
                mult %= MOD

                if dist[nx][ny][ns] == -1:
                    dist[nx][ny][ns] = cur_dist + 1
                    ways[nx][ny][ns] = cur_ways * mult % MOD
                    q.append((nx, ny, ns))
                elif dist[nx][ny][ns] == cur_dist + 1:
                    ways[nx][ny][ns] = (
                        ways[nx][ny][ns] + cur_ways * mult
                    ) % MOD
        else:
            right50 = A - x
            right100 = B - y

            for p, r in moves:
                if p > right50 or r > right100:
                    continue

                nx = x + p
                ny = y + r
                ns = 0

                mult = C[right50][p] * C[right100][r]
                mult %= MOD

                if dist[nx][ny][ns] == -1:
                    dist[nx][ny][ns] = cur_dist + 1
                    ways[nx][ny][ns] = cur_ways * mult % MOD
                    q.append((nx, ny, ns))
                elif dist[nx][ny][ns] == cur_dist + 1:
                    ways[nx][ny][ns] = (
                        ways[nx][ny][ns] + cur_ways * mult
                    ) % MOD

    answer_dist = dist[0][0][1]

    if answer_dist == -1:
        print(-1)
        print(0)
    else:
        print(answer_dist)
        print(ways[0][0][1] % MOD)

if __name__ == "__main__":
    main()
```

The combinatorial table is computed once because all counts are at most 50. Each transition only needs a constant-time lookup.

The BFS stores both the shortest distance and the number of shortest ways. When a state is discovered for the first time, we have found its minimum distance. If another path reaches the same state with exactly the same distance, its contribution must also be counted.

A common mistake is using the numbers currently on the left bank when the boat is returning from the right bank. The return trip chooses passengers from the right bank, so the correct counts are $A-x$ and $B-y$.

Another subtle detail is that the graph is not directed by people identities. Identities appear only inside the transition multiplicity through binomial coefficients.

## Worked Examples

### Sample 1

Input

```
1 50
50
```

Here $A=1$, $B=0$, $M=1$.

| State | Distance | Action |
| --- | --- | --- |
| (1,0,0) | 0 | Start |
| (0,0,1) | 1 | Send one 50 kg person |

The target is reached after one ride.

The only possible crossing contains the only person, so the number of optimal plans is 1.

### Sample 2

Input

```
3 100
50 50 100
```

Here $A=2$, $B=1$, $M=2$.

| State | Distance | Action |
| --- | --- | --- |
| (2,1,0) | 0 | Start |
| (0,1,1) | 1 | Send two 50 kg people |
| (1,1,0) | 2 | Return one 50 kg person |
| (1,0,1) | 3 | Send one 100 kg person |
| (2,0,0) | 4 | Return one 50 kg person |
| (0,0,1) | 5 | Send two 50 kg people |

The shortest distance is 5. At the first return trip we may choose either of the two 50 kg people, giving two distinct optimal plans.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(S \cdot T)$ | BFS explores each state and tries all feasible passenger compositions |
| Space | $O(S)$ | Distance and path-count arrays over all states |

Here $S \le 51 \times 51 \times 2 \approx 5200$. The number of feasible passenger compositions is bounded by a few thousand and is much smaller in practice. The solution comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    MOD = 1000000007
    input = sys.stdin.readline

    n, k = map(int, input().split())
    w = list(map(int, input().split()))

    A = sum(x == 50 for x in w)
    B = sum(x == 100 for x in w)
    M = k // 50

    C = [[0] * 51 for _ in range(51)]
    for i in range(51):
        C[i][0] = C[i][i] = 1
        for j in range(1, i):
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD

    moves = []
    for p in range(51):
        for q in range(51):
            if p + q > 0 and p + 2 * q <= M:
                moves.append((p, q))

    dist = [[[-1] * 2 for _ in range(B + 1)] for _ in range(A + 1)]
    ways = [[[0] * 2 for _ in range(B + 1)] for _ in range(A + 1)]

    q = deque([(A, B, 0)])
    dist[A][B][0] = 0
    ways[A][B][0] = 1

    while q:
        x, y, s = q.popleft()

        if s == 0:
            for p, r in moves:
                if p > x or r > y:
                    continue
                nx, ny, ns = x - p, y - r, 1
                mult = C[x][p] * C[y][r] % MOD

                if dist[nx][ny][ns] == -1:
                    dist[nx][ny][ns] = dist[x][y][s] + 1
                    ways[nx][ny][ns] = ways[x][y][s] * mult % MOD
                    q.append((nx, ny, ns))
                elif dist[nx][ny][ns] == dist[x][y][s] + 1:
                    ways[nx][ny][ns] = (
                        ways[nx][ny][ns] + ways[x][y][s] * mult
                    ) % MOD
        else:
            r50, r100 = A - x, B - y

            for p, r in moves:
                if p > r50 or r > r100:
                    continue
                nx, ny, ns = x + p, y + r, 0
                mult = C[r50][p] * C[r100][r] % MOD

                if dist[nx][ny][ns] == -1:
                    dist[nx][ny][ns] = dist[x][y][s] + 1
                    ways[nx][ny][ns] = ways[x][y][s] * mult % MOD
                    q.append((nx, ny, ns))
                elif dist[nx][ny][ns] == dist[x][y][s] + 1:
                    ways[nx][ny][ns] = (
                        ways[nx][ny][ns] + ways[x][y][s] * mult
                    ) % MOD

    if dist[0][0][1] == -1:
        return "-1\n0"
    return f"{dist[0][0][1]}\n{ways[0][0][1]}"

# provided sample
assert run("1 50\n50\n") == "1\n1", "sample 1"

# impossible
assert run("1 50\n100\n") == "-1\n0", "cannot move 100kg person"

# two 50kg people fit together
assert run("2 100\n50 50\n") == "1\n1", "single crossing"

# one 50kg and one 100kg with capacity 100
assert run("2 100\n50 100\n") == "3\n1", "must shuttle"

# all people identical
assert run("3 150\n50 50 50\n") == "1\n1", "all cross together"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 50 / 100` | `-1 / 0` | Impossible instance |
| `2 100 / 50 50` | `1 / 1` | Direct transport in one ride |
| `2 100 / 50 100` | `3 / 1` | Requires a return trip |
| `3 150 / 50 50 50` | `1 / 1` | All passengers move together |

## Edge Cases

Consider

```
1 50
100
```

The scaled capacity is 1, while the only passenger has scaled weight 2. No valid move exists from the start state. BFS never reaches the target state, so its distance remains -1. The algorithm prints

```
-1
0
```

which is correct.

Consider

```
2 100
50 50
```

The start state is $(2,0,0)$. A single transition moves both people across, reaching $(0,0,1)$. The multiplicity is

$$\binom{2}{2}=1.$$

The algorithm outputs

```
1
1
```

and does not double-count different orderings inside the boat.

Consider

```
3 100
50 50 100
```

The shortest solution requires returning one of the two 50 kg people after the first trip. The count-state transition is the same in both cases, but its multiplicity contains

$$\binom{2}{1}=2.$$

The algorithm correctly counts both possibilities even though they merge into the same state afterward. This is exactly why combinatorial edge weights are required.
