---
title: "CF 1468C - Berpizza"
description: "We process a sequence of events in a pizzeria. Every time a query of type 1 m appears, a new customer arrives. Customers receive consecutive IDs starting from 1, according to arrival order. Each customer also has a predicted spending value m."
date: "2026-06-11T01:25:11+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1468
codeforces_index: "C"
codeforces_contest_name: "2020-2021 ICPC, NERC, Southern and Volga Russian Regional Contest (Online Mirror, ICPC Rules)"
rating: 1400
weight: 1468
solve_time_s: 367
verified: true
draft: false
---

[CF 1468C - Berpizza](https://codeforces.com/problemset/problem/1468/C)

**Rating:** 1400  
**Tags:** data structures, implementation  
**Solve time:** 6m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We process a sequence of events in a pizzeria.

Every time a query of type `1 m` appears, a new customer arrives. Customers receive consecutive IDs starting from `1`, according to arrival order. Each customer also has a predicted spending value `m`.

A query of type `2` asks us to serve the earliest customer who has not been served yet.

A query of type `3` asks us to serve the currently unserved customer with maximum predicted spending. If several customers have the same spending value, the earliest arrival among them must be chosen.

Each customer can be served exactly once. For every query of type `2` or `3`, we must output the ID of the served customer.

The constraint `q ≤ 5 · 10^5` immediately rules out scanning all active customers whenever a service query appears. In the worst case there may be hundreds of thousands of customers waiting simultaneously. An `O(q)` scan per operation would lead to roughly `O(q²)` work, which is far too large.

We need data structures that can return both:

1. The earliest unserved customer.
2. The highest-priority unserved customer.

Each operation should run in logarithmic time or better.

A subtle issue is that the same customer can be selected by either waiter. Once served, that customer must disappear from both selection systems. Forgetting this creates duplicate answers.

Consider:

```
1 10
1 20
3
2
```

Customer `2` is served first by Polycarp. The answer to the second query must be customer `1`, not customer `2` again.

Another subtle case appears when several customers have equal spending.

```
1 10
1 10
3
```

The answer must be customer `1`, because ties are broken by arrival order.

## Approaches

A brute-force solution stores all active customers in a list.

For query type `2`, it scans forward until it finds the first unserved customer.

For query type `3`, it scans all active customers to find the largest spending value and then applies the tie-break rule.

This approach is correct because it directly follows the problem definition. Unfortunately, a single query can require examining `O(q)` customers. With up to `5 · 10^5` operations, the worst-case complexity becomes `O(q²)`.

The key observation is that the two waiters use two different orderings.

Monocarp always wants the smallest arrival index.

Polycarp always wants the largest spending value, with arrival order as a secondary key.

Instead of maintaining one complicated structure, we maintain two independent views of the same customers.

A queue-like structure gives access to the earliest arrival.

A priority queue gives access to the largest spending value.

The remaining challenge is synchronization. When one waiter serves a customer, that customer still exists inside the other structure. Removing arbitrary elements from heaps or queues is expensive.

The standard solution is lazy deletion. We keep a boolean array indicating whether a customer has already been served. Whenever a structure returns a customer, we repeatedly discard entries that are already marked as served.

This turns both operations into efficient logarithmic-time queries.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(q²) | O(q) | Too slow |
| Two structures + lazy deletion | O(q log q) | O(q) | Accepted |

## Algorithm Walkthrough

1. Assign every arriving customer a unique ID.

2. Store each arriving customer in arrival order inside an array or queue structure.

3. Also insert the customer into a max-heap keyed by `(spending, arrival order)`.

4. Maintain a boolean array `served[id]`.

5. For query type `2`, advance a pointer through arrival order until it reaches an unserved customer. Output that ID and mark it served.

6. For query type `3`, repeatedly remove heap entries whose customer has already been served. The first remaining entry is the valid answer. Output its ID and mark it served.

7. Continue processing all queries.

### Why it works

The arrival pointer always moves from left to right and skips exactly those customers already marked as served. Consequently, the first unserved customer it reaches is precisely the customer Monocarp would choose.

The heap always contains every customer that has ever arrived. Lazy deletion removes obsolete entries only when they reach the top. After all served customers at the top are discarded, the remaining top element is the unserved customer with maximum spending. Because arrival ID is included in the heap key, ties are resolved toward earlier arrivals exactly as required.

Since every customer is marked served at most once, neither waiter can serve the same customer twice.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    q = int(input())

    arrivals = []
    served = [False] * (q + 5)

    heap = []

    next_id = 1
    front = 0

    ans = []

    for _ in range(q):
        parts = input().split()

        if parts[0] == '1':
            m = int(parts[1])

            arrivals.append(next_id)

            heapq.heappush(heap, (-m, next_id))

            next_id += 1

        elif parts[0] == '2':
            while served[arrivals[front]]:
                front += 1

            cid = arrivals[front]
            served[cid] = True
            ans.append(str(cid))

        else:
            while heap and served[heap[0][1]]:
                heapq.heappop(heap)

            _, cid = heapq.heappop(heap)

            served[cid] = True
            ans.append(str(cid))

    print(" ".join(ans))

solve()
```

The `arrivals` array stores customers in the exact order they entered the restaurant. The variable `front` acts like a queue head.

The heap stores pairs `(-money, id)`. Python provides a min-heap, so negating the spending value turns it into a max-heap. Using the customer ID as the second component automatically enforces the required tie-break rule because smaller IDs correspond to earlier arrivals.

The `served` array is the key to lazy deletion. Whenever a customer is served by one waiter, we mark that customer. The other data structure eventually encounters the stale record and discards it.

No customer is ever removed from the middle of either structure, which keeps all operations efficient.

## Worked Example

### Sample Input

```
8
1 8
1 10
1 6
3
2
1 9
2
3
```

| Step | Query | Queue Order | Heap Best | Output |
|---|---|---|---|---|
| 1 | 1 8 | 1 | 1 | |
| 2 | 1 10 | 1,2 | 2 | |
| 3 | 1 6 | 1,2,3 | 2 | |
| 4 | 3 | 1,2,3 | 2 | 2 |
| 5 | 2 | 1,2,3 | 1 | 1 |
| 6 | 1 9 | 1,2,3,4 | 4 | |
| 7 | 2 | 1,2,3,4 | 4 | 3 |
| 8 | 3 | 1,2,3,4 | 4 | 4 |

The outputs are:

```
2 1 3 4
```

This example demonstrates lazy deletion. After customer `2` is served by Polycarp, customer `2` still remains inside the arrival structure. The served marker prevents that stale record from being chosen again.

### Tie-Break Example

```
1 10
1 10
3
```

| Customer | Spending | Arrival |
|---|---|---|
| 1 | 10 | First |
| 2 | 10 | Second |

Both spending values are equal. The heap compares IDs next, so customer `1` is selected.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(q log q) | Each insertion and heap removal costs O(log q) |
| Space | O(q) | All customers are stored once |

Each customer enters the heap exactly once and leaves it at most once. The arrival pointer only moves forward. The total work comfortably fits inside the limits for `5 · 10^5` operations.

## Test Cases

```python
# sample

# input:
# 8
# 1 8
# 1 10
# 1 6
# 3
# 2
# 1 9
# 2
# 3
#
# output:
# 2 1 3 4

# earliest customer after highest-value service
# expected: 2 1

# equal spending values
# 1 10
# 1 10
# 3
# expected: 1

# repeated lazy deletions
# 1 5
# 1 10
# 1 7
# 3
# 3
# 2
# expected: 2 3 1

# single customer
# 1 100
# 2
# expected: 1
```

| Test input | Expected output | What it validates |
|---|---|---|
| Sample case | 2 1 3 4 | Normal mixed operations |
| Equal priorities | 1 | Tie-breaking by arrival |
| Multiple type 3 queries | 2 3 1 | Heap ordering correctness |
| Single customer | 1 | Minimum nontrivial case |

## Edge Cases

Consider:

```
1 10
1 20
3
2
```

Customer `2` is served first. When Monocarp serves next, the arrival pointer skips customer `2` because `served[2] = True` and correctly returns customer `1`.

Consider:

```
1 10
1 10
3
```

Both customers have equal spending. The heap stores `(-10, 1)` and `(-10, 2)`. Lexicographic tuple comparison makes customer `1` the winner.

Consider:

```
1 5
1 8
2
3
```

Customer `1` is served by Monocarp. The heap still contains customer `1`, but lazy deletion removes that stale entry before selecting customer `2`. This guarantees that no customer is served twice.
:::
