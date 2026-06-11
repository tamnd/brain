---
title: "CF 1361A - Johnny and Contribution"
description: "We are given an undirected graph. Each vertex represents a blog, and every blog has a desired topic number t[i]. Johnny writes blogs one by one. When he writes a blog, he looks only at neighbors that have already been written."
date: "2026-06-11T12:47:51+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1361
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 647 (Div. 1) - Thanks, Algo Muse!"
rating: 1700
weight: 1361
solve_time_s: 247
verified: true
draft: false
---

[CF 1361A - Johnny and Contribution](https://codeforces.com/problemset/problem/1361/A)

**Rating:** 1700  
**Tags:** constructive algorithms, graphs, greedy, sortings  
**Solve time:** 4m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph. Each vertex represents a blog, and every blog has a desired topic number `t[i]`.

Johnny writes blogs one by one. When he writes a blog, he looks only at neighbors that have already been written. Among their topics, he finds the smallest positive integer that does not appear and assigns exactly that topic to the current blog.

The desired topics are already fixed. Our task is to find an order of writing the blogs such that Johnny's rule produces exactly the given topic for every vertex. If no such order exists, we must output `-1`.

The graph contains up to `5 * 10^5` vertices and `5 * 10^5` edges. These limits immediately rule out anything quadratic. Even `O(n√n)` would be uncomfortable. Since the graph itself contains only `O(n + m)` data, an accepted solution should stay close to linear or `O((n + m) log n)`.

The tricky part is that the desired topics are not arbitrary labels. They must match the mex-like rule Johnny uses. A vertex with topic `k` must already see every topic from `1` through `k - 1` among its previously written neighbors, and it must not see topic `k`.

Several edge cases can easily break a naive construction.

Consider two adjacent vertices with the same topic:

```
2 1
1 2
1 1
```

If one of them is written first, the other already sees topic `1`, so it cannot also receive topic `1`. The correct answer is `-1`.

Consider a vertex whose topic is `3`, but it has neighbors only with topics `1` and `4`:

```
3 2
1 2
1 3
3 1 4
```

Topic `2` is missing from its neighborhood. No ordering can make Johnny assign topic `3` to that vertex. The correct answer is `-1`.

Another subtle case is when all required smaller topics exist but a neighbor has the same topic:

```
3 3
1 2
2 3
1 3
2 1 2
```

Vertex `1` has topic `2`. It sees a neighbor with topic `1`, which is good, but it also has a neighbor with topic `2`. When that topic-2 neighbor is processed earlier, topic `2` is already present among written neighbors, preventing the mex from being `2`. The instance is impossible.

The solution must verify all these conditions efficiently.

## Approaches

A brute-force idea is to try constructing an order and repeatedly simulate Johnny's rule. For every vertex, we could examine already processed neighbors, compute the smallest missing topic, and check whether it equals the desired value.

The problem is deciding which vertex comes next. Exploring possible orders is exponential. Even if we somehow fixed an order, recomputing the mex from scratch for every vertex could require scanning many neighbors repeatedly, leading to roughly `O(nm)` work in dense situations.

The key observation comes from looking at what must happen if a valid order exists.

Suppose a vertex has desired topic `t`.

For Johnny to assign topic `t`, every topic `1, 2, ..., t-1` must already appear among previously written neighbors. Since those topics must already exist before this vertex is written, all vertices with smaller topic numbers must be processed earlier.

This immediately suggests the only meaningful ordering: process vertices in increasing order of desired topic. Vertices sharing the same topic can appear in any relative order.

Now consider a vertex `v` with topic `t[v]`.

When all smaller-topic vertices have already been processed, the set of topics visible in `v`'s neighborhood must be exactly enough to make the mex equal `t[v]`.

That means:

1. No neighbor may have topic `t[v]`.
2. Every topic from `1` to `t[v]-1` must appear among the topics of its neighbors.

If these conditions hold for every vertex, then simply sorting vertices by topic already gives a valid writing order. All neighbors with smaller topics are processed earlier, all equal-topic neighbors are absent, and every required smaller topic is present.

This converts the problem from constructing a complicated order into verifying a local condition for every vertex.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential or worse | Large | Too slow |
| Optimal | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the graph and the desired topic of every vertex.
2. Create an ordering of vertices by increasing topic value.

If a valid solution exists, every vertex with smaller topic must be processed before every vertex with larger topic.
3. Traverse vertices in this sorted order.
4. For the current vertex `v`, collect the set of topic values appearing among all its neighbors.

We only need the topic labels themselves, not the neighbor identities.
5. If topic `t[v]` appears among the neighbor topics, the answer is impossible.

Johnny cannot receive topic `t[v]` if that topic already exists among neighbors.
6. Check whether the number of neighbor topics smaller than `t[v]` equals `t[v] - 1`.

Since topics are positive integers, this means every topic `1, 2, ..., t[v]-1` is present exactly as required.

A set is used, so duplicates do not matter.
7. If either check fails, output `-1`.
8. If all vertices pass, output the vertices in increasing-topic order.

### Why it works

Consider a vertex `v` with desired topic `t`.

If a valid writing order exists, every topic from `1` through `t-1` must already appear among previously written neighbors of `v`. Consequently, `v` must have neighbors carrying all those topic values. Also, topic `t` itself cannot appear among neighbors, otherwise the smallest missing topic would be larger than `t`.

These are necessary conditions.

They are also sufficient. After sorting vertices by increasing topic, every neighbor with a smaller topic is guaranteed to be processed earlier. Since every topic `1..t-1` exists in the neighborhood and topic `t` does not, the smallest missing topic among already written neighbors is exactly `t`. Thus Johnny assigns the desired topic.

Since every vertex satisfies this argument independently, the sorted order is valid for the whole graph.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    g = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    t = list(map(int, input().split()))

    order = sorted(range(n), key=lambda x: t[x])

    for v in order:
        cur = t[v]

        seen = set()

        for to in g[v]:
            topic = t[to]

            if topic == cur:
                print(-1)
                return

            if topic < cur:
                seen.add(topic)

        if len(seen) != cur - 1:
            print(-1)
            return

    print(*[v + 1 for v in order])

if __name__ == "__main__":
    solve()
```

The graph is stored as an adjacency list because both `n` and `m` can reach `5 * 10^5`.

The sorting step creates the candidate writing order. This is the central observation of the solution: any valid order must respect increasing topic values.

For each vertex, only neighbor topics matter. The set `seen` stores distinct topics smaller than the current topic. Duplicates are ignored automatically.

The condition

```
len(seen) == cur - 1
```

works because every topic is positive. If there are exactly `cur - 1` distinct smaller topics and all of them are less than `cur`, they must be precisely the set `{1, 2, ..., cur - 1}`.

Checking for a neighbor with the same topic is essential. Without this test, cases such as two adjacent vertices both labeled `1` would incorrectly pass.

No integer-overflow concerns exist because all values fit comfortably in Python integers.

## Worked Examples

### Sample 1

Input:

```
3 3
1 2
2 3
3 1
2 1 3
```

Sorted order by topic is `[2, 1, 3]`.

| Vertex | Topic | Smaller Neighbor Topics | Same Topic Neighbor Exists | Valid |
| --- | --- | --- | --- | --- |
| 2 | 1 | {} | No | Yes |
| 1 | 2 | {1} | No | Yes |
| 3 | 3 | {1,2} | No | Yes |

Output:

```
2 1 3
```

This example shows the intended behavior. Every vertex sees exactly the topics needed to make its topic value the mex.

### Impossible Example

Input:

```
2 1
1 2
1 1
```

Sorted order is `[1, 2]`.

| Vertex | Topic | Smaller Neighbor Topics | Same Topic Neighbor Exists | Valid |
| --- | --- | --- | --- | --- |
| 1 | 1 | {} | Yes | No |

The algorithm immediately outputs:

```
-1
```

This demonstrates why adjacent equal-topic vertices are forbidden.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Sorting costs O(n log n), graph scanning costs O(n + m) |
| Space | O(n + m) | Adjacency lists plus temporary sets |

With `n, m ≤ 5 * 10^5`, the graph traversal is linear in input size and the sorting step is easily fast enough within the 2-second limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())

    g = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    t = list(map(int, input().split()))

    order = sorted(range(n), key=lambda x: t[x])

    for v in order:
        cur = t[v]

        seen = set()

        for to in g[v]:
            topic = t[to]

            if topic == cur:
                return "-1\n"

            if topic < cur:
                seen.add(topic)

        if len(seen) != cur - 1:
            return "-1\n"

    return " ".join(str(v + 1) for v in order) + "\n"

# sample 1
assert run(
"""3 3
1 2
2 3
3 1
2 1 3
"""
) == "2 1 3\n"

# minimum graph
assert run(
"""1 0
1
"""
) == "1\n"

# adjacent equal topics
assert run(
"""2 1
1 2
1 1
"""
) == "-1\n"

# missing smaller topic
assert run(
"""3 2
1 2
1 3
3 1 4
"""
) == "-1\n"

# disconnected graph
assert run(
"""3 0
1 1 1
"""
) == "1 2 3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | `1` | Smallest possible instance |
| Two adjacent topic-1 vertices | `-1` | Equal-topic conflict |
| Missing topic below target | `-1` | Required neighborhood topics must exist |
| Empty graph with all topic 1 | Any permutation | Disconnected components work correctly |

## Edge Cases

Consider adjacent vertices with equal topics.

```
2 1
1 2
1 1
```

For vertex `1`, the neighbor-topic set contains topic `1`, which equals its own topic. The algorithm fails the same-topic check and outputs `-1`. If this check were omitted, the instance would incorrectly appear valid.

Consider a vertex missing one required smaller topic.

```
3 2
1 2
1 3
3 1 4
```

Vertex `1` wants topic `3`. Its neighbors have topics `{1,4}`. The set of smaller neighbor topics is `{1}`. Its size is `1`, but `3 - 1 = 2`. The algorithm correctly rejects the instance because topic `2` is absent.

Consider duplicated smaller topics.

```
4 3
1 2
1 3
1 4
3 1 1 1
```

Vertex `1` wants topic `3`. Its neighbors contribute topics `{1,1,1}`. A naive count of neighbors might incorrectly think there are enough smaller topics. The set removes duplicates, leaving only `{1}`. Since topic `2` is missing, the algorithm outputs `-1`.

Consider a disconnected graph.

```
3 0
1 1 1
```

Every vertex wants topic `1`. Each vertex has no neighbors, so the set of smaller topics is empty and the same-topic check never triggers. All vertices pass validation, and any ordering is valid. The algorithm outputs the sorted order.
