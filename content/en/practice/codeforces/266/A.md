---
title: "CF 266A - Stones on the Table"
description: "We are given a row of stones, each painted one of three colors. The goal is to remove as few stones as possible so that after removals, no two adjacent stones share the same color."
date: "2026-06-04T18:07:18+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 266
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 163 (Div. 2)"
rating: 800
weight: 266
solve_time_s: 61
verified: true
draft: false
---

[CF 266A - Stones on the Table](https://codeforces.com/problemset/problem/266/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of stones, each painted one of three colors. The goal is to remove as few stones as possible so that after removals, no two adjacent stones share the same color.

In other words, we want to take the original string of characters and delete characters until every remaining pair of consecutive characters differs. The order of the remaining stones must stay unchanged, so we are not reordering, only removing elements.

The input size is very small, with at most 50 stones. This means even a straightforward linear scan or even more expensive reasoning would work comfortably within time limits. Any solution up to quadratic complexity is effectively instantaneous here, but the structure of the problem suggests something simpler exists.

A naive mistake here is to think about rearranging or counting frequencies. For example, given `RRG`, someone might think that because there are two R's, one must always be removed regardless of position. That is correct in this case, but frequency alone is not sufficient in general because adjacency matters.

Another common incorrect approach is to attempt to "balance" colors globally, for example trying to alternate R, G, B in some fixed pattern. This fails on inputs like `RGRGRG`, where no removals are needed even though any rigid pattern assumption might incorrectly remove valid stones.

A correct solution must depend only on local adjacency, not global distribution.

## Approaches

The brute-force idea is to simulate removals by trying all subsets of stones and checking which subsets satisfy the condition that no two adjacent stones are equal. For each subset, we verify validity in linear time. Since there are $2^n$ subsets, this leads to $O(n \cdot 2^n)$ time complexity. Even with $n = 50$, this becomes astronomically large, making it infeasible.

The key observation is that we do not need to choose which stones to keep globally. Instead, we can decide greedily from left to right whether a stone must be removed based only on its relationship with the previous kept stone.

The structure of the problem is a classic local constraint reduction: the validity condition depends only on adjacent kept elements. This means once we fix what we keep up to position $i-1$, the decision at position $i$ is fully determined by whether it matches the last kept color.

This reduces the problem from combinatorial selection to a single pass filtering process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot 2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Start with a counter set to zero, representing how many stones are removed.
2. Track the last kept stone color. Initially, this is undefined because no stones have been processed yet.
3. Scan the string from left to right, processing one stone at a time.
4. For each stone, compare its color with the last kept color. If it is the same, this stone must be removed because keeping it would violate the adjacency rule.
5. If it differs from the last kept color, we keep it and update the last kept color to the current one.
6. Continue until the end of the string, accumulating the number of removed stones.

### Why it works

At any point in the scan, the kept sequence is guaranteed to satisfy the condition that no two adjacent stones are equal. This is maintained because we only append a stone when it differs from the last kept one. If it matches, removing it is always safe because it cannot help future decisions: keeping it would only introduce an invalid adjacency with no benefit, since all future checks depend only on the most recently kept stone, not any earlier ones. This establishes a greedy invariant that the kept prefix is always optimal for its length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()
    
    removed = 0
    last = None
    
    for c in s:
        if c == last:
            removed += 1
        else:
            last = c
    
    print(removed)

if __name__ == "__main__":
    solve()
```

The code maintains a single variable `last` representing the most recently kept stone. When the current character matches `last`, it is discarded and counted as a removal. Otherwise, it becomes the new `last`. This directly implements the greedy rule from the algorithm walkthrough in one pass.

The important subtlety is initialization: `last = None` ensures the first character is always kept, since it cannot match anything before it. There are no boundary issues beyond this, since every comparison is safe and uniform.

## Worked Examples

### Example 1

Input:

```
3
RRG
```

| i | stone | last before | action | removed | last after |
| --- | --- | --- | --- | --- | --- |
| 1 | R | None | keep | 0 | R |
| 2 | R | R | remove | 1 | R |
| 3 | G | R | keep | 1 | G |

This shows that only consecutive duplicates are removed, while valid transitions are preserved.

### Example 2

Input:

```
5
RGBBB
```

| i | stone | last before | action | removed | last after |
| --- | --- | --- | --- | --- | --- |
| 1 | R | None | keep | 0 | R |
| 2 | G | R | keep | 0 | G |
| 3 | B | G | keep | 0 | B |
| 4 | B | B | remove | 1 | B |
| 5 | B | B | remove | 2 | B |

This confirms that only repeated adjacent blocks are collapsed into a single representative.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Single left-to-right scan over the string |
| Space | $O(1)$ | Only one tracking variable is used |

With $n \le 50$, the algorithm is trivial in terms of performance, but the linear scan structure is still the cleanest formulation and scales beyond constraints if needed.

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

# provided sample
assert run("3\nRRG\n") == "1"

# all distinct, no removals
assert run("4\nRGBR\n") == "0"

# all same
assert run("5\nRRRRR\n") == "4"

# alternating pattern
assert run("6\nRGRGRG\n") == "0"

# single element
assert run("1\nB\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| RGRGRG | 0 | no removals needed |
| RRRRR | 4 | full collapse of duplicates |
| B | 0 | minimum edge case |

## Edge Cases

For a single stone like `B`, the algorithm sets `last = None`, keeps the stone, and produces zero removals. There are no comparisons that trigger deletion, which matches the requirement since a single element is always valid.

For a fully uniform string like `RRRRR`, the first `R` is kept and every subsequent character equals `last`, so each is counted as removed. The scan never updates `last`, which ensures the result is exactly $n-1$, consistent with keeping one representative of a maximal identical block.

For alternating strings such as `RGRGRG`, every character differs from `last`, so nothing is removed. The invariant that only equal-adjacent pairs are invalid ensures this structure is already optimal, and the algorithm preserves all elements correctly.
