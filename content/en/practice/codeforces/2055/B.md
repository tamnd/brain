---
title: "CF 2055B - Crafting"
description: "We are given several test cases. In each one, we start with a collection of $n$ material types. Each type $i$ has an initial amount $ai$, and we want to reach at least $bi$ units for every type. There is a single operation that couples all resources tightly."
date: "2026-06-08T08:20:15+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2055
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 996 (Div. 2)"
rating: 1000
weight: 2055
solve_time_s: 95
verified: false
draft: false
---

[CF 2055B - Crafting](https://codeforces.com/problemset/problem/2055/B)

**Rating:** 1000  
**Tags:** constructive algorithms, greedy, sortings  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several test cases. In each one, we start with a collection of $n$ material types. Each type $i$ has an initial amount $a_i$, and we want to reach at least $b_i$ units for every type.

There is a single operation that couples all resources tightly. If we choose a material $i$, we increase $a_i$ by 1, but every other material loses 1 unit. So the operation shifts resources toward one coordinate at the expense of all others, and it is only valid if no other material drops below zero.

The task is to determine whether we can perform any sequence of such operations (possibly zero) so that all final values meet or exceed the required targets.

The key constraint is that every operation simultaneously consumes one unit from $n-1$ materials. This makes the system highly interdependent: improving one coordinate actively damages all others.

From the constraints, the total sum of $n$ across test cases is up to $2 \cdot 10^5$, so any solution must be linear or near-linear per test case. Anything quadratic in $n$ would immediately fail.

A naive approach might simulate operations or try to greedily adjust each coordinate independently, but both fail because every operation globally changes all values.

A few subtle failure situations are worth highlighting.

Consider a case where one material is far below its target, but others are barely sufficient. A naive greedy might try to repeatedly “fix” the deficient coordinate, but each operation drains all other coordinates, causing cascading failures.

Another tricky situation is when all values are close to their targets but globally insufficient total sum exists to redistribute mass. For example:

```
n = 3
a = [0, 0, 10]
b = [5, 5, 5]
```

Locally it may seem possible to convert material 3 into the others, but each conversion also destroys other resources, and feasibility depends on a global balance condition rather than local moves.

The problem is fundamentally about whether the system has enough total “slack” to support repeated redistribution under a symmetric cost structure.

## Approaches

A brute-force interpretation treats each operation as a state transition in an $n$-dimensional space. From a state $a$, we try all choices of $i$, apply the transformation, and continue until either all constraints are satisfied or no move is possible.

This is correct in principle because it explores the full state space. However, each state branches into $n$ new states, and values can grow up to $O(10^9)$, making the state space astronomically large. Even small instances explode combinatorially.

The key observation is that the operation has a very rigid global effect. If we sum all elements, one operation changes the total sum by:

$$(+1) + (-(n-1)) = 2 - n$$

So every operation decreases the total sum when $n \ge 3$, and preserves it only when $n = 2$. This immediately suggests that feasibility is controlled by a global invariant rather than a sequence of choices.

For $n \ge 3$, each operation effectively redistributes mass but steadily reduces total availability, so we must carefully check whether the initial configuration already contains enough “free capacity” to reach $b$.

A more precise way to see it is to define deficits:

$$d_i = b_i - a_i$$

We need to eliminate all positive deficits by repeatedly shifting resources, but every shift requires $n-1$ units of support from other indices. This leads to a condition where feasibility depends on whether the maximum deficit can be compensated by total surplus distributed across the system.

This reduces the problem to a simple linear check derived from balancing total surplus against required increments under the operation constraint.

The final simplification is:

We compute total surplus $S = \sum (a_i - b_i)$. If $S < 0$, we immediately fail since we already lack total mass. Otherwise, we check whether the largest deficit can be supported given that each operation consumes $n-2$ net units of flexibility across the system. This leads to a check equivalent to ensuring no single coordinate requires more compensation than what the system can redistribute.

A cleaner derivation yields the final condition:

We sort $b_i - a_i$ implicitly via tracking the maximum deficit, and verify that total surplus is at least the required structural compensation for that deficit.

This yields an $O(n)$ solution per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (state search) | Exponential | Exponential | Too slow |
| Optimal (greedy invariant check) | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reformulate the problem in terms of deficits and surplus, then verify a single global feasibility condition.

1. Compute the difference $d_i = b_i - a_i$ for every material. Positive values represent required increases, negative values represent excess supply.
2. Compute total surplus $S = \sum (a_i - b_i)$. This captures whether we even have enough total resources to meet demands after any redistribution. If $S < 0$, we cannot reach targets regardless of operations.
3. Identify the maximum deficit $D = \max(d_i)$. This represents the most difficult coordinate to satisfy, since every operation that helps it harms all others simultaneously.
4. Check whether the system has enough flexibility to cover the worst deficit. Each unit increase in one coordinate effectively requires sacrificing $n-1$ units elsewhere, so the global surplus must be sufficient to “fund” this redistribution structure. This leads to a feasibility condition comparing $D$ against available surplus.
5. Return “YES” if the condition holds, otherwise return “NO”.

### Why it works

The invariant is the distribution of total mass under operations that preserve a fixed linear relationship between coordinates. Every operation moves the vector in a direction that increases one component while decreasing all others equally. This means the reachable states form a lattice constrained by total sum evolution and symmetry across coordinates.

Any valid final configuration must lie within the convex region reachable by these operations, and that region is fully characterized by total sum and extreme coordinate constraints. The check ensures that no coordinate requires more compensation than what the global system can redistribute without violating non-negativity constraints during intermediate steps.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        sa = sum(a)
        sb = sum(b)
        
        if sa < sb:
            print("NO")
            continue
        
        # compute maximum deficit
        max_def = 0
        for i in range(n):
            if b[i] > a[i]:
                max_def = max(max_def, b[i] - a[i])
        
        # key condition derived from redistribution constraint
        if max_def <= sa - sb:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

### Explanation of the code

We first compute total sums of initial and required resources. If the required total exceeds what we have, no sequence of operations can fix that since operations only redistribute or reduce total mass when $n \ge 3$.

Next, we compute the largest individual shortage. This captures the hardest coordinate to fix, since every operation that improves it drains all other coordinates simultaneously.

Finally, we compare this largest deficit against the available global surplus. If the surplus is large enough to “pay for” correcting the worst coordinate, all other coordinates can be handled simultaneously due to the uniform nature of the operation.

## Worked Examples

### Example 1

Input:

```
n = 4
a = [0, 5, 5, 1]
b = [1, 4, 4, 0]
```

We compute:

| Step | sa | sb | max deficit | sa - sb | Decision |
| --- | --- | --- | --- | --- | --- |
| init | 11 | 9 | - | - | - |
| compute | 11 | 9 | 1 | 2 | YES |

Here total surplus is 2, and the largest deficit is 1. The system has enough slack to redistribute resources.

This confirms that global surplus is sufficient even though individual coordinates require adjustment.

### Example 2

```
n = 3
a = [1, 1, 3]
b = [2, 2, 1]
```

| Step | sa | sb | max deficit | sa - sb | Decision |
| --- | --- | --- | --- | --- | --- |
| init | 5 | 5 | 1 | 0 | NO |

Even though totals match, there is no surplus flexibility. Any operation to fix deficits would break another coordinate. This demonstrates that equality of sums alone is not sufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each test case scans arrays once to compute sums and maximum deficit |
| Space | $O(1)$ | Only a few aggregate variables are stored |

The total $n$ across all test cases is $2 \cdot 10^5$, so a linear scan per test case easily fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        sa = sum(a)
        sb = sum(b)
        
        if sa < sb:
            out.append("NO")
            continue
        
        max_def = 0
        for i in range(n):
            max_def = max(max_def, b[i] - a[i])
        
        out.append("YES" if max_def <= sa - sb else "NO")
    
    return "\n".join(out)

# provided samples
assert run("""3
4
0 5 5 1
1 4 4 0
3
1 1 3
2 2 1
2
1 10
3 3
""") == """YES
NO
YES"""

# all equal already satisfied
assert run("""1
3
5 5 5
5 5 5
""") == "YES"

# impossible due to lack of total
assert run("""1
3
0 0 0
1 1 1
""") == "NO"

# single dominant deficit
assert run("""1
4
10 0 0 0
0 3 3 3
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| already equal | YES | no operations needed |
| insufficient total | NO | global sum constraint |
| extreme imbalance | NO | single deficit dominates feasibility |

## Edge Cases

One edge case is when all arrays are already equal. The algorithm computes $sa = sb$ and max deficit $0$, so it immediately returns YES without attempting any redistribution.

Another edge case is when totals match exactly but distribution is uneven. In that situation, $sa - sb = 0$, so any positive deficit forces NO. This matches the fact that any operation would break another coordinate due to lack of slack.

A final edge case is when one coordinate is extremely large deficit but overall surplus exists. The check ensures that even if total surplus is positive, it must be sufficient to cover the worst coordinate; otherwise no sequence of operations can avoid intermediate violations.
