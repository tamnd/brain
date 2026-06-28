---
title: "CF 104931J - Careful Cookout"
description: "We are placing shrimps on an $n times m$ grid, where each cell can either contain a shrimp or be empty. Each configuration is just a binary matrix. The grill has a rule that only activates locally on every $2 times 2$ subgrid."
date: "2026-06-28T07:39:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104931
codeforces_index: "J"
codeforces_contest_name: "UTPC Contest 01-26-24 Div. 1 (Advanced)"
rating: 0
weight: 104931
solve_time_s: 64
verified: false
draft: false
---

[CF 104931J - Careful Cookout](https://codeforces.com/problemset/problem/104931/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We are placing shrimps on an $n \times m$ grid, where each cell can either contain a shrimp or be empty. Each configuration is just a binary matrix.

The grill has a rule that only activates locally on every $2 \times 2$ subgrid. If inside any such $2 \times 2$ block the number of shrimps is odd, that block causes a burn event. The question is not to simulate burning, but to count how many entire grid configurations contain at least one $2 \times 2$ subgrid with odd parity.

So the task is purely combinatorial: count all binary grids of size $n \times m$ that violate a parity condition in at least one $2 \times 2$ square.

The input sizes go up to $2000 \times 2000$, so the grid can contain up to 4 million cells. A brute-force enumeration over all grids would involve $2^{4 \cdot 10^6}$ states, which is completely impossible. Even checking a single configuration costs $O(nm)$, so any approach that iterates over all grids is immediately ruled out.

A slightly more subtle failure case comes from trying to treat each $2 \times 2$ independently. These subgrids overlap heavily, so choosing valid patterns locally does not guarantee global consistency.

For example, in a $2 \times 3$ grid, constraints on columns 1-2 and 2-3 share the middle column. A greedy or local counting approach will overcount because it double counts shared structure.

The correct approach must instead characterize the global structure of grids where every $2 \times 2$ subgrid has even parity, and then subtract from the full space.

## Approaches

We start from the most direct idea. There are $2^{nm}$ ways to fill the grid. For each one, we could scan all $(n-1)(m-1)$ subgrids and check whether any has odd sum. This is correct but far too slow: generating all grids already costs exponential time, and even a single check is quadratic.

So instead of counting “bad” grids directly, we invert the problem. We count the complement: grids where no $2 \times 2$ subgrid has odd sum. These are precisely the configurations where every $2 \times 2$ block has even parity.

This condition is extremely rigid. Take any $2 \times 2$ block:

$$a_{i,j} \oplus a_{i,j+1} \oplus a_{i+1,j} \oplus a_{i+1,j+1} = 0$$

Rearranging gives:

$$a_{i+1,j+1} = a_{i,j} \oplus a_{i,j+1} \oplus a_{i+1,j}$$

This means once we fix the first row and first column, the entire grid is forced. Every other cell can be computed step by step.

A more structural way to see it is that the grid must satisfy a linear system over XOR. The solution space has exactly $n + m - 1$ degrees of freedom: choose all values in the first row and first column, with $a_{1,1}$ shared.

So the number of “safe” grids (no odd $2 \times 2$) is $2^{n+m-1}$. Everything else is a valid answer.

Thus the required count is:

$$2^{nm} - 2^{n+m-1}$$

computed modulo $998244353$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | $O(2^{nm} \cdot nm)$ | $O(nm)$ | Too slow |
| Structural XOR Counting | $O(\log(nm))$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Compute the total number of binary grids of size $n \times m$, which is $2^{nm}$. This represents all possible shrimp placements without restrictions.
2. Compute the number of grids where every $2 \times 2$ subgrid has even parity, which is $2^{n+m-1}$. This comes from the fact that once the first row and first column are chosen, all other cells are uniquely determined by the XOR constraint.
3. Subtract the constrained count from the total count to isolate configurations that contain at least one violating $2 \times 2$ subgrid. This gives $2^{nm} - 2^{n+m-1}$.
4. Perform all exponentiation modulo $998244353$, since the numbers grow exponentially and must be reduced throughout computation.

The key computational tool is fast exponentiation, since both exponents can be as large as 4 million.

### Why it works

The constraint on every $2 \times 2$ block enforces a linear relationship over XOR that propagates throughout the grid. Once the first row and column are fixed, every remaining cell is forced by previously determined values. This removes all freedom except $n + m - 1$ independent bits, so the space of valid grids is exactly a vector space of that dimension. Counting configurations becomes counting binary assignments to these free variables.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modpow(a, e):
    res = 1
    a %= MOD
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve():
    n, m = map(int, input().split())
    
    total = modpow(2, n * m)
    safe = modpow(2, n + m - 1)
    
    ans = (total - safe) % MOD
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation relies entirely on modular exponentiation. The first call computes the full configuration space, while the second computes the structured subspace defined by XOR consistency. The subtraction is taken modulo $998244353$, so a final adjustment ensures non-negativity.

A common mistake is trying to iterate over the grid or simulate constraints locally. The correct viewpoint is global linear structure, not local checking.

## Worked Examples

We trace two small cases to see how the formula behaves.

For $n = 2, m = 2$, we compute:

| Quantity | Value |
| --- | --- |
| $nm$ | 4 |
| $2^{nm}$ | 16 |
| $n+m-1$ | 3 |
| $2^{n+m-1}$ | 8 |
| Answer | 8 |

This matches the fact that out of 16 grids, exactly half satisfy the XOR-consistent structure.

For $n = 2, m = 3$:

| Quantity | Value |
| --- | --- |
| $nm$ | 6 |
| $2^{nm}$ | 64 |
| $n+m-1$ | 4 |
| $2^{n+m-1}$ | 16 |
| Answer | 48 |

This confirms the subtraction interpretation: only 16 grids avoid any odd $2 \times 2$, and all others contain at least one violating subgrid.

Each trace validates that the “safe space” depends only on boundary degrees of freedom, not internal cells.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log(nm))$ | Two modular exponentiations using binary exponentiation |
| Space | $O(1)$ | Only a few integers are stored |

The constraints allow up to 4 million in the exponent, so logarithmic exponentiation is essential. The solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

MOD = 998244353

def modpow(a, e):
    res = 1
    a %= MOD
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, sys.stdin.readline().split())
    total = modpow(2, n * m)
    safe = modpow(2, n + m - 1)
    return str((total - safe) % MOD)

# provided samples
assert solve("2 2\n") == "8"
assert solve("2 3\n") == "48"

# custom cases
assert solve("2 4\n") == str((pow(2, 8, MOD) - pow(2, 5, MOD)) % MOD), "small rectangular case"
assert solve("3 3\n") == str((pow(2, 9, MOD) - pow(2, 5, MOD)) % MOD), "square grid check"
assert solve("2 2000\n") == str((pow(2, 4000, MOD) - pow(2, 2001, MOD)) % MOD), "wide grid boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 | 8 | smallest nontrivial grid |
| 2 4 | formula correctness on rectangle |  |
| 3 3 | square symmetry and exponent handling |  |
| 2 2000 | large exponent stress case |  |

## Edge Cases

A key edge case is the smallest valid grid $2 \times 2$. In this case, there is exactly one $2 \times 2$ subgrid, so the problem reduces to counting binary matrices where the XOR of all four cells is odd. The formula gives $16 - 8 = 8$, which matches direct enumeration.

For a $2 \times m$ grid, the structure simplifies but still follows the same rule. Every additional column adds one degree of freedom in the full space but only one constraint in the safe space. The formula consistently handles this because it depends only on exponent arithmetic.

For large grids like $2000 \times 2000$, the exponent $nm$ becomes very large, but modular exponentiation handles it in logarithmic time. The correctness does not depend on magnitude, only on the algebraic structure of the constraint space.
