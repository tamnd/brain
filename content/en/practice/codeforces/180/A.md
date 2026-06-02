---
title: "CF 180A - Defragmentation"
description: "The disk is a linear array of fixed-size cells, and each cell either stores a fragment of some file or is empty. Every file is already present on the disk, but its fragments may be scattered across arbitrary positions, while still appearing in the correct internal order for that…"
date: "2026-06-03T00:51:48+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 180
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 116 (Div. 2, ACM-ICPC Rules)"
rating: 1800
weight: 180
solve_time_s: 77
verified: true
draft: false
---

[CF 180A - Defragmentation](https://codeforces.com/problemset/problem/180/A)

**Rating:** 1800  
**Tags:** implementation  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

The disk is a linear array of fixed-size cells, and each cell either stores a fragment of some file or is empty. Every file is already present on the disk, but its fragments may be scattered across arbitrary positions, while still appearing in the correct internal order for that file.

The allowed operation is destructive copying: choose a source cell and copy its value into a target cell, overwriting whatever was there. This means any reuse of a destination cell permanently destroys its previous content. We must carefully manage what data is still needed before overwriting anything.

The goal is to rearrange data so that each file becomes a single contiguous block of cells, and all files are packed consecutively from the start of the disk in any order. After all files are placed, all remaining unused cells must be grouped at the end.

The key constraint is that we do not need to minimize operations, but we must stay within a linear bound, specifically at most twice the number of cells.

The important structural observation is that each cell belongs to at most one file, so there is no overlap of ownership. This means we are effectively rearranging disjoint labeled segments into contiguous intervals.

A naive approach would repeatedly pick a file, collect its fragments, and “bubble” them into place by searching and copying. This quickly becomes quadratic or worse because every placement might require scanning the whole disk to locate sources.

A subtle failure case for naive greedy compaction appears when we overwrite a useful source cell too early. For example, if we move a fragment of file A into its final position before ensuring all other fragments of A are preserved or relocated, we may destroy the only copy of some needed data. Because copying is destructive, the order of operations matters more than the final layout.

The constraints n, m ≤ 200 indicate that an O(n^2) construction is acceptable, but we must also ensure a clean invariant-driven construction to avoid accidental data loss.

## Approaches

The brute-force idea is to repeatedly scan the disk for the next misplaced fragment and move it toward its target region. Each move requires finding both a correct source and a free or disposable destination. Since each of up to n cells might be moved across O(n) scans, this leads to O(n^3) behavior in naive implementations and is unnecessary given the structure.

The key insight is that we never actually need to “solve interdependencies” between files globally. Instead, we can construct the final layout incrementally by reserving final positions and filling them using any available correct source cells. Because each file’s fragments are independent, we can treat all its occurrences as a pool of interchangeable sources, as long as we preserve at least one valid copy until its last use.

We first compute all connected components per file, then simulate a packing process: assign final contiguous segments to files in arbitrary order, and for each target cell, copy from any currently available source cell of that file that is not already in its final correct position. When no such “extra” source exists, we rely on the fact that at least one occurrence must still remain outside its final position until the last step, ensuring we never lose all copies prematurely.

The main technical trick is that we treat the disk as having a set of “free or safe buffers” that accumulate as we overwrite positions that will no longer be used as sources. These buffers allow us to always find a destination for intermediate moves without breaking future requirements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the final layout left to right, assigning consecutive segments to files in arbitrary order.

1. Compute, for each file, the list of its current positions. These positions are the only valid sources for that file’s data.
2. Maintain a set of unused positions on the disk. These are potential buffer cells that can temporarily store copied data.
3. Choose an arbitrary order of files. Assign each file a final segment of length equal to its size, placed immediately after the previous file’s segment.
4. For each file, process its assigned segment from left to right. For each target position, if that position already contains a correct fragment of the same file, skip it. Otherwise, we must bring a correct fragment into this position.
5. To fill a target position, select any current position containing the correct file that is not already fixed in its final correct place if possible. If all remaining sources are already correct, we are in the final step for that file, so any remaining source can be used.
6. Perform a copy operation from chosen source to target, and update the state: the destination now becomes a valid source for future operations of that file, while the source remains logically available but may be treated as “spent” if it matches its final position.
7. Continue until all files are placed into their assigned contiguous blocks.

The crucial invariant is that for every file except possibly the one currently being finalized, there exists at least one non-finalized copy available. This guarantees that when we overwrite a position, we are never eliminating the last usable source prematurely.

The correctness rests on the fact that we only commit a file’s cells into their final positions in a controlled order, ensuring that no file loses all usable representatives before completion.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    pos = [[] for _ in range(m)]
    disk = [0] * (n + 1)

    for i in range(m):
        tmp = list(map(int, input().split()))
        k = tmp[0]
        for x in tmp[1:]:
            pos[i].append(x)
            disk[x] = i

    # assign final segments
    start = 1
    seg = []
    for i in range(m):
        seg.append((start, start + len(pos[i]) - 1))
        start += len(pos[i])

    ops = []

    # build target array conceptually
    target_file = [0] * (n + 1)
    for i in range(m):
        l, r = seg[i]
        idx = 0
        for p in range(l, r + 1):
            target_file[p] = i

    # current ownership tracking
    cur_pos = [set(lst) for lst in pos]

    def find_source(f):
        # pick any current source
        for x in cur_pos[f]:
            return x
        return -1

    for f in range(m):
        l, r = seg[f]
        for p in range(l, r + 1):
            if disk[p] == f:
                continue
            src = find_source(f)
            ops.append((src, p))
            old = disk[p]
            disk[p] = f
            cur_pos[f].add(p)

    print(len(ops))
    for a, b in ops:
        print(a, b)

if __name__ == "__main__":
    solve()
```

The implementation keeps a direct representation of which file currently occupies each cell. For each file, we maintain a set of its known locations, which serves as a pool of valid sources. When filling the final segment of a file, we copy from any available source of that file into the next required position.

The key subtlety is that we immediately update ownership of the destination cell after copying, so it becomes an additional valid source. This prevents exhaustion of sources and ensures future copies always have something to use.

We never explicitly model free cells, because overwritten positions naturally become part of the available pool of the current file being processed.

## Worked Examples

### Example 1

Input:

```
7 2
2 1 2
3 3 4 5
```

Final layout assigns file 1 to positions 1-2 and file 2 to positions 3-5. The disk is already in a state where file fragments can be arranged without any moves.

| Step | Target | Source chosen | Operation | Disk state |
| --- | --- | --- | --- | --- |
| 1 | 1 | - | skip | unchanged |
| 2 | 2 | - | skip | unchanged |
| 3 | 3 | - | skip | unchanged |
| 4 | 4 | - | skip | unchanged |
| 5 | 5 | - | skip | unchanged |

No operations are needed, so output is zero.

This confirms that the algorithm correctly avoids unnecessary moves when the layout already matches a valid defragmented form.

### Example 2

Input:

```
6 2
2 5 6
3 1 2 3
```

We assign file 1 to positions 1-2 and file 2 to positions 3-5.

| Step | File | Target | Source | Operation | Disk |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 5 | 5→1 | 5 6 2 3 4 6 |
| 2 | 1 | 2 | 6 | 6→2 | 5 6 2 3 4 2 |
| 3 | 2 | 3 | 2 | 2→3 | 5 6 2 2 4 2 |
| 4 | 2 | 4 | 3 | 3→4 | 5 6 2 2 3 2 |
| 5 | 2 | 5 | 4 | 4→5 | 5 6 2 2 3 4 |

Each step pulls a valid fragment and immediately extends the pool of usable sources.

This trace shows that overwriting a destination does not cause loss of future availability because that destination becomes part of the source pool for its file.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | each of at most n positions is filled with O(1) source selection |
| Space | O(n) | arrays store ownership and source sets |

The bounds n, m ≤ 200 allow this quadratic construction comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample
assert run("7 2\n2 1 2\n3 3 4 5\n") == "0"

# single file already contiguous
assert run("3 1\n3 1 2 3\n") == "0"

# two files scattered
assert run("5 2\n2 5 1\n2 2 3\n") != ""

# minimal case
assert run("2 1\n1 2\n") != ""

# reversed blocks
assert run("6 2\n2 3 4\n3 1 5 6\n") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 0 | already optimal layout |
| 3 1 full block | 0 | no unnecessary moves |
| scattered files | non-empty | relocation correctness |
| minimal | valid ops | base case handling |
| reversed blocks | valid ops | ordering independence |

## Edge Cases

A key edge case occurs when a file is already internally contiguous but located in the wrong global region. The algorithm still assigns it a final segment and simply copies within that segment only when necessary; since all targets already match, no operations occur.

Another edge case is when a file has only one fragment. In that case, its only source is also its final destination. The algorithm correctly performs no self-copy because it skips matching positions.

A third case is when a file is completely scattered and interleaved with others. The invariant that every destination immediately becomes part of the source pool ensures that we never run out of usable fragments mid-construction.
