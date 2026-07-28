---
title: "CF 102760D - Fix Wiring"
description: "The installation is a complete graph: every pair of nodes has a wire between them. The only missing information is which tag value belongs to which wire. We receive all tag values, and we must decide two different assignments of these values."
date: "2026-07-28T23:49:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102760
codeforces_index: "D"
codeforces_contest_name: "2020 KAIST 10th ICPC Mock Contest (XXI Open Cup. Grand Prix of Korea. Division 2)"
rating: 0
weight: 102760
solve_time_s: 66
verified: true
draft: false
---

[CF 102760D - Fix Wiring](https://codeforces.com/problemset/problem/102760/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The installation is a complete graph: every pair of nodes has a wire between them. The only missing information is which tag value belongs to which wire. We receive all tag values, and we must decide two different assignments of these values.

The first assignment should make the minimum spanning tree as cheap as possible. The second assignment should make the minimum spanning tree as expensive as possible. The output is the MST cost in both cases.

The number of nodes is at most 100, so the number of wires can reach

$$\frac{100 \cdot 99}{2}=4950$$

which is small enough that we can sort all tags and do linear scans. A solution that tries every possible assignment of tags to wires would be impossible because even 4950! assignments exist. The intended approach has to use the structure of complete graphs instead of exploring individual wires.

The main tricky cases are caused by equal values and by very small graphs. Equal tags cannot be treated as distinct choices because swapping them changes nothing. Small values of `N` are also important because formulas based on groups of vertices must still work when only one or two MST edges exist.

For example, with two nodes there is only one wire.

```
Input
2
10

Output
10 10
```

A careless implementation that assumes there are multiple MST edges could access nonexistent positions.

Another case is when all tags are identical.

```
Input
4
7 7 7 7 7 7

Output
21 21
```

Every possible assignment creates the same MST cost. An approach that tries to force different smallest and largest choices would produce the wrong answer.

A third edge case is a small complete graph where the maximum assignment is not obtained by taking the largest `N - 1` tags.

```
Input
4
3 5 5 8 8 9

Output
13 16
```

The largest three tags sum to 25, but that cannot be forced into the MST. The smaller tags can be hidden inside already connected groups, and the largest possible MST uses tags from specific positions in the sorted order.

## Approaches

A direct solution would try to place every tag on every possible wire and calculate the resulting MST. The MST calculation itself is easy with Kruskal's algorithm, but the number of assignments is factorial in the number of wires. Even for `N = 10`, there are already 45 wires, making this approach completely unusable.

The first observation is that the graph is complete. Because every pair of nodes has a wire, the cheapest MST assignment is simple. We can place the smallest `N - 1` tags on the edges of any tree. Kruskal will select exactly those edges because they already connect all vertices. Every remaining edge can receive a larger value without affecting the MST. The minimum answer is the sum of the first `N - 1` values after sorting.

The maximum case requires a different view. Kruskal processes edges from smallest to largest. The first edge always enters the MST because initially every node is isolated. After that edge connects two nodes, the edge between those two nodes can be made useless by assigning it a small value, because both endpoints are already in the same component.

To delay later MST choices, we want to create one growing connected component. After selecting `i - 1` MST edges, this component has `i` vertices. Inside it there are

$$\frac{i(i-1)}{2}$$

edges, and all of them can appear before the next useful edge without being selected. This means the `i`th MST edge can be placed at position

$$\frac{i(i-1)}{2}+1$$

in the sorted list of tags, using one based indexing.

For example, with four vertices, the maximum MST uses positions:

```
i = 1: position 1
i = 2: position 2
i = 3: position 4
```

For the sample values `3 5 5 8 8 9`, this gives `3 + 5 + 8 = 16`.

The two strategies can be summarized as follows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(M! * M log M) | O(M) | Too slow |
| Optimal | O(M log M) | O(M) | Accepted |

## Algorithm Walkthrough

1. Sort all tag values in nondecreasing order. The order of tags is the only information needed because the MST depends on relative edge weights.
2. Compute the minimum MST cost by adding the first `N - 1` sorted values. These values can always be placed on a spanning tree, forcing Kruskal to choose them.
3. Compute the maximum MST cost by iterating over the first `N - 1` MST edges. For the `i`th chosen edge, add the value at index `i * (i - 1) / 2` in zero based indexing.
4. Print the two accumulated sums.

The maximum construction works because after `i - 1` chosen edges, the best arrangement has one component containing `i` vertices. All edges inside that component can be filled with smaller tags and ignored by Kruskal. The next edge connecting this component to a new vertex appears exactly after all those internal edges have been processed.

Why it works:

For the minimum answer, no MST can contain fewer than `N - 1` edges, and the smallest possible sum of that many tags is achieved by using the smallest `N - 1` tags.

For the maximum answer, every MST edge must connect two different components at the moment Kruskal chooses it. The first useful edge can only appear after zero internal edges, the second after one internal edge, the third after three internal edges, and so on. Growing a single component maximizes the number of edges that can be hidden before each MST edge. The positions produced by the formula are exactly the latest possible positions, so the resulting sum is the largest achievable MST cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    c = list(map(int, input().split()))
    c.sort()

    mn = sum(c[:n - 1])

    mx = 0
    for i in range(1, n):
        idx = i * (i - 1) // 2
        mx += c[idx]

    print(mn, mx)

if __name__ == "__main__":
    solve()
```

The input contains exactly one test case, so the solution only needs one execution path.

After sorting, the minimum calculation takes the first `n - 1` entries. The slicing is safe because a tree on `n` vertices always has exactly `n - 1` edges.

For the maximum calculation, the loop variable `i` represents the number of vertices already inside the growing component before adding the next MST edge. The zero based index `i * (i - 1) // 2` is the same as the one based position `i * (i - 1) / 2 + 1`.

Python integers do not overflow, which matters because tag values can be up to `2 * 10^9` and the MST can contain 99 edges.

## Worked Examples

### Sample 1

Input:

```
4
5 3 8 8 5 9
```

Sorted tags are:

```
3 5 5 8 8 9
```

| Step | i | Minimum contribution | Maximum index | Maximum contribution |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 0 | 3 |
| 2 | 2 | 5 | 1 | 5 |
| 3 | 3 | 5 | 3 | 8 |

The minimum answer is `3 + 5 + 5 = 13`.

The maximum answer is `3 + 5 + 8 = 16`.

This trace shows why choosing the largest three values is not correct.

### Sample 2

A custom example:

```
5
1 2 3 4 5 6 7 8 9 10
```

| Step | i | Minimum contribution | Maximum index | Maximum contribution |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 1 |
| 2 | 2 | 2 | 1 | 2 |
| 3 | 3 | 3 | 3 | 4 |
| 4 | 4 | 4 | 6 | 7 |

The minimum answer is `1 + 2 + 3 + 4 = 10`.

The maximum answer is `1 + 2 + 4 + 7 = 14`.

The trace demonstrates how many small edges can be hidden inside the growing component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M log M) | Sorting the `M` tags dominates the runtime. |
| Space | O(M) | The array of tag values is stored in memory. |

With `M <= 4950`, sorting is easily within the limits. The memory usage is also small because the number of tags is only a few thousand.

## Test Cases

```python
import sys
import io

def solve_case(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    n = int(input())
    c = list(map(int, input().split()))
    c.sort()

    mn = sum(c[:n - 1])
    mx = 0
    for i in range(1, n):
        mx += c[i * (i - 1) // 2]

    ans = f"{mn} {mx}"

    sys.stdin = old_stdin
    return ans

assert solve_case("4\n5 3 8 8 5 9\n") == "13 16", "sample 1"
assert solve_case("2\n10\n") == "10 10", "minimum size"
assert solve_case("4\n7 7 7 7 7 7\n") == "21 21", "all equal values"
assert solve_case("5\n1 2 3 4 5 6 7 8 9 10\n") == "10 14", "larger complete graph"
assert solve_case("3\n1000000000 2000000000 3000000000\n") == "3000000000 3000000000", "boundary values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 / 5 3 8 8 5 9` | `13 16` | Sample behavior and maximum construction |
| `2 / 10` | `10 10` | Single edge graph |
| All values equal | `21 21` | Duplicate weights |
| Ten tags with five nodes | `10 14` | Multiple hidden internal edges |
| Large values | `3000000000 3000000000` | Large integer handling |

## Edge Cases

For two nodes, there is only one wire, so both the cheapest and most expensive MST costs are the same.

```
Input
2
10
```

The sorted array is `[10]`. The minimum uses the only value. The maximum loop also runs once and selects index zero. The output is:

```
10 10
```

When every tag is equal, every possible assignment gives the same MST.

```
Input
4
7 7 7 7 7 7
```

The minimum uses three sevens. The maximum also selects three positions, but every position contains seven. Both results are:

```
21 21
```

For the case where the largest `N - 1` tags cannot form the maximum MST:

```
Input
4
3 5 5 8 8 9
```

After sorting, the maximum positions are indices `0`, `1`, and `3`. The algorithm selects `3`, `5`, and `8`. The values `8` and `9` cannot both be forced into the MST because too many larger edges would already leave the smaller edges unable to be hidden. The result is:

```
13 16
```

This is exactly the situation where the component growth argument matters. The algorithm does not simply pick large values; it picks values that can actually appear as Kruskal's chosen edges.
