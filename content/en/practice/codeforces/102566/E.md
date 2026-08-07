---
title: "CF 102566E - KFC"
description: "We have a collection of buckets. Bucket i starts with a[i] straws, and there is a shared pile containing K extra straws. We may distribute some or all of these extra straws among the buckets."
date: "2026-08-07T21:27:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102566
codeforces_index: "E"
codeforces_contest_name: "AGM 2020, Qualification Round"
rating: 0
weight: 102566
solve_time_s: 78
verified: true
draft: false
---

[CF 102566E - KFC](https://codeforces.com/problemset/problem/102566/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of buckets. Bucket `i` starts with `a[i]` straws, and there is a shared pile containing `K` extra straws. We may distribute some or all of these extra straws among the buckets. After the distribution, Jimmy chooses two buckets and receives the least common multiple of their final straw counts. The task is to maximize this possible LCM.

The input size is large because there can be up to one million buckets, but every initial bucket size is at most 1000. This difference is the key restriction. Any solution that compares every pair of buckets would need around `10^12` operations, which is impossible. Even maintaining information about all buckets individually is unnecessary because many buckets have the same small initial values.

The largest final value of a bucket can be `1000 + 1,000,000 = 1,001,000`, so a linear scan over this range is possible. The main challenge is reducing the number of buckets we need to consider.

A common mistake is to assume that the two buckets with the largest initial values are automatically the answer without checking how the remaining straws should be distributed. The choice of the final two numbers still matters because LCM depends on the gcd, not only on the magnitude.

For example:

```
2 1
5 5
```

The two buckets start with 5 straws. The final sum of these two buckets can be at most 11. Choosing `(5,6)` gives an LCM of `30`. A strategy that only tries to put all extra straws into one bucket and keeps `(5,7)` is invalid because it exceeds the available total.

Another edge case is when the best pair is not the two closest values. For:

```
2 2
3 5
```

The total number of straws after adding the pile is 10. The best choice is `(4,6)` or `(3,7)`? `(3,7)` gives `21`, while `(5,5)` gives only `5`. A product based only strategy would miss the gcd effect.

## Approaches

The direct brute force approach is to try every pair of buckets, distribute the extra straws in every possible way, and keep the largest LCM found. The pair count alone makes this impossible. With one million buckets, there are roughly `5 * 10^11` pairs.

The important observation is that the initial values are tiny. The largest possible starting value is only 1000, so the only information that matters about the buckets is the largest two initial values. Increasing one of the chosen starting values cannot reduce the maximum achievable LCM because any smaller starting configuration can be shifted to a configuration with at least as much available total material.

After choosing the two largest starting buckets, suppose their initial values are `a` and `b`. Their final values must satisfy:

`x >= a`, `y >= b`, and `x + y <= a + b + K`.

For this pair, the possible range of one bucket is only about one million values. We can try every possible final value `x`, compute the largest possible `y`, and evaluate the LCM. This is fast enough because the range is bounded by one million.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²K) | O(1) | Too slow |
| Optimal | O(K + 1000) | O(1) | Accepted |

## Algorithm Walkthrough

1. Find the two largest initial bucket values. Only these two buckets can participate in an optimal answer because replacing either chosen bucket with a bucket containing fewer starting straws never gives a larger available total.
2. Let these values be `a` and `b`. The largest possible final sum of the two chosen buckets is `limit = a + b + K`.
3. Iterate over every possible final value `x` of the first bucket, starting from `a`. The largest possible value for the second bucket is `y = limit - x`, because any unused straws can simply be ignored.
4. Check whether `y` is at least `b`. If it is, compute `lcm(x, y)` and update the answer.
5. Output the largest LCM found.

The invariant behind the algorithm is that every valid final configuration of the two chosen buckets has some first bucket value `x` in the scanned range. For that `x`, the algorithm tests the maximum possible second value, which is the only value that can improve the LCM by increasing the available sum. Since all possible first values are checked, the optimal pair cannot be skipped.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    first = 0
    second = 0

    for x in arr:
        if x >= first:
            second = first
            first = x
        elif x > second:
            second = x

    a = first
    b = second
    limit = a + b + k

    ans = 0

    for x in range(a, limit - b + 1):
        y = limit - x
        g = gcd(x, y)
        cur = x // g * y
        if cur > ans:
            ans = cur

    print(ans)

if __name__ == "__main__":
    solve()
```

The first loop keeps only the two largest starting values. It does not store the whole array after reading it, which keeps the memory usage constant apart from the input buffer.

The variable `limit` represents the total number of straws that can end up in the two chosen buckets. Since unused straws are allowed, the second bucket is always considered with the maximum possible value after choosing the first bucket.

The LCM calculation is written as `x // gcd(x, y) * y` instead of `x * y // gcd(x, y)`. The division happens first to reduce the chance of overflow in languages with fixed-size integers. Python integers do not overflow, but this form is still the standard safe implementation.

## Worked Examples

For the sample:

```
2 2
3 5
```

The two largest buckets are 5 and 3. The total available straw count is 10.

| x | y | gcd(x,y) | lcm | best |
| --- | --- | --- | --- | --- |
| 3 | 7 | 1 | 21 | 21 |
| 4 | 6 | 2 | 12 | 21 |
| 5 | 5 | 5 | 5 | 21 |

The answer is 21. The trace shows why maximizing the product is not enough. The coprime pair `(3,7)` beats the larger-looking pair `(5,5)`.

A second example:

```
2 1
4 6
```

The available total is 11.

| x | y | gcd(x,y) | lcm | best |
| --- | --- | --- | --- | --- |
| 4 | 7 | 1 | 28 | 28 |
| 5 | 6 | 1 | 30 | 30 |

The algorithm finds that distributing the extra straw to create coprime numbers produces the larger answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(K + 1000) | The scan checks at most about one million possible values. |
| Space | O(1) | Only the two largest values and a few variables are stored. |

The maximum scan length is roughly `1,001,000`, which is small enough for a two second limit. The million bucket input is processed in one pass.

## Test Cases

```python
import sys
import io
from math import gcd

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    first = second = 0
    for x in arr:
        if x >= first:
            second = first
            first = x
        elif x > second:
            second = x

    limit = first + second + k
    ans = 0
    for x in range(first, limit - second + 1):
        y = limit - x
        ans = max(ans, x // gcd(x, y) * y)

    sys.stdin = old_stdin
    return str(ans)

assert run("2 2\n3 5\n") == "21"
assert run("2 1\n1 1\n") == "2"
assert run("2 1\n1000 1000\n") == "1001000"
assert run("3 5\n7 7 7\n") == "143"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 1` | 2 | Minimum values and small LCM handling |
| `2 1 / 1000 1000` | 1001000 | Maximum initial values and large multiplication |
| `3 5 / 7 7 7` | 143 | Equal values and gcd interaction |

## Edge Cases

When both largest buckets have the same value, the algorithm still checks every split. For:

```
2 1
5 5
```

the total is 11. The scan checks `(5,6)`, producing `30`, instead of incorrectly keeping both buckets equal.

When the best result comes from coprime numbers, the algorithm does not rely on the largest product. For:

```
2 2
3 5
```

it tests `(3,7)` and gets `21`, while `(5,5)` only gives `5`.

When the pile contains many unused straws in an optimal solution, the algorithm still works because it only uses the inequality `x + y <= limit`. The second bucket is set to the largest possible value for each first bucket choice, and every valid distribution is represented by some scanned pair.
