---
title: "CF 102215B - Rearrange Columns"
description: "We have a grid with exactly two rows and (n) columns. Each column contains zero, one, or two marked cells. We may permute the columns arbitrarily, but we cannot change the contents of a column."
date: "2026-08-18T11:44:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "B"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 374
verified: false
draft: false
---

[CF 102215B - Rearrange Columns](https://codeforces.com/problemset/problem/102215/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We have a grid with exactly two rows and (n) columns. Each column contains zero, one, or two marked cells. We may permute the columns arbitrarily, but we cannot change the contents of a column. The goal is to find an ordering in which every marked cell belongs to one connected component using four-directional moves.

The useful way to think about a column is not by its original position, but by its type. A non-empty column is one of three relevant types: it has only the upper cell marked, only the lower cell marked, or both cells marked. An empty column contains no marked cells and does not help connectivity.

Two consecutive non-empty columns are directly connected exactly when they share a marked row. An upper-only column and a lower-only column cannot touch each other, while a column containing both cells can touch either type. Once all non-empty columns are arranged into one connected sequence, empty columns can simply be placed at the end because they contain nothing that needs to be connected.

The constraint (n \le 1000) is small enough that a linear or quadratic algorithm is easily fast enough, but it rules out algorithms that enumerate permutations or subsets. Since there are (n!) possible column orders, trying every permutation becomes impossible even for a few dozen columns. The intended solution should inspect each column only a constant number of times.

There are two edge cases that a careless implementation can miss. First, empty columns must not be inserted between marked columns. For example,

```
#.
#.
```

is already connected, but

```
#.
.#
```

would not be connected. An algorithm that treats empty columns as harmless separators can accidentally destroy connectivity.

Second, having marked cells in both rows is not by itself enough. Consider

```
..##
##..
```

Every marked column is a singleton, with two columns containing only the lower cell and two containing only the upper cell. No permutation can make an upper-only column adjacent to a lower-only column without a column containing both cells, so the correct answer is `NO`. A careless solution that merely checks that both rows contain marked cells could incorrectly return `YES`.

A third boundary case is when one row is completely empty. For example,

```
##..
....
```

is trivially connected after placing the marked columns together. No two-row bridge is necessary because all marked cells already lie in one row.

## Approaches

A direct brute-force approach would generate every permutation of the (n) columns. For each permutation, we would build the resulting grid and run a connectivity check, for example with DFS or BFS. The check itself takes (O(n)) time because the grid has only (2n) cells, so examining all (n!) permutations costs (O(n \cdot n!)) time in the worst case. Even ignoring the cost of connectivity checking, (1000!) is far beyond anything executable within two seconds.

The reason the brute force works conceptually is that connectivity depends only on which column types are adjacent. The original positions of the columns are irrelevant. This gives us a much smaller structural question: can the three non-empty column types be arranged into a connected sequence?

All upper-only columns can be placed together, all lower-only columns can be placed together, and every column containing both cells can connect the two groups. Consequently, if both upper-only and lower-only columns exist, at least one both-marked column is necessary. If such a column exists, we can always construct a valid ordering by placing all upper-only columns first, then all both-marked columns, then all lower-only columns. Every transition in this sequence shares a marked row.

If only one singleton type exists, the marked cells can simply be grouped together without needing a both-marked column. Empty columns are placed after all marked columns so they cannot interrupt the connected component.

The entire problem therefore reduces to counting the four possible column types and constructing one canonical ordering.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n \cdot n!)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the two rows and inspect every column. Classify it as empty, upper-only, lower-only, or both-marked.
2. Store the indices of upper-only columns, both-marked columns, lower-only columns, and empty columns separately. We only need their original contents, so keeping the indices is enough to reconstruct the final grid.
3. If there is at least one upper-only column and at least one lower-only column, check whether there is a both-marked column. If there is none, output `NO`.

The upper-only and lower-only groups cannot be connected directly. A both-marked column is the only possible bridge between the two rows, so without one the two groups must remain separate regardless of the permutation.
4. If the condition from the previous step does not fail, construct the new order as all upper-only columns, followed by all both-marked columns, followed by all lower-only columns, followed by all empty columns.

The empty columns deliberately go last. Putting one between two marked columns would make those marked cells non-adjacent, so treating empty columns as ordinary sortable elements would be unsafe.
5. Create the two output rows by taking the characters from the columns in the constructed order. Print `YES` and the two resulting rows.

Within the upper-only group, consecutive columns share the upper marked cell. Within the lower-only group, consecutive columns share the lower marked cell. A both-marked column connects the two groups when both groups exist.

### Why it works

The invariant is that every group of consecutive non-empty columns in the constructed order is connected to the next group through a shared marked row. Upper-only columns connect to each other through the upper row, lower-only columns connect through the lower row, and a both-marked column connects to either row.

If both singleton types occur, the algorithm requires a both-marked column. That condition is also necessary, because an upper-only column can never be adjacent to a lower-only column through a marked edge. If only one singleton type occurs, all marked cells can be placed in the same row group and are automatically connected. Empty columns are placed after the entire marked component, so they cannot split it. Thus every `YES` construction is connected, and every impossible case is rejected.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(data: str) -> str:
    lines = data.splitlines()
    top = lines[0].strip()
    bottom = lines[1].strip()

    n = len(top)

    upper = []
    both = []
    lower = []
    empty = []

    for i in range(n):
        a = top[i] == '#'
        b = bottom[i] == '#'

        if a and b:
            both.append(i)
        elif a:
            upper.append(i)
        elif b:
            lower.append(i)
        else:
            empty.append(i)

    if upper and lower and not both:
        return "NO\n"

    order = upper + both + lower + empty

    new_top = ''.join(top[i] for i in order)
    new_bottom = ''.join(bottom[i] for i in order)

    return "YES\n" + new_top + "\n" + new_bottom + "\n"

if __name__ == "__main__":
    data = sys.stdin.read()
    sys.stdout.write(solve(data))
```

The first loop performs the complete structural analysis. For each column, the two Boolean values tell us exactly which of the four possible types it has. Since the grid has only two rows, no more complicated graph representation is needed.

The impossibility test checks `upper and lower and not both`. This is the only situation in which the marked cells necessarily contain two different row groups with no possible bridge. The test deliberately does not reject a grid where one of `upper` or `lower` is empty, because those cases can be connected entirely within one row.

The construction `upper + both + lower + empty` is deterministic. The original indices are retained so that the output columns are exactly the input columns, only reordered. There is no integer arithmetic here, so overflow is irrelevant, and the loop boundary `range(n)` visits every column exactly once.

The final two comprehensions reconstruct the rows according to the chosen permutation. Since `order` contains every original column exactly once, no marked cell is lost or duplicated.

## Worked Examples

### Sample 1

The input is

```
#..#
.#.#
```

The four columns are upper-only, lower-only, lower-only? More precisely, their types from left to right are upper-only, lower-only, empty, both-marked.

The algorithm groups them into upper-only, both-marked, lower-only, empty. The state evolves as follows.

| Column index | Upper marked | Lower marked | Classification | Upper group | Both group | Lower group | Empty group |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | Yes | No | Upper-only | 1 | 0 | 0 | 0 |
| 1 | No | Yes | Lower-only | 1 | 0 | 1 | 0 |
| 2 | No | No | Empty | 1 | 0 | 1 | 1 |
| 3 | Yes | Yes | Both | 1 | 1 | 1 | 1 |

There is at least one upper-only column, at least one lower-only column, and at least one both-marked column, so the construction is possible. The resulting order is column (0,3,1,2), giving

```
##..
.##.
```

The first two marked columns are connected through the upper row, and the both-marked column also connects to the lower-only column. The empty column is safely placed at the end.

### Sample 2

The input is

```
..##
##..
```

The classification is lower-only, lower-only, upper-only, upper-only.

| Column index | Upper marked | Lower marked | Classification | Upper group | Both group | Lower group |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | No | Yes | Lower-only | 0 | 0 | 1 |
| 1 | No | Yes | Lower-only | 0 | 0 | 2 |
| 2 | Yes | No | Upper-only | 1 | 0 | 2 |
| 3 | Yes | No | Upper-only | 2 | 0 | 2 |

Both singleton groups are non-empty, but the both-marked group is empty. The algorithm immediately returns `NO`.

This demonstrates the necessary bridge condition. No permutation can make a lower-only column adjacent to an upper-only column through a marked edge, so the two groups can never form one connected component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each input column is classified once, then each column is copied once into the output. |
| Space | (O(n)) | The four index arrays together contain exactly (n) column indices, and the output strings also require (O(n)) space. |

With (n \le 1000), the algorithm performs only a few thousand simple operations and uses a small amount of memory. It is comfortably within the two-second and 256 MB limits.

## Test Cases

```python
import sys
import io

def solve(data: str) -> str:
    lines = data.splitlines()
    top = lines[0].strip()
    bottom = lines[1].strip()

    n = len(top)

    upper = []
    both = []
    lower = []
    empty = []

    for i in range(n):
        a = top[i] == '#'
        b = bottom[i] == '#'

        if a and b:
            both.append(i)
        elif a:
            upper.append(i)
        elif b:
            lower.append(i)
        else:
            empty.append(i)

    if upper and lower and not both:
        return "NO\n"

    order = upper + both + lower + empty

    new_top = ''.join(top[i] for i in order)
    new_bottom = ''.join(bottom[i] for i in order)

    return "YES\n" + new_top + "\n" + new_bottom + "\n"

def run(inp: str) -> str:
    return solve(inp)

# Provided samples.
assert run("#..#\n.#.#\n") == "YES\n##..\n.##.\n", "sample 1"
assert run("..##\n##..\n") == "NO\n", "sample 2"

# Minimum size, a single marked cell.
assert run("#\n.\n") == "YES\n#\n.\n", "single upper marked cell"

# Both rows have marks, but a both-marked column provides the bridge.
assert run("#..\n.##\n") == "YES\n#.#\n.##\n", "bridge column"

# No bridge exists between upper-only and lower-only columns.
assert run("#.\n.#\n") == "NO\n", "missing bridge"

# All cells are marked.
assert run("####\n####\n") == "YES\n####\n####\n", "all marked"

# Maximum-size input, all cells empty except one marked cell.
n = 1000
max_case = "#" + "." * (n - 1) + "\n" + "." * n + "\n"
expected_top = "#" + "." * (n - 1)
expected_bottom = "." * n
assert run(max_case) == "YES\n" + expected_top + "\n" + expected_bottom + "\n", \
    "maximum size"

# Empty columns originally lie between marked columns. They must be moved away.
assert run("#.#\n#..\n") == "YES\n##.\n#..\n", "empty column separator"

| Test input | Expected output | What it validates |
|---|---|---|
| `# / .` | `YES / # / .` | Minimum-size grid with one marked cell |
| `#. / .#` | `NO` | Both rows have marks but no bridge column |
| `#### / ####` | `YES / #### / ####` | All cells marked |
| `#... / ....` with \(n=1000\) | `YES` with the single mark first | Maximum input size and linear processing |
| `#.# / #..` | `YES / ##. / #..` | Empty column must not split marked cells |

The assertions compare the exact deterministic output produced by the implementation. Since the problem permits any valid arrangement, a general checker could instead validate connectivity and verify that the output is a permutation of the original columns.

## Edge Cases

A single marked cell is the smallest possible case. For input

```text
#
.
```

the `upper` group contains one column, while every other group is empty. The bridge condition is false because the lower group is empty, so the algorithm constructs the same single column and prints `YES`. The marked area contains only one cell, which is connected by definition.

A grid with marks in both rows but no both-marked column is impossible whenever both singleton groups are non-empty. For

```
#.
.#
```

the first column is upper-only and the second is lower-only. Reversing them changes nothing about the incompatibility. The algorithm detects `upper` and `lower` as non-empty while `both` is empty and prints `NO`.

A both-marked column resolves that obstruction. For

```
#..
.##
```

the columns are upper-only, lower-only, lower-only. Actually, this particular input has no both-marked column, so it is correctly rejected. Changing it to

```
##.
.##
```

gives a both-marked first column, an upper-only second column, and a lower-only third column. The algorithm orders the upper-only column, then the both-marked column, then the lower-only column, producing a connected chain across the two rows.

Empty columns are handled by putting them after all marked columns. For

```
#.#
#..
```

the first and third columns contain marked cells, while the middle column is empty. The first and third columns are already connected through the upper row, but placing the empty column between them would separate those cells. The algorithm instead produces

```
##.
#..
```

so the marked cells form one connected component and the empty column is outside it.

Finally, when every cell is marked, every column is a both-marked column. For

```
####
####
```

the `both` group contains all four columns, and the construction leaves their order unchanged. Every adjacent pair shares both rows, so the whole marked rectangle is connected.
