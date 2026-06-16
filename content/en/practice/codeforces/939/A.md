---
title: "CF 939A - Love Triangle"
description: "We are given a directed structure over $n$ nodes, where each node has exactly one outgoing edge. Concretely, plane $i$ points to plane $fi$, meaning it “likes” exactly one other plane. Self-loops are explicitly disallowed, so no node points to itself."
date: "2026-06-17T02:35:48+07:00"
tags: ["codeforces", "competitive-programming", "graphs"]
categories: ["algorithms"]
codeforces_contest: 939
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 464 (Div. 2)"
rating: 800
weight: 939
solve_time_s: 68
verified: true
draft: false
---

[CF 939A - Love Triangle](https://codeforces.com/problemset/problem/939/A)

**Rating:** 800  
**Tags:** graphs  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed structure over $n$ nodes, where each node has exactly one outgoing edge. Concretely, plane $i$ points to plane $f_i$, meaning it “likes” exactly one other plane. Self-loops are explicitly disallowed, so no node points to itself.

The task is to determine whether there exists a directed cycle of length exactly three. In other words, we are looking for three distinct planes $A, B, C$ such that $A \to B$, $B \to C$, and $C \to A$.

The structure is a functional graph, since every node has outdegree 1. That immediately implies every connected component consists of a cycle with directed trees feeding into it. However, only cycles of length 3 matter here.

The constraint $n \le 5000$ is small enough that an $O(n^2)$ or even a simple $O(n)$ scan with constant checks per node is sufficient. Anything cubic or involving repeated traversal per node would still pass, but is unnecessary.

A subtle edge case comes from misunderstanding the direction of traversal. Since each node points to exactly one node, but multiple nodes can point to the same target, thinking in undirected terms or assuming symmetry will break correctness.

Another edge case is assuming that any cycle qualifies. For example, a cycle of length 2 like $1 \to 2 \to 1$ is not valid. Only length 3 cycles count.

A concrete example of a trap:

Input:

```
3
2 1 2
```

This forms $1 \to 2 \to 1$, and $3 \to 2$. There is a cycle, but it is length 2, so the correct output is:

```
NO
```

A naive cycle-detection approach that stops at “cycle exists” would incorrectly answer YES.

## Approaches

A brute-force idea is to try every ordered triple $(i, j, k)$ and check whether $i \to j$, $j \to k$, and $k \to i$. This is straightforward to implement by direct lookup in the array $f$. However, this requires $O(n^3)$ checks, since there are $n^3$ possible triples, and each check is constant time. With $n = 5000$, this is on the order of $1.25 \times 10^{11}$ checks, which is far beyond the time limit.

We can eliminate unnecessary search by observing the structure of the graph. Since each node has exactly one outgoing edge, starting from any node $i$, there is only one possible chain to follow: $i \to f_i \to f_{f_i} \to \dots$. If a 3-cycle exists, it must appear in this deterministic chain structure.

This suggests a direct check per node. For each node $i$, we can define:

- $a = f_i$
- $b = f_a$
- $c = f_b$

Then we only need to verify whether $c = i$. If so, we have found a 3-cycle involving $i$, $a$, and $b$. Because every node has exactly one outgoing edge, every potential 3-cycle will be detected by starting from one of its nodes.

This reduces the problem to $O(n)$ checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all triples) | $O(n^3)$ | $O(1)$ | Too slow |
| Direct 3-step check per node | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the array $f$, adjusting for 0-based indexing if needed. This ensures we can access successors in constant time.
2. For each node $i$, compute its first, second, and third jump: $a = f[i]$, $b = f[a]$, and $c = f[b]$. This simulates following directed edges exactly three times.
3. Check whether $c == i$. If this holds, we have closed a directed cycle of length 3 starting and ending at $i$.
4. If any such $i$ satisfies the condition, immediately output YES. This early exit is valid because existence of one valid triangle is sufficient.
5. If no node produces a valid 3-step return, output NO.

### Why it works

Each node has exactly one outgoing edge, so every length-3 cycle must be uniquely represented by its starting node. If a cycle $A \to B \to C \to A$ exists, then starting from $A$ will deterministically produce $f_A = B$, $f_B = C$, and $f_C = A$, making the check succeed. Since all transitions are deterministic, no cycle can be missed, and no false positive can occur because the condition explicitly enforces closure after exactly three steps.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
f = list(map(int, input().split()))

# convert to 0-based indexing
for i in range(n):
    f[i] -= 1

for i in range(n):
    a = f[i]
    b = f[a]
    c = f[b]
    if c == i:
        print("YES")
        sys.exit()

print("NO")
```

The key implementation detail is the immediate conversion to 0-based indexing. This avoids repeated -1 adjustments during traversal and keeps array access clean.

Another important point is the early exit. Once a valid triangle is found, we terminate immediately because the problem only asks for existence, not enumeration.

The triple jump logic directly mirrors the mathematical condition $f(f(f(i))) = i$, which is the defining property of a 3-cycle in a functional graph.

## Worked Examples

### Example 1

Input:

```
5
2 4 5 1 3
```

We trace each node:

| i | a = f[i] | b = f[a] | c = f[b] | c == i |
| --- | --- | --- | --- | --- |
| 0 | 1 | 3 | 0 | YES |

At $i = 0$, we get $0 \to 1 \to 3 \to 0$, forming a valid 3-cycle.

This confirms the algorithm correctly identifies a cycle when it exists.

### Example 2

Input:

```
3
2 1 2
```

| i | a = f[i] | b = f[a] | c = f[b] | c == i |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | NO |
| 1 | 0 | 1 | 0 | NO |
| 2 | 1 | 0 | 1 | NO |

No starting node returns to itself in exactly three steps, so no 3-cycle exists.

This demonstrates that shorter cycles (length 2 here) do not produce false positives.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each node performs exactly three array lookups and one comparison |
| Space | $O(n)$ | Stores the functional graph in an array |

The solution easily fits within constraints since $n \le 5000$, and the computation is linear with a very small constant factor.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    f = list(map(int, input().split()))
    for i in range(n):
        f[i] -= 1

    for i in range(n):
        a = f[i]
        b = f[a]
        c = f[b]
        if c == i:
            return "YES"
    return "NO"

# provided sample
assert run("5\n2 4 5 1 3\n") == "YES"

# no cycle of length 3
assert run("3\n2 1 2\n") == "NO"

# minimal n
assert run("2\n2 1\n") == "NO"

# simple 3-cycle
assert run("3\n2 3 1\n") == "YES"

# larger with embedded triangle
assert run("4\n2 3 1 2\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 2 4 5 1 3 | YES | basic valid 3-cycle |
| 3 2 1 2 | NO | only 2-cycle exists |
| 2 2 1 | NO | minimum size, no triangle possible |
| 3 2 3 1 | YES | direct 3-cycle |
| 4 2 3 1 2 | YES | triangle embedded in larger graph |

## Edge Cases

A key edge case is when the graph contains cycles but none of length 3. For example, a pure 2-cycle like:

```
3
2 1 2
```

Starting from each node, the algorithm computes exactly three transitions. For node 1: $1 \to 2 \to 1 \to 2$, which does not return to 1, so it is correctly rejected. The same happens for all nodes, so the output is NO.

Another edge case is when multiple nodes feed into a valid 3-cycle. The algorithm still works because it does not rely on reachability or connectivity, only on direct functional composition. For any node inside the cycle, the triple jump will stay inside the cycle and return correctly, ensuring detection even if the cycle is not isolated.
