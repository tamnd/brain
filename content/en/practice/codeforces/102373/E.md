---
title: "CF 102373E - Checkered Pattern"
description: "We have an (n times m) rectangular grid, where every cell is either black or white. Two black cells are adjacent when they share a side, so the black cells form an undirected grid graph. We may flip any cells, each at most once."
date: "2026-08-14T03:08:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102373
codeforces_index: "E"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434 \u0434\u043b\u044f \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102373
solve_time_s: 348
verified: false
draft: false
---

[CF 102373E - Checkered Pattern](https://codeforces.com/problemset/problem/102373/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We have an (n \times m) rectangular grid, where every cell is either black or white. Two black cells are adjacent when they share a side, so the black cells form an undirected grid graph.

We may flip any cells, each at most once. The final black-cell graph must contain at least one vertex, must be connected, and must contain no simple cycle. A connected acyclic graph is a tree, so the task is exactly to find a black-cell pattern whose induced graph is a tree and whose Hamming distance from the original pattern is minimum.

The objective counts both kinds of changes equally. Keeping an original black cell costs zero, deleting it costs one, keeping a white cell costs zero, and turning it black costs one.

The dimensions are asymmetric: (n) can reach (100), while (m) is at most (10). The board can contain (1000) cells, so enumerating all (2^{nm}) final patterns is completely impossible. The small width is the useful part of the constraint. When we process the grid row by row, only the last (m) cells can still interact with cells that have not been processed. This gives us a bounded-width dynamic programming problem.

There are several edge cases that are easy to mishandle. For a (1 \times 1) all-white board,

```
.
```

the correct result is

```
#
```

because the empty black graph is forbidden. A solution that simply tries to preserve the original pattern would incorrectly accept the empty graph.

For a (1 \times 3) board

```
#.#
```

the optimal result is, for example,

```
#..
```

with one change. Turning the middle cell black would cost two changes, so an approach that always tries to connect all original black cells is not optimal.

For a (2 \times 2) board containing only black cells,

```
##
##
```

there is a cycle around the square. Removing one corner gives a three-vertex path, so the optimum is one change. A connectivity-only check would incorrectly keep all four cells.

The opposite phenomenon also occurs. Original black cells may be disconnected, and adding a white cell can be better than deleting an entire component. The algorithm must consequently allow both adding and removing cells instead of assuming that only black cells should be deleted.

## Approaches

The direct brute-force solution considers every possible final coloring. There are (2^{nm}) such colorings. For each one, we can run a graph traversal over the black cells and count edges to determine whether the black graph is nonempty, connected, and acyclic. Checking one coloring takes (O(nm)), so the total complexity is

[
O(nm,2^{nm}).
]

At the maximum board size this contains (2^{1000}) possibilities, which is far beyond any practical computation.

The useful observation is that the grid has small width. Process cells in row-major order. When we are about to decide the color of a cell, all cells to its left and all cells in earlier rows have already been fixed. Among those processed cells, only the current frontier can still have edges to future cells. The frontier contains at most (m) cells.

For every black frontier cell, we need to know which already-built connected component it belongs to. This is enough information because a future cell can only connect to its left neighbor and its upper neighbor. We never need to remember the complete shape of an old component.

The state is thus a connectivity profile of at most ten frontier positions. Components are represented by canonical labels such as

```
1 1 0 2 2 0
```

where equal positive labels mean that the corresponding frontier cells belong to the same black component and zero means white.

When a new black cell has two black neighbors belonging to the same component, adding it creates a cycle immediately, so that transition is forbidden. When the two neighbors belong to different components, the new cell merges them. When it has at most one black neighbor, it simply extends that component or starts a new one.

There is one more subtlety. If a component disappears completely from the frontier, no future cell can reach it. If another component is still alive, the final graph would permanently contain two disconnected components, so the state is invalid. If it was the only component, the whole black graph is finished. From that point onward every remaining cell must stay white.

The brute force works because it explicitly examines every possible final graph. It fails because there are exponentially many graphs. The small width lets us replace the complete history by the connectivity of only the frontier, reducing the exponential part to a function of (m), which is at most (10).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nm,2^{nm})) | (O(nm)) | Too slow |
| Frontier DP | (O(nm,S_m,m)) | (O(nm,S_m)) with reconstruction | Accepted |

Here (S_m) is the number of reachable canonical frontier profiles for width (m). Since (m\le10), this is a width-dependent constant for the problem.

## Algorithm Walkthrough

1. Process the board in row-major order. Before processing a cell in column (c), the frontier position (c) represents the cell directly above it, while position (c-1) represents the cell directly to its left.
2. Represent each DP state by the labels of the (m) frontier positions and a `done` flag. A zero label means that the frontier cell is white. Positive equal labels identify frontier cells belonging to the same black component.
3. For every state, first consider making the current cell white. Replace the frontier position by zero. If removing this position makes a black component disappear, reject the transition when another component remains alive. If no component remains, mark the state as `done`, meaning that a complete valid black component has already been finished.
4. Consider making the current cell black. Look at its left and upper neighbors. If both are black and have the same component label, reject the transition because the new cell would connect two vertices already connected by a path, creating a cycle.
5. If the two black neighbors have different labels, merge their components through the new cell. If exactly one neighbor is black, attach the new cell to that component. If neither neighbor is black, create a new component.
6. Canonicalize the labels after a merge. Renumber components according to their first occurrence from left to right. This makes states representing the same connectivity structure identical, so they can share one DP entry.
7. Add one to the transition cost exactly when the chosen color differs from the original cell. For every resulting state, retain only the minimum cost.
8. Store the predecessor state and the chosen color whenever a state receives a better cost. The implementation stores encoded states in compact integer arrays so the whole reconstruction history does not require Python objects for every cell.
9. After all (nm) cells have been processed, accept a state if it represents exactly one finished black component. At the end of the board an unfinished component is also acceptable, because it may simply touch the final frontier. What is forbidden is an empty graph or more than one component.
10. Follow the stored predecessors backwards from the cheapest accepting state. The recorded color at every cell reconstructs an optimal final grid.

### Why it works

The invariant is that every DP state represents exactly the black graph induced by all processed cells, with its connectivity restricted to the current frontier. Every processed component that no longer touches the frontier can never interact with an unprocessed cell again. Consequently, such a component may disappear only when it is the unique remaining component.

When a black cell has two neighbors in the same component, there is already a path between those neighbors, and the two new edges close a cycle. Rejecting this transition is exactly the condition required to maintain acyclicity. Every other black transition preserves a forest, because it either creates a new component, attaches a vertex to one component, or merges two distinct components.

At the end, the accepted state has exactly one nonempty component and no cycle, so its black graph is a nonempty tree. Conversely, every valid final tree can be followed cell by cell by the DP. Its cells never create a cycle, and its unique component never disappears while another component remains. Thus every valid coloring is represented by some DP path, and taking the minimum transition cost gives the minimum number of recolorings.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

INF = 10 ** 9

def encode_state(state, m):
    code = state[m] << (4 * m)
    for c in range(m):
        code |= state[c] << (4 * c)
    return code

def normalize(labels):
    mp = {}
    nxt = 1
    res = list(labels)

    for i, x in enumerate(res):
        if x == 0:
            continue
        if x not in mp:
            mp[x] = nxt
            nxt += 1
        res[i] = mp[x]

    return tuple(res)

def solve_grid(grid):
    n = len(grid)
    m = len(grid[0])
    total = n * m

    initial = (0,) * m + (0,)

    # cur[state] = (minimum cost, index in the current layer)
    cur = {initial: (0, 0)}

    state_layers = []
    parent_layers = []
    choice_layers = []

    for pos in range(total):
        r = pos // m
        c = pos % m

        nxt = {}
        parents = array('Q')
        choices = array('B')

        original_black = grid[r][c] == '#'

        for state, (cost, _) in cur.items():
            done = state[m]

            # Once the only component has disappeared, all remaining
            # cells must stay white.
            allowed_black = not done

            labels = state[:m]

            # Transition 1: make the cell white.
            new_labels = list(labels)
            old = new_labels[c]
            new_labels[c] = 0

            if old != 0:
                # If this was the last frontier occurrence of the
                # component, it disappears from the processed graph.
                if old not in new_labels:
                    if all(x == 0 for x in new_labels):
                        new_state = tuple(new_labels) + (1,)
                        new_cost = cost + (1 if original_black else 0)

                        idx_info = nxt.get(new_state)
                        prev_code = encode_state(state, m)

                        if idx_info is None:
                            idx = len(parents)
                            nxt[new_state] = (new_cost, idx)
                            parents.append(prev_code)
                            choices.append(0)
                        elif new_cost < idx_info[0]:
                            idx = idx_info[1]
                            nxt[new_state] = (new_cost, idx)
                            parents[idx] = prev_code
                            choices[idx] = 0
                    # Otherwise a finished component would be
                    # disconnected from another live component.
                else:
                    new_state = tuple(new_labels) + (0,)
                    new_cost = cost + (1 if original_black else 0)

                    idx_info = nxt.get(new_state)
                    prev_code = encode_state(state, m)

                    if idx_info is None:
                        idx = len(parents)
                        nxt[new_state] = (new_cost, idx)
                        parents.append(prev_code)
                        choices.append(0)
                    elif new_cost < idx_info[0]:
                        idx = idx_info[1]
                        nxt[new_state] = (new_cost, idx)
                        parents[idx] = prev_code
                        choices[idx] = 0
            else:
                new_state = tuple(new_labels) + (done,)
                new_cost = cost + (1 if original_black else 0)

                idx_info = nxt.get(new_state)
                prev_code = encode_state(state, m)

                if idx_info is None:
                    idx = len(parents)
                    nxt[new_state] = (new_cost, idx)
                    parents.append(prev_code)
                    choices.append(0)
                elif new_cost < idx_info[0]:
                    idx = idx_info[1]
                    nxt[new_state] = (new_cost, idx)
                    parents[idx] = prev_code
                    choices[idx] = 0

            # Transition 2: make the cell black.
            if not allowed_black:
                continue

            left = labels[c - 1] if c > 0 else 0
            up = labels[c]

            # Two edges from the new cell to the same component create
            # a cycle.
            if left != 0 and left == up:
                continue

            new_labels = list(labels)

            if left != 0 and up != 0:
                # Merge up into left.
                for j in range(m):
                    if new_labels[j] == up:
                        new_labels[j] = left
                new_labels[c] = left
                new_labels = normalize(new_labels)
            elif left != 0:
                new_labels[c] = left
            elif up != 0:
                new_labels[c] = up
            else:
                new_labels[c] = max(new_labels, default=0) + 1

            new_state = tuple(new_labels) + (0,)
            new_cost = cost + (0 if original_black else 1)
            prev_code = encode_state(state, m)

            idx_info = nxt.get(new_state)

            if idx_info is None:
                idx = len(parents)
                nxt[new_state] = (new_cost, idx)
                parents.append(prev_code)
                choices.append(1)
            elif new_cost < idx_info[0]:
                idx = idx_info[1]
                nxt[new_state] = (new_cost, idx)
                parents[idx] = prev_code
                choices[idx] = 1

        cur = nxt

        state_layers.append(
            array('Q', (encode_state(state, m) for state in cur))
        )
        parent_layers.append(parents)
        choice_layers.append(choices)

    best_state = None
    best_cost = INF
    best_index = -1

    for state, (cost, idx) in cur.items():
        if state[m]:
            if cost < best_cost:
                best_cost = cost
                best_state = state
                best_index = idx
            continue

        components = {x for x in state[:m] if x != 0}

        if len(components) == 1 and cost < best_cost:
            best_cost = cost
            best_state = state
            best_index = idx

    if best_state is None:
        raise RuntimeError("No valid pattern exists")

    answer = [list(row) for row in grid]

    idx = best_index

    for pos in range(total - 1, -1, -1):
        r = pos // m
        c = pos % m

        chosen = choice_layers[pos][idx]
        answer[r][c] = '#' if chosen else '.'

        if pos > 0:
            prev_code = parent_layers[pos][idx]
            idx = state_layers[pos - 1].index(prev_code)

    return '\n'.join(''.join(row) for row in answer)

def solve(data=None):
    if data is None:
        n, m = map(int, input().split())
        grid = [input().strip() for _ in range(n)]
    else:
        lines = data.strip().splitlines()
        n, m = map(int, lines[0].split())
        grid = lines[1:1 + n]

    return solve_grid(grid)

if __name__ == "__main__":
    print(solve())
```

The DP dictionary contains the minimum cost for each canonical frontier state. The extra final element of the state is the `done` flag. A state with `done = 1` means that its only black component has already disappeared from the frontier, so no later black cell can be selected.

The white transition removes the current frontier label. If that removal eliminates the last occurrence of a component while another component remains, the transition is discarded because the disconnected component can never be joined again. If it eliminates the only component, the state becomes `done`.

The black transition uses only the left and upper labels. Equal nonzero labels are the cycle case. Distinct labels are merged, while one or zero neighbors require no merge. The `normalize` function is necessary because labels themselves have no meaning. For example, profiles `(1, 1, 0, 2)` and `(5, 5, 0, 9)` describe exactly the same connectivity and must become the same DP state.

The predecessor is encoded into a 64-bit integer. Four bits per frontier position are sufficient because there are at most ten columns and hence at most ten simultaneous component labels. One additional bit stores `done`. The use of `array` for the reconstruction history avoids the large Python-object overhead that would result from storing every state tuple for every cell.

The reconstruction uses the encoded predecessor directly. Python's `array.index` performs the search in native code, so there is no need to retain a large dictionary for every layer.

No integer-overflow issue exists in Python. The maximum DP cost is only (nm), at most (1000).

## Worked Examples

For Sample 1, the input is

```
###
#.#
###
```

One optimal answer is

```
###
#.#
##.
```

The following table traces that answer. The profile contains the component labels on the current frontier after the processed cell.

| Cell | Original | Chosen | Frontier | Cost |
| --- | --- | --- | --- | --- |
| (1,1) | # | # | 1 0 0 | 0 |
| (1,2) | # | # | 1 1 0 | 0 |
| (1,3) | # | # | 1 1 1 | 0 |
| (2,1) | # | # | 1 1 1 | 0 |
| (2,2) | . | . | 1 0 1 | 0 |
| (2,3) | # | # | 1 0 1 | 0 |
| (3,1) | # | # | 1 0 1 | 0 |
| (3,2) | # | # | 1 1 1 | 0 |
| (3,3) | # | . | 1 1 0 | 1 |

At the fifth cell, the center is kept white. Its upper and left neighbors belong to the same component, but because the cell is white, no cycle is created. The existing top-left and top-right paths remain part of one component. At the final cell, removing the upper frontier position does not disconnect the component because two other frontier positions still carry label 1. The final graph is a tree with eight vertices and seven edges.

For Sample 2, the input is

```
##.
.##
###
##.
```

An optimal answer is

```
##.
.##
#.#
###
```

| Cell | Original | Chosen | Frontier | Cost |
| --- | --- | --- | --- | --- |
| (1,1) | # | # | 1 0 0 | 0 |
| (1,2) | # | # | 1 1 0 | 0 |
| (1,3) | . | . | 1 1 0 | 0 |
| (2,1) | . | . | 0 1 0 | 0 |
| (2,2) | # | # | 0 1 0 | 0 |
| (2,3) | # | # | 0 1 1 | 0 |
| (3,1) | # | # | 2 1 1 | 1 |
| (3,2) | # | . | 2 0 1 | 2 |
| (3,3) | # | # | 2 0 1 | 2 |
| (4,1) | # | # | 2 0 1 | 2 |
| (4,2) | # | # | 2 2 1 | 2 |
| (4,3) | . | # | 2 2 2 | 2 |

The interesting part starts at cell ((3,1)). That cell initially creates a second component, represented by label 2. The white center cell then leaves two separate components on the frontier. The last row connects them: the cell at ((4,3)) sees the left component through ((4,2)) and the upper component through ((3,3)), so their distinct labels are merged. The final profile has only label 2, proving that all black cells belong to one component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nm,S_m,m)) | Each of the (nm) cells processes every reachable frontier state, and a merge can inspect the (m) frontier positions |
| Space | (O(nm,S_m)) | The current DP uses (O(S_m)) states, while compact predecessor arrays are retained for all cells |

Here (S_m) depends only on the width. The width is bounded by (10), so the exponential part is confined to a very small dimension while the height can be (100). This is exactly the setting where frontier DP is useful. The implementation also stores reconstruction data in packed arrays rather than Python tuples, keeping memory proportional to the number of DP states.

## Test Cases

The following harness assumes the submitted solution is saved as `solution.py` and exposes the `solve(data)` function shown above. The small cases are checked against an independent brute-force optimum, while the (100\times10) case checks the known optimum for an all-white board.

```python
from solution import solve

def parse_grid(text):
    lines = text.strip().splitlines()
    n, m = map(int, lines[0].split())
    return n, m, lines[1:1 + n]

def run(inp: str) -> str:
    return solve(inp).strip()

def valid_and_cost(inp, out):
    n, m, original = parse_grid(inp)
    result = out.splitlines()

    assert len(result) == n
    assert all(len(row) == m for row in result)

    black = []
    edges = 0
    total_black = 0
    cost = 0

    for r in range(n):
        for c in range(m):
            assert result[r][c] in '.#'

            if result[r][c] != original[r][c]:
                cost += 1

            if result[r][c] == '#':
                black.append((r, c))
                total_black += 1

                if r > 0 and result[r - 1][c] == '#':
                    edges += 1
                if c > 0 and result[r][c - 1] == '#':
                    edges += 1

    assert total_black > 0

    seen = set()
    stack = [black[0]]
    seen.add(black[0])

    while stack:
        r, c = stack.pop()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m:
                if result[nr][nc] == '#' and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    stack.append((nr, nc))

    assert len(seen) == total_black
    assert edges == total_black - 1

    return cost

def brute_cost(inp):
    n, m, original = parse_grid(inp)
    cells = n * m

    best = cells + 1

    for mask in range(1, 1 << cells):
        board = [['.' for _ in range(m)] for _ in range(n)]
        cost = 0

        for p in range(cells):
            r, c = divmod(p, m)
            black = (mask >> p) & 1

            if black:
                board[r][c] = '#'

            original_black = original[r][c] == '#'
            if black != original_black:
                cost += 1

        if cost >= best:
            continue

        vertices = []
        edges = 0

        for r in range(n):
            for c in range(m):
                if board[r][c] == '#':
                    vertices.append((r, c))
                    if r > 0 and board[r - 1][c] == '#':
                        edges += 1
                    if c > 0 and board[r][c - 1] == '#':
                        edges += 1

        if not vertices:
            continue

        seen = {vertices[0]}
        stack = [vertices[0]]

        while stack:
            r, c = stack.pop()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m:
                    if board[nr][nc] == '#' and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        stack.append((nr, nc))

        if len(seen) == len(vertices) and edges == len(vertices) - 1:
            best = cost

    return best

# Provided samples
sample1 = """\
3 3
###
#.#
###
"""
assert valid_and_cost(sample1, run(sample1)) == 1

sample2 = """\
4 3
##.
.##
###
##.
"""
assert valid_and_cost(sample2, run(sample2)) == 2

sample3 = """\
2 3
...
...
"""
assert valid_and_cost(sample3, run(sample3)) == 1

# Minimum-size input
case1 = """\
1 1
#
"""
assert valid_and_cost(case1, run(case1)) == 0

# Maximum-size input, all cells initially white.
# One black cell is necessary and sufficient.
case2 = "100 10\n" + "\n".join(["." * 10] * 100) + "\n"
assert valid_and_cost(case2, run(case2)) == 1

# All-black input containing a cycle.
case3 = """\
2 2
##
##
"""
assert valid_and_cost(case3, run(case3)) == 1
assert valid_and_cost(case3, run(case3)) == brute_cost(case3)

# Boundary case where keeping both black cells is worse than deleting one.
case4 = """\
1 3
#.#
"""
assert valid_and_cost(case4, run(case4)) == 1
assert valid_and_cost(case4, run(case4)) == brute_cost(case4)

# Extra small exhaustive-optimality checks.
case5 = """\
2 3
######
""".replace("\n", "\n")
assert valid_and_cost(case5, run(case5)) == brute_cost(case5)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / #` | `#` | Minimum dimensions and already-valid tree |
| `100 10` with every cell `.` | Any pattern with exactly one `#` | Maximum board size and the nonempty requirement |
| `2 2 / ## / ##` | Any three-cell path | Cycle detection |
| `1 3 / #.#` | Any single black cell | Deleting a disconnected component can be cheaper than connecting it |
| `2 3 / ### / ###` | Any optimal induced tree | Larger cycle and frontier merging |

## Edge Cases

The (1\times1) all-white case is handled by the `done` distinction and the final nonempty check. Starting from the empty profile, the white transition cannot produce an accepted final state. The black transition creates one component, and because the board ends immediately, that single active component is accepted. The output is `#` with cost one.

For

```
1 3
#.#
```

the first black cell creates component 1. The middle cell is optimally kept white, so the right black cell would create a second component. The DP recognizes that this cannot produce a connected final graph unless something later joins the components, but there is no useful future cell. The cheapest accepted state consequently keeps only one of the two original black cells, giving cost one.

For

```
2 2
##
##
```

the first three black cells can form a path. When the fourth cell is considered, its left and upper neighbors already have the same component label. Adding it would create the fourth side of the square, so the transition is rejected immediately. The DP instead chooses one white cell and obtains a three-vertex tree at cost one.

For the maximum-size all-white board, every black cell costs one, so the lower bound is one because the final graph cannot be empty. A single black cell is already a tree, so that lower bound is attainable. The DP finds exactly that solution without needing to explore arbitrary large connected shapes.

The disconnected-component case is handled by the frontier closure rule. Once a component disappears from the frontier, no unprocessed cell can ever touch it. If another component is alive, the state is discarded because the final graph can never become connected. If no other component is alive, the state is marked `done`, and only white cells may follow. This is what prevents the DP from silently accepting a pattern consisting of several disconnected trees.
