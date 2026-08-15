---
title: "CF 102354C - Money Sharing"
description: "We process one chronological sequence containing two kinds of events. A positive value means that this much money is added to the shared account. A negative value represents a borrowing request whose size is the absolute value of that number."
date: "2026-08-16T01:42:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102354
codeforces_index: "C"
codeforces_contest_name: "2018-2019 Summer Petrozavodsk Camp, Oleksandr Kulkov Contest 2"
rating: 0
weight: 102354
solve_time_s: 163
verified: false
draft: false
---

[CF 102354C - Money Sharing](https://codeforces.com/problemset/problem/102354/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We process one chronological sequence containing two kinds of events. A positive value means that this much money is added to the shared account. A negative value represents a borrowing request whose size is the absolute value of that number. The account starts at zero, and an approved request immediately removes its amount from the account. A request can only be approved if the account can pay it at that moment.

The output has one line for every event. A positive event is always printed as `resupplied`. For a request, we print `approved` if we keep that request in the accepted set and `declined` otherwise. The objective is to minimize the total number of declined requests, not the total amount of money borrowed.

There can be up to (10^5) requests and (10^5) resupplies, so the event sequence can contain (2\cdot10^5) elements. A quadratic algorithm could perform around (4\cdot10^{10}) operations in the worst case, which is far beyond a one-second limit. We need essentially linear or (O(N\log N)) work, where (N=n+m). The amounts can reach (10^9), and their total can reach roughly (2\cdot10^{14}), so the running balance must use an integer type capable of holding values much larger than 32-bit integers. Python integers already provide this safely.

The first tricky case is a request that is too large for the account by itself. For example,

```
1 1
-5
+5
```

has output

```
declined
resupplied
```

The first request must be declined because money arriving later cannot retroactively approve it. A careless solution that first computes the total amount of all resupplies and then decides which requests to accept would incorrectly treat the first request as feasible.

Another subtle case is when the current request can be rejected, but rejecting an earlier request is better. Consider,

```
3 1
+5
-3
-2
-1
```

A correct output is

```
resupplied
approved
approved
approved
```

Here the balance after the first two requests is zero, so the final request is impossible and must actually be declined. Thus the correct output is instead

```
resupplied
approved
approved
declined
```

A more revealing example is,

```
3 1
+5
-4
-3
+10
```

At `-3`, the account has only one unit left. We can make the current prefix feasible by declining the earlier request of 4 rather than the current request of 3. The output can be

```
resupplied
declined
approved
resupplied
```

A greedy rule that always declines the current request whenever there is insufficient money loses an unnecessary accepted request.

There is also a case where several requests have to be removed at one event. For example,

```
3 1
+3
-2
-2
-2
```

After accepting the first two requests, the balance would be negative when the third request arrives. Removing the largest accepted request is enough here, but in general several removals may be required. The implementation must keep removing accepted requests until the balance is nonnegative.

## Approaches

The direct brute-force approach is to decide independently whether every request is approved or declined. With (n) requests there are (2^n) possible subsets. For each subset, we can scan the complete event sequence and check whether its accepted requests are feasible at every point. That gives (O((n+m)2^n)) operations. With (n=10^5), even (2^n) itself is hopeless, so this approach is useful only for understanding the optimization target.

The key observation is that feasibility depends only on the total amount of accepted requests seen so far. Suppose the total resupply received so far is (S), and the accepted requests in the prefix have total amount (C). The prefix is feasible exactly when (C\le S).

Now process requests from left to right and tentatively accept every one. If accepting the current request makes the total exceed the available money, at least one accepted request from the processed prefix must be removed. Since the objective counts declined requests, we want to remove exactly one request whenever one removal can restore feasibility. Among all accepted requests, removing the largest one gives the greatest reduction in consumed money while costing the same one rejection.

This greedy choice also preserves the most money for future requests. Suppose two accepted requests have sizes (a<b). If we must reject one of them, rejecting (b) leaves (b-a) more money available than rejecting (a), while both choices increase the number of rejected requests by exactly one. A larger remaining balance can never make future feasibility worse.

That leads naturally to a max-heap containing all currently accepted request sizes. When a request arrives, tentatively accept it and insert it into the heap. If the balance becomes negative, remove the largest accepted request from the heap and mark that request as declined. Repeat until the balance is nonnegative. The heap lets us find the largest accepted request in (O(\log n)).

The brute-force method considers every possible accepted subset because it has no way to recognize which decisions are interchangeable. The greedy method exploits the fact that every request has the same cost in the objective, namely one rejection, while their monetary sizes differ. Whenever a rejection is forced, the largest accepted request is the most valuable one to discard.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O((n+m)2^n)) | (O(n+m)) | Too slow |
| Optimal | (O((n+m)\log n)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Read the complete event sequence and create an output array initialized according to the event type. For a positive event, the answer is immediately `resupplied`; for a request, initially mark it `approved` because the greedy algorithm will first try to accept every request.
2. Maintain `balance`, the amount of money currently left in the account, and a max-heap of accepted requests. Python's `heapq` is a min-heap, so store each request amount as a negative number. Store the event index together with the amount because a later heap removal may reject an earlier request.
3. When a positive event of value (x) occurs, add (x) to `balance`. Nothing has to be removed from the heap because resupply only increases the available money.
4. When a negative event of value (-x) occurs, tentatively approve it. Subtract (x) from `balance` and insert (( -x, index)) into the heap.
5. If `balance` is now negative, repeatedly remove the largest request from the heap. For a heap entry representing amount (x), add (x) back to `balance` and change that request's output from `approved` to `declined`.

The removed request does not have to be the current one. This is the central greedy step: one rejection can recover the largest possible amount of money, leaving the largest possible balance for future requests.
6. Continue until all events have been processed. Every accepted request remains in the heap, and every request removed from the heap is marked `declined`.

### Why it works

After processing any prefix, the heap contains exactly the requests that the algorithm currently accepts. The invariant is that their total cost never exceeds the total resupply received in that prefix, so the account balance is always nonnegative.

When a new request causes a deficit, every feasible solution must reject at least one request from the accepted prefix. The algorithm rejects the largest accepted request. This uses the minimum possible number of new rejections, because one rejection is enough whenever the largest request restores feasibility. If several requests must be removed, each removal chooses the largest remaining request, maximizing the money recovered for every rejection.

More strongly, among all feasible choices having the same number of accepted requests in the processed prefix, keeping the largest possible remaining balance is always at least as good for the future. Rejecting the largest request achieves exactly that. Thus the greedy state never has fewer possibilities for future requests than another solution with the same number of rejections. By induction over the event sequence, the final number of declined requests is minimal.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    total = n + m

    events = [int(input()) for _ in range(total)]

    answer = []
    heap = []
    balance = 0

    for i, x in enumerate(events):
        if x > 0:
            balance += x
            answer.append("resupplied")
            continue

        amount = -x
        balance -= amount
        heapq.heappush(heap, (-amount, i))
        answer.append("approved")

        while balance < 0:
            neg_amount, idx = heapq.heappop(heap)
            amount_removed = -neg_amount
            balance += amount_removed
            answer[idx] = "declined"

    sys.stdout.write("\n".join(answer))

if __name__ == "__main__":
    solve()
```

The input is stored first so that every request has a stable event index. This index is necessary because a request accepted earlier can later become the request we decide to decline.

For a resupply, the code only increases `balance` and records `resupplied`. There is no reason to modify the heap because existing accepted requests remain accepted when more money arrives.

For a request, the code first treats it as accepted. This temporarily subtracts its amount from `balance` and inserts it into the heap. If the resulting balance is negative, the current prefix cannot be feasible with all tentative approvals.

The heap stores `(-amount, index)`. Because Python's heap returns the smallest value, the most negative entry corresponds to the largest request amount. For example, requests of sizes 3, 8, and 5 are stored as `-3`, `-8`, and `-5`, so `-8` is removed first.

When a request is removed, the code adds its amount back to the balance and changes `answer[idx]` to `declined`. This is why the output cannot simply be decided at the moment a request arrives. A request that was initially approved can become the rejected request later.

The `while` condition is necessary rather than an `if`. A single large request can create a deficit greater than every other accepted request, so several accepted requests may have to be discarded. The heap always contains at least the current request while the balance is negative, so the loop cannot run out of elements before restoring feasibility.

Python integers handle the possible balance of roughly (2\cdot10^{14}) without overflow. The heap contains at most (n) requests, and every request is inserted once and removed at most once.

## Worked Examples

### Sample 1

The input is

```
4 1
+5
-3
-2
-1
-1
```

The state evolves as follows.

| Event | Action | Balance | Heap amounts | Output change |
| --- | --- | --- | --- | --- |
| `+5` | Resupply | 5 | `{}` | `resupplied` |
| `-3` | Accept | 2 | `{3}` | `approved` |
| `-2` | Accept | 0 | `{3, 2}` | `approved` |
| `-1` | Accept | -1 | `{3, 2, 1}` | Remove 3, so request 2 becomes `declined` |
| `-1` | Accept | 0 | `{2, 1, 1}` | `approved` |

The third request in the table is the original `-1` at event index 3. It initially becomes approved, but the heap identifies the earlier request of size 3 as the best one to reject. That leaves enough money for both size-2 and size-1 requests.

The final output is

```
resupplied
declined
approved
approved
approved
```

The trace demonstrates why the heap must store event indices. The request that becomes declined is not necessarily the request currently being processed.

### Constructed Example 2

Consider

```
3 2
+5
-4
-3
+2
-2
```

The trace is:

| Event | Action | Balance | Heap amounts | Output change |
| --- | --- | --- | --- | --- |
| `+5` | Resupply | 5 | `{}` | `resupplied` |
| `-4` | Accept | 1 | `{4}` | `approved` |
| `-3` | Accept | -2 | `{4, 3}` | Remove 4, so request 2 becomes `declined` |
| `+2` | Resupply | 3 | `{3}` | `resupplied` |
| `-2` | Accept | 1 | `{3, 2}` | `approved` |

The algorithm rejects the earlier request of size 4 and keeps the request of size 3. Both choices would involve one rejection at the moment of the deficit, but keeping the smaller request leaves more money available. The later resupply then makes the final request feasible as well.

The output is

```
resupplied
declined
approved
resupplied
approved
```

This example exercises the central exchange argument: when exactly one rejection is required, removing the largest accepted request is always the strongest choice for the remaining sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((n+m)\log n)) | Every request enters the heap once and can leave it once, with (O(\log n)) cost per heap operation. |
| Space | (O(n+m)) | The event array, output array, and heap together use linear memory. |

With at most (2\cdot10^5) events, the heap performs only a linear number of insertions and removals, each logarithmic in the number of requests. This is comfortably within the intended complexity for the one-second limit, and the memory usage is linear.

## Test Cases

The following test harness uses the same algorithm as the submitted solution, but wraps it in a function so that several complete inputs can be checked with assertions.

```python
import heapq
import io
import sys

def solve_io(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    m = next(it)
    events = [next(it) for _ in range(n + m)]

    answer = []
    heap = []
    balance = 0

    for i, x in enumerate(events):
        if x > 0:
            balance += x
            answer.append("resupplied")
        else:
            amount = -x
            balance -= amount
            heapq.heappush(heap, (-amount, i))
            answer.append("approved")

            while balance < 0:
                neg_amount, idx = heapq.heappop(heap)
                balance += -neg_amount
                answer[idx] = "declined"

    return "\n".join(answer)

# Provided sample
assert solve_io(
    """4 1
+5
-3
-2
-1
-1
"""
) == """resupplied
declined
approved
approved
approved""", "sample 1"

# Minimum-sized input, request arrives before any money.
assert solve_io(
    """1 1
-5
+5
"""
) == """declined
resupplied""", "initial empty account"

# A previous larger request must be rejected instead of the current request.
assert solve_io(
    """3 1
+5
-4
-3
-1
"""
) == """resupplied
declined
approved
approved""", "reject largest accepted request"

# All request and resupply amounts are equal, with exact balance at every request.
assert solve_io(
    """3 3
+1
-1
+1
-1
+1
-1
"""
) == """resupplied
approved
resupplied
approved
resupplied
approved""", "all equal values"

# Maximum-size structure: 100000 resupplies followed by 100000 requests.
# Every request has exactly one unit available.
max_n = 100000
max_m = 100000
max_input = (
    f"{max_n} {max_m}\n"
    + "+1\n" * max_m
    + "-1\n" * max_n
)
max_output = (
    "resupplied\n" * max_m
    + "approved\n" * max_n
).rstrip()

assert solve_io(max_input) == max_output, "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1`, followed by `-5`, `+5` | `declined`, `resupplied` | Initial balance is zero, and future money cannot satisfy a past request. |
| `+5, -4, -3, -1` | `resupplied`, `declined`, `approved`, `approved` | An earlier larger request must be removed instead of blindly rejecting the current request. |
| Alternating `+1, -1` events | Every request is `approved` | Exact zero-balance boundaries and equal request sizes. |
| 100000 `+1` events followed by 100000 `-1` events | Every request is `approved` | Maximum event count, large output, and linear heap usage. |

## Edge Cases

The first edge case is a request before the first resupply. For

```
1 1
-5
+5
```

the heap receives the size-5 request, making the balance (-5). The heap immediately removes that request, restores the balance to zero, and marks it declined. The later `+5` only increases the balance afterward. The result is `declined`, `resupplied`, which respects the chronological nature of the account.

The second edge case is a deficit where rejecting the current request is not optimal. For

```
3 1
+5
-4
-3
-1
```

after `-4` the balance is 1. Accepting `-3` gives a balance of (-2). The heap contains requests of sizes 4 and 3, so the size-4 request is removed. The balance becomes 2, leaving the size-3 request accepted. The final `-1` then succeeds, leaving balance 1. The output is `resupplied`, `declined`, `approved`, `approved`.

The third edge case is an exact boundary where the balance becomes zero. With

```
3 1
+5
-2
-3
-1
```

the first request leaves balance 3, the second leaves balance 0, and the third request would make it negative. The heap contains sizes 2, 3, and 1 after tentative acceptance, so the largest request, size 3, is removed. The balance returns to 2, and the current size-1 request remains approved. The output is `resupplied`, `approved`, `declined`, `approved`. The condition must be `balance < 0`, not `balance <= 0`, because having exactly zero money is still feasible.

The fourth edge case is a request that creates a deficit requiring more than one removal. For example,

```
3 1
+3
-2
-2
-2
```

after the first request the balance is 1. After the second request it is (-1), so the heap removes one size-2 request and restores the balance to 1. The current request remains approved. The next size-2 request again creates a deficit, so another size-2 request is removed. The algorithm therefore handles multiple removals at one event rather than assuming a single rejection is always sufficient.

The final edge case is the maximum input size. With (10^5) resupplies of `+1` followed by (10^5) requests of `-1`, every request is immediately feasible. The heap grows to (10^5) elements, but every operation remains (O(\log n)), and the complete sequence still requires only (O((n+m)\log n)) time and (O(n+m)) memory.
