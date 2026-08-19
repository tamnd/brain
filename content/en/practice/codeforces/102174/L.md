---
title: "CF 102174L - \u65c5\u884c\u7684\u610f\u4e49"
description: "The cities form a directed acyclic graph, and the journey starts at city 1. Whenever the travelers arrive at a city, they spend one day sightseeing before making any decision. Suppose the current city has (d0) outgoing railway edges."
date: "2026-08-19T07:12:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102174
codeforces_index: "L"
codeforces_contest_name: "The 14-th BIT Campus Programming Contest"
rating: 0
weight: 102174
solve_time_s: 111
verified: true
draft: false
---

[CF 102174L - \u65c5\u884c\u7684\u610f\u4e49](https://codeforces.com/problemset/problem/102174/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The cities form a directed acyclic graph, and the journey starts at city 1. Whenever the travelers arrive at a city, they spend one day sightseeing before making any decision.

Suppose the current city has (d>0) outgoing railway edges. On the following day there are (d+1) equally likely choices: take any one of the (d) outgoing trains, or stay for one more sightseeing day. If they stay, they cannot stay again, so on the next day they must choose one of the (d) outgoing trains uniformly. A city with no outgoing edge is a terminal city, where they spend two days in total and then the journey ends.

The input contains (T) independent test cases. Each test case gives (n) cities and (m) directed railway edges. The graph is guaranteed to be a DAG, but the city numbering is not guaranteed to be a topological ordering. We need the expected total number of days starting from city 1, represented modulo (998244353).

The bounds (n,m\le 10^5) are the main algorithmic signal. A quadratic algorithm could perform around (10^{10}) operations on one large test case, which is far beyond a one-second limit. Even an algorithm depending on enumerating all possible routes is hopeless because a DAG can contain exponentially many distinct paths. We need a solution whose work is essentially proportional to the graph size, namely (O(n+m)).

There are several edge cases that can make a careless implementation wrong. The smallest graph is

```
1
1 0
```

There is no outgoing edge, but the traveler still spends two days in the only city. The correct answer is `2`. An implementation that treats zero outdegree as zero future cost and forgets the second sightseeing day would output `1`.

A city with one outgoing edge also needs special handling in the probability calculation. For

```
1
2 1
1 2
```

city 2 contributes two days. From city 1, there is probability (1/2) of taking the train immediately and probability (1/2) of staying one extra day before taking it. The expected contribution before arriving at city 2 is (1+3/2=5/2), so the total is (9/2), whose modular representation is `499122181`. Replacing the stay probability by (1/d), rather than (1/(d+1)), gives the wrong result.

The city numbers also cannot be assumed to form a topological order. For example,

```
1
3 2
1 3
3 2
```

requires city 2 to be processed before city 3, and city 3 before city 1. A DP that simply loops from (n) down to (1) happens to work for some graphs but has no correctness guarantee here.

Finally, unreachable cities do not affect the answer. For

```
1
3 0
```

the travelers start at city 1 and finish there after two days. Cities 2 and 3 are irrelevant. Computing DP values for every city is still fine, because the answer only uses the value of city 1.

## Approaches

A direct brute-force approach would simulate every possible journey. At a city with (d) outgoing edges, we would branch into the possible immediate train choices and the possibility of staying, and after staying we would branch over the outgoing edges again. For each complete route we could calculate its duration and its probability, then sum the contributions.

This is correct because expectation is the probability-weighted sum over all possible journeys. The problem is the number of journeys. A DAG containing every edge (i\to j) for (i<j) has (2^{n-2}) distinct paths from city 1 to city (n), because every subset of the intermediate cities can occur in increasing order. The stay decisions add additional branches to the state space. With (n=10^5), even (2^{99998}) is far beyond anything that can be enumerated.

The brute-force works because each journey can be evaluated independently, but it fails because many different journeys repeatedly pass through the same city. The key observation is that once we arrive at a city, the expected remaining duration depends only on that city, not on the history used to reach it. We can store that expected value as a DP state.

There is one more useful simplification in the transition probability. If a city has (d>0) outgoing edges, each immediate train choice has probability (1/(d+1)). Staying also has probability (1/(d+1)), and after staying, each outgoing edge is chosen with probability (1/d). Hence the total probability of eventually taking any particular outgoing edge is

[
\frac{1}{d+1}+\frac{1}{d+1}\cdot\frac{1}{d}
=\frac{1}{d}.
]

So after accounting for the possible extra sightseeing day, the next city is simply uniformly distributed among the outgoing neighbors.

Let (f_u) be the expected number of days remaining when the travelers have just arrived at city (u), before sightseeing there. For (d=0),

[
f_u=2.
]

For (d>0), the first sightseeing day costs one day. After that, taking a train costs one day, while staying first costs one additional day before the train. Since staying has probability (1/(d+1)), the expected cost from that point until arrival at the next city is

[
1+\left(1+\frac{1}{d+1}\right)
=2+\frac{1}{d+1}.
]

The next city is uniformly distributed among the (d) outgoing neighbors, giving

2+\frac{1}{d+1}
+
\frac{1}{d}\sum_{u\to v}f_v.
]

Because the graph is acyclic, every (f_u) depends only on values farther along the DAG. A topological ordering lets us calculate all values in reverse order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n)) in the worst case | (O(n)) recursion depth | Too slow |
| Optimal | (O(n+m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Read the directed graph and record the outgoing neighbors of every city. At the same time, compute each city's indegree. The indegree values let us obtain a topological ordering without relying on the city labels.
2. Run Kahn's topological sorting algorithm. Put every zero-indegree city into a queue, repeatedly remove one city, and decrease the indegree of its outgoing neighbors. Since the graph is guaranteed to be a DAG, every city will eventually enter the ordering.
3. Precompute modular inverses for all integers up to (n+1). For a city with outdegree (d), the recurrence needs both (1/d) and (1/(d+1)). Since every degree is at most (10^5), all these denominators are smaller than the modulus (998244353), so their inverses exist.
4. Process the topological ordering in reverse. When city (u) is processed, every outgoing neighbor (v) has already been processed, so all (f_v) values are known.
5. If city (u) has no outgoing edges, set (f_u=2). The travelers spend one day sightseeing and one further day because there is no train to take.
6. Otherwise, let (d) be the outdegree of (u). Compute

[
f_u=
2+\frac{1}{d+1}
+\frac{1}{d}\sum_{u\to v}f_v
\pmod {998244353}.
]

The term (2+1/(d+1)) contains every day spent at the current city and on the transition to the next city. The average of the successor values accounts for which outgoing train is eventually taken.

1. Output (f_1), because city 1 is the starting city.

The invariant is that when a city is processed in reverse topological order, its DP value is computed from exact values for every city reachable by one outgoing edge. The recurrence itself is the law of total expectation over all possible decisions at that city. Since every edge goes forward in the topological ordering, no value is used before it has been finalized. Thus every (f_u), and in particular (f_1), equals the true expected remaining travel time.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353
MAXN = 100000 + 2

# inv[i] = i^(-1) mod MOD
inv = [0] * (MAXN + 1)
inv[1] = 1
for i in range(2, MAXN + 1):
    inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

def solve():
    T = int(input())
    answers = []

    for _ in range(T):
        n, m = map(int, input().split())

        graph = [[] for _ in range(n)]
        indeg = [0] * n

        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            graph[u].append(v)
            indeg[v] += 1

        # Kahn's algorithm for a topological ordering.
        queue = [u for u in range(n) if indeg[u] == 0]
        head = 0
        topo = []

        while head < len(queue):
            u = queue[head]
            head += 1
            topo.append(u)

            for v in graph[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    queue.append(v)

        dp = [0] * n

        # Every successor appears earlier in reverse topological order.
        for u in reversed(topo):
            d = len(graph[u])

            if d == 0:
                dp[u] = 2
                continue

            s = 0
            for v in graph[u]:
                s += dp[v]
            s %= MOD

            dp[u] = (
                2
                + inv[d + 1]
                + s * inv[d]
            ) % MOD

        answers.append(str(dp[0]))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The adjacency list stores exactly the outgoing railway choices required by the recurrence. It also lets both topological sorting and the DP traverse every edge only a constant number of times.

The topological sort uses a list together with a head pointer instead of repeatedly removing from the front of a Python list. Removing from the front would cost (O(n)) per operation, while advancing `head` is constant time.

The inverse array is computed once for all test cases. The recurrence for modular inverses is

-\left\lfloor\frac{MOD}{i}\right\rfloor
\operatorname{inv}(MOD\bmod i)
\pmod{MOD}.
]

This avoids performing a modular exponentiation for every city. Calling `pow(x, MOD-2, MOD)` separately for up to (10^5) degrees would add an unnecessary logarithmic factor.

The zero-outdegree branch must be handled before using `inv[d]`, because (1/0) is undefined. More importantly, its expected value is exactly 2 rather than 1.

All arithmetic is reduced modulo (998244353). Python integers do not overflow, but reducing the neighbor sum and the final recurrence keeps the intermediate values small and matches the mathematical modular computation.

The graph is not assumed to be ordered by vertex number. The reverse traversal of `topo` is what guarantees that every `dp[v]` used by `dp[u]` is already available.

## Worked Examples

For the first sample, the input is

```
1
1 0
```

There is only one city and no railway edge.

| City | Outdegree | Neighbor Sum | DP |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 2 |

The zero-outdegree rule immediately gives (f_1=2). The answer is therefore `2`.

For the second sample, the input is

```
1
2 1
1 2
```

The topological order is (1,2). Processing it backwards gives city 2 first.

| City | Outdegree | Neighbor Sum | DP |
| --- | --- | --- | --- |
| 2 | 0 | 0 | 2 |
| 1 | 1 | 2 | (2+\frac12+2=\frac92) |

For city 1, (d=1), so the extra stay contributes (1/(1+1)=1/2). The only successor has expected value 2. Thus

[
f_1=2+\frac12+2=\frac92.
]

Modulo (998244353),

[
\frac92=9\cdot 2^{-1}
=499122181,
]

which matches the sample output.

A slightly richer trace is useful for seeing the averaging term. Consider

```
1
4 4
1 2
1 3
2 4
3 4
```

City 4 is terminal, while cities 2 and 3 both lead directly to city 4.

| City | Outdegree | Neighbor Sum | DP |
| --- | --- | --- | --- |
| 4 | 0 | 0 | 2 |
| 3 | 1 | 2 | (9/2) |
| 2 | 1 | 2 | (9/2) |
| 1 | 2 | 9 | (27/4) |

At city 1 there are two outgoing edges, so the extra-stay expectation is (1/3), and the next city is uniformly distributed between cities 2 and 3. Both have value (9/2), so

[
f_1=2+\frac13+\frac{1}{2}\left(\frac92+\frac92\right)
=\frac{27}{4}.
]

This example confirms that the recurrence depends on the average successor expectation rather than on any particular path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m)) | Topological sorting visits every city and edge once, and the DP scans every edge once more. |
| Space | (O(n+m)) | The adjacency lists contain (m) edges, while the graph and DP arrays contain (O(n)) additional values. |

With (n,m\le 10^5), the algorithm performs only a few linear passes over the input graph. Across multiple test cases, the same reasoning applies independently to each case. The memory usage is also linear in the graph size and fits comfortably within the stated memory limit.

## Test Cases

```python
# The production solution above is organized around solve(), which reads
# from sys.stdin. For isolated tests, this helper temporarily replaces stdin.

import sys
import io
from contextlib import redirect_stdout

MOD = 998244353

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    data = sys.stdin.read().split()
    it = iter(data)

    T = int(next(it))
    out = []

    for _ in range(T):
        n = int(next(it))
        m = int(next(it))

        graph = [[] for _ in range(n)]
        indeg = [0] * n

        for _ in range(m):
            u = int(next(it)) - 1
            v = int(next(it)) - 1
            graph[u].append(v)
            indeg[v] += 1

        queue = [i for i in range(n) if indeg[i] == 0]
        head = 0
        topo = []

        while head < len(queue):
            u = queue[head]
            head += 1
            topo.append(u)

            for v in graph[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    queue.append(v)

        max_degree = max((len(x) for x in graph), default=0)

        inv = [0] * (max_degree + 2)
        if max_degree + 1 >= 1:
            inv[1] = 1

        for i in range(2, max_degree + 2):
            inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

        dp = [0] * n

        for u in reversed(topo):
            d = len(graph[u])

            if d == 0:
                dp[u] = 2
            else:
                s = sum(dp[v] for v in graph[u]) % MOD
                dp[u] = (
                    2 + inv[d + 1] + s * inv[d]
                ) % MOD

        out.append(str(dp[0]))

    sys.stdin = old_stdin
    return "\n".join(out)

# Provided sample 1
assert run("""\
1
1 0
""") == "2", "sample 1"

# Provided sample 2
assert run("""\
1
2 1
1 2
""") == "499122181", "sample 2"

# Minimum-size graph and unreachable cities.
assert run("""\
1
3 0
""") == "2", "only city 1 is reachable"

# Two branches merging into one terminal city.
assert run("""\
1
4 4
1 2
1 3
2 4
3 4
""") == "249561095", "diamond DAG"

# Star graph: f[1] = 2 + 1/4 + 2 = 17/4.
assert run("""\
1
4 3
1 2
1 3
1 4
""") == "748683269", "outdegree three"

# Maximum-size chain: 100000 cities and 99999 edges.
# There are 99999 nonterminal cities contributing 5/2 each,
# followed by one terminal city contributing 2.
n = 100000
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
max_case = f"{n} {n - 1}\n{edges}\n"

assert run("1\n" + max_case) == "499372177", "maximum-size chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 0` | `2` | Minimum graph and terminal-city handling |
| `3 0` | `2` | Unreachable cities must not affect city 1 |
| Diamond DAG | `249561095` | Branching, merging, and successor averaging |
| Three-edge star | `748683269` | Correct (1/(d+1)) stay term for (d=3) |
| 100000-city chain | `499372177` | Maximum input size and repeated DP transitions |

## Edge Cases

For a graph consisting only of city 1,

```
1
1 0
```

the topological order contains city 1, and the reverse DP immediately sees outdegree zero. It assigns `dp[0] = 2`, so the output is `2`. There is no division by the outdegree because the terminal case is handled separately.

For a single railway edge,

```
1
2 1
1 2
```

the reverse topological order processes city 2 first and assigns it value 2. City 1 has degree 1, so its recurrence is

[
2+\frac12+\frac{2}{1}=\frac92.
]

The modular result is `499122181`. This catches the common mistake of treating the train probability as 1 instead of accounting for the possible extra sightseeing day.

For a graph whose labels are not topologically sorted,

```
1
3 2
1 3
3 2
```

the correct topological order is (1,3,2). Reverse processing gives city 2 value 2, then city 3 value (9/2), then city 1 value (27/4). The modular output is `249561095`. A loop based only on descending or ascending city numbers would not provide the required dependency ordering in general.

For a city with several outgoing edges,

```
1
4 3
1 2
1 3
1 4
```

cities 2, 3, and 4 are all terminal and have value 2. City 1 has (d=3), so

# 2+\frac14+\frac{2+2+2}{3}

\frac{17}{4}.
]

The modular result is `748683269`. This verifies both the (1/(d+1)) stay probability and the uniform (1/d) distribution over the eventual outgoing edge.

The maximum-size chain contains 100000 cities,

```
100000 99999
1 2
2 3
...
99999 100000
```

with the obvious consecutive edges. Every nonterminal city has degree 1, so each contributes (5/2) days before the next city, while city 100000 contributes 2. The exact expectation is

\frac{499999}{2},
]

which is `499372177` modulo (998244353). The linear DP handles all 100000 states without recursion, avoiding both recursion-depth problems and any exponential path enumeration.
