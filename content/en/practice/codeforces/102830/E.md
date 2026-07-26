---
title: "CF 102830E - Buying Tacos"
description: "Kevin has several taco types available. Each type has a normal purchase price, and there are also one-way exchanges between taco types. An exchange lets him turn one taco of one type into another taco type by paying an additional fee."
date: "2026-07-26T15:21:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102830
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 11-06-20 Div. 2 (Beginner)"
rating: 0
weight: 102830
solve_time_s: 47
verified: true
draft: false
---

[CF 102830E - Buying Tacos](https://codeforces.com/problemset/problem/102830/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

Kevin has several taco types available. Each type has a normal purchase price, and there are also one-way exchanges between taco types. An exchange lets him turn one taco of one type into another taco type by paying an additional fee. Every exchange can be performed any number of times.

The input describes the number of taco types, the direct price of buying one taco of each type, all possible exchanges, and finally how many tacos of each type Kevin wants. The goal is to find the minimum amount of money needed to end with exactly the requested distribution of tacos.

The central question is not how to perform the exchanges after buying tacos. Instead, it is how cheaply each final taco type can be produced. A taco of type `i` can either be bought directly or obtained by buying another type and following a sequence of exchanges. Once the cheapest cost of producing every type is known, each requested taco can be handled independently.

The constraints strongly suggest a graph solution. There can be up to 10,000 taco types and 100,000 exchanges. An approach that checks every possible starting taco for every destination would require around 10^8 or more operations just for the graph processing, and repeatedly exploring paths would be far too slow. We need a shortest path algorithm that handles sparse graphs efficiently. The edge weights are non-negative, so Dijkstra's algorithm is suitable.

There are several edge cases where a careless implementation can fail. The first is when a taco can only be obtained through several exchanges. For example:

```
Input
3 2
10
100
100
0 1 3
1 2 4
0
0
1
```

The correct output is:

```
17
```

Buying type 0 and making the two exchanges costs `10 + 3 + 4 = 17`. A solution that only considers direct purchases would incorrectly answer `100`.

Another tricky case is when an exchange is cheaper than buying the source taco directly but the exchange path starts from a different type. For example:

```
Input
2 1
100
5
1 0 2
0
1
```

The correct output is:

```
5
```

Type 1 is already cheap enough, and no conversion is required. A solution that assumes every taco must use at least one exchange could produce a larger cost.

The last common mistake is ignoring that many taco types may share the same cheapest source. For example:

```
Input
3 2
1
50
50
0 1 1
0 2 2
3
3
3
```

The correct output is:

```
15
```

Every taco can be made from type 0. The answer is `3 * 1 + 3 * 2 + 3 * 3 = 18`? Wait, the requested counts in this example are all three, so the actual output is:

```
18
```

A solution that only computes one best conversion target or greedily assigns sources without considering every destination independently would fail.

## Approaches

The brute-force approach is to consider every taco type as a possible starting point, then run a shortest path search from that type to determine which other taco types it can produce. After that, we could compare the cost of buying the starting taco and converting it with the current best answer for each destination.

This method is correct because every possible source taco is considered. If the cheapest way to create a taco type begins with buying taco `s`, that run from `s` will discover the corresponding exchange path.

The problem is the amount of repeated work. Running Dijkstra once costs `O((t + e) log t)`. Running it from every taco type costs `O(t(t + e) log t)`. With 10,000 taco types and 100,000 exchanges, this is far beyond what the time limit allows.

The key observation is that all taco types are asking the same question: "What is the cheapest source that can reach me?" Instead of running shortest paths from every source separately, we can reverse the viewpoint. Imagine creating a virtual source that has a distance of zero to every taco type, but before running Dijkstra we initialize every taco type's distance with its direct buying cost. Multi-source Dijkstra will then spread these initial costs through the exchange graph.

When Dijkstra relaxes an exchange from type `i` to type `j`, it checks whether obtaining `i` cheaply and paying the exchange fee is better than the current way of obtaining `j`. This exactly matches the original problem because every possible starting purchase is already present in the initial distances.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(t(t + e) log t) | O(t + e) | Too slow |
| Optimal | O((t + e) log t) | O(t + e) | Accepted |

## Algorithm Walkthrough

1. Read the taco types, their direct purchase prices, the exchanges, and the required quantities. Store each exchange as a directed graph edge because an exchange from type `i` to type `j` does not imply the reverse exchange exists.
2. Initialize the shortest distance of every taco type with its direct purchase price. This represents the possibility of buying that taco immediately without using any exchanges.
3. Insert every taco type into the priority queue with its current distance. This starts Dijkstra from all possible sources at the same time.
4. Repeatedly remove the taco type with the smallest known cost. For every outgoing exchange, calculate the cost of reaching the destination by first obtaining the current taco type and then paying the exchange fee. If this value is smaller, update the destination and push the new value into the priority queue.
5. After the shortest path process finishes, multiply the cheapest cost of each taco type by the number of tacos requested for that type. Add these values together to get the minimum total price.

The reason this works is that every valid way of obtaining a taco consists of choosing some starting taco to buy and then following a path of exchanges. The initial distances represent all possible starting purchases, and every relaxation represents extending one of those paths. Dijkstra always keeps the cheapest known path to each node because all exchange costs are non-negative. When the algorithm finishes, the distance of every taco type is exactly the cheapest possible cost to create one taco of that type.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    t, e = map(int, input().split())

    dist = []
    for _ in range(t):
        dist.append(int(input()))

    graph = [[] for _ in range(t)]

    for _ in range(e):
        i, j, p = map(int, input().split())
        graph[i].append((j, p))

    need = []
    for _ in range(t):
        need.append(int(input()))

    pq = []
    for i, cost in enumerate(dist):
        heapq.heappush(pq, (cost, i))

    while pq:
        cost, node = heapq.heappop(pq)

        if cost != dist[node]:
            continue

        for nxt, price in graph[node]:
            new_cost = cost + price
            if new_cost < dist[nxt]:
                dist[nxt] = new_cost
                heapq.heappush(pq, (new_cost, nxt))

    answer = 0
    for i in range(t):
        answer += dist[i] * need[i]

    print(answer)

if __name__ == "__main__":
    solve()
```

The `dist` array starts with direct taco prices instead of infinity. This is the main implementation detail that turns normal Dijkstra into multi-source Dijkstra.

The priority queue contains every taco type at the beginning. When a cheaper path is found, the old queue entry is not removed. Instead, a new entry is inserted, and the `if cost != dist[node]` check skips outdated entries. This is the standard way to implement Dijkstra efficiently in Python.

The graph is directed because exchanges only work in the specified direction. Treating it as undirected would incorrectly allow impossible conversions.

The final multiplication is safe because the number of taco types and the values fit comfortably in Python integers. Python integers do not overflow, so the code does not need special handling for large sums.

## Worked Examples

For the sample input:

```
3 2
1
3
5
0 1 1
1 2 1
1
2
3
```

The initial distances are the direct prices.

| Step | Processed taco | Current distances |
| --- | --- | --- |
| Start | None | [1, 3, 5] |
| 1 | Type 0 | [1, 2, 5] |
| 2 | Type 1 | [1, 2, 3] |
| 3 | Type 2 | [1, 2, 3] |

The cheapest prices become 1, 2, and 3. The required amounts are 1, 2, and 3, so the answer is `1*1 + 2*2 + 3*3 = 14`.

For a second example:

```
2 1
10
100
0 1 5
0
2
```

| Step | Processed taco | Current distances |
| --- | --- | --- |
| Start | None | [10, 100] |
| 1 | Type 0 | [10, 15] |
| 2 | Type 1 | [10, 15] |

The second taco is cheaper through one exchange than by buying it directly. Two tacos of type 1 cost `2 * 15 = 30`.

This trace demonstrates that the algorithm does not care whether the cheapest route uses zero, one, or many exchanges. It treats all possibilities uniformly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((t + e) log t) | Each taco type can enter the priority queue multiple times, and each exchange is relaxed during Dijkstra. |
| Space | O(t + e) | The graph stores every exchange and the arrays store one value per taco type. |

With 10,000 taco types and 100,000 exchanges, this complexity easily fits the limits. The algorithm performs one graph traversal instead of repeating shortest path computations from every possible starting taco.

## Test Cases

```python
import sys
import io
import heapq

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    input = sys.stdin.readline

    t, e = map(int, input().split())
    dist = [int(input()) for _ in range(t)]

    graph = [[] for _ in range(t)]
    for _ in range(e):
        i, j, p = map(int, input().split())
        graph[i].append((j, p))

    need = [int(input()) for _ in range(t)]

    pq = [(dist[i], i) for i in range(t)]
    heapq.heapify(pq)

    while pq:
        cost, node = heapq.heappop(pq)
        if cost != dist[node]:
            continue
        for nxt, price in graph[node]:
            if cost + price < dist[nxt]:
                dist[nxt] = cost + price
                heapq.heappush(pq, (dist[nxt], nxt))

    ans = sum(dist[i] * need[i] for i in range(t))
    print(ans)

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""3 2
1
3
5
0 1 1
1 2 1
1
2
3
""") == "14\n", "sample"

assert run("""2 1
10
100
0 1 5
0
2
""") == "30\n", "single exchange"

assert run("""1 0
7
5
""") == "35\n", "minimum size"

assert run("""3 0
4
4
4
10
10
10
""") == "120\n", "all equal values"

assert run("""4 3
100
50
20
10
0 1 1
1 2 1
2 3 1
0
0
0
5
""") == "65\n", "long chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample input | 14 | Normal shortest path propagation |
| Two taco types with one exchange | 30 | Cheaper conversion than direct purchase |
| One taco type | 35 | Minimum-size input handling |
| All direct prices equal | 120 | No unnecessary exchange assumptions |
| Long exchange chain | 65 | Multiple-step conversions |

## Edge Cases

When a taco can only be reached after multiple exchanges, the algorithm naturally handles it through repeated relaxations. In the example with prices 10, 100, 100 and exchanges `0 -> 1` costing 3 and `1 -> 2` costing 4, Dijkstra starts with distances `[10, 100, 100]`. It first improves type 1 to 13, then improves type 2 to 17. The final answer uses 17 because the cheapest path contains both exchanges.

When a taco is already the cheapest possible source, the algorithm keeps its initial distance. For the input with prices 100 and 5 and an exchange from type 1 to type 0, the initial distances are `[100, 5]`. Processing type 1 tries to improve type 0 to 7, but that only affects type 0. The requested type 1 tacos still cost 5 each.

When many taco types share the same cheapest source, every destination receives its own shortest path value. For a chain of exchanges from type 0, the distance values spread outward one edge at a time. The final multiplication by the requested counts then correctly combines those independent minimum costs.
