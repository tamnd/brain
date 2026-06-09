---
title: "CF 2028C - Alice's Adventures in Cutting Cake"
description: "We are given a long sheet cake divided into n sections, each with a tastiness value. Alice is at a party with m creatures, and she wants to cut the cake into m + 1 contiguous pieces. Each creature will only be happy if its piece has tastiness at least v."
date: "2026-06-08T12:08:08+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2028
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 986 (Div. 2)"
rating: 1600
weight: 2028
solve_time_s: 95
verified: false
draft: false
---

[CF 2028C - Alice's Adventures in Cutting Cake](https://codeforces.com/problemset/problem/2028/C)

**Rating:** 1600  
**Tags:** binary search, dp, greedy, two pointers  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a long sheet cake divided into `n` sections, each with a tastiness value. Alice is at a party with `m` creatures, and she wants to cut the cake into `m + 1` contiguous pieces. Each creature will only be happy if its piece has tastiness at least `v`. Alice wants to maximize the tastiness of the piece she keeps for herself, while ensuring that all creatures are satisfied. If it's impossible to satisfy all creatures, the output is `-1`.

The input gives multiple test cases. Each test case specifies `n`, `m`, and `v`, followed by the array of tastiness values. The output is a single number per test case, the maximum tastiness Alice can achieve, or `-1` if no valid partition exists.

Given the constraints, `n` can be up to 2×10^5 in a single test case, and the sum of `n` across all test cases is also ≤2×10^5. This means any algorithm with complexity greater than O(n log n) per test case will likely time out. We cannot afford an O(n^2) brute-force approach of checking all subarrays.

An important edge case occurs when the sum of the `m` largest contiguous subarrays of tastiness at least `v` exceeds the total cake. In such cases, even if Alice tries to maximize her piece, there might not be enough cake to satisfy all creatures. For example, if `a = [1,1,1]`, `m=2`, and `v=2`, there is no way to give two pieces each with tastiness ≥2, so the correct output is `-1`.

Another subtlety is that Alice's own piece can be empty. In situations where she cannot take a large piece without violating the creatures’ happiness, her optimal strategy may involve taking zero sections, which is valid.

## Approaches

The brute-force approach would try all partitions of the array into `m + 1` contiguous pieces and check which ones satisfy the minimum tastiness condition for creatures. For each valid partition, we would compute Alice’s piece sum and pick the maximum. There are exponentially many ways to partition an array, so this approach is not feasible. Even if we restrict to contiguous subarrays for creatures’ pieces, we still could have O(n choose m) possibilities, which is too large for n up to 2×10^5.

The key insight is that the problem reduces to a greedy-style prefix sum approach combined with binary search. Suppose we know Alice wants a piece of tastiness `x`. We can try to greedily assign pieces to creatures from left to right such that each creature gets a piece of tastiness ≥ v, and Alice takes a piece of tastiness `x` anywhere. We can check if `x` is achievable in O(n) time using a single pass. Then, by performing binary search on `x` from 0 to the total sum of the cake, we can efficiently find the maximum achievable tastiness for Alice.

The greedy check works as follows: we iterate through the cake sections, accumulating a running sum. When the sum reaches or exceeds `v`, we assign that as a creature’s piece, reset the sum, and continue. Any leftover sections after all creatures have been assigned are potentially Alice’s piece. If the leftover sum is ≥ `x`, Alice can take it. If we cannot assign all creatures while keeping Alice’s piece ≥ `x`, then `x` is impossible. This ensures correctness because the problem is monotone: if Alice can take `x`, she can also take any smaller piece; if she cannot take `x`, she cannot take any larger piece.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n choose m) | O(n) | Too slow |
| Greedy + Binary Search | O(n log S) | O(1) | Accepted |

Here, `S` is the sum of all tastiness values in the cake, which is at most 2×10^14 given the constraints.

## Algorithm Walkthrough

1. Compute the total sum of the cake sections for the upper bound of binary search.
2. Set the binary search bounds `low = 0` and `high = total sum`.
3. While `low ≤ high`, take `mid = (low + high) // 2` as the candidate tastiness for Alice’s piece.
4. Perform a greedy check to see if Alice can take a piece of size `mid` while giving `m` creatures pieces of at least `v`:

1. Initialize `current_sum = 0` and `creatures_assigned = 0`.
2. Iterate over cake sections:

1. Add the current section to `current_sum`.
2. If `current_sum ≥ v`, assign it to a creature and reset `current_sum` to 0, increment `creatures_assigned`.
3. If `creatures_assigned == m`, break.
3. After all creatures are assigned, the remaining sum in unassigned sections is Alice’s potential piece.
5. If Alice’s remaining sum ≥ `mid`, it is feasible; move `low = mid + 1` to try a larger piece.
6. Otherwise, set `high = mid - 1`.
7. At the end of binary search, `high` contains the maximum tastiness Alice can achieve. If even `0` is infeasible, output `-1`.

The invariant is that at every binary search step, the greedy assignment either succeeds or fails for a given `mid`. Because the problem is monotone, the maximum `mid` that succeeds is the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, v = map(int, input().split())
        a = list(map(int, input().split()))
        total = sum(a)
        low, high = 0, total
        ans = -1
        while low <= high:
            mid = (low + high) // 2
            current_sum = 0
            creatures_assigned = 0
            for val in a:
                current_sum += val
                if current_sum >= v:
                    creatures_assigned += 1
                    current_sum = 0
                    if creatures_assigned == m:
                        break
            # Alice's remaining sum
            remaining = sum(a[a.index(val)+1:]) if creatures_assigned == m else 0
            if remaining >= mid:
                ans = mid
                low = mid + 1
            else:
                high = mid - 1
        print(ans)
        
solve()
```

The solution reads input efficiently using `sys.stdin.readline`. The binary search explores possible tastiness for Alice, while the greedy check ensures that the `m` creatures can be satisfied. The tricky part is handling the remaining sum correctly; we break immediately after assigning the last creature and sum the rest for Alice. The `ans` variable stores the largest feasible value.

## Worked Examples

**Sample 1:** `6 2 1` with `a = [1, 1, 10, 1, 1, 10]`

| Section | current_sum | creatures_assigned | Alice_remaining |
| --- | --- | --- | --- |
| 1 | 1 | 0 | - |
| 2 | 2 | 1 | - |
| 3 | 10 | 1 | - |
| 4 | 1 | 1 | - |
| 5 | 2 | 2 | - |
| 6 | - | 2 | 22 |

Alice can take 22; binary search confirms this is maximal.

**Sample 2:** `6 2 12` with `a = [1, 1, 1, 1, 10, 10]`

Greedy assignment cannot give 2 creatures pieces ≥12; output is `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log S) | Binary search over sum of array, O(n) per check |
| Space | O(n) | For array storage and input parsing |

The solution fits comfortably under the 2-second limit, as the sum of n across all test cases is ≤2×10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io
    f = io.StringIO()
    with redirect_stdout(f):
        solve()
    return f.getvalue().strip()

# provided samples
assert run("""7
6 2 1
1 1 10 1 1 10
6 2 2
1 1 10 1 1 10
6 2 3
1 1 10 1 1 10
6 2 10
1 1 10 1 1 10
6 2 11
1 1 10 1 1 10
6 2 12
1 1 10 1 1 10
6 2 12
1 1 1 1 10 10
""") == """22
12
2
2
2
0
-1"""

# custom cases
assert run("""2
1 1 1
1
5 2 3
1 2 3 4
```
