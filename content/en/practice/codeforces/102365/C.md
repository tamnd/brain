---
title: "CF 102365C - Unjob Search"
description: "We have a tree with (N) cities. A terminal city is simply a leaf, a vertex whose degree is exactly one. The tree itself is hidden from us. We cannot inspect its edges directly."
date: "2026-08-14T02:54:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102365
codeforces_index: "C"
codeforces_contest_name: "UBC Programming Contest 2019 (UBCPC 2019)"
rating: 0
weight: 102365
solve_time_s: 141
verified: true
draft: false
---

[CF 102365C - Unjob Search](https://codeforces.com/problemset/problem/102365/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree with (N) cities. A terminal city is simply a leaf, a vertex whose degree is exactly one. The tree itself is hidden from us. We cannot inspect its edges directly. Instead, we have an oracle that answers a path-membership query: given three cities (a,b,c), it tells us whether (b) belongs to the unique path from (a) to (c).

The task is to output any leaf while asking at most (N) such questions. Since this is an interactive problem, the input after (N) consists of answers supplied by the judge in response to our queries. The sample is consequently a transcript rather than an ordinary input/output pair.

The constraint (N \le 2000) is large enough that reconstructing the whole tree through many queries is not viable under a query budget of only (N). A solution using (O(N^2)) or (O(N^3)) oracle calls is already disqualified, regardless of how cheap each individual operation is. The target is linear in the number of cities, and the memory requirement is trivial because the hidden tree never needs to be stored.

There are two subtle cases that can break a careless approach. First, the initial candidate does not have to be a leaf. For the tree (1-2-3), starting at city (2) is fine only if the algorithm knows how to move from an internal vertex toward a descendant. Simply returning city (2) would be wrong because the correct outputs are (1) or (3).

Second, the candidate can change several times, and a vertex already examined must not cause us to move back toward the root. Consider the tree (1-2-5-3). Starting from city (2), city (3) may move the candidate to (3), and later city (5) must not move it back to (5). The query asks whether the current candidate lies on the path from the root to the new city. Since (3) is not on the path (1) to (5), the answer is false, so the leaf (3) is preserved. A careless interpretation of the path direction can silently reverse this decision.

## Approaches

A direct approach would try to determine whether each city is a leaf. A city (b) is not a leaf exactly when there are two other cities whose path passes through (b). We could test many pairs (a,c) and ask whether (b) lies on their path. In the worst case, checking one candidate against all pairs of other cities requires (\binom{N-1}{2}) queries, and doing that for all candidates requires

[
N\binom{N-1}{2} = \frac{N(N-1)(N-2)}{2},
]

which is (\Theta(N^3)). For (N=2000), this is about (4\times 10^9) queries, far beyond the allowed (N).

The useful observation is that we do not need to determine whether every vertex is a leaf. We only need to move one candidate toward a leaf.

Root the hidden tree at city (1). For any city (v), call another city (x) a descendant of (v) if (v) lies on the path from the root (1) to (x). The oracle gives us exactly the test we need. The query

[
? \ 1\ v\ x
]

returns true precisely when (v) is an ancestor of (x).

Suppose our current candidate is (v). If (v) is not a leaf, then because it is not the root, it has at least one child, and that child has some descendant (x). For such an (x), the query returns true, so we can replace (v) with (x), moving strictly downward in the rooted tree.

The crucial detail is that we process every city exactly once. If a descendant of the current candidate was encountered earlier, the candidate would already have moved into that descendant's subtree. Consequently, when a later city becomes the candidate, it cannot be an ancestor of a previously processed candidate. The candidate only moves downward.

This turns the entire problem into a single scan. We start with city (2), then inspect cities (3,4,\ldots,N). Whenever the current candidate lies on the path from city (1) to the inspected city, we move the candidate to that inspected city. After all cities have been processed, the candidate cannot have an unprocessed descendant. It is consequently a leaf.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^3)) queries | (O(1)) | Too slow |
| Optimal | (O(N)) queries | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Choose city (1) as a conceptual root and city (2) as the initial candidate. We do not need to know any actual edges. The only property we use is the meaning of a path query with city (1) as one endpoint.
2. Process every city (c) from (3) through (N). Ask whether the current candidate (v) lies on the path from city (1) to (c).
3. If the answer is true, replace (v) with (c). In the tree rooted at (1), this means (c) is in the subtree rooted at (v), so moving to (c) moves the candidate farther away from the root.
4. If the answer is false, leave (v) unchanged. City (c) is either outside the subtree of (v) or is above (v), so it cannot be used to move the candidate downward.
5. After all (N-2) queries have been made, output the current candidate. The candidate is a terminal city.

The query count is actually (N-2), which is safely below the limit of (N).

### Why it works

Maintain the invariant that the current candidate is a vertex on a downward chain in the rooted tree, and every processed vertex that lies in its subtree has already been able to move the candidate farther downward.

When a query returns true for a city (c), the current candidate (v) lies on the path (1) to (c). Thus (c) is a descendant of (v), so replacing (v) by (c) is a valid downward move.

Suppose the final candidate (v) were not a leaf. Since (v\neq1), it would have a child and hence at least one descendant (x). Because (x\neq v), it appears somewhere in the scan. When (x) was processed, either the current candidate was (v), in which case the query would have returned true and moved the candidate downward, or the candidate had already moved to another descendant of (v). In the latter case, the current candidate is already below (v), and the same argument applies recursively. Thus an internal candidate cannot survive the complete scan. The only possible final candidate is a leaf.

## Python Solution

The original task is interactive, so the program must print each query, flush the output, and then read the judge's response. The helper `ask` encapsulates this protocol.

```python
import sys

input = sys.stdin.readline

def solve():
    n = int(input())

    current = 2

    for c in range(3, n + 1):
        print("?", 1, current, c, flush=True)

        response = int(input())
        if response == -1:
            return

        if response == 1:
            current = c

    print("!", current, flush=True)

if __name__ == "__main__":
    solve()
```

The first line gives (N), after which no tree edges are available. The variable `current` stores the only piece of state needed by the algorithm. City `1` remains fixed as the root.

The loop starts at `3` because city `2` is already the initial candidate. Every iteration asks exactly one query. When the response is `1`, the candidate becomes the newly inspected city because the current candidate is an ancestor of it in the tree rooted at city `1`.

The response `-1` is the judge's signal that the interaction has failed. The program must terminate immediately rather than issuing another query.

`flush=True` is essential in an interactive problem. Without it, Python may buffer the query instead of sending it to the judge, causing the program to wait forever for an answer that the judge never receives the request for.

There are no integer-overflow concerns in Python, and the algorithm stores only two integer variables. The final answer is printed with the required `!` prefix and the program terminates afterward.

## Worked Examples

### Sample 1

The sample is consistent with the three-city path

[
1 - 2 - 3.
]

Both cities (1) and (3) are leaves. Our algorithm is allowed to output either one.

| Step | Current candidate | Inspected city | Query | Response | New candidate |
| --- | --- | --- | --- | --- | --- |
| Initial | 2 |  |  |  | 2 |
| 1 | 2 | 3 | Is 2 on path (1) to (3)? | 1 | 3 |

The algorithm outputs city (3). This differs from the sample's transcript, which uses a different sequence of valid queries and outputs city (1), but both answers are terminal cities.

### Sample 2

For a second trace, consider the rooted tree

[
1-2,\qquad 1-3,\qquad 3-4,\qquad 3-5.
]

The leaves are (2,4,5). The initial candidate (2) is already a leaf, so every later query must leave it unchanged.

| Step | Current candidate | Inspected city | Query | Response | New candidate |
| --- | --- | --- | --- | --- | --- |
| Initial | 2 |  |  |  | 2 |
| 1 | 2 | 3 | Is 2 on path (1) to (3)? | 0 | 2 |
| 2 | 2 | 4 | Is 2 on path (1) to (4)? | 0 | 2 |
| 3 | 2 | 5 | Is 2 on path (1) to (5)? | 0 | 2 |

The final answer is (2). This trace demonstrates why a false answer must not cause the candidate to change. City (2) is in a different branch from cities (3,4,5), so none of those cities is a descendant of (2).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | There is exactly one oracle query for each city from (3) through (N). |
| Space | (O(1)) | Only (N), the current candidate, and the current response are stored. |

The algorithm asks (N-2) queries, which fits the maximum of (N) queries with room to spare. With (N\le2000), the computation performed locally is negligible. The dominant cost is interaction with the judge, and the solution keeps that cost linear.

## Test Cases

Because the original problem is interactive, a normal `run(input)` function cannot test the official solution by feeding it a complete static input. The judge's answers depend on the hidden tree and on the queries produced by the program. For offline testing, the clean approach is to keep the same candidate-selection logic and replace the interactive oracle with a simulator that knows the tree.

The following harness uses the exact path definition from the problem to answer simulated queries. The provided sample is represented by the compatible path (1-2-3), while the custom cases exercise stars, chains, and branches.

```python
# Offline version of the algorithm for testing.
# The real submission uses the interactive solve() above.

def find_leaf(n, edges):
    graph = [[] for _ in range(n + 1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    parent = [0] * (n + 1)
    parent[1] = -1
    stack = [1]

    while stack:
        v = stack.pop()
        for to in graph[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            stack.append(to)

    def is_on_path_root_to(v, x):
        while x != 0:
            if x == v:
                return True
            x = parent[x]
        return False

    current = 2

    for c in range(3, n + 1):
        if is_on_path_root_to(current, c):
            current = c

    return current

def run(n, edges):
    return find_leaf(n, edges)

# Provided sample, represented by the compatible tree 1-2-3.
answer = run(3, [(1, 2), (2, 3)])
assert answer in {1, 3}, "sample 1"

# Minimum-size tree.
answer = run(3, [(1, 2), (1, 3)])
assert answer in {2, 3}, "minimum-size tree"

# Star centered at 1.
answer = run(
    6,
    [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]
)
assert answer in {2, 3, 4, 5, 6}, "star"

# Chain with the initial candidate already a leaf.
answer = run(
    7,
    [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)]
)
assert answer in {1, 7}, "chain"

# Branching tree designed to catch an incorrect interpretation
# that moves upward when the query answer is 0.
answer = run(
    7,
    [(1, 2), (2, 3), (2, 4), (4, 5), (4, 6), (6, 7)]
)
assert answer in {3, 5, 7}, "branching tree"

# Larger boundary-style case.
n = 2000
edges = [(1, 2)] + [(i, i + 1) for i in range(2, n)]
answer = run(n, edges)
assert answer in {1, n}, "n = 2000 chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (1-2-3) | (1) or (3) | Provided sample and minimum number of cities |
| Star centered at (1) | Any city from (2) through (6) | Many leaves and immediate branching |
| Chain (1-2-3-4-5-6-7) | (1) or (7) | Deep tree and repeated downward movement |
| (1-2), (2-3), (2-4), (4-5), (4-6), (6-7) | (3), (5), or (7) | Branching and correct interpretation of a false query |
| Chain with (N=2000) | (1) or (2000) | Maximum-size input and linear behavior |

The offline simulator reconstructs parent relationships only for testing. The submitted interactive solution never has access to those edges.

## Edge Cases

For the minimum-size tree with input

```
3
```

there are only two queries available in the protocol, and the algorithm needs just one. It starts with city (2) and asks whether city (2) lies on the path from (1) to (3). If the answer is false, city (2) is a leaf and is returned. If the answer is true, city (3) is farther down the rooted tree and becomes the candidate. Since a three-vertex tree always has two leaves, either result is valid.

For a star such as

```
1
/|\
2 3 4
```

the initial candidate (2) is already a leaf. Every query involving cities (3) and (4) asks whether (2) lies on a path starting at the center (1). The answer is always false because those paths go directly through (1), not through (2). The candidate remains (2).

For a long chain such as

```
1 - 2 - 3 - 4 - 5 - 6
```

the algorithm starts at (2). The query for city (3) is true, so the candidate becomes (3). The query for (4) is then true, followed by true answers for (5) and (6). The final candidate is (6), a leaf. This demonstrates that the algorithm can repeatedly descend through the rooted tree and still use only one query per city.

For a branching tree such as

```
      1
      |
      2
     / \
    3   4
       / \
      5   6
           \
            7
```

the candidate starts at (2). City (3) is a descendant of (2), so the candidate becomes (3). When city (4) is examined, the query asks whether (3) lies on the path from (1) to (4). It does not, so the candidate stays at (3). Later cities (5,6,7) are also outside the subtree rooted at (3), so the candidate remains (3), which is a leaf. This case catches the common mistake of treating a false query as evidence that the inspected city should replace the candidate.

For the maximum size (N=2000), the loop performs exactly (1998) queries. The algorithm does not allocate a graph, recursion stack, or auxiliary array, so the memory usage remains constant. The query count stays below the strict limit of (2000), which is the central constraint of the problem.
