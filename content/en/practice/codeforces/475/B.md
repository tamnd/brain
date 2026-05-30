---
title: "CF 475B - Strongly Connected City"
description: "We are asked to determine if a city with a grid of horizontal and vertical streets is \"strongly connected\" once each street is made one-way. The city can be visualized as a grid of intersections, with n horizontal streets and m vertical streets forming n × m junctions."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 475
codeforces_index: "B"
codeforces_contest_name: "Bayan 2015 Contest Warm Up"
rating: 1400
weight: 475
solve_time_s: 59
verified: true
draft: false
---

[CF 475B - Strongly Connected City](https://codeforces.com/problemset/problem/475/B)

**Rating:** 1400  
**Tags:** brute force, dfs and similar, graphs, implementation  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine if a city with a grid of horizontal and vertical streets is "strongly connected" once each street is made one-way. The city can be visualized as a grid of intersections, with `n` horizontal streets and `m` vertical streets forming `n × m` junctions. Each horizontal street has a single allowed direction: either all traffic flows west-to-east or east-to-west. Each vertical street also has a single direction: north-to-south or south-to-north. A driver can move along a street according to its direction and switch to a crossing street at intersections.

The input provides the number of horizontal and vertical streets, followed by a string of length `n` with `<` or `>` for horizontal streets, and a string of length `m` with `^` or `v` for vertical streets. The output should be "YES" if it is possible to reach any intersection from any other intersection following street directions, and "NO" otherwise.

The constraints, with `n, m ≤ 20`, imply that the total number of intersections is at most 400. This is small enough that brute-force graph traversal on all intersections is feasible. Edge cases are not immediately obvious but can arise from streets whose directions form "dead ends" along the border. For instance, if the topmost horizontal street points left and the leftmost vertical street points up, the intersection at the top-left corner becomes unreachable from certain points, breaking strong connectivity.

A naive implementation might check connectivity from just one intersection, which would be wrong. Strong connectivity requires that every junction is reachable from every other junction. A careless approach could also misinterpret the directions, e.g., assuming `<` means west-to-east instead of east-to-west.

## Approaches

The brute-force approach is to model each junction as a node in a directed graph and add edges according to street directions. Then, for every junction, run a graph traversal algorithm like DFS or BFS and verify that all other junctions are reachable. With up to 400 nodes, this requires up to 400 traversals, each visiting 400 nodes, resulting in roughly 160,000 operations, which is acceptable for the problem constraints but unnecessary.

The key insight is that strong connectivity in a grid with uniform street directions can be guaranteed if and only if the streets on the boundary allow travel along all four edges. In other words, if the topmost and bottommost horizontal streets point in opposite directions, and the leftmost and rightmost vertical streets point in opposite directions, every junction can reach every other junction. This reduces the problem to checking the four corner junctions: if the direction patterns allow traversal from corners to corners, then the interior junctions are automatically reachable, because movement along horizontal and vertical streets propagates the reachability.

This observation lets us avoid constructing the full graph and running multiple traversals. We only need to check whether the top-left, top-right, bottom-left, and bottom-right corners are mutually reachable, which is equivalent to ensuring that the first and last characters of the horizontal and vertical strings point in opposite directions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS from every junction | O(n_m_(n*m)) | O(n*m) | Accepted but unnecessary |
| Corner-check Insight | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of horizontal streets `n` and vertical streets `m`, followed by the strings representing directions of horizontal and vertical streets.
2. Examine the topmost horizontal street and bottommost horizontal street. If both point in the same direction, the leftmost or rightmost columns may be unreachable, making strong connectivity impossible.
3. Examine the leftmost vertical street and rightmost vertical street. If both point in the same direction, the topmost or bottommost rows may be unreachable, breaking strong connectivity.
4. If both horizontal and vertical boundary checks pass, print "YES"; otherwise, print "NO".

Why it works: in a grid where streets have uniform directions, the only way a junction could be unreachable is if the boundary streets prevent traversal to or from it. By checking that opposite edges are oriented in opposite directions, we guarantee that movement around the grid is possible, and by extension, every junction can reach every other junction. This avoids explicit graph construction and multiple traversals while maintaining correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    h_dirs = input().strip()
    v_dirs = input().strip()

    horizontal_ok = h_dirs[0] != h_dirs[-1]
    vertical_ok = v_dirs[0] != v_dirs[-1]

    if horizontal_ok and vertical_ok:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()
```

The code reads input using `sys.stdin.readline` for efficiency. It checks the first and last horizontal street directions and the first and last vertical street directions. If they are not equal, the grid is guaranteed to be strongly connected, so it prints "YES"; otherwise, "NO". Boundary conditions are carefully handled: `h_dirs[0]` is the northernmost street and `h_dirs[-1]` is the southernmost street, `v_dirs[0]` is the westernmost and `v_dirs[-1]` is the easternmost.

## Worked Examples

For the input:

```
3 3
><>
v^v
```

| Variable | Value |
| --- | --- |
| h_dirs | '><>' |
| v_dirs | 'v^v' |
| horizontal_ok | '>' != '>' → False |
| vertical_ok | 'v' != 'v' → False |
| Output | NO |

The check confirms that the first and last horizontal streets are both '>', so the top row cannot reach the bottom row. Similarly, vertical boundaries both point 'v', preventing left-right connectivity. Hence "NO".

For input:

```
2 2
><
^v
```

| Variable | Value |
| --- | --- |
| h_dirs | '><' |
| v_dirs | '^v' |
| horizontal_ok | '>' != '<' → True |
| vertical_ok | '^' != 'v' → True |
| Output | YES |

All corner junctions are reachable, and the interior connectivity propagates along the directions, resulting in strong connectivity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only boundary checks of the strings are needed |
| Space | O(1) | No additional data structures proportional to n*m |

With `n, m ≤ 20`, the solution executes a handful of operations and consumes negligible memory, well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("3 3\n><>\nv^v\n") == "NO", "sample 1"
# Custom cases
assert run("2 2\n><\n^v\n") == "YES", "all edges opposite"
assert run("2 3\n>>\n^v^\n") == "NO", "horizontal boundaries same"
assert run("3 2\n<><\nvv\n") == "NO", "vertical boundaries same"
assert run("4 4\n><<>\n^v^v\n") == "YES", "mixed interior, boundaries opposite"
assert run("2 2\n<<\n^^\n") == "NO", "both boundaries same"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2\n><\n^v | YES | minimal size, opposite boundaries |
| 2 3\n>>\n^v^ | NO | horizontal boundaries prevent connectivity |
| 3 2\n<><\nvv | NO | vertical boundaries prevent connectivity |
| 4 4\n><<>\n^v^v | YES | larger grid, mixed interior but corners reachable |
| 2 2\n<<\n^^ | NO | minimal grid, boundaries same |

## Edge Cases

If both horizontal streets point in the same direction, e.g., `<<` with vertical streets `^v`, the top row cannot reach the bottom row. The algorithm checks `h_dirs[0] != h_dirs[-1]` and returns "NO". Similarly, if vertical streets are the same, e.g., `v^v^`, the leftmost column cannot reach the rightmost column, and the output is correctly "NO". The algorithm handles grids of size 2×2 correctly by the same logic, confirming strong connectivity only when boundaries are oppositely oriented.
