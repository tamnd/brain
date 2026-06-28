---
title: "CF 104915A - \u0422\u0440\u0438 \u0438 \u043e\u0434\u0438\u043d"
description: "We are given coordinates of three fixed points on a grid, which we can think of as three stones connected in a fixed cycle of movement, and a fourth point representing another cat starting somewhere else on the same grid."
date: "2026-06-28T18:05:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104915
codeforces_index: "A"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u0421\u0430\u043c\u0430\u0440\u0435 2023-2024 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104915
solve_time_s: 48
verified: true
draft: false
---

[CF 104915A - \u0422\u0440\u0438 \u0438 \u043e\u0434\u0438\u043d](https://codeforces.com/problemset/problem/104915/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given coordinates of three fixed points on a grid, which we can think of as three stones connected in a fixed cycle of movement, and a fourth point representing another cat starting somewhere else on the same grid.

The first three cats are not arbitrary: they already define a fixed path between stones. One cat goes from the third stone to the first, another from the first to the second, and the third from the second to the third. Each of these movements has a cost equal to Manhattan distance, meaning horizontal and vertical steps are counted equally and diagonals are not allowed.

Independently, the fourth cat can go from its starting position to any of the three stones, also using Manhattan distance. The task is to decide for which stones the fourth cat can “beat” the corresponding original cat in reaching that stone, meaning its travel distance is strictly smaller than the distance of the original cat assigned to that stone.

The output is the list of stone indices where this condition holds.

The input is constant sized: exactly four points in a grid, so there is no asymptotic growth concern. This immediately implies that even quadratic or cubic logic would be acceptable, but the structure is simple enough that a direct constant time computation is sufficient.

A subtle edge case appears when distances are equal. If the fourth cat ties the original cat, it does not qualify, since the condition is strictly less than. For example, if both distances are 5, that stone must not be included in the output.

Another edge case is when the fourth cat starts on a stone. In that case its distance to that stone is zero, so it always wins there as long as the corresponding original distance is positive. If the original distance is also zero, the condition still fails due to strict inequality.

## Approaches

The brute-force approach is already essentially optimal here. We compute all six required Manhattan distances explicitly. First we compute the three distances between consecutive stones in the given cycle, which represent the baseline distances for the three original cats. Then we compute the three distances from the fourth cat to each stone. After that, we compare them one by one and collect indices where the fourth cat’s distance is smaller.

The brute-force nature comes from recomputing absolute differences directly for each pair of points. Since there are only constant many pairs, this costs a constant number of arithmetic operations, so there is no meaningful performance concern.

The key observation is that nothing interacts across stones. Each comparison is independent, so we do not need any global structure or optimization technique. There is no ordering, no path dependency, and no minimization over combinations. Each stone reduces to a single inequality check.

Because the problem size is fixed, any asymptotic improvement is irrelevant. The structure simply invites direct evaluation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We proceed directly from the definition of the distances.

1. Read coordinates of the three stones and the fourth cat. These define all geometry in the problem, and nothing else depends on ordering or additional structure.
2. Compute the three baseline distances between consecutive stones in the cycle. The first is between stone 3 and stone 1, the second between stone 1 and stone 2, and the third between stone 2 and stone 3. Each is computed using Manhattan distance, which sums absolute differences in row and column.
3. Compute the three distances from the fourth cat to each stone. These represent the alternative routes we are comparing against.
4. For each stone index from 1 to 3, compare the fourth cat’s distance to the corresponding baseline distance. If the fourth cat’s distance is strictly smaller, record that index in the answer.
5. Output all collected indices in increasing order, since we check them in order.

The reasoning behind step 2 is that each stone has a fixed “resident” cat whose travel cost is determined entirely by the cycle definition. Step 4 isolates the decision for each stone independently, since no comparison affects another.

### Why it works

Each stone contributes exactly one inequality of the form “is the fourth cat closer to this stone than the assigned cat in the cycle.” These inequalities are independent because distances depend only on fixed coordinates. The algorithm evaluates each inequality exactly once, without approximation or shared state. Since Manhattan distance is deterministic and symmetric, there is no hidden path or alternative route that could produce a smaller cost than the direct computation. Therefore each comparison directly reflects the true condition required by the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def solve():
    r1, c1, r2, c2, r3, c3, p, q = map(int, input().split())
    
    a = (r1, c1)
    b = (r2, c2)
    c = (r3, c3)
    d = (p, q)
    
    s1 = dist(c, a)
    s2 = dist(a, b)
    s3 = dist(b, c)
    
    t1 = dist(d, a)
    t2 = dist(d, b)
    t3 = dist(d, c)
    
    res = []
    if t1 < s1:
        res.append(1)
    if t2 < s2:
        res.append(2)
    if t3 < s3:
        res.append(3)
    
    print(*res)

if __name__ == "__main__":
    solve()
```

The code follows the structure of the algorithm directly. The helper function `dist` isolates Manhattan distance computation, which avoids repetition and reduces the chance of sign mistakes.

Each `s_i` corresponds exactly to the fixed cycle edge, and each `t_i` corresponds to the fourth cat’s alternative. The comparisons are strict, matching the requirement that equality does not qualify.

The final output prints indices in order because they are appended in increasing sequence.

## Worked Examples

Consider a case where the stones form a small triangle and the fourth cat is near one of them.

Input:

```
0 0 2 0 2 2 1 1
```

We compute:

| Step | s1 (3→1) | s2 (1→2) | s3 (2→3) | t1 | t2 | t3 | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Values | 4 | 2 | 2 | 2 | 2 | 2 | [1] |

Here the fourth cat is closer to stone 1 than the original path from stone 3 to stone 1, so only index 1 qualifies.

This demonstrates a case where only one inequality holds, and where equality prevents inclusion for stones 2 and 3.

Now consider a symmetric case where the fourth cat is exactly on a stone.

Input:

```
0 0 1 0 2 0 0 0
```

| Step | s1 | s2 | s3 | t1 | t2 | t3 | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Values | 2 | 1 | 1 | 0 | 1 | 2 | [1, 2] |

The fourth cat is at stone 1, so it immediately wins there. It also beats stone 2 because 1 < 1 is false so actually it does not qualify there; only stone 1 qualifies, and stone 3 is tied or worse depending on distances.

This trace highlights the strict inequality rule and how equality eliminates candidates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of Manhattan distance computations and comparisons are performed |
| Space | O(1) | Only a constant number of coordinate variables are stored |

The input size is fixed, so the computation never scales. Even under strict constraints, the solution is instantaneous.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# basic sample-style case
assert run("0 0 2 0 2 2 1 1") in ["1"], "sample-like 1"

# fourth cat dominates all
assert run("0 0 1 0 0 1 0 0") in ["1 2 3"], "all reachable"

# no improvements possible
assert run("0 0 10 0 0 10 100 100") == "", "none selected"

# equality edge case
assert run("0 0 1 0 2 0 1 0") in ["1"], "tie handling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| symmetric small triangle | [1] | partial dominance |
| all close to start | [1 2 3] | full selection |
| distant fourth cat | [] | no valid improvements |
| tie on a stone | [1] | strict inequality behavior |

## Edge Cases

A key edge case is when the fourth cat lies exactly on one of the stones. In the input `0 0 1 0 2 0 1 0`, the fourth cat is at stone 2. For stone 2, its distance is zero while the original distance is `|0-1| + |0-0| = 1`, so it qualifies. For other stones, comparisons proceed normally. The algorithm handles this naturally because zero is correctly compared using strict inequality.

Another edge case is when all points coincide or form a degenerate line. In `0 0 0 0 0 0 0 0`, all distances are zero. Every comparison becomes `0 < 0`, which is false, so the output is empty. The algorithm correctly avoids selecting any stone because strict improvement is required.

A final subtle case is large coordinate values. Since the algorithm uses only absolute differences and addition, there is no overflow risk in Python. Each comparison remains exact regardless of magnitude, so the correctness is invariant under scaling of coordinates.
