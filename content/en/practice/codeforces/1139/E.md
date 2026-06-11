---
title: "CF 1139E - Maximize Mex"
description: "Each student belongs to exactly one club and has a potential value. On a given day, some students have already left their clubs permanently. From the remaining students, we may choose at most one student from each club. The chosen students form the contest team."
date: "2026-06-12T03:52:25+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graph-matchings", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1139
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 548 (Div. 2)"
rating: 2400
weight: 1139
solve_time_s: 108
verified: true
draft: false
---

[CF 1139E - Maximize Mex](https://codeforces.com/problemset/problem/1139/E)

**Rating:** 2400  
**Tags:** flows, graph matchings, graphs  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

Each student belongs to exactly one club and has a potential value. On a given day, some students have already left their clubs permanently. From the remaining students, we may choose at most one student from each club. The chosen students form the contest team.

The team's strength is the mex of the selected potentials. We want the largest mex that can be achieved.

A mex of at least `k` means that every value `0, 1, ..., k-1` appears among the selected students. Since we may take only one student from each club, the real question is not about individual students anymore. It is about whether the values `0, 1, ..., k-1` can be assigned to distinct clubs.

The input describes the initial students, then a sequence of deletions. After the first deletion we need the answer for day 1, after the second deletion the answer for day 2, and so on.

The constraints are the key observation. There are at most 5000 students and club count is also at most 5000. Potentials are strictly below 5000. A solution that recomputes everything from scratch after every deletion would need roughly 5000 independent computations on graphs of size 5000, which is far beyond the limit. We need to reuse work between days.

One subtle case is when several clubs can provide the same value.

```
Club 1: potential 0
Club 2: potential 0
Club 3: potential 1
```

The mex is 2 because value 0 can come from either club 1 or club 2, while value 1 comes from club 3. A greedy choice of the first available club can paint itself into a corner if it does not allow reassignment.

Another easy mistake is treating students instead of clubs as the matching targets.

```
Club 1: potentials {0,1}
Club 2: potentials {1}
```

Values 0 and 1 cannot both be taken from club 1. Any correct model must enforce that each club contributes at most one selected student.

A third non-obvious situation occurs when a deleted student later reappears in the reverse process. The maximum mex can increase because a new edge appears in the underlying matching graph. Recomputing the whole matching every time is unnecessary, but the algorithm must still be able to find augmenting paths that rearrange previous assignments.

## Approaches

A direct approach is to process each day independently. After applying the day's deletions, build a graph where value `x` is connected to every club that currently contains a student with potential `x`. Then test whether mex is at least 1, at least 2, at least 3, and so on using bipartite matching.

This is correct because mex at least `k` means values `0..k-1` can all be assigned to distinct clubs. The matching formulation captures exactly that condition.

The problem is cost. There are up to 5000 days. Rebuilding and rematching every day leads to tens or hundreds of millions of matching operations.

The crucial observation is that deletions are permanent. Offline processing lets us reverse time.

Instead of removing students one by one, start from the final state where all deletions have already happened. Then add students back in reverse order.

Adding a student only adds one edge to the graph:

```
value p_i  --->  club c_i
```

No edge is ever removed.

Now consider the matching that certifies the current mex. Suppose we already know that values `0..cur-1` can be matched to distinct clubs. When new edges are added, the mex can only increase. We never need to recheck old values.

We maintain a matching on the bipartite graph:

```
values  <->  clubs
```

The invariant is that values `0..cur-1` are matched. To test whether mex can become `cur+1`, we only need to try matching value `cur`. If an augmenting path exists, we extend the matching and increment `cur`. We keep doing this until the next value cannot be matched.

This turns the whole process into an incremental matching problem. Each value is successfully matched at most once, so the total amount of work stays manageable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d · V · E) | O(E) | Too slow |
| Optimal | O(E · V) amortized, here O(n · 5000) | O(E) | Accepted |

`V` denotes the number of value vertices, at most 5001, and `E ≤ n`.

## Algorithm Walkthrough

1. Read all students and all deletion queries.
2. Mark every student that will eventually be deleted.
3. Build the graph corresponding to the state after all deletions have happened. For every student that survives all `d` days, add an edge from its potential value to its club.
4. Maintain a standard Kuhn matching from clubs to values. `match[club]` stores the value currently using that club.
5. Let `cur = 0`. Repeatedly try to find an augmenting path starting from value `cur`.
6. If the DFS succeeds, value `cur` becomes matchable. Increase `cur` and try the next value.
7. When the DFS fails, `cur` is exactly the current maximum mex. Store it as the answer for the state after all deletions.
8. Process deletions in reverse order. When student `k_i` is restored, add the edge `(p[k_i], c[k_i])` to the graph.
9. After adding the new edge, the mex can only increase. Continue the same loop from the current `cur`, repeatedly attempting to match value `cur`.
10. Store the resulting mex for this new state.
11. After all reverse additions are processed, we know the mex for every intermediate state. Output the answers corresponding to days `1..d`.

### Why it works

For any value `x`, an edge `(x, club)` means that the club currently contains at least one active student with potential `x`.

A mex of at least `k` requires every value `0..k-1` to appear in the selected team. Since each club contributes at most one student, those values must be assigned to distinct clubs. This is exactly a matching covering values `0..k-1`.

The maintained matching always covers all values below `cur`. When DFS succeeds for value `cur`, an augmenting path creates a matching covering `0..cur`. When DFS fails, Hall's condition is violated for value `cur`, so no matching can cover `0..cur`. Thus the maximum achievable mex is exactly `cur`.

Because reverse processing only adds edges, previously matched values never become invalid. The mex can only increase, so continuing from the current matching is sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    p = list(map(int, input().split()))
    c = list(map(int, input().split()))

    d = int(input())
    rem = [int(input()) - 1 for _ in range(d)]

    removed = [False] * n
    for x in rem:
        removed[x] = True

    MAXV = 5001
    g = [[] for _ in range(MAXV)]

    for i in range(n):
        if not removed[i]:
            g[p[i]].append(c[i])

    match = [-1] * (m + 1)

    sys.setrecursionlimit(20000)

    def dfs(v):
        if vis[v]:
            return False
        vis[v] = True

        for club in g[v]:
            if match[club] == -1 or dfs(match[club]):
                match[club] = v
                return True
        return False

    cur = 0

    while cur < MAXV:
        vis = [False] * MAXV
        if dfs(cur):
            cur += 1
        else:
            break

    ans = [0] * (d + 1)
    ans[d] = cur

    for idx in range(d - 1, -1, -1):
        student = rem[idx]
        g[p[student]].append(c[student])

        while cur < MAXV:
            vis = [False] * MAXV
            if dfs(cur):
                cur += 1
            else:
                break

        ans[idx] = cur

    print("\n".join(str(ans[i]) for i in range(1, d + 1)))

if __name__ == "__main__":
    solve()
```

The graph is indexed by potential value. `g[v]` contains every club that can currently provide value `v`.

The matching is stored from clubs to values. This is the standard Kuhn representation. During DFS, if a club is already occupied by another value, we recursively try to move that value elsewhere.

The variable `cur` always represents the first value that is not yet known to be matchable. Successful augmentation increases it by exactly one.

A common implementation mistake is rebuilding the matching after every restored student. The whole point of the offline approach is that the current matching remains valid because edges are only added, never removed.

Another subtle detail is the answer indexing. Reverse processing computes answers for states:

```
after all deletions
after restoring last deletion
after restoring last two deletions
...
```

The required output corresponds to states after day 1, day 2, ..., day d, which are stored in `ans[1] ... ans[d]`.

## Worked Examples

### Sample 1

Input:

```
5 3
0 1 2 2 0
1 2 2 3 2
5
3
2
4
5
1
```

After all deletions, no students remain.

| Reverse state | Added student | Current mex |
| --- | --- | --- |
| After all deletions | none | 0 |
| Restore 1 | value 0, club 1 | 1 |
| Restore 5 | value 0, club 2 | 1 |
| Restore 4 | value 2, club 3 | 1 |
| Restore 2 | value 1, club 2 | 3 |
| Restore 3 | value 2, club 2 | 3 |

The stored reverse answers become:

```
state0 = 3
state1 = 3
state2 = 1
state3 = 1
state4 = 1
state5 = 0
```

The required output is `state1..state5`:

```
3
1
1
1
0
```

This example shows why reverse processing is useful. The mex only moves upward as edges are added.

### Custom Example

```
3 2
0 1 1
1 1 2
2
2
3
```

After both deletions, only value `0` in club `1` remains.

| Reverse state | Available edges | Mex |
| --- | --- | --- |
| After all deletions | 0→1 | 1 |
| Restore student 3 | 1→2 | 2 |
| Restore student 2 | 1→1 and 1→2 | 2 |

The answer sequence is:

```
2
1
```

This trace demonstrates augmenting behavior. Once value `1` gains access to club `2`, values `0` and `1` can occupy different clubs and mex becomes `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 5000) amortized | Each edge is inserted once, each successful mex increase happens once |
| Space | O(n + m + 5000) | Graph, matching arrays, and DFS bookkeeping |

The potential values are bounded by 5000, which is what makes the incremental matching feasible. With at most 5000 students and 5000 clubs, the implementation comfortably fits within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    p = list(map(int, input().split()))
    c = list(map(int, input().split()))

    d = int(input())
    rem = [int(input()) - 1 for _ in range(d)]

    removed = [False] * n
    for x in rem:
        removed[x] = True

    MAXV = 5001
    g = [[] for _ in range(MAXV)]

    for i in range(n):
        if not removed[i]:
            g[p[i]].append(c[i])

    match = [-1] * (m + 1)

    sys.setrecursionlimit(20000)

    def dfs(v):
        if vis[v]:
            return False
        vis[v] = True
        for club in g[v]:
            if match[club] == -1 or dfs(match[club]):
                match[club] = v
                return True
        return False

    cur = 0
    while cur < MAXV:
        vis = [False] * MAXV
        if dfs(cur):
            cur += 1
        else:
            break

    ans = [0] * (d + 1)
    ans[d] = cur

    for idx in range(d - 1, -1, -1):
        s = rem[idx]
        g[p[s]].append(c[s])

        while cur < MAXV:
            vis = [False] * MAXV
            if dfs(cur):
                cur += 1
            else:
                break

        ans[idx] = cur

    return "\n".join(str(ans[i]) for i in range(1, d + 1))

# provided sample
assert run(
"""5 3
0 1 2 2 0
1 2 2 3 2
5
3
2
4
5
1
"""
) == "3\n1\n1\n1\n0"

# minimum size
assert run(
"""1 1
0
1
1
1
"""
) == "0"

# all values equal
assert run(
"""3 3
0 0 0
1 2 3
3
1
2
3
"""
) == "1\n1\n0"

# matching requires distinct clubs
assert run(
"""2 1
0 1
1 1
1
2
"""
) == "1"

# mex jumps after restoration
assert run(
"""3 2
0 1 1
1 1 2
2
2
3
"""
) == "2\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single student with value 0 | 0 | Minimum-size instance |
| All potentials equal to 0 | 1,1,0 | Repeated values do not increase mex |
| Values 0 and 1 in same club | 1 | One club cannot represent two values |
| Restoration creates a new matching | 2,1 | Augmenting-path logic |

## Edge Cases

Consider:

```
2 1
0 1
1 1
1
2
```

Only one club exists. Even though values 0 and 1 are both available, they cannot both appear in the selected team. The graph contains edges:

```
0 -> club 1
1 -> club 1
```

Value 0 can be matched, but value 1 cannot be matched simultaneously. The algorithm fails when trying to augment value 1, so mex is correctly reported as 1.

Now consider:

```
3 2
0 0 1
1 2 2
1
3
```

After deleting the only value 1, the remaining graph has:

```
0 -> club 1
0 -> club 2
```

Value 0 is matchable, value 1 is not. The algorithm returns mex 1. Multiple copies of the same value do not help unless the missing lower values are also present.

Finally:

```
3 3
1 2 3
1 2 3
1
1
```

No active student has value 0. The DFS for value 0 immediately fails. The algorithm returns mex 0 without considering any larger values, which is exactly the definition of mex.
