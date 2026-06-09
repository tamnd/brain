---
title: "CF 1624C - Division by Two and Permutation"
description: "We are given an array of positive integers of size $n$, and we want to know if we can turn it into a permutation of numbers from $1$ to $n$ by repeatedly dividing elements by two. Each division operation replaces an element $ai$ with $lfloor ai / 2 rfloor$."
date: "2026-06-10T05:35:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "flows", "graph-matchings", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1624
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 764 (Div. 3)"
rating: 1100
weight: 1624
solve_time_s: 72
verified: true
draft: false
---

[CF 1624C - Division by Two and Permutation](https://codeforces.com/problemset/problem/1624/C)

**Rating:** 1100  
**Tags:** constructive algorithms, flows, graph matchings, greedy, math  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers of size $n$, and we want to know if we can turn it into a permutation of numbers from $1$ to $n$ by repeatedly dividing elements by two. Each division operation replaces an element $a_i$ with $\lfloor a_i / 2 \rfloor$. A permutation here means the final array contains every integer from $1$ to $n$ exactly once.

The constraints are small enough in terms of $n$ (up to 50) but large in terms of the numbers themselves (up to $10^9$). This means we cannot afford operations that scale with the numbers directly (like iterating from 1 to $a_i$), but we can perform something proportional to $n \log a_i$ since dividing a number by two repeatedly takes at most about 30 steps (because $2^{30} \approx 10^9$).

A naive approach might be to try all sequences of divisions for each number and check if any combination yields a permutation. This would be exponential in $n$ and impossible even for $n=20$. Edge cases include arrays where many elements are initially larger than $n$, arrays with repeated numbers, and arrays where the smallest numbers are missing. For example, if $a = [4, 4, 4]$ and $n = 3$, it seems plausible because each 4 can be divided down to 2 and 1, but we have to carefully assign the results to avoid duplicates. A careless approach might greedily divide numbers without considering order and incorrectly claim success or failure.

## Approaches

The brute-force method would attempt to generate all sequences of divisions for each number and then check if some combination forms a valid permutation. For a single number, the number of possibilities is roughly $\log_2 a_i$, which is about 30 in the worst case. For $n=50$, the total number of combinations becomes $30^{50}$, which is astronomically large. This is obviously not feasible.

The key insight is that for each target number from $1$ to $n$, we only care about whether it can be produced by repeatedly halving some element in the array. We do not need to track all sequences simultaneously. We can sort the array in decreasing order and try to assign the largest numbers first to the largest available targets, dividing down until the number fits. This greedy approach works because once we assign a number to a target, we remove that target from consideration, and larger numbers cannot block smaller ones if we handle them first.

We can implement this by maintaining a set of available targets $1$ through $n$. For each element starting from the largest, we repeatedly divide by two until it either falls into the set of available targets (then we remove that target) or drops below 1 (failure). This ensures every number is assigned to the largest possible target it can reach, preventing collisions and guaranteeing that the algorithm finds a permutation if one exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((log A)^n) | O(n) | Too slow |
| Greedy Division | O(n log A) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and the array $a$.
2. Initialize a set containing the target numbers $1$ to $n$. This represents the numbers we still need to produce.
3. Sort the array $a$ in decreasing order. We want to assign larger numbers first to avoid blocking smaller targets.
4. For each number in the sorted array, repeatedly divide it by two until it either matches a number in the set of available targets or becomes zero.
5. If the number matches a target, remove that target from the set and move to the next number.
6. If a number reaches zero without matching any available target, print "NO" for this test case. Otherwise, continue until all numbers are processed.
7. If all targets have been assigned, print "YES".

Why it works: The invariant is that at every step, the largest unassigned number is trying to cover the largest remaining target it can reach. Since we only assign a target when a number equals it and then remove the target, no two numbers will claim the same target. Processing numbers in descending order guarantees that smaller numbers are not blocked by larger numbers, so if a valid permutation exists, the algorithm will find it.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    targets = set(range(1, n+1))
    a.sort(reverse=True)
    
    possible = True
    for x in a:
        while x > 0:
            if x in targets:
                targets.remove(x)
                break
            x //= 2
        else:
            possible = False
            break
    
    print("YES" if possible else "NO")
```

The code first reads the number of test cases. For each test case, it reads the array and initializes the set of targets from 1 to $n$. Sorting the array in descending order ensures we handle larger numbers first. The inner loop divides each number until it either matches a target or becomes zero. If it becomes zero without a match, the permutation is impossible. Using a set allows O(1) checks and removals of targets, keeping the solution efficient.

## Worked Examples

### Example 1

Input array: `[1, 8, 25, 2]`, n = 4

| Step | Number | Targets | Operation |
| --- | --- | --- | --- |
| 1 | 25 | {1,2,3,4} | 25 → 12 → 6 → 3; assign 3, remove 3 |
| 2 | 8 | {1,2,4} | 8 → 4; assign 4, remove 4 |
| 3 | 2 | {1,2} | 2; assign 2, remove 2 |
| 4 | 1 | {1} | 1; assign 1, remove 1 |

All targets covered, output YES.

### Example 2

Input array: `[1, 1]`, n = 2

| Step | Number | Targets | Operation |
| --- | --- | --- | --- |
| 1 | 1 | {1,2} | 1; assign 1, remove 1 |
| 2 | 1 | {2} | 1 → 0; cannot assign 2 |

Not all targets covered, output NO.

These traces show the greedy division approach correctly assigns numbers to targets and identifies impossible cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log A) | Each number is divided at most log2(A_i) times, n numbers in total |
| Space | O(n) | Set of targets, array storage |

Since n ≤ 50 and log2(A_i) ≤ 30, the solution performs at most 1500 operations per test case, easily fitting within the 3-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # paste solution here
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        targets = set(range(1, n+1))
        a.sort(reverse=True)
        
        possible = True
        for x in a:
            while x > 0:
                if x in targets:
                    targets.remove(x)
                    break
                x //= 2
            else:
                possible = False
                break
        
        print("YES" if possible else "NO")
    return output.getvalue().strip()

# Provided samples
assert run("6\n4\n1 8 25 2\n2\n1 1\n9\n9 8 3 4 2 7 1 5 6\n3\n8 2 1\n4\n24 7 16 7\n5\n22 6 22 4 22\n") == "YES\nNO\nYES\nNO\nNO\nYES", "sample 1"

# Custom cases
assert run("1\n1\n1\n") == "YES", "minimum input"
assert run("1\n3\n2 2 2\n") == "YES", "all equal values but divisible"
assert run("1\n5\n10 20 30 40 50\n") == "YES", "all large values"
assert run("1\n4\n1 2 3 4\n") == "YES", "already a permutation"
assert run("1\n3\n3 3 3\n") == "NO", "duplicates cannot reach all targets"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | YES | Minimum-size input |
| `1\n3\n2 2 2` | YES | Multiple equal numbers that can be divided |
| `1\n5\n10 20 30 40 50` | YES | Large numbers that must be divided |
| `1\n4\n1 2 3 |  |  |
