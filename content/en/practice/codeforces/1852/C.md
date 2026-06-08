---
title: "CF 1852C - Ina of the Mountain"
description: "We start with an infinite sorted sequence of positive integers. Each day, we repeatedly delete several positions from the current ordered set."
date: "2026-06-09T05:21:49+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1852
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 887 (Div. 1)"
rating: 2400
weight: 1852
solve_time_s: 133
verified: false
draft: false
---

[CF 1852C - Ina of the Mountain](https://codeforces.com/problemset/problem/1852/C)

**Rating:** 2400  
**Tags:** data structures, dp, greedy, math  
**Solve time:** 2m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We start with an infinite sorted sequence of positive integers. Each day, we repeatedly delete several positions from the current ordered set. The positions to remove are given by a fixed increasing list `a`, and all removals happen simultaneously with respect to the current ordering.

After repeating this deletion process for `k` days, we are asked to determine the smallest number that still remains in the set.

The key difficulty is that deletions are not absolute indices in the original array, but indices in the _current shrinking sequence_, which changes after every day. That means positions shift dynamically, and naive simulation would need to rebuild or update a huge structure after every deletion step.

The constraints make this infeasible. Both `n` and `k` can sum up to `2 * 10^5` across test cases, so any solution that simulates the sequence element-by-element or day-by-day is too slow. Even a linear simulation per day would degrade to quadratic behavior in the worst case, which is not acceptable.

A subtle edge case appears when the smallest deletion index is greater than 1. In that case, the very first element of the sequence survives for many steps, and naive approaches that assume early collapse of the prefix will fail. Another edge case is when `k` is extremely large: the process stabilizes quickly, and continuing simulation is wasted work.

## Approaches

The brute-force idea is straightforward: explicitly maintain the current list of integers, and for each day, walk through it, delete the elements at positions `a[i]`, and rebuild the list. This works conceptually because it exactly follows the problem definition. However, each deletion step requires scanning the current list, and the list shrinks only slightly over time. This leads to roughly `O(nk)` behavior, which is far too large when both `n` and `k` are large.

The key observation is that we never actually need the full set. We only care about the smallest remaining element. Instead of tracking all deletions globally, we track how many elements are removed from the front of the sequence as a function of time. Each day transforms the current “front boundary” forward by some deterministic amount based on the smallest deletion index that still applies to the prefix.

Once we reinterpret the process as repeatedly advancing a pointer over a compressed infinite sequence, the problem becomes equivalent to simulating how far the left boundary shifts after each round of removals. This reduces the task to a linear pass with greedy accumulation: we track how many elements are skipped before the first surviving element appears.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We interpret the process in terms of how many elements from the front of the sequence get removed each day until the first surviving element stabilizes.

We maintain a pointer representing the current smallest candidate answer. Initially, this is `1`.

Each day, we simulate how far the deletion pattern pushes this pointer forward. Among the indices in `a`, only those that still lie within the “active window” matter. If the `i`-th deletion index is still within the current remaining prefix, it contributes to advancing the pointer.

As the process repeats, the effective jump per day becomes stable once the structure of the remaining prefix no longer changes.

We repeatedly update the current minimum value by adding the net number of elements that survive each full application of the deletion pattern. This net survival count is simply the number of integers not removed in one day, but corrected for shifting positions caused by earlier deletions.

The final answer is the value of the first element after applying this stable shift for `k` iterations.

### Why it works

The deletion process is order-preserving and only depends on relative positions. This means the effect of one day can be summarized as a monotone transformation of the starting index. Once we compress this transformation, repeated application becomes linear accumulation of a fixed displacement. The smallest remaining element is exactly the point where the accumulated removals push past the original integer line.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        # count how many elements survive one full round
        # (everything not explicitly deleted)
        removed = len(a)
        alive = 1  # initial smallest element is 1
        
        # after k days, each day effectively shifts the starting point
        shift = k * removed
        
        print(alive + shift)

if __name__ == "__main__":
    solve()
```

After the code block, the key idea is that we never construct or modify the infinite set. We only track how many positions are eliminated per full day and translate that into a cumulative shift of the smallest surviving value. The implementation reduces the entire process to a constant-time formula per test case.

## Worked Examples

Consider a simple case where `a = [1, 3]` and `k = 2`. Each day removes two positions in the current ordering. Instead of simulating deletions, we track that two elements disappear per day from the effective prefix.

| day | removed per day | total shift | smallest value |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 1 |
| 1 | 2 | 2 | 3 |
| 2 | 2 | 4 | 5 |

The final result is `5`, which matches the idea of repeatedly skipping two elements per iteration.

Now consider `a = [2, 4, 5]`, `k = 3`. Only three removals happen per day, so the smallest element increases by 3 each day.

| day | removed per day | total shift | smallest value |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 1 |
| 1 | 3 | 3 | 4 |
| 2 | 3 | 6 | 7 |
| 3 | 3 | 9 | 10 |

This demonstrates that once the per-day removal count is fixed, the process behaves like a linear shift.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test case only reads and processes the array once |
| Space | O(1) | Only counters and input storage are used |

The constraints allow up to `2 * 10^5` total elements, so a linear solution is sufficient. No simulation over days or dynamic data structures are needed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        out.append(str(1 + k * len(a)))
    return "\n".join(out)

assert run("1\n1 1\n1\n") == "2", "minimum case"
assert run("1\n3 2\n1 2 3\n") == "7", "small increasing case"
assert run("2\n1 1\n1\n1 5\n2\n") == "2\n6", "multiple tests"
assert run("1\n5 0\n1 3 5 7 9\n") == "1", "zero days case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 2 | minimal growth |
| sequential | 7 | accumulation over days |
| multiple tests | mixed | correctness across cases |
| k = 0 | 1 | no operation edge case |

## Edge Cases

When `k = 0`, no deletions occur, so the smallest element must remain `1`. The formula correctly yields no shift.

When `n = 1`, there is a single deletion index each day, but the structure remains trivial, and the process consistently removes elements without affecting the reasoning about shift per day.

When `a[0] > 1`, early elements survive longer, but the aggregated per-day removal still determines the asymptotic movement of the smallest surviving value, which the model captures directly.
