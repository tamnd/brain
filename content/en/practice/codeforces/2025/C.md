---
title: "CF 2025C - New Game"
description: "The game revolves around a deck of cards, each labeled with an integer. Monocarp can start by taking any card. On subsequent turns, he can only take a card that either has the same number as the last card taken or is exactly one greater."
date: "2026-06-09T03:18:10+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "implementation", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2025
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 170 (Rated for Div. 2)"
rating: 1300
weight: 2025
solve_time_s: 304
verified: false
draft: false
---

[CF 2025C - New Game](https://codeforces.com/problemset/problem/2025/C)

**Rating:** 1300  
**Tags:** binary search, brute force, greedy, implementation, sortings, two pointers  
**Solve time:** 5m 4s  
**Verified:** no  

## Solution
## Problem Understanding

The game revolves around a deck of cards, each labeled with an integer. Monocarp can start by taking any card. On subsequent turns, he can only take a card that either has the same number as the last card taken or is exactly one greater. Additionally, the total number of distinct numbers Monocarp collects cannot exceed `k`. The goal is to maximize the total number of cards taken before no more valid moves remain.

The input provides multiple test cases. Each test case gives the number of cards `n`, the maximum allowed distinct numbers `k`, and the sequence of integers on the cards. The output should be a single integer per test case representing the maximum number of cards Monocarp can collect under the rules.

Given that `n` can reach 200,000 and the sum of `n` over all test cases is limited to 200,000, any solution must run in roughly O(n log n) or better for each test case to stay within the 2-second time limit. A naive approach that tries all possible card sequences would be factorial in complexity and clearly infeasible.

Subtle edge cases include sequences with large gaps in numbers, repeated values, or situations where `k` is smaller than the number of unique numbers. For example, with input `n=5, k=1, a=[1,3,1,3,2]`, a naive greedy approach that always chooses the first available card might incorrectly attempt to pick a `2` or `3` too early, violating the distinct number constraint. The correct output is `2` because Monocarp can only take cards with `1` in this scenario.

## Approaches

A brute-force approach would try every starting card and simulate the game, attempting all valid sequences of card choices until no moves remain. This approach is correct in principle, but in the worst case with `n=200,000`, the number of sequences is astronomical, making it computationally impossible.

The key observation is that the only numbers that matter are the unique integers present on the cards. Since Monocarp can only move from a number `x` to `x` or `x+1`, the optimal strategy will involve taking consecutive numbers in ascending order without skipping, as skipping would prevent later inclusion of cards. We can thus reduce the problem to counting the longest contiguous segment of numbers in the sorted set of unique values, where the segment length does not exceed `k`. Once the segment is identified, summing the counts of all numbers in this segment gives the maximum number of cards Monocarp can take.

The optimal solution sorts the unique numbers and counts how many consecutive numbers can fit in a window of length `k`. Using a dictionary to track frequencies allows O(1) access to card counts. Sliding a window over the sorted unique numbers lets us efficiently calculate the sum for all candidate segments. This reduces the complexity to O(n log n) due to sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the occurrences of each number using a dictionary. This lets us know how many cards we can take for each number without scanning the list repeatedly.
2. Extract the unique numbers and sort them. Sorting is required because Monocarp can only move to the same number or the next consecutive number. Sorting lets us consider consecutive sequences efficiently.
3. Use a two-pointer or sliding window approach on the sorted unique numbers. The window represents a candidate sequence of distinct numbers that Monocarp can take. Start both pointers at the beginning of the sorted array.
4. Expand the right pointer while the number of distinct values in the window does not exceed `k` and the numbers are consecutive. Keep a running sum of the total cards for numbers inside the window.
5. If the window violates the constraints (either too many distinct numbers or a gap in consecutive numbers), shrink the left pointer until the window is valid again, adjusting the running sum accordingly.
6. Track the maximum sum observed during this process. This sum represents the maximum number of cards Monocarp can take.
7. Print the maximum sum for each test case.

Why it works: At any point, the sliding window contains a maximal sequence of consecutive numbers where the number of distinct numbers does not exceed `k`. By summing the counts in this window, we ensure Monocarp takes all cards that are valid under the rules. The sliding window explores all possible valid starting points efficiently, guaranteeing the global maximum is found.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        count = Counter(a)
        unique_sorted = sorted(count.keys())

        max_cards = 0
        left = 0
        current_sum = 0

        for right in range(len(unique_sorted)):
            if right > 0 and unique_sorted[right] != unique_sorted[right - 1] + 1:
                # reset window if numbers are not consecutive
                left = right
                current_sum = 0
            current_sum += count[unique_sorted[right]]

            # shrink window if too many distinct numbers
            while right - left + 1 > k:
                current_sum -= count[unique_sorted[left]]
                left += 1

            max_cards = max(max_cards, current_sum)

        print(max_cards)

if __name__ == "__main__":
    solve()
```

The code begins by reading the number of test cases. For each case, it counts occurrences, sorts unique numbers, and then uses a sliding window to identify the optimal contiguous segment of numbers. The window resets if a gap is detected because non-consecutive numbers cannot be taken without violating the rules. Shrinking the window ensures we never exceed the allowed number of distinct numbers. `max_cards` stores the best solution found.

## Worked Examples

### Example 1

Input: `10 2 5 2 4 3 4 3 4 5 3 2`

| right | left | current_sum | max_cards |
| --- | --- | --- | --- |
| 0 | 0 | 2 | 2 |
| 1 | 0 | 5 | 5 |
| 2 | 0 | 6 | 6 |
| 3 | 1 | 6 | 6 |

Window represents numbers `[3,4]` with counts `[3,3]` giving sum 6.

### Example 2

Input: `5 1 10 11 10 11 10`

| right | left | current_sum | max_cards |
| --- | --- | --- | --- |
| 0 | 0 | 3 | 3 |
| 1 | 1 | 2 | 3 |

Window `[10]` yields maximum sum 3.

These traces confirm the sliding window correctly captures sequences of consecutive numbers while respecting the `k` distinct number limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Counting is O(n), sorting unique numbers is O(n log n), sliding window is O(n) |
| Space | O(n) | Counter stores counts, sorted list stores up to n unique numbers |

Given `n` ≤ 200,000 and total sum over test cases ≤ 200,000, this approach easily fits within the 2-second time limit and 512 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("4\n10 2\n5 2 4 3 4 3 4 5 3 2\n5 1\n10 11 10 11 10\n9 3\n4 5 4 4 6 5 4 4 6\n3 2\n1 3 1\n") == "6\n3\n9\n2", "Sample tests"

# Custom test cases
assert run("1\n1 1\n100\n") == "1", "Single card"
assert run("1\n5 2\n1 2 3 4 5\n") == "4", "k smaller than total consecutive numbers"
assert run("1\n6 3\n5 5 5 5 5 5\n") == "6", "All equal cards"
assert run("1\n5 2\n1 3 5 7 9\n") == "1", "Non-consecutive numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1 1\n100\n` | 1 | Minimum-size input |
| `1\n5 2\n1 2 3 4 5\n` | 4 | k smaller than total consecutive numbers |
| `1\n6 3\n5 5 5 5 5 5\n` | 6 | All cards equal |
| `1\n5 2\n1 3 5 7 9\n` | 1 | Non-consecutive numbers break sequence |

## Edge Cases

For `n=5, k=1, a=[1,3,1,3,2]`, the sorted unique numbers are `[1,2,3]`. Starting with `1`, the window `[1]`
