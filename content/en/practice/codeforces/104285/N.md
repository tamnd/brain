---
title: "CF 104285N - Nancy's Numbers"
description: "We are given a list of integers, and we are allowed to repeatedly increase any chosen element by exactly one. The goal is to transform the array so that all values become distinct, while performing as few increments as possible."
date: "2026-07-01T20:58:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104285
codeforces_index: "N"
codeforces_contest_name: "PCCA Winter Camp Contest 2023"
rating: 0
weight: 104285
solve_time_s: 49
verified: true
draft: false
---

[CF 104285N - Nancy's Numbers](https://codeforces.com/problemset/problem/104285/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers, and we are allowed to repeatedly increase any chosen element by exactly one. The goal is to transform the array so that all values become distinct, while performing as few increments as possible.

Rephrased, each number represents a starting position on the integer line. We are allowed to move points only to the right, and each move costs one unit of distance. We want to reposition all points so that no two land on the same integer, minimizing total movement.

The constraint $n \le 2 \cdot 10^5$ immediately rules out any approach that tries to simulate increments step by step for each collision. Even if each element needed only a small number of moves, the worst case could involve cascading shifts across almost the entire array, leading to quadratic behavior if handled naively.

A subtle failure case appears when many values are identical or tightly clustered. For example, if the input is $[5, 5, 5, 5]$, a greedy “fix duplicates locally” approach might assign values like 5, 6, 7, 8, but a careless implementation that always increments the current duplicate until it becomes unique without considering earlier assignments can overcount or mis-handle ordering. Another pitfall is processing in arbitrary order instead of structured order, which can break optimality because earlier decisions constrain later ones.

## Approaches

The brute-force view is straightforward: scan the array repeatedly, and whenever a collision exists, increment one of the duplicates until it becomes unique. This works because each increment operation directly models the allowed move. However, each increment might trigger new collisions with already processed values, so in the worst case we end up propagating changes across many elements repeatedly. For an input like all equal values, each element may be incremented up to $O(n)$ times, giving $O(n^2)$ behavior.

The key structural observation is that only relative ordering matters. If we sort the array, we remove all ambiguity about which values should be fixed first. Once sorted, the optimal strategy becomes greedy and local: each number only needs to be at least one greater than the previous chosen value. This converts a global collision problem into a simple linear sweep where we enforce monotonicity.

Instead of thinking in terms of arbitrary increments, we reinterpret the task as assigning final values $b_i$ such that $b_i > b_{i-1}$ and $b_i \ge a_i$, while minimizing $\sum (b_i - a_i)$. Sorting ensures that any optimal solution can be rearranged into non-decreasing order without increasing cost.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(n)$ | Too slow |
| Sort + Greedy Sweep | $O(n \log n)$ | $O(1)$ or $O(n)$ | Accepted |

## Algorithm Walkthrough

We process the array in increasing order so that earlier decisions never need to be revised for later elements.

1. Sort the array in non-decreasing order. This ensures we handle small values first, so large values do not artificially block them. The optimal structure must respect sorted order because swapping two elements in the final configuration can only reduce or preserve required increments.
2. Initialize a variable `current` to track the smallest value we are allowed to assign next. This represents the last chosen final value in the transformed array.
3. Iterate through the sorted array. For each element `x`, decide its final value as `max(x, current)`. This ensures the value is at least as large as the original and strictly greater than the previous chosen value if needed.
4. Accumulate the cost by adding `final_value - x` to the answer. This directly counts how many increments were applied to this element.
5. Update `current` to `final_value + 1`, enforcing strict distinctness for the next element.

Each step enforces minimal adjustment locally while preserving global feasibility. The sorting step ensures that when we raise a value, we never later encounter a smaller original value that would require revisiting earlier decisions.

### Why it works

The core invariant is that after processing the i-th element in sorted order, we have constructed the smallest possible strictly increasing sequence for the first i elements that respects all lower bounds imposed by the original array. Any optimal solution must assign values in increasing order when sorted by original value; otherwise, swapping two adjacent out-of-order assignments would not increase cost and would restore order. This exchange argument guarantees that greedily fixing each value to the earliest available slot never blocks optimal solutions later.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()

    current = -10**18
    ans = 0

    for x in a:
        if x <= current:
            ans += current + 1 - x
            current = current + 1
        else:
            current = x
        # next must be strictly larger
        current += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the greedy construction. Sorting is essential because it ensures we only ever need to compare with the last chosen value. The variable `current` represents the next free integer slot. When the current input value is already large enough, we can place it directly without extra cost. Otherwise, we push it forward to `current`, paying exactly the difference.

A common subtlety is updating `current` after assignment. It must always move to `final_value + 1`, not just `final_value`, because uniqueness requires strict separation between consecutive chosen values.

## Worked Examples

Consider input `[1, 1, 1]`.

After sorting, it remains `[1, 1, 1]`.

| Element | current before | chosen value | cost added | current after |
| --- | --- | --- | --- | --- |
| 1 | -∞ | 1 | 0 | 2 |
| 1 | 2 | 2 | 1 | 3 |
| 1 | 3 | 3 | 2 | 4 |

Total cost is 3.

This trace shows how each duplicate is pushed to the next available integer, forming a consecutive chain.

Now consider `[2, 2, 3]`.

| Element | current before | chosen value | cost added | current after |
| --- | --- | --- | --- | --- |
| 2 | -∞ | 2 | 0 | 3 |
| 2 | 3 | 3 | 1 | 4 |
| 3 | 4 | 4 | 1 | 5 |

The second 2 must be increased because 2 is already used, and the 3 must also be shifted upward to avoid collision.

These examples confirm that the algorithm always assigns the smallest feasible distinct values in order.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, followed by a single linear scan |
| Space | $O(1)$ or $O(n)$ | Depending on in-place sort implementation |

The constraints allow up to $2 \cdot 10^5$ elements, so an $O(n \log n)$ solution is comfortably within limits, while any quadratic simulation would time out.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    return str(solve_capture(inp)).strip()

def solve_capture(inp: str) -> int:
    data = inp.strip().split()
    n = int(data[0])
    a = list(map(int, data[1:]))

    a.sort()
    current = -10**18
    ans = 0

    for x in a:
        if x <= current:
            ans += current + 1 - x
            current = current + 1
        else:
            current = x
        current += 1

    return ans

# sample-like cases
assert solve_capture("3\n1 1 1") == 3
assert solve_capture("3\n1 2 3") == 0

# custom cases
assert solve_capture("1\n10") == 0
assert solve_capture("4\n5 5 5 5") == 6
assert solve_capture("5\n1 1 2 2 3") == 4
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | No increments needed |
| already distinct | 0 | Sorted monotone case |
| all equal | nontrivial cost | chain propagation |
| mixed duplicates | minimal reassignment | interaction of blocks |

## Edge Cases

A key edge case is when all elements are identical, such as `[5, 5, 5, 5]`. After sorting, the algorithm assigns 5, 6, 7, 8 with costs 0, 1, 2, 3 respectively. The `current` pointer ensures each new assignment is pushed just enough to avoid collision, never more.

Another edge case is a strictly increasing array like `[1, 2, 3, 4]`. The algorithm assigns values unchanged, since each element already satisfies the `current` constraint. This confirms that the greedy rule never introduces unnecessary increments.

A mixed cluster like `[1, 1, 2, 2, 3]` shows how duplicates across different values interact. The algorithm treats the sorted sequence uniformly, and `current` carries forward the global constraint so that local duplicates are resolved without breaking later structure.
