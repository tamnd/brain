---
problem: 1260B
contest_id: 1260
problem_index: B
name: "Obtain Two Zeroes"
contest_name: "Educational Codeforces Round 77 (Rated for Div. 2)"
rating: 1300
tags: ["binary search", "math"]
answer: passed_samples
verified: true
solve_time_s: 289
date: 2026-06-13
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2d7f9c-3e08-83ec-a865-d8e20e6df5bb
---

# CF 1260B - Obtain Two Zeroes

**Rating:** 1300  
**Tags:** binary search, math  
**Model:** gpt-5-3-mini  
**Solve time:** 4m 49s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2d7f9c-3e08-83ec-a865-d8e20e6df5bb  

---

## Solution

## Problem Understanding

We are given two piles of units, described by integers $a$ and $b$. In one move we are allowed to pick a positive integer $x$ and apply one of two transformations: either we subtract $x$ from $a$ and $2x$ from $b$, or we subtract $2x$ from $a$ and $x$ from $b$. We can repeat these moves any number of times, choosing different values of $x$ each time.

The question is whether it is possible to completely drain both piles to zero at the same time, without ever making a value negative.

The constraints are small in terms of number of test cases, but the values of $a$ and $b$ can be as large as $10^9$. That rules out any simulation that tries to apply operations step by step, because the magnitude of reductions is too large and the space of choices for $x$ is continuous over positive integers. Any correct solution must reduce the problem to a constant-time check per test case.

A subtle issue arises from the freedom to choose different values of $x$. A naive intuition might suggest greedily subtracting the larger value first, or always using $x=1$, but these approaches fail because the operations are not independent unit steps; each operation couples the two variables in a fixed ratio, so local greedy decisions can destroy global feasibility. For example, starting from $(1,2)$, greedily applying only the $(x,2x)$ operation fails immediately even though a valid sequence exists using both operation types.

The core difficulty is that we are not distributing a fixed number of unit operations, but combining two vector transformations with arbitrary scaling.

## Approaches

If we ignore efficiency, we could try to think in terms of repeatedly applying operations and exploring all possible sequences. Each operation reduces the pair $(a,b)$ by either $x(1,2)$ or $x(2,1)$. A brute-force search would branch over operation types and possible values of $x$, attempting to reach $(0,0)$. Even if we discretize $x$ to unit steps, the state space grows extremely fast because both coordinates can be as large as $10^9$. This makes any search-based method infeasible.

The key observation is that the order of operations does not matter. Only the total contribution of each operation type matters. Suppose we aggregate all operations of type $(1,2)$ into a total amount $p$, and all operations of type $(2,1)$ into a total amount $q$. Then the problem becomes solving a linear system where these aggregated contributions must exactly match $a$ and $b$.

This reduces the problem from reasoning about sequences to solving two linear equations with non-negative constraints. Once we do that, the structure becomes rigid enough that feasibility can be checked in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | O(1) | Too slow |
| Linear Equation Reduction | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We reinterpret the operations in terms of total accumulated usage of each operation type. Instead of thinking about individual moves, we group all $(1,2)$-type reductions together and all $(2,1)$-type reductions together.

1. Let $p$ represent the total amount contributed by operations of type $(1,2)$, and $q$ represent the total amount contributed by operations of type $(2,1)$. This is valid because scaling an operation by splitting $x$ into smaller parts does not change the net effect.
2. Express the final reductions on $a$ and $b$ in terms of $p$ and $q$. The total decrease in $a$ becomes $p + 2q$, while the total decrease in $b$ becomes $2p + q$. To reach zero, we require the system:

$$p + 2q = a, \quad 2p + q = b$$
3. Solve this system to understand feasibility conditions. Eliminating variables gives $3p = 2b - a$ and $3q = 2a - b$. This immediately implies both expressions must be non-negative and divisible by 3 for integer solutions to exist.
4. A simpler necessary condition emerges by adding the equations: $3(p+q) = a + b$, so $a + b$ must be divisible by 3. This condition already restricts most impossible cases.
5. The non-negativity constraints translate into geometric feasibility: neither coordinate can be too small relative to the other. Specifically, one must never require more reduction from one variable than can be supplied by combining both operation types.
6. Combining these conditions leads to a compact check: the sum must be divisible by 3, and neither $a$ nor $b$ can exceed twice the other.

### Why it works

Every operation reduces the total $a + b$ by exactly $3x$, so the total sum is invariant modulo 3 across all operations. This makes divisibility by 3 a hard requirement. Once that condition is satisfied, the entire process reduces to distributing this total reduction between two fixed vectors $(1,2)$ and $(2,1)$. These vectors form a two-dimensional basis, so any reachable endpoint corresponds exactly to a non-negative combination of them. The inequalities ensure that this combination does not require negative coefficients, which would correspond to reversing operations, something not allowed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())

        if (a + b) % 3 != 0:
            print("NO")
            continue

        if max(a, b) > 2 * min(a, b):
            print("NO")
            continue

        print("YES")

if __name__ == "__main__":
    solve()
```

The code directly implements the derived feasibility conditions. The first check enforces the modulo-3 invariant coming from the fact that every operation removes exactly $3x$ total units. The second check enforces that neither variable is too large compared to the other, which would make it impossible to balance reductions using the allowed operation ratios.

## Worked Examples

We trace the logic on two representative cases.

### Example 1: (6, 9)

| Step | a | b | a+b mod 3 | max condition | decision |
| --- | --- | --- | --- | --- | --- |
| start | 6 | 9 | 0 | 9 ≤ 12 | YES |

The sum is divisible by 3, and neither value dominates beyond the allowed factor of 2. This corresponds to a valid decomposition into the two operation types, so the answer is YES.

### Example 2: (1, 1)

| Step | a | b | a+b mod 3 | max condition | decision |
| --- | --- | --- | --- | --- | --- |
| start | 1 | 1 | 2 | 1 ≤ 2 | NO |

Even though the values are small and balanced, the total sum is not divisible by 3. Since every operation removes multiples of 3 from the sum, reaching zero is impossible.

The second example shows that balance alone is not sufficient; the modular constraint is the real limiting factor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case requires only a constant number of arithmetic checks |
| Space | $O(1)$ | No additional memory beyond input variables is used |

The solution easily fits within constraints since $t \le 100$ and each case is processed independently in constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        a, b = map(int, input().split())
        if (a + b) % 3 != 0:
            out.append("NO")
        elif max(a, b) > 2 * min(a, b):
            out.append("NO")
        else:
            out.append("YES")
    return "\n".join(out) + "\n"

# provided samples
assert run("3\n6 9\n1 1\n1 2\n") == "YES\nNO\nYES\n"

# custom cases
assert run("1\n0 0\n") == "YES\n", "already zero"
assert run("1\n2 2\n") == "NO\n", "sum not divisible by 3"
assert run("1\n2 4\n") == "YES\n", "valid balanced pair"
assert run("1\n1 1000000000\n") == "NO\n", "extreme imbalance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 0 | YES | trivial base case |
| 2 2 | NO | modular impossibility |
| 2 4 | YES | valid constructive ratio case |
| 1 1000000000 | NO | extreme imbalance constraint |

## Edge Cases

A frequent pitfall is relying only on the ratio condition without checking the modular constraint. For instance, $(2,4)$ satisfies balance intuition but fails if the sum condition is ignored in similar variants; here it actually works because the full system is consistent. The correct handling is always to enforce both constraints together, since one captures global conservation and the other captures directional feasibility of reductions.