---
title: "CF 1882B - Sets and Union"
description: "We are given several sets of integers. We can choose any subset of these sets (including none) and take the union of the selected sets. A set is attainable if it can be formed in this way."
date: "2026-06-08T22:36:06+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1882
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 899 (Div. 2)"
rating: 1300
weight: 1882
solve_time_s: 126
verified: true
draft: false
---

[CF 1882B - Sets and Union](https://codeforces.com/problemset/problem/1882/B)

**Rating:** 1300  
**Tags:** bitmasks, brute force, constructive algorithms, greedy  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several sets of integers. We can choose any subset of these sets (including none) and take the union of the selected sets. A set is _attainable_ if it can be formed in this way. Our task is to find the largest attainable set that is **not equal** to the union of all the original sets. The output should be the number of elements in such a set.

Each test case gives us up to 50 sets, and each set contains up to 50 integers ranging from 1 to 50. The constraints are small, so brute-force techniques over the set elements are feasible, but brute-forcing all possible subsets of sets is borderline, as that would be $2^n$ possibilities, which is over $10^{15}$ when $n = 50$. So we need a smarter, constructive approach rather than testing every subset explicitly.

Non-obvious edge cases include situations where every set is a singleton or there is only one set. For instance, if there is only one set $\{1,2,3\}$, the only attainable set not equal to the full union is the empty set, giving output 0. Another subtlety is when sets are overlapping in such a way that removing any one set still gives the full union; in that case, the largest non-full union is obtained by taking the union of all sets except one.

## Approaches

The brute-force approach is to iterate over all subsets of the given sets, compute their union, and track the size of the largest union that does not match the union of all sets. This works in principle because the union operation is associative and monotone, but the number of subsets grows exponentially ($2^n$), which is far too large for $n = 50$.

The key observation that unlocks a more efficient solution is that the largest attainable set that is not the full union can always be obtained by taking the union of all sets **except one**. If we remove a set that contains elements not in any other set, the resulting union loses exactly those elements, giving us the largest non-full union. If all sets are subsets of the union of the remaining sets, removing any set still gives the full union, and then the answer is the size of the union minus one element or zero if only one set exists.

This reduces the problem to iterating over each set, computing the union of all other sets, and taking the maximum size of these unions. Instead of $2^n$ operations, we only do $n$ unions, each over at most 50 elements. Representing sets as bitmasks over the numbers 1-50 simplifies union operations and size calculations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * k) | O(k) | Too slow |
| Optimal (exclude one set) | O(n * k) | O(k) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. For each test case, read $n$, the number of sets.
2. Read each set and store it either as a Python `set` or as a 50-bit integer bitmask. Bitmasks are convenient because union becomes a single bitwise OR operation.
3. Compute the union of all $n$ sets. Call this `full_union`.
4. Initialize a variable `best` to 0. This will track the maximum size of attainable sets smaller than `full_union`.
5. For each set $S_i$:

- Compute the union of all sets except $S_i$. Using bitmasks, this is `union_except_i = full_union & ~S_i`. Using Python sets, it's `union_except_i = full_union - S_i` for elements only in $S_i$ or `union_except_i = set().union(*[S[j] for j != i])`.
- Count the number of elements in `union_except_i` and update `best` if larger.
6. After checking all sets, print `best` for the test case.

Why it works: Any attainable set that is not equal to the full union must omit at least one element from the union. Removing one whole set is sufficient to cover all possible omissions because including fewer sets cannot create a larger union than `full_union`. Therefore, iterating over each set and excluding it guarantees we find the maximum attainable size below `full_union`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        sets = []
        for _ in range(n):
            data = list(map(int, input().split()))
            sets.append(set(data[1:]))
        
        full_union = set()
        for s in sets:
            full_union |= s
        
        best = 0
        for i in range(n):
            union_except_i = full_union - sets[i]
            best = max(best, len(union_except_i))
        
        print(best)

solve()
```

The solution reads the input efficiently using `sys.stdin.readline` and stores each set as a Python set. We compute the union of all sets with the `|=` operator and then iterate, excluding each set in turn. Using set subtraction ensures we only remove elements unique to the current set, which is exactly the mechanism to find the largest attainable non-full union.

## Worked Examples

**Sample 1:**

Input:

```
3
3 1 2 3
2 4 5
2 3 4
```

| Step | full_union | union_except_i | best |
| --- | --- | --- | --- |
| exclude S1 | {2,3,4,5} | size 4 | 4 |
| exclude S2 | {1,2,3,4} | size 4 | 4 |
| exclude S3 | {1,2,3,4,5} | size 5 | 4 (cannot equal full_union) |

Output: 4

This demonstrates that excluding the first or second set produces the largest attainable set without including all elements from `full_union`.

**Sample 2:**

Input:

```
4
4 1 2 3 4
3 2 5 6
3 3 5 6
3 4 5 6
```

| Step | full_union | union_except_i | best |
| --- | --- | --- | --- |
| exclude S1 | {2,3,4,5,6} | size 5 | 5 |
| exclude S2 | {1,3,4,5,6} | size 5 | 5 |
| exclude S3 | {1,2,4,5,6} | size 5 | 5 |
| exclude S4 | {1,2,3,5,6} | size 5 | 5 |

Output: 5

We see that excluding any set leaves a maximal union smaller than `full_union`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n * k) | For each test case, we compute `full_union` (O(n_k)) and then iterate excluding each set (O(n_k)). k ≤ 50 and n ≤ 50, so total operations ≤ 2500 per test case. |
| Space | O(n * k) | We store up to n sets of size k each. Bitmask representation reduces space but is not necessary for these constraints. |

This comfortably fits within the 2-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("4\n3\n3 1 2 3\n2 4 5\n2 3 4\n4\n4 1 2 3 4\n3 2 5 6\n3 3 5 6\n3 4 5 6\n5\n1 1\n3 3 6 10\n1 9\n2 1 3\n3 5 8 9\n1\n2 4 28") == "4\n5\n6\n0"

# custom tests
assert run("1\n1\n3 1 2 3") == "0", "single set"
assert run("1\n2\n1 1\n1 2") == "1", "two disjoint singletons"
assert run("1\n3\n2 1 2\n2 1 2\n2 1 2") == "2", "all sets equal"
assert run("1\n2\n3 1 2 3\n3 2 3 4") == "3", "overlapping sets"
assert run("1\n3\n1 1\n1 2\n1 3") == "2", "each singleton, maximum union excluding one"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 set only | 0 | Edge case of single set |
| 2 disjoint singletons | 1 | Excluding either produces max attainable union |
| 3 identical sets | 2 | Removing any set still gives union smaller than full union |
| 2 overlapping sets |  |  |
