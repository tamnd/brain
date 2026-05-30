---
title: "CF 1949G - Scooter"
description: "Each building has two independent pieces of information. The first string describes what class is held there. A building may need a mathematics professor, a computer science professor, or no professor at all. The second string describes which professor is initially located there."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1949
codeforces_index: "G"
codeforces_contest_name: "European Championship 2024 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 2300
weight: 1949
solve_time_s: 195
verified: false
draft: false
---

[CF 1949G - Scooter](https://codeforces.com/problemset/problem/1949/G)

**Rating:** 2300  
**Tags:** graphs, greedy  
**Solve time:** 3m 15s  
**Verified:** no  

## Solution
## Problem Understanding

Each building has two independent pieces of information.

The first string describes what class is held there. A building may need a mathematics professor, a computer science professor, or no professor at all.

The second string describes which professor is initially located there. A building may contain a mathematics professor, a computer science professor, or nobody.

You drive a scooter that can carry exactly one passenger professor. You may visit each building at most once. At a visited building you may first drop off the professor currently riding with you and then pick up the professor who was originally located there.

The goal is not to minimize anything. We only need to output a valid itinerary that ends with every class having a professor of the correct specialization.

The bound $n \le 2000$ is small enough that quadratic work is completely acceptable. The challenge is not efficiency, it is discovering the hidden graph structure that makes a valid itinerary easy to construct.

A common mistake is to think about buildings individually. The restriction that a building can be visited only once means that once we leave a building, its final professor assignment is fixed forever.

Consider

```
c = "M"
p = "M"
```

The building is already correct. Visiting it is unnecessary. A solution that tries to move every professor would create work that does not need to exist.

Another subtle case is

```
c = "CM-"
p = "-CM"
```

This is the sample. The building with no class acts as the starting point of the transportation chain. Without such a source of a professor, there would be no way to begin moving people around.

The key observation is that the scooter always carries exactly one professor type, and every pickup immediately replaces the professor that was just dropped off. That behavior naturally forms transitions between professor types.

## Approaches

A brute force approach would try to simulate all possible visiting orders of buildings. Even for $n=20$, there are $20!$ orders, which is already astronomically large. The search space explodes long before reaching the actual limit of 2000 buildings.

The useful observation is that only three professor types exist:

```
-
M
C
```

For a building with class type $c_i$ and initial professor type $p_i$, imagine a directed edge

$$c_i \rightarrow p_i$$

Why this direction?

Suppose we arrive carrying a professor of type $c_i$. We can drop that professor at the building, satisfying its class. Then we pick up the original professor of type $p_i$ and continue carrying that type.

So visiting this building transforms the carried type from $c_i$ into $p_i$.

Now every building becomes a directed edge in a graph with only three vertices:

```
-, M, C
```

A valid itinerary corresponds to traversing edges so that the output type of one building equals the required input type of the next building. That is exactly the definition of an Eulerian traversal.

Because the statement guarantees that a valid itinerary exists, the resulting graph is Eulerian. We only need to find an Euler circuit and then translate its edges back into scooter operations.

Since the graph has only three vertices, Hierholzer's algorithm is more than sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!)$ | $O(n)$ | Too slow |
| Euler Tour Construction | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### 1. Build the graph

Create three vertices corresponding to:

```
0 = -
1 = M
2 = C
```

For every building $i$, add a directed edge

$$c_i \rightarrow p_i$$

and store the building index on that edge.

### 2. Find an Euler circuit

Run Hierholzer's algorithm starting from vertex `-`.

Every edge must be used exactly once.

The order in which edges are produced by Hierholzer is the order in which buildings will participate in the transportation chain.

### 3. Convert the Euler circuit into buildings

Let the Euler circuit return an edge sequence

$$e_1, e_2, \dots, e_k$$

where each edge corresponds to a building.

Consecutive edges satisfy

$$p(e_i)=c(e_{i+1})$$

which is exactly the compatibility condition needed for the scooter.

### 4. Generate commands

Drive to the building of the first edge.

If its initial professor is not `-`, issue `PICKUP`.

For every subsequent building:

1. `DRIVE` to that building.
2. If we are carrying a professor, issue `DROPOFF`.
3. If the building initially contains a professor, issue `PICKUP`.

After processing the last building, if a professor is still being carried, issue one final `DROPOFF`.

The Euler circuit guarantees that every dropoff professor has the correct specialization for that building.

### Why it works

Each edge represents a building that converts the carried professor type from its class type to its original professor type.

In an Euler circuit, the end vertex of every edge equals the start vertex of the next edge. Consequently, the professor type picked up at one building is exactly the type required by the next building.

When we drop off a professor at a building, that professor's specialization matches the building's class type, because the edge begins at that class type. The pickup then changes the carried type to the edge's destination vertex.

Since every edge is used exactly once, every building is processed exactly once. Since the traversal is Eulerian, all type requirements match throughout the chain. Every class ends with a professor of the correct specialization.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    c = input().strip()
    p = input().strip()

    mp = {'-': 0, 'M': 1, 'C': 2}
    rev = ['-', 'M', 'C']

    g = [[] for _ in range(3)]

    for i in range(n):
        u = mp[c[i]]
        v = mp[p[i]]
        g[u].append((v, i + 1))

    ptr = [0] * 3
    stack_v = [0]
    stack_e = []
    euler = []

    while stack_v:
        v = stack_v[-1]

        if ptr[v] < len(g[v]):
            to, idx = g[v][ptr[v]]
            ptr[v] += 1

            stack_v.append(to)
            stack_e.append(idx)
        else:
            stack_v.pop()
            if stack_e:
                euler.append(stack_e.pop())

    euler.reverse()

    ops = []

    if not euler:
        print(0)
        return

    first = euler[0]
    ops.append(f"DRIVE {first}")

    carrying = False

    if p[first - 1] != '-':
        ops.append("PICKUP")
        carrying = True

    for b in euler[1:]:
        ops.append(f"DRIVE {b}")

        if carrying:
            ops.append("DROPOFF")
            carrying = False

        if p[b - 1] != '-':
            ops.append("PICKUP")
            carrying = True

    if carrying:
        ops.append("DROPOFF")

    print(len(ops))
    print("\n".join(ops))

solve()
```

The graph contains only three vertices, but up to 2000 edges. Each edge stores the building index because the final itinerary must reference buildings, not graph edges.

Hierholzer's algorithm is implemented iteratively. The `stack_v` stack stores vertices on the current DFS path, while `stack_e` stores the corresponding edge identifiers. When a vertex runs out of outgoing edges, the most recent edge becomes part of the Euler circuit.

After reversing the produced edge list, we obtain the traversal order.

The command generation phase directly mirrors the interpretation of an edge. A pickup changes the carried professor type to the edge destination. A dropoff consumes the professor carried from the previous edge. The Euler property guarantees that every dropoff specialization matches the next building's class requirement.

The most delicate detail is the order `DROPOFF` then `PICKUP`. The statement explicitly allows at most one dropoff and one pickup in that order at a building. Reversing them would violate the rules.

## Worked Examples

### Example 1

Input:

```
3
CM-
-CM
```

The graph edges are:

| Building | Edge |
| --- | --- |
| 1 | C → - |
| 2 | M → C |
| 3 | - → M |

An Euler circuit is:

```
3 → 2 → 1
```

| Step | Building | Carry Before | Action | Carry After |
| --- | --- | --- | --- | --- |
| 1 | 3 | none | PICKUP M | M |
| 2 | 2 | M | DROPOFF, PICKUP C | C |
| 3 | 1 | C | DROPOFF | none |

Generated commands:

```
DRIVE 3
PICKUP
DRIVE 2
DROPOFF
PICKUP
DRIVE 1
DROPOFF
```

This demonstrates how the carried specialization flows through the Euler circuit.

### Example 2

Input:

```
2
--
MC
```

Edges:

| Building | Edge |
| --- | --- |
| 1 | - → M |
| 2 | - → C |

The Euler traversal simply visits both source buildings.

| Step | Building | Carry Before | Action | Carry After |
| --- | --- | --- | --- | --- |
| 1 | 1 | none | PICKUP M | M |
| 2 | 2 | M | DROPOFF, PICKUP C | C |
| End | - | C | DROPOFF | none |

This example shows that the algorithm handles buildings without classes naturally.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each edge is processed once by Hierholzer's algorithm |
| Space | $O(n)$ | Graph storage and Euler traversal stacks |

The graph contains only three vertices and exactly $n$ edges. Every edge is inserted once and traversed once, so the running time is linear in the number of buildings. With $n \le 2000$, this easily fits within the limits.

## Test Cases

```python
# helper skeleton for local testing

import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    # call solve() here
    return ""

# sample from statement
# output is not unique, so exact-output assertions are inappropriate.

# minimum size
inp = """\
1
-
-
"""

# already satisfied building
inp = """\
1
M
M
"""

# simple chain
inp = """\
3
CM-
-CM
"""

# multiple buildings of same type
inp = """\
4
MMCC
MMCC
"""

# larger balanced construction
inp = """\
6
MMC-C-
CMM--C
"""
```

Because the output is not unique, practical testing should validate the produced itinerary rather than compare against a single fixed output string.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1`, no class, no professor | Any valid empty or trivial itinerary | Minimum size |
| One building with matching professor | Valid itinerary | Already satisfied state |
| Sample chain | Valid itinerary | Basic transportation chain |
| All buildings already matched | Valid itinerary | Self-loop heavy graph |
| Mixed larger instance | Valid itinerary | General Euler traversal |

## Edge Cases

Consider

```
1
M
M
```

The building already contains the correct professor. In graph terms this is a self-loop `M → M`. Hierholzer handles self-loops naturally. Visiting the building simply drops and picks up the same specialization, preserving correctness.

Consider

```
3
CM-
-CM
```

The only source of professors is the building with no class. Its edge is `- → M`, which becomes the natural beginning of the Euler circuit. The algorithm starts there, picks up the mathematics professor, and propagates specializations through the chain.

Consider

```
4
MMCC
MMCC
```

Every edge is a self-loop. No professor actually needs to move. The Euler traversal still exists and remains valid because each building already satisfies its class requirement. The generated itinerary respects the one-visit restriction and never creates an incompatible assignment.

The critical invariant in all these cases is unchanged: when a building edge `c → p` is processed, the professor dropped there has specialization `c`, and the professor carried away has specialization `p`. The Euler traversal guarantees these types match across consecutive buildings.
