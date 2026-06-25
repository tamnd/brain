---
title: "CF 105813F - Walkable Strings"
description: "We are given an undirected graph whose edges are colored either R or B. A string is called walkable if there exists some walk in the graph whose edge colors, read in order, exactly match the characters of the string. Walks may revisit vertices and edges."
date: "2026-06-26T00:06:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105813
codeforces_index: "F"
codeforces_contest_name: "Rutgers University Programming Contest Spring 2025"
rating: 0
weight: 105813
solve_time_s: 71
verified: true
draft: false
---

[CF 105813F - Walkable Strings](https://codeforces.com/problemset/problem/105813/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected graph whose edges are colored either `R` or `B`.

A string is called walkable if there exists some walk in the graph whose edge colors, read in order, exactly match the characters of the string. Walks may revisit vertices and edges.

For each test case, we must output a shortest string that is **not** walkable. If every possible string over `{R,B}` is walkable, we print `-1`.

The graph can contain up to `2·10^5` vertices and edges across all test cases. Any solution that explicitly builds automaton subsets or checks all strings of a given length is hopeless. Even checking all strings of length 30 would already require over one billion candidates.

The challenge is to exploit the special structure of a binary alphabet.

A subtle point is that a shortest forbidden string is not necessarily a single color repeated many times.

Consider:

```
1 --R-- 2
```

The string `RR` is not walkable, but `R` is. The shortest answer is `RR`.

Another easy mistake is to assume that if both colors appear somewhere, then every length-1 string is walkable and we only need to check longer lengths.

Example:

```
1 --R-- 2

3 --B-- 4
```

Both `R` and `B` are walkable, but `RB` is not. No walk can switch from the red component to the blue component. The correct answer has length 2.

A third pitfall is handling cycles incorrectly.

If the graph contains a walk whose color pattern repeats forever in the right way, then arbitrarily long strings become possible. Detecting this situation is exactly what separates the `-1` cases from the finite-answer cases.

## Approaches

A brute-force viewpoint is useful first.

Suppose we want to know whether a string is walkable. We can treat every vertex as a possible current position. After reading each character, we move along edges of the corresponding color. This is just simulation of an NFA.

That immediately suggests checking strings level by level in BFS order and stopping at the first non-walkable one.

The problem is the number of candidate strings. There are `2^k` strings of length `k`. Even if the shortest forbidden string has length only 40, that already means roughly one trillion candidates.

So we need a completely different perspective.

The key observation is a beautiful combinatorial lemma used for binary walkability problems.

Define the infinite periodic pattern

```
RRBBRRBBRRBB...
```

and its four cyclic shifts:

```
RRBBRRBB...
RBBRRBBR...
BBRRBBRR...
BRRBBRRB...
```

Call these four periodic strings `P0, P1, P2, P3`.

A classical result is:

If all four length-`k` prefixes of these periodic strings are walkable, then **every** binary string of length `k` is walkable.

This completely changes the problem.

Instead of checking all `2^k` strings, we only need to understand the longest walkable prefix of each of these four periodic sequences.

Now the graph structure becomes important.

Create four phase states corresponding to positions inside the cycle

```
R -> R -> B -> B -> R -> ...
```

For every original vertex `v`, create four copies `(v,0)...(v,3)`.

If phase `p` expects color `c`, then every original edge of color `c` becomes a directed transition

```
(u,p) -> (v,(p+1) mod 4)
(v,p) -> (u,(p+1) mod 4)
```

A directed path in this new graph corresponds exactly to following the periodic sequence from a particular phase.

If this directed graph contains a cycle, then some periodic sequence can be extended forever. Repeating that cycle generates arbitrarily long prefixes, and the lemma implies that every binary string is walkable. The answer is `-1`.

Otherwise the graph is a DAG.

In a DAG, the longest walkable prefix from a phase is just the longest directed path starting from any node of that phase.

Once we know those four maximum lengths, the shortest forbidden string is obtained from the phase whose maximum walkable prefix is smallest.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over strings | Exponential | Exponential | Too slow |
| Phase graph + DAG DP | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build a directed graph with `4n` nodes.
2. Use the phase pattern:

```
phase 0 -> R
phase 1 -> R
phase 2 -> B
phase 3 -> B
```

1. For every original edge `(u,v,color)` and every phase whose expected color equals `color`, add:

```
(u,phase) -> (v,next_phase)
(v,phase) -> (u,next_phase)
```

1. Run a topological process on this directed graph.
2. If not all nodes are removed by the topological process, the graph contains a directed cycle. Output `-1`.
3. Otherwise process nodes in reverse topological order and compute:

```
dp[x] = longest number of edges in a path starting from x
```

1. For each phase `p`, compute:

```
best[p] = max(dp[(v,p)])
```

over all original vertices `v`.

1. Let

```
p = argmin(best[p])
```

The longest walkable prefix from that phase has length `best[p]`, so the shortest non-walkable prefix has length:

```
L = best[p] + 1
```

1. Output the first `L` characters of the periodic sequence starting from phase `p`.

### Why it works

The constructed phase graph encodes exactly one periodic family of strings.

A directed path of length `t` starting in phase `p` corresponds to a walk whose color sequence is the first `t` characters of the periodic string beginning at phase `p`.

If the phase graph contains a cycle, that periodic family has arbitrarily long walkable prefixes. The cycle length is a multiple of four because phases advance modulo four. Repeating the cycle produces arbitrarily long prefixes for all four shifts, which by the lemma implies that every binary string is walkable.

If the phase graph is acyclic, the longest path computation gives the maximum walkable prefix length for each shift. The first prefix length that fails for some shift is exactly `best[p] + 1`. The lemma guarantees that this is also the minimum length at which some binary string becomes non-walkable. Hence the constructed periodic prefix is a valid shortest answer.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

PAT = "RRBB"

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n, m = map(int, input().split())

        N = 4 * n
        g = [[] for _ in range(N)]
        indeg = [0] * N

        for _ in range(m):
            u, v, c = input().split()
            u = int(u) - 1
            v = int(v) - 1

            for p in range(4):
                if PAT[p] == c:
                    np = (p + 1) & 3

                    a = u * 4 + p
                    b = v * 4 + np
                    g[a].append(b)
                    indeg[b] += 1

                    a = v * 4 + p
                    b = u * 4 + np
                    g[a].append(b)
                    indeg[b] += 1

        q = deque(i for i in range(N) if indeg[i] == 0)
        topo = []

        while q:
            v = q.popleft()
            topo.append(v)

            for to in g[v]:
                indeg[to] -= 1
                if indeg[to] == 0:
                    q.append(to)

        if len(topo) != N:
            out.append("-1")
            continue

        dp = [0] * N

        for v in reversed(topo):
            best = 0
            for to in g[v]:
                cand = 1 + dp[to]
                if cand > best:
                    best = cand
            dp[v] = best

        phase_best = [0] * 4

        for phase in range(4):
            mx = 0
            for v in range(n):
                mx = max(mx, dp[v * 4 + phase])
            phase_best[phase] = mx

        phase = min(range(4), key=lambda p: phase_best[p])
        length = phase_best[phase] + 1

        ans = []
        for i in range(length):
            ans.append(PAT[(phase + i) & 3])

        out.append("".join(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The graph has `4n` nodes because every original vertex is duplicated once for each position inside the `RRBB` cycle.

The topological sort serves two purposes. It detects cycles and also provides the ordering needed for longest-path DP in a DAG.

The DP stores path lengths in edges, not vertices. Since a string of length `L` corresponds to traversing exactly `L` colored edges, this is the quantity we need.

The final answer length is `best + 1`, because `best` is the maximum walkable prefix length. The next character is the first point where walkability fails.

## Worked Examples

### Example 1

Input:

```
3 3
1 2 R
2 3 R
3 1 R
```

Only red edges exist.

For phase 2, the periodic sequence starts with `B`.

| Phase | Longest walkable prefix |
| --- | --- |
| RRBB... | 2 |
| RBBR... | 1 |
| BBRR... | 0 |
| BRRB... | 0 |

The minimum value is `0`, so the answer length is `1`.

Output:

```
B
```

This demonstrates that a missing color immediately creates a forbidden string of length one.

### Example 2

Input:

```
4 2
1 2 R
3 4 B
```

| Phase | Longest walkable prefix |
| --- | --- |
| RRBB... | 1 |
| RBBR... | 1 |
| BBRR... | 1 |
| BRRB... | 1 |

The minimum is `1`, so the answer length is `2`.

Starting from phase 1 produces:

```
RB
```

No walk can use a red edge and then a blue edge because the colors live in different connected components.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | The phase graph has 4n nodes and O(m) transitions per phase construction, still linear overall |
| Space | O(n + m) | Adjacency lists, indegrees, and DP arrays |

The total number of vertices and edges across all test cases is at most `2·10^5`, so a linear solution comfortably fits within the limits.

## Test Cases

```python
import sys
import io

# helper sketch

# 1. no edges
inp = """1
1 0
"""

# expected: R or B, length 1

# 2. only red edges
inp = """1
3 3
1 2 R
2 3 R
3 1 R
"""

# expected: B

# 3. disconnected colors
inp = """1
4 2
1 2 R
3 4 B
"""

# expected length 2 answer such as RB

# 4. graph where all strings are walkable
inp = """1
7 10
1 2 B
1 4 R
2 4 B
4 5 B
6 7 R
6 2 R
5 7 B
3 6 B
3 7 R
1 7 B
"""

# expected: -1

# 5. minimum-size graph
inp = """1
1 0
"""

# expected length 1
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single isolated vertex | Length 1 string | No walk exists |
| All-red graph | `B` | Missing color |
| Separate red and blue components | Length 2 answer | Component transitions matter |
| Sample `-1` graph | `-1` | Infinite walkability |
| Smallest graph | Length 1 answer | Boundary conditions |

## Edge Cases

Consider a graph with no edges:

```
1 0
```

No non-empty string is walkable. The phase graph has no edges, so every DP value is zero. The algorithm outputs a periodic prefix of length one, such as `R`. That is correct.

Consider a graph containing only red edges:

```
3 3
1 2 R
2 3 R
3 1 R
```

Any periodic sequence beginning with `B` has maximum walkable prefix length zero. The algorithm immediately returns `B`, which is the shortest forbidden string.

Consider two disconnected monochromatic components:

```
4 2
1 2 R
3 4 B
```

A single `R` and a single `B` are both walkable. However, any string requiring a color switch is impossible. The DP finds that every periodic shift has longest walkable prefix length one, producing a forbidden string of length two such as `RB`. This catches the common mistake of checking only individual colors.

The cycle case is handled by the topological sort. If the phase graph contains a directed cycle, the algorithm outputs `-1`, recognizing that arbitrarily long periodic prefixes exist and consequently every binary string is walkable.
