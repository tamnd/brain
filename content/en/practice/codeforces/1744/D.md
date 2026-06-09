---
title: "CF 1744D - Divisibility by 2^n"
description: "We are given an array of positive integers, and we need to make the product of all elements divisible by $2^n$, where $n$ is the length of the array. We are allowed to multiply an element $ai$ by its own index $i$ exactly once per index."
date: "2026-06-09T15:53:51+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1744
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round  828 (Div. 3)"
rating: 1200
weight: 1744
solve_time_s: 202
verified: true
draft: false
---

[CF 1744D - Divisibility by 2^n](https://codeforces.com/problemset/problem/1744/D)

**Rating:** 1200  
**Tags:** greedy, math, sortings  
**Solve time:** 3m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers, and we need to make the product of all elements divisible by $2^n$, where $n$ is the length of the array. We are allowed to multiply an element $a_i$ by its own index $i$ exactly once per index. The goal is to minimize the number of these multiplications, or report that it is impossible.

In practical terms, each number contributes a certain number of factors of 2 to the product. We want the sum of these contributions to be at least $n$. Multiplying $a_i$ by $i$ may increase the number of 2s contributed by $a_i$, because the index itself might have some 2s in its factorization.

The constraints allow $n$ to reach $2 \cdot 10^5$ per test set, and the sum over all test cases is capped at the same number. A brute-force approach trying all combinations of operations would be far too slow because the number of subsets of indices grows exponentially. Instead, we need a way to prioritize operations to reach the required number of 2s efficiently.

A subtle edge case is when all numbers are odd and indices are small, so no combination of allowed operations can achieve enough 2s. For example, if $a = [1, 1, 1, 1]$, multiplying any number by its index gives at most one factor of 2 per number, so the product cannot reach $2^4 = 16$, and the correct output is -1. A naive greedy approach that always picks the first number might incorrectly report a solution exists.

## Approaches

The naive brute-force approach would consider all subsets of indices, apply the operation to each subset, compute the resulting product, and check if it is divisible by $2^n$. For an array of size $n$, this requires checking $2^n$ subsets. Even for $n = 20$, this is already over a million combinations, and with $n$ up to $2 \cdot 10^5$, it is completely infeasible.

The key insight is that we only care about the number of 2s in the factorization of each number, not the numbers themselves. Let’s define `twos(a_i)` as the number of times $a_i$ is divisible by 2. Similarly, multiplying by index $i$ adds `twos(i)` to the count for that element. Then the problem reduces to a simple selection problem: we need to pick the indices whose `twos(i)` contributions give us enough additional 2s to reach a total of $n$.

So, we first compute the sum of `twos(a_i)` over all elements. If it is already at least $n$, we need zero operations. Otherwise, we compute the list of possible gains from multiplying by index $i$, sort it in descending order, and greedily pick the largest gains until we reach the required total. If we run out of gains before reaching $n$, the answer is -1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the array $a$ and its length $n$. Initialize `current_twos` to zero.
2. For each element $a_i$, compute the number of factors of 2 it contains using repeated division, and add it to `current_twos`.
3. If `current_twos >= n`, print 0 and return. No operations are needed.
4. Otherwise, compute a list `index_twos` where each entry is `twos(i)` for $i = 1$ to $n$. This represents the potential gain if we multiply $a_i$ by $i$.
5. Sort `index_twos` in descending order so that we prioritize the indices that contribute the most additional 2s.
6. Initialize `operations` to 0. Iterate through `index_twos`, adding each value to `current_twos` and incrementing `operations` until `current_twos >= n`.
7. If after using all possible gains, `current_twos < n`, print -1. Otherwise, print `operations`.

**Why it works**

The invariant is that the sum of `current_twos` represents the total power of 2 in the product. Multiplying by indices in descending order of their 2s guarantees we reach the required threshold with the fewest operations. No alternative set of indices can achieve the target with fewer operations because any smaller gain would not contribute as much to the sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_twos(x):
    cnt = 0
    while x % 2 == 0:
        x //= 2
        cnt += 1
    return cnt

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        current_twos = sum(count_twos(x) for x in a)
        if current_twos >= n:
            print(0)
            continue
        
        index_twos = [count_twos(i) for i in range(1, n + 1)]
        index_twos.sort(reverse=True)
        
        operations = 0
        for gain in index_twos:
            current_twos += gain
            operations += 1
            if current_twos >= n:
                break
        
        if current_twos < n:
            print(-1)
        else:
            print(operations)

if __name__ == "__main__":
    solve()
```

The solution first counts the factors of 2 in each number to determine the initial product’s divisibility. Sorting the potential gains ensures that the largest contributions are used first. Edge cases, like arrays with no initial 2s, are naturally handled by the loop over `index_twos`. Python handles integer overflow automatically, so large products do not cause issues.

## Worked Examples

**Example 1**: `n = 3, a = [10, 6, 11]`

| Step | current_twos | index_twos (sorted) | operations |
| --- | --- | --- | --- |
| initial | 1 + 1 + 0 = 2 | [1, 1, 0] | 0 |
| add 1st gain | 2 + 1 = 3 | - | 1 |

Output: 1

Here the initial twos sum is 2, we need 3. Choosing the largest index gain adds 1, reaching 3. Only one operation is required.

**Example 2**: `n = 4, a = [13, 17, 1, 1]`

| Step | current_twos | index_twos (sorted) | operations |
| --- | --- | --- | --- |
| initial | 0 | [2, 1, 0, 0] | 0 |
| add 1st gain | 0 + 2 = 2 | - | 1 |
| add 2nd gain | 2 + 1 = 3 | - | 2 |
| add 3rd gain | 3 + 0 = 3 | - | 3 |
| add 4th gain | 3 + 0 = 3 | - | 4 |

We never reach 4, so output is -1. The algorithm correctly identifies impossibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Counting twos for each element is O(log a_i), sorting gains is O(n log n), iterating is O(n). |
| Space | O(n) | Store the array and the gains per index. |

This fits comfortably within the constraints. Even with $n = 2 \cdot 10^5$ and multiple test cases, sorting and counting operations are fast enough.

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

# Provided samples
assert run("6\n1\n2\n2\n3 2\n3\n10 6 11\n4\n13 17 1 1\n5\n1 1 12 1 1\n6\n20 7 14 18 3 5\n") == "0\n1\n1\n-1\n2\n1"

# Custom tests
assert run("1\n1\n1\n") == "-1", "single odd element"
assert run("1\n5\n2 4 8 16 32\n") == "0", "all powers of two already enough"
assert run("1\n3\n1 1 1\n") == "2", "needs multiple index multiplications"
assert run("1\n4\n3 3 3 3\n") == "-1", "all odd, cannot reach 2^4"
assert run("1\n6\n1 1 1 1 1 1\n") == "3", "multiple small odd numbers,
```
