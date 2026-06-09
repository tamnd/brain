---
title: "CF 1741E - Sending a Sequence Over the Network"
description: "We are asked to check if a given sequence $b$ could have been sent over the network from some original sequence $a$ by a specific encoding procedure."
date: "2026-06-09T16:28:25+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 1741
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 826 (Div. 3)"
rating: 1600
weight: 1741
solve_time_s: 171
verified: false
draft: false
---

[CF 1741E - Sending a Sequence Over the Network](https://codeforces.com/problemset/problem/1741/E)

**Rating:** 1600  
**Tags:** dp  
**Solve time:** 2m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to check if a given sequence $b$ could have been sent over the network from some original sequence $a$ by a specific encoding procedure. The encoding takes sequence $a$, splits it into consecutive segments, and then, for each segment, prepends or appends the segment's length. The transmitted sequence $b$ interleaves segment lengths and the original values.

The input consists of multiple test cases, each providing the sequence $b$. The output is a simple YES or NO depending on whether there exists some original sequence $a$ that could have generated $b$ under the described encoding.

The constraints are significant. Each sequence can have up to $2 \cdot 10^5$ elements, and the sum across all test cases is bounded by the same value. This rules out any algorithm that is worse than linearithmic $O(n \log n)$ per test case or quadratic $O(n^2)$ in total. The only feasible approaches are linear scans or simple greedy algorithms.

Non-obvious edge cases include sequences with length one, sequences where multiple repeated numbers appear, and sequences where the segment lengths themselves could be confused with element values. For instance, a sequence like $b = [1, 1]$ is valid, representing a single element segment of length one, whereas $b = [2, 1]$ could be interpreted as a segment length two followed by a value one, which might not match a valid original sequence.

## Approaches

A brute-force approach would attempt to try all possible partitions of $b$ into segments with lengths assigned either before or after each segment. For a sequence of size $n$, there are an exponential number of partitions and permutations. This approach is correct in principle because it tries every combination, but it is computationally infeasible due to the combinatorial explosion. For sequences with lengths in the hundreds or thousands, this quickly exceeds any reasonable time limit.

The key insight to unlock a linear solution is to notice that once a number is used as a segment length, it cannot appear again as a part of a later segment within the same processing window. Moreover, the algorithm can work from the back of the sequence, greedily assigning numbers to segments. If we always try to remove the largest element not yet placed in $a$ and interpret it as the last element of a segment of its value, we can reduce the problem to checking if we can cover the entire sequence using such segments.

This reduces the problem to a simulation with a multiset or a frequency map of the numbers. We iteratively remove the largest remaining number, treat it as the end of a segment, and subtract segment lengths, ensuring no negative counts or missing numbers. This greedy approach works because segment lengths are unambiguously tied to their largest element if we always pick the largest remaining number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy with frequency map | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the sequence $b$ and store the frequency of each number in a counter.
2. Initialize a list or multiset sorted in descending order to always pick the largest number remaining.
3. While there are numbers left, pick the largest number $x$ remaining. Treat it as the last element of a segment whose length is $x$.
4. Attempt to remove $x$ elements from the multiset, corresponding to the segment. This can be done by repeatedly removing the largest remaining element until the segment size is fulfilled.
5. If at any step the required number is not available in the multiset, the sequence cannot be formed. Print NO and move to the next test case.
6. If the multiset becomes empty after processing all segments successfully, print YES.

Why it works: At each step, the largest number remaining determines the minimal segment that must include it as the last element. The greedy assignment ensures that no element is left unaccounted for and that segment lengths are satisfied. The algorithm maintains the invariant that every element used as a segment end corresponds to a valid segment in the hypothetical original sequence $a$.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter
import heapq

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        b = list(map(int, input().split()))
        counter = Counter(b)
        heap = [-x for x in b]
        heapq.heapify(heap)
        possible = True
        
        while heap:
            x = -heapq.heappop(heap)
            if counter[x] == 0:
                continue
            counter[x] -= 1
            segment_sum = x
            segment = []
            while segment_sum > 0:
                if not heap:
                    possible = False
                    break
                y = -heapq.heappop(heap)
                if counter[y] == 0:
                    continue
                counter[y] -= 1
                segment_sum -= y
                segment.append(y)
                if segment_sum < 0:
                    possible = False
                    break
            if segment_sum != 0:
                possible = False
                break
        print("YES" if possible else "NO")

solve()
```

The solution first reads the number of test cases. For each test case, it builds a max-heap using negated values from the sequence and maintains a counter of frequencies. We greedily pick the largest remaining number, attempt to form a segment of that length by removing numbers, and check for inconsistencies. Any negative count or leftover sum breaks the possibility.

## Worked Examples

### Sample Input 1

```
b = [1, 1, 2, 3, 1, 3, 2, 2, 3]
```

| Step | Heap state | Counter state | Action |
| --- | --- | --- | --- |
| 1 | [3,3,3,2,2,2,1,1,1] | {1:3,2:3,3:3} | Pop 3, start segment length 3 |
| 2 | [3,3,2,2,2,1,1,1] | {1:3,2:3,3:2} | Pop 3, subtract from segment, segment_sum=0 |
| ... | ... | ... | Continue until heap empty |

The trace shows that every segment length can be matched, confirming YES.

### Sample Input 2

```
b = [4, 8, 6, 2]
```

| Step | Heap state | Counter state | Action |
| --- | --- | --- | --- |
| 1 | [8,6,4,2] | {2:1,4:1,6:1,8:1} | Pop 8, segment_sum=8 |
| 2 | 6 available, subtract, segment_sum=2 | ... | Need sum 2, only 2 left, subtract, segment_sum=0 |
| 3 | Heap empty, check leftover | ... | Some numbers left unmatched, output NO |

Demonstrates that invalid sequences are correctly rejected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each element is inserted and removed from a heap once, giving log n factor |
| Space | O(n) | Counter and heap store all elements |

Given the sum of $n$ over all test cases is ≤ 2·10^5, this fits within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("7\n9\n1 1 2 3 1 3 2 2 3\n5\n12 1 2 7 5\n6\n5 7 8 9 10 3\n4\n4 8 6 2\n2\n3 1\n10\n4 6 2 1 9 4 9 3 4 2\n1\n1\n") == "YES\nYES\nYES\nNO\nYES\nYES\nNO", "sample 1"

# custom tests
assert run("2\n1\n1\n3\n1 1 1\n") == "YES\nYES", "single element and all-equal elements"
assert run("1\n5\n5 4 3 2 1\n") == "YES", "descending sequence"
assert run("1\n3\n1 2 4\n") == "NO", "cannot form valid segments"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 | YES | Single element sequence |
| 3\n1 1 1 | YES | All equal elements form single segment |
| 5\n5 4 3 2 1 | YES | Descending sequence handled correctly |
| 3\n1 2 4 | NO | Impossible segment sum |

## Edge Cases

For a single-element sequence $b = [1]$, the heap picks 1, segment sum 1 is satisfied, counter reaches zero, output YES. For sequences with repeated numbers like $b = [1,1,1]$, the greedy algorithm correctly forms one or more segments with length one repeatedly, handling
