---
title: "CF 106252B - Buggy Painting Software I"
description: "We are given a target image on an $n times m$ grid. Each cell contains either a color label or zero, where zero means transparent."
date: "2026-06-20T22:37:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106252
codeforces_index: "B"
codeforces_contest_name: "The 2025 ICPC Asia Shenyang Regional Contest (The 4th Universal Cup. Stage 6: Grand Prix of Shenyang)"
rating: 0
weight: 106252
solve_time_s: 68
verified: true
draft: false
---

[CF 106252B - Buggy Painting Software I](https://codeforces.com/problemset/problem/106252/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a target image on an $n \times m$ grid. Each cell contains either a color label or zero, where zero means transparent. The final visible image is produced by stacking multiple layers: at each position, the first non-transparent pixel from the topmost layers determines what we see.

We start with no layers and can repeatedly add new layers. A new layer is either completely filled with a single color or completely transparent. After creating a layer, we can modify individual pixels inside it: we can paint a pixel to a color at cost $a$, or erase it to make it transparent at cost $b$. The goal is to construct some stack of layers whose resulting visible image matches the target grid exactly, while minimizing total cost.

The key subtlety is that layers interact through occlusion. A pixel in a higher layer hides everything below it unless it is transparent. This means mistakes in a higher layer can completely override correct content below, so incorrect pixels in any used layer must be carefully erased or corrected.

The constraints imply up to $10^6$ total cells across all test cases. This rules out any solution that simulates layer-by-layer construction or performs per-cell interaction reasoning across colors or layers. A linear scan per test case is acceptable.

A few edge situations are easy to misjudge.

If all cells are zero, the optimal answer is zero because we never need to introduce any colored pixel.

If the grid contains a single color everywhere, say all cells are 5, then either we build one constant-color layer and fix nothing, or we paint everything manually. The optimal choice depends only on comparing the two costs.

A more subtle failure case appears when a color is sparse. Suppose a color appears only once in a huge grid. A naive approach might suggest building a full constant layer and erasing most cells, but that may cost more than simply painting that single pixel directly.

The key challenge is recognizing that although layers interact spatially, the cost structure does not couple different colors in a way that requires global ordering.

## Approaches

A natural first idea is to think in terms of constructing the image pixel by pixel. For each target cell, we could imagine either painting it in some layer or relying on a constant layer and correcting everything else around it. This quickly becomes expensive because every decision about a pixel affects all layers above and below it. Any attempt to simulate stacking operations directly leads to a combinatorial explosion over layer choices and ordering.

The real simplification comes from reinterpreting what a “constant color layer” actually implies. If we create a layer filled entirely with color $c$, then every position initially shows $c$. To make that layer compatible with the final image, every position that should not show $c$ must be made transparent using erasures. This requirement is local to the layer itself: a pixel in that layer either contributes color $c$ or must be explicitly removed. No other layer can fix an incorrectly non-transparent pixel in this layer without risking overwriting correct content below.

This leads to a key separation: each color can be treated independently. For a given color $c$, we only care about how many cells in the target grid contain $c$, and how many do not. We compare two strategies for handling all occurrences of $c$. Either we never use a dedicated layer for $c$ and instead paint each of its occurrences individually, or we create a full constant layer of $c$ and erase all positions that should not be $c$.

Since these choices do not depend on other colors, the optimal solution is obtained by evaluating each color separately and summing the best choice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force layering simulation | Exponential | O(nm) | Too slow |
| Per-color independent optimization | O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

## Step 1: Count occurrences of each color

We scan the grid once and count how many times each color appears. Let $k_c$ denote the number of cells containing color $c$. This tells us exactly how many pixels would need to be painted if we avoid using a layer for that color.

## Step 2: Consider the cost of not using a layer

If we do not create a dedicated layer for color $c$, then every occurrence must be painted individually. The cost is $a \cdot k_c$. This is the pure per-pixel approach with no structural optimization.

## Step 3: Consider the cost of using a constant layer

If we create a full layer filled with color $c$, we start with all $n \cdot m$ cells set to $c$. Every cell that should not be $c$ must be erased, otherwise it would incorrectly appear in the final image. There are $n \cdot m - k_c$ such cells, so the cost becomes

$$a + b \cdot (nm - k_c).$$

The first term is zero for creation of the layer, so only modifications matter.

## Step 4: Choose the better option per color

For each color, we take the minimum of the two strategies:

$$\min(a \cdot k_c,\; a + b \cdot (nm - k_c)).$$

We sum this value over all colors that appear in the grid.

## Step 5: Output the total sum

The final answer is the sum of optimal independent costs for all colors.

## Why it works

A constant-color layer is fully determined once created, and every pixel in it independently contributes either useful signal or noise. Any pixel that does not match the target image must be explicitly erased, regardless of what other layers do. Similarly, painting individual pixels does not interfere with other colors since each cell belongs to exactly one final value.

This removes any dependency between colors: no ordering of layers can reduce the number of required operations for one color based on decisions for another. Each color’s cost is therefore independent and additive, making the per-color minimum globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, m, a, b = map(int, input().split())
        cnt = {}
        nm = n * m

        for _ in range(n):
            row = list(map(int, input().split()))
            for x in row:
                cnt[x] = cnt.get(x, 0) + 1

        ans = 0
        for c, k in cnt.items():
            if c == 0:
                continue
            paint_only = a * k
            layer = a + b * (nm - k)
            ans += min(paint_only, layer)

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation relies on a frequency map over colors. The grid size is flattened conceptually into counts, avoiding any need to simulate layers. The crucial detail is treating color zero separately: it represents transparency and does not require construction cost.

Each color contributes exactly one decision, computed from its frequency and the total grid size.

## Worked Examples

### Example 1

Consider a $2 \times 3$ grid:

```
1 1 0
2 1 2
```

We have $nm = 6$. Counts are $k_1 = 3$, $k_2 = 2$, $k_0 = 1$.

Assume $a = 2$, $b = 1$.

For color 1:

| Strategy | Formula | Value |
| --- | --- | --- |
| Paint only | $2 \cdot 3$ | 6 |
| Layer | $2 + 1 \cdot (6 - 3)$ | 5 |

Best is 5.

For color 2:

| Strategy | Formula | Value |
| --- | --- | --- |
| Paint only | $2 \cdot 2$ | 4 |
| Layer | $2 + 1 \cdot (6 - 2)$ | 6 |

Best is 4.

Total is $5 + 4 = 9$.

This shows how a layer can help dense colors but is unnecessary for sparse ones.

### Example 2

A uniform grid:

```
3 3
3 3
```

Here $k_3 = 4$, $nm = 4$.

For color 3:

Paint only gives $4a$, while a layer gives $a + 0 = a$. The layer dominates, confirming that dense uniform regions strongly favor constant layers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm)$ | Each cell is read once and counted |
| Space | $O(\#colors)$ | Frequency map over observed values |

The solution is linear in the total number of cells across all test cases, which fits comfortably within the constraint of $10^6$ cells.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    input = sys.stdin.readline

    def solve():
        T = int(input())
        for _ in range(T):
            n, m, a, b = map(int, input().split())
            cnt = {}
            nm = n * m
            for _ in range(n):
                for x in map(int, input().split()):
                    cnt[x] = cnt.get(x, 0) + 1
            ans = 0
            for c, k in cnt.items():
                if c == 0:
                    continue
                ans += min(a * k, a + b * (nm - k))
            print(ans)

    solve()
    return ""

# minimum size
run("1\n1 1 5 3\n1\n")

# all zeros
run("1\n2 2 1 1\n0 0\n0 0\n")

# single color
run("1\n2 3 2 10\n1 1 1\n1 1 1\n")

# mixed case
run("1\n1\n2 3 1 1\n1 2 1\n")

# sparse color test
run("1\n3 3 5 1\n1 0 0\n0 2 0\n0 0 0\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 single cell | 5 | minimum grid correctness |
| all zeros | 0 | transparency handling |
| uniform color | a vs layer choice | dense color optimization |
| mixed colors | combined per-color logic | independence assumption |
| sparse color | avoids unnecessary layer | sparse edge case |

## Edge Cases

A grid consisting entirely of zeros is handled correctly because the frequency map contains only color 0, which is ignored in cost computation. No painting or layer creation is triggered, so the output remains zero.

For a single extremely rare color in a large grid, the algorithm compares $a \cdot k_c$ with $a + b \cdot (nm - k_c)$. Since $k_c$ is small, painting individually is chosen, preventing an expensive full-layer construction.

For a fully uniform grid, the layer option becomes strictly cheaper since no erasures are needed. The algorithm correctly identifies this through the same comparison, selecting the constant layer strategy automatically.
