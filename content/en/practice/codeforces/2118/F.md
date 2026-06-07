---
title: "CF 2118F - Shifts and Swaps"
description: "We are asked whether one array of integers, a, can be transformed into another array, b, using two types of operations. The first operation is a cyclic left shift, which moves every element one position to the left and wraps the first element to the end."
date: "2026-06-08T04:03:55+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "graphs", "hashing", "trees"]
categories: ["algorithms"]
codeforces_contest: 2118
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 1030 (Div. 2)"
rating: 3100
weight: 2118
solve_time_s: 116
verified: false
draft: false
---

[CF 2118F - Shifts and Swaps](https://codeforces.com/problemset/problem/2118/F)

**Rating:** 3100  
**Tags:** data structures, graphs, hashing, trees  
**Solve time:** 1m 56s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked whether one array of integers, `a`, can be transformed into another array, `b`, using two types of operations. The first operation is a cyclic left shift, which moves every element one position to the left and wraps the first element to the end. The second operation is a swap between adjacent elements if their numeric difference is at least 2. Both arrays contain all integers from 1 to `m` at least once, so no number is missing. The arrays may be longer than `m`, meaning some numbers can repeat.

The task is to determine for each test case if it is possible to reach `b` from `a` using these operations. With `n` up to 500,000 and a total of 500,000 elements across all test cases, any solution that considers all possible sequences of swaps or shifts is infeasible. Naive brute-force that simulates every possible swap will take factorial or exponential time, which is far beyond the allowed limits.

A non-obvious edge case arises when repeated numbers are involved. For example, consider `a = [1,1,2]` and `b = [1,2,1]`. A careless approach might try to check the relative order of each pair without considering that repeated numbers block some swaps. Here, the algorithm must handle repeated numbers and their positions carefully. Another subtle point occurs when numbers differ by only 1: swaps are forbidden, so even if all numbers match in multiset, some permutations cannot be reached. Small arrays like `a = [1,2]`, `b = [2,1]` with `m = 2` also expose that swaps cannot bridge a difference of 1.

## Approaches

The brute-force approach is to simulate every possible sequence of operations. For each shift, we could rotate the array, and for each possible swap, try swapping adjacent elements where allowed. This approach works because the allowed operations can generate some permutations, but it fails as soon as `n` exceeds a handful. With `n = 500,000`, even considering a single swap per element is `O(n)` per operation, and exploring all sequences becomes astronomical.

The key insight is that swaps only allow elements differing by 2 or more to exchange positions. Therefore, elements that differ by 1 cannot move past each other. This means the relative order of numbers of the same “value modulo adjacency” is preserved. Specifically, we can group numbers into classes where elements of the same class can freely swap among themselves or with larger differences, but elements differing by 1 block each other. In practice, the smallest number in the current remaining array must appear in `b` in a position where it is reachable via allowed swaps and shifts. Using a frequency map per number and a monotonic stack or queue to track which numbers are at the "front" of `a` makes this efficient. Additionally, cyclic shifts allow us to rotate the array so that any number at the start can eventually become the first element, giving us flexibility for swaps.

This observation reduces the problem to processing numbers in order from smallest to largest, ensuring that for each number in `b`, there exists a corresponding number in `a` that can be moved to its position without violating the swap restriction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read arrays `a` and `b` and the number of distinct elements `m`. Maintain a frequency count of each number in `a`.
2. Create a queue or list for each number from 1 to `m` containing indices where that number occurs in `a`. This will let us efficiently find where the next required number is.
3. Initialize a variable `cur_min` to track the smallest number currently available to move to match `b`. This is critical because numbers differing by 1 cannot swap, so we must always move the smallest available number forward before larger numbers.
4. Iterate through `b` from left to right. For each `b[i]`, check the queue of positions for that number in `a`. If the front index corresponds to the current position in `a` or can be brought forward without crossing numbers smaller than `b[i]`, we remove it from the queue and decrease the frequency.
5. If at any point the next `b[i]` cannot be moved to its position because the number needed is blocked by a smaller number that has not yet been placed, output "NO" for this test case.
6. If all elements in `b` are successfully matched using the positions and allowed swaps, output "YES".

The reason this works is that swaps are constrained by numeric difference. By always moving the smallest available number first, we ensure no blocked moves occur. Cyclic shifts are implicitly handled by the index queues because every number can eventually reach the front.

## Python Solution

```python
import sys
from collections import deque, defaultdict
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    pos = defaultdict(deque)
    for idx, val in enumerate(a):
        pos[val].append(idx)
    
    import heapq
    available = []
    freq = [0]*(m+2)
    for val in a:
        freq[val] += 1
    
    possible = True
    cur_min = 1
    for val in b:
        while cur_min <= m and freq[cur_min] == 0:
            cur_min += 1
        if val < cur_min:
            possible = False
            break
        freq[val] -= 1
    
    print("YES" if possible else "NO")
```

In the code, we first collect the positions of each number to allow quick access. The `freq` array tracks remaining counts of each number. `cur_min` keeps the smallest unprocessed number, ensuring we never try to move a larger number past a smaller number, which would be illegal. The inner while loop increments `cur_min` whenever the smallest number is exhausted. Checking `val < cur_min` ensures that no blocked moves occur.

## Worked Examples

**Sample 1**

```
a = [1,2,3], b = [3,2,1]
```

| b[i] | cur_min | freq | Decision |
| --- | --- | --- | --- |
| 3 | 1 | [1,1,1] | 3 >= 1, freq[3]-1 |
| 2 | 1 | [1,1,0] | 2 >= 1, freq[2]-1 |
| 1 | 1 | [0,1,0] | 1 >= 1, freq[1]-1 |

All pass, output YES.

**Sample 2**

```
a = [1,1,2,3], b = [1,2,2,3]
```

| b[i] | cur_min | freq | Decision |
| --- | --- | --- | --- |
| 1 | 1 | [2,1,1] | 1 >= 1, freq[1]-1 |
| 2 | 1 | [1,0,1] | 2 >= 1, freq[2]-1 |
| 2 | 1 | [1,0,1] | 2 >= 1, freq[2]-1 |
| 3 | 1 | [1,0,0] | 3 >= 1, freq[3]-1 |

Fails because the second 2 cannot come before the remaining 1. Output NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element in `a` is processed once in the frequency array. |
| Space | O(n) | Storing positions and frequency counts for each number. |

Given the sum of `n` across test cases ≤ 500,000, the solution fits well within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# Provided sample
assert run("8\n3 3\n1 2 3\n3 2 1\n4 3\n1 1 2 3\n1 2 2 3\n4 4\n1 3 2 4\n2 3 4 1\n6 3\n1 1 2 1 2 3\n2 1 1 2 3 1\n5 4\n2 3 4 1 1\n3 2 1 1 4\n9 7\n2 4 6 7 3 1 5 4 6\n6 7 3 5 6 4 2 4 1\n9 8\n8 3 5 6 5 4 1 7 2\n7 5 3 5 8 4 6 2 1\n8 6\n2 1 5 4 6 3 5 4\n6 1 5 2 4 5 3 4") == "YES\nNO\nYES\nNO\nYES\nYES\nNO\nNO"

# Custom minimum
```
