---
title: "CF 102428I - Improve SPAM"
description: "Think of every mailing list as a vertex in a directed graph. When mailing list i contains mailing list j, draw an edge from i to j. Client emails are terminal vertices."
date: "2026-08-12T07:20:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102428
codeforces_index: "I"
codeforces_contest_name: "2019-2020 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 102428
solve_time_s: 107
verified: true
draft: false
---

[CF 102428I - Improve SPAM](https://codeforces.com/problemset/problem/102428/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of every mailing list as a vertex in a directed graph. When mailing list `i` contains mailing list `j`, draw an edge from `i` to `j`. Client emails are terminal vertices. Sending a message to a mailing list means following every outgoing choice, so the same client can be reached along many different paths.

The creation rule gives this graph a crucial property: mailing lists form a DAG. A list can only be inserted into lists that already existed, and lists are created one at a time, so following list-to-list edges always moves forward or backward through creation time without ever returning to an already existing list. The numerical address of a list does not represent its creation time, so we cannot assume that an edge goes from a smaller index to a larger index.

The first answer, `B`, counts every delivery separately. If a client can be reached through three different paths, that client contributes three to `B`. The second answer, `A`, counts each reachable client only once. Thus `A` is simply the number of distinct client addresses reachable from mailing list `1`.

There are at most `1000` mailing lists and `2000` total addresses. A list can contain almost every address, so the total number of membership entries can approach `L(N-1)`, which is just under two million. That rules out algorithms that repeatedly expand the same sublists or enumerate all possible paths. A linear or near-linear graph algorithm is appropriate for these bounds.

There are several easy cases where a careless implementation gives the wrong result. First, the same client can be reached through two different branches. For example,

```
4 3
2 2 3
1 4
1 4
```

Here mailing list `1` reaches client `4` through both lists `2` and `3`. The ordinary system sends two messages, while the improved system sends one, so the answer is `2 1`. A solution that merely counts distinct addresses appearing directly in list `1` misses the duplicate.

A second trap is that a client can occur both directly and through another list:

```
4 2
2 2 3
1 3
```

List `1` contains list `2` and client `3`, while list `2` also contains client `3`. The ordinary delivery count is `2`, but only one distinct client exists, so the answer is `2 1`. A solution that only removes duplicate entries inside each individual list still overcounts.

The third trap is assuming list indices describe creation order. Consider

```
3 2
1 2
1 3
```

List `1` contains list `2`, and list `2` contains client `3`. The correct answer is `1 1`. A DP that processes lists in numerical order tries to calculate list `1` before list `2`, even though list `1` depends on it. The graph must be topologically ordered instead.

## Approaches

The direct brute-force simulation follows the mailing-list hierarchy exactly as the real system does. Whenever it encounters a client, it increments the delivery count, and whenever it encounters another mailing list, it recursively processes that list. This is correct because every occurrence of a mailing list represents another independent traversal, exactly as in the original system.

The problem is that the same subgraph can be expanded over and over. Consider mailing lists arranged as a complete DAG, with list `1` pointing to every later list, list `2` pointing to every later list, and so on. Put one client email in the final list. Every subset of the intermediate lists gives a different path from list `1` to that final email. With `L` lists, this creates `2^(L-2)` deliveries to the same client. At `L = 1000`, that is `2^998` recursive leaf visits, far beyond anything that can be executed.

The observation that fixes this is that the graph is a DAG, so the effect of every mailing list can be calculated once and reused. Define `ways[i]` as the number of client deliveries produced when mailing list `i` is processed. For a client directly inside the list, we add one. For another mailing list `j`, we add `ways[j]`. Once all children have been calculated, `ways[i]` is known regardless of how many different paths eventually reach `i`.

The duplicate-free answer is even simpler. We do not need to construct the set of reachable clients for every list. Starting from list `1`, run a graph traversal and mark every address as soon as it is encountered. A mailing list is processed only the first time it is reached, and a client is counted only the first time it is reached. This directly models the improved behavior.

The only structural detail we need before the DP is a topological ordering of the mailing-list graph. Kahn's algorithm gives an order from parents toward children. Reversing that order guarantees that every list referenced by `i` has already been evaluated when we calculate `ways[i]`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of expanded paths) | O(L) recursion depth | Too slow |
| Optimal | O(N + E) | O(N + E) | Accepted |

Here `E` denotes the total number of membership entries. The brute-force complexity is not polynomial because the number of paths can be exponential in `L`.

## Algorithm Walkthrough

1. Read every mailing list and store its members. For every member that is another mailing list, add a directed edge from the current list to that member and increase the member's indegree. Keeping the complete membership lists is useful because the same representation will later be used both by the DP and by the duplicate-free traversal.
2. Run Kahn's topological sort on the mailing-list graph. Start with every list whose indegree is zero, repeatedly remove one such list, and decrease the indegree of its children. The creation rule guarantees that the graph is acyclic, so every mailing list eventually appears in the ordering.
3. Reverse the topological order. If `i -> j` means that list `i` contains list `j`, then `j` must be evaluated before `i`. The reversed order gives exactly that dependency direction.
4. Process mailing lists in the reversed order and calculate `ways[i]`. For every direct client in list `i`, add `1`. For every mailing list `j` in list `i`, add `ways[j]`. Take the result modulo `10^9 + 7`. Since every referenced list has already been processed, no recursive expansion is necessary.
5. Starting from mailing list `1`, perform a DFS or BFS over all addresses. Maintain one `seen` array covering both mailing lists and client addresses. When a previously unseen client is reached, mark it and increment `A`. When a previously unseen mailing list is reached, mark it and put it into the traversal queue.
6. Output `ways[1]` and the number of distinct clients reached by the traversal. The first value counts every path separately, while the second counts each address at most once.

### Why it works

For the first answer, the invariant is that after processing list `i`, `ways[i]` equals exactly the number of client-delivery paths starting at `i`. Every direct client contributes one path, and every contained mailing list contributes all paths beginning from that child list. Since the reversed topological order processes every child first, the recurrence accounts for every possible delivery exactly once.

For the second answer, the invariant is that an address is processed at most once. Every client reachable from list `1` is eventually encountered by the traversal, so every reachable client contributes exactly one to `A`. If several paths reach the same client, its `seen` entry is already set when the later paths encounter it, so no duplicate is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    input = sys.stdin.readline

    n, l = map(int, input().split())

    members = [[] for _ in range(l)]
    graph = [[] for _ in range(l)]
    indegree = [0] * l

    for i in range(l):
        data = list(map(int, input().split()))
        k = data[0]
        cur = [x - 1 for x in data[1:k + 1]]
        members[i] = cur

        for x in cur:
            if x < l:
                graph[i].append(x)
                indegree[x] += 1

    # Topological order of the mailing-list DAG.
    queue = []
    head = 0

    for i in range(l):
        if indegree[i] == 0:
            queue.append(i)

    topo = []

    while head < len(queue):
        u = queue[head]
        head += 1
        topo.append(u)

        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    # Children must be evaluated before parents.
    ways = [0] * l

    for u in reversed(topo):
        total = 0

        for x in members[u]:
            if x < l:
                total += ways[x]
            else:
                total += 1

        ways[u] = total % MOD

    # Count distinct client emails reachable from list 1.
    seen = [False] * n
    seen[0] = True

    queue = [0]
    head = 0
    distinct_clients = 0

    while head < len(queue):
        u = queue[head]
        head += 1

        for x in members[u]:
            if seen[x]:
                continue

            seen[x] = True

            if x < l:
                queue.append(x)
            else:
                distinct_clients += 1

    return f"{ways[0]} {distinct_clients}"

if __name__ == "__main__":
    print(solve())
```

The input is stored in `members`, using zero-based addresses. A value smaller than `l` is a mailing list, while a value at least `l` is a client address. This is why the condition is `x < l`, rather than `x <= l`.

The `graph` array contains only list-to-list edges. It is separate from `members` because topological sorting needs only those edges, while the DP needs to distinguish both list and client members.

The indegree array belongs to Kahn's algorithm. After the topological ordering is built, it is no longer needed, so the same memory is not duplicated.

The DP iterates over `reversed(topo)`. This direction is easy to get wrong. If list `u` contains list `v`, the graph contains `u -> v`, so ordinary topological order puts `u` before `v`. The DP needs the opposite order, with `v` before `u`.

Python integers do not overflow, but the modulo operation is still necessary because the required answer is modulo `10^9 + 7`. The modulo is performed once after computing each list, which is sufficient because the intermediate sum is bounded by the number of members times `MOD`.

For the duplicate-free traversal, one `seen` array is enough for both kinds of addresses. A seen mailing list is never expanded again, and a seen client is never counted again. This is exactly the distinction between counting paths for `B` and counting reachable vertices for `A`.

## Worked Examples

### Sample 1

The mailing-list edges are `1 -> 2`, `1 -> 3`, and `3 -> 2`. Kahn's algorithm can produce the order `1, 3, 2`, so the DP processes `2, 3, 1`.

| List | Members | `ways` after processing | Reachable clients |
| --- | --- | --- | --- |
| 2 | 4, 5 | 2 | 4, 5 |
| 3 | 4, 2 | 3 | 4, 5 |
| 1 | 2, 3 | 5 | 4, 5 |

List `2` directly sends to clients `4` and `5`, giving `ways[2] = 2`. List `3` sends directly to `4` and then processes list `2`, so `ways[3] = 1 + 2 = 3`. Finally, list `1` processes both lists, giving `2 + 3 = 5`.

The reachability traversal sees clients `4` and `5` once each. Client `4` is encountered through both lists `2` and `3`, but `seen[4]` prevents the second encounter from increasing the answer. The result is `5 2`.

### Sample 2

The relevant mailing-list edges are `1 -> 6`, `3 -> 6`, `3 -> 4`, `3 -> 5`, `5 -> 4`, `6 -> 5`, and `6 -> 4`. One valid topological order is `1, 2, 3, 6, 5, 4`, so the DP uses the reverse order.

| List | Members relevant to DP | `ways` |
| --- | --- | --- |
| 4 | 14, 15 | 2 |
| 5 | 6? no, actually 4, 14 | 3 |
| 6 | 5, 4 | 5 |
| 3 | 6, 14, 4, 5, 15 | 12 |
| 2 | 10, 11, 12, 13, 9, 7, 8 | 7 |
| 1 | 6 | 5 |

List `4` directly contains clients `14` and `15`, so it produces two messages. List `5` contains list `4` and client `14`, producing `2 + 1 = 3`. List `6` contains lists `5` and `4`, producing `3 + 2 = 5`. Since list `1` contains only list `6`, `B = 5`.

For the improved system, traversing from list `1` reaches list `6`, then lists `5` and `4`, and ultimately only clients `14` and `15`. Both paths to those clients collapse into one delivery per address, giving `A = 2`.

## Complexity Analysis

Let `E` be the total number of membership entries across all mailing lists.

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + E) | Topological sorting, DP, and the reachability traversal each inspect every stored membership a constant number of times |
| Space | O(N + E) | The membership lists, mailing-list graph, indegrees, DP values, queue, and visited array are all linear in the input size |

The maximum possible `E` is below `L(N-1)`, which is below two million under the given constraints. Every membership is inspected only a constant number of times, so the algorithm stays within the intended scale even for dense mailing-list structures.

## Test Cases

```python
import sys
import io

MOD = 1_000_000_007

def solve():
    input = sys.stdin.readline

    n, l = map(int, input().split())

    members = [[] for _ in range(l)]
    graph = [[] for _ in range(l)]
    indegree = [0] * l

    for i in range(l):
        data = list(map(int, input().split()))
        k = data[0]
        cur = [x - 1 for x in data[1:k + 1]]
        members[i] = cur

        for x in cur:
            if x < l:
                graph[i].append(x)
                indegree[x] += 1

    queue = []
    head = 0

    for i in range(l):
        if indegree[i] == 0:
            queue.append(i)

    topo = []

    while head < len(queue):
        u = queue[head]
        head += 1
        topo.append(u)

        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    ways = [0] * l

    for u in reversed(topo):
        total = 0
        for x in members[u]:
            if x < l:
                total += ways[x]
            else:
                total += 1
        ways[u] = total % MOD

    seen = [False] * n
    seen[0] = True

    queue = [0]
    head = 0
    distinct_clients = 0

    while head < len(queue):
        u = queue[head]
        head += 1

        for x in members[u]:
            if seen[x]:
                continue

            seen[x] = True

            if x < l:
                queue.append(x)
            else:
                distinct_clients += 1

    return f"{ways[0]} {distinct_clients}"

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

sample1 = """\
5 3
2 2 3
2 4 5
2 4 2
"""

sample2 = """\
15 6
1 6
7 10 11 12 13 9 7 8
5 6 14 4 5 15
2 14 15
2 4 14
2 5 4
"""

sample3 = """\
10 5
4 8 9 10 3
3 9 10 6
3 8 9 7
6 2 3 6 7 8 10
5 9 10 3 1 7
"""

assert run(sample1) == "5 2", "sample 1"
assert run(sample2) == "5 2", "sample 2"
assert run(sample3) == "6 4", "sample 3"

# Minimum-size instance.
assert run("""\
2 1
1 2
""") == "1 1", "minimum-size case"

# Same client reached through two different lists.
assert run("""\
4 3
2 2 3
1 4
1 4
""") == "2 1", "duplicate through two branches"

# Same client appears directly and through a nested list.
assert run("""\
4 2
2 2 3
1 3
""") == "2 1", "direct plus indirect duplicate"

# Many paths to the same client.
assert run("""\
8 4
4 2 3 4 8
3 3 4 8
2 4 8
1 8
""") == "8 1", "exponential path structure"

# Maximum N and maximum L, with the boundary client N appearing.
n = 2000
l = 1000
lines = [f"{n} {l}"]
for i in range(l):
    lines.append(f"1 {l + i + 1}")

max_case = "\n".join(lines) + "\n"
assert run(max_case) == "1 1", "maximum-size boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 2` | `1 1` | Minimum values and the first client address |
| `4 3 / 2 2 3 / 1 4 / 1 4` | `2 1` | The same client reached through separate branches |
| `4 2 / 2 2 3 / 1 3` | `2 1` | A client reached both directly and indirectly |
| `8 4 / 4 2 3 4 8 / 3 3 4 8 / 2 4 8 / 1 8` | `8 1` | Many distinct paths ending at one client |
| `N=2000, L=1000`, each list contains its own boundary client | `1 1` | Maximum sizes and address `N` |

## Edge Cases

The first edge case is duplicate reachability through different branches. For

```
4 3
2 2 3
1 4
1 4
```

the topological DP calculates `ways[2] = 1` and `ways[3] = 1`, so `ways[1] = 2`. During the reachability traversal, list `2` discovers client `4` first. When list `3` is processed, `seen[4]` is already true, so the client is not counted again. The output is `2 1`.

The second edge case is a duplicate caused by direct and nested membership. For

```
4 2
2 2 3
1 3
```

list `2` produces one delivery to client `3`. List `1` also contains client `3` directly, so `ways[1] = 2`. The traversal reaches `3` directly from list `1` and then encounters it again through list `2`, but the second occurrence is ignored. The output is `2 1`.

The third edge case is the mismatch between numerical address order and dependency order:

```
3 2
1 2
1 3
```

The graph contains `1 -> 2`, and list `2` contains client `3`. Kahn's algorithm places list `1` before list `2`, then the reversed order evaluates list `2` first. Thus `ways[2] = 1`, followed by `ways[1] = 1`. The traversal from list `1` also reaches client `3`, giving `1 1`. A numeric-index DP would fail because it would try to use `ways[2]` before calculating it.

The final structural edge case is a graph with exponentially many paths to the same client:

```
8 4
4 2 3 4 8
3 3 4 8
2 4 8
1 8
```

There are eight different paths from list `1` to client `8`, so `B = 8`. The improved traversal sees client `8` once and gives `A = 1`. The DP handles all eight paths by calculating each list once, rather than explicitly traversing those eight paths. This is the property that makes the algorithm scale to the much larger maximum case.
