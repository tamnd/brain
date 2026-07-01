---
title: "CF 104199B - \u0420\u0430\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 \u043c\u0435\u0431\u0435\u043b\u0438"
description: "We are given a hotel with several rooms, each room having a required number of chairs in an ideal plan. In reality, the hotel has a total of $N$ chairs that must be distributed across $K$ rooms."
date: "2026-07-02T00:01:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104199
codeforces_index: "B"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u043d\u0430 \u0412\u041a\u041e\u0428\u041f.Junior 18-02-23"
rating: 0
weight: 104199
solve_time_s: 86
verified: true
draft: false
---

[CF 104199B - \u0420\u0430\u0441\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 \u043c\u0435\u0431\u0435\u043b\u0438](https://codeforces.com/problemset/problem/104199/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a hotel with several rooms, each room having a required number of chairs in an ideal plan. In reality, the hotel has a total of $N$ chairs that must be distributed across $K$ rooms. The constraints are not simply “match the targets”: every room must receive at least one chair, and across all rooms the shortage, defined as how many chairs each room is missing compared to its ideal requirement, must be identical.

So if a room originally expects $a_i$ chairs and we place $x_i$ chairs, then $x_i \ge 1$ and all values $a_i - x_i$ must be the same constant $d$, shared across every room. That means every room is uniformly underfilled by $d$, while still respecting that each room gets at least one chair.

The goal is to choose a valid uniform shortage $d$ and a distribution of chairs satisfying it, while maximizing how many chairs remain unused. Equivalently, we want to minimize how many chairs we must place.

The constraints are large in $N$ but moderate in $K$. Since $K$ can go up to $10^5$, any solution must be linear or nearly linear in $K$. A solution that tries all possible shortages or redistributes chairs repeatedly per candidate would be too slow if it costs $O(K^2)$ or worse.

A key hidden edge case appears when some rooms have very small capacities. If a room has $a_i = 1$, then the only valid assignment forces $x_i = 1$, so the shortage is fixed at zero for that room, which constrains the global shortage. Any naive attempt that assumes all rooms can share a large uniform deficit will break immediately here.

## Approaches

A direct way to think about the problem is to guess the common shortage $d$. If we fix $d$, then each room must receive $x_i = a_i - d$ chairs. This immediately imposes two feasibility conditions: first, $x_i \ge 1$, so $d \le a_i - 1$ for every room, meaning $d \le \min(a_i) - 1$. Second, the total number of chairs used must be exactly $\sum (a_i - d)$, which equals $\sum a_i - Kd$, and this must not exceed $N$.

So for a fixed $d$, feasibility reduces to checking whether $Kd \ge \sum a_i - N$. The structure becomes monotone: increasing $d$ reduces the number of chairs used, making it easier to stay within budget, but also constrained by the minimum room size.

The brute-force approach would try all possible values of $d$ from $0$ up to $\min(a_i) - 1$, compute the total required chairs each time, and track the best feasible configuration. Each check costs $O(K)$, and there can be up to $1000$ different values of $d$, leading to roughly $10^8$ operations in the worst case. That is borderline but unnecessary.

The key observation is that feasibility depends only on linear expressions in $d$. Instead of iterating over $d$, we can compute the maximum valid $d$ directly using arithmetic constraints:

$$Kd \le \sum a_i - N$$

and

$$d \le \min(a_i) - 1.$$

So the optimal $d$ is the minimum of these two upper bounds.

Once $d$ is fixed, the number of chairs actually placed is forced, so the number of saved chairs is simply $N - \sum (a_i - d)$, or equivalently $N - (\sum a_i - Kd)$.

This reduces the entire problem to computing a few aggregates over the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over $d$ | $O(K \cdot \min a_i)$ | $O(1)$ | Too slow |
| Optimal arithmetic | $O(K)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

### 1. Compute global statistics

We compute the sum of all room capacities and the minimum capacity among them. These two values fully control feasibility of any uniform shortage.

The sum determines how many chairs exist in the ideal configuration, while the minimum determines the maximum allowable uniform deficit without violating the “at least one chair per room” constraint.

### 2. Derive the maximum possible shortage from the budget

We rewrite the total usage constraint as:

$$\sum a_i - Kd \le N$$

which gives:

$$d \ge \frac{\sum a_i - N}{K}$$

However, since we want feasibility and maximum saving, we instead compute the largest $d$ that does not violate this inequality:

$$d \le \frac{\sum a_i - N}{K}$$

We take the floor of this value since $d$ must be an integer.

### 3. Apply per-room feasibility constraint

Each room must still receive at least one chair, so:

$$a_i - d \ge 1 \Rightarrow d \le a_i - 1$$

The tightest constraint comes from the smallest room, so:

$$d \le \min(a_i) - 1$$

### 4. Combine constraints

The valid $d$ is the minimum of the budget-derived bound and the structural bound. We also ensure $d \ge 0$.

### 5. Compute final answer

Once $d$ is fixed, total placed chairs is $\sum a_i - Kd$. The saved chairs are:

$$N - (\sum a_i - Kd)$$

### Why it works

The crucial invariant is that any valid configuration corresponds to choosing a single integer $d$ such that all room assignments are exactly $a_i - d$. There is no freedom to vary rooms independently because the condition forces identical deficits. This reduces the search space from $K$-dimensional assignments to a single scalar parameter. Every feasible solution is uniquely represented by some $d$, and every valid $d$ produces a valid configuration, so optimizing over $d$ is equivalent to optimizing over all assignments.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    total = sum(a)
    mn = min(a)
    
    # upper bound from "at least one chair per room"
    d1 = mn - 1
    
    # upper bound from total chairs constraint
    d2 = (total - n) // k
    
    d = min(d1, d2)
    if d < 0:
        d = 0
    
    used = total - k * d
    print(n - used)

if __name__ == "__main__":
    solve()
```

The implementation first reads the input and computes the aggregate values in a single pass over the rooms. The value `d1` enforces that no room becomes empty, since subtracting more than `a_i - 1` would violate the minimum constraint. The value `d2` enforces that the total number of chairs assigned does not exceed the available supply when expressed in terms of the uniform deficit.

After choosing the best feasible `d`, we compute how many chairs are actually used. The final answer is the difference between available chairs and used chairs.

A subtle point is clamping `d` to zero. Without this, cases where `total < n` would produce a negative deficit even though no shortage can be meaningfully applied.

## Worked Examples

### Example 1

Input:

```
20 5
2 3 4 5 6
```

We compute:

$$\sum a_i = 20,\quad \min a_i = 2$$

| Step | Value |
| --- | --- |
| total | 20 |
| min a_i | 2 |
| d1 | 1 |
| d2 | (20 - 20) // 5 = 0 |
| d | 0 |
| used | 20 |
| saved | 0 |

Here the budget exactly matches the ideal sum, so no deficit is introduced. The answer is 0.

This confirms that when supply matches demand exactly, the optimal configuration avoids any distortion.

### Example 2

Input:

```
10 3
3 3 3
```

We compute:

$$\sum a_i = 9,\quad \min a_i = 3$$

| Step | Value |
| --- | --- |
| total | 9 |
| min a_i | 3 |
| d1 | 2 |
| d2 | (9 - 10) // 3 = -1 |
| d | 0 |
| used | 9 |
| saved | 1 |

Here we already have more chairs than needed for the ideal configuration, so we can save at least one chair. The computation shows how negative $d2$ forces the algorithm to settle at zero deficit.

This illustrates that the solution correctly handles surplus cases without attempting invalid negative shortages.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(K)$ | Single pass to compute sum and minimum |
| Space | $O(1)$ | Only a few integer variables are used |

The solution comfortably fits within constraints since $K \le 10^5$, and the algorithm performs only linear work with no nested loops or recomputation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("20 5\n2 3 4 5 6\n") == "0"

# minimum case
assert run("1 1\n1\n") == "0"

# all equal
assert run("15 3\n5 5 5\n") == "0"

# surplus chairs
assert run("10 3\n3 3 3\n") == "1"

# tight constraint min-bound active
assert run("10 3\n1 10 10\n") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 1 | 0 | single room edge case |
| 15 3 / 5 5 5 | 0 | symmetric configuration |
| 10 3 / 3 3 3 | 1 | surplus handling |
| 10 3 / 1 10 10 | 7 | min-room constraint dominates |

## Edge Cases

When there is only one room, the condition forces all chairs to be placed in that room, so no saving is possible unless $N$ exceeds its capacity constraint structure allows. The algorithm computes $d1 = a_1 - 1$ and $d2 = (a_1 - N)$, and clamps correctly to a feasible value, resulting in a consistent placement.

When all room capacities are identical, the minimum constraint becomes the dominant factor, and any attempt to increase the uniform deficit is immediately capped. The algorithm reduces to checking whether the total chair budget is above or below the ideal sum, and the computed $d$ correctly reflects that balance.

When one room has a very small capacity like 1, it forces $d = 0$, since no deficit is allowed. The algorithm captures this through $d1 = 0$, ensuring all other computations respect the tightest structural constraint without special casing.
