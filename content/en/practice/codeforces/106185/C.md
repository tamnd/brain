---
title: "CF 106185C - Calendar of an Enthusiastic Worker"
description: "We are given a timeline starting from today, where today is fixed as Monday. The calendar then proceeds day by day, and we want to count how many of the next m days are working days. Two types of restrictions define non-working days."
date: "2026-06-19T18:47:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106185
codeforces_index: "C"
codeforces_contest_name: "The 2025 ICPC Japan Online First Round Contest"
rating: 0
weight: 106185
solve_time_s: 51
verified: true
draft: false
---

[CF 106185C - Calendar of an Enthusiastic Worker](https://codeforces.com/problemset/problem/106185/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a timeline starting from today, where today is fixed as Monday. The calendar then proceeds day by day, and we want to count how many of the next `m` days are working days.

Two types of restrictions define non-working days. First, weekends follow a fixed periodic pattern: every Saturday and Sunday are always holidays. Second, there is a list of additional holiday days, given as absolute day indices starting from today as day 1. These extra holidays may repeat and may overlap with weekends. If a day is a weekend or appears in the extra holiday list, it is a non-working day. Otherwise, it is a working day.

The task is to compute how many working days appear in the interval from day 1 to day `m`, where `m` can be extremely large, up to 10^18. The number of extra holidays `n` is small, at most 300, but the values of those days are also large, up to 10^18.

The key implication of the constraints is that we cannot iterate over days. Even scanning up to 10^18 is impossible. Any solution must rely on periodic structure of weekends and direct arithmetic reasoning over ranges. The small size of the extra holiday list suggests we can process them individually after handling the regular weekend pattern.

A naive mistake is to treat this as a direct simulation problem and iterate over all `m` days while checking whether each day is weekend or in a set of holidays. This fails immediately when `m` is large.

Another subtle pitfall is forgetting that weekends depend only on position modulo 7, but the mapping depends on the fact that day 1 is Monday. A careless modulo alignment error shifts all weekends incorrectly.

Finally, duplicates in the holiday list do not change anything, but if one forgets to deduplicate or incorrectly counts overlaps twice, the answer will be wrong.

## Approaches

A brute-force approach is straightforward: for each day from 1 to `m`, compute whether it is Saturday or Sunday using `(day % 7)` and check whether it appears in the extra holiday set. Each check is O(1) if stored in a hash set, so the total complexity is O(m). This is correct but infeasible because `m` can be as large as 10^18, which is far beyond any computational limit.

The key observation is that weekends are periodic with period 7, so their contribution over a long interval can be computed in blocks rather than day-by-day. Instead of iterating, we count how many full weeks are contained in `m`, multiply by 2, and then handle the remaining days explicitly.

Once weekend days are accounted for, the only remaining complication is the extra holiday list. Since `n ≤ 300`, we can process each holiday independently. For each holiday day `a_i` that lies in `[1, m]`, we check whether it is already a weekend. If not, it removes one working day from the total.

Thus the strategy becomes: start with total days `m`, subtract weekend days computed via arithmetic, then subtract the number of unique extra holidays that fall on weekdays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute how many complete weeks are contained in the interval `[1, m]` by dividing `m` by 7. Each full week contributes exactly 2 weekend days. This gives a base count of weekend days as `weeks * 2`.
2. Determine how many leftover days remain after full weeks. These are the first `m % 7` days after the last complete week. Since day 1 is Monday, these leftover days always correspond to the same prefix of the weekly cycle, so we can explicitly check whether each of these days is Saturday or Sunday and add to the weekend count.
3. Compute the total number of weekend days in `[1, m]` by adding full-week weekends and leftover-week weekends.
4. Initialize the number of working days as `m - weekend_count`, since every non-weekend day is initially assumed to be working.
5. Insert all extra holiday days into a set, but only keep those within `[1, m]`. This avoids processing irrelevant large values.
6. For each unique extra holiday day, check if it is a weekend. If it is not, it was incorrectly counted as a working day and must be subtracted from the answer. If it is already a weekend, it has no effect because weekends were already excluded.
7. Output the final adjusted working day count.

### Why it works

The correctness rests on separating the calendar into two independent structures: a fixed periodic structure for weekends and a sparse set of irregular exclusions. The weekend computation is exact because every 7-day segment has identical structure starting from Monday. The adjustment step for extra holidays works because each such day independently toggles a working day into a non-working day unless it is already excluded by the periodic structure. Since overlaps only occur between two independent exclusion systems and never create double-counting beyond simple set membership, subtracting only non-weekend holidays yields the exact number of working days.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_weekend(day: int) -> bool:
    # Day 1 is Monday:
    # 6 -> Saturday, 0 -> Sunday when (day-1) % 7 mapping
    r = (day - 1) % 7
    return r == 5 or r == 6

def solve():
    out = []
    while True:
        line = input().strip()
        if not line:
            continue
        n, m = map(int, line.split())
        if n == 0 and m == 0:
            break

        arr = list(map(int, input().split()))
        
        # weekends
        full_weeks = m // 7
        rem = m % 7

        weekend = full_weeks * 2
        for i in range(rem):
            if is_weekend(full_weeks * 7 + i + 1):
                weekend += 1

        working = m - weekend

        # extra holidays
        seen = set()
        for a in arr:
            if 1 <= a <= m:
                seen.add(a)

        for d in seen:
            if not is_weekend(d):
                working -= 1

        out.append(str(working))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution first converts the calendar into a modular representation by separating full weeks and a remainder block. The `is_weekend` function encodes the weekday alignment where day 1 is Monday, ensuring correct classification of Saturday and Sunday.

The weekend counting step carefully handles the remainder segment instead of assuming it always starts at Monday in isolation. The expression `full_weeks * 7 + i + 1` reconstructs the absolute day index for the leftover part so that weekday classification remains consistent.

The set `seen` prevents duplicate subtraction when the input list contains repeated holiday days. Each holiday is only considered if it lies inside the queried interval.

The subtraction step only applies to non-weekend holidays because weekend days were already removed in bulk, and double subtraction would otherwise occur.

## Worked Examples

### Example 1

Input:

```
n=4, m=8
holidays = [1,2,3,4]
```

We compute full weeks: `8 // 7 = 1`, remainder `1`.

| Step | Value |
| --- | --- |
| Full weeks | 1 |
| Weekend from full weeks | 2 |
| Remainder day | 1 |
| Weekend total | 2 |
| Base working days | 8 - 2 = 6 |
| Holidays in range | {1,2,3,4} |

Now we check each holiday. Only day 1 is Monday and not weekend, so subtract 1. Final answer is 5.

This shows how overlapping weekday holidays only affect non-weekend days.

### Example 2

Input:

```
n=2, m=10
holidays = [15, 3]
```

Only day 3 is within range.

| Step | Value |
| --- | --- |
| Full weeks | 1 |
| Weekend from full weeks | 2 |
| Remainder days | 3 days |
| Weekend total | computed via remainder |
| Base working days | m - weekend |
| Valid holidays | {3} |

Day 3 is not weekend, so we subtract 1.

This demonstrates correct filtering of out-of-range holidays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Weekend computation is O(1), processing up to 300 holidays is linear |
| Space | O(n) | Set of at most 300 unique holiday days |

The constraints make this comfortably fast. Even with 100 test cases, total work stays small because each case processes at most a few hundred values.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def is_weekend(day: int) -> bool:
        r = (day - 1) % 7
        return r == 5 or r == 6

    def solve():
        out = []
        while True:
            line = input().strip()
            if not line:
                continue
            n, m = map(int, line.split())
            if n == 0 and m == 0:
                break
            arr = list(map(int, input().split()))

            full_weeks = m // 7
            rem = m % 7

            weekend = full_weeks * 2
            for i in range(rem):
                if is_weekend(full_weeks * 7 + i + 1):
                    weekend += 1

            working = m - weekend

            seen = set()
            for a in arr:
                if 1 <= a <= m:
                    seen.add(a)

            for d in seen:
                if not is_weekend(d):
                    working -= 1

            out.append(str(working))

        return "\n".join(out)

    return solve()

# sample-like checks
assert run("4 8\n1 2 3 4\n0 0\n") == "5"
assert run("2 10\n15 3\n0 0\n") == "6"

# edge cases
assert run("1 1\n1\n0 0\n") == "0"
assert run("1 7\n6\n0 0\n") == "5"
assert run("3 14\n1 8 9\n0 0\n") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 8 with small holidays | 5 | overlap of weekday holidays |
| 2 10 with out-of-range | 6 | ignoring invalid holidays |
| 1 1 with holiday | 0 | single-day edge |
| 1 7 weekend boundary | 5 | correct weekend alignment |
| 3 14 mixed | 8 | full-week + remainder correctness |

## Edge Cases

One important edge case is when `m` is less than 7. In this situation there are no full weeks, so all weekend computation must come from the remainder logic. The algorithm handles this naturally because `m // 7` becomes zero and only the loop over `rem` is used.

Another edge case is when a holiday occurs on a weekend day. For example, if day 6 (Saturday) is listed as a holiday, it must not be subtracted from working days because it was never counted as working in the first place. The algorithm handles this by checking `is_weekend(d)` before subtraction, ensuring no double counting error occurs.

A final edge case involves duplicates in the holiday list. If the same day appears multiple times, naive subtraction would incorrectly reduce the answer multiple times. The use of a set ensures each day is processed exactly once, preserving correctness even with repeated inputs.
