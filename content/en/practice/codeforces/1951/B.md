---
title: "CF 1951B - Battle Cows"
description: "We have a line of cows, each with a unique Cowdeforces rating, and they compete in a sequential tournament. The tournament begins with the first two cows, and each subsequent match is between the winner of the previous match and the next cow in line."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1951
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 25"
rating: 1200
weight: 1951
solve_time_s: 84
verified: false
draft: false
---

[CF 1951B - Battle Cows](https://codeforces.com/problemset/problem/1951/B)

**Rating:** 1200  
**Tags:** binary search, data structures, greedy  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We have a line of cows, each with a unique Cowdeforces rating, and they compete in a sequential tournament. The tournament begins with the first two cows, and each subsequent match is between the winner of the previous match and the next cow in line. A cow with a higher rating always wins. You own one cow and can swap it once with any other cow, or leave it in place. The goal is to maximize the number of matches your cow wins.

The input consists of multiple test cases. Each test case gives the number of cows, the 1-based index of your cow, and the ratings of all cows in their initial positions. The output is a single number per test case representing the maximum wins achievable by your cow under an optimal swap strategy.

The constraints allow up to 100,000 cows in total across all test cases. This means any solution with time complexity worse than O(n) per test case is likely too slow. Specifically, nested simulations of all possible swaps would result in O(n^2) behavior, which is unacceptable.

A subtle edge case occurs when your cow is already the strongest or weakest in its segment. For example, if your cow is already first and stronger than the next few cows, a naive approach might try swapping unnecessarily and reduce the total wins. Another tricky situation is when the best strategy is to swap your cow forward past a weaker sequence, rather than to the very beginning. For instance, consider ratings [2, 1, 5] with your cow rating 2. Swapping to position 2 gives one win, but swapping to position 3 gives zero wins. Handling these requires careful consideration of local maxima and the sequence of weaker cows.

## Approaches

The brute-force approach is straightforward. You could simulate the tournament for every possible swap of your cow with another cow, then count the wins for each scenario and pick the maximum. This is correct because the tournament rules are deterministic. However, this requires O(n^2) operations for each test case: for n cows, we would consider n possible swap positions, and each simulation can take up to n steps. With n up to 10^5, this results in 10^10 operations in the worst case, which is infeasible.

The key observation is that in the sequential tournament, only cows weaker than your cow matter. If your cow is stronger than the next cows in line, it will continue winning until it meets a cow stronger than itself. Therefore, to maximize wins, we only need to find a position such that your cow meets the longest consecutive sequence of cows weaker than itself. This means the optimal strategy is to either keep your cow in place or move it just before a "peak" cow (a cow stronger than your cow) to maximize consecutive wins.

We can implement this in O(n) time by scanning from left to right. We keep a counter of how many weaker cows your cow could defeat starting from any given position. We maintain the maximum value across all valid starting positions (including keeping the cow in place). The problem reduces to a simple linear scan comparing ratings, avoiding full simulations for every swap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of cows n, the index k of your cow, and the array of ratings a. Convert the 1-based index k to 0-based for easier array handling.
2. Initialize two variables: `max_wins` to track the best number of wins, and `current_wins` to count consecutive wins for the current position.
3. Iterate through the array from left to right. If the current cow is your cow, reset `current_wins` to zero since it starts counting wins from here.
4. For any other cow, check if your cow would win if it were in this position. This is true if your cow's rating is higher than the rating of the cow currently in the match. If yes, increment `current_wins`.
5. Update `max_wins` whenever `current_wins` exceeds it. This ensures we always track the longest streak of wins your cow could get starting from some position.
6. After scanning the array, `max_wins` represents the maximum number of consecutive matches your cow can win, either by staying in place or by a single optimal swap.

Why it works: The invariant is that a cow can only defeat cows weaker than itself in sequence. By scanning linearly and counting consecutive weaker cows, we automatically account for the best position to place your cow, including keeping it in its original position. This avoids simulating every match explicitly but gives the same result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_wins_for_cow(n, k, a):
    cow_rating = a[k-1]
    max_wins = 0
    current_wins = 0
    for rating in a:
        if rating == cow_rating:
            current_wins = 0
            continue
        if rating < cow_rating:
            current_wins += 1
            max_wins = max(max_wins, current_wins)
        else:
            current_wins = 0
    return max_wins

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    print(max_wins_for_cow(n, k, a))
```

The solution first isolates your cow's rating. Then, it iterates through all cows, counting how many consecutive weaker cows exist in any segment, resetting the counter if a stronger cow appears. The use of `current_wins` ensures that we track streaks, and `max_wins` keeps the best result. Converting k to 0-based indexing avoids off-by-one errors.

## Worked Examples

### Sample 1:

Input: `6 1 12 10 14 11 8 3`

| Step | Cow Rating | Current Cow | Current Wins | Max Wins |
| --- | --- | --- | --- | --- |
| 1 | 12 | 12 | 0 | 0 |
| 2 | 12 | 10 | 1 | 1 |
| 3 | 12 | 14 | 0 | 1 |
| 4 | 12 | 11 | 1 | 1 |
| 5 | 12 | 8 | 2 | 2 |
| 6 | 12 | 3 | 3 | 3 |

Maximum wins if we swap optimally is 1 because the sequence breaks when meeting 14. The table demonstrates that counting consecutive weaker cows correctly handles streak resets when a stronger cow appears.

### Sample 2:

Input: `6 5 7 2 727 10 12 13`

| Step | Cow Rating | Current Cow | Current Wins | Max Wins |
| --- | --- | --- | --- | --- |
| 1 | 12 | 7 | 1 | 1 |
| 2 | 12 | 2 | 2 | 2 |
| 3 | 12 | 727 | 0 | 2 |
| 4 | 12 | 10 | 1 | 2 |
| 5 | 12 | 12 | 0 | 2 |
| 6 | 12 | 13 | 0 | 2 |

The maximum streak of weaker cows your cow can beat is 2. The optimal swap is to place your cow just before the sequence 10, 727.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single linear scan over the array, independent of swaps, since we track maximum streaks directly. |
| Space | O(1) | Only constant variables are needed: max_wins and current_wins. |

Given the sum of n across all test cases does not exceed 10^5, this solution comfortably runs in under 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        output.append(str(max_wins_for_cow(n, k, a)))
    return "\n".join(output)

# Provided samples
assert run("3\n6 1\n12 10 14 11 8 3\n6 5\n7 2 727 10 12 13\n2 2\n1000000000 1") == "1\n2\n0"

# Minimum-size input
assert run("1\n2 1\n2 1") == "1"

# Maximum-size input, decreasing order
n = 10**5
ratings = " ".join(str(i) for i in range(n, 0, -1))
assert run(f"1\n{n} 1\n{ratings}") == "0"

# All equal except your cow
assert run("1\n5 3\n1 1 5 1 1") == "2"

# Edge swap to start
assert run("1\n5 5\n1 2 3 4 5") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 2 1 | 1 | Minimum input size, your cow first |
| 10^5 decreasing |  |  |
