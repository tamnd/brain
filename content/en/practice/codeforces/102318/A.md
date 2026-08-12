---
title: "CF 102318A - Electric Bill"
description: "The problem models two households whose electricity consumptions are positive integers. The electricity company uses a progressive tariff: the first 100 CWh cost 2 Americus each, the next 9,900 cost 3 each, the next 990,000 cost 5 each, and every unit beyond 1,000,000 costs 7."
date: "2026-08-13T05:08:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102318
codeforces_index: "A"
codeforces_contest_name: "UCF Locals 2017"
rating: 0
weight: 102318
solve_time_s: 193
verified: true
draft: false
---

[CF 102318A - Electric Bill](https://codeforces.com/problemset/problem/102318/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models two households whose electricity consumptions are positive integers. The electricity company uses a progressive tariff: the first 100 CWh cost 2 Americus each, the next 9,900 cost 3 each, the next 990,000 cost 5 each, and every unit beyond 1,000,000 costs 7. The original problem gives us two numbers, `A` and `B`. `A` is the bill that would result if both households' consumptions were combined before applying the tariff. `B` is the absolute difference between their individual bills. We are guaranteed that exactly one pair of consumptions produces these two values, and we must output the smaller household's individual bill. The input contains multiple test cases and ends with `0 0`.

The first task is to recover the total consumption from `A`. This is possible because the tariff function is strictly increasing. Once the total consumption is known, call it `C`, the two individual consumptions must be `x` and `C - x`. Since we are promised that our consumption is no greater than the neighbor's, we only need to consider `1 <= x <= C / 2`.

The numeric bound is `A <= 10^9`. That means the total consumption can be on the order of 10^8, because the highest tariff charges 7 per unit. A linear scan over every possible `x` would consequently require tens of millions of iterations for one test case. With a 1 second limit, that is far too much work, especially in Python. The structure of the tariff instead gives us a monotone function, which lets us use binary search and reduce the search to roughly 30 iterations.

There are several boundary cases where a direct implementation can fail. The first is the smallest valid non-terminating case. For

```
6 2
```

the combined consumption is 3, because `bill(3) = 6`. The only possible split is 1 and 2, whose bills are 2 and 4, so the answer is

```
2
```

A careless implementation that assumes every test case has a large enough consumption to enter the second tariff range could calculate this incorrectly.

The tariff boundary at exactly 100 units is another common source of off-by-one errors. Consider

```
200 4
```

The combined consumption is 100. The unique split is 49 and 51. Their bills are 98 and 102, giving a difference of 4, so the answer is

```
98
```

Using `100` as the size of the first range rather than charging exactly the first 100 units at rate 2 is necessary here.

The boundary immediately after the first tariff range is similarly significant. The combined consumption of 201 units has bill `503`, since the first 100 units cost 200 and the next 101 cost 303. A solution that accidentally uses the second rate for the 100th unit will shift every later calculation.

The highest tariff range also matters. For example,

```
4979977 4979968
```

corresponds to consumptions of 1,000,010 and 1, so the smaller household pays 2. The combined consumption crosses the 1,000,000-unit boundary, so the final tariff branch must be implemented correctly. This boundary case is useful because an implementation can appear correct on ordinary values while failing as soon as consumption exceeds 1,000,000.

Finally, `0 0` is not an ordinary case. It is the input terminator. In particular, although equal bills would produce `B = 0`, regular test cases have positive `B`, so the only zero-difference input we should expect is the terminating pair.

## Approaches

A straightforward solution would first convert `A` into the total consumption `C`, then try every possible smaller consumption `x` from 1 through `C / 2`. For each candidate, it would calculate `bill(x)` and `bill(C - x)`, compare their difference with `B`, and stop when the required difference is found. This works because every possible split is explicitly checked, and the statement guarantees that exactly one split is valid.

The problem is the size of the search space. When `A` is close to `10^9`, the corresponding total consumption is about 143 million units. Half of that is roughly 71 million candidate splits. Each candidate needs at least a couple of arithmetic operations and tariff evaluations, so the worst case is about 71 million iterations per test case. That is not compatible with a 1 second limit.

The key observation is that the difference between the two bills changes monotonically as we move the split. Let

`D(x) = bill(C - x) - bill(x)`

for `x <= C / 2`. As `x` increases, the smaller household consumes more and the larger household consumes less. Because `bill` is strictly increasing, `bill(x)` increases while `bill(C - x)` decreases. Consequently, `D(x)` strictly decreases.

That turns the brute-force search into a binary search. If `D(x)` is larger than `B`, our chosen household is still too small, so we increase `x`. If `D(x)` is smaller than `B`, we made the smaller household too large, so we decrease `x`. The unique-solution guarantee means the exact target is eventually found.

There is one more useful simplification. We do not need to search over possible total consumptions to recover `C`. The tariff function can be inverted directly because each range has a fixed price. For example, a bill above 29,900 but at most 4,979,900 corresponds to

`10,000 + (A - 29,900) / 5`

units. Since `A` is guaranteed to come from a real combined consumption, the division is exact.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C) | O(1) | Too slow |
| Optimal | O(log C) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `A` and `B`. If both are zero, stop because this is the sentinel marking the end of the input.
2. Convert the combined bill `A` into the combined consumption `C`. The inverse tariff is piecewise, using the cumulative costs 200, 29,900, and 4,979,900 at the three tariff boundaries.
3. Set the binary-search range to `lo = 1` and `hi = C // 2`. We only search up to half of the total consumption because the problem identifies our household as the one that consumes no more than its neighbor.
4. Choose `mid = (lo + hi) // 2` and let the two consumptions be `mid` and `C - mid`.
5. Calculate the two individual bills and their difference, `diff = bill(C - mid) - bill(mid)`. The second bill is at least the first because `mid <= C - mid`, so the absolute value is unnecessary inside the search.
6. If `diff == B`, we have found the unique split, and `bill(mid)` is the required answer.
7. If `diff > B`, increase `mid` by moving `lo` to `mid + 1`. Increasing the smaller household's consumption makes the two bills closer, which decreases `diff`.
8. If `diff < B`, decrease `mid` by moving `hi` to `mid - 1`. We have moved too far toward equal consumption, so the bill difference has become smaller than required.

The invariant is that the correct smaller consumption remains inside `[lo, hi]`. The function `D(x)` is strictly decreasing, so every comparison tells us which half cannot contain the answer. When `D(mid) > B`, every value at or below `mid` produces a difference at least as large, so the answer must be to the right. When `D(mid) < B`, every value at or above `mid` produces a difference no larger, so the answer must be to the left. Since the valid split is guaranteed to be unique, binary search cannot discard it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def bill(energy):
    if energy <= 100:
        return energy * 2

    result = 200
    energy -= 100

    if energy <= 9900:
        return result + energy * 3

    result += 9900 * 3
    energy -= 9900

    if energy <= 990000:
        return result + energy * 5

    result += 990000 * 5
    energy -= 990000

    return result + energy * 7

def consumption_from_bill(amount):
    if amount <= 200:
        return amount // 2

    if amount <= 29900:
        return 100 + (amount - 200) // 3

    if amount <= 4979900:
        return 10000 + (amount - 29900) // 5

    return 1000000 + (amount - 4979900) // 7

def solve():
    while True:
        A, B = map(int, input().split())

        if A == 0 and B == 0:
            break

        total = consumption_from_bill(A)

        lo = 1
        hi = total // 2

        while lo <= hi:
            mid = (lo + hi) // 2

            smaller_bill = bill(mid)
            larger_bill = bill(total - mid)
            diff = larger_bill - smaller_bill

            if diff == B:
                print(smaller_bill)
                break

            if diff > B:
                lo = mid + 1
            else:
                hi = mid - 1

if __name__ == "__main__":
    solve()
```

The `bill` function implements the progressive tariff using cumulative costs. After the first 100 units, the first 200 Americus have already been charged. After the next 9,900 units, the cumulative cost is `200 + 9900 * 3 = 29,900`. After another 990,000 units, it becomes `29,900 + 990000 * 5 = 4,979,900`. These constants let each bill calculation run in constant time.

The `consumption_from_bill` function reverses those same boundaries. For example, if `amount` is between 29,901 and 4,979,900, the first 10,000 units have already accounted for 29,900 Americus, so the remaining amount is divided by 5 and added to 10,000.

The binary search deliberately uses consumption rather than money. The tariff is nonlinear, so trying to binary-search directly on the bill difference without first recovering total consumption makes the relationship harder to express. Once `total` is known, the two consumptions always add to that fixed value.

The search uses `bill(total - mid) - bill(mid)` rather than `abs(...)`. Because `mid <= total // 2`, the second household consumes at least as much as the first, and the bill function is increasing. The larger bill is consequently known in advance.

Python integers have arbitrary precision, so there is no overflow concern. The largest intermediate value is comfortably within Python's integer representation anyway. The use of `sys.stdin.readline` also avoids unnecessary input overhead when there are many test cases.

## Worked Examples

### Sample 1

The input is

```
1100 300
```

The combined bill of 1100 corresponds to 400 units because `bill(400) = 1100`. The smaller consumption must be between 1 and 200.

| `lo` | `hi` | `mid` | `bill(mid)` | `bill(400-mid)` | `diff` | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 200 | 100 | 200 | 700 | 500 | `diff > 300`, increase `lo` |
| 101 | 200 | 150 | 350 | 650 | 300 | Found |

The first midpoint gives a difference of 500, which is too large. The smaller household therefore needs more consumption. The next midpoint is exactly 150, giving bills 350 and 650, whose difference is 300. The required output is `350`. The sample and its underlying 150/250 split are documented in the original problem source.

### Sample 2

The input is

```
35515 27615
```

The combined bill corresponds to 11,123 units. The valid split is 1,000 and 10,123, producing bills 2,900 and 30,515.

| `lo` | `hi` | `mid` | `bill(mid)` | `bill(total-mid)` | `diff` | Action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 5561 | 2781 | 8243 | 24926 | 16683 | `diff < B`, decrease `hi` |
| 1 | 2780 | 1390 | 4070 | 29099 | 25029 | `diff < B`, decrease `hi` |
| 1 | 1389 | 695 | 1985 | 32040 | 30055 | `diff > B`, increase `lo` |
| 696 | 1389 | 1042 | 3026 | 30305 | 27279 | `diff < B`, decrease `hi` |
| 696 | 1041 | 868 | 2504 | 31175 | 28671 | `diff > B`, increase `lo` |
| 869 | 1041 | 975 | 2825 | 30640 | 27815 | `diff > B`, increase `lo` |
| 976 | 1041 | 1008 | 2924 | 30495 | 27571 | `diff < B`, decrease `hi` |
| 976 | 1007 | 991 | 2873 | 30565 | 27692 | `diff > B`, increase `lo` |
| 992 | 1007 | 999 | 2897 | 30520 | 27623 | `diff > B`, increase `lo` |
| 1000 | 1007 | 1003 | 2909 | 30500 | 27591 | `diff < B`, decrease `hi` |
| 1000 | 1002 | 1001 | 2903 | 30510 | 27607 | `diff < B`, decrease `hi` |
| 1000 | 1000 | 1000 | 2900 | 30515 | 27615 | Found |

The search repeatedly narrows the interval while preserving the unique valid consumption. Once `mid` reaches 1,000, the difference is exactly 27,615, so the answer is `2,900`. The official sample output is `350` and `2900`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log C) | Each test case performs a constant-time bill calculation and halves the consumption search interval each iteration. |
| Space | O(1) | Only a fixed number of integer variables are used. |

For `A <= 10^9`, the combined consumption is at most about 143 million units, so the binary search needs fewer than 28 iterations. Each iteration performs only a handful of integer arithmetic operations. This is comfortably within the 1 second and 256 MB limits stated for the problem.

## Test Cases

```python
import sys
import io

def bill(energy):
    if energy <= 100:
        return energy * 2
    if energy <= 10000:
        return 200 + (energy - 100) * 3
    if energy <= 1000000:
        return 29900 + (energy - 10000) * 5
    return 4979900 + (energy - 1000000) * 7

def consumption_from_bill(amount):
    if amount <= 200:
        return amount // 2
    if amount <= 29900:
        return 100 + (amount - 200) // 3
    if amount <= 4979900:
        return 10000 + (amount - 29900) // 5
    return 1000000 + (amount - 4979900) // 7

def solve_data(data: str) -> str:
    inp = io.StringIO(data)
    out = []

    while True:
        line = inp.readline()
        if not line:
            break

        A, B = map(int, line.split())

        if A == 0 and B == 0:
            break

        total = consumption_from_bill(A)

        lo = 1
        hi = total // 2

        while lo <= hi:
            mid = (lo + hi) // 2

            small = bill(mid)
            large = bill(total - mid)
            diff = large - small

            if diff == B:
                out.append(str(small))
                break

            if diff > B:
                lo = mid + 1
            else:
                hi = mid - 1

    return "\n".join(out)

# Provided samples
assert solve_data(
    "1100 300\n35515 27615\n0 0\n"
) == "350\n2900", "provided samples"

# Minimum valid non-terminating case:
# consumptions 1 and 2 -> bills 2 and 4.
assert solve_data(
    "6 2\n0 0\n"
) == "2", "minimum valid case"

# Both households are inside the first tariff range:
# consumptions 49 and 51 -> bills 98 and 102.
assert solve_data(
    "200 4\n0 0\n"
) == "98", "first tariff boundary"

# Crosses the 1,000,000-unit tariff boundary:
# consumptions 1 and 1000010.
assert solve_data(
    "4979977 4979968\n0 0\n"
) == "2", "highest tariff boundary"

# Maximum-size valid A close to 1e9:
# consumptions 1 and 143145727.
assert solve_data(
    "999999996 999999987\n0 0\n"
) == "2", "large input"

# The all-equal case is represented by the required sentinel 0 0.
assert solve_data(
    "0 0\n"
) == "", "termination sentinel"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6 2` | `2` | Minimum valid input and smallest possible positive consumption |
| `200 4` | `98` | Exact 100-unit tariff boundary and equal per-unit rate on both sides |
| `4979977 4979968` | `2` | Transition into the highest tariff range |
| `999999996 999999987` | `2` | Large values near the `10^9` input bound |
| `0 0` | No output | Sentinel handling |

## Edge Cases

For the minimum valid input `6 2`, the inverse tariff converts 6 Americus into 3 total units. Binary search starts with `lo = 1` and `hi = 1`, so `mid = 1`. The two consumptions are 1 and 2, their bills are 2 and 4, and the difference is exactly 2. The algorithm immediately prints 2. There is no assumption that either household consumes enough electricity to reach the second tariff range.

For the first tariff boundary, consider `200 4`. The inverse function returns 100 units because the first 100 units cost exactly 200. Binary search tests the only possible smaller consumption, 50, if the interval is represented as `1..50`, and eventually finds the unique split 49 and 51. Their bills are 98 and 102, giving the required difference of 4. The calculation treats unit 100 as part of the first range and unit 101 as the first unit charged at rate 3.

For a case crossing the highest boundary, consider `4979977 4979968`. The combined bill converts to 1,000,011 units. The valid split is 1 and 1,000,010. The first household pays 2. The second pays `4,979,900 + 10 * 7 = 4,979,970`, so the difference is 4,979,968. The search therefore finds the smaller consumption as 1 and outputs 2. This exercises both the inverse tariff's final branch and the forward tariff's final branch.

For the large-bound case `999999996 999999987`, the combined consumption is 143,145,728. The valid split is 1 and 143,145,727. The smaller bill is 2, while the larger bill is 999,999,989, giving a difference of 999,999,987. Even though the total consumption is more than 143 million units, binary search needs only logarithmically many iterations rather than scanning those possible splits one by one.

The `0 0` input is handled before any tariff conversion or binary search. It terminates the loop immediately, so it cannot accidentally be interpreted as a pair of zero-consumption households. This distinction matters because regular test cases have positive `A` and `B`, while `0 0` is reserved solely as the end marker.
