---
title: "CF 1950G - Shuffling Songs"
description: "Each song has two attributes, a genre and a writer. After removing some songs, we are allowed to reorder the remaining songs arbitrarily."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dfs-and-similar", "dp", "graphs", "hashing", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1950
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 937 (Div. 4)"
rating: 1900
weight: 1950
solve_time_s: 82
verified: true
draft: false
---

[CF 1950G - Shuffling Songs](https://codeforces.com/problemset/problem/1950/G)

**Rating:** 1900  
**Tags:** bitmasks, dfs and similar, dp, graphs, hashing, implementation, strings  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

Each song has two attributes, a genre and a writer. After removing some songs, we are allowed to reorder the remaining songs arbitrarily. The goal is to arrange them so that every pair of neighboring songs shares at least one attribute: either the same genre, the same writer, or both.

We want to remove as few songs as possible. Equivalently, we want to keep as many songs as possible and find whether those songs can be ordered into a valid sequence.

A useful way to view the problem is as a graph. Create one vertex for each song. Connect two songs if they have the same genre or the same writer. Then an exciting playlist is exactly an ordering of songs where every consecutive pair is connected by an edge.

That means we are looking for the largest subset of vertices that can be arranged as a path visiting every chosen vertex exactly once. In graph terms, we want the size of the largest Hamiltonian path contained in the graph. The answer is:

$$n - (\text{maximum number of songs that can appear in such a path})$$

The constraints reveal the intended approach. The number of songs is at most 16, which is extremely small. A solution exponential in $n$ is possible. The statement even gives a strong hint: the sum of $2^n$ over all test cases does not exceed $2^{16}$. This is a classic setup for subset dynamic programming.

The long string lengths do not matter algorithmically. We only compare genres and writers for equality. Once the strings are read, each pair of songs can be checked independently.

Several edge cases are easy to mishandle.

Consider a single song:

```
1
pop taylor
```

The correct answer is 0. A path consisting of one vertex is already valid. Implementations that require at least one edge in the path would incorrectly return 1.

Consider three completely unrelated songs:

```
3
a x
b y
c z
```

No two songs can be adjacent. The largest valid playlist contains exactly one song, so the answer is 2. A careless implementation might assume that every connected component contributes all its vertices.

Consider a graph where the best solution does not use all vertices from a connected component:

```
4
a x
a y
b y
c z
```

Songs 1, 2, and 3 form a chain, while song 4 is isolated. The optimal playlist keeps songs 1, 2, and 3. The answer is 1. Connectivity alone is not enough; we need an actual Hamiltonian path on the chosen subset.

## Approaches

The most direct brute-force idea is to try every subset of songs and every ordering inside that subset. For a subset of size $k$, there are $k!$ possible orders. In the worst case, this becomes

$$\sum_{k=0}^{n} \binom{n}{k} k!$$

which is already enormous for $n=16$. Even checking all permutations of 16 songs requires roughly $2 \times 10^{13}$ orders, completely infeasible.

The reason brute force works conceptually is that the property we care about depends only on consecutive songs in an ordering. The challenge is avoiding enumeration of all possible orderings.

The key observation is that the graph has only 16 vertices. Whenever a problem asks whether a subset of vertices can be arranged into a path, a Hamiltonian-path style bitmask DP becomes natural.

Let `dp[mask][last]` mean:

"Using exactly the vertices in `mask`, is there a valid path whose final vertex is `last`?"

If such a path exists, we can append another vertex `nxt` whenever there is an edge between `last` and `nxt`.

This transforms permutation enumeration into dynamic programming over subsets. Each state represents many possible orderings at once.

The largest subset size for which some state is reachable gives the maximum number of songs we can keep.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Optimal Bitmask DP | $O(2^n \cdot n^2)$ | $O(2^n \cdot n)$ | Accepted |

## Algorithm Walkthrough

1. Read all songs.
2. Build an undirected graph on the songs.

Connect songs `i` and `j` if they share a genre or share a writer.
3. Create a DP table `dp[mask][last]`.

`dp[mask][last] = True` means there exists a valid path using exactly the vertices in `mask` and ending at `last`.
4. Initialize all singleton subsets.

For every song `i`:

`dp[1<<i][i] = True`

A single song is always a valid path.
5. Iterate through all masks.

For every reachable state `(mask, last)`, try extending the path.
6. For every vertex `nxt` not already in `mask`, check whether there is an edge between `last` and `nxt`.

If there is, mark:

`dp[mask | (1<<nxt)][nxt] = True`

This corresponds to appending `nxt` to the end of the existing path.
7. Whenever a state is reachable, update the maximum path length using the number of set bits in `mask`.
8. After processing all states, let `best` be the largest reachable subset size.
9. Output `n - best`.

### Why it works

The DP state stores exactly the information needed to extend a path: which vertices have already been used and which vertex is currently at the end.

The initialization covers all paths of length one.

Every transition appends a new vertex connected to the current endpoint, so every generated path is valid.

Conversely, any valid path can be reconstructed by repeatedly removing its last vertex. Starting from the first vertex, the DP will reproduce every valid path through these extensions.

Because every valid path corresponds to some reachable DP state and every reachable DP state corresponds to a valid path, the DP enumerates precisely all possible valid playlists. The largest reachable subset size is exactly the maximum number of songs that can be kept.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())

        genre = []
        writer = []

        for _ in range(n):
            g, w = input().split()
            genre.append(g)
            writer.append(w)

        adj = [[False] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                if genre[i] == genre[j] or writer[i] == writer[j]:
                    adj[i][j] = adj[j][i] = True

        m = 1 << n
        dp = [[False] * n for _ in range(m)]

        best = 1

        for i in range(n):
            dp[1 << i][i] = True

        for mask in range(m):
            length = mask.bit_count()

            for last in range(n):
                if not dp[mask][last]:
                    continue

                if length > best:
                    best = length

                for nxt in range(n):
                    if mask & (1 << nxt):
                        continue

                    if adj[last][nxt]:
                        dp[mask | (1 << nxt)][nxt] = True

        print(n - best)

solve()
```

The graph construction follows directly from the adjacency rule in the statement. Two songs are connected exactly when they may appear next to each other.

The DP table stores reachability rather than path length. Reachability is sufficient because every state already uniquely determines how many vertices are used through the bitmask.

The singleton initialization is essential. Without it, paths consisting of one song would never exist, causing incorrect answers for isolated vertices.

The transition always appends a new unused vertex. Since the bitmask records all used vertices, no vertex can appear twice in the same path.

The variable `best` tracks the largest reachable subset encountered anywhere in the DP. We do not require the path to end at a specific vertex, so every reachable endpoint is considered.

## Worked Examples

### Example 1

Input:

```
4
electronic themotans
electronic carlasdreams
pop themotans
pop irinarimes
```

Graph edges:

| Pair | Connected? |
| --- | --- |
| 1-2 | Same genre |
| 1-3 | Same writer |
| 2-4 | No |
| 3-4 | Same genre |

A valid path is:

```
4 -> 3 -> 1 -> 2
```

DP evolution:

| Mask | Last | Reachable |
| --- | --- | --- |
| 0001 | 1 | Yes |
| 0101 | 3 | Yes |
| 0111 | 2 | Yes |
| 1111 | 4 | Yes |

The largest reachable subset has size 4, so:

| Quantity | Value |
| --- | --- |
| n | 4 |
| best | 4 |
| answer | 0 |

This example shows that the order can be completely rearranged. We are not restricted by the original playlist order.

### Example 2

Input:

```
4
a b
c d
e f
g h
```

No songs share a genre or writer.

Graph:

| Vertex | Neighbors |
| --- | --- |
| 1 | None |
| 2 | None |
| 3 | None |
| 4 | None |

Reachable states:

| Mask | Size |
| --- | --- |
| 0001 | 1 |
| 0010 | 1 |
| 0100 | 1 |
| 1000 | 1 |

No larger masks become reachable.

| Quantity | Value |
| --- | --- |
| n | 4 |
| best | 1 |
| answer | 3 |

This demonstrates that an isolated song still forms a valid playlist of length one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(2^n \cdot n^2)$ | Every state tries all possible next vertices |
| Space | $O(2^n \cdot n)$ | DP table over masks and endpoints |

With $n \le 16$, we have at most $2^{16} = 65536$ masks. The resulting number of operations is comfortably within the limits. The memory usage is also small, roughly one million boolean states.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = []

    t = int(input())

    for _ in range(t):
        n = int(input())

        genre = []
        writer = []

        for _ in range(n):
            g, w = input().split()
            genre.append(g)
            writer.append(w)

        adj = [[False] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                if genre[i] == genre[j] or writer[i] == writer[j]:
                    adj[i][j] = adj[j][i] = True

        m = 1 << n
        dp = [[False] * n for _ in range(m)]

        best = 1

        for i in range(n):
            dp[1 << i][i] = True

        for mask in range(m):
            for last in range(n):
                if not dp[mask][last]:
                    continue

                best = max(best, mask.bit_count())

                for nxt in range(n):
                    if (mask & (1 << nxt)) == 0 and adj[last][nxt]:
                        dp[mask | (1 << nxt)][nxt] = True

        out.append(str(n - best))

    return "\n".join(out)

# provided samples
assert run(
"""4
1
pop taylorswift
4
electronic themotans
electronic carlasdreams
pop themotans
pop irinarimes
7
rap eminem
rap drdre
rap kanyewest
pop taylorswift
indierock arcticmonkeys
indierock arcticmonkeys
punkrock theoffspring
4
a b
c d
e f
g h
"""
) == """0
0
4
3"""

# minimum size
assert run(
"""1
1
a b
"""
) == "0"

# all songs connected by same genre
assert run(
"""1
4
rock a
rock b
rock c
rock d
"""
) == "0"

# completely isolated songs
assert run(
"""1
3
a x
b y
c z
"""
) == "2"

# chain of length 3 plus isolated vertex
assert run(
"""1
4
a x
a y
b y
c z
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single song | 0 | Base case, singleton path |
| All same genre | 0 | Full Hamiltonian path exists |
| All isolated | 2 | Largest path may have size 1 |
| Chain plus isolated vertex | 1 | Best subset need not include all vertices |

## Edge Cases

Consider a single song:

```
1
pop taylor
```

The DP initializes `dp[1][0] = True`. No transitions exist, but the reachable subset size is already 1. Thus `best = 1` and the answer is `1 - 1 = 0`.

Consider completely disconnected songs:

```
3
a x
b y
c z
```

Every singleton mask is reachable. No larger mask can ever be reached because there are no graph edges. The maximum reachable subset size remains 1, giving answer `3 - 1 = 2`.

Consider a connected component that is not fully usable:

```
4
a x
a y
b y
c z
```

The graph contains edges `(1,2)` and `(2,3)`. Vertex 4 is isolated. The DP reaches masks corresponding to the path `1 -> 2 -> 3`, achieving size 3. No state of size 4 becomes reachable. The algorithm correctly reports `4 - 3 = 1`.

This is exactly the kind of situation where checking only connectivity would fail, while the Hamiltonian-path DP remains correct.
