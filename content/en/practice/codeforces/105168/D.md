---
title: "CF 105168D - XOR Pairing"
description: "We are given several independent test cases. In each test case, there is an array of integers and a target value $k$."
date: "2026-06-27T09:01:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105168
codeforces_index: "D"
codeforces_contest_name: "2024 Fujian Normal University Programming Contest"
rating: 0
weight: 105168
solve_time_s: 39
verified: true
draft: false
---

[CF 105168D - XOR Pairing](https://codeforces.com/problemset/problem/105168/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, there is an array of integers and a target value $k$. The task is to count how many unordered index pairs $(i, j)$ with $i < j$ have the property that the bitwise XOR of the two chosen array elements equals exactly $k$.

The input is purely numerical: each test case describes a multiset of values, and the question is how many pairs of values interact under XOR to produce a fixed result. The output for each test case is a single integer representing that count.

The constraints make it clear that any solution that examines all pairs directly will not scale. The total number of elements across all test cases can reach $2 \cdot 10^5$, so a quadratic scan would imply on the order of $4 \cdot 10^{10}$ XOR operations in the worst case, which is far beyond what 2 seconds allows. This immediately rules out naive pair enumeration.

There are two subtle edge situations that often trip incorrect approaches.

First, when $k = 0$, the condition becomes $a_i = a_j$. A naive implementation that does not separate this case might still work, but some optimizations that assume $k > 0$ or attempt to "avoid self-inverse counting" can break. For example, in an array $[1, 1, 1]$, the correct answer is 3 pairs, not 0.

Second, repeated values matter heavily. If an element appears many times, it contributes combinatorially to the answer. Any approach that treats the array as a set instead of a multiset will undercount.

## Approaches

The brute-force idea is straightforward. For each pair of indices $(i, j)$, compute $a_i \oplus a_j$ and check whether it equals $k$. This is correct because it directly evaluates the condition stated in the problem. However, it performs one constant-time XOR per pair, leading to $\frac{n(n-1)}{2}$ operations per test case. With $n = 2 \cdot 10^5$, this is infeasible.

The key observation is that XOR equations can be rearranged deterministically. If $a_i \oplus a_j = k$, then fixing $a_i$ implies a unique required value for $a_j$: namely $a_j = a_i \oplus k$. This turns the problem into a frequency matching task instead of a pair enumeration task.

Instead of searching pairs, we maintain a frequency map of values seen so far. As we scan the array from left to right, for each element $x$, we compute the value $x \oplus k$ and check how many times it has already appeared. Each such occurrence forms a valid pair with the current element. Then we record $x$ into the frequency map.

This works because XOR is reversible: applying XOR with $k$ transforms a target into its unique partner. No collisions or ambiguity exist in this mapping, so counting complements incrementally yields exactly the number of valid pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Frequency Hash Map | $O(n)$ average | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Initialize an empty hash map `freq` to store counts of values we have already processed.
2. Initialize an პასუხ variable `ans = 0`.
3. Iterate through the array from left to right, taking each value `x`.
4. Compute the required partner value `y = x XOR k`. This is the only value that can pair with `x` to produce XOR equal to `k`.
5. Add `freq[y]` to `ans`. This counts all previous occurrences of valid partners.
6. Increment `freq[x]` by 1 to record that we have now seen `x`.

The order is essential: we only count pairs where the second index is greater than the first, which is ensured by only matching against previously seen elements.

### Why it works

At every position, `freq` stores the exact multiset of values from indices strictly less than the current index. For each current element `x`, every earlier element `y` such that $y \oplus x = k$ corresponds to a valid pair with $i < j$. Because XOR defines a bijection $y = x \oplus k$, every valid pair is counted exactly once, when the right endpoint is processed. No pair is missed and no pair is double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        freq = {}
        ans = 0
        
        for x in a:
            y = x ^ k
            ans += freq.get(y, 0)
            freq[x] = freq.get(x, 0) + 1
        
        out.append(str(ans))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution relies on a single pass per test case. The dictionary `freq` tracks counts of previously seen numbers. For each element, we immediately query its XOR complement before updating the map, preserving the strict index ordering requirement.

A common implementation mistake is updating `freq[x]` before querying `freq[y]`, which would incorrectly count pairs where $i = j$. Another subtle issue is forgetting to reset the frequency map between test cases, which would mix counts across independent arrays.

## Worked Examples

### Example 1

Input:

```
n = 6, k = 1
a = [1, 1, 4, 5, 1, 4]
```

We track `freq` and `ans` step by step.

| x | y = x XOR k | freq[y] | ans | freq after update |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | {1:1} |
| 1 | 0 | 0 | 0 | {1:2} |
| 4 | 5 | 0 | 0 | {1:2, 4:1} |
| 5 | 4 | 1 | 1 | {1:2, 4:1, 5:1} |
| 1 | 0 | 0 | 1 | {1:3, 4:1, 5:1} |
| 4 | 5 | 1 | 2 | {1:3, 4:2, 5:1} |

Final answer is 2.

This shows how repeated values contribute multiple times through frequency accumulation rather than explicit pairing.

### Example 2

Input:

```
n = 5, k = 0
a = [2, 2, 2, 3, 3]
```

Here XOR condition reduces to equality.

| x | y | freq[y] | ans | freq |
| --- | --- | --- | --- | --- |
| 2 | 2 | 0 | 0 | {2:1} |
| 2 | 2 | 1 | 1 | {2:2} |
| 2 | 2 | 2 | 3 | {2:3} |
| 3 | 3 | 0 | 3 | {2:3, 3:1} |
| 3 | 3 | 1 | 4 | {2:3, 3:2} |

This confirms correct handling of the special case $k = 0$, where every pair of equal elements contributes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each element triggers constant-time hash operations |
| Space | $O(n)$ worst case | Frequency map stores up to all distinct values |

The total complexity over all test cases is linear in the total input size, which is at most $2 \cdot 10^5$, comfortably within limits for 2 seconds in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        freq = {}
        ans = 0
        for x in a:
            y = x ^ k
            ans += freq.get(y, 0)
            freq[x] = freq.get(x, 0) + 1
        out.append(str(ans))
    return "\n".join(out)

# sample-like test 1
assert run("1\n6 1\n1 1 4 5 1 4\n") == "2"

# sample-like test 2
assert run("1\n5 0\n2 2 2 3 3\n") == "4"

# all distinct, no pairs
assert run("1\n4 10\n1 2 3 4\n") == "0"

# all equal, k=0
assert run("1\n5 0\n7 7 7 7 7\n") == "10"

# k forces impossible matches
assert run("1\n3 1\n0 2 4\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all distinct | 0 | no accidental matching |
| all equal, k=0 | 10 | combinatorial counting correctness |
| impossible XOR | 0 | correctness under no solutions |

## Edge Cases

When all elements are identical and $k = 0$, every pair is valid. The frequency method naturally accumulates counts: the first element contributes 0, the second contributes 1, and so on, yielding $n(n-1)/2$.

When $k \neq 0$ but the array contains many repeated values, only specific complements matter. The algorithm does not assume uniqueness, so each repetition correctly multiplies contributions through `freq[y]`.

When $k = 0$, the XOR complement of each element is itself. Because we query the frequency map before incrementing, we only count previous occurrences, ensuring each pair $(i, j)$ with equal values is counted exactly once when $j$ is processed.
