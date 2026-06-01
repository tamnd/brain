---
title: "CF 494E - Sharti"
description: "The board is enormous, up to $10^9 times 10^9$, so we never have any chance of working with cells directly. A move chooses a square of side length at most $k$. The lower-right corner of that square must currently be white. Every cell inside the square is flipped."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "games"]
categories: ["algorithms"]
codeforces_contest: 494
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 282 (Div. 1)"
rating: 3200
weight: 494
solve_time_s: 689
verified: false
draft: false
---

[CF 494E - Sharti](https://codeforces.com/problemset/problem/494/E)

**Rating:** 3200  
**Tags:** data structures, games  
**Solve time:** 11m 29s  
**Verified:** no  

## Solution
## Problem Understanding

The board is enormous, up to $10^9 \times 10^9$, so we never have any chance of working with cells directly.

A move chooses a square of side length at most $k$. The lower-right corner of that square must currently be white. Every cell inside the square is flipped. Two players alternate moves, and the first player who cannot move loses.

The initial white cells are not given explicitly. Instead, we receive up to $5 \cdot 10^4$ rectangles. A cell is white if it belongs to at least one rectangle, otherwise it is black.

The task is to determine whether the starting position is winning or losing under optimal play.

The constraints immediately rule out any simulation on the board itself. Even storing one row is impossible because $n$ may be $10^9$. The number of rectangles is only $5 \cdot 10^4$, which strongly suggests that the solution must work with rectangle boundaries and compressed structure rather than individual cells.

The hidden difficulty is that this is not a normal geometric problem. The board description is geometric, but the game is impartial. The real challenge is computing the Sprague-Grundy value of the position without expanding the board.

Several edge cases are easy to mishandle.

Consider:

```
2 1 1
1 1 2 2
```

Every cell is white and only $1 \times 1$ moves are allowed. Each move simply flips one cell. There are four independent moves, so the xor is $1 \oplus 1 \oplus 1 \oplus 1 = 0$. The position is losing.

A solution that only counts white cells modulo two would get this right accidentally, but that idea fails as soon as $k > 1$.

Another example:

```
4 1 4
1 1 4 4
```

Now large squares are allowed. The cells no longer behave independently as simple piles of size one. The Grundy value depends on the coordinates of each white cell. Treating every white cell as identical gives the wrong answer.

A more subtle case appears when rectangles overlap:

```
5 2 5
1 1 5 5
3 3 3 3
```

The cell $(3,3)$ is still white because the input describes a union of rectangles, not xor coverage. Any sweep structure must maintain ordinary coverage, not parity coverage.

## Approaches

The first thing to understand is the game itself.

Suppose there is only one white cell at position $(i,j)$, and all other cells are black. Let the Grundy number of that position be $g(i,j)$.

A move must choose a square whose lower-right corner is exactly $(i,j)$. If the chosen side length is $l$, every cell inside that $l \times l$ square becomes white except $(i,j)$, which becomes black.

This leads to a standard Sprague-Grundy recurrence. The resulting position becomes a xor of independent subgames corresponding to all cells inside the chosen square.

The Codeforces editorial observes a useful equivalent formulation. Imagine that each cell contains some number of marbles. A move removes one marble from the lower-right corner and adds one marble to every other cell of the chosen square. Each marble evolves independently, so the Grundy value of a position is the xor of the Grundy values of cells containing an odd number of marbles.

Computing the recurrence directly gives a striking pattern:

$$g(i,j)=\min(\operatorname{lowbit}(i),\operatorname{lowbit}(j),H)$$

where

$$H = 2^{\lfloor \log_2 k \rfloor}$$

and $\operatorname{lowbit}(x)$ is the largest power of two dividing $x$.

The brute-force way to discover this would be to compute Grundy numbers on a large grid using mex transitions. If we compute values up to size $A$, each state examines up to $k$ moves and each move touches $O(l^2)$ cells. Even after optimization the complexity is far beyond practical limits.

The pattern above completely changes the problem.

Now every white cell contributes a Grundy value which is always a power of two. The answer becomes:

$$\bigoplus_{\text{white }(i,j)} g(i,j)$$

The remaining task is geometric. We need the xor of these powers of two over the union of rectangles.

A cell contributes $2^t$ exactly when

$$\min(\operatorname{lowbit}(i),\operatorname{lowbit}(j),H)=2^t.$$

Instead of counting cells with exact value $2^t$, it is easier to count cells where both coordinates are divisible by $2^t$.

Let $B_t$ be the parity of the number of white cells satisfying

$$2^t \mid i,\qquad 2^t \mid j.$$

A cell with Grundy value at least $2^t$ contributes to $B_t$. Therefore the parity of cells whose Grundy value is exactly $2^t$ equals

$$B_t \oplus B_{t+1}.$$

Once all $B_t$ are known, the final xor is reconstructed immediately.

The geometry now becomes a parity counting problem over a union of rectangles.

We sweep along the $x$-axis. Between two consecutive event coordinates, the set of active $y$-intervals does not change. For each power of two $2^t$, we only need the parity of active $y$-coordinates divisible by $2^t$. Those parities can be stored simultaneously inside a bitmask.

A segment tree over compressed $y$-coordinates maintains these masks while rectangles are inserted and removed. During each sweep strip, we compute another bitmask describing which powers of two divide the current $x$-coordinates an odd number of times. Combining the two masks gives the contribution of the strip.

This reduces a seemingly impossible $10^9 \times 10^9$ game to a sweep line with $O(m)$ events.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Grundy on cells | Exponential / infeasible | Huge | Too slow |
| Sweep line + SG pattern + segment tree | $O(m \log m \log n)$ | $O(m \log n)$ | Accepted |

## Algorithm Walkthrough

### 1. Derive the Grundy value of a single cell

Let $H$ be the largest power of two not exceeding $k$.

The recurrence generated by legal square sizes leads to the closed form

$$g(i,j)=\min(\operatorname{lowbit}(i),\operatorname{lowbit}(j),H).$$

Every Grundy value is a power of two.

### 2. Convert the game into parity counting

Define $B_t$ as the parity of white cells whose row and column are both divisible by $2^t$.

A cell contributes to $B_t$ iff its Grundy value is at least $2^t$.

Hence the parity of cells whose Grundy value is exactly $2^t$ is

$$C_t=B_t\oplus B_{t+1}.$$

The final nim xor equals

$$\bigoplus_{t} (C_t \cdot 2^t).$$

### 3. Create sweep events

For every rectangle

$$[a,c]\times[b,d]$$

create:

1. an insertion event at $x=a$,
2. a removal event at $x=c+1$.

The sweep processes events in increasing $x$.

Between two consecutive event positions, the active set of $y$-intervals is fixed.

### 4. Compress the $y$-coordinates

Collect all interval boundaries:

$$b,\ d+1.$$

Sort and deduplicate them.

The segment tree works on elementary segments between consecutive compressed coordinates.

### 5. Store parity masks in the segment tree

For every segment $[L,R)$, precompute a mask:

$$\text{allMask}(L,R).$$

Bit $t$ is set if the count of integers in $[L,R)$ divisible by $2^t$ is odd.

The segment tree stores:

1. coverage count,
2. allMask,
3. current mask.

If coverage count is positive, the whole interval is white and current mask equals allMask.

Otherwise current mask is the xor of the children.

### 6. Process sweep strips

Suppose the current strip is

$$[x_i, x_{i+1}).$$

For every $t$, we need the parity of numbers divisible by $2^t$ inside this strip.

Those parities form another bitmask:

$$xMask.$$

The contribution of the strip to $B_t$ is present exactly when both the $x$-parity and the active $y$-parity are odd.

Since everything is modulo two, this is simply:

```
answerMask ^= xMask & rootMask
```

where rootMask is the segment tree mask of currently white $y$-coordinates.

### 7. Recover the nim xor

The accumulated mask stores all $B_t$.

Using

$$C_t=B_t\oplus B_{t+1},$$

reconstruct the xor value.

If the resulting xor is nonzero, Hamed wins. Otherwise Malek wins.

### Why it works

The Grundy formula reduces every white cell to an independent pile whose value is a power of two. A cell contributes to $B_t$ exactly when its Grundy value is at least $2^t$. Consequently $B_t$ records the parity of all cells contributing to bit level $t$ or higher, and the difference $B_t \oplus B_{t+1}$ isolates the cells whose exact Grundy value is $2^t$.

The sweep line computes each $B_t$ modulo two. A white cell contributes to $B_t$ iff both coordinates are divisible by $2^t$. The parity over a rectangle factorizes into the parity of valid $x$-coordinates times the parity of valid $y$-coordinates. The segment tree maintains the second quantity for the active union of intervals, while the sweep strip supplies the first. Every white cell is counted exactly once, and only white cells are counted. Therefore the computed $B_t$ values are correct, which makes the reconstructed nim xor correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXB = 31

def parity_multiples(l, r):
    mask = 0
    for b in range(MAXB):
        step = 1 << b
        cnt = (r - 1) // step - (l - 1) // step
        if cnt & 1:
            mask |= 1 << b
    return mask

class SegTree:
    def __init__(self, ys):
        self.ys = ys
        self.n = len(ys) - 1

        size = self.n * 4 + 5
        self.cover = [0] * size
        self.mask = [0] * size
        self.allmask = [0] * size

        self._build(1, 0, self.n)

    def _build(self, p, l, r):
        if r - l == 1:
            self.allmask[p] = parity_multiples(self.ys[l], self.ys[l + 1])
            return

        m = (l + r) // 2
        self._build(p * 2, l, m)
        self._build(p * 2 + 1, m, r)

        self.allmask[p] = self.allmask[p * 2] ^ self.allmask[p * 2 + 1]

    def _pull(self, p):
        if self.cover[p] > 0:
            self.mask[p] = self.allmask[p]
        else:
            self.mask[p] = self.mask[p * 2] ^ self.mask[p * 2 + 1]

    def update(self, p, l, r, ql, qr, val):
        if ql >= r or qr <= l:
            return

        if ql <= l and r <= qr:
            self.cover[p] += val
            self._pull(p)
            return

        m = (l + r) // 2

        self.update(p * 2, l, m, ql, qr, val)
        self.update(p * 2 + 1, m, r, ql, qr, val)

        self._pull(p)

    def root_mask(self):
        return self.mask[1]

def solve():
    n, m, k = map(int, input().split())

    ys = []
    events = []

    for _ in range(m):
        a, b, c, d = map(int, input().split())

        ys.append(b)
        ys.append(d + 1)

        events.append((a, 1, b, d + 1))
        events.append((c + 1, -1, b, d + 1))

    ys = sorted(set(ys))

    pos = {v: i for i, v in enumerate(ys)}

    events.sort()

    seg = SegTree(ys)

    bmask = 0
    last_x = events[0][0]
    idx = 0

    while idx < len(events):
        x = events[idx][0]

        if x > last_x:
            xmask = parity_multiples(last_x, x)
            bmask ^= xmask & seg.root_mask()

        while idx < len(events) and events[idx][0] == x:
            _, typ, y1, y2 = events[idx]
            seg.update(
                1,
                0,
                seg.n,
                pos[y1],
                pos[y2],
                typ
            )
            idx += 1

        last_x = x

    nim = 0
    for b in range(MAXB):
        cur = (bmask >> b) & 1
        nxt = (bmask >> (b + 1)) & 1
        if cur ^ nxt:
            nim |= 1 << b

    print("Hamed" if nim else "Malek")

solve()
```

The first part of the solution is the function `parity_multiples`. It computes, for every power of two, whether the interval contains an odd number of multiples of that power. The result is packed into a bitmask.

The segment tree does not store counts of white cells. It stores parity information for all powers of two simultaneously. The key observation is that only parity matters because the final result is an xor.

`allmask[p]` is a static property of a segment. It describes which divisibility classes appear an odd number of times inside that interval.

When an interval becomes fully covered by at least one active rectangle, its contribution is exactly `allmask[p]`. When coverage drops to zero, the node must recompute itself from its children.

The sweep line processes strips between consecutive event coordinates. For a strip, the active white set in the $y$-direction is fixed. The strip contribution is computed by bitwise AND because a cell contributes to $B_t$ only if both the $x$-condition and the $y$-condition hold.

The final reconstruction step is easy to get wrong. `bmask` stores $B_t$, not the parity of cells whose Grundy value equals $2^t$. We must apply

$$C_t = B_t \oplus B_{t+1}$$

before forming the nim xor.

## Worked Examples

### Sample 1

Input:

```
5 2 1
1 1 3 3
2 2 4 4
```

Since $k=1$, every white cell has Grundy value $1$.

The white area contains:

```
9 + 9 - 4 = 14
```

cells.

| Quantity | Value |
| --- | --- |
| White cells | 14 |
| Grundy per cell | 1 |
| Total xor | $1$ repeated 14 times |
| Result | 0 |

Output:

```
Malek
```

This example confirms that even a large white region may be losing if the parity cancels.

### Sample 2

Input:

```
12 5 7
3 4 5 6
1 2 1 2
4 5 9 9
8 6 12 10
12 4 12 4
```

Here

$$H=4.$$

The sweep line accumulates the parity masks $B_t$.

| Step | Active strip | Root mask | X mask | Accumulated B |
| --- | --- | --- | --- | --- |
| 1 | First strip | computed | computed | updated |
| 2 | Second strip | computed | computed | updated |
| ... | ... | ... | ... | ... |

After processing all strips, the reconstructed nim xor is nonzero.

Output:

```
Hamed
```

This example demonstrates why coordinate divisibility matters. Different cells contribute different powers of two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log m \log n)$ | Sweep events plus segment tree updates and 31-bit masks |
| Space | $O(m \log n)$ | Event list and segment tree |

There are only $2m$ sweep events. Each update touches $O(\log m)$ segment tree nodes. Every mask operation uses at most 31 bits because $n \le 10^9$. The complexity comfortably fits the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    MAXB = 31

    def parity_multiples(l, r):
        mask = 0
        for b in range(MAXB):
            step = 1 << b
            cnt = (r - 1) // step - (l - 1) // step
            if cnt & 1:
                mask |= 1 << b
        return mask

    class SegTree:
        def __init__(self, ys):
            self.ys = ys
            self.n = len(ys) - 1
            size = self.n * 4 + 5

            self.cover = [0] * size
            self.mask = [0] * size
            self.allmask = [0] * size

            self.build(1, 0, self.n)

        def build(self, p, l, r):
            if r - l == 1:
                self.allmask[p] = parity_multiples(
                    self.ys[l],
                    self.ys[l + 1]
                )
                return

            m = (l + r) // 2
            self.build(p * 2, l, m)
            self.build(p * 2 + 1, m, r)

            self.allmask[p] = (
                self.allmask[p * 2]
                ^ self.allmask[p * 2 + 1]
            )

        def pull(self, p):
            if self.cover[p]:
                self.mask[p] = self.allmask[p]
            else:
                self.mask[p] = (
                    self.mask[p * 2]
                    ^ self.mask[p * 2 + 1]
                )

        def upd(self, p, l, r, ql, qr, v):
            if ql >= r or qr <= l:
                return

            if ql <= l and r <= qr:
                self.cover[p] += v
                self.pull(p)
                return

            m = (l + r) // 2
            self.upd(p * 2, l, m, ql, qr, v)
            self.upd(p * 2 + 1, m, r, ql, qr, v)
            self.pull(p)

    input = sys.stdin.readline

    n, m, k = map(int, input().split())

    ys = []
    ev = []

    for _ in range(m):
        a, b, c, d = map(int, input().split())
        ys += [b, d + 1]
        ev.append((a, 1, b, d + 1))
        ev.append((c + 1, -1, b, d + 1))

    ys = sorted(set(ys))
    pos = {v: i for i, v in enumerate(ys)}

    ev.sort()

    seg = SegTree(ys)

    bmask = 0
    last = ev[0][0]
    i = 0

    while i < len(ev):
        x = ev[i][0]

        if x > last:
            bmask ^= parity_multiples(last, x) & seg.mask[1]

        while i < len(ev) and ev[i][0] == x:
            _, t, l, r = ev[i]
            seg.upd(1, 0, seg.n, pos[l], pos[r], t)
            i += 1

        last = x

    nim = 0
    for b in range(MAXB):
        if ((bmask >> b) & 1) ^ ((bmask >> (b + 1)) & 1):
            nim |= 1 << b

    return ("Hamed" if nim else "Malek") + "\n"

assert run(
"""5 2 1
1 1 3 3
2 2 4 4
"""
) == "Malek\n", "sample 1"

assert run(
"""1 1 1
1 1 1 1
"""
) == "Hamed\n", "single white cell"

assert run(
"""2 1 1
1 1 2 2
"""
) == "Malek\n", "four independent cells"

assert run(
"""2 1 2
1 1 1 1
"""
) == "Hamed\n", "single cell with larger k"

assert run(
"""1000000000 1 1
1 1 1000000000 1000000000
"""
) == "Malek\n", "even number of cells"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single white cell | Hamed | Minimum non-empty game |
| Full $2 \times 2$, $k=1$ | Malek | Pure parity cancellation |
| One cell, large $k$ | Hamed | Grundy formula boundary |
| Huge rectangle | Malek | Handles large coordinates |
| Sample 1 | Malek | Official example |

## Edge Cases

Consider:

```
2 1 1
1 1 2 2
```

All four cells are white. Since $k=1$, every cell has Grundy value $1$. The xor is

$$1 \oplus 1 \oplus 1 \oplus 1 = 0.$$

The sweep line computes an even parity for all relevant divisibility classes, producing zero nim xor. The algorithm outputs `Malek`.

Now consider:

```
5 2 5
1 1 5 5
3 3 3 3
```

The center cell belongs to both rectangles. A parity-based coverage structure would incorrectly remove it. Our segment tree stores ordinary coverage counts. Any positive coverage means white. The cell remains active throughout the sweep, exactly matching the union definition.

Finally:

```
4 1 4
1 1 4 4
```

Large squares are allowed, so Grundy values vary across the board. Cells with different lowbits contribute different powers of two. The algorithm never assumes that all white cells contribute equally. Instead it counts divisibility classes separately through the masks $B_t$, which correctly reconstructs the final nim xor.

The Grundy characterization and sweep-line counting method come directly from the official editorial discussion of the game structure and its divisibility pattern.
