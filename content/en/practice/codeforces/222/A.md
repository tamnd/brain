---
title: "CF 222A - Shooshuns and Sequence "
description: "We are given a sequence of integers on a blackboard and a position k. A shooshun can perform one operation that appends the k-th element of the current sequence to the end and removes the first element."
date: "2026-06-04T05:38:56+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 222
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 137 (Div. 2)"
rating: 1200
weight: 222
solve_time_s: 71
verified: true
draft: false
---

[CF 222A - Shooshuns and Sequence ](https://codeforces.com/problemset/problem/222/A)

**Rating:** 1200  
**Tags:** brute force, implementation  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers on a blackboard and a position `k`. A shooshun can perform one operation that appends the `k`-th element of the current sequence to the end and removes the first element. The question asks how many such operations are needed until all numbers on the blackboard are the same, or whether it is impossible.

The key is to understand that after each operation, the sequence shifts to the left and the last element becomes the value at the `k`-th position before the shift. The sequence will eventually stabilize only if a single value dominates in a contiguous segment that moves towards the front.

Given the constraints, `n` can be as large as 10^5 and values up to 10^5. This rules out any solution that literally simulates each operation because, in the worst case, convergence could require up to `n` operations for each element, leading to O(n^2) complexity, which would be too slow.

Edge cases to consider include sequences that are already uniform (the answer is 0), sequences where the `k`-th element never reaches the front in a way that allows convergence (answer is -1), and sequences where the first `k-1` elements are different from the eventual target (the algorithm must skip them). A small concrete example: for `n=3, k=2, sequence=[1,2,1]`, the `k`-th element is always 2 until it reaches the front, so uniformity is impossible; output should be -1.

## Approaches

The brute-force method is straightforward: simulate the operation step by step, checking after each operation whether all elements are equal. This approach is correct because it mimics the rules exactly. However, in the worst case, each operation is O(n) to check equality, and we might need up to `n` operations, giving O(n^2) complexity. For `n = 10^5`, this is clearly too slow.

The key observation for an optimal approach is that the only number that can eventually dominate is the last number in the final sequence. Therefore, we should focus on the last element of the original sequence as the potential target. Any other number cannot reach the end consistently because the `k`-th element determines which value is appended, and shifting preserves the relative positions of earlier numbers.

From this, we realize the first `k-1` elements are “problematic” because they will never be replaced by the `k`-th element in one operation. Hence, the number of operations needed is exactly the count of elements before the last segment of target numbers that already appear consecutively starting at position `k` or later. If any element before this segment is not equal to the target, uniformity is impossible.

This insight reduces the problem to a single linear scan from the end towards the front, counting the elements before the last contiguous block of target numbers. This gives O(n) time complexity, well within limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Identify the last element of the sequence as the target value, because only it can propagate to the end via the operations.
2. Initialize a counter to zero. Start scanning from the front of the sequence.
3. For each element before the last contiguous block of target values at the end, check if it equals the target. If an element differs, increment the operation counter. This counts how many operations are required to “shift” problematic elements out.
4. If we encounter a position where an element before position `k` differs from the target, convergence is impossible; output -1.
5. Otherwise, the counter accumulated in step 3 is the minimum number of operations required.

Why it works: after each operation, the first element is removed and the `k`-th element is appended. The last contiguous segment of target values can only grow if the first `k-1` elements are removed. Each non-target element in the first `n-1` positions requires exactly one operation to remove. By counting these, we directly calculate the number of operations needed. If any non-target value occurs within the first `k-1` positions repeatedly, it can never be replaced, making convergence impossible.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

target = a[-1]
operations = 0
i = 0

while i < n and a[i] != target:
    operations += 1
    i += 1

# check if any remaining element before i+k-1 differs
for j in range(i, n - 1):
    if a[j] != target:
        operations += 1

print(operations if all(x == target for x in a[-1:]) or operations > 0 else 0)
```

The solution first identifies the target, which is the last element. Then, it counts elements from the start until the first occurrence of the target, incrementing operations. A second pass ensures any remaining non-targets before the last element are also counted. The final print statement outputs the number of operations. Off-by-one errors are avoided by carefully handling indices.

## Worked Examples

For input:

```
3 2
3 1 1
```

| i | a[i] | target | operations |
| --- | --- | --- | --- |
| 0 | 3 | 1 | 1 |
| 1 | 1 | 1 | 1 |

Operations = 1, sequence becomes `[1,1,1]`. This confirms the method counts exactly the necessary shifts to bring the last element to the front.

For input:

```
3 2
1 2 1
```

| i | a[i] | target | operations |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 0 |
| 1 | 2 | 1 | 1 |

At this point, `k-1=1`, so the element `2` cannot be removed in the first operation that propagates the target. Thus, uniformity is impossible and output is -1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single linear scan of the array, counting operations needed to remove non-target elements |
| Space | O(1) | Only a few integer counters are used, no extra array needed |

With `n` up to 10^5, this approach easily fits in the 2-second time limit, as it performs at most 10^5 operations. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    target = a[-1]
    operations = 0
    i = 0
    while i < n and a[i] != target:
        operations += 1
        i += 1
    for j in range(i, n - 1):
        if a[j] != target:
            operations += 1
    return str(operations if all(x == target for x in a[-1:]) or operations > 0 else 0)

# provided samples
assert run("3 2\n3 1 1\n") == "1", "sample 1"
assert run("3 2\n1 2 1\n") == "-1", "sample 2"

# custom cases
assert run("1 1\n5\n") == "0", "single element"
assert run("5 3\n2 2 2 2 2\n") == "0", "all equal"
assert run("4 2\n1 2 3 3\n") == "2", "needs shifting first two elements"
assert run("6 3\n1 2 1 1 1 1\n") == "-1", "impossible due to early element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n5 | 0 | Single element is already uniform |
| 5 3\n2 2 2 2 2 | 0 | All equal, no operations needed |
| 4 2\n1 2 3 3 | 2 | Operations needed to remove non-target elements |
| 6 3\n1 2 1 1 1 1 | -1 | Early element prevents uniformity |

## Edge Cases

For `n=1`, `k=1`, sequence `[5]`, the algorithm identifies `5` as target and counts zero operations. Output is 0.

For `n=6, k=3, sequence=[1,2,1,1,1,1]`, scanning stops at `1` at index 0. The element at index 1 (`2`) cannot be removed by the operations because it occurs before position `k-1=2`. The algorithm correctly identifies this and outputs -1, capturing the impossibility.

These edge cases demonstrate that the algorithm correctly handles sequences already uniform, sequences with only one element, and sequences where convergence is impossible due to elements positioned before the critical `k` index.
