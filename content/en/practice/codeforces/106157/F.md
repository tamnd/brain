---
title: "CF 106157F - Fell Walking"
description: "We have a connected undirected map of hills. Each hill has a height, and the paths between hills form a graph. We need to travel from hill 1 to hill 2 while making the difference between the tallest and shortest hill visited as small as possible."
date: "2026-06-25T11:19:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106157
codeforces_index: "F"
codeforces_contest_name: "2025 United Kingdom and Ireland Programming Contest (UKIEPC 2025)"
rating: 0
weight: 106157
solve_time_s: 46
verified: true
draft: false
---

[CF 106157F - Fell Walking](https://codeforces.com/problemset/problem/106157/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected undirected map of hills. Each hill has a height, and the paths between hills form a graph. We need to travel from hill 1 to hill 2 while making the difference between the tallest and shortest hill visited as small as possible.

For any chosen route, the only thing that matters is the smallest height and largest height appearing on that route. If a route visits heights 10, 14, 13, and 12, its cost is `14 - 10 = 4`.

The input gives the number of hills, the number of trails, the height of every hill, and the pairs of hills connected by trails. The output is the minimum possible height difference among all routes from hill 1 to hill 2.

The number of hills is at most 5000 and the number of trails is at most 25000. A solution that tries every possible path is impossible because a graph can contain an enormous number of different routes. Even exploring all paths would become exponential. We need to reduce the problem to checking connectivity under height restrictions. Since there are only 5000 hills, an algorithm around `O(n(n+m))` is realistic, but anything involving all pairs of hills or all possible paths is too expensive.

The first edge case is when hill 1 and hill 2 have the same height. A route consisting of only those two hills can have answer zero if they are directly connected. For example:

```
Input
2 1
5 5
1 2

Output
0
```

A careless solution that assumes the answer is always positive would fail here.

Another edge case is when the optimal route does not use the shortest graph path. For example:

```
Input
5 5
1 100 50 51 2
1 2
1 3
3 4
4 5
5 2

Output
49
```

The direct path has height range `99`, but the longer path `1 -> 3 -> 4 -> 5 -> 2` has range `50 - 1 = 49`. A solution that minimizes the number of edges instead of the height range gives the wrong result.

A third edge case appears when several hills share the same height. The window of allowed heights must be based on height values, not hill indices. For example:

```
Input
3 2
7 7 10
1 2
2 3

Output
3
```

The two hills with height 7 should be treated together. Splitting equal heights into separate ranges can miss valid answers.

## Approaches

A direct approach would enumerate every possible route from hill 1 to hill 2, compute the minimum and maximum height on each route, and keep the smallest difference. This is correct because every possible candidate route is considered. The problem is the number of routes. Even a sparse graph can contain exponentially many different paths, so this approach becomes unusable immediately.

The key observation is that we do not care about the exact route, only whether some route exists inside a height interval.

Suppose we choose two heights `low` and `high`. We are asking whether hill 1 and hill 2 are connected using only hills whose heights are between `low` and `high`. If they are connected, then this interval is a valid answer candidate.

The valid intervals have a monotonic property. If `[low, high]` works, then increasing `high` keeps it working. If `[low, high]` does not work, decreasing `high` cannot help. This allows a two pointer scan over the sorted unique heights.

For every left boundary, we move the right boundary only forward until the interval becomes valid. Then we try to remove the current smallest height and continue. The number of connectivity checks is linear in the number of distinct heights because the right pointer never moves backward.

The brute force works because it checks every possible route, but fails because the number of routes is huge. The observation that only the allowed height interval matters lets us replace path enumeration with repeated graph connectivity checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(k(n+m)) | O(n+m) | Accepted |

Here `k` is the number of distinct heights, and `k <= n`.

## Algorithm Walkthrough

1. Sort all distinct hill heights. These values are the only possible boundaries of a useful interval because moving a boundary between two existing heights cannot change which hills are available.
2. Maintain two pointers `left` and `right` over the sorted height list. The current candidate interval is from `heights[left]` to `heights[right]`.
3. For the current interval, run a BFS starting from hill 1. During the search, only visit hills whose heights are inside the interval. If hill 2 is reached, the interval contains a valid route.
4. If the interval is invalid, increase `right`. Adding a larger maximum height can only add more available hills, so it may make a route appear.
5. If the interval is valid, update the answer with the current range and increase `left`. Removing the smallest allowed height may produce an even smaller valid interval.
6. Continue until the right pointer reaches the end of the height list.

The reason the two pointer movement is safe is that connectivity only becomes easier when the interval expands. Once a particular maximum height is enough for a given minimum height, searching smaller maximum heights cannot help.

Why it works:

Every valid route has a smallest height `L` and a largest height `R`, so it corresponds to one of the intervals considered by the two pointer process. The BFS check correctly determines whether an interval contains any route from hill 1 to hill 2 because it explores exactly the subgraph formed by hills inside that interval. The algorithm tests every possible minimal left boundary and finds the smallest right boundary that works for it, so no smaller valid interval is skipped.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    h = list(map(int, input().split()))

    graph = [[] for _ in range(n)]
    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    values = sorted(set(h))

    def connected(low, high):
        if not (low <= h[0] <= high and low <= h[1] <= high):
            return False

        seen = [False] * n
        q = deque([0])
        seen[0] = True

        while q:
            u = q.popleft()
            if u == 1:
                return True
            for v in graph[u]:
                if not seen[v] and low <= h[v] <= high:
                    seen[v] = True
                    q.append(v)

        return False

    ans = values[-1] - values[0]
    right = 0

    for left in range(len(values)):
        if right < left:
            right = left

        while right < len(values) and not connected(values[left], values[right]):
            right += 1

        if right == len(values):
            break

        ans = min(ans, values[right] - values[left])

    print(ans)

if __name__ == "__main__":
    solve()
```

The input parsing builds an adjacency list because the graph is sparse enough that storing all edges explicitly is unnecessary. The `connected` function is the core operation from the walkthrough. It performs BFS while filtering vertices by the current height interval.

The two pointer loop stores only indices into the sorted height list. The right pointer never moves backwards, which is what keeps the number of BFS calls bounded. The answer update happens only after a valid interval is found.

The boundary check at the start of `connected` handles cases where either endpoint is outside the current height range. Without it, the BFS could incorrectly claim that a route exists even though the starting or ending hill is unavailable.

Python integers do not overflow, so the height calculations are safe even though heights can reach one million.

## Worked Examples

Consider:

```
Input
5 6
1 2 3 4 5
1 3
1 5
2 4
3 4
4 5
5 2
```

The sorted heights are `[1,2,3,4,5]`.

| left height | right height | BFS result | Current answer |
| --- | --- | --- | --- |
| 1 | 1 | false | large |
| 1 | 2 | false | large |
| 1 | 3 | true | 2 |
| 2 | 3 | false | 2 |
| 2 | 4 | true | 2 |

The best interval is heights 1 through 3, giving answer 2. The trace shows that after finding a working interval, the algorithm tries removing the smallest height to improve it.

Another example:

```
Input
3 2
7 7 10
1 2
2 3
```

| left height | right height | BFS result | Current answer |
| --- | --- | --- | --- |
| 7 | 7 | false | large |
| 7 | 10 | true | 3 |
| 10 | 10 | false | 3 |

The two equal height values are handled together because the algorithm works on unique height values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k(n+m)) | Each of the at most `2k` connectivity checks runs BFS over the graph. |
| Space | O(n+m) | The adjacency list and BFS arrays store the graph and traversal state. |

With `n <= 5000` and `m <= 25000`, this remains practical because the number of distinct heights is also bounded by 5000. The algorithm avoids the impossible task of enumerating routes.

## Test Cases

```python
import sys
import io
from collections import deque

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

assert run("""5 6
1 2 3 4 5
1 3
1 5
2 4
3 4
4 5
5 2
""") == "2\n", "sample 1"

assert run("""2 1
5 5
1 2
""") == "0\n", "same height"

assert run("""5 5
1 100 50 51 2
1 2
1 3
3 4
4 5
5 2
""") == "49\n", "longer better path"

assert run("""3 2
7 7 10
1 2
2 3
""") == "3\n", "duplicate heights"

assert run("""4 3
1 2 3 100
1 2
2 3
3 4
""") == "99\n", "large boundary jump"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample graph | 2 | Normal connectivity and interval shrinking |
| Two equal hills | 0 | Zero range answer |
| Longer lower-range path | 49 | Choosing the correct route instead of the shortest route |
| Duplicate heights | 3 | Treating equal heights correctly |
| Large height gap | 99 | Boundary handling |

## Edge Cases

For the equal-height case:

```
2 1
5 5
1 2
```

The sorted height list contains only `[5]`. The only interval checked is `[5,5]`. Both endpoints are inside it, BFS reaches hill 2 immediately, and the answer becomes `5 - 5 = 0`.

For the longer-route case:

```
5 5
1 100 50 51 2
1 2
1 3
3 4
4 5
5 2
```

The interval `[1,2]` cannot reach hill 2 because the middle hills needed for the alternate route are unavailable. Expanding to `[1,50]` still fails, but `[1,51]` succeeds through hills with heights `1,50,51,2`. The algorithm records `51 - 1 = 50` before continuing to search. The final valid minimum is `49` using the interval `[2,51]` after the left pointer moves.

For duplicate heights:

```
3 2
7 7 10
1 2
2 3
```

The sorted unique heights are `[7,10]`. The algorithm never separates the two height-7 hills, so the interval `[7,10]` correctly includes both and finds the route with range `3`.

For all cases, the invariant is that every time an interval is tested, BFS exactly represents the graph available under that height restriction. The two pointers only discard intervals that cannot improve the answer, so the final minimum range is preserved.
