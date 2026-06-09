---
title: "CF 1635A - Min Or Sum"
description: "We are given several arrays, each containing small non-negative integers. For each array, we are allowed to repeatedly pick two different positions and replace both values with new numbers, as long as the bitwise OR of the chosen pair stays unchanged after the replacement."
date: "2026-06-10T04:40:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1635
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 772 (Div. 2)"
rating: 800
weight: 1635
solve_time_s: 69
verified: true
draft: false
---

[CF 1635A - Min Or Sum](https://codeforces.com/problemset/problem/1635/A)

**Rating:** 800  
**Tags:** bitmasks, greedy  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several arrays, each containing small non-negative integers. For each array, we are allowed to repeatedly pick two different positions and replace both values with new numbers, as long as the bitwise OR of the chosen pair stays unchanged after the replacement. The goal is to make the sum of the array as small as possible after any number of such operations.

The key object here is the bitwise OR across the whole array. Every operation preserves the OR of the chosen pair, and since every element can participate in operations repeatedly, the global OR of the array never changes. That means the final array must still have the same overall OR as the original input.

The constraints are small: each test case has at most 100 elements, and values are bounded by less than 2^30. This strongly suggests that any O(n^2) or O(n * 30) solution per test case is easily fast enough, and we should focus on bitwise reasoning rather than simulation of operations.

A subtle pitfall is assuming we can freely redistribute bits independently across elements. For example, one might think we can always concentrate bits into a single element and zero out others. This is not always consistent with the OR preservation rule unless we respect how bits can be split across multiple numbers while maintaining pairwise constraints during operations.

A second edge case is arrays with a single dominant element containing all bits. In such cases, no reduction is possible, and the answer remains the same as the sum.

## Approaches

A brute-force interpretation would try to simulate all valid operations, repeatedly picking pairs and redistributing bits in all possible ways that preserve OR. This quickly becomes intractable because each operation introduces many possible states, and the number of sequences of operations grows exponentially. Even with only 100 elements, the state space explodes.

The key observation is that the only invariant that truly matters is the bitwise OR of the entire array. Let that OR be denoted as S. No matter what operations we perform, S stays fixed.

Now consider what the final array must look like. Each element contributes some subset of bits, and the union of all these subsets must equal S. The sum is minimized when we avoid duplicating bits across multiple elements, because any repeated bit increases the sum unnecessarily. The optimal configuration is to ensure that each bit set in S appears in exactly one element, and no element carries redundant bits beyond that structure.

This leads to a strong simplification: we want to distribute the bits of S across elements while respecting that each element must be derived from original values through allowed operations. The optimal achievable structure turns out to be that we can always reduce the array to having exactly one element equal to S, and all other elements equal to 0, except in cases where original values already constrain minimal redistribution. However, a more careful reasoning shows an even simpler fact: the minimum achievable sum is the sum of all elements after replacing each element with the OR of the entire array, but distributed minimally, which collapses to a greedy bit contribution argument.

A cleaner and standard derivation is the following: each bit contributes independently. For each bit, if it appears in k elements, it can be reduced so that only one element keeps that bit while others drop it to zero, without changing global OR feasibility. Thus, each bit contributes exactly its value once to the final sum. Since overlapping bits do not multiply cost, the optimal sum becomes simply the value of the OR plus contributions already unavoidable from structure, which simplifies to:

The answer is the sum of all elements minus something that depends on overlaps, but more directly and correctly known from this problem: the minimal sum is equal to the OR of all elements plus the sum of all elements with redundant contributions removed, which simplifies further to the sum of elements after repeatedly merging any pair by replacing them with their bitwise OR split optimally. The well-known result is that the optimal strategy is to repeatedly merge elements so that the final multiset becomes one element equal to the global OR, and all others zero, yielding answer equal to OR + sum of remaining zeros, which is OR.

But since zeros must still account for distribution constraints, the correct invariant simplifies to: the answer equals the sum of elements after replacing all but one element by zero while keeping total OR unchanged, which evaluates to total sum minus sum of minimal representation, and this resolves to sum(a) with optimal bit consolidation giving final answer equal to sum of all elements minus sum of duplicated bit savings, which is equivalent to sum(a) when no merging helps, but strictly reduces to sum of individual bit contributions once overlaps are removed.

A more precise and implementable observation is that every operation effectively allows us to transfer bits between two numbers without changing their OR, which means we can combine all bits into one element, and all others become zero. The final minimal sum is therefore exactly the OR of the entire array.

Thus the problem reduces to computing the bitwise OR of all elements.

### Comparison Table

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force State Simulation | Exponential | Exponential | Too slow |
| Bitwise OR aggregation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array and compute the bitwise OR of all elements. This captures all bits that must exist in any valid final configuration because no operation can introduce or remove bits globally.
2. Maintain a running variable `result` initialized to 0, and for each element update `result |= a[i]`. This ensures every bit present in any element is preserved.
3. After processing the full array, output `result` as the answer for that test case.

### Why it works

The crucial property is that the OR of the entire array is invariant under the allowed operation. Any replacement of two numbers keeps their pairwise OR unchanged, so no bit that appears anywhere can disappear from the global OR. Conversely, every valid final configuration must still cover exactly those bits. Since minimizing the sum under these constraints is equivalent to concentrating all necessary bits without duplication, the best achievable outcome corresponds to representing all required bits once, which is exactly the global OR value.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    
    res = 0
    for x in arr:
        res |= x
    
    print(res)
```

The code processes each test case independently. The loop over elements accumulates the bitwise OR, which is the only value that matters for the final answer. There are no edge cases in implementation beyond ensuring fast input handling, since all values fit comfortably within Python integers.

## Worked Examples

### Example 1

Input:

```
3
1 3 2
```

We track the OR accumulation.

| Step | Element | Current OR |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 3 | 3 |
| 3 | 2 | 3 |

Final answer is 3.

This shows how overlapping bits are merged into a single representative value.

### Example 2

Input:

```
5
1 2 4 8 16
```

| Step | Element | Current OR |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 2 | 3 |
| 3 | 4 | 7 |
| 4 | 8 | 15 |
| 5 | 16 | 31 |

Final answer is 31.

This confirms that when bits are disjoint, the OR accumulates all contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once with a bitwise OR operation |
| Space | O(1) | Only a single accumulator is used |

The constraints allow up to 1000 test cases with arrays of size up to 100, so a linear scan per test case is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        res = 0
        for x in arr:
            res |= x
        output.append(str(res))
    return "\n".join(output)

# provided samples
assert run("""4
3
1 3 2
5
1 2 4 8 16
2
6 6
3
3 5 6
""") == """3
31
6
7"""

# all equal
assert run("""1
4
7 7 7 7
""") == "7"

# minimum size
assert run("""1
2
1 2
""") == "3"

# single bit chain
assert run("""1
5
1 1 1 1 1
""") == "1"

# mixed bits
assert run("""1
3
2 4 6
""") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 7 7 7 7 | 7 | redundancy and identical values |
| 1 2 | 3 | smallest valid array size |
| 1 1 1 1 1 | 1 | repeated identical elements |
| 2 4 6 | 6 | overlapping bit patterns |

## Edge Cases

A key edge case is when all numbers are identical. For example, `[7, 7, 7]` has OR equal to 7. The algorithm correctly outputs 7, and no operations can reduce it further because any redistribution still preserves the same bit structure.

Another case is when values are pairwise disjoint in bits, such as `[1, 2, 4, 8]`. The OR accumulates to 15, and the algorithm outputs 15. This matches the intuition that no merging can reduce total bit cost because each element contributes a unique bit.

A final case is minimal size arrays like `[a, b]`. The OR of both is always correct, and since no operation can reduce below preserving OR, the answer is simply `a | b`.
