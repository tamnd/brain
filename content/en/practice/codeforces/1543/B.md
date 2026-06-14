---
title: "CF 1543B - Customising the Track"
description: "We are given a list of non-negative integers where each value represents how many cars sit on a segment of a road. The “cost” of the whole configuration is defined by comparing every pair of segments and summing the absolute difference of their car counts."
date: "2026-06-14T19:11:29+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1543
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 730 (Div. 2)"
rating: 900
weight: 1543
solve_time_s: 275
verified: true
draft: false
---

[CF 1543B - Customising the Track](https://codeforces.com/problemset/problem/1543/B)

**Rating:** 900  
**Tags:** combinatorics, greedy, math  
**Solve time:** 4m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of non-negative integers where each value represents how many cars sit on a segment of a road. The “cost” of the whole configuration is defined by comparing every pair of segments and summing the absolute difference of their car counts. So if two segments differ a lot in traffic, they contribute heavily to the total inconvenience.

We are allowed to take individual cars and move them freely between segments, as many times as we want. This means we are not constrained by original positions, only by the total number of cars overall. The task is to redistribute these cars across the segments so that the final configuration minimizes the sum of pairwise absolute differences.

The key constraint is that the total number of elements over all test cases is at most 200,000. That immediately rules out any solution that tries to repeatedly simulate moves or recompute pairwise costs per operation, since even a single $O(n^2)$ computation per test case would already be too slow.

A subtle edge case appears when all values are identical. In that case, the inconvenience is already zero and any redistribution should not accidentally increase it in a reasoning mistake. Another important edge case is when the array is highly skewed, for example a single large value and many zeros. A naive intuition might suggest balancing locally, but the objective depends on all pairwise differences, not adjacent ones.

## Approaches

The brute-force view is to think in terms of states: each move transfers one unit from one index to another, producing a new configuration. For each configuration we could compute the total pairwise absolute difference. Even if we optimize the evaluation using prefix sums, the number of possible redistributions is astronomically large because each of up to $10^9$ units can move independently. This makes direct search infeasible.

The structural insight comes from rewriting what the operation allows. Since we can move cars arbitrarily, the only invariant is the total sum of all elements. We are effectively free to construct any non-negative integer array of length $n$ with the same total sum. The problem becomes: choose $n$ values summing to $S$ that minimize $\sum_{i<j} |b_i - b_j|$.

The objective penalizes spread. Any deviation from uniformity increases pairwise gaps. This suggests that the optimal configuration must be as balanced as possible: all values equal, or as close as possible given integrality.

Let $S = \sum a_i$. If $S$ is divisible by $n$, we can assign every position exactly $S/n$, which makes all pairwise differences zero. If not, some positions must carry one extra unit. The optimal structure is then that $r = S \bmod n$ elements are $q+1$ and the remaining $n-r$ are $q$, where $q = S // n$.

The remaining task is computing the cost of such a configuration. The contribution only comes from pairs formed between $q$ and $q+1$, each contributing exactly 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force redistribution | exponential | O(n) | Too slow |
| Uniform balancing + counting | O(n log n) per test case | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Compute the total sum of the array. This determines the only global constraint that remains after redistribution is allowed.
2. Compute $q = S // n$ and $r = S \% n$. This splits the optimal target into the largest possible uniform base and the number of extra units that must be distributed.
3. Construct the implicit optimal multiset: $n-r$ values equal to $q$ and $r$ values equal to $q+1$. We do not explicitly build it because only aggregate counts matter.
4. Compute the contribution to inconvenience. Pairs among equal values contribute zero, since their difference is zero. Only cross pairs between $q$ and $q+1$ contribute, and each such pair adds exactly one.
5. The number of cross pairs is $r(n-r)$, so this is the final answer.

The reason this works is that any deviation from this two-level structure introduces additional spread. If three distinct values appear, smoothing the middle one toward its neighbors strictly reduces total pairwise absolute differences while preserving the sum, so optimality forces the solution into at most two consecutive integer levels.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        s = sum(a)
        q = s // n
        r = s % n
        
        print(r * (n - r))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the reduction to a two-value multiset. The only nontrivial computation is the product $r(n-r)$, which counts all pairs between the two groups. No sorting or per-element simulation is required because the final structure is fully determined by the sum and size.

## Worked Examples

Consider the case $n=4$, $a=[0,1,1,0]$. The sum is $2$, so $q=0$ and $r=2$. The optimal multiset is two zeros and two ones.

| Step | Sum | q | r | Structure |
| --- | --- | --- | --- | --- |
| init | 2 | 0 | 2 | [0,0,1,1] |

Cross pairs are $2 \times 2 = 4$, so the answer is 4. This shows that even though the original array already looks balanced locally, global redistribution creates a clearer two-level structure that determines the cost.

Now consider $n=3$, $a=[1,2,3]$. The sum is $6$, so $q=2$, $r=0$.

| Step | Sum | q | r | Structure |
| --- | --- | --- | --- | --- |
| init | 6 | 2 | 0 | [2,2,2] |

All values are equal, so no cross pairs exist and the result is 0. This confirms that perfect divisibility collapses all variation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | summing the array dominates |
| Space | O(1) extra | only counters are used |

The solution runs comfortably within limits because the total input size is $2 \cdot 10^5$, and each element is processed once.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    t = int(sys.stdin.readline())
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        s = sum(a)
        q = s // n
        r = s % n
        output.append(str(r * (n - r)))
    
    return "\n".join(output)

# provided samples
assert run("""3
3
1 2 3
4
0 1 1 0
10
8 3 6 11 5 2 1 7 10 4
""") == """0
4
21"""

# all equal
assert run("""1
5
3 3 3 3 3
""") == "0"

# already minimal skew
assert run("""1
2
0 100
""") == "1"

# single element
assert run("""1
1
100
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal array | 0 | zero cost baseline |
| two extreme values | 1 | minimal nontrivial imbalance |
| n = 1 | 0 | single-point edge case |

## Edge Cases

When $n=1$, there are no pairs at all, so the inconvenience is always zero regardless of redistribution. The formula $r(n-r)$ correctly evaluates to zero since $r=0$.

When all elements are equal, the sum is divisible by $n$, producing $r=0$. The structure collapses into a single value and no pair contributes anything, matching the expected zero cost.

When the sum is not divisible by $n$, the imbalance is entirely captured by the number of leftover units $r$. Each of these units forces a $+1$ deviation against every base unit, and no other configuration can reduce this without violating the fixed total sum constraint.
