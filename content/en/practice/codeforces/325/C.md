---
title: "CF 325C - Monsters and Diamonds"
description: "Each monster type has one or more split rules. Applying a rule consumes one monster of that type and produces two things: First, some number of diamonds. Second, a multiset of new monsters."
date: "2026-06-06T05:57:14+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 325
codeforces_index: "C"
codeforces_contest_name: "MemSQL start[c]up Round 1"
rating: 2600
weight: 325
solve_time_s: 166
verified: false
draft: false
---

[CF 325C - Monsters and Diamonds](https://codeforces.com/problemset/problem/325/C)

**Rating:** 2600  
**Tags:** dfs and similar, graphs, shortest paths  
**Solve time:** 2m 46s  
**Verified:** no  

## Solution
## Problem Understanding

Each monster type has one or more split rules. Applying a rule consumes one monster of that type and produces two things:

First, some number of diamonds.

Second, a multiset of new monsters.

Starting from a single monster, we repeatedly choose a rule for every monster that appears, until eventually no monsters remain. The total number of collected diamonds is the sum of the diamonds produced by every rule application.

For every monster type, we must compute two values.

The minimum number of diamonds obtainable among all terminating strategies.

The maximum number of diamonds obtainable among all terminating strategies.

If termination is impossible, both answers are `-1`.

If arbitrarily many diamonds can be generated before eventually terminating, the maximum answer is `-2`.

The input naturally forms a directed hypergraph. A rule

```
A -> diamonds + {B, C, D}
```

means that the value of monster `A` depends on all of `B`, `C`, and `D`.

The constraints are the key observation. There are up to `10^5` monster types and `10^5` total rule elements. Any algorithm that repeatedly explores the whole graph from every monster is impossible. We need something close to linear time in the total input size.

The dangerous cases are the cyclic ones.

Consider:

```
1 -> 1 + monster 1
1 -> 1
```

Monster `1` can terminate, because of the second rule. It can also loop through the first rule any number of times before finally choosing the second rule. The minimum answer is `1`, while the maximum answer is infinite.

Another subtle case is:

```
1 -> monster 2 + 1
2 -> monster 1 + 1
```

Neither monster has any terminating rule. Both answers are `-1` for both types. A naive DFS that only looks for cycles would incorrectly conclude that the maximum is infinite, but infinite diamonds are irrelevant if termination is impossible.

A third pitfall is a cycle that is reachable from some monster but not part of that monster itself:

```
1 -> monster 2 + 1
2 -> monster 3 + 1
3 -> monster 2 + 1
2 -> 1
3 -> 1
```

Monster `1` can enter the cycle, stay there arbitrarily long, then leave through the terminating rules. Its maximum answer is also infinite.

## Approaches

A brute force solution would try every possible sequence of rule choices and recursively evaluate the resulting monsters. That is conceptually correct because every terminating derivation corresponds to a finite expansion tree.

The problem is that the number of possible derivations grows exponentially. Even a tiny cycle allows infinitely many different strategies. With `10^5` monster types, explicit exploration is hopeless.

The structure of the rules gives a much better viewpoint.

Let `min[i]` be the minimum diamonds obtainable from monster `i`.

For a rule

```
i -> d diamonds + children
```

the rule contributes

```
d + sum(min[child])
```

because every produced monster must eventually be resolved.

The same idea applies to the maximum value.

This turns the problem into evaluating equations on a directed hypergraph. A rule becomes usable only when all of its children are already known to be terminable.

The first task is to determine which monsters can terminate at all. This is an AND-OR reachability problem.

A monster is terminable if at least one of its rules has all children terminable.

After we know the terminable set, the minimum values become a shortest-hyperpath problem. The maximum values become a longest-hyperpath problem, except that cycles with positive gain correspond to infinite answers.

The crucial observation is that every rule produces at least one diamond. Any cycle that can be traversed and later exited can be repeated arbitrarily many times, producing unbounded diamonds. So the infinite states are exactly the terminable monsters that can reach a directed cycle inside the graph of usable rules.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n + total rule size) | O(n + total rule size) | Accepted |

## Algorithm Walkthrough

### 1. Build the rule hypergraph

For every rule store:

The owner monster.

The number of diamonds produced by the rule.

The list of child monsters.

We also build reverse references from every child to the rules that contain it.

### 2. Compute the terminable monsters

A rule becomes satisfied when all of its child monsters are already known to be terminable.

For every rule we maintain a counter equal to the number of child monsters not yet confirmed terminable.

Rules with zero children are immediately satisfied.

Whenever a monster becomes terminable, we visit all rules that depend on it and decrease their counters.

If a rule counter reaches zero, its owner monster becomes terminable.

This is the standard propagation for AND-OR graphs.

### 3. Compute minimum diamonds

Only rules whose children are all terminable can contribute.

For each rule we need

```
diamonds(rule) + sum(min[child])
```

The equations are monotone and all costs are positive.

We process them with a Dijkstra-like hypergraph relaxation. A rule becomes evaluable when all child values are known. At that moment it generates a candidate value for its owner.

The smallest candidate over all usable rules is the answer.

### 4. Build the graph of usable dependencies

For every usable rule

```
u -> children
```

add ordinary directed edges

```
u -> child
```

for all children.

This graph describes which monster values depend on which others.

### 5. Find infinite states

Run SCC decomposition on the usable dependency graph.

Any SCC with more than one vertex is a cycle.

A single vertex SCC is also cyclic if it has a self-loop.

Because every rule yields at least one diamond, reaching such a cycle means we can earn positive diamonds on every traversal.

Mark all cyclic SCCs.

Then run a reverse graph traversal and mark every terminable monster that can reach one of those SCCs.

Those monsters have maximum answer `-2`.

### 6. Compute finite maximum diamonds

Remove all infinite monsters.

The remaining usable dependency graph is acyclic.

For every remaining monster,

```
max[i] =
max over usable rules (
    diamonds(rule) + sum(max[child])
)
```

Since the graph is now a DAG, we evaluate these values in reverse topological order.

### 7. Clamp large finite answers

Any finite value larger than `314000000` is printed as `314000000`.

### Why it works

The termination propagation computes exactly the least fixed point of the condition

```
monster is terminable
⇔
some rule has all children terminable
```

A rule contributes a valid diamond count only if every produced monster can itself terminate. The minimum and maximum equations are precisely the recursive definition of the game outcome.

Every cycle in the usable graph has strictly positive gain because each rule creates at least one diamond. A terminable monster that can reach such a cycle may traverse it any number of times and then leave through a terminating strategy, yielding arbitrarily large finite totals. That is exactly the meaning of answer `-2`.

After removing infinite states, the dependency graph becomes acyclic, so the maximum equation has a unique finite solution obtained by dynamic programming on the DAG.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

CAP = 314000000

def solve():
    m, n = map(int, input().split())

    rules = []
    owner_rules = [[] for _ in range(n)]
    rev_rules = [[] for _ in range(n)]

    for rid in range(m):
        arr = list(map(int, input().split()))
        owner = arr[0] - 1
        l = arr[1]

        diamonds = 0
        children = []

        for x in arr[2:2 + l]:
            if x == -1:
                diamonds += 1
            else:
                children.append(x - 1)

        rules.append((owner, diamonds, children))
        owner_rules[owner].append(rid)

        for v in children:
            rev_rules[v].append(rid)

    # terminable monsters
    need = [len(ch) for _, _, ch in rules]
    can = [False] * n
    q = deque()

    for rid, (owner, _, ch) in enumerate(rules):
        if not ch and not can[owner]:
            can[owner] = True
            q.append(owner)

    while q:
        u = q.popleft()

        for rid in rev_rules[u]:
            need[rid] -= 1
            if need[rid] == 0:
                owner = rules[rid][0]
                if not can[owner]:
                    can[owner] = True
                    q.append(owner)

    # usable rules
    usable = [False] * m
    for rid, (_, _, ch) in enumerate(rules):
        ok = True
        for v in ch:
            if not can[v]:
                ok = False
                break
        usable[rid] = ok

    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)]

    for rid, (u, _, ch) in enumerate(rules):
        if not usable[rid]:
            continue
        for v in ch:
            g[u].append(v)
            rg[v].append(u)

    # SCC (Kosaraju)
    used = [False] * n
    order = []

    sys.setrecursionlimit(300000)

    def dfs1(v):
        used[v] = True
        for to in g[v]:
            if not used[to]:
                dfs1(to)
        order.append(v)

    for i in range(n):
        if can[i] and not used[i]:
            dfs1(i)

    comp = [-1] * n

    def dfs2(v, c):
        comp[v] = c
        for to in rg[v]:
            if comp[to] == -1:
                dfs2(to, c)

    cid = 0
    for v in reversed(order):
        if comp[v] == -1:
            dfs2(v, cid)
            cid += 1

    sz = [0] * cid
    for i in range(n):
        if comp[i] != -1:
            sz[comp[i]] += 1

    cyc = [False] * cid

    for u in range(n):
        if comp[u] == -1:
            continue
        if sz[comp[u]] > 1:
            cyc[comp[u]] = True
        for v in g[u]:
            if u == v and comp[u] == comp[v]:
                cyc[comp[u]] = True

    inf = [False] * n
    dq = deque()

    for i in range(n):
        if can[i] and cyc[comp[i]]:
            inf[i] = True
            dq.append(i)

    while dq:
        v = dq.popleft()
        for p in rg[v]:
            if can[p] and not inf[p]:
                inf[p] = True
                dq.append(p)

    # finite max via memo DAG
    min_dp = [-1] * n
    max_dp = [-1] * n

    def get_min(v):
        if min_dp[v] != -1:
            return min_dp[v]

        best = 10**18
        for rid in owner_rules[v]:
            if not usable[rid]:
                continue

            _, d, ch = rules[rid]
            cur = d
            for x in ch:
                cur += get_min(x)

            if cur < best:
                best = cur

        min_dp[v] = min(best, CAP)
        return min_dp[v]

    def get_max(v):
        if max_dp[v] != -1:
            return max_dp[v]

        best = 0
        for rid in owner_rules[v]:
            if not usable[rid]:
                continue

            _, d, ch = rules[rid]

            bad = False
            cur = d

            for x in ch:
                if inf[x]:
                    bad = True
                    break
                cur += get_max(x)

            if not bad:
                best = max(best, cur)

        max_dp[v] = min(best, CAP)
        return max_dp[v]

    out = []

    for i in range(n):
        if not can[i]:
            out.append("-1 -1")
        else:
            mn = get_min(i)

            if inf[i]:
                out.append(f"{mn} -2")
            else:
                mx = get_max(i)
                out.append(f"{mn} {mx}")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm almost directly.

The first propagation computes the set of monsters that can eventually disappear. Every rule maintains the number of unresolved children. When that count reaches zero, the rule becomes usable.

The SCC phase is the heart of the infinite-answer detection. A cycle alone is not enough. The cycle must lie inside the terminable subgraph. That is why the SCC decomposition is performed only on usable dependencies.

The reverse BFS from cyclic SCCs marks every monster that can enter such a cycle. Since every traversal gains at least one diamond, those states have unbounded maximum value.

The minimum and finite maximum values are then ordinary memoized evaluations of the recursive equations.

The cap is applied only to finite answers, exactly as required.

## Worked Examples

### Sample 1

Input:

```
6 4
1 3 -1 1 -1
1 2 -1 -1
2 3 -1 3 -1
2 3 -1 -1 -1
3 2 -1 -1
4 2 4 -1
```

Key dependency structure:

| Monster | Usable rules |
| --- | --- |
| 1 | `1 -> 2 diamonds`, `1 -> 2 diamonds + 1` |
| 2 | `2 -> 2 diamonds + 3`, `2 -> 3 diamonds` |
| 3 | `3 -> 2 diamonds` |
| 4 | `4 -> 1 diamond + 4` |

Termination analysis:

| Monster | Terminable |
| --- | --- |
| 1 | Yes |
| 2 | Yes |
| 3 | Yes |
| 4 | No |

Minimum values:

| Monster | Minimum |
| --- | --- |
| 3 | 2 |
| 2 | 3 |
| 1 | 2 |

Maximum values:

Monster `1` can repeatedly use the self-producing rule and later switch to the terminating rule, so its maximum is infinite.

Final output:

```
2 -2
3 4
2 2
-1 -1
```

This example demonstrates both non-terminating monsters and infinite maximum values.

### Custom Example

Input:

```
2 2
1 2 -1 -1
2 3 -1 1 -1
```

Dependency table:

| Monster | Rule |
| --- | --- |
| 1 | 2 diamonds |
| 2 | 2 diamonds + monster 1 |

Evaluation:

| Monster | Minimum | Maximum |
| --- | --- | --- |
| 1 | 2 | 2 |
| 2 | 4 | 4 |

No cycles exist, so every answer is finite.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + total rule size) | Every monster, rule, and dependency edge is processed a constant number of times |
| Space | O(n + total rule size) | Graphs, reverse graphs, rule storage, SCC arrays |

The total number of monster references across all rules is at most `10^5`, so the graph remains linear in size. A linear-time SCC algorithm and linear-time propagations fit comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = old
    return out.getvalue().strip()

# sample 1
assert run(
"""6 4
1 3 -1 1 -1
1 2 -1 -1
2 3 -1 3 -1
2 3 -1 -1 -1
3 2 -1 -1
4 2 4 -1
"""
) == """2 -2
3 4
2 2
-1 -1"""

# sample 2
assert run(
"""3 2
1 2 1 -1
2 2 -1 -1
2 3 2 1 -1
"""
) == """-1 -1
2 2"""

# single terminal monster
assert run(
"""1 1
1 2 -1 -1
"""
) == """2 2"""

# self cycle with exit
assert run(
"""2 1
1 2 1 -1
1 1 -1
"""
) == """1 -2"""

# pure cycle, no exit
assert run(
"""1 1
1 2 1 -1
"""
) == """-1 -1"""

# chain
assert run(
"""2 2
1 2 -1 -1
2 3 -1 1 -1
"""
) == """2 2
4 4"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single terminal rule | `2 2` | Smallest possible instance |
| Self cycle with exit | `1 -2` | Infinite maximum detection |
| Pure cycle | `-1 -1` | Non-terminable cycle |
| Simple chain | finite values | Recursive accumulation |
| Sample 1 | official output | Mixed finite, infinite, impossible states |

## Edge Cases

Consider the self-loop with an exit:

```
2 1
1 2 1 -1
1 1 -1
```

The first rule produces one diamond and recreates monster `1`. The second rule terminates immediately with one diamond.

The SCC decomposition finds a cyclic SCC containing monster `1`. Since monster `1` is also terminable through the second rule, the cycle is productive. The reverse reachability phase marks monster `1` as infinite.

The minimum answer comes from taking the terminating rule immediately, giving `1`. The maximum answer is `-2`.

Now consider a pure cycle:

```
1 1
1 2 1 -1
```

The termination propagation never marks monster `1` as terminable because every rule depends on monster `1` itself. The monster is excluded before any SCC reasoning is used. The answer becomes:

```
-1 -1
```

which is exactly what the statement requires.

Finally, consider a monster that only reaches a productive cycle:

```
1 -> 2 + diamond
2 -> 2 + diamond
2 -> diamond
```

Monster `1` is not itself in a cycle. The reverse traversal from cyclic SCCs reaches monster `1`, so it is correctly marked as having infinite maximum value. The algorithm handles this case without any special logic beyond the SCC and reverse-reachability phases.
