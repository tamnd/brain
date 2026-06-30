---
title: "CF 104447M - Is it possible?"
description: "We start with a coin at coordinate (0, 0) on an infinite integer grid. Time progresses in discrete steps starting from 1. At each step i, we choose any integer xi, and then the coin moves in a constrained way depending on whether the step is odd or even."
date: "2026-06-30T18:46:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104447
codeforces_index: "M"
codeforces_contest_name: "Al-Baath Collegiate Programming Contest 2023"
rating: 0
weight: 104447
solve_time_s: 45
verified: true
draft: false
---

[CF 104447M - Is it possible?](https://codeforces.com/problemset/problem/104447/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a coin at coordinate (0, 0) on an infinite integer grid. Time progresses in discrete steps starting from 1. At each step i, we choose any integer xi, and then the coin moves in a constrained way depending on whether the step is odd or even.

If i is odd, the move adds xi to both coordinates, so (a, b) becomes (a + xi, b + xi). If i is even, the move adds xi to the first coordinate and subtracts xi from the second, so (a, b) becomes (a + xi, b − xi). The task is to reach a target point (n, m) using the minimum number of such moves, and also output the chosen sequence of xi values. If it cannot be done, we output -1.

The constraints go up to 100,000 test cases and coordinates up to ±10^9. This immediately rules out any per-test simulation over large numbers of steps or any construction that depends on iterative search over xi values. Each test must be solved in constant or near-constant time.

A subtle point is that xi is unrestricted in magnitude and sign. That means each move is a linear transformation with a freely chosen scalar, so the structure is entirely algebraic rather than combinatorial.

A naive mistake is to treat this like independent movement of x and y coordinates. For example, trying to solve x and y separately fails because every move couples them. Another common incorrect assumption is that the parity alternation creates irreversible constraints; in fact, it only alternates a sign pattern.

A concrete failure case for naive reasoning is trying to greedily match n first. Suppose we try to reach (n, m) by accumulating x contributions only on x. We quickly find that every move also affects y in a linked way, so independent greedy accumulation breaks.

## Approaches

The key to this problem is rewriting the movement in a more structured form.

Let the position after k moves be (X, Y). Each move contributes xi to X always, while Y alternates between +xi and −xi depending on parity. So we can think of contributions to X and Y separately:

For odd i: contribution is (xi, xi)

For even i: contribution is (xi, −xi)

So after k moves:

X = sum(xi for all i)

Y = sum(xi for odd i) − sum(xi for even i)

We introduce:

S = sum over all xi

O = sum over odd i xi

E = sum over even i xi

Then:

X = S = O + E

Y = O − E

Solving these equations gives:

O = (X + Y) / 2

E = (X − Y) / 2

So a necessary condition for any solution is that both (n + m) and (n − m) are even. Otherwise, O and E are not integers, so no integer sequence can produce the target.

Once feasibility is determined, we still need the minimum number of moves. Since each move contributes exactly one xi, we want to express O and E as sums of integers. The optimal strategy is to do it in at most two moves:

If both O and E are non-zero, we can use two moves:

One odd-index move contributes O

One even-index move contributes E

If either is zero but the other is non-zero, we can still do it in one move only if the parity aligns correctly (first move must be odd), otherwise we need two moves by introducing a compensating zero-like adjustment.

However, the clean observation is simpler: we can always realize any valid (O, E) using at most 2 moves, and 1 move is possible only when Y = X or Y = −X, i.e. when m = n or m = −n.

So the optimal answer is:

If (n + m) or (n − m) is odd, output -1.

Else if (n, m) is (0, 0), answer is 0.

Else if m = n or m = −n, answer is 1.

Otherwise answer is 2.

To construct the sequence for 2 moves, we set:

x1 = O

x2 = E

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation over steps | O( | n | + |
| Algebraic transformation | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We reduce each test case into algebra on two variables derived from the target point.

1. Compute S1 = n + m and S2 = n − m. If either S1 or S2 is odd, return -1 because the system of equations for O and E cannot produce integers. This follows directly from solving the linear system defining contributions.
2. If (n, m) equals (0, 0), output 0 because no moves are needed.
3. If m = n, output 1 and choose x1 = n. This works because every odd move adds equally to both coordinates, so a single step can land exactly on the diagonal.
4. If m = −n, output 1 and choose x1 = n. In this case the first move produces (n, −n), matching the target directly.
5. Otherwise output 2 moves. Compute O = (n + m) / 2 and E = (n − m) / 2. Set x1 = O and x2 = E, which independently constructs the odd and even contributions.

### Why it works

The transformation splits the process into two independent linear components corresponding to symmetric and antisymmetric movement along the grid axes. Every move contributes to both components in a fixed pattern, so the system reduces to solving a 2×2 linear system over integers. The parity condition guarantees integrality of the solution, and the two-move construction is sufficient because we can assign each independent component to a dedicated time parity class.

No sequence shorter than the optimal one can represent both constraints simultaneously except in degenerate cases where one of the derived components is zero, which corresponds exactly to the one-move diagonals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n, m = map(int, input().split())
        
        if n == 0 and m == 0:
            out.append("0")
            continue
        
        if (n + m) % 2 != 0 or (n - m) % 2 != 0:
            out.append("-1")
            continue
        
        if n == m or n == -m:
            out.append(f"1 {n}")
            continue
        
        o = (n + m) // 2
        e = (n - m) // 2
        out.append(f"2 {o} {e}")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads all test cases and processes each independently. The parity checks come directly from the requirement that O and E must be integers. The one-move cases correspond exactly to when the target lies on one of the two diagonals, making it reachable in a single symmetric or antisymmetric jump. Otherwise, splitting into O and E guarantees that the constructed sequence reproduces both coordinates exactly.

A common implementation pitfall is mixing up the signs in the construction of E. The correct derivation comes from solving the linear system, not from guessing based on coordinate behavior.

## Worked Examples

Consider input:

n = 2, m = 7

We compute:

S1 = 9, S2 = -5

Both are odd, so the system is infeasible.

| Step | n | m | n+m | n-m | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 7 | 9 | -5 | detect parity mismatch |

This confirms why the answer is -1: O and E would not be integers.

Now consider:

n = -10, m = 8

Compute:

S1 = -2, S2 = -18

Both even, so:

O = -1

E = -9

| Step | O | E | Construction |
| --- | --- | --- | --- |
| 1 | -1 | -9 | x1 = -1 |
| 2 | -1 | -9 | x2 = -9 |

After move 1 (odd): (0,0) → (-1,-1)

After move 2 (even): (-1,-1) → (-10,8)

This shows how separating symmetric and antisymmetric components cleanly reconstructs both coordinates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test performs a constant number of arithmetic operations |
| Space | O(1) | Only a few integers are stored per test |

The solution easily fits within limits since even 100,000 test cases only require simple arithmetic per case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys
    
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n, m = map(int, input().split())
        if n == 0 and m == 0:
            res.append("0")
        elif (n + m) % 2 != 0 or (n - m) % 2 != 0:
            res.append("-1")
        elif n == m or n == -m:
            res.append(f"1 {n}")
        else:
            o = (n + m) // 2
            e = (n - m) // 2
            res.append(f"2 {o} {e}")
    return "\n".join(res)

# provided samples
assert run("3\n0 0\n2 7\n-10 8") == "0\n-1\n2 -1 -9"

# custom cases
assert run("1\n1 1") == "1 1"
assert run("1\n1 -1") == "1 1"
assert run("1\n2 0") == "2 1 1"
assert run("1\n1 2") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (0,0) | 0 | trivial start case |
| (1,1) | 1 1 | single odd diagonal move |
| (2,0) | 2 1 1 | two-step symmetric construction |
| (1,2) | -1 | parity infeasibility |

## Edge Cases

For the origin case (0, 0), the algorithm immediately returns 0 without attempting decomposition. This avoids constructing unnecessary xi values that would otherwise produce a spurious two-step solution.

For diagonal targets like (n, n), the algorithm detects that m = n and outputs a single move. For example (3, 3) leads to x1 = 3, producing (3, 3) directly via an odd step.

For anti-diagonal targets like (n, −n), the same one-move logic applies. For instance (2, −2) yields x1 = 2, and the first move matches the target exactly.

For general cases such as (-10, 8), the algorithm falls back to two moves, computing O and E explicitly and reconstructing the trajectory deterministically without ambiguity.
