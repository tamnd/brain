---
title: "CF 1143A - The Doors"
description: "The problem can be restated as follows. Mr. Black has a house with two sets of doors, each leading to a separate exit: left and right. Each door is initially closed, and we know the exact sequence in which Mr. Black opens them."
date: "2026-06-12T03:35:26+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1143
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 549 (Div. 2)"
rating: 800
weight: 1143
solve_time_s: 71
verified: true
draft: false
---

[CF 1143A - The Doors](https://codeforces.com/problemset/problem/1143/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem can be restated as follows. Mr. Black has a house with two sets of doors, each leading to a separate exit: left and right. Each door is initially closed, and we know the exact sequence in which Mr. Black opens them. Once all doors in at least one exit are open, he can leave the house. The task is to find the earliest point in his sequence when this becomes possible.

The input consists of an integer `n` representing the total number of doors, followed by a list of `n` integers where each integer is `0` if the door belongs to the left exit, or `1` if it belongs to the right exit. We need to determine the smallest prefix of this sequence that opens all doors in one of the exits. The output is this prefix length `k`.

The constraints allow up to `n = 200,000` doors. This rules out any approach with quadratic time complexity, because `n^2` operations would reach 40 billion, far exceeding the 1-second time limit. Linear or near-linear solutions are feasible. The main edge case to consider is when one exit has only one door; if that door is opened last, a naive prefix-checking approach might incorrectly report the first opportunity to exit.

A small but illustrative example is `n = 3` with sequence `1 0 0`. The left exit has two doors, the right exit has one. After opening the first door (right exit), Mr. Black can already leave, so the correct output is `1`. A careless approach that only counts total doors opened or scans from the left exit first could incorrectly produce `3`.

## Approaches

The brute-force method is straightforward: for each prefix of the sequence, check whether all doors of the left exit are open or all doors of the right exit are open. To implement this, we would maintain two sets: one for doors remaining closed in the left exit and one for the right exit. For each door opened, remove it from its respective set. Once either set becomes empty, output the current index. This is correct, but constructing the sets and checking emptiness at every step involves roughly `O(n)` operations per prefix, giving `O(n^2)` total. With `n` up to 200,000, this approach is too slow.

The optimal approach relies on counting. First, we count how many doors belong to the left exit and how many to the right. Then we maintain counters of doors opened in each exit as we iterate through the sequence. The moment either counter reaches the total number of doors in that exit, we know that all doors in that exit are open, and we can immediately return the current position as the answer. This works in linear time `O(n)` because each door is processed exactly once, and requires only constant extra space for the counters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize two variables `left_total` and `right_total` to count the number of doors in each exit. Iterate through the input once to populate these counts. This is necessary to know the target counts for when all doors in an exit are open.
2. Initialize two counters `left_opened` and `right_opened` to zero. These will track how many doors in each exit have been opened so far.
3. Iterate through the sequence of doors using a single pass. For each door, increment the corresponding counter (`left_opened` for a `0` and `right_opened` for a `1`).
4. After updating the counter, check whether it equals the total number of doors for that exit (`left_opened == left_total` or `right_opened == right_total`). The first time this condition holds, output the current index (1-based) and terminate.
5. Since the problem guarantees that every door is eventually opened, we are guaranteed to find a solution before reaching the end of the sequence.

Why it works: at every step, `left_opened` and `right_opened` exactly represent the number of doors currently open in each exit. Once one of these matches the total count of doors in that exit, it means all doors in that exit are open, satisfying the exit condition. Because we return immediately at the first occurrence, we are guaranteed to find the minimal `k`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
doors = list(map(int, input().split()))

left_total = doors.count(0)
right_total = n - left_total

left_opened = 0
right_opened = 0

for i, door in enumerate(doors, start=1):
    if door == 0:
        left_opened += 1
    else:
        right_opened += 1
    if left_opened == left_total or right_opened == right_total:
        print(i)
        break
```

The solution starts by counting how many doors belong to each exit. The counters for opened doors are then updated as we iterate through the sequence. The `enumerate` function is used with `start=1` to match the 1-based output required. The conditional check ensures that the first moment an exit is fully open is returned immediately. Using `doors.count(0)` is a simple linear pass that is negligible compared to the main loop, keeping the overall complexity linear. Off-by-one errors are avoided by 1-based indexing in `enumerate`.

## Worked Examples

Sample 1: `5`, sequence `0 0 1 0 0`.

| i | door | left_opened | right_opened | Condition |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | false |
| 2 | 0 | 2 | 0 | false |
| 3 | 1 | 2 | 1 | true |

After opening the third door, all doors in the right exit (only one door) are open, so the output is `3`.

Sample 2: `6`, sequence `1 0 1 0 0 1`.

| i | door | left_opened | right_opened | Condition |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | false |
| 2 | 0 | 1 | 1 | false |
| 3 | 1 | 1 | 2 | false |
| 4 | 0 | 2 | 2 | false |
| 5 | 0 | 3 | 2 | true |

All left doors (3 total) are open after the fifth door, so the answer is `5`. This trace confirms that the algorithm tracks counters correctly and identifies the minimal prefix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting doors and iterating through the sequence are each linear in `n` |
| Space | O(1) | Only four integer counters are used, independent of `n` |

The algorithm easily handles the maximum input size of 200,000 doors in a fraction of a second. Memory usage is trivial compared to the 256 MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    doors = list(map(int, input().split()))
    left_total = doors.count(0)
    right_total = n - left_total
    left_opened = right_opened = 0
    for i, door in enumerate(doors, start=1):
        if door == 0:
            left_opened += 1
        else:
            right_opened += 1
        if left_opened == left_total or right_opened == right_total:
            return str(i)

# provided samples
assert run("5\n0 0 1 0 0\n") == "3", "sample 1"
assert run("6\n1 0 1 0 0 1\n") == "5", "sample 2"

# custom cases
assert run("2\n0 1\n") == "1", "minimum size, either door first opens an exit"
assert run("4\n1 1 0 0\n") == "2", "first exit fully opened immediately"
assert run("5\n0 0 0 1 1\n") == "3", "left exit completes before right"
assert run("5\n1 1 1 0 0\n") == "3", "right exit completes before left"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n0 1 | 1 | minimal number of doors, immediate exit |
| 4\n1 1 0 0 | 2 | first exit finishes early in sequence |
| 5\n0 0 0 1 1 | 3 | left exit completed first, right unfinished |
| 5\n1 1 1 0 0 | 3 | right exit completed first, left unfinished |

## Edge Cases

For a single-door exit, the algorithm immediately detects the exit once that door is opened. Input `2\n0 1\n` shows that opening the first door (right exit) allows Mr. Black to leave even though the left exit still
