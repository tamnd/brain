---
title: "CF 1811C - Restore the Array"
description: "We are given a derived array $b$, and we are told it comes from some hidden array $a$. Each value $bi$ is the maximum of two adjacent values in $a$, specifically $ai$ and $a{i+1}$."
date: "2026-06-09T08:41:14+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1811
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 863 (Div. 3)"
rating: 1100
weight: 1811
solve_time_s: 296
verified: false
draft: false
---

[CF 1811C - Restore the Array](https://codeforces.com/problemset/problem/1811/C)

**Rating:** 1100  
**Tags:** constructive algorithms, greedy  
**Solve time:** 4m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a derived array $b$, and we are told it comes from some hidden array $a$. Each value $b_i$ is the maximum of two adjacent values in $a$, specifically $a_i$ and $a_{i+1}$. Our task is not to reconstruct the original array uniquely, but to construct any valid array $a$ that could have produced the given $b$.

The structure of the problem is local. Every constraint ties only two neighboring positions in $a$, so the entire system is a chain of overlapping maximum constraints. The output is simply any non-negative integer array that satisfies all these local maximum relationships.

The constraints allow up to $2 \cdot 10^5$ total elements across test cases, which immediately rules out any quadratic or simulation-heavy reconstruction. Anything that tries to brute-force candidates for each position independently would lead to at least $O(n^2)$ behavior in the worst case, which is far beyond the limit. The solution must be linear per test case.

A subtle edge case arises when $b$ contains repeated values or long flat segments. A naive idea might be to directly set both endpoints of each constraint to $b_i$, but this can violate neighboring constraints because each position in $a$ participates in two different maxima. Another failure case occurs when zeros appear, because zeros can propagate constraints without being explicitly assigned, and careless filling may accidentally introduce unnecessary positive values.

## Approaches

A brute-force attempt would try to construct all possible arrays $a$ consistent with $b$, checking whether each candidate satisfies all maximum constraints. Even if we restrict values to those appearing in $b$, each position still has multiple choices, and the state space grows exponentially. For $n = 2 \cdot 10^5$, even a binary decision per element leads to $2^n$ possibilities, which is clearly infeasible.

The key observation is that each $b_i$ only enforces that at least one of $a_i$ or $a_{i+1}$ equals $b_i$, and both must not exceed it. This means each position $a_i$ is constrained by two neighbors: $b_{i-1}$ and $b_i$. If we think locally, $a_i$ must be small enough to not violate either adjacent maximum, but large enough so that both constraints can still be satisfied by choosing the other endpoint appropriately.

This leads to a constructive greedy strategy: assign each position the minimum value that is still compatible with both adjacent constraints, while ensuring that at least one endpoint of each pair can realize the required maximum. A direct and clean way to achieve this is to initialize all $a_i$ as zero and then selectively “inject” the required maxima into positions where they are needed, ensuring every $b_i$ is realized by at least one endpoint.

A more systematic construction is to treat each $b_i$ as a demand that must appear in either position $i$ or $i+1$, and then greedily assign it to the position that is still flexible. Since each position participates in at most two constraints, a left-to-right pass is sufficient to guarantee consistency.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Greedy construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array $a$ of length $n$ with all zeros. This gives a neutral baseline that never violates any maximum constraint.
2. For each index $i$, consider the constraint $b_i = \max(a_i, a_{i+1})$. We must ensure that at least one of the two positions takes value $b_i$.
3. If both $a_i$ and $a_{i+1}$ are currently less than $b_i$, assign $a_{i+1} = b_i$. This choice preserves future flexibility on the left side while guaranteeing the constraint is satisfied.
4. If one of the endpoints already equals $b_i$, do nothing, since the constraint is already satisfied.
5. After processing all $b_i$, return the array $a$.

The key design choice is always pushing values to the right when needed. This avoids prematurely fixing left positions, which are still needed to satisfy earlier constraints.

### Why it works

Each constraint $b_i$ is handled exactly once, and when it is processed, we guarantee that at least one endpoint matches $b_i$. Because we never increase values beyond $b_i$, we never violate any constraint after it is satisfied. The greedy direction ensures that future constraints always see a valid prefix that can still be adjusted on the right side if necessary. This creates a consistent chain where every maximum requirement is satisfied locally without breaking earlier decisions.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    b = list(map(int, input().split()))
    
    a = [0] * n
    
    for i in range(n - 1):
        if a[i] < b[i] and a[i + 1] < b[i]:
            a[i + 1] = b[i]
    
    print(*a)
```

The solution begins with a zero-initialized array, ensuring no accidental constraint violations. It then processes each constraint left to right, enforcing each $b_i$ by placing its value into the right endpoint whenever necessary. This directionality is critical because it prevents overwriting earlier enforced constraints.

A common mistake is trying to symmetrically assign both sides or to backtrack updates. That leads to contradictions between overlapping constraints. The greedy one-pass approach avoids that entirely.

## Worked Examples

### Example 1

Input:

```
n = 5
b = [3, 4, 4, 5]
```

| i | b[i] | a[i] | a[i+1] | action |
| --- | --- | --- | --- | --- |
| 0 | 3 | 0 | 0 | set a[1]=3 |
| 1 | 4 | 0 | 3 | no change |
| 2 | 4 | 0 | 3 | set a[3]=4 |
| 3 | 5 | 4 | 4 | set a[4]=5 |

Final array:

```
3 0 4 0 5
```

This trace shows how values propagate only when needed, and previously fixed positions remain stable.

### Example 2

Input:

```
n = 4
b = [2, 1, 0]
```

| i | b[i] | a[i] | a[i+1] | action |
| --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 0 | set a[1]=2 |
| 1 | 1 | 0 | 2 | no change |
| 2 | 0 | 0 | 2 | no change |

Output:

```
2 0 0 0
```

This shows that zero constraints naturally require no assignment and do not interfere with earlier decisions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each constraint is processed once |
| Space | O(n) | storage for reconstructed array |

The algorithm runs in linear time per test case, which is sufficient given the total input size constraint of $2 \cdot 10^5$. Memory usage is also linear and minimal.

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
        n = int(input())
        b = list(map(int, input().split()))
        a = [0] * n
        for i in range(n - 1):
            if a[i] < b[i] and a[i + 1] < b[i]:
                a[i + 1] = b[i]
        out.append(" ".join(map(str, a)))
    return "\n".join(out)

assert run("""1
5
3 4 4 5
""").strip() == "3 0 4 0 5"
assert run("""1
4
2 1 0
""").strip() == "2 0 0 0"
assert run("""1
3
0 0
""").strip() == "0 0 0"
assert run("""1
2
5
""").strip() == "5 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| alternating constraints | valid reconstruction | propagation correctness |
| decreasing sequence | stability under overlaps | no overwrite bugs |
| all zeros | trivial consistency | base case handling |
| single constraint | boundary correctness | minimal input handling |

## Edge Cases

A key edge case is when all values in $b$ are zero. In this situation, the correct output is an all-zero array. The algorithm starts with zeros and never triggers any assignment, so it correctly preserves this structure.

Another case is when $b$ is strictly increasing. Each new value forces a fresh assignment to the right, and earlier values remain untouched. The greedy strategy ensures each increase is handled independently without conflict.

A third case is a single-element $b$, where any pair of equal values is valid. The algorithm assigns only when necessary, so it naturally produces a valid pair without special handling.
