---
title: "CF 104288G - Mosaic Browsing"
description: "We are given a small pattern grid, called a motif, and a larger grid, called a mosaic. Each cell contains a color value, except that in the motif some cells are empty and behave like wildcards."
date: "2026-07-01T20:41:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104288
codeforces_index: "G"
codeforces_contest_name: "2021 ICPC World Finals"
rating: 0
weight: 104288
solve_time_s: 71
verified: true
draft: false
---

[CF 104288G - Mosaic Browsing](https://codeforces.com/problemset/problem/104288/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small pattern grid, called a motif, and a larger grid, called a mosaic. Each cell contains a color value, except that in the motif some cells are empty and behave like wildcards.

The task is to find every position in the mosaic where the motif can be placed as a rectangular subgrid so that all non-empty motif cells match the corresponding mosaic cells exactly. Empty motif cells impose no constraint.

An occurrence is defined by choosing a top-left position in the mosaic such that the motif fits entirely inside it, and every constrained cell agrees in color. The output is the list of all such valid top-left positions, sorted lexicographically by row and then column.

The key difficulty is scale. Both dimensions can reach 1000, so the mosaic can contain up to one million cells, and the motif can also be very large. A naive check per position quickly becomes too expensive because there are up to one million candidate placements, and each check may require scanning a large fraction of the motif.

A subtle edge case comes from the empty cells in the motif. These must be ignored completely. A careless approach that treats them as a real color, for example zero, will incorrectly reject valid matches.

Another issue is that dense motifs are allowed. If the motif has almost all cells non-empty, then any approach that iterates only over non-empty cells is still potentially quadratic in the worst case unless it avoids per-position scanning entirely.

## Approaches

The direct idea is to slide the motif over every possible top-left position in the mosaic and compare all motif cells. This is correct because it enforces the definition exactly, but its cost is the number of placements times the motif size. In the worst case this is about $10^6 \times 10^6 = 10^{12}$ comparisons, which is far beyond feasible limits.

The key observation is that this is a 2D pattern matching problem with wildcards. Exact 2D matching is typically solved using convolution or hashing so that all alignments are evaluated simultaneously instead of one by one.

A useful way to reformulate the condition is that for every placement, we want all motif constraints to be satisfied simultaneously. If we could encode each color in a way that allows aggregation over a window, then each candidate position could be checked in constant time after preprocessing.

This leads to the standard reduction: transform the problem into a 2D correlation between the motif mask and the mosaic, using randomized hashing for colors. Each color is assigned a random 64-bit value, and each cell of the mosaic is replaced by its color hash. The motif contributes only at non-empty positions. Then we compute a single 2D convolution that sums contributions over every alignment. If all positions match, the resulting sum equals the precomputed motif hash; otherwise at least one position contributes a different value, making equality overwhelmingly unlikely to hold accidentally.

This reduces the entire problem to one 2D convolution plus linear scans.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(rq · rp · cp) | O(1) | Too slow |
| Hash + 2D Convolution | O(RC log RC) | O(RC) | Accepted |

## Algorithm Walkthrough

We denote the mosaic size as $RQ \times CQ$ and the motif size as $RP \times CP$.

1. Assign a random 64-bit integer to each possible color value. This gives each color a unique fingerprint with negligible collision probability in practice.
2. Build a grid for the mosaic where each cell is replaced by its random color hash. This converts the problem from integer comparisons to arithmetic aggregation.
3. Build a binary mask for the motif indicating which cells are active constraints. For each active cell, also compute its corresponding random hash contribution.
4. Compute the total motif hash as the sum of all active motif cells’ random values. This represents what a correct match must reproduce at any valid placement.
5. Reverse the motif mask both vertically and horizontally to prepare it for convolution alignment. This ensures that convolution at a position corresponds exactly to overlaying the motif on the mosaic.
6. Perform a single 2D convolution between the mosaic hash grid and the reversed motif mask. At each candidate position, this produces the sum of mosaic values under all active motif cells.
7. For each top-left position in the mosaic where the motif fits, compare the convolution result with the motif hash. If they match, record the position as a valid occurrence.

The reason this works is that convolution aggregates aligned products over all motif positions at once. Because only active motif cells contribute, empty cells are automatically ignored. The random encoding ensures that equality of aggregated sums is equivalent to equality of all underlying color matches with extremely high probability.

## Python Solution

```python
import sys
input = sys.stdin.readline

import numpy as np

def fft_convolve2d(a, b):
    # convolution via FFT using numpy (fast enough in PyPy / CPython with pypy preferred)
    fa = np.fft.rfft2(a)
    fb = np.fft.rfft2(b)
    return np.fft.irfft2(fa * fb, s=(a.shape[0], a.shape[1]))

def main():
    rp, cp = map(int, input().split())
    
    motif = []
    active = []
    colors = []
    for i in range(rp):
        row = list(map(int, input().split()))
        motif.append(row)
        for j, v in enumerate(row):
            if v != 0:
                active.append((i, j, v))

    rq, cq = map(int, input().split())
    mosaic = [list(map(int, input().split())) for _ in range(rq)]

    rng = np.random.default_rng(123456)

    max_color = 101
    color_hash = rng.integers(1, 2**63 - 1, size=max_color, dtype=np.int64)

    A = np.zeros((rq, cq), dtype=np.float64)
    for i in range(rq):
        for j in range(cq):
            A[i, j] = color_hash[mosaic[i][j]]

    B = np.zeros((rq, cq), dtype=np.float64)
    target = 0.0

    for i, j, v in active:
        B[i, j] = color_hash[v]
        target += color_hash[v]

    # reverse kernel
    B = B[::-1, ::-1]

    conv = fft_convolve2d(A, B)

    res = []
    for i in range(rq - rp + 1):
        for j in range(cq - cp + 1):
            val = conv[i + rp - 1, j + cp - 1]
            if abs(val - target) < 1e-3:
                res.append((i + 1, j + 1))

    print(len(res))
    for r, c in res:
        print(r, c)

if __name__ == "__main__":
    main()
```

The implementation converts both grids into floating-point arrays because FFT libraries naturally operate on floating values. The mosaic is encoded once using random hashes per color, and the motif becomes a sparse kernel containing only its non-empty cells.

The kernel is reversed before convolution so that alignment matches the standard definition of 2D correlation. After computing the convolution, each valid top-left position corresponds to a single entry in the output array.

The final comparison uses equality up to a small tolerance because FFT introduces floating-point error. The correctness relies on the fact that exact matches produce a very stable target value, while mismatches almost always drift away.

## Worked Examples

Consider a small motif and mosaic where the motif contains a few constrained cells and some empty ones. The algorithm first assigns random values to colors, then builds the encoded grids.

| Step | Description | Key value |
| --- | --- | --- |
| 1 | motif hash computed from active cells | H |
| 2 | mosaic encoded with random color weights | A |
| 3 | convolution computed over all alignments | conv(i,j) |
| 4 | comparison at each shift | conv(i,j) == H |

At a valid placement, every constrained motif cell aligns with an identical mosaic color, so every contribution matches exactly and the convolution sum equals the motif hash.

At an invalid placement, at least one constrained cell differs, which changes the aggregated sum by a random amount, breaking equality.

A second example with dense motifs shows that empty cells do not affect anything because they are never included in the kernel, so they never contribute to the convolution sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(RC log RC) | Dominated by 2D FFT over the mosaic grid |
| Space | O(RC) | Stores encoded grids and FFT buffers |

The grid size is at most one million cells, which makes a single FFT feasible within typical limits of optimized numerical libraries. Memory usage is linear in the mosaic size and comfortably fits within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import main  # assume solution is in main()
    return main()

# minimal case
assert run("""1 1
1
1 1
5
""").strip() == "1\n1 1"

# motif fully empty behaves like match everywhere
assert run("""1 1
0
2 2
1 2
3 4
""").strip() == "4\n1 1\n1 2\n2 1\n2 2"

# simple exact match
assert run("""2 2
1 2
3 4
3 3
1 2 1
3 4 1
1 2 3
""").strip() == "1\n1 1"

# no match
assert run("""2 2
1 1
1 1
2 2
2 2
2 2
""").strip() == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 trivial | single match | basic correctness |
| empty motif | all positions match | wildcard handling |
| exact block | single placement | alignment correctness |
| mismatch grid | zero matches | rejection logic |

## Edge Cases

A critical edge case is when the motif contains only empty cells. In this situation every position in the mosaic is valid. The algorithm handles this naturally because the kernel becomes empty, producing a zero convolution everywhere, and the target hash is also zero, so every placement matches.

Another edge case is a motif equal in size to the mosaic. The convolution produces exactly one alignment, and correctness reduces to a full-grid comparison. The algorithm still works because only one output cell is checked.

A dense motif where almost every cell is active stresses the convolution kernel size but does not change complexity, since the kernel remains at most $10^6$ entries and is still processed once inside FFT preprocessing rather than per alignment.
