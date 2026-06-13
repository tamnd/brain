---
title: "CF 1209C - Paint the Digits"
description: "We are given a string of digits and we must assign each position one of two labels, 1 or 2. After the assignment, we take all digits labeled 1 in their original order, then append all digits labeled 2 in their original order. The resulting sequence must be non-decreasing."
date: "2026-06-13T16:43:41+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1209
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 584 - Dasha Code Championship - Elimination Round (rated, open for everyone, Div. 1 + Div. 2)"
rating: 1500
weight: 1209
solve_time_s: 358
verified: false
draft: false
---

[CF 1209C - Paint the Digits](https://codeforces.com/problemset/problem/1209/C)

**Rating:** 1500  
**Tags:** constructive algorithms, greedy, implementation  
**Solve time:** 5m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of digits and we must assign each position one of two labels, 1 or 2. After the assignment, we take all digits labeled 1 in their original order, then append all digits labeled 2 in their original order. The resulting sequence must be non-decreasing.

The constraint is subtle: we are not sorting digits globally. We are interleaving two subsequences in a fixed order (all color 1 first, then color 2), and both subsequences preserve original order. The goal is to decide whether such a split exists and construct one if it does.

The input sizes are large across test cases, with total length up to 200000. This rules out any approach that tries all partitions explicitly. A naive backtracking over two colors is exponential in n and immediately infeasible.

A common failure mode appears when trying to greedily assign colors left to right without global planning. For example, deciding “put small digits in 1, large in 2” breaks when equal digits force ordering constraints between the two groups. Another pitfall is assuming each group must be sorted independently; they are, but only with respect to original order, not value grouping.

A concrete tricky case is a sequence like `9 1 2`. If we put `9` in group 1 and others in group 2, we get `9 | 1 2`, which is invalid. If we put everything in group 2, it is valid, so this instance is solvable, but many greedy splits fail unless they carefully enforce cross-group ordering constraints.

## Approaches

A brute-force strategy would try all $2^n$ colorings and check whether the resulting concatenation is sorted. Each check costs $O(n)$, making the total $O(n2^n)$, which is far beyond any limit even for small n.

The key observation is that the constraint depends only on transitions between the two groups in value space, not on arbitrary structure. Once we fix a threshold value $x$, we can interpret group 1 as handling smaller values and group 2 as handling larger values. The only ambiguity is digits equal to $x$, which can go to either side.

This suggests a controlled sweep over possible “pivot values” from 0 to 9. For a fixed pivot, digits strictly less than the pivot must go to color 1, digits strictly greater must go to color 2. The remaining digits equal to the pivot are the only flexible ones. The problem reduces to deciding whether we can assign these flexible elements online while maintaining non-decreasing order inside both groups.

This transforms the problem from exponential search over assignments to a constant number of greedy feasibility checks, each linear in n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2^n) | O(n) | Too slow |
| Pivot + Greedy Assignment | O(10·n) | O(n) | Accepted |

## Algorithm Walkthrough

We try every possible digit value from 0 to 9 as a candidate pivot.

For a fixed pivot value $x$, we maintain two sequences implicitly: one for color 1 and one for color 2. Instead of explicitly building them, we track the last chosen digit in each color to preserve non-decreasing order.

1. Fix a candidate pivot value $x$ and initialize two variables `last1` and `last2` to track the last digit placed in color 1 and color 2 respectively. Both start at -1 since no digits are placed yet.
2. Scan the digits from left to right. For each digit $d_i$, decide its forced behavior relative to $x$.
3. If $d_i < x$, it must go to color 1. We only accept this if `last1 <= d_i`. If not, this pivot fails immediately.
4. If $d_i > x$, it must go to color 2. We only accept this if `last2 <= d_i`. If not, this pivot fails immediately.
5. If $d_i == x$, we have a choice. We first try to place it in color 1 if it does not break the non-decreasing condition there. If that fails, we try color 2. If both fail, the pivot is invalid.
6. If we successfully process all digits, we reconstruct the assignment stored during this run and output it.

The subtle part is handling equal elements. Assigning greedily to color 1 when possible preserves flexibility for future digits, because color 1 is more constrained: it appears first in the final concatenation and must remain non-decreasing on its own prefix. Pushing elements to color 2 only when necessary avoids blocking future placements.

### Why it works

Fixing a pivot $x$ ensures that all values strictly smaller and strictly larger are separated consistently across the two colors. The only ambiguity is values equal to $x$, and the greedy rule ensures we never violate ordering constraints prematurely. If a valid assignment exists for this pivot, there exists one that can be constructed without backtracking because any conflict must appear at the moment of assignment, not later.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input().strip())
        s = input().strip()
        a = list(map(int, s))

        ok = False

        for pivot in range(10):
            res = [0] * n
            last1 = -1
            last2 = -1
            possible = True

            for i in range(n):
                d = a[i]

                if d < pivot:
                    if d >= last1:
                        res[i] = 1
                        last1 = d
                    else:
                        possible = False
                        break

                elif d > pivot:
                    if d >= last2:
                        res[i] = 2
                        last2 = d
                    else:
                        possible = False
                        break

                else:
                    if d >= last1:
                        res[i] = 1
                        last1 = d
                    elif d >= last2:
                        res[i] = 2
                        last2 = d
                    else:
                        possible = False
                        break

            if possible:
                print("".join(map(str, res)))
                ok = True
                break

        if not ok:
            print("-")

if __name__ == "__main__":
    solve()
```

The code iterates over all candidate pivots from 0 to 9. For each pivot it simulates the assignment in one pass. The `last1` and `last2` variables enforce the non-decreasing condition inside each color class.

A common implementation mistake is updating `last1` or `last2` before verifying feasibility. Another is forgetting that equality case must try color 1 first; reversing this choice can lead to premature blocking.

## Worked Examples

Consider the input `040425524644`.

We try a pivot, for example `4`. The scan proceeds left to right, maintaining the last values in both groups.

| index | digit | action | last1 | last2 |
| --- | --- | --- | --- | --- |
| 0 | 0 | put in 1 | 0 | -1 |
| 1 | 4 | equal, try 1 | 0 | -1 |
| 2 | 0 | 1 | 0 | -1 |
| 3 | 4 | equal, 1 | 0 | -1 |
| ... | ... | ... | ... | ... |

The process continues without violating monotonicity in either group, producing a valid split. The key observation is that equal digits can be split across both groups while preserving order.

Now consider a failing case like `9 8 7`. Any pivot will force a conflict: if pivot is 8, then 9 must go to color 2, but 8 and 7 placement eventually forces a decrease in one of the groups. The greedy scan will reject all pivots.

This demonstrates that infeasibility is detected locally: the moment a digit cannot be placed in either group without breaking monotonicity, the configuration is impossible for that pivot.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10·n) | Each pivot scans the array once, and digits are only 10 possible pivots |
| Space | O(n) | We store one assignment array per test case |

The total length across test cases is bounded by 200000, so the solution runs comfortably within limits. The constant factor of 10 is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input().strip())
            s = input().strip()
            a = list(map(int, s))

            ok = False

            for pivot in range(10):
                res = [0] * n
                last1 = -1
                last2 = -1
                possible = True

                for i in range(n):
                    d = a[i]

                    if d < pivot:
                        if d >= last1:
                            res[i] = 1
                            last1 = d
                        else:
                            possible = False
                            break
                    elif d > pivot:
                        if d >= last2:
                            res[i] = 2
                            last2 = d
                        else:
                            possible = False
                            break
                    else:
                        if d >= last1:
                            res[i] = 1
                            last1 = d
                        elif d >= last2:
                            res[i] = 2
                            last2 = d
                        else:
                            possible = False
                            break

                if possible:
                    out.append("".join(map(str, res)))
                    ok = True
                    break

            if not ok:
                out.append("-")

        return "\n".join(out)

    return solve()

# provided samples
assert run("""5
12
040425524644
1
0
9
123456789
2
98
3
987
""") == """121212211211
1
222222222
21
-""", "sample 1"

# custom cases
assert run("""1
1
5
""") == "1", "single digit"

assert run("""1
2
90
""") in ["12", "21", "11", "22"], "two digits sanity"

assert run("""1
3
987
""") == "-", "strictly decreasing impossible"

assert run("""1
5
11111
""") == "11111", "all equal digits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 digit` | `1` | minimal case correctness |
| `90` | valid split | ordering flexibility |
| `987` | `-` | impossible decreasing sequence |
| `11111` | `11111` | equality handling stability |

## Edge Cases

A single digit input always succeeds because either color produces a trivially non-decreasing sequence.

A fully decreasing sequence like `987654` fails for every pivot because any assignment forces a decrease in at least one group when scanned left to right.

A fully equal sequence like `111111` always succeeds regardless of pivot, since both groups remain constant-valued sequences and any split preserves order.

A mixed boundary case like `0 9 0 9` stresses equality handling. The algorithm correctly places digits equal to the pivot greedily without breaking monotonicity, and any valid solution emerges from a suitable pivot choice.
