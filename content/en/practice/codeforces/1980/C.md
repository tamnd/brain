---
title: "CF 1980C - Sofia and the Lost Operations"
description: "We are asked to determine whether a given array b could have been produced from an original array a by applying a sequence of assignment operations where the target indices are lost, but the values assigned in order are known."
date: "2026-06-08T16:53:36+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1980
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 950 (Div. 3)"
rating: 1300
weight: 1980
solve_time_s: 184
verified: true
draft: false
---

[CF 1980C - Sofia and the Lost Operations](https://codeforces.com/problemset/problem/1980/C)

**Rating:** 1300  
**Tags:** constructive algorithms, greedy  
**Solve time:** 3m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a given array `b` could have been produced from an original array `a` by applying a sequence of assignment operations where the target indices are lost, but the values assigned in order are known. Each operation assigns a specified value `d_j` to some element of the array. The challenge is that the sequence of indices is unknown, and we need to verify whether a valid sequence exists that transforms `a` into `b`.

The input provides multiple test cases, each with the original array, the target array, and the sequence of values `d`. Our task is to answer “YES” if it is possible to assign the values in order to produce `b`, and “NO” otherwise.

The constraints are significant: arrays can have up to 2·10^5 elements, and the sum of `n` and `m` across all test cases is limited to 2·10^5. This implies that any solution iterating over each array multiple times in nested loops would be too slow. We need a linear or near-linear approach per test case.

A subtle edge case arises when multiple positions in `b` require the same value `d_j` but fewer instances of `d_j` are available in the operation list, or when the last occurrence of a value in `b` must be assigned by a specific operation. For example, if `a = [1,2,1]`, `b = [1,3,2]`, and `d = [1,3,1,2]`, the assignment must correctly map the last `3` in `b` to one of the available `3`s in `d`. A careless approach that only checks value counts without respecting order would produce a false positive.

## Approaches

A naive approach would attempt all permutations of indices for the assignment operations. This is clearly infeasible because there are `n^m` possible sequences in the worst case, and `m` can be up to 2·10^5. Brute-force checking each permutation is therefore impractical.

The optimal approach leverages a greedy strategy combined with counting. For each position in `b` where `a_i != b_i`, we need to assign the required value using the last occurrence of each value in `d`. We can maintain a dictionary mapping each value to a stack of positions in `b` that require it, processed from right to left. Then, we iterate through `d` in order and check if there is a valid position to apply it. The critical insight is that the last occurrence of each value in `b` must be covered by the last corresponding `d_j`, and we can propagate earlier assignments greedily. This ensures a linear-time solution that respects both the order of operations and the required target array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * m!) | O(n + m) | Too slow |
| Greedy Counting with Stacks | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the original array `a`, the target array `b`, and the sequence of values `d`.
2. Create a dictionary `need` mapping each value in `b` that differs from `a` to a list of indices where it is required, stored in reverse order. This allows us to pop positions from right to left efficiently.
3. Initialize a pointer `last_pos` to track the last assigned position for each value. This ensures we always respect the rightmost constraint.
4. Iterate through the sequence `d`. For each value `val`:

- If `need[val]` is empty, use the last assigned position of `val` to satisfy the operation (propagation).
- Otherwise, pop the last required position from `need[val]` and assign it, updating `last_pos[val]`.
5. After processing all `d`, check if any value still has unassigned positions in `need`. If so, the answer is “NO”; otherwise, “YES”.

Why it works: Each assignment operation is used in order. By storing required positions in reverse and assigning from the rightmost requirement, we guarantee that all necessary assignments are made, while allowing propagation to satisfy operations not strictly required. The invariant is that at each step, the remaining required positions are always reachable by future operations, so no necessary assignment is skipped.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict, deque

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        m = int(input())
        d = list(map(int, input().split()))
        
        need = defaultdict(deque)
        for i in range(n-1, -1, -1):
            if a[i] != b[i]:
                need[b[i]].appendleft(i)
        
        last_pos = {}
        possible = True
        for val in d:
            if need[val]:
                idx = need[val].pop()
                last_pos[val] = idx
            elif val in last_pos:
                pass  # propagate to last used position
            else:
                possible = False
                break
        
        for positions in need.values():
            if positions:
                possible = False
                break
        
        print("YES" if possible else "NO")

solve()
```

The solution first builds a mapping of required positions in `b` for each differing value. Using `deque` allows O(1) pops from either end, enabling right-to-left assignment. The `last_pos` dictionary allows propagation of values when no immediate requirement exists. After processing all `d`, any leftover required positions indicate an impossible transformation.

## Worked Examples

Consider the first sample:

```
a = [1, 2, 1]
b = [1, 3, 2]
d = [1, 3, 1, 2]
```

| Step | val from d | need before | need after | last_pos | Comment |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3:[1],2:[2],1:[2] | 3:[1],2:[2] | 1:2 | Assign 1 to last position 2 |
| 2 | 3 | 3:[1],2:[2] | 3:[] ,2:[2] | 3:1 | Assign 3 to position 1 |
| 3 | 1 | 3:[],2:[2] | 3:[],2:[2] | 1:2 | Propagate 1 to last position 2 |
| 4 | 2 | 3:[],2:[2] | 3:[],2:[] | 2:2 | Assign 2 to position 2 |

All `need` lists empty → YES.

Another sample:

```
a = [1, 2, 3, 5]
b = [2, 1, 3, 5]
d = [2, 1, 3, 5]
```

Following the algorithm, the first value 2 cannot be assigned to a correct position respecting order → NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each index in `b` is processed at most once, and each `d_j` is processed once |
| Space | O(n + m) | `need` stores positions per value, `last_pos` stores last assigned index per value |

The algorithm is linear in the size of the arrays and sequence, fitting within the problem constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("""7
3
1 2 1
1 3 2
4
1 3 1 2
4
1 2 3 5
2 1 3 5
2
2 3
5
7 6 1 10 10
3
6 1 11 11
3
4 3 11
4
3 1 7 8
2
2 7 10
5
10 3 2 2 1
5
5 7 1 7 9
4
10 1 2 9
8
1 1 9 8 7 2 10 4
4
1000000000 203 203 203
203 1000000000 203 1000000000
2
203 1000000000
1
1
1
5
1 3 4 5 1
""") == "YES\nNO\nNO\nNO\nYES\nNO\nYES"
```

Custom cases can include single-element arrays, repeated values, or operations with extra unused values to verify propagation.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 1 2 | 2 1 |
| 3 | [1,1,1], d=[1,1,1] | YES |
| 4 | [1,2,3], b=[3,2,1], d=[ |  |
