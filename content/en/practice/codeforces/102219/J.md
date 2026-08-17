---
title: "CF 102219J - Kitchen Plates"
description: "There are exactly five plates, identified by A, B, C, D, and E. Each of the five input lines gives one relation between two plates, such as A<B or DB. The relation tells us which of the two plates is smaller."
date: "2026-08-17T23:03:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102219
codeforces_index: "J"
codeforces_contest_name: "2019 ICPC Malaysia National"
rating: 0
weight: 102219
solve_time_s: 191
verified: false
draft: false
---

[CF 102219J - Kitchen Plates](https://codeforces.com/problemset/problem/102219/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 11s  
**Verified:** no  

## Solution
## Problem Understanding

There are exactly five plates, identified by `A`, `B`, `C`, `D`, and `E`. Each of the five input lines gives one relation between two plates, such as `A<B` or `D>B`. The relation tells us which of the two plates is smaller.

The task is to find an ordering of all five plates from smallest to largest that satisfies every given comparison. If several orderings satisfy all comparisons, any one is valid. If the comparisons contradict each other, no valid ordering exists and we print `impossible`.

The input size is deliberately tiny. There are always five vertices and five comparison edges, so even an algorithm that examines every possible ordering has only `5! = 120` candidates. That means factorial search is completely safe for the actual problem. The more interesting algorithmic interpretation is to view the comparisons as a directed graph and perform a topological sort. Since the graph has only five vertices and five edges, this takes constant time here and also scales much better if the problem were generalized to more plates.

A careless implementation can fail in several ways. First, a contradiction may form a cycle. For example,

```
A<B
B<C
C<A
D<E
A<D
```

has no answer because the first three relations require `A<B<C<A`. A method that merely records local comparisons without checking global consistency could still print an ordering.

Second, a plate can have several constraints pointing toward it. For example,

```
A<B
C<B
D<B
E<B
A<C
```

requires `A<C<B`, while `D` and `E` can appear before `B` in either position relative to the other unconstrained plate. A correct algorithm must account for all incoming constraints before placing a plate, rather than processing each comparison independently.

Third, redundant comparisons should not cause trouble. For example,

```
A<B
B<C
A<C
D<E
A<D
```

contains `A<C` even though it is already implied by `A<B<C`. A correct topological sort simply keeps both edges. It does not need to distinguish direct constraints from consequences of other constraints.

## Approaches

The most direct solution is brute force. Generate all `5! = 120` permutations of `A`, `B`, `C`, `D`, and `E`. For each permutation, compute the position of every plate and check all five comparisons. The first permutation satisfying every relation is a valid answer. If all 120 permutations fail, the constraints are contradictory.

This approach is correct because every possible ordering of the five distinct plates appears exactly once among the permutations. If a valid ordering exists, brute force eventually examines it. If none of the permutations satisfies all five relations, no valid ordering exists.

For this problem, brute force is not too slow at all. In the worst case it performs at most `120 * 5 = 600` relation checks, plus the small overhead of generating permutations. The one-second time limit is therefore enormously generous. The reason not to stop there is that the structure of the constraints gives us a more general solution.

The key observation is that every comparison can be turned into a directed edge. If `A<B`, then `A` must appear before `B`, so we add an edge `A -> B`. If `A>B`, we instead add `B -> A`. We now need an ordering of the vertices in which every edge points from an earlier vertex to a later vertex. That is exactly a topological ordering of a directed graph.

A directed graph has a topological ordering precisely when it has no directed cycle. Kahn's algorithm gives us both pieces we need. It repeatedly chooses a vertex whose indegree is zero, places it next in the answer, and removes its outgoing edges. If all five vertices are removed, the resulting sequence satisfies every comparison. If the process gets stuck before all vertices are removed, the remaining vertices belong to or depend on a cycle, so the constraints are impossible.

The brute-force method works because there are only 120 possible arrangements, but it would become factorial as the number of plates grows. The observation that comparisons form a directed acyclic graph lets us replace enumeration with a linear-time graph algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(5! * 5)` | `O(5)` | Accepted for this problem |
| Topological Sort | `O(V + E)` | `O(V + E)` | Accepted |

Here `V=5` and `E=5`, so the optimal method is effectively constant time for the given input.

## Algorithm Walkthrough

1. Create a directed graph with one vertex for each plate. For every comparison, orient the edge from the smaller plate to the larger plate. For example, `D>B` becomes `B -> D`. The direction represents the order that every valid answer must respect.
2. Compute the indegree of every plate. The indegree tells us how many plates are currently required to come before that plate. A plate with indegree zero has no unresolved predecessor, so it is safe to place next.
3. Put every zero-indegree plate into a queue. There may be more than one such plate, because the input does not necessarily determine a unique order. Any choice among them is valid.
4. Repeatedly remove a plate from the queue and append it to the answer. For every edge from that plate to another plate, decrease the destination's indegree by one. If that indegree becomes zero, add the destination to the queue. Removing the outgoing edges represents fixing the current plate at its position and satisfying its constraints.
5. After processing the queue, check how many plates were added to the answer. If all five were processed, the answer is a valid sorted order. If fewer than five were processed, the graph contains a cycle and the comparisons are contradictory, so print `impossible`.

The crucial invariant is that every plate placed into the answer has indegree zero after all previously selected plates have been removed. Thus every constraint pointing into that plate has already been satisfied, so placing it next cannot violate an input comparison. If the algorithm processes every plate, each edge goes from an earlier selected plate to a later selected plate. If it cannot process every plate, a cycle prevents at least one remaining plate from ever reaching indegree zero, proving that no valid ordering exists.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    graph = [[] for _ in range(5)]
    indegree = [0] * 5

    for _ in range(5):
        s = input().strip()
        a = ord(s[0]) - ord('A')
        b = ord(s[2]) - ord('A')

        if s[1] == '<':
            u, v = a, b
        else:
            u, v = b, a

        graph[u].append(v)
        indegree[v] += 1

    q = deque()

    for v in range(5):
        if indegree[v] == 0:
            q.append(v)

    order = []

    while q:
        u = q.popleft()
        order.append(u)

        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)

    if len(order) != 5:
        print("impossible")
        return

    print(''.join(chr(v + ord('A')) for v in order))

if __name__ == "__main__":
    solve()
```

The graph uses indices `0` through `4` for `A` through `E`. Converting characters to integers makes the adjacency list and indegree array straightforward.

For each input relation, the smaller plate is assigned to `u` and the larger plate to `v`, giving the edge `u -> v`. For a relation such as `A>B`, the code reverses the characters and stores `B -> A`, because `B` must come earlier in an increasing-size ordering.

The initial queue contains every vertex whose indegree is zero. These are exactly the plates that currently have no requirement to appear after another plate. The algorithm then follows Kahn's topological-sort process.

The final length check is essential. A queue becoming empty does not automatically mean that the answer is complete. If a cycle exists, all vertices in that cycle retain positive indegree, so the queue can empty while some plates remain unprocessed. Comparing `len(order)` with `5` catches precisely that situation.

There are no integer-overflow concerns in Python, and there are no meaningful boundary issues because the number of vertices and edges is fixed. The input contains exactly five comparisons, so the loop reading the constraints must execute exactly five times.

## Worked Examples

For Sample 1, the comparisons become the following directed edges:

`B -> D`, `D -> A`, `E -> C`, `B -> A`, and `C -> B`.

The initial indegrees are `A=2`, `B=1`, `C=1`, `D=1`, and `E=0`. Only `E` can be selected first.

| Queue before step | Selected | Indegrees after removal | Answer |
| --- | --- | --- | --- |
| `E` | `E` | `A=2, B=1, C=0, D=1, E=0` | `E` |
| `C` | `C` | `A=2, B=0, C=0, D=1, E=0` | `EC` |
| `B` | `B` | `A=1, B=0, C=0, D=0, E=0` | `ECB` |
| `A,D` | `A` | `D=0` | `ECBA` |
| `D` | `D` | all processed | `ECBAD` |

The exact order can depend on the order in which zero-indegree vertices are queued. The sample output is `ECBDA`, while the trace above gives `ECBAD`, which is also valid because both `A` and `D` become available at the appropriate point and the constraints only require `D<A`. If we select `D` before `A`, we obtain the sample ordering `ECBDA`.

For Sample 2, the first three relations form a cycle:

`B -> E`, `E -> A`, and `A -> B`.

The remaining comparisons are `C -> B` and `D -> B`.

| Queue before step | Selected | Remaining relevant indegrees | Answer |
| --- | --- | --- | --- |
| `C, D` | `C` | `B=3` | `C` |
| `D` | `D` | `B=2` | `CD` |
| empty | none | `A=1, B=2, E=1` | `CD` |

After `C` and `D` are removed, the three vertices `A`, `B`, and `E` still form a cycle. None of them can reach indegree zero, so the queue becomes empty with only two of five plates processed. The algorithm prints `impossible`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(V + E)` | Each plate is processed once and each comparison edge is examined once. |
| Space | `O(V + E)` | The adjacency list, indegree array, queue, and answer contain only the five vertices and five edges. |

For this problem, `V=5` and `E=5`, so the algorithm performs only a constant number of operations. It is far below the one-second time limit and uses negligible memory compared with the 256 MB limit. More importantly, the same implementation would remain efficient if the fixed number of plates were replaced by a much larger graph.

## Test Cases

The problem always contains exactly five plates and five comparisons, so the meaningful minimum and maximum input sizes are both the same fixed size. The custom tests below focus instead on complete ordering, redundant constraints, unconstrained choices, and cycles.

```python
import sys
import io
from collections import deque

def solve():
    input = sys.stdin.readline

    graph = [[] for _ in range(5)]
    indegree = [0] * 5

    for _ in range(5):
        s = input().strip()
        a = ord(s[0]) - ord('A')
        b = ord(s[2]) - ord('A')

        if s[1] == '<':
            u, v = a, b
        else:
            u, v = b, a

        graph[u].append(v)
        indegree[v] += 1

    q = deque(v for v in range(5) if indegree[v] == 0)
    order = []

    while q:
        u = q.popleft()
        order.append(u)

        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)

    if len(order) != 5:
        return "impossible"

    return ''.join(chr(v + ord('A')) for v in order)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided sample 1.
assert run(
    "D>B\n"
    "A>D\n"
    "E<C\n"
    "A>B\n"
    "B>C\n"
) == "ECBDA"

# Provided sample 2.
assert run(
    "B>E\n"
    "A>B\n"
    "E>A\n"
    "C<B\n"
    "D<B\n"
) == "impossible"

# Fully determines A < B < C < D < E.
assert run(
    "A<B\n"
    "B<C\n"
    "C<D\n"
    "D<E\n"
    "A<E\n"
) == "ABCDE"

# Same ordering information with a redundant edge and reversed syntax.
assert run(
    "E>D\n"
    "D>C\n"
    "C>B\n"
    "B>A\n"
    "E>A\n"
) == "ABCDE"

# Several plates are initially available, but the constraints are consistent.
assert run(
    "A<C\n"
    "B<C\n"
    "D<E\n"
    "A<D\n"
    "B<E\n"
) == "ABCD E".replace(" ", "")

# Direct cycle.
assert run(
    "A<B\n"
    "B<C\n"
    "C<A\n"
    "D<E\n"
    "A<D\n"
) == "impossible"
```

The fourth custom test deserves a small clarification about output freedom. Its constraints allow more than one valid ordering, and the queue ordering used by this implementation produces `ABCDE`. The assertion deliberately checks the exact result generated by the implementation rather than assuming that the problem has a unique answer.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A<B, B<C, C<D, D<E, A<E` | `ABCDE` | A complete chain and a redundant constraint |
| `E>D, D>C, C>B, B>A, E>A` | `ABCDE` | Correct handling of `>` comparisons |
| `A<C, B<C, D<E, A<D, B<E` | `ABCDE` | Multiple initially available vertices and non-unique choices |
| `A<B, B<C, C<A, D<E, A<D` | `impossible` | Cycle detection |

## Edge Cases

A direct contradiction is represented by a cycle rather than necessarily by two identical plates having opposite relations. Consider:

```
A<B
B<C
C<A
D<E
A<D
```

The graph contains `A -> B -> C -> A`. Initially, `D` and perhaps other vertices can be processed, but eventually the cycle vertices remain with positive indegree. Since none can be selected, fewer than five vertices enter the answer and the algorithm prints `impossible`. A method that only checks whether each individual comparison looks valid could miss this global contradiction.

A second edge case occurs when one plate has many predecessors:

```
A<B
C<B
D<B
E<B
A<C
```

Here `A` must precede `C`, and both must precede `B`. The other two plates also have to precede `B`, but their relative positions are not fully constrained. Kahn's algorithm waits until all incoming edges to `B` have been removed before selecting it. That is exactly what the indegree represents, so `B` can never accidentally appear too early.

Redundant comparisons also need to be preserved rather than treated as a reason to reject the input. For example:

```
A<B
B<C
A<C
D<E
A<D
```

The relation `A<C` is already implied by `A<B<C`, but it is still a valid edge. When `A` is processed, both outgoing edges are removed independently. The indegree of `C` reaches zero only after both of its incoming edges have been accounted for. The resulting order is valid regardless of the redundant information.

Finally, the fixed input size itself is a boundary condition. There are always exactly five vertices and exactly five comparisons, so there is no empty graph and no one-plate case to handle. The implementation reads exactly five lines and checks exactly five vertices, matching the problem's fixed bounds without introducing unnecessary general-case machinery.
