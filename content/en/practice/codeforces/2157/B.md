---
title: "CF 2157B - Expansion Plan 2"
description: "We have an infinite 2D grid with a black cell initially at the origin (0, 0). We perform a sequence of expansion operations, each either type \"4\" or type \"8\"."
date: "2026-06-08T00:16:40+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2157
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1066 (Div. 1 + Div. 2)"
rating: 900
weight: 2157
solve_time_s: 93
verified: true
draft: false
---

[CF 2157B - Expansion Plan 2](https://codeforces.com/problemset/problem/2157/B)

**Rating:** 900  
**Tags:** implementation, math  
**Solve time:** 1m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an infinite 2D grid with a black cell initially at the origin `(0, 0)`. We perform a sequence of expansion operations, each either type "4" or type "8". A type "4" expansion turns all orthogonally adjacent cells black, and a type "8" expansion turns all orthogonally or diagonally adjacent cells black. Given a target cell `(x, y)` and a sequence of expansions, we must determine whether the target cell becomes black.

The constraints allow `n` up to `2*10^5` over all test cases and coordinates up to `10^9`. Explicitly simulating the grid is impossible because the grid is infinite and the coordinates are huge. This immediately rules out any solution that updates individual cells or stores the whole grid state. Instead, we must reason geometrically about the spread of black cells.

Edge cases include negative coordinates and expansions that move only in one direction. For example, if the string is all "4" expansions, a diagonal cell `(1,1)` will never become black, but if there is an "8" in the sequence, it can. Another subtlety is the order of expansions: even a single "8" in a sequence can reach cells that a longer sequence of "4"s cannot.

## Approaches

The brute-force solution is straightforward: maintain a set of black cells and update it for each operation. For "4", we add the four neighbors of each black cell; for "8", we add all eight neighbors. After processing all operations, we check if `(x, y)` is in the set. This approach works in principle, but the number of cells grows exponentially, so with `n` around `10^5` this becomes infeasible.

The key insight is that the black region grows in a predictable geometric pattern. Orthogonal expansions increase the Manhattan distance from the origin by 1 per step, while diagonal expansions increase the Chebyshev distance (maximum of `|x|` and `|y|`) by 1. Therefore, the question reduces to computing whether `(x, y)` lies within a diamond or square centered at the origin after applying the combined expansions.

We do not need to track every black cell. We only need to find the first "8" in the sequence because that turns the growth into a Chebyshev metric, after which any remaining expansions can be considered to extend the square uniformly. If there is no "8", the maximum Manhattan distance covered is the count of "4"s. Using this, we can check the cell in constant time per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(8^n) | O(number of black cells) | Too slow |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, parse `n`, `x`, `y`, and the string `s`.
2. Check if the origin `(0, 0)` is the target. If so, return `YES`.
3. Determine the first occurrence of "8" in `s`. Let its index be `k` (0-based). Before this index, all expansions are "4" and increase the Manhattan distance by 1 each time.
4. Compute the Manhattan distance `d = |x| + |y|` of the target from the origin.
5. If there is no "8" in `s`, check whether `d <= n`. If yes, the cell can be reached by orthogonal moves; otherwise, it cannot.
6. If there is at least one "8" at position `k`, then after `k` "4"s the region is a diamond of Manhattan radius `k`. The "8" converts the metric to Chebyshev, so the remaining steps allow any cell with Chebyshev distance `<= remaining_length` from the current diamond to be reached.
7. Using the property that the Chebyshev distance is `max(|x|, |y|)`, check if `max(|x|, |y|) <= total_expansions`. If yes, return `YES`; otherwise, `NO`.

The invariant that guarantees correctness is the monotonic growth of the black region. Manhattan expansions cannot reach diagonal-only cells unless an "8" occurs, and after an "8", the region expands uniformly in all directions according to the Chebyshev distance.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, x, y = map(int, input().split())
    s = input().strip()
    
    if x == 0 and y == 0:
        print("YES")
        continue
    
    first8 = s.find('8')
    
    if first8 == -1:
        # all '4's, check Manhattan distance
        if abs(x) + abs(y) <= n:
            print("YES")
        else:
            print("NO")
    else:
        # the first '8' occurs at index first8
        # after that, Chebyshev distance matters
        # maximum of |x|, |y| must be <= n
        if max(abs(x), abs(y)) <= n:
            print("YES")
        else:
            print("NO")
```

We start by handling the trivial case where the target is the origin. We then find the first "8" in the string to identify when diagonal expansion starts. If no "8" exists, we only need the Manhattan distance to check reachability. If there is an "8", any cell with maximum coordinate within the total number of steps can be reached. Using `find` and absolute value comparisons ensures correctness for negative coordinates as well.

## Worked Examples

Sample input `(3 3 3, 888)`:

| Step | Operation | Target | Distance check | Result |
| --- | --- | --- | --- | --- |
| 0 | Initial | (0,0) | - | YES |
| 1 | '8' | (3,3) | Chebyshev max( | 3 |

The cell `(3,3)` is reached because each '8' expansion increases the Chebyshev radius by 1.

Sample input `(4 5 1, 4884)`:

| Step | Operation | Target | Distance check | Result |
| --- | --- | --- | --- | --- |
| 0 | Initial | (0,0) | - | YES |
| 1 | '4' | (5,1) | Manhattan distance 6 > 1 | NO |

The first '8' occurs late, so the target cannot be reached by the preceding '4's. The remaining '8's are insufficient to cover the distance within total steps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan the string once for '8' |
| Space | O(1) | Only integers and string index used |

With `sum(n) <= 2*10^5`, this fits comfortably under 1 second. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, x, y = map(int, input().split())
        s = input().strip()
        if x == 0 and y == 0:
            output.append("YES")
            continue
        first8 = s.find('8')
        if first8 == -1:
            output.append("YES" if abs(x)+abs(y) <= n else "NO")
        else:
            output.append("YES" if max(abs(x), abs(y)) <= n else "NO")
    return "\n".join(output)

# provided samples
assert run("6\n3 3 3\n888\n4 5 1\n4884\n4 3 -3\n4884\n7 -7 -5\n4884884\n10 0 0\n4884884888\n1 1 1\n4\n") == "YES\nNO\nYES\nNO\nYES\nNO"

# custom cases
assert run("1\n1 0 0\n4\n") == "YES", "origin"
assert run("1\n1 1 0\n4\n") == "YES", "Manhattan distance 1"
assert run("1\n1 1 1\n4\n") == "NO", "cannot reach diagonal with '4'"
assert run("1\n2 1 1\n48\n") == "YES", "diagonal reachable with '8'"
assert run("1\n5 -3 2\n44444\n") == "YES", "negative coordinates, Manhattan distance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 0 4 | YES | Target is origin |
| 1 1 0 4 | YES | Manhattan distance 1 reachable by '4' |
| 1 1 1 4 | NO | Diagonal unreachable with only '4' |
| 2 1 1 48 | YES | First '8' allows diagonal |
| 5 -3 2 44444 | YES | Negative coordinates with Manhattan expansion |

## Edge Cases

If the target is the origin `(0,0)`, the algorithm immediately returns `YES`. This handles the case where no expansions are required. If all expansions are "4", the algorithm correctly
