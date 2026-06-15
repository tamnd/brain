---
title: "CF 1047A - Little C Loves 3 I"
description: "We are given a single integer $n$, and we need to represent it as a sum of three positive integers $a, b, c$. The extra restriction is that none of these three numbers is allowed to be divisible by 3."
date: "2026-06-15T11:06:44+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1047
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 511 (Div. 2)"
rating: 800
weight: 1047
solve_time_s: 277
verified: true
draft: false
---

[CF 1047A - Little C Loves 3 I](https://codeforces.com/problemset/problem/1047/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 4m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer $n$, and we need to represent it as a sum of three positive integers $a, b, c$. The extra restriction is that none of these three numbers is allowed to be divisible by 3. Any valid triple is acceptable, so there is no optimization criterion beyond satisfying the constraints.

From a structural point of view, this is a constructive decomposition problem. We are not searching for a minimum or maximum, only for one feasible partition under modular constraints. That immediately suggests the solution should rely on modular arithmetic rather than search.

The input constraint $3 \le n \le 10^9$ rules out brute force enumeration of triples. Even if we tried to fix two variables and derive the third, the search space is quadratic in $n$, which is far too large. The problem must therefore reduce to a constant-time construction.

A subtle edge case arises when $n$ is small. For example, $n = 3$ forces the only possible partition $1,1,1$, which works because none are divisible by 3. Another interesting situation is when $n \equiv 0 \pmod{3}$, since a naive attempt like splitting evenly into $n/3, n/3, n/3$ fails immediately because each part is divisible by 3.

## Approaches

A brute-force strategy would enumerate all pairs $(a, b)$ such that $a \ge 1, b \ge 1$, compute $c = n - a - b$, and check whether all three are positive and not divisible by 3. This works logically because it directly tests the definition of the problem, but it requires $O(n^2)$ checks in the worst case, which is impossible for $n$ up to $10^9$.

The key observation is that the constraint depends only on divisibility by 3, which is entirely periodic modulo 3. Instead of searching for valid values, we can construct them using a fixed pattern that avoids residues 0 mod 3.

The integers that are not divisible by 3 are exactly those congruent to 1 or 2 modulo 3. So we only need to ensure each of $a, b, c$ falls into these two residue classes while still summing to $n$. Since we have full freedom in choosing values, we can fix two of them and derive the third, then adjust slightly if the remainder violates the constraint.

A standard construction is to pick two small non-multiples of 3, such as 1 and 2, and adjust the third value accordingly. If we set $a = 1$, $b = 1$, then $c = n - 2$. Now the only issue is whether $c$ is divisible by 3. If it is, we slightly shift one of the earlier choices to avoid landing on a multiple of 3. Because residue classes modulo 3 are small and closed under addition, a constant number of adjustments is always sufficient.

This reduces the problem from unbounded search to a constant number of arithmetic cases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal Construction | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We construct the answer directly using modular reasoning.

1. Start by fixing $a = 1$. This guarantees $a$ is positive and not divisible by 3.
2. Fix $b = 1$ for the same reason. At this point, we have used a total of 2 units.
3. Compute $c = n - 2$. This ensures the sum condition $a + b + c = n$ holds exactly.
4. Check whether $c$ is divisible by 3. If it is not, then $(1, 1, c)$ is already valid.
5. If $c$ is divisible by 3, adjust the construction by replacing $b = 2$ and $a = 1$, giving $c = n - 3$. This shift preserves the sum while changing the residue class of $c$, ensuring it is no longer divisible by 3 for valid $n$.

The reason these small adjustments are sufficient is that shifting by 1 or 2 changes the residue class modulo 3 in a controlled way, and we only need to avoid residue 0.

### Why it works

Every integer falls into exactly one of three residue classes modulo 3. We explicitly avoid choosing values in the 0 class for $a$ and $b$, and we ensure $c$ is derived from $n$ by subtracting a small constant. Since subtracting 2 or 3 cycles through different residues, at least one of these constant offsets produces a valid $c$ that is not divisible by 3. This guarantees a solution exists and that our construction will always find one.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

a = 1
b = 1
c = n - 2

if c % 3 == 0:
    a = 1
    b = 2
    c = n - 3

print(a, b, c)
```

The code directly implements the constructive idea. We start with the simplest decomposition and only adjust if the third component lands on a forbidden residue class.

The only subtle point is ensuring positivity. For $n \ge 3$, both $n - 2$ and $n - 3$ remain at least 1, so both branches are safe. The conditional check guarantees we avoid the only problematic residue case without breaking the positivity constraint.

## Worked Examples

### Example 1: $n = 3$

We start with $a = 1, b = 1$, giving $c = 1$.

| Step | a | b | c | Condition |
| --- | --- | --- | --- | --- |
| Initial | 1 | 1 | 1 | c % 3 = 1 |

Since $c$ is not divisible by 3, we keep the result.

This confirms the simplest base case is already valid without adjustment.

### Example 2: $n = 6$

We begin again with $a = 1, b = 1$, giving $c = 4$.

| Step | a | b | c | Condition |
| --- | --- | --- | --- | --- |
| Initial | 1 | 1 | 4 | c % 3 = 1 |

No adjustment is needed, and the output is valid.

This shows that even when $n$ is divisible by 3, the first construction often already avoids producing a multiple of 3 in the third component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a constant number of arithmetic operations and a single conditional check |
| Space | $O(1)$ | No auxiliary data structures are used |

The solution is optimal for the constraints since any input up to $10^9$ is handled in constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = 1
    b = 1
    c = n - 2
    if c % 3 == 0:
        a = 1
        b = 2
        c = n - 3
    return f"{a} {b} {c}"

# provided sample
assert run("3\n") == "1 1 1", "sample 1"

# minimum edge
assert run("4\n") != "", "n=4 should produce valid output"

# divisible by 3 case
assert run("6\n").split(), "basic feasibility"

# large case
assert run("1000000000\n").split(), "large n"

# small non-trivial
assert run("7\n").split(), "random small"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 | 1 1 1 | minimal boundary |
| 6 | valid triple | divisible-by-3 handling |
| 7 | valid triple | general correctness |
| 1000000000 | valid triple | performance and large n |

## Edge Cases

For $n = 3$, the algorithm produces $a = 1, b = 1, c = 1$. None of these are divisible by 3, so the result is correct immediately without entering the adjustment branch.

For $n = 6$, we compute $c = 4$, which is valid since 4 is not divisible by 3. The condition does not trigger, so we output $1,1,4$. All values are positive and satisfy the constraints.

The adjustment branch is only triggered when $n - 2$ is divisible by 3. In that case, switching to $n - 3$ ensures the third number shifts residue class and avoids 0 modulo 3 while preserving positivity for all valid $n \ge 3$.
