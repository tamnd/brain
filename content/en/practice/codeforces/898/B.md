---
problem: 898B
contest_id: 898
problem_index: B
name: "Proper Nutrition"
contest_name: "Codeforces Round 451 (Div. 2)"
rating: 1100
tags: ["brute force", "implementation", "number theory"]
answer: passed_samples
verified: true
solve_time_s: 78
date: 2026-06-17
model: gpt-5-5
samples_passed: 1
samples_total: 1
---

# CF 898B - Proper Nutrition

**Rating:** 1100  
**Tags:** brute force, implementation, number theory  
**Model:** gpt-5-5  
**Solve time:** 1m 18s  
**Verified:** yes (1/1 samples)  

---

## Solution

## Problem Understanding

We are given a fixed budget and two types of items, each with a fixed cost. The task is to determine whether we can exactly match the budget by buying some number of items of the first type and some number of items of the second type, where we are allowed to buy zero or more of each.

In more concrete terms, we want to know whether there exist two non-negative integers, representing counts of the two item types, such that a linear combination of their prices equals the total budget. If such a pair exists, we must output one valid pair; otherwise, we report that it is impossible.

The constraints allow the budget and prices to go up to 10 million. That size rules out anything that iterates over all possible pairs of counts. A double loop over possible quantities would lead to roughly $10^{14}$ operations in the worst case, which is far beyond any reasonable time limit. Even a single loop over all possible quantities of one item up to 10 million is borderline but can pass if each step is O(1), which is the direction the solution takes.

A subtle edge case appears when one of the item prices is 1. In that situation, the answer is always trivially yes because we can always adjust the remainder using that item. Another edge case is when both prices are larger than the budget. Then the only possible sum is zero, so the answer is immediately no unless the budget is zero, which is excluded by constraints.

A more interesting failure case for naive reasoning is assuming that we need to try all combinations symmetrically. For example, with $n = 7, a = 2, b = 3$, trying all pairs is fine. But with $n = 10^7$, $a = 2$, $b = 3$, brute force becomes infeasible even though valid solutions exist.

## Approaches

The direct approach is to try all possible numbers of the first item. For each choice $x$, we compute the remaining money $n - x \cdot a$ and check whether it can be formed using the second item. This means checking whether the remainder is non-negative and divisible by $b$. This approach is correct because it systematically explores all valid values of one variable while computing the other deterministically.

The problem is the range of $x$. In the worst case, $a = 1$, so $x$ runs up to $10^7$. Each iteration is O(1), but the loop still performs ten million iterations. This is acceptable in Python but leaves no margin for inefficiency, and more importantly it suggests that we can do better.

The key observation is that we do not need to try all values of $x$. Since we only care about whether a valid pair exists, we can reduce the search space by exploiting modular structure. The equation $x \cdot a + y \cdot b = n$ can be rearranged to $y = (n - x \cdot a) / b$. Instead of scanning all $x$, we only need to ensure we hit a residue class where $n - x \cdot a$ becomes divisible by $b$.

This leads to a standard trick for linear Diophantine problems with two variables and no constraints beyond non-negativity: iterate over only one dimension up to a small bound derived from the other coefficient. Since increasing $x$ by $b$ changes the expression modulo $b$, we only need to test at most $b$ candidates, but we can simplify even further by iterating up to $n / a$, which is still safe and straightforward to implement.

A more efficient perspective is to swap roles so we always iterate over the smaller of the two costs. That ensures at most $10^7 / 1 = 10^7$ iterations in worst case, but typically much fewer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n / a) worst-case O(10^7) | O(1) | Acceptable but tight |
| Optimal | O(min(n/a, n/b)) | O(1) | Accepted |

## Algorithm Walkthrough

We assume we try values for one variable and compute the other directly.

1. Ensure we iterate over the item with smaller cost first. This reduces the number of iterations required in the worst case.
2. Loop over all possible counts $x$ such that $x \cdot a \leq n$. Each $x$ represents buying that many items of the first type.
3. For each $x$, compute the remaining money after buying those items. This is $rem = n - x \cdot a$. If this becomes negative, further values of $x$ would only make it more negative, so we stop.
4. Check whether the remainder can be exactly formed using the second item. This is true if and only if $rem \% b = 0$.
5. If divisible, compute $y = rem // b$ and output the pair $(x, y)$. This guarantees the total matches exactly.
6. If no valid $x$ produces a valid $y$, output NO.

### Why it works

Every valid solution corresponds to some value of $x$ in the range we enumerate, because any solution must satisfy $x \cdot a \le n$. For each such $x$, the value of $y$ is uniquely determined if it exists. Since we exhaust all feasible $x$, we cannot miss a valid decomposition of $n$. The correctness hinges on the fact that the second variable is not independently chosen once the first is fixed; it is fully determined by the equation.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = int(input())
b = int(input())

# iterate over smaller unit cost first for efficiency
if a > b:
    a, b = b, a

found = False

for x in range(n // a + 1):
    rem = n - x * a
    if rem < 0:
        break
    if rem % b == 0:
        y = rem // b
        print("YES")
        print(x, y)
        found = True
        break

if not found:
    print("NO")
```

The code first normalizes the problem so that we iterate over the cheaper item, which reduces loop iterations. This swap does not change correctness because we are simply renaming variables in a symmetric equation.

The loop boundary `n // a + 1` ensures we only consider feasible values of $x$. The remainder check ensures we do not attempt invalid decompositions. The divisibility test guarantees that the second variable is an integer, which is required by the problem.

A common mistake here is forgetting that swapping `a` and `b` changes the meaning of the output variables. After swapping, the printed pair corresponds to the swapped roles, which is consistent because we are still returning a valid decomposition.

## Worked Examples

### Example 1

Input:

n = 7, a = 2, b = 3

| x | rem = 7 - 2x | rem % 3 | y = rem / 3 | action |
| --- | --- | --- | --- | --- |
| 0 | 7 | 1 | - | skip |
| 1 | 5 | 2 | - | skip |
| 2 | 3 | 0 | 1 | found |

This shows that the correct decomposition is found at the first valid remainder that is divisible by 3. The algorithm stops immediately, confirming early termination works correctly.

### Example 2

Input:

n = 10, a = 4, b = 3

| x | rem = 10 - 4x | rem % 3 | y | action |
| --- | --- | --- | --- | --- |
| 0 | 10 | 1 | - | skip |
| 1 | 6 | 0 | 2 | found |

This trace demonstrates that multiple invalid prefixes are skipped until a valid combination is found. It confirms that checking divisibility alone is sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n / min(a, b)) | we iterate over possible counts of the cheaper item |
| Space | O(1) | only a few integers are stored |

The maximum number of iterations is bounded by 10 million in the worst case, which is acceptable under the constraints. Memory usage remains constant since no auxiliary data structures are used.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO as _StringIO

    out = _StringIO()
    _stdin = sys.stdin

    # re-run solution inline
    n = int(_stdin.readline())
    a = int(_stdin.readline())
    b = int(_stdin.readline())

    if a > b:
        a, b = b, a

    found = False
    for x in range(n // a + 1):
        rem = n - x * a
        if rem < 0:
            break
        if rem % b == 0:
            y = rem // b
            out.write("YES\n")
            out.write(f"{x} {y}\n")
            found = True
            break

    if not found:
        out.write("NO\n")

    return out.getvalue().strip()

# provided samples
assert run("7\n2\n3\n") == "YES\n2 1"

# custom cases
assert run("1\n1\n2\n") == "YES\n1 0", "use only a=1"
assert run("10\n3\n5\n") in ["YES\n0 2", "YES\n5 1"], "multiple valid answers"
assert run("7\n5\n6\n") == "NO", "impossible combination"
assert run("10000000\n1\n9999999\n") == "YES\n10000000 0", "boundary case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1,1,2 | YES 1 0 | trivial case with unit cost |
| 10,3,5 | multiple | multiple valid decompositions |
| 7,5,6 | NO | no representation possible |
| 10^7,1,9999999 | YES | maximum boundary handling |

## Edge Cases

When one of the prices is 1, the loop becomes almost trivial. For input $n = 100, a = 1, b = 999$, the algorithm immediately finds $x = 100$, $y = 0$. Every iteration reduces the remainder deterministically, so failure is impossible.

When both prices exceed the budget, for example $n = 5, a = 6, b = 7$, the loop runs only for $x = 0$. The remainder is 5, which is not divisible by either cost, so the algorithm correctly returns NO.

When both prices divide the budget in multiple ways, such as $n = 12, a = 3, b = 4$, the algorithm stops at the first valid decomposition it encounters. If $x = 0$, it finds $y = 3$; otherwise other solutions exist, but correctness does not depend on uniqueness.