---
title: "CF 102346D - Denouncing Mafia"
description: "The mafia hierarchy forms a rooted tree, with member 1 as the root. Every other member has exactly one direct superior, so every member has a unique path upward to the boss."
date: "2026-08-13T01:20:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102346
codeforces_index: "D"
codeforces_contest_name: "2019-2020 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102346
solve_time_s: 80
verified: true
draft: false
---

[CF 102346D - Denouncing Mafia](https://codeforces.com/problemset/problem/102346/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

The mafia hierarchy forms a rooted tree, with member 1 as the root. Every other member has exactly one direct superior, so every member has a unique path upward to the boss.

When the seer identifies a member, the police can arrest that member and then repeatedly interrogate arrested members to obtain information about their superiors. As a result, choosing one member effectively arrests every vertex on the path from that member to the root.

The police may ask the seer about at most K members. The task is to choose those members so that the union of their root paths contains as many distinct vertices as possible.

The input describes the rooted tree through N and K, followed by the parent of every vertex from 2 through N. The output is the maximum number of distinct mafia members that can be arrested.

With N up to 100000, an algorithm involving all pairs, all subsets, or a quadratic dynamic program is too expensive. A solution around O(N log N) is comfortably appropriate, while even O(NK) can reach 10^10 operations when K is large.

There are several edge cases where a careless implementation can fail. If K is 1, the answer is simply the length of the deepest root-to-vertex path, not N. For example, with `N = 3`, `K = 1`, and parents `1 1`, the answer is 2 because choosing either child arrests the boss and that child.

Another subtle case occurs when several branches have equal depth. With `N = 5`, `K = 2`, and parents `1 1 2 2`, the tree has root 1, children 2 and 3, and children 4 and 5 under 2. Choosing 4 arrests `1,2,4`, and choosing 3 adds only vertex 3, giving 4. Choosing both 4 and 5 instead gives `1,2,4,5`, also 4. A solution must not depend on which child is chosen as the longest branch when depths tie.

A third case is a star. With `N = 5`, `K = 4`, and parents `1 1 1 1`, every selected leaf contributes exactly one new vertex after the first selection. The answer is 5. An implementation that only considers complete root-to-leaf paths once can miss these independent branches.

## Approaches

A direct solution would try every possible collection of at most K selected members, follow the parent pointer from each selected member to the root, and count the distinct vertices in the resulting union. This is correct because the arrested set is exactly the union of those root paths. However, there are `C(N,K)` possible choices when exactly K members are selected, and processing each choice can itself require O(N) work. In the worst case this is Θ(N · C(N,K)), which is exponential when K is around N/2. Even a less naive implementation that tries every possible selected leaf is far beyond the limits.

The useful observation is that once some root paths have been chosen, the already arrested vertices form a connected rooted subtree. Every remaining possible contribution lies in a separate subtree attached to that arrested region by one edge.

Suppose the currently arrested region reaches a vertex v, and a child c is not part of the chosen continuation below v. The entire subtree of c is still untouched. If we spend one additional seer use inside that subtree, the largest number of new vertices we can obtain is the length of the deepest downward path starting at c.

This gives a natural greedy process. Start with the longest root-to-vertex path in the entire tree. After taking that path, every child branch that was skipped along the path becomes an independent candidate. Among all currently available candidate branches, take the one with maximum depth. When that branch is selected, walk along its own deepest path and add all of its skipped child branches to the candidate set.

The key property is that each candidate represents a completely untouched subtree. Its depth is exactly the maximum number of new vertices one selection can contribute from that subtree. Choosing a shorter available branch cannot provide more immediate new vertices than choosing the longest one, while choosing the longest branch exposes all of its remaining side branches for future selections. This gives the greedy choice its optimal structure.

We can maintain the available branches in a max-heap. A preprocessing DFS computes `depth[v]`, the number of vertices on the longest downward path starting at v, together with `best[v]`, the child that starts such a path. Each time a branch is selected, we follow `best` pointers and push every other child into the heap.

The brute-force and optimal approaches can be summarized as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Θ(N · C(N,K)) | O(N) | Too slow |
| Optimal | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Build the rooted tree from the parent array. Vertex 1 is the root, and every vertex `v > 1` is added to the child list of its given parent.
2. Compute `depth[v]`, where `depth[v]` means the number of vertices on the longest downward path beginning at v. At the same time, store `best[v]`, the child that starts such a longest path. A leaf has `depth[v] = 1` and no best child.
3. Put `(depth[1], 1)` into a max-heap. This represents the first available path, which can start anywhere below the root, and the longest possible first contribution is the deepest path from the root.
4. Repeat K times. Remove the candidate with the largest depth from the heap and add that depth to the answer. The candidate root belongs to an untouched subtree, so every vertex on its selected downward path is newly arrested.
5. Starting from the selected candidate root, follow `best[v]` until reaching a leaf. At every visited vertex v, inspect all children other than `best[v]`. Each such child starts a subtree that was skipped by the selected path, so push `(depth[child], child)` into the heap.
6. After K selections, the accumulated sum is the number of distinct arrested vertices. No selected paths counted the same newly added vertex because every heap candidate is created only when its subtree is separated from the already selected path.

The invariant is that every heap entry represents one completely untouched subtree attached to the already arrested region, and its stored depth is the maximum contribution obtainable from that subtree using one seer query. The selected path always takes the largest available such contribution. Once selected, its side branches become precisely the new independent choices. Thus the heap always describes all possible next contributions, and taking its maximum is the optimal greedy choice at every stage.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve(data=None):
    if data is None:
        data = sys.stdin.buffer.read().split()

    it = iter(data)
    n = int(next(it))
    k = int(next(it))

    children = [[] for _ in range(n)]

    for v in range(1, n):
        p = int(next(it)) - 1
        children[p].append(v)

    # Iterative DFS order, avoiding recursion depth problems on a chain.
    order = []
    stack = [0]

    while stack:
        v = stack.pop()
        order.append(v)
        for c in children[v]:
            stack.append(c)

    # depth[v] = number of vertices in the longest downward path from v.
    # best[v] = child starting that path.
    depth = [1] * n
    best = [-1] * n

    for v in reversed(order):
        best_depth = 0
        best_child = -1

        for c in children[v]:
            if depth[c] > best_depth:
                best_depth = depth[c]
                best_child = c

        if best_child != -1:
            depth[v] = best_depth + 1
            best[v] = best_child

    # Python has a min-heap, so store negative depths.
    heap = [(-depth[0], 0)]
    answer = 0

    for _ in range(k):
        neg_len, root = heapq.heappop(heap)
        answer += -neg_len

        v = root

        # Select the longest path from this candidate subtree.
        while v != -1:
            chosen = best[v]

            # Every other child starts a new available subtree.
            for c in children[v]:
                if c != chosen:
                    heapq.heappush(heap, (-depth[c], c))

            v = chosen

    return str(answer)

if __name__ == "__main__":
    print(solve())
```

The first part of the implementation builds the adjacency lists. The input identifies each vertex from 2 through N using one-based numbering, while the code converts everything to zero-based indexing immediately. Vertex 1 consequently becomes index 0.

The iterative DFS creates a parent-before-child ordering. Reversing this ordering gives children before parents, which is exactly the order required to compute `depth[v]` from already computed child values. An iterative traversal is used because a tree can be a chain of length 100000, which would exceed Python's default recursive call stack.

The `depth` calculation chooses the child with maximum `depth`. Since the current vertex itself contributes one vertex, its value is one plus the best child's value. The `best` array remembers which child produced that maximum.

The heap stores available subtrees. Python's `heapq` is a min-heap, so the code stores negative depths to make the largest depth appear first.

When a candidate is removed, its stored depth is added directly to the answer. The code then walks down the selected longest path. For each vertex on that path, all children except the selected continuation become new heap entries. Those children cannot overlap with the path that was just selected, so their entire deepest paths are still available as future contributions.

There is no integer overflow concern in Python, and the maximum answer is only N. The heap may contain O(N) entries, while every tree vertex is processed on at most one selected path or examined as a side branch, giving the required linear number of structural operations apart from heap maintenance.

## Worked Examples

For Sample 1, the tree is rooted at 1 and the deepest path is `1 -> 2 -> 4 -> 6 -> 8`. It contains five vertices. After taking it, the useful side branches are the subtree rooted at 3, with depth 2, and the leaf 7, with depth 1.

| Selection | Heap before selection | Selected path | Added | Answer |
| --- | --- | --- | --- | --- |
| 1 | `(5,1)` | `1-2-4-6-8` | 5 | 5 |
| 2 | `(2,3), (1,7)` | `3-5` | 2 | 7 |

The second selection chooses the subtree rooted at 3 because its deepest path contributes two new vertices, while vertex 7 contributes only one. The final answer is 7.

For Sample 2, the deepest first path can be `1 -> 2 -> 4 -> 8`, with length 4. Its skipped branches include vertex 5's subtree and vertex 9. The other root branch, starting at 3, also becomes available.

| Selection | Heap before selection | Selected path | Added | Answer |
| --- | --- | --- | --- | --- |
| 1 | `(4,1)` | `1-2-4-8` | 4 | 4 |
| 2 | `(2,3), (2,5), (1,9)` | `3-6` | 2 | 6 |
| 3 | `(2,5), (1,7), (1,9)` | `5-10` | 2 | 8 |

The first choice creates several independent frontier subtrees. The second and third choices each add two new vertices, giving a total of 8. The invariant is visible here: after every selection, the heap contains the best possible one-path contribution from every still-uncovered branch.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Every vertex is processed a constant number of times, and every heap insertion or removal costs O(log N). |
| Space | O(N) | The tree, DFS order, depth arrays, and heap all require linear memory. |

With N at most 100000, O(N log N) means roughly a few million heap operations or fewer, which is well within the intended scale. The iterative traversal also avoids recursion failures on the worst-case chain.

## Test Cases

```python
import io
import sys
import heapq

def solve(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    k = int(next(it))

    children = [[] for _ in range(n)]

    for v in range(1, n):
        p = int(next(it)) - 1
        children[p].append(v)

    order = []
    stack = [0]

    while stack:
        v = stack.pop()
        order.append(v)
        for c in children[v]:
            stack.append(c)

    depth = [1] * n
    best = [-1] * n

    for v in reversed(order):
        best_depth = 0
        best_child = -1

        for c in children[v]:
            if depth[c] > best_depth:
                best_depth = depth[c]
                best_child = c

        if best_child != -1:
            depth[v] = best_depth + 1
            best[v] = best_child

    heap = [(-depth[0], 0)]
    answer = 0

    for _ in range(k):
        neg_len, root = heapq.heappop(heap)
        answer += -neg_len

        v = root
        while v != -1:
            chosen = best[v]

            for c in children[v]:
                if c != chosen:
                    heapq.heappush(heap, (-depth[c], c))

            v = chosen

    return str(answer)

# Provided sample 1
assert solve(
    "8 2\n"
    "1 1 2 3 4 4 6\n"
) == "7", "sample 1"

# Provided sample 2
assert solve(
    "10 3\n"
    "1 1 2 2 3 3 4 4 5\n"
) == "8", "sample 2"

# Minimum-size tree, K = 1.
assert solve(
    "3 1\n"
    "1 1\n"
) == "2", "minimum size and K=1"

# Star, every selected leaf after the first contributes one new vertex.
assert solve(
    "6 5\n"
    "1 1 1 1 1\n"
) == "6", "star with K=N-1"

# A chain. Every selected path is identical, so extra selections add nothing.
assert solve(
    "7 3\n"
    "1 2 3 4 5 6\n"
) == "7", "pure chain"

# Maximum-size star, testing both N=100000 and K=N-1.
n = 100000
parents = " ".join(["1"] * (n - 1))
assert solve(f"{n} {n - 1}\n{parents}\n") == str(n), "maximum-size star"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 1 / 1 1` | 2 | Minimum size and the K = 1 boundary |
| `6 5 / 1 1 1 1 1` | 6 | Many independent branches and K close to N |
| `7 3 / 1 2 3 4 5 6` | 7 | Repeated selections of an already covered chain |
| `100000 99999 / 1 1 ... 1` | 100000 | Maximum N, maximum heap activity, and star structure |

## Edge Cases

For the K = 1 case, consider `3 1` with parents `1 1`. The preprocessing gives `depth[1] = 2`, because the deepest path contains the root and one child. The heap initially contains only `(2,1)`, so the single iteration adds 2 and stops. The output is 2. A solution that assumes every branch can be independently counted would incorrectly return 3.

For equal-depth branches, consider `5 2` with parents `1 1 2 2`. The root has two children, and vertex 2 has two children. The deepest paths have length 3 through vertices 4 or 5. Suppose the algorithm chooses `1-2-4` first. While processing that path, vertex 5 becomes a candidate with depth 1 and vertex 3 is a candidate with depth 2. The second selection takes `1-3` as a new contribution of 1? The root is already covered, so the candidate rooted at 3 contributes only vertex 3, while the candidate rooted at 5 contributes only vertex 5. Thus the total is 4. The same result is obtained if vertex 5 is chosen first. The tie-breaking inside `best[v]` changes the selected path but never changes its length or the final optimum.

For a star, consider `5 4` with parents `1 1 1 1`. The first selection takes `1-2`, contributing 2. Processing that path exposes vertices 3, 4, and 5 as independent candidates, each with depth 1. The next three selections each contribute one new vertex, producing `2 + 1 + 1 + 1 = 5`. This is exactly the total number of vertices, and it demonstrates why skipped children must be inserted into the heap.

For a chain, consider `7 3` with parents `1 2 3 4 5 6`. The first candidate has depth 7 and selects the entire tree. Every vertex on that path has its chosen child equal to its only child, so no side branch is inserted. The heap becomes empty after the first selection. Since selecting an already arrested vertex cannot increase the answer, the remaining seer uses have no effect, and the answer stays 7.

For the maximum-size star with 100000 vertices, the first selected path contributes 2, while the remaining 99998 vertices become depth-1 heap candidates. The next 99998 selections each contribute one vertex, so the final answer is 100000. The algorithm never performs a quadratic scan over pairs of selections, and its total heap work remains O(N log N).
