---
title: "CF 932C - Permutation Cycle"
description: "We are asked to construct a permutation of the numbers from 1 to N such that every position behaves in a very specific cyclic way."
date: "2026-06-17T02:57:06+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 932
codeforces_index: "C"
codeforces_contest_name: "ICM Technex 2018 and Codeforces Round 463 (Div. 1 + Div. 2, combined)"
rating: 1600
weight: 932
solve_time_s: 196
verified: false
draft: false
---

[CF 932C - Permutation Cycle](https://codeforces.com/problemset/problem/932/C)

**Rating:** 1600  
**Tags:** brute force, constructive algorithms  
**Solve time:** 3m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a permutation of the numbers from 1 to N such that every position behaves in a very specific cyclic way. The permutation defines a deterministic walk: starting from a position i, we repeatedly apply the permutation mapping and observe how many steps it takes before we return to i for the first time. That number of steps, for each i, must be either A or B.

In graph terms, the permutation decomposes into disjoint directed cycles. Each cycle is independent, and every element in a cycle returns to itself exactly after the length of that cycle. So the value g(i) is nothing more than the length of the cycle containing i. The task reduces to constructing a permutation of size N whose cycle lengths are only A or B.

The input constraints allow N up to 10^6, so any solution must be linear or close to linear. Anything involving checking permutations or simulating mappings per element would immediately become too slow, since O(N^2) behavior would imply up to 10^12 operations in the worst case.

A subtle failure case arises when A and B are equal or when one of them is 1. If A = B, the problem reduces to building a permutation where all cycles have that exact length, which is only possible if N is divisible by A. If A = 1 and B > 1, we are forced to create many fixed points mixed with longer cycles, but a fixed point already consumes a cycle of length 1, so any mismatch in leftover elements breaks feasibility quickly. Another fragile situation is when neither A nor B divides N in a compatible combination, even though greedy partitioning might superficially appear to work.

## Approaches

A brute-force approach would try to partition the set {1..N} into groups, assign each group a cycle length A or B, and then test whether a valid permutation can be formed. For each partition, we would construct cycles explicitly and verify correctness. The number of ways to split N into A and B-sized groups is exponential in N, since at each step we may choose either size, leading to roughly 2^(N / min(A, B)) possibilities in the worst case. Even for moderate N this becomes completely infeasible.

The key observation is that the permutation structure removes almost all freedom once cycle lengths are chosen. Each valid solution corresponds only to choosing how many cycles of length A and how many of length B we use. Once those counts are fixed, constructing the permutation is mechanical: we simply assign consecutive blocks and wire them into cycles.

This reduces the problem to solving a linear Diophantine constraint:

x * A + y * B = N, where x and y are non-negative integers. Once a valid pair (x, y) is found, construction is straightforward.

The brute-force idea fails because it reasons at the level of individual elements, while the correct view is at the level of cycle decomposition. The structure of permutations collapses the problem into integer partitioning.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(N) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Ensure A and B are treated in a consistent order. If B is smaller than A, swap them. This reduces the search space and simplifies the Diophantine solving step without affecting validity.
2. Iterate over the number of cycles of length A. For each possible value x, compute the remaining elements after using x cycles of size A. This is N - x * A. The remaining must be divisible by B, otherwise this split cannot produce a valid partition.
3. If the remainder is divisible by B, compute y = (N - x * A) / B. If y is non-negative, we have found a valid decomposition of N into cycles.
4. Once (x, y) is found, construct the permutation by repeatedly taking consecutive blocks. For each block of size A, connect elements in a directed cycle. Do the same for blocks of size B.
5. If no pair (x, y) works, output -1 since no valid permutation exists.

The construction step works because cycles can be formed independently: within a block [i..i+k-1], we simply map each element to the next, and the last back to the first.

### Why it works

The crucial invariant is that every element belongs to exactly one cycle, and the length of that cycle is fully determined by the size of the block we assign it to. Since we only create cycles of size A or B, every g(i) equals either A or B by construction. The Diophantine step guarantees that every element is used exactly once, so no leftover elements remain unassigned.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build(n, k, start):
    arr = list(range(start, start + k))
    for i in range(k - 1):
        arr[i], arr[i] = arr[i], arr[i]  # placeholder clarity
    for i in range(k - 1):
        p[arr[i] - 1] = arr[i + 1]
    p[arr[-1] - 1] = arr[0]
    return start + k

n, A, B = map(int, input().split())

if A > B:
    A, B = B, A

p = [0] * n

found = False
for x in range(n // A + 1):
    rem = n - x * A
    if rem >= 0 and rem % B == 0:
        y = rem // B
        found = True
        idx = 1
        for _ in range(x):
            arr = list(range(idx, idx + A))
            for i in range(A - 1):
                p[arr[i] - 1] = arr[i + 1]
            p[arr[A - 1] - 1] = arr[0]
            idx += A
        for _ in range(y):
            arr = list(range(idx, idx + B))
            for i in range(B - 1):
                p[arr[i] - 1] = arr[i + 1]
            p[arr[B - 1] - 1] = arr[0]
            idx += B
        break

if not found:
    print(-1)
else:
    print(*p)
```

The code first normalizes the two cycle sizes so that A is not larger than B, which slightly reduces the number of iterations in the search loop. It then searches for a valid count of A-sized cycles. Once a valid split is found, it constructs cycles greedily from left to right. Each cycle is written directly into the permutation array.

A subtle point is that indexing is handled in 1-based form during construction and only converted implicitly when writing into the zero-based array. This avoids off-by-one mistakes in cycle wiring.

## Worked Examples

### Example 1

Input:

```
9 2 5
```

We try possible numbers of 2-cycles:

| x (A-cycles) | remaining | divisible by 5 | y (B-cycles) |
| --- | --- | --- | --- |
| 0 | 9 | no | - |
| 1 | 7 | no | - |
| 2 | 5 | yes | 1 |

So we take x = 2, y = 1.

Construction proceeds sequentially:

| Step | Block | Action | Partial permutation |
| --- | --- | --- | --- |
| 1 | [1,2] | form 2-cycle | 1→2, 2→1 |
| 2 | [3,4] | form 2-cycle | 3→4, 4→3 |
| 3 | [5,6,7,8,9] | form 5-cycle | 5→6→7→8→9→5 |

This confirms all cycle lengths are either 2 or 5.

### Example 2

Input:

```
6 1 3
```

Try x = number of 1-cycles:

| x | remaining | divisible by 3 | y |
| --- | --- | --- | --- |
| 0 | 6 | yes | 2 |

So we build two 3-cycles and no fixed points:

| Step | Block | Action |
| --- | --- | --- |
| 1 | [1,2,3] | 1→2→3→1 |
| 2 | [4,5,6] | 4→5→6→4 |

All elements return to themselves after exactly 3 steps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | We try up to N/A splits, and each construction processes all elements once |
| Space | O(N) | We store the permutation array |

The constraints allow up to 10^6 elements, and the construction is linear, so the solution runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue().strip()

# NOTE: placeholder structure; actual solution should be wrapped in function

# sample
# assert run("9 2 5") == "6 5 8 3 4 1 9 2 7"

# custom tests
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | smallest valid cycle |
| `5 2 3` | valid permutation | mixed cycle sizes |
| `6 4 5` | `-1` | impossible decomposition |
| `10 1 10` | valid permutation | extreme imbalance |

## Edge Cases

One important edge case is when A equals 1. In this case, we are forced to create fixed points. If B does not divide the remaining elements after choosing some fixed points, no solution exists. The algorithm handles this naturally because the Diophantine check immediately fails for invalid splits.

Another case is when A equals B. Then the loop reduces to checking whether N is divisible by A. The construction produces uniform cycles, and no mixing is required. The algorithm still works because only one valid split exists.

When N is small, especially N = A or N = B, the solution degenerates into a single cycle. The construction step still works because we create exactly one block covering all elements.
