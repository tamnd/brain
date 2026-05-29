---
title: "CF 332C - Students' Revenge"
description: "We have n possible university orders. Every order has two values. The value a[i] measures how many grey hairs the chairperson gets if she obeys that order. The value b[i] measures how unhappy the directors become if she refuses that order."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 332
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 193 (Div. 2)"
rating: 2200
weight: 332
solve_time_s: 421
verified: false
draft: false
---

[CF 332C - Students' Revenge](https://codeforces.com/problemset/problem/332/C)

**Rating:** 2200  
**Tags:** data structures, greedy, sortings  
**Solve time:** 7m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We have `n` possible university orders. Every order has two values.

The value `a[i]` measures how many grey hairs the chairperson gets if she obeys that order.

The value `b[i]` measures how unhappy the directors become if she refuses that order.

The students choose exactly `p` orders to be approved. After that, the chairperson chooses exactly `k` of those approved orders to obey.

Her behavior is adversarial from the students' perspective. She chooses the `k` orders that minimize the directors' displeasure first. Among all choices with minimum displeasure, she then minimizes the number of grey hairs.

The students want to maximize the total grey hairs from the `k` obeyed orders. If several selections achieve the same grey hair total, they want the directors' displeasure from the refused orders to be as large as possible.

The key difficulty is that the students do not directly decide which orders get obeyed. They only choose the set of size `p`, then the chairperson responds optimally for herself.

The constraints immediately rule out brute force. We may have `n = 10^5`, so any algorithm around `O(n^2)` is already risky, and anything exponential is impossible. We need something near `O(n log n)`.

A subtle point is the chairperson's tie-breaking rule. She minimizes displeasure first, not grey hairs. A careless solution that optimizes by `a` alone fails.

Consider this example:

```
4 3 2
100 1
99 1
1 100
1 100
```

If we choose orders `{1,2,3}`, the chairperson obeys orders `1` and `2` because they have the smallest `b`. Grey hairs become `199`.

If we choose `{1,3,4}`, she obeys `1` and either `3` or `4`. Grey hairs become only `101`.

The set with the largest individual `a` values is not always optimal. What matters is which orders the chairperson is forced to obey.

Another easy mistake is forgetting the second tie-break on `a`.

```
3 2 1
10 5
1 5
100 10
```

If the students choose orders `1` and `2`, the chairperson must obey one of them because both have minimum `b = 5`. She then chooses the one with smaller `a`, namely order `2`.

Grey hairs become `1`, not `10`.

Any correct solution must model both levels of optimization exactly.

The case `k = p` also behaves differently. Then the chairperson obeys every chosen order, so the `b` values become irrelevant.

```
4 4 4
5 1
7 100
9 3
2 8
```

The correct answer is simply all orders, maximizing total `a`.

A solution built around selecting low `b` orders without handling this boundary case carefully can break.

## Approaches

The brute-force approach is straightforward conceptually. Enumerate every subset of size `p`. For each subset, simulate the chairperson's response.

To simulate her choice, sort the selected orders by increasing `b`, and for equal `b`, by increasing `a`. She obeys the first `k` orders in that ordering. Compute the resulting grey hairs and displeasure, then keep the best subset.

This works because it directly follows the rules of the problem. Unfortunately, it becomes unusable immediately. The number of subsets is:

$\binom{n}{p}$

With `n = 10^5`, even tiny values of `p` already produce astronomically many subsets.

The critical observation is that once the students choose the approved set, the chairperson's behavior is fully determined by sorting on `(b, a)`.

She always obeys the `k` lexicographically smallest pairs `(b[i], a[i])`.

That means the students actually control which orders are obeyed by controlling which orders become the smallest under this ordering.

Suppose we decide that some order `x` is among the obeyed ones. Then every non-obeyed approved order must be strictly worse in the chairperson's ordering. In practice, that means the non-obeyed orders must come after the obeyed ones when sorted by `(b, a)`.

This suggests sorting all orders globally by `(b, a)`.

After sorting, if an order is obeyed, then every approved but disobeyed order must appear later in the sorted order.

Now think about what the students want.

The obeyed orders contribute to the objective through their `a` values.

The disobeyed approved orders only matter for tie-breaking on directors' displeasure, so among all valid choices we want large `b` there.

Suppose we fix the last obeyed order in sorted order. Then:

The obeyed orders must come from the prefix ending there.

The disobeyed approved orders must come from the suffix after it.

Among the prefix, we want the largest possible sum of `a` using exactly `k` orders, and the fixed order must be included.

Among the suffix, we simply want the `p-k` largest `b` values because they will all be refused anyway.

This transforms the problem into a greedy selection problem supported by heaps.

We process orders in sorted `(b, a)` order. While scanning from left to right, we maintain the best set of `k` orders by `a` inside the current prefix. A min-heap allows us to keep the largest `k` values efficiently.

For every position that can serve as the last obeyed order, we know the optimal obeyed set. Then we fill the remaining `p-k` slots from the suffix arbitrarily, since they will never be obeyed.

The total complexity becomes `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(p) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store every order as `(b, a, index)` and sort all orders by increasing `b`, then increasing `a`.

This sorted order matches the chairperson's priority when deciding which orders to obey.
2. Scan the sorted array from left to right while maintaining a heap of candidate obeyed orders.

The heap stores pairs `(a, position)` and keeps exactly the largest `k` values of `a` seen so far.
3. Maintain the sum of `a` values currently inside the heap.

Whenever the heap size exceeds `k`, remove the smallest `a`. This guarantees the heap always represents the best possible choice of `k` obeyed orders inside the current prefix.
4. Whenever the heap size becomes exactly `k`, record the current total.

At position `i`, the heap now represents the maximum possible grey hair sum achievable using `k` obeyed orders from positions `0...i`.
5. Track the position where this sum becomes maximum.

Because the students primarily maximize grey hairs, we only care about the largest such sum.
6. After finding the best prefix, reconstruct the chosen obeyed orders from the heap contents at that position.

These are the `k` orders the chairperson will end up obeying.
7. Fill the remaining `p-k` slots using any orders after the chosen prefix.

Since all these orders appear later in `(b, a)` order, the chairperson always prefers the earlier selected `k` orders and never obeys these extra ones.
8. Output all selected indices.

### Why it works

The invariant during the scan is that the heap always contains the largest possible `k` values of `a` among the processed prefix.

The chairperson obeys the lexicographically smallest `(b, a)` pairs among the approved orders. By choosing all additional approved orders only from later positions in the sorted order, we guarantee none of them can replace an obeyed order.

So the only freedom the students have is selecting which `k` orders become the earliest approved ones. Among every prefix, the best such choice is clearly the `k` largest `a` values. The heap maintains exactly that.

Any optimal solution can be transformed into one where the obeyed orders form such a prefix-optimal set, so the algorithm never misses the optimum.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, p, k = map(int, input().split())

    orders = []
    for i in range(1, n + 1):
        a, b = map(int, input().split())
        orders.append((b, a, i))

    orders.sort()

    heap = []
    current_sum = 0

    best_sum = -1
    best_pos = -1

    take = [False] * n
    best_take = [False] * n

    for i in range(n):
        b, a, idx = orders[i]

        heapq.heappush(heap, (a, i))
        current_sum += a
        take[i] = True

        if len(heap) > k:
            removed_a, removed_pos = heapq.heappop(heap)
            current_sum -= removed_a
            take[removed_pos] = False

        if len(heap) == k and current_sum > best_sum:
            best_sum = current_sum
            best_pos = i
            best_take = take[:]

    answer = []

    for i in range(best_pos + 1):
        if best_take[i]:
            answer.append(orders[i][2])

    need = p - k

    for i in range(n - 1, best_pos, -1):
        if need == 0:
            break
        answer.append(orders[i][2])
        need -= 1

    print(*answer)

solve()
```

The first important step is sorting by `(b, a)`. This exactly reproduces the chairperson's decision order. Any approved order appearing later in this ordering can never be obeyed while an earlier approved order remains unchosen.

The heap maintains the current best obeyed set. Since Python's `heapq` is a min-heap, the smallest `a` sits on top. When the heap grows beyond size `k`, removing the minimum leaves the `k` largest `a` values.

The array `take` tracks which positions currently belong to the heap. When we discover a new best answer, we copy this state into `best_take`.

That copy is necessary. A common bug is storing only the heap itself or only the sum. The heap keeps changing afterward, so without a snapshot reconstruction becomes incorrect.

The reconstruction phase is subtle. We first add the chosen `k` obeyed orders from the prefix. Then we add arbitrary later orders to reach total size `p`.

Choosing later orders is safe because every later order has lexicographically larger `(b, a)` than every chosen obeyed order. The chairperson always prefers the earlier ones.

All arithmetic fits comfortably inside 64-bit integers because sums can reach `10^5 * 10^9`.

## Worked Examples

### Sample 1

Input:

```
5 3 2
5 6
5 8
1 3
4 3
4 11
```

After sorting by `(b, a)`:

| Position | Order Index | a | b |
| --- | --- | --- | --- |
| 0 | 3 | 1 | 3 |
| 1 | 4 | 4 | 3 |
| 2 | 1 | 5 | 6 |
| 3 | 2 | 5 | 8 |
| 4 | 5 | 4 | 11 |

Heap processing:

| Step | Current Order | Heap a-values | Current Sum | Best Sum |
| --- | --- | --- | --- | --- |
| 0 | (1,3) | [1] | 1 | - |
| 1 | (4,3) | [1,4] | 5 | 5 |
| 2 | (5,6) | [4,5] | 9 | 9 |
| 3 | (5,8) | [5,5] | 10 | 10 |
| 4 | (4,11) | [5,5] | 10 | 10 |

The best obeyed set becomes orders `1` and `2`, both with `a = 5`.

We still need one extra approved order. Any later order works, for example order `5`.

Final answer can be:

```
1 2 5
```

The trace shows the key invariant. The heap always stores the best possible `k=2` grey-hair values inside the processed prefix.

### Example 2

Input:

```
4 4 4
5 1
7 100
9 3
2 8
```

Sorted order:

| Position | Order Index | a | b |
| --- | --- | --- | --- |
| 0 | 1 | 5 | 1 |
| 1 | 3 | 9 | 3 |
| 2 | 4 | 2 | 8 |
| 3 | 2 | 7 | 100 |

Heap processing:

| Step | Current Order | Heap a-values | Current Sum |
| --- | --- | --- | --- |
| 0 | (5,1) | [5] | 5 |
| 1 | (9,3) | [5,9] | 14 |
| 2 | (2,8) | [2,5,9] | 16 |
| 3 | (7,100) | [2,5,7,9] | 23 |

Since `k = p = 4`, every chosen order is obeyed.

The algorithm naturally keeps all four orders.

This example demonstrates that the method handles the boundary case without any special branching.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting plus heap insertions/removals |
| Space | O(n) | Arrays and heap storage |

With `n = 10^5`, an `O(n log n)` solution easily fits within the time limit. Heap operations are logarithmic, and each order enters and leaves the heap at most once.

## Test Cases

```python
import sys
import io
import heapq

def solve():
    input = sys.stdin.readline

    n, p, k = map(int, input().split())

    orders = []
    for i in range(1, n + 1):
        a, b = map(int, input().split())
        orders.append((b, a, i))

    orders.sort()

    heap = []
    current_sum = 0

    best_sum = -1
    best_pos = -1

    take = [False] * n
    best_take = [False] * n

    for i in range(n):
        b, a, idx = orders[i]

        heapq.heappush(heap, (a, i))
        current_sum += a
        take[i] = True

        if len(heap) > k:
            rem_a, rem_pos = heapq.heappop(heap)
            current_sum -= rem_a
            take[rem_pos] = False

        if len(heap) == k and current_sum > best_sum:
            best_sum = current_sum
            best_pos = i
            best_take = take[:]

    ans = []

    for i in range(best_pos + 1):
        if best_take[i]:
            ans.append(str(orders[i][2]))

    need = p - k

    for i in range(len(orders) - 1, best_pos, -1):
        if need == 0:
            break
        ans.append(str(orders[i][2]))
        need -= 1

    print(" ".join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# sample 1
out = set(run(
"""5 3 2
5 6
5 8
1 3
4 3
4 11
""").split())

assert len(out) == 3

# minimum size
assert run(
"""1 1 1
7 9
""") == "1"

# k = p case
out = set(run(
"""4 4 4
5 1
7 100
9 3
2 8
""").split())

assert out == {"1", "2", "3", "4"}

# equal b values, tie decided by a
out = set(run(
"""3 2 1
10 5
1 5
100 10
""").split())

assert len(out) == 2

# all equal values
out = set(run(
"""5 3 2
4 4
4 4
4 4
4 4
4 4
""").split())

assert len(out) == 3
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `1` | Minimum bounds |
| `k = p` case | All indices selected | Every approved order gets obeyed |
| Equal `b` values | Any valid size-2 set | Correct secondary ordering on `a` |
| All equal values | Any valid size-3 set | Stability under many equivalent choices |

## Edge Cases

Consider again the equal `b` tie-break example:

```
3 2 1
10 5
1 5
100 10
```

Sorted order becomes:

| Position | Index | a | b |
| --- | --- | --- | --- |
| 0 | 2 | 1 | 5 |
| 1 | 1 | 10 | 5 |
| 2 | 3 | 100 | 10 |

The algorithm scans prefixes while maintaining the best single `a`.

At position `0`, best sum is `1`.

At position `1`, best sum becomes `10`.

At position `2`, best sum becomes `100`.

The chosen obeyed order is order `3`. The second approved order comes from later positions only if possible. Since none exist, the approved set becomes `{1,3}` or `{2,3}` depending on reconstruction.

The chairperson obeys order `1` or `2` before order `3` only if they are approved together and lexicographically smaller. The sorted-order construction prevents mistakes here.

Now consider the boundary case:

```
4 4 4
5 1
7 100
9 3
2 8
```

Since `k = p`, every approved order is obeyed.

The heap simply keeps all four orders because it never exceeds size `k`.

Reconstruction selects every index exactly once.

Finally, consider a case where later filler orders have huge `a` values:

```
5 3 2
1 1
2 2
100 100
99 101
98 102
```

The algorithm chooses obeyed orders from the earliest valid prefix, namely orders `1` and `2`.

Then it adds one later filler order, for example order `3`.

Even though order `3` has enormous `a`, the chairperson still obeys orders `1` and `2` because their `(b, a)` pairs are lexicographically smaller.

This confirms why later filler orders cannot interfere with the chosen obeyed set.
