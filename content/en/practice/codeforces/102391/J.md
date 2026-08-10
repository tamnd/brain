---
title: "CF 102391J - Parklife"
description: "Each bridge can be represented by the half-open interval ([Si,Ei)). A bridge is visible from the small arc between consecutive points (i) and (i+1) exactly when that arc lies inside this interval. The input contains (N) weighted bridges."
date: "2026-08-10T20:10:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "J"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 193
verified: true
draft: false
---

[CF 102391J - Parklife](https://codeforces.com/problemset/problem/102391/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

Each bridge can be represented by the half-open interval ([S_i,E_i)). A bridge is visible from the small arc between consecutive points (i) and (i+1) exactly when that arc lies inside this interval.

The input contains (N) weighted bridges. We may choose any subset of them, but for every elementary arc, at most (k) chosen bridges may cover it. Since every aesthetic value is positive, the task is to maximize the total value of the chosen bridges. We need this maximum for every (k=1,2,\ldots,N).

The geometric condition is much stronger than it first appears. Two bridge segments cannot cross, so their visibility intervals can never partially overlap. For any two intervals, they are either disjoint or one completely contains the other. This laminar structure is the central property of the problem. The official editorial makes the same reduction by viewing the intervals as matching pairs of brackets and then forming a parse tree.

The value of (N) can reach (250,000), so an (O(N^2)) dynamic program would examine at least (62.5) billion states in the worst case. That is far beyond what a 2 second contest limit can tolerate. The coordinate range reaches (10^6), but that does not mean we should build an array over all coordinates and run a coordinate-based DP. The useful structure is determined by the (N) bridges themselves, so the algorithm should be close to (O(N\log N)).

There are several boundary cases that are easy to mishandle.

Consider a single bridge.

```
1
1 2 7
```

There is only one bridge, so every allowed (k\ge1) selects it. The answer is

```
7
```

A careless implementation that treats the interval as closed rather than half-open can incorrectly make bridges touching at an endpoint overlap. For example,

```
2
1 2 5
2 3 7
```

The two visible intervals are ([1,2)) and ([2,3)), so they are disjoint. Both bridges can be selected even for (k=1), giving

```
12 12
```

Another important case is a chain of nested intervals.

```
3
1 6 10
2 5 20
3 4 30
```

For (k=1), only the value (30) bridge can be selected. For (k=2), the inner two bridges can be selected, and for (k=3) all three can be selected. The correct output is

```
30 50 60
```

A solution that simply takes the best (k) values globally would fail because the nesting constraint depends on where the bridges overlap.

Finally, intervals can have the same left endpoint. For example,

```
3
1 5 10
1 4 20
2 3 30
```

The correct containment order is ([1,5)) containing ([1,4)) containing ([2,3)). Sorting only by the left endpoint is not enough to recover that order. When left endpoints are equal, the longer interval must come first.

## Approaches

A direct tree DP is the natural first attempt. Once the intervals are converted into a containment tree, define (F_u(k)) as the maximum value obtainable from the subtree of (u) when every root-to-descendant path contains at most (k) selected vertices. For every node and every (k), we could calculate this value by considering whether (u) itself is selected.

This DP is correct because every feasible selection has exactly one of those two possibilities. If (u) is not selected, every child subtree still has capacity (k). If (u) is selected, it consumes one unit of capacity for every interval inside it, so every child receives capacity (k-1). The problem is the number of states. There are (O(N^2)) possible pairs ((u,k)), giving at least (62.5) billion states when (N=250,000), before accounting for the work needed to combine children.

The brute-force DP works because the containment tree captures every interaction between bridges. It fails because it stores the same information separately for every (k), even though the values for consecutive (k) have a strong structure.

The key observation is that each subtree's DP as a function of (k) has diminishing marginal gains. Define

[
D_u(k)=F_u(k)-F_u(k-1).
]

These differences are non-increasing. We can consequently represent the entire function (F_u) by the multiset of its marginal gains instead of storing every DP value.

Suppose the children of (u) have marginal sequences (A,B,\ldots). Their intervals are disjoint, so all children can use the same (k) layers independently. If the marginal gains of two children are

[
a_1\ge a_2\ge\cdots
]

and

[
b_1\ge b_2\ge\cdots,
]

then the combined subtree has marginal gains

[
a_1+b_1,\ a_2+b_2,\ldots.
]

After combining all children, consider the bridge (u) itself with value (w_u). Selecting it consumes one layer, so the resulting DP is equivalent to inserting one additional marginal gain (w_u) into the sorted marginal sequence.

This is exactly the structure described by the official solution: child functions are combined by pairwise addition of their sorted derivatives, and adding a node corresponds to inserting its weight into that derivative set.

A max-heap stores the marginal gains. To combine two child heaps, repeatedly remove their largest elements, add those two values, and put the resulting value into the parent heap. We always merge the smaller heap into the larger one. This is the standard small-to-large technique, and the official analysis gives an (O(N\log N)) bound for the whole heap process.

The final virtual root has value zero and contains every bridge. Its heap represents the marginal improvement obtained by increasing (k). We repeatedly take the largest remaining marginal gain and accumulate it. Once the heap becomes empty, the answer has already reached its maximum and stays unchanged for all larger (k).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive tree DP | (O(N^2)) | (O(N^2)) or (O(N)) with recomputation | Too slow |
| Optimal heap DP | (O(N\log N)) | (O(N)) active heap entries plus the tree | Accepted |

## Algorithm Walkthrough

1. Represent every bridge by its visibility interval ([S_i,E_i)). Because bridges never cross, any two such intervals are either disjoint or nested. This turns the geometric problem into a laminar interval problem.
2. Add a virtual interval containing the entire coordinate range and give it value zero. This virtual node becomes the root, allowing several top-level disjoint bridges to coexist in one tree.
3. Sort the real intervals by increasing left endpoint, breaking ties by decreasing right endpoint. This is the preorder of the containment tree. When the left endpoints are equal, the larger interval must appear first because it is the ancestor.
4. Scan the sorted intervals with a stack. The stack contains the current path from the virtual root to the most recently processed interval. For a new interval ([S,E)), pop intervals whose right endpoint is smaller than (E). The interval remaining on top is exactly the smallest interval that contains the new one, so it becomes the new interval's parent.
5. Process the tree bottom-up. For every node (u), maintain a max-heap containing the marginal gains of its DP function. A leaf starts with the single value (w_u).
6. For an internal node, first combine the heaps of all its children. If two heaps contain marginal sequences (A) and (B), remove their largest elements pairwise and insert their sums. This computes the marginal sequence of (F_A(k)+F_B(k)), because both independent subtrees receive the same capacity (k).
7. Always use the larger heap as the destination heap. If the current heap has fewer elements than another child's heap, swap them before merging. Only elements from the smaller heap need to be removed, which gives the small-to-large bound.
8. After all children have been combined, insert (w_u) into the heap. This represents the choice of selecting (u), which consumes one additional nesting level and contributes exactly (w_u) to the corresponding marginal gain.
9. At the virtual root, repeatedly remove the largest marginal gain. Add it to a running answer and print that running answer for the next value of (k). If the heap is empty, keep printing the same answer because no further bridge can improve the solution.

Why it works: for every node (u), the heap invariant is that its elements are exactly the marginal gains (F_u(k)-F_u(k-1)), arranged in non-increasing order. Independent child subtrees add their DP functions, so their marginal gains add position by position. Adding (u) itself changes the DP from (G(k)) to (\max(G(k),w_u+G(k-1))), which is exactly the operation of inserting (w_u) into the sorted marginal gains of (G). Thus the invariant holds inductively from leaves to the root. At the root, taking the largest (k) marginal gains gives (F_{\text{root}}(k)), which is precisely the maximum total aesthetic value under capacity (k).

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve(stream=None):
    if stream is None:
        stream = sys.stdin

    read = stream.readline
    n = int(read())

    intervals = []
    for _ in range(n):
        s, e, w = map(int, read().split())
        intervals.append((s, e, w))

    # Increasing left endpoint, decreasing right endpoint.
    intervals.sort(key=lambda x: (x[0], -x[1]))

    # Node 0 is the virtual root.
    # Its interval contains every real interval and its value is zero.
    end = [1_000_001] + [0] * n
    weight = [0] * (n + 1)

    parent = [0] * (n + 1)

    # Children are stored as linked lists to avoid creating
    # N separate Python list objects.
    head = [-1] * (n + 1)
    nxt = [-1] * (n + 1)

    stack = [0]

    for u, (s, e, w) in enumerate(intervals, 1):
        end[u] = e
        weight[u] = w

        # Since left endpoints are processed increasingly,
        # containment is determined by the right endpoint here.
        while e > end[stack[-1]]:
            stack.pop()

        p = stack[-1]
        parent[u] = p

        nxt[u] = head[p]
        head[p] = u

        stack.append(u)

    # Each heap stores negative marginal gains, so heapq acts
    # as a max-heap on the original positive values.
    heaps = [None] * (n + 1)

    # Parent IDs are always smaller than child IDs because the
    # intervals were processed in preorder.
    for u in range(n, -1, -1):
        h = None
        child = head[u]

        while child != -1:
            other = heaps[child]

            if h is None:
                h = other
            else:
                # Always merge the smaller heap into the larger heap.
                if len(other) > len(h):
                    h, other = other, h

                m = len(other)

                # Pair the largest marginal gains.
                merged = [
                    heapq.heappop(h) + heapq.heappop(other)
                    for _ in range(m)
                ]

                # Rebuild once instead of performing m separate pushes.
                h.extend(merged)
                heapq.heapify(h)

            # The child heap has now been completely consumed.
            heaps[child] = None
            child = nxt[child]

        if h is None:
            h = []

        # Selecting u contributes one new marginal gain w[u].
        heapq.heappush(h, -weight[u])
        heaps[u] = h

    # Extract marginal gains from the virtual root.
    h = heaps[0]
    answer = 0
    result = []

    for _ in range(n):
        if h:
            answer -= heapq.heappop(h)
        result.append(str(answer))

    return " ".join(result)

if __name__ == "__main__":
    sys.stdout.write(solve() + "\n")
```

The input intervals are sorted before the tree is constructed. The tie breaker is `-x[1]`, so if two bridges start at the same point, the larger interval is processed first and can become the ancestor of the smaller one.

The stack condition uses `e > end[stack[-1]]`, not `>=`. Equal right endpoints are allowed because one interval can contain another while sharing its right endpoint. The visibility intervals are half-open, so bridges ending at one point and bridges starting at that same point are disjoint, which is naturally handled by the stack after the previous interval is popped.

The tree is stored using `head` and `nxt` instead of a list for every node. This reduces Python object overhead substantially when (N) is large. Because the sorted intervals form a preorder, every parent has a smaller node index than every descendant, so a reverse numerical traversal is enough for bottom-up DP and avoids recursion depth problems.

The heap stores negative values because Python's `heapq` is a min-heap. The largest original marginal gain is consequently the smallest stored value. During a child merge, the largest elements are removed from both heaps and their negative representations are added. If the original gains are (a) and (b), the stored values are (-a) and (-b), and their sum is (-(a+b)), exactly what the merged heap needs.

The `merged` list is built first and then appended to the destination heap followed by one `heapify`. Repeatedly calling `heappush` would perform unnecessary logarithmic work for every new merged value. Python integers have arbitrary precision, so the total aesthetic value, which can reach (250,000\cdot10^9=2.5\cdot10^{14}), requires no special overflow handling.

The final extraction deliberately continues after the heap becomes empty. Missing marginal gains mean that increasing (k) further cannot improve the answer, so the running total simply remains unchanged.

## Worked Examples

For Sample 1, the containment tree has two major branches. The first contains the intervals ([1,2)), ([2,3)), and their parent ([1,3)). The second contains ([3,4)), ([4,5)), and their parent ([3,5)).

| Processed node | Child marginal sequences | After combining children | After inserting node value |
| --- | --- | --- | --- |
| ([1,2),10) | none | `[]` | `[10]` |
| ([2,3),10) | none | `[]` | `[10]` |
| ([1,3),21) | `[10]`, `[10]` | `[20]` | `[21,20]` |
| ([3,4),10) | none | `[]` | `[10]` |
| ([4,5),10) | none | `[]` | `[10]` |
| ([3,5),19) | `[10]`, `[10]` | `[20]` | `[20,19]` |
| virtual root, 0 | `[21,20]`, `[20,19]` | `[41,39]` | `[41,39,0]` |

The first marginal gain is (41), so (k=1) gives (41). The second marginal gain is (39), so (k=2) gives (80). The remaining marginal gain is zero, so every larger (k) also gives (80). This produces the sample output `41 80 80 80 80 80`.

For Sample 2, every interval contains the next one:

[
[1,5)\supset[2,5)\supset[3,5)\supset[4,5).
]

Every bridge has value (1).

| Processed node | Child marginal sequence | After inserting value 1 |
| --- | --- | --- |
| ([4,5),1) | `[]` | `[1]` |
| ([3,5),1) | `[1]` | `[1,1]` |
| ([2,5),1) | `[1,1]` | `[1,1,1]` |
| ([1,5),1) | `[1,1,1]` | `[1,1,1,1]` |
| virtual root, 0 | `[1,1,1,1]` | `[1,1,1,1,0]` |

The first four positive marginal gains are all (1). Consequently the answers are (1,2,3,4). The zero contributed by the virtual root does not change the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N)) | Sorting costs (O(N\log N)), and the small-to-large heap processing is (O(N\log N)) overall |
| Space | (O(N)) | The interval arrays, containment tree, and active heap entries contain (O(N)) elements |

The (250,000) bridge limit makes quadratic DP impossible, while (O(N\log N)) is appropriate for the input size. The coordinate bound of (10^6) never appears as a multiplicative factor because the algorithm only works with the supplied bridges and their containment relationships. The arbitrary-precision integer representation in Python is also sufficient for the maximum possible total value.

## Test Cases

```
# The solution is written so solve(stream) can be tested directly.
import io

def run(inp: str) -> str:
    return solve(io.StringIO(inp))

# Provided sample 1
assert run(
    """6
1 2 10
2 3 10
1 3 21
3 4 10
4 5 10
3 5 19
"""
) == "41 80 80 80 80 80", "sample 1"

# Provided sample 2
assert run(
    """4
1 5 1
2 5 1
3 5 1
4 5 1
"""
) == "1 2 3 4", "sample 2"

# Minimum-size input.
assert run(
    """1
1 2 7
"""
) == "7", "single bridge"

# Three disjoint bridges. They can all be selected already for k = 1.
assert run(
    """3
1 2 5
2 3 7
4 5 3
"""
) == "15 15 15", "disjoint intervals"

# A pure nesting chain.
assert run(
    """3
1 6 10
2 5 20
3 4 30
"""
) == "30 50 60", "nested chain"

# Endpoint touching plus an inner interval.
# [1,2) and [2,5) are disjoint, while [3,4) is nested in [2,5).
assert run(
    """3
1 2 5
2 5 100
3 4 7
"""
) == "105 112 112", "endpoint boundary"

# Same left endpoint, forcing the decreasing-right-endpoint tie breaker.
assert run(
    """3
1 5 10
1 4 20
2 3 30
"""
) == "30 50 60", "equal left endpoints"

# Maximum-size stress case.
# All 250000 intervals are pairwise disjoint and have value 1,
# so every answer is exactly 250000.
n = 250000
stress_input = str(n) + "\n" + "".join(
    f"{2 * i - 1} {2 * i} 1\n" for i in range(1, n + 1)
)
expected = " ".join(["250000"] * n)

assert run(stress_input) == expected, "maximum-size disjoint input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 2 7` | `7` | Minimum (N), single-node tree, and root handling |
| Three touching or disjoint intervals | `15 15 15` | Half-open visibility intervals and independent sibling subtrees |
| `1 6`, `2 5`, `3 4` | `30 50 60` | Pure nesting and successive marginal gains |
| `1 2`, `2 5`, `3 4` | `105 112 112` | Endpoint touching combined with nesting |
| `1 5`, `1 4`, `2 3` | `30 50 60` | Equal left endpoints and decreasing-right-endpoint sorting |
| 250000 disjoint unit intervals | `250000` repeated 250000 times | Maximum (N), large output, heap and tree scalability |

## Edge Cases

The single-bridge case is handled by creating a leaf heap containing its value. For

```
1
1 2 7
```

the bridge heap is `[7]`, the virtual root combines that heap with no other child, and inserts its own zero. The first extraction adds (7), giving the required output `7`.

For touching intervals,

```
2
1 2 5
2 3 7
```

the first bridge corresponds to ([1,2)), while the second corresponds to ([2,3)). When the second interval is processed, the first interval no longer contains it, so the stack returns to the virtual root. They become siblings. Their one-element marginal heaps are combined as (5+7=12), giving a single positive marginal gain of (12). The output is `12 12`. Treating intervals as closed would incorrectly make these bridges conflict for (k=1).

For a nested chain,

```
3
1 6 10
2 5 20
3 4 30
```

the tree is a path. The innermost bridge starts with marginal sequence `[30]`. Its parent inserts (20), producing `[30,20]`, and the outer bridge inserts (10), producing `[30,20,10]`. The root adds zero. Extracting these gains gives `30`, then `50`, then `60`. This is exactly the optimum because each additional unit of allowed overlap lets us select one more bridge in the chain.

For equal left endpoints,

```
3
1 5 10
1 4 20
2 3 30
```

sorting by `(left, -right)` places ([1,5)) before ([1,4)). The stack consequently identifies the containment chain correctly. If the tie breaker were reversed, ([1,4)) could incorrectly be treated as unrelated to its true ancestor. The resulting marginal sequence is `[30,20,10]`, giving `30 50 60`.

For the maximum-size disjoint case, every bridge becomes a separate child of the virtual root. Each child contributes one marginal gain of (1). Since the children are disjoint, their values are combined into a single marginal gain of (250000). There is no benefit from increasing (k), so every one of the (250000) answers is `250000`. This case also exercises the small-to-large heap merging and confirms that the implementation does not depend on the coordinate range being close to (N).

The central idea to carry to similar problems is the marginal-gain representation: once a laminar constraint becomes a tree, the entire k-dimensional DP can collapse into one ordered collection of gains per subtree.
