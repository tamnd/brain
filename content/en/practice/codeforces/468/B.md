---
title: "CF 468B - Two Sets"
description: "We are given a set of n distinct integers. Every number must be assigned to one of two groups. If a number x is placed into group A, then its complement with respect to a, namely a - x, must also be present and must belong to A."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "2-sat", "dfs-and-similar", "dsu", "graph-matchings", "greedy"]
categories: ["algorithms"]
codeforces_contest: 468
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 268 (Div. 1)"
rating: 2000
weight: 468
solve_time_s: 152
verified: true
draft: false
---

[CF 468B - Two Sets](https://codeforces.com/problemset/problem/468/B)

**Rating:** 2000  
**Tags:** 2-sat, dfs and similar, dsu, graph matchings, greedy  
**Solve time:** 2m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of `n` distinct integers. Every number must be assigned to one of two groups.

If a number `x` is placed into group `A`, then its complement with respect to `a`, namely `a - x`, must also be present and must belong to `A`.

Similarly, if `x` is placed into group `B`, then its complement with respect to `b`, namely `b - x`, must also be present and must belong to `B`.

The numbers themselves are fixed. We are not allowed to add missing values. We only choose whether each existing number belongs to group `A` or group `B`.

The output is an assignment for every input number. Conventionally, `0` means the number belongs to `A`, and `1` means it belongs to `B`.

The constraint `n ≤ 100000` immediately rules out any exponential search. Even an `O(n²)` algorithm would require around `10¹⁰` operations in the worst case, which is far beyond the limit. We need something close to linear or `O(n log n)`.

Several edge cases make the problem tricky.

Consider:

```
n = 1
a = 10
b = 20
p = [3]
```

The number `3` has neither complement `7` nor complement `17` in the set. No assignment is possible, so the answer is `NO`.

Now consider:

```
n = 2
a = 5
b = 100
p = [2, 3]
```

Here `2` and `3` form a valid pair for sum `5`. Neither number has a valid partner for sum `100`. Both numbers are forced into set `A`.

A careless solution that tries to decide numbers independently can fail on situations such as:

```
a = 10
b = 12
p = [1, 9, 3]
```

Number `1` can only participate in sum `10`, since `9` exists. Number `3` can only participate in sum `12`, but `9` would then need to be in both sets simultaneously. The answer is `NO`.

The main difficulty is that decisions propagate through the graph of complement relations.

## Approaches

The most direct approach is brute force. For every number, choose either set `A` or set `B`, then verify whether all complement requirements hold.

There are `2ⁿ` assignments. With `n = 100000`, this is completely impossible.

The reason brute force works conceptually is that the constraints are local. A number only cares about its complement with respect to `a` and `b`. The problem is that local choices interact, creating long chains of dependencies.

The key observation is that every number can have at most one partner for sum `a` and at most one partner for sum `b`.

If we build a graph whose vertices are the given numbers, then:

A-type edge:

`x ↔ a - x` whenever both numbers exist.

B-type edge:

`x ↔ b - x` whenever both numbers exist.

Suppose a number lacks its A-partner. Then it can never belong to set `A`, so it is forced into set `B`.

Likewise, if a number lacks its B-partner, it is forced into set `A`.

These forced choices propagate. If a vertex is forced into `A`, then every vertex connected through an A-edge must also be in `A`. If one of those vertices was already forced into `B`, we have a contradiction.

This structure is perfectly suited for a Disjoint Set Union construction.

Introduce two special nodes:

`SA` meaning "belongs to A"

`SB` meaning "belongs to B"

For every number:

If its A-partner does not exist, union it with `SB`.

If its B-partner does not exist, union it with `SA`.

For every existing A-edge `(x, a-x)`:

Union the corresponding vertices.

For every existing B-edge `(x, b-x)`:

Union the corresponding vertices.

The classical accepted solution actually models the problem as a graph whose connected components are paths or cycles. Inside each component, all vertices must end up in the same group. The DSU captures exactly this propagation.

After all unions, if `SA` and `SB` become connected, the constraints are inconsistent.

Otherwise, every component connected to `SA` is assigned to set `A`, every component connected to `SB` is assigned to set `B`, and remaining free components can be assigned arbitrarily.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ · n) | O(n) | Too slow |
| Optimal DSU | O(n α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all numbers and build a hash map from value to index.
2. Create a DSU with `n + 2` vertices.

The last two vertices represent the special states `SA` and `SB`.
3. For each number `x`, check whether `a - x` exists.

If it does not exist, then `x` cannot belong to set `A`. Union its vertex with `SB`.
4. For each number `x`, check whether `b - x` exists.

If it does not exist, then `x` cannot belong to set `B`. Union its vertex with `SA`.
5. For every existing A-partner pair, union the two corresponding vertices.

If one vertex belongs to `A`, the other must also belong to `A`.
6. For every existing B-partner pair, union the two corresponding vertices.

If one vertex belongs to `B`, the other must also belong to `B`.
7. After all unions, check whether `SA` and `SB` belong to the same DSU component.

If they do, some number is simultaneously forced into both sets and no valid assignment exists.
8. Otherwise, determine the assignment of every number.

If its component is connected to `SA`, output `0`.

Otherwise output `1`.

### Why it works

A missing A-partner means the number can never be placed into set `A`, so it must belong to `B`. The symmetric statement holds for missing B-partners.

Every complement relation requires both endpoints to receive the same assignment. DSU merges exactly the vertices that must always move together.

After all such implications are processed, every DSU component represents a group of numbers whose assignments are inseparable. Connecting a component to `SA` fixes it to set `A`, while connecting it to `SB` fixes it to set `B`.

If `SA` and `SB` end up in the same component, some chain of implications forces a number to belong to both sets simultaneously. Otherwise, every component has a consistent assignment, giving a valid partition.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return

        if self.size[a] < self.size[b]:
            a, b = b, a

        self.parent[b] = a
        self.size[a] += self.size[b]

def solve():
    n, a, b = map(int, input().split())
    p = list(map(int, input().split()))

    pos = {x: i for i, x in enumerate(p)}

    SA = n
    SB = n + 1

    dsu = DSU(n + 2)

    for i, x in enumerate(p):
        ax = a - x
        bx = b - x

        if ax not in pos:
            dsu.union(i, SB)

        if bx not in pos:
            dsu.union(i, SA)

    for i, x in enumerate(p):
        ax = a - x
        bx = b - x

        if ax in pos:
            dsu.union(i, pos[ax])

        if bx in pos:
            dsu.union(i, pos[bx])

    if dsu.find(SA) == dsu.find(SB):
        print("NO")
        return

    rootA = dsu.find(SA)

    ans = []
    for i in range(n):
        if dsu.find(i) == rootA:
            ans.append("0")
        else:
            ans.append("1")

    print("YES")
    print(" ".join(ans))

solve()
```

The hash map `pos` allows constant-time lookup of complements. Without it, every complement search would require a linear scan and the solution would become quadratic.

The two special DSU vertices are the central idea. They represent forced membership in one of the two sets. Missing complements create those forced assignments immediately.

The second pass merges all complement pairs. Since every complement rule requires equal assignment, DSU is exactly the right structure.

The final check compares the representatives of `SA` and `SB`. A match means contradictory requirements reached the same component.

When building the answer, every component connected to `SA` is assigned to set `A`. All remaining components belong to set `B`. Because `SA` and `SB` are disconnected, this assignment is always consistent.

## Worked Examples

### Example 1

Input:

```
4 5 9
2 3 4 5
```

| Number | A-partner | Exists | B-partner | Exists |
| --- | --- | --- | --- | --- |
| 2 | 3 | Yes | 7 | No |
| 3 | 2 | Yes | 6 | No |
| 4 | 1 | No | 5 | Yes |
| 5 | 0 | No | 4 | Yes |

Forced assignments:

| Number | Forced to |
| --- | --- |
| 2 | A |
| 3 | A |
| 4 | B |
| 5 | B |

Complement unions connect `(2,3)` and `(4,5)`.

Final assignment:

| Number | Set |
| --- | --- |
| 2 | A |
| 3 | A |
| 4 | B |
| 5 | B |

Output:

```
YES
0 0 1 1
```

This example shows how missing complements immediately force components to one side.

### Example 2

Input:

```
3 10 12
1 9 3
```

| Number | A-partner | Exists | B-partner | Exists |
| --- | --- | --- | --- | --- |
| 1 | 9 | Yes | 11 | No |
| 9 | 1 | Yes | 3 | Yes |
| 3 | 7 | No | 9 | Yes |

Forces:

| Number | Forced to |
| --- | --- |
| 1 | A |
| 3 | B |

A-edge connects `1` and `9`.

B-edge connects `9` and `3`.

All three numbers become part of one DSU component.

That component is connected to both `SA` and `SB`, creating a contradiction.

Output:

```
NO
```

This demonstrates how independent local constraints can collide through a chain of complement relations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n α(n)) | Hash lookups plus DSU operations |
| Space | O(n) | DSU arrays and hash map |

`α(n)` is the inverse Ackermann function and is effectively constant for all practical input sizes. With `n = 100000`, the solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string

import sys
import io

def run(inp: str) -> str:
    out = io.StringIO()

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))
            self.size = [1] * n

        def find(self, x):
            while self.parent[x] != x:
                self.parent[x] = self.parent[self.parent[x]]
                x = self.parent[x]
            return x

        def union(self, a, b):
            a = self.find(a)
            b = self.find(b)
            if a == b:
                return
            if self.size[a] < self.size[b]:
                a, b = b, a
            self.parent[b] = a
            self.size[a] += self.size[b]

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, a, b = map(int, input().split())
    p = list(map(int, input().split()))

    pos = {x: i for i, x in enumerate(p)}

    SA = n
    SB = n + 1

    dsu = DSU(n + 2)

    for i, x in enumerate(p):
        if a - x not in pos:
            dsu.union(i, SB)
        if b - x not in pos:
            dsu.union(i, SA)

    for i, x in enumerate(p):
        if a - x in pos:
            dsu.union(i, pos[a - x])
        if b - x in pos:
            dsu.union(i, pos[b - x])

    if dsu.find(SA) == dsu.find(SB):
        return "NO"

    rootA = dsu.find(SA)
    ans = []

    for i in range(n):
        ans.append("0" if dsu.find(i) == rootA else "1")

    return "YES\n" + " ".join(ans)

# provided sample
assert run("4 5 9\n2 3 4 5\n") == "YES\n0 0 1 1"

# single value, impossible
assert run("1 10 20\n3\n") == "NO"

# pair forced into A
assert run("2 5 100\n2 3\n") == "YES\n0 0"

# contradiction through chain
assert run("3 10 12\n1 9 3\n") == "NO"

# all numbers belong to B
assert run("2 100 5\n2 3\n") == "YES\n1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 10 20 / 3` | `NO` | Number has no valid complement |
| `2 5 100 / 2 3` | `YES 0 0` | Entire component forced into A |
| `3 10 12 / 1 9 3` | `NO` | Contradiction propagation |
| `2 100 5 / 2 3` | `YES 1 1` | Entire component forced into B |

## Edge Cases

Consider:

```
1 10 20
3
```

The number `3` lacks both complements `7` and `17`. The algorithm unions its component with both `SA` and `SB`. Since those representatives become identical, the answer is immediately `NO`.

Consider:

```
2 5 100
2 3
```

Both numbers have valid A-partners but no valid B-partners. The algorithm connects both vertices to `SA`, merges them through the A-edge, and never touches `SB`. The final assignment is uniquely determined as set `A`.

Consider:

```
3 10 12
1 9 3
```

Vertex `1` is forced to `A`, vertex `3` is forced to `B`. Complement edges merge `1 ↔ 9` and `9 ↔ 3`, so all three vertices become one DSU component. That component touches both special nodes, creating a contradiction. The algorithm correctly outputs `NO`.

Consider:

```
4 8 8
1 7 3 5
```

Here both sums are identical. Every complement relation is the same relation. The DSU simply merges the matching pairs. No contradiction appears, and any consistent assignment works. The algorithm handles this naturally because unions are idempotent.
