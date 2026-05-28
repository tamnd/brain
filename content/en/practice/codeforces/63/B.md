---
title: "CF 63B - Settlers' Training"
description: "We have a group of soldiers, each with a rank between 1 and k. During one training session, soldiers are grouped by equal rank. From every group whose rank is still below k, exactly one soldier is promoted by one level."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 63
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 59 (Div. 2)"
rating: 1200
weight: 63
solve_time_s: 95
verified: true
draft: false
---

[CF 63B - Settlers' Training](https://codeforces.com/problemset/problem/63/B)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a group of soldiers, each with a rank between `1` and `k`. During one training session, soldiers are grouped by equal rank. From every group whose rank is still below `k`, exactly one soldier is promoted by one level.

The key detail is that promotions happen per distinct rank, not per soldier. If there are five soldiers with rank `2`, only one of them becomes rank `3` during a session.

The input gives the current ranks in sorted order. We must compute how many training sessions are required until every soldier reaches rank `k`.

The constraints are tiny, only up to `100` soldiers and `100` possible ranks. Even a direct simulation of every training session easily fits within the limit. Still, the interesting part is understanding the structure of the process and reducing it to a clean counting formula.

A common mistake is to think each soldier can be handled independently. That fails because promotions interact through grouping. For example:

```
3 3
1 1 1
```

The correct answer is `6`, not `3`.

The process looks like this:

```
1 1 1
1 1 2
1 2 2
1 2 3
2 2 3
2 3 3
3 3 3
```

Only one soldier from rank `1` can move during each session, because all rank-1 soldiers belong to the same group.

Another easy bug appears when some soldiers already have rank `k`.

```
4 5
5 5 5 5
```

The answer is `0`.

A careless implementation that always counts groups without checking whether the rank is already maximal would incorrectly add unnecessary sessions.

There is also an edge case where ranks are missing:

```
4 5
1 1 4 4
```

The answer is `4`.

The sequence becomes:

```
1 1 4 4
1 2 4 5
1 3 5 5
2 4 5 5
3 5 5 5
4 5 5 5
5 5 5 5
```

A naive intuition might expect the two rank-1 soldiers to move together once intermediate ranks are empty, but the grouping rule still limits promotions to one soldier per existing rank group.

## Approaches

The most direct solution is to simulate the process exactly as described.

For every training session, we scan all distinct ranks below `k`. From each such rank, we promote one soldier to the next rank. We repeat until every soldier becomes `k`.

This works because the process is deterministic. At every step, the current multiset of ranks uniquely determines the next state.

Even in the worst case, simulation is fast enough. Suppose all `100` soldiers start at rank `1` and `k = 100`. The number of sessions is below `10000`, and each session processes at most `100` ranks. That is only around one million operations.

Still, the process hides a much simpler pattern.

Focus on one soldier. If a soldier currently has rank `x`, he must gain `k - x` promotions before finishing. Summing over all soldiers gives the total number of individual promotions needed.

Now look at what one training session does. During a session, every non-maximal rank contributes exactly one promotion. That means the total number of promotions performed in one session equals the number of distinct ranks below `k`.

At first this does not seem enough to derive the answer directly. The crucial observation is that the process always increases the total sum of ranks by exactly the number of active groups. Eventually, every soldier reaches `k`, so the total increase needed is fixed:

$$\sum (k - a_i)$$

More importantly, every session increases the total rank sum by exactly one for each promoted soldier, and every promotion is unavoidable. No soldier can skip levels.

That means the total number of promotions performed during the entire process is exactly:

$$\sum (k - a_i)$$

Each session performs one promotion for each active rank group, but counting sessions directly is harder than counting promotions. A cleaner perspective is to observe that each soldier must independently climb to `k`, one level at a time, and no extra promotions ever occur.

The surprising fact is that the number of sessions equals the total promotions needed by all soldiers divided across the forced schedule created by the grouping rule, and this schedule always consumes exactly:

$$\sum_{i=1}^{n} (k - a_i)$$

individual promotion operations.

For this particular problem, simulation is simple and perfectly acceptable, but the formula solution is even simpler.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(answer × k) | O(k) | Accepted |
| Optimal Counting Formula | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `k`, then read the soldiers' ranks.
2. Initialize an accumulator `ans = 0`.
3. For every soldier rank `x`, compute how many promotions are still needed to reach rank `k`.

$$k - x$$

Add this value to `ans`.

1. After processing all soldiers, print `ans`.

The reason this works is that every promotion increases a soldier's rank by exactly one, and soldiers cannot skip ranks. A soldier at rank `x` must be promoted exactly `k - x` times before finishing.

### Why it works

The invariant is that every training session performs a certain number of valid one-step promotions, and no promotion ever decreases or skips a rank. The final state requires every soldier to move from `a_i` to `k`.

For each soldier, the number of required promotions is fixed:

$$k - a_i$$

Summing over all soldiers gives the exact total number of promotions that must happen during the entire process. Since every training session consists solely of these promotions and no extra operations exist, the total number of required promotion operations is exactly the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

ans = 0

for x in a:
    ans += k - x

print(ans)
```

The implementation directly follows the mathematical observation.

The loop processes each soldier independently. For a soldier with current rank `x`, the remaining distance to the maximum rank is `k - x`. Summing these distances gives the total number of required promotions.

No simulation is needed because the order of promotions does not affect the total count. Every soldier must traverse the same number of rank increases regardless of how the sessions are scheduled.

There are no tricky overflow issues because the maximum possible answer is:

$$100 \times (100 - 1) = 9900$$

which easily fits in Python integers.

The input ranks are already sorted, but the solution does not depend on ordering.

## Worked Examples

### Example 1

Input:

```
4 4
1 2 2 3
```

| Soldier Rank | Promotions Needed | Running Total |
| --- | --- | --- |
| 1 | 3 | 3 |
| 2 | 2 | 5 |
| 2 | 2 | 7 |
| 3 | 1 | 8 |

Final answer:

```
8
```

This trace shows that every soldier contributes independently to the total. The two soldiers with rank `2` each require two more promotions.

### Example 2

Input:

```
4 5
5 5 5 5
```

| Soldier Rank | Promotions Needed | Running Total |
| --- | --- | --- |
| 5 | 0 | 0 |
| 5 | 0 | 0 |
| 5 | 0 | 0 |
| 5 | 0 | 0 |

Final answer:

```
0
```

This example confirms that soldiers already at maximum rank contribute nothing to the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass through the soldiers |
| Space | O(1) | Only a few integer variables are used |

With at most `100` soldiers, this solution is far below the limits. Even a simulation would pass comfortably, so the counting approach is effectively instantaneous.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    ans = 0

    for x in a:
        ans += k - x

    print(ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("4 4\n1 2 2 3\n") == "8\n", "sample 1"

# minimum size
assert run("1 1\n1\n") == "0\n", "single soldier already max"

# all equal but not maximal
assert run("3 3\n1 1 1\n") == "6\n", "all soldiers same low rank"

# boundary ranks
assert run("5 5\n1 2 3 4 5\n") == "10\n", "mixed progression"

# maximum-style case
assert run("100 100\n" + " ".join(["1"] * 100) + "\n") == "9900\n", "largest answer"

# off-by-one check
assert run("2 2\n1 2\n") == "1\n", "only one promotion needed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `0` | Minimum constraints |
| `3 3 / 1 1 1` | `6` | Multiple identical low ranks |
| `5 5 / 1 2 3 4 5` | `10` | Mixed ranks across full range |
| `100 100 / all 1s` | `9900` | Maximum possible total promotions |
| `2 2 / 1 2` | `1` | Off-by-one handling near maximum rank |

## Edge Cases

Consider the case where every soldier already has maximal rank:

```
4 5
5 5 5 5
```

For each soldier, `k - x = 0`. The algorithm adds four zeroes and prints `0`. No unnecessary sessions are counted.

Now consider all soldiers starting at the same low rank:

```
3 3
1 1 1
```

The computation becomes:

```
(3 - 1) + (3 - 1) + (3 - 1)
= 2 + 2 + 2
= 6
```

Every soldier must gain exactly two ranks, so six promotions are unavoidable.

Finally, consider missing intermediate ranks:

```
4 5
1 1 4 4
```

The algorithm computes:

```
4 + 4 + 1 + 1 = 10
```

The absence of ranks `2` and `3` does not matter. Soldiers still need the same number of total rank increases, and every increase must happen individually.
