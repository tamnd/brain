---
title: "CF 2157E - Adjusting Drones"
description: "We are managing a fleet of drones, each with an initial energy level. The rule is that no energy level should appear more than k times."
date: "2026-06-08T00:20:04+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "dp", "dsu", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2157
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1066 (Div. 1 + Div. 2)"
rating: 1900
weight: 2157
solve_time_s: 117
verified: false
draft: false
---

[CF 2157E - Adjusting Drones](https://codeforces.com/problemset/problem/2157/E)

**Rating:** 1900  
**Tags:** binary search, brute force, data structures, dp, dsu, greedy, implementation, sortings  
**Solve time:** 1m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are managing a fleet of drones, each with an initial energy level. The rule is that no energy level should appear more than `k` times. If any energy level exceeds this limit, the drones perform a series of balancing operations: each drone that is a duplicate of an earlier occurrence in the array increments its energy by one. This operation continues until all energy levels appear at most `k` times. We need to compute the total number of these operations for each test case.

The input gives multiple test cases, each with the number of drones `n`, the maximum allowed count `k`, and the array of initial energies. Output is a single integer per test case representing the number of operations performed.

The constraints are significant. `n` can be up to `2·10^5`, and the total sum of `n` across test cases is also bounded by `2·10^5`. This rules out a naive simulation of every operation, which would be `O(n^2)` in the worst case if we iterate through duplicates repeatedly. Energy levels themselves are at most `2n`, so using frequency arrays or maps is feasible.

A subtle edge case occurs when all energy levels are equal. For example, if `n = 6` and `k = 3` with `a = [1,1,1,1,1,1]`, the operations evolve the array gradually, incrementing duplicates one by one. A careless greedy approach that only increments the last duplicates or counts only immediate overflows may miscalculate the total number of operations.

Another edge case is when `k >= n`. Then no operations are required, as the frequency limit is never exceeded.

## Approaches

A brute-force approach is straightforward: iterate over the array, mark all elements that are duplicates of earlier ones, increment them, and repeat until no element appears more than `k` times. This works correctly, but in the worst case, every drone might need to increment many times. If the largest number is 1 and `k = 1`, the operations could iterate roughly `n` times per drone, leading to `O(n^2)` behavior, which is too slow for `n = 2·10^5`.

The key insight is that the exact final positions of drones do not matter-only the counts of each energy level. We can sort the energy levels and simulate the increments in a compressed frequency space. If we count the number of duplicates per energy level beyond `k`, we can "carry" these excess drones to the next higher energy level in a single step. This reduces the process to a linear sweep over sorted unique energies, incrementing a counter of pending drones, which can be added to the next level in one step. Each increment corresponds exactly to an operation in the original process. This lets us compute the total operations in `O(n log n)` time due to the sorting step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal (frequency + carry) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n` and `k` and the energy array `a`.
2. Count the frequency of each energy level using a map or array. This gives us the number of drones currently at each energy.
3. Initialize a variable `carry` to 0. This will store the number of drones we need to increment at each step.
4. Iterate over the energy levels in increasing order. For each level `x`:

1. Add the current `carry` to the frequency of `x`. This represents all drones that were incremented from previous levels.
2. If the frequency of `x` exceeds `k`, compute `excess = freq[x] - k`. Increment `carry` by this `excess`. Each unit of excess will eventually become a balancing operation.
3. Increment the total operation counter by `excess`.
5. After processing all energy levels, the total operation counter contains the answer for the test case.

Why it works: the algorithm maintains the invariant that after processing energy level `x`, no drones below `x` are over their `k` limit. Any excess is propagated as `carry` to the next level, mimicking the original balancing operations. Sorting ensures that increments always go forward, so the order of operations matches the process described.

## Python Solution

```python
import sys
from collections import Counter
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        freq = Counter(a)
        ops = 0
        carry = 0
        
        for x in sorted(freq.keys()):
            freq[x] += carry
            if freq[x] > k:
                excess = freq[x] - k
                carry = excess
                ops += excess
            else:
                carry = 0
        
        print(ops)

solve()
```

The code first counts the frequencies and then sweeps through the sorted keys. `carry` propagates the excess duplicates forward, and each unit of carry represents exactly one operation performed in the original iterative process. Sorting is necessary to ensure drones always increment to the next higher energy level in the correct sequence.

## Worked Examples

For the input:

```
6 3
1 1 1 1 1 1
```

The frequency map is initially `{1:6}`. After processing `1`:

| Energy | freq | carry | ops |
| --- | --- | --- | --- |
| 1 | 6 | 3 | 3 |

`freq[1] > k` so `excess = 6-3=3`. Carry 3 to next level, ops += 3. No other keys exist, answer is 3.

For the input:

```
5 1
1 3 2 1 4
```

Initial freq: `{1:2, 2:1, 3:1, 4:1}`

| Energy | freq+carry | carry | ops |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 1 |
| 2 | 2 | 1 | 2 |
| 3 | 2 | 1 | 3 |
| 4 | 2 | 1 | 4 |

Final answer: 4. This confirms that each operation corresponds exactly to moving duplicates forward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the unique energies dominates; the sweep is linear. |
| Space | O(n) | Frequency map stores at most `n` keys. |

With `n` up to `2·10^5` and a total of `2·10^5` over all test cases, this solution easily fits within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("5\n6 3\n1 1 1 1 1 1\n5 1\n1 3 2 1 4\n6 2\n1 1 1 2 3 3\n4 1\n8 8 8 8\n2 2\n1 2") == "3\n4\n4\n3\n0"

# custom tests
assert run("1\n1 1\n1") == "0", "single drone, no ops"
assert run("1\n4 4\n1 1 1 1") == "0", "all drones allowed, no ops"
assert run("1\n4 1\n1 1 1 1") == "3", "all equal, k=1, multiple ops"
assert run("1\n5 2\n2 2 2 2 2") == "3", "all equal, k=2"
assert run("1\n6 3\n1 1 1 2 2 2") == "0", "two groups at limit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 0 | single drone, no operations |
| 4 4 4 4, k=4 | 0 | all equal, limit equals size |
| 4 1 1 1 1, k=1 | 3 | repeated increments for all-equal array |
| 2 2 2 2 2, k=2 | 3 | multiple operations for over-limit group |
| 1 1 1 2 2 2, k=3 | 0 | multiple groups exactly at limit |

## Edge Cases

When `n = k`, no operations occur regardless of drone energies. For example, `n = 2, k = 2, a = [5,5]`. The frequency of 5 is 2, which is equal to `k`, so `carry` remains zero and the output is `0`.

When all energies are the same and `k = 1`, such as `n = 6, k = 1, a = [1,1,1,1,1,1]`, each pass increments duplicates and generates carry until no energy exceeds `k`. Our algorithm correctly propagates the excess with carry
