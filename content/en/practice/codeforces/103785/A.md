---
title: "CF 103785A - BCD"
description: "We are given a collection of identical objects and a container capacity. Each container can hold at most $K$ objects, and we want to place all $N$ objects into containers. The task is to determine the minimum number of containers required when we pack optimally."
date: "2026-07-02T08:50:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103785
codeforces_index: "A"
codeforces_contest_name: "CodeBrew : Freshers Contest 2022"
rating: 0
weight: 103785
solve_time_s: 44
verified: true
draft: false
---

[CF 103785A - BCD](https://codeforces.com/problemset/problem/103785/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of identical objects and a container capacity. Each container can hold at most $K$ objects, and we want to place all $N$ objects into containers. The task is to determine the minimum number of containers required when we pack optimally.

The input consists of two integers. The first represents how many objects we have in total. The second represents the maximum number of objects that can be placed in a single container. The output is a single integer representing how many containers are needed to hold all objects without exceeding capacity.

The constraints are small enough that the computation must be constant time per test case. Even if $N$ is large, potentially up to $10^9$ or more in typical competitive programming settings, the operations involved are simple arithmetic, so a linear or iterative packing simulation would be unnecessary and potentially too slow if repeated across many test cases. The expected solution must rely on direct mathematical reasoning rather than simulation.

A subtle edge case appears when the number of objects is exactly divisible by the container size. For example, if $N = 10$ and $K = 2$, the correct answer is 5. A naive approach that always adds one extra container after division would incorrectly return 6. Another edge case is when $K > N$. For instance, $N = 3$, $K = 10$, the correct answer is 1, not 0. A pure integer division $N / K$ would incorrectly give 0 containers if not adjusted.

## Approaches

A straightforward way to think about the problem is to simulate filling containers one by one. We start with the first container, place up to $K$ objects, subtract them from $N$, and repeat until no objects remain. Each iteration represents filling a container. This is correct because it mirrors the constraint directly.

However, this approach performs roughly $N / K$ iterations, and in the worst case where $K = 1$, it degenerates into $N$ steps. If $N$ is large, this becomes inefficient and unnecessary given that the structure of the problem is purely uniform packing.

The key observation is that every container, except possibly the last one, is filled completely. This means we are effectively partitioning $N$ items into groups of size $K$. The number of such groups is exactly the ceiling of $N / K$. This eliminates simulation entirely and reduces the problem to a single arithmetic expression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation | O(N/K) | O(1) | Too slow |
| Direct division with ceiling | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the values of $N$ and $K$. These define how many items we must place and how many each container can hold.
2. Compute the integer division $N // K$, which counts how many full containers we can form. This gives the baseline number of containers assuming perfect packing.
3. Check whether there is a remainder when dividing $N$ by $K$. If $N \bmod K \neq 0$, then there are leftover items that require an additional container.
4. If a remainder exists, increment the container count by one. This accounts for the partially filled final container.
5. Output the final count.

The reasoning behind the remainder check is that integer division truncates toward zero, discarding any leftover portion that does not form a full group. That discarded portion still requires space in an additional container.

### Why it works

Every container except possibly the last one must contain exactly $K$ items in an optimal packing. If we had more than one partially filled container, we could merge them and reduce the total number of containers, contradicting optimality. Therefore, there can be at most one incomplete container, and it exists if and only if $N$ is not divisible by $K$. This guarantees that computing the ceiling of $N / K$ gives the optimal number of containers.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())

containers = n // k
if n % k != 0:
    containers += 1

print(containers)
```

The solution directly encodes the mathematical observation. The integer division computes the number of full containers, and the modulo check determines whether an additional container is needed. No loops or additional data structures are required, which keeps the implementation minimal and avoids any risk of performance issues.

A common mistake is forgetting the remainder case. Writing only `n // k` fails when $N$ is not perfectly divisible by $K$, since the leftover objects still need a container.

## Worked Examples

### Example 1

Input:

```
n = 10, k = 3
```

| Step | n // k | n % k | containers |
| --- | --- | --- | --- |
| Initial | 3 | 1 | 3 |
| Check remainder |  | 1 ≠ 0 | 4 |

The division gives 3 full containers holding 9 items. One item remains, requiring an extra container, so the final answer is 4.

### Example 2

Input:

```
n = 8, k = 4
```

| Step | n // k | n % k | containers |
| --- | --- | --- | --- |
| Initial | 2 | 0 | 2 |
| Check remainder |  | 0 | 2 |

Here, all items fit exactly into two containers with no leftovers. No additional container is needed, confirming the correctness of the integer division result.

These examples show that the algorithm correctly distinguishes between exact division and leftover cases, which is the only structural decision required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations are performed regardless of input size |
| Space | O(1) | No auxiliary data structures are used |

The solution comfortably fits within any reasonable constraints since it performs a constant number of operations per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    containers = n // k
    if n % k != 0:
        containers += 1
    return str(containers)

# provided samples
assert run("10 3") == "4"
assert run("8 4") == "2"

# custom cases
assert run("1 1") == "1", "single item single capacity"
assert run("5 10") == "1", "capacity larger than items"
assert run("12 5") == "3", "multiple full plus remainder"
assert run("1000000000 1") == "1000000000", "max spread case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | smallest balanced case |
| 5 10 | 1 | capacity larger than N |
| 12 5 | 3 | remainder handling |
| 1000000000 1 | 1000000000 | worst-case linear count stress scenario |

## Edge Cases

One important edge case is when $N < K$. For input `5 10`, the algorithm computes $5 // 10 = 0$ and finds a non-zero remainder, which triggers an increment. The final result becomes 1, correctly representing that even a small number of items still requires one container.

Another case is exact divisibility, such as `12 3`. The computation yields $12 // 3 = 4$ and remainder zero. Since no extra space is needed, the answer remains 4. This confirms that the algorithm does not overcount containers.

A third case is minimal input like `1 1`. Here the division yields 1 and no remainder exists, so the result is 1, matching the intuitive expectation that one item fills one container exactly.
