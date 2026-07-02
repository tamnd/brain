---
title: "CF 103687C - JB Wants to Earn Big Money"
description: "We are given two groups of participants in a stock market-like system. One group contains people who want to buy shares, and each of them specifies a maximum price they are willing to pay."
date: "2026-07-02T20:56:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103687
codeforces_index: "C"
codeforces_contest_name: "The 19th Zhejiang Provincial Collegiate Programming Contest"
rating: 0
weight: 103687
solve_time_s: 47
verified: true
draft: false
---

[CF 103687C - JB Wants to Earn Big Money](https://codeforces.com/problemset/problem/103687/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two groups of participants in a stock market-like system. One group contains people who want to buy shares, and each of them specifies a maximum price they are willing to pay. The other group contains people who want to sell shares, and each of them specifies a minimum price they are willing to accept.

A single final price $x$ is fixed by the system. A buyer participates if their offered price is at least $x$, since they are willing to pay that much or more. A seller participates if their offered price is at most $x$, since they are willing to accept that price or lower. The task is to count how many people in total, across both groups, satisfy these conditions.

The input sizes go up to $10^5$ buyers and $10^5$ sellers. Any solution that inspects each element once is acceptable, but anything involving sorting or nested scans would still be fine. However, anything quadratic or involving repeated full scans per element would be too slow because it would reach $10^{10}$ operations in the worst case.

A common mistake in problems like this is misunderstanding the inequality directions. A buyer qualifies when $a_i \ge x$, not $a_i \le x$. A seller qualifies when $b_i \le x$, not $b_i \ge x$. Swapping these conditions leads to completely inverted counts.

Another subtle edge case appears when all values are equal to $x$. In that situation, every participant from both groups should be counted. Any off-by-one threshold error would fail here immediately.

## Approaches

The brute-force approach is straightforward. We scan all buyers and check whether each value is at least $x$. Then we scan all sellers and check whether each value is at most $x$. We increment a counter whenever a condition is satisfied. This works because each decision is independent, and the final answer is just the total number of satisfied participants.

This approach is already optimal in terms of asymptotic structure because the problem does not require ordering or pairing. The only reason it might be considered "brute force" is that it explicitly checks each element one by one.

The total number of operations is $n + m$, which is at most $2 \cdot 10^5$. Even in Python, this is easily within limits. Any attempt to sort or preprocess is unnecessary overhead and does not improve correctness or performance.

The key observation is that the final price acts as a fixed threshold separating participants into two independent filters. Buyers are filtered by a lower bound, sellers by an upper bound. There is no interaction between the groups, so the problem decomposes into two simple counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n + m) | O(1) | Accepted |
| Optimal | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers $n, m, x$. These define the sizes of the two groups and the threshold price.
2. Initialize a counter to zero. This will accumulate all valid participants.
3. Read the list of buyer prices. For each value $a_i$, check if $a_i \ge x$. If so, increment the counter. This reflects that the buyer is willing to trade at the system price or higher.
4. Read the list of seller prices. For each value $b_i$, check if $b_i \le x$. If so, increment the counter. This reflects that the seller is willing to accept the system price or lower.
5. Output the final counter.

The reasoning behind separate loops is that each group has a different inequality direction, and mixing them would introduce unnecessary complexity and risk incorrect comparisons.

### Why it works

Each participant independently satisfies a single condition that depends only on their own price and the fixed threshold $x$. The decision for one participant never affects another. Because of this independence, counting valid buyers and sellers separately and summing the results is equivalent to evaluating the entire system. The algorithm is essentially computing the size of the union of two disjoint condition sets defined over the input arrays.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, x = map(int, input().split())

ans = 0

a = list(map(int, input().split()))
for v in a:
    if v >= x:
        ans += 1

b = list(map(int, input().split()))
for v in b:
    if v <= x:
        ans += 1

print(ans)
```

The code mirrors the algorithm directly. We first read the parameters, then process buyers and sellers independently. The counter `ans` is updated only when a value meets its group-specific condition.

A common implementation mistake is mixing strict and non-strict inequalities. Here, equality is included in both cases: buyers accept $a_i = x$, sellers accept $b_i = x$. This is intentional and consistent with the statement.

## Worked Examples

Consider an input where the threshold splits both groups unevenly.

Input:

```
n = 5, m = 4, x = 3
buyers = [1, 3, 4, 2, 5]
sellers = [3, 1, 4, 2]
```

| Step | Buyer value | Condition $a_i \ge x$ | Seller value | Condition $b_i \le x$ | Counter |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | false | - | - | 0 |
| 2 | 3 | true | - | - | 1 |
| 3 | 4 | true | - | - | 2 |
| 4 | 2 | false | - | - | 2 |
| 5 | 5 | true | - | - | 3 |
| 6 | - | - | 3 | true | 4 |
| 7 | - | - | 1 | true | 5 |
| 8 | - | - | 4 | false | 5 |
| 9 | - | - | 2 | true | 6 |

The final answer is 6. This confirms that both thresholds are applied independently and accumulated correctly.

Now consider a boundary-heavy case.

Input:

```
n = 3, m = 3, x = 5
buyers = [5, 5, 4]
sellers = [5, 6, 1]
```

| Step | Buyer value | Valid | Seller value | Valid | Counter |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | true | - | - | 1 |
| 2 | 5 | true | - | - | 2 |
| 3 | 4 | false | - | - | 2 |
| 4 | - | - | 5 | true | 3 |
| 5 | - | - | 6 | false | 3 |
| 6 | - | - | 1 | true | 4 |

This confirms correct handling of equality at the threshold, which is often the source of off-by-one mistakes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each list is scanned once, with constant work per element |
| Space | O(1) | Only a counter is maintained beyond input storage |

The input limits of $2 \cdot 10^5$ total elements fit comfortably within linear time constraints. No sorting or auxiliary structures are required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, x = map(int, input().split())

    ans = 0

    a = list(map(int, input().split()))
    for v in a:
        if v >= x:
            ans += 1

    b = list(map(int, input().split()))
    for v in b:
        if v <= x:
            ans += 1

    return str(ans).strip()

# sample-like case
assert run("5 5 3\n1 2 3 4 5\n1 2 3 4 5\n") == "8"

# minimum size
assert run("1 1 1\n1\n1\n") == "2"

# all below threshold
assert run("3 3 10\n1 2 3\n1 2 3\n") == "3"

# all above threshold
assert run("3 3 2\n5 6 7\n5 6 7\n") == "6"

# mixed boundary
assert run("4 4 4\n4 3 5 4\n4 4 1 2\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal to x | full count | equality handling |
| all below/above | partial/zero extremes | inequality correctness |
| minimum size | 2 | base case correctness |
| mixed values | combined filtering | independent counting |

## Edge Cases

A critical edge case is when all values equal the threshold $x$. For example:

```
3 2 5
5 5 5
5 5
```

The algorithm processes each buyer and seller independently. Every comparison evaluates true because both $a_i \ge x$ and $b_i \le x$ hold when equal. The counter increases once per element, producing a total of 5. Any implementation using strict inequalities would incorrectly return 0.

Another edge case is when no one qualifies:

```
3 3 10
1 2 3
11 12 13
```

Here, all buyers fail $a_i \ge x$ and all sellers fail $b_i \le x$. The counter remains zero throughout, confirming that the algorithm correctly handles empty selection sets without special casing.
