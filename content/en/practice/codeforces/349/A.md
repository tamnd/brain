---
title: "CF 349A - Cinema Line"
description: "We are given a queue of people waiting to buy cinema tickets. Each person holds a bill worth 25, 50, or 100 rubles, and each ticket costs 25 rubles. The clerk starts with no money and must sell tickets in the exact order of the line, giving correct change if necessary."
date: "2026-06-06T18:42:15+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 349
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 202 (Div. 2)"
rating: 1100
weight: 349
solve_time_s: 196
verified: true
draft: false
---

[CF 349A - Cinema Line](https://codeforces.com/problemset/problem/349/A)

**Rating:** 1100  
**Tags:** greedy, implementation  
**Solve time:** 3m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a queue of people waiting to buy cinema tickets. Each person holds a bill worth 25, 50, or 100 rubles, and each ticket costs 25 rubles. The clerk starts with no money and must sell tickets in the exact order of the line, giving correct change if necessary. The task is to determine whether the clerk can serve everyone successfully.

The input provides the number of people $n$ and a sequence of integers representing the bills each person holds. The output is "YES" if every person can buy a ticket with correct change, or "NO" otherwise.

With $n$ up to $10^5$ and a 2-second limit, we need a solution that is linear or close to linear. Any approach that repeatedly searches through the current cash held would risk $O(n^2)$ complexity and could exceed the time limit.

Non-obvious edge cases include sequences where large bills appear early without enough small bills to provide change. For example, if the line is `[50, 25]`, the clerk cannot give change for the first person because he starts with no money. Another tricky case is `[25, 25, 50, 100]` versus `[25, 50, 25, 100]`, which require careful handling of the available bills when giving change for a 100-ruble note.

## Approaches

A brute-force approach would simulate the queue and, for each person, try all combinations of available bills to provide exact change. For a 100-ruble bill, this might involve checking multiple subsets of previously collected 25s and 50s. While correct in principle, the worst-case complexity grows quickly: for each of $n$ people, up to $O(n)$ operations may be required to find change, giving $O(n^2)$. For $n = 10^5$, this is too slow.

The key observation is that we never need to store all bills, only counts of 25s and 50s. A 50-ruble note always requires a single 25 as change, and a 100-ruble note requires either one 50 and one 25, or three 25s. This reduces the problem to a greedy strategy: always use the largest bills possible to give change. This works because smaller bills cannot substitute for larger bills in a cheaper combination, so prioritizing larger bills never blocks a valid solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two counters: `c25` for 25-ruble bills and `c50` for 50-ruble bills. Start both at zero. These track how many bills the clerk has at any moment.
2. Iterate through each person in the line, examining the bill they hold.
3. If the person has a 25-ruble bill, increment `c25` by one because no change is needed. This increases the clerk's available cash for future transactions.
4. If the person has a 50-ruble bill, check if `c25` is at least one. If so, decrement `c25` by one and increment `c50` by one. If not, the clerk cannot give change, so output "NO" and terminate.
5. If the person has a 100-ruble bill, first try to give change using one 50 and one 25, because this uses fewer 25s. If `c50 >= 1` and `c25 >= 1`, decrement both accordingly. Otherwise, check if `c25 >= 3` to give three 25s as change. If neither option is possible, output "NO" and terminate.
6. If the loop completes without failing, output "YES".

Why it works: At each step, the clerk's state is fully captured by the counts of 25 and 50 ruble bills. By always using the largest bills possible for change, we never block a future transaction. The invariant is that the clerk's cash composition always allows all previous transactions, and if the greedy choice fails, no alternative combination could succeed.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
bills = list(map(int, input().split()))

c25 = 0
c50 = 0

for bill in bills:
    if bill == 25:
        c25 += 1
    elif bill == 50:
        if c25 == 0:
            print("NO")
            sys.exit(0)
        c25 -= 1
        c50 += 1
    else:  # bill == 100
        if c50 >= 1 and c25 >= 1:
            c50 -= 1
            c25 -= 1
        elif c25 >= 3:
            c25 -= 3
        else:
            print("NO")
            sys.exit(0)

print("YES")
```

The code mirrors the algorithm steps exactly. Initializing counters ensures we know the clerk's resources at all times. The greedy choice for 100-ruble bills is explicit, prioritizing the use of 50s to minimize depletion of 25s. Using `sys.exit(0)` allows immediate termination when change cannot be provided.

## Worked Examples

Trace Sample 1:

Input: `[25, 25, 50, 50]`

| Person | Bill | c25 before | c50 before | Action | c25 after | c50 after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 25 | 0 | 0 | Accept, no change | 1 | 0 |
| 2 | 25 | 1 | 0 | Accept, no change | 2 | 0 |
| 3 | 50 | 2 | 0 | Give 25 change | 1 | 1 |
| 4 | 50 | 1 | 1 | Give 25 change | 0 | 2 |

Output is "YES". The trace confirms the clerk always had enough change.

Custom example:

Input: `[25, 100]`

| Person | Bill | c25 before | c50 before | Action | c25 after | c50 after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 25 | 0 | 0 | Accept, no change | 1 | 0 |
| 2 | 100 | 1 | 0 | Cannot give change | - | - |

Output is "NO". This tests the inability to provide change for a 100-ruble bill when only 25s are insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the array of bills, constant work per person |
| Space | O(1) | Only two counters maintained |

With $n \le 10^5$, the algorithm performs roughly 100,000 operations, well within the 2-second limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    bills = list(map(int, input().split()))

    c25 = 0
    c50 = 0

    for bill in bills:
        if bill == 25:
            c25 += 1
        elif bill == 50:
            if c25 == 0:
                return "NO"
            c25 -= 1
            c50 += 1
        else:  # bill == 100
            if c50 >= 1 and c25 >= 1:
                c50 -= 1
                c25 -= 1
            elif c25 >= 3:
                c25 -= 3
            else:
                return "NO"
    return "YES"

# Provided sample
assert run("4\n25 25 50 50\n") == "YES", "sample 1"

# Custom cases
assert run("2\n25 100\n") == "NO", "cannot give change for 100 early"
assert run("5\n25 25 25 50 100\n") == "YES", "enough 25s to cover 100"
assert run("3\n50 25 25\n") == "NO", "50 first, no change"
assert run("6\n25 25 50 50 25 100\n") == "YES", "mixed sequence handled correctly"
assert run("1\n25\n") == "YES", "single person, no change needed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n25 100 | NO | Cannot provide change for a 100-ruble bill early |
| 5\n25 25 25 50 100 | YES | Enough 25s to cover 100 |
| 3\n50 25 25 | NO | 50 first, no change available |
| 6\n25 25 50 50 25 100 | YES | Mixed sequence handled correctly |
| 1\n25 | YES | Single person, no change required |

## Edge Cases

For input `[50, 25]`, the algorithm immediately fails at the first person because `c25` is zero, correctly outputting "NO". For `[25, 25, 50, 100]`, the clerk gives change for 50 using one 25, then for 100
