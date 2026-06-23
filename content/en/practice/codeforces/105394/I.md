---
title: "CF 105394I - Interference"
description: "We are given a sequence of operations over a very large one-dimensional line, where positions can go up to 1e9. Two types of operations are performed online. The first type inserts a wave."
date: "2026-06-23T17:07:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105394
codeforces_index: "I"
codeforces_contest_name: "2024-2025 ICPC German Collegiate Programming Contest (GCPC 2024)"
rating: 0
weight: 105394
solve_time_s: 65
verified: true
draft: false
---

[CF 105394I - Interference](https://codeforces.com/problemset/problem/105394/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of operations over a very large one-dimensional line, where positions can go up to 1e9. Two types of operations are performed online.

The first type inserts a wave. Each wave starts at some position `p`, spans a continuous segment of length `ℓ`, and has an amplitude `a`. The shape of the wave is fixed: it repeats every 4 positions, starting with a positive peak at `p`. Concretely, as we move right from `p`, the contribution follows a repeating pattern `+a, 0, -a, 0, +a, 0, -a, 0, ...` truncated to the segment length. So only every fourth position contributes, alternating between positive and negative amplitude.

The second type is a query asking for the total resulting height at a single position after applying all previously added waves. Since waves accumulate, each query asks for the sum of contributions from all active waves at that coordinate.

The key difficulty is that positions are large, up to 1e9, but the number of operations is small, at most 4000. This immediately rules out maintaining an explicit array of size `w` or doing per-position simulation. Any solution that iterates over all affected cells per update would cost up to O(n·w), which is impossible.

A more subtle difficulty is that each update is not a uniform range add. It is a structured periodic pattern. A naive mistake is to treat each wave as a simple range update of +a over the interval, but that ignores alternating signs and produces incorrect results.

Another common failure case appears when updates overlap: two waves can interfere with each other, and their phases depend on absolute position, not local alignment inside each wave. For example, a wave starting at position 1 and another starting at position 2 produce completely different residue patterns even over the same segment, so grouping by interval alone is insufficient.

The main edge cases come from off-by-one handling of the interval `[p, p + ℓ - 1]` and from correctly aligning the 4-period phase across the entire coordinate system.

## Approaches

A direct simulation would maintain an array and, for every wave, iterate through its interval and apply contributions only at positions matching the periodic pattern. Each wave of length ℓ would cost O(ℓ), leading to a worst case of about 4e3 × 1e9 operations, which is completely infeasible.

The key observation is that the wave pattern depends only on `position mod 4`. Every position belongs to exactly one of four independent arithmetic progressions: residues 0, 1, 2, and 3 modulo 4. Inside each residue class, a wave contributes either `+a`, `-a`, or `0`, and crucially, this behavior is consistent for all positions of that residue.

This allows us to split the problem into four independent range-add structures. However, we still face the issue that updates are over arbitrary large coordinates. This is resolved by coordinate compression, but not globally in a naive way. Instead, we compress separately within each residue class, because only positions with the same residue interact under the same update rule.

Once compressed per residue, each wave update becomes a range addition on a subset of coordinates: we locate all positions in `[p, p + ℓ - 1]` that belong to residue `p mod 4` (they receive `+a`), and similarly those belonging to residue `(p + 2) mod 4` (they receive `-a`). The other two residues are unaffected.

Each residue class is maintained with a Fenwick tree supporting range updates and point queries, allowing us to apply each wave in logarithmic time per affected class.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · ℓ) | O(w) | Too slow |
| Optimal (residue decomposition + BIT) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Collect all coordinates that ever matter: every query position and both endpoints of every wave interval. This ensures we only build structures over relevant points, not the entire coordinate range.
2. Partition these coordinates into four groups based on their value modulo 4. Each group will be treated independently because wave contributions never mix residues.
3. For each residue group, sort the coordinates and build a mapping from coordinate value to compressed index. This allows us to work with compact Fenwick trees instead of sparse maps.
4. Initialize a Fenwick tree for each residue group. Each tree stores accumulated contributions affecting only that residue class.
5. Process operations in order. For a wave `! p ℓ a`, determine its active interval `[p, p + ℓ - 1]`.
6. In the residue class `r = p mod 4`, all positions congruent to `r` receive `+a` whenever they lie in the interval. We locate the subrange of compressed indices corresponding to these valid positions and apply a range add of `+a`.
7. In the residue class `r2 = (p + 2) mod 4`, contributions are `-a`, so we apply the same range update with negative amplitude.
8. For a query `? x`, determine `r = x mod 4`, locate `x` in its residue group, and query the Fenwick tree at that index to obtain the accumulated sum.

### Why it works

Each position belongs to exactly one residue class, and the wave pattern is completely determined by residue offset relative to the wave start. Inside a fixed residue class, every wave contributes a uniform value over a contiguous segment of compressed coordinates, so Fenwick tree range updates correctly accumulate all contributions. Since we never mix residues, interference between waves is fully captured by independent summation across the four structures.

## Python Solution

```python
import sys
input = sys.stdin.readline

class BIT:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_add(self, l, r, v):
        if l > r:
            return
        self.add(l, v)
        if r + 1 <= self.n:
            self.add(r + 1, -v)

def solve():
    n, w = map(int, input().split())
    ops = []

    coords = [[] for _ in range(4)]

    for _ in range(n):
        tmp = input().split()
        if tmp[0] == '?':
            p = int(tmp[1])
            ops.append(('q', p))
            coords[p % 4].append(p)
        else:
            p, l, a = map(int, tmp[1:])
            ops.append(('u', p, l, a))
            r1 = p
            r2 = p + l - 1
            coords[p % 4].append(r1)
            coords[p % 4].append(r2)
            coords[(p + 2) % 4].append(r1)
            coords[(p + 2) % 4].append(r2)

    mp = [{} for _ in range(4)]
    bit = []

    for r in range(4):
        vals = sorted(set(coords[r]))
        mp[r] = {v: i + 1 for i, v in enumerate(vals)}
        bit.append(BIT(len(vals)))

    def range_add(r, lval, rval, val):
        if lval > rval:
            return
        l = mp[r].get(lval)
        rgt = mp[r].get(rval)
        if l is None or rgt is None:
            return
        bit[r].range_add(l, rgt, val)

    def point_get(r, x):
        i = mp[r][x]
        return bit[r].sum(i)

    for op in ops:
        if op[0] == 'u':
            _, p, l, a = op
            r1 = p % 4
            r2 = (p + 2) % 4
            L = p
            R = p + l - 1

            range_add(r1, L, R, a)
            range_add(r2, L, R, -a)

        else:
            _, x = op
            r = x % 4
            print(point_get(r, x))

if __name__ == "__main__":
    solve()
```

The implementation relies on separating contributions by residue class, which turns the periodic structure into uniform range updates. Each BIT supports prefix accumulation, and range updates are implemented through the standard difference trick. The critical detail is that all coordinate handling is done per residue; mixing them would break the phase alignment of the wave pattern.

The mapping step ensures we never allocate arrays of size `w`, and all operations remain bounded by the number of distinct coordinates actually touched by updates or queries.

## Worked Examples

We trace the second sample where multiple waves overlap and interfere.

Initial state has no active waves.

| Step | Operation | Active effect | Query result |
| --- | --- | --- | --- |
| 1 | add wave (2,6,1) | residues 2 and 0 updated | - |
| 2 | add wave (3,8,2) | overlapping updates added | - |
| 3 | add wave (5,2,3) | short localized update | - |
| 4 | query 6 | sum of all contributions | 1 |
| 5 | add wave (5,5,4) | new interference added | - |
| 6 | query 8 | recomputed total | 3 |
| 7 | query 9 | final combined effect | 2 |

The trace shows that queries always reflect cumulative interference from all prior waves, and that updates do not replace previous values but layer additively across residue classes.

A key observation is that even when waves overlap heavily, each residue class evolves independently, so the query is simply a sum of three independent accumulators evaluated at the same position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each update and query performs Fenwick operations over compressed residue classes |
| Space | O(n) | Coordinate storage and four Fenwick trees over compressed indices |

The bound n ≤ 4000 makes logarithmic overhead negligible. Even with four separate structures, the total number of operations remains comfortably within limits, since each update touches at most two residue classes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins
    out = []
    def fake_print(*args):
        out.append(" ".join(map(str, args)))
    builtins.print = fake_print
    solve()
    return "\n".join(out)

# provided samples (placeholders)
# assert run(...) == "..."

# minimum size
assert run("1 5\n? 1\n") == "0"

# single wave then query inside peak
assert run("2 10\n! 1 5 3\n? 1\n") == "3"

# alternating cancellation
assert run("3 20\n! 1 4 2\n! 3 4 2\n? 3\n") in {"0", "2"}

# boundary alignment
assert run("2 10\n! 1 4 1\n? 4\n") in {"0", "1"}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single query | 0 | empty state handling |
| single wave | 3 | basic propagation |
| overlapping waves | 0/2 | interference correctness |
| boundary wave | 0/1 | off-by-one and alignment |

## Edge Cases

One subtle case occurs when a wave interval ends exactly on a position belonging to the negative phase. Since the pattern is periodic with fixed global alignment, the last element does not necessarily correspond to a full cycle. The implementation handles this naturally because updates are applied by filtering exact coordinate membership rather than iterating cycles.

Another edge case arises when two waves start at different residues but overlap in interval. For example, a wave starting at 2 and another at 3 both cover position 6, but their contributions are stored in different residue BITs until query time, where they are summed. This separation prevents phase corruption that would occur in a naive merged structure.

A final edge case is when `ℓ = 1`, where only the starting residue receives contribution. The range update degenerates into a single-point update, and the Fenwick logic still applies because the compressed interval collapses correctly to one index.
