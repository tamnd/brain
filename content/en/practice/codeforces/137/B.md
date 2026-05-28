---
title: "CF 137B - Permutation"
description: "We are given an array of $n$ integers, each between 1 and 5000, and we are asked to transform this array into a permutation of the numbers from 1 to $n$. A permutation is a sequence where each integer from 1 to $n$ appears exactly once."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 137
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 98 (Div. 2)"
rating: 1000
weight: 137
solve_time_s: 73
verified: true
draft: false
---

[CF 137B - Permutation](https://codeforces.com/problemset/problem/137/B)

**Rating:** 1000  
**Tags:** greedy  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of $n$ integers, each between 1 and 5000, and we are asked to transform this array into a permutation of the numbers from 1 to $n$. A permutation is a sequence where each integer from 1 to $n$ appears exactly once. The operation allowed is changing a single element to any other integer. The goal is to minimize the number of such changes.

The input gives the sequence length $n$ and the array itself. The output is a single integer representing the minimum number of replacements needed.

The constraints are modest: $n$ can be up to 5000. Since a naive $O(n^2)$ approach could involve scanning the array repeatedly, we should aim for a solution that is $O(n \log n)$ or $O(n)$. Memory usage is also limited, but storing a frequency array of size 5000 is acceptable.

Edge cases include sequences that already form a valid permutation, sequences where all elements are the same, or sequences where many numbers are out of the 1-to-$n$ range. For instance, if $n = 3$ and the array is $[5, 5, 5]$, the correct output is 3 because all three numbers must be changed to 1, 2, and 3. A careless approach might only count duplicates without checking bounds, producing the wrong answer.

## Approaches

The brute-force approach is to iterate through all numbers from 1 to $n$ and check if each is present in the array. If it is missing, we can scan the array for an element to replace. This works in principle, but scanning repeatedly makes the complexity $O(n^2)$ in the worst case, which is too slow for $n = 5000$.

The optimal approach leverages counting. We observe that for a valid permutation, each number 1 through $n$ must appear exactly once. Any number outside this range or any duplicate inside the range must be changed. Therefore, we can compute the frequency of each number and iterate over the numbers from 1 to $n$. Each missing number corresponds to one required change. We also count the "extra" numbers that are either duplicates or out of bounds. The minimum number of changes is the total count of missing numbers, which will always be matched by enough extra numbers to replace.

The insight is that the problem reduces to counting missing numbers and excess numbers. Sorting the array or attempting to do complex swaps is unnecessary because any excess element can be repurposed to fill a missing slot.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a frequency array `freq` of size $n+1$ to count occurrences of numbers 1 to $n$. Ignore numbers outside this range for now.
2. Iterate over the input array. For each element $a_i$, if it is within 1 to $n$, increment `freq[a_i]`. Otherwise, count it as an "excess" element, which will eventually need replacement.
3. Initialize a counter `changes` to zero. Iterate through numbers 1 to $n$. If `freq[i]` is zero, it means the number $i$ is missing. Increment `changes` by one. For numbers with frequency greater than one, the extra copies will contribute to the pool of excess elements.
4. Return `changes`. This value is exactly the number of replacements needed because each missing number can be filled using an extra element from duplicates or numbers out of range.

The invariant is that after counting frequencies, the sum of missing numbers equals the minimum replacements needed. There is no ambiguity in which elements to change because any excess number can be changed to a missing number without affecting other missing numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

freq = [0] * (n + 1)
excess = 0

for x in a:
    if 1 <= x <= n:
        freq[x] += 1
    else:
        excess += 1

changes = 0
for i in range(1, n + 1):
    if freq[i] == 0:
        changes += 1

print(changes)
```

The code first counts how many times each number in the valid permutation range appears. Any number outside 1 to $n$ is automatically considered excess. Then, for each number from 1 to $n$, we check whether it is missing. Each missing number corresponds directly to one required change. We do not need to track exactly which excess number gets changed because the question only asks for the count.

## Worked Examples

### Sample Input 1

```
3
3 1 2
```

| Step | freq | excess | changes |
| --- | --- | --- | --- |
| Initial | [0,0,0,0] | 0 | 0 |
| Process 3 | [0,0,0,1] | 0 | 0 |
| Process 1 | [0,1,0,1] | 0 | 0 |
| Process 2 | [0,1,1,1] | 0 | 0 |
| Check missing | no zeros in freq[1..3] | 0 | 0 |

Output: 0. The array is already a permutation.

### Sample Input 2

```
4
4 4 1 5
```

| Step | freq | excess | changes |
| --- | --- | --- | --- |
| Initial | [0,0,0,0,0] | 0 | 0 |
| Process 4 | [0,0,0,0,1] | 0 | 0 |
| Process 4 | [0,0,0,0,2] | 0 | 0 |
| Process 1 | [0,1,0,0,2] | 0 | 0 |
| Process 5 | out of range | 1 | 0 |
| Check missing | freq[2]=0, freq[3]=0 | changes = 2 | 2 |

Output: 2. We need to replace two excess elements (one 4 and the 5) with 2 and 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to count frequencies, single pass to count missing numbers. |
| Space | O(n) | Frequency array of size n+1. |

This fits comfortably within the 2-second limit for $n \le 5000$ and memory limit of 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    freq = [0] * (n + 1)
    excess = 0
    for x in a:
        if 1 <= x <= n:
            freq[x] += 1
        else:
            excess += 1
    changes = 0
    for i in range(1, n + 1):
        if freq[i] == 0:
            changes += 1
    return str(changes)

# Provided samples
assert run("3\n3 1 2\n") == "0", "sample 1"
assert run("4\n4 4 1 5\n") == "2", "sample 2"

# Custom cases
assert run("1\n1\n") == "0", "single element correct"
assert run("3\n5 5 5\n") == "3", "all out of range"
assert run("5\n1 2 2 4 5\n") == "1", "one missing in range"
assert run("5\n1 1 1 1 1\n") == "4", "all duplicates"
assert run("5\n2 3 4 6 7\n") == "2", "mix of duplicates and out-of-range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | 0 | Minimum input, already correct |
| 3\n5 5 5 | 3 | All numbers out of range, all must change |
| 5\n1 2 2 4 5 | 1 | One number missing, some duplicates |
| 5\n1 1 1 1 1 | 4 | All duplicates, need multiple changes |
| 5\n2 3 4 6 7 | 2 | Missing 1 and 5, extra out-of-range numbers |

## Edge Cases

If the sequence has all numbers equal to a value outside the permutation range, such as `[6, 6, 6]` for `n=3`, the algorithm counts all three as excess and identifies missing numbers 1, 2, 3. The `changes` counter becomes 3, matching the number of missing numbers.

If the sequence has duplicates within the range, like `[1, 1, 2, 4]` for `n=4`, the algorithm counts frequencies `[0,2,1,0,1]` and identifies missing number 3
