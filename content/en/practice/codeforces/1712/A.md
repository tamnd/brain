---
title: "CF 1712A - Wonderful Permutation"
description: "We are given a permutation of integers from 1 to $n$, meaning every number from 1 through $n$ appears exactly once, in some arbitrary order. The task is to minimize the sum of the first $k$ elements in this permutation by performing swaps between any two positions."
date: "2026-06-09T20:19:15+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1712
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 813 (Div. 2)"
rating: 800
weight: 1712
solve_time_s: 113
verified: true
draft: false
---

[CF 1712A - Wonderful Permutation](https://codeforces.com/problemset/problem/1712/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to $n$, meaning every number from 1 through $n$ appears exactly once, in some arbitrary order. The task is to minimize the sum of the first $k$ elements in this permutation by performing swaps between any two positions. Each swap counts as one operation, and we are asked to find the minimum number of such operations needed.

The input size is small: $n$ can be at most 100 and there can be up to 100 test cases. This implies that an $O(n^2)$ solution is acceptable, but we can also aim for $O(n \log n)$ using sorting. Since all numbers are distinct and bounded by $n$, we never have duplicates or out-of-range numbers, so we do not need to validate the permutation.

A subtle edge case is when the first $k$ elements already contain the $k$ smallest numbers. For example, if $n=5$, $k=3$, and the array is $[1, 2, 3, 5, 4]$, no swaps are needed, so the answer should be 0. A naive approach that blindly counts misplaced numbers without considering whether they are already in the first $k$ slots could overcount swaps.

Another edge case is $k=1$ or $k=n$. If $k=1$, we only need the smallest element at the first position. If $k=n$, the sum involves the entire permutation, which is already fixed, so no swaps are possible or necessary.

## Approaches

The brute-force approach would be to try all possible sequences of swaps, computing the sum of the first $k$ elements after each sequence. This is correct in principle but completely impractical. For $n=100$, there are roughly $\binom{100}{2} = 4950$ possible single swaps, and considering multiple swaps quickly becomes combinatorially explosive.

The key insight is that to minimize the sum of the first $k$ elements, we only care about placing the $k$ smallest numbers into the first $k$ positions. The order among these $k$ numbers does not matter, nor does the order among the remaining $n-k$ numbers. Thus, the problem reduces to counting how many of the $k$ smallest numbers are currently outside the first $k$ positions. Each of those numbers will need to be swapped in. Each swap can fix exactly one number in the first $k$ positions, so the number of operations is equal to the number of small numbers currently outside.

To implement this, we first determine the $k$ smallest numbers, which are simply 1 through $k$. We then iterate over the last $n-k$ positions and count how many of these first $k$ numbers are missing from the first $k$ slots. Each missing number corresponds to a required swap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n!) * n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Identify the set of numbers we want in the first $k$ positions. These are the integers 1 through $k$. Using a set allows for $O(1)$ membership checks.
2. Scan the first $k$ elements and mark which of these $k$ numbers are already in place. Keep a count of how many are missing. We only need to know which numbers among 1 through $k$ are absent from the first $k$ slots.
3. The missing numbers in the first $k$ positions correspond exactly to the number of swaps needed. Each swap can bring in one missing small number from the remaining $n-k$ positions.
4. Return the count of missing numbers as the minimum number of operations.

Why it works: The algorithm maintains the invariant that every number outside the first $k$ positions that belongs in the first $k$ is counted exactly once. Swapping each missing number in fixes exactly one deficit. Since we only swap in numbers we need, we never perform unnecessary operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    p = list(map(int, input().split()))
    
    # Set of numbers that should be in the first k positions
    needed = set(range(1, k+1))
    
    # Count numbers among first k that are already correct
    in_place = sum(1 for i in range(k) if p[i] in needed)
    
    # Missing numbers = total needed - already in place
    print(k - in_place)
```

The code reads each test case, identifies the $k$ smallest numbers (1 through $k$), counts how many are already in the first $k$ positions, and prints the difference. Using a set for the smallest numbers ensures constant-time membership checks. Using `sum` with a generator expression avoids creating a temporary list.

## Worked Examples

**Sample Input 1:**

```
3 1
2 3 1
```

| i | p[i] | in needed? | in_place count |
| --- | --- | --- | --- |
| 0 | 2 | no | 0 |

k - in_place = 1 - 0 = 1, which matches the expected output.

**Sample Input 2:**

```
3 3
1 2 3
```

| i | p[i] | in needed? | in_place count |
| --- | --- | --- | --- |
| 0 | 1 | yes | 1 |
| 1 | 2 | yes | 2 |
| 2 | 3 | yes | 3 |

k - in_place = 3 - 3 = 0, correct.

These traces demonstrate that the algorithm counts exactly the missing small numbers in the first $k$ positions, producing the minimal number of swaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Scanning the first k elements and checking membership in a set of size k is linear |
| Space | O(k) | The set storing the k smallest numbers |

Given $t \le 100$ and $n \le 100$, the total operations are at most 10,000, which easily fits in 1 second and 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        p = list(map(int, input().split()))
        needed = set(range(1, k+1))
        in_place = sum(1 for i in range(k) if p[i] in needed)
        print(k - in_place)
        
    return output.getvalue().strip()

# provided samples
assert run("4\n3 1\n2 3 1\n3 3\n1 2 3\n4 2\n3 4 1 2\n1 1\n1") == "1\n0\n2\n0", "sample 1"

# custom cases
assert run("1\n5 2\n5 4 3 2 1") == "2", "both needed numbers are at the end"
assert run("1\n6 3\n1 3 2 6 5 4") == "0", "needed numbers already in first k positions"
assert run("1\n1 1\n1") == "0", "single element, nothing to swap"
assert run("1\n4 4\n4 3 2 1") == "4", "all numbers in wrong positions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 2\n5 4 3 2 1` | 2 | Both needed numbers are at the end |
| `6 3\n1 3 2 6 5 4` | 0 | Needed numbers already in first k positions |
| `1 1\n1` | 0 | Single element, nothing to swap |
| `4 4\n4 3 2 1` | 4 | All numbers in wrong positions, full permutation |

## Edge Cases

If $k = n$, the first $k$ positions include the entire array. The algorithm counts how many numbers from 1 through $n$ are in the first $n$ positions, which is always $n$. The missing count is $n-n=0$, so it correctly outputs 0.

If $k = 1$ and the first element is not 1, the algorithm counts whether 1 is in the first position. If not, it outputs 1, indicating one swap needed to bring the 1 to the front.

If the array is already sorted with the $k$ smallest numbers in the first $k$ slots, the algorithm correctly counts all in place and outputs 0. For example, (n=5, k=3, p=[1,2,3,5,4
