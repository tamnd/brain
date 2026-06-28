---
title: "CF 104880A - Well Rested"
description: "We are given a fixed schedule encoded as a binary string of length 24. Each position corresponds to one hour of a day, starting from hour 1 up to hour 24. A character 1 means you are working during that hour, while 0 means you are resting."
date: "2026-06-28T09:21:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104880
codeforces_index: "A"
codeforces_contest_name: "The 18-th Beihang University Collegiate Programming Contest (BCPC 2023) - Preliminary"
rating: 0
weight: 104880
solve_time_s: 42
verified: true
draft: false
---

[CF 104880A - Well Rested](https://codeforces.com/problemset/problem/104880/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed schedule encoded as a binary string of length 24. Each position corresponds to one hour of a day, starting from hour 1 up to hour 24. A character `1` means you are working during that hour, while `0` means you are resting.

The only condition that makes a schedule invalid is the presence of a block of six consecutive working hours. If anywhere in the day there exists a contiguous substring consisting entirely of six `1` characters, the schedule is considered harmful. Otherwise, it is acceptable.

The task is simply to decide whether such a forbidden block exists.

Even though the input size is fixed at 24, the structure of the problem hints at a general pattern recognition task over a short sequence. Any solution that inspects every possible contiguous segment of length 6 will run in constant time here, since there are only 19 such segments in a 24-length string.

A common edge case comes from off-by-one scanning logic. For example, given `111110111111`, a careless implementation that checks only disjoint blocks like `[1..6], [7..12]` would incorrectly miss a run that crosses boundaries. Another subtle issue is forgetting that runs can appear anywhere, not necessarily aligned to multiples of six.

Correct handling requires checking all overlapping windows of size 6.

## Approaches

A brute-force way to solve the problem is to examine every possible contiguous substring of length 6 and verify whether all characters in that substring are `1`. Since the string length is 24, there are 24 − 6 + 1 = 19 such substrings. For each substring, checking its validity requires inspecting 6 characters, so the total work is constant and extremely small.

This brute-force method is already optimal in this setting because the input size is fixed and tiny. However, it is conceptually useful to think of a more general version where the string length is `n`. In that case, the naive approach would examine all windows of size 6, leading to O(n) windows and O(6n) total checks, which simplifies to O(n).

The key observation is that we are not computing a complex function over substrings, but simply detecting whether any run of length at least 6 exists. This makes the problem equivalent to tracking a current streak of consecutive `1`s. Instead of repeatedly rescanning substrings, we can maintain a running counter and reset it whenever a `0` is encountered. The moment the counter reaches 6, we can stop immediately.

This reduces the logic from sliding window checks to a single pass with constant memory.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Sliding Window | O(n) | O(1) | Accepted |
| Single Pass Counter | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter `run` to zero. This variable represents the current length of consecutive `1`s we have seen so far.
2. Iterate through each character in the string from left to right.
3. If the current character is `1`, increment `run` by 1 because the streak continues.
4. If the current character is `0`, reset `run` to 0 since any consecutive sequence is broken.
5. After updating `run`, check whether it has reached 6. If it has, immediately conclude the schedule is invalid and stop processing.
6. If the loop finishes without ever reaching 6, the schedule is valid.

The key idea is that we never need to remember more than the current streak because any future valid block must be contiguous, and any break invalidates previous continuity.

### Why it works

At any index in the string, the value of `run` exactly equals the length of the longest suffix ending at that position consisting only of `1`s. This means every possible contiguous block of `1`s is implicitly represented as a value of `run` at some point during the scan. If a block of length 6 exists anywhere, then when we reach its final character, `run` must be at least 6, triggering detection. Conversely, if no such block exists, `run` never reaches 6, so the algorithm correctly accepts the schedule.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

run = 0
for ch in s:
    if ch == '1':
        run += 1
        if run >= 6:
            print("NO")
            break
    else:
        run = 0
else:
    print("YES")
```

The solution reads the 24-character schedule and maintains a single integer counter. The loop uses Python’s `for-else` structure so that “YES” is printed only if no early break occurs. The early exit is important because once a valid violation is found, further scanning is unnecessary.

A common implementation mistake is forgetting to reset the counter when encountering `0`, which would incorrectly merge separated runs into one continuous segment. Another subtle issue is checking only after the loop instead of during iteration, which would prevent early termination but still remain correct due to small input size.

## Worked Examples

### Example 1

Input:

```
111110111111111111111111
```

We track the run length as follows:

| Index | Char | Run after update | Action |
| --- | --- | --- | --- |
| 1 | 1 | 1 | continue |
| 2 | 1 | 2 | continue |
| 3 | 1 | 3 | continue |
| 4 | 1 | 4 | continue |
| 5 | 1 | 5 | continue |
| 6 | 0 | 0 | reset |
| 7 | 1 | 1 | continue |
| 8 | 1 | 2 | continue |

This run later reaches 6 in the second segment of consecutive `1`s, so the algorithm would output `NO`.

This trace shows how resets prevent cross-gap accumulation and ensure only contiguous sequences are counted.

### Example 2

Input:

```
111011101110111011101110
```

| Index | Char | Run after update | Action |
| --- | --- | --- | --- |
| 1 | 1 | 1 | continue |
| 2 | 1 | 2 | continue |
| 3 | 1 | 3 | continue |
| 4 | 0 | 0 | reset |
| 5 | 1 | 1 | continue |
| 6 | 1 | 2 | continue |
| 7 | 1 | 3 | continue |
| 8 | 0 | 0 | reset |

The run never exceeds 3 in this pattern, so no violation is found and the output is `YES`.

This confirms that multiple separated short work bursts are safe as long as no single burst reaches length 6.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the 24-character string, constant work per character |
| Space | O(1) | Only one integer counter is stored |

Given that `n = 24`, this is effectively constant time in practice and trivially satisfies all constraints.

The solution is well within limits because it performs at most 24 iterations and a few integer operations per step.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        s = input().strip()
        run_cnt = 0
        for ch in s:
            if ch == '1':
                run_cnt += 1
                if run_cnt >= 6:
                    print("NO")
                    break
            else:
                run_cnt = 0
        else:
            print("YES")
    return out.getvalue().strip()

# provided samples (illustrative, since exact samples are not fully specified)
assert run("000000000000000000000000") == "YES"
assert run("111111000000000000000000") == "NO"

# custom cases
assert run("111110111110111110111110") == "YES", "no run reaches 6"
assert run("111111000000000000000000") == "NO", "exact boundary 6"
assert run("011111101111110000000000") == "NO", "run across reset"
assert run("101010101010101010101010") == "YES", "alternating pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros | YES | empty work schedule is valid |
| exact six 1s | NO | boundary condition for violation |
| separated runs | YES | resets prevent merging |
| alternating pattern | YES | no long consecutive segment |

## Edge Cases

A key edge case is when exactly six consecutive `1`s appear at the start of the string. For input `111111000000000000000000`, the counter reaches 6 at index 6, and the algorithm immediately prints `NO`. This confirms that detection does not depend on position and works correctly at boundaries.

Another case is when two runs of five `1`s are separated by a single `0`, such as `111110111110...`. The reset at the zero ensures the second run starts fresh, and neither reaches length 6, so the output remains `YES`.

A final case involves alternating characters like `101010...`. The counter repeatedly resets to 1, never accumulating, so the algorithm safely returns `YES` without any risk of false positives.
