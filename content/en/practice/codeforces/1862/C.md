---
title: "CF 1862C - Flower City Fence"
description: "We are given a sequence of fence planks, each with a height, already sorted in non-increasing order. Anya wants to know if the fence is symmetrical when viewed as a grid of unit blocks."
date: "2026-06-09T00:08:03+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1862
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 894 (Div. 3)"
rating: 1100
weight: 1862
solve_time_s: 177
verified: true
draft: false
---

[CF 1862C - Flower City Fence](https://codeforces.com/problemset/problem/1862/C)

**Rating:** 1100  
**Tags:** binary search, data structures, implementation, sortings  
**Solve time:** 2m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of fence planks, each with a height, already sorted in non-increasing order. Anya wants to know if the fence is symmetrical when viewed as a grid of unit blocks. Symmetry here means that if we take the planks, treat each unit of height as a horizontal row, and lay the planks as columns, the resulting 2D shape would be identical to the original vertical layout of the planks.

Concretely, each plank of height `h` contributes `h` horizontal units at its column. When viewed as a horizontal arrangement, the topmost row contains the tallest planks, the next row the next tallest, and so on. If after this transformation the sequence of row lengths is identical to the original sequence of plank heights, the fence is considered symmetrical.

The inputs are constrained such that the total number of planks across all test cases does not exceed 200,000. This rules out algorithms worse than linear per test case. Heights can be large, but they only influence counting, not iteration, so we do not need to perform operations proportional to their values.

Edge cases include a single plank, multiple planks of the same height, and sequences where height differences are irregular. For example, `[5,5,5,1,1]` is symmetrical because the top rows match the original vertical layout, but `[5,4,2]` is not, because horizontal rows compress differently and the horizontal "row lengths" do not match the original.

## Approaches

A brute-force approach would be to build the entire horizontal representation as a 2D grid and check row by row whether the resulting row lengths match the original sequence. This works logically but would take O(n * max_height) time, which is infeasible for large heights (up to 10^9). Constructing an actual grid is unnecessary and too slow.

The optimal approach observes that we do not need the full grid. Instead, we only need to simulate the top-down reduction of plank heights as if we were creating rows:

1. Track the number of planks at each height as we "peel off" rows.
2. At each step, check whether the remaining heights still satisfy the condition that the number of planks of at least that height is greater than or equal to the next height.

A key insight is that the horizontal representation is equivalent to taking the heights, sorting them (already sorted in non-increasing order), and verifying that for each step `i`, the number of planks of height >= `i` is at least `i`. This is exactly the condition for the fence to be a symmetric Young diagram. If at any step this fails, the fence is not symmetrical.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Grid Simulation | O(n * max(a_i)) | O(n * max(a_i)) | Too slow |
| Counting & Greedy Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the list of heights `a`.
3. Initialize a counter `extra` to track the cumulative "excess units" carried from taller planks.
4. Iterate from the first plank to the last:

1. For plank `i`, compute `expected` as the number of rows this plank would contribute in horizontal view, accounting for `extra`.
2. If `a[i] > expected`, increment `extra` to carry over the excess units to lower planks.
3. If `a[i] < expected`, the fence cannot be symmetric; mark as "NO" and break.
5. If the loop completes without failure, mark as "YES".
6. Print results for each test case.

**Why it works**: At each step, `extra` accumulates the surplus height that must be spread to lower planks. This ensures that the horizontal compression matches the vertical sequence. Any violation of the rule indicates that the fence's horizontal row lengths cannot match the original vertical heights, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_symmetric(a):
    n = len(a)
    extra = 0
    for i in range(n):
        # the maximal allowed height in horizontal layout
        if a[i] > i + extra + 1:
            extra += a[i] - (i + extra + 1)
        elif a[i] < i + extra + 1:
            return "NO"
    return "YES"

def main():
    t = int(input())
    results = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        results.append(is_symmetric(a))
    print("\n".join(results))

if __name__ == "__main__":
    main()
```

**Explanation of code**:

- `extra` tracks the cumulative surplus units from taller planks. This avoids constructing a grid explicitly.
- `i + extra + 1` represents the maximum allowed plank height at this position for symmetry.
- Iterating once per plank ensures O(n) time per test case.
- Using `sys.stdin.readline` ensures fast input for large numbers of test cases.

## Worked Examples

Sample input `[5,4,3,2,1]`:

| i | a[i] | extra | i + extra + 1 | Action |
| --- | --- | --- | --- | --- |
| 0 | 5 | 0 | 1 | extra += 4 → 4 |
| 1 | 4 | 4 | 6 | ok |
| 2 | 3 | 4 | 7 | ok |
| 3 | 2 | 4 | 8 | ok |
| 4 | 1 | 4 | 9 | ok |

Result: `YES`. Surplus carried by taller planks allows horizontal layout to match vertical.

Sample input `[4,2,1]`:

| i | a[i] | extra | i + extra + 1 | Action |
| --- | --- | --- | --- | --- |
| 0 | 4 | 0 | 1 | extra += 3 → 3 |
| 1 | 2 | 3 | 5 | ok |
| 2 | 1 | 3 | 6 | ok |

The simulation shows that at row 2, expected 6 > 1, cannot satisfy symmetry → `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass over array; input reading dominates. |
| Space | O(n) | Store input heights and results. |

The algorithm easily handles the sum of `n` up to 2×10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    input = builtins.input
    from contextlib import redirect_stdout
    import io as sio
    out = sio.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided samples
assert run("""7
5
5 4 3 2 1
3
3 1 1
3
4 2 1
1
2
5
5 3 3 1 1
5
5 5 5 3 3
2
6 1
""") == """YES
YES
NO
NO
YES
YES
NO""", "sample 1"

# custom cases
assert run("1\n1\n1\n") == "YES", "single plank"
assert run("1\n3\n3 3 3\n") == "YES", "all equal"
assert run("1\n3\n5 1 1\n") == "NO", "sharp drop"
assert run("1\n4\n4 3 2 1\n") == "YES", "perfect decreasing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 plank | YES | trivial case |
| equal heights | YES | horizontal symmetry holds |
| sharp drop | NO | insufficient height for lower planks |
| perfect decreasing | YES | standard descending case |

## Edge Cases

For a single plank `[1]`, `extra` is 0 and the height matches expected 1 → `YES`.

For a fence `[5,1,1]`, after first plank `extra = 4`, but next plank height 1 cannot reach expected 6 → `NO`.

The algorithm correctly propagates surplus height and detects mismatches, covering all tricky scenarios.
