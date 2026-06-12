---
title: "CF 913B - Christmas Spruce"
description: "We are given a rooted tree with vertices numbered from 1 to n. Vertex 1 is always the root. For every other vertex, the input tells us its parent, which completely defines the tree structure. A vertex is considered a leaf if it has no children and is not the root."
date: "2026-06-12T10:10:03+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 913
codeforces_index: "B"
codeforces_contest_name: "Hello 2018"
rating: 1200
weight: 913
solve_time_s: 178
verified: true
draft: false
---

[CF 913B - Christmas Spruce](https://codeforces.com/problemset/problem/913/B)

**Rating:** 1200  
**Tags:** implementation, trees  
**Solve time:** 2m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree with vertices numbered from 1 to _n_. Vertex 1 is always the root. For every other vertex, the input tells us its parent, which completely defines the tree structure.

A vertex is considered a leaf if it has no children and is not the root. A tree is called a spruce when every non-leaf vertex has at least three children that are themselves leaves.

The task is simply to determine whether the given tree satisfies this condition. If every non-leaf vertex has at least three leaf children, print `"Yes"`. Otherwise print `"No"`.

The constraints are very small. The tree contains at most 1000 vertices. Even an algorithm that examines every vertex and all of its children will run comfortably within the limits. There is no need for advanced tree algorithms, recursion tricks, or heavy preprocessing.

The main challenge is interpreting the condition correctly. We are not counting all descendants that are leaves. We are only counting immediate children that are leaves.

Consider this example:

```
5
1
1
2
2
```

The tree is:

```
1
├─2
│ ├─4
│ └─5
└─3
```

Vertex 1 has only one leaf child, vertex 3. Vertices 4 and 5 are leaves, but they are grandchildren of 1, not children. The correct answer is:

```
No
```

A careless implementation that counts leaf descendants instead of leaf children would incorrectly accept this tree.

Another subtle case is when an internal vertex has many children, but not enough of them are leaves:

```
7
1
1
1
2
2
2
```

The tree is:

```
1
├─2
│ ├─5
│ ├─6
│ └─7
├─3
└─4
```

Vertex 2 is valid because it has three leaf children. Vertex 1 has only two leaf children, vertices 3 and 4. The correct answer is:

```
No
```

A careless solution might only check the root or might count total children instead of leaf children.

One more edge case is a vertex that has exactly three leaf children:

```
4
1
1
1
```

The root has three leaf children, so the answer is:

```
Yes
```

The condition is "at least 3", so exactly 3 must be accepted.

## Approaches

The most direct approach is to examine every non-leaf vertex and count how many of its children are leaves.

A brute-force version could determine whether a child is a leaf by scanning all vertices each time. For every vertex, for every child, we search the entire tree to see whether that child has children of its own. With _n_ vertices, this leads to roughly _O(n²)_ work.

For _n = 1000_, even _O(n²)_ is acceptable. Roughly one million operations is well within the limit.

There is an even cleaner approach. While reading the input, we build an adjacency list containing the children of every vertex. Once we have that structure, determining whether a vertex is a leaf becomes trivial: a vertex is a leaf exactly when its children list is empty.

The key observation is that the spruce condition depends only on immediate children. We never need to traverse subtrees or compute depths. For each internal vertex, we simply count how many children have zero children of their own.

This reduces the solution to a single pass over all adjacency lists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of vertices.
2. Build a children list for every vertex. For each vertex `i` from 2 to `n`, read its parent `p` and append `i` to `children[p]`.
3. Iterate through every vertex.
4. If a vertex has no children, it is a leaf. The spruce condition does not apply to leaves, so skip it.
5. For every non-leaf vertex, count how many of its immediate children are leaves. A child is a leaf exactly when its own children list is empty.
6. If this count is less than 3 for any non-leaf vertex, print `"No"` and stop immediately.
7. If every non-leaf vertex passes the check, print `"Yes"`.

### Why it works

A vertex violates the spruce definition if and only if it is an internal vertex and fewer than three of its immediate children are leaves.

The algorithm checks exactly this condition for every internal vertex. Every leaf is ignored because the definition places no restriction on leaves. Every internal vertex is examined once, and the number of leaf children is computed exactly according to the definition.

If the algorithm prints `"No"`, some internal vertex fails the requirement, so the tree cannot be a spruce. If the algorithm prints `"Yes"`, every internal vertex satisfies the requirement, which matches the definition of a spruce. Thus the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

children = [[] for _ in range(n + 1)]

for v in range(2, n + 1):
    p = int(input())
    children[p].append(v)

for v in range(1, n + 1):
    if not children[v]:
        continue

    leaf_children = 0

    for child in children[v]:
        if not children[child]:
            leaf_children += 1

    if leaf_children < 3:
        print("No")
        sys.exit()

print("Yes")
```

The first part constructs the rooted tree as an adjacency list. Since the input directly gives each vertex's parent, building the children lists is straightforward.

The second part iterates through all vertices. A vertex with an empty children list is a leaf, so it is skipped.

For every internal vertex, the code counts how many children themselves have empty children lists. Those are exactly the leaf children required by the definition.

The moment a vertex has fewer than three leaf children, the answer is known to be `"No"`, so the program terminates early. If the loop finishes, every internal vertex satisfies the condition and the answer is `"Yes"`.

A common mistake is to count all leaf descendants instead of immediate leaf children. The implementation avoids that by examining only the vertices in `children[v]`.

## Worked Examples

### Sample 1

Input:

```
4
1
1
1
```

Tree:

```
1
├─2
├─3
└─4
```

| Vertex | Children | Leaf children count | Valid? |
| --- | --- | --- | --- |
| 1 | {2,3,4} | 3 | Yes |
| 2 | {} | Skip | - |
| 3 | {} | Skip | - |
| 4 | {} | Skip | - |

The root has exactly three leaf children, which satisfies the requirement. Every other vertex is a leaf, so the answer is `"Yes"`.

### Sample 2

Input:

```
5
1
1
2
2
```

Tree:

```
1
├─2
│ ├─4
│ └─5
└─3
```

| Vertex | Children | Leaf children count | Valid? |
| --- | --- | --- | --- |
| 1 | {2,3} | 1 | No |
| 2 | {4,5} | Not reached | - |
| 3 | {} | - | - |
| 4 | {} | - | - |
| 5 | {} | - | - |

Vertex 1 has only one leaf child, vertex 3. Vertices 4 and 5 are grandchildren, so they do not count. The answer is `"No"`.

This example demonstrates the most common pitfall: only immediate children matter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each vertex and each parent-child edge is examined a constant number of times |
| Space | O(n) | The adjacency lists store all vertices and edges |

Since the tree contains at most 1000 vertices, an O(n) solution is extremely fast. The memory usage is also tiny because the adjacency list stores only the tree edges.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    children = [[] for _ in range(n + 1)]

    for v in range(2, n + 1):
        p = int(input())
        children[p].append(v)

    for v in range(1, n + 1):
        if not children[v]:
            continue

        cnt = 0
        for child in children[v]:
            if not children[child]:
                cnt += 1

        if cnt < 3:
            print("No")
            return

    print("Yes")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# provided sample
assert run("4\n1\n1\n1\n") == "Yes", "sample 1"

# minimum valid tree
assert run("4\n1\n1\n1\n") == "Yes", "minimum spruce"

# root has only two leaf children
assert run("3\n1\n1\n") == "No", "root needs at least three leaf children"

# internal node valid, root invalid
assert run("7\n1\n1\n1\n2\n2\n2\n") == "No", "count only immediate leaf children"

# larger valid tree
assert run("8\n1\n1\n1\n2\n2\n2\n1\n") == "Yes", "all internal vertices satisfy condition"

# chain structure
assert run("4\n1\n2\n3\n") == "No", "every internal vertex fails"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 / 1 1 1` | Yes | Exactly three leaf children is sufficient |
| `3 / 1 1` | No | Root with only two leaf children |
| `7 / 1 1 1 2 2 2` | No | Leaf descendants do not count |
| `8 / 1 1 1 2 2 2 1` | Yes | Multiple internal vertices can all satisfy the rule |
| `4 / 1 2 3` | No | Deep chain where every internal vertex fails |

## Edge Cases

Consider the tree:

```
5
1
1
2
2
```

The algorithm builds:

```
children[1] = [2, 3]
children[2] = [4, 5]
```

When processing vertex 1, child 2 is not a leaf because it has children. Child 3 is a leaf. The count is 1, which is less than 3, so the algorithm prints `"No"`.

This correctly handles the case where leaf descendants exist but are not immediate children.

Consider:

```
7
1
1
1
2
2
2
```

Vertex 2 has three leaf children and passes. Vertex 1 has children `{2,3,4}`. Only vertices 3 and 4 are leaves, so its count is 2. The algorithm prints `"No"`.

This verifies that every internal vertex must satisfy the condition, not just some of them.

Consider:

```
4
1
1
1
```

The root's children are all leaves, so the count is exactly 3. Since the condition is "at least 3", the algorithm accepts the tree and prints `"Yes"`.

This confirms the boundary case where the count is exactly the required minimum.
