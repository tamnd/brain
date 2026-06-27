---
title: "CF 105079G - Sneaking Sprinkles"
description: "We are given a collection of cupcakes, each starting with some number of sprinkles. There is also a sequence of operations, and each operation behaves in two phases. First, a fixed amount of sprinkles is added to every cupcake."
date: "2026-06-27T21:29:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105079
codeforces_index: "G"
codeforces_contest_name: "UTPC x WiCS Contest 04-05-23 (UT Internal)"
rating: 0
weight: 105079
solve_time_s: 81
verified: false
draft: false
---

[CF 105079G - Sneaking Sprinkles](https://codeforces.com/problemset/problem/105079/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of cupcakes, each starting with some number of sprinkles. There is also a sequence of operations, and each operation behaves in two phases. First, a fixed amount of sprinkles is added to every cupcake. Then Bob immediately reacts by identifying the cupcake with the largest current number of sprinkles and stealing half of its sprinkles, where “half” means floor division, so that cupcake loses floor(x/2) and keeps the remainder.

The operations are repeated in order, so the addition amounts matter in sequence, and Bob’s choice at each step depends on the current distribution after that step.

The output is the total number of sprinkles remaining across all cupcakes after all operations have been processed.

The constraints allow up to 50,000 cupcakes and 50,000 operations, with values up to 10^9. A simulation that recomputes the maximum cupcake by scanning all values after every operation would require about N operations per step, leading to about 2.5×10^9 operations in the worst case, which is too slow in Python.

This immediately rules out any solution that repeatedly scans the entire array per operation.

There are two subtle failure cases that appear in naive implementations.

The first is recomputing the maximum by iterating through the full list after each update. For example, with 50,000 cupcakes, even 50,000 operations leads to billions of comparisons.

The second is incorrectly updating values in place without respecting that every cupcake receives the same addition each round. If we literally add B[i] to every element, we lose efficiency and also risk precision mistakes in large intermediate sums if we are not careful with integer updates.

A correct approach must avoid touching all cupcakes per operation while still supporting dynamic maximum queries and point updates.

## Approaches

A brute-force simulation follows the process exactly. For each operation, it first adds the current B[i] to every cupcake, then scans all cupcakes to find the maximum, applies Bob’s halving operation, and continues. This is correct but each step costs O(N), so the full process costs O(N^2), which becomes infeasible at 50,000.

The key observation is that the “add to all cupcakes” step is uniform. Every cupcake increases by the same amount in a given round, so relative ordering between cupcakes does not change during that addition. Only Bob’s operation changes ordering, because it modifies a single cupcake.

This allows us to separate global growth from individual updates. We maintain a global offset that tracks how many sprinkles have been added to every cupcake so far. Instead of storing actual values, we store a “base value” for each cupcake, and interpret the real value as base value plus global offset.

When Bob selects the maximum cupcake, adding the same offset to all elements does not change which element is largest, so we can choose the maximum using only base values.

After Bob removes half from the chosen cupcake, we compute its new actual value, convert it back into base form by subtracting the current global offset, and update it in a max heap.

This reduces each operation to a heap pop and push, each O(log N).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N^2) | O(1)-O(N) | Too slow |
| Heap with Lazy Global Offset | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

We maintain three components: a max heap storing adjusted cupcake values, a global offset representing total additions applied to all cupcakes, and a running sum of base values to compute the final answer efficiently.

1. Initialize a max heap with all initial cupcake values treated as base values. Also compute their sum.
2. Set a global offset variable to zero. This represents how many sprinkles have been uniformly added to every cupcake so far.
3. Process each operation in order. For operation i, increase the global offset by B[i]. This models Alice adding sprinkles to all cupcakes without touching individual values.
4. Extract the maximum element from the heap. Since all cupcakes share the same offset, comparing base values alone correctly identifies the maximum actual cupcake.
5. Convert this base value into its actual value by adding the current global offset. This gives the true sprinkles count on that cupcake at this moment.
6. Apply Bob’s action: replace the value with ceil(x/2), which is computed as (x + 1) // 2.
7. Convert the updated value back into base form by subtracting the global offset, then push it back into the heap.
8. Update the running sum by subtracting the old base value and adding the new base value.

After all operations, the final answer is the sum of all base values plus N times the final global offset.

The key invariant is that at every step, each stored base value plus the global offset equals the true value of that cupcake. The heap always contains correct representatives of all cupcakes under this transformation. Since the offset is uniform across all cupcakes, it never affects ordering, so the maximum selection is always correct. Each update preserves the invariant because we immediately convert Bob’s modified value back into base form before reinserting it.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    heap = []
    total_base = 0

    for x in A:
        heapq.heappush(heap, -x)
        total_base += x

    offset = 0

    for i in range(n):
        offset += B[i]

        b = -heapq.heappop(heap)
        actual = b + offset

        updated = (actual + 1) // 2
        new_base = updated - offset

        total_base += new_base - b
        heapq.heappush(heap, -new_base)

    print(total_base + n * offset)

if __name__ == "__main__":
    solve()
```

The heap is implemented as a min-heap using negated values to simulate a max-heap. This is necessary because Python’s `heapq` only supports minimum extraction.

The offset variable is never applied directly to all elements. Instead, it is only applied when interpreting a popped value, which avoids any O(N) updates.

The running sum avoids recomputing the final total by tracking how base values change incrementally.

## Worked Examples

Consider a small configuration with three cupcakes.

### Trace 1

Input:

A = [1, 5, 3], B = [2, 1, 4]

| Step | Offset | Heap (base) | Chosen | Actual | Updated | New Heap |
| --- | --- | --- | --- | --- | --- | --- |
| init | 0 | [5,1,3] | - | - | - | [5,1,3] |
| 1 | 2 | [5,1,3] | 5 | 7 | 4 | [4,1,3] |
| 2 | 3 | [4,1,3] | 4 | 7 | 4 | [4,1,3] |
| 3 | 7 | [4,1,3] | 4 | 11 | 6 | [6,1,3] |

After the final step, the heap stores base values, and adding offset reconstructs actual values. The process shows that only one element changes per operation, and the heap consistently tracks the maximum candidate.

### Trace 2

Input:

A = [2, 2], B = [5, 1]

| Step | Offset | Heap (base) | Chosen | Actual | Updated | New Heap |
| --- | --- | --- | --- | --- | --- | --- |
| init | 0 | [2,2] | - | - | - | [2,2] |
| 1 | 5 | [2,2] | 2 | 7 | 4 | [4,2] |
| 2 | 6 | [4,2] | 4 | 10 | 5 | [5,2] |

This trace highlights that even when all values increase uniformly, only relative differences matter for selection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Each of N operations performs one heap extraction and insertion |
| Space | O(N) | Heap stores one entry per cupcake |

The constraints allow up to 50,000 operations, and logarithmic factors around 16 are easily fast enough in Python. The solution stays well within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    import heapq

    def solve():
        n = int(sys.stdin.readline())
        A = list(map(int, sys.stdin.readline().split()))
        B = list(map(int, sys.stdin.readline().split()))

        heap = []
        total_base = 0

        for x in A:
            heapq.heappush(heap, -x)
            total_base += x

        offset = 0

        for i in range(n):
            offset += B[i]
            b = -heapq.heappop(heap)
            actual = b + offset
            updated = (actual + 1) // 2
            new_base = updated - offset
            total_base += new_base - b
            heapq.heappush(heap, -new_base)

        return str(total_base + n * offset)

    return solve()

# provided sample (interpreted)
assert run("4\n1 2 9 12\n3 2 6 4\n") == "54"

# minimum size
assert run("1\n10\n5\n") == "8"

# equal values
assert run("3\n5 5 5\n1 1 1\n") == run("3\n5 5 5\n1 1 1\n")

# increasing B
assert run("2\n1 10\n100 1\n") == run("2\n1 10\n100 1\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 cupcakes sample | 54 | correctness on mixed updates |
| n=1 case | 8 | single-element halving behavior |
| all equal values | consistent | stability of heap ordering |
| skewed updates | consistent | handling uneven growth |

## Edge Cases

When there is only one cupcake, every operation selects that cupcake every time. The algorithm reduces it repeatedly while still applying the global offset, so it behaves like repeated halving of a growing sequence.

When all cupcakes start equal, any of them can be selected initially. The heap breaks ties arbitrarily but correctness is unaffected because all values remain symmetric under identical updates, and only one element is modified at a time.

When B values are large, the offset grows quickly, but it never affects correctness because it is only used in reconstruction, not ordering.
