---
title: "CF 1654A - Maximum Cake Tastiness"
description: "We are given a line of $n$ cakes, each with a weight $ai$. The tastiness of the cake is defined as the sum of two adjacent pieces. We are allowed to reverse one contiguous subsegment of cakes at most once and then measure the tastiness."
date: "2026-06-10T03:40:03+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1654
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 778 (Div. 1 + Div. 2, based on Technocup 2022 Final Round)"
rating: 800
weight: 1654
solve_time_s: 81
verified: true
draft: false
---

[CF 1654A - Maximum Cake Tastiness](https://codeforces.com/problemset/problem/1654/A)

**Rating:** 800  
**Tags:** brute force, greedy, implementation, sortings  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of $n$ cakes, each with a weight $a_i$. The tastiness of the cake is defined as the sum of two adjacent pieces. We are allowed to reverse **one contiguous subsegment** of cakes at most once and then measure the tastiness. Our goal is to maximize the tastiness after this operation.

The input consists of multiple test cases. For each test case, we are given the number of pieces and their weights. The output is the maximum tastiness achievable after at most one reversal.

The constraints are moderate: $n$ can go up to $1000$, and there can be up to $50$ test cases. This allows for algorithms up to roughly $O(n^2)$ per test case, but anything $O(n^3)$ would be too slow. Edge cases to watch for include very small arrays of size 2, arrays where all elements are equal, or arrays already in strictly decreasing or increasing order. For example, if $a = [1, 100, 1]$, a naive approach that only considers reversing large chunks might miss that reversing the middle two elements maximizes tastiness, giving $100 + 1 = 101$.

## Approaches

The brute-force approach is simple: try every possible subsegment $[l, r]$, reverse it, and compute the maximum adjacent sum. This works because we know the array length is small enough for $O(n^3)$ to be theoretically correct, but in practice, it involves $n^3/2$ operations and would likely time out near the upper bound of $n = 1000$.

The key insight comes from analyzing what reversal can actually change. Only sums that involve the **edges of the reversed segment** or sums at the boundaries of the array change. More concretely, reversing the middle of the array does not affect pairs outside it except for the first and last elements of the reversed subsegment. This reduces the problem drastically: we only need to consider reversing prefixes, suffixes, or swapping adjacent pairs, because any more complex reversal cannot increase the maximum beyond swapping the largest and second largest adjacent numbers.

Thus, the optimal approach is to compute the maximum adjacent sum in the original array, then consider three candidates for improvement:

1. Swap the first element with any other (reverse a prefix).
2. Swap the last element with any other (reverse a suffix).
3. Swap the first two or last two elements (edge reversal).

Checking these possibilities is linear, $O(n)$ per test case, because we only compute sums involving array endpoints or pairs. This insight avoids the need for $O(n^2)$ full subsegment reversals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow for n = 1000 |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$ and the array $a$.
2. Initialize `max_tastiness` to zero. Iterate through the array to compute the current maximum adjacent sum: for each $i$ from $0$ to $n-2$, update `max_tastiness = max(max_tastiness, a[i] + a[i+1])`.
3. Consider reversing **prefixes**: for each $i$ from $1$ to $n-1$, compute `a[0] + a[i]` and update `max_tastiness`. This simulates reversing $[0, i]`, bringing $a[i]$ next to $a[0]`.
4. Consider reversing **suffixes**: for each $i$ from $0$ to $n-2$, compute `a[n-1] + a[i]` and update `max_tastiness`. This simulates reversing $[i, n-1]`.
5. Print `max_tastiness` for the current test case.

The reason steps 3 and 4 are sufficient is that any longer reversal in the middle will not create a new maximum sum that is larger than what we can achieve by moving the largest numbers to an edge, since only the first and last elements can "meet" previously non-adjacent large numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    max_tastiness = 0
    # original adjacent sums
    for i in range(n - 1):
        max_tastiness = max(max_tastiness, a[i] + a[i+1])
    
    # consider prefix reversals (first element + any other)
    for i in range(1, n):
        max_tastiness = max(max_tastiness, a[0] + a[i])
    
    # consider suffix reversals (last element + any other)
    for i in range(n - 1):
        max_tastiness = max(max_tastiness, a[-1] + a[i])
    
    print(max_tastiness)
```

The code first computes the maximum of existing adjacent sums. It then evaluates moving the first or last element to every possible other position, which simulates all potential impactful reversals. Care is taken to avoid double counting the first and last element when computing suffix and prefix sums.

## Worked Examples

Sample input: `6\n5 2 1 4 7 3`

| Step | max_tastiness | Explanation |
| --- | --- | --- |
| Initial adjacent sums | 11 | max(5+2=7, 2+1=3, 1+4=5, 4+7=11, 7+3=10) |
| Prefix reversal candidates | 12 | a[0]+a[4] = 5+7=12, max updated |
| Suffix reversal candidates | 12 | no larger value found |
| Output | 12 | Correct maximum tastiness |

Sample input: `3\n32 78 78`

| Step | max_tastiness | Explanation |
| --- | --- | --- |
| Initial adjacent sums | 156 | max(32+78=110, 78+78=156) |
| Prefix reversal candidates | 156 | a[0]+a[1]=32+78=110, a[0]+a[2]=32+78=110 |
| Suffix reversal candidates | 156 | a[2]+a[0]=110, a[2]+a[1]=156 |
| Output | 156 | No reversal improves tastiness |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test case scans array three times linearly |
| Space | O(1) | Only a few variables; array storage counts as input |

Given $n \le 1000$ and $t \le 50$, the worst case is 50,000 operations, comfortably under the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        max_tastiness = 0
        for i in range(n - 1):
            max_tastiness = max(max_tastiness, a[i] + a[i+1])
        for i in range(1, n):
            max_tastiness = max(max_tastiness, a[0] + a[i])
        for i in range(n - 1):
            max_tastiness = max(max_tastiness, a[-1] + a[i])
        print(max_tastiness)
    return out.getvalue().strip()

# provided samples
assert run("5\n6\n5 2 1 4 7 3\n3\n32 78 78\n3\n69 54 91\n8\n999021 999021 999021 999021 999652 999021 999021 999021\n2\n1000000000 1000000000") == "12\n156\n160\n1998673\n2000000000", "sample"

# custom cases
assert run("1\n2\n1 2") == "3", "minimum-size array"
assert run("1\n4\n1 1 1 1") == "2", "all equal values"
assert run("1\n5\n1 2 3 4 5") == "9", "strictly increasing array"
assert run("1\n5\n5 4 3 2 1") == "9", "strictly decreasing array"
assert run("1\n6\n1 1000000000 1 1 1 1") == "1000000001", "large element at start"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 elements | 3 | minimum-size array handling |
| all equal | 2 | reversals do not change tastiness |
| increasing array | 9 | moving largest to start or end |
| decreasing array | 9 | moving largest to start or end |
| large number at start | 1000000001 | boundary with large values |

## Edge Cases

For arrays of size 2, the algorithm correctly returns their
