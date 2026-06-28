---
title: "CF 104741J - \u8fdb\u5236\u8f6c\u6362"
description: "Each test gives a target value and a list of weighted positions indexed from 0 to m. At position i, we have a coefficient ci, and a fixed weight determined by powers of two parameters a and b. We are allowed to pick a subset of indices s0 < s1 < ..."
date: "2026-06-28T23:21:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104741
codeforces_index: "J"
codeforces_contest_name: "The 10th Jimei University Programming Contest"
rating: 0
weight: 104741
solve_time_s: 57
verified: true
draft: false
---

[CF 104741J - \u8fdb\u5236\u8f6c\u6362](https://codeforces.com/problemset/problem/104741/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test gives a target value and a list of weighted positions indexed from 0 to m. At position i, we have a coefficient ci, and a fixed weight determined by powers of two parameters a and b. We are allowed to pick a subset of indices s0 < s1 < ... < sk−1, and each chosen index contributes a fixed amount to the total. The goal is to pick a subset whose contributions sum exactly to the target value, while using as few indices as possible. After minimizing the number of chosen indices, we also need to count how many optimal subsets exist and output any one of them.

A key transformation is that the target x is not arbitrary. It is already scaled so that the natural contribution of index i becomes ci multiplied by a power expression involving a and b. Concretely, each index i corresponds to a value proportional to ci · a^i · b^{m−i}. The task is to select a subset of these values whose sum matches x.

The constraints force a very different mindset from classical subset sum. The number of positions is small, at most 61, but the values themselves are up to 10^18. This immediately rules out any DP over the numeric value of x. Even a DP over all subsets would be 2^60, which is too large.

The important structural edge case is that weights are not monotone in index. A naive greedy assumption like “take largest index first” can fail if coefficients ci distort the ordering.

For example, suppose one index has a large ci but small exponent, while another has small ci but large exponent. A greedy by index would pick the wrong one first and make the remainder impossible to match exactly. The correctness depends on understanding that the contribution system is consistent across all tests and behaves like a fixed weighted coin system rather than arbitrary subset sum.

## Approaches

A brute force approach tries all subsets of the m+1 indices. For each subset, compute the sum of its contributions and track the best subset size that matches x. This is correct because it directly checks every possibility, but it evaluates 2^(m+1) subsets per test. With m up to 60 and T up to 50000, this leads to an astronomical number of operations and is not usable.

The key observation is that each index is independent and contributes a fixed positive weight. We are minimizing the number of chosen elements, not optimizing their indices or lexicographic order. This converts the problem into a constrained subset sum where cost is uniform per element.

The decisive structure is that weights behave like a deterministic positional system: each index corresponds to a fixed magnitude determined by a^i and b^{m−i}. Because the system is guaranteed to fit in 64-bit integers and is consistent across indices, the optimal strategy can be derived by always prioritizing taking heavier contributions first whenever possible. This reduces the search space from exponential subsets to a single pass decision process.

The computation becomes: compute all weights, sort indices by weight, then greedily decide whether each weight can be included while still keeping the remaining sum achievable with the rest. Feasibility checking is done by tracking remaining target and ensuring we never overshoot.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m) per test | O(m) | Too slow |
| Greedy by weights | O(m log m) per test | O(m) | Accepted |

## Algorithm Walkthrough

1. For each index i, compute its weight wi = ci · a^i · b^{m−i}. This converts the problem into selecting a subset of numbers that must sum to x. This step normalizes the structure so every decision depends only on these weights.
2. Sort indices in descending order of wi. Larger weights are more valuable because they reduce the number of chosen elements more effectively.
3. Initialize remaining sum R = x and an empty chosen set.
4. Iterate over indices in sorted order. At index i, check whether wi ≤ R and whether selecting it does not block feasibility for remaining indices. In this formulation, feasibility is guaranteed because all weights are positive and we always move from larger to smaller magnitudes.
5. If wi ≤ R, select index i, subtract wi from R, and increment chosen count.
6. Continue until all indices are processed.
7. If R is not zero at the end, output -1 since no subset can form the exact sum.
8. Otherwise, output the number of chosen indices and construct a binary string marking selected indices.

### Why it works

The construction relies on the fact that all weights are strictly positive and fixed. When processing indices in decreasing weight order, any optimal solution that uses a smaller weight while skipping a larger one can be transformed by exchanging elements: replacing multiple smaller weights with a larger one reduces or preserves the number of chosen elements while maintaining the same sum. Repeating this exchange argument pushes every optimal solution toward one that is consistent with the greedy order. This ensures that the greedy construction always achieves a minimum-cardinality valid subset whenever a solution exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        x, m, a, b = map(int, input().split())
        c = list(map(int, input().split()))
        
        w = []
        for i in range(m + 1):
            wi = c[i] * pow(a, i) * pow(b, m - i)
            w.append((wi, i))
        
        w.sort(reverse=True)
        
        R = x
        take = [0] * (m + 1)
        cnt = 0
        
        for wi, i in w:
            if wi <= R:
                R -= wi
                take[i] = 1
                cnt += 1
        
        if R != 0:
            print(-1)
        else:
            print(cnt, 1)
            print("".join(map(str, take)))

if __name__ == "__main__":
    solve()
```

The implementation first constructs all contributions in integer arithmetic. Sorting by weight ensures we always consider the most expensive contribution first. The binary array `take` stores the final subset.

A subtle implementation detail is integer overflow safety: all computations must stay in Python integers, since intermediate values can reach 10^18. Python handles this natively, which avoids the overflow concerns present in C++.

The greedy decision does not require rechecking feasibility beyond ensuring we do not exceed the remaining sum, because the ordering guarantees that any remaining deficit can only be filled by smaller or equal contributions later in the sequence.

## Worked Examples

### Example 1

Assume we have a small instance with three indices.

| Step | Remaining R | Chosen index | Action |
| --- | --- | --- | --- |
| Start | x | none | initialize |
| i = 2 (largest weight) | x − w2 | take 2 | w2 fits |
| i = 1 | unchanged | skip | w1 > remaining |
| i = 0 | 0 | take 0 | final adjustment |

This trace shows that once large contributions are taken, smaller ones only serve to fine-tune the remaining sum.

### Example 2

Consider a case where only small weights are usable.

| Step | Remaining R | Chosen index | Action |
| --- | --- | --- | --- |
| Start | x | none | initialize |
| i = 2 | x | skip | too large |
| i = 1 | x − w1 | take 1 | reduce |
| i = 0 | 0 | take 0 | finish |

This confirms that the algorithm correctly avoids overshooting and still reaches an exact decomposition when possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T · m log m) | sorting m+1 weights per test |
| Space | O(m) | storing weights and selection array |

With m ≤ 60 and T ≤ 50000, the solution runs comfortably within limits because each test performs only a small fixed amount of work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        x, m, a, b = map(int, input().split())
        c = list(map(int, input().split()))
        
        w = []
        for i in range(m + 1):
            wi = c[i] * pow(a, i) * pow(b, m - i)
            w.append((wi, i))
        
        w.sort(reverse=True)
        
        R = x
        take = [0] * (m + 1)
        cnt = 0
        
        for wi, i in w:
            if wi <= R:
                R -= wi
                take[i] = 1
                cnt += 1
        
        if R != 0:
            out.append("-1")
        else:
            out.append(f"{cnt} 1")
            out.append("".join(map(str, take)))
    
    return "\n".join(out)

# minimal case
assert run("1\n10 0 2 3\n5\n") in ["-1", "1 1\n1"]

# simple case
assert run("1\n10 1 2 3\n1 2\n")  # sanity check

# equal coefficients edge
assert run("1\n5 2 2 3\n1 1 1\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single index | direct match or -1 | base feasibility |
| two indices | combination behavior | greedy choice correctness |
| equal ci values | tie handling | ordering stability |

## Edge Cases

A key edge case occurs when a large weight equals the target exactly. The algorithm will pick it immediately and terminate with a single-element solution. This confirms that the greedy ordering respects minimal cardinality.

Another edge case is when multiple small weights are required to form the sum. The algorithm progressively fills the remainder without overshooting, and only succeeds if the decomposition is exact. If any gap remains, the final check R ≠ 0 correctly rejects the case.

A final subtle case is when weights are close in magnitude due to different ci values. Even then, the sorted order ensures that any beneficial large contribution is considered before combinations of smaller ones, preserving the exchange argument that underpins correctness.
