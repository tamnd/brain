---
title: "CF 105986K - Capoo's stack"
description: "We are given multiple independent test cases. In each test case there are several Capoo, each with a positive strength value. We want to choose some of them and arrange them into a vertical stack. The stack has a constraint that only the top Capoo is unrestricted."
date: "2026-06-22T16:35:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105986
codeforces_index: "K"
codeforces_contest_name: "2025 Wuhan University of Technology Programming Contest"
rating: 0
weight: 105986
solve_time_s: 60
verified: true
draft: false
---

[CF 105986K - Capoo's stack](https://codeforces.com/problemset/problem/105986/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple independent test cases. In each test case there are several Capoo, each with a positive strength value. We want to choose some of them and arrange them into a vertical stack.

The stack has a constraint that only the top Capoo is unrestricted. Every other Capoo must have strength at least as large as the sum of the strengths of all Capoo placed above it. In other words, as we go downward in the stack, each Capoo must be strong enough to “support” everything above it combined.

The goal is not to maximize total strength or minimize violations, but to maximize how many Capoo can be included while still being able to order them into a valid stack.

From a constraints perspective, the total number of Capoo across all test cases is at most 200000, and each strength can be as large as 10^9. This immediately rules out any approach that tries all permutations or subsets. Even checking a single arrangement naively requires linear verification, and there are factorially many orderings, so brute force is completely out of reach.

The key difficulty is that both selection and ordering are coupled. Choosing a weak element early may make the prefix sum too large too quickly, preventing later additions. On the other hand, placing strong elements too early may waste their capacity and reduce how many items fit overall.

A subtle edge case appears when many values are equal or very small. For example, if all Capoo have strength 1, then stacking two is fine, but stacking three already fails because the third must be at least 2. So a naive “take everything” or “sort arbitrarily” approach breaks immediately. Another tricky case is when one very large value exists among many small ones. For instance, values like [1, 1, 1, 100]. If placed incorrectly, the large value might be consumed too early, making it impossible to fit more small elements afterward even though a better ordering exists.

## Approaches

A brute-force idea is to try every subset of Capoo, and for each subset try all permutations to see whether a valid stack exists. For a given ordering, we can verify validity in linear time by maintaining the running sum of elements above each position. This already costs O(k) per permutation, and across all permutations this becomes O(k!), which is infeasible even for n around 15, let alone 200000.

We need a structural observation about how the constraint behaves. The condition only depends on the sum of all previously placed elements, not their individual arrangement. This suggests that once we fix an ordering, the only state that matters during construction is the current prefix sum.

This leads to a greedy insight: if we are building a valid stack from top to bottom, at every step we want to keep the prefix sum as small as possible so that more elements remain eligible to be placed later. This naturally suggests sorting and always trying the smallest available valid element first.

The key realization is that if we maintain a current sum S of everything already placed, then the next chosen element must satisfy ai ≥ S. Among all such valid candidates, choosing the smallest one keeps S as small as possible after the update, because S becomes S + ai. This is exactly the structure of a greedy feasibility process.

So we sort all values in increasing order and iterate through them, greedily taking an element whenever it can support the current sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Greedy after sorting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Sort all Capoo strengths in increasing order.

Sorting ensures that when we consider an element, all smaller or equal elements have already been considered, which is important because smaller elements are always easier to place early without violating the sum constraint.
2. Initialize a variable S = 0 to represent the sum of strengths already placed in the stack.

This value models the total load that the next chosen Capoo must be able to support.
3. Initialize a counter ans = 0 to track how many Capoo we successfully include.
4. Iterate through the sorted strengths from smallest to largest. For each value x:

If x is at least S, we include it in the stack, increment ans by 1, and update S = S + x.

If x is smaller than S, we skip it because placing it would violate the requirement immediately. There is no benefit in trying to force it later, since S only increases over time.
5. After processing all elements, output ans as the maximum number of Capoo that can be stacked.

### Why it works

At any point, the only way to extend a valid stack is to choose an element that can support the current accumulated load S. If we pick a larger element than necessary when a smaller valid one exists, we increase S more than needed, which can only reduce future feasibility because all remaining elements are fixed and non-negative.

This establishes a greedy dominance property: among all valid choices at a given step, the smallest valid element preserves the most future options. Since S is monotone increasing, skipping a valid smaller element can never help later, because it only makes the constraint stricter for every remaining element.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        a.sort()
        
        s = 0
        ans = 0
        
        for x in a:
            if x >= s:
                ans += 1
                s += x
        
        out.append(str(ans))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution is structured around a single greedy sweep. The sorting step ensures that we always encounter smaller candidates first, which is crucial for keeping the accumulated sum minimal whenever possible. The variable `s` tracks the cumulative strength requirement induced by the chosen prefix of the stack. Each decision is local: we either accept an element if it can currently support the stack, or skip it permanently.

A common mistake is to try building the stack in descending order. That approach tends to place large values early, which inflates the running sum and reduces the number of elements that can fit later. Another mistake is to try pairing elements or using two pointers without enforcing the global prefix-sum constraint, which leads to incorrect feasibility reasoning.

## Worked Examples

Consider the input:

```
1
3
4 7 9
```

After sorting, we get [4, 7, 9].

| Step | Current x | Current S | Action | New S | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 4 | 0 | take | 4 | 1 |
| 2 | 7 | 4 | take | 11 | 2 |
| 3 | 9 | 11 | skip | 11 | 2 |

This shows that even though 9 is large, it arrives too late because the accumulated sum becomes too large for it to satisfy the constraint.

Now consider:

```
1
3
1 1 1
```

Sorted array is [1, 1, 1].

| Step | Current x | Current S | Action | New S | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | take | 1 | 1 |
| 2 | 1 | 1 | take | 2 | 2 |
| 3 | 1 | 2 | skip | 2 | 2 |

Only two elements can be used because the third 1 cannot support the accumulated sum of 2.

These traces show how the constraint rapidly becomes stricter as S grows, which is the core limiting factor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | Sorting dominates, single linear scan afterward |
| Space | O(1) extra (excluding input) | Only a few variables used beyond storage of array |

The total complexity over all test cases is O(N log N), where N is the sum of all n values. With N up to 2 × 10^5, this easily fits within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        s = 0
        ans = 0
        for x in a:
            if x >= s:
                ans += 1
                s += x
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("1\n3\n4 7 9\n") == "2"
assert run("1\n3\n1 1 1\n") == "2"

# custom cases
assert run("1\n1\n5\n") == "1", "single element"
assert run("1\n5\n1 2 3 4 5\n") == "3", "mixed increasing"
assert run("1\n4\n10 1 1 1\n") == "3", "large + smalls"
assert run("1\n6\n1 1 1 1 1 10\n") == "3", "late large element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | minimum size correctness |
| 1 2 3 4 5 | 3 | greedy progression behavior |
| 10 1 1 1 | 3 | effect of large early constraint |
| many 1s + 10 | 3 | ordering sensitivity |

## Edge Cases

One important edge case is when all values are equal to 1. For input `[1, 1, 1, 1]`, the algorithm takes the first element, making S = 1. The second is still valid, giving S = 2. The third 1 is then rejected because it cannot support 2. This demonstrates that even uniform arrays do not allow full selection due to the rapidly increasing prefix sum.

Another edge case is a single large element surrounded by many small ones, such as `[100, 1, 1, 1, 1]`. The algorithm first takes 1, then 1, then 1, but eventually S grows and blocks further inclusion. The large element is typically taken late if at all, and this ordering ensures we do not waste early capacity on it.

A final edge case is a single element input. Since the top element has no constraint above it, any single Capoo is always valid, and the algorithm correctly returns 1 immediately.
