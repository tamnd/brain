---
title: "CF 103486A - Random Number Checker"
description: "We are given a sequence of integers and need to judge whether it looks “balanced” in terms of parity. Each number is either odd or even, and we simply count how many fall into each category."
date: "2026-07-03T06:20:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103486
codeforces_index: "A"
codeforces_contest_name: "The 15th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 103486
solve_time_s: 45
verified: true
draft: false
---

[CF 103486A - Random Number Checker](https://codeforces.com/problemset/problem/103486/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and need to judge whether it looks “balanced” in terms of parity. Each number is either odd or even, and we simply count how many fall into each category.

The rule is very strict: compute the number of odd values and the number of even values, then take their absolute difference. If that difference is at most one, the generator is considered acceptable, otherwise it is not.

The input size goes up to 100,000 numbers, so any solution that scans the array once is easily fast enough. A quadratic approach would try to compare elements in pairs or repeatedly filter the list, which would do on the order of 10¹⁰ operations in the worst case and clearly exceed limits. This immediately suggests that we only need a single pass with constant work per element.

Edge cases here are mostly about small inputs. When N equals 1, the answer is always “Good” because the counts are either (1,0) or (0,1), and the difference is exactly 1. When N equals 2, configurations like one odd and one even are good, while two of the same parity are also good because the difference is 2 minus 0 equals 2, which is not allowed. So “1 1” or “2 2” should output “Not Good”, while “1 2” should output “Good”. A careless implementation might mistakenly only check whether both parities exist, instead of comparing counts correctly.

## Approaches

The brute-force way to think about the problem is to separate the array into two groups: odds and evens, then explicitly count both groups by scanning or filtering multiple times. One could imagine iterating over all numbers, and for each element checking whether it is odd or even and incrementing counters. This is already sufficient, but if someone instead repeatedly filtered the array or recomputed counts inside nested loops, the complexity would degrade to O(N²), since each pass over the array is O(N) and it might be repeated for each element.

The key observation is that nothing depends on ordering or relationships between elements. Each number contributes independently to exactly one of two counters. Once we realize this, the problem collapses into a single linear scan where we maintain two integers: one for odd counts and one for even counts. After processing all numbers, we just compare their difference.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two counters, one for odd numbers and one for even numbers, both set to zero. This prepares us to accumulate frequencies in a single pass.
2. Iterate through each number in the array. For each value, determine its parity using the condition `value % 2 == 0`. This operation is constant time and does not depend on input size.
3. If the number is even, increment the even counter; otherwise increment the odd counter. This ensures every element contributes exactly once to the correct category.
4. After processing all numbers, compute the absolute difference between the two counters.
5. If this difference is less than or equal to 1, output “Good”. Otherwise output “Not Good”.

### Why it works

Each element in the input belongs to exactly one of two disjoint sets: odd or even. The algorithm maintains exact counts for both sets without approximation or overlap. Since every element is processed once and only once, the final counters are exact cardinalities of the two sets. The decision rule depends solely on these cardinalities, so correctness follows directly from the fact that the counts are exact and no transformation of the data is performed beyond classification.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    odd = 0
    even = 0
    
    for x in arr:
        if x % 2 == 0:
            even += 1
        else:
            odd += 1
    
    if abs(odd - even) <= 1:
        print("Good")
    else:
        print("Not Good")

if __name__ == "__main__":
    solve()
```

The implementation follows the algorithm directly. We read all values once, then maintain two counters. The parity check uses modulo 2, which is safe for all constraints since values are up to 10⁹. The final comparison uses absolute difference, ensuring symmetry between odd and even counts.

A subtle point is input parsing: we read the entire second line into a list in one call. This is safe because N is at most 10⁵, so memory usage is negligible.

## Worked Examples

### Example 1

Input:

```
5
1 2 3 4 5
```

| Step | Number | Odd | Even |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 0 |
| 2 | 2 | 1 | 1 |
| 3 | 3 | 2 | 1 |
| 4 | 4 | 2 | 2 |
| 5 | 5 | 3 | 2 |

Final odd = 3, even = 2, difference = 1, so output is “Good”.

This shows the intended balanced behavior where both categories grow almost equally.

### Example 2

Input:

```
5
1 1 3 4 5
```

| Step | Number | Odd | Even |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 0 |
| 2 | 1 | 2 | 0 |
| 3 | 3 | 3 | 0 |
| 4 | 4 | 3 | 1 |
| 5 | 5 | 4 | 1 |

Final odd = 4, even = 1, difference = 3, so output is “Not Good”.

This highlights how a skewed distribution violates the threshold even though both parities exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | We scan the array once and do constant work per element |
| Space | O(1) | Only two counters are stored regardless of input size |

The linear scan comfortably fits within the constraints for N up to 100,000, and memory usage remains constant aside from the input array.

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
assert run("5\n1 2 3 4 5\n") == "Good"
assert run("5\n1 1 3 4 5\n") == "Not Good"

# minimum size
assert run("1\n2\n") == "Good"
assert run("1\n1\n") == "Good"

# perfectly balanced
assert run("4\n1 2 3 4\n") == "Good"

# all same parity (even)
assert run("4\n2 4 6 8\n") == "Not Good"

# all same parity (odd)
assert run("5\n1 3 5 7 9\n") == "Not Good"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 even/odd | Good | single-element boundary |
| mixed small | Good | balanced condition |
| all even | Not Good | extreme imbalance |
| all odd | Not Good | extreme imbalance |

## Edge Cases

### Single element input

Input:

```
1
7
```

The algorithm initializes odd = 0, even = 0, then reads 7 which is odd, so odd becomes 1. The difference is 1, so the output is “Good”. This confirms the boundary condition where the minimum input size still satisfies the rule.

### All elements identical parity

Input:

```
6
2 4 6 8 10 12
```

Processing sets even to 6 and odd remains 0. The absolute difference is 6, which exceeds 1, so the output is “Not Good”. The algorithm correctly aggregates counts without needing any pairwise reasoning.

### Near-balanced case

Input:

```
3
1 2 3
```

Odd becomes 2 and even becomes 1. Difference is 1, so output is “Good”. This confirms that the threshold condition is inclusive and correctly handled by `<= 1`.
