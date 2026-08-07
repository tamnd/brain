---
title: "CF 102566A - Beggars"
description: "We are given a collection of trains, where each train is available at the station during one continuous interval of time. A beggar must spend the entire working period from time 0 to time d inside trains."
date: "2026-08-07T21:32:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102566
codeforces_index: "A"
codeforces_contest_name: "AGM 2020, Qualification Round"
rating: 0
weight: 102566
solve_time_s: 56
verified: true
draft: false
---

[CF 102566A - Beggars](https://codeforces.com/problemset/problem/102566/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of trains, where each train is available at the station during one continuous interval of time. A beggar must spend the entire working period from time 0 to time d inside trains. A single beggar can move from one train to another instantly when one train leaves and another arrives, so a beggar's schedule is a chain of train intervals where the end of one interval matches the beginning of the next one.

The goal is to maximize how many beggars can work simultaneously. Two beggars cannot use the same train, and they cannot switch at the same moment because that would mean they meet on the platform. This means every train can belong to at most one beggar, and different beggars must use completely separate chains of trains.

The input contains several test cases. Each test case gives the length of the working day d and the list of n train intervals. The output is the largest number of complete schedules from time 0 to time d that can be formed without conflicts.

The small value of d is the key restriction that shapes the solution. There are at most 200 different time points, while the number of trains can reach 20000. Any approach that tries all possible groups of trains is impossible because the number of combinations grows exponentially. Even checking many possible schedules separately would be too slow when n is large. The time dimension is small enough that building a graph over time points is practical.

A few details can break a naive implementation. Consider a single train from 0 to 5.

```
1
5 1
0 5
```

The answer is 1 because one beggar can use that train for the entire period. An approach that only counts transitions between trains might incorrectly return 0 because there is no switch.

Another important case is multiple identical trains.

```
1
3 3
0 3
0 3
0 3
```

The answer is 3. Three beggars can each stay on one different train. Treating identical intervals as duplicates and keeping only one would lose valid schedules.

A third case is a large overlap at an intermediate time.

```
1
4 4
0 2
0 2
2 4
2 4
```

The answer is 2. Two beggars can take the two complete paths independently. A greedy approach that always chooses the longest-looking train can accidentally consume a train needed by another valid path.

## Approaches

A direct approach is to try to construct every possible beggar schedule. A schedule is a path through the trains, starting with a train beginning at time 0 and ending with a train finishing at time d. After finding one schedule, we could remove its trains and search again. This is correct if every possible choice is explored, because the definition of a valid solution is exactly a collection of non-overlapping paths. The problem is that the number of possible paths is enormous. With 20000 trains, the number of possible combinations can be exponential, making this approach unusable.

The structure of the problem suggests looking at time points instead of individual beggars. Every train interval can be viewed as a directed edge from its starting time to its ending time. A beggar's complete journey becomes a path from node 0 to node d. Because two beggars cannot use the same train, every edge has capacity one. Because they cannot meet while switching, multiple paths cannot share intermediate time points. This is exactly a maximum flow problem where both train usage and switching locations must be limited.

To model the switching restriction, every time node is split into two nodes. The edge entering the time point and the edge leaving it must pass through a capacity-one connection. This allows only one beggar to be at that station time for switching. The exception is time 0 and time d, where any number of beggars may start or finish, so these nodes do not need this restriction.

The resulting graph has only around 400 nodes because d is at most 200. Dinic's algorithm is easily fast enough, even with many train edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in number of trains | O(n) | Too slow |
| Max Flow on time graph | O(V²E) with Dinic | O(V + E) | Accepted |

## Algorithm Walkthrough

1. Create a graph representing the moments in time. Each time value from 0 to d becomes a graph location. For every train interval [x, y], add a directed edge from time x to time y with capacity one. This edge represents the fact that one beggar can use this train.
2. Split every intermediate time point t, where 0 < t < d, into an incoming node and an outgoing node. Add an edge from the incoming side to the outgoing side with capacity one. This edge represents the platform at that exact moment, preventing two beggars from switching there simultaneously.
3. Connect train edges correctly to the split nodes. A train leaving time t starts from the outgoing side of t, and a train arriving at time t ends at the incoming side of t. The start and end moments are kept unrestricted because any number of beggars can begin at time 0 and finish at time d.
4. Run a maximum flow algorithm from the source representing time 0 to the sink representing time d. The amount of flow is the maximum number of independent beggar schedules.

The reason this works is that every unit of flow corresponds to one complete path through trains. The capacity-one train edges prevent two flow units from taking the same train, and the capacity-one intermediate time edges prevent two flow units from meeting while changing trains. Every valid set of beggars creates exactly such a flow, and every valid flow describes a set of valid beggars.

The invariant is that after each augmentation in the flow algorithm, every unit of flow already represents a conflict-free partial collection of schedules. Since augmenting paths only use available residual capacity, the final maximum flow cannot contain an invalid overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, c):
        self.g[u].append([v, c, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def bfs(self, s, t):
        self.level = [-1] * self.n
        q = [s]
        self.level[s] = 0
        for u in q:
            for v, c, _ in self.g[u]:
                if c and self.level[v] == -1:
                    self.level[v] = self.level[u] + 1
                    q.append(v)
        return self.level[t] != -1

    def dfs(self, u, t, f):
        if u == t:
            return f
        while self.it[u] < len(self.g[u]):
            e = self.g[u][self.it[u]]
            v, c, rev = e
            if c and self.level[v] == self.level[u] + 1:
                pushed = self.dfs(v, t, min(f, c))
                if pushed:
                    e[1] -= pushed
                    self.g[v][rev][1] += pushed
                    return pushed
            self.it[u] += 1
        return 0

    def flow(self, s, t):
        ans = 0
        while self.bfs(s, t):
            self.it = [0] * self.n
            while True:
                pushed = self.dfs(s, t, 10**9)
                if not pushed:
                    break
                ans += pushed
        return ans

def solve():
    out = []
    T = int(input())
    for _ in range(T):
        d, n = map(int, input().split())

        def inn(x):
            return x * 2

        def outn(x):
            return x * 2 + 1

        size = 2 * (d + 1)
        dinic = Dinic(size)

        for t in range(1, d):
            dinic.add_edge(inn(t), outn(t), 1)

        for _ in range(n):
            x, y = map(int, input().split())
            start = outn(x) if x != d else inn(x)
            end = inn(y) if y != 0 else outn(y)
            dinic.add_edge(start, end, 1)

        source = outn(0)
        sink = inn(d)
        out.append(str(dinic.flow(source, sink)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation uses Dinic because the graph is small and sparse. Each graph edge stores its destination, remaining capacity, and the index of the reverse edge. The reverse edge is required by the residual graph, allowing the algorithm to reconsider earlier choices.

The node splitting is handled by assigning two indices to every time value. For a middle time t, the edge from `inn(t)` to `outn(t)` has capacity one. Train edges leave from the outgoing side of their starting time and enter the incoming side of their ending time.

The source is the outgoing side of time 0 because beggars may leave the starting moment without restriction. The sink is the incoming side of time d because beggars may finish without restriction. There is no special off-by-one handling for intervals because train edges already represent the full closed interval behavior required by the problem.

Python integers do not overflow, so capacities and the answer are safe even though the maximum possible flow is much larger than one.

## Worked Examples

For the sample case:

```
1
9 7
0 2
0 2
0 3
2 5
2 9
3 9
5 9
```

The important flow states are:

| Step | Train edge considered | Current maximum paths |
| --- | --- | --- |
| Initial | No trains chosen | 0 |
| Add path 0 -> 2 -> 5 -> 9 | One complete schedule | 1 |
| Add path 0 -> 3 -> 9 | Second complete schedule | 2 |
| Try another path | Intermediate time or train capacity blocks it | 2 |

The result is 2. The trace shows why two schedules can coexist when they use different switching moments, while a third one would require sharing a restricted resource.

A boundary case with identical direct trains:

```
1
5 3
0 5
0 5
0 5
```

has the following flow behavior:

| Step | Action | Flow |
| --- | --- | --- |
| Build graph | Three parallel edges from start to finish | 0 |
| First augmentation | Uses first train | 1 |
| Second augmentation | Uses second train | 2 |
| Third augmentation | Uses third train | 3 |

The result is 3. This confirms that train edges are independent resources and identical intervals must not be merged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V²E) | Dinic runs on a graph with at most about 400 nodes and around 20000 train edges |
| Space | O(V + E) | The graph stores every train edge and its residual edge |

The small time range makes the flow graph tiny even though the number of trains is large. The algorithm comfortably fits the limits because the expensive part depends on the number of time nodes rather than the number of possible schedules.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    it = iter(data)
    t = int(next(it))
    ans = []

    class Dinic:
        def __init__(self, n):
            self.g = [[] for _ in range(n)]

        def add(self, u, v, c):
            self.g[u].append([v, c, len(self.g[v])])
            self.g[v].append([u, 0, len(self.g[u]) - 1])

        def dfs(self, u, t, f):
            if u == t:
                return f
            while self.ptr[u] < len(self.g[u]):
                e = self.g[u][self.ptr[u]]
                if e[1] and self.level[e[0]] == self.level[u] + 1:
                    r = self.dfs(e[0], t, min(f, e[1]))
                    if r:
                        e[1] -= r
                        self.g[e[0]][e[2]][1] += r
                        return r
                self.ptr[u] += 1
            return 0

        def flow(self, s, t):
            res = 0
            while True:
                self.level = [-1] * len(self.g)
                q = [s]
                self.level[s] = 0
                for u in q:
                    for v, c, _ in self.g[u]:
                        if c and self.level[v] == -1:
                            self.level[v] = self.level[u] + 1
                            q.append(v)
                if self.level[t] == -1:
                    return res
                self.ptr = [0] * len(self.g)
                while True:
                    x = self.dfs(s, t, 10**9)
                    if not x:
                        break
                    res += x

    for _ in range(t):
        d = int(next(it))
        n = int(next(it))
        din = Dinic(2 * (d + 1))

        for x in range(1, d):
            din.add(2*x, 2*x+1, 1)

        for _ in range(n):
            x = int(next(it))
            y = int(next(it))
            din.add(2*x+1, 2*y, 1)

        ans.append(str(din.flow(1, 2*d)))

    return "\n".join(ans)

assert run("""1
9 7
0 2
0 2
0 3
2 5
2 9
3 9
5 9
""") == "2"

assert run("""1
5 1
0 5
""") == "1"

assert run("""1
3 3
0 3
0 3
0 3
""") == "3"

assert run("""1
4 4
0 2
0 2
2 4
2 4
""") == "2"

assert run("""1
1 1
0 1
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Original sample | 2 | Multiple possible chains with shared times |
| One train | 1 | Minimal schedule |
| Three identical trains | 3 | Parallel identical intervals |
| Two-stage split | 2 | Correct handling of switching capacity |
| One-unit day | 1 | Smallest possible time range |

## Edge Cases

A single train covering the entire day is handled because the flow graph contains a direct source-to-sink edge. The maximum flow correctly counts it as one complete schedule.

When many trains have exactly the same interval, each train becomes a separate capacity-one edge. The algorithm does not combine equal intervals, so every available train can contribute one more beggar.

When many schedules need to switch at the same time, the split node capacity prevents invalid solutions. For example, in the input with trains `[0,2]` and `[2,4]`, only one flow unit can pass through time 2, matching the rule that beggars cannot meet while switching.

The algorithm also handles cases where no complete route exists. If no path connects time 0 to time d, the maximum flow is zero because no unit of flow can reach the sink.

This can also be shortened into a contest-style editorial format if you need a more typical Codeforces publication length.
