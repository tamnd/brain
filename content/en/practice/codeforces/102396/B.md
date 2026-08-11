---
title: "CF 102396B - Cash Gap"
description: "We have an initial account balance s and n transactions that must all happen during the next m days. Transaction i changes the balance by count[i], but its exact day can be any day in the inclusive interval [from[i], to[i]]."
date: "2026-08-11T15:26:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102396
codeforces_index: "B"
codeforces_contest_name: "2019-2020 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 19)"
rating: 0
weight: 102396
solve_time_s: 658
verified: true
draft: false
---

[CF 102396B - Cash Gap](https://codeforces.com/problemset/problem/102396/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an initial account balance `s` and `n` transactions that must all happen during the next `m` days. Transaction `i` changes the balance by `count[i]`, but its exact day can be any day in the inclusive interval `[from[i], to[i]]`. If several transactions happen on the same day, their internal order is unrestricted.

We need to decide whether there is at least one valid choice of transaction days and within-day ordering that makes the balance negative at some moment. A negative balance is the cash gap. If the balance becomes exactly zero, that is still safe, because the company has exactly enough money for the payment.

The useful part of the input is that `n` and `m` are both at most `1000`. An `O(nm)` solution performs at most about one million transaction-day checks, which is easily reasonable for the time limit. More importantly, the bounds rule out enumerating possible schedules, because every transaction may have many possible days. With intervals spanning all `m` days, merely assigning a day to every transaction creates `m^n` possibilities. For `n = m = 1000`, that is `1000^1000` assignments before we even consider the ordering of transactions on a day.

Several boundary cases can make an otherwise plausible solution wrong. First, reaching zero is not a cash gap. For example,

```
1 1 5
-5 1 1
```

has output `NO`, because the only transaction leaves the balance at zero. A check using `balance <= 0` instead of `balance < 0` would incorrectly answer `YES`.

Second, a transaction whose interval ends before the current day is already forced to have happened, while a transaction whose interval includes the current day can be deliberately scheduled on that day. For example,

```
2 2 5
5 1 1
-6 2 2
```

has output `YES`. The first transaction must happen on day 1, giving a balance of 10. The second transaction happens on day 2 and reduces the balance to 4, so this particular example is actually safe. To expose the boundary correctly, change the initial balance to 0, but the constraints require `s >= 1`. A valid example is instead

```
2 2 5
0 1 1
-6 2 2
```

which has output `YES`, because the balance becomes `-1` on day 2. A solution that accidentally treats transactions ending on the current day as already completed before examining that day can misclassify such cases.

Third, transactions on the same day may be ordered adversarially. Consider

```
2 1 5
-3 1 1
-3 1 1
```

which has output `YES`. The first payment leaves 2 euros, and the second payment then requires 3 euros. Summing the two payments is enough here, but an implementation that assumes an arbitrary fixed input order can fail in cases where positive and negative transactions share a day.

Finally, a zero-valued transaction has no effect at all. For example,

```
2 1 5
0 1 1
0 1 1
```

has output `NO`. Such transactions should not accidentally be treated as negative payments when maintaining the active set of dangerous transactions.

## Approaches

A direct brute-force approach would choose an allowed day for every transaction, then simulate the resulting schedule. If every interval is `[1, m]`, there are `m^n` possible assignments of days. If we also explicitly try every possible ordering of transactions, there can be another factor of `n!`, giving `m^n n!` candidate combinations, with `O(n)` work to simulate each one. For the maximum constraints this is far beyond feasible.

The brute force works because it literally explores every valid way the transactions might happen. It fails because almost all of that information is irrelevant to the question. We do not need to construct a complete schedule. We only need to know whether some moment can have a negative balance.

Fix a particular day `d`, and ask how small the balance can be immediately before or during transactions on that day. Every transaction with `to < d` is forced to have happened before day `d`, regardless of how we choose its exact date. Its contribution must already be included in the balance.

Now consider a transaction whose interval contains `d`. If its value is negative, we can schedule it on day `d` and execute it before all positive transactions on that day. Since we are searching for the smallest possible balance, every such negative transaction should be included before checking for a cash gap. Positive transactions whose intervals contain `d` can be postponed until after the dangerous moment, so they do not help prevent the gap.

This gives a simple characterization. For every day `d`, the smallest balance that can be reached by that point is

`initial balance + sum of all transactions with to < d + sum of all negative transactions with from <= d <= to`.

If this value is negative for any `d`, the answer is `YES`. Conversely, if it is never negative, then no valid ordering can produce a cash gap, because the expression already includes every transaction that can possibly make the balance smaller before that moment.

We can evaluate this expression in linear time. For the first sum, group transaction values by their ending day. For the second sum, maintain the currently active negative transactions using a difference array. A negative transaction `[from, to]` contributes its value starting at `from` and stops contributing after `to`, so we add its value at `from` and subtract it at `to + 1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(m^n n! n)` | `O(n)` | Too slow |
| Optimal | `O(n + m)` | `O(m)` | Accepted |

## Algorithm Walkthrough

1. Create an array `ending` where `ending[d]` stores the sum of all transaction changes whose latest possible day is exactly `d`. When we are about to inspect day `d`, every transaction with `to < d` is already forced to have happened, so we can accumulate `ending[d - 1]` into a running value called `forced`.
2. Create a difference array `active`. For every negative transaction with interval `[from, to]` and value `count`, add `count` at `active[from]` and subtract `count` at `active[to + 1]`. Its prefix sum will then equal the total value of all negative transactions whose intervals contain the current day.
3. Scan the days from `1` through `m`. At day `d`, first add `ending[d - 1]` to `forced`. This makes `forced` equal to the contribution of every transaction that must have happened strictly before day `d`.
4. Add `active[d]` to a running variable `dangerous`. After the prefix update, `dangerous` is exactly the sum of all negative transactions that can be performed on day `d`.
5. Compute `balance = s + forced + dangerous`. This is the smallest balance that can be reached while processing day `d`, because every forced transaction has already occurred, every currently available negative transaction can be executed now, and positive transactions that could still be delayed have not been executed.
6. If `balance < 0`, print `YES` immediately. Otherwise continue with the next day. If every day is safe, print `NO`.

### Why it works

Consider any day `d`. Every transaction with `to < d` must have occurred before day `d`, so its contribution cannot be avoided. Among transactions whose intervals contain `d`, every negative transaction can be placed on day `d` and executed before positive transactions. Including all of them produces the minimum possible balance reachable at that point. No other transaction can lower the balance earlier than this expression. Thus the algorithm finds a negative balance exactly when some valid transaction schedule can create a cash gap.

The invariant during the scan is that `forced + dangerous` represents the smallest possible cumulative transaction change at the current day. The ending contributions account for everything that is already unavoidable, while the active negative contributions account for everything currently available that can be deliberately placed before the dangerous moment. If this minimum is never negative, every valid schedule is safe.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, s = map(int, input().split())

    ending = [0] * (m + 2)
    active = [0] * (m + 2)

    for _ in range(n):
        count, left, right = map(int, input().split())

        ending[right] += count

        if count < 0:
            active[left] += count
            active[right + 1] -= count

    forced = 0
    dangerous = 0

    for day in range(1, m + 1):
        forced += ending[day - 1]
        dangerous += active[day]

        if s + forced + dangerous < 0:
            print("YES")
            return

    print("NO")

if __name__ == "__main__":
    solve()
```

The `ending` array stores complete transaction contributions, including positive and negative values. A transaction with `to = d` is not added to `forced` until day `d + 1`, because on day `d` it can still be executed during that day and potentially be part of the dangerous ordering.

The `active` array contains only negative transactions. For a transaction with value `count < 0` and interval `[left, right]`, adding `count` at `left` makes it active starting on exactly the first legal day. Subtracting it at `right + 1` removes it immediately after the last legal day. The prefix sum at day `d` consequently contains exactly the negative transactions satisfying `left <= d <= right`.

The order of the updates in the day loop handles the boundaries correctly. `ending[day - 1]` is added before checking day `day`, while `active[day]` is added for the current day itself. This distinction is what separates transactions that are already unavoidable from transactions that can still be deliberately scheduled on the current day.

Python integers have arbitrary precision, so the potentially large intermediate sums do not overflow. Even though the maximum absolute total can reach around `10^9`, using Python integers makes the implementation independent of that bound.

## Worked Examples

For Sample 1,

```
4 3 100
100 1 2
-100 1 2
1 2 3
0 3 3
```

The negative transaction `-100` is active on days 1 and 2. The positive transaction ending on day 2 is not forced before day 2, so it cannot be counted as protection against a gap there.

| Day | Forced before day | Active negative changes | Minimum balance | Result |
| --- | --- | --- | --- | --- |
| 1 | 0 | -100 | 0 | Safe |
| 2 | 0 | -100 | 0 | Safe |
| 3 | 1 | 0 | 101 | Safe |

The minimum balance reaches exactly zero on days 1 and 2. That is not negative, so no cash gap exists and the answer is `NO`. The example also demonstrates why checking `<= 0` would be incorrect.

For Sample 2,

```
4 3 100
100 1 2
-100 1 2
1 2 3
-1 2 2
```

There are two negative transactions that can both be executed on day 2. The `-100` transaction is active from day 1 through day 2, while `-1` is active only on day 2.

| Day | Forced before day | Active negative changes | Minimum balance | Result |
| --- | --- | --- | --- | --- |
| 1 | 0 | -100 | 0 | Safe |
| 2 | 0 | -101 | -1 | Gap |
| 3 | 1 | 0 | 101 | Not reached |

At day 2, both negative payments can be placed before the positive `+100` and `+1` transactions. Starting from 100 euros, the balance becomes `100 - 100 - 1 = -1`. The algorithm detects this and prints `YES`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + m)` | Each transaction is processed once, and each of the `m` days is scanned once. |
| Space | `O(m)` | Two arrays of size proportional to the number of days are maintained. |

With `n, m <= 1000`, the algorithm performs only a few thousand array operations and uses negligible memory compared with the 512 MB limit. It is comfortably within the 1 second time limit.

## Test Cases

```python
import sys
import io

def solve_text(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))
    s = int(next(it))

    ending = [0] * (m + 2)
    active = [0] * (m + 2)

    for _ in range(n):
        count = int(next(it))
        left = int(next(it))
        right = int(next(it))

        ending[right] += count

        if count < 0:
            active[left] += count
            active[right + 1] -= count

    forced = 0
    dangerous = 0

    for day in range(1, m + 1):
        forced += ending[day - 1]
        dangerous += active[day]

        if s + forced + dangerous < 0:
            return "YES\n"

    return "NO\n"

assert solve_text("""\
4 3 100
100 1 2
-100 1 2
1 2 3
0 3 3
""") == "NO\n", "sample 1"

assert solve_text("""\
4 3 100
100 1 2
-100 1 2
1 2 3
-1 2 2
""") == "YES\n", "sample 2"

assert solve_text("""\
1 1 1
-1 1 1
""") == "NO\n", "minimum input and exact zero"

assert solve_text("""\
3 1 1
1 1 1
1 1 1
1 1 1
""") == "NO\n", "all equal positive values"

assert solve_text("""\
2 2 5
0 1 1
-6 2 2
""") == "YES\n", "transaction starting and ending on boundary day"

assert solve_text("""\
1000 1000 1000000
""" + "\n".join(["0 1 1000"] * 1000) + "\n") == "NO\n", "maximum-size zero transactions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` with `-1 1 1` | `NO` | Minimum size and the distinction between zero and negative balance |
| Three `+1` transactions on day 1 | `NO` | All-equal values and harmless positive transactions |
| `0 1 1`, `-6 2 2` with `s = 5` | `YES` | Exact interval boundaries and a transaction active on only one day |
| 1000 zero transactions with intervals `[1,1000]` | `NO` | Maximum input size and neutral transactions |

## Edge Cases

The first edge case is an account that reaches exactly zero. For

```
1 1 1
-1 1 1
```

the scan starts with `forced = 0` and `dangerous = -1`. The candidate balance is `1 - 1 = 0`, so the condition `balance < 0` is false and the algorithm prints `NO`. This prevents the common mistake of treating an exhausted account as already being in a cash gap.

The second edge case concerns an interval that ends on the current day. Consider

```
2 2 5
0 1 1
-6 2 2
```

On day 1, the `-6` transaction is not active, so the minimum balance is 5. On day 2, it becomes active through `active[2]`, while it is not included in `forced`, because its `to` value is exactly 2 rather than less than 2. The candidate balance is `5 - 6 = -1`, producing `YES`. This demonstrates why the forced sum must use `to < day`, not `to <= day`.

The third edge case is multiple negative transactions on the same day. In Sample 2, day 2 has active negative contributions `-100` and `-1`, so `dangerous = -101`. The algorithm effectively puts both payments before all positive transactions on that day, giving the smallest possible balance. A fixed input order would not capture this possibility.

The fourth edge case is a transaction with zero change. For a transaction such as `0 1 1`, the code adds nothing to `active`, because zero is neither dangerous nor useful for lowering the balance. Its presence cannot change the answer, and the maximum-size test confirms that many such transactions are handled without special cases.
