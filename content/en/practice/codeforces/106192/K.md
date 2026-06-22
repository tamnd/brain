---
title: "CF 106192K - \u0417\u0430\u043b\u0438\u0432\u043a\u0430"
description: "We are given a complete graph with $n$ vertices. Each vertex initially has a color, and colors are given as integers. The graph structure itself is not really something we need to manipulate explicitly because every pair of vertices is connected."
date: "2026-06-22T19:10:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106192
codeforces_index: "K"
codeforces_contest_name: "\u041f\u0435\u0440\u043c\u0441\u043a\u0430\u044f \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2025"
rating: 0
weight: 106192
solve_time_s: 50
verified: true
draft: false
---

[CF 106192K - \u0417\u0430\u043b\u0438\u0432\u043a\u0430](https://codeforces.com/problemset/problem/106192/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a complete graph with $n$ vertices. Each vertex initially has a color, and colors are given as integers. The graph structure itself is not really something we need to manipulate explicitly because every pair of vertices is connected.

The only operation available is to pick a connected subgraph whose vertices all currently share the same color, and recolor all of them into any other color. The goal is to make every vertex end up with a single uniform color using the minimum number of such operations.

Because the graph is complete, any subset of vertices is connected. This changes the problem significantly: connectivity does not restrict which vertices we can choose, only the condition that all chosen vertices must currently have the same color.

The input size goes up to $10^6$, which immediately rules out anything quadratic such as trying all pairs of colors or simulating operations on subsets repeatedly. We need a solution that essentially processes the color array in linear time.

A few subtle situations matter:

If all vertices already have the same color, for example:

Input:

```
5
3 3 3 3 3
```

the answer must be 0, since no operation is needed. Any approach that blindly assumes at least one operation per color would be wrong here.

If all colors are distinct, for example:

```
4
1 2 3 4
```

we might suspect we need many operations, but because we can recolor multiple vertices of the same color at once, the true answer depends only on how many distinct colors exist, not on $n$ itself.

The key pitfall is overthinking connectivity. Since the graph is complete, connectivity never restricts us, and the only real structure is how colors are distributed.

## Approaches

A brute-force interpretation would simulate the process. At each step, we choose some color class, pick some subset of it, recolor it, update the graph, and repeat until all vertices share one color. This is correct in principle, but it requires maintaining dynamic color groups and repeatedly scanning or updating sets of vertices. In the worst case, each operation might touch $O(n)$ vertices, and we may perform up to $O(n)$ operations, leading to $O(n^2)$ behavior, which is far too slow for $n = 10^6$.

The key observation is that the structure of the graph makes every set of vertices with the same color interchangeable as a single unit. Since any subset of equal-colored vertices is connected, we can treat each distinct color as a block. More importantly, we can eliminate an entire color in one move by recoloring all vertices of that color into some target color.

Once this is clear, the process becomes purely combinatorial. Suppose there are $k$ distinct colors initially. We choose one of them as the final target color. Every other color class must be merged into it at least once, and each can be merged in a single operation. This immediately gives $k - 1$ as the optimal answer.

There is no benefit in trying to recolor partial subsets or doing intermediate transformations, because each operation can already consume an entire color class at no extra cost.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(n)$ | Too slow |
| Count Distinct Colors | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We reduce the problem to understanding how many distinct colors exist in the initial array.

1. Read all vertex colors and store them in a list. The structure of the graph is irrelevant because it is complete, so connectivity imposes no restrictions on grouping vertices.
2. Compute the number of distinct colors in the array. This can be done using a hash set while scanning the array once. The reason this works is that each color behaves as an independent group that can be merged in a single operation.
3. Let the number of distinct colors be $k$. If $k = 1$, return 0 immediately since the graph is already monochromatic.
4. Otherwise, return $k - 1$. This corresponds to choosing one color as the final target and merging all other color classes into it one by one.

### Why it works

The crucial invariant is that at any point in the process, each remaining color class is fully collapsible into any other color in a single operation. Because any subset of a color is connected in a complete graph, we never need more than one operation per distinct color we decide to eliminate. No operation can reduce the number of distinct colors by more than one unless it merges an entire color class into another, and such a merge is always possible. This makes $k - 1$ both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    colors = list(map(int, input().split()))
    distinct = len(set(colors))
    print(max(0, distinct - 1))

if __name__ == "__main__":
    main()
```

The solution reads the color array, inserts all values into a set to compute how many unique colors exist, and prints $k - 1$. The `max(0, ...)` guard handles the trivial case where all vertices already share the same color.

The main subtlety is that we never attempt to simulate operations. Any simulation would be unnecessary because the operation structure allows entire color classes to collapse in one step.

## Worked Examples

### Example 1

Input:

```
4
1 2 3 4
```

We track distinct colors:

| Step | Processed colors | Distinct count |
| --- | --- | --- |
| Start | {} | 0 |
| After scan | {1,2,3,4} | 4 |

We have $k = 4$, so the answer is $3$.

This confirms that even though all vertices differ, we can merge them efficiently by repeatedly absorbing one full color class into another.

### Example 2

Input:

```
5
2 2 2 1 1
```

| Step | Processed colors | Distinct count |
| --- | --- | --- |
| Start | {} | 0 |
| After scan | {1,2} | 2 |

Here $k = 2$, so the answer is $1$.

This shows the minimal non-trivial case where exactly one merge is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Single pass to build a set of colors |
| Space | $O(n)$ | Set stores up to $n$ distinct values in worst case |

The constraints allow up to $10^6$ vertices, so a linear scan with hashing is comfortably within limits both in time and memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n = int(input())
    colors = list(map(int, input().split()))
    return str(max(0, len(set(colors)) - 1))

# provided sample (if interpreted as single case)
assert run("1\n1\n") == "0"

# all equal
assert run("5\n3 3 3 3 3\n") == "0"

# all distinct
assert run("4\n1 2 3 4\n") == "3"

# mixed
assert run("5\n1 1 2 2 3\n") == "2"

# two colors only
assert run("6\n7 7 7 8 8 8\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 0 | no operations needed |
| all distinct | n-1 | worst-case merging |
| mixed duplicates | k-1 | correctness under repetition |
| two colors | 1 | minimal non-trivial case |

## Edge Cases

When all vertices share the same color, the set size is 1, so the formula yields $1 - 1 = 0$. The algorithm correctly returns 0 without requiring any special branching beyond the final `max(0, ...)`.

When every vertex has a different color, the set size becomes $n$, and the answer becomes $n - 1$. This matches the fact that each color class must be absorbed once, and each absorption is a single valid operation.

When colors repeat in arbitrary patterns, such as alternating or clustered values, the set abstraction removes all structure beyond uniqueness. Since operations depend only on color identity and not positions, this simplification remains valid for all configurations.
