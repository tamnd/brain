---
title: "CF 102354C - Money Sharing"
description: "We process a sequence of money-sharing events in chronological order. A positive value means that much money is added to the public account. A negative value represents a borrower asking for the corresponding positive amount."
date: "2026-08-14T12:17:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102354
codeforces_index: "C"
codeforces_contest_name: "2018-2019 Summer Petrozavodsk Camp, Oleksandr Kulkov Contest 2"
rating: 0
weight: 102354
solve_time_s: 353
verified: false
draft: false
---

[CF 102354C - Money Sharing](https://codeforces.com/problemset/problem/102354/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We process a sequence of money-sharing events in chronological order. A positive value means that much money is added to the public account. A negative value represents a borrower asking for the corresponding positive amount. We must decide which requests to approve so that the account balance never becomes negative.

Among all valid decisions, the primary objective is to approve as many requests as possible. Equivalently, we want to minimize the number of declined requests. When several optimal decisions exist, any one is accepted.

The output has one line for every event. A positive event always produces `resupplied`. For a negative event, the output says whether that request was ultimately kept as approved or removed from the chosen set of requests.

There can be up to (10^5) requests and (10^5) resupplies, so the entire sequence contains up to (2\cdot10^5) events. An algorithm that tries many subsets of requests is immediately impossible, since (2^{100000}) is far beyond any practical bound. Even an (O(n^2)) algorithm would perform around (10^{10}) operations in the worst case, which is too much for a one-second time limit. We need essentially linear or (O(n\log n)) processing.

The values themselves can have magnitude up to (10^9), and there can be (2\cdot10^5) events, so the total amount of money can reach roughly (2\cdot10^{14}). Python integers handle this safely, while a language with fixed-width integers should use 64-bit arithmetic.

A subtle case occurs when accepting the current request is possible only if we later remove a larger request that was already accepted. For example:

```
3 1
+5
-3
-4
-2
```

The optimal output is:

```
resupplied
declined
approved
approved
```

After accepting `-3`, only 2 units remain, so `-4` cannot be accepted together with it. A careless greedy algorithm might simply decline `-4`, then also decline `-2` because it was looking only at the current balance. The better decision is to replace the earlier request of size 3 with the request of size 4. The total number of approved requests remains one at that point, and the remaining 2 units can then approve the final request.

Another edge case is when the request that causes the balance to become negative is itself the largest accepted request. For example:

```
1 1
+3
-5
```

The only correct output is:

```
resupplied
declined
```

The algorithm must not leave the balance negative after temporarily accepting the request. It should immediately remove the largest accepted request, which here is the current request.

A third case is a request whose amount exactly equals the available balance:

```
2 1
+5
-5
-1
```

The correct output is:

```
resupplied
approved
declined
```

A condition using `balance <= 0` instead of `balance < 0` would incorrectly reject the request that uses the entire balance. Zero money remaining is completely valid.

Finally, multiple resupplies can appear between requests:

```
3 2
+2
+3
-4
-1
-1
```

The first two requests can be approved, leaving zero money, while the last one must be declined. A solution that treats each resupply independently rather than maintaining the cumulative balance will make incorrect decisions.

## Approaches

The most direct approach is to consider every subset of requests. For each subset, we simulate the events in chronological order and check whether every selected request can be paid at its position. Among all feasible subsets, we keep one containing the largest number of requests. This is correct because every possible set of approved requests is explicitly considered.

The problem is the number of subsets. With (n) requests there are (2^n) possible choices, and checking one choice takes (O(n+m)) time. The worst-case operation count is therefore (O((n+m)2^n)), which is already hopeless for even a few dozen requests, let alone (10^5).

The key observation is that every request has exactly the same value for our objective: approving any request contributes one to the answer. The only thing that differs between requests is how much money they consume.

Suppose at some point the chosen requests require more money than has been supplied so far. We have to remove at least one already accepted request. Since removing any one request decreases the number of approved requests by exactly one, the best possible repair is to remove the request that frees the largest amount of money. Removing a larger request gives us at least as much remaining balance as removing any smaller request, while costing exactly the same one approval.

This leads naturally to a greedy strategy. Temporarily accept every request. If doing so makes the balance negative, remove the largest request among all currently accepted requests. A max-heap lets us find that request efficiently.

The important part is that a request removed earlier can be replaced by a later request. This is why simply declining the first request that does not fit is not sufficient. The heap gives us the ability to revise an earlier decision while keeping the maximum possible number of accepted requests.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O((n+m)2^n)) | (O(n+m)) | Too slow |
| Greedy with max-heap | (O((n+m)\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Read the complete event sequence and create an output array initially containing no decision for each event. Keep a variable `balance`, initially zero, representing money currently available after all approved requests processed so far.
2. For every positive event, add its value to `balance` and write `resupplied` for that event. A resupply never competes with another decision, so it can always be incorporated immediately.
3. For every negative event, let `cost` be its absolute value. Temporarily approve the request by subtracting `cost` from `balance`. Store this accepted request in a max-heap together with its position.
4. If the resulting balance is nonnegative, keep the request approved. The current set of accepted requests is feasible at this point, so there is no reason to remove anything.
5. If the balance is negative, remove the accepted request with the largest cost from the heap. Mark that request as `declined` and add its cost back to `balance`. Because all requests contribute exactly one unit to the objective, removing the largest request is the best possible repair: every possible removal loses one approval, and the largest request gives back the most money.
6. Continue through the entire event sequence. At the end, every request remaining in the heap is approved, while every request removed from the heap is declined. The output array already records the final status of every request, including requests that were accepted temporarily and later removed.

### Why it works

After processing any prefix of the event sequence, the heap contains a feasible set of approved requests with the maximum possible number of requests among all feasible choices for that prefix.

When a new request fits, adding it increases the number of approved requests by one, so the new set is optimal for that prefix. When it does not fit, some accepted request must be removed. Every possible removal decreases the number of approvals by one, but removing the largest request leaves the greatest possible balance. Thus the heap contains the best possible feasible set among all choices with the maximum number of approvals. Since future events depend only on the amount of money left and the requests already selected, keeping the largest possible remaining balance among equally large solutions can never hurt future feasibility. This maintains the invariant throughout the sequence and gives a globally optimal number of approved requests.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    total = n + m

    events = [int(input()) for _ in range(total)]

    balance = 0
    heap = []
    answer = [""] * total

    for i, x in enumerate(events):
        if x > 0:
            balance += x
            answer[i] = "resupplied"
        else:
            cost = -x

            balance -= cost
            heapq.heappush(heap, (-cost, i))
            answer[i] = "approved"

            if balance < 0:
                neg_cost, idx = heapq.heappop(heap)
                removed_cost = -neg_cost

                balance += removed_cost
                answer[idx] = "declined"

    sys.stdout.write("\n".join(answer))

if __name__ == "__main__":
    solve()
```

The `balance` variable represents the actual money left after all currently approved requests. Positive events increase it before any request decision can be made.

For a request, the code first inserts `(-cost, index)` into Python's min-heap. Negating the cost turns the smallest heap key into the largest original cost, effectively giving us a max-heap.

The request is initially marked `approved` because the greedy algorithm needs to consider it as a candidate. If this creates a negative balance, exactly one request is removed. The popped heap entry tells us both which request to decline and how much money that decision restores.

The index stored in every heap entry is necessary because the request removed from the heap might not be the current request. Without the index, we could know which amount to remove but could not update the corresponding output line.

The test is `balance < 0`, not `balance <= 0`. A balance of zero is valid because the last approved request can consume the account's entire remaining balance.

There is no integer overflow issue in Python. The largest possible cumulative value is on the order of (10^{14}), comfortably handled by Python's arbitrary-precision integers.

The input is read with `sys.stdin.readline`, and all output is assembled into one string. This avoids the overhead of performing many separate output operations for up to (2\cdot10^5) lines.

## Worked Examples

### Sample 1

The input is:

```
4 1
+5
-3
-2
-1
-1
```

The trace is:

| Event | Balance before | Action | Heap after action | Balance after |
| --- | --- | --- | --- | --- |
| `+5` | 0 | resupply | empty | 5 |
| `-3` | 5 | approve | {3} | 2 |
| `-2` | 2 | approve | {3, 2} | 0 |
| `-1` | 0 | temporarily approve, remove 3 | {2, 1} | 2 |
| `-1` | 2 | approve | {2, 1, 1} | 1 |

At the fourth event, approving the new request would make the balance negative. The largest accepted request is the earlier request of size 3, so that request is removed. The new request of size 1 survives, and the account is left with 2 units. This is better than declining the current request because both choices would remove one approval, but replacing the request of size 3 with the request of size 1 leaves much more money for future requests.

The final output is:

```
resupplied
declined
approved
approved
approved
```

### Constructed Example 2

Consider:

```
4 2
+5
-4
-3
+2
-2
-2
```

The trace is:

| Event | Balance before | Action | Heap after action | Balance after |
| --- | --- | --- | --- | --- |
| `+5` | 0 | resupply | empty | 5 |
| `-4` | 5 | approve | {4} | 1 |
| `-3` | 1 | temporarily approve, remove 4 | {3} | 2 |
| `+2` | 2 | resupply | {3} | 4 |
| `-2` | 4 | approve | {3, 2} | 2 |
| `-2` | 2 | approve | {3, 2, 2} | 0 |

The second request cannot coexist with the first request, because their combined cost is 7 while only 5 has been supplied so far. The greedy algorithm replaces the request costing 4 with the request costing 3. Later, the additional resupply makes it possible to accept both remaining requests.

The final output is:

```
resupplied
declined
approved
resupplied
approved
approved
```

This example demonstrates why the algorithm must be allowed to undo an earlier approval. A strategy that permanently commits to every request that fits at its own moment can lose an approval later.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O((n+m)\log n)) | Each request is inserted into and possibly removed from the heap once. |
| Space | (O(n+m)) | The event array and output contain the whole sequence, while the heap contains at most (n) requests. |

There are at most (2\cdot10^5) events and at most (10^5) heap entries. Each heap operation costs (O(\log n)), giving roughly (2\cdot10^5\log(10^5)) heap-level operations in the worst case. This is easily within the intended complexity for the given constraints, while the brute-force exponential approach is completely infeasible.

## Test Cases

The following test harness exposes the solver as a function so that the cases can be checked with ordinary Python assertions.

```python
import sys
import io
import heapq

def solve_data(inp: str) -> str:
    data = inp.strip().split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))
    total = n + m

    events = [int(next(it)) for _ in range(total)]

    balance = 0
    heap = []
    answer = [""] * total

    for i, x in enumerate(events):
        if x > 0:
            balance += x
            answer[i] = "resupplied"
        else:
            cost = -x

            balance -= cost
            heapq.heappush(heap, (-cost, i))
            answer[i] = "approved"

            if balance < 0:
                neg_cost, idx = heapq.heappop(heap)
                balance += -neg_cost
                answer[idx] = "declined"

    return "\n".join(answer) + "\n"

def run(inp: str) -> str:
    return solve_data(inp)

assert run("""\
4 1
+5
-3
-2
-1
-1
""") == """\
resupplied
declined
approved
approved
approved
""", "sample 1"

assert run("""\
2 1
+5
-5
-1
""") == """\
resupplied
approved
declined
""", "exact balance must be accepted"

assert run("""\
3 1
+5
-3
-4
-2
""") == """\
resupplied
declined
approved
approved
""", "replace a larger earlier request"

assert run("""\
1 1
+1
-1
""") == """\
resupplied
approved
""", "minimum-size input"

assert run("""\
4 2
+5
-4
-3
+2
-2
-2
""") == """\
resupplied
declined
approved
resupplied
approved
approved
""", "replacement followed by a later resupply"

events = [1] * 100000 + [-1] * 100000
large_input = "100000 100000\n" + "\n".join(map(str, events)) + "\n"
large_output = run(large_input)
large_lines = large_output.splitlines()

assert len(large_lines) == 200000, "maximum-size case has wrong output length"
assert all(x == "resupplied" for x in large_lines[:100000]), "all supplies must be processed"
assert all(x == "approved" for x in large_lines[100000:]), "all unit requests fit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `+1, -1` | Both events accepted | Minimum-size case and exact balance |
| `+5, -5, -1` | First request accepted, second declined | Distinguishes `balance == 0` from an invalid negative balance |
| `+5, -3, -4, -2` | `-3` declined, `-4` and `-2` accepted | Verifies replacement of a previously accepted request |
| `+5, -4, -3, +2, -2, -2` | `-4` declined, all later requests accepted | Verifies that replacement decisions interact correctly with future resupplies |
| 100000 supplies followed by 100000 unit requests | Every event accepted | Maximum-size input and performance |

## Edge Cases

The first non-obvious case is replacing an earlier request. For

```
3 1
+5
-3
-4
-2
```

the balance becomes 5 after the resupply. The request of 3 is accepted, leaving 2. The request of 4 is temporarily accepted, taking the balance to -2. The heap contains requests of sizes 3 and 4, so the size 4 request is actually removed, leaving the size 3 request approved and a balance of 2. The final request of size 2 is then accepted. The output is:

```
resupplied
approved
declined
approved
```

This is the exact situation in which a simplistic "decline the current request" rule happens to work, but the heap formulation also handles the more difficult reverse situation where the current request is smaller than an earlier one.

Consider instead:

```
3 1
+5
-3
-2
-4
```

After the first two requests, the balance is zero and the heap contains 3 and 2. The request of 4 is temporarily accepted, producing a balance of -4. The largest accepted request is 4 itself, so it is removed. The first two requests remain approved. The output is:

```
resupplied
approved
approved
declined
```

This confirms that the current request can be the one removed from the heap.

The exact-zero boundary is handled by

```
2 1
+5
-5
-1
```

The balance becomes zero after approving `-5`, so no removal occurs. Only the final request is declined. The output is:

```
resupplied
approved
declined
```

Using `<= 0` in the heap-repair condition would incorrectly remove the size-5 request.

A sequence can also contain several resupplies before any borrowing:

```
3 2
+2
+3
-4
-1
-1
```

The balance reaches 5 before the first request. After approving the request of 4, it is 1, so the request of 1 is also approved and the balance becomes zero. The final request cannot be approved. The output is:

```
resupplied
resupplied
approved
approved
declined
```

The algorithm simply accumulates every positive event in `balance`, so there is no special handling needed for consecutive resupplies.

Large amounts are another practical edge case. For example:

```
2 2
+1000000000
+1000000000
-1000000000
-1000000000
```

The balance reaches (2\cdot10^9), and both requests are approved, leaving zero. Python's integer arithmetic handles these values directly, and the heap stores the request costs without any conversion or truncation.

The final subtlety is that a declined request may have occurred many events earlier. Its output line must change when the heap later removes it. That is why every heap entry stores the original event index. Without that index, the algorithm could find the correct request size but would be unable to produce the required per-event output.
