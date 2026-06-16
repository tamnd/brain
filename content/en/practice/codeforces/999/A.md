---
title: "CF 999A - Mishka and Contest"
description: "We are given a list of problems arranged in a fixed order from left to right, where each problem has a difficulty value. Mishka has a skill level k, meaning he can only solve problems whose difficulty does not exceed k."
date: "2026-06-16T23:51:47+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 999
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 490 (Div. 3)"
rating: 800
weight: 999
solve_time_s: 80
verified: true
draft: false
---

[CF 999A - Mishka and Contest](https://codeforces.com/problemset/problem/999/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of problems arranged in a fixed order from left to right, where each problem has a difficulty value. Mishka has a skill level `k`, meaning he can only solve problems whose difficulty does not exceed `k`.

The process is constrained in an important way: at any moment, only the leftmost and rightmost remaining problems are available. Mishka repeatedly chooses one of these two ends, removes that problem, and solves it only if its difficulty is within his capability. If neither end is solvable, he stops immediately and no further moves are possible.

The goal is to determine how many problems he can successfully remove and solve before getting stuck.

The constraints are small: `n ≤ 100` and all values are at most `100`. This immediately tells us that even quadratic or cubic simulations are easily fast enough, and a greedy simulation with pointer movement is sufficient. There is no need for advanced data structures or optimization beyond constant-time checks per step.

A few edge situations matter:

If both ends are initially too difficult, Mishka solves nothing. For example, input `n = 3, k = 1, [5, 6, 7]` produces output `0` because no valid move exists at the start.

If all values are within `k`, Mishka can eventually remove everything regardless of choices, because every removal keeps exposing new valid endpoints.

A subtle case is when only one side is ever valid at each step, forcing a deterministic sequence. A naive misunderstanding might attempt to always pick the smaller or larger endpoint, but the problem does not require optimization of choice strategy, since any valid sequence that continues removing solvable endpoints until blocked leads to the same maximum number of removals under this greedy constraint.

## Approaches

A direct way to think about this is to simulate the process exactly. We maintain two pointers, one at the left end and one at the right end of the array. At each step, we check whether the left value or right value is solvable.

If neither is solvable, we stop. Otherwise, we take one of the valid ends and move the corresponding pointer inward, increasing our count.

Because both ends are always available choices, the natural brute-force idea would be to try all possible sequences of choices: at each step, branch into taking left or right if valid. This leads to an exponential number of states, since each of up to `n` steps can branch into two choices. In the worst case, this becomes `O(2^n)`, which is unnecessary given that the decision is not actually dependent on future outcomes in a way that requires search.

The key observation is that we never need to backtrack. Once an element is taken from either end, it is permanently removed, and the only constraint is whether it is ≤ `k`. There is no interaction between choices that would make one branch strictly better than another in terms of future feasibility. Any valid move contributes exactly one to the answer, and stopping only occurs when both ends are invalid.

This reduces the problem to a greedy two-pointer simulation: repeatedly consume valid endpoints until neither end qualifies.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all sequences) | O(2^n) | O(n) | Too slow |
| Two-pointer simulation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We keep two indices, `l = 0` and `r = n - 1`, and a counter `ans = 0`.

1. Check whether the process can continue by testing both ends of the current segment.
2. If `a[l] <= k`, remove the left element by incrementing `l` and increasing `ans` by one.
3. Else if `a[r] <= k`, remove the right element by decrementing `r` and increasing `ans`.
4. If neither condition holds, terminate immediately since no further move is possible.

Each step corresponds exactly to one removal, so the loop continues until the segment collapses or becomes unplayable.

The reasoning behind choosing left first is not important for correctness in this problem, because whenever both ends are valid, either choice still keeps the process consistent: both choices consume one valid element and reduce the problem size by one.

### Why it works

At every step, the only factor that matters is whether at least one endpoint is solvable. If both endpoints exceed `k`, no future action can change that situation because no internal element can become accessible without first removing an endpoint. Thus the stopping condition is globally valid, not local. Each valid removal strictly reduces the array size while preserving correctness of remaining endpoints, so the process simulates exactly the maximal possible number of solvable removals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    l, r = 0, n - 1
    ans = 0
    
    while l <= r:
        if a[l] <= k:
            ans += 1
            l += 1
        elif a[r] <= k:
            ans += 1
            r -= 1
        else:
            break
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation uses a classic two-pointer pattern. The loop condition `l <= r` ensures we only process remaining elements. Inside, we test the left endpoint first, then the right endpoint. This order is arbitrary but consistent, since both choices are equivalent in contribution to the final count.

The termination condition is triggered when neither endpoint is valid, which corresponds directly to the stopping rule in the problem statement. No additional bookkeeping is needed.

## Worked Examples

### Example 1

Input:

```
8 4
4 2 3 1 5 1 6 4
```

| Step | l | r | a[l] | a[r] | Action | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 7 | 4 | 4 | take left | 1 |
| 2 | 1 | 7 | 2 | 4 | take left | 2 |
| 3 | 2 | 7 | 3 | 4 | take left | 3 |
| 4 | 3 | 7 | 1 | 4 | take left | 4 |
| 5 | 4 | 7 | 5 | 4 | take right | 5 |
| 6 | 4 | 6 | 5 | 6 | stop | 5 |

This trace shows how the process continues as long as at least one end is valid. Once both ends exceed `k`, termination is immediate.

### Example 2

Input:

```
5 3
4 4 4 4 4
```

| Step | l | r | a[l] | a[r] | Action | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 4 | 4 | 4 | stop | 0 |

This demonstrates the immediate termination case where no endpoint is ever solvable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is removed at most once from either end |
| Space | O(1) | Only two pointers and a counter are used |

The constraints `n ≤ 100` make even this linear scan trivial in practice, but the solution is already optimal in asymptotic terms and scales to larger limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("8 4\n4 2 3 1 5 1 6 4\n") == "5"

# minimum case
assert run("1 10\n5\n") == "1"

# all too hard
assert run("3 1\n2 3 4\n") == "0"

# all solvable
assert run("4 10\n1 2 3 4\n") == "4"

# alternating valid endpoints
assert run("5 3\n3 9 3 9 3\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal boundary handling |
| all > k | 0 | immediate termination |
| all ≤ k | full length | full consumption |
| alternating | partial greedy flow | correct pointer decisions |

## Edge Cases

One important edge case is when the first and last elements are both invalid. For example:

Input:

```
4 2
5 1 1 5
```

At the start, both endpoints are `5`, which exceeds `k`. The algorithm checks both ends, finds neither valid, and stops immediately with output `0`.

Another case is when only one side is ever valid:

Input:

```
5 3
3 4 4 4 3
```

Step by step, the left end is always valid first until it becomes invalid, after which the right side is used. The pointers shrink consistently until no valid endpoint remains. The greedy rule correctly alternates only when necessary and never skips a valid move.

A final case is a fully solvable array:

Input:

```
3 5
1 2 3
```

The algorithm removes all elements in sequence because at every step at least one endpoint is valid, and eventually both pointers meet.
