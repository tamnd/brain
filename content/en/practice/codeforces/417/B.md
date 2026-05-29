---
title: "CF 417B - Crash"
description: "We are given a list of submissions made by participants in a programming contest. Each submission is described by two numbers: x, which counts how many unique solutions this participant had already submitted before this one, and k, the participant's ID."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 417
codeforces_index: "B"
codeforces_contest_name: "RCC 2014 Warmup (Div. 2)"
rating: 1400
weight: 417
solve_time_s: 89
verified: true
draft: false
---

[CF 417B - Crash](https://codeforces.com/problemset/problem/417/B)

**Rating:** 1400  
**Tags:** implementation  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of submissions made by participants in a programming contest. Each submission is described by two numbers: _x_, which counts how many unique solutions this participant had already submitted before this one, and _k_, the participant's ID. Submissions for the same participant must appear in chronological order: if a submission shows _x = 2_, then there must have been a previous submission by the same participant with _x = 1_ somewhere earlier in the list. The task is to verify that the restored list respects this chronological order for every participant.

The constraints indicate that there can be up to 100,000 submissions, and each participant ID and solution number can also go up to 100,000. This implies that a quadratic algorithm that scans all previous submissions for each new submission would be too slow. We need a solution that scales linearly or nearly linearly with the number of submissions. Edge cases include multiple participants with interleaved submissions, participants with gaps in their _x_ values, and the smallest case with a single submission. For example, a list like:

```
3
0 1
2 1
1 1
```

must output "NO" because the second submission claims _x = 2_ without a preceding _x = 1_ for participant 1, even though _x = 1_ appears later.

## Approaches

A naive approach is to maintain a list of all previous submissions for each participant and, for every new submission, scan backward to ensure all smaller _x_ values have appeared. This would be correct, but in the worst case, each submission could require scanning through nearly all prior submissions, yielding an O(n²) time complexity. With n up to 10^5, this approach is impractical.

The key observation is that for each participant, we only need to know the largest _x_ that has appeared so far. If a new submission for participant _k_ has _x_ larger than the current maximum for _k_ plus 1, the list is invalid. If _x_ equals the current maximum or current maximum plus 1, it is consistent. Therefore, we can store the current maximum _x_ for each participant in a dictionary. This reduces the check for each submission to O(1), yielding an overall O(n) solution. The idea is that chronological order only requires tracking the latest submitted index per participant; we never need the full list of submissions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty dictionary to map participant IDs to the largest _x_ seen so far. This captures the most recent chronological submission for each participant.
2. Iterate through each submission in the list. For each submission, read the participant ID _k_ and solution number _x_.
3. Check the dictionary for the participant's current maximum. If the participant has no previous submissions, treat the maximum as -1.
4. If the new _x_ is greater than the current maximum plus 1, immediately output "NO" and stop. This means there is a skipped submission number and the chronological order is broken.
5. Otherwise, update the participant's maximum _x_ to the maximum of the current value and _x_. This handles repeated submissions with the same _x_ without breaking the sequence.
6. If the loop completes without detecting a violation, output "YES".

The invariant maintained is that for every participant, the dictionary always stores the largest _x_ seen up to that point in the sequence. If any submission violates the rule _x ≤ current_max + 1_, the chronological order is guaranteed to be broken.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
latest = {}

valid = True
for _ in range(n):
    x, k = map(int, input().split())
    current_max = latest.get(k, -1)
    if x > current_max + 1:
        valid = False
        break
    latest[k] = max(current_max, x)

print("YES" if valid else "NO")
```

The dictionary `latest` tracks the largest submission index per participant. Using `get(k, -1)` allows us to handle participants who have not yet submitted any solutions. The `max` ensures repeated submissions with the same _x_ do not decrease the stored maximum. Early termination on a violation avoids unnecessary work.

## Worked Examples

Trace for the sample input:

```
2
0 1
1 1
```

| Step | x | k | current_max | Check | latest[k] | valid |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | -1 | 0 ≤ -1+1 | 0 | True |
| 2 | 1 | 1 | 0 | 1 ≤ 0+1 | 1 | True |

The algorithm confirms chronological order and prints "YES".

Trace for a failing case:

```
3
0 1
2 1
1 1
```

| Step | x | k | current_max | Check | latest[k] | valid |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | -1 | 0 ≤ 0 | 0 | True |
| 2 | 2 | 1 | 0 | 2 ≤ 0+1? | - | False |

The algorithm stops at step 2, prints "NO", correctly catching the skipped submission.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each submission is processed once, with dictionary access O(1). |
| Space | O(n) | Dictionary stores one entry per participant, up to n participants. |

With n up to 100,000, the algorithm performs well within typical 1-second time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    latest = {}
    valid = True
    for _ in range(n):
        x, k = map(int, input().split())
        current_max = latest.get(k, -1)
        if x > current_max + 1:
            valid = False
            break
        latest[k] = max(current_max, x)
    return "YES" if valid else "NO"

# Provided sample
assert run("2\n0 1\n1 1\n") == "YES", "sample 1"

# Edge: single submission
assert run("1\n0 1\n") == "YES", "single submission"

# Skipped submission
assert run("3\n0 1\n2 1\n1 1\n") == "NO", "skipped submission"

# Multiple participants
assert run("4\n0 1\n0 2\n1 1\n1 2\n") == "YES", "multiple participants"

# Interleaved violation
assert run("4\n0 1\n1 2\n2 1\n1 2\n") == "NO", "interleaved violation"

# Large x repeated
assert run("3\n0 1\n0 1\n1 1\n") == "YES", "repeated same x allowed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n0 1` | YES | Minimum input case |
| `3\n0 1\n2 1\n1 1` | NO | Submission number skipped |
| `4\n0 1\n0 2\n1 1\n1 2` | YES | Multiple participants maintain independent sequences |
| `4\n0 1\n1 2\n2 1\n1 2` | NO | Interleaved submissions can break order |
| `3\n0 1\n0 1\n1 1` | YES | Duplicate submissions with same x allowed |

## Edge Cases

For the skipped submission case `3\n0 1\n2 1\n1 1\n`, the algorithm sets `latest[1]` to 0 after the first submission. On the second submission with x=2, the check `2 > 0+1` fails, immediately returning "NO" without ever looking at the last line. This demonstrates correct handling of out-of-order sequences. For repeated x values, like `0 1` twice, `latest[1]` remains 0, allowing the next submission with x=1, which matches the current maximum, confirming that repeated solutions are acceptable.
