---
title: "CF 1822B - Karina and Array"
description: "We are given an array of integers and we are allowed to delete any subset of elements while preserving the relative order of what remains."
date: "2026-06-09T07:47:59+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1822
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 867 (Div. 3)"
rating: 800
weight: 1822
solve_time_s: 68
verified: true
draft: false
---

[CF 1822B - Karina and Array](https://codeforces.com/problemset/problem/1822/B)

**Rating:** 800  
**Tags:** greedy, math, sortings  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and we are allowed to delete any subset of elements while preserving the relative order of what remains. After deletions, we must keep at least two elements, and we evaluate the resulting array by looking at all adjacent pairs and taking the maximum product among them. The goal is to choose which elements to keep so that this maximum adjacent product is as large as possible.

The key detail is that deletions allow us to “connect” any two surviving elements that were not originally adjacent. So the problem is not about original neighbors, but about choosing any pair of indices $i < j$ that become consecutive after removing everything in between, and maximizing $a_i \cdot a_j$.

The constraints allow up to $2 \cdot 10^5$ elements total across test cases, which immediately rules out any quadratic exploration of all pairs or all subsequences. A solution that tries all pairs or simulates deletions explicitly would be too slow because a single test case could already require around $10^{10}$ operations in the worst case.

A subtle failure mode appears when thinking only about adjacent elements in the original array. For example, in an array like $[1, 100, 2]$, the best adjacent product is $100$, but after deletion we can choose $[1, 2]$ to get $2$, which is worse, or $[100]$ is invalid. However, more interesting cases involve skipping elements to connect distant large values that were not originally adjacent.

Another edge case is negative numbers. A naive approach that only considers large absolute values would fail because products depend on sign, and the maximum product may come from two negatives.

## Approaches

The brute-force idea is straightforward: consider every subset of size at least two, compute its best adjacent product, and track the maximum. Even if we restrict ourselves to checking pairs after deletions, we still effectively consider all pairs of indices $(i, j)$ with $i < j$, since any such pair can be made adjacent by deleting the elements in between. For each pair, we compute $a_i \cdot a_j$ and take the maximum.

This immediately becomes $O(n^2)$ per test case, which is too large when $n$ reaches $2 \cdot 10^5$.

The key observation is that deletions allow us to ignore structure entirely. Any two chosen elements can become adjacent, so the final answer is simply the maximum product over all pairs $i < j$. That reduces the problem to selecting the best pair, not arranging a sequence.

Once this is recognized, the task becomes finding the maximum product of two numbers in an array. The only subtlety is sign: the maximum product can come either from the two largest positive numbers or from the two smallest (most negative) numbers.

Thus, we only need to track four candidates: the two largest values and the two smallest values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Scan the array once while maintaining the two largest values and the two smallest values seen so far.

We maintain these extremes because any optimal pair must come from one of these boundary cases.
2. For each element $x$, update the maximum pair $(max1, max2)$ so that $max1 \ge max2$, and similarly update the minimum pair $(min1, min2)$ so that $min1 \le min2$.

This ensures we always retain the best candidates for positive and negative contributions.
3. After processing all elements, compute two candidate answers: $max1 \cdot max2$ and $min1 \cdot min2$.
4. Return the maximum of these two values.

The reason we split into these two cases is that multiplication behaves differently under sign changes. Large positive values maximize product directly, while large-magnitude negative values can produce a large positive product when multiplied together.

### Why it works

Any optimal solution depends only on two chosen indices $i < j$. Since any pair can be made adjacent after deletions, the problem reduces to selecting two elements maximizing their product. The best such pair must come from extremal values: either the two largest numbers or the two smallest numbers. Any interior value cannot outperform these combinations because replacing a chosen element with a more extreme value always improves or preserves the product in absolute contribution under the correct pairing case.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # initialize extremes
        max1 = max2 = -10**30
        min1 = min2 = 10**30
        
        for x in a:
            # update max pair
            if x > max1:
                max2 = max1
                max1 = x
            elif x > max2:
                max2 = x
            
            # update min pair
            if x < min1:
                min2 = min1
                min1 = x
            elif x < min2:
                min2 = x
        
        ans = max(max1 * max2, min1 * min2)
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation keeps track of the two largest and two smallest values in a single pass. The initialization uses very large sentinel values to ensure correct updates even when all numbers are negative or all are positive.

The final comparison between the two candidate products is essential because it captures both positive-pair dominance and negative-pair dominance.

## Worked Examples

### Example 1

Input: $[5, 0, 2, 1]$

| Step | max1 | max2 | min1 | min2 | action |
| --- | --- | --- | --- | --- | --- |
| 5 | 5 | -inf | 5 | inf | initialize |
| 0 | 5 | 0 | 0 | 5 | update both sides |
| 2 | 5 | 2 | 0 | 5 | update max side |
| 1 | 5 | 2 | 0 | 1 | update max side |

Candidates are $5 \cdot 2 = 10$ and $0 \cdot 1 = 0$, so answer is $10$.

This trace shows that the best result comes from the two largest positive numbers, not involving zeros or smaller values.

### Example 2

Input: $[-8, 4, 3, 7, 1, -9]$

| Step | max1 | max2 | min1 | min2 | action |
| --- | --- | --- | --- | --- | --- |
| -8 | -8 | -inf | -8 | inf | init |
| 4 | 4 | -8 | -8 | -8 | update both |
| 3 | 4 | 3 | -8 | -8 | update max |
| 7 | 7 | 4 | -8 | -8 | update max |
| 1 | 7 | 4 | -8 | -8 | no change |
| -9 | 7 | 4 | -9 | -8 | update min |

Candidates are $7 \cdot 4 = 28$ and $(-9) \cdot (-8) = 72$, so answer is $72$.

This confirms the importance of considering negative pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | single pass per test case |
| Space | $O(1)$ | only four variables stored |

The algorithm processes each element once, which fits comfortably within the total constraint of $2 \cdot 10^5$ elements. Constant memory ensures no overhead beyond a few integer variables.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []
    
    def input():
        return sys.stdin.readline()
    
    t = int(sys.stdin.readline())
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        
        max1 = max2 = -10**30
        min1 = min2 = 10**30
        
        for x in a:
            if x > max1:
                max2 = max1
                max1 = x
            elif x > max2:
                max2 = x
            
            if x < min1:
                min2 = min1
                min1 = x
            elif x < min2:
                min2 = x
        
        out.append(str(max(max1 * max2, min1 * min2)))
    
    return "\n".join(out)

# provided samples
assert run("""7
4
5 0 2 1
3
-1 1 0
5
2 0 -1 -4 0
6
-8 4 3 7 1 -9
6
0 3 -2 5 -4 -4
2
1000000000 910000000
7
-1 -7 -2 -5 -4 -6 -3
""") == """10
0
4
72
16
910000000000000000
42"""

# custom cases
assert run("""1
2
1 2
""") == "2", "simple positive pair"

assert run("""1
2
-5 -6
""") == "30", "two negatives"

assert run("""1
3
-10 1 2
""") == "2", "skip negative extreme"

assert run("""1
4
0 -1 -2 -3
""") == "6", "best negative pair"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 1 2 | 2 | basic positive case |
| -5 -6 | 30 | negative pair dominance |
| -10 1 2 | 2 | ignoring harmful extremes |
| 0 -1 -2 -3 | 6 | zero vs negative interaction |

## Edge Cases

A tricky situation occurs when the array contains both large positives and large-magnitude negatives. For example, $[-100, 1, 2, 3, 4]$. The algorithm tracks both extremes, so max pair becomes $4 \cdot 3 = 12$, while min pair is not competitive because there is only one large negative.

For $[-5, -6, 2]$, the tracked values end as max1 = 2, max2 = -5 and min1 = -6, min2 = -5. The algorithm evaluates $2 \cdot -5 = -10$ and $(-6) \cdot (-5) = 30$, correctly selecting the negative pair.

In cases with zeros like $[0, -1, -2]$, zeros are naturally included in max tracking but do not interfere with the min pair, ensuring that the correct answer comes from $(-1) \cdot (-2)$.
