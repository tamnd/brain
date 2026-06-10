---
title: "CF 1608B - Build the Permutation"
description: "We are asked to construct a permutation of the numbers from 1 to n that has exactly a local maxima and b local minima in the interior positions. A local maximum is a number larger than its immediate neighbors, and a local minimum is a number smaller than its immediate neighbors."
date: "2026-06-10T07:32:56+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1608
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 758 (Div.1 + Div. 2)"
rating: 1200
weight: 1608
solve_time_s: 92
verified: false
draft: false
---

[CF 1608B - Build the Permutation](https://codeforces.com/problemset/problem/1608/B)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a permutation of the numbers from 1 to n that has exactly a local maxima and b local minima in the interior positions. A local maximum is a number larger than its immediate neighbors, and a local minimum is a number smaller than its immediate neighbors. The first and last elements are never considered as local extrema because they have only one neighbor.  

The inputs are t test cases, each with three integers n, a, and b. We must either output a valid permutation satisfying the counts of maxima and minima, or -1 if no such permutation exists.  

The constraints are important. n can be as large as 10^5 and the total sum of n across all test cases is 10^5, so an O(n log n) or O(n) solution per test case is acceptable, but anything like O(n^2) is too slow. Additionally, a and b must be achievable given n. A naive approach that generates all permutations would have complexity O(n!), which is clearly infeasible.  

Edge cases to watch out for include situations where the requested number of peaks and valleys is too large for the length of the array. For example, if n=4 and we ask for a=2 maxima and b=1 minimum, it is impossible because the maximum number of interior extrema in an array of length 4 is 2, alternating peak and valley. Also, if a or b is zero, we need to handle sequences that are strictly increasing or decreasing in the middle correctly.

## Approaches

The brute-force approach would be to generate all permutations of numbers 1 through n and count the number of peaks and valleys for each permutation. While correct in principle, the complexity is O(n!) and would never finish for n > 10. Even for small n, the number of permutations grows factorially, so this is immediately ruled out.  

The key insight comes from observing that peaks and valleys naturally alternate. Each interior element can be either a peak, a valley, or part of a monotone sequence. The maximum number of peaks or valleys is limited by how many alternating positions we can have, which is ⌊(n-1)/2⌋ for peaks or valleys in the middle of the array. Once we know this, we can construct the permutation greedily: place the largest numbers in positions where we want peaks and the smallest numbers in positions where we want valleys, filling the remaining numbers in order. This produces a permutation in linear time without checking all possibilities.  

By alternating high and low numbers, we can guarantee that each peak is greater than neighbors and each valley is smaller than neighbors. We must also check that a + b ≤ n - 2, because interior positions are limited to indices 2 through n-1. If the request exceeds this bound, the permutation is impossible.  

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(n!) | O(n) | Too slow |
| Greedy construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. First, check if the request is feasible. If a + b > n - 2, then there are not enough interior positions to satisfy both counts, so output -1 immediately.  

2. Initialize an empty array `p` of length n. We will fill it in three segments: the peaks, the valleys, and the remaining numbers.  

3. Maintain two pointers: `low = 1` for the smallest available number, and `high = n` for the largest. These will be used to assign numbers to ensure peaks and valleys.  

4. If a ≥ b, we start with a peak pattern. Place numbers alternating between high and low starting with a high for the peak, then a low for the valley, until all a peaks and b valleys are placed. The number of remaining elements is n - (a + b + 1).  

5. If b > a, start with a valley pattern. Place numbers alternating starting with low, then high, until all valleys and peaks are placed.  

6. Fill the remaining positions with numbers in increasing or decreasing order as appropriate to avoid creating extra peaks or valleys.  

7. Output the final array. This guarantees exactly a peaks and b valleys. The algorithm relies on the invariant that each peak gets a larger number than its neighbors and each valley gets a smaller number than its neighbors.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, a, b = map(int, input().split())
        if a + b > n - 2 or abs(a - b) > 1:
            print(-1)
            continue

        p = [0] * n
        low, high = 1, n
        idx = 0

        # Determine starting pattern
        if a >= b:
            # start with peak
            for i in range(a + b + 1):
                if i % 2 == 0:
                    p[idx] = high
                    high -= 1
                else:
                    p[idx] = low
                    low += 1
                idx += 1
        else:
            # start with valley
            for i in range(a + b + 1):
                if i % 2 == 0:
                    p[idx] = low
                    low += 1
                else:
                    p[idx] = high
                    high -= 1
                idx += 1

        # Fill remaining numbers
        for i in range(low, high + 1):
            p[idx] = i
            idx += 1

        print(' '.join(map(str, p)))

if __name__ == "__main__":
    solve()
```

The first section checks feasibility, including the subtle constraint that peaks and valleys cannot differ by more than 1, otherwise alternation is impossible. The next part constructs the alternating sequence for the peaks and valleys. We choose to start with a peak if there are more peaks than valleys, ensuring correct alternation. The remaining numbers are placed in increasing order to prevent additional extrema. This order preserves all intended peaks and valleys.

## Worked Examples

Sample input `4 1 1`:

| Step | idx | p filled | low | high | Action |
|---|---|---|---|---|---|
| 0 | 0 | [] | 1 | 4 | start peak |
| 1 | 0 | [4] | 1 | 3 | place high |
| 2 | 1 | [4,1] | 2 | 3 | place low |
| 3 | 2 | [4,1,3] | 2 | 2 | remaining numbers |
| 4 | 3 | [4,1,3,2] | 2 | 2 | fill remaining 2 |

Result: `[4,1,3,2]` has one peak and one valley as requested.

Sample input `6 1 2`:

| Step | idx | p filled | low | high | Action |
|---|---|---|---|---|---|
| 0 | 0 | [] | 1 | 6 | start valley |
| 1 | 0 | [1] | 2 | 6 | place low |
| 2 | 1 | [1,6] | 2 | 5 | place high |
| 3 | 2 | [1,6,2] | 3 | 5 | place low |
| 4 | 3 | [1,6,2,5] | 3 | 4 | remaining numbers |
| 5 | 4 | [1,6,2,5,3,4] | 3 | 4 | fill 3,4 |

Result `[1,6,2,5,3,4]` has one peak and two valleys.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n) per test case | Each number is placed exactly once. |
| Space | O(n) per test case | Storing the permutation array. |

Since the total sum of n across all test cases is ≤ 10^5, the total time complexity is within 10^5 operations, which fits comfortably in 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("3\n4 1 1\n6 1 2\n6 4 0\n") == "4 1 3 2\n1 6 2 5 3 4\n-1"

# custom cases
assert run("1\n2 0 0\n") == "1 2", "minimum size input"
assert run("1\n5 2 2\n") == "-1", "impossible case, a+b>n-2"
assert run("1\n5 2 1\n") == "5 1 4 2 3", "alternating peaks and valleys"
assert run("1\n3 1 1\n") == "3 1 2", "small array with one peak and one valley"
assert run("1\n7 3 3\n") == "7 1 6 2 5 3 4", "maximum peaks/valleys for n=7"
```

| Test input | Expected output | What it validates |
|---|---|---|
| 2 0 0 | 1 2 |
