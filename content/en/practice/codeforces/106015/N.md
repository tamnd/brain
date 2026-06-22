---
title: "CF 106015N - The Squirrel's Scattered Nuts"
description: "We are given a collection of integers, each representing the “energy” of a nut. The task is to choose two distinct nuts such that the sum of their energies is odd, and among all such valid pairs, return the maximum possible sum. If no pair produces an odd sum, the answer is −1."
date: "2026-06-22T16:48:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106015
codeforces_index: "N"
codeforces_contest_name: "Game of Coders 4 - Over the Garden Wall"
rating: 0
weight: 106015
solve_time_s: 47
verified: true
draft: false
---

[CF 106015N - The Squirrel's Scattered Nuts](https://codeforces.com/problemset/problem/106015/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of integers, each representing the “energy” of a nut. The task is to choose two distinct nuts such that the sum of their energies is odd, and among all such valid pairs, return the maximum possible sum. If no pair produces an odd sum, the answer is −1.

The output depends entirely on pairing behavior, not on ordering or positions. We are effectively working with a multiset of values and must reason about which two elements can be combined to satisfy a parity constraint while maximizing the resulting sum.

The constraints allow up to 200,000 values, each up to 200,000. This immediately rules out any quadratic approach that explicitly checks all pairs, since that would require about 4 × 10¹⁰ operations in the worst case, far beyond a 1 second limit. We need a solution that processes the array in linear or near-linear time.

A subtle edge case arises when all numbers share the same parity. If all values are even, every sum is even. If all are odd, every sum is also even. In both cases, no valid pair exists.

For example, input `2 4 6` produces no odd sum pairs, so the answer is −1. A naive approach might still attempt to compute a maximum pair sum and mistakenly return 10.

Another edge case occurs when only one odd or one even exists. For instance, `1 2 4 6` has only one odd element, so no valid odd-sum pair can be formed even though large values exist.

## Approaches

A brute-force solution tries every pair (i, j) and checks whether Ai + Aj is odd. This is straightforward: for each pair, compute the sum and update the best answer if the sum is odd. The correctness is obvious because it enumerates all possibilities.

The issue is scale. With N up to 200,000, the number of pairs is about N(N−1)/2, which is roughly 2 × 10¹⁰ operations in the worst case. This cannot run within the time limit.

The key observation comes from parity structure. A sum is odd if and only if one number is even and the other is odd. This reduces the problem from “all pairs” to “cross-parity pairs only.” Among all valid pairs, the maximum sum is achieved by taking the largest even value and the largest odd value.

This transforms the problem into a simple scan: track the maximum even and maximum odd element, then compute their sum if both exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Optimal | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We proceed by extracting the structure imposed by parity and reducing the search space to two candidates.

1. Scan through the array once while maintaining two variables: the maximum even value seen so far and the maximum odd value seen so far. We initialize both as absent, for example using a sentinel like −1.
2. For each number Ai, determine its parity. If Ai is even, compare it with the current best even value and update it if Ai is larger. If Ai is odd, do the same for the odd tracker. This ensures we always retain the best possible candidate in each parity class.
3. After processing all values, check whether both a maximum even and a maximum odd value exist. If either is missing, no valid pair can form an odd sum, so the answer is −1.
4. If both exist, compute their sum. This is the only structure that guarantees oddness, since even + odd is the only way to produce an odd result.

The choice of only keeping maxima is justified because any valid solution must pair one odd and one even, and maximizing the sum independently within each parity group yields the best possible pair.

### Why it works

At any moment, the algorithm preserves the largest seen even number and the largest seen odd number. Any valid odd-sum pair must consist of one element from each parity class. Replacing either element in such a pair with a larger value of the same parity can only increase the sum. Therefore, the optimal pair is formed by the maximum even and maximum odd values in the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    
    max_even = -1
    max_odd = -1
    
    for x in arr:
        if x % 2 == 0:
            if x > max_even:
                max_even = x
        else:
            if x > max_odd:
                max_odd = x
    
    if max_even == -1 or max_odd == -1:
        print(-1)
    else:
        print(max_even + max_odd)

if __name__ == "__main__":
    solve()
```

The implementation maintains two running maxima while scanning the input once. The sentinel value −1 works safely because all inputs are at least 1, so it cannot be confused with a valid array value.

A common mistake is attempting to track only the sum without separating parity classes. That fails because it ignores the structural constraint that odd sums require opposite parity.

## Worked Examples

### Example 1

Input: `1 2 3 4`

We track maximum even and odd values step by step.

| Element | Parity | max_even | max_odd |
| --- | --- | --- | --- |
| 1 | odd | -1 | 1 |
| 2 | even | 2 | 1 |
| 3 | odd | 2 | 3 |
| 4 | even | 4 | 3 |

Final maximum even is 4 and maximum odd is 3, so answer is 7.

This demonstrates that intermediate values do not matter beyond their role in updating the best candidates.

### Example 2

Input: `2 4 6 8`

| Element | Parity | max_even | max_odd |
| --- | --- | --- | --- |
| 2 | even | 2 | -1 |
| 4 | even | 4 | -1 |
| 6 | even | 6 | -1 |
| 8 | even | 8 | -1 |

No odd values exist, so no valid pair can be formed and the output is −1.

This confirms the correctness of the feasibility check.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | single pass through the array, constant work per element |
| Space | O(1) | only two integer variables are maintained |

The solution fits easily within constraints since even the maximum input size requires only 200,000 operations.

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

# provided sample-style cases
assert run("4\n1 2 3 4\n") == "7"
assert run("4\n2 4 6 8\n") == "-1"

# minimum size
assert run("2\n1 2\n") == "3"

# all odds
assert run("5\n1 3 5 7 9\n") == "-1"

# large mixed
assert run("6\n10 20 1 3 7 8\n") == "28"

# duplicate max parity values
assert run("5\n2 2 2 1 100\n") == "101"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4, 1 2 3 4 | 7 | normal mixed parity selection |
| 4, 2 4 6 8 | -1 | no odd-sum pair exists |
| 2, 1 2 | 3 | minimum valid input |
| all odds | -1 | parity-only invalid case |
| mixed large | 28 | correct max selection across distribution |
| duplicates | 101 | handling repeated maxima correctly |

## Edge Cases

One edge case is when the array contains only even numbers. For input `6\n2 4 6 8 10 12`, the scan sets max_even to 12 while max_odd remains −1 throughout. At the end, the algorithm correctly outputs −1 because no cross-parity pairing is possible.

Another edge case is when there is exactly one element of a parity class. For input `4\n100 2 3 4`, max_even becomes 100 and max_odd becomes 3. The algorithm still works because having a single odd or even is sufficient as long as the other class exists.

A third case is when the largest even and largest odd appear late in the array. For input `5\n1 8 3 6 7`, the running maxima evolve until max_even = 8 and max_odd = 7 at the end. The final answer 15 confirms that order does not affect correctness, only the maxima matter.
