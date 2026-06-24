---
title: "CF 105408F - Fair Toy Missing"
description: "We are given two small collections of toy identifiers. Alice’s bag contains five toys, and Bob’s bag is supposed to contain exactly the same set of toys but one item is missing, so his bag has only four."
date: "2026-06-24T23:08:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105408
codeforces_index: "F"
codeforces_contest_name: "2024 ICPC Gran Premio de Mexico Repechaje"
rating: 0
weight: 105408
solve_time_s: 63
verified: false
draft: false
---

[CF 105408F - Fair Toy Missing](https://codeforces.com/problemset/problem/105408/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two small collections of toy identifiers. Alice’s bag contains five toys, and Bob’s bag is supposed to contain exactly the same set of toys but one item is missing, so his bag has only four. Every toy is represented by an integer, and all values in Alice’s list are guaranteed to appear in Bob’s list except for exactly one.

The task is to determine which integer appears in Alice’s list but does not appear in Bob’s list.

The input size is tiny, only five and four numbers. That immediately removes any concern about performance constraints. Any solution that even scans the data multiple times will comfortably fit within time limits, so the problem is entirely about extracting the correct logical relationship between the two multisets.

A few edge situations are worth keeping in mind. One is when the missing toy is the smallest or largest value in the set, for example Alice has `1 2 3 4 5` and Bob has `2 3 4 5`, where the answer is `1`. Another is when values are not sorted or are interleaved, for example Alice has `10 14 22 32 110` and Bob has `14 22 32 110`, where the missing value is `10`. A careless approach that assumes ordering or tries to match positions would fail immediately because there is no guarantee of sorted input or alignment between positions.

## Approaches

A direct but inefficient way to solve the problem is to take each element from Alice’s list and check whether it exists in Bob’s list using a linear scan. For each of the five elements, we may scan up to four elements in Bob’s list. This leads to a constant number of operations, roughly 20 comparisons, which is already small. Even though this brute-force idea is logically correct, it becomes unnecessary to structure it as repeated search.

The cleaner perspective comes from noticing that we are comparing two almost identical multisets where only one value differs in frequency. Instead of searching for the missing element explicitly, we can compare aggregate structure. One simple invariant is that the sum of all elements in Alice’s bag exceeds the sum of Bob’s bag exactly by the missing toy’s value. This works because all common elements cancel out in the subtraction.

Another equivalent viewpoint is using XOR. Since identical values cancel under XOR, XORing all elements of Alice’s bag with all elements of Bob’s bag leaves only the missing value. Both approaches rely on the same cancellation principle, but summation is more immediately intuitive in this constrained setting.

The key reduction is moving from membership checking to aggregation comparison. Once we accept that all shared elements disappear under subtraction or XOR, the problem collapses into a single arithmetic operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Search | O(5 × 4) | O(1) | Accepted but unnecessary |
| Sum Difference | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We use the sum difference method because it is the most direct interpretation of the cancellation idea.

1. Read the five integers from Alice’s bag and compute their sum. This sum represents the total weight of all intended toys.
2. Read the four integers from Bob’s bag and compute their sum. This sum represents the reduced total after one missing item.
3. Subtract Bob’s sum from Alice’s sum. The result of this subtraction isolates exactly the missing toy value.
4. Output the computed difference.

The reason subtraction works here is that every shared toy appears exactly once in both sums and therefore cancels out perfectly.

### Why it works

Let the full set be A and Bob’s set be B. B is identical to A except that one value x is removed. When we compute sum(A) − sum(B), every shared element contributes equally to both sums and disappears in subtraction. Only x remains uncancelled, so the result must equal x. Since the problem guarantees exactly one missing element and no extra modifications, this invariant holds deterministically.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    return str(sum(a) - sum(b))

if __name__ == "__main__":
    print(solve())
```

The solution reads both lines, converts them into integer lists, and computes their sums. The subtraction step is the core of the logic, directly implementing the cancellation argument described earlier. The output is returned as a string for clean printing.

A subtle implementation detail is ensuring that input is split correctly even if spacing is irregular. Using `split()` handles all whitespace uniformly, so there is no risk of parsing errors.

## Worked Examples

### Example 1

Input:

`1 2 3 4 5`

`2 4 5 1`

| Step | Alice Sum | Bob Sum | Difference |
| --- | --- | --- | --- |
| After reading input | 15 | 12 | 3 |

The difference is `3`, which matches the missing value. This confirms that all shared elements cancel cleanly regardless of order.

### Example 2

Input:

`10 14 22 32 110`

`14 22 32 110`

| Step | Alice Sum | Bob Sum | Difference |
| --- | --- | --- | --- |
| After reading input | 188 | 178 | 10 |

The result is `10`, which is exactly the value absent from Bob’s list. This example demonstrates that the method does not rely on ordering or adjacency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only fixed-size lists of length 5 and 4 are processed |
| Space | O(1) | No additional data structures beyond a few variables |

The computation is constant work, so it easily satisfies the constraints even under repeated execution.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

def solve():
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    return str(sum(a) - sum(b))

# provided samples
assert run("1 2 3 4 5\n2 4 5 1\n") == "3", "sample 1"
assert run("10 14 22 32 110\n14 22 32 110\n") == "10", "sample 2"

# custom cases
assert run("1 1 1 1 1\n1 1 1 1\n") == "1", "all equal values"
assert run("100 2 3 4 5\n2 3 4 5\n") == "100", "missing largest"
assert run("1 2 3 4 5\n1 2 3 4\n") == "5", "missing last element"
assert run("7 8 9 10 11\n8 9 10 11\n") == "7", "missing first element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| All equal values | 1 | cancellation still isolates repeated value |
| Missing largest | 100 | works when answer is max element |
| Missing last element | 5 | positional independence |
| Missing first element | 7 | no ordering assumptions |

## Edge Cases

One edge case is when all values except the missing one are identical. For input like `1 1 1 1 1` and `1 1 1 1`, the subtraction still isolates the missing `1` correctly because four copies cancel and one remains.

Another case is when the missing value is the smallest or largest number. For `100 2 3 4 5` with Bob having `2 3 4 5`, the sum difference produces `100` directly because extremes do not affect cancellation behavior.

A final case is arbitrary ordering, such as `7 8 9 10 11` and `8 9 10 11`. Even though the missing value is at the start of the input, positional structure is irrelevant since only aggregate sums matter, and the subtraction still yields `7` without any dependency on arrangement.
