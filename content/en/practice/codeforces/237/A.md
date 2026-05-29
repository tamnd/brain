---
title: "CF 237A - Free Cash"
description: "We are given the arrival times of customers visiting a cafe during one day. Every customer is served in less than one minute, so the only time a queue can appear is when several customers arrive at exactly the same minute."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 237
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 147 (Div. 2)"
rating: 1000
weight: 237
solve_time_s: 197
verified: true
draft: false
---

[CF 237A - Free Cash](https://codeforces.com/problemset/problem/237/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 3m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the arrival times of customers visiting a cafe during one day. Every customer is served in less than one minute, so the only time a queue can appear is when several customers arrive at exactly the same minute.

The cafe needs enough cash desks operating so that every customer who arrives can immediately start being served. If three people arrive at 12:30, then at least three cash desks must exist at that moment. Customers arriving at different minutes never overlap because service time is strictly less than one minute.

The task is simply to find the largest number of customers sharing the same arrival time.

The input already comes in chronological order, which is useful because equal times will appear consecutively. With up to $10^5$ customers, the solution must run efficiently. A quadratic approach that compares every pair of customers would require around $10^{10}$ operations in the worst case, which is far too slow for a 2-second limit. Linear or near-linear solutions are appropriate here.

One easy mistake is forgetting that only identical times matter. Consider:

```
3
10 00
10 01
10 02
```

The correct answer is:

```
1
```

Even though the arrivals are close together, each customer finishes before the next minute begins.

Another common bug appears when counting consecutive equal times and forgetting to update the maximum at the end of the loop. For example:

```
4
9 30
9 30
9 30
9 30
```

The correct answer is:

```
4
```

If the implementation only updates the answer when the time changes, it may incorrectly print `0` or `1`.

A third edge case happens when there is only one customer:

```
1
0 0
```

The answer must still be:

```
1
```

Some implementations initialize counters incorrectly and accidentally return `0`.

## Approaches

The brute-force idea is straightforward. For every customer, scan the entire array and count how many customers have the same hour and minute. The maximum such count is the required number of cash desks.

This works because the problem only asks for the highest frequency of an arrival time. If five customers arrive at 14:20, then every customer with time 14:20 contributes to the same count.

The issue is performance. With $n = 10^5$, comparing every pair of customers performs roughly $10^{10}$ comparisons. That is much too slow.

The key observation is that the input is already sorted chronologically. Equal times always appear next to each other. That means we do not need to repeatedly scan the whole array. We only need to count the length of each consecutive block of identical times.

As we iterate through the arrivals, we maintain the current streak length. If the next time matches the previous one, we extend the streak. Otherwise, we start a new streak from 1. The largest streak encountered during the scan is the answer.

This reduces the problem to a single linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of customers.
2. Read the first arrival time and treat it as the current active time. Initialize both the current streak and the answer to 1.

At least one customer exists, so the minimum answer is always 1.
3. Iterate through the remaining customers one by one.
4. For each new arrival time, compare it with the previous time.

If both the hour and minute are equal, increment the current streak because another customer arrived at the same moment.
5. If the time differs, reset the current streak to 1.

A new group of equal times has started.
6. After updating the streak, update the global maximum answer.
7. Print the maximum streak length.

### Why it works

Because the input is sorted chronologically, all customers arriving at the same minute form one continuous segment in the array. The algorithm computes the size of every such segment and keeps the largest one.

The current streak always represents the number of consecutive customers sharing the same arrival time up to the current position. Since every identical-time group is processed exactly once, the maximum streak found during the scan is exactly the minimum number of cash desks needed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    prev_h, prev_m = map(int, input().split())

    current = 1
    answer = 1

    for _ in range(n - 1):
        h, m = map(int, input().split())

        if h == prev_h and m == prev_m:
            current += 1
        else:
            current = 1

        answer = max(answer, current)

        prev_h, prev_m = h, m

    print(answer)

solve()
```

The solution begins by reading the first customer separately. This avoids awkward special handling inside the loop and guarantees that both `current` and `answer` start from valid values.

The variable `current` stores the size of the ongoing block of identical times. Whenever the current arrival matches the previous one, the block grows by one. Otherwise, a completely new block begins, so the streak resets to 1.

The answer is updated after every iteration. This is important because the largest block may appear at the very end of the input. Forgetting this update is one of the most common mistakes for this problem.

The algorithm uses constant extra memory because it only stores the previous arrival time and two counters.

## Worked Examples

### Sample 1

Input:

```
4
8 0
8 10
8 10
8 45
```

| Step | Current Time | Previous Time | Current Streak | Best Answer |
| --- | --- | --- | --- | --- |
| Start | 8:00 | 8:00 | 1 | 1 |
| 1 | 8:10 | 8:00 | 1 | 1 |
| 2 | 8:10 | 8:10 | 2 | 2 |
| 3 | 8:45 | 8:10 | 1 | 2 |

The largest consecutive block of equal times has size 2, corresponding to the two customers arriving at 8:10. That means two cash desks are required.

### Sample 2

Input:

```
3
1 1
2 2
3 3
```

| Step | Current Time | Previous Time | Current Streak | Best Answer |
| --- | --- | --- | --- | --- |
| Start | 1:01 | 1:01 | 1 | 1 |
| 1 | 2:02 | 1:01 | 1 | 1 |
| 2 | 3:03 | 2:02 | 1 | 1 |

Every customer arrives at a different minute, so one cash desk is always enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One linear scan through all customers |
| Space | O(1) | Only a few variables are stored |

With $10^5$ customers, a linear solution easily fits within the time limit. The memory usage is constant and negligible compared to the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())

        prev_h, prev_m = map(int, input().split())

        current = 1
        answer = 1

        for _ in range(n - 1):
            h, m = map(int, input().split())

            if h == prev_h and m == prev_m:
                current += 1
            else:
                current = 1

            answer = max(answer, current)

            prev_h, prev_m = h, m

        return str(answer)

    return solve()

# provided sample
assert run(
    "4\n8 0\n8 10\n8 10\n8 45\n"
) == "2", "sample 1"

# minimum-size input
assert run(
    "1\n0 0\n"
) == "1", "single customer"

# all arrivals equal
assert run(
    "5\n12 30\n12 30\n12 30\n12 30\n12 30\n"
) == "5", "all equal times"

# all arrivals distinct
assert run(
    "4\n1 0\n1 1\n1 2\n1 3\n"
) == "1", "all unique times"

# maximum block at the end
assert run(
    "6\n5 0\n5 1\n5 2\n6 0\n6 0\n6 0\n"
) == "3", "largest streak at end"

# boundary times
assert run(
    "3\n0 0\n23 59\n23 59\n"
) == "2", "boundary hour and minute values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single customer | 1 | Correct initialization |
| All equal times | 5 | Long consecutive streak |
| All distinct times | 1 | No unnecessary counting |
| Largest block at end | 3 | Final streak handling |
| Boundary times | 2 | Correct handling of 0:00 and 23:59 |

## Edge Cases

Consider the case where every customer arrives at the same minute:

```
4
9 30
9 30
9 30
9 30
```

The algorithm starts with `current = 1`. Each new arrival matches the previous time, so the streak grows to 2, then 3, then 4. The answer is updated after every increment, producing the correct output:

```
4
```

Now consider completely distinct arrival times:

```
3
10 00
10 01
10 02
```

Each comparison fails because the minute changes every time. The streak repeatedly resets to 1, and the maximum never exceeds 1. The output becomes:

```
1
```

Finally, consider the tricky case where the largest group appears at the end:

```
5
8 00
8 10
9 00
9 00
9 00
```

The algorithm processes the first three customers with streaks `1, 1, 1`. Then the last two arrivals extend the streak to 2 and 3. Since the answer is updated during every iteration, the final result correctly becomes:

```
3
```
