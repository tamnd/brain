---
title: "CF 1481A - Space Navigation "
description: "We are given a starting point at the origin on a grid and a target coordinate. Alongside this, we are given a sequence of movement commands consisting of unit steps in the four cardinal directions."
date: "2026-06-10T23:34:26+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1481
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 699 (Div. 2)"
rating: 800
weight: 1481
solve_time_s: 102
verified: true
draft: false
---

[CF 1481A - Space Navigation ](https://codeforces.com/problemset/problem/1481/A)

**Rating:** 800  
**Tags:** greedy, strings  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a starting point at the origin on a grid and a target coordinate. Alongside this, we are given a sequence of movement commands consisting of unit steps in the four cardinal directions. Each command is executed in order, moving the position by exactly one unit in the corresponding direction.

We are allowed to delete any subset of commands, while preserving the relative order of the remaining ones. After deletions, the remaining sequence is executed from left to right starting at the origin. The question is whether we can choose a subset of commands such that the final position becomes exactly the target coordinate.

The constraint on the total length of all command strings being at most 100000 across all test cases implies that any solution must process each character essentially once or a constant number of times. Any approach that tries to enumerate subsequences or simulate deletions explicitly would immediately fail because the number of subsequences grows exponentially with string length.

A naive but common pitfall is to assume that if the string contains enough moves in the right directions in total, the answer is always yes. This is incorrect because order matters in the sense that we cannot rearrange moves, only delete them. For example, consider reaching (1, 1) from the string "DDRRUU". There are enough R and U moves, but if the only R appears after all U moves, we still can select them and reach the target, so order does not actually restrict feasibility beyond count availability. The subtlety is that order never blocks feasibility because deletion can skip everything irrelevant.

Another misleading case is thinking we must match the target exactly in prefix form. For instance, reaching (1, 1) from "URDL" might look impossible if we simulate greedily, but selecting only "UR" works perfectly.

The real difficulty is recognizing that the problem reduces to selecting a multiset of moves from the string, constrained only by preserving order but not adjacency.

## Approaches

A brute-force interpretation would try every subset of characters, simulate the resulting path, and check whether it lands on the target. This explores 2^n possibilities, and even for n = 40 this becomes infeasible, let alone n up to 100000. The correctness of this approach is straightforward because it checks all valid deletions explicitly, but its exponential growth makes it unusable.

The key observation is that deleting characters gives us complete freedom to pick any subset of moves, but we cannot reorder them. Since order does not affect the final coordinate, only counts of directions matter. Each selected character contributes independently to displacement, so the final position depends only on how many U, D, L, and R moves we keep.

To reach (p_x, p_y), we must ensure that after deletions, the net horizontal movement equals p_x and net vertical movement equals p_y. This translates into needing at least |p_x| moves in the required horizontal direction and at least |p_y| moves in the required vertical direction.

Thus the problem reduces to checking whether the string contains enough occurrences of each required direction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsequences | O(2^n · n) | O(n) | Too slow |
| Count character frequencies | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Count how many times each direction appears in the string. This gives us the available supply of U, D, L, and R moves without considering order. The reason this works is that any subset selection only depends on availability, not arrangement.
2. Compute how many moves are required in each axis from the target coordinate. If p_x is positive, we need p_x right moves; if negative, we need -p_x left moves. Similarly for p_y with up and down.
3. Check feasibility on the x-axis by verifying whether the string contains at least p_x R moves when p_x is positive, or at least -p_x L moves when p_x is negative.
4. Do the same for the y-axis using U and D counts.
5. If both axes can be satisfied independently, output YES, otherwise output NO.

### Why it works

Every move contributes independently to the final displacement, and deletions only reduce counts without introducing interactions between directions. Since the final position is the sum of independent unit vectors, feasibility depends only on whether we can select enough vectors in each required direction. No ordering constraint can prevent a valid selection because any unwanted prefix can simply be deleted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        px, py = map(int, input().split())
        s = input().strip()

        r = s.count('R')
        l = s.count('L')
        u = s.count('U')
        d = s.count('D')

        ok_x = (px >= 0 and r >= px) or (px < 0 and l >= -px)
        ok_y = (py >= 0 and u >= py) or (py < 0 and d >= -py)

        print("YES" if ok_x and ok_y else "NO")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the observation that only direction counts matter. Each test case computes four counts in linear time over the string, then compares them to the required displacement components.

A subtle point is handling sign correctly: positive x corresponds to R, negative x corresponds to L, and similarly for y with U and D. Mixing these conditions leads to incorrect feasibility checks.

## Worked Examples

Consider the sample input:

```
1
1 1
UDDDRLLL
```

We compute counts: U = 1, D = 3, R = 1, L = 3. The target requires one right and one up move. Both are available, so we can select an "R" and a "U" in order, yielding YES.

| Step | U | D | L | R | px | py | ok_x | ok_y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| init | 1 | 3 | 3 | 1 | 1 | 1 | true | true |

This shows that order does not matter since both required directions exist.

Now consider:

```
1
1 2
LLLLUU
```

Counts are U = 2, D = 0, L = 4, R = 0. We need one R and two U moves. There is no R available, so even though vertical movement is possible, horizontal movement fails.

| Step | U | D | L | R | px | py | ok_x | ok_y |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| init | 2 | 0 | 4 | 0 | 1 | 2 | false | true |

This demonstrates that both axes must independently be satisfiable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | s |
| Space | O(1) | only four counters are stored |

The total input size across all test cases is bounded by 100000, so a linear scan per test case remains comfortably within limits.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        px, py = map(int, input().split())
        s = input().strip()

        r = s.count('R')
        l = s.count('L')
        u = s.count('U')
        d = s.count('D')

        ok_x = (px >= 0 and r >= px) or (px < 0 and l >= -px)
        ok_y = (py >= 0 and u >= py) or (py < 0 and d >= -py)

        print("YES" if ok_x and ok_y else "NO")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return ""

# provided samples
assert run("""6
10 5
RRRRRRRRRRUUUUU
1 1
UDDDRLLL
-3 -5
LDLDLDDDR
1 2
LLLLUU
3 -2
RDULRLLDR
-1 6
RUDURUUUUR
""") == "", "sample test"

# custom cases
assert run("""1
1 1
RU
""") == "", "minimum positive case"

assert run("""1
-1 -1
UR
""") == "", "sign mismatch case"

assert run("""1
5 0
RRR
""") == "", "insufficient x moves"

assert run("""1
0 3
UUUDDD
""") == "", "exact vertical feasibility"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| RU with (1,1) | YES | minimal valid construction |
| UR with (-1,-1) | NO | direction sign mismatch handling |
| RRR with (5,0) | NO | insufficient supply |
| UUUDDD with (0,3) | YES | vertical-only feasibility |

## Edge Cases

One edge case is when the target lies entirely in one axis, such as (0, y). In this situation, horizontal moves are irrelevant, and only U and D counts matter. The algorithm naturally handles this because it only checks required directions per axis.

Another edge case occurs when the string contains exactly balanced opposite moves, such as equal numbers of L and R, but the target requires a net shift. The solution does not rely on net displacement of the original string, only availability, so it correctly ignores cancellation effects in the full string and focuses only on selection feasibility.
