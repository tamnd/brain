---
title: "CF 105123B - Neural Network"
description: "We are given a layered structure where each layer contains a certain number of nodes. Between every pair of consecutive layers, every node in the left layer is connected to every node in the right layer."
date: "2026-06-27T19:32:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105123
codeforces_index: "B"
codeforces_contest_name: "BioCode 2024"
rating: 0
weight: 105123
solve_time_s: 75
verified: false
draft: false
---

[CF 105123B - Neural Network](https://codeforces.com/problemset/problem/105123/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a layered structure where each layer contains a certain number of nodes. Between every pair of consecutive layers, every node in the left layer is connected to every node in the right layer. That means if one layer has `x` nodes and the next has `y` nodes, the number of edges between them is exactly `x × y`.

The task is to compute the total number of edges across all adjacent layer pairs and output the sum.

The input size is small, with at most 1000 layers and each layer having at most 1000 nodes. This immediately tells us that even an O(n²) solution would be safe, but the structure of the problem suggests we do not need anything close to that. We only ever interact with adjacent pairs, so a single linear pass is sufficient.

A naive mistake here is to think in terms of building or enumerating the graph. If someone tries to explicitly simulate edges, for example by iterating over all nodes in both layers, they are still effectively doing the correct computation but with unnecessary conceptual overhead. Another incorrect approach would be to misunderstand the structure and attempt to count edges globally rather than per adjacent pair, which would miss that only consecutive layers matter.

Edge cases are straightforward but still worth sanity checking. If there is only one layer, there are no adjacent pairs, so the answer must be zero. For example, input `1 / 5` should produce `0`. If layers contain ones, such as `1 1 1 1`, each pair contributes exactly one edge, so the answer becomes the number of transitions, which is `n - 1`.

## Approaches

A brute-force interpretation would explicitly consider each pair of adjacent layers and compute the product by iterating over nodes. For two layers of sizes `x` and `y`, that would mean looping `x` times and `y` times to count all connections. Over all adjacent pairs, this becomes proportional to the sum of products computed via nested iteration, which is unnecessary because multiplication already gives the result directly.

The inefficiency comes from treating each edge as something to enumerate individually. Since every possible pair of nodes between two adjacent layers contributes exactly one edge, we do not gain anything from simulating the connections.

The key observation is that the structure already gives us the exact formula per transition: for every `i`, the contribution is simply `a[i] × a[i+1]`. There is no dependency between different pairs of layers, so we can accumulate the result in a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate node pairs) | O(∑ a[i]·a[i+1]) | O(1) | Too slow |
| Optimal (adjacent multiplication) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of layers `n` and the list `a` representing the number of nodes in each layer. This establishes the structure we will traverse.
2. Initialize an accumulator `ans = 0` to store the total number of edges. This keeps the computation incremental so we do not need any extra storage.
3. Iterate through the layers from index `0` to `n - 2`. Each index represents a boundary between two consecutive layers.
4. For each index `i`, compute `a[i] * a[i + 1]` and add it to `ans`. This directly counts all edges between the two layers, since every node in the first connects to every node in the second.
5. After processing all adjacent pairs, output `ans`.

### Why it works

Each edge in the network exists only between two consecutive layers, and every such edge is uniquely identified by a pair of nodes chosen from those two layers. For a fixed pair of layers `i` and `i+1`, the number of possible node pairs is exactly the Cartesian product `a[i] × a[i+1]`. Summing these independent contributions over all adjacent layer pairs counts every edge exactly once, with no overlap between pairs of layers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    ans = 0
    for i in range(n - 1):
        ans += a[i] * a[i + 1]
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by reading the structure of the network. The loop then walks through each boundary between layers, ensuring we only ever multiply adjacent values. The accumulator `ans` is kept as a single integer since the maximum possible value is well within Python’s integer capacity.

A subtle point is that we never attempt to store intermediate edge structures. This avoids both memory overhead and unnecessary complexity. The loop bounds `n - 1` are critical since each multiplication requires a valid pair `(i, i+1)`.

## Worked Examples

### Example 1

Input:

```
4
3 5 2 7
```

| i | a[i] | a[i+1] | Product | Running Sum |
| --- | --- | --- | --- | --- |
| 0 | 3 | 5 | 15 | 15 |
| 1 | 5 | 2 | 10 | 25 |
| 2 | 2 | 7 | 14 | 39 |

This trace shows how each boundary contributes independently. The running sum accumulates each layer transition without interference, confirming that adjacency alone defines all edges.

### Example 2

Input:

```
5
1 1 1 1 1
```

| i | a[i] | a[i+1] | Product | Running Sum |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 2 |
| 2 | 1 | 1 | 1 | 3 |
| 3 | 1 | 1 | 1 | 4 |

Each transition contributes exactly one edge, which confirms the interpretation that every node pair is valid and counted once per adjacent layer pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the list of layer sizes |
| Space | O(1) | Only a constant number of variables are used |

The constraints allow up to 1000 layers, so a linear traversal is trivial in terms of runtime. The operations are simple integer multiplications and additions, well within the limits of a 1-second time budget.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    ans = 0
    for i in range(n - 1):
        ans += a[i] * a[i + 1]
    return str(ans)

# provided sample
assert run("4\n3 5 2 7\n") == "39"

# single layer
assert run("1\n5\n") == "0"

# all ones
assert run("4\n1 1 1 1\n") == "3"

# increasing values
assert run("3\n2 3 4\n") == "18"

# max-ish small check
assert run("2\n1000 1000\n") == "1000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5` | `0` | single layer edge case |
| `1 1 1 1` | `3` | uniform transitions |
| `2 3 4` | `18` | non-trivial multiplication |
| `1000 1000` | `1000000` | maximum product boundary |

## Edge Cases

For a single layer input like `1 / 5`, the loop `for i in range(n - 1)` never executes because `n - 1 = 0`. The accumulator remains `0`, which matches the fact that there are no adjacent layer pairs and therefore no edges.

For minimal adjacency such as `2 / 3 4`, the loop runs once with `i = 0`. The computation is `3 × 4 = 12`, and that is immediately returned. There is no hidden state or carry-over between iterations, so each boundary is fully independent and safely handled in isolation.
