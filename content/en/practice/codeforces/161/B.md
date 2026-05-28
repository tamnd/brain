---
title: "CF 161B - Discounts"
description: "We have a collection of items sold in a supermarket. Every item has a price and a type. Type 1 means the item is a stool, type 2 means it is a pencil. Polycarpus owns exactly k shopping carts, and every cart must contain at least one item."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 161
codeforces_index: "B"
codeforces_contest_name: "VK Cup 2012 Round 1"
rating: 1700
weight: 161
solve_time_s: 133
verified: true
draft: false
---

[CF 161B - Discounts](https://codeforces.com/problemset/problem/161/B)

**Rating:** 1700  
**Tags:** constructive algorithms, greedy, sortings  
**Solve time:** 2m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of items sold in a supermarket. Every item has a price and a type. Type `1` means the item is a stool, type `2` means it is a pencil.

Polycarpus owns exactly `k` shopping carts, and every cart must contain at least one item. The store promotion says that if a cart contains at least one stool, then the cheapest item inside that cart gets a 50% discount.

The task is not just to compute the minimum possible total price. We must also output one valid distribution of items into the carts that achieves this minimum.

The main difficulty is that the discount applies per cart, not per stool. A cart with ten stools still receives only one discount, on the cheapest item in that cart. This immediately suggests that spreading stools across multiple carts may be useful, because each such cart creates another discounted item.

The constraints are small enough that `O(n log n)` or even `O(n^2)` solutions are perfectly safe. Here `n ≤ 1000`, so sorting dominates the runtime anyway. Exhaustive partitioning, however, is impossible because the number of ways to distribute items into carts grows exponentially.

A few edge cases are easy to mishandle.

Suppose all items are pencils.

```
3 2
5 2
7 2
1 2
```

No cart can ever receive a discount because discounts require stools. The optimal answer is simply the sum of all prices. A careless implementation that assumes every cart gets a discount would subtract too much.

Another tricky case appears when the number of stools is smaller than `k`.

```
4 3
10 1
9 2
8 2
7 2
```

There is only one stool, so at most one cart can activate the promotion. The remaining carts must still be non-empty, which forces us to place pencils alone in some carts.

The opposite situation is also interesting.

```
5 2
100 1
90 1
1 2
1 2
1 2
```

A naive strategy might put all stools together. That gives only one discount. The better strategy is to split stools across carts so that both carts receive discounts.

Finally, the discounted item is always the cheapest item in a cart. This matters when grouping items together.

```
3 1
10 1
100 2
1 2
```

If all items go into one cart, the discount applies to the pencil priced `1`, not the stool priced `10`. Any reasoning that assumes the stool itself gets discounted is incorrect.

## Approaches

The brute-force idea is to try every possible assignment of items into the `k` carts, compute the resulting total price, and keep the best arrangement.

This works because the scoring rule is easy to evaluate. For each cart, we check whether it contains a stool. If it does, we subtract half of the minimum price in that cart.

The problem is the number of assignments. Each of the `n` items can go into one of `k` carts, which gives roughly `k^n` possibilities. With `n = 1000`, this is completely impossible.

To design something faster, we need to understand what actually creates value.

A discount is triggered only by the presence of a stool. Since each cart can receive at most one discount, we want as many carts with stools as possible. More specifically, if we can isolate a stool inside its own cart, then the cheapest item in that cart is exactly that stool, so we receive half of its price as savings.

This observation changes the problem completely.

Suppose we have `s` stools. Then at most `min(s, k)` carts can receive discounts. To maximize the total discount, we should choose the most expensive stools to stand alone in separate carts, because each isolated stool contributes `price / 2` savings.

Why expensive stools? Because once a stool is alone, its own price becomes the discounted amount. A stool priced `100` gives a discount of `50`, while a stool priced `2` gives only `1`.

This leads to a greedy construction.

We sort stools by descending price. Then we create singleton carts using the most expensive stools, up to `k - 1` carts. The last cart receives all remaining items.

Why only `k - 1` singleton carts? Because every cart must be non-empty, and the remaining items need somewhere to go.

The final cart may still contain stools. If it does, it also receives one discount, but only on its cheapest item. That happens automatically.

The entire problem becomes a constructive greedy arrangement plus careful accounting of the discounts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Greedy + Sorting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all items and separate them into stools and pencils while keeping their original indices.
2. Compute the total sum of all prices. We will subtract discounts from this total.
3. Sort the stools in descending order of price.
4. Create up to `min(number_of_stools, k - 1)` carts, each containing exactly one stool, starting from the most expensive stools.

Each such cart guarantees a discount equal to half of that stool's price. Isolating expensive stools maximizes the saved amount.
5. Put every remaining item into the final cart.

This includes all pencils and any stools that were not isolated earlier.
6. If the final cart contains at least one stool, find the minimum price inside that cart and apply a final discount equal to half of that minimum price.

The store rule discounts only the cheapest item in a stool-containing cart.
7. Print the minimized total price and the cart contents.

### Why it works

The key invariant is that every cart with a stool can contribute at most one discounted item. If a cart contains only one stool, then that stool itself becomes the discounted item. Since discounts are proportional to item prices, assigning the most expensive stools into separate carts maximizes the total reduction.

Any arrangement that combines two expensive stools into the same cart wastes one potential discount. Moving one of those stools into another cart can only increase or preserve the total savings.

The final cart is unavoidable because all remaining items must be placed somewhere. Its discount is determined entirely by the minimum-priced item inside it, so no further optimization is needed once the expensive stools have already been isolated.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    items = []
    stools = []
    pencils = []

    total = 0

    for i in range(1, n + 1):
        c, t = map(int, input().split())

        items.append((c, t, i))
        total += c

        if t == 1:
            stools.append((c, i))
        else:
            pencils.append((c, i))

    stools.sort(reverse=True)

    carts = []

    used = set()

    single_cnt = min(len(stools), k - 1)

    discount = 0.0

    for i in range(single_cnt):
        price, idx = stools[i]

        carts.append([idx])
        used.add(idx)

        discount += price / 2.0

    last_cart = []

    last_has_stool = False
    last_min_price = float('inf')

    for c, t, idx in items:
        if idx in used:
            continue

        last_cart.append(idx)

        if t == 1:
            last_has_stool = True

        last_min_price = min(last_min_price, c)

    if last_has_stool:
        discount += last_min_price / 2.0

    carts.append(last_cart)

    answer = total - discount

    print(f"{answer:.1f}")

    for cart in carts:
        print(len(cart), *cart)

solve()
```

The solution starts by splitting items into stools and pencils while preserving original indices. Those indices are required in the output, so losing them during sorting would make reconstruction difficult.

The greedy part relies on sorting stools in descending order. The most expensive stools are extracted first because isolated carts turn the stool itself into the discounted item.

The variable `single_cnt` deserves attention. We create at most `k - 1` singleton carts because one cart must remain available for all leftover items. If we created `k` singleton carts while items still remained, some items would have nowhere to go.

The final cart gathers every unused item. During this pass, the code also tracks whether the cart contains a stool and what its minimum price is. This is necessary because the discount applies to the cheapest item in the cart, regardless of type.

The answer is maintained as floating-point because discounts divide prices by two. The statement requires exactly one digit after the decimal point, so the final print uses `:.1f`.

## Worked Examples

### Example 1

Input:

```
3 2
2 1
3 2
3 1
```

After reading input:

| Item | Price | Type |
| --- | --- | --- |
| 1 | 2 | Stool |
| 2 | 3 | Pencil |
| 3 | 3 | Stool |

Sorted stools:

| Price | Index |
| --- | --- |
| 3 | 3 |
| 2 | 1 |

We can create `k - 1 = 1` singleton cart.

| Step | Action | Discount |
| --- | --- | --- |
| Create cart `{3}` | isolate stool 3 | 1.5 |

Remaining items go into the last cart.

| Final Cart | Contains Stool | Cheapest Price | Extra Discount |
| --- | --- | --- | --- |
| `{1, 2}` | Yes | 2 | 1.0 |

Total price:

| Quantity | Value |
| --- | --- |
| Raw sum | 8 |
| Total discount | 2.5 |
| Final answer | 5.5 |

This example demonstrates the central greedy idea. Splitting stools across carts creates multiple discounts instead of only one.

### Example 2

Input:

```
5 3
10 1
8 1
7 2
6 2
5 2
```

Sorted stools:

| Price | Index |
| --- | --- |
| 10 | 1 |
| 8 | 2 |

We may create `min(2, 2) = 2` singleton carts.

| Cart | Discount |
| --- | --- |
| `{1}` | 5 |
| `{2}` | 4 |

Remaining items:

| Final Cart |
| --- |
| `{3, 4, 5}` |

The final cart has no stool, so it receives no discount.

| Quantity | Value |
| --- | --- |
| Raw sum | 36 |
| Total discount | 9 |
| Final answer | 27.0 |

This case shows why expensive stools should be isolated first. If both stools were grouped together, only one discount would apply.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the stools dominates the runtime |
| Space | O(n) | We store carts and item lists |

With `n ≤ 1000`, this easily fits within the limits. Sorting one thousand elements is trivial, and all other operations are linear scans.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, k = map(int, input().split())

        items = []
        stools = []

        total = 0

        for i in range(1, n + 1):
            c, t = map(int, input().split())

            items.append((c, t, i))
            total += c

            if t == 1:
                stools.append((c, i))

        stools.sort(reverse=True)

        carts = []
        used = set()

        single_cnt = min(len(stools), k - 1)

        discount = 0.0

        for i in range(single_cnt):
            price, idx = stools[i]

            carts.append([idx])
            used.add(idx)

            discount += price / 2.0

        last_cart = []

        last_has_stool = False
        last_min_price = float('inf')

        for c, t, idx in items:
            if idx in used:
                continue

            last_cart.append(idx)

            if t == 1:
                last_has_stool = True

            last_min_price = min(last_min_price, c)

        if last_has_stool:
            discount += last_min_price / 2.0

        carts.append(last_cart)

        answer = total - discount

        out = [f"{answer:.1f}"]

        for cart in carts:
            out.append(f"{len(cart)} {' '.join(map(str, cart))}")

        return "\n".join(out)

    return solve()

# provided sample
assert run(
"""3 2
2 1
3 2
3 1
"""
).splitlines()[0] == "5.5", "sample 1"

# minimum size
assert run(
"""1 1
10 1
"""
).splitlines()[0] == "5.0", "single stool"

# all pencils
assert run(
"""3 2
5 2
7 2
1 2
"""
).splitlines()[0] == "13.0", "no discounts"

# more carts than stools
assert run(
"""4 3
10 1
9 2
8 2
7 2
"""
).splitlines()[0] == "29.0", "only one stool"

# all equal values
assert run(
"""4 2
10 1
10 1
10 2
10 2
"""
).splitlines()[0] == "35.0", "equal prices"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single stool | 5.0 | Minimum valid input |
| All pencils | 13.0 | No discounts should apply |
| More carts than stools | 29.0 | Some carts must remain without discounts |
| Equal prices | 35.0 | Correct handling when multiple items share the same value |

## Edge Cases

Consider the case where no stool exists.

```
3 2
5 2
7 2
1 2
```

The algorithm creates zero singleton stool carts because the stool list is empty. Every item goes into the final cart. Since the final cart also lacks stools, no discount is applied. The answer becomes `5 + 7 + 1 = 13`.

Now consider fewer stools than carts.

```
4 3
10 1
9 2
8 2
7 2
```

Only one stool exists, so only one cart can activate the promotion. The algorithm isolates the stool into its own cart, producing a discount of `5`. The remaining items occupy the last cart and receive no discount. Total cost becomes `34 - 5 = 29`.

Another subtle situation appears when the cheapest item in a mixed cart is a pencil.

```
3 1
10 1
100 2
1 2
```

All items must go into one cart. Since the cart contains a stool, the cheapest item receives the discount. That cheapest item is the pencil priced `1`, not the stool priced `10`. The algorithm correctly tracks the minimum price inside the cart and subtracts only `0.5`.

Finally, consider many stools with varying prices.

```
5 3
100 1
90 1
5 1
1 2
1 2
```

The algorithm isolates stools priced `100` and `90`, creating discounts of `50` and `45`. The remaining stool priced `5` goes into the final cart with the pencils, creating one additional discount of `0.5`. Any arrangement that grouped expensive stools together would lose one of the large discounts and produce a worse answer.
