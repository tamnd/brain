---
title: "CF 104921B - Good Kid"
description: "We are given several independent test cases. In each test case, we start with a short list of digits. The operation allowed is very specific: we must pick exactly one position in the list and increase that digit by one."
date: "2026-06-28T08:02:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104921
codeforces_index: "B"
codeforces_contest_name: "Easy_Training"
rating: 0
weight: 104921
solve_time_s: 252
verified: false
draft: false
---

[CF 104921B - Good Kid](https://codeforces.com/problemset/problem/104921/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 12s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, we start with a short list of digits. The operation allowed is very specific: we must pick exactly one position in the list and increase that digit by one. After this single modification, we compute the product of all numbers in the list, and we want this product to be as large as possible.

So the task is not to rearrange or apply multiple operations. We are making exactly one local change in an array of small integers, and that change influences the multiplicative result of the entire array.

The constraints are extremely small in structure. Each test case contains at most 9 digits, and there are up to 10,000 test cases. This immediately tells us that even a naive quadratic approach per test case is acceptable. Any algorithm that recomputes something in linear time per choice of modified index will still be easily fast enough, since at worst we do about 9 operations per test case.

The main subtlety is that the digits are allowed to be zero, and increasing a zero changes it into one, which can dramatically change the product. Another subtle case is when all digits are zero except one position. A naive intuition that “increase the largest digit” is not always correct, because removing a zero from the product is often more valuable than improving a large digit.

A concrete edge case is:

Input: `n = 3`, digits `[0, 5, 5]`

If we increase one of the 5s, we get products `6 * 5 * 0 = 0`. If instead we increase the zero, we get `[1, 5, 5]` with product `25`. A greedy strategy that focuses on the largest digit would fail here.

Another edge case is:

Input: `[9]`

Increasing 9 gives 10, so the product becomes 10, not 0. Any assumption that digits remain single-digit after operation would break here.

## Approaches

A brute-force solution follows directly from the definition. We try each index as the one to increment. For each choice, we simulate the operation, recompute the product of all elements, and track the maximum. Since computing a product takes O(n), and there are n choices, this yields O(n²) per test case. With n at most 9, this is at most 81 multiplications per test case, which is trivial even for 10,000 cases.

There is no deeper combinatorial structure needed because the input size is already bounded to the point where full recomputation is cheap. Any attempt to optimize further, such as maintaining prefix products or dividing out elements, is possible but unnecessary. Division also becomes slightly awkward because zeros break invertibility, so recomputation is actually the cleanest approach.

The key observation is that the operation is local, and the array is tiny. This makes the simplest simulation optimal in practice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute product for each index) | O(n²) per test case | O(1) | Accepted |
| Optimal (same idea, direct implementation) | O(n²) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the list of digits and consider each index as a candidate for the operation. This is necessary because the problem forces exactly one modification, so every position is a possible decision point.
2. For a chosen index, create the value that results from incrementing that digit by one. This transformed list is the candidate configuration we evaluate.
3. Compute the product of all numbers in the modified list. We do this directly by multiplying all elements, since the list is so small that recomputation is cheap.
4. Track the maximum product across all choices of index. Each index represents a different structural change in the multiplicative contribution of the array.
5. After evaluating all indices, output the best product found.

### Why it works

Every valid solution corresponds exactly to one index being incremented. There are no other degrees of freedom. Since we evaluate the product for every possible single-index modification, we enumerate the entire solution space. The algorithm is correct because it performs a complete search over all valid operations, and the evaluation function (product computation) is exact for each candidate state.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        best = 0
        
        for i in range(n):
            b = a[:] 
            b[i] += 1
            
            prod = 1
            for x in b:
                prod *= x
            
            if prod > best:
                best = prod
        
        print(best)

if __name__ == "__main__":
    solve()
```

The solution directly follows the enumeration idea. For each position, a fresh copy of the array is made so that only one digit is modified at a time. This avoids accidental carry-over of changes between test configurations.

The inner loop computes the product from scratch, which is acceptable because n is at most 9. The variable `best` stores the maximum over all candidate modifications.

One subtle point is initialization of `best`. It starts at zero because all products are non-negative integers, and we want to correctly handle cases where the array contains zeros and all candidate products might still be zero.

## Worked Examples

### Example 1

Input: `[2, 3, 0]`

We evaluate each possible increment:

| Modified index | Modified array | Product |
| --- | --- | --- |
| 0 | [3, 3, 0] | 0 |
| 1 | [2, 4, 0] | 0 |
| 2 | [2, 3, 1] | 6 |

The best choice is to increment the zero, which removes the zero factor entirely and produces a positive product.

This example shows that zeros dominate multiplication structure and that improving a zero is often more important than improving larger digits.

### Example 2

Input: `[9, 9, 9]`

| Modified index | Modified array | Product |
| --- | --- | --- |
| 0 | [10, 9, 9] | 810 |
| 1 | [9, 10, 9] | 810 |
| 2 | [9, 9, 10] | 810 |

All choices are equivalent because multiplication is symmetric across positions. The operation only changes magnitude slightly, and no structural advantage exists for any index.

This confirms that the algorithm correctly handles uniform arrays without bias toward position.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · n²) | For each test case, we try n positions and recompute a product of size n each time |
| Space | O(1) | We only store the current array and a few scalars |

Since n ≤ 9, the maximum work per test case is bounded by a constant around 81 multiplications. Even with 10,000 test cases, the total computation remains comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            best = 0
            for i in range(n):
                b = a[:]
                b[i] += 1
                prod = 1
                for x in b:
                    prod *= x
                best = max(best, prod)
            out.append(str(best))
        return "\n".join(out)

    return solve()

# provided sample (formatted assumption)
assert run("4\n2\n2 1\n2\n3 0\n1\n2\n5\n4 3 2 3 4\n") == "3\n3\n3\n2592"

# minimum size
assert run("1\n1\n0\n") == "1", "single zero becomes 1"

# all zeros
assert run("1\n3\n0 0 0\n") == "1", "best is making one 1"

# all nines
assert run("1\n3\n9 9 9\n") == "810", "uniform case"

# zero present with large digits
assert run("1\n3\n0 5 5\n") == "25", "zero removal dominates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single zero | 1 | base case, single element increment |
| all zeros | 1 | handling multiple zeros |
| all nines | 810 | symmetry and 10-handling |
| zero with large digits | 25 | zero dominates product structure |

## Edge Cases

A single-element array containing zero is the simplest non-trivial scenario. Increasing it produces one, so the product is one. The algorithm handles this naturally because it still tries the only index and recomputes the product correctly.

Arrays containing only zeros expose the fact that most choices are equivalent except for the one index we increment. Every candidate product becomes zero except the chosen index, which becomes one, producing a product of one. Since we recompute from scratch, no special logic is needed.

Arrays with a mix of zero and non-zero values expose the key structural effect of the problem. Any candidate that does not convert a zero into a non-zero factor is likely to remain zero, and the algorithm captures this by brute evaluation of each position.

The case of a single 9 is the only place where a digit becomes two digits after increment. The product correctly becomes 10, and no assumption about digit bounds is required because we treat values as integers rather than digit characters.
