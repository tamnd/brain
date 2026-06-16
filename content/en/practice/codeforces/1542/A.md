---
title: "CF 1542A - Odd Set"
description: "We are given a collection of numbers with even size, specifically 2n integers per test case. The task is to decide whether it is possible to partition these numbers into n disjoint pairs such that every pair consists of two numbers whose sum is odd."
date: "2026-06-16T15:14:50+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1542
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 729 (Div. 2)"
rating: 800
weight: 1542
solve_time_s: 309
verified: true
draft: false
---

[CF 1542A - Odd Set](https://codeforces.com/problemset/problem/1542/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 5m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of numbers with even size, specifically 2n integers per test case. The task is to decide whether it is possible to partition these numbers into n disjoint pairs such that every pair consists of two numbers whose sum is odd.

A sum is odd exactly when one number in the pair is even and the other is odd. So every valid pairing must match an even number with an odd number. No pair can contain two evens or two odds.

From the constraints, n is at most 100 and values are small, so each test case has at most 200 numbers. This immediately tells us that any approach up to O(n²) per test case is easily fast enough. We are not forced into complex optimizations, but we should still avoid unnecessary simulation of pairings.

The key structure of the problem is not about arrangement, but about counting parity. The only thing that matters is how many even and odd numbers exist.

A naive mistake here is to try to actually construct pairs greedily without checking feasibility globally. For example, pairing the first odd with the first even might fail later even though a different pairing order would work. Another mistake is to assume that having at least one odd and one even is enough. That fails when counts are imbalanced.

A concrete failing case for naive thinking is:

Input:

```
n = 2
array = [1, 3, 2, 4]
```

There are two odds and two evens. This works. But if we slightly change it:

```
n = 2
array = [1, 3, 5, 2]
```

Now we have 3 odds and 1 even. A greedy attempt might still pair (1,2), but then odds remain unmatched, so it fails. The correct answer depends only on counts.

## Approaches

A brute-force approach would attempt to enumerate all pairings of 2n elements. The number of ways to partition 2n elements into pairs is (2n)! / (2^n n!), which grows extremely fast even for n = 10. Each partition would need validation of all pairs for parity, making this completely infeasible.

The key observation is that each valid pair must contain exactly one even and one odd number. That means every even contributes exactly one pairing with an odd, and vice versa. Therefore, the number of evens must equal the number of odds. Since total elements are 2n, this condition is equivalent to having exactly n evens and n odds.

This reduces the problem from combinatorial pairing to a simple frequency check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pair Enumeration | O((2n)! ) | O(2n) | Too slow |
| Count parity | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We solve each test case independently by analyzing parity counts.

1. Read n and the list of 2n integers.
2. Count how many numbers are even and how many are odd.

The parity of a number is determined by checking a % 2.
3. Check whether the number of even elements equals the number of odd elements.

This condition is necessary because every valid pair consumes exactly one even and one odd.
4. If they are equal, print "Yes". Otherwise, print "No".

### Why it works

Each valid pair must contain one even and one odd number, so every pairing consumes exactly one element from each parity class. If the counts differ, at least one element will be left without a valid partner of opposite parity. Conversely, if counts are equal, we can always pair each even with a distinct odd arbitrarily, since there is no additional constraint on values beyond parity. This establishes both necessity and sufficiency of equal parity counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    
    even = 0
    odd = 0
    
    for x in arr:
        if x % 2 == 0:
            even += 1
        else:
            odd += 1
    
    print("Yes" if even == odd else "No")
```

The solution iterates through each test case independently. The key implementation detail is that we never attempt to construct pairs explicitly. We only track parity counts, which avoids unnecessary complexity and eliminates ordering concerns.

The comparison `even == odd` is sufficient because total size is fixed at 2n, so equality automatically implies both are exactly n.

## Worked Examples

### Sample 1

Input:

```
2
2
2 3 4 5
3
2 3 4 5 5 5
```

For the first test case:

| Step | Array | Even Count | Odd Count | Decision |
| --- | --- | --- | --- | --- |
| Init | [2,3,4,5] | 0 | 0 | - |
| Process 2 | [2,3,4,5] | 1 | 0 | - |
| Process 3 | [2,3,4,5] | 1 | 1 | - |
| Process 4 | [2,3,4,5] | 2 | 1 | - |
| Process 5 | [2,3,4,5] | 2 | 2 | Yes |

This confirms that pairing is possible because parity counts match.

For the second test case:

| Step | Array | Even Count | Odd Count | Decision |
| --- | --- | --- | --- | --- |
| Init | [2,3,4,5,5,5] | 0 | 0 | - |
| Process 2 | ... | 1 | 0 | - |
| Process 3 | ... | 1 | 1 | - |
| Process 4 | ... | 2 | 1 | - |
| Process 5 | ... | 2 | 4 | No |

The imbalance in parity makes it impossible to match every element.

### Sample 2

Input:

```
1
1
2 3
```

| Step | Array | Even Count | Odd Count | Decision |
| --- | --- | --- | --- | --- |
| Process | [2,3] | 1 | 1 | Yes |

This shows the minimal valid configuration, where exactly one even and one odd form a valid pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan each element once to count parity |
| Space | O(1) | Only two counters are maintained |

The input size is small, so linear scanning is easily within limits even for the maximum number of test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        
        even = sum(1 for x in arr if x % 2 == 0)
        odd = 2 * n - even
        
        output.append("Yes" if even == odd else "No")
    
    return "\n".join(output)

# provided samples
assert run("""5
2
2 3 4 5
3
2 3 4 5 5 5
1
2 4
1
2 3
4
1 5 3 2 6 7 3 4""") == """Yes
No
No
Yes
No"""

# custom cases
assert run("""3
1
1 2
2
1 3 5 7
2
2 4 6 8""") == """Yes
No
No"""

assert run("""1
2
1 2 3 4""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 / 1 3 5 7 / 2 4 6 8 | Yes / No / No | mixed parity, all odd, all even |
| 1 2 3 4 | Yes | balanced parity case |

## Edge Cases

One important edge case is when all numbers have the same parity.

For input:

```
n = 2
array = [2, 4, 6, 8]
```

The algorithm counts even = 4, odd = 0. Since they are not equal, it outputs "No". This matches the reasoning because no odd element exists to form any valid pair.

Another case is perfect balance:

```
n = 3
array = [1, 2, 3, 4, 5, 6]
```

Here even = 3 and odd = 3. The algorithm prints "Yes", and a valid pairing exists such as (1,2), (3,4), (5,6). This confirms sufficiency of the parity condition.
