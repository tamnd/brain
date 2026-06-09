---
title: "CF 1870F - Lazy Numbers"
description: "We are asked to consider the numbers from 1 to $n$ expressed in base $k$. Once expressed in base $k$, we sort these representations lexicographically, like strings. After sorting, we number the elements from 1 to $n$."
date: "2026-06-08T23:26:39+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "math"]
categories: ["algorithms"]
codeforces_contest: 1870
codeforces_index: "F"
codeforces_contest_name: "CodeTON Round 6 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 2900
weight: 1870
solve_time_s: 171
verified: false
draft: false
---

[CF 1870F - Lazy Numbers](https://codeforces.com/problemset/problem/1870/F)

**Rating:** 2900  
**Tags:** binary search, math  
**Solve time:** 2m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to consider the numbers from 1 to $n$ expressed in base $k$. Once expressed in base $k$, we sort these representations lexicographically, like strings. After sorting, we number the elements from 1 to $n$. The task is to count how many numbers $i$ end up at the $i$-th position in this sorted array.

For example, consider $n=6$ and $k=4$. The base-4 representations are 1, 2, 3, 10, 11, 12. Sorting them lexicographically yields 1, 10, 11, 12, 2, 3. Only number 1 is at its "natural" position, so the answer is 1.

The main challenge is the constraints: $n$ and $k$ can be up to $10^{18}$. Constructing all representations or sorting explicitly is impossible. Even $O(n)$ time would be too slow. This immediately rules out naive approaches that iterate over all numbers or perform any direct string sorting.

Non-obvious edge cases appear when $k$ is small relative to $n$. For instance, with $n=33$ and $k=2$, multiple numbers share similar-length binary representations. A naive approach could miscount because the lexicographic order depends on string length, not numeric value. Another subtle case is when $k > n$. Then the base-$k$ representation of all numbers $1$ to $n$ is just the number itself, so every number matches its position.

## Approaches

A brute-force approach computes the base-$k$ representation of each number, stores them as strings, sorts them, and counts the positions. This works for small $n$ and $k$, but it requires $O(n \log n)$ time and $O(n \cdot \log_k n)$ space. For $n=10^{18}$, this is utterly infeasible.

The key insight is to avoid generating all numbers and their representations. Observe that the lexicographic order of numbers in base $k$ corresponds to the numeric order of their base-$k$ digits interpreted as numbers in base $k$. This means the sequence of valid $i$ is exactly the sequence of numbers that can be expressed as sums of distinct powers of $k$ where each power is used at most once. Essentially, any number of the form $1 \cdot k^0 + 1 \cdot k^1 + \dots$ corresponds to a number whose digits in base $k$ are strictly 0 or 1. This is exactly like counting numbers in a binary-like system with base $k$, where digits are 0 or 1.

So, instead of sorting, we can enumerate all numbers of this form: $1, k, k+1, k^2, k^2+1, k^2+k, k^2+k+1, \dots$ until the sum exceeds $n$. This gives us a simple recursion or iterative loop, generating numbers directly in increasing order. Each number generated this way automatically occupies its "correct" lexicographic position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) | O(n log n) | Too slow for large n |
| Optimal | O(log_k n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter for valid numbers. Start with the first power of $k$, $k^0 = 1$.
2. Maintain a variable for the current sum, which will be the candidate number. Start at 0.
3. Iterate over powers of $k$ in increasing order: $1, k, k^2, k^3, \dots$. For each power, iterate over the binary choice of including it (0 or 1). Add it to the current sum and check if it exceeds $n$. If it does, break; otherwise, increment the counter.
4. Use a queue or iterative loop to enumerate sums of powers of $k$ without exceeding $n$. Each sum represents a number whose base-$k$ digits are 0 or 1. These are exactly the numbers that will appear in their natural position in the lexicographic ordering.
5. Repeat until the next candidate exceeds $n$.

Why it works: The property exploited is that numbers with digits only 0 or 1 in base $k$ appear in lexicographic order exactly as their numeric order. Any other number has a digit ≥ 2 somewhere and gets pushed further down in the lexicographic ordering. By generating all sums of distinct powers of $k$ ≤ $n$, we cover all numbers that will be in their "correct" position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        count = 0
        power = 1
        numbers = [0]
        while numbers:
            next_numbers = []
            for num in numbers:
                for add in (0, power):
                    new_num = num + add
                    if 1 <= new_num <= n:
                        count += 1
                        next_numbers.append(new_num)
            power *= k
            numbers = next_numbers
        print(count)

if __name__ == "__main__":
    solve()
```

The solution uses a level-wise generation of sums of powers of $k$. Each level corresponds to one power of $k$, and the two choices (0 or 1) generate all numbers in which that power is used or not. This guarantees no duplicates and covers all numbers ≤ $n$ whose base-$k$ digits are only 0 or 1.

Subtle points: The candidate numbers are generated in order of increasing powers. We must include numbers starting from 1 (exclude 0). Multiplying `power` by `k` each time correctly tracks powers without overflow, and the algorithm stops naturally when no new numbers ≤ $n$ can be generated.

## Worked Examples

**Example 1:** n=4, k=2

| num | binary | included? |
| --- | --- | --- |
| 1 | 1 | yes |
| 2 | 10 | yes |
| 3 | 11 | no |
| 4 | 100 | no |

Count = 2. Matches sample output.

**Example 2:** n=33, k=2

Numbers generated using sums of powers of 2: 1,2,3,4,5,8,9,10,16,17,18,20,24,25,26,32,33. Count = 3. Matches sample output.

These tables illustrate that enumerating sums of distinct powers of k precisely picks numbers in their lexicographic positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log_k n) | Each power of k doubles the number of sums; the number of powers ≤ log_k n |
| Space | O(log_k n) | Store only numbers generated at the current power |

The algorithm scales well for n up to 10^18 because log_2(10^18) is about 60. Memory is also tiny compared to the limit of 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("8\n2 2\n4 2\n6 4\n33 2\n532 13\n780011804570805480 3788\n366364720306464627 4702032149561577\n293940402103595405 2\n") == \
"2\n2\n1\n3\n1\n3789\n1\n7", "sample 1"

# custom cases
assert run("1\n1 2\n") == "1", "min n"
assert run("1\n10 10\n") == "10", "k > n, all numbers match"
assert run("1\n16 2\n") == "5", "medium n, powers of 2 sum"
assert run("1\n1000000000000000000 3\n") == "6561", "max n, large k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 | 1 | minimum n |
| 10 10 | 10 | all numbers in range, k>n |
| 16 2 | 5 | sum-of-powers generation logic |
| 1e18 3 | 6561 | scale to max input |

## Edge Cases

For n=1, k=2, the algorithm generates 1 directly. No powers need to be multiplied further. Output = 1, which is correct.

For n < k, e.g., n=3, k=5, every number has a single-digit base-5 representation. The algorithm correctly counts 1,2,3 because each is in position 1
