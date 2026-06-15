---
title: "CF 1272B - Snow Walking Robot"
description: "We are given a sequence of moves for a robot on an infinite grid starting from the origin. Each character in the string tells the robot to move one step in one of the four cardinal directions."
date: "2026-06-16T01:23:50+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1272
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 605 (Div. 3)"
rating: 1200
weight: 1272
solve_time_s: 534
verified: false
draft: false
---

[CF 1272B - Snow Walking Robot](https://codeforces.com/problemset/problem/1272/B)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy, implementation  
**Solve time:** 8m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of moves for a robot on an infinite grid starting from the origin. Each character in the string tells the robot to move one step in one of the four cardinal directions. We are allowed to delete any subset of these moves and then reorder the remaining ones arbitrarily before executing them.

The resulting movement must form a valid walk with a strict constraint: the robot is not allowed to visit any grid cell more than once, except that it may start and end at the origin. So the path must be simple except for the origin, which can appear at most twice, at the beginning and the end.

The task is to keep as many moves as possible, rearrange them optimally, and output any valid sequence that achieves the maximum possible length.

The constraints imply that we must process up to 100000 characters across all test cases. This rules out any exponential or quadratic construction. We can only afford linear work per test case, essentially counting and constructing an answer in O(n).

A naive interpretation would suggest trying all subsets of moves and checking whether a permutation forms a valid simple cycle. This immediately fails because there are 2^n subsets and n! permutations, both far beyond feasible limits.

A more subtle pitfall comes from thinking that we can simply use all balanced directions independently. For example, taking many left and right moves and arranging them as "LRLRLR..." looks balanced but actually revisits intermediate points and violates the rule. Similarly, using many vertical moves in a row causes repeated visits to cells on the same line. The constraint is not just balance, but geometric simplicity of the entire path.

## Approaches

A brute-force strategy would try selecting a subset of moves and then verifying whether some ordering produces a valid non-self-intersecting closed walk. Even if we fix a subset, checking validity requires reasoning about all permutations or simulating possible paths, which in the worst case still degenerates into exponential exploration. The number of subsets alone is 2^n, and each verification would be at least O(n), which is far too slow.

The key insight is that since we are allowed to reorder arbitrarily, only the counts of each direction matter, not the original structure. This reduces the problem to selecting how many L, R, U, and D moves we keep.

Now we ask what shape of path maximizes length while avoiding revisits. A valid long path must essentially form a simple closed polygon. On a grid with axis-aligned steps, the best structure we can build is a rectangle: go right some distance, go up, go left back, and go down back to the origin. This guarantees no repeated internal cells.

To form such a rectangle, we need matching horizontal moves and matching vertical moves. If we take x = min(L, R), we can build x steps right and x steps left. Similarly, y = min(U, D) gives y steps up and y steps down. If both x and y are positive, we can combine them into a rectangle of perimeter 2(x + y).

If only one axis has matching pairs, we cannot extend it beyond a single back-and-forth pair without revisiting intermediate cells. So in that case, we can only take one pair total.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets and permutations | O(2^n · n!) | O(n) | Too slow |
| Count directions and build rectangle | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Count how many times each direction appears in the input string. We store counts of L, R, U, and D. This is necessary because the order is irrelevant after reordering, so only frequencies matter.
2. Compute how many balanced horizontal moves we can form by taking x = min(L, R). This represents the maximum number of left-right pairs that can be used without breaking symmetry.
3. Compute how many balanced vertical moves we can form by taking y = min(U, D). This represents the maximum number of up-down pairs.
4. If both x and y are greater than zero, we construct a rectangle. We output x times 'R', then y times 'U', then x times 'L', then y times 'D'. This ordering ensures the path goes around the boundary of a rectangle and returns to the origin without visiting any cell twice.
5. If one of x or y is zero but the other is positive, we cannot form a rectangle. In this case, we output exactly one pair in the non-zero direction axis: either "LR" or "UD". This gives a valid path of length 2.
6. If both x and y are zero, no valid move pair exists, so the answer is empty.

### Why it works

The constructed path is always a simple closed walk in the grid. When both axes are used, the robot traces the boundary of a rectangle. Every intermediate cell lies on exactly one side of the rectangle boundary, so no cell except the origin is revisited. When only one axis exists, any attempt to use more than one pair would force revisiting an intermediate cell, so restricting to a single pair is necessary and optimal.

Optimality follows from the fact that every valid closed non-self-intersecting path must use equal numbers of opposite directions. Any additional imbalance cannot be used without violating the endpoint condition. Since we maximize x and y independently, we use all available balanced pairs, and no larger valid construction exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    q = int(input())
    for _ in range(q):
        s = input().strip()

        L = s.count('L')
        R = s.count('R')
        U = s.count('U')
        D = s.count('D')

        x = min(L, R)
        y = min(U, D)

        if x == 0 and y == 0:
            print(0)
            print()
            continue

        if x == 0:
            print(2)
            print("UD")
            continue

        if y == 0:
            print(2)
            print("LR")
            continue

        ans = []
        ans.append("R" * x)
        ans.append("U" * y)
        ans.append("L" * x)
        ans.append("D" * y)

        res = "".join(ans)
        print(len(res))
        print(res)

if __name__ == "__main__":
    solve()
```

The code first aggregates direction frequencies, which is the only information needed after reordering is allowed. It then computes the usable symmetric pairs per axis.

The construction logic follows the rectangle idea directly. The ordering R, U, L, D is intentional because it traces the boundary without crossing itself. Any permutation that preserves this cycle structure would also work, but breaking it would introduce repeated cells.

The edge handling for single-axis cases is important: even if many pairs exist, only one can be used safely without violating the “no revisit” constraint.

## Worked Examples

We trace two representative cases.

### Example 1: `LRU`

| Step | L | R | U | D | x=min(L,R) | y=min(U,D) | Decision | Output |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Input | 1 | 1 | 1 | 0 | 1 | 0 | single axis | "LR" |

Here only horizontal balance exists, so we cannot form a rectangle. Using more than one pair would force revisiting `(1,0)` or `(0,0)` prematurely, so we keep exactly one pair.

### Example 2: `LRUDDLRUDRUL`

| Step | L | R | U | D | x | y | Decision | Output construction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Count | 3 | 3 | 3 | 3 | 3 | 3 | rectangle | RRR UUU LLL DDD |

All directions balance perfectly. The algorithm forms a 3 by 3 rectangle boundary, yielding a simple cycle that returns to origin without revisiting any other cell.

This confirms that when both axes are available, the solution always uses the full symmetric capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each string is scanned once to count directions and construct output |
| Space | O(1) | Only four counters and output buffer are used |

The total input size is bounded by 100000 across all test cases, so the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    q = int(input())
    out = []
    for _ in range(q):
        s = input().strip()

        L = s.count('L')
        R = s.count('R')
        U = s.count('U')
        D = s.count('D')

        x = min(L, R)
        y = min(U, D)

        if x == 0 and y == 0:
            out.append("0\n")
            continue
        if x == 0:
            out.append("2\nUD\n")
            continue
        if y == 0:
            out.append("2\nLR\n")
            continue

        res = "R"*x + "U"*y + "L"*x + "D"*y
        out.append(str(len(res)) + "\n" + res + "\n")

    return "".join(out)

# provided samples
assert run("""6
LRU
DURLDRUDRULRDURDDL
LRUDDLRUDRUL
LLLLRRRR
URDUR
LLL
""") == """2
LR
14
RUURDDDDLLLUUR
12
URDDDLLLRRUU
2
LR
2
UD
0
""", "sample check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single direction only | 0 or 2 | handling degenerate axis cases |
| balanced rectangle | full cycle | maximal construction correctness |
| excess one axis | limited pair | prevents invalid long chains |

## Edge Cases

When all moves are in one direction pair only, such as `"LLLLRRRR"`, the algorithm correctly reduces the answer to a single "LR" pair. Attempting to use all pairs would create repeated visits along the line, specifically revisiting `(1,0)` multiple times.

When all four directions exist but are unbalanced, the algorithm still safely uses only the minimum matching counts. Any extra unmatched moves are discarded because they cannot be part of a closed simple cycle.

When only one type of move exists, such as `"LLL"`, both x and y are zero, and the algorithm correctly returns an empty path since no valid cycle can be formed.
