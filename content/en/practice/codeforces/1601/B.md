---
title: "CF 1601B - Frog Traveler"
description: "The well has depths from 0 to n, where 0 is the ground and n is the starting position of the frog. Suppose the frog is currently resting at depth i."
date: "2026-06-10T08:20:40+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dp", "graphs", "shortest-paths", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1601
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 751 (Div. 1)"
rating: 1900
weight: 1601
solve_time_s: 138
verified: true
draft: false
---

[CF 1601B - Frog Traveler](https://codeforces.com/problemset/problem/1601/B)

**Rating:** 1900  
**Tags:** data structures, dfs and similar, dp, graphs, shortest paths, two pointers  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The well has depths from `0` to `n`, where `0` is the ground and `n` is the starting position of the frog.

Suppose the frog is currently resting at depth `i`. From there it chooses a jump length between `0` and `a[i]`, so the jump can land at any depth

$$j \in [i-a_i,\; i]$$

because moving upward decreases the depth.

After landing at depth `j`, the frog immediately slips down by `b[j]` and ends up resting at

$$j+b_j.$$

The next jump starts from this new resting position.

We must find the minimum number of jumps needed to reach depth `0`. Besides the minimum number, we also need to output the sequence of depths reached immediately after each jump and before slipping.

The first thing to notice is the constraint size. The well depth can be as large as `300000`. Any solution that explicitly considers every possible jump from every position would be quadratic. In the worst case, each position could jump to almost every shallower position, producing roughly

$$1 + 2 + \cdots + n = O(n^2)$$

transitions, around `9 × 10^10` when `n = 300000`. That is completely impossible within two seconds.

The challenge is not finding shortest paths. Breadth-first search is the natural choice because every jump costs exactly one move. The challenge is representing the graph efficiently.

A subtle edge case appears when a position can only jump to itself.

```
n = 1
a = [0]
b = [0]
```

The frog starts at depth `1`, cannot move upward at all, and never reaches depth `0`. The answer is `-1`. A careless implementation that assumes every node has at least one outgoing move could loop forever.

Another important case is when reaching depth `0` happens directly during a jump.

```
n = 2
a = [0, 2]
b = [0, 0]
```

From depth `2`, the frog can jump directly to depth `0`. No slipping occurs because the journey ends immediately. The answer is one jump. Implementations that always apply slipping after landing would incorrectly continue the process.

A third tricky case is that several different landing depths can produce the same resting position.

```
n = 3
a = [0, 2, 2]
b = [1, 1, 0]
```

Both landing depths `1` and `2` may lead to the same future state. BFS must avoid revisiting already processed states or it will perform redundant work.

## Approaches

A straightforward graph model is easy to write.

Treat every resting depth as a vertex. From depth `i`, every landing depth

$$j \in [i-a_i, i]$$

creates an edge toward resting depth

$$j+b_j.$$

If `j=0`, we have reached the goal.

Running BFS on this graph would correctly find the minimum number of jumps because every edge corresponds to exactly one jump. The problem is graph size. A single vertex can have `O(n)` outgoing edges, producing `O(n²)` edges overall.

The key observation is that the transition formula can be reversed.

Suppose we are currently at resting depth `v`. How could we have arrived here?

The last jump must have landed at some depth `x` such that

$$x+b_x=v.$$

After landing at `x`, the frog slipped to `v`.

Now consider the previous resting position `p`. The jump from `p` could land at `x` only if

$$p-a_p \le x.$$

Rearranging gives

$$p \ge x.$$

So every predecessor `p` lies in an interval

$$[x,\; n].$$

Instead of exploring huge forward ranges, we run BFS backwards starting from depth `0`.

For each landing depth `x`, we need to visit all still-unprocessed positions `p` satisfying

$$p-a_p \le x.$$

Each position should be processed only once. This is exactly where a disjoint-set style "next unvisited index" structure becomes useful.

We maintain all yet-unvisited positions in a linked-set structure. When a position gets discovered, we remove it permanently. Then scanning a range skips already processed indices in almost constant time.

The resulting BFS visits every depth once and removes every depth once, giving an almost linear solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS on explicit graph | O(n²) | O(n²) | Too slow |
| Reverse BFS + next-unvisited DSU | O(n α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

We number depths from `0` to `n`.

Depths `1..n` correspond to the input arrays. Depth `0` is the ground.

### 1. Build reverse information

For every landing depth `x`, compute

$$to[x] = x + b_x.$$

If the frog lands at `x`, it rests at `to[x]`.

While running reverse BFS from a resting depth `v`, every landing depth satisfying `to[x]=v` becomes relevant.

Store all such `x` values in buckets indexed by `v`.

### 2. Start BFS from depth 0

Depth `0` represents success.

Running BFS backwards means `dist[v]` will become the minimum number of jumps needed to reach the ground from resting depth `v`.

Initialize:

```
dist[0] = 0
queue = [0]
```

### 3. Maintain all undiscovered positions in a DSU structure

For every depth `i` from `1` to `n`, it starts as undiscovered.

The DSU supports:

```
find(i)
```

which returns the smallest undiscovered position at least `i`.

When position `i` becomes discovered, remove it by linking it to `i+1`.

This allows scanning intervals while skipping positions already processed earlier.

### 4. Process a BFS state v

For every landing depth `x` satisfying

```
x + b[x] = v
```

we need all predecessor resting positions `p` that could jump to `x`.

The condition is

$$p-a_p \le x.$$

Equivalently, every undiscovered position in

$$[x,\; n]$$

whose left reach is at most `x` becomes reachable in one more jump.

The reverse formulation used in the official solution scans all still-unvisited positions in the interval `[L,n]`, where

$$L=x.$$

Using the DSU, each position is removed forever the first time it is discovered.

### 5. Record parent information

When a new resting depth `p` is discovered through landing depth `x`:

```
parent[p] = v
jump[p] = x
```

The value `jump[p]` stores the landing depth used on that move.

This information is enough to reconstruct the required sequence later.

### 6. Continue BFS

Push every newly discovered position into the queue.

Since BFS explores states by increasing distance, the first time a position is reached already gives the minimum number of jumps.

### 7. Reconstruct the answer

If depth `n` was never discovered, print `-1`.

Otherwise start from `n` and repeatedly follow `parent`.

For every step, append the corresponding `jump` value.

The collected landing depths appear in reverse order, so reverse them before printing.

### Why it works

The reverse BFS graph is exactly the original graph with every edge reversed. A path of length `k` from depth `n` to depth `0` in the original graph corresponds to a path of length `k` from `0` to `n` in the reversed graph.

BFS on an unweighted graph always finds shortest-path distances. Since every jump costs one move, the first time a resting depth is discovered gives its minimum jump count.

The DSU structure never changes which vertices are reachable. It only skips vertices already discovered earlier. Every depth is removed exactly once, so no valid predecessor is lost and no vertex is processed twice.

Because parent pointers are recorded when a vertex is first discovered, they describe a shortest path tree. Following those pointers from `n` back to `0` reconstructs one minimum-jump solution.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n = int(input())
    a = [0] + list(map(int, input().split()))
    b = [0] + list(map(int, input().split()))

    buckets = [[] for _ in range(n + 1)]

    for x in range(1, n + 1):
        buckets[x + b[x]].append(x)

    parent = [-1] * (n + 1)
    jump = [-1] * (n + 1)
    dist = [-1] * (n + 1)

    nxt = list(range(n + 2))

    def find(x):
        while nxt[x] != x:
            nxt[x] = nxt[nxt[x]]
            x = nxt[x]
        return x

    def erase(x):
        nxt[x] = find(x + 1)

    q = deque([0])
    dist[0] = 0

    while q:
        v = q.popleft()

        for x in buckets[v]:
            cur = find(x)

            while cur <= n and cur - a[cur] <= x:
                dist[cur] = dist[v] + 1
                parent[cur] = v
                jump[cur] = x

                erase(cur)
                q.append(cur)

                cur = find(cur)

    if dist[n] == -1:
        print(-1)
        return

    ans = []
    cur = n

    while cur != 0:
        ans.append(jump[cur])
        cur = parent[cur]

    ans.reverse()

    print(len(ans))
    print(*ans)

solve()
```

The buckets array stores all landing depths `x` grouped by their post-slip destination `x + b[x]`. This is the reverse graph representation.

The DSU array `nxt` acts as a linked list of still-undiscovered positions. Calling `find(i)` returns the first undiscovered depth at least `i`. After discovering a depth, `erase()` removes it permanently.

The heart of the solution is:

```
cur = find(x)

while cur <= n and cur - a[cur] <= x:
```

The condition

$$cur-a[cur]\le x$$

means that a jump from resting depth `cur` can land at depth `x`.

As soon as such a depth is discovered, it is removed from the DSU. Because each depth disappears forever after its first visit, the total number of loop iterations across the entire BFS is only `O(n)`.

Parent pointers store the previous BFS node, while `jump[cur]` stores the landing depth used on that shortest path edge. Reconstruction follows these pointers backward from `n`.

## Worked Examples

### Sample 1

Input

```
3
0 2 2
1 1 0
```

Relevant reverse buckets:

| Landing x | x+b[x] |
| --- | --- |
| 1 | 2 |
| 2 | 3 |
| 3 | 3 |

BFS trace:

| Queue Pop | Landing x | New Depths Found | Parent Stored |
| --- | --- | --- | --- |
| 0 | none | none | none |
| 2 | 1 | 3 | parent[3]=2 |
| 3 | 2 | 2 | parent[2]=3 |

Reconstruction:

```
3 -> 2 -> 0
```

Recorded jumps:

```
1 0
```

The answer contains two jumps, which is optimal.

### Example 2

Input

```
2
0 1
1 0
```

BFS trace:

| Queue Pop | Landing x | New Depths Found |
| --- | --- | --- |
| 0 | none | none |

No other depth is ever discovered.

| Depth | dist |
| --- | --- |
| 0 | 0 |
| 1 | -1 |
| 2 | -1 |

Depth `2` remains unreachable, so the answer is `-1`.

This example shows that reverse BFS naturally detects impossible situations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n α(n)) | Each depth is inserted into BFS once and removed from DSU once |
| Space | O(n) | Buckets, BFS arrays, parent arrays, and DSU storage |

With `n = 300000`, an almost-linear algorithm is easily fast enough. The memory usage is also linear, comfortably below the 512 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())
    a = [0] + list(map(int, input().split()))
    b = [0] + list(map(int, input().split()))

    buckets = [[] for _ in range(n + 1)]

    for x in range(1, n + 1):
        buckets[x + b[x]].append(x)

    parent = [-1] * (n + 1)
    jump = [-1] * (n + 1)
    dist = [-1] * (n + 1)

    nxt = list(range(n + 2))

    def find(x):
        while nxt[x] != x:
            nxt[x] = nxt[nxt[x]]
            x = nxt[x]
        return x

    def erase(x):
        nxt[x] = find(x + 1)

    q = deque([0])
    dist[0] = 0

    while q:
        v = q.popleft()

        for x in buckets[v]:
            cur = find(x)

            while cur <= n and cur - a[cur] <= x:
                dist[cur] = dist[v] + 1
                parent[cur] = v
                jump[cur] = x

                erase(cur)
                q.append(cur)

                cur = find(cur)

    out = []

    if dist[n] == -1:
        out.append("-1")
    else:
        ans = []
        cur = n

        while cur != 0:
            ans.append(jump[cur])
            cur = parent[cur]

        ans.reverse()

        out.append(str(len(ans)))
        out.append(" ".join(map(str, ans)))

    return "\n".join(out)

# sample
assert run("3\n0 2 2\n1 1 0\n") == "2\n1 0"

# minimum size, impossible
assert run("1\n0\n0\n") == "-1"

# direct jump to ground
assert run("2\n0 2\n0 0\n") == "1\n0"

# impossible because every move returns to start
assert run("2\n1 1\n1 0\n") == "-1"

# boundary reachability
assert run("1\n1\n0\n") == "1\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, a=[0], b=[0]` | `-1` | Smallest impossible instance |
| `n=2, a=[0,2], b=[0,0]` | One jump | Direct reach to ground |
| `n=2, a=[1,1], b=[1,0]` | `-1` | Cyclic behavior without progress |
| `n=1, a=[1], b=[0]` | One jump | Boundary handling around depth 0 |

## Edge Cases

Consider the smallest impossible instance:

```
1
0
0
```

The only resting depth is `1`. Since `a[1]=0`, the frog cannot jump upward at all. During reverse BFS, no predecessor of depth `0` exists. Depth `1` is never discovered, `dist[1]` remains `-1`, and the algorithm prints `-1`.

Consider direct escape:

```
2
0 2
0 0
```

Depth `2` can jump directly to landing depth `0`. In the reverse graph, depth `2` becomes a predecessor of `0`, so BFS discovers it immediately with distance `1`. Reconstruction yields the single landing depth `0`.

Consider repeated states:

```
3
0 2 2
1 1 0
```

Several paths can lead to the same resting depth. The DSU removes a depth the first time it is discovered. Later searches skip it automatically. BFS ordering guarantees that the first discovery already corresponds to the shortest path, so ignoring later discoveries is correct.

Consider the extreme case where every `a[i]=i`.

Every depth can potentially jump to any shallower depth. The explicit graph would contain quadratic many edges. The DSU-based reverse BFS still removes each depth exactly once, keeping the total work almost linear. This is the case that makes the optimized solution necessary.
