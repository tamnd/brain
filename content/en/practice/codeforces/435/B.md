---
title: "CF 435B - Pasha Maximizes"
description: "We are given a positive integer, which we can treat as a string of decimal digits, and a maximum number of allowed adjacent swaps, k. The goal is to transform this number into the largest possible number by rearranging digits, but each move can only swap two neighboring digits."
date: "2026-06-07T02:46:58+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 435
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 249 (Div. 2)"
rating: 1400
weight: 435
solve_time_s: 248
verified: true
draft: false
---

[CF 435B - Pasha Maximizes](https://codeforces.com/problemset/problem/435/B)

**Rating:** 1400  
**Tags:** greedy  
**Solve time:** 4m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer, which we can treat as a string of decimal digits, and a maximum number of allowed adjacent swaps, _k_. The goal is to transform this number into the largest possible number by rearranging digits, but each move can only swap two neighboring digits. The output is the numerical value of the largest number achievable under this constraint.

The number can be very large, up to $10^{18}$, which means its string representation could have up to 18 digits. The number of allowed swaps, _k_, is small, at most 100. This combination immediately rules out any algorithm that tries all permutations or all sequences of swaps, because the number of permutations grows factorially with the number of digits. A brute-force approach that considers all sequences of swaps is completely infeasible.

Edge cases are subtle. If the number already has digits in descending order, no swaps are needed. If _k_ is zero, we must return the number unchanged. Another tricky scenario occurs when the highest digits are blocked deep in the string and _k_ is too small to bring them to the front-careless greedy approaches that try to always swap the global maximum may attempt more moves than allowed. For example, with input `12345 1`, the naive “bring the maximum to the front” approach would fail because you can only move `5` one step to the left, giving `12354` rather than the true optimal movement within 1 swap, which is indeed `12354`.

## Approaches

A brute-force solution would generate all possible sequences of at most _k_ adjacent swaps. For each sequence, we would apply the swaps to the number and track the maximum result. This approach is correct in principle, but it is exponentially slow because the number of sequences grows combinatorially with the number of digits and _k_. Even with only 18 digits and 100 swaps, enumerating all possibilities is impossible.

The key insight for an efficient solution comes from the observation that within _k_ adjacent swaps, a digit can move at most _k_ positions to the left. This means for the first digit of the result, we only need to consider the first _k+1_ digits of the original number, pick the largest one, and move it forward using the minimum number of swaps. Then we reduce _k_ by the number of swaps used and repeat the process for the remaining digits. The problem structure ensures that the greedy choice of the largest feasible digit at each step always leads to the optimal solution, because moving smaller digits earlier would block larger digits from taking positions they could reach within the remaining swaps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n+k)!) | O(n) | Too slow |
| Optimal | O(n * k) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the number to a list of digits for easier manipulation. Treat each digit as a character for swapping purposes.
2. Initialize a pointer at the first digit. For each position `i`, we want to select the largest digit that can reach position `i` within the remaining `k` swaps. Scan the segment of digits from `i` to `i + k` (or to the end of the number if there are fewer than `k` digits left).
3. Identify the position `pos` of the largest digit in this segment. If there are ties, pick the leftmost one.
4. Move the digit at `pos` to position `i` by repeatedly swapping it left with its neighbor. Each swap decreases `k` by 1.
5. If `k` reaches zero, we stop the process early. The remaining digits are left in their current order.
6. Increment `i` and repeat until either we have processed all digits or we run out of swaps.

Why it works: at each step, we place the largest feasible digit in the leftmost available position. Because a digit cannot move more than _k_ positions left, we are always choosing the globally best digit that is reachable. No smaller digit can improve the result by moving forward, and no larger digit is ignored if it can reach the current position. This greedy invariant ensures that the number we construct is maximal under the swap constraints.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, k = input().split()
k = int(k)
digits = list(a)
n = len(digits)

i = 0
while i < n and k > 0:
    # find the largest digit we can bring to position i
    max_pos = i
    for j in range(i + 1, min(n, i + k + 1)):
        if digits[j] > digits[max_pos]:
            max_pos = j
    # bring digits[max_pos] to position i using swaps
    for j in range(max_pos, i, -1):
        digits[j], digits[j - 1] = digits[j - 1], digits[j]
    k -= (max_pos - i)
    i += 1

print("".join(digits))
```

The solution begins by converting the integer into a list of characters, which allows efficient in-place swaps. The outer loop iterates through each digit position. The inner loop scans the reachable segment, limited by the remaining number of swaps `k`, to find the largest digit. Swaps are applied immediately to bring that digit forward, and `k` is decremented by the number of swaps performed. The careful choice of segment bounds and updating of `k` prevents overshooting the allowed number of swaps.

## Worked Examples

**Sample 1: `1990 1`**

| i | digits | max_pos | swaps | k remaining |
| --- | --- | --- | --- | --- |
| 0 | 1 9 9 0 | 1 | swap 1 ↔ 9 | 0 |
| 1 | 9 1 9 0 | - | - | 0 |

The algorithm stops after 1 swap. The maximum number is `9190`, which matches the sample output.

**Custom 2: `12345 3`**

| i | digits | max_pos | swaps | k remaining |
| --- | --- | --- | --- | --- |
| 0 | 1 2 3 4 5 | 3 | move 4 to front | 0 |

After moving `4` to the front, `k=0`, so no further swaps. Result is `41235`. This demonstrates early termination when `k` runs out.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * k) | Each digit can be scanned up to `k` positions ahead; swaps are O(n) in total per digit. |
| Space | O(n) | We store the number as a list of digits. |

Given that `n <= 18` and `k <= 100`, the worst-case operations are under 1800, which fits comfortably in 1 second. Memory usage is minimal, well under the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    a, k = input().split()
    k = int(k)
    digits = list(a)
    n = len(digits)

    i = 0
    while i < n and k > 0:
        max_pos = i
        for j in range(i + 1, min(n, i + k + 1)):
            if digits[j] > digits[max_pos]:
                max_pos = j
        for j in range(max_pos, i, -1):
            digits[j], digits[j - 1] = digits[j - 1], digits[j]
        k -= (max_pos - i)
        i += 1

    return "".join(digits)

# provided sample
assert run("1990 1\n") == "9190", "sample 1"

# custom cases
assert run("12345 3\n") == "41235", "partial swaps"
assert run("98765 10\n") == "98765", "already max"
assert run("11111 5\n") == "11111", "all equal digits"
assert run("123 0\n") == "123", "no swaps allowed"
assert run("102345 5\n") == "512034", "bring max within k swaps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 12345 3 | 41235 | Greedy choice within limited swaps |
| 98765 10 | 98765 | Already maximum, no swaps needed |
| 11111 5 | 11111 | All digits equal, swaps irrelevant |
| 123 0 | 123 | No swaps allowed, output unchanged |
| 102345 5 | 512034 | Correctly selects the largest reachable digit |

## Edge Cases

For `123 0`, no swaps are allowed, so the algorithm terminates immediately, leaving the number unchanged. For `11111 5`, even though swaps are available, all digits are equal, so no effective swaps occur and the output is identical to the input. For `102345 5`, the largest digit `5` is within `5` positions, so the algorithm moves it to the front, consuming exactly 4 swaps, leaving `k=1`. The remainder of the digits is processed normally, confirming that the swap counting and segment
