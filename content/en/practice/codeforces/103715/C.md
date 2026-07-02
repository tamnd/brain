---
title: "CF 103715C - \u041a\u043e\u043d\u0442\u0440\u043e\u043b\u044c \u0441\u0430\u0445\u0430\u0440\u0430"
description: "We are given a list of sugar shops. Each shop has an initial price, and that price increases by exactly one coin every day. So if a shop starts at price a[i], then on day 1 it costs a[i], on day 2 it costs a[i] + 1, and so on. Every day, you go shopping with a fixed budget x."
date: "2026-07-02T09:26:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103715
codeforces_index: "C"
codeforces_contest_name: "\u0421\u0443\u0440\u0441\u043a\u0438\u0435 \u0442\u0430\u043b\u0430\u043d\u0442\u044b 2022"
rating: 0
weight: 103715
solve_time_s: 49
verified: true
draft: false
---

[CF 103715C - \u041a\u043e\u043d\u0442\u0440\u043e\u043b\u044c \u0441\u0430\u0445\u0430\u0440\u0430](https://codeforces.com/problemset/problem/103715/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of sugar shops. Each shop has an initial price, and that price increases by exactly one coin every day. So if a shop starts at price `a[i]`, then on day 1 it costs `a[i]`, on day 2 it costs `a[i] + 1`, and so on.

Every day, you go shopping with a fixed budget `x`. On that day, you can visit any subset of shops, but each shop can be used at most once per day, and you buy as many packs as possible without exceeding the budget. The next day, prices increase again, and you repeat the same process.

Eventually, all shops become too expensive to buy even a single pack within your budget. The task is to compute the total number of packs you manage to buy across all days until that moment.

The input consists of multiple independent test cases. Each test case gives the number of shops and your daily budget, followed by the initial prices of all shops. The output is a single integer per test case representing the total number of packs purchased over the entire process.

The constraints imply up to about two hundred thousand shops in total across all test cases. That rules out any simulation that iterates day by day. A naive daily simulation would be far too slow because the process can last up to `max(x - min(a[i]) + 1)` days, which in worst cases reaches up to one billion iterations.

A subtle edge case appears when some shops start already above the budget. For example, if `x = 5` and a shop has `a[i] = 10`, then it is never usable and contributes zero. Another case is when all `a[i]` are equal to `x`, meaning each shop can be bought only on day one and becomes unavailable immediately after.

## Approaches

A brute-force interpretation simulates the process day by day. On each day, we recompute the price of every shop and count how many we can afford. If there are `n` shops and `D` days, this costs `O(nD)` operations. Since `D` can be as large as `x`, which goes up to `10^9`, this approach is immediately impossible.

The key observation is that shops do not interact with each other in any meaningful way across days. Each shop evolves independently, and the decision for a shop depends only on whether its current price is within the budget. Instead of thinking in terms of days, we can invert the perspective and ask: for a fixed shop, how many days will it remain affordable?

For a shop with initial price `a[i]`, it is affordable on day `d` exactly when `a[i] + (d - 1) <= x`. This inequality can be solved directly, giving a contiguous range of valid days. That means each shop contributes independently to the total answer, and we can sum contributions across all shops without simulating time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (day simulation) | O(n · x) | O(1) | Too slow |
| Per-shop contribution counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `x`, then read the array `a` of initial prices. We process each test case independently because no state carries over.
2. For each shop `i`, determine how long it remains purchasable. We require `a[i] + (d - 1) <= x`, which rearranges to `d <= x - a[i] + 1`. This gives the exact number of days the shop can be used.
3. If `a[i] > x`, then the expression `x - a[i] + 1` becomes non-positive, which means the shop never contributes any purchases. In that case we treat its contribution as zero.
4. Sum the contribution of all shops. Since each shop contributes independently per day and we always buy whenever possible, this sum equals the total number of packs purchased across all days.
5. Output the final sum for the test case.

### Why it works

The crucial property is independence across shops. On any given day, every shop behaves deterministically: it is either affordable or not, and this condition depends only on the day index and its initial price. Because the budget resets daily and there is no competition between shops beyond the budget constraint, each shop contributes a fixed number of successful days. Summing these independent contributions exactly counts every purchase once, with no overlap or omission.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        
        ans = 0
        for v in a:
            if v <= x:
                ans += (x - v + 1)
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution directly implements the per-shop contribution formula. The only subtlety is guarding against negative contributions by checking `v <= x`. Without this, subtraction would incorrectly add negative values for overpriced shops.

The loop is linear per test case, and no sorting or auxiliary structure is required because each element is processed independently.

## Worked Examples

### Example 1

Suppose `n = 3`, `x = 5`, and `a = [1, 4, 6]`.

For each shop, we compute how many days it is affordable.

| Shop | a[i] | x - a[i] + 1 | Contribution |
| --- | --- | --- | --- |
| 1 | 1 | 5 | 5 |
| 2 | 4 | 2 | 2 |
| 3 | 6 | negative | 0 |

Total answer is `7`.

This trace shows that each shop contributes independently across days, and overpriced shops simply vanish from consideration.

### Example 2

Let `n = 4`, `x = 3`, `a = [3, 3, 3, 1]`.

| Shop | a[i] | x - a[i] + 1 | Contribution |
| --- | --- | --- | --- |
| 1 | 3 | 1 | 1 |
| 2 | 3 | 1 | 1 |
| 3 | 3 | 1 | 1 |
| 4 | 1 | 3 | 3 |

Total answer is `6`.

This example highlights that a very cheap shop contributes many more purchases because it remains under budget for more days.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each shop is processed once with constant work |
| Space | O(1) extra | Only a running sum is maintained |

The total `n` across test cases is at most `2 · 10^5`, so the solution easily fits within time limits. No sorting or preprocessing is needed, keeping memory and runtime minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import sys
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))
        ans = 0
        for v in a:
            if v <= x:
                ans += (x - v + 1)
        print(ans)

    return output.getvalue().strip()

# sample-like tests
assert run("1\n3 5\n1 4 6\n") == "7"
assert run("1\n4 3\n3 3 3 1\n") == "6"

# minimum case
assert run("1\n1 10\n10\n") == "1"

# all too expensive
assert run("1\n5 2\n5 6 7 8 9\n") == "0"

# all equal and cheap
assert run("1\n3 4\n2 2 2\n") == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 shop equal to x | 1 | single boundary purchase |
| all overpriced | 0 | no negative contributions |
| uniform cheap values | 9 | repeated daily accumulation |

## Edge Cases

One edge case is when all prices exceed the budget. For input like `n = 3, x = 5, a = [10, 20, 30]`, every term satisfies `a[i] > x`, so each contributes zero. The algorithm correctly skips all values due to the `v <= x` check.

Another edge case is when a shop starts exactly at the budget. For `a[i] = x`, the formula gives `x - x + 1 = 1`, meaning it contributes exactly once. The algorithm correctly counts a single purchase before it becomes unaffordable on the next day.

A final edge case is when `a[i] = 1` and `x` is large. In that case, the shop contributes `x` purchases, corresponding to one purchase per day until the price hits the limit. The algorithm accumulates this as a simple arithmetic expression without needing simulation.
