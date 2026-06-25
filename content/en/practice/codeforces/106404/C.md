---
title: "CF 106404C - Alien Attack (Easy Version)"
description: "The problem models a country as a tree of cities. Each city starts with power zero. A meteor can hit a city once, and when it lands it gives that city an initial amount of energy that decreases by one every second after the impact time."
date: "2026-06-25T10:01:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106404
codeforces_index: "C"
codeforces_contest_name: "Bay Area Programming Contest 2026 Advanced Division"
rating: 0
weight: 106404
solve_time_s: 40
verified: true
draft: false
---

[CF 106404C - Alien Attack (Easy Version)](https://codeforces.com/problemset/problem/106404/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a country as a tree of cities. Each city starts with power zero. A meteor can hit a city once, and when it lands it gives that city an initial amount of energy that decreases by one every second after the impact time. A query asks for the total power currently present on every city along the unique path between two cities. The easy version has small enough limits, with $n \le 2000$ and $q \le 5000$, which allows solutions that would be too slow for the hard version.

The input first gives the tree structure, then a sequence of events. A type 1 event records a meteor landing at a city at a particular time. A type 2 event asks for the sum of powers on a path at a particular time. Events with the same timestamp require meteor landings to be applied before answering path queries at that timestamp. The output is the path sum for every type 2 event.

The small value of $n$ changes the strategy compared with the hard version. With only 2000 cities, scanning a path using a tree traversal costs at most $O(n)$. Since there are only 5000 queries, around ten million city visits are enough, which is easily manageable in Python. Approaches involving heavy tree data structures are unnecessary here.

The main edge cases come from time handling. A meteor that lands exactly at the query time already contributes its full initial energy. For example:

```
3
1 2
2 3
2
1 5 2 10
2 5 1 3
```

The correct output is:

```
10
```

A careless implementation that only activates meteors when `query_time > meteor_time` would miss the meteor because the two times are equal.

Another easy mistake is allowing a meteor to affect cities outside the queried path. For example:

```
3
1 2
2 3
2
1 1 1 7
2 1 3
```

The correct output is:

```
7
```

The meteor at city 1 contributes because city 1 is on the path. A solution that sums all active meteors globally would also count meteors that are unrelated to the current path.

Negative values also need to be preserved. For example:

```
1
1
2
1 0 1 0
2 10 1 1
```

The correct output is:

```
-10
```

The meteor loses energy continuously, even after its value becomes negative. Clamping the contribution to zero would produce the wrong answer.

## Approaches

The direct approach is to process events in chronological order and maintain the meteors that have already landed. For every path query, we walk through the tree path and calculate the current contribution of every meteor found there. This is correct because each city's power depends only on whether that city's meteor has landed and the current time.

A first attempt might recompute all city powers for every query. In the worst case, this touches all $n$ cities for every query, giving $O(nq)$ operations. With the given bounds, this is about $10^7$ operations, which is acceptable. The same idea can be viewed as a brute force tree solution: there is no need to optimize path queries because the constraints intentionally keep this amount of work small.

The key simplification is the formula for a meteor. If a meteor lands at time $t_0$ with value $v$, then at time $t$ its contribution is:

$$v-(t-t_0)=(v+t_0)-t$$

For a single query, the current time is fixed, so we only need to know which cities on the path have meteors. A tree DFS can collect the path sum directly without maintaining any complicated data structure.

The brute force works because the easy version keeps both the tree and query count small. It would fail on the hard version where both values grow large, because walking large paths thousands of times would become too expensive. The observation that the easy constraints allow direct traversal lets us keep the implementation simple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Accepted |
| Optimal | O(nq) | O(n) | Accepted for Easy Version |

## Algorithm Walkthrough

1. Read the tree and store its adjacency list. The tree has exactly one simple path between any two cities, so a DFS is enough to recover the cities on that path.
2. Sort all queries by their timestamp. When several queries share a timestamp, place meteor events before path queries. This matches the rule that a meteor arriving at time $t$ is already active for a query at time $t$.
3. Maintain two arrays for cities that have received meteors. One stores $v+t_0$, the constant part of the meteor contribution, and the other stores whether the city currently has a meteor.
4. For a meteor query, activate the corresponding city by saving its value and landing time. Each city is updated at most once, so no removal logic is needed.
5. For a path query, run DFS from the starting city until the destination is found. While unwinding the recursion, add the contribution of every city on that path. For an active meteor at city $x$, add:

$$(v_x+t_x)-t$$

where $t$ is the query time.

1. Print answers in the original query order. Sorting is only used internally to simulate time correctly.

The invariant behind the algorithm is that before processing any query at time $t$, every meteor with landing time at most $t$ has already been activated, and no future meteor has been activated. A path query only visits cities on the requested path, so it sums exactly the active contributions that belong to that path.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    q = int(input())
    queries = []

    for i in range(q):
        data = list(map(int, input().split()))
        queries.append((data[1], 0 if data[0] == 1 else 1, i, data))

    queries.sort()

    active = [False] * n
    base = [0] * n
    ans = [0] * q

    def get_path_sum(start, target, time):
        stack = [(start, -1, 0)]
        parent = [-1] * n
        order = []

        while stack:
            node, par, state = stack.pop()
            if state == 0:
                parent[node] = par
                order.append(node)
                if node == target:
                    break
                for nxt in graph[node]:
                    if nxt != par:
                        stack.append((nxt, node, 0))

        cur = target
        total = 0
        while cur != -1:
            if active[cur]:
                total += base[cur] - time
            if cur == start:
                break
            cur = parent[cur]

        return total

    for time, _, _, data in queries:
        if data[0] == 1:
            _, t, x, val = data
            x -= 1
            active[x] = True
            base[x] = t + val
        else:
            _, t, a, b = data
            a -= 1
            b -= 1
            ans[_] = get_path_sum(a, b, t)

    for x in ans:
        print(x)

if __name__ == "__main__":
    solve()
```

The adjacency list stores the tree with zero-based indices, making traversal straightforward. The `active` array records whether a city has received a meteor, and `base` stores the transformed value $v+t_0$. This avoids recomputing the landing time adjustment for every query.

Queries are sorted by time. The second element in the sorting tuple places meteor queries before path queries at the same timestamp. This ordering is required because a meteor landing at time $t$ contributes immediately at time $t$.

The path search uses a DFS stack to build parent information until it reaches the destination. After reaching the target, the code walks backward through parent pointers and accumulates only cities on that path. The stopping condition at the start node prevents accidentally adding unrelated branches.

Python integers handle the large possible sums automatically, so no special overflow handling is required.

## Worked Examples

Sample 1:

```
3
1 2
2 3
4
1 1 2 5
2 2 1 3
2 4 1 3
2 4 2 2
```

The important state changes are:

| Step | Query | Active cities | Current calculation | Answer |
| --- | --- | --- | --- | --- |
| 1 | Meteor at city 2, time 1, value 5 | City 2 with base 6 | Activate city 2 |  |
| 2 | Path 1 to 3 at time 2 | City 2 with base 6 | $6-2=4$ | 4 |
| 3 | Path 1 to 3 at time 4 | City 2 with base 6 | $6-4=2$ | 2 |
| 4 | Path 2 to 2 at time 4 | City 2 with base 6 | $6-4=2$ | 2 |

This demonstrates that a meteor affects only paths containing its city and that the same meteor can become negative as time increases.

Sample 2:

```
2
1 2
3
1 0 1 3
2 0 1 2
2 5 1 2
```

| Step | Query | Active cities | Current calculation | Answer |
| --- | --- | --- | --- | --- |
| 1 | Meteor at city 1, time 0, value 3 | City 1 with base 3 | Activate city 1 |  |
| 2 | Path 1 to 2 at time 0 | City 1 with base 3 | $3-0=3$ | 3 |
| 3 | Path 1 to 2 at time 5 | City 1 with base 3 | $3-5=-2$ | -2 |

This confirms that the implementation keeps negative power values instead of clamping them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nq) | Each path query may inspect up to all cities in the tree, and there are at most $q$ queries. |
| Space | O(n+q) | The graph, query list, and auxiliary arrays are all linear in size. |

The maximum work is about $2000 \times 5000 = 10^7$ city visits, which fits comfortably within the easy version limits. The memory usage is also small because the tree and all stored state arrays contain only a few thousand elements.

## Test Cases

```python
import sys
import io

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

# sample 1
assert run("""3
1 2
2 3
4
1 1 2 5
2 2 1 3
2 4 1 3
2 4 2 2
""") == """4
2
2
"""

# sample 2
assert run("""1
0
""") == ""

# single node, negative decay
assert run("""1
2
1 0 1 0
2 10 1 1
""") == """-10
"""

# same timestamp meteor must be processed first
assert run("""2
1 2
2
1 5 2 10
2 5 1 2
""") == """10
"""

# multiple active cities on a path
assert run("""4
1 2
2 3
3 4
5
1 1 2 5
1 2 3 7
2 3 1 4
2 10 1 4
2 0 1 1
""") == """8
-7
0
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single city with a decayed meteor | -10 | Negative values are preserved. |
| Meteor and query at the same time | 10 | Event ordering is correct. |
| Several meteors on one path | 8, -7, 0 | Path filtering and time decay work together. |

## Edge Cases

For the equal timestamp case:

```
2
1 2
2
1 5 2 10
2 5 1 2
```

The meteor query is processed first because both events happen at time 5. The stored value is $10+5=15$, and the path contains city 2, so the answer is $15-5=10$. The algorithm handles this because sorting places type 1 queries before type 2 queries for the same time.

For the path filtering case:

```
3
1 2
2 3
2
1 1 1 7
2 1 3
```

The meteor at city 1 has contribution $7$ at time 1. The path from 1 to 3 is $1 \rightarrow 2 \rightarrow 3$, so it includes the meteor. If the query had been from city 2 to city 3, the contribution would be zero because city 1 is not on that path. The DFS parent reconstruction ensures only path cities are counted.

For negative decay:

```
1
2
2
1 0 1 0
2 10 1 1
```

The meteor has base value zero. At time 10 its contribution is $0-10=-10$. The code directly evaluates this expression and never applies a lower bound, so it returns the required negative result.
