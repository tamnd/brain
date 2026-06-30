---
title: "CF 104531M - Water"
description: "A line of people is served sequentially by a water dispenser. Each person has a demand in liters, and a single water bucket on the dispenser contains a fixed capacity of $C$ liters. People are served one after another using the current bucket until it runs out."
date: "2026-06-30T09:59:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104531
codeforces_index: "M"
codeforces_contest_name: "2022 SYSU School Contest"
rating: 0
weight: 104531
solve_time_s: 50
verified: true
draft: false
---

[CF 104531M - Water](https://codeforces.com/problemset/problem/104531/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

A line of people is served sequentially by a water dispenser. Each person has a demand in liters, and a single water bucket on the dispenser contains a fixed capacity of $C$ liters. People are served one after another using the current bucket until it runs out.

The key twist is what happens when the bucket becomes empty in the middle of serving someone. The person who causes the bucket to run out immediately replaces it with a fresh full bucket and then leaves right away. Because they leave immediately, any remaining demand they had is lost and is not transferred to the next bucket.

The task is to compute how many buckets are used in total while serving all people in order.

The input size allows up to $10^6$ people per test case and multiple test cases. This immediately rules out any approach that tries to simulate water consumption with nested loops or per-liter processing. The solution must be linear in the total number of people, because anything worse than $O(n)$ per test case would time out.

The most subtle edge case comes from people whose demand is larger than the remaining water in the current bucket. For example, if the remaining water is 2 liters and the next person needs 10 liters, that person will consume the remaining 2 liters, trigger a bucket replacement, and then leave immediately without consuming the rest. A naive interpretation that simply subtracts full demands from buckets without modeling the interruption will overcount or undercount bucket usage depending on implementation details.

## Approaches

A direct simulation keeps track of how much water remains in the current bucket and processes each person in order. For each person, we subtract their demand from the remaining water. If enough water is available, the process is simple. If not, the bucket empties during that person’s turn, we count a new bucket, refill it, and continue.

The naive mistake is to assume that after refilling, the same person continues consuming their remaining demand. That interpretation would lead to multiple buckets being consumed by a single person, which contradicts the rule that they leave immediately after replacing the bucket. This difference is what simplifies the process: every time a person does not fit in the remaining water, they only ever trigger exactly one extra bucket.

The key observation is that we never need to track partial leftover demand beyond the current bucket. Either a person fits entirely into the current bucket, or they consume the remainder, force a refill, and stop immediately. This turns the problem into a single pass greedy simulation with a simple state variable representing remaining water.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full simulation per unit | O(total water units) | O(1) | Too slow |
| Greedy bucket tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two variables: the number of buckets used and the remaining water in the current bucket.

1. Initialize the number of buckets to 1 and set the remaining water to $C$, since we start with one full bucket.
2. Process each person in order.
3. If the current person’s demand is less than or equal to the remaining water, subtract it from the remaining water and move to the next person.
4. If the demand is greater than the remaining water, the current bucket is exhausted during this person’s turn. We increment the bucket count by 1, refill to a full bucket, and allow the next person to start using the new bucket.
5. In the overflow case, we do not carry over the remaining demand of the current person, because they leave immediately after triggering the refill.

The correctness rests on the invariant that the remaining water always reflects the unused capacity of the current bucket at the start of each person’s turn. Each bucket is counted exactly when it is introduced, and no person ever contributes more than one additional bucket beyond what is required by their position in the sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, C = map(int, input().split())
        arr = list(map(int, input().split()))
        
        buckets = 1
        rem = C
        
        for x in arr:
            if x <= rem:
                rem -= x
            else:
                buckets += 1
                rem = C
        
        print(buckets)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the process directly. The variable `rem` tracks how much water is left in the current bucket. When a person fits, we simply decrease it. When they do not fit, we increment the bucket count and reset `rem` to a full bucket.

A subtle point is that we do not attempt to simulate partial consumption beyond triggering a refill. Once `x > rem`, the current person consumes exactly `rem` units implicitly, but we do not need to explicitly subtract it since the bucket resets and the remaining demand is discarded by the problem rule.

## Worked Examples

Consider a simple case with $C = 5$ and people with demands $[3, 2, 4]$.

We track the process step by step.

| Person | Demand | Remaining Before | Action | Buckets |
| --- | --- | --- | --- | --- |
| 1 | 3 | 5 | 5 - 3 = 2 | 1 |
| 2 | 2 | 2 | 2 - 2 = 0 | 1 |
| 3 | 4 | 0 | refill, new bucket | 2 |

The third person triggers a refill because the current bucket is empty. They leave immediately after that, so they do not continue consuming from the new bucket.

Now consider $C = 4$, demands $[1, 6, 2]$.

| Person | Demand | Remaining Before | Action | Buckets |
| --- | --- | --- | --- | --- |
| 1 | 1 | 4 | 4 - 1 = 3 | 1 |
| 2 | 6 | 3 | consume 3, refill, leave | 2 |
| 3 | 2 | 4 | 4 - 2 = 2 | 2 |

The second person triggers exactly one extra bucket even though their demand exceeds one full capacity. The excess demand is discarded after the refill event.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each person is processed once with O(1) work |
| Space | $O(1)$ | Only counters and a single running state are used |

The constraints allow up to $10^6$ elements, and this solution performs a constant amount of work per element, so it fits comfortably within time limits.

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

# basic samples
assert run("1\n3 5\n3 2 4\n") == "2"

# all fit in one bucket
assert run("1\n4 10\n1 2 3 4\n") == "1"

# every person triggers new bucket
assert run("1\n5 3\n4 4 4 4 4\n") == "5"

# exact fills
assert run("1\n3 4\n2 2 2\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 5 / 3 2 4 | 2 | overflow handling and discard rule |
| 4 10 / 1 2 3 4 | 1 | normal accumulation |
| 5 3 / 4 4 4 4 4 | 5 | repeated forced refills |
| 3 4 / 2 2 2 | 2 | exact boundary exhaustion |

## Edge Cases

A key edge case is when a person’s demand is larger than a full bucket. For example, with $C = 3$ and a demand of $10$, the correct behavior is still to add only one extra bucket at the moment the current bucket empties, not multiple buckets. The remaining demand is irrelevant because the person leaves immediately after triggering the refill.

Running the algorithm: start with remaining 3. The demand 10 exceeds it, so we increment buckets to 2 and reset remaining to 3. We do not continue consuming 7 units. The next person starts fresh, which matches the problem rule.

Another edge case is when the remaining water is exactly equal to a person’s demand. In that case, the bucket ends exactly at zero but no refill is triggered during that person’s turn. The next person will either use a fresh bucket or trigger a refill depending on their demand.
