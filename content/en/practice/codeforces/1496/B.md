---
title: "CF 1496B - Max and Mex"
description: "We are given a multiset of distinct non-negative integers and need to simulate a process where, up to k times, we add the element (mex + max + 1) // 2 to the multiset. The mex of a set is the smallest non-negative integer not present, and max is the largest element."
date: "2026-06-10T21:55:10+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1496
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 706 (Div. 2)"
rating: 1100
weight: 1496
solve_time_s: 271
verified: false
draft: false
---

[CF 1496B - Max and Mex](https://codeforces.com/problemset/problem/1496/B)

**Rating:** 1100  
**Tags:** math  
**Solve time:** 4m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of distinct non-negative integers and need to simulate a process where, up to `k` times, we add the element `(mex + max + 1) // 2` to the multiset. The `mex` of a set is the smallest non-negative integer not present, and `max` is the largest element. After performing the operation `k` times, we must report how many **distinct** integers the multiset contains.

The input specifies multiple test cases. Each case gives `n`, the initial multiset size, `k`, the number of operations, and the distinct integers in the multiset. The output is a single integer per case.

Constraints are significant. `n` can be up to `10^5`, and `k` can be up to `10^9`. That means simulating every operation is impossible. We must reason mathematically about what happens after each addition. The sum of `n` over all test cases is `10^5`, so we can afford `O(n log n)` operations per test case, but anything like `O(k)` is hopeless.

Subtle edge cases arise when the `mex` is greater than the `max`. For example, if the set is `{0,1,2}` and `k=2`, the `mex` is `3` and `max` is `2`. Adding `(3+2+1)//2=3` creates a duplicate, so the first operation does not increase the number of distinct elements. However, after duplicates are allowed, adding a new `mex` larger than the current `max` will increase the distinct count predictably.

A careless implementation might simulate every operation or fail to handle `k=0`, producing wrong results for cases where no operations are performed.

## Approaches

The brute-force approach is straightforward. For each operation, compute `mex` and `max`, calculate `(mex + max + 1) // 2`, and insert it into the multiset. After `k` operations, count the distinct elements. This works because each step correctly follows the problem definition. However, with `k` up to `10^9`, this is far too slow; even computing `mex` repeatedly would cost `O(n)` per operation, giving `O(n*k)` which is unfeasible.

The key observation is that the process stabilizes quickly. Let `a = mex(S)` and `b = max(S)`. If `a > b`, then `(a+b+1)//2 = a`, which is strictly larger than `b`, so each operation just adds the next integer after the current max. In this case, the number of distinct elements increases by `k`. If `a <= b`, then `(a+b+1)//2` produces a number between `a` and `b`. Adding this number may either introduce a new element (if it is not in the set) or a duplicate (if it is). In most cases, adding it once is enough; after that, the set no longer changes, because the `mex` becomes equal to the new number, stabilizing the set.

Thus, we only need to consider two scenarios: either the set stabilizes after one operation or we just append new numbers beyond the current `max`. This reduces the problem to a constant-time calculation per test case once we know `mex` and `max`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*k) | O(n) | Too slow for large k |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the input array into a Python `set` to track distinct elements efficiently.
2. Compute the `mex` by iterating from `0` upwards until an integer is missing in the set.
3. Compute the `max` using the built-in `max()` function.
4. If `k=0`, return the current number of distinct elements immediately.
5. If `mex` is greater than `max`, each operation will add a new integer larger than `max`. So the total distinct count after `k` operations is `len(S) + k`.
6. Otherwise, compute the candidate new element as `(mex + max + 1) // 2`. Add it to the set if it is not already present.
7. Return the size of the updated set.

Why it works: the `mex` ensures we are always targeting the smallest missing element, and the formula `(mex + max + 1) // 2` produces either a new element within the current range or extends the set beyond the current maximum. In either case, only one addition can potentially change the distinct count if `mex <= max`; further operations do not introduce new numbers because the `mex` shifts to the added element, which is now in the set, stabilizing the set immediately.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        arr = list(map(int, input().split()))
        S = set(arr)
        mex = 0
        while mex in S:
            mex += 1
        max_val = max(S)
        
        if k == 0:
            print(len(S))
            continue
        
        if mex > max_val:
            # Every operation adds a new number beyond current max
            print(len(S) + k)
        else:
            new_elem = (mex + max_val + 1) // 2
            S.add(new_elem)
            print(len(S))

if __name__ == "__main__":
    solve()
```

The code converts the array to a set for O(1) membership checks. Computing `mex` requires scanning from 0 upward until a missing number is found. If `mex > max_val`, we simply add `k` distinct numbers sequentially, each beyond the current maximum. Otherwise, adding `(mex + max + 1)//2` once is enough because the set will stabilize immediately afterward. Handling `k=0` ensures we do not accidentally modify the set.

## Worked Examples

**Example 1:**

Input: `S = {0,1,3,4}`, `k=1`

| Step | S | mex | max | new_elem | Notes |
| --- | --- | --- | --- | --- | --- |
| init | {0,1,3,4} | 2 | 4 | - | initial set |
| op1 | add 3 | 2 | 4 | 3 | 3 already exists, so S becomes {0,1,3,3,4} |
| final | {0,1,3,4} | - | - | - | distinct elements = 4 |

This shows that adding an element already present does not increase the distinct count.

**Example 2:**

Input: `S = {0,1,2}`, `k=2`

| Step | S | mex | max | new_elem | Notes |
| --- | --- | --- | --- | --- | --- |
| init | {0,1,2} | 3 | 2 | - | initial set |
| op1 | add 3 | 3 | 3 | 3 | mex > max, adding new element |
| op2 | add 4 | 4 | 3 | 4 | mex > max again |
| final | {0,1,2,3,4} | - | - | - | distinct elements = 5 |

This demonstrates the scenario when `mex > max`, where each operation adds a genuinely new element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Converting to set, computing `mex` by scanning at most `n+1` numbers, computing `max` |
| Space | O(n) | Storing the set of elements |

Given the sum of all `n` ≤ 10^5, this fits comfortably within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("5\n4 1\n0 1 3 4\n3 1\n0 1 4\n3 0\n0 1 4\n3 2\n0 1 2\n3 2\n1 2 3\n") == "4\n4\n3\n5\n3"

# Custom tests
# k = 0, should return original size
assert run("1\n5 0\n0 1 2 4 5\n") == "5"
# mex > max, k > 1
assert run("1\n3 3\n0 1 2\n") == "6"
# adding a number that already exists
assert run("1\n3 1\n0 1 4\n") == "4"
# single element, k = 5
assert run("1\n1 5\n0\n") == "6"
# large max with small mex
assert run("1\n4 2\n0 2 3 10\n") == "5"
```

|
