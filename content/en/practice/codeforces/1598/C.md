---
title: "CF 1598C - Delete Two Elements"
description: "We are given an array and its average value is fixed for the original array. The task is to remove exactly two elements and count how many pairs of indices can be removed such that the average of the remaining elements does not change."
date: "2026-06-10T08:46:03+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "implementation", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1598
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 115 (Rated for Div. 2)"
rating: 1200
weight: 1598
solve_time_s: 86
verified: true
draft: false
---

[CF 1598C - Delete Two Elements](https://codeforces.com/problemset/problem/1598/C)

**Rating:** 1200  
**Tags:** data structures, dp, implementation, math, two pointers  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and its average value is fixed for the original array. The task is to remove exactly two elements and count how many pairs of indices can be removed such that the average of the remaining elements does not change.

Instead of thinking in terms of averages directly, it is more useful to translate the condition into a sum constraint. If the original array has sum $S$ and size $n$, then the average is $k = S/n$. After removing two elements $a_i$ and $a_j$, the remaining sum becomes $S - a_i - a_j$, and the remaining size is $n - 2$. We require:

$$\frac{S - a_i - a_j}{n - 2} = \frac{S}{n}$$

This equation fully describes which pairs are valid.

The constraints allow up to $2 \cdot 10^5$ total elements across all test cases, which rules out any quadratic solution per test case. Any approach that tries all pairs directly would require up to $O(n^2)$ operations, which is far beyond what is feasible in two seconds.

A subtle issue appears when handling averages: since $k$ may not be an integer, naive integer comparisons can break correctness if one tries to compute $k$ and compare floating point values. Another common mistake is recomputing sums repeatedly inside loops, which accidentally turns an $O(n)$ idea into $O(n^2)$.

A concrete edge case is when all elements are equal. For example, in `[5, 5, 5, 5]`, every pair works, but a wrong derivation that assumes some “special structure” might incorrectly reject valid pairs because it expects variability in values.

Another case is when only very specific complementary pairs work, such as `[50, 20, 10]`, where removing any pair changes the mean, so the answer is zero. This catches solutions that incorrectly assume symmetry or frequency-based heuristics without deriving the exact condition.

## Approaches

A brute-force solution tries every pair $(i, j)$, removes them, recomputes the sum, and checks whether the resulting mean equals the original mean. Recomputing the sum after each removal costs $O(n)$, and there are $O(n^2)$ pairs, so the total becomes $O(n^3)$. Even if we precompute the sum once, each pair still requires checking a derived condition, giving $O(n^2)$, which already becomes too large for $2 \cdot 10^5$ total elements.

The key observation comes from rewriting the condition algebraically. Starting from:

$$\frac{S - a_i - a_j}{n - 2} = \frac{S}{n}$$

cross-multiplying gives:

$$n(S - a_i - a_j) = (n - 2)S$$

Expanding:

$$nS - n(a_i + a_j) = nS - 2S$$

Canceling $nS$:

$$n(a_i + a_j) = 2S$$

So:

$$a_i + a_j = \frac{2S}{n}$$

This reduces the entire problem to counting pairs whose sum equals a fixed target value. That immediately suggests a frequency-based linear solution: we scan the array while tracking how many times each value has appeared, and for each element, we check how many previous elements form the required sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Compute the total sum $S$ of the array and derive the target sum $T = \frac{2S}{n}$. If $2S$ is not divisible by $n$, no valid pair exists, so the answer is zero. This divisibility check prevents working with non-integer targets that cannot correspond to integer array elements.
2. Create a hash map to store frequencies of values seen so far. This allows constant-time lookup for complements.
3. Iterate through the array from left to right, treating each element $a[i]$ as the second element of a potential pair.
4. For each element, compute the required complement $T - a[i]$. The number of valid pairs ending at this index is exactly the number of times this complement has already appeared in the prefix.
5. Add this count to the answer, then increment the frequency of the current element.

The key idea is that every valid pair is counted exactly once when the second element of the pair is processed.

### Why it works

The transformation reduces the condition to a fixed-sum pairing problem. Each valid pair corresponds uniquely to a pair of indices $(i, j)$ with $i < j$ and $a_i + a_j = T$. The frequency map ensures that when processing index $j$, we count exactly those $i < j$ that satisfy the equation. No pair is missed because every index is processed as a second endpoint exactly once, and no pair is double-counted because we never look forward in the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        
        S = sum(arr)
        if (2 * S) % n != 0:
            print(0)
            continue
        
        target = (2 * S) // n
        
        freq = {}
        ans = 0
        
        for x in arr:
            need = target - x
            if need in freq:
                ans += freq[need]
            freq[x] = freq.get(x, 0) + 1
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by computing the total sum and checking whether a valid integer target pair-sum exists. If not, it immediately returns zero, since no pair of integers can satisfy a fractional requirement.

The frequency dictionary stores how many times each value has been seen so far. As we scan the array, each element contributes to the answer based on previously seen complements, ensuring correct ordering $i < j$.

Using prefix frequencies avoids double counting and keeps the solution linear per test case.

## Worked Examples

### Example 1

Input:

```
n = 5
arr = [1, 4, 7, 3, 5]
```

We compute:

$S = 20$, so $T = 2S/n = 40/5 = 8$

We track frequency and contributions:

| i | a[i] | freq before | need = 8 - a[i] | contribution | freq after |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | {} | 7 | 0 | {1:1} |
| 1 | 4 | {1:1} | 4 | 0 | {1:1,4:1} |
| 2 | 7 | {1:1,4:1} | 1 | 1 | {1:1,4:1,7:1} |
| 3 | 3 | ... | 5 | 0 | ... |
| 4 | 5 | ... | 3 | 1 | ... |

Total answer is 2.

This shows that valid pairs are exactly those forming sum 8, and each is counted when the second element is encountered.

### Example 2

Input:

```
n = 4
arr = [8, 8, 8, 8]
```

Here $S = 32$, so $T = 16$. Every pair of elements sums to 16.

| i | a[i] | freq before | need | contribution | freq after |
| --- | --- | --- | --- | --- | --- |
| 0 | 8 | {} | 8 | 0 | {8:1} |
| 1 | 8 | {8:1} | 8 | 1 | {8:2} |
| 2 | 8 | {8:2} | 8 | 2 | {8:3} |
| 3 | 8 | {8:3} | 8 | 3 | {8:4} |

Total is $1 + 2 + 3 = 6$.

This demonstrates that multiplicity is naturally handled by frequency accumulation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each element is processed once with O(1) hash operations |
| Space | $O(n)$ | Frequency map stores at most n distinct values |

The total sum of $n$ across test cases is $2 \cdot 10^5$, so a linear scan over all input elements is well within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n = int(input())
            arr = list(map(int, input().split()))
            S = sum(arr)
            if (2 * S) % n != 0:
                print(0)
                continue
            target = (2 * S) // n
            freq = {}
            ans = 0
            for x in arr:
                ans += freq.get(target - x, 0)
                freq[x] = freq.get(x, 0) + 1
            print(ans)

    solve()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("""4
4
8 8 8 8
3
50 20 10
5
1 4 7 3 5
7
1 2 3 4 5 6 7
""") == "6\n0\n2\n3"

# all equal small
assert run("""1
3
5 5 5
""") == "3"

# impossible fractional target
assert run("""1
3
1 1 2
""") == "0"

# large symmetric
assert run("""1
6
1 2 3 4 5 6
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 3 | all pairs valid counting |
| fractional mean | 0 | divisibility guard |
| 1..6 array | 3 | correct pair counting for multiple matches |

## Edge Cases

For an array where all values are identical, such as `[10, 10, 10]`, the algorithm computes a target equal to twice that value. Every element matches the complement condition, and the frequency accumulation counts all pairs exactly once as the second index increases. The final output is $\binom{3}{2} = 3$, matching the expected combinatorial result.

For a case where the required sum is not an integer, such as `[1, 1, 2]`, the computed target becomes non-integral because $2S/n$ is not divisible. The algorithm immediately returns zero, and no frequency processing occurs. This avoids any incorrect pairing attempts that would otherwise rely on impossible equality.
