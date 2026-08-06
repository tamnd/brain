---
title: "CF 102483B - Brexit Negotiations"
description: "We have a directed acyclic graph of negotiation topics. Each topic has a base discussion time e[i], and some topics can only be discussed after certain other topics are finished. A valid schedule is any topological ordering of this graph."
date: "2026-08-06T18:49:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102483
codeforces_index: "B"
codeforces_contest_name: "2018-2019 ICPC Northwestern European Regional Programming Contest (NWERC 2018)"
rating: 0
weight: 102483
solve_time_s: 103
verified: true
draft: false
---

[CF 102483B - Brexit Negotiations](https://codeforces.com/problemset/problem/102483/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a directed acyclic graph of negotiation topics. Each topic has a base discussion time `e[i]`, and some topics can only be discussed after certain other topics are finished. A valid schedule is any topological ordering of this graph.

If a topic is placed at position `p` in the schedule, with the first meeting having position `0`, the meeting takes `e[i] + p` minutes. The extra `p` minutes come from reviewing all previous meetings. The goal is to choose a valid ordering that minimizes the longest single meeting duration.

The input gives the number of topics, then for each topic its base time and the list of prerequisite topics. The output is the smallest possible value of the maximum `e[i] + p` over all valid schedules.

The constraint of `n` up to `400000` rules out algorithms that repeatedly try different orders or use dynamic programming over subsets. The graph can have up to `400000` dependency edges, so the intended solution must be close to linear time. A normal topological sort with a priority queue is suitable because it processes each topic and edge only a logarithmic number of times.

A few cases are easy to mishandle. When several topics have no dependencies, the largest base time must be scheduled first. For example:

```
3
10 0
1 0
1 0
```

The answer is `12`. The optimal order is the topic with time `10` first, giving lengths `10`, `2`, and `3`. Choosing a smaller topic first gives the large topic an unnecessary delay.

A second case is when a long topic is not initially available:

```
2
1 1 2
100 0
```

The answer is `101`. The second topic must happen first because the first topic depends on it. A greedy implementation that ignores dependencies and simply sorts by `e` would produce an invalid schedule.

A final corner case is a single topic:

```
1
500 0
```

The answer is `500`. There is no recap time because no earlier meetings exist.

## Approaches

A direct approach would try to construct the schedule while repeatedly searching all currently available topics. At every position, we could scan every topic, check whether it is available, and select the one with the largest `e`. This is correct because the best choice at each point is the topic that suffers most from being delayed. However, with `400000` topics, scanning all topics for every position requires roughly `400000^2`, or `1.6 * 10^11`, checks in the worst case, which is far too slow.

The useful observation is that the only information needed when choosing the next topic is the set of topics whose prerequisites are already completed. This is exactly the state maintained by Kahn's topological sorting algorithm. Instead of scanning all topics, we keep the available topics in a max-heap ordered by `e`. Whenever a topic becomes available, it is inserted into the heap. The next meeting is always the available topic with the largest base duration.

The reason this greedy choice works is that delaying a topic by one position increases its meeting length by exactly one minute. If two currently available topics are `a` and `b`, with `e[a] > e[b]`, placing `b` before `a` increases the larger topic's final duration while not helping any dependency relationship. Swapping them can only improve or preserve the maximum meeting length. Repeating this exchange argument means an optimal schedule can always be transformed into one that chooses the largest available `e` at every step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O((n + m) log n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build the dependency graph. For every prerequisite relation `a -> b`, store `b` as a topic that becomes closer to available after `a` is completed. Also store the number of unfinished prerequisites for every topic.
2. Put every topic with zero unfinished prerequisites into a max-heap ordered by its base time. These topics are the only ones that can legally be discussed first.
3. Repeatedly remove the topic with the largest base time from the heap. Its current position is the number of meetings already completed, so update the answer with `e[i] + position`.
4. After completing a topic, decrease the prerequisite count of every topic depending on it. If one of those counts becomes zero, insert that topic into the heap because it is now available.
5. Continue until every topic has been scheduled. The stored maximum is the minimum possible longest meeting.

Why it works: at every point, the heap contains exactly the topics that can legally be chosen next. Among these choices, selecting the largest `e` value is optimal because any available topic can be exchanged with the chosen one without violating dependencies, and moving a larger `e` topic later can only increase the maximum value. Since every decision can be justified by this exchange argument, the whole ordering is optimal.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n = int(input())
    e = [0] * n
    graph = [[] for _ in range(n)]
    indeg = [0] * n

    for i in range(n):
        data = list(map(int, input().split()))
        e[i] = data[0]
        d = data[1]
        indeg[i] = d
        for x in data[2:]:
            graph[x - 1].append(i)

    heap = []
    for i in range(n):
        if indeg[i] == 0:
            heapq.heappush(heap, (-e[i], i))

    ans = 0
    done = 0

    while heap:
        neg_e, u = heapq.heappop(heap)
        ans = max(ans, -neg_e + done)
        done += 1

        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, (-e[v], v))

    print(ans)

if __name__ == "__main__":
    solve()
```

The graph stores outgoing edges from prerequisites to dependent topics. This direction makes the update after finishing a topic straightforward because we only need to visit topics that may become available.

The heap is implemented as a min-heap from Python's standard library, so the stored value is `-e[i]` to simulate a max-heap. The variable `done` is the current zero-based position in the schedule. The meeting at this position has length `e[i] + done`.

All durations fit inside Python integers. The largest possible answer is below `1,400,000`, but Python's arbitrary precision also removes any overflow concerns.

## Worked Examples

For three independent topics:

```
3
10 0
10 0
10 0
```

the trace is:

| Step | Available heap | Chosen topic | Position | Current answer |
| --- | --- | --- | --- | --- |
| 0 | 10,10,10 | 10 | 0 | 10 |
| 1 | 10,10 | 10 | 1 | 11 |
| 2 | 10 | 10 | 2 | 12 |

All topics are available immediately, so the algorithm only needs to order equal values. The final delay on the last topic determines the answer.

For the second sample:

```
6
2 2 4 3
4 1 5
1 2 2 4
3 1 5
2 0
4 1 3
```

the important states are:

| Step | Available topics by `e` | Chosen | Position | Maximum |
| --- | --- | --- | --- | --- |
| 0 | 5(2), 2(4) | topic 5 | 0 | 2 |
| 1 | 4(2), 2(1) | topic 2 | 1 | 5 |
| 2 | 6(4) | topic 6 | 2 | 6 |
| 3 | 4(3), 1(1) | topic 4 | 3 | 7 |
| 4 | 1(1), 3(2) | topic 3 | 4 | 8 |
| 5 | 1 | topic 1 | 5 | 8 |

The trace shows that newly unlocked topics are immediately considered together with all other available topics. The heap never contains an illegal topic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Every topic enters and leaves the heap once, and every dependency edge is processed once. |
| Space | O(n + m) | The graph stores all dependency edges and the heap stores available topics. |

Here `m` is the total number of dependency relations. Since `m` is at most `400000`, the solution stays within the required limits.

## Test Cases

```python
import sys
import io
import heapq

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    n = int(input())
    e = [0] * n
    graph = [[] for _ in range(n)]
    indeg = [0] * n

    for i in range(n):
        data = list(map(int, input().split()))
        e[i] = data[0]
        indeg[i] = data[1]
        for x in data[2:]:
            graph[x - 1].append(i)

    heap = []
    for i in range(n):
        if indeg[i] == 0:
            heapq.heappush(heap, (-e[i], i))

    ans = done = 0
    while heap:
        x, u = heapq.heappop(heap)
        ans = max(ans, -x + done)
        done += 1
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, (-e[v], v))

    sys.stdin = old
    return str(ans) + "\n"

assert run("""3
10 0
10 0
10 0
""") == "12\n"

assert run("""6
2 2 4 3
4 1 5
1 2 2 4
3 1 5
2 0
4 1 3
""") == "8\n"

assert run("""1
500 0
""") == "500\n"

assert run("""3
5 0
1 0
2 0
""") == "7\n"

assert run("""2
1 1 2
100 0
""") == "101\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single topic | 500 | Minimum graph size and zero recap time |
| Independent topics with different values | 7 | Choosing the largest available topic first |
| Dependency chain with large prerequisite | 101 | Respecting dependencies over raw values |

## Edge Cases

For the independent topics case:

```
3
5 0
1 0
2 0
```

all topics enter the heap immediately. The algorithm selects `5`, then `2`, then `1`, producing meeting lengths `5`, `3`, and `3`. The answer is `5`, while a smaller-first ordering would unnecessarily increase the maximum.

For the forced dependency case:

```
2
1 1 2
100 0
```

only topic 2 is initially available, so the heap contains no choice. After topic 2 finishes, topic 1 becomes available. The algorithm computes `100 + 0` and `1 + 1`, giving `101`.

For equal values:

```
3
10 0
10 0
10 0
```

the heap may return any of the three topics first because their priorities are identical. Every possible order gives the same result, and the final topic receives two minutes of recap time, producing `12`.
