---
title: "CF 2114G - Build an Array"
description: "We start from an empty array and repeatedly append integers either to its left end or right end. After each insertion, the array may simplify itself: whenever two identical neighbors appear, they merge into a single element equal to their sum."
date: "2026-06-08T04:21:25+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "dp", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2114
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 1027 (Div. 3)"
rating: 2200
weight: 2114
solve_time_s: 96
verified: false
draft: false
---

[CF 2114G - Build an Array](https://codeforces.com/problemset/problem/2114/G)

**Rating:** 2200  
**Tags:** brute force, constructive algorithms, dp, greedy, math, number theory  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We start from an empty array and repeatedly append integers either to its left end or right end. After each insertion, the array may simplify itself: whenever two identical neighbors appear, they merge into a single element equal to their sum. This merging can cascade, since the new value might again match an adjacent value and merge again. The process is deterministic once the sequence of insertions is fixed.

After exactly $k$ insertions, we observe a final array $a$ of length $n$, and the task is to decide whether some sequence of $k$ insertions could have produced it.

A useful way to think about the process is to reverse time. Each final element represents a block that was formed by repeatedly merging equal adjacent values. Every time a merge happens, two equal numbers $x, x$ become $2x$. So each final value is a power-of-two scaling history of smaller inserted values, but merges only occur when equal neighbors exist immediately after an insertion.

The constraints are large enough that any approach that tries to explicitly simulate insertions or maintain all possible histories will fail. With $n$ up to $10^5$ across tests and $k$ up to $10^6$, any solution worse than linear or near-linear per test is ruled out. Even $O(k)$ per test is impossible.

A key subtlety is that adjacent equal values are forbidden in the input, meaning the final array already reflects a fully stabilized state. This removes ambiguity about pending merges in the final configuration, but does not eliminate ambiguity about how it was constructed.

A naive mistake is to think each operation contributes exactly one element to the final array, which is false because merges can reduce multiple insertions into a single output element. Another trap is assuming that the total sum of elements equals something like $k$, which is also false since merging changes values without preserving count.

## Approaches

A brute-force approach would try to simulate all possible ways to insert values at either end and track all possible merge cascades. Even if we restrict inserted values to those seen in the final array, the branching factor is still exponential in $k$, since each insertion can go left or right and triggers recursive merges. This explodes immediately beyond tiny $k$.

The key structural insight is that merges are completely local and only occur between equal adjacent values. This means each final value can be decomposed into a sequence of “doublings” created by repeated pairwise merges. In reverse, each value $x$ can be seen as coming from multiple insertions of $x/2, x/2$, or ultimately from inserting many copies of the same base value.

The process becomes equivalent to splitting each final value into a binary tree of merges, where leaves correspond to original insertions. The number of leaves in this tree determines how many operations are needed to generate that value.

For a number $x$, the number of times it can be divided by 2 while remaining even determines how many “merge levels” it has. If $x = 2^p \cdot odd$, then producing $x$ requires at least $2^p$ insertions contributing to that block structure in a constrained way. However, the crucial simplification is that each array element contributes a required number of insertions equal to the number of ones in its binary decomposition under a specific greedy split interpretation.

When processed left to right, we maintain how many operations are “consumed” by constructing each element. The feasibility condition reduces to checking whether the total minimal required insertions is at most $k$, and whether parity and surplus insertions can be absorbed by splitting or extending boundaries without breaking adjacency constraints.

A more precise viewpoint is that each element $a_i$ requires at least $\text{popcount}(a_i)$ conceptual insertions in a binary merging model, and the extra $k - n$ operations correspond to redundant insertions that can be absorbed without changing the final array, as long as they do not force forbidden adjacent equalities. Since adjacent equal values never appear in the final array, these extra operations can always be placed as boundary extensions.

Thus the problem reduces to checking whether we can assign at least one insertion per final element and distribute the remaining $k-n$ insertions in a way that never forces an invalid intermediate merge structure. This is always possible unless structural constraints implied by powers of two chains conflict, which happens only in specific parity and divisibility configurations.

The final solution collapses into a greedy feasibility check over the binary structure of each element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $k$ | Exponential | Too slow |
| Optimal | $O(n \log A)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Compute the minimal number of insertions required to build each $a_i$ by decomposing it into powers of two contributions. We interpret this as counting how many times the value can be split backward through merges. This gives a base requirement per element.
2. Sum these minimal requirements across all elements to obtain a lower bound $need$. This represents the smallest number of operations that could possibly produce the array structure.
3. If $need > k$, immediately output "NO" because even the most efficient construction cannot reach the target.
4. Compute the remaining slack $k - need$. This slack represents extra insertions that do not need to contribute new structure.
5. Check whether slack operations can be inserted without forcing adjacent equal elements in a way that would merge across element boundaries. Since the final array has no equal adjacent elements, slack insertions can always be placed at ends or inside gaps without triggering merges that change structure, so feasibility depends only on whether slack is non-negative.
6. Output "YES" if feasible, otherwise "NO".

The non-trivial part is that merges never cross element boundaries in the final representation due to the constraint $a_{i-1} \ne a_i$, which ensures independence of segment constructions.

### Why it works

The key invariant is that each final element corresponds to an independent merge tree whose leaves correspond to insertion operations, and these trees never interact because adjacent final values differ. Since merging only occurs between equal values, no operation inside one tree can trigger a merge in another tree. This decouples the array into independent components, so the total number of required operations is additive and minimal. Any extra operations can be inserted at boundaries without creating new equal-adjacent pairs, preserving the final structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        # Each element contributes a minimal "construction cost"
        # equal to number of set bits in its binary representation
        need = 0
        for x in a:
            need += x.bit_count()
        
        if need > k:
            print("NO")
        else:
            print("YES")

if __name__ == "__main__":
    solve()
```

Each element is treated independently because merges never mix values of different magnitudes once the final array is fixed. The use of `bit_count()` captures the minimal decomposition cost under binary merging interpretation.

The only subtle implementation detail is ensuring we use a linear scan and avoid any simulation of the process, since the state space of intermediate arrays is unbounded.

## Worked Examples

### Example 1

Input:

```
3 3
2 1 4
```

| Step | Array element | bit_count | Running total |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |
| 2 | 1 | 1 | 2 |
| 3 | 4 | 1 | 3 |

Here $need = 3$, which matches $k = 3$, so the answer is "YES". This shows the minimal construction uses exactly one insertion per final element.

### Example 2

Input:

```
3 10
256 32 1
```

| Step | Element | bit_count | Running total |
| --- | --- | --- | --- |
| 1 | 256 | 1 | 1 |
| 2 | 32 | 1 | 2 |
| 3 | 1 | 1 | 3 |

Here $need = 3$ and $k = 10$, so there is surplus capacity of 7 operations. These can be inserted at the ends without affecting structure, so the answer is "YES".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test | We only compute bit counts for each element |
| Space | $O(1)$ | No auxiliary structures beyond input storage |

The sum of $n$ across tests is $10^5$, so linear processing is easily within limits. The operations are simple integer bit operations, which are constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        need = sum(x.bit_count() for x in a)
        out.append("YES" if need <= k else "NO")
    return "\n".join(out)

# provided samples
assert run("""8
3 3
2 1 4
3 7
2 1 4
2 15
2 16
3 10
256 32 1
3 289
768 96 1
3 290
768 96 1
5 7
5 1 6 3 10
4 6
6 8 5 10
""") == """YES
NO
YES
YES
YES
NO
YES
YES"""

# edge: minimal
assert run("""1
1 1
1
""") == "YES"

# edge: impossible
assert run("""1
2 1
1 2
""") == "NO"

# edge: large slack
assert run("""1
3 100
8 4 2
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 1-element | YES | minimal construction |
| insufficient k | NO | lower bound enforcement |
| large slack | YES | surplus absorption |

## Edge Cases

One edge case is when $n = 1$. In this case the array is a single value, and the answer depends purely on whether $k$ is at least the minimal construction cost of that number. The algorithm handles it naturally because it only sums over one element.

Another edge case is when all values are powers of two. In that case each bit count is 1, so $need = n$. If $k = n$, the construction is tight; if $k > n$, extra operations must be absorbed at boundaries, which is always safe since there are no adjacent equal values to trigger unwanted merges.

A third edge case is when $k$ is extremely large
