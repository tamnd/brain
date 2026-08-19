---
title: "CF 102168E - \u041a\u0443\u0431\u0438\u043a\u0438"
description: "We have a rectangular box of unit cubes with dimensions x × y × z. A cube is identified by coordinates (x, y, z). Three two-dimensional arrays describe which positions are visible in the three coordinate projections."
date: "2026-08-19T07:22:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102168
codeforces_index: "E"
codeforces_contest_name: "\u041b\u0438\u0447\u043d\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u043e\u0433\u043e \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442\u0430 \u0441\u0440\u0435\u0434\u0438 \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432 2018-2019"
rating: 0
weight: 102168
solve_time_s: 138
verified: true
draft: false
---

[CF 102168E - \u041a\u0443\u0431\u0438\u043a\u0438](https://codeforces.com/problemset/problem/102168/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular box of unit cubes with dimensions `x × y × z`. A cube is identified by coordinates `(x, y, z)`. Three two-dimensional arrays describe which positions are visible in the three coordinate projections.

The left projection has size `z × y`, so `left[z][y]` is `#` exactly when at least one cube with those fixed `y` and `z` coordinates exists. The front projection has size `z × x`, so `front[z][x]` is `#` when some cube with those `x` and `z` coordinates exists. The top projection has size `y × x`, so `top[y][x]` is `#` when some cube with those `x` and `y` coordinates exists.

We have to reconstruct an actual three-dimensional figure whose three projections are exactly the given arrays. Among all such figures, we want one containing as many cubes as possible.

For a particular position `(x, y, z)`, a cube can only exist if all three corresponding projection cells are `#`. If even one of them is `.`, putting a cube there would immediately make that projection contain an unwanted `#`.

The dimensions are at most `100`, so there are at most `100^3 = 1,000,000` possible cube positions. A linear pass over all positions is easily feasible. This also means we should avoid algorithms that enumerate subsets of cubes or otherwise explore exponentially many configurations. Even quadratic work over the whole three-dimensional space would already be unnecessarily expensive.

The main edge cases come from confusing a necessary condition with a sufficient one. For example, consider

```
2 2 1#..#
.##.
#...
```

The only `#` in the left projection is at `(y=0,z=0)`, so a cube realizing it must have `y=0`. The only `#` in the front projection requires `x=1`, while the only `#` in the top projection at `y=0` requires `x=0`. No single cube can satisfy all three requirements, so the correct answer is `NO`. A careless solution that merely checks whether every projection contains some `#` would incorrectly accept it.

Another edge case is a projection cell that is `#` but has no compatible cube even though several other cubes can be placed. For example,

```
2 2 1##..
.#..
#...
```

The left projection requires both `y=0` and `y=1` to contain a cube. The front projection allows only `x=1`, while the top projection allows only `x=0` at `y=0`. The `y=0` left cell cannot be realized, so the answer is `NO`. A construction that simply fills every position allowed by two of the projections can silently create the wrong third projection.

At the opposite extreme, when all three projections consist entirely of `#`, every one of the `x*y*z` positions can be filled. The answer is then the completely full box, which reaches the maximum possible number of cubes.

## Approaches

The most direct brute-force approach is to consider every possible three-dimensional figure and check its projections. There are `x*y*z` possible cube positions, so the number of different figures is `2^(x*y*z)`. In the largest case this is `2^1,000,000` possible configurations, far beyond anything that can be processed.

A more useful naive approach is to examine every possible cube and decide whether it is compatible with the three projections. That already suggests the key observation. For a cube `(x, y, z)`, its presence is allowed exactly when

```
left[z][y] = '#'front[z][x] = '#'top[y][x] = '#'
```

Suppose all such allowed cubes are placed. This construction cannot introduce a `#` into any projection cell that was originally `.`, because every placed cube was explicitly required to agree with all three projections.

The remaining question is whether every original `#` is actually represented by at least one placed cube. We can answer that during the same scan. Whenever a position satisfies all three conditions, we mark its three projection cells as covered. After processing all `x*y*z` positions, every `#` in every projection must have been covered. If some `#` remains uncovered, no valid figure can exist, because every cube capable of covering that projection cell would have to satisfy the other two projections as well.

The same observation also proves maximality. Every cube in any valid solution must belong to the set of positions compatible with all three projections. Our construction contains every such position. Thus no other valid figure can contain more cubes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over figures | `O(2^(xyz))` or worse | Exponential | Too slow |
| Check every cube and cover projections | `O(xyz)` | `O(xy + xz + yz)` besides output | Accepted |

## Algorithm Walkthrough

1. Read the three projection arrays. Ignore empty separator lines because the actual projection rows contain only `#` and `.`.
2. Allocate three boolean coverage arrays with the same shapes as the input projections. `covered_left[z][y]` means that we have already found a valid cube whose projection covers that left-view cell. The other two arrays have the analogous meaning.
3. Iterate through every possible cube position `(z, y, x)`. A cube is a candidate exactly when `left[z][y]`, `front[z][x]`, and `top[y][x]` are all `#`.
4. For every candidate cube, mark its three projection cells as covered. The candidate itself is also part of the final answer, because adding it cannot damage any projection.
5. After the scan, inspect every `#` in each projection. If any such cell is not covered, print `NO`. There is no alternative placement that could fix it, because every possible cube covering that cell was already tested and rejected by at least one of the other projections.
6. If all `#` cells are covered, print `YES`. Generate every output cell again using the same compatibility condition. A position is `#` exactly when all three corresponding projection cells are `#`; otherwise it is `.`.
7. Print the layers in increasing `z` order, with a blank line between consecutive layers. This matches the required layer format.

### Why it works

Consider the set `C` of all cube positions whose three projection cells are `#`. Every valid figure can contain only cubes from `C`, because a cube outside `C` would create a `#` in a projection position that is supposed to be empty. Our construction contains every cube in `C`, so it contains at least as many cubes as any valid figure.

The construction produces the correct projections exactly when every input `#` belongs to at least one cube in `C`. The coverage arrays test precisely this condition. If every `#` is covered, every required projection cell is produced, while no forbidden `.` can be produced because all placed cubes belong to `C`. If some `#` is not covered, no valid figure exists because there is no compatible cube capable of producing it. This proves both feasibility and maximality.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve():    x, y, z = map(int, input().split())
    # Empty lines are separators between projections.    lines = [line.strip() for line in sys.stdin if line.strip()]
    pos = 0
    left = lines[pos:pos + z]    pos += z
    front = lines[pos:pos + z]    pos += z
    top = lines[pos:pos + y]
    covered_left = [[False] * y for _ in range(z)]    covered_front = [[False] * x for _ in range(z)]    covered_top = [[False] * x for _ in range(y)]
    # Find every cube that is compatible with all three projections.    for zz in range(z):        for yy in range(y):            if left[zz][yy] != '#':                continue
            for xx in range(x):                if front[zz][xx] != '#':                    continue                if top[yy][xx] != '#':                    continue
                covered_left[zz][yy] = True                covered_front[zz][xx] = True                covered_top[yy][xx] = True
    # Every '#' in every projection must be represented.    for zz in range(z):        for yy in range(y):            if left[zz][yy] == '#' and not covered_left[zz][yy]:                print("NO")                return
    for zz in range(z):        for xx in range(x):            if front[zz][xx] == '#' and not covered_front[zz][xx]:                print("NO")                return
    for yy in range(y):        for xx in range(x):            if top[yy][xx] == '#' and not covered_top[yy][xx]:                print("NO")                return
    print("YES")
    # Every compatible cube is present in the maximum construction.    for zz in range(z):        for yy in range(y):            row = []            for xx in range(x):                if (                    left[zz][yy] == '#'                    and front[zz][xx] == '#'                    and top[yy][xx] == '#'                ):                    row.append('#')                else:                    row.append('.')            print(''.join(row))
        if zz + 1 < z:            print()

if __name__ == "__main__":    solve()
```

The first part of the implementation reads all non-empty lines after the dimensions. This is convenient because the input explicitly separates the three projections with blank lines, but those separators carry no information.

The three coverage arrays store only projection information, not the entire three-dimensional figure. Their total size is `xy + xz + yz`, which is much smaller than the possible `xyz` cube positions and is already enough to determine whether every requested projection cell has been realized.

The nested loops implement the central condition directly. The indices are deliberately written as `zz`, `yy`, and `xx` so their relationship to the three projections remains visible. The left projection uses `(zz, yy)`, the front projection uses `(zz, xx)`, and the top projection uses `(yy, xx)`.

There is no need to store the constructed figure. After feasibility has been established, the same three conditions can be evaluated again while printing. This keeps the implementation simple and avoids allocating another million-element three-dimensional structure.

The coverage checks are separate for the three projections because a failure in any one of them makes the entire reconstruction impossible. There is no integer overflow issue in Python, and the largest loop contains only one million iterations.

## Worked Examples

### Sample 1

For the first sample, the dimensions are `x=4`, `y=3`, `z=2`. The first layer has the following projection-compatible rows:

```
#####.#####.
```

The second layer is

```
####....###.
```

The algorithm reaches each `#` in the projections through at least one compatible cube.

| `z` | `y` | `x` | Left | Front | Top | Cube |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | # | # | # | # |
| 0 | 0 | 1 | # | # | # | # |
| 0 | 0 | 2 | # | # | # | # |
| 0 | 0 | 3 | # | # | # | # |
| 0 | 1 | 0 | # | # | # | # |
| 0 | 1 | 1 | # | . | # | . |
| 0 | 1 | 2 | # | # | # | # |
| 0 | 1 | 3 | # | # | # | # |
| 0 | 2 | 0 | # | # | # | # |
| 0 | 2 | 1 | # | # | # | # |
| 0 | 2 | 2 | # | # | # | # |
| 0 | 2 | 3 | # | # | . | . |

The same test is performed for `z=1`. Every required projection cell becomes covered, so the answer is `YES`. Filling every compatible position produces the maximum possible figure.

### Sample 2

For an all-`#` `2 × 2 × 2` instance, every cube is compatible with every projection cell.

| `z` | Candidate positions | Covered left cells | Covered front cells | Covered top cells |
| --- | --- | --- | --- | --- |
| 0 | 4 | all 2 | all 2 | all 4 |
| 1 | 4 | all 2 | all 2 | all 4 |

There are eight compatible cubes, so all eight are placed. The output consists of two layers, each containing

```
####
```

The example demonstrates the maximality property particularly clearly. Since no projection contains a `.`, there is no reason to leave any compatible cube empty.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(xyz)` | Every possible cube position is examined once, followed by `O(xy + xz + yz)` projection checks and output. |
| Space | `O(xy + xz + yz)` | The input projections and three coverage arrays are stored; the three-dimensional figure is generated directly during output. |

With `x,y,z <= 100`, the main loop performs at most one million cube checks. The generated output can itself contain about one million characters, so the running time is naturally proportional to the amount of data the program may need to print.

## Test Cases

Because a valid reconstruction is not necessarily unique, a test harness should not compare arbitrary `YES` outputs character-for-character. The helper below validates the returned figure against the three projections and also checks that the figure has the maximum number of cubes.

```python
Python# helper: run solution on input string, return output stringimport sysimport io

def solve():    x, y, z = map(int, input().split())
    lines = [line.strip() for line in sys.stdin if line.strip()]    pos = 0
    left = lines[pos:pos + z]    pos += z
    front = lines[pos:pos + z]    pos += z
    top = lines[pos:pos + y]
    covered_left = [[False] * y for _ in range(z)]    covered_front = [[False] * x for _ in range(z)]    covered_top = [[False] * x for _ in range(y)]
    for zz in range(z):        for yy in range(y):            if left[zz][yy] != '#':                continue            for xx in range(x):                if front[zz][xx] == '#' and top[yy][xx] == '#':                    covered_left[zz][yy] = True                    covered_front[zz][xx] = True                    covered_top[yy][xx] = True
    for zz in range(z):        for yy in range(y):            if left[zz][yy] == '#' and not covered_left[zz][yy]:                print("NO")                return
    for zz in range(z):        for xx in range(x):            if front[zz][xx] == '#' and not covered_front[zz][xx]:                print("NO")                return
    for yy in range(y):        for xx in range(x):            if top[yy][xx] == '#' and not covered_top[yy][xx]:                print("NO")                return
    print("YES")
    for zz in range(z):        for yy in range(y):            print(''.join(                '#'                if left[zz][yy] == '#'                and front[zz][xx] == '#'                and top[yy][xx] == '#'                else '.'                for xx in range(x)            ))        if zz + 1 < z:            print()

def run(inp: str) -> str:    global input
    old_stdin = sys.stdin    old_stdout = sys.stdout    old_input = input
    sys.stdin = io.StringIO(inp)    sys.stdout = io.StringIO()    input = sys.stdin.readline
    try:        solve()        return sys.stdout.getvalue()    finally:        sys.stdin = old_stdin        sys.stdout = old_stdout        input = old_input

def parse_result(inp: str, out: str):    data = [line.strip() for line in inp.splitlines() if line.strip()]    x, y, z = map(int, data[0].split())
    p = 1    left = data[p:p + z]    p += z    front = data[p:p + z]    p += z    top = data[p:p + y]
    out_lines = out.splitlines()    assert out_lines, "empty output"
    if out_lines[0] == "NO":        return False, None, (left, front, top, x, y, z)
    assert out_lines[0] == "YES"
    figure = []    p = 1
    for zz in range(z):        layer = []        for yy in range(y):            row = out_lines[p]            p += 1            assert len(row) == x            assert all(c in ".#" for c in row)            layer.append(row)        figure.append(layer)
        if zz + 1 < z:            assert out_lines[p] == ""            p += 1
    return True, figure, (left, front, top, x, y, z)

def validate(inp: str, out: str) -> bool:    ok, figure, info = parse_result(inp, out)    left, front, top, x, y, z = info
    expected_exists = True
    for zz in range(z):        for yy in range(y):            if left[zz][yy] == '#':                if not any(                    figure[zz][yy][xx] == '#'                    for xx in range(x)                ):                    expected_exists = False
    for zz in range(z):        for xx in range(x):            if front[zz][xx] == '#':                if not any(                    figure[zz][yy][xx] == '#'                    for yy in range(y)                ):                    expected_exists = False
    for yy in range(y):        for xx in range(x):            if top[yy][xx] == '#':                if not any(                    figure[zz][yy][xx] == '#'                    for zz in range(z)                ):                    expected_exists = False
    if not ok:        return not expected_exists
    # The construction must contain exactly every position compatible    # with all three projections.    for zz in range(z):        for yy in range(y):            for xx in range(x):                allowed = (                    left[zz][yy] == '#'                    and front[zz][xx] == '#'                    and top[yy][xx] == '#'                )                assert (figure[zz][yy][xx] == '#') == allowed
    return expected_exists

# Provided Sample 1.sample1 = """\4 3 2####.##############.#####."""
out = run(sample1)assert out == """\YES#####.#####.####....###.""", "sample 1"

# Provided NO sample, reconstructed from the three projection groups# shown in the statement.sample_no = """\3 3 3#...#...#.#...##....##...#."""
assert run(sample_no).strip() == "NO", "provided NO sample"

# Minimum-size valid instance.minimum = """\1 1 1#
#
#"""
assert run(minimum) == """\YES#""", "minimum valid instance"

# Minimum-size impossible instance. At least one projection requests# a cube, but the three requests cannot refer to the same cube.minimum_no = """\1 1 1.
#
#"""
assert run(minimum_no).strip() == "NO", "minimum impossible instance"

# Boundary case where every projection is full.all_full = """\2 2 2####
####
####"""
assert validate(all_full, run(all_full)), "all projections full"

# A compatibility conflict: every projection has '#', but no cube can# satisfy all three projections simultaneously.conflict = """\2 2 1#...
.#..
#..."""
assert run(conflict).strip() == "NO", "incompatible projections"

# A larger boundary case with one compatible cube and many empty cells.single_cube = """\3 3 2#........
.#.......
.#......."""
assert validate(single_cube, run(single_cube)), "single compatible cube"
```

The first assertion compares the complete output because the deterministic construction for the first sample has a unique result under this implementation. The remaining positive tests use `validate`, since constructive problems generally allow several different valid outputs.

The all-full test is especially useful for checking the upper bounds of every loop. The conflict test catches the most common logical mistake, accepting the instance merely because every projection contains the requested `#` cells independently. The single-cube test exercises nonzero coordinates inside the box and checks that empty projection cells force the corresponding three-dimensional positions to remain empty.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| First provided sample | Exact `YES` construction | Normal reconstruction and maximal filling |
| Provided `NO` sample | `NO` | Incompatible projection constraints |
| `1 × 1 × 1`, all `#` | One cube | Minimum dimensions |
| `1 × 1 × 1`, one projection `.` | `NO` | Smallest impossible instance |
| `2 × 2 × 2`, all `#` | Full box of 8 cubes | Full boundaries and maximal construction |
| Conflicting `2 × 2 × 1` projections | `NO` | Detecting incompatible `#` cells |
| Sparse `3 × 3 × 2` instance | `YES`, one compatible cube | Coordinate mapping and empty cells |

## Edge Cases

For the minimum valid input,

```
1 1 1#
#
#
```

there is exactly one possible cube. All three projections request it, so the triple `(0,0,0)` satisfies the three conditions. All projection cells are marked covered and the output is

```
YES#
```

The algorithm does not require any special handling for dimension `1`; the ordinary loops naturally execute exactly once.

For the minimum impossible input,

```
1 1 1.
#
#
```

the only possible cube is rejected immediately because the left projection is `.`. The two `#` cells in the other projections cannot be realized without that cube, so the coverage check finds an uncovered `#` and returns `NO`.

The conflict case

```
2 2 1#...
.#..
#...
```

shows why all three projections must be checked together. The left projection asks for `y=0`, the front projection asks for `x=1`, while the top projection asks for `x=0` at `y=0`. During the only height layer, no `(x,y)` pair satisfies all three conditions. Consequently `covered_left[0][0]` stays false and the algorithm rejects the instance.

For a completely filled `2 × 2 × 2` box,

```
2 2 2####
####
####
```

every combination of `x`, `y`, and `z` satisfies all three conditions. The scan covers every projection cell and the output contains all eight cubes. Since every possible cube is compatible, no valid solution can contain more than eight cubes, so the construction is optimal.

The sparse case is handled without special cases as well. A projection cell marked `.` eliminates every three-dimensional position that maps onto it. Since the final figure is exactly the intersection of the three lifted projections, one-dimensional boundaries and interior empty regions are treated identically. This is the central invariant behind the whole construction.
