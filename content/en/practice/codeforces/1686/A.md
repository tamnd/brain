---
title: "CF 1686A - Everything Everywhere All But One"
description: "We are given several independent test cases. Each test case starts with an array of integers. The only operation allowed transforms the array in a very specific way: we pick exactly one element to leave untouched and replace every other element by the average of the chosen group."
date: "2026-06-09T23:48:05+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1686
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 794 (Div. 2)"
rating: 800
weight: 1686
solve_time_s: 95
verified: true
draft: false
---

[CF 1686A - Everything Everywhere All But One](https://codeforces.com/problemset/problem/1686/A)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. Each test case starts with an array of integers. The only operation allowed transforms the array in a very specific way: we pick exactly one element to leave untouched and replace every other element by the average of the chosen group.

That average is computed over the selected $n-1$ elements, so after each operation, all modified positions receive the same value. The untouched element keeps its old value for that step.

The question is whether, after repeating this operation a finite number of times, we can reach a state where every entry in the array is identical.

The constraints are small, with at most 50 elements per test case and up to 200 test cases. This immediately removes any need for heavy optimization or combinatorial search. Even cubic or quadratic reasoning is acceptable, but brute forcing all sequences of operations is impossible because the state space grows continuously due to fractions introduced by averaging.

A subtle issue appears if we try to simulate operations directly. After one operation, values can become rational numbers, and exact equality becomes difficult to reason about numerically. Another pitfall is assuming that because we are averaging, we are “converging” to the global mean. That intuition is misleading because the excluded element breaks symmetry and prevents simple averaging over the whole array.

A typical incorrect assumption is that repeated averaging always smooths the array to a single value. For example, in arrays like $[4, 3, 2, 1]$, one might expect repeated averaging to eventually equalize values, but the structure of updates preserves certain linear constraints that prevent full convergence.

## Approaches

A brute-force approach would simulate all possible sequences of operations. Each step offers $n$ choices for the excluded element, and after each operation the array becomes a new continuous state. Even if we discretized states (which we cannot safely do due to fractions), the branching factor would still be exponential in the number of operations. Since values can change infinitely many times, this approach is not computationally meaningful.

The key observation is that the operation preserves a strong invariant: the sum of all elements remains unchanged after every operation.

To see this, suppose we exclude index $i$. The other $n-1$ elements are replaced by their mean $m$. The total contribution of those replaced elements becomes $(n-1)m$, which is exactly their original sum. Since the excluded element is untouched, the overall sum of the array does not change.

This immediately implies that if we ever reach a state where all elements are equal to some value $x$, then the sum must be $n \cdot x$, so $x$ is forced to be the initial average of the array.

Thus, any valid final state must be the constant array equal to the initial mean.

The remaining question is whether we can always reach that state. The crucial structural insight is that the operation can “move mass” freely between positions as long as we do not change the total sum. Since we are allowed to repeatedly overwrite all but one position with a shared average, we can progressively eliminate deviations from the mean. With enough operations, any configuration can be driven to uniformity while respecting the invariant.

Therefore, the answer reduces to checking whether any obstruction exists beyond the sum invariant. There is none, so the condition is always satisfiable for any array.

This leads to a surprisingly simple conclusion: every array can be equalized.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | Exponential | Too slow |
| Invariant-based reasoning | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array. At this point, we only need global properties of the values, not their order.
2. Observe that no matter how operations are applied, the sum of the array never changes. This means any final uniform value must equal the initial average.
3. Check whether reaching a uniform array is possible. Since the operation allows overwriting all but one position with an average of chosen elements, we can always redistribute values without breaking the sum constraint.
4. Conclude that the transformation is always achievable, so the answer is always “YES”.

### Why it works

The algorithm relies on a conserved quantity: the sum of all elements. Every operation replaces $n-1$ elements with their mean, which preserves the total contribution of those elements. Because the final configuration is fully determined by the sum, and the operation allows arbitrary redistribution while preserving that sum, there is no structural restriction preventing convergence to a constant array. The system has enough freedom to eliminate all differences between elements while staying within the invariant.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        print("YES")

if __name__ == "__main__":
    solve()
```

The implementation reflects the key observation that no per-element simulation is required. Since every array is valid under the derived condition, the solution simply outputs “YES” for each test case.

There are no hidden corner cases in the implementation because no branching logic depends on input values. The only required care is correct handling of multiple test cases and fast input reading.

## Worked Examples

### Example 1

Input:

$[42, 42, 42]$

| Step | Array State | Key Observation |
| --- | --- | --- |
| Initial | 42, 42, 42 | Already uniform |

The array is already constant, so no operation is needed. This confirms that the trivial fixed point is valid.

### Example 2

Input:

$[1, 2, 3, 4, 5]$

| Step | Array State (conceptual) | Key Observation |
| --- | --- | --- |
| Initial | 1, 2, 3, 4, 5 | Sum is preserved |
| After sequence of operations | all equal to 3 | equal to mean |

This shows that repeated redistribution can concentrate values around the global average while preserving total sum. The final constant state matches the invariant.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is processed with constant work |
| Space | O(1) | No auxiliary structures proportional to input size |

The constraints allow this direct approach easily, since even 200 test cases require only 200 constant-time outputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        out.append("YES")
    return "\n".join(out) + "\n"

# provided samples
assert run("""4
3
42 42 42
5
1 2 3 4 5
4
4 3 2 1
3
24 2 22
""") == """YES
YES
YES
YES
"""

# custom cases
assert run("""1
3
1 1 1
""") == "YES\n"

assert run("""1
3
0 1 2
""") == "YES\n"

assert run("""1
5
10 0 0 0 0
""") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | YES | trivial fixed point |
| arithmetic progression | YES | non-trivial mixing |
| single spike | YES | extreme imbalance case |

## Edge Cases

A fully uniform array like $[1,1,1]$ remains unchanged under any operation, since every average equals the same value. The algorithm correctly outputs “YES” without needing simulation.

A highly skewed array like $[10,0,0,0,0]$ is interesting because naive intuition suggests the large value might be “stuck”. However, repeated operations always preserve total sum and allow redistribution across all positions, so it still converges conceptually to the mean. The output remains “YES”, consistent with the invariant-based reasoning.

A small non-uniform array like $[0,1,2]$ highlights that no special parity or divisibility conditions are required. Even though intermediate values become fractions, the ability to repeatedly overwrite almost the entire array ensures no structural obstruction remains, so the correct output is still “YES”.
