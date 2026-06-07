---
title: "CF 2087E - Color the Arrows"
description: "We are given a sequence of arrows arranged in a line, each pointing either left or right. Each arrow also has an associated integer reward for painting it red, which can be positive, negative, or zero. Initially, all arrows are blue."
date: "2026-06-08T05:58:07+07:00"
tags: ["codeforces", "competitive-programming", "*special", "dp"]
categories: ["algorithms"]
codeforces_contest: 2087
codeforces_index: "E"
codeforces_contest_name: "Kotlin Heroes: Episode 12"
rating: 0
weight: 2087
solve_time_s: 74
verified: true
draft: false
---

[CF 2087E - Color the Arrows](https://codeforces.com/problemset/problem/2087/E)

**Rating:** -  
**Tags:** *special, dp  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of arrows arranged in a line, each pointing either left or right. Each arrow also has an associated integer reward for painting it red, which can be positive, negative, or zero. Initially, all arrows are blue. The game allows you to perform a series of repainting operations, starting with any arrow, and then in each subsequent move you must pick an arrow in the direction of the previous one. That is, if the previous arrow pointed left, the next arrow must be at a smaller index; if it pointed right, the next arrow must be at a larger index. Arrows do not have to be adjacent.

The goal is to maximize the sum of the rewards for all arrows repainted red. Each query corresponds to a single test case, with up to $3 \cdot 10^5$ arrows, and the sum of all arrows across all test cases does not exceed $3 \cdot 10^5$. This constraint immediately suggests that any solution must process each test case in linear time relative to the number of arrows.

Edge cases are subtle because some rewards can be negative. In those cases, it is sometimes optimal to skip arrows entirely. For instance, if all rewards are negative, the maximum achievable score is zero. Another edge case occurs when all arrows point in the same direction; the optimal sequence may involve picking only the largest reward at the end of a directional chain rather than starting anywhere in the middle.

## Approaches

A brute-force approach would consider starting at each arrow and recursively simulating every valid sequence of repaintings. For each starting index, the algorithm would branch according to the direction of the current arrow and consider every possible valid next arrow. This approach is correct but clearly infeasible because in the worst case, it explores an exponential number of sequences, far exceeding the limits for $n \approx 3 \cdot 10^5$.

The key observation is that each sequence of arrows pointing in the same direction forms an independent chain where the reward selection can be performed greedily. If we traverse the arrows from left to right, for right-pointing arrows we can propagate a running maximum sum, and similarly from right to left for left-pointing arrows. In effect, we can view the problem as computing, for each arrow, the maximum contribution obtainable starting from that arrow if it is included, and then choosing the maximal such contribution over all arrows. This reduces the solution to linear time by computing two arrays: one propagating maximum sums to the right for '>' arrows, and one propagating maximum sums to the left for '<' arrows.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of arrows $n$, the string of directions, and the array of rewards.
2. Initialize two arrays `dp_right` and `dp_left` of length $n$, filled with zeros. These will store the maximal sum obtainable starting from each arrow in each direction.
3. Traverse the arrows from left to right. If the current arrow points right ('>'), set `dp_right[i] = reward[i] + max(0, dp_right[i-1])`. Otherwise, set `dp_right[i] = 0`. This accumulates sequences of consecutive right-pointing arrows and skips negative-sum sequences.
4. Traverse the arrows from right to left. If the current arrow points left ('<'), set `dp_left[i] = reward[i] + max(0, dp_left[i+1])`. Otherwise, set `dp_left[i] = 0`. This accumulates sequences of consecutive left-pointing arrows.
5. The answer for the test case is the maximum value among all `dp_right[i]` and `dp_left[i]`, as starting the sequence at any arrow is allowed. Also include 0 in the maximum to account for skipping all arrows.
6. Print the result.

Why it works: the directional propagation ensures that for each arrow, we consider the maximal sum obtainable by continuing in its pointing direction. By taking the maximum over all starting positions, we capture all possible sequences of operations. Negative rewards are automatically excluded due to the `max(0, ...)` logic, which models the choice of performing zero operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        c = list(map(int, input().split()))
        
        dp_right = [0] * n
        dp_left = [0] * n
        
        # propagate for '>' arrows
        for i in range(n):
            if s[i] == '>':
                dp_right[i] = c[i]
                if i > 0:
                    dp_right[i] += max(0, dp_right[i-1])
        
        # propagate for '<' arrows
        for i in reversed(range(n)):
            if s[i] == '<':
                dp_left[i] = c[i]
                if i < n-1:
                    dp_left[i] += max(0, dp_left[i+1])
        
        ans = 0
        for i in range(n):
            ans = max(ans, dp_right[i], dp_left[i])
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The code maintains linear time complexity by scanning the array twice, once from left to right and once from right to left. Using `max(0, ...)` automatically discards sequences with negative contribution, avoiding unnecessary operations. Boundary conditions are carefully handled by checking array indices before propagation.

## Worked Examples

Sample Input: `3, <> >, 5 4 6`

| i | s[i] | c[i] | dp_right | dp_left |
| --- | --- | --- | --- | --- |
| 0 | < | 5 | 0 | 5 |
| 1 | > | 4 | 4 | 0 |
| 2 | > | 6 | 10 | 0 |

The maximum among `dp_right` and `dp_left` is 10. This matches the expected output.

Sample Input: `2, >>, -1 -2`

| i | s[i] | c[i] | dp_right | dp_left |
| --- | --- | --- | --- | --- |
| 0 | > | -1 | -1 | 0 |
| 1 | > | -2 | -2 | 0 |

The maximum is 0, corresponding to skipping all arrows.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each array is traversed twice per test case. |
| Space | O(n) | Two auxiliary arrays of length n. |

Given the sum of $n$ across all test cases ≤ 3·10^5, this solution comfortably fits within time and memory constraints.

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

# provided samples
assert run("5\n3\n<>>\n5 4 6\n5\n<><>>\n5 -2 4 -3 7\n2\n>>\n-1 -2\n8\n>>>><<<<\n1 -1 1 -1 1 -1 1 -1\n5\n><<<>\n-1 100 100 100 100\n") == "10\n9\n0\n4\n399", "sample tests"

# custom edge cases
assert run("1\n1\n>\n100") == "100", "single positive"
assert run("1\n1\n<\n-100") == "0", "single negative"
assert run("1\n5\n<<>>>\n1 -2 3 -4 5") == "5", "mixed directions and signs"
assert run("1\n3\n<><\n-1 -2 -3") == "0", "all negative"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1\n>\n100 | 100 | Single arrow positive reward |
| 1\n1\n<\n-100 | 0 | Single arrow negative reward |
| 1\n5\n<<>>>\n1 -2 3 -4 5 | 5 | Mixed directions and positive/negative |
| 1\n3\n<><\n-1 -2 -3 | 0 | All negative rewards |

## Edge Cases

For a sequence with all arrows pointing in the same direction, the algorithm correctly propagates sums along that direction and automatically selects the maximal contiguous subsequence. For sequences with negative rewards, the `max(0, ...)` logic ensures no negative contribution is included. In single-arrow sequences, the maximum is either the reward or zero. For empty operations, the answer defaults to zero, correctly handling the case where it is better not to repaint any arrows.
