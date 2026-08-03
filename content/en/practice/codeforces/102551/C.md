---
title: "CF 102551C - \u041f\u0440\u043e\u0434\u0443\u043a\u0442\u044b \u0432 \u044d\u043a\u0441\u043f\u0435\u0434\u0438\u0446\u0438\u0438"
description: "We have n food types. Type i has ki portions, and if we decide to keep this type, every one of those portions must be eaten by the end of day ti. Each day the expedition can consume exactly c portions whenever enough food remains."
date: "2026-08-03T20:15:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102551
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0422\u0440\u0435\u0442\u044c\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102551
solve_time_s: 603
verified: false
draft: false
---

[CF 102551C - \u041f\u0440\u043e\u0434\u0443\u043a\u0442\u044b \u0432 \u044d\u043a\u0441\u043f\u0435\u0434\u0438\u0446\u0438\u0438](https://codeforces.com/problemset/problem/102551/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We have `n` food types. Type `i` has `k_i` portions, and if we decide to keep this type, every one of those portions must be eaten by the end of day `t_i`. Each day the expedition can consume exactly `c` portions whenever enough food remains. The task is not to maximize the total number of portions eaten. It is to choose the largest possible set of food types that can be completely finished before their spoilage days. The output is the size of this set and the indices of the chosen types.

The constraints force us away from trying subsets. With `n` up to `200000`, an approach that checks many combinations is impossible because even quadratic solutions already approach tens of billions of operations. The large values of `k_i`, `t_i`, and `c` also mean we cannot simulate days. The solution has to reason about total capacity by deadlines and run in roughly `O(n log n)` time.

The main cases that cause mistakes are related to the deadline interpretation and the fact that a large product can block many smaller ones. For example:

```
1 2
1 2
```

The correct output is:

```
1
1
```

There are two people, so two portions can be eaten on day one. A solution that treats the deadline as the start of day `t_i` instead of the end of day `t_i` would incorrectly reject this product.

Another example is:

```
2 1
1 5
5 4
```

The correct output is:

```
1
2
```

The first product alone needs five portions on the first day, which is impossible. The second product can be finished within five days. A greedy solution that always keeps the earliest products without removing anything would fail because an impossible early product consumes the available capacity.

A final corner case is when a product exactly fills the remaining capacity:

```
2 3
2 6
3 3
```

The correct output is:

```
2
1 2
```

After two days, six portions can be eaten, and after three days, nine portions can be eaten. The equality case must be accepted.

## Approaches

A direct solution would try every possible set of food types and check whether that set can be scheduled. For a chosen set, sorting the products by deadline and checking every prefix would tell us whether the total amount due by each day fits inside `c * day` portions of available eating capacity. This method is correct because a deadline schedule is feasible exactly when every deadline prefix has enough total capacity. However, checking all subsets requires `2^n` choices, which is already impossible for `n` around 50, let alone `200000`.

A more useful way to look at the problem is to start from all products and remove only the products that prevent feasibility. Sort products by increasing spoilage day. While processing this order, every prefix contains all products whose deadlines are at most the current deadline. If the current prefix requires too many portions, some product in this prefix must be discarded.

The important observation is that when a prefix is impossible, removing the product with the largest number of portions is always the best repair. All products in the prefix have already passed the same deadline check, so removing any one product gives the same reduction in the number of selected types. Removing the largest one leaves the most remaining capacity for future products. This is the same exchange argument behind the classic scheduling greedy algorithm for maximizing the number of completed jobs.

After sorting by deadline, we maintain the selected products and their total number of portions. When adding a product breaks feasibility, we remove the selected product with maximum `k_i`. A heap supports this removal efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^n * n)` | `O(n)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Sort all products by increasing `t_i`. Products with earlier spoilage dates must be considered first because every product with deadline `d` competes for the total capacity available during the first `d` days.
2. Add the current product to the chosen set. Increase the total number of portions of the chosen products and insert the product into a max-heap ordered by `k_i`.
3. Check whether the chosen products can still be finished by the current deadline. The condition is:

$$\text{total portions} \leq c \times t_i$$

If this condition fails, the current set contains too many portions that must be eaten by this day.

1. Remove the product with the largest `k_i` from the heap and subtract its size from the total. This keeps the maximum possible number of product types because one removed type always fixes the violation, and removing the largest type wastes the least number of possible future choices.
2. After all products are processed, the remaining heap contains the indices of the maximum possible set of completely consumable products.

Why it works: after processing all products with deadlines up to a certain day, the maintained set is the largest possible set among those products that satisfies the capacity limit for that day. If adding a product makes the set invalid, every valid solution must remove at least one product from this prefix. Removing the largest product gives the smallest possible loss of consumed capacity while removing exactly one type. This keeps the set optimal for the current prefix, and the invariant continues to hold as later deadlines are processed.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

def solve():
    n, c = map(int, input().split())
    products = []

    for i in range(1, n + 1):
        t, k = map(int, input().split())
        products.append((t, k, i))

    products.sort()

    heap = []
    total = 0

    for t, k, idx in products:
        total += k
        heapq.heappush(heap, (-k, idx))

        if total > c * t:
            removed_k, _ = heapq.heappop(heap)
            total += removed_k

    ans = [idx for _, idx in heap]

    print(len(ans))
    if ans:
        print(*ans)

if __name__ == "__main__":
    solve()
```

The products are sorted by deadline so that every check represents all products that must be completed by the current day. The heap stores negative sizes because Python provides a min-heap, and negating the value turns it into a max-heap.

The variable `total` stores the total number of portions among currently accepted products. When it exceeds `c * t`, the current set cannot be completed before the current deadline. Removing the heap maximum is enough because only one product must be discarded to restore the invariant.

Python integers handle the large values safely. The maximum possible sum of portions is much larger than 64-bit integers, so languages with fixed-width integers need a wider type. The multiplication `c * t` must also be evaluated without overflow.

The output order does not matter, so the heap contents can be printed directly.

## Worked Examples

For Sample 1:

```
1 1
4 4
```

| Step | Current product | Total portions | Capacity by deadline | Heap | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | type 1, `(t=4,k=4)` | 4 | 4 | `{1}` | Keep |

The product requires exactly all available capacity before day four. Equality is allowed, so the answer contains type 1.

For Sample 2:

```
5 3
3 4
2 6
4 5
3 4
5 7
```

| Step | Current product | Total portions | Capacity by deadline | Heap | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | type 2, `(2,6)` | 6 | 6 | `{2}` | Keep |
| 2 | type 1, `(3,4)` | 10 | 9 | `{2,1}` | Remove type 2 |
| 3 | type 4, `(3,4)` | 8 | 9 | `{1,4}` | Keep |
| 4 | type 3, `(4,5)` | 13 | 12 | `{1,4,3}` | Remove type 3 |
| 5 | type 5, `(5,7)` | 19 | 15 | `{1,4,5}` | Remove type 5 |

The final set is `{1,4,5}`. It contains three products, which is optimal. The trace demonstrates why removing the largest product is useful. The initially large products with early deadlines are replaced by smaller products that allow more types to survive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Sorting takes `O(n log n)`, and every heap insertion or removal costs `O(log n)` |
| Space | `O(n)` | The sorted product list and heap store at most all products |

The algorithm only performs sorting and heap operations over the `200000` products, which fits comfortably within typical competitive programming limits. No simulation over days is performed, so large deadline values do not affect runtime.

## Test Cases

```python
import sys
import io
import heapq

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n, c = map(int, sys.stdin.readline().split())
    products = []

    for i in range(1, n + 1):
        t, k = map(int, sys.stdin.readline().split())
        products.append((t, k, i))

    products.sort()

    heap = []
    total = 0

    for t, k, idx in products:
        total += k
        heapq.heappush(heap, (-k, idx))

        if total > c * t:
            total += heapq.heappop(heap)[0]

    ans = [x[1] for x in heap]
    result = str(len(ans)) + "\n"
    if ans:
        result += " ".join(map(str, ans)) + "\n"

    sys.stdin = old_stdin
    return result

assert solve_data("""1 1
4 4
""") == "1\n1\n", "sample 1"

assert sorted(map(int, solve_data("""5 3
3 4
2 6
4 5
3 4
5 7
""").split()[1:])) == [1, 4, 5], "sample 2"

assert solve_data("""3 2
2 6
4 9
1 3
""").split()[0] == "0", "sample 3"

assert solve_data("""1 10
1 10
""") == "1\n1\n", "single exact capacity"

assert solve_data("""2 1
1 5
5 4
""").split()[0] == "1", "remove impossible large early product"

assert solve_data("""3 2
1 2
2 4
3 1
""").split()[0] == "3", "exact deadline boundaries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 10 / 1 10` | One product | Minimum input and exact capacity handling |
| `2 1 / 1 5 / 5 4` | One product | Removing an oversized early product |
| `3 2 / 1 2 / 2 4 / 3 1` | Three products | Equality at every deadline boundary |

## Edge Cases

For the first deadline interpretation case:

```
1 2
1 2
```

The algorithm sorts the only product, adds its two portions, and checks against `c * t = 2 * 1 = 2`. The condition is satisfied because the total is equal to the available capacity. The product remains selected, giving output:

```
1
1
```

For the case where a large product must be removed:

```
2 1
1 5
5 4
```

The first product is added with total `5`, but the capacity by day one is only `1`. The heap removes this product immediately. The second product is then added, and its four portions fit inside the five available days. The final output contains only type 2.

For the exact boundary case:

```
2 3
2 6
3 3
```

The first product gives total `6` and capacity `6`, so it remains. The second product increases the total to `9`, while the capacity by day three is also `9`. Since equality is valid, no removal happens and both products are returned.
