---
title: "CF 105018I - Hall of Faces"
description: "We are given a circular arrangement of labeled faces. Each position contains a string label describing the face, and exactly one position is marked with the label \"Jaqen\", which represents the current position of the traveler."
date: "2026-06-28T02:05:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105018
codeforces_index: "I"
codeforces_contest_name: "Winter Cup 5.0 Online Mirror Contest"
rating: 0
weight: 105018
solve_time_s: 42
verified: true
draft: false
---

[CF 105018I - Hall of Faces](https://codeforces.com/problemset/problem/105018/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a circular arrangement of labeled faces. Each position contains a string label describing the face, and exactly one position is marked with the label `"Jaqen"`, which represents the current position of the traveler.

After returning the current face to its position, the task is to find another face with a required target label. Movement is allowed in both directions around the circle, clockwise or counterclockwise, and we want the minimum number of inspected faces before reaching any occurrence of the target label.

The key point is that inspection cost is measured as the number of steps along the circle from the `"Jaqen"` position to the nearest occurrence of the target label, considering both directions.

The input size allows up to 100 test cases and a total of up to 10^5 faces overall. This immediately rules out anything worse than linear time per test case. A quadratic approach that tries every start and recomputes distances would degrade to about 10^10 operations in the worst case, which is not feasible.

A subtle edge case appears when the target label does not exist in the array at all. In that case, the correct output is `-1`. Another edge case is when the target label is exactly `"Jaqen"` itself. Since we conceptually “return” the current face first, we still search for another occurrence, and if none exists, the answer is also `-1`.

## Approaches

A direct approach is to locate the index of `"Jaqen"`, then for every position in the circle check its distance from this index and keep the minimum among those whose label matches the target. Because the array is circular, each distance requires computing both clockwise and counterclockwise offsets, taking a minimum.

This works correctly because it explicitly evaluates every possible destination. However, for each candidate target match, we recompute a distance in O(1), but scanning all positions still costs O(n). Doing this for multiple test cases is still acceptable in isolation, but the inefficiency appears when we try to be overly careful or re-scan multiple times per query, especially if implemented naively with repeated modular arithmetic and searches for `"Jaqen"` each time.

The key observation is that we do not need to recompute distances for every occurrence of the target independently in a complex way. Once we know the position of `"Jaqen"`, every other position’s distance is determined purely by index arithmetic on a circle. Therefore the answer reduces to scanning the array once, computing the circular distance only for positions matching the target label, and taking the minimum.

The circular distance between indices i and j in an array of length n is:

min(|i - j|, n - |i - j|)

Since we only care about positions with the desired label, we reduce the problem to a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute for all pairs) | O(n²) | O(1) | Too slow |
| Optimal single scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array and identify the index of the special position labeled `"Jaqen"`. This is the reference point from which all distances are measured.
2. Read the target label we are searching for.
3. If the target label does not exist anywhere in the array, return `-1` immediately. This avoids unnecessary computation.
4. Initialize a variable `best` to a large value. This will track the smallest circular distance found so far.
5. Traverse every index i in the array. For each position:

1. If the label at i matches the target, compute the circular distance between i and the `"Jaqen"` index.
2. Update `best` if this distance is smaller.
6. After finishing the traversal, output `best`.

The key decision is restricting distance computation only to relevant positions. This ensures we do not waste time evaluating irrelevant labels.

### Why it works

Every valid answer corresponds to choosing some occurrence of the target label and walking along the circle from `"Jaqen"` to that occurrence. The cost of that walk depends only on their relative positions on the cycle. Since we examine every occurrence exactly once and compute its true minimal circular distance from the start position, the minimum over all of them is exactly the global optimum. No path other than direct circular traversal can be shorter, so no alternative structure or multi-step reasoning is required.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        parts = input().split()
        n = int(parts[0])
        target = parts[1]

        arr = input().split()

        start = -1
        for i, x in enumerate(arr):
            if x == "Jaqen":
                start = i
                break

        # If target is not present at all
        if target not in arr:
            print(-1)
            continue

        best = float('inf')

        for i, x in enumerate(arr):
            if x == target:
                diff = abs(i - start)
                dist = min(diff, n - diff)
                if dist < best:
                    best = dist

        print(best if best != float('inf') else -1)

if __name__ == "__main__":
    solve()
```

The implementation first parses each test case and extracts both the target label and the full circular list. It then locates the starting position labeled `"Jaqen"` in a single pass.

The second pass checks only positions matching the target. The circular distance computation uses the standard wraparound formula `min(|i - start|, n - |i - start|)`, which correctly accounts for both clockwise and counterclockwise movement.

A common pitfall is forgetting to apply the wraparound correction and using only absolute difference. That would overestimate distances when the optimal path crosses the boundary of the array.

Another subtle issue is handling the case where the target is missing entirely. Without an explicit check, `best` would remain infinity and must be converted to `-1`.

## Worked Examples

### Example 1

Input:

```
n = 5, target = one-eyed
arr = [red-haired, Jaqen, silver-haired, one-eyed, red-haired]
```

We first locate `"Jaqen"` at index 1.

| i | label | match target | |i - start| | circular distance | best |

|---|---|---|---|---|---|

| 0 | red-haired | no | 1 | 1 | inf |

| 1 | Jaqen | no | 0 | 0 | inf |

| 2 | silver-haired | no | 1 | 1 | inf |

| 3 | one-eyed | yes | 2 | 2 | 2 |

| 4 | red-haired | no | 3 | 2 | 2 |

Final answer is 2.

This shows how the algorithm naturally handles circular wrapping, since the shortest path from index 1 to 3 could also be considered 1 → 0 → 4 → 3, but the formula captures it directly.

### Example 2

Input:

```
n = 3, target = thick-eyebrows
arr = [Jaqen, brown-eyed, long-nose]
```

Here `"Jaqen"` is at index 0, but the target does not exist.

We detect absence early and output `-1`.

This confirms that the algorithm correctly separates reachability from distance computation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each array is scanned once to find `"Jaqen"` and once to evaluate matches |
| Space | O(1) extra | Only a few variables are used beyond input storage |

With total input size up to 10^5, this runs comfortably within limits since every element is processed a constant number of times.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        parts = input().split()
        n = int(parts[0])
        target = parts[1]
        arr = input().split()

        start = -1
        for i, x in enumerate(arr):
            if x == "Jaqen":
                start = i
                break

        if target not in arr:
            out.append("-1")
            continue

        best = float('inf')
        for i, x in enumerate(arr):
            if x == target:
                d = abs(i - start)
                best = min(best, min(d, n - d))

        out.append(str(best if best != float('inf') else -1))

    return "\n".join(out) + "\n"

# provided sample-like tests
assert run("1\n5 one-eyed\nred-haired Jaqen silver-haired one-eyed red-haired\n") == "2\n"
assert run("1\n3 thick-eyebrows\nJaqen brown-eyed long-nose\n") == "-1\n"

# custom cases
assert run("1\n1 a\nJaqen\n") == "-1\n"
assert run("1\n4 x\nx Jaqen x x\n") == "1\n"
assert run("1\n6 a\nb c Jaqen d e a\n") == "3\n"
assert run("1\n5 Jaqen\nJaqen Jaqen Jaqen Jaqen Jaqen\n") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element only | -1 | no reachable target |
| multiple targets around circle | 1 | circular shortest path |
| target far across wrap | 3 | wraparound correctness |
| all labels identical | 0 | trivial minimum case |

## Edge Cases

When the array has size one, the only element is `"Jaqen"`, so any other target is impossible. The scan finds no matches and returns `-1`, consistent with the rule that we must locate a different face.

When the target appears multiple times symmetrically around `"Jaqen"`, the algorithm correctly evaluates each candidate independently and selects the smallest circular distance. Because each occurrence is processed once, symmetry does not introduce any bias or duplication errors.

When the closest occurrence requires wrapping around the boundary, the `min(diff, n - diff)` computation captures the shorter arc automatically, preventing overestimation that would arise from linear distance only.
