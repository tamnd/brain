---
title: "CF 102623A - Archmage"
description: "The Archmage starts with a full mana pool of size n. During each second, he may spend x mana to summon one Water Element if enough mana is available, or he may wait. After that decision, his aura restores y mana, but the mana cannot go above n."
date: "2026-08-01T08:55:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102623
codeforces_index: "A"
codeforces_contest_name: "2020 Lenovo Cup USST Campus Online Invitational Contest"
rating: 0
weight: 102623
solve_time_s: 87
verified: true
draft: false
---

[CF 102623A - Archmage](https://codeforces.com/problemset/problem/102623/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

The Archmage starts with a full mana pool of size `n`. During each second, he may spend `x` mana to summon one Water Element if enough mana is available, or he may wait. After that decision, his aura restores `y` mana, but the mana cannot go above `n`.

The task is to find the largest number of summons possible during the first `m` seconds. Each test case gives the mana limit, the number of seconds available, the mana cost of one summon, and the regeneration amount.

The constraints make the main difficulty clear. There can be up to `100000` test cases, and each value can be as large as `10^9`. A simulation that processes every second would require up to `10^14` operations in the worst case, which is far beyond what a 2 second limit allows. The solution has to reduce the process to constant time per test case.

The tricky cases come from the interaction between regeneration and the mana cap. A direct simulation often works on small examples but fails when `m` is huge or when the Archmage can either cast forever or must rely on accumulated regeneration.

For example, consider:

```
1
2 5 1 1
```

The correct output is:

```
5
```

A careless solution might think the mana decreases because every summon costs mana. However, the cost and regeneration are equal, so after every complete second the mana returns to the same value.

Another edge case is when regeneration is smaller than the spell cost:

```
1
6 10 4 2
```

The correct output is:

```
6
```

A simulation that assumes the Archmage should wait whenever possible may miss the fact that the initial full mana can be converted into several immediate casts before regeneration becomes necessary.

A final boundary case is when the number of seconds is the limiting factor:

```
1
100 3 20 5
```

The correct output is:

```
3
```

Even though the mana supply is large enough for more spells, only three actions are allowed because the game lasts exactly three seconds.

## Approaches

The straightforward approach is to simulate every second. Keep the current mana value, check whether a summon is possible, subtract `x` if it is, then add `y` with the cap applied. This exactly follows the game rules, so the result is correct.

The problem is the number of seconds. Since `m` can reach `10^9` and there can be `10^5` test cases, the total number of simulated seconds could reach `10^14`. The simulation is useful for understanding the process, but it cannot be used in the final solution.

The key observation is that the only resource that matters is the total amount of mana available over the entire period. Initially the Archmage owns `n` mana. During the following `m - 1` restorations, at most `(m - 1) * y` additional mana can be recovered. The last second's restoration happens after the final decision, so it cannot help create another summon.

When `x <= y`, every summon effectively pays for itself after the restoration. Since the Archmage starts full and `n >= x + y >= x`, he can cast in every second.

When `x > y`, every summon consumes more mana than one restoration returns. However, the total amount of mana that can be spent on summons is still bounded by the initial mana plus all restorations before the final action. Dividing this total by `x` gives the maximum possible number of summons. The answer also cannot exceed `m`, because there are only `m` seconds.

The optimal solution is thus a constant time calculation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. If the regeneration amount `y` is at least the spell cost `x`, output `m`. Every cast is compensated by the restoration at the end of the second, so the Archmage can summon during every available second.
2. Otherwise, compute the total mana that can be used for summons as `n + (m - 1) * y`. The initial mana is available before the first action, and only the first `m - 1` restorations can contribute to future summons.
3. Divide this total by `x` to obtain the maximum number of complete summons that the available mana can pay for.
4. Limit the result by `m`, because even unlimited mana cannot produce more than one summon per second.

Why it works:

When `x > y`, every summon permanently removes `x - y` mana from the system after the restoration. The exact order of waiting and casting does not increase the total amount of mana that can be spent. The initial mana and the first `m - 1` restorations are the complete budget available for all summons. Every summon consumes exactly `x` from this budget, so the number of summons cannot exceed the integer division of the budget by `x`. Since the Archmage can always arrange his actions to spend this available mana whenever the count is within the limit, this bound is achievable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m, x, y = map(int, input().split())

        if y >= x:
            ans.append(str(m))
        else:
            ans.append(str(min(m, (n + (m - 1) * y) // x)))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The solution first separates the case where regeneration keeps pace with spell usage. In that situation there is no reason to ever skip a second.

For the other case, the expression `n + (m - 1) * y` represents the total mana that can contribute to casts. The multiplication uses `m - 1` rather than `m` because the restoration after the final second happens too late to create another spell.

Python integers handle the largest intermediate value safely. The largest multiplication is around `10^18`, which fits comfortably in Python's arbitrary precision integer type. The `min` operation handles the boundary where the computed mana budget allows more spells than the number of available seconds.

## Worked Examples

For the first sample:

```
n = 2, m = 2, x = 1, y = 1
```

Since `y >= x`, every second can contain a summon.

| Second | Mana before action | Action | Mana after restoration | Summons |
| --- | --- | --- | --- | --- |
| 1 | 2 | Cast | 2 | 1 |
| 2 | 2 | Cast | 2 | 2 |

The trace shows the infinite regeneration case. The mana returns to the same value after every second, so the time limit is the only restriction.

For the second sample:

```
n = 4, m = 4, x = 2, y = 1
```

Here `x > y`, so the available mana calculation is used.

| Variable | Value |
| --- | --- |
| Initial mana | 4 |
| Restorations before final second | 3 |
| Total usable mana | 4 + 3 = 7 |
| Spell cost | 2 |
| Mana-based summons | 7 // 2 = 3 |
| Time limit | 4 |
| Answer | 3 |

The trace demonstrates that the final restoration is excluded. Counting it would incorrectly give one extra possible summon.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Each test case uses only arithmetic operations |
| Space | O(1) | Only a few integer variables are stored |

The solution performs constant work for every test case, so `100000` cases are easily handled within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out.getvalue()

def solve():
    input = sys.stdin.readline
    t = int(input())
    res = []

    for _ in range(t):
        n, m, x, y = map(int, input().split())
        if y >= x:
            res.append(str(m))
        else:
            res.append(str(min(m, (n + (m - 1) * y) // x)))

    print("\n".join(res))

assert run("""3
2 2 1 1
4 4 2 1
6 10 4 2
""") == "2\n3\n6\n", "samples"

assert run("""1
2 1 1 1
""") == "1\n", "minimum values"

assert run("""1
2000000000 1000000000 1000000000 1
""") == "2\n", "large values"

assert run("""1
100 3 20 5
""") == "3\n", "time limit boundary"

assert run("""1
10 20 3 3
""") == "20\n", "equal cost and regeneration"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 1 1` | `2` | Regeneration equal to cost |
| `2000000000 1000000000 1000000000 1` | `2` | Large arithmetic values |
| `100 3 20 5` | `3` | The number of seconds limits the answer |
| `10 20 3 3` | `20` | Infinite casting pattern |

## Edge Cases

For the equal regeneration case:

```
1
2 5 1 1
```

The algorithm checks `y >= x`, which is true. It immediately returns `5`. This matches the real process because every second spends one mana and restores one mana afterward.

For the initial mana burst case:

```
1
6 10 4 2
```

The algorithm computes:

```
(6 + 9 * 2) // 4 = 24 // 4 = 6
```

The result is `6`. The initial mana allows several early casts, and the later restorations add enough mana for additional summons. The final restoration is not included because it happens after the last possible cast.

For the large time case:

```
1
100 3 20 5
```

The calculation gives:

```
(100 + 2 * 5) // 20 = 110 // 20 = 5
```

The answer is then limited by `m`, producing `3`. The algorithm correctly respects the fact that one second can create at most one Water Element.
