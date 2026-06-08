---
title: "CF 1878A - How Much Does Daytona Cost?"
description: "The problem asks whether, given an array of integers and a target integer $k$, there exists at least one contiguous subarray in which $k$ is the element that appears more frequently than any other element."
date: "2026-06-08T22:50:36+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1878
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 900 (Div. 3)"
rating: 800
weight: 1878
solve_time_s: 106
verified: true
draft: false
---

[CF 1878A - How Much Does Daytona Cost?](https://codeforces.com/problemset/problem/1878/A)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks whether, given an array of integers and a target integer $k$, there exists at least one contiguous subarray in which $k$ is the element that appears more frequently than any other element. Each test case gives the size of the array $n$, the target $k$, and the array $a$ itself. The answer for each test case is "YES" if such a subsegment exists and "NO" otherwise.

The constraints are small: $n$ is at most 100, and $t$, the number of test cases, is up to 1000. Each element $a_i$ and $k$ is also at most 100. This means an $O(n^2)$ approach for a single test case, which would explore all subarrays, is acceptable in terms of computation since the worst case would involve $1000 \cdot 100^2 = 10^7$ operations, manageable under a 1-second time limit.

The subtle edge cases arise when $k$ occurs only once in the array or appears at the very end or beginning. For instance, if $a = [1, 2, 3]$ and $k = 3$, the only subarray containing $k$ is $[3]$. In such a scenario, the algorithm must correctly identify that a single-element subarray qualifies, as $k$ is trivially the most common element there. Another case to consider is when $k$ appears multiple times but always separated by other elements such that no subarray allows $k$ to dominate in count; handling the minimal-length windows correctly ensures the solution is robust.

## Approaches

The brute-force solution would iterate over all possible subarrays of $a$ and count the frequency of each element in that subarray, then check if $k$ has the highest count. For a single array of length $n$, there are roughly $n(n+1)/2$ subarrays, and counting frequencies in each subarray could take up to $O(n)$ operations, resulting in $O(n^3)$ per test case. This approach is correct but inefficient even for $n = 100$, yielding $10^6$ operations per test case and $10^9$ in the worst-case across all test cases.

A key observation reduces the problem drastically: $k$ only needs to occur in a subarray alongside at most one other occurrence of $k$ nearby to dominate its neighbors. More concretely, if $k$ appears at least twice and the two occurrences are at positions $i$ and $j$ with $j - i \le 2$, then $k$ can be the most frequent in the subarray covering positions $i$ through $j$. A single occurrence is enough if the array has length one or if there is no other element around to compete with it.

The optimal solution leverages this by scanning the array and checking the distance between occurrences of $k$. If $k$ appears at least twice within a distance of two elements, we can immediately answer "YES". Otherwise, we check if $k$ occurs at least once in the array: if it occurs only once and the array length is one, the answer is "YES"; if the array is longer, a single isolated $k$ is enough, since even in a two-element subarray, it can be the most frequent if the other element differs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$, $k$, and the array $a$.
2. Count how many times $k$ appears in the array. If it appears zero times, print "NO" and move to the next test case.
3. If the array contains exactly one element, print "YES" if that element is $k$.
4. Otherwise, iterate through the array and check for every pair of indices $i$ and $j$ where $i < j$ and $j - i \le 2$. If both positions contain $k$, immediately print "YES".
5. If no such pair is found but $k$ exists in the array, print "YES" because a single-element subarray containing $k$ qualifies.
6. If none of these conditions are met, print "NO".

Why it works: The invariant here is that any subarray of length one containing $k$ is automatically valid. For longer subarrays, the distance check ensures that $k$ can dominate at least two adjacent elements, forming a valid subarray. The algorithm correctly identifies all minimal subarrays where $k$ could be the most frequent, avoiding unnecessary counting of all subarrays.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    count_k = a.count(k)
    
    if count_k == 0:
        print("NO")
        continue
    
    if n == 1:
        print("YES")
        continue
    
    found = False
    for i in range(n):
        if a[i] != k:
            continue
        for j in range(i, min(i + 3, n)):
            if a[j] == k and j - i <= 2:
                found = True
                break
        if found:
            break
    
    print("YES" if found else "NO")
```

This solution first counts occurrences of $k$. If $k$ is absent, the answer is "NO". Single-element arrays are trivial to handle. The nested loop checks pairs within a small window (length at most 3) to see if $k$ can dominate locally. The upper bound of the inner loop ensures we do not go out of array bounds.

## Worked Examples

**Sample Input 1:**

```
5 4
1 4 3 4 1
```

| i | j | a[i..j] | Condition check | Result |
| --- | --- | --- | --- | --- |
| 1 | 2 | [4,3] | k appears once, length 2, dominates | YES |

This shows a valid subarray [4,3] where 4 is the most frequent.

**Sample Input 2:**

```
4 1
2 3 4 4
```

| i | j | a[i..j] | Condition check | Result |
| --- | --- | --- | --- | --- |
| 0 | 0 | [2] | k=1 not present | NO |
| ... | ... | ... | none contains k | NO |

No subarray contains 1, so the algorithm correctly outputs "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n) | Each test case scans the array once and checks small windows of at most 3 elements. |
| Space | O(n) | Storing the array for each test case. |

Given $t \le 1000$ and $n \le 100$, at most $10^5$ operations occur, well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        count_k = a.count(k)
        if count_k == 0:
            print("NO")
            continue
        if n == 1:
            print("YES")
            continue
        found = False
        for i in range(n):
            if a[i] != k:
                continue
            for j in range(i, min(i + 3, n)):
                if a[j] == k and j - i <= 2:
                    found = True
                    break
            if found:
                break
        print("YES" if found else "NO")
    return output.getvalue().strip()

# provided samples
assert run("7\n5 4\n1 4 3 4 1\n4 1\n2 3 4 4\n5 6\n43 5 60 4 2\n2 5\n1 5\n4 1\n5 3 3 1\n1 3\n3\n5 3\n3 4 1 5 5\n") == \
"YES\nNO\nNO\nYES\nYES\nYES\nYES", "Sample tests"

# custom cases
assert run("2\n1 1\n1\n3 2\n1 2 2\n") == "YES\nYES", "single-element and duplicate k"
assert run("1\n5 5\n1 2 3 4 5\n") == "YES", "k at end"
assert run("1\n4 10\n1 2 3 4\n") == "NO", "k absent"
assert run("1\n3 2\n2 1 2\n") == "
```
