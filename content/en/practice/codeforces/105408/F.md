---
title: "CF 105408F - Fair Toy Missing"
description: "We are given two small collections of integers representing toys bought from a fair. The first collection has exactly five values, and the second collection has four values."
date: "2026-06-23T04:45:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105408
codeforces_index: "F"
codeforces_contest_name: "2024 ICPC Gran Premio de Mexico Repechaje"
rating: 0
weight: 105408
solve_time_s: 70
verified: false
draft: false
---

[CF 105408F - Fair Toy Missing](https://codeforces.com/problemset/problem/105408/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two small collections of integers representing toys bought from a fair. The first collection has exactly five values, and the second collection has four values. Both collections originally come from the same fixed “complete set” of five distinct toys, but one value is missing from Bob’s version.

The task is to recover that missing integer, meaning we must find the value that appears in Alice’s list but does not appear in Bob’s list.

Although the input size is constant and tiny, the problem is essentially about detecting a single discrepancy between two multisets, where one is guaranteed to be exactly the other minus one element.

Since the input size is fixed at 9 integers total, any algorithm from constant time up to trivial sorting is fast enough. Even an O(n²) comparison would be acceptable, but the structure strongly suggests a simpler arithmetic or hashing-based solution.

A few edge cases still matter conceptually. If all numbers except one are identical, for example Alice has `1 1 1 1 2` and Bob has `1 1 1 1`, then the missing value is the only non-repeated element. If all numbers are distinct, like `10 20 30 40 50` and Bob has four of them, the missing value is the one absent from Bob’s set. A naive approach that assumes sorted alignment without checking membership can fail if the lists are not ordered.

## Approaches

A straightforward brute-force approach is to take each element from Alice’s list and check whether it exists in Bob’s list. If it does not exist, that element is the answer.

This works because Alice’s list is exactly Bob’s list plus one extra element. The brute-force check for each candidate requires scanning Bob’s four elements, so the total work is 5 × 4 comparisons, which is constant but conceptually O(n²). In this particular problem size it is still trivial, but if the lists were larger this repeated membership checking would become expensive.

A more efficient and cleaner observation is that we are comparing two multisets where one is missing exactly one element. This naturally suggests either set difference or arithmetic aggregation. Since all values are integers and we are guaranteed exactly one missing element, summing both lists gives a direct way to isolate it: the difference between the sum of Alice’s toys and the sum of Bob’s toys is exactly the missing toy.

This avoids any searching or data structure overhead and reduces the problem to a single pass over both lists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(5 × 4) | O(1) | Accepted |
| Optimal (sum difference) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We use the sum-difference idea.

1. Read the five integers from Alice’s bag and compute their total sum. This represents the complete set total.
2. Read the four integers from Bob’s bag and compute their total sum. This represents the incomplete set total.
3. Subtract Bob’s sum from Alice’s sum. The result is the missing toy value.
4. Output this difference.

Each step relies on the fact that addition is associative and commutative, so the order of values does not matter. This allows us to compress the entire structure of the input into a single scalar per list.

### Why it works

Both bags contain the same multiset of five distinct integers except that Bob’s bag is missing exactly one element. When we sum Alice’s values, we get the sum of all five unique toys. When we sum Bob’s values, we get the sum of the same five toys minus one. Subtracting the two sums cancels all shared elements, leaving exactly the missing value. Since no other discrepancy exists, the result cannot be anything else.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    print(sum(a) - sum(b))

if __name__ == "__main__":
    main()
```

The solution reads two lines and converts them into integer lists. The key computation is the subtraction of sums. There are no loops beyond the implicit linear parsing of input, and no edge-case handling is needed beyond correct parsing of whitespace-separated integers.

A subtle point is ensuring both lines are read completely and independently. Since the problem guarantees exactly five and four integers per line, `split()` is safe and no additional validation is required.

## Worked Examples

### Example 1

Input:

```
1 2 3 4 5
2 4 5 1
```

| Step | Alice List | Bob List | Alice Sum | Bob Sum | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | [1,2,3,4,5] | [] | 0 | 0 | - |
| 2 | [1,2,3,4,5] | [2,4,5,1] | 15 | 12 | 3 |

The difference between sums isolates the missing value 3, since all other elements cancel out between the two lists.

### Example 2

Input:

```
10 14 22 32 1
10 14 22 32
```

| Step | Alice List | Bob List | Alice Sum | Bob Sum | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | [10,14,22,32,1] | [] | 0 | 0 | - |
| 2 | [10,14,22,32,1] | [10,14,22,32] | 79 | 78 | 1 |

This confirms that even when the missing value is small or large, the arithmetic cancellation still isolates it cleanly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only fixed-size inputs are processed (5 and 4 integers) |
| Space | O(1) | Only a constant number of integers are stored |

The constraints are extremely small, so the solution is far below any practical limits. Even a significantly slower algorithm would pass, but the sum-difference approach is minimal and robust.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    return str(sum(a) - sum(b))

# provided samples
assert run("1 2 3 4 5\n2 4 5 1\n") == "3", "sample 1"
assert run("10 14 22 32 1\n10 14 22 32\n") == "1", "sample 2"

# custom cases
assert run("1 2 3 4 5\n1 2 3 4\n") == "5", "missing largest"
assert run("5 4 3 2 1\n4 3 2 1\n") == "5", "reverse order"
assert run("7 7 7 7 8\n7 7 7 7\n") == "8", "duplicate structure"
assert run("100 1 50 25 75\n100 50 25 75\n") == "1", "mixed ordering"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 3 4 5 / 1 2 3 4 | 5 | missing last element |
| 5 4 3 2 1 / 4 3 2 1 | 5 | order independence |
| 7 7 7 7 8 / 7 7 7 7 | 8 | repeated values |
| 100 1 50 25 75 / 100 50 25 75 | 1 | mixed ordering |

## Edge Cases

A subtle case is when values repeat, even though the statement guarantees distinctness. If we consider a relaxed version, say Alice has `7 7 7 7 8` and Bob has `7 7 7 7`, the sum-difference still correctly returns `8`. Each repeated value cancels exactly as many times as it appears in both lists, leaving only the unmatched contribution.

Another case is ordering. For `10 14 22 32 1` and `32 22 10 14`, Bob’s input arrives shuffled, but since summation is order-independent, the result remains stable. The algorithm never relies on positional correspondence, so permutation differences have no effect on correctness.
