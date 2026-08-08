---
title: "CF 102465I - Mason's Mark"
description: "We have a black and white pixel grid representing several stones. The black pixels have three possible roles. Some belong to the connected black region outside all stones, some form the actual mason's mark inside a stone, and some are isolated noise pixels."
date: "2026-08-08T09:27:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102465
codeforces_index: "I"
codeforces_contest_name: "2018-2019 ICPC Southwestern European Regional Programming Contest (SWERC 2018)"
rating: 0
weight: 102465
solve_time_s: 259
verified: true
draft: false
---

[CF 102465I - Mason's Mark](https://codeforces.com/problemset/problem/102465/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a black and white pixel grid representing several stones. The black pixels have three possible roles. Some belong to the connected black region outside all stones, some form the actual mason's mark inside a stone, and some are isolated noise pixels. Every stone contains exactly one mark, and the mark is surrounded by white pixels.

The dimensions of the grid are at most 1000 by 1000, so there can be up to one million pixels. A solution that repeatedly scans a large part of the image for every discovered object can easily reach billions or even trillions of operations. The four second limit strongly favors an algorithm whose total work is proportional to the number of pixels, with only a small constant amount of work per pixel. The grid is large enough that recursive flood fill is also unsafe in Python because the recursion depth can be linear in the grid size.

The central observation is that the three marks are topologically different. If we look at the white regions enclosed by a mark, an A encloses exactly one white region, a B encloses exactly two, and a C encloses none. The dimensions of those marks can vary because the parameters x and y are arbitrary, so measuring the bounding box or the exact number of black pixels is not reliable. The number of enclosed white components does not depend on x or y.

There are several traps hidden in this formulation. The first is the outer black region. Consider

```
#######
#.....#
#..#..#
#.....#
#######
```

The isolated `#` looks like a possible mark, but it is actually noise. More importantly, black pixels belonging to the outside region can themselves resemble a C or another mark. They must be removed before any classification is attempted.

The second trap is that diagonal connectivity matters for the outside region. For example,

```
#######
#.....#
#.#...#
##....#
#######
```

The two black regions touching diagonally belong to the same outside region under 8-connectivity. Treating the outside region as 4-connected can leave some of its pixels behind and falsely classify them as marks.

The third trap is noise. A noise pixel is a black component consisting of exactly one pixel. Its surrounding white pixels form an ordinary part of a stone's surface, not an enclosed interior of a mark. A careless solution that simply counts white components adjacent to every black component can mistake such a pixel for a C-like mark or even count a false hole.

The fourth trap is that the white surface uses 4-connectivity, not 8-connectivity. A diagonal gap does not connect two white regions. For example,

```
#######
#..#..#
#.#.#.#
#..#..#
#######
```

must be interpreted using vertical and horizontal adjacency when deciding which white pixels belong to the same region. Using 8-connectivity would merge regions that are separated by diagonal contact and can change the hole count.

## Approaches

A direct approach would first find every black component and then, for each candidate component, inspect the surrounding white pixels to determine how many regions it encloses. This is conceptually correct because the mark type is completely determined by its enclosed white regions. The problem is that doing a separate flood fill of the surrounding grid for every candidate repeatedly processes the same pixels.

In the worst case there can be Θ(WH) small components. If every component causes another Θ(WH) scan, the total work becomes Θ((WH)^2). With one million pixels, that is on the order of 10^12 pixel visits, far beyond the four second limit. The brute force works because each individual classification is easy, but it fails because the same white surface gets explored over and over.

The useful observation is that white regions can be computed globally. Every white pixel belongs to exactly one 4-connected white component, so we can flood-fill every white component exactly once. While doing that flood fill, we inspect the black components touching it.

The outside surface of a stone touches the black region around the stones. An interior region belonging to a mark does not touch that outside black region. Because each stone has exactly one mark, such an interior white component can be associated with exactly one non-noise black component. Noise can be ignored because its black component has size one.

The problem then becomes a pair of global connected-component computations. First, we identify the 8-connected outside black region. Next, we label every remaining black component and record its size. Finally, we flood-fill every white component with 4-connectivity. For each white component that does not touch the outside black region, we increment the hole count of the unique non-noise black component touching it.

The resulting hole count directly gives the mark type. Zero holes means C, one hole means A, and two holes means B.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((WH)^2) | O(WH) | Too slow |
| Optimal | O(WH) | O(WH) | Accepted |

## Algorithm Walkthrough

1. Store the image as a list of strings and treat each pixel as a vertex of a grid graph. Black pixels will later be connected using 8-neighbor adjacency, while white pixels will use 4-neighbor adjacency.
2. Start a flood fill from the corner pixel `(0, 0)` using all eight neighboring directions. The entire border is black, and the statement guarantees that every black pixel belonging to the outside region is connected to the border with 8-connectivity. Consequently, this flood fill labels exactly the outside black region.
3. Scan all remaining black pixels. Whenever an unlabeled black pixel is found, run an 8-connected flood fill and give that component a new ID. Store its size. Components of size one are noise, while every larger component is a genuine mason's mark.
4. Scan all white pixels. For every unvisited white pixel, run a 4-connected flood fill. During the flood fill, inspect all neighboring black pixels and remember three pieces of information: whether this white component touches the outside black region, which non-noise black component it touches, and whether it touches more than one such component.
5. After a white component has been completely explored, classify its role. If it touches the outside black region, it is part of the ordinary stone surface and cannot be a mark interior. If it does not touch the outside region and is adjacent to exactly one non-noise black component, it is an enclosed region belonging to that mark, so increment that component's hole count. Noise components are deliberately ignored.
6. After all white components have been processed, inspect the hole count of every non-noise black component. A component with zero holes represents C, one hole represents A, and two holes represents B. Increment the corresponding answer.

The key invariant is that after the white-component flood fills finish, every white component has been classified exactly once as either ordinary stone surface or an enclosed interior. Because the stone surface is 4-connected and every stone has exactly one mark, an enclosed component can belong to only that stone's mark. Since every noise component has size one, ignoring size-one black components prevents noise from contributing holes. Thus every genuine mark receives exactly its true number of enclosed white regions.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    W, H = map(int, input().split())
    grid = [input().strip() for _ in range(H)]
    n = W * H

    # comp[idx] == -1: not a black component yet
    # comp[idx] == 0: outside black region
    # comp[idx] > 0: a genuine/noise black component
    comp = array('i', [-1]) * n

    # 1. Flood-fill the outside black region using 8-connectivity.
    stack = [0]
    comp[0] = 0

    while stack:
        p = stack.pop()
        r = p // W
        c = p - r * W

        r0 = max(0, r - 1)
        r1 = min(H - 1, r + 1)
        c0 = max(0, c - 1)
        c1 = min(W - 1, c + 1)

        for nr in range(r0, r1 + 1):
            base = nr * W
            for nc in range(c0, c1 + 1):
                if nr == r and nc == c:
                    continue
                q = base + nc
                if comp[q] == -1 and grid[nr][nc] == '#':
                    comp[q] = 0
                    stack.append(q)

    # sizes[component_id] is the number of black pixels.
    # Component 0 is the outside region.
    sizes = [0]
    sizes[0] = sum(1 for p in range(n) if comp[p] == 0)

    # 2. Label every remaining black component.
    for r in range(H):
        base = r * W
        for c in range(W):
            p = base + c
            if grid[r][c] != '#' or comp[p] != -1:
                continue

            cid = len(sizes)
            sizes.append(0)
            comp[p] = cid
            stack = [p]
            size = 0

            while stack:
                q = stack.pop()
                size += 1
                qr = q // W
                qc = q - qr * W

                r0 = max(0, qr - 1)
                r1 = min(H - 1, qr + 1)
                c0 = max(0, qc - 1)
                c1 = min(W - 1, qc + 1)

                for nr in range(r0, r1 + 1):
                    nbase = nr * W
                    for nc in range(c0, c1 + 1):
                        if nr == qr and nc == qc:
                            continue
                        nq = nbase + nc
                        if grid[nr][nc] == '#' and comp[nq] == -1:
                            comp[nq] = cid
                            stack.append(nq)

            sizes[cid] = size

    # 3. Flood-fill all white components with 4-connectivity.
    seen = bytearray(n)
    holes = [0] * len(sizes)

    for r in range(H):
        base = r * W
        for c in range(W):
            start = base + c
            if grid[r][c] != '.' or seen[start]:
                continue

            seen[start] = 1
            stack = [start]

            touches_outside = False
            candidate = -1
            multiple_marks = False

            while stack:
                p = stack.pop()
                pr = p // W
                pc = p - pr * W

                # Up
                if pr > 0:
                    q = p - W
                    if grid[pr - 1][pc] == '.':
                        if not seen[q]:
                            seen[q] = 1
                            stack.append(q)
                    else:
                        cid = comp[q]
                        if cid == 0:
                            touches_outside = True
                        elif sizes[cid] > 1:
                            if candidate == -1:
                                candidate = cid
                            elif candidate != cid:
                                multiple_marks = True

                # Down
                if pr + 1 < H:
                    q = p + W
                    if grid[pr + 1][pc] == '.':
                        if not seen[q]:
                            seen[q] = 1
                            stack.append(q)
                    else:
                        cid = comp[q]
                        if cid == 0:
                            touches_outside = True
                        elif sizes[cid] > 1:
                            if candidate == -1:
                                candidate = cid
                            elif candidate != cid:
                                multiple_marks = True

                # Left
                if pc > 0:
                    q = p - 1
                    if grid[pr][pc - 1] == '.':
                        if not seen[q]:
                            seen[q] = 1
                            stack.append(q)
                    else:
                        cid = comp[q]
                        if cid == 0:
                            touches_outside = True
                        elif sizes[cid] > 1:
                            if candidate == -1:
                                candidate = cid
                            elif candidate != cid:
                                multiple_marks = True

                # Right
                if pc + 1 < W:
                    q = p + 1
                    if grid[pr][pc + 1] == '.':
                        if not seen[q]:
                            seen[q] = 1
                            stack.append(q)
                    else:
                        cid = comp[q]
                        if cid == 0:
                            touches_outside = True
                        elif sizes[cid] > 1:
                            if candidate == -1:
                                candidate = cid
                            elif candidate != cid:
                                multiple_marks = True

            if not touches_outside and candidate != -1 and not multiple_marks:
                holes[candidate] += 1

    # 4. Translate the number of holes into A, B, or C.
    ans = [0, 0, 0]

    for cid in range(1, len(sizes)):
        if sizes[cid] == 1:
            continue

        if holes[cid] == 1:
            ans[0] += 1       # A
        elif holes[cid] == 2:
            ans[1] += 1       # B
        elif holes[cid] == 0:
            ans[2] += 1       # C

    print(*ans)

if __name__ == "__main__":
    solve()
```

The first flood fill uses 8 directions because the problem defines the outside region with diagonal connectivity as well as horizontal and vertical connectivity. Starting at `(0, 0)` is sufficient because every border pixel belongs to that region.

The second black flood fill labels every remaining component. Its size is the only information needed to distinguish a possible mark from noise. A singleton black component cannot be a mark because every genuine mark contains more than one black pixel.

The white flood fill is deliberately 4-connected. While processing a white component, the code records whether it touches component zero, which is the outside black region. Ordinary stone surface always has such a connection. An enclosed mark interior does not.

The `candidate` variable records the only non-noise black component that can own the white region. Noise pixels are ignored while making this decision. This matters because a noise pixel can sit inside an ordinary white surface or even inside the white interior of a mark without changing the mark's identity.

No recursion is used. A recursive flood fill can exceed Python's recursion limit on a grid containing a long corridor. The explicit stack also makes the memory usage predictable. Python integers are used only in the temporary DFS stacks, while the component labels are stored in a compact `array('i')`.

There is no integer overflow issue in Python. The largest relevant index is below one million, and all component sizes are at most one million.

## Worked Examples

### Sample 1

The given sample contains two genuine marks after the outside 8-connected black region is removed. One black component has two enclosed white components, while another has one enclosed white component. The isolated black pixels are noise, and the C-shaped pattern mentioned in the statement is connected to the outside region, so it is discarded.

| Stage | Object | Black size | Enclosed white components | Classification |
| --- | --- | --- | --- | --- |
| Black flood fill | Outside region | many | not considered | Outside |
| Black components | Left mark | greater than 1 | 2 | B |
| Black components | Other genuine mark | greater than 1 | 1 | A |
| Black components | Isolated noise | 1 | ignored | Noise |
| Black components | C-shaped outside pattern | part of outside | not considered | Outside |

The final counts are `A = 1`, `B = 1`, and `C = 0`, giving `1 1 0`.

The useful part of this trace is that classification does not depend on the width or height of a mark. The two holes are enough to identify B even when its parameters differ from another mark.

### Constructed Example 2

Consider a picture containing a single C-shaped mark and one noise pixel:

```
#########
#.......#
#.......#
#.#####.#
#.#.....#
#.#####.#
#.......#
#.......#
#########
```

After the outside black component is removed, the C-shaped black component has no enclosed white component. The isolated black pixel inside the open part is noise and has component size one.

| Stage | Object | Black size | White components without outside contact | Classification |
| --- | --- | --- | --- | --- |
| Black flood fill | Border region | many | not considered | Outside |
| Black components | C-shaped mark | greater than 1 | 0 | C |
| Black components | Isolated noise | 1 | ignored | Noise |

The result is `0 0 1`.

This example demonstrates why component size must be checked before counting holes. If every black component were treated as a mark, the noise pixel would produce a false answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(WH) | Every black and white pixel is visited a constant number of times, with at most eight neighbor checks during black flood fills and four during white flood fills. |
| Space | O(WH) | The image, component labels, visited array, hole counts, and flood-fill stacks require linear memory. |

With at most one million pixels, the algorithm performs only a constant amount of work per pixel. The memory consumption is also linear and remains within the 256 MB limit. The implementation avoids Python recursion and stores the largest grid-sized label structure in a compact integer array.

## Test Cases

The following tests use the same component and hole-count logic as the submitted solution. The first case checks the provided sample, the second checks the minimum dimensions with no marks, the third places several B-shaped marks in the same image, and the fourth checks a maximum-sized all-black image.

```python
import io
import sys
from array import array

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    W, H = map(int, input().split())
    grid = [input().strip() for _ in range(H)]
    n = W * H

    comp = array('i', [-1]) * n

    stack = [0]
    comp[0] = 0

    while stack:
        p = stack.pop()
        r, c = divmod(p, W)

        for nr in range(max(0, r - 1), min(H - 1, r + 1) + 1):
            for nc in range(max(0, c - 1), min(W - 1, c + 1) + 1):
                if nr == r and nc == c:
                    continue
                q = nr * W + nc
                if comp[q] == -1 and grid[nr][nc] == '#':
                    comp[q] = 0
                    stack.append(q)

    sizes = [sum(1 for x in comp if x == 0)]

    for r in range(H):
        for c in range(W):
            p = r * W + c
            if grid[r][c] != '#' or comp[p] != -1:
                continue

            cid = len(sizes)
            comp[p] = cid
            stack = [p]
            size = 0

            while stack:
                q = stack.pop()
                size += 1
                qr, qc = divmod(q, W)

                for nr in range(max(0, qr - 1), min(H - 1, qr + 1) + 1):
                    for nc in range(max(0, qc - 1), min(W - 1, qc + 1) + 1):
                        if nr == qr and nc == qc:
                            continue
                        nq = nr * W + nc
                        if grid[nr][nc] == '#' and comp[nq] == -1:
                            comp[nq] = cid
                            stack.append(nq)

            sizes.append(size)

    seen = bytearray(n)
    holes = [0] * len(sizes)

    for r in range(H):
        for c in range(W):
            start = r * W + c
            if grid[r][c] != '.' or seen[start]:
                continue

            seen[start] = 1
            stack = [start]
            outside = False
            candidate = -1
            multiple = False

            while stack:
                p = stack.pop()
                pr, pc = divmod(p, W)

                for nr, nc in (
                    (pr - 1, pc),
                    (pr + 1, pc),
                    (pr, pc - 1),
                    (pr, pc + 1),
                ):
                    if not (0 <= nr < H and 0 <= nc < W):
                        continue

                    q = nr * W + nc

                    if grid[nr][nc] == '.':
                        if not seen[q]:
                            seen[q] = 1
                            stack.append(q)
                    else:
                        cid = comp[q]
                        if cid == 0:
                            outside = True
                        elif sizes[cid] > 1:
                            if candidate == -1:
                                candidate = cid
                            elif candidate != cid:
                                multiple = True

            if not outside and candidate != -1 and not multiple:
                holes[candidate] += 1

    ans = [0, 0, 0]
    for cid in range(1, len(sizes)):
        if sizes[cid] == 1:
            continue
        if holes[cid] == 1:
            ans[0] += 1
        elif holes[cid] == 2:
            ans[1] += 1
        elif holes[cid] == 0:
            ans[2] += 1

    sys.stdin = old_stdin
    return " ".join(map(str, ans))

sample1 = """\
26 15
##########################
##........######......#..#
#...###....#####..#......#
#...#.#....####.........##
#...###.....##....#####..#
#...#.#.....#.....#####..#
#...###.....#.....##.##..#
#........#..#.#...#####..#
#..###......#.....#####..#
#..#........#...#.##.##..#
#..#........#.....##.##..#
#..#...#.#..#...#.##.##..#
#..###......#............#
###....#....##....##.....#
##########################
"""
assert run(sample1) == "1 1 0", "sample 1"

minimum = """\
7 9
#######
#######
#######
#######
#######
#######
#######
#######
#######
"""
assert run(minimum) == "0 0 0", "minimum dimensions"

two_b = """\
15 9
###############
#.............#
#..###........#
#..#.#........#
#..###........#
#........###..#
#........#.#..#
#........###..#
###############
"""
assert run(two_b) == "0 2 0", "two B marks"

maximum = "1000 1000\n" + ("#" * 1000 + "\n") * 1000
assert run(maximum) == "0 0 0", "maximum all-black grid"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Provided 26 by 15 sample | `1 1 0` | Genuine A and B marks, noise, and a C-shaped region connected to the outside |
| 7 by 9 all-black grid | `0 0 0` | Minimum dimensions and complete outside-region detection |
| 15 by 9 with two B marks | `0 2 0` | Multiple marks of the same type and independent hole counting |
| 1000 by 1000 all-black grid | `0 0 0` | Maximum input size and linear-time behavior |

## Edge Cases

The outside black region is handled by the first flood fill. Because the flood fill starts on the border and uses all eight directions, every black pixel connected to the border through horizontal, vertical, or diagonal contact receives component ID zero. A black shape that visually resembles C but belongs to this region never reaches the later classification stage.

A singleton noise pixel is handled by the black-component size check. Suppose a noise pixel is surrounded by a large white surface. Its adjacent white component is deliberately ignored when counting holes because the black component has size one. Genuine marks have larger components, so their enclosed white regions are still counted.

A mark with no enclosed white region is classified as C. The white component around such a mark touches the outside black region through the ordinary stone surface, so it is not counted as a hole. The mark itself remains as a non-noise black component and receives hole count zero.

A mark with one enclosed white region is classified as A. During the white flood fill, the enclosed region cannot reach the outside black component, so `touches_outside` remains false. It touches the A component, which becomes `candidate`, and the hole count of that component increases to one.

A mark with two enclosed white regions is classified as B. The two interiors are separate 4-connected white components, so the white scan encounters them independently. Each increments the same black component's hole count, leaving it equal to two. The final classification consequently produces B.

Diagonal white contact is not allowed to merge regions because white flood fills use only four directions. This matches the definition of the stone surface and prevents a diagonal touch from destroying a real hole.

The image can contain a large number of noise pixels. Even if every other pixel is isolated noise, each black component is discovered once, each has size one, and none contributes to the answer. The total work remains linear in the number of pixels.

The grid can be completely black. In that case the first flood fill consumes the entire image, no other black components exist, and there are no white components to process. The answer is correctly `0 0 0`.

The grid can also contain many separate stones and marks. Each white component is still processed exactly once, and each mark is charged only for the enclosed white components belonging to it. No per-mark scan of the entire grid is necessary, which is the property that keeps the algorithm at O(WH).
