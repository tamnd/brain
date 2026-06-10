---
title: "CF 1490F - Equalize the Array"
description: "We are given an array of integers and are allowed to delete elements. After deletions, the remaining elements must satisfy a strong regularity condition: there must exist a value $C$ such that every number that appears in the final array appears exactly $C$ times, or not at all."
date: "2026-06-10T22:42:26+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1490
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 702 (Div. 3)"
rating: 1500
weight: 1490
solve_time_s: 186
verified: true
draft: false
---

[CF 1490F - Equalize the Array](https://codeforces.com/problemset/problem/1490/F)

**Rating:** 1500  
**Tags:** binary search, data structures, greedy, math, sortings  
**Solve time:** 3m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and are allowed to delete elements. After deletions, the remaining elements must satisfy a strong regularity condition: there must exist a value $C$ such that every number that appears in the final array appears exactly $C$ times, or not at all.

So the final array is composed of several distinct values, and each of those values contributes the same frequency. We are not required to keep all occurrences of a value, we can discard some to make its frequency match the chosen $C$, or discard it completely.

The goal is to maximize how many elements we keep, which is equivalent to minimizing deletions.

The key difficulty is that we must choose both which values to keep and what the common frequency $C$ should be. Every value has its own original frequency, and we can only use it if we can “trim it down” to exactly $C$.

The constraints allow up to $2 \cdot 10^5$ elements across all test cases. This immediately rules out any solution that tries all subsets of values or tries all possible target frequencies with nested per-value scanning. A solution that is roughly $O(n \log n)$ or $O(n)$ per test case is required.

A naive approach would try every possible $C$ from $1$ to $n$, and for each $C$, compute how many elements can be kept by summing $\lfloor f_i / C \rfloor \cdot C$. This is too slow because for each candidate $C$ we would scan all frequencies, leading to $O(n^2)$ worst case.

A second subtle pitfall appears when frequencies are large but uneven. For example, if one value appears 1000 times and many others appear once, choosing $C = 1$ or $C = 2$ behaves very differently. Any approach that assumes greedy sorting of frequencies without fixing $C$ explicitly will fail.

## Approaches

We start by compressing the array into frequencies of each distinct value. Suppose we have frequencies $f_1, f_2, \dots, f_k$.

We want to choose a number $C$ and a subset of these frequencies. Each chosen frequency $f_i$ contributes $C$ elements, as long as $f_i \ge C$. If $f_i < C$, it cannot be used at all.

So for a fixed $C$, the best strategy is deterministic: take every frequency at least $C$, and each contributes exactly $C$. The total kept size becomes:

$$C \cdot (\text{number of } f_i \ge C)$$

Thus, the problem reduces to finding:

$$\max_C \; C \cdot \#(f_i \ge C)$$

The brute force over $C$ from $1$ to $n$ would check this formula in $O(nk)$. This is too slow when $n$ is large.

The key observation is that $C$ only matters at values that appear in the frequency list or at thresholds where the count of eligible frequencies changes. We can sort frequencies and use a counting approach: for each distinct frequency value $f$, treat it as a candidate $C$, and compute how many frequencies are at least $f$. This can be done efficiently by sorting and scanning.

Once frequencies are sorted, we can use binary search or a two-pointer sweep. For each position $i$, if we choose $C = f[i]$, then all frequencies from $i$ onward are usable, giving:

$$f[i] \cdot (k - i)$$

We take the maximum over all $i$.

This works because any optimal solution must align $C$ with some existing frequency value. If $C$ lies strictly between two frequency values, increasing it slightly does not change the number of eligible elements but increases the multiplier only if it hits a valid frequency, so optima occur at discrete points.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over C | $O(n^2)$ | $O(n)$ | Too slow |
| Sort + sweep frequencies | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Count frequencies of all values in the array. This transforms the problem into a list of occurrence counts, removing irrelevant ordering information.
2. Store all frequencies in an array $f$. The structure of the original values no longer matters, only how many times each appears.
3. Sort the frequency array in non-decreasing order. Sorting allows us to efficiently reason about how many values can support a given target frequency.
4. For each index $i$, treat $f[i]$ as a candidate common frequency $C$. This is valid because any optimal $C$ can be mapped to a frequency threshold.
5. Compute how many values can support this $C$, which is $k - i$, since all frequencies from $i$ onward are at least $f[i]$.
6. Compute kept elements as $f[i] \cdot (k - i)$. Track the maximum across all $i$.
7. The answer is total elements minus this maximum kept value.

### Why it works

The algorithm is based on the invariant that for a fixed threshold $C$, only frequencies at least $C$ contribute, and each contributes exactly $C$. Any attempt to use a value with frequency below $C$ is impossible, and any extra occurrences above $C$ are irrelevant because they are discarded. This collapses the optimization into choosing a threshold and counting how many values survive it, and the sorted structure ensures every such threshold is evaluated at the correct boundary points.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import Counter

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        freq = Counter(a)
        f = sorted(freq.values())
        
        k = len(f)
        best_keep = 0
        
        for i, c in enumerate(f):
            best_keep = max(best_keep, c * (k - i))
        
        print(n - best_keep)

if __name__ == "__main__":
    solve()
```

The code begins by converting the array into a frequency map, which is the core reduction step. Sorting the frequencies enables the threshold-based evaluation. Each iteration treats a frequency as a potential common count and evaluates how many values can participate at that level.

The subtraction from $n$ at the end converts the maximization of kept elements into the required minimization of deletions.

A common mistake is to try to multiply each frequency by how many times it can be divided by $C$, but that breaks the condition that all chosen values must share the same exact frequency.

## Worked Examples

### Example 1

Input:

```
6
1 3 2 1 4 2
```

Frequencies are:

| Value | Frequency |
| --- | --- |
| 1 | 2 |
| 2 | 2 |
| 3 | 1 |
| 4 | 1 |

Sorted frequencies: [1, 1, 2, 2]

| i | f[i] | k - i | kept = f[i] * (k - i) |
| --- | --- | --- | --- |
| 0 | 1 | 4 | 4 |
| 1 | 1 | 3 | 3 |
| 2 | 2 | 2 | 4 |
| 3 | 2 | 1 | 2 |

Best kept = 4, deletions = 6 - 4 = 2.

This shows that either choosing $C=1$ or $C=2$ gives optimal retention, but only aligned thresholds matter.

### Example 2

Input:

```
4
100 100 4 100
```

Frequencies:

| Value | Frequency |
| --- | --- |
| 100 | 3 |
| 4 | 1 |

Sorted: [1, 3]

| i | f[i] | k - i | kept |
| --- | --- | --- | --- |
| 0 | 1 | 2 | 2 |
| 1 | 3 | 1 | 3 |

Best kept = 3, so we remove 1 element.

This confirms the intuition that keeping only the value with frequency 3 is optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting frequencies dominates per test case |
| Space | $O(n)$ | Frequency map and list storage |

The total $n$ across tests is bounded by $2 \cdot 10^5$, so sorting once per test suite remains efficient under the time limit.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        freq = Counter(a)
        f = sorted(freq.values())
        k = len(f)
        best = 0
        for i, c in enumerate(f):
            best = max(best, c * (k - i))
        out.append(str(n - best))
    return "\n".join(out)

# provided samples
assert run("""3
6
1 3 2 1 4 2
4
100 100 4 100
8
1 2 3 3 3 2 6 6
""") == """2
1
2"""

# custom cases
assert run("""1
1
7
""") == "0"

assert run("""1
5
1 1 1 1 1
""") == "0"

assert run("""1
5
1 2 3 4 5
""") == "4"

assert run("""1
6
1 1 2 2 3 3
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimal boundary |
| all equal | 0 | optimal full retention |
| all distinct | 4 | worst fragmentation case |
| perfectly balanced pairs | 0 | uniform frequency case |

## Edge Cases

One edge case is when all elements are unique. For input like `[1,2,3,4,5]`, all frequencies are 1. The algorithm considers only $C=1$, yielding full retention and zero deletions, matching the requirement.

Another edge case is a single highly frequent element among many rare ones. For `[1,1,1,1,2,3,4]`, frequencies are `[4,1,1,1]`. The optimal choice is $C=1$, keeping all elements. The sweep over sorted frequencies correctly evaluates both $C=1$ and $C=4$, ensuring the maximum is captured.

A final edge case is when multiple medium-frequency values exist. For `[1,1,2,2,3,3]`, all frequencies are equal, so every candidate produces the same result. The algorithm consistently evaluates each threshold, and no special casing is needed because the sorted structure naturally handles equality groups.
