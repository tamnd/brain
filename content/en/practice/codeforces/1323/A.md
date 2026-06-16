---
title: "CF 1323A - Even Subset Sum Problem"
description: "We are given several independent arrays of positive integers. For each array, we must select a non-empty group of positions such that the sum of the chosen values is even. If no such group exists, we report failure."
date: "2026-06-16T07:23:18+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1323
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 626 (Div. 2, based on Moscow Open Olympiad in Informatics)"
rating: 800
weight: 1323
solve_time_s: 228
verified: true
draft: false
---

[CF 1323A - Even Subset Sum Problem](https://codeforces.com/problemset/problem/1323/A)

**Rating:** 800  
**Tags:** brute force, dp, greedy, implementation  
**Solve time:** 3m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent arrays of positive integers. For each array, we must select a non-empty group of positions such that the sum of the chosen values is even. If no such group exists, we report failure.

The output is not the subset itself but the indices of elements forming a valid subset. Any valid choice is acceptable, so we are not optimizing size or lexicographic order, only feasibility.

The constraints are small: at most 100 test cases, each array has at most 100 elements. This immediately tells us that even a cubic or quadratic approach over subsets is feasible in the worst case. However, since parity is the only property that matters, we should expect a much simpler structure than enumerating subsets.

The key edge cases come from very small arrays. If there is a single element, then the only subset has sum equal to that element, so the answer depends entirely on whether that number is even. If there are two elements, odd-even interactions become relevant: a single even element already solves the problem, while two odd elements also form an even sum.

A subtle failure case for naive thinking is assuming that whenever there is at least one odd and one even number, we must take both. That is unnecessary, since a single even element already gives a valid answer. Another pitfall is assuming that if all numbers are odd and there are more than two, a solution always exists; in fact, we need an even count of odd numbers to get an even sum.

## Approaches

A brute-force solution would enumerate all subsets and check whether their sum is even. There are $2^n - 1$ non-empty subsets, and for each we compute a sum in $O(n)$, giving $O(n 2^n)$ per test case. With $n = 100$, this is completely infeasible, as it exceeds astronomical limits.

The structure of the problem simplifies dramatically if we observe how parity behaves. The sum of integers depends only on how many odd elements are included. Even numbers do not affect parity at all, while each odd number flips the parity of the sum.

This means we never need more than a few elements. If there is an even number, we can take it alone. Otherwise, we look for pairs of odd numbers, since two odds sum to an even number. If there is exactly one odd number and no even numbers, no solution exists.

So the problem reduces to scanning the array once and remembering positions of evens and odds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot 2^n)$ | $O(n)$ | Too slow |
| Parity observation | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Scan the array once and record the index of any even element.

If we find an even number, we can immediately stop scanning further because a single even element already forms a valid subset. This is optimal because it guarantees minimal subset size and correctness.
2. If no even element exists, collect indices of all odd elements.

This step is necessary because odd elements cannot individually produce an even sum, but pairs of them can.
3. If we have at least two odd elements, output the first two indices.

Their sum is odd plus odd, which is even, so the subset condition is satisfied.
4. If we have fewer than two odd elements and no even elements, output -1.

The only remaining case is a single odd element, which cannot form an even sum in any non-empty subset.

### Why it works

Parity of a sum depends only on the parity of included elements. Even numbers contribute zero to parity, while each odd number flips it. Therefore, the sum is even exactly when the number of selected odd elements is even. The algorithm constructs either one even element (zero odd elements) or two odd elements (two is even), covering all feasible cases. No other structure is required because any larger subset can always be reduced to one of these canonical forms without changing feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        even_idx = -1
        odd_indices = []

        for i, x in enumerate(a, 1):
            if x % 2 == 0:
                even_idx = i
            else:
                odd_indices.append(i)

        if even_idx != -1:
            print(1)
            print(even_idx)
        elif len(odd_indices) >= 2:
            print(2)
            print(odd_indices[0], odd_indices[1])
        else:
            print(-1)

if __name__ == "__main__":
    solve()
```

The solution first checks for an even element because that immediately gives a size-1 valid subset. If none exists, it falls back to the only remaining constructive case: pairing odd elements. The enumeration is 1-based because the problem requires indices starting from 1.

A common implementation mistake is continuing the scan after finding an even element and accidentally overwriting or complicating the logic. Another is forgetting that only indices are required, not values.

## Worked Examples

We trace two cases: one where a single even element exists, and one where only odd elements exist.

### Example 1

Input: `[1, 4, 3]`

| Step | Current element | Even index | Odd list |
| --- | --- | --- | --- |
| 1 | 1 | -1 | [1] |
| 2 | 4 | 2 | [1] |
| 3 | 3 | 2 | [1, 3] |

We stop after finding 4 and output index 2. The trace shows that once an even number appears, later elements do not matter.

### Example 2

Input: `[3, 5, 7]`

| Step | Current element | Even index | Odd list |
| --- | --- | --- | --- |
| 1 | 3 | -1 | [1] |
| 2 | 5 | -1 | [1, 2] |
| 3 | 7 | -1 | [1, 2, 3] |

No even element exists, so we use the first two odd indices, 1 and 2. This confirms that any two odd numbers suffice regardless of their values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | single linear scan of the array |
| Space | $O(1)$ auxiliary | only storing a few indices |

The total work over all test cases is at most 10,000 elements, which is comfortably within limits. Memory usage is constant apart from input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        even_idx = -1
        odd = []

        for i, x in enumerate(a, 1):
            if x % 2 == 0:
                even_idx = i
            else:
                odd.append(i)

        if even_idx != -1:
            output.append("1")
            output.append(str(even_idx))
        elif len(odd) >= 2:
            output.append("2")
            output.append(f"{odd[0]} {odd[1]}")
        else:
            output.append("-1")

    return "\n".join(output)

# provided samples
assert run("""3
3
1 4 3
1
15
2
3 5
""") == """1
2
-1
2
1 2"""

# all even single
assert run("""1
1
2
""") == "1\n1"

# single odd
assert run("""1
1
3
""") == "-1"

# two odds
assert run("""1
2
1 7
""") == "2\n1 2"

# mixed case
assert run("""1
4
1 2 3 5
""") in ["1\n2", "1\n4"]  # any even index valid
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single even | 1 1 | minimal valid subset |
| single odd | -1 | impossibility case |
| two odds | 2 indices | pairing logic |
| mixed array | even index | early termination correctness |

## Edge Cases

A critical edge case is when the array contains exactly one element. If that element is even, the answer is that index; if it is odd, there is no solution. The algorithm handles this naturally because it either sets `even_idx` or collects a single odd index and fails the second condition.

Another edge case is when multiple even elements exist. The algorithm returns the last seen even index, which is still valid because any single even element suffices. No dependency on ordering exists.

A third case is when all elements are odd but their count is large. The algorithm still only picks the first two indices, which works because two odd numbers already guarantee an even sum, regardless of total count.
