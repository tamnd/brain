---
title: "CF 1905B - Begginer's Zelda"
description: "We are given a tree and a special operation. In one operation, we choose any two vertices and look at the unique path between them. Every vertex on that path is merged into a single new vertex."
date: "2026-06-09T01:18:47+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1905
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 915 (Div. 2)"
rating: 1100
weight: 1905
solve_time_s: 110
verified: true
draft: false
---

[CF 1905B - Begginer's Zelda](https://codeforces.com/problemset/problem/1905/B)

**Rating:** 1100  
**Tags:** greedy, trees  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree and a special operation.

In one operation, we choose any two vertices and look at the unique path between them. Every vertex on that path is merged into a single new vertex. Any edge that originally connected some outside vertex to the path is redirected to this new vertex.

The goal is to repeatedly perform such path-compressions until the entire tree becomes a single vertex. We must find the minimum number of operations.

Since the graph is a tree, there are exactly $n-1$ edges and a unique path between every pair of vertices. The total number of vertices across all test cases is at most $10^5$, so we need something close to linear time. Any solution that repeatedly modifies the tree and searches for optimal paths would quickly become too expensive. An $O(n^2)$ approach is already too slow in the worst case.

The tricky part is understanding what a path-compression actually does to the structure of the tree.

Consider a simple chain:

```
1 - 2 - 3 - 4 - 5
```

Choosing vertices 1 and 5 compresses the entire tree into one vertex, so the answer is 1.

Input:

```
1
5
1 2
2 3
3 4
4 5
```

Output:

```
1
```

A careless approach based only on the number of vertices would miss that one operation can remove many vertices at once.

Now consider a star:

```
    2
    |
3 - 1 - 4
    |
    5
```

There are four leaves. Compressing a path between two leaves removes those two leaves and the center, but the other leaves remain attached. The answer is not 1.

Input:

```
1
5
1 2
1 3
1 4
1 5
```

Output:

```
2
```

This example shows that the number of leaves matters much more than the total number of vertices.

Another easy mistake is assuming every operation decreases the number of leaves by exactly two. A path can pass through many internal vertices, but only its endpoints can be leaves. Understanding precisely how leaves disappear is the key observation.

## Approaches

A brute-force viewpoint is to think of the tree as changing after every operation. We could try every possible pair of vertices, simulate the compression, recursively solve the remaining tree, and take the minimum.

This is correct in principle because it explores all possible sequences of operations. Unfortunately, even one operation already has $O(n^2)$ choices, and the number of resulting trees grows explosively. Such an approach is completely infeasible even for a few dozen vertices.

To find a useful pattern, forget about individual vertices and focus on leaves.

Every tree with more than one vertex has at least two leaves. Suppose we compress a path whose endpoints are leaves. All leaves lying on that path disappear. Since a simple path can only have leaves at its endpoints, this operation removes exactly two leaves from the tree.

What happens to the remaining structure? The compressed path becomes a single vertex. If the path connected to the rest of the tree, that new vertex may itself become a leaf. Effectively, one operation can combine two existing leaves into one "representative".

This starts looking similar to repeatedly pairing leaves.

Let $L$ be the number of leaves.

One operation can reduce the leaf count by at most two. To eliminate all leaves and end with a single vertex, we need at least

$$\left\lceil \frac{L}{2} \right\rceil$$

operations.

The surprising part is that this lower bound is always achievable.

At any stage, choose two leaves and compress the path between them. This removes those two leaves from consideration. Repeating this process keeps pairing leaves until none remain. If $L$ is even, we need $L/2$ operations. If $L$ is odd, after pairing $L-1$ leaves, one leaf-equivalent structure remains and requires one final operation. The count becomes $(L+1)/2$.

Thus the answer depends only on the number of leaves:

$$\boxed{\left\lceil \frac{L}{2} \right\rceil}$$

All we need is to count vertices of degree 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the tree.
2. Compute the degree of every vertex by processing all edges.
3. Count how many vertices have degree equal to 1. Let this value be $L$.
4. Output $(L + 1) // 2$.

The expression $(L + 1) // 2$ is the integer form of $\lceil L/2 \rceil$.

### Why it works

The crucial property is that every operation can eliminate at most two leaves, namely the endpoints of the chosen path. Since there are $L$ leaves initially, any solution needs at least $\lceil L/2 \rceil$ operations.

Conversely, repeatedly selecting paths between pairs of leaves always removes two leaves at a time. This process achieves exactly $\lceil L/2 \rceil$ operations. Since we have both a lower bound and a matching construction, the minimum number of operations is precisely $\lceil L/2 \rceil$.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        n = int(input())

        deg = [0] * (n + 1)

        for _ in range(n - 1):
            u, v = map(int, input().split())
            deg[u] += 1
            deg[v] += 1

        leaves = 0
        for v in range(1, n + 1):
            if deg[v] == 1:
                leaves += 1

        answers.append(str((leaves + 1) // 2))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The implementation follows the mathematical result directly.

The degree array stores how many edges touch each vertex. In a tree, a leaf is exactly a vertex whose degree equals 1. After reading all edges, we count such vertices.

The final answer is computed using `(leaves + 1) // 2`, which performs ceiling division by 2 for nonnegative integers.

A common mistake is trying to simulate the operations themselves. None of that is necessary. Once the leaf count is known, the answer is determined immediately.

Another subtle point is the minimum tree size. When `n = 2`, both vertices are leaves, so `leaves = 2` and the formula correctly returns 1.

## Worked Examples

### Example 1

Input:

```
4
1 2
1 3
3 4
```

Degrees:

| Vertex | Degree |
| --- | --- |
| 1 | 2 |
| 2 | 1 |
| 3 | 2 |
| 4 | 1 |

Leaf count:

| Leaves |
| --- |
| 2 |

Answer:

| L | (L + 1) // 2 |
| --- | --- |
| 2 | 1 |

Output:

```
1
```

The tree is already a single path from 2 to 4. Compressing that path merges the entire tree in one operation.

### Example 2

Input:

```
9
3 1
3 5
3 2
5 6
6 7
7 8
7 9
6 4
```

Degrees:

| Vertex | Degree |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 3 |
| 4 | 1 |
| 5 | 2 |
| 6 | 3 |
| 7 | 3 |
| 8 | 1 |
| 9 | 1 |

Leaf count:

| Leaves |
| --- |
| 5 |

Answer:

| L | (L + 1) // 2 |
| --- | --- |
| 5 | 3 |

Output:

```
3
```

This example demonstrates the odd-leaf case. Five leaves require three operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each edge is processed once, then all vertices are scanned once |
| Space | O(n) | Degree array stores one value per vertex |

The sum of all $n$ values across test cases is at most $10^5$. A linear solution performs only a few hundred thousand operations in total, comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        deg = [0] * (n + 1)

        for _ in range(n - 1):
            u, v = map(int, input().split())
            deg[u] += 1
            deg[v] += 1

        leaves = sum(1 for x in deg[1:] if x == 1)
        ans.append(str((leaves + 1) // 2))

    return "\n".join(ans)

# provided sample
assert run(
"""4
4
1 2
1 3
3 4
9
3 1
3 5
3 2
5 6
6 7
7 8
7 9
6 4
7
1 2
1 3
2 4
4 5
3 6
2 7
6
1 2
1 3
1 4
4 5
2 6
"""
) == "1\n3\n2\n2"

# minimum tree
assert run(
"""1
2
1 2
"""
) == "1"

# path graph
assert run(
"""1
5
1 2
2 3
3 4
4 5
"""
) == "1"

# star with four leaves
assert run(
"""1
5
1 2
1 3
1 4
1 5
"""
) == "2"

# star with five leaves
assert run(
"""1
6
1 2
1 3
1 4
1 5
1 6
"""
) == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two-node tree | 1 | Smallest valid input |
| Simple path | 1 | Entire tree can be compressed at once |
| Four-leaf star | 2 | Even number of leaves |
| Five-leaf star | 3 | Odd number of leaves |
| Official sample | Matching sample output | General correctness |

## Edge Cases

Consider the smallest tree:

```
1
2
1 2
```

Both vertices have degree 1, so $L = 2$. The algorithm returns $(2+1)//2 = 1$. Compressing the path between the two vertices indeed produces a single vertex in one operation.

Consider a path:

```
1
5
1 2
2 3
3 4
4 5
```

Only vertices 1 and 5 are leaves. The algorithm finds $L = 2$ and returns 1. Choosing the path from one end to the other covers every vertex, so one operation is optimal.

Consider a star with five leaves:

```
1
6
1 2
1 3
1 4
1 5
1 6
```

The leaves are 2, 3, 4, 5, and 6, so $L = 5$. The algorithm returns $(5+1)//2 = 3$. A mistaken formula such as `L // 2` would return 2, which is impossible because each operation removes at most two leaves. The ceiling division handles odd leaf counts correctly.
