---
title: "CF 104014C - \u0412\u0435\u043d\u0434\u043e\u043c\u0430\u0442"
description: "We are given a vending machine that contains a collection of snack packs, each with a name and a price expressed in rubles and kopeks. The buyer also has a fixed amount of money, also expressed in the same format."
date: "2026-07-02T04:55:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104014
codeforces_index: "C"
codeforces_contest_name: "2022-2023 ICPC NERC, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0440\u0435\u0433\u0438\u043e\u043d\u0430 \u0438 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438"
rating: 0
weight: 104014
solve_time_s: 47
verified: true
draft: false
---

[CF 104014C - \u0412\u0435\u043d\u0434\u043e\u043c\u0430\u0442](https://codeforces.com/problemset/problem/104014/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a vending machine that contains a collection of snack packs, each with a name and a price expressed in rubles and kopeks. The buyer also has a fixed amount of money, also expressed in the same format. The task is to choose a single snack pack whose price is as large as possible but does not exceed the buyer’s money, with the additional constraint that the buyer must pay the exact amount, meaning no change is allowed.

The input therefore represents a constrained selection problem over a list of items, where each item has a numeric weight (its price), and we must find the maximum weight that is less than or equal to a fixed budget.

The structure of the constraints strongly suggests a linear scan solution. With up to 100,000 items, any approach that sorts or performs repeated searches per item would still be acceptable in O(N log N), but unnecessary overhead is avoidable because we only need a single best candidate. This immediately rules out anything quadratic such as pairwise comparisons or nested scans.

A subtle part of the problem is parsing the monetary format. Values are given as strings like “R,cc”, where rubles and kopeks must be normalized into a single integer value. A careless implementation might compare strings lexicographically or compare rubles and kopeks separately without proper normalization, which leads to incorrect ordering.

A few edge cases matter:

One edge case is when no item is affordable. For example, if the budget is 10,00 and all items cost more than that, the correct output is “-1”. A naive solution that initializes the best candidate incorrectly (for example, using index 0 without checking affordability) would incorrectly return an invalid snack.

Another edge case is when multiple items have the same maximum affordable price. For example, if two items both cost 50,00 and the budget is 50,00, either is valid. A buggy implementation might overwrite or skip valid candidates depending on comparison logic, but any stable “take maximum ≤ budget” logic works.

A final edge case is when prices are very close to the budget, especially around kopek boundaries, such as 99,99 versus 100,00. Incorrect parsing of kopeks can shift comparisons by a factor of 100 and silently break correctness.

## Approaches

The brute-force idea is straightforward: convert all prices into a single integer unit, then scan every item and check whether its price is within budget. If it is, compare it with the best candidate found so far and keep the maximum.

This works because the problem reduces to finding a maximum element under a constraint. However, any more complex strategy like sorting is unnecessary since we do not need ordering beyond a single maximum feasible value.

The brute-force approach already runs in O(N), which is optimal in terms of asymptotic complexity. There is no hidden structure like prefix sums or combinatorics; each item is independent. The only real improvement over a naive attempt is careful normalization of currency values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan | O(N) | O(1) | Accepted |
| Sorting then scan | O(N log N) | O(N) | Accepted but unnecessary |

## Algorithm Walkthrough

We convert all monetary values into integers representing total kopeks, then perform a single pass over the items while tracking the best valid candidate.

1. Parse the budget string into rubles and kopeks, then compute total budget in kopeks as `budget = R * 100 + cc`. This ensures uniform comparison across all items.
2. Initialize two variables: `best_price = -1` and `best_name = ""`. The sentinel `-1` guarantees that any valid item will replace it.
3. For each snack pack, parse its price string into the same integer format. This step must be identical to the budget conversion to preserve correctness.
4. Check whether the snack price is less than or equal to the budget. If it is not, skip it entirely since it cannot be purchased without change.
5. If the snack is affordable and its price is greater than `best_price`, update both `best_price` and `best_name` with this item. This greedy update works because we only care about the maximum feasible value.
6. After processing all items, output `best_name` if it was updated at least once, otherwise output “-1”.

### Why it works

At every step of the scan, `best_price` stores the largest affordable price seen so far. Because we only update it when encountering a strictly larger valid value, it is always the maximum over the processed prefix. When the scan ends, the prefix is the entire array, so the stored value is the global maximum under the budget constraint. No future operation can invalidate earlier comparisons since all items are independent and there are no side effects.

## Python Solution

```python
import sys
input = sys.stdin.readline

def parse_money(s):
    # format: R,cc
    r, cc = s.strip().split(',')
    return int(r) * 100 + int(cc)

n, budget_str = input().split()
n = int(n)
budget = parse_money(budget_str)

best_price = -1
best_name = ""

for _ in range(n):
    parts = input().split()
    name = parts[0]
    price = parse_money(parts[1])

    if price <= budget and price > best_price:
        best_price = price
        best_name = name

print(best_name if best_price != -1 else -1)
```

The core of the solution is the `parse_money` function, which normalizes all values into a single comparable integer. Without this step, comparing mixed ruble-kopek values would require lexicographic or tuple logic, which is more error-prone under manual implementation.

The scan maintains a single best candidate, updated only when a strictly better affordable price is found. This ensures correctness without needing sorting or additional data structures.

## Worked Examples

### Example 1

Input:

```
3 89,54
ChipsIT 69,69
YaChips 99,09
noChips 0,00
```

We convert budget to 8954 kopeks.

| Step | Name | Price (kopeks) | Affordable | Best Price | Best Name |
| --- | --- | --- | --- | --- | --- |
| 1 | ChipsIT | 6969 | Yes | 6969 | ChipsIT |
| 2 | YaChips | 9909 | No | 6969 | ChipsIT |
| 3 | noChips | 0 | Yes | 6969 | ChipsIT |

Final answer is `ChipsIT`.

This trace shows that the algorithm ignores unaffordable items and maintains the maximum among valid ones.

### Example 2

Input:

```
4 50,00
A 10,00
B 50,00
C 49,99
D 60,00
```

Budget is 5000 kopeks.

| Step | Name | Price | Affordable | Best Price | Best Name |
| --- | --- | --- | --- | --- | --- |
| 1 | A | 1000 | Yes | 1000 | A |
| 2 | B | 5000 | Yes | 5000 | B |
| 3 | C | 4999 | Yes | 5000 | B |
| 4 | D | 6000 | No | 5000 | B |

Final answer is `B`.

This demonstrates correct handling of equality at the budget boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each item is processed once with O(1) parsing and comparison |
| Space | O(1) | Only a few variables are stored regardless of input size |

The solution comfortably fits within constraints since 100,000 simple integer operations and string splits are easily handled within 2 seconds in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def parse_money(s):
        r, cc = s.strip().split(',')
        return int(r) * 100 + int(cc)

    n, budget_str = input().split()
    n = int(n)
    budget = parse_money(budget_str)

    best_price = -1
    best_name = ""

    for _ in range(n):
        parts = input().split()
        name = parts[0]
        price = parse_money(parts[1])
        if price <= budget and price > best_price:
            best_price = price
            best_name = name

    return str(best_name if best_price != -1 else -1)

# sample
assert run("""3 89,54
ChipsIT 69,69
YaChips 99,09
noChips 0,00
""") == "ChipsIT"

# minimum case
assert run("""1 10,00
A 10,00
""") == "A"

# no affordable
assert run("""2 5,00
A 10,00
B 20,00
""") == "-1"

# boundary kopeks
assert run("""3 1,00
A 0,99
B 1,01
C 1,00
""") == "C"

# multiple optimal
assert run("""3 50,00
A 50,00
B 50,00
C 10,00
""") in ["A", "B"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 item exact match | A | Single element correctness |
| No affordable items | -1 | Failure case handling |
| Kopek boundary | C | Correct numeric parsing |
| Duplicate optimal values | A or B | Stability under ties |

## Edge Cases

One important edge case is when all items are more expensive than the budget. For example, with budget 10,00 and items 20,00 and 30,00, the algorithm never updates `best_price`, which stays at -1. The output correctly becomes “-1” because no valid candidate is ever selected.

Another edge case occurs at exact equality. If the budget is 50,00 and an item costs exactly 50,00, the condition `price <= budget` ensures it is accepted. The scan updates `best_price` and this becomes the final answer unless a later equal or larger valid item appears.

A third edge case is parsing correctness. For input like 0,05, failure to pad or interpret kopeks as two-digit values would treat it as 5 instead of 0.05 rubles, breaking comparisons. The integer normalization into kopeks ensures that 0,05 becomes 5 consistently and comparisons remain correct.
