---
title: "CF 102756H - Voyager"
description: "The problem models a voyage between islands. Each island has a position on a 2D plane and a number of supplies. The starting island is the first one, and the destination is the last one."
date: "2026-07-29T00:32:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102756
codeforces_index: "H"
codeforces_contest_name: "UTPC Contest 10-09-20 Div. 1"
rating: 0
weight: 102756
solve_time_s: 66
verified: true
draft: false
---

[CF 102756H - Voyager](https://codeforces.com/problemset/problem/102756/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a voyage between islands. Each island has a position on a 2D plane and a number of supplies. The starting island is the first one, and the destination is the last one. Kiana's boat has an initial travel capacity equal to the supplies already used on the starting island. Whenever she reaches another island, she collects its supplies, increasing the maximum distance she can travel in one trip.

The task is to decide whether there exists a sequence of islands that allows her to eventually reach the destination. Movement is not restricted to a path already drawn between islands. An island can be visited whenever its Euclidean distance from the island Kiana is currently on is at most the boat's current capacity.

The number of islands is less than 1000. This immediately rules out exploring every possible route, because the number of possible island orders can be enormous. A quadratic solution is acceptable because 1000 squared is only one million operations, which is small for a one second limit.

The main edge cases come from treating the problem like a normal graph search. The graph itself depends on the amount of supplies collected so far, so building edges once at the beginning can give incorrect results. For example:

```
3
0 0 5
4 0 10
10 0 0
```

The correct output is:

```
YES
```

The first island can reach the second island because the distance is 4. After collecting 10 more supplies, the capacity becomes 15 and the destination is reachable. A careless implementation that only considers the initial capacity would incorrectly reject the route.

Another edge case is a chain where islands with zero supplies are still necessary.

```
3
0 0 3
3 0 0
6 0 0
```

The correct output is:

```
YES
```

The first jump is exactly possible, and the second jump is possible with the same capacity. An implementation that only considers islands that increase the range would miss valid paths.

A third common mistake is ignoring the starting island's supplies or adding them twice.

```
2
0 0 5
5 0 0
```

The correct output is:

```
YES
```

The destination is exactly at the initial limit. The starting supplies are already active and must be counted once.

## Approaches

A direct brute-force approach would try every possible route from the starting island. For every current island, it would try all unused islands and recursively continue whenever the distance is reachable. This is correct because it examines every possible sequence of visits, but the number of routes grows factorially. With nearly 1000 islands, even considering a tiny fraction of all possible paths is impossible.

A more useful way to look at the problem is to stop caring about the exact order of islands that have already been collected. At any moment, the only information that affects future moves is the current set of reachable islands and the total supplies collected from them. Since supplies are never removed, every newly reached island can only make future moves easier.

This gives a greedy expansion process. Start with the first island visited and repeatedly collect every island that is currently reachable. Each collected island increases the capacity, which may reveal more reachable islands. The process ends when either the destination is collected or no new island can be reached.

The reason we do not need to choose a special island first is that visiting any currently reachable island cannot hurt. It only adds supplies and never decreases the set of possible future moves. Delaying a reachable island gives no advantage because the same island will still be available later with the same or a larger capacity.

The implementation keeps the minimum distance from every unvisited island to any visited island. Whenever that minimum distance is at most the current capacity, the island can be added.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N!) in the worst case | O(N) recursion stack | Too slow |
| Optimal | O(N²) | O(N²) | Accepted |

## Algorithm Walkthrough

1. Read all islands and precompute the squared distance between every pair of islands. Squared distances avoid floating point errors while comparing with the boat capacity.
2. Mark the starting island as visited and set the current capacity to its supplies. The starting supplies are already installed in the boat.
3. Repeatedly scan every unvisited island. If there exists a visited island whose distance is within the current capacity, mark that island as visited and add its supplies to the capacity.
4. Continue expanding until no new island can be added or the destination becomes visited.
5. Output `YES` if the destination was reached, otherwise output `NO`.

The reason this greedy expansion is valid is that the visited islands form the largest set that can be reached with the current amount of collected supplies. If an island is reachable at some point, collecting it earlier only increases the available capacity. The algorithm never skips a possible improvement, so when it stops, every unvisited island is genuinely unreachable.

Why it works:

Maintain the invariant that every visited island is reachable using exactly the islands already marked as visited. The algorithm only adds an island after verifying that a boat trip to it is possible, so the invariant remains true. When an island is added, its supplies increase the capacity, meaning every move that was possible before remains possible. If the destination is never added, the final scan proves that no unvisited island can be reached from the current reachable region, so no continuation exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)

    islands = []
    for _ in range(n):
        x, y, s = map(int, input().split())
        islands.append((x, y, s))

    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        xi, yi, _ = islands[i]
        for j in range(i + 1, n):
            xj, yj, _ = islands[j]
            d = (xi - xj) ** 2 + (yi - yj) ** 2
            dist[i][j] = d
            dist[j][i] = d

    visited = [False] * n
    visited[0] = True
    capacity = islands[0][2]
    remaining = n - 1

    while remaining:
        changed = False
        for i in range(1, n):
            if visited[i]:
                continue
            reachable = False
            for j in range(n):
                if visited[j] and dist[i][j] <= capacity * capacity:
                    reachable = True
                    break
            if reachable:
                visited[i] = True
                capacity += islands[i][2]
                remaining -= 1
                changed = True

        if visited[n - 1]:
            print("YES")
            return
        if not changed:
            break

    print("YES" if visited[n - 1] else "NO")

if __name__ == "__main__":
    solve()
```

The first part computes squared distances. Using squared values avoids calling square roots repeatedly and avoids precision problems when a distance is exactly on the boundary.

The visited array represents the islands whose supplies have already been collected. The capacity variable is the total number of miles the boat can currently travel in one continuous trip.

The main loop performs the greedy expansion. Each pass tries to find islands that can be reached from the current visited region. When an island is added, its supplies immediately affect later checks in the same pass or future passes.

The comparison uses `dist[i][j] <= capacity * capacity` because `dist` stores squared distances. The equality case is included because reaching an island exactly at the boat's limit is allowed.

## Worked Examples

Using the sample:

```
7
50 50 3
50 52 0
50 55 0
50 58 10
50 49 1
50 35 10
74 50 0
```

| Step | Visited islands | Capacity | Action |
| --- | --- | --- | --- |
| 0 | {0} | 3 | Start |
| 1 | {0,1,4} | 4 | Reach islands within distance 3 |
| 2 | {0,1,2,4} | 4 | Reach island 2 through expansion |
| 3 | {0,1,2,3,4} | 14 | Collect supplies from island 3 |
| 4 | {0,1,2,3,4,5} | 24 | Collect supplies from island 5 |
| 5 | {0,1,2,3,4,5,6} | 24 | Destination reached |

The trace shows why zero-supply islands still matter. Islands 1 and 2 increase the set of reachable positions even though they do not improve the capacity.

A small chain example:

```
3
0 0 3
3 0 0
6 0 0
```

| Step | Visited islands | Capacity | Action |
| --- | --- | --- | --- |
| 0 | {0} | 3 | Start |
| 1 | {0,1} | 3 | Island 1 is exactly reachable |
| 2 | {0,1,2} | 3 | Destination is exactly reachable |

This confirms that boundary distances are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N²) | Each expansion checks pairs of islands, and there are at most N successful additions. |
| Space | O(N²) | The distance matrix stores every pair of islands. |

With fewer than 1000 islands, the distance matrix contains about one million entries, which fits comfortably in memory. The quadratic scanning is also small enough for the given limits.

## Test Cases

```python
import io
import sys

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""7
50 50 3
50 52 0
50 55 0
50 58 10
50 49 1
50 35 10
74 50 0
""") == "YES\n", "sample 1"

assert run("""3
0 0 3
3 0 0
6 0 0
""") == "YES\n", "zero supply chain"

assert run("""2
0 0 1
5 0 0
""") == "NO\n", "unreachable destination"

assert run("""2
0 0 5
5 0 0
""") == "YES\n", "exact boundary distance"

assert run("""4
0 0 0
1 0 0
2 0 0
3 0 0
""") == "NO\n", "no initial movement"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample case | YES | Normal multi-island expansion |
| Zero supply chain | YES | Islands without supplies still matter |
| Destination too far | NO | Correct stopping condition |
| Exact distance match | YES | Boundary comparison |
| No initial movement | NO | Starting capacity handling |

## Edge Cases

For the zero-supply chain:

```
3
0 0 3
3 0 0
6 0 0
```

The algorithm begins with capacity 3. Island 1 is added because its squared distance is 9, equal to the squared capacity. The capacity remains 3, but island 1 is now a new position from which island 2 is also at distance 3. The destination is reached.

For the case where new supplies unlock a distant island:

```
3
0 0 5
4 0 10
15 0 0
```

The first island can reach the second island. After collecting 10 supplies, the capacity becomes 15, allowing the destination to be reached. The algorithm finds this because the newly visited island is immediately included in later reachability checks.

For exact boundary movement:

```
2
0 0 5
5 0 0
```

The squared distance is 25 and the squared capacity is also 25. The comparison uses `<=`, so the island is correctly considered reachable. A strict comparison would produce the wrong answer.
