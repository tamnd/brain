---
title: "CF 105485C - \u6587\u795e\u7684\u5e8f\u5217"
description: "We are given a sequence of positive integers. In one operation, we pick two different positions i and j, and replace the value at i with the bitwise AND of the two values, ai becomes ai & aj."
date: "2026-06-23T18:22:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105485
codeforces_index: "C"
codeforces_contest_name: "2024 China Unversity of Geosciences (Wuhan) Freshman Contest"
rating: 0
weight: 105485
solve_time_s: 66
verified: true
draft: false
---

[CF 105485C - \u6587\u795e\u7684\u5e8f\u5217](https://codeforces.com/problemset/problem/105485/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of positive integers. In one operation, we pick two different positions i and j, and replace the value at i with the bitwise AND of the two values, ai becomes ai & aj. The second value is unchanged, so the operation only modifies one element, but it lets values “absorb” bits from others.

The goal is to determine whether, after performing at most n such operations, we can make every element in the array equal to zero.

The key detail is the nature of bitwise AND. A bit survives only if it is present in both operands. So applying ai & aj can only remove bits from ai, never introduce new ones. This already implies that values are monotonically non-increasing in terms of set bits.

The constraint n ≤ 3000 suggests that an O(n²) or O(n² log n) approach is potentially acceptable. Anything cubic in n would be borderline but might still pass in optimized Python depending on constants, but a clean solution should avoid it.

A subtle edge case arises when thinking locally. A naive idea is to greedily try to reduce each number independently, but this ignores that operations interfere globally. Another pitfall is assuming that if every bit appears at least twice in the array, then we can eliminate it. This is false because the structure of sharing matters, not just frequency.

For example, if we had values where each bit is present but isolated in disjoint components, naive counting would suggest success, but no sequence of AND operations can transfer that bit into a position where it can be eliminated everywhere within n steps.

The real challenge is to understand what global structure allows repeated AND operations to eventually drive every number to zero.

## Approaches

The operation ai = ai & aj has a very specific behavior: it makes ai a subset of bits of aj. Thinking in set terms, each number is a set of bits, and AND replaces one set with its intersection with another.

A brute-force approach would simulate all possible sequences of up to n operations. Each state is an array of integers, and each operation picks an ordered pair (i, j). This leads to an enormous branching factor of n² per step and depth n, so the state space explodes as (n²)ⁿ, which is completely infeasible.

To get anywhere, we need to understand what transformations are actually possible rather than enumerating sequences.

A crucial observation is to look at the global AND structure. If we compute the bitwise AND of all elements in the array, call it G, then every element always remains a superset of G in terms of bits it can preserve through intersections. However, AND operations never introduce new bits, so the only way to reach all zeros is if every bit can be eliminated through repeated intersection cascades.

The key structural insight is to interpret each bit independently. A bit position is either present or absent in each array element. An operation ai = ai & aj removes that bit from ai unless aj also has it. So a bit can only survive if it is always supported by some “carrier” element that keeps it alive during propagation steps.

This leads to a graph interpretation per bit: for a fixed bit, consider all indices where that bit is 1. We can only remove that bit from all positions if there exists a sequence of operations that eventually forces every occurrence to be intersected with a 0-holder for that bit. Since we are allowed up to n operations, we have enough flexibility to use a central pivot strategy.

The final key idea is to construct a target state: we want to accumulate enough “destructive interactions” so that every bit is eliminated everywhere. This is possible exactly when there exists a sequence of pairwise intersections that can propagate zeros across all components, which reduces to checking whether the array has at least one element that can be used as a universal reducer after enough reductions are performed.

A simpler and correct reformulation emerges: we can always propagate a value downward using AND, so the best strategy is to repeatedly collapse the array into a single value equal to the global AND of all elements, and then propagate zeros if and only if that global AND is zero. However, since operations are directional and only one side changes, we can simulate that after sufficient operations we can force all elements to become the global AND if and only if the array is connected under the relation of sharing at least one common bit chain.

This simplifies to checking whether the bitwise graph induced by elements is connected enough to allow full propagation, which in this problem resolves to a simpler necessary and sufficient condition: the bitwise AND of all elements must be zero, because otherwise there exists at least one bit that can never be eliminated from every element simultaneously.

Thus, the problem reduces to computing the global AND and checking whether it is zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n³) or worse | O(n²) | Too slow |
| Global AND Reduction Insight | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the bitwise AND of all elements in the array. This value represents the set of bits that are present in every number.

We then check whether this result is zero.

1. Read the array of n integers.
2. Initialize a variable g as the first element of the array.
3. Iterate through the rest of the array and update g = g & ai for each element.
4. After processing all elements, check whether g equals zero.
5. If g is zero, output "Yes", otherwise output "No".

The reason this works is that any bit that is present in all numbers can never be eliminated from the system. Every operation preserves that bit in at least one element that contains it, and since AND never introduces new zeros into that shared intersection globally, such a bit cannot be fully removed from all positions. Conversely, if no bit is common to all elements, then every bit appears somewhere outside any fixed intersection core, and repeated pairwise AND operations can be arranged to progressively eliminate bits across the array until all entries become zero.

The invariant is that after any sequence of operations, the bitwise AND of all elements remains equal to the original global AND. This invariant restricts the final achievable configuration: if the final state were all zeros, its global AND would be zero, so the initial global AND must also be zero. Conversely, when the global AND is zero, there is no bit that is permanently locked into every element, so complete elimination is achievable within the allowed number of operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    g = a[0]
    for x in a[1:]:
        g &= x
    
    print("Yes" if g == 0 else "No")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the reduction to computing a global bitwise AND. The only subtle point is initialization: starting from a[0] ensures correctness without introducing an identity value. The loop then folds the AND across the array.

The output condition is a strict equality check to zero, which captures whether any bit is common to all elements.

## Worked Examples

### Example 1

Input:

```
3
1 2 5
```

We compute the running AND:

| Step | Current g | Next value | New g |
| --- | --- | --- | --- |
| 1 | 1 (001) | 2 (010) | 0 (000) |
| 2 | 0 (000) | 5 (101) | 0 (000) |

Final result is 0, so output is Yes.

This demonstrates a case where no bit is shared across all elements, allowing complete elimination.

### Example 2

Input:

```
3
7 7 7
```

| Step | Current g | Next value | New g |
| --- | --- | --- | --- |
| 1 | 7 (111) | 7 (111) | 7 (111) |
| 2 | 7 (111) | 7 (111) | 7 (111) |

Final result is 7, so output is No.

This shows that when a bit is common to all elements, it is permanently preserved and prevents full zeroing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass computing bitwise AND over the array |
| Space | O(1) | Only a constant number of variables are used |

The solution easily fits within constraints since n ≤ 3000 and the operation count is linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def solve():
        n = int(input().strip())
        a = list(map(int, input().split()))
        g = a[0]
        for x in a[1:]:
            g &= x
        print("Yes" if g == 0 else "No")
    
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# provided sample
assert run("3\n1 2 5\n") == "Yes"

# all zeros achievable trivial case
assert run("1\n1\n") == "No"

# all equal non-zero
assert run("4\n7 7 7 7\n") == "No"

# mixed with zero
assert run("3\n0 1 2\n") == "Yes"

# large spread
assert run("5\n1 2 4 8 16\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 2 5 | Yes | sample behavior, no common bits |
| 4 7 7 7 7 | No | fully shared bits block success |
| 3 0 1 2 | Yes | presence of zero element |
| 5 1 2 4 8 16 | Yes | disjoint bits case |

## Edge Cases

One edge case is a single-element array. If n = 1 and the value is non-zero, no operation is possible, so the answer must be No. The algorithm handles this because the global AND equals the element itself, which is non-zero.

Another edge case is when all elements are already zero. The global AND is zero, so the answer is Yes immediately, matching the fact that no operations are needed.

A third case is when some elements are zero and others are non-zero. Since AND with zero forces bits down, the global AND becomes zero, and the algorithm correctly outputs Yes, reflecting that zero acts as a universal bit eliminator in the system.
