---
title: "CF 102297D - Lemonade Stand"
description: "We have a sequence of selling days. On day (i), exactly (ci) cups are requested. Every cup consumes (x) lemons and (s) ounces of sugar. Lemons can be purchased individually, while sugar is sold only in five-pound bags."
date: "2026-08-13T08:24:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102297
codeforces_index: "D"
codeforces_contest_name: "UCF Locals 2015"
rating: 0
weight: 102297
solve_time_s: 153
verified: true
draft: false
---

[CF 102297D - Lemonade Stand](https://codeforces.com/problemset/problem/102297/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of selling days. On day (i), exactly (c_i) cups are requested. Every cup consumes (x) lemons and (s) ounces of sugar. Lemons can be purchased individually, while sugar is sold only in five-pound bags. Since one pound contains 16 ounces, one sugar bag contains exactly 80 ounces.

Both ingredients can be bought in the morning before that day's customers arrive, and unused supplies remain available on later days. The price of a lemon and the price of a sugar bag can change from day to day. We know the entire sequence in advance and have unlimited capital, so the only question is when and how much to buy.

For each test case, the output is the minimum total number of cents needed to purchase enough lemons and sugar for every day's demand.

The constraints are small enough that even (O(d^2)) would fit comfortably because (d\le1000), but the structure allows an (O(d)) solution. There are at most 100 test cases, so an (O(d^2)) approach could perform around (100\times1000^2=10^8) inner-loop iterations in the theoretical maximum, which is unnecessarily close to the limits in Python. A linear scan is much safer. The official Codeforces archive lists a 1 second time limit and 256 MB memory limit.

The first subtle case is that sugar is sold in whole bags. Consider

```
1
1 1 10
1 1 7
```

One cup needs 10 ounces of sugar, so one entire 80-ounce bag is necessary. The lemon costs 1 cent and the sugar bag costs 7 cents, giving an answer of 8. A careless solution that multiplies the required 10 ounces by the price of a bag would produce 71 cents, while a solution that rounds each day's demand independently after some transformation can also mishandle the unused 70 ounces.

A second edge case occurs when several days together still fit in one sugar bag. Consider

```
1
2 1 10
1 10 100
7 20 99
```

The first day needs 10 ounces and the second needs 70, so exactly 80 ounces are needed in total. One bag bought on day 1 is enough for both days, giving 10 cents for lemons and 100 cents for sugar, for a total of 110 cents. A solution that rounds each day's sugar requirement separately would buy two bags and get 209 cents instead.

A third case is when a cheaper price appears later. Consider

```
1
2 1 1
1 50 500
80 1 1
```

The first day forces one lemon and one sugar bag to be bought at the first day's prices. On day 2 the cheaper prices can be used for the additional requirements. The answer is 631 cents. A strategy that buys several bags early merely because the first day is cheap relative to the future would miss the fact that waiting is allowed and a later price can be even lower.

## Approaches

A direct brute-force solution could enumerate every possible purchase schedule. For sugar, let (B) be the total number of bags required over all days. Every bag can in principle be assigned to one of the (d) purchase days, after which we check whether the resulting schedule has enough sugar on every day and calculate its cost. The total number of assignments is at most (d^B). Since total demand can reach (1000\cdot1000\cdot10=10^7) ounces, (B) can reach (\lceil10^7/80\rceil=125000). With (d=1000), this gives up to (1000^{125000}) assignments for the sugar alone. The brute force is correct because it explicitly considers every legal schedule, but it becomes useless long before the maximum constraints.

The useful observation is that supplies of the same ingredient are interchangeable. For lemons, there is no packaging restriction at all. Suppose day (i) requires (q_i=c_i x) new lemons. Those particular (q_i) lemons must have been purchased no later than day (i), so the cheapest possible price for each is simply the minimum lemon price among days (1) through (i). We can buy them on whichever earlier day has that minimum price.

Sugar is almost the same, except that bags have capacity 80. Let (S_i) be the total number of ounces needed through day (i). By the start of day (i), at least

[
B_i=\left\lceil\frac{S_i}{80}\right\rceil
]

bags must have been purchased. On the previous day, only (B_{i-1}) bags were forced. Thus exactly (B_i-B_{i-1}) additional bags become necessary at day (i). Each of those bags can be purchased on any day from 1 through (i), so their cheapest possible price is the minimum sugar-bag price seen so far.

The key point is that we do not round each day's sugar demand separately. We round the cumulative demand. This captures the fact that unused ounces from a bag carry into later days.

The two ingredients are independent, so we can process them simultaneously in one scan. For lemons, add the day's required lemons multiplied by the cheapest lemon price seen so far. For sugar, update the cumulative ounces, compute the new required number of bags, and charge only for the newly required bags at the cheapest sugar price seen so far.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(d^B)) for sugar | (O(B)) | Too slow |
| Optimal | (O(d)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Initialize the minimum lemon price and minimum sugar-bag price to a value larger than every possible input price. Also initialize the cumulative sugar demand and the number of sugar bags already required to zero.
2. Read one day at a time. For day (i), update the minimum lemon price to the cheapest lemon price among days (1) through (i), and do the same for sugar bags. A supply needed on day (i) may have been purchased on any earlier day, so these prefix minima describe the cheapest legal purchase price.
3. Compute the number of new lemons required on this day as (c_i x). Multiply that quantity by the current minimum lemon price and add it to the answer. Lemons are individual units, so there is no rounding or inventory-state complication.
4. Add (c_i s) to the cumulative sugar demand. Convert that cumulative amount into the minimum number of bags using
[
B_i=\left\lceil\frac{S_i}{80}\right\rceil.
]
In integer arithmetic this is `(S_i + 79) // 80`.
5. Compute `new_bags = B_i - B_previous`. Only these newly required bags add to the cost. Multiply them by the cheapest sugar-bag price seen so far and add that amount to the answer.
6. Store (B_i) as the previous bag count and continue to the next day. After the final day, the accumulated answer is the minimum cost for the entire test case.

### Why it works

For lemons, every newly required lemon on day (i) must be purchased by day (i), and all earlier purchase days are unrestricted in quantity. Thus its minimum possible price is exactly the minimum lemon price in the prefix ending at (i). Buying the required number at that price is both feasible and optimal.

For sugar, after day (i) the total demand is (S_i) ounces, so every feasible schedule must own at least (\lceil S_i/80\rceil) bags. The difference (B_i-B_{i-1}) is exactly the number of additional bags that any feasible schedule must have acquired by day (i). Each such bag may be purchased on any day in the prefix, so its cheapest possible cost is the prefix minimum sugar price. Buying those bags at a day attaining that minimum is feasible because supplies carry forward and storage is unlimited. Consequently, every charged bag has the smallest price legally available for it, while every bag that is necessary is charged exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30
BAG_OUNCES = 80

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        d, x, s = map(int, input().split())

        min_lemon_price = INF
        min_sugar_price = INF

        cumulative_sugar = 0
        previous_bags = 0
        answer = 0

        for _ in range(d):
            c, pl, ps = map(int, input().split())

            min_lemon_price = min(min_lemon_price, pl)
            min_sugar_price = min(min_sugar_price, ps)

            lemons_needed = c * x
            answer += lemons_needed * min_lemon_price

            cumulative_sugar += c * s
            required_bags = (cumulative_sugar + BAG_OUNCES - 1) // BAG_OUNCES

            new_bags = required_bags - previous_bags
            answer += new_bags * min_sugar_price

            previous_bags = required_bags

        out.append(str(answer))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input loop processes exactly one day per iteration, so the algorithm never needs to store the entire sequence. `min_lemon_price` and `min_sugar_price` represent the cheapest purchase opportunity available for the current day.

The lemon calculation uses `c * x` because every cup consumes exactly `x` individual lemons. There is no reason to track leftover lemons separately. Any lemons bought cheaply for an earlier day can simply remain available, and the prefix-minimum argument already accounts for that.

For sugar, `cumulative_sugar` is the crucial state. The expression `(cumulative_sugar + 79) // 80` performs a ceiling division by 80. Using `c * s` directly in the rounding calculation would be incorrect because a partially used bag can satisfy later demand.

`new_bags` is the difference between the current cumulative requirement and the previous cumulative requirement. This prevents us from charging again for bags whose unused sugar is already available. It also handles exact multiples of 80 correctly. If cumulative demand changes from 79 to 80 ounces, the required bag count stays at one, so no new bag is purchased.

Python integers have arbitrary precision, so even the largest possible total cost is handled without overflow. The largest values remain far below any practical memory concern, and the algorithm only keeps a constant number of integer variables.

## Worked Examples

The official contest material gives the sample outputs as 31977 and 1347.

For Sample 1,

```
3 3 2
200 10 399
300 8 499
400 12 499
```

the state evolves as follows.

| Day | Cups | Lemon price | Min lemon price | Sugar price | Min sugar price | Cumulative sugar | Required bags | New bags | Daily cost |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 200 | 10 | 10 | 399 | 399 | 400 | 5 | 5 | 7995 |
| 2 | 300 | 8 | 8 | 499 | 399 | 1000 | 13 | 8 | 10392 |
| 3 | 400 | 12 | 8 | 499 | 399 | 1800 | 23 | 10 | 13590 |

The lemon costs are 6000, 7200, and 9600 cents. Sugar costs are 1995, 3192, and 3990 cents. Their combined total is (7995+10392+13590=31977). The second day's cheaper lemon price affects all newly required lemons from that day onward, while the sugar price of 399 remains the prefix minimum throughout the test.

For Sample 2,

```
2 5 10
9 10 199
8 20 99
```

the trace is:

| Day | Cups | Min lemon price | Cumulative sugar | Min sugar price | Required bags | New bags | Daily cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 9 | 10 | 90 | 199 | 2 | 2 | 848 |
| 2 | 8 | 10 | 170 | 99 | 3 | 1 | 499 |

The first day requires 45 lemons, costing 450 cents, and 90 ounces of sugar, requiring two bags at 199 cents each. On the second day the lemon price is worse, so the prefix minimum remains 10. The sugar price falls to 99, so the one additional bag costs only 99 cents. The total is (848+499=1347).

This example demonstrates why the algorithm tracks cumulative sugar rather than independently rounding each day. The first two bags are already enough to cover the first 160 ounces, so only one additional bag is needed after the second day's demand is included.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(d)) per test case | Every day is processed once with constant work |
| Space | (O(1)) | Only prefix prices, cumulative demand, and a few counters are stored |

With (d\le1000), the linear scan performs at most 1000 iterations per test case. Even with 100 test cases, that is only 100000 day records, so the solution is comfortably within the stated constraints and uses negligible memory.

## Test Cases

The following tests assume the submitted solution is saved as `lemonade_solution.py` and exposes `solve()` as shown above.

```python
# helper: run solution on input string, return output string
import sys
import io
from lemonade_solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run(
    """2
3 3 2
200 10 399
300 8 499
400 12 499
2 5 10
9 10 199
8 20 99
"""
) == "31977\n1347", "provided samples"

# Minimum-size input
assert run(
    """1
1 1 1
1 7 1
"""
) == "8", "minimum-size case"

# All values equal
assert run(
    """1
2 2 3
10 5 100
10 5 100
"""
) == "300", "all-equal values"

# Exactly 80 ounces across two days, so only one sugar bag is needed
assert run(
    """1
2 1 10
1 10 100
7 20 99
"""
) == "180", "exact bag boundary"

# A cheaper later price must be used for later requirements
assert run(
    """1
2 1 1
1 50 500
80 1 1
"""
) == "631", "later cheaper prices"

# Maximum-size dimensions and values.
# 1000 days, 1000 cups/day, 10 lemons/cup, 10 ounces/cup.
# Lemon cost = 10,000,000 * 50 = 500,000,000.
# Sugar demand = 10,000,000 ounces = 125,000 bags.
# Sugar cost = 125,000 * 500 = 62,500,000.
# Total = 562,500,000.
max_case = ["1", "1000 10 10"]
max_case.extend(["1000 50 500"] * 1000)

assert run("\n".join(max_case) + "\n") == "562500000", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 1 / 1 7 1` | `8` | Minimum input and one partially used sugar bag |
| `2 2 3` with two identical days | `300` | Equal prices and cumulative inventory |
| `2 1 10 / 1 10 100 / 7 20 99` | `180` | Exact 80-ounce boundary and no unnecessary second bag |
| `2 1 1 / 1 50 500 / 80 1 1` | `631` | Later cheaper prices and waiting to buy additional supplies |
| 1000 identical maximum-value days | `562500000` | Maximum day count, demand, ingredient requirements, and prices |

## Edge Cases

The first edge case is a partially filled sugar bag. For

```
1
1 1 10
1 1 7
```

the cumulative sugar demand is 10 ounces. The algorithm computes ((10+79)//80=1), so one bag is charged at 7 cents. The lemon cost is 1 cent, giving 8 cents. The unused 70 ounces remain available, but there is no later demand, so they simply remain unused.

The second edge case is the exact bag boundary:

```
1
2 1 10
1 10 100
7 20 99
```

After day 1, cumulative demand is 10 ounces, so one bag is required. After day 2, cumulative demand becomes exactly 80 ounces, and the required bag count is still one. Thus `new_bags` is zero on day 2, despite there being a new 70-ounce demand. The one existing bag already contains exactly enough sugar. The lemon costs are 10 and 70 cents, because the cheapest lemon price seen so far is 10, and the sugar cost is only the first day's 100 cents. The total is 180.

The third edge case tests a future price decrease:

```
1
2 1 1
1 50 500
80 1 1
```

After day 1, one lemon and one sugar bag are unavoidable, costing 50 and 500 cents. After day 2, 81 ounces of sugar have been requested, so two bags are required in total. Only one new bag is needed, and the current prefix minimum sugar price is now 1 cent. The second day's 80 lemons also use the new prefix minimum lemon price of 1 cent each. The total is (50+500+80+1=631). This is exactly the situation where buying extra bags on day 1 would be wasteful.

The final boundary case is the largest possible input size. With 1000 days of 1000 cups, (x=s=10), every day requires 10000 lemons and 10000 ounces of sugar. Over the entire period this is 10,000,000 lemons and 10,000,000 ounces of sugar. The latter requires exactly 125,000 bags because (10,000,000/80=125,000). At constant prices of 50 cents per lemon and 500 cents per bag, the answer is 500,000,000 plus 62,500,000, or 562,500,000 cents. The algorithm reaches this result with one pass and never constructs an inventory array.
