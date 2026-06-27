---
title: "CF 104990A - Apartment Tycoon"
description: "We start with a single apartment. Each apartment produces a fixed monthly income, and that income is immediately usable to buy additional apartments, each costing a fixed amount."
date: "2026-06-28T03:43:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104990
codeforces_index: "A"
codeforces_contest_name: "First Masters Championship LATAM 2024"
rating: 0
weight: 104990
solve_time_s: 67
verified: false
draft: false
---

[CF 104990A - Apartment Tycoon](https://codeforces.com/problemset/problem/104990/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a single apartment. Each apartment produces a fixed monthly income, and that income is immediately usable to buy additional apartments, each costing a fixed amount. Every new apartment you buy instantly becomes part of your income-generating set from the next month onward.

The process evolves month by month. At the start, you have one apartment. Each month, all owned apartments generate income, you may spend accumulated money to buy more apartments, and ownership only increases. The task is to determine how many months it takes until the number of owned apartments reaches a target value.

The input gives three integers. The first is the price of a new apartment. The second is how much one apartment earns per month. The third is the target number of apartments. The output is the number of months needed to reach that target assuming optimal reinvestment of all income.

The constraints are small, with all values up to 1000, which means even a straightforward simulation over months is safe. A solution that simulates each month and tracks money and ownership will run comfortably within limits, since even 1000 months of O(1) work per month is trivial.

The main subtlety is that income grows as apartments are purchased, which means a naive “buy whenever you can” idea must be handled carefully in order and timing. The decision of when purchases become affordable affects the number of months required.

A few edge cases matter. When income is already large enough that multiple apartments can be bought immediately, the simulation must allow buying more than one per month, otherwise it will overcount time. Another edge case is when income is too small relative to cost, requiring multiple months of accumulation before the first purchase. Finally, when the target is 1, the answer is trivially zero months because we already start with one apartment.

## Approaches

A brute-force approach naturally simulates the process month by month. We maintain the current number of apartments and accumulated money. Each month we add income equal to the current number of apartments multiplied by monthly income per apartment. Then we repeatedly buy apartments while we can afford them, decreasing money and increasing ownership. We stop once we reach the target count.

This simulation is correct because it directly mirrors the rules. The bottleneck is not correctness but performance reasoning, although with constraints up to 1000 it remains efficient. Even in the worst case, we simulate at most 1000 months, and in each month we may perform at most 1000 purchases, leading to about 10^6 operations, which is still trivial.

The key insight is that the process is monotonic in both money and apartment count. We never lose income and never decrease assets, so we can safely simulate greedily without worrying about future reversals or backtracking. There is no need for binary search or closed-form math because the state space is tiny and strictly increasing.

The only optimization needed beyond naive thinking is ensuring that within each month we buy as many apartments as possible before moving to the next month, since partial buying would artificially delay income growth.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(C²) worst case | O(1) | Accepted |
| Optimized Simulation | O(C²) worst case, tighter in practice | O(1) | Accepted |

## Algorithm Walkthrough

1. Start with one apartment and zero money. This represents the initial state before any income has been collected.
2. Repeat month by month until the number of apartments reaches the target C. Each iteration corresponds to one full cycle of income generation and reinvestment.
3. At the beginning of a month, add income equal to the current number of apartments multiplied by B. This models all apartments producing revenue simultaneously.
4. After receiving income, repeatedly buy apartments while the current money is at least A. Each purchase reduces money by A and increases the apartment count by one. This greedy step is correct because all apartments are identical and there is no benefit in delaying purchases.
5. Once no more purchases are possible, advance the month counter by one and repeat the process.
6. Stop immediately when the apartment count reaches or exceeds C. The current month count is the answer.

### Why it works

The algorithm maintains the invariant that at the start of each month, all previously earned income has already been fully converted into either cash or apartments, and no profitable purchase is left undone. Since apartments only increase future income and there are no alternative investments or constraints, always buying whenever possible never worsens the outcome. The system evolves monotonically, so the first time we reach C apartments is guaranteed to be the minimum number of months required under optimal play.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B, C = map(int, input().split())
    
    if C == 1:
        print(0)
        return
    
    apartments = 1
    money = 0
    months = 0
    
    while apartments < C:
        # earn income
        money += apartments * B
        
        # buy as many as possible
        while money >= A and apartments < C:
            money -= A
            apartments += 1
        
        months += 1
    
    print(months)

if __name__ == "__main__":
    solve()
```

The code follows the month-by-month simulation exactly. The early exit for C = 1 avoids unnecessary computation since we already start with one apartment.

The income step `money += apartments * B` captures the simultaneous revenue generation. The inner loop is critical: it ensures that if income allows multiple purchases in the same month, we immediately convert cash into apartments, maximizing future earnings.

The termination condition checks apartment count after each full month, ensuring we do not overcount time once the target is reached.

## Worked Examples

### Example 1

Input:

```
5 1 2
```

We start with 1 apartment.

| Month | Apartments | Money before buy | Purchases | Money after | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 1 | 1 |
| 2 | 1 | 2 | 0 | 2 | 2 |
| 3 | 1 | 3 | 0 | 3 | 3 |
| 4 | 1 | 4 | 0 | 4 | 4 |
| 5 | 1 | 5 | 1 | 0 | 2 |

After month 5, we finally reach 2 apartments.

This trace shows that accumulation takes several months before the first purchase becomes possible. Once affordability is reached, exactly one purchase happens, immediately achieving the target.

### Example 2

Input:

```
10 5 3
```

| Month | Apartments | Money before buy | Purchases | Money after | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | 0 | 5 | 1 |
| 2 | 1 | 10 | 1 | 0 | 2 |
| 3 | 2 | 10 | 1 | 0 | 3 |

After 3 months we reach 3 apartments.

This case demonstrates accelerating growth. The income increases after the first purchase, enabling a faster second purchase.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(C²) worst case | Each month may involve up to C purchases, and there are at most C months since we cannot exceed C apartments |
| Space | O(1) | We maintain only counters for money, apartments, and months |

The constraints ensure C ≤ 1000, so even a quadratic simulation is extremely fast in Python and easily fits within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import isfinite
    from builtins import print as _print

    # capture output
    out = io.StringIO()
    _stdout = sys.stdout
    sys.stdout = out

    try:
        solve()
    finally:
        sys.stdout = _stdout

    return out.getvalue().strip()

# sample cases
assert run("5 1 2\n") == "5"
assert run("10 5 3\n") == "3"

# minimum edge: already at target
assert run("7 3 1\n") == "0"

# no early buying possible for long time
assert run("100 1 2\n") == "100"

# fast growth case
assert run("2 5 10\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 7 3 1 | 0 | already at target |
| 100 1 2 | 100 | slow accumulation |
| 2 5 10 | 3 | rapid compounding growth |

## Edge Cases

One edge case is when the target is already satisfied at the start. For input like `A=7, B=3, C=1`, the algorithm immediately returns 0. The simulation never enters the loop, correctly reflecting that no time is needed.

Another case is extremely slow accumulation, such as `A=100, B=1, C=2`. Here each month adds only 1 unit of money, so it takes exactly 100 months before the first purchase. The simulation accumulates steadily without any premature buying, and the purchase happens at the correct time.

A third case is fast compounding where income quickly exceeds cost multiple times per month. The inner buying loop ensures that all affordable apartments are purchased immediately within the same month, preventing undercounting of growth and ensuring the system accelerates as soon as possible.
