---
title: "CF 106157L - Last Orders"
description: "We have a town with one pub at each junction of a road network. Traveling along roads takes time, and every pub has a closing time. We start at pub 1 at time 0. The duration of the drinking sessions is fixed in advance."
date: "2026-06-25T11:20:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106157
codeforces_index: "L"
codeforces_contest_name: "2025 United Kingdom and Ireland Programming Contest (UKIEPC 2025)"
rating: 0
weight: 106157
solve_time_s: 48
verified: true
draft: false
---

[CF 106157L - Last Orders](https://codeforces.com/problemset/problem/106157/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a town with one pub at each junction of a road network. Traveling along roads takes time, and every pub has a closing time. We start at pub 1 at time 0.

The duration of the drinking sessions is fixed in advance. The first pint takes $t_1$ seconds, the second takes $t_2$, and so on up to $t_r$. The durations are not necessarily increasing.

A pint only counts if it is completely finished before the pub where it is being drunk closes. We may move through the road network in any way we like, revisit pubs multiple times, and even pass through pubs without drinking. The only restriction is that two consecutive pints cannot be drunk in the same pub. The goal is to maximize the number of pints consumed.

The limits are small in the number of pints, $r \le 100$, and moderate in the number of pubs, $k \le 300$. The graph can be quite dense with up to 90,000 roads.

A brute force search over all possible pub sequences would be hopeless. Even choosing a pub for each pint already gives roughly $k^r$ possibilities. With $k=300$ and $r=100$, that is astronomically large.

The graph size suggests that computing shortest travel times between every pair of pubs is feasible. Once those shortest paths are known, the actual road structure no longer matters, only the minimum travel time between pubs.

A subtle edge case appears when revisiting a pub. Revisiting is allowed, but only after drinking somewhere else in between.

Example:

```
2
5 5
2
20 20
1
1 2 1
```

The sequence pub 1 → pub 1 is illegal because the same pub is used for consecutive pints. A solution that only checks closing times would incorrectly count two pints.

Another edge case is that the first pint does not need to be drunk at pub 1.

Example:

```
1
10
2
100 15
1
1 2 1
```

Travel to pub 2 takes 1 second, so the first pint finishes at time 11 and is valid. Any solution that forces the first pint to be consumed at pub 1 would miss this possibility.

A third edge case is that the graph may contain multiple roads between the same pair of junctions. Only the shortest travel time matters. Using an arbitrary road instead of the best one can make feasible schedules appear impossible.

## Approaches

The most direct idea is to try every possible pub choice for every pint. If the current pint is drunk in pub $u$, we choose a pub $v \ne u$ for the next one, add the travel time and drinking duration, and check whether the closing time is respected.

This approach is correct because it explicitly enumerates all valid schedules. The problem is the number of possibilities. Even ignoring travel details, there are roughly $k$ choices per pint, producing $k^r$ states. With $k=300$ and $r=100$, this is completely infeasible.

The key observation is that only the earliest possible finishing time matters.

Suppose we have already drunk $j$ pints and the last one was finished in pub $u$. If two different schedules reach the same state $(j,u)$, the schedule with the smaller finishing time is always at least as good as the other. Arriving earlier can never reduce future options because all constraints are upper bounds on time.

This gives a dynamic programming formulation.

Before the DP, we compute all-pairs shortest paths. Any route between two pubs can be replaced by the shortest one, since arriving earlier is always better.

Define:

$$dp[j][u]$$

as the minimum possible absolute time at which the $j$-th pint finishes in pub $u$.

From such a state, the next pint can be drunk in any pub $v \ne u$. The finishing time becomes:

$$dp[j][u] + dist[u][v] + t_{j+1}$$

and the transition is valid only if that finishing time does not exceed $c_v$.

The number of states is only $r \times k$, and each state tries all possible next pubs, giving $O(rk^2)$ transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k^r)$ | $O(r)$ | Too slow |
| Optimal | $O(k^3 + rk^2)$ | $O(rk)$ | Accepted |

## Algorithm Walkthrough

1. Read the drinking durations, pub closing times, and road network.
2. Build a distance matrix initialized to infinity.
3. Set the distance from every pub to itself as 0.
4. For every road, keep the minimum weight between its endpoints. Multiple roads may connect the same pair of pubs.
5. Run Floyd-Warshall to compute the shortest travel time between every pair of pubs.
6. Create a DP table where `dp[j][u]` stores the earliest possible finishing time after drinking exactly `j` pints and ending in pub `u`.
7. Initialize the first pint. For every pub `u`, the first pint can be drunk there if

$$dist[1][u] + t_1 \le c_u$$

When this holds, store that finishing time in `dp[1][u]`.

1. For every number of consumed pints `j` from 1 to `r-1`, process all reachable ending pubs `u`.
2. For every destination pub `v` different from `u`, compute

$$finish = dp[j][u] + dist[u][v] + t_{j+1}$$

If `finish <= c[v]`, update

$$dp[j+1][v]$$

with the minimum finishing time found so far.

1. The answer is the largest `j` for which some state `dp[j][u]` is reachable.

### Why it works

The DP state records the earliest achievable finishing time for a fixed pair consisting of the number of pints consumed and the pub where the last pint was drunk.

Any future decision depends only on those two pieces of information. Earlier completion is always at least as good as later completion because all constraints are deadlines. Replacing a schedule by another schedule that reaches the same state earlier cannot invalidate any future sequence of moves.

Floyd-Warshall guarantees that `dist[u][v]` is the minimum possible travel time between pubs. Any schedule using a longer route can only finish later, so considering shortest paths is sufficient.

Since every valid sequence of pubs corresponds to a sequence of DP transitions, and every DP transition represents a valid action sequence, the DP explores exactly all feasible schedules. The largest reachable pint count is the optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

r = int(input())
t = list(map(int, input().split()))

k = int(input())
c = list(map(int, input().split()))

m = int(input())

dist = [[INF] * k for _ in range(k)]

for i in range(k):
    dist[i][i] = 0

for _ in range(m):
    a, b, d = map(int, input().split())
    a -= 1
    b -= 1
    if d < dist[a][b]:
        dist[a][b] = d
        dist[b][a] = d

for mid in range(k):
    dm = dist[mid]
    for i in range(k):
        if dist[i][mid] == INF:
            continue
        via = dist[i][mid]
        di = dist[i]
        for j in range(k):
            nd = via + dm[j]
            if nd < di[j]:
                di[j] = nd

dp = [[INF] * k for _ in range(r + 1)]

start = 0

for u in range(k):
    if dist[start][u] == INF:
        continue
    finish = dist[start][u] + t[0]
    if finish <= c[u]:
        dp[1][u] = finish

answer = 0

for u in range(k):
    if dp[1][u] < INF:
        answer = 1

for drank in range(1, r):
    for u in range(k):
        cur = dp[drank][u]
        if cur == INF:
            continue

        for v in range(k):
            if v == u:
                continue
            if dist[u][v] == INF:
                continue

            finish = cur + dist[u][v] + t[drank]

            if finish <= c[v] and finish < dp[drank + 1][v]:
                dp[drank + 1][v] = finish
                answer = max(answer, drank + 1)

print(answer)
```

The first part constructs the shortest-path matrix. Multiple roads between the same pair of pubs are handled by keeping only the minimum edge weight.

The Floyd-Warshall implementation updates the matrix in place. Since $k \le 300$, the $O(k^3)$ complexity is acceptable.

The DP table stores earliest finishing times rather than boolean reachability. This is the crucial optimization. If two schedules end at the same pub after the same number of pints, only the earlier one matters.

The first pint requires special handling because there is no previous pub. We simply travel from pub 1 to the chosen pub and spend $t_1$ seconds drinking there.

The transition skips `v == u`, enforcing the rule that consecutive pints cannot be consumed in the same pub.

## Worked Examples

### Example 1

```
2
5 5
2
10 20
1
1 2 2
```

Shortest distances:

| From | To 1 | To 2 |
| --- | --- | --- |
| 1 | 0 | 2 |
| 2 | 2 | 0 |

Initialization:

| Pub | Finish first pint | Valid |
| --- | --- | --- |
| 1 | 5 | Yes |
| 2 | 7 | Yes |

DP transitions:

| Pints | Current Pub | Time | Next Pub | New Time |
| --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 2 | 12 |
| 1 | 2 | 7 | 1 | 14 |

Only the first transition respects the closing time of pub 2.

Answer: `2`.

This trace shows why we store the earliest finishing time. Ending the first pint in pub 1 is better than ending it in pub 2 because it leaves more time for future actions.

### Example 2

```
3
4 4 4
3
5 20 20
2
1 2 1
2 3 1
```

Initialization:

| Pub | Finish first pint |
| --- | --- |
| 1 | 4 |
| 2 | 5 |
| 3 | 6 |

After one pint:

| Pints | Pub | Time |
| --- | --- | --- |
| 1 | 1 | 4 |
| 1 | 2 | 5 |
| 1 | 3 | 6 |

After two pints:

| Pints | Pub | Best Time |
| --- | --- | --- |
| 2 | 2 | 9 |
| 2 | 3 | 10 |

After three pints:

| Pints | Pub | Best Time |
| --- | --- | --- |
| 3 | 3 | 14 |

Answer: `3`.

This example demonstrates that revisiting and moving through intermediate pubs is naturally handled by shortest-path distances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k^3 + rk^2)$ | Floyd-Warshall plus DP transitions |
| Space | $O(rk + k^2)$ | DP table and distance matrix |

With $k \le 300$ and $r \le 100$, the Floyd-Warshall phase performs about 27 million updates and the DP performs about 9 million transitions, both comfortably within typical contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    INF = 10**18

    r = int(input())
    t = list(map(int, input().split()))

    k = int(input())
    c = list(map(int, input().split()))

    m = int(input())

    dist = [[INF] * k for _ in range(k)]
    for i in range(k):
        dist[i][i] = 0

    for _ in range(m):
        a, b, d = map(int, input().split())
        a -= 1
        b -= 1
        dist[a][b] = min(dist[a][b], d)
        dist[b][a] = min(dist[b][a], d)

    for mid in range(k):
        for i in range(k):
            for j in range(k):
                dist[i][j] = min(
                    dist[i][j],
                    dist[i][mid] + dist[mid][j]
                )

    dp = [[INF] * k for _ in range(r + 1)]

    for u in range(k):
        finish = dist[0][u] + t[0]
        if finish <= c[u]:
            dp[1][u] = finish

    ans = 0
    for u in range(k):
        if dp[1][u] < INF:
            ans = 1

    for drank in range(1, r):
        for u in range(k):
            if dp[drank][u] == INF:
                continue
            for v in range(k):
                if v == u:
                    continue
                finish = dp[drank][u] + dist[u][v] + t[drank]
                if finish <= c[v]:
                    dp[drank + 1][v] = min(
                        dp[drank + 1][v],
                        finish
                    )
                    ans = max(ans, drank + 1)

    return str(ans) + "\n"

# minimum size
assert run("""1
5
1
5
1
1 1 1
""") == "1\n"

# cannot drink any pint
assert run("""1
10
1
5
1
1 1 1
""") == "0\n"

# alternating between two pubs
assert run("""2
5 5
2
10 20
1
1 2 2
""") == "2\n"

# revisiting allowed, consecutive not allowed
assert run("""3
1 1 1
2
100 100
1
1 2 1
""") == "3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single pub, one feasible pint | 1 | Minimum-size valid instance |
| Single pub, deadline already missed | 0 | No reachable state |
| Two pubs with one transition | 2 | Basic DP transition |
| Alternating between two pubs repeatedly | 3 | Revisiting is allowed |

## Edge Cases

Consider the case where the same pub would be used twice consecutively:

```
2
1 1
1
100
1
1 1 1
```

After the first pint, the only pub is still pub 1. The transition loop rejects `v == u`, so no second pint is generated. The answer remains 1.

Consider the case where the first pint is not drunk in pub 1:

```
1
10
2
100 15
1
1 2 1
```

The initialization checks every pub. For pub 2, the finish time is `1 + 10 = 11`, which satisfies the closing time. The state `dp[1][2] = 11` is created, giving the correct answer of 1.

Consider multiple roads between the same pubs:

```
1
5
2
100 100
2
1 2 100
1 2 1
```

The algorithm stores the minimum edge weight, namely 1. The shortest-path matrix then correctly records a travel time of 1 rather than 100. Any implementation that ignored parallel edges could incorrectly eliminate feasible schedules.
