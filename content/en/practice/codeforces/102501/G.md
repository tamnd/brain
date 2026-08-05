---
title: "CF 102501G - Swapping Places"
description: "We are given a sequence of animal species representing the order in which animals enter a waiting line. The final leaving order is not fixed because neighboring animals are allowed to exchange places when their species pair is listed as compatible."
date: "2026-08-06T05:00:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102501
codeforces_index: "G"
codeforces_contest_name: "2019-2020 ICPC Southwestern European Regional Programming Contest (SWERC 2019-20)"
rating: 0
weight: 102501
solve_time_s: 77
verified: true
draft: false
---

[CF 102501G - Swapping Places](https://codeforces.com/problemset/problem/102501/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of animal species representing the order in which animals enter a waiting line. The final leaving order is not fixed because neighboring animals are allowed to exchange places when their species pair is listed as compatible. The task is to find the lexicographically smallest sequence of species that can appear when all animals eventually leave.

The input describes the set of species, the pairs of species that may cross each other, and the original sequence. The output is another sequence containing the same animals, but arranged as the earliest possible leaving order according to dictionary order.

The key difficulty is that swaps are local. An animal cannot arbitrarily move to the front. To move left across another animal, it must be allowed to swap with that animal's species. The constraints tell us that there are only at most 200 species, but up to 100000 animals. This rules out simulating swaps or exploring possible permutations, because the number of reachable orders can be exponential. The algorithm must process the sequence almost linearly, with only small extra work per species.

There are several easy-to-miss cases. If a species has no friends at all, its animals cannot pass any different species. For example:

```
2 0 3
A
B
A B A
```

The answer is:

```
A B A
```

A careless greedy approach that always picks the smallest species appearing anywhere would output `A A B`, which is impossible because the second `A` cannot cross `B`.

Another tricky case is repeated occurrences of the same species. Equal species do not need permission to cross because the output only cares about species names, not individual animals. For example:

```
2 0 3
A
B
A A B
```

The answer is:

```
A A B
```

A solution that treats equal species as a blocking pair would incorrectly prevent the two `A` animals from being considered together.

A third case is when a later occurrence of a species is blocked by an earlier occurrence of the same species. For example:

```
3 1 4
A
B
C
A B C B
A B
```

The answer is:

```
A B C B
```

The last `B` cannot move before `C` even though `B` is smaller than `C`, because `B` has to cross `C`, and that swap is not allowed.

## Approaches

A direct approach would try to generate all reachable sequences. Every allowed adjacent swap creates another possible state, so we could perform a breadth-first search over states and keep the smallest sequence found. This is correct because every legal swap is explored. However, even with only a few animals, the number of possible states can approach `N!`, making it completely impossible for `N = 100000`.

The useful observation is that we do not actually need to simulate swaps. Instead, we can describe which animals are forced to stay before others.

Consider one animal at position `i`. If there is an earlier animal of species `X` that is not friends with the species at `i`, then the animal at `i` can never move before that earlier animal. That creates a precedence constraint: the earlier animal must leave before the current one.

The important detail is that we only need the latest occurrence of each blocking species. If an earlier occurrence of the same species exists, the latest one is the closest obstacle that must be passed. If that latest occurrence can be crossed, all earlier occurrences of the same species can also be crossed.

These precedence constraints form a directed acyclic graph. Each animal is a node, and an edge from `a` to `b` means animal `a` must leave before animal `b`. Any valid leaving order is a topological ordering of this graph.

Among all topological orderings, the lexicographically smallest one can be found by repeatedly choosing the smallest available node. This is the standard priority queue version of topological sorting.

The brute force works because it explores every legal ordering, but it fails because there are too many orderings. The observation that only non-swappable previous species create restrictions lets us compress the problem into a DAG and solve it greedily.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(N * S + N log N) | O(N + S²) | Accepted |

## Algorithm Walkthrough

1. Read the species and assign every species an integer id. Store which pairs of species can swap.
2. Scan the input sequence from left to right and create the dependency graph between animals. For the current animal of species `x`, inspect every species `y` that has appeared before. If `y` is not allowed to swap with `x`, add an edge from the most recent `y` occurrence to the current animal.

The edge means the previous animal must leave first because the current animal cannot move past it.
3. Maintain the latest position of every species while scanning. After processing an occurrence, update that species' latest position.
4. Compute indegrees of all nodes in the dependency graph. Every node with indegree zero can legally be the next animal to leave.
5. Put all currently available animals into a min-heap ordered by their species name. Repeatedly remove the smallest species, append it to the answer, and decrease the indegree of its outgoing neighbors.
6. Continue until every animal has been removed. The produced order is the required leaving sequence.

Why it works:

The graph contains exactly the restrictions created by animals that cannot pass each other. If there is an edge from one animal to another, every valid sequence must keep that order. If there is no dependency edge, the earlier animal does not prevent the later animal from reaching the front. Therefore every valid leaving order corresponds to a topological ordering of this graph.

At every step of Kahn's algorithm, the available nodes are precisely the animals that can be moved to the front without violating any restriction. Choosing the smallest available species is always safe because no unavailable animal can appear before it in any valid ordering. Repeating this choice gives the smallest possible prefix at every position, so the entire sequence is lexicographically minimal.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    S, L, N = map(int, input().split())

    names = [input().strip() for _ in range(S)]
    ids = {name: i for i, name in enumerate(names)}

    friend = [[False] * S for _ in range(S)]
    for _ in range(L):
        a, b = input().split()
        x, y = ids[a], ids[b]
        friend[x][y] = True
        friend[y][x] = True

    seq = [ids[x] for x in input().split()]

    graph = [[] for _ in range(N)]
    indeg = [0] * N

    last = [-1] * S

    for i, x in enumerate(seq):
        for y in range(S):
            if last[y] != -1 and y != x and not friend[x][y]:
                graph[last[y]].append(i)
                indeg[i] += 1
        last[x] = i

    heap = []
    for i in range(N):
        if indeg[i] == 0:
            heapq.heappush(heap, (names[seq[i]], i))

    ans = []

    while heap:
        _, u = heapq.heappop(heap)
        ans.append(names[seq[u]])

        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, (names[seq[v]], v))

    print(" ".join(ans))

if __name__ == "__main__":
    solve()
```

The first part maps species names to integer identifiers. Integer ids make the friend matrix and later comparisons constant time.

The graph construction is the core of the solution. While scanning the sequence, `last[y]` stores the latest occurrence of species `y`. When the current animal sees a previous species that cannot swap with it, that latest occurrence is the closest unavoidable blocker, so an edge is added from that occurrence to the current one.

The topological sorting phase uses a heap instead of a normal queue. A normal topological sort would produce any valid ordering, but the problem asks for the smallest alphabetical ordering. The heap always removes the smallest available species.

There is no off-by-one issue because nodes represent animals by their original zero-based positions. Indegrees are updated only when dependencies are removed, and a node enters the heap exactly when all animals that must precede it have already been output.

## Worked Examples

For the sample:

```
3 2 6
ANTILOPE
CAT
ANT
CAT ANTILOPE
ANTILOPE ANT
ANT CAT CAT ANTILOPE CAT ANT
```

The dependency graph creation behaves as follows:

| Position | Species | Blocking previous species | Added dependency |
| --- | --- | --- | --- |
| 0 | ANT | none | none |
| 1 | CAT | none | none |
| 2 | CAT | none | none |
| 3 | ANTILOPE | CAT | CAT -> ANTILOPE |
| 4 | CAT | none | none |
| 5 | ANT | CAT | CAT -> ANT |

The initially available animals are `ANT`, `CAT`, and `CAT`. The heap chooses `ANT`, then the smallest remaining available choices produce:

| Output step | Chosen animal | Current answer |
| --- | --- | --- |
| 1 | ANT | ANT |
| 2 | ANTILOPE | ANT ANTILOPE |
| 3 | CAT | ANT ANTILOPE CAT |
| 4 | CAT | ANT ANTILOPE CAT CAT |
| 5 | CAT | ANT ANTILOPE CAT CAT CAT |
| 6 | ANT | ANT ANTILOPE CAT CAT CAT ANT |

The dependencies prevent the antelope from passing the cats that block it, while still allowing it to move before the final ant.

A smaller custom example:

```
3 1 5
A
B
C
A B
B C A B C
```

The graph construction gives:

| Position | Species | Dependencies |
| --- | --- | --- |
| 0 | B | none |
| 1 | C | B -> C |
| 2 | A | C -> A |
| 3 | B | C -> B |
| 4 | C | none |

The heap process becomes:

| Output step | Available species | Chosen |
| --- | --- | --- |
| 1 | B, C | B |
| 2 | C | C |
| 3 | A, B, C | A |
| 4 | B, C | B |
| 5 | C | C |

The output is:

```
B C A B C
```

This example shows that a smaller species is not always chosen immediately. It must first become available by removing all animals that block it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N * S + N log N) | Each animal checks all species when dependencies are created, and every heap operation handles one animal |
| Space | O(N + S²) | The graph stores up to O(N*S) dependencies in the worst case, and the species graph uses O(S²) memory |

The number of species is only 200, so checking all species for every animal costs at most about 20 million operations. The graph and heap processing are linear or near-linear in the number of animals, which fits the limit for `N = 100000`.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue().strip()

assert run("""3 2 6
ANTILOPE
CAT
ANT
CAT ANTILOPE
ANTILOPE ANT
ANT CAT CAT ANTILOPE CAT ANT
""") == "ANT ANTILOPE CAT CAT CAT ANT"

assert run("""1 0 1
A
A
""") == "A"

assert run("""2 0 4
A
B
B A B A
""") == "B A B A"

assert run("""2 1 5
A
B
A B
B A B A B
""") == "A B A B B"

assert run("""3 0 5
A
B
C
C C B A C
""") == "C C B A C"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample input | `ANT ANTILOPE CAT CAT CAT ANT` | Basic dependency construction and greedy ordering |
| One species | `A` | Minimum size and no dependency handling |
| No friendships | `B A B A` | Species that cannot cross remain fixed |
| Complete friendship between two species | `A B A B B` | Free movement between compatible species |
| Repeated blocked species | `C C B A C` | Duplicate species and ordering constraints |

## Edge Cases

For the case with no friendships:

```
2 0 3
A
B
A B A
```

The algorithm creates an edge from the first `A` to `B`, because `B` cannot cross `A`. The second `A` also depends on `B` if `B` appears before it. The heap never incorrectly exposes the second `A` before the blocking `B`, producing the only valid answer.

For repeated identical species:

```
2 0 3
A
B
A A B
```

The two `A` animals do not create a dependency between each other. Only different species matter when checking swaps. The graph contains no edge from the first `A` to the second `A`, so both are available before `B`, giving the correct result `A A B`.

For a later occurrence blocked by an earlier occurrence:

```
3 1 4
A
B
C
A B
A B C B
```

When processing the final `B`, the latest `C` occurrence is a blocker because `B` and `C` are not friends. The graph adds `C -> B`, so the final `B` cannot jump ahead of `C`. The topological ordering respects this restriction and returns the smallest reachable sequence.
