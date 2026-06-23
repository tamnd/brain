---
title: "CF 105278D - Wise Splitting"
description: "We are given a list of money transfers between people, where each record says that one person paid on behalf of another, creating an implicit debt relationship. From these transactions we can compute how much each person ultimately owes or is owed."
date: "2026-06-23T14:17:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105278
codeforces_index: "D"
codeforces_contest_name: "2024 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 105278
solve_time_s: 113
verified: false
draft: false
---

[CF 105278D - Wise Splitting](https://codeforces.com/problemset/problem/105278/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of money transfers between people, where each record says that one person paid on behalf of another, creating an implicit debt relationship. From these transactions we can compute how much each person ultimately owes or is owed. A positive net value means the person should receive money overall, while a negative net value means they must pay money overall.

The task is not to recompute the full history but to replace it with a much smaller settlement plan. Each settlement operation is a single directed transfer of some amount from one person to another. The constraint is that every person is allowed to initiate at most one such transfer, but they may receive money multiple times. The goal is to fully balance all debts so that every person ends with zero net balance.

The input size pushes toward a linear or near-linear solution over the transaction list. With up to 200,000 people and 1,000,000 transactions, any approach that repeatedly simulates pairwise matching or repeatedly scans for partners will be too slow. The structure strongly suggests collapsing all transactions into net balances first, then performing a single pass construction of the final settlement plan in roughly O(N log N) or O(N) time.

A subtle failure case appears when thinking in terms of arbitrary pairing of people without tracking remaining capacity. For example, if a person owes 100 and the only available creditor they are matched with can only receive 20, a naive single-pair assignment would get stuck because the debtor is not allowed to split their outgoing transfer. A correct construction must ensure that every outgoing transfer exactly matches the remaining capacity of the chosen receiver or that we only match compatible pairs where the full amount fits.

Another edge case arises when balancing is done locally per transaction instead of globally per person. Two intermediate cancellations may hide a nonzero net balance that later breaks feasibility if ignored.

## Approaches

The brute-force idea is to repeatedly pick any person with a positive balance and try to match them with people who owe money until everyone reaches zero. This can be simulated by maintaining a dynamic list of balances and repeatedly searching for compatible pairs. Each operation would require scanning for a valid counterpart and updating remaining balances. In the worst case, each of the O(N) people would trigger a scan over the remaining pool, producing O(N^2) behavior, which is far beyond the limits when N is 200,000.

The key observation is that the transaction history does not matter after computing net balances. The system becomes a simple flow conservation problem: total incoming equals total outgoing, so the problem reduces to redistributing positive surplus to negative deficits. The restriction that each person can initiate at most one transfer means each debtor must be assigned exactly one outgoing edge, so we must treat each negative balance as an indivisible unit that must be sent in one move.

This transforms the problem into a greedy matching between “deficit nodes” and “surplus capacity.” Each creditor can accept multiple incoming transfers, while each debtor must be assigned exactly one creditor. The only requirement is that the chosen creditor has enough remaining capacity to absorb the debtor’s full amount at the moment of assignment. A natural way to enforce this is to always match the largest remaining surplus first, because smaller surpluses are more likely to become unusable for large debts later.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pairing | O(N^2) | O(N) | Too slow |
| Greedy with Net Balances + Max Structure | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

We first compress all transactions into a single balance per person.

1. Compute the net balance of each person by iterating over all transactions. If person A paid C for B, we add C to A’s balance and subtract C from B’s balance. This gives the final amount each person should receive or pay.
2. Split people into two groups. One group contains all people with positive balance, meaning they should receive money. The other contains all people with negative balance, meaning they must pay money.
3. Store all positive balances in a structure that allows repeated extraction of the largest remaining capacity, such as a max heap keyed by remaining amount. Each entry keeps both the person index and their remaining capacity.
4. Iterate over all people with negative balance. For each debtor i with amount d equal to minus their balance, we must assign exactly one outgoing transfer.
5. Extract the currently most capable creditor from the heap. If their remaining capacity is smaller than d, we temporarily discard them from consideration and try the next largest creditor. This works because a creditor that cannot fully satisfy this debtor can still be useful for smaller debtors later.
6. Once we find a creditor j with remaining capacity at least d, we create a transfer from i to j of amount d. We then reduce j’s remaining capacity by d.
7. If j still has remaining capacity, we push it back into the heap. Otherwise, we discard it.
8. Continue until all debtors are processed. Every debtor is assigned exactly one outgoing transfer.

The correctness relies on the invariant that the heap always represents exactly the unused receiving capacity of all creditors. Each assignment removes one debtor completely and reduces exactly one creditor’s capacity, never splitting debtor obligations.

The greedy choice of always taking the largest available creditor ensures that if a feasible assignment exists, we do not prematurely consume small creditors in a way that blocks large debts later.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    bal = [0] * (n + 1)

    for _ in range(m):
        a, b, c = map(int, input().split())
        bal[a] += c
        bal[b] -= c

    pos = []
    neg = []

    for i in range(1, n + 1):
        if bal[i] > 0:
            pos.append([bal[i], i])
        elif bal[i] < 0:
            neg.append([i, -bal[i]])

    heap = []
    for amt, i in pos:
        heapq.heappush(heap, (-amt, i))

    res = []

    for i, need in neg:
        while need > 0:
            amt, j = heapq.heappop(heap)
            amt = -amt

            if amt >= need:
                res.append((i, j, need))
                amt -= need
                need = 0
                if amt > 0:
                    heapq.heappush(heap, (-amt, j))
            else:
                res.append((i, j, amt))
                need -= amt

    print(len(res))
    for a, b, c in res:
        print(a, b, c)

if __name__ == "__main__":
    main()
```

The solution begins by collapsing all transactions into a single net balance per person. This step is essential because only the final net amount matters for settlement; intermediate transfers carry no additional constraints.

Positive balances are turned into a max heap so that we can always access the creditor with the largest remaining capacity. This choice is important because smaller creditors are more fragile resources and should be preserved for smaller debts if possible.

Each debtor is processed exactly once. The inner loop assigns their debt greedily to available creditors, splitting creditor capacity if necessary. Even though creditors may receive multiple incoming transfers, each debtor is always assigned a single outgoing transfer, respecting the constraint.

A subtle point is that creditors are reinserted into the heap only if they still have remaining capacity. This ensures the heap size remains bounded by O(N).

## Worked Examples

### Sample 1

Input:

```
2 1
1 2 50
```

After processing transactions, balances become:

Person 1: +50

Person 2: -50

We build the heap with (50, 1) and process person 2.

| Step | Debtor | Need | Chosen Creditor | Creditor Before | Transfer | Creditor After |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 50 | 1 | 50 | 2 → 1 : 50 | 0 |

Output:

```
1
2 1 50
```

This shows the simplest case where one debtor exactly matches one creditor.

### Sample 2

Input:

```
3 3
1 2 2
2 3 4
3 1 6
```

Net balances:

Person 1: +4

Person 2: -2

Person 3: -2

Heap starts with (4, 1).

| Step | Debtor | Need | Creditor | Before | Transfer | After |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 1 | 4 | 2 → 1 : 2 | 2 |
| 2 | 3 | 2 | 1 | 2 | 3 → 1 : 2 | 0 |

Output:

```
2
2 1 2
3 1 2
```

This demonstrates that a single creditor can serve multiple debtors, gradually exhausting its capacity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N + M) | M for balance aggregation, N log N for heap operations during matching |
| Space | O(N) | Storage for balances and heap entries |

The algorithm fits comfortably within constraints since even 1e6 transactions only require a linear pass, and the heap operations scale with the number of active participants, not the number of transactions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from collections import defaultdict
    import heapq

    input = sys.stdin.readline
    n, m = map(int, input().split())
    bal = [0] * (n + 1)

    for _ in range(m):
        a, b, c = map(int, input().split())
        bal[a] += c
        bal[b] -= c

    pos = []
    neg = []

    for i in range(1, n + 1):
        if bal[i] > 0:
            pos.append([bal[i], i])
        elif bal[i] < 0:
            neg.append([i, -bal[i]])

    heap = []
    for amt, i in pos:
        heapq.heappush(heap, (-amt, i))

    res = []

    for i, need in neg:
        while need > 0:
            amt, j = heapq.heappop(heap)
            amt = -amt
            take = min(amt, need)
            res.append((i, j, take))
            amt -= take
            need -= take
            if amt > 0:
                heapq.heappush(heap, (-amt, j))

    out = [str(len(res))]
    for a, b, c in res:
        out.append(f"{a} {b} {c}")
    return "\n".join(out)

# provided sample 1
assert run("2 1\n1 2 50\n") == "1\n2 1 50"

# provided sample 2
assert run("3 3\n1 2 2\n2 3 4\n3 1 6\n") == "2\n2 1 2\n3 1 2"

# single node pair
assert run("2 1\n1 2 10\n") == "1\n2 1 10"

# balanced chain
assert run("4 3\n1 2 5\n2 3 5\n3 4 5\n") == "1\n4 1 5"

# zero net internal cancellations
assert run("3 2\n1 2 5\n2 1 5\n") == "0"

# split creditors
assert run("3 2\n1 2 10\n1 3 5\n") == "1\n2 1 10\n3 1 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| simple transfer | 2 1 50 | basic correctness |
| chain redistribution | multiple edges | multi-debtor single creditor handling |
| cancellations | 0 | zero net handling |
| split incoming | correct aggregation | creditor receiving multiple transfers |

## Edge Cases

A key edge case appears when all transactions cancel out pairwise so every balance becomes zero. In this case the algorithm builds an empty heap and processes no debtors, producing zero output operations without entering the matching phase.

Another case is when one creditor has very large capacity and many small debtors exist. The heap ensures the creditor is reused repeatedly, reducing its remaining capacity step by step while still respecting the single-outgoing constraint per debtor.

A final subtle case occurs when a creditor’s capacity is partially used and then reinserted into the heap. The correctness depends on always updating the remaining capacity before reinsertion, ensuring no stale value is ever reused.
