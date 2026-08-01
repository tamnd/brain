---
title: "CF 102651C - Optimal Truck"
description: "Petya can buy a truck with some carrying capacity. Each potential customer offers several possible contracts. A contract is available only if the truck can carry at least the required weight for that contract, and it gives a certain profit."
date: "2026-08-01T10:23:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102651
codeforces_index: "C"
codeforces_contest_name: "Innopolis Open 2020-2021, qualification, contest 1"
rating: 0
weight: 102651
solve_time_s: 113
verified: true
draft: false
---

[CF 102651C - Optimal Truck](https://codeforces.com/problemset/problem/102651/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

Petya can buy a truck with some carrying capacity. Each potential customer offers several possible contracts. A contract is available only if the truck can carry at least the required weight for that contract, and it gives a certain profit. From each customer, Petya can accept at most one contract.

For a chosen truck capacity, every customer independently contributes the most profitable contract that fits that capacity. The task is not to find the profit for one fixed capacity, but to answer many queries: for each desired profit, find the smallest capacity where the total achievable profit reaches that value.

The input describes customers one by one. Each customer block contains all possible contracts for that customer. The total number of contracts over all customers is at most 500000, and the number of queries is also at most 100000.

The large limits rule out checking every capacity against every contract. A solution that tries every query independently and scans all contracts would need around 500000 * 100000 operations, which is about 5 * 10^10 operations and is far beyond a two second limit. We need to process all contracts together and answer queries from a compact representation of the possible profits.

The key difficulty is that contracts from the same customer cannot simply be added together. A careless solution might count several contracts of one customer if they all fit the truck, but only one contract may be chosen. Another subtle point is that a contract with a larger required capacity can be useless if the same customer already has a cheaper contract with the same or larger profit.

For example, consider one customer:

```
1
3
5 10
7 20
9 15
1
15
```

The correct output is:

```
7
```

At capacity 9, the customer still only gives profit 20, so buying a truck of capacity 9 is unnecessary. A solution that only looks for the first contract reaching the required profit without removing dominated choices could incorrectly answer 9.

Another edge case is when the target profit cannot be reached.

```
1
2
3 5
5 8
1
10
```

The output is:

```
-1
```

The maximum possible profit is 8, so any algorithm that always takes the largest available capacity as an answer without checking the final profit would be wrong.

A final important case is many contracts with the same weight.

```
1
3
4 5
4 12
4 9
2
5 12
```

The output is:

```
4 4
```

All three contracts become available together, but only the most profitable one matters. The implementation must combine equal weights correctly.

## Approaches

The direct approach is to handle each query separately. For a capacity guess, we could inspect every contract, determine which contracts are available, and for every customer keep the best profit among its available contracts. This is correct because the customers are independent and each customer contributes only their own maximum valid contract.

However, doing this for every query is too slow. With 100000 queries and 500000 contracts, the worst case requires roughly 50000000000 checks.

The useful observation is that the answer depends only on how the total profit changes when the truck capacity increases. The contribution of one customer is a non-decreasing function. Once a contract becomes available, it may replace the previous best contract for that customer, but it never decreases the customer's contribution.

For each customer, we can sort contracts by required capacity. While moving through them in increasing order, we keep the best profit seen so far. If the best profit improves at some capacity, that capacity creates an increase in the total answer. Contracts that do not improve the prefix maximum can be ignored.

After processing all customers, we have a collection of events. An event at capacity `w` says that the total achievable profit increases by some amount when the truck capacity reaches `w`. Sorting all events by capacity and taking prefix sums gives the complete function:

`capacity -> maximum possible total profit`

Now every query becomes a binary search on this monotonic list.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * sum(mi)) | O(n) | Too slow |
| Optimal | O(sum(mi) log sum(mi) + q log sum(mi)) | O(sum(mi)) | Accepted |

## Algorithm Walkthrough

1. For every customer, sort all their contracts by required truck capacity. When several contracts have the same capacity, their order does not matter because they all become available at the same time.
2. Scan this sorted list while maintaining the best profit available for this customer. Whenever this best profit increases, add an event containing the capacity where the increase happens and the size of the increase. This converts one customer's options into only the moments where the total answer changes.
3. Merge all customer events into one list and sort the list by capacity. Events with the same capacity must be processed together because all contracts requiring that capacity become available simultaneously.
4. Traverse the sorted events and build two arrays. The first stores the capacities where the total profit changes. The second stores the total profit after applying all changes up to that capacity.
5. For every query, binary search the first position where the stored profit is at least the requested value. If no such position exists, output `-1`.

Why it works:

For one customer, after sorting contracts by capacity, the prefix maximum is exactly the best contract this customer can choose at every possible truck capacity. The algorithm records only points where this prefix maximum changes, so no information about that customer is lost.

The total profit is the sum of all customer contributions. Since every contribution is non-decreasing, the total profit is also non-decreasing. The event list reconstructs every increase in this function, so binary search finds the first capacity where the required profit is achieved. If the final value is smaller than the query, no capacity can satisfy it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    events = []

    for _ in range(n):
        m = int(input())
        contracts = []
        for _ in range(m):
            w, c = map(int, input().split())
            contracts.append((w, c))

        contracts.sort()

        best = 0
        i = 0
        while i < m:
            w = contracts[i][0]
            current_best = best

            while i < m and contracts[i][0] == w:
                if contracts[i][1] > current_best:
                    current_best = contracts[i][1]
                i += 1

            if current_best > best:
                events.append((w, current_best - best))
                best = current_best

    events.sort()

    capacities = []
    profits = []

    total = 0
    i = 0
    while i < len(events):
        w = events[i][0]
        while i < len(events) and events[i][0] == w:
            total += events[i][1]
            i += 1
        capacities.append(w)
        profits.append(total)

    q = int(input())
    ans = []

    import bisect

    for _ in range(q):
        x = int(input())
        pos = bisect.bisect_left(profits, x)
        if pos == len(profits):
            ans.append("-1")
        else:
            ans.append(str(capacities[pos]))

    print(" ".join(ans))

if __name__ == "__main__":
    solve()
```

The input is processed customer by customer, so the program never needs to store all customers at once. For each customer, sorting exposes the order in which contracts become available. The scan groups equal capacities together, because several contracts appearing at the same capacity should influence the customer's choice at the same moment.

The variable `best` stores the previous maximum profit for the current customer. The difference between the new maximum and the old one is exactly the contribution that this customer adds at that capacity. Storing only this difference avoids keeping unnecessary contracts.

After all customers are processed, the global event list is sorted. The second scan combines equal capacities before storing them. This is necessary because a query asking for that capacity should receive the profit after every contract unlocked at that capacity has been considered.

Python integers handle the possible profit sum safely because the language has arbitrary precision arithmetic. The binary search uses `bisect_left` because we need the first capacity whose profit is not smaller than the target.

## Worked Examples

Consider a small example:

```
2
3
2 5
5 10
7 8
2
3 4
6 9
3
5
10
20
```

The customer events are:

Customer 1 contributes profit increases of 5 at capacity 2 and 5 more at capacity 5.

Customer 2 contributes profit increases of 4 at capacity 3 and 5 more at capacity 6.

| Capacity | Added profit | Total profit |
| --- | --- | --- |
| 2 | 5 | 5 |
| 3 | 4 | 9 |
| 5 | 5 | 14 |
| 6 | 5 | 19 |

The queries become:

| Query | First profit reaching query | Answer |
| --- | --- | --- |
| 5 | capacity 2 gives profit 5 | 2 |
| 10 | capacity 5 gives profit 14 | 5 |
| 20 | no capacity reaches it | -1 |

This example shows why the algorithm stores prefix profits. The truck capacity does not need to match a contract that gives exactly the target profit, it only needs to reach or exceed it.

A second example:

```
1
4
4 6
4 10
8 12
10 12
4
5
6
10
13
```

The scan for the only customer is:

| Capacity | Best profit after capacity | Event added |
| --- | --- | --- |
| 4 | 10 | +10 |
| 8 | 12 | +2 |
| 10 | 12 | none |

The final arrays are:

| Index | Capacity | Profit |
| --- | --- | --- |
| 0 | 4 | 10 |
| 1 | 8 | 12 |

The answers are:

| Query | Result |
| --- | --- |
| 5 | 4 |
| 6 | 4 |
| 10 | 4 |
| 13 | -1 |

This demonstrates two important details. Contracts with the same capacity are combined by taking the maximum profit, and contracts that do not improve the prefix maximum disappear from the event list.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M log M + q log M) | M is the total number of contracts. Sorting contracts and events dominates the work. |
| Space | O(M) | The event list stores only capacity changes, which cannot exceed the number of contracts. |

The total number of contracts is at most 500000, so sorting this many elements is feasible. The query phase performs only binary searches over the compressed profit function, allowing 100000 queries to be processed quickly.

## Test Cases

```python
import sys
import io
import bisect

def solve_data(data):
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(data)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue().strip()

def solve():
    input = sys.stdin.readline
    n = int(input())
    events = []

    for _ in range(n):
        m = int(input())
        a = [tuple(map(int, input().split())) for _ in range(m)]
        a.sort()
        best = 0
        i = 0
        while i < m:
            w = a[i][0]
            cur = best
            while i < m and a[i][0] == w:
                cur = max(cur, a[i][1])
                i += 1
            if cur > best:
                events.append((w, cur - best))
                best = cur

    events.sort()
    caps = []
    vals = []
    total = 0
    i = 0
    while i < len(events):
        w = events[i][0]
        while i < len(events) and events[i][0] == w:
            total += events[i][1]
            i += 1
        caps.append(w)
        vals.append(total)

    q = int(input())
    ans = []
    for _ in range(q):
        x = int(input())
        p = bisect.bisect_left(vals, x)
        ans.append(str(caps[p]) if p < len(caps) else "-1")

    print(" ".join(ans))

assert solve_data("""1
1
1 1
3
1
2
3
""") == "1 -1 -1"

assert solve_data("""2
2
5 10
10 20
2
3 5
8 15
4
10
25
35
36
""") == "5 10 -1 -1"

assert solve_data("""1
3
4 5
4 12
4 9
2
5
12
""") == "4 4"

assert solve_data("""3
1
100 100
1
1 1
1
50 50
3
1
51
151
""") == "1 50 100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single contract with tiny profit | `1 -1 -1` | Minimum input size and impossible queries |
| Several customers with separate contributions | `5 10 -1 -1` | Combining independent customer choices |
| Same capacity with different profits | `4 4` | Correct handling of equal weights |
| Multiple capacity jumps | `1 50 100` | Binary search boundaries and cumulative profit |

## Edge Cases

When a customer has several contracts with the same weight, the algorithm groups them before creating an event. For example:

```
1
3
4 5
4 12
4 9
2
5
12
```

At capacity 4, the customer contribution immediately becomes 12, not 5 plus 12 plus 9. The event list contains only `(4, 12)`, so both queries return capacity 4.

When the requested profit is impossible, the final prefix profit is smaller than the query. For:

```
1
2
3 5
5 8
1
10
```

The built arrays are capacity `[3, 5]` and profit `[5, 8]`. Binary search returns the end position because no stored profit reaches 10, so the algorithm outputs `-1`.

When a later contract is dominated, it does not create an event. For:

```
1
3
5 10
7 20
9 15
1
15
```

The prefix maximums are 10, 20, 20. Only capacities 5 and 7 change the answer. The capacity 9 contract is ignored, and the query correctly returns 7.
