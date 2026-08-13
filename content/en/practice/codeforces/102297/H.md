---
title: "CF 102297H - Reach for the Stars"
description: "The stamp is a fixed axis-aligned cross consisting of five cells: the center cell and its four orthogonally adjacent cells. A stamping turns those five paper cells black."
date: "2026-08-13T22:44:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102297
codeforces_index: "H"
codeforces_contest_name: "UCF Locals 2015"
rating: 0
weight: 102297
solve_time_s: 112
verified: true
draft: false
---

[CF 102297H - Reach for the Stars](https://codeforces.com/problemset/problem/102297/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

The stamp is a fixed axis-aligned cross consisting of five cells: the center cell and its four orthogonally adjacent cells. A stamping turns those five paper cells black. Since black ink stays black after another stamping, overlapping stamps are allowed, but a stamp can never touch a cell that is supposed to remain white.

The task is to find the smallest number of such cross placements whose union is exactly the set of black cells. If the picture is already completely white, the answer is zero. If some black cell cannot be covered by any legal stamp, the answer is impossible.

Each image has at most 9 rows and 9 columns. The Codeforces page currently gives a 2.5 second time limit and 256 MB memory limit. The grid is tiny in absolute size, but there can be up to 49 possible stamp centers in a 9 by 9 image. That makes trying every subset of stamp positions exponential in the number of cells that can hold a stamp, not merely exponential in the grid width.

The first useful observation is that a stamp center can only be an interior cell, because all four arms must remain inside the paper. A legal center must also have `#` at all five cells occupied by the cross. Once those conditions hold, placing the stamp is always safe. This lets us separate the problem into choosing legal stamp centers and making sure their union covers every black cell.

There are several edge cases that defeat simpler implementations. A one-cell black image cannot be stamped:

```
1
1 1
#
```

The correct output is `Image #1: impossible`, because the stamp cannot fit inside a 1 by 1 paper.

An empty image needs no stamp at all:

```
1
1 1
.
```

The answer is `Image #1: 0`. A search that insists on finding a stamp would incorrectly declare this impossible.

A black corner is also impossible to cover. For example,

```
1
3 3
###
###
###
```

is impossible. The only possible stamp center in a 3 by 3 paper is the middle cell, and its cross does not contain either corner. A careless solution that only checks whether every chosen stamp is safe could accept this image without checking that every black cell is covered.

There is another subtle case where a legal stamp exists but is not enough. For

```
1
3 3
.#.
###
.#.
```

the center cross is a legal stamp and covers every black cell, so the answer is exactly 1. Checking only for the existence of legal centers would not be sufficient for larger images, because all black cells still have to be covered.

## Approaches

The most direct brute-force approach is to identify every legal stamp position and try every subset of those positions. For every subset, we could construct the resulting black cells, compare them with the target, and keep the smallest subset.

This is correct because every possible stamping sequence can be represented by the set of positions that were stamped. Repeating the same position never helps, since a second stamping changes no cell. However, a 9 by 9 board has 7 by 7, or 49, possible stamp centers. In the worst case there can be a legal stamp at every one of them, giving `2^49 = 562,949,953,421,312` subsets. Even if checking one subset took only a few operations, this is far beyond the available time.

The key structure that makes the problem manageable is that every stamp affects only one row and its two neighboring rows. Inside its own row, it affects three consecutive columns. That means when processing the image row by row, the coverage of the current row depends only on the stamp choices in the previous, current, and next rows.

Because there are at most 9 columns, we can represent all stamp centers selected in one row by a bitmask. A stamp center can only occur in one of the `c - 2` interior columns, so there are at most `2^7 = 128` possible masks for one row.

Suppose the previous row uses mask `prev`, the current row uses mask `cur`, and the next row uses mask `nxt`. The current row receives vertical coverage from `prev` and `nxt`. It receives horizontal coverage from `cur`, because every selected center also colors the cell immediately to its left and right. If `horizontal[cur]` denotes

`cur | (cur << 1) | (cur >> 1)`,

then the complete coverage of the current row is

`prev | horizontal[cur] | nxt`.

We can check whether this covers exactly what is needed in the target row. Since every selected center is already known to be a legal stamp, no selected stamp can color a dot. Thus we only need to check that every target `#` is covered.

This gives a dynamic program whose state remembers two consecutive row masks. When we choose the next row mask, the oldest row becomes completely determined and can be checked and discarded. The brute force works because it explicitly considers every set of stamps, but fails when there are many possible centers. The row-local nature of the cross lets us replace the exponential search over 49 positions with a small bitmask dynamic program.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^((r-2)(c-2)) * rc)` | `O(rc)` | Too slow |
| Optimal | `O(r * 2^(3(c-2)))` | `O(2^(2(c-2)))` | Accepted |

With `c <= 9`, the optimal transition bound is at most roughly `9 * 2^21`, which is practical for these tiny grids.

## Algorithm Walkthrough

1. Read the grid and determine which interior cells can serve as stamp centers. A center `(i,j)` is legal exactly when the center and its four neighbors are all `#`. Such a stamp can safely be used because it never creates black ink on a target dot.
2. For every row, build a bitmask `allowed[row]` containing all legal stamp centers in that row. Boundary rows automatically have an empty mask because a stamp cannot be centered there.
3. Generate every submask of `allowed[row]`. Each submask represents one possible choice of which legal stamps to place in that row. The zero mask is included because placing no stamps in a row is a valid choice.
4. Precompute the horizontal coverage for every possible row mask. If `cur` selects some stamp centers, `cur`, `cur << 1`, and `cur >> 1` represent the center cells and their horizontal arms. Their union is exactly the part of the current row colored by stamps centered in that row.
5. Initialize the dynamic program with two empty rows. Conceptually, the row before the image has no stamps and the first image row has no possible stamp centers either, so the initial state is `(prev, cur) = (0, 0)` with cost zero.
6. Process the image from top to bottom. For the current row, choose a mask `nxt` from the possible stamp masks of the next row. The current row is then fully determined, because its vertical coverage comes from `prev` and `nxt`, while its horizontal coverage comes from `cur`.
7. Compute `covered = prev | horizontal[cur] | nxt`. Keep this transition only when every black cell in the current target row is included in `covered`. In bitmask form, the condition is `(covered & target[row]) == target[row]`.
8. Move the dynamic-programming state from `(prev, cur)` to `(cur, nxt)` and add the number of selected stamps in `nxt` to the cost. The number of selected stamps is simply `nxt.bit_count()`.
9. On the last row, force `nxt = 0`. This prevents stamps from being placed outside the paper and gives the final row a complete coverage check.
10. After the last row has been processed, take the minimum cost among all surviving states. If no state survives, the target image is impossible.

### Why it works

The invariant is that a DP state `(prev, cur)` represents every possible choice of stamps up through the current row with exactly the stored minimum number of stamps, while leaving only the next row undecided. When the algorithm chooses `nxt`, every stamp that can affect the current row is now known: they are centered in the previous, current, or next row. Thus the coverage test is exact. A transition is kept precisely when the current row's black cells are all covered, and because every chosen stamp is individually legal, no dot is ever colored. After checking the row, the previous row can be forgotten because no future stamp can reach it. Every valid stamping configuration produces one sequence of row masks considered by the DP, and every DP sequence corresponds to legal stamps, so minimizing the accumulated number of stamps gives the true optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**9

def solve_case(r, c, grid):
    # A stamp center must be strictly inside the grid.
    # allowed[i] contains the columns where a legal stamp can be centered.
    allowed = [0] * r

    for i in range(1, r - 1):
        mask = 0
        for j in range(1, c - 1):
            if (
                grid[i][j] == '#'
                and grid[i - 1][j] == '#'
                and grid[i + 1][j] == '#'
                and grid[i][j - 1] == '#'
                and grid[i][j + 1] == '#'
            ):
                mask |= 1 << j
        allowed[i] = mask

    # Every possible set of stamp centers in a row.
    choices = []
    for mask in allowed:
        row_choices = []
        sub = mask
        while True:
            row_choices.append(sub)
            if sub == 0:
                break
            sub = (sub - 1) & mask
        choices.append(row_choices)

    # Target row as a bitmask.
    target = []
    for row in grid:
        mask = 0
        for j, ch in enumerate(row):
            if ch == '#':
                mask |= 1 << j
        target.append(mask)

    # Horizontal coverage produced by stamps centered in each row.
    full = (1 << c) - 1
    horizontal = [0] * (1 << c)
    for mask in range(1 << c):
        horizontal[mask] = (
            mask
            | ((mask << 1) & full)
            | (mask >> 1)
        )

    # dp[(prev, cur)] = minimum number of stamps selected so far.
    # Initially both rows contain no stamps.
    dp = {(0, 0): 0}

    for i in range(r):
        ndp = {}

        if i + 1 < r:
            next_choices = choices[i + 1]
        else:
            # Nothing may be centered outside the paper.
            next_choices = [0]

        for (prev, cur), cost in dp.items():
            base = prev | horizontal[cur]

            for nxt in next_choices:
                covered = base | nxt

                # Every '#' in this row must be covered.
                if (covered & target[i]) != target[i]:
                    continue

                new_cost = cost + nxt.bit_count()
                state = (cur, nxt)

                old = ndp.get(state, INF)
                if new_cost < old:
                    ndp[state] = new_cost

        dp = ndp

        if not dp:
            return None

    return min(dp.values()) if dp else None

def solve():
    t = int(input())

    out = []

    for case in range(1, t + 1):
        r, c = map(int, input().split())
        grid = [input().strip() for _ in range(r)]

        answer = solve_case(r, c, grid)

        if answer is None:
            result = "impossible"
        else:
            result = str(answer)

        out.append(f"Image #{case}: {result}")
        out.append("")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part of `solve_case` identifies legal stamp centers. The five-cell test is deliberately done before the dynamic program, because once a center passes it, every future use of that center is guaranteed not to create an unwanted black cell.

The `allowed` mask uses the actual column number as the bit position. This makes the horizontal shifts line up directly with the grid columns, so there is no conversion between compressed and original column indices. Since legal centers are only at columns `1` through `c - 2`, shifting their masks left or right stays inside the paper.

The `choices` construction enumerates every subset of legal centers for each row. This is not enumerating arbitrary subsets of all columns. In the worst case there are only seven possible center columns, so a row has at most 128 choices.

The target rows are also represented as masks. The expression `(covered & target[i]) == target[i]` checks coverage without caring whether a black cell was covered once or several times. This matches the physical stamping process, where repeated black ink is indistinguishable from a single layer.

The dynamic-programming state contains exactly two row masks. `prev` supplies the downward arm of stamps centered above the current row, `cur` supplies the centers and horizontal arms in the current row, and `nxt` supplies the upward arm of stamps centered below it. Once the current row has been checked, `prev` is no longer needed.

There is no integer-overflow issue in Python, and the largest mask uses only nine bits. The `INF` value is much larger than the maximum possible number of useful stamps, which is 49.

The last transition explicitly uses `[0]` for `nxt`. Without this boundary condition, the DP could conceptually use a stamp centered below the paper to cover a cell in the last row, which would violate the requirement that the whole stamp remain inside the paper.

## Worked Examples

The first sample image is a 1 by 1 paper containing only a dot. There is no reason to place a stamp, and in fact no stamp can fit. The DP starts with empty masks and immediately verifies that the empty coverage satisfies the empty target row.

| Row | `prev` | `cur` | `nxt` | Target | Coverage | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | `0` | `0` | `0` | `0` | `0` | `0` |

The transition survives because the target contains no black cells. The final minimum is zero, giving `Image #1: 0`. This demonstrates why an empty picture must be treated as a valid zero-stamp solution.

The second sample image is a single black cell. Again there is only one row, so there can be no legal stamp center. The target bitmask contains one bit, but the only possible coverage is zero.

| Row | `prev` | `cur` | `nxt` | Target | Coverage | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | `0` | `0` | `0` | `1` | `0` | not valid |

The coverage test fails because `(0 & 1) != 1`. No DP state survives, so the result is `impossible`. This confirms that the algorithm distinguishes an empty target from a target containing an uncovered black cell.

For the third sample, the 3 by 3 cross has exactly one legal center.

```
.#.
###
.#.
```

The only possible stamp mask is the center bit. The first row has no possible center, so the DP chooses the center as `nxt` while checking the top row. The center's upward arm covers the only black cell in that row.

| Row | `prev` | `cur` | `nxt` | Target | Coverage | Cost |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | `0` | `0` | center | center | center | `1` |
| 1 | `0` | center | `0` | left, center, right | left, center, right | `1` |
| 2 | center | `0` | `0` | center | center | `1` |

After all three rows are checked, the single selected center covers every black cell. The answer is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(r * 2^(3(c-2)))` | At most `2^(c-2)` masks for each of three consecutive rows are considered in the worst case |
| Space | `O(2^(2(c-2)))` | A state stores two row masks, with at most `2^(c-2)` possibilities for each |

For `r,c <= 9`, there are at most seven possible stamp-center columns in a row. The DP consequently works with at most 128 masks per row and at most 16,384 two-row states. Even the worst transition bound is small enough for the 2.5 second limit and uses only a small fraction of the 256 MB memory limit.

## Test Cases

```python
import sys
import io

INF = 10**9

def solve_case(r, c, grid):
    allowed = [0] * r

    for i in range(1, r - 1):
        mask = 0
        for j in range(1, c - 1):
            if (
                grid[i][j] == '#'
                and grid[i - 1][j] == '#'
                and grid[i + 1][j] == '#'
                and grid[i][j - 1] == '#'
                and grid[i][j + 1] == '#'
            ):
                mask |= 1 << j
        allowed[i] = mask

    choices = []
    for mask in allowed:
        row_choices = []
        sub = mask
        while True:
            row_choices.append(sub)
            if sub == 0:
                break
            sub = (sub - 1) & mask
        choices.append(row_choices)

    target = []
    for row in grid:
        mask = 0
        for j, ch in enumerate(row):
            if ch == '#':
                mask |= 1 << j
        target.append(mask)

    full = (1 << c) - 1
    horizontal = [0] * (1 << c)
    for mask in range(1 << c):
        horizontal[mask] = (
            mask
            | ((mask << 1) & full)
            | (mask >> 1)
        )

    dp = {(0, 0): 0}

    for i in range(r):
        ndp = {}
        next_choices = choices[i + 1] if i + 1 < r else [0]

        for (prev, cur), cost in dp.items():
            base = prev | horizontal[cur]

            for nxt in next_choices:
                covered = base | nxt

                if (covered & target[i]) != target[i]:
                    continue

                state = (cur, nxt)
                new_cost = cost + nxt.bit_count()

                if new_cost < ndp.get(state, INF):
                    ndp[state] = new_cost

        dp = ndp

        if not dp:
            return None

    return min(dp.values()) if dp else None

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for case in range(1, t + 1):
        r, c = map(int, input().split())
        grid = [input().strip() for _ in range(r)]

        ans = solve_case(r, c, grid)
        value = "impossible" if ans is None else str(ans)

        out.append(f"Image #{case}: {value}")
        out.append("")

    sys.stdout.write("\n".join(out))

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

sample_input = """5
1 1
.
1 1
#
3 3
.#.
###
.#.
3 5
.#.#.
#####
.#.#.
4 7
.##.#..
######.
.######
..#..#.
"""

sample_output = """Image #1: 0

Image #2: impossible

Image #3: 1

Image #4: 2

Image #5: 5

"""

assert run(sample_input) == sample_output, "provided samples"

assert run("""1
1 1
.
""") == """Image #1: 0

""", "minimum-size empty image"

assert run("""1
1 1
#
""") == """Image #1: impossible

""", "minimum-size black image"

assert run("""1
3 3
###
###
###
""") == """Image #1: impossible

""", "corner cells cannot be covered"

assert run("""1
3 3
.#.
###
.#.
""") == """Image #1: 1

""", "single legal stamp"

max_empty = "9 9\n" + "\n".join(["........."] * 9) + "\n"
assert run("1\n" + max_empty) == """Image #1: 0

""", "maximum-size empty image"
```

The first custom case checks the smallest possible paper and verifies that an entirely white image needs zero stamps. The second uses the same dimensions with one black cell, testing the distinction between an empty target and an impossible target. The third catches the common mistake of checking only whether stamps themselves are legal, because the 3 by 3 all-black grid has a legal center but leaves its corners uncovered. The fourth is the smallest nontrivial valid stamping and checks the central boundary conditions. The fifth exercises the maximum 9 by 9 dimensions while keeping the answer trivially zero, which also checks mask creation and DP behavior at the largest allowed input size.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` with `.` | `Image #1: 0` | Minimum dimensions and empty target |
| `1 1` with `#` | `Image #1: impossible` | Stamp cannot fit |
| `3 3` with all `#` | `Image #1: impossible` | Uncoverable corners |
| `3 3` cross | `Image #1: 1` | Exact single-stamp solution |
| `9 9` with all `.` | `Image #1: 0` | Maximum dimensions and zero-mask handling |

## Edge Cases

For a completely white image, every target row has mask zero. The DP can always choose zero stamps, and every row passes the coverage test because `(0 & 0) == 0`. For example,

```
1
1 1
.
```

produces `Image #1: 0`. No special case is required in the implementation because the empty set of stamps is naturally represented by the zero mask.

For a black image smaller than the stamp, there are no legal center positions. Consider

```
1
1 1
#
```

The `allowed` array contains only zero. The only DP state has zero coverage, but the target contains one black bit, so the coverage test rejects it. The final state set is empty and the answer becomes `impossible`.

A black corner is never covered by the cross because the stamp has no diagonal cells. In

```
1
3 3
###
###
###
```

the center is legal, but its coverage is

```
.#.
###
.#.
```

The corner bits remain absent. When the DP checks the first row, the selected center can cover only the middle bit, so the target mask is not contained in the coverage mask. The configuration is rejected before it can reach the last row.

A valid center also requires all five stamp cells to be black. For example,

```
1
3 3
...
.#.
...
```

has a black center but no legal stamp, because placing the cross would color four dots. The center is not added to `allowed`, so the DP has no way to use it and correctly reports `impossible`.

Overlapping stamps require no special treatment. In the 3 by 5 sample,

```
.#.#.
#####
.#.#.
```

two crosses can be centered at the two interior black columns. Some cells are covered by both stamps, but the target only cares whether a cell is black at least once. The bitwise union used by the DP naturally removes any distinction between one and multiple coverings, and the minimum is 2.

The final-row boundary is handled by forcing `nxt` to zero. Without that restriction, a transition could use a hypothetical center below the paper whose upward arm covers a target cell in the last row. The same principle is already applied at the top through the initial zero state, so no stamp is ever allowed to extend beyond either vertical boundary.
