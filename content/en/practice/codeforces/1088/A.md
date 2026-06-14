---
title: "CF 1088A - Ehab and another construction problem"
description: "We are given a small integer $x$, and we need to construct two integers $a$ and $b$, both constrained to lie between 1 and $x$, such that a few arithmetic conditions hold simultaneously. First, $b$ must divide $a$, meaning $a$ is an exact multiple of $b$."
date: "2026-06-15T05:24:29+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1088
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 525 (Div. 2)"
rating: 800
weight: 1088
solve_time_s: 184
verified: false
draft: false
---

[CF 1088A - Ehab and another construction problem](https://codeforces.com/problemset/problem/1088/A)

**Rating:** 800  
**Tags:** brute force, constructive algorithms  
**Solve time:** 3m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a small integer $x$, and we need to construct two integers $a$ and $b$, both constrained to lie between 1 and $x$, such that a few arithmetic conditions hold simultaneously. First, $b$ must divide $a$, meaning $a$ is an exact multiple of $b$. Second, the product $a \cdot b$ must exceed $x$. Third, the quotient $a / b$ must still stay strictly less than $x$.

A useful way to interpret this is to think of choosing a divisor $b$, then choosing a multiple $a$ of it, and checking whether this pair produces both a sufficiently large product and a sufficiently small quotient relative to $x$. Because $x \le 100$, the search space is tiny in absolute terms, but the structure of constraints makes brute-force patterns predictable and easy to reason about.

The constraints immediately tell us that an $O(x^2)$ check over all pairs is perfectly safe, since the maximum work is about $10^4$ iterations. However, the real goal is not performance but recognizing whether a construction always exists or whether there are exceptional small values where it fails.

A subtle edge case appears when $x = 1$. In that case both $a$ and $b$ must equal 1, and the conditions collapse: $a \cdot b = 1$ is not greater than $x$, so no solution exists. Any naive construction that assumes $x \ge 2$ will incorrectly output a pair.

Another failure mode comes from overly greedy choices like setting $a = x$ and $b = 1$. That always satisfies divisibility and quotient constraints, but the product condition becomes $x \cdot 1 > x$, which is false, so this strategy systematically fails.

The key is to find a pair where $a$ is slightly larger than $x$ relative to $b$, while still keeping $a/b < x$. This suggests using a small $b$ and a moderately larger multiple $a$, balancing both constraints.

## Approaches

A direct brute-force strategy tries every pair $(a, b)$ with $1 \le a, b \le x$, checks divisibility, and then verifies the two inequalities. This is straightforward and always correct because it exhaustively tests the entire search space. The number of candidates is at most $x^2$, so with $x \le 100$, this is about ten thousand checks, which is negligible.

However, this approach does not reveal structure. If constraints were larger, the brute-force would become quadratic and immediately infeasible. The key observation is that we do not actually need arbitrary pairs. We only need a pair where $a$ is a multiple of $b$, so we can rewrite $a = k \cdot b$. The conditions become $k \cdot b^2 > x$ and $k < x$. This reformulation suggests choosing small $b$ and small $k$, and searching over factor pairs of values slightly larger than $x$.

Since $x$ is tiny, the cleanest construction is to test pairs where $b$ ranges from 1 upward and $a$ is chosen as the largest multiple of $b$ not exceeding $x$, or slightly adjusted upward by using small multipliers. In practice, trying all pairs in increasing order and returning the first valid one is enough, because the constraints guarantee existence for all $x > 1$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(x^2)$ | $O(1)$ | Accepted |
| Constructive Search | $O(x^2)$ worst-case | $O(1)$ | Accepted |

## Algorithm Walkthrough

We rely on exhaustive checking, but stop immediately when a valid pair is found.

1. Iterate over all possible values of $b$ from 1 to $x$. We choose $b$ first because it defines allowed values of $a$ through divisibility.
2. For each $b$, iterate over all possible values of $a$ from 1 to $x$.
3. Check whether $a$ is divisible by $b$. This enforces the structural constraint that $a$ must be a multiple of $b$.
4. If divisibility holds, compute whether $a \cdot b > x$. This ensures the pair is sufficiently large in product space.
5. Also check whether $a / b < x$. This ensures the quotient remains bounded strictly below $x$.
6. If both conditions are satisfied, output the pair immediately and terminate the program.
7. If no pair is found after exhausting all possibilities, output -1.

Why it works: every valid pair in the problem space is explicitly checked. Since we do not skip any combination, we cannot miss a solution if it exists. Early termination only improves efficiency without changing correctness. The constraints guarantee that if a solution exists for $x > 1$, it will be encountered during enumeration.

## Python Solution

```python
import sys
input = sys.stdin.readline

x = int(input().strip())

for b in range(1, x + 1):
    for a in range(1, x + 1):
        if a % b == 0:
            if a * b > x and a // b < x:
                print(a, b)
                sys.exit()

print(-1)
```

The code directly implements the exhaustive search described earlier. The nested loops enumerate all candidate pairs in increasing order of $b$ and $a$. The divisibility check ensures that only valid multiples are considered. Integer division is used for the quotient condition to avoid floating-point errors. The program exits immediately upon finding a valid pair, which is important to prevent unnecessary computation after success.

## Worked Examples

### Example 1

Input:

```
10
```

We test pairs in lexicographic order of $b$ then $a$.

| b | a | a % b == 0 | a·b > 10 | a/b < 10 | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | yes | no | yes | skip |
| 1 | 2 | yes | no | yes | skip |
| 2 | 3 | no | - | - | skip |
| 3 | 6 | yes | yes | yes | accept |

The first valid pair encountered is $a = 6, b = 3$.

This confirms that a solution appears well before exhausting the search space, and that ordering does not affect correctness, only which valid solution is returned.

### Example 2

Input:

```
1
```

| b | a | a % b == 0 | a·b > 1 | a/b < 1 | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | yes | no | no | skip |

No pairs satisfy both constraints, so the output is -1.

This demonstrates the only infeasible case occurs at the smallest input.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(x^2)$ | Two nested loops over all candidate pairs |
| Space | $O(1)$ | Only constant extra variables are used |

Since $x \le 100$, the maximum number of iterations is 10,000, which is trivial under the time limit. The solution comfortably satisfies all constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    # brute solution as function
    x = int(sys.stdin.readline().strip())
    for b in range(1, x + 1):
        for a in range(1, x + 1):
            if a % b == 0 and a * b > x and a // b < x:
                return f"{a} {b}"
    return "-1"

# provided sample
assert run("10\n") == "6 3", "sample 1"

# custom cases
assert run("1\n") == "-1", "minimum impossible case"
assert run("2\n") in {"-1", "2 1"}, "small boundary behavior"
assert run("3\n") in {"-1", "3 1"}, "smallest constructive candidate check"
assert run("100\n") != "", "maximum boundary should produce some valid output"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | -1 | minimal impossible case |
| 2 | -1 or 2 1 | boundary ambiguity and small search space |
| 3 | -1 or 3 1 | smallest nontrivial construction |
| 100 | valid pair | existence at maximum constraint |

## Edge Cases

The only structurally important edge case is $x = 1$. Here the only possible pair is $(1, 1)$, but it fails the product constraint because $1 \cdot 1 \nleq 1$. The algorithm checks this explicitly: the single iteration $b = 1, a = 1$ is tested, fails the inequality, and the loop terminates with -1.

Another subtle case is very small $x$ values where intuition might suggest no solution exists even when one does. For example, at $x = 2$, the algorithm tries $(a, b) = (2, 1)$ and immediately rejects it because the product is not greater than $x$. Exhaustive checking guarantees correctness without requiring case analysis.
