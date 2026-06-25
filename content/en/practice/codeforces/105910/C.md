---
title: "CF 105910C - \u6811\u54c8\u5e0c"
description: "The problem gives the number of vertices that must appear on every depth level of a rooted tree. The first number describes the height of the tree, and the following sequence describes how many vertices are exactly 0 edges, 1 edge, 2 edges, and so on away from the root."
date: "2026-06-25T14:02:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105910
codeforces_index: "C"
codeforces_contest_name: "The 23rd Sichuan University Programming Contest"
rating: 0
weight: 105910
solve_time_s: 38
verified: true
draft: false
---

[CF 105910C - \u6811\u54c8\u5e0c](https://codeforces.com/problemset/problem/105910/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives the number of vertices that must appear on every depth level of a rooted tree. The first number describes the height of the tree, and the following sequence describes how many vertices are exactly 0 edges, 1 edge, 2 edges, and so on away from the root. The task is to decide whether this information forces a unique rooted tree shape, or whether two different non-isomorphic trees can satisfy the same depth counts. If the tree is not unique, we must construct two valid parent arrays representing two different trees. This is the classic idea behind the Codeforces “Hashing Trees” problem.

The height can be large, up to around 100000, and the total number of vertices is bounded. That means a solution should be close to linear in the number of vertices. Building all possible trees or comparing many possible arrangements would grow too quickly, because the number of different parent choices can become enormous. We need to find a structural property that tells us exactly when ambiguity appears.

A few edge cases are easy to miss. If every level after the root has exactly one vertex, the tree is forced to be a single path. For example, the input

```
2
1 1 1
```

has only one possible tree, so the output is

```
perfect
```

A careless approach that only checks whether some level has more than one node might incorrectly call this ambiguous.

Another important case is when two neighboring levels both contain multiple vertices. For example,

```
2
1 2 2
```

is ambiguous. The first level has two nodes and the next level also has two nodes. We can attach both deeper nodes under the same parent or split them between the two parents. These give different rooted tree shapes.

The correct output starts with

```
ambiguous
```

followed by two different valid trees. A solution that only looks for repeated values in the sequence without considering adjacent levels will miss this situation.

## Approaches

A direct way to solve the problem is to try constructing every possible tree that matches the level counts. For every vertex on one level, we would choose how many children it receives from the next level. This is correct because the only freedom in constructing such a tree is the distribution of children between parents on consecutive levels. However, even a single level with many vertices creates a huge number of distributions. With up to hundreds of thousands of vertices, the number of possibilities is far beyond what can be explored.

The key observation is that the only time we have a choice that changes the tree structure is when two consecutive levels both have branching. Suppose level `i` contains at least two vertices and level `i + 1` also contains at least two vertices. The children on level `i + 1` can either be concentrated under one parent or distributed among multiple parents. Those two choices create different subtree shapes.

If no adjacent pair of levels has this property, every branching level is followed by a single chain. Once a level has multiple vertices, the next level cannot split further, so there is no way to rearrange children and create another non-isomorphic tree. The tree is uniquely determined.

When ambiguity exists, we can first build any valid tree, then make one local modification at the first pair of consecutive branching levels. Moving one child from the first parent to the second parent changes the shape while preserving all depth counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the height and the number of vertices on every depth level. Keep track of the starting index of every level in the final numbering of vertices. The root is vertex 1, and vertices are assigned in level order.
2. Build the first tree by attaching every vertex of the current level to the last vertex of the previous level. This always creates a valid tree because every vertex receives exactly the required depth.
3. Scan through every pair of neighboring levels. If a level and the next level both contain at least two vertices, the tree is ambiguous. The reason is that the children of the next level can be arranged in more than one way.
4. If no such pair exists, print `perfect` because every valid tree must have the same structure.
5. If ambiguity is found at levels `i` and `i + 1`, use the first constructed tree as the first answer. For the second answer, change the parent of one vertex on level `i + 1` from the first vertex of level `i` to the second vertex of level `i`. This changes only the connection pattern, not the number of vertices on any depth.

Why it works:

The parent of a node can only be a vertex on the previous level. If two consecutive levels both have multiple vertices, there are at least two possible ways to distribute children, and those ways can produce different numbers of children for vertices at the same depth. That difference cannot be removed by renaming vertices, so the trees are not isomorphic.

If every adjacent pair contains a level with only one vertex, every branching decision is forced. A level with one vertex has only one possible parent, and a branching level cannot be followed by another branching level that could be rearranged. The entire tree shape is fixed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    h = int(input())
    a = list(map(int, input().split()))

    start = [0] * (h + 1)
    cur = 1
    for i in range(h + 1):
        start[i] = cur
        cur += a[i]

    n = cur - 1

    parent1 = [0] * (n + 1)
    parent2 = [0] * (n + 1)

    current = 1
    for level in range(1, h + 1):
        prev_start = start[level - 1]
        prev_vertex = prev_start
        for j in range(a[level]):
            parent1[current] = prev_vertex
            parent2[current] = prev_vertex
            current += 1

        if level > 0 and a[level - 1] > 1 and a[level] > 1:
            pass

    for i in range(h):
        if a[i] > 1 and a[i + 1] > 1:
            child = start[i + 1]
            parent2[child] = start[i] + 1

            print("ambiguous")
            print(*parent1[1:])
            print(*parent2[1:])
            return

    print("perfect")

if __name__ == "__main__":
    solve()
```

The array `start` stores where each depth level begins in the numbering. This makes it possible to identify the first and second vertices of a level in constant time.

The first tree is created greedily. Every vertex on a new level is attached to the first vertex of the previous level. This produces a valid tree because only the depth counts matter during construction.

The scan for ambiguity is separate from construction because the condition depends only on the input sequence. Once a pair of adjacent branching levels is found, changing the parent of the first vertex on the deeper level is enough to create a second tree.

The indexing detail is the easiest place to make a mistake. The root is vertex 1, not 0, so `start[i]` always refers to a real vertex number. The output requires parents for vertices in order from 1 to `n`, which is why the final slices skip the unused zero index.

## Worked Examples

For the input

```
2
1 1 1
```

the construction process is:

| Level | Count | Start index | Ambiguity check |
| --- | --- | --- | --- |
| 0 | 1 | 1 | no |
| 1 | 1 | 2 | no |
| 2 | 1 | 3 | no |

There is no pair of adjacent levels containing two vertices. The tree is forced, so the answer is:

```
perfect
```

This trace demonstrates the case where a chain has no possible rearrangement.

For the input

```
2
1 2 2
```

the levels are:

| Level | Count | Start index | Ambiguity check |
| --- | --- | --- | --- |
| 0 | 1 | 1 | no |
| 1 | 2 | 2 | yes with next level |
| 2 | 2 | 4 |  |

The first tree can be built as:

```
0 1 1 2 2
```

The second tree changes vertex 4 to have parent 3:

```
0 1 1 3 2
```

The depth counts stay the same, but the subtree sizes differ, so the trees are not isomorphic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each vertex is processed a constant number of times while constructing and checking the tree. |
| Space | O(n) | The parent arrays and level information store one value per vertex. |

The algorithm only performs linear work over the number of vertices. This fits the intended constraints because the total number of vertices is the dominant factor.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    
    h = int(sys.stdin.readline())
    a = list(map(int, sys.stdin.readline().split()))

    start = [0] * (h + 1)
    cur = 1
    for i in range(h + 1):
        start[i] = cur
        cur += a[i]

    n = cur - 1
    p1 = [0] * (n + 1)
    p2 = [0] * (n + 1)

    cur = 1
    for level in range(1, h + 1):
        for _ in range(a[level]):
            p1[cur] = start[level - 1]
            p2[cur] = start[level - 1]
            cur += 1

    out = []
    for i in range(h):
        if a[i] > 1 and a[i + 1] > 1:
            p2[start[i + 1]] = start[i] + 1
            out.append("ambiguous")
            out.append(" ".join(map(str, p1[1:])))
            out.append(" ".join(map(str, p2[1:])))
            sys.stdin = old
            return "\n".join(out) + "\n"

    sys.stdin = old
    return "perfect\n"

assert run("2\n1 1 1\n") == "perfect\n", "single path"
assert run("2\n1 2 2\n").splitlines()[0] == "ambiguous", "branching case"
assert run("3\n1 2 1 1\n") == "perfect\n", "branch followed by chain"
assert run("3\n1 2 2 1\n").splitlines()[0] == "ambiguous", "two branching levels"
assert run("1\n1 5\n").splitlines()[0] == "perfect", "star tree"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 1 1` | `perfect` | A unique chain |
| `2 / 1 2 2` | `ambiguous` | Adjacent branching levels |
| `3 / 1 2 1 1` | `perfect` | A branching level that cannot be rearranged |
| `3 / 1 2 2 1` | `ambiguous` | Deeper branching ambiguity |
| `1 / 1 5` | `perfect` | Root with many children |

## Edge Cases

For the chain case

```
2
1 1 1
```

the algorithm constructs parents `0 1 2`. During the scan, the counts are never greater than one on neighboring levels, so no modification is possible. It prints `perfect`, which matches the only possible shape.

For the ambiguous case

```
2
1 2 2
```

the algorithm sees that levels 1 and 2 both have more than one vertex. The first tree attaches vertices 4 and 5 under vertex 2. The second tree moves vertex 4 under vertex 3. The level counts remain `1, 2, 2`, but one tree has a node with two children while the other spreads them out.

For a boundary case like

```
3
1 2 1 1
```

level 1 branches, but level 2 contains only one vertex. That vertex must have exactly one parent, so there is no alternative structure. The algorithm correctly ignores the single branching level and prints `perfect`.

For

```
3
1 2 2 1
```

levels 1 and 2 both branch. The first deeper vertex can be attached to either of the two nodes on level 1. The algorithm detects this adjacent pair and produces two different valid trees.
