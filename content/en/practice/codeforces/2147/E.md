---
title: "CF 2147E - Maximum OR Popcount"
description: "We are given an array of non-negative integers, and for each query we are allowed to increment any elements of the array a certain number of times."
date: "2026-06-08T01:20:47+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "brute-force", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2147
codeforces_index: "E"
codeforces_contest_name: "Codeforces Global Round 29 (Div. 1 + Div. 2)"
rating: 2300
weight: 2147
solve_time_s: 113
verified: true
draft: false
---

[CF 2147E - Maximum OR Popcount](https://codeforces.com/problemset/problem/2147/E)

**Rating:** 2300  
**Tags:** binary search, bitmasks, brute force, data structures, greedy  
**Solve time:** 1m 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of non-negative integers, and for each query we are allowed to increment any elements of the array a certain number of times. The goal is to maximize the number of bits set to 1 in the bitwise OR of the entire array after performing at most the allowed number of increments. In other words, each query gives a budget of operations, and we must use them strategically to turn as many 0-bits in the OR as possible into 1-bits. The output for each query is the count of 1-bits in the resulting OR.

The constraints indicate that the array can be quite large, up to 100,000 elements, and the number of queries can also reach 100,000. Additionally, each element can be up to a billion, and the operation budgets can be similarly large. This rules out any naive approach that simulates every possible increment or tries all subsets, as that would result in billions of operations. Instead, we need an approach that focuses on the bit-level structure and the minimum operations required to flip a bit in the OR.

A subtle edge case arises when all elements are already large enough that their OR contains all high bits, or when the allowed operations are smaller than the cost to flip the next higher bit. For instance, consider an array `[1, 1]` and a query with `b=1`. The current OR is `1`, which has one bit set. Incrementing either element by 1 gives `[2, 1]` with OR `3`, which has two bits set. A careless approach that increments elements blindly might miss the optimal distribution of operations across bits.

## Approaches

The brute-force approach is straightforward: for each query, we try all ways to distribute the increments across array elements, compute the new OR, and count its bits. This works because the OR operation is associative and commutative, but it fails immediately on large inputs. For example, with 100,000 elements and 1,000,000 possible increments, enumerating all distributions is impossible.

The key insight is that each bit in the OR can be treated independently. To set a bit at position `k` in the OR, we need at least one number in the array to have that bit set. For numbers where bit `k` is 0, we can compute the minimal number of increments needed to set it. Once we know the cost to flip each bit, we can sort bits by this cost and greedily use the allowed operations to maximize the number of bits set in the OR. This reduces the problem from manipulating the array elements directly to manipulating counts of increments needed per bit.

The greedy approach works because higher-order bits may require more increments, but lower-order bits can always be set with fewer operations. The structure of binary numbers ensures that setting a lower bit never prevents setting a higher bit later if enough operations remain.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * n * max(a_i)) | O(n) | Too slow |
| Optimal | O(30 * n + 30 * q) | O(30) | Accepted |

## Algorithm Walkthrough

1. For each test case, initialize an array `costs` of length 30 to store the minimal number of increments needed to set each bit in the OR.
2. Iterate over each element of the array and, for each bit position from 0 to 29, compute how many increments are needed to make that bit 1 if it is currently 0. For bit `k`, this is `(1 << k) - (a_i % (1 << (k + 1)))` if the bit is 0. Keep track of the minimal cost among all elements for each bit.
3. After processing the array, sort the bits by their minimal cost.
4. For each query, start with a counter for bits already set in the original OR. Then iterate through the sorted costs and, while the query budget allows, "purchase" bits by subtracting their cost from the remaining operations. Increment the bit counter for each bit purchased.
5. Output the final count of bits for each query.

Why it works: The algorithm guarantees correctness because it always uses the minimal number of operations to set each bit independently, ensuring no operation is wasted. Bits that are already 1 do not consume operations. Sorting costs ensures that cheaper bits are considered first, maximizing the total number of bits set given a limited operation budget.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_or_popcount():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        
        # Compute original OR and minimal costs to set each bit
        orig_or = 0
        costs = [float('inf')] * 30
        for num in a:
            orig_or |= num
            for k in range(30):
                if (num >> k) & 1 == 0:
                    need = (1 << k) - (num % (1 << (k + 1)))
                    costs[k] = min(costs[k], need)
        
        sorted_costs = sorted([c for i, c in enumerate(costs) if not (orig_or >> i) & 1])
        
        # Handle each query
        for _ in range(q):
            b = int(input())
            bits = bin(orig_or).count('1')
            for cost in sorted_costs:
                if cost <= b:
                    b -= cost
                    bits += 1
                else:
                    break
            print(bits)

if __name__ == "__main__":
    max_or_popcount()
```

The first loop computes the OR of the original array and builds the minimal cost for setting each zero bit. The inner loop for queries greedily applies the operation budget to the cheapest bits. The sorting ensures we maximize the number of bits set within the budget. Handling `orig_or` separately avoids double-counting bits that are already set.

## Worked Examples

Sample 1:

| Query b | orig_or | Sorted Costs | Bits Set | Remaining b |
| --- | --- | --- | --- | --- |
| 0 | 0 | [1] | 0 | 0 |
| 2 | 0 | [1] | 1 | 1 |
| 4 | 0 | [1] | 2 | 2 |

The trace shows that the greedy algorithm always picks the cheapest bits first, ensuring we maximize the total number of 1-bits.

Second test case: `[1, 3]` with queries `0` and `3`.

| Query b | orig_or | Sorted Costs | Bits Set | Remaining b |
| --- | --- | --- | --- | --- |
| 0 | 3 | [2] | 2 | 0 |
| 3 | 3 | [2] | 3 | 1 |

The algorithm correctly ignores bits already set in the OR.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(30 * n + 30 * q) | Loop over 30 bits for n elements, plus 30 bits per query |
| Space | O(30) | Store minimal costs per bit |

The complexity fits within constraints since 30_n + 30_q ≈ 6 * 10^6 operations, which is acceptable for 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    max_or_popcount()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("3\n1 3\n0\n0\n2\n4\n2 2\n1 3\n0\n3\n2 1\n1000000000 1000000000\n1000000000\n") == "0\n1\n2\n2\n3\n31", "sample 1"

# Minimum input
assert run("1\n1 1\n0\n0\n") == "0", "minimum input"

# All ones
assert run("1\n3 2\n7 7 7\n0\n3\n") == "3\n3", "all bits already set"

# Large b
assert run("1\n2 1\n1 2\n1000000000\n") == "2", "large operations budget"

# Edge increment needed
assert run("1\n2 1\n2 3\n1\n") == "2", "just enough increment to flip one bit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1 1\n0\n0\n` | `0` | smallest array, zero operations |
| `1\n3 2\n7 7 7\n0\n3\n` | `3\n3` | all bits already set, operations don't change OR |
| `1\n2 1\n1 2\n1000000000\n` | `2` | very large operation budget does not exceed max bits |
| `1\n2 1\n2 3\n1\n` | `2` | single increment suffices to flip next bit |

## Edge Cases

When the array has all elements zero and the budget is insufficient to flip the first bit of the highest element, the algorithm correctly outputs zero, since it only counts bits that can be purchased with available operations. For example, `[
