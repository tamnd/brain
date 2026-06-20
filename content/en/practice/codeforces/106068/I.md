---
title: "CF 106068I - The judges problem"
description: "Ten judges each pick a number between 1 and 10, representing which problem they want added to the contest. After all votes are collected, the selected problem is the one with the highest number of votes."
date: "2026-06-20T13:13:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106068
codeforces_index: "I"
codeforces_contest_name: "2025 Aleppo and Idlib Private Universities Collegiate Programming Contest (APUCPC 2025)"
rating: 0
weight: 106068
solve_time_s: 45
verified: true
draft: false
---

[CF 106068I - The judges problem](https://codeforces.com/problemset/problem/106068/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

Ten judges each pick a number between 1 and 10, representing which problem they want added to the contest. After all votes are collected, the selected problem is the one with the highest number of votes. If several problems share the same highest vote count, the decision rule prefers the largest problem number among them.

So the input is simply ten integers, each acting like a vote for one of ten candidates labeled 1 through 10. The output is the single candidate that wins under a frequency majority rule with a tie-break toward larger labels.

Although the constraints are tiny, the logic still contains a subtle detail in the tie-breaking rule. A naive implementation that only tracks the maximum frequency but forgets to enforce the “largest label wins ties” rule would produce incorrect results whenever multiple numbers are equally frequent.

For example, consider the input `1 2 2 3 3 4 4 5 5 6`. Here, numbers 2, 3, 4, and 5 all appear twice. The correct answer is 5 because it is the largest among those tied for maximum frequency. A solution that simply returns the first number reaching maximum frequency might incorrectly return 2 or 3 depending on iteration order.

Another edge case appears when all votes are identical, such as `7 7 7 7 7 7 7 7 7 7`. The output must be 7, which is straightforward but confirms that the algorithm handles uniform distributions correctly.

Since the input size is fixed at 10, any reasonable approach runs instantly. Even an O(n²) simulation would be acceptable, but the structure naturally suggests a frequency counting approach.

## Approaches

A brute-force way to solve this is to simulate counting separately for each possible candidate from 1 to 10. For each candidate, we scan all ten votes and count how many times it appears. We then track the best candidate based on highest frequency, breaking ties by choosing the larger number.

This approach works correctly because it directly evaluates every candidate independently. However, it redundantly rescans the same list for each candidate, leading to repeated work. In general, if the number of votes were large, say n, this would become O(10n), which is still fine here but conceptually inefficient and not scalable if the candidate space also grows.

The key observation is that we do not need repeated scans. A single pass is enough to compute all frequencies. Once we know the frequency of every number, selecting the best candidate becomes a simple comparison problem over a fixed set of size 10.

This reduces the problem to maintaining a small frequency table and then finding the maximum according to a custom ordering rule.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(100) | O(1) | Accepted |
| Optimal Frequency Count | O(10) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `freq` of size 11 (indices 1 to 10) filled with zeros. This array stores how many times each problem number is voted for.
2. Read the ten input values and increment the corresponding frequency for each value. Each vote directly updates the count of that candidate.
3. Initialize two variables: `best_value = 1` and `best_count = 0`. These store the current winning candidate and its frequency.
4. Iterate through all candidate numbers from 1 to 10. For each candidate, compare its frequency with the current best.
5. If the current candidate has a strictly higher frequency than `best_count`, update `best_value` and `best_count` to this candidate and its frequency.
6. If the frequency is equal to `best_count`, update `best_value` only if the current candidate number is larger. This enforces the tie-breaking rule.
7. After scanning all candidates, output `best_value`.

### Why it works

The algorithm maintains a correct summary of all votes in `freq`, so no information is lost after the first pass. The second phase compares candidates only based on their aggregated frequencies, which is sufficient because the ordering rule depends solely on frequency and value. At every step, `best_value` represents the largest-numbered candidate among those seen so far with maximal frequency, so when the scan finishes, no unseen candidate can improve the result.

## Python Solution

```python
import sys
input = sys.stdin.readline

freq = [0] * 11

votes = list(map(int, input().split()))
for v in votes:
    freq[v] += 1

best_value = 1
best_count = freq[1]

for i in range(2, 11):
    if freq[i] > best_count or (freq[i] == best_count and i > best_value):
        best_value = i
        best_count = freq[i]

print(best_value)
```

The code first builds the frequency table in a single linear pass over the ten votes. The second loop performs a deterministic selection of the optimal candidate. The tie-breaking condition is handled explicitly by checking equality of counts and preferring the larger index.

One subtle point is initializing `best_count` with `freq[1]` instead of zero. This avoids unnecessary special-case reasoning and ensures the comparison logic always works uniformly even when all frequencies are zero except one.

## Worked Examples

### Example 1

Input:

`1 2 2 3 3 3 4 4 4 4`

We compute frequencies first.

| Step | Candidate | Frequency | Best Value | Best Count |
| --- | --- | --- | --- | --- |
| Init | - | - | 1 | 0 |
| 1 | 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 2 | 2 |
| 3 | 3 | 3 | 3 | 3 |
| 4 | 4 | 4 | 4 | 4 |

The final answer is 4 because it has the highest frequency.

This trace shows how the algorithm updates the winner monotonically as higher frequencies appear.

### Example 2

Input:

`1 1 2 2 3 3 4 4 5 5`

Frequencies are all equal to 2 for every number from 1 to 5.

| Step | Candidate | Frequency | Best Value | Best Count |
| --- | --- | --- | --- | --- |
| Init | - | - | 1 | 0 |
| 1 | 1 | 2 | 1 | 2 |
| 2 | 2 | 2 | 2 | 2 |
| 3 | 3 | 2 | 3 | 2 |
| 4 | 4 | 2 | 4 | 2 |
| 5 | 5 | 2 | 5 | 2 |

The final answer is 5 because all candidates tie and the largest index wins.

This confirms that the tie-breaking rule is correctly implemented through the strict comparison on index when frequencies are equal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(10) | One pass to count votes and one pass over 10 candidates |
| Space | O(1) | Fixed-size frequency array independent of input size |

The problem size is constant, so the algorithm runs in constant time and easily satisfies any typical contest constraints. Even if scaled up, the same structure would remain efficient due to the bounded candidate space.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    freq = [0] * 11
    votes = list(map(int, input().split()))
    for v in votes:
        freq[v] += 1

    best_value = 1
    best_count = freq[1]

    for i in range(2, 11):
        if freq[i] > best_count or (freq[i] == best_count and i > best_value):
            best_value = i
            best_count = freq[i]

    return str(best_value)

# provided sample-style case
assert run("1 2 3 4 2 3 4 3 4 4") == "4"

# all equal
assert run("7 7 7 7 7 7 7 7 7 7") == "7"

# tie with largest wins
assert run("1 1 2 2 3 3 4 4 5 5") == "5"

# single dominant
assert run("10 10 10 1 2 3 4 5 6 7") == "10"

# no tie, clear winner
assert run("1 2 3 4 5 6 7 8 8 8") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal 7 | 7 | uniform distribution handling |
| alternating pairs 1-5 | 5 | tie-breaking toward largest |
| dominant 10 | 10 | clear majority case |
| last three equal 8 | 8 | frequency aggregation correctness |

## Edge Cases

The all-equal scenario is handled naturally by the tie-breaking rule. When every frequency is identical, the scan over candidates always prefers larger indices because equality triggers the `i > best_value` condition.

For example, with input `7 7 7 7 7 7 7 7 7 7`, the frequency array has `freq[7] = 10` and all others zero. The algorithm initializes with candidate 1, then eventually reaches 7, where the maximum frequency is found and stored. No later candidate exceeds it, so 7 remains the final answer.

In a full tie case like `1 1 2 2 3 3 4 4 5 5`, every candidate from 1 to 5 has frequency 2. The algorithm successively updates the best value at each equality step, ending at 5. This directly reflects the tie-breaking rule and confirms that equality is handled consistently during the scan rather than after it.
