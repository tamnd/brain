---
title: "CF 489D - Unbearable Controversy of Being"
description: "We are given a directed graph representing intersections and one-way roads. A \"damn rhombus\" consists of four distinct vertices $a, b, c, d$ such that there are directed edges $$a rightarrow b,quad b rightarrow c,quad a rightarrow d,quad d rightarrow c$$ In other words, from the…"
date: "2026-06-07T17:36:35+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 489
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 277.5 (Div. 2)"
rating: 1700
weight: 489
solve_time_s: 113
verified: true
draft: false
---

[CF 489D - Unbearable Controversy of Being](https://codeforces.com/problemset/problem/489/D)

**Rating:** 1700  
**Tags:** brute force, combinatorics, dfs and similar, graphs  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph representing intersections and one-way roads.

A "damn rhombus" consists of four distinct vertices $a, b, c, d$ such that there are directed edges

$$a \rightarrow b,\quad b \rightarrow c,\quad a \rightarrow d,\quad d \rightarrow c$$

In other words, from the same starting vertex $a$, there are two different length-2 directed paths that end at the same vertex $c$, using different intermediate vertices $b$ and $d$.

The task is to count how many such structures exist in the graph. The order of the middle vertices does not matter, so $(b,d)$ and $(d,b)$ describe the same rhombus.

The graph contains at most 3000 vertices and 30000 directed edges. The vertex count is relatively large, but the edge count is only ten times larger. A solution that checks all quadruples of vertices would require roughly $3000^4$ operations, which is completely impossible. Even checking all triples would be far too expensive.

The constraint $m \le 30000$ is the real clue. Algorithms whose complexity depends mainly on edges, such as $O(m\sqrt m)$ or $O(nm)$, are plausible. An $O(n^2)$ or $O(n^3)$ algorithm must be examined carefully.

Several edge cases can cause mistakes.

Consider:

```
3 2
1 2
2 3
```

There is only one length-2 path from 1 to 3, so the answer is:

```
0
```

A careless solution that merely counts length-2 paths could incorrectly return 1.

Another important case is when multiple length-2 paths share the same start and end.

```
4 4
1 2
2 4
1 3
3 4
```

There are exactly two paths from 1 to 4, namely $1\to2\to4$ and $1\to3\to4$. These form one rhombus, so the answer is:

```
1
```

A different subtle case is when more than two intermediates exist.

```
5 6
1 2
2 5
1 3
3 5
1 4
4 5
```

There are three length-2 paths from 1 to 5. Any pair of intermediates forms a rhombus:

$$(2,3),\ (2,4),\ (3,4)$$

The answer is:

```
3
```

A solution that only checks whether at least two paths exist would undercount.

Finally, the four vertices must be distinct. Because the graph contains no self-loops, counting pairs of different intermediate vertices automatically guarantees distinctness, but this fact must be understood during the correctness argument.

## Approaches

The most direct idea is to enumerate every quadruple $(a,b,d,c)$ and check whether all four required edges exist.

This is correct because every rhombus corresponds to exactly one such quadruple. Unfortunately, there are $O(n^4)$ quadruples. With $n=3000$, this is completely infeasible.

A better observation is to focus on the start vertex $a$.

Suppose $a$ is fixed. Every outgoing edge $a \rightarrow x$ can be the first step of a length-2 path. If we follow all such edges and record where these length-2 paths end, then for every destination vertex $c$ we obtain the number of distinct intermediates that create a path

$$a \rightarrow * \rightarrow c.$$

Let this count be $k$.

Each pair of intermediates among these $k$ choices forms a rhombus with start vertex $a$ and end vertex $c$. The number of such pairs is

$$\binom{k}{2} = \frac{k(k-1)}{2}.$$

This transforms the problem into counting length-2 paths grouped by their common start and end vertices.

The graph is sparse. For a fixed source $a$, we can iterate through every outgoing neighbor $u$, then through every outgoing neighbor $v$ of $u$. Every visit corresponds to one directed walk of length 2 starting at $a$.

The total work over all sources is

$$\sum_{a}\sum_{u \in out(a)} outdeg(u).$$

Reordering the summation gives

$$\sum_{u} indeg(u)\cdot outdeg(u).$$

Since $m \le 30000$, the maximum value of this expression is comfortably within the limit and is the intended solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^4)$ | $O(1)$ | Too slow |
| Optimal | $O\!\left(\sum indeg(v)\,outdeg(v)\right)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Store the graph using adjacency lists.
2. Initialize the answer to zero.
3. For every vertex $a$:

1. Create an array `cnt` of size $n$, initially filled with zeros.
2. For every outgoing neighbor $u$ of $a$:

1. For every outgoing neighbor $v$ of $u$:

1. Increment `cnt[v]`.

After this loop, `cnt[v]` equals the number of distinct length-2 paths from $a$ to $v$.
4. For every vertex $v$:

1. Let $k = cnt[v]$.
2. Add $k(k-1)/2$ to the answer.

Every pair of length-2 paths ending at the same vertex contributes one rhombus.
5. Print the accumulated answer.

### Why it works

Fix a source vertex $a$ and a destination vertex $c$.

Every time the algorithm reaches $c$ while traversing

$$a \rightarrow b \rightarrow c,$$

it increments `cnt[c]`. Thus `cnt[c]` becomes exactly the number of valid intermediate vertices that produce a length-2 path from $a$ to $c$.

A rhombus with endpoints $a$ and $c$ is obtained by choosing any two distinct intermediates among these paths. The number of such choices is precisely $\binom{k}{2}$, where $k=cnt[c]$.

Every rhombus is counted exactly once because it has a unique start vertex $a$ and end vertex $c$. No rhombus is missed because every length-2 path contributes to the corresponding count. No rhombus is counted twice because unordered pairs of intermediates are counted exactly once by the combination formula.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    g = [[] for _ in range(n)]

    for _ in range(m):
        a, b = map(int, input().split())
        g[a - 1].append(b - 1)

    ans = 0

    for a in range(n):
        cnt = [0] * n

        for u in g[a]:
            for v in g[u]:
                cnt[v] += 1

        for k in cnt:
            ans += k * (k - 1) // 2

    print(ans)

if __name__ == "__main__":
    solve()
```

The adjacency list stores all outgoing edges.

For each source vertex `a`, the array `cnt` counts how many length-2 paths end at every vertex. The nested traversal

```
for u in g[a]:
    for v in g[u]:
```

enumerates every directed walk of length two starting from `a`.

After all such walks are processed, `cnt[v]` equals the number of intermediates connecting `a` to `v`. Choosing any two of those intermediates yields one rhombus, which is why the contribution is

```
k * (k - 1) // 2
```

The answer can become much larger than $2^{31}$, so it must be stored in a 64-bit capable integer. Python integers grow automatically, so no special handling is needed.

The graph is converted to zero-based indexing immediately after reading. This avoids repeated index adjustments inside the main loops.

## Worked Examples

### Example 1

Input:

```
5 4
1 2
2 3
1 4
4 3
```

For source vertex 1:

| Path | Destination | cnt |
| --- | --- | --- |
| 1→2→3 | 3 | cnt[3]=1 |
| 1→4→3 | 3 | cnt[3]=2 |

After processing:

| Vertex | k | Contribution |
| --- | --- | --- |
| 3 | 2 | 1 |
| Others | 0 | 0 |

Total answer becomes 1.

Output:

```
1
```

This demonstrates the basic rhombus structure: two different intermediates leading from the same start to the same end.

### Example 2

Input:

```
5 6
1 2
2 5
1 3
3 5
1 4
4 5
```

For source vertex 1:

| Path | Destination | cnt |
| --- | --- | --- |
| 1→2→5 | 5 | 1 |
| 1→3→5 | 5 | 2 |
| 1→4→5 | 5 | 3 |

Now `k=3` for vertex 5.

| Vertex | k | Contribution |
| --- | --- | --- |
| 5 | 3 | 3 |
| Others | 0 | 0 |

Output:

```
3
```

The three rhombi correspond to choosing any pair among intermediates {2, 3, 4}.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O\!\left(\sum indeg(v)\,outdeg(v)\right)$ | Every length-2 directed walk is processed once |
| Space | $O(n)$ | Counting array for one source vertex |

The graph contains at most 30000 edges. The accepted solution processes all length-2 walks and uses only a single counting array of size $n$. Both the running time and memory usage comfortably fit within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, m = map(int, input().split())

    g = [[] for _ in range(n)]

    for _ in range(m):
        a, b = map(int, input().split())
        g[a - 1].append(b - 1)

    ans = 0

    for a in range(n):
        cnt = [0] * n

        for u in g[a]:
            for v in g[u]:
                cnt[v] += 1

        for k in cnt:
            ans += k * (k - 1) // 2

    return str(ans)

# provided sample
assert run("""5 4
1 2
2 3
1 4
4 3
""") == "1", "sample 1"

# minimum graph
assert run("""1 0
""") == "0", "single vertex"

# no rhombus
assert run("""3 2
1 2
2 3
""") == "0", "single length-2 path"

# three intermediates
assert run("""5 6
1 2
2 5
1 3
3 5
1 4
4 5
""") == "3", "three choose two"

# two independent rhombi
assert run("""6 8
1 2
2 4
1 3
3 4
1 5
5 6
1 4
4 6
""") == "2", "multiple destinations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex, no edges | 0 | Minimum bounds |
| One length-2 path | 0 | Paths alone are not rhombi |
| Three intermediates to same destination | 3 | Correct use of combinations |
| Two separate rhombi | 2 | Accumulation across destinations |
| Sample case | 1 | Basic correctness |

## Edge Cases

Consider a graph with only one length-2 path:

```
3 2
1 2
2 3
```

For source 1, the algorithm records `cnt[3] = 1`. The contribution is

$$\binom{1}{2}=0.$$

The output is correctly 0 because a rhombus requires two different intermediates.

Consider three different intermediates:

```
5 6
1 2
2 5
1 3
3 5
1 4
4 5
```

The algorithm obtains `cnt[5]=3`. Instead of counting merely one rhombus, it computes

$$\binom{3}{2}=3,$$

which correctly counts all pairs of intermediates.

Consider disconnected components:

```
6 4
1 2
2 3
4 5
5 6
```

Each source generates at most one length-2 path to any destination. Every count remains at most 1, so every contribution is zero. The algorithm naturally handles disconnected graphs without any special cases.

Consider additional edges between the four vertices:

```
4 6
1 2
2 4
1 3
3 4
2 3
3 2
```

The extra edges do not affect the required paths. The algorithm only groups length-2 paths by common start and end vertices. It still finds exactly two such paths from 1 to 4, giving

$$\binom{2}{2}=1.$$

The output remains correct.
