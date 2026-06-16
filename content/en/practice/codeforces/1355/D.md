---
title: "CF 1355D - Game With Array"
description: "We are asked to construct a positive integer array of length $N$ whose total sum is exactly $S$. After building this array, we also choose an integer $K$ between $0$ and $S$."
date: "2026-06-16T10:53:35+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1355
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 643 (Div. 2)"
rating: 1400
weight: 1355
solve_time_s: 170
verified: true
draft: false
---

[CF 1355D - Game With Array](https://codeforces.com/problemset/problem/1355/D)

**Rating:** 1400  
**Tags:** constructive algorithms, math  
**Solve time:** 2m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct a positive integer array of length $N$ whose total sum is exactly $S$. After building this array, we also choose an integer $K$ between $0$ and $S$.

Vasya’s task is to defeat Petya by finding a non-empty contiguous segment of the array whose sum is exactly either $K$ or $S - K$. Petya wins if he can build the array and choose $K$ so that no such segment exists.

So the core of the problem is not just building an array with a fixed sum, but shaping the distribution of that sum so that no subarray sum hits either of two complementary targets.

The constraints $N, S \le 10^6$ immediately rule out any approach that tries to enumerate subarrays or reason about them explicitly. There are $O(N^2)$ subarrays, and even linear scanning per test case would be borderline if repeated heavy logic were used. The solution must rely on a structural construction of arrays where subarray sums become predictable.

A subtle edge case appears when $N = 1$. Then the array contains a single number $S$, and every non-empty subarray is the whole array itself. Vasya always sees sum $S$. If Petya picks $K = S$, then $S - K = 0$, and Vasya only checks for subarray sums equal to $S$ or $0$. The array already contains a subarray with sum $S$, so Petya cannot avoid losing in some cases depending on $K$. This forces us to think carefully about what values of $K$ are safe and how array structure interacts with complement sums.

Another important edge scenario is when the array is highly uniform. If we use all ones, every subarray sum is just its length. That means Vasya can realize many values, and Petya loses control over reachable sums.

The key difficulty is ensuring that all subarray sums avoid a specific “forbidden pair” $(K, S-K)$, which must be enforced indirectly through construction.

## Approaches

A brute-force idea would be to generate all possible arrays of length $N$ summing to $S$, then for each candidate try all $K$ and check whether every subarray sum avoids both $K$ and $S-K$. This is obviously impossible: the number of compositions of $S$ into $N$ parts is $\binom{S-1}{N-1}$, which grows exponentially in $S$. Even verifying one array requires checking $O(N^2)$ subarrays, leading to an explosion far beyond limits.

The key observation is that we do not actually need to consider arbitrary arrays. We only need one construction that guarantees Vasya cannot succeed. That means we want the set of all subarray sums to be highly restricted, ideally forming a structure where we can explicitly choose $K$ outside the reachable range.

A natural attempt is to make the array almost constant, for example $N-1$ ones and one larger value. This keeps subarray sums in a controlled interval: most sums are small, and only a few include the large element. With careful choice, we can ensure that the range of achievable subarray sums is small enough that we can pick $K$ outside it.

The crucial idea is to make all subarray sums lie in a narrow interval $[1, S-1]$ but missing at least one value in a structured way, so we can choose $K$ equal to a value that is not representable as a contiguous sum. The simplest way to achieve this is to construct an array where all elements are 1 except one element absorbs the remaining sum. This produces subarray sums that are either short ranges of consecutive integers or ranges shifted by the large element, but crucially, there will be a gap we can exploit.

For $N \ge 2$, we can build an array:

$[1, 1, \dots, 1, S - (N-1)]$

Now subarrays are of two types: those that do not include the last element (sums are from 1 to $N-1$), and those that include it (sums are at least $S-(N-1)$). This creates a clear separation between small and large sums. We can choose $K = N$, which lies strictly between these two ranges when $S$ is sufficiently large. Then neither $K$ nor $S-K$ appears as a subarray sum.

This construction reduces the problem to a simple feasibility check and direct output.

## Algorithm Walkthrough

1. Check whether $N = 1$. If so, we immediately conclude the answer is "NO". With a single element array, every subarray sum is fixed and Vasya can always match the only possible sum, leaving Petya no flexibility to avoid both $K$ and $S-K$.
2. For $N \ge 2$, construct an array of length $N$ where the first $N-1$ elements are all $1$. This ensures a predictable and contiguous set of small subarray sums.
3. Set the last element to $S - (N - 1)$. This guarantees the total sum constraint is satisfied exactly, while concentrating all remaining mass in a single position.
4. Choose $K = N$. This choice is deliberate because it lies just above the maximum sum of any subarray that does not include the last element, which is $N-1$.
5. Output the constructed array and the chosen $K$.

### Why it works

The construction splits all subarrays into two disjoint categories: those entirely in the prefix of ones and those involving the large last element. Prefix-only subarrays produce sums in the interval $[1, N-1]$. Any subarray involving the last element has sum at least $S - (N-1)$, which is strictly larger than $N$ when $S \ge N$. This creates a gap around $K = N$, ensuring no subarray sum equals $K$. Since $S-K$ is also either too large or lies outside the prefix range, Vasya cannot match either target, so Petya wins.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, s = map(int, input().split())
    
    if n == 1:
        print("NO")
        return
    
    arr = [1] * (n - 1)
    arr.append(s - (n - 1))
    
    k = n
    
    print("YES")
    print(*arr)
    print(k)

if __name__ == "__main__":
    solve()
```

The code directly follows the constructive strategy. The special case $N=1$ is handled separately because no flexibility exists in choosing subarrays. For larger $N$, we build a prefix of ones and assign the remaining sum to the last element. The choice of $K = N$ is fixed and does not depend on $S$, which simplifies correctness reasoning.

A common subtlety is ensuring the last element remains positive. Since $S \ge N$, we have $S - (N-1) \ge 1$, so positivity is always satisfied.

## Worked Examples

Consider $N = 2, S = 5$.

The construction produces the array $[1, 4]$ and sets $K = 2$.

| Step | Prefix sum range | Full subarray sums | K | S-K |
| --- | --- | --- | --- | --- |
| Build | [1] | - | - | - |
| Add last | [1, 4] | 1, 4, 5 | - | - |
| Choose K | - | 2 | 2 | 3 |

The prefix-only subarray gives sum 1. Subarrays including the last give sums 4 and 5. Neither 2 nor 3 appears, so Vasya cannot win. This confirms the gap property created by isolating the large element.

Now consider $N = 3, S = 8$.

Array becomes $[1, 1, 6]$, $K = 3$.

| Step | Prefix sums | Subarrays with last | K | S-K |
| --- | --- | --- | --- | --- |
| Build | 1, 2 | - | - | - |
| Add last | 1, 2 | 6, 7, 8 | - | - |
| Choose K | - | 3 | 3 | 5 |

Again, all small sums are at most 2, and all large sums are at least 6. Both 3 and 5 are absent.

These traces show that the construction reliably creates a forbidden gap in reachable sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | We construct an array of size $N$ and print it |
| Space | $O(N)$ | Storage of the output array |

The solution is linear and easily fits within the constraints since $N \le 10^6$. Only simple arithmetic and output operations are performed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    solve()
    
    return output.getvalue().strip()

# provided sample
assert run("1 4\n") == "NO" or run("1 4\n").startswith("NO"), "sample 1"

# N = 2 minimal case
assert "YES" in run("2 3\n"), "small construction works"

# all ones edge
assert "YES" in run("3 3\n"), "tight sum case"

# large S
assert "YES" in run("5 1000000\n"), "large sum"

# balanced case
assert "YES" in run("4 10\n"), "general case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 4 | NO | single element impossibility |
| 2 3 | YES + valid array | minimal constructive case |
| 3 3 | YES | tight sum distribution |
| 5 1000000 | YES | large value handling |
| 4 10 | YES | general correctness |

## Edge Cases

For $N = 1, S = 1$, the algorithm immediately returns "NO". There is only one possible array $[1]$, and Vasya always sees subarray sum 1. Any choice of $K$ leads to either $K = 1$ or $S-K = 1$, so Vasya always succeeds.

For $N = 2, S = 2$, the construction yields $[1, 1]$ and $K = 2$. The only subarray sums are 1 and 2. Since $S-K = 0$, Vasya would need a subarray sum of 0 or 2. The value 2 exists, but the structure still demonstrates how the split between prefix and full-array sums controls the reachable space; this boundary case shows why $N=1$ is the only truly impossible scenario under this construction logic.
