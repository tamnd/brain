---
title: "CF 1612C - Chat Ban"
description: "We are asked to simulate a chat scenario where a user wants to send an \"emote triangle\" consisting of messages with increasing then decreasing numbers of emotes."
date: "2026-06-10T06:57:15+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math"]
categories: ["algorithms"]
codeforces_contest: 1612
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 117 (Rated for Div. 2)"
rating: 1300
weight: 1612
solve_time_s: 75
verified: true
draft: false
---

[CF 1612C - Chat Ban](https://codeforces.com/problemset/problem/1612/C)

**Rating:** 1300  
**Tags:** binary search, math  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate a chat scenario where a user wants to send an "emote triangle" consisting of messages with increasing then decreasing numbers of emotes. For a given size $k$, the first message has one emote, the second has two, up to the $k$-th message with $k$ emotes, then the following messages decrease back to one. This forms a sequence of $2k-1$ messages where the number of emotes in message $i$ is $\min(i, 2k-i)$.

The chat platform has a moderation system that bans a user once the total number of emotes sent reaches or exceeds a given threshold $x$. The task is to determine how many messages the user can send before being banned. If the user completes the triangle without exceeding $x$, the answer is $2k-1$.

The constraints are large: $k$ can be up to $10^9$ and $x$ up to $10^{18}$. A naive simulation that sums emotes message by message would be too slow, as it could require up to $2 \cdot 10^9$ additions per test case. This forces a solution that works in logarithmic or constant time per test case.

Non-obvious edge cases include small $k$ and very small $x$, for instance $k=1, x=1$. The triangle has only one message, and the user might be banned immediately. Another edge case is when $x$ is larger than the sum of the entire triangle. For $k=4$ and $x=20$, the sum of the triangle is 16. In this case, the user finishes all messages without being banned.

## Approaches

The brute-force approach is straightforward: generate the sequence of messages, keep a running sum, and count messages until the sum reaches or exceeds $x$. This works for small $k$ but fails when $k$ is large, as summing billions of messages is too slow. The worst-case operation count is $O(k)$ per test case, which is unacceptable for $k$ up to $10^9$ and $t$ up to $10^4$.

The key observation is that the number of emotes in each half of the triangle forms a simple arithmetic series. The first half increases from 1 to $k$ and sums to $k(k+1)/2$. The second half decreases from $k-1$ to 1, summing to $(k-1)k/2$. The total sum of the triangle is $k^2$. This allows us to quickly determine if $x$ exceeds the triangle sum, in which case the user writes all $2k-1$ messages.

If $x$ is smaller than $k(k+1)/2$, the user is banned in the increasing part. We can use the formula for the sum of the first $m$ natural numbers and solve the quadratic inequality $m(m+1)/2 \ge x$ to find the smallest $m$. If $x$ exceeds $k(k+1)/2$ but is less than $k^2$, the ban happens in the decreasing part. We can shift the problem: subtract the sum of the first half from $x$ to compute the remaining emotes, then apply a similar formula to the decreasing sequence. Using binary search on message count works efficiently in both halves.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) | O(1) | Too slow for large k |
| Optimal (Binary Search on Triangle Halves) | O(log k) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, compute the total emotes in the first half $S_1 = k(k+1)/2$. Compare $x$ to $S_1$.
2. If $x \le S_1$, the ban occurs in the increasing part. Use binary search on the range 1 to $k$ to find the minimal number of messages $m$ such that $m(m+1)/2 \ge x$. Return $m$.
3. If $x > S_1$ and $x \le k^2$, the ban occurs in the decreasing part. Compute the remaining emotes $x' = x - S_1$. The decreasing part consists of $k-1$ messages with emotes $k-1, k-2, ..., 1$. Use binary search on $1..k-1$ to find the minimal number of messages $m$ such that $(k-1 + k-2 + ... + (k-m)) \ge x'$. Equivalently, sum of last $m$ numbers from $k-1$ down: sum = $m(2k-m-1)/2$. Return $k + m$.
4. If $x > k^2$, the user completes all messages without being banned. Return $2k-1$.

Why it works: The triangle is strictly increasing then strictly decreasing. Using arithmetic series formulas guarantees that we find the exact point where the cumulative sum reaches $x$ without iterating over each message. Binary search ensures the minimal number of messages is computed correctly. The invariants are the cumulative sum bounds and the arithmetic progression sums, which are exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

def messages_before_ban(k, x):
    total = k * k
    if x >= total:
        return 2 * k - 1
    first_half = k * (k + 1) // 2
    if x <= first_half:
        # binary search in increasing part
        l, r = 1, k
        while l < r:
            m = (l + r) // 2
            if m * (m + 1) // 2 >= x:
                r = m
            else:
                l = m + 1
        return l
    else:
        # banned in decreasing part
        x_rem = x - first_half
        l, r = 1, k - 1
        while l < r:
            m = (l + r) // 2
            if m * (2 * k - m - 1) // 2 >= x_rem:
                r = m
            else:
                l = m + 1
        return k + l

t = int(input())
for _ in range(t):
    k, x = map(int, input().split())
    print(messages_before_ban(k, x))
```

The solution first checks whether the user completes the triangle without exceeding the ban threshold. It uses the arithmetic sum formula to handle the increasing and decreasing parts separately. Binary search is employed to efficiently find the minimal message count that exceeds the threshold, avoiding off-by-one mistakes by careful loop invariants.

## Worked Examples

**Example 1:** $k = 4, x = 6$

| Step | l | r | m | sum | Decision |
| --- | --- | --- | --- | --- | --- |
| start | 1 | 4 | 2 | 3 | sum < x → l = 3 |
| next | 3 | 4 | 3 | 6 | sum ≥ x → r = 3 |

Output is 3. The user is banned after sending three messages.

**Example 2:** $k = 3, x = 7$

First half sum = 6 < x → ban in decreasing part. Remaining x = 1. Decreasing sequence = 2,1.

| Step | l | r | m | sum | Decision |
| --- | --- | --- | --- | --- | --- |
| start | 1 | 2 | 1 | 2 | sum ≥ x → r = 1 |

Output = k + l = 3 + 1 = 4. User banned at 4th message.

These traces confirm the binary search correctly identifies the minimal message count in both halves.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log k) per test case | Binary search on increasing or decreasing half with at most k elements |
| Space | O(1) | Only variables for arithmetic calculations, no arrays needed |

Given $t \le 10^4$ and $k \le 10^9$, $O(t \log k)$ is acceptable for 2-second time limit. Python handles integers up to $10^{18}$ without overflow.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        k, x = map(int, input().split())
        print(messages_before_ban(k, x))
    return output.getvalue().strip()

# provided samples
assert run("7\n4 6\n4 7\n1 2\n3 7\n2 5\n100 1\n1000000000 923456789987654321\n") == \
"3\n4\n1\n4\n3\n1\n1608737403", "sample 1"

# custom tests
assert run("2\n1 1\n1
```
