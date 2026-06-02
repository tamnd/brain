---
title: "CF 2227A - Koshary"
description: "We are given a grid starting at the origin point $(0,0)$ and a target point $(x,y)$. At each move, Yousef can increase exactly one coordinate by 2 using a long step, either moving right by 2 or up by 2."
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2227
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1096 (Div. 3)"
rating: 0
weight: 2227
solve_time_s: 158
verified: false
draft: false
---

[CF 2227A - Koshary](https://codeforces.com/problemset/problem/2227/A)

**Rating:** -  
**Tags:** implementation, math  
**Solve time:** 2m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid starting at the origin point $(0,0)$ and a target point $(x,y)$. At each move, Yousef can increase exactly one coordinate by 2 using a long step, either moving right by 2 or up by 2. In addition, he is allowed to use a single special move during the entire journey, a short step, which increases exactly one coordinate by 1.

The task is to determine whether there exists any sequence of moves that lands exactly on $(x,y)$.

The constraints are very small, with both coordinates at most 10 and at most 100 test cases. This immediately suggests that any solution that depends only on constant time per test case is sufficient. Even a naive enumeration of all paths would be feasible in principle because the state space is tiny, but a systematic search would still be unnecessary overhead compared to a direct structural characterization.

A common failure case for intuitive approaches is to treat the problem greedily, for example by repeatedly subtracting 2 from the larger coordinate or alternating directions. Such strategies can fail because the only real restriction is parity consistency combined with the single-use short step, not the order of operations.

A concrete misleading example is $(1,1)$. A naive attempt might try to use one short step for either axis and then complete the rest, but after using a short step once, the remaining coordinate would require odd increments as well, which is impossible with only steps of size 2.

## Approaches

A brute-force interpretation models each state as a position $(a,b)$ together with whether the short step has been used. From each state, we branch into at most three transitions: move $(a+2,b)$, move $(a,b+2)$, or if unused, move $(a+1,b)$ or $(a,b+1)$. Since $x,y \le 10$, the number of reachable states is at most $11 \times 11 \times 2$, and a BFS would terminate quickly. This is correct because it explores all legal move sequences.

However, this approach is structurally heavier than necessary. The key observation is that every move changes exactly one coordinate, and every change is either even or odd depending on whether it is a long or short step. Long steps preserve parity, while a short step flips parity of exactly one coordinate and can only happen once.

This reduces the problem to a parity feasibility condition. Without using the short step, both coordinates must remain even throughout, so both $x$ and $y$ must be even. With exactly one short step, exactly one coordinate becomes odd while the other remains even, and all remaining contributions are even increments. Therefore the only impossible configuration is when both coordinates are odd, since that would require two independent parity flips.

The brute-force method works because it explores all combinations explicitly, but it fails in terms of conceptual clarity and efficiency compared to the parity reduction, which collapses all paths into a single invariant condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS | $O(xy)$ per test | $O(xy)$ | Accepted but unnecessary |
| Parity Analysis | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read integers $x$ and $y$ for each test case. These represent the required displacement along each axis.
2. Compute the parity of both coordinates by checking whether each is even or odd. This is the only structural property that matters because all allowed moves change coordinates in increments of 1 or 2.
3. If both $x$ and $y$ are odd, output "NO". This follows from the fact that each coordinate starts at 0, which is even, and long steps preserve parity, so reaching two odd coordinates would require two independent parity flips, but only one short step exists.
4. Otherwise output "YES". Any remaining configuration can be constructed by assigning the optional short step to the coordinate that needs odd parity, while using long steps to complete the rest.

### Why it works

The invariant is that each long step preserves the parity of both coordinates, while a short step flips the parity of exactly one coordinate and is used at most once. Starting from $(0,0)$, both coordinates are even. Therefore, after all moves, the parity of $(x,y)$ must be reachable by either zero or one parity flip. The only parity pattern that requires two independent flips is $(\text{odd}, \text{odd})$, which is unreachable under the constraint of a single short step. This invariant completely characterizes feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        x, y = map(int, input().split())
        if x % 2 == 1 and y % 2 == 1:
            print("NO")
        else:
            print("YES")

if __name__ == "__main__":
    solve()
```

The implementation reads each test case independently and directly applies the parity condition. The only subtle point is ensuring both coordinates are checked simultaneously, since the impossibility condition requires both to be odd at the same time. There is no need to track the number of steps or simulate movement, because the structure of allowed operations reduces everything to parity logic.

## Worked Examples

Consider the input $(x,y) = (2,4)$. Both coordinates are even, so no short step is needed. Two-dimensional parity remains consistent under repeated long steps.

| Step | x parity | y parity | State |
| --- | --- | --- | --- |
| start | even | even | (0,0) |
| after long steps | even | even | (2,4) |

This confirms that even-even configurations are reachable.

Now consider $(x,y) = (1,1)$.

| Step | x parity | y parity | State |
| --- | --- | --- | --- |
| start | even | even | (0,0) |
| after short step | odd | even or even | odd depending choice |
| final requirement | odd | odd | impossible |

This shows that whichever coordinate receives the short step, the other coordinate remains even throughout, making simultaneous odd parity unattainable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case is checked using constant-time parity operations |
| Space | $O(1)$ | No additional structures beyond a few integers |

The solution is optimal for the constraints since it performs a fixed number of arithmetic and modulo operations per test case, well within limits for $t \le 100$.

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
        x, y = map(int, input().split())
        if x % 2 == 1 and y % 2 == 1:
            out.append("NO")
        else:
            out.append("YES")
    return "".join(out)

# provided samples (as concatenated style)
assert run("6\n1 1\n2 4\n6 5\n9 7\n2 10\n10 10\n") == "NOYESYESNOYESYES"

# minimum values
assert run("1\n1 2\n") == "YES"

# both odd case
assert run("1\n3 3\n") == "NO"

# all even large-ish
assert run("1\n10 10\n") == "YES"

# mixed parity
assert run("1\n8 7\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (1,2) | YES | single odd coordinate reachable |
| (3,3) | NO | both odd impossibility |
| (10,10) | YES | all-even boundary case |
| (8,7) | YES | one odd coordinate case |

## Edge Cases

For $(1,1)$, both coordinates are odd. The algorithm immediately outputs "NO" because the condition detects simultaneous odd parity. Any attempted construction would require assigning the short step to only one axis, leaving the other axis impossible to fix using only increments of 2.

For $(1,2)$, exactly one coordinate is odd. The algorithm outputs "YES". A trace shows that using the short step on the x-coordinate makes it possible: $(0,0) \rightarrow (1,0)$ via short step, then repeated long steps reach $(1,2)$.

| Step | x | y | Action |
| --- | --- | --- | --- |
| start | 0 | 0 | start |
| 1 | 1 | 0 | short step in x |
| 2 | 1 | 2 | long step in y |

This confirms that single-odd-coordinate cases are always feasible under the allowed operations.
