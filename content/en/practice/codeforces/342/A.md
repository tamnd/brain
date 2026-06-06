---
title: "CF 342A - Xenia and Divisors"
description: "We are given a sequence of positive integers, all between 1 and 7, and the length of the sequence is divisible by three."
date: "2026-06-06T17:34:32+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 342
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 199 (Div. 2)"
rating: 1200
weight: 342
solve_time_s: 96
verified: true
draft: false
---

[CF 342A - Xenia and Divisors](https://codeforces.com/problemset/problem/342/A)

**Rating:** 1200  
**Tags:** greedy, implementation  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of positive integers, all between 1 and 7, and the length of the sequence is divisible by three. Xenia wants to partition this sequence into groups of three numbers each such that within each group, the numbers increase strictly and each number divides the next. The output is either the list of these triplets or -1 if no such partition exists.

The constraints tell us that n can be as large as 99999, which rules out any algorithm that tries all possible triplets in the sequence, because that would involve choosing combinations of n elements three at a time and checking divisibility, leading to roughly n³ operations. Since n³ is on the order of 10¹⁵ for n near 10⁵, this is completely infeasible. We need a linear or at most O(n) approach.

The non-obvious edge cases arise because not all numbers between 1 and 7 can coexist in a valid triplet. For instance, three 1s cannot form a triplet because 1,1,1 is not strictly increasing. Similarly, a number like 5 cannot appear in any triplet because there is no sequence of the form a divides b divides c that ends with 5 using only numbers 1-7. Another tricky case is having a mismatch in counts: if we have more 2s than 1s, we cannot form a triplet 1,2,x for all 2s.

A concrete failing example is the input `6\n1 1 1 2 2 2`. The 1s and 2s cannot be combined to satisfy the strictly increasing and divisibility conditions, so the correct output is -1.

## Approaches

The brute-force approach would be to generate all combinations of three elements and check whether the conditions a<b<c and a divides b divides c hold. For each valid triplet, we would mark elements as used and continue until all elements are grouped. This approach is correct in principle, but it involves choosing combinations of n elements three at a time, which is O(n³), far too slow for n up to 10⁵.

The key observation is that the numbers are restricted to the range 1-7. That makes the total number of distinct numbers very small. We can count the occurrences of each number, then try to assemble triplets only from valid sequences. By listing all possible triplets that satisfy the constraints (1,2,4), (1,2,6), (1,3,6), we see that only these combinations can appear. If the count of any number does not match the required counts across these triplets, a solution is impossible.

Thus, the optimal approach is a greedy counting method: count the occurrences of 1 through 7, check if the counts allow forming the required triplets, then output the triplets using the counts. This reduces the complexity to O(n) since we only need to traverse the list once to count, then output the triplets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Counting + Greedy | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many times each integer from 1 to 7 appears in the sequence. We will store this in an array `cnt` where `cnt[i]` represents the count of number i.
2. Check for impossible numbers. If any number appears that is not part of a valid triplet, like 5 or 7, we can immediately return -1.
3. Validate the counts against feasible triplets. The only valid triplets are (1,2,4), (1,2,6), and (1,3,6). The sum of counts of 1 must equal n/3, and each 1 must be used exactly once. Similarly, counts of 2, 3, 4, and 6 must satisfy the relationships implied by the triplets:

- Each 2 is part of either (1,2,4) or (1,2,6).
- Each 3 must be paired with a 6 in (1,3,6).
- Counts of 4 and 6 must be sufficient to cover all triplets.
- 5 and 7 are invalid.
4. Construct triplets using a greedy approach. First form as many (1,2,4) triplets as possible using `min(cnt[1], cnt[2], cnt[4])`, then form (1,2,6) triplets with remaining 1s, 2s, and 6s, then (1,3,6) triplets with remaining 1s, 3s, and 6s.
5. If after forming triplets any count remains non-zero, return -1. Otherwise, output all the triplets.

The invariant is that at every step, we only form a valid triplet with available numbers, ensuring each number is used exactly once. Because the counts fully determine whether a partition exists, this guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

cnt = [0] * 8
for x in a:
    cnt[x] += 1

# impossible numbers
if cnt[5] > 0 or cnt[7] > 0:
    print(-1)
    sys.exit()

triplets = []

# form (1,2,4) as much as possible
k = min(cnt[1], cnt[2], cnt[4])
for _ in range(k):
    triplets.append((1,2,4))
    cnt[1] -= 1
    cnt[2] -= 1
    cnt[4] -= 1

# form (1,2,6)
k = min(cnt[1], cnt[2], cnt[6])
for _ in range(k):
    triplets.append((1,2,6))
    cnt[1] -= 1
    cnt[2] -= 1
    cnt[6] -= 1

# form (1,3,6)
k = min(cnt[1], cnt[3], cnt[6])
for _ in range(k):
    triplets.append((1,3,6))
    cnt[1] -= 1
    cnt[3] -= 1
    cnt[6] -= 1

# if any leftover numbers, impossible
if sum(cnt) != 0:
    print(-1)
else:
    for t in triplets:
        print(*t)
```

The first part counts occurrences and immediately rejects any invalid numbers. The greedy steps ensure that we form the triplets in a valid sequence without leaving leftovers. Checking the sum of remaining counts confirms that no number is unassigned.

## Worked Examples

Sample Input 1:

```
6
1 1 1 2 2 2
```

| Step | cnt[1] | cnt[2] | cnt[3] | cnt[4] | cnt[6] | Triplets |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 3 | 3 | 0 | 0 | 0 | [] |
| Form (1,2,4) | 3 | 3 | 0 | 0 | 0 | 0 triplets, cannot form |
| Form (1,2,6) | 3 | 3 | 0 | 0 | 0 | 0 triplets, cannot form |
| Form (1,3,6) | 3 | 3 | 0 | 0 | 0 | 0 triplets, cannot form |
| Remaining sum | 6 | => -1 |  |  |  |  |

This demonstrates that when required numbers for valid triplets are missing, the algorithm correctly detects impossibility.

Custom Input 2:

```
6
1 1 2 2 4 6
```

| Step | cnt[1] | cnt[2] | cnt[4] | cnt[6] | Triplets |
| --- | --- | --- | --- | --- | --- |
| Initial | 2 | 2 | 1 | 1 | [] |
| Form (1,2,4) | 1 | 1 | 0 | 1 | [(1,2,4)] |
| Form (1,2,6) | 0 | 0 | 0 | 1 | [(1,2,4),(1,2,6)] |
| Remaining sum | 0 | valid |  |  |  |

The table shows that the algorithm forms triplets greedily without leaving leftovers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting each element once, then forming triplets based on counts takes O(n) total |
| Space | O(1) | Count array is size 8 and triplets array stores n/3 triplets |

With n ≤ 99999, this linear solution comfortably fits within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        exec(open("solution.py").read())
    return out.getvalue().strip()

# Provided sample
assert run("6\n1 1 1 2 2 2\n") == "-1", "sample 1"

# Custom cases
assert run("6\n1
```
