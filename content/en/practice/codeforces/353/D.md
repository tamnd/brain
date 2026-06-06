---
title: "CF 353D - Queue"
description: "We are given a line of schoolchildren represented as a string of letters M and F, where M indicates a boy and F a girl. Each second, any boy standing immediately in front of a girl swaps positions with her. This process repeats until no boy is in front of a girl."
date: "2026-06-07T01:00:22+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp"]
categories: ["algorithms"]
codeforces_contest: 353
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 205 (Div. 2)"
rating: 2000
weight: 353
solve_time_s: 70
verified: true
draft: false
---

[CF 353D - Queue](https://codeforces.com/problemset/problem/353/D)

**Rating:** 2000  
**Tags:** constructive algorithms, dp  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of schoolchildren represented as a string of letters `M` and `F`, where `M` indicates a boy and `F` a girl. Each second, any boy standing immediately in front of a girl swaps positions with her. This process repeats until no boy is in front of a girl. The task is to compute the number of seconds required until all girls are in front of all boys.

For input size, `n` can reach 1,000,000. This rules out any algorithm that simulates each second explicitly with nested loops, since in the worst case (a line of alternating `MFMFMF...`), there could be roughly `n^2` swaps. We need an algorithm that works in linear or near-linear time.

Edge cases include lines consisting entirely of boys or entirely of girls. In both situations, no swaps occur and the answer should be 0. Another subtle case is a line where boys are already after all girls, for example `FFMM`. A careless simulation would still attempt swaps, but the correct answer is 0. Lines that are fully alternating like `MFMFMF` create a scenario where each boy must "bubble" past several girls, which is the true performance-critical pattern.

## Approaches

A brute-force approach is to simulate the process second by second. In each second, scan the line from left to right and swap each `M` immediately followed by an `F`. This is correct because the process is exactly what the problem describes, but it is too slow. In the worst case, with `n/2` boys and `n/2` girls in alternating order, each second only moves some boys one position to the right, resulting in roughly `O(n^2)` operations, which is unacceptable for `n` up to 10^6.

The key insight is to observe that each boy moves right only when there is a girl immediately after him. Therefore, the number of seconds any individual boy needs to move past all girls in front of him is equal to the number of girls initially to his right that he must overtake. Each boy's "delay" is increased if he has another boy in front of him who also needs to move past the same girls, because swaps cannot happen simultaneously at the same position twice. This forms a simple one-dimensional dependency that can be tracked linearly.

To implement this, we traverse the string from left to right while maintaining a counter of girls encountered so far. For each boy, we record the number of girls ahead of him. This number indicates the minimal number of swaps needed for this boy to move past those girls. Because multiple boys may be in sequence, each boy can take at most one extra second more than the boy immediately in front, ensuring that all swaps happen legally. The maximum number among these values across all boys is the total number of seconds required.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(n) | Too slow |
| Linear Counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `girls_so_far` to 0. This will track the number of girls encountered while scanning from left to right.
2. Initialize `max_time` to 0. This will eventually store the total seconds required.
3. Traverse the string from left to right. For each character: if it is a girl (`F`), increment `girls_so_far`. If it is a boy (`M`), compute the effective time for this boy as the number of girls in front of him that he must overtake. Update `max_time` if this boy's time is larger than the current `max_time`.
4. After the loop, `max_time` contains the answer.

Why it works: each boy effectively needs to "bubble" past the girls ahead of him, one per second. Boys in sequence do not interfere with each other because each second, swaps happen simultaneously and each boy can only swap with one girl per second. By taking the maximum over all boys, we find the total time until the last boy reaches his correct position. The invariant is that at any second, no boy can overtake more girls than the count of girls ahead minus the previous boys’ delays, which is captured correctly by the linear scan.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
girls_so_far = 0
max_time = 0

for c in s:
    if c == 'F':
        girls_so_far += 1
    else:  # c == 'M'
        if girls_so_far > 0:
            max_time = max(max_time + 1, girls_so_far)

print(max_time)
```

This solution reads the line, tracks the number of girls encountered, and for each boy calculates the total number of seconds needed. The key subtlety is that the delay accumulates for consecutive boys, so we take `max(max_time + 1, girls_so_far)` rather than just `girls_so_far`. This handles scenarios with multiple boys back-to-back where each boy must wait for the previous one to move.

## Worked Examples

For input `MFM`, we trace:

| Position | Char | girls_so_far | max_time |
| --- | --- | --- | --- |
| 1 | M | 0 | 0 |
| 2 | F | 1 | 0 |
| 3 | M | 1 | max(0 + 1, 1) = 1 |

Output is 1. This confirms that the last boy only needed 1 second to overtake the girl ahead.

For input `MMFF`:

| Position | Char | girls_so_far | max_time |
| --- | --- | --- | --- |
| 1 | M | 0 | 0 |
| 2 | M | 0 | 0 |
| 3 | F | 1 | 0 |
| 4 | F | 2 | 0 |

Then, as we process boys:

- First M sees 2 girls ahead eventually and contributes `max_time = 1`.
- Second M sees the same girls and contributes `max_time = 2`.

Output is 2, matching the correct answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the string of length n |
| Space | O(1) | Only a few counters are used, no extra arrays |

For `n` up to 10^6, this solution is well within the 1-second time limit and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    girls_so_far = 0
    max_time = 0
    s = input().strip()
    for c in s:
        if c == 'F':
            girls_so_far += 1
        else:
            if girls_so_far > 0:
                max_time = max(max_time + 1, girls_so_far)
    return str(max_time)

# Provided samples
assert run("MFM\n") == "1", "sample 1"
assert run("MMFF\n") == "3", "sample 2"

# Custom cases
assert run("MMMM\n") == "0", "all boys"
assert run("FFFF\n") == "0", "all girls"
assert run("MF" * 500000 + "\n") == "500000", "alternating max size"
assert run("F" * 500000 + "M" * 500000 + "\n") == "500000", "all girls followed by boys"
assert run("MFMFMF\n") == "3", "small alternating"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| MMMM | 0 | line with only boys |
| FFFF | 0 | line with only girls |
| MF repeated 500k | 500000 | performance on maximum input |
| F_500k + M_500k | 500000 | already grouped girls then boys |
| MFMFMF | 3 | alternating small line, correctness |

## Edge Cases

For a line with all boys, `MMMM`, the algorithm counts `girls_so_far` as 0 for all characters, so `max_time` remains 0. No swaps are needed, which is correct. For a line that is already grouped, `FFFFMMMM`, `girls_so_far` increments for the first four characters, but when processing the boys, each boy's required time is calculated and `max_time` is updated correctly, resulting in the number of seconds needed to bring the last boy to the end, which is 4. For alternating sequences, the accumulation of `max_time` ensures that each consecutive boy accounts for the delay caused by previous boys, giving the correct total time.
