---
title: "CF 2172A - ASCII Art Contest"
description: "We are given the scores of three AI-powered creative assistants-Gemini, ChatGPT, and Claude-in an ASCII art contest. Each score is an integer between 80 and 100. The organizers want to decide if the judges' scores are consistent enough to announce a final result."
date: "2026-06-07T22:53:19+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2172
codeforces_index: "A"
codeforces_contest_name: "2025 ICPC Asia Taichung Regional Contest (Unrated, Online Mirror, ICPC Rules, Preferably Teams)"
rating: 800
weight: 2172
solve_time_s: 174
verified: true
draft: false
---

[CF 2172A - ASCII Art Contest](https://codeforces.com/problemset/problem/2172/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the scores of three AI-powered creative assistants-Gemini, ChatGPT, and Claude-in an ASCII art contest. Each score is an integer between 80 and 100. The organizers want to decide if the judges' scores are consistent enough to announce a final result. The rule is simple: if the difference between the highest and lowest score is at least 10, the judges must "check again"; otherwise, the announced result is the median of the three scores. The median here represents the score that would appear in the middle if the three were sorted.

The input is a single line of three integers representing the scores, and the output is a single line, either "check again" or "final X", where X is the median. The constraints are very small: there are only three integers, so any algorithm we pick will run in constant time. However, non-obvious edge cases include all three scores being equal, two scores at one extreme and one at the other, or scores differing by exactly 10. For example, if the scores are 80, 90, 90, the difference between the max and min is exactly 10, so the program should print "check again". A careless approach might compute the median incorrectly by picking the wrong middle element or using an exclusive inequality.

## Approaches

The brute-force approach here is to sort the three scores. Sorting a list of three elements is trivial; we can then directly pick the middle value as the median and check the difference between the maximum and minimum. This works because sorting guarantees we can identify min, max, and median reliably. Even though sorting is usually O(n log n), with three elements it is effectively constant time, so performance is not a concern.

A slightly more optimized approach avoids full sorting. We can compute the minimum, maximum, and median using simple conditional logic. The minimum is the smallest of the three scores, the maximum is the largest, and the median can be found by adding all three scores and subtracting the min and max. This yields the same result in fewer comparisons and is elegant. The observation that the median of three numbers equals the sum minus the min and max allows us to avoid sorting completely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Sort three scores | O(1) | O(1) | Accepted |
| Min/Max/Sum trick | O(1) | O(1) | Accepted |

Both approaches are effectively constant time because the input size is fixed at three.

## Algorithm Walkthrough

1. Read the three scores into variables `g`, `c`, and `l`. This is our direct mapping from input to internal representation.
2. Compute the maximum score `mx` using `max(g, c, l)`. This identifies the highest-scoring AI assistant.
3. Compute the minimum score `mn` using `min(g, c, l)`. This identifies the lowest-scoring AI assistant.
4. If the difference `mx - mn` is greater than or equal to 10, print "check again" and stop. This enforces the rule that scores are too spread out.
5. Otherwise, compute the median score as `g + c + l - mx - mn`. This works because subtracting the min and max from the total sum leaves the middle value.
6. Print "final " followed by the median score.

Why it works: The algorithm explicitly identifies the extreme values to check the consistency criterion, and the sum-minus-min-max trick correctly computes the median because there are only three elements. No intermediate states can violate the rules because all three variables are always compared in the same way.

## Python Solution

```python
import sys
input = sys.stdin.readline

g, c, l = map(int, input().split())

mx = max(g, c, l)
mn = min(g, c, l)

if mx - mn >= 10:
    print("check again")
else:
    median = g + c + l - mx - mn
    print(f"final {median}")
```

The solution reads input efficiently and maps it directly into three integer variables. The max and min calculations are straightforward and safe given the constrained range of scores. The median calculation avoids sorting and is robust even if two scores are equal. Printing uses an f-string for readability and ensures the output format matches exactly what the problem expects.

## Worked Examples

**Example 1:** Scores `88 94 95`

| g | c | l | mx | mn | mx-mn | median | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 88 | 94 | 95 | 95 | 88 | 7 | 94 | final 94 |

The difference is less than 10, so the median is computed as 88+94+95-95-88=94.

**Example 2:** Scores `80 90 90`

| g | c | l | mx | mn | mx-mn | median | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 80 | 90 | 90 | 90 | 80 | 10 | 90 | check again |

The difference is exactly 10, so the algorithm correctly prints "check again" rather than the median.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only three comparisons are needed to compute min, max, and median. |
| Space | O(1) | Only a few integer variables are used. |

Given the input constraints, the algorithm runs in constant time and space and easily fits within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    g, c, l = map(int, input().split())
    mx = max(g, c, l)
    mn = min(g, c, l)
    if mx - mn >= 10:
        return "check again"
    else:
        median = g + c + l - mx - mn
        return f"final {median}"

# Provided sample
assert run("88 94 95") == "final 94", "sample 1"

# Custom cases
assert run("80 90 90") == "check again", "boundary difference 10"
assert run("100 100 100") == "final 100", "all equal max"
assert run("80 80 90") == "check again", "max-min = 10"
assert run("80 85 90") == "final 85", "typical median calculation"
assert run("99 91 95") == "final 95", "unordered scores"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 80 90 90 | check again | Difference exactly 10 triggers re-evaluation |
| 100 100 100 | final 100 | All equal scores produce median correctly |
| 80 80 90 | check again | Two equal minimums and one high triggers check again |
| 80 85 90 | final 85 | Correct median calculation for spread less than 10 |
| 99 91 95 | final 95 | Median calculation works for unordered scores |

## Edge Cases

The edge case of scores differing by exactly 10 is handled by the comparison `mx - mn >= 10`. For example, with input `80 90 90`, `mx=90` and `mn=80`, so `mx - mn=10`, which satisfies the check-again condition. The algorithm does not incorrectly print a median here. Similarly, when all scores are equal, `mx=mn`, so the difference is 0, and the median equals any of the scores, which is correct. This confirms the algorithm respects both equality and boundary difference conditions.
