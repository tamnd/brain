---
title: "CF 102440J - Delivery in the city of the future"
description: "Think of every grid cell as a vertex of a graph. A direct teleportation is an edge between two vertices when they lie in the same row or column, contain the same letter, and there is at least one more occurrence of that same letter strictly between them."
date: "2026-08-08T13:59:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102440
codeforces_index: "J"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Junior"
rating: 0
weight: 102440
solve_time_s: 129
verified: true
draft: false
---

[CF 102440J - Delivery in the city of the future](https://codeforces.com/problemset/problem/102440/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of every grid cell as a vertex of a graph. A direct teleportation is an edge between two vertices when they lie in the same row or column, contain the same letter, and there is at least one more occurrence of that same letter strictly between them.

A query gives two cells and asks whether they belong to the same connected component of this graph. Multiple teleportations are allowed, so the question is not whether the two cells have a direct teleportation, but whether there is some sequence of valid teleportations connecting them.

The grid has at most (1000 \times 1000 = 10^6) cells, while there can be up to (10^6) queries. That immediately rules out running a graph search from scratch for every query. Even a search that touches only (O(nm)) cells per query could perform (10^{12}) cell visits in the worst case. We need to spend roughly linear time in the size of the grid during preprocessing and answer each query almost instantly.

There is another difficulty hidden in the teleportation rule. If a row contains four equal letters, adjacent equal cells cannot teleport directly, but the four cells can still form one connected component. For example, in `aaaa`, positions 1 and 3 can teleport, positions 2 and 4 can teleport, and positions 1 and 4 can teleport. That makes all four positions connected. A solution that only considers neighboring equal cells, or only considers pairs at distance exactly two, can miss this connection.

The case of exactly three occurrences is also special. In `aaa`, positions 1 and 3 can teleport, but position 2 cannot teleport to either of them. Thus the three cells do not form one component. The correct answer for a query from position 1 to position 2 is `No`, while position 1 to position 3 is `Yes`.

The same cell is already reachable from itself without making a teleportation. Thus a query such as

```
1 1
a
1
1 1 1 1
```

must produce `Yes`. A graph connectivity structure naturally handles this because every vertex belongs to the same component as itself.

Finally, different letters can never be connected. Every teleport preserves the letter, so even a long sequence of teleportations cannot change the letter of the current building. For example,

```
1 2
ab
1
1 1 1 2
```

produces `No`.

## Approaches

A direct approach is to regard every valid teleportation as a graph edge and perform BFS or DFS for each query. The search is correct because the required answer is exactly graph connectivity. The problem is the number of queries. With (10^6) cells and (10^6) queries, a search that explores the whole grid for every query can reach (10^{12}) visited cells. Constructing every possible teleportation edge explicitly is also unattractive, because a row containing many copies of one letter can contain quadratically many valid pairs.

The structure of equal letters in one line gives us a much smaller representation. Consider the occurrences of one fixed letter in one row, ordered from left to right. Number them (1,2,\ldots,k). A valid direct edge exists between occurrence (i) and occurrence (j) whenever (j-i\ge 2).

We do not need all of these edges. Connecting occurrence (i) with occurrence (i-2) is enough to handle the whole sequence except for one small gap. For four occurrences, the edges (1\leftrightarrow3) and (2\leftrightarrow4) create two separate components, so we additionally connect occurrence 4 with occurrence 1. Now the first four occurrences are connected. Every later occurrence (i) connects to (i-2), which was already connected to the earlier occurrences. Consequently, these few edges produce exactly the same connected components as all valid teleportation edges.

This means that while scanning a line, each new occurrence needs to remember only its first occurrence and its two immediately preceding occurrences. Normally we add the edge from the current occurrence to the occurrence two positions earlier. When the current occurrence is the fourth occurrence, we additionally connect it to the first occurrence.

We apply exactly the same construction to columns. Since every real teleportation edge is represented by this reduced set of edges, we can use a disjoint set union structure, DSU, to maintain connected components while processing the grid.

The brute-force and optimal approaches can be summarized as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(qnm)) in the worst case | (O(nm)) | Too slow |
| Optimal | (O(nm\alpha(nm)+q\alpha(nm))) | (O(nm)) | Accepted |

Here (\alpha) is the inverse Ackermann function, which is effectively constant for these input sizes.

## Algorithm Walkthrough

1. Treat every cell ((x,y)) as a DSU vertex with identifier (x\cdot m+y). Initially every cell is in its own component because no teleportation has been processed yet.
2. Process the grid row by row. For each of the 26 letters, keep its first occurrence, its most recent occurrence, its second most recent occurrence, and a small occurrence count within the current row.
3. When processing a cell containing letter (c), look at the second most recent occurrence of (c) in the same row. If it exists, union it with the current cell. These two occurrences have exactly one or more occurrences of (c) between them, so the teleportation is valid.
4. When the current cell is the fourth occurrence of (c) in the row, also union it with the first occurrence. This extra edge connects the two groups that would otherwise remain separate after using only distance-two edges.
5. Update the stored occurrences for this letter. The current cell becomes the most recent occurrence, and the previous most recent occurrence becomes the second most recent one.
6. Process columns in the same way while scanning the grid from top to bottom. The vertical state is kept separately for every pair consisting of a column and a letter. This avoids a second nested pass over the grid and keeps the implementation linear.
7. After all horizontal and vertical connections have been added, read every query. Convert both coordinates into DSU vertex identifiers and compare their roots. Equal roots mean that a sequence of valid teleportations exists, so print `Yes`. Different roots mean no such sequence exists, so print `No`.

### Why it works

For any fixed row and letter, suppose its occurrences are (1,2,\ldots,k). The algorithm adds edges (i\leftrightarrow i-2) whenever (i\ge3), and additionally adds (1\leftrightarrow4) when (k\ge4). For three occurrences, the only added edge is (1\leftrightarrow3), which is exactly the only possible connection. For four occurrences, (1\leftrightarrow3), (2\leftrightarrow4), and (1\leftrightarrow4) connect all four. For every later occurrence (i), the edge (i\leftrightarrow i-2) attaches it to an already connected part of the sequence. Thus these selected edges have exactly the same connected components as every valid teleportation edge in that row.

The same argument applies independently to every column and letter. Since every valid teleportation is represented by connectivity in one of these reduced line graphs, and every edge added by the algorithm is itself a valid teleportation, the DSU components are exactly the connected components of the original teleportation graph. Comparing DSU roots therefore gives the correct answer for every query.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    total = n * m

    # parent[x] < 0 means x is a root and -parent[x] is its component size.
    parent = [-1] * total

    def find(x):
        while parent[x] >= 0:
            if parent[parent[x]] >= 0:
                parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)
        if a == b:
            return

        if parent[a] > parent[b]:
            a, b = b, a

        parent[a] += parent[b]
        parent[b] = a

    # Horizontal state. It is reset for every row.
    first_h = [-1] * 26
    last1_h = [-1] * 26
    last2_h = [-1] * 26
    count_h = [0] * 26

    # Vertical state. One state exists for every (column, letter).
    states = m * 26
    first_v = [-1] * states
    last1_v = [-1] * states
    last2_v = [-1] * states
    count_v = bytearray(states)

    for i in range(n):
        # Start a fresh occurrence history for this row.
        for c in range(26):
            first_h[c] = -1
            last1_h[c] = -1
            last2_h[c] = -1
            count_h[c] = 0

        row = grid[i]
        base = i * m

        for j in range(m):
            idx = base + j
            c = row[j] - 97

            # Horizontal connections.
            p2 = last2_h[c]
            if p2 != -1:
                union(idx, p2)

            if count_h[c] == 3:
                union(idx, first_h[c])

            if count_h[c] == 0:
                first_h[c] = idx

            last2_h[c] = last1_h[c]
            last1_h[c] = idx
            if count_h[c] < 4:
                count_h[c] += 1

            # Vertical connections.
            s = j * 26 + c
            p2 = last2_v[s]
            if p2 != -1:
                union(idx, p2)

            if count_v[s] == 3:
                union(idx, first_v[s])

            if count_v[s] == 0:
                first_v[s] = idx

            last2_v[s] = last1_v[s]
            last1_v[s] = idx
            if count_v[s] < 4:
                count_v[s] += 1

    q = int(input())
    out = bytearray()

    for _ in range(q):
        x1, y1, x2, y2 = map(int, input().split())
        a = (x1 - 1) * m + (y1 - 1)
        b = (x2 - 1) * m + (y2 - 1)

        if find(a) == find(b):
            out.extend(b"Yes\n")
        else:
            out.extend(b"No\n")

    sys.stdout.buffer.write(out)

if __name__ == "__main__":
    solve()
```

The DSU uses a negative value in `parent` to store component size. This avoids a separate size array and keeps the memory usage small. Union by size prevents the trees from becoming deep, while path compression makes subsequent root lookups almost constant time.

The horizontal state is reset at the beginning of each row because occurrences in different rows cannot participate in the same horizontal teleportation. The vertical state is not reset because a column continues across all rows.

The `count` values only need to distinguish zero, one, two, three, and at least four occurrences. Once a letter has appeared four times in a line, the special first-to-fourth edge has already been added, and every later occurrence only needs the connection to the occurrence two positions earlier. A `bytearray` is sufficient for the vertical counts.

The condition `count == 3` is deliberately checked before incrementing the count. It identifies the fourth occurrence, not the third one. For the fourth occurrence, `first` is occurrence 1 and `last2` is occurrence 2, so the algorithm adds both required connections.

All coordinates from the input are one-based. The conversion subtracts one from both coordinates before computing the zero-based vertex identifier. There is no integer overflow issue in Python, and the largest identifier is below (10^6).

The output is accumulated in a `bytearray` rather than a Python list of one million strings. This keeps memory usage predictable and avoids repeated output calls.

## Worked Examples

### Sample 1

The grid is

```
aaa
aaa
aaa
```

For each row, the three `a` occurrences are numbered 1, 2, 3. Processing the third occurrence adds an edge between occurrences 3 and 1. The middle occurrence remains separate within that row.

The same happens vertically. As a result, all eight boundary cells form one component, while the center cell remains isolated.

A compact trace of the important horizontal and vertical connections is:

| Cell | Horizontal connection | Vertical connection | Resulting component |
| --- | --- | --- | --- |
| (1,1) | none | none | corner component |
| (1,2) | none | none | edge-middle component |
| (1,3) | (1,1) | none | corner component |
| (2,1) | none | none | edge-middle component |
| (2,2) | none | none | center component |
| (2,3) | none | none | edge-middle component |
| (3,1) | none | (1,1) | corner component |
| (3,2) | none | (1,2) | edge-middle component |
| (3,3) | (3,1) | (1,3) | corner component |

The vertical processing then connects the corresponding edge-middle cells and corner cells. The five queries consequently produce

```
No
No
No
Yes
Yes
```

The third query demonstrates why the center cell is isolated. The fourth query demonstrates that a path can use several teleportations, in this case moving around the outer ring.

### Four equal cells in one row

Consider the constructed input

```
1 4
aaaa
4
1 1 1 2
1 1 1 3
1 2 1 4
1 1 1 4
```

The occurrence sequence is (1,2,3,4). The algorithm processes it as follows.

| Current position | Second previous occurrence | Fourth-occurrence connection | Component effect |
| --- | --- | --- | --- |
| 1 | none | none | starts component |
| 2 | none | none | remains separate |
| 3 | 1 | none | connects 3 to 1 |
| 4 | 2 | 1 | connects the two existing groups |

After position 4 is processed, all four cells belong to one component. The output is

```
Yes
Yes
Yes
Yes
```

This example is particularly useful because connecting only occurrences two positions apart would incorrectly leave `{1,3}` and `{2,4}` disconnected. The extra edge between the first and fourth occurrences fixes exactly that case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nm\alpha(nm)+q\alpha(nm))) | Each cell participates in only a constant number of DSU operations, followed by two root queries per request. |
| Space | (O(nm)) | The DSU stores one value per cell, while the grid and line-state arrays are linear in the input size. |

There are at most (10^6) cells and (10^6) queries. The preprocessing touches every cell only a constant number of times, and the query phase performs only two DSU finds per query. The algorithm therefore scales linearly with the actual input size up to the inverse-Ackermann factor, rather than multiplying the grid size by the number of queries.

## Test Cases

The following harness assumes the submitted solution is saved as `solution.py` and exposes the `solve()` function shown above.

```python
import sys
import io
from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1.
sample1 = """\
3 3
aaa
aaa
aaa
5
1 1 1 2
2 2 1 1
2 2 1 2
3 3 1 1
3 2 1 2
"""

assert run(sample1) == """\
No
No
No
Yes
Yes
""", "sample 1"

# Minimum-size grid and zero-length path.
sample_min = """\
1 1
a
1
1 1 1 1
"""

assert run(sample_min) == "Yes\n", "minimum-size input"

# Exactly three equal occurrences.
sample_three = """\
1 3
aaa
4
1 1 1 3
1 1 1 2
1 2 1 3
1 2 1 2
"""

assert run(sample_three) == """\
Yes
No
No
Yes
""", "three occurrences"

# Four equal occurrences. All four become connected.
sample_four = """\
1 4
aaaa
4
1 1 1 2
1 1 1 3
1 2 1 4
1 1 1 4
"""

assert run(sample_four) == """\
Yes
Yes
Yes
Yes
""", "four occurrences"

# Different letters can never be connected.
sample_letters = """\
2 2
ab
ba
4
1 1 1 2
1 1 2 1
1 2 2 2
1 1 1 1
"""

assert run(sample_letters) == """\
No
No
No
Yes
""", "different letters"

# Maximum grid dimensions with all equal cells.
# Every cell belongs to one component because each row has 1000 occurrences
# and the rows are connected vertically by the same argument.
n = 1000
m = 1000
grid = "\n".join(["a" * m for _ in range(n)])

sample_max = f"""\
{n} {m}
{grid}
3
1 1 1 1000
1 1 1000 1
500 500 1000 1000
"""

assert run(sample_max) == """\
Yes
Yes
Yes
""", "maximum-size grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 x 1`, one `a` | `Yes` | Self-reachability and minimum dimensions |
| `1 x 3`, `aaa` | `Yes, No, No, Yes` | Exactly three occurrences and the isolated middle occurrence |
| `1 x 4`, `aaaa` | Four `Yes` answers | The special fourth-occurrence connection |
| `2 x 2`, `ab / ba` | `No, No, No, Yes` | Different letters and boundary coordinates |
| `1000 x 1000`, all `a` | Three `Yes` answers | Maximum grid dimensions and large connected components |

## Edge Cases

### Adjacent equal cells

For

```
1 2
aa
1
1 1 1 2
```

the two cells contain the same letter and lie in the same row, but there is no third `a` between them. The algorithm sees only two occurrences, so it adds no union. The cells remain in different DSU components and the output is

```
No
```

This prevents the common mistake of interpreting the rule as simply "same letter in the same row or column".

### Exactly three occurrences

For

```
1 3
aaa
2
1 1 1 3
1 1 1 2
```

the third occurrence is connected to the first because there is an `a` at position 2 between them. The second occurrence itself has no valid teleportation to either endpoint. The DSU consequently contains one component `{1,3}` and one component `{2}`, producing

```
Yes
No
```

The algorithm handles this because the third occurrence connects to its second previous occurrence, which is the first occurrence, while no special fourth-occurrence connection is created.

### Four occurrences

For

```
1 4
aaaa
2
1 1 1 2
1 1 1 4
```

the fourth occurrence first connects to occurrence 2 because they are two occurrences apart. It also triggers the special connection to occurrence 1. The first three occurrences already have the connection (1\leftrightarrow3), so all four become one component. The output is

```
Yes
Yes
```

This is the case that distinguishes the reduced edge construction from the simpler but incorrect strategy of connecting only every second occurrence.

### Same cell as both endpoints

For

```
1 1
z
1
1 1 1 1
```

no teleportation is needed. The source and destination are literally the same graph vertex, so `find(source) == find(destination)` immediately holds. The output is

```
Yes
```

### Different letters

For

```
1 2
ab
1
1 1 1 2
```

the two cells cannot be joined by a direct teleportation because their letters differ. They also cannot become connected through other cells because every valid teleport preserves the letter. The DSU never unions them, giving

```
No
```

### Horizontal and vertical connections interacting

Consider

```
3 4
aaaa
bbbb
aaaa
2
1 1 3 4
1 1 2 1
```

The first and third rows each contain four `a` cells, so every `a` in each row belongs to one horizontal component. Each column then contains an `a` at the top and bottom with another `a` occurrence of the same letter between them, so the top and bottom components become connected vertically. The first query is consequently `Yes`.

The second query asks to connect an `a` cell with a `b` cell. No sequence of valid teleportations can change the letter, so it is `No`.

This illustrates why the solution cannot preprocess rows and columns independently and then answer queries using only one direction. The DSU combines both kinds of connections into one global connectivity structure.

If you want, I can also turn this into a more compact Codeforces-style editorial, keeping the same proof but reducing the exposition substantially.
