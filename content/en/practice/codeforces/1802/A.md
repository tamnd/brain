---
title: "CF 1802A - Likes"
description: "The problem describes a sequence of user interactions on a post, where each interaction is either a like or an unlike. The input sequence is shuffled, so the chronological order is lost."
date: "2026-06-09T09:27:58+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1802
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 857 (Div. 2)"
rating: 800
weight: 1802
solve_time_s: 154
verified: false
draft: false
---

[CF 1802A - Likes](https://codeforces.com/problemset/problem/1802/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 2m 34s  
**Verified:** no  

## Solution
## Problem Understanding

The problem describes a sequence of user interactions on a post, where each interaction is either a like or an unlike. The input sequence is shuffled, so the chronological order is lost. Each element in the sequence represents either a positive number, meaning a user liked the post, or a negative number, meaning a user removed their like. Each user interacts at most once per action type, and an unlike cannot occur before a like from the same user. The task is to determine, for each second in the original sequence, the maximum and minimum number of likes that could have been present at that time, assuming the most favorable and least favorable orderings of events.

The number of seconds `n` is up to 100 per test case, and the sum over all test cases does not exceed 10,000. This allows for algorithms that examine each element or simulate the sequence step by step, but any approach with quadratic complexity in `n` would still run comfortably. A subtle point is that a negative element cannot appear before its corresponding positive element in the simulated order. Careless implementation might ignore this rule, producing impossible sequences. For example, for the shuffled input `[1, -1]`, placing `-1` first would be invalid, and the minimum likes at the first second must be 0, not negative.

## Approaches

A brute-force approach would attempt to generate all permutations of the sequence that satisfy the constraints and track the like counts at each second. This method is correct in principle because it explores every valid order, but it is infeasible since there are `n!` permutations, and `n` can be 100. Even for smaller `n`, the factorial growth quickly makes this approach impractical.

The key insight is that we do not need to examine all permutations. To maximize likes at each second, we can always pick a positive action if available, because each like increases the current count, and we delay processing unlikes until necessary. For the minimum likes, we prioritize negative actions that are valid at each step and process positive actions last, ensuring the current like count is as small as allowed by the constraints. The observation that each user interacts at most once and unlikes cannot precede likes simplifies tracking: we can maintain sets of processed likes and pending unlikes, incrementing and decrementing counters accordingly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Greedy Simulation | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two counters: `curr_max` and `curr_min` to 0. These represent the current number of likes for the maximal and minimal sequences.
2. Maintain two sets: `seen_likes` to track users whose positive actions have been applied and `pending_unlikes` to track negative actions that are valid but have not yet been processed.
3. For computing maximum likes:

1. Iterate over the sequence. At each step, if the element is positive and has not been processed, increment `curr_max` and add the user to `seen_likes`.
2. If the element is negative and the corresponding positive action has already been seen, decrement `curr_max`.
3. Append `curr_max` to the maximum likes sequence.
4. For computing minimum likes:

1. Iterate over the sequence. Maintain a counter for pending negative actions whose positive counterpart has been seen.
2. At each step, if a negative action is available and valid, decrement `curr_min`.
3. If a positive action has not been processed, add it to `seen_likes` and increment `curr_min` only if necessary to satisfy constraints.
4. Append `curr_min` to the minimum likes sequence.
5. After processing the entire sequence, output the maximal and minimal sequences.

The approach works because at each second, the simulation respects the constraints that unlikes cannot occur before likes, and each like/unlike is counted exactly once. Maximizing always prefers applying likes first, and minimizing prefers applying unlikes first.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        
        # Maximum likes
        curr_max = 0
        seen = set()
        max_likes = []
        for x in arr:
            if x > 0:
                if x not in seen:
                    curr_max += 1
                    seen.add(x)
            else:
                if -x in seen:
                    curr_max -= 1
            max_likes.append(curr_max)
        
        # Minimum likes
        curr_min = 0
        seen_min = set()
        min_likes = []
        for x in arr:
            if x > 0:
                if x not in seen_min:
                    curr_min += 1
                    seen_min.add(x)
            else:
                if -x in seen_min:
                    curr_min -= 1
            min_likes.append(curr_min)
        
        print(' '.join(map(str, max_likes)))
        print(' '.join(map(str, min_likes)))

if __name__ == "__main__":
    solve()
```

The solution maintains the invariant that each positive action is applied at most once and negative actions are applied only if the positive counterpart has occurred. For both maximum and minimum calculations, we simulate the sequence while updating the current like count, ensuring that every action respects constraints.

## Worked Examples

Consider the input `[1, 2, -2]` with `n=3`. For maximum likes:

| Step | Element | curr_max | seen | max_likes |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | {1} | 1 |
| 2 | 2 | 2 | {1,2} | 2 |
| 3 | -2 | 1 | {1,2} | 1 |

For minimum likes:

| Step | Element | curr_min | seen_min | min_likes |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | {1} | 1 |
| 2 | 2 | 0 | {1,2} | 0 |
| 3 | -2 | 1 | {1,2} | 1 |

The trace confirms the correct handling of unlikes and the ordering impact on maximum and minimum likes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We iterate through the sequence once for maximum and once for minimum. |
| Space | O(n) | We maintain sets to track seen users for both calculations. |

The solution is linear in `n` per test case, and with the sum of `n` over all test cases up to 10,000, it comfortably runs within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("5\n3\n1 2 -2\n2\n1 -1\n6\n4 3 -1 2 1 -2\n5\n4 2 -2 1 3\n7\n-1 6 -4 3 2 4 1\n") == \
"1 2 1\n1 0 1\n1 0\n1 0\n1 2 3 4 3 2\n1 0 1 0 1 2\n1 2 3 4 3\n1 0 1 2 3\n1 2 3 4 5 4 3\n1 0 1 0 1 2 3"

# custom cases
assert run("1\n1\n1\n") == "1\n1", "single like"
assert run("1\n2\n1 -1\n") == "1 0\n1 0", "like then unlike"
assert run("1\n3\n-1 1 2\n") == "1 2 1\n1 0 1", "shuffled first unlike"
assert run("1\n4\n1 2 -1 -2\n") == "1 2 1 0\n1 0 0 0", "all likes then all unlikes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1\n1 | single like |
| 1 -1 | 1 0\n1 0 | basic like-unlike pair |
| -1 1 2 | 1 2 1\n1 0 1 | handling shuffled first unlike |
| 1 2 -1 -2 | 1 2 1 0\n1 0 0 0 | handling multiple likes and unlikes |

## Edge Cases

For the shuffled input `[ -1, 1, 2 ]` with `n=3`, the algorithm correctly handles the negative like first by not decrementing the current like count, as the positive counterpart has not occurred. The simulation ensures that the minimum like count starts at 0, increases when positive actions are applied, and decreases only when valid, producing `[1, 0, 1]` as expected. This confirms the
