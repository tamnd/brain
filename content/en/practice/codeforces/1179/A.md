---
title: "CF 1179A - Valeriy and Deque"
description: "We are given a deque containing n integers. Valeriy repeatedly performs an operation where he removes the first two elements, compares them, and then reinserts them: the larger of the two goes to the front, and the smaller goes to the back."
date: "2026-06-12T01:35:59+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1179
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 569 (Div. 1)"
rating: 1500
weight: 1179
solve_time_s: 184
verified: true
draft: false
---

[CF 1179A - Valeriy and Deque](https://codeforces.com/problemset/problem/1179/A)

**Rating:** 1500  
**Tags:** data structures, implementation  
**Solve time:** 3m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a deque containing `n` integers. Valeriy repeatedly performs an operation where he removes the first two elements, compares them, and then reinserts them: the larger of the two goes to the front, and the smaller goes to the back. We are asked, for `q` queries, to determine which two elements are removed on the `m_j`-th operation for each query.

The key constraints are that `n` can be up to 10^5, and the number of queries `q` can be up to 3×10^5. Each query can ask about the `m_j`-th operation, where `m_j` can be as large as 10^18. This immediately rules out any solution that simulates each operation one by one for all queries, because even `O(n)` per query would be far too slow, and `O(m_j)` is impossible for large `m_j`.

Edge cases that can cause naive implementations to fail include: all elements equal, already sorted arrays, or queries for operations after the largest element has reached the front. For instance, if the deque is `[5, 5, 5]` and we ask for the 10th operation, a careless simulation might assume a change in order that never occurs.

## Approaches

The brute-force approach is simple. Start with the deque as given, and for each operation, pop the first two elements, compare them, and reinsert accordingly. Repeat this until the desired operation count is reached. This works for small `m_j`, but if `m_j` is on the order of 10^18, it is infeasible. Even for `n = 10^5` and `q = 10^5`, simulating operations one by one would require trillions of operations in the worst case.

The key insight is that the process has two phases. First, the maximum element in the deque will eventually reach the front. During this phase, each operation compares two numbers, moves the larger to the front, and the smaller to the back. Once the maximum is at the front, the first element never changes. After that, every operation just pairs the front element (the maximum) with the next element, sending the next element to the back. This second phase is completely periodic: it rotates the remaining `n-1` elements behind the maximum in a fixed cycle.

By observing this, we can precompute the first `n` operations until the maximum reaches the front. For queries within this range, we return the precomputed results. For queries beyond this, the answer can be computed using modular arithmetic on the cyclic sequence of the remaining elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m_j) | O(n) | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input, including the deque elements and the queries. Identify the maximum element in the deque.
2. Initialize a deque structure to simulate operations until the maximum reaches the front. Keep a list `first_phase` to store the pairs of elements removed in each operation.
3. While the front of the deque is not the maximum, pop the first two elements `A` and `B`. Append `(A, B)` to `first_phase`. Compare `A` and `B`, and push the larger to the front and the smaller to the back. This ensures that eventually the maximum will occupy the front.
4. Once the maximum is at the front, record the remaining elements behind it in order as `cycle`. These elements rotate behind the maximum after each operation.
5. For each query `m_j`, check if it falls within the precomputed `first_phase`. If so, simply output the stored pair. Otherwise, subtract the number of operations in `first_phase` to get the index in the cyclic phase. The element paired with the maximum is `cycle[(m_j - len(first_phase) - 1) % len(cycle)]`, and the maximum itself is always the other element.
6. Print the answers for all queries in the order they were given.

Why it works: The invariant is that once the maximum is at the front, it never moves. The remaining elements form a fixed sequence behind it, and each operation moves the next element to the back. This guarantees that every query can be answered using either the precomputed first-phase list or a simple modular lookup in the cyclic phase.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

n, q = map(int, input().split())
a = list(map(int, input().split()))
queries = [int(input()) for _ in range(q)]

d = deque(a)
first_phase = []

max_val = max(a)

while d[0] != max_val:
    A = d.popleft()
    B = d.popleft()
    first_phase.append((A, B))
    if A > B:
        d.appendleft(A)
        d.append(B)
    else:
        d.appendleft(B)
        d.append(A)

# Now the maximum is at the front
d.popleft()  # remove max for cycle
cycle = list(d)

answers = []
for m in queries:
    if m <= len(first_phase):
        answers.append(first_phase[m - 1])
    else:
        idx = (m - len(first_phase) - 1) % len(cycle)
        answers.append((max_val, cycle[idx]))

for a, b in answers:
    print(a, b)
```

The solution first simulates operations only until the maximum reaches the front, storing the result of each operation. After that, the deque is split into the maximum and a cycle of the remaining elements. For queries after the first phase, modular arithmetic is used to identify which element is paired with the maximum. This handles extremely large query numbers efficiently without simulating all operations.

## Worked Examples

Trace for sample input:

```
5 3
1 2 3 4 5
1
2
10
```

### First Phase Simulation

| Operation | Deque Front Two | Deque After Operation |
| --- | --- | --- |
| 1 | 1, 2 | 2, 3, 4, 5, 1 |
| 2 | 2, 3 | 3, 4, 5, 1, 2 |
| 3 | 3, 4 | 4, 5, 1, 2, 3 |
| 4 | 4, 5 | 5, 1, 2, 3, 4 |

Maximum `5` reached front, cycle is `[1,2,3,4]`.

### Query Handling

Query 1 → Operation 1 → `(1,2)` from first phase.

Query 2 → Operation 2 → `(2,3)` from first phase.

Query 10 → Operation 10 → 10 - 4 = 6 → index 6 % 4 = 2 → cycle[2] = 3 → answer `(5,3)`.

This trace shows the separation between first phase and cyclic phase, and that modular arithmetic gives the correct pairing with the maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Simulate at most `n` operations to bring max to front, then O(1) per query using modular arithmetic |
| Space | O(n) | Store deque and first-phase operations, and the cycle of length at most n-1 |

This is efficient enough for the largest inputs because `n` ≤ 10^5 and `q` ≤ 3×10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline
    
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    queries = [int(input()) for _ in range(q)]
    
    d = deque(a)
    first_phase = []

    max_val = max(a)
    while d[0] != max_val:
        A = d.popleft()
        B = d.popleft()
        first_phase.append((A, B))
        if A > B:
            d.appendleft(A)
            d.append(B)
        else:
            d.appendleft(B)
            d.append(A)
    
    d.popleft()
    cycle = list(d)
    
    answers = []
    for m in queries:
        if m <= len(first_phase):
            answers.append(first_phase[m - 1])
        else:
            idx = (m - len(first_phase) - 1) % len(cycle)
            answers.append((max_val, cycle[idx]))
    
    return "\n".join(f"{x[0]} {x[1]}" for x in answers)

# Provided samples
assert run("5 3\n1 2 3 4 5\n1\n2\n10\n") == "1 2\n2 3\n5 2"

# Minimum input
assert run("2 1\n0 0\n1\n") == "0 0"

# Maximum element at front initially
assert run("3 2\n9 1 2\n1\n4\n") == "9 1\n9 2"

# All equal elements
assert run("4 3\n7 7 7 7\n1\n5\n10\n") == "7 7\n7 7\n7 7"

# Large query beyond first phase
assert run("5 2\n1 2
```
