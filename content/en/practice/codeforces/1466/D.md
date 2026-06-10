---
title: "CF 1466D - 13th Labour of Heracles"
description: "We are given a tree whose vertices carry weights. For every value of $k$ from $1$ to $n-1$, we may assign one of $k$ colors to each edge. Edges with the same color form a subgraph."
date: "2026-06-11T01:45:34+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1466
codeforces_index: "D"
codeforces_contest_name: "Good Bye 2020"
rating: 1500
weight: 1466
solve_time_s: 147
verified: true
draft: false
---

[CF 1466D - 13th Labour of Heracles](https://codeforces.com/problemset/problem/1466/D)

**Rating:** 1500  
**Tags:** data structures, greedy, sortings, trees  
**Solve time:** 2m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree whose vertices carry weights. For every value of $k$ from $1$ to $n-1$, we may assign one of $k$ colors to each edge. Edges with the same color form a subgraph. The value of a color is the maximum weight-sum among its connected components, and the value of the whole coloring is the sum of these per-color values.

The task is to compute the maximum possible coloring value for every $k$.

The first thing to notice is that the answer is not really about colors. Colors are only a mechanism that lets us split the tree into multiple pieces. The challenge is understanding how much contribution each vertex weight can make as we increase the number of colors.

The total number of vertices across all test cases is at most $2 \cdot 10^5$. Any solution that tries to explicitly construct colorings, simulate connected components for every $k$, or perform repeated graph traversals will be far too slow. An $O(n^2)$ solution would already require roughly $4 \cdot 10^{10}$ operations in the worst case. We need something close to $O(n \log n)$ per test file.

A subtle edge case appears when the tree is just a single edge.

```
2
21 32
1 2
```

The answer is:

```
53
```

There is only one possible value of $k$, namely $1$. Some implementations mistakenly try to generate additional contributions from degrees and produce extra values.

Another important case is a path.

```
4
10 10 10 10
1 2
2 3
3 4
```

The answer is:

```
40 50 60
```

Only the two internal vertices have degree greater than one. Leaves cannot contribute more than once. Any solution that treats every vertex weight as repeatedly usable will overcount.

A star-shaped tree exposes the main idea.

```
5
100 1 1 1 1
1 2
1 3
1 4
1 5
```

The answers are:

```
104 204 304 404
```

The center has degree $4$, so its weight can appear a total of $4$ times. A greedy solution that ignores vertex degrees misses this behavior entirely.

## Approaches

A brute-force approach would try to reason directly about colorings. For a fixed $k$, we could consider all ways to split edges among colors, compute connected components inside every color class, evaluate their values, and take the maximum. This is correct by definition, but even for modest trees the number of edge colorings is exponential. Since there are $n-1$ edges and up to $n-1$ colors, the search space becomes astronomically large.

To find something faster, we need to understand what actually changes when we increase the number of colors.

Start with $k=1$. Every edge has the same color, so the entire tree forms one connected component. The answer is simply the sum of all vertex weights.

Now imagine splitting the tree further. Every time we separate part of the tree, some vertex may become counted again in another color's best component. A vertex of degree $d$ is incident to $d$ edges. Across all possible splits, its weight can appear at most $d$ times in total.

The first appearance is already included in the initial sum. The remaining $d-1$ appearances are extra profit that we may collect later.

This transforms the problem completely. Instead of thinking about colorings, think about available extra contributions.

For every vertex $v$:

$$w_v$$

is already counted once in the initial answer.

Additionally, we may add its weight another

$$\deg(v)-1$$

times.

Since every extra appearance contributes exactly $w_v$, the best strategy is obvious: collect the largest available extra contributions first.

We create a list containing $w_v$ repeated $\deg(v)-1$ times for every vertex. After sorting this list in descending order, we start from the total weight sum and repeatedly add the next largest contribution. Each addition produces the answer for the next value of $k$.

This greedy process exactly matches the optimal sequence of answers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the vertex weights and compute their total sum.
2. Compute the degree of every vertex while reading the tree edges.
3. Initialize the answer sequence with the total weight sum. This is the value for $k=1$.
4. For every vertex, insert its weight into a list exactly $\deg(v)-1$ times.

The first copy of each vertex weight is already present in the total sum. Every additional copy represents one extra time that this vertex can contribute.
5. Sort this list in descending order.

Larger weights should be used earlier because every step adds exactly one extra contribution.
6. Starting from the total sum, repeatedly add the next value from the sorted list.
7. After each addition, append the current sum to the answer sequence.
8. Print the first $n-1$ values.

Why it works:

Initially every vertex contributes once, giving the total weight sum. A vertex with degree $d$ can belong to the maximal component of up to $d$ different color classes, so it can contribute its weight $d$ times overall. Since one copy is already included, there are exactly $d-1$ additional copies available.

Every increase in the number of colors consumes exactly one additional contribution. The profit from choosing a contribution is independent of all others and equals the corresponding vertex weight. Because all profits are non-negative and independent, taking the largest remaining profit at every step maximizes every prefix sum. Sorting all extra contributions in descending order and adding them one by one produces the optimal answer sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        w = list(map(int, input().split()))

        deg = [0] * n

        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            deg[u] += 1
            deg[v] += 1

        total = sum(w)

        extra = []
        for i in range(n):
            extra.extend([w[i]] * (deg[i] - 1))

        extra.sort(reverse=True)

        ans = [total]
        cur = total

        for x in extra:
            cur += x
            ans.append(cur)

        out.append(" ".join(map(str, ans[:n - 1])))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The degree array is the key data structure. After reading the tree, each vertex contributes its weight to the `extra` list exactly `degree - 1` times.

The total number of inserted elements is

$$\sum (\deg(v)-1)=2(n-1)-n=n-2$$

so the list size remains linear.

Sorting the list gives the optimal order in which extra contributions should be consumed. We start from the total vertex-weight sum and keep adding contributions one at a time. Since there are exactly $n-2$ extra contributions, we obtain exactly $1 + (n-2) = n-1$ answers.

Python integers automatically handle the large values involved. The maximum answer can exceed 32-bit range because weights are up to $10^9$.

## Worked Examples

### Example 1

Input:

```
4
3 5 4 6
2 1
3 1
4 3
```

Degrees are:

| Vertex | Weight | Degree | Extra Copies |
| --- | --- | --- | --- |
| 1 | 3 | 2 | 1 |
| 2 | 5 | 1 | 0 |
| 3 | 4 | 2 | 1 |
| 4 | 6 | 1 | 0 |

Initial sum:

$$18$$

Extra list:

$$[3,4]$$

Sorted descending:

$$[4,3]$$

| Step | Added Value | Current Sum | Answer Produced |
| --- | --- | --- | --- |
| Initial | 0 | 18 | 18 |
| 1 | 4 | 22 | 22 |
| 2 | 3 | 25 | 25 |

Output:

```
18 22 25
```

This example shows how each non-leaf vertex contributes one additional copy of its weight.

### Example 2

Input:

```
6
20 13 17 13 13 11
2 1
3 1
4 1
5 1
6 1
```

This is a star centered at vertex 1.

| Vertex | Weight | Degree | Extra Copies |
| --- | --- | --- | --- |
| 1 | 20 | 5 | 4 |
| 2 | 13 | 1 | 0 |
| 3 | 17 | 1 | 0 |
| 4 | 13 | 1 | 0 |
| 5 | 13 | 1 | 0 |
| 6 | 11 | 1 | 0 |

Initial sum:

$$87$$

Extra list:

$$[20,20,20,20]$$

| Step | Added Value | Current Sum |
| --- | --- | --- |
| Initial | 0 | 87 |
| 1 | 20 | 107 |
| 2 | 20 | 127 |
| 3 | 20 | 147 |
| 4 | 20 | 167 |

Output:

```
87 107 127 147 167
```

This trace highlights the central observation. A vertex of degree five can contribute its weight five times in total, once initially and four more times later.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the extra contribution list dominates |
| Space | O(n) | Degree array and extra contribution list |

The total number of vertices across all test cases is at most $2 \cdot 10^5$. Sorting at most $n-2$ extra contributions per test case gives an overall complexity of $O(n \log n)$, which easily fits within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = []

    t = int(input())
    for _ in range(t):
        n = int(input())
        w = list(map(int, input().split()))

        deg = [0] * n

        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            deg[u] += 1
            deg[v] += 1

        total = sum(w)

        extra = []
        for i in range(n):
            extra.extend([w[i]] * (deg[i] - 1))

        extra.sort(reverse=True)

        ans = [total]
        cur = total

        for x in extra:
            cur += x
            ans.append(cur)

        out.append(" ".join(map(str, ans[:n - 1])))

    return "\n".join(out)

# provided samples
assert run(
"""4
4
3 5 4 6
2 1
3 1
4 3
2
21 32
2 1
6
20 13 17 13 13 11
2 1
3 1
4 1
5 1
6 1
4
10 6 6 6
1 2
2 3
4 1
"""
) == (
"""18 22 25
53
87 107 127 147 167
28 38 44"""
), "sample"

# minimum tree
assert run(
"""1
2
7 9
1 2
"""
) == "16"

# path graph
assert run(
"""1
4
10 10 10 10
1 2
2 3
3 4
"""
) == "40 50 60"

# star graph
assert run(
"""1
5
100 1 1 1 1
1 2
1 3
1 4
1 5
"""
) == "104 204 304 404"

# all weights zero
assert run(
"""1
4
0 0 0 0
1 2
2 3
3 4
"""
) == "0 0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two vertices | 16 | Minimum valid tree |
| Path of length 3 | 40 50 60 | Internal vertices contribute once more |
| Star centered at heavy vertex | 104 204 304 404 | High degree creates many extra contributions |
| All weights zero | 0 0 0 | Handles zero-valued contributions correctly |

## Edge Cases

Consider the smallest tree:

```
1
2
21 32
1 2
```

The total sum is $53$. Both vertices have degree $1$, so there are no extra contributions. The extra list is empty, and the algorithm outputs only:

```
53
```

which is correct because only $k=1$ exists.

Consider a path:

```
1
4
10 10 10 10
1 2
2 3
3 4
```

Degrees are $[1,2,2,1]$. The extra list becomes $[10,10]$. Starting from $40$, we add these contributions one by one and obtain:

```
40 50 60
```

Leaves never appear in the extra list because their degree is one. This prevents overcounting.

Consider a star:

```
1
5
100 1 1 1 1
1 2
1 3
1 4
1 5
```

The center has degree $4$, so its weight appears $4-1=3$ times in the extra list. The list is:

```
100 100 100
```

Starting from $104$, successive additions produce:

```
104 204 304 404
```

The algorithm correctly captures the fact that a high-degree vertex can contribute multiple times, while leaves contribute only once.
