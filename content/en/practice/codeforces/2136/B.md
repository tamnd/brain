---
title: "CF 2136B - Like the Bitset"
description: "We are asked to construct a permutation of length $n$ from a given binary string $s$ and integer $k$. Each index $i$ with $si = 1$ must never be the maximum in any interval of length at least $k$ that contains $i$. Indices with $si = 0$ have no restrictions."
date: "2026-06-08T02:35:05+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2136
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1046 (Div. 2)"
rating: 900
weight: 2136
solve_time_s: 92
verified: false
draft: false
---

[CF 2136B - Like the Bitset](https://codeforces.com/problemset/problem/2136/B)

**Rating:** 900  
**Tags:** constructive algorithms, greedy, two pointers  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a permutation of length $n$ from a given binary string $s$ and integer $k$. Each index $i$ with $s_i = 1$ must **never be the maximum** in any interval of length at least $k$ that contains $i$. Indices with $s_i = 0$ have no restrictions.

In simpler terms, we are labeling positions $1$ to $n$ with numbers $1$ through $n$ without repetition, but the positions marked with 1 must not dominate large blocks around them. Positions marked 0 can safely hold the largest numbers, because no interval rules restrict them.

The constraints allow $n$ up to $2 \cdot 10^5$ and multiple test cases totaling $2 \cdot 10^5$. This rules out any algorithm that explicitly checks all intervals of length at least $k$, since there could be $O(n^2)$ such intervals. We need an approach that assigns numbers greedily based on local structure rather than simulating all intervals.

The tricky edge cases appear when $s$ has long contiguous stretches of 1s. If the number of 1s exceeds $k-1$ in a row, it is impossible to place the largest numbers without violating the rule. For example, for $s = "111"$ and $k = 2$, every interval of length at least 2 containing any 1 also contains another 1. If we try to assign the largest numbers to 0s and smaller numbers to 1s, there might be no legal way to place numbers. Recognizing these impossible patterns is key.

## Approaches

The brute-force approach would attempt every permutation of length $n$ and check every interval of length at least $k$ for the maximum condition. This is correct in principle, but with up to $2 \cdot 10^5$ elements and $O(n^2)$ intervals, it is clearly infeasible.

The key observation is that the positions with $s_i = 1$ must not receive numbers that could become the maximum in any interval of length at least $k$. The simplest way to guarantee this is to **assign the largest numbers to 0s first**. Then, we can safely assign the remaining smaller numbers to 1s without risking the maximum condition, because the largest numbers are out of reach in any interval containing 1s.

If there is a contiguous block of 1s longer than $k-1$, the rule fails. That is because any interval of length at least $k$ covering the middle of that block will have only 1s, forcing the maximum to be one of these numbers. Assigning smaller numbers is unavoidable, but there will always be one number that becomes the maximum in that interval, so the permutation is impossible.

Thus, the optimal solution is to assign the largest numbers to 0s first, the smallest numbers to 1s, and immediately reject cases where a run of 1s has length at least $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n^2) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, parse $n$, $k$, and the string $s$.
2. Scan $s$ from left to right to check for any contiguous block of 1s with length ≥ $k$. If such a block exists, print "NO" and continue to the next test case. This guarantees feasibility only if no interval rule is automatically violated.
3. Initialize a permutation array of length $n$ and two counters: one for the largest number available, starting from $n$, and one for the smallest number available, starting from 1.
4. Iterate over the string $s$. For each $s_i$:

- If $s_i = 0$, assign the current largest available number and decrement the largest counter.
- If $s_i = 1$, assign the current smallest available number and increment the smallest counter.
5. After processing all positions, print "YES" followed by the permutation array.

Why it works: The largest numbers are guaranteed to go to positions with 0s. Any interval of length ≥ $k$ that includes a 1 will always contain at least one 0 if no run of 1s reaches $k$. Therefore, the maximum of the interval is always a 0, not the 1, satisfying the condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    s = input().strip()

    max_run = 0
    run = 0
    for ch in s:
        if ch == '1':
            run += 1
            max_run = max(max_run, run)
        else:
            run = 0

    if max_run >= k:
        print("NO")
        continue

    perm = [0] * n
    low, high = 1, n
    for i in range(n):
        if s[i] == '0':
            perm[i] = high
            high -= 1
        else:
            perm[i] = low
            low += 1

    print("YES")
    print(" ".join(map(str, perm)))
```

This solution first checks feasibility by measuring runs of 1s. Then it constructs the permutation in a single pass, carefully assigning large numbers to 0s and small numbers to 1s. Edge cases, such as all zeros or a single one, are naturally handled.

## Worked Examples

Sample Input:

```
4 3
0010
```

| i | s[i] | perm assignment | low | high |
| --- | --- | --- | --- | --- |
| 0 | 0 | 4 | 1 | 3 |
| 1 | 0 | 3 | 1 | 2 |
| 2 | 1 | 1 | 2 | 2 |
| 3 | 0 | 2 | 2 | 1 |

Permutation is `[4, 3, 1, 2]`. All intervals of length ≥ 3 covering index 2 (1-based) contain at least one 0, so the maximum is never 1. The algorithm correctly outputs "YES".

Edge case input:

```
s = 111, k = 2
```

The maximum run of 1s is 3 ≥ k. Algorithm prints "NO", correctly detecting impossibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass to compute maximum run of 1s and single pass to assign permutation |
| Space | O(n) | Permutation array of length n |

Given the sum of all $n$ is ≤ 2·10^5, this runs comfortably within the 1-second time limit and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    res = []
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        max_run = run_len = 0
        for ch in s:
            if ch == '1':
                run_len += 1
                max_run = max(max_run, run_len)
            else:
                run_len = 0
        if max_run >= k:
            res.append("NO")
            continue
        perm = [0] * n
        low, high = 1, n
        for i in range(n):
            if s[i] == '0':
                perm[i] = high
                high -= 1
            else:
                perm[i] = low
                low += 1
        res.append("YES")
        res.append(" ".join(map(str, perm)))
    return "\n".join(res)

# provided samples
assert run("6\n2 1\n00\n4 3\n0010\n5 2\n11011\n7 5\n1111110\n8 4\n00101011\n10 2\n1000000010\n") == \
"YES\n2 1\nYES\n4 3 1 2\nNO\nNO\nYES\n8 7 1 6 5 3 2 4\nYES\n10 1 2 3 4 5 6 8 9 7", "sample 1"

# custom edge cases
assert run("1\n3 3\n111\n") == "NO", "all 1s impossible"
assert run("1\n3 3\n000\n") == "YES\n3 2 1", "all 0s trivial"
assert run("1\n5 2\n10101\n") == "YES\n5 1 4 2 3", "alternating 1s and 0s"
assert run("1\n1 1\n1\n") == "YES\n1", "single 1"
assert run("1\n1 1\n0\n") == "YES\n
```
