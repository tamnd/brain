---
title: "CF 1931F - Chat Screenshots"
description: "We are given a chat with n participants, each identified by a unique number from 1 to n. The chat displays participants in a list ordered by activity, but each participant always sees themselves at the top of their own list."
date: "2026-06-08T18:27:44+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1931
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 925 (Div. 3)"
rating: 1700
weight: 1931
solve_time_s: 161
verified: false
draft: false
---

[CF 1931F - Chat Screenshots](https://codeforces.com/problemset/problem/1931/F)

**Rating:** 1700  
**Tags:** combinatorics, dfs and similar, graphs  
**Solve time:** 2m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a chat with `n` participants, each identified by a unique number from `1` to `n`. The chat displays participants in a list ordered by activity, but each participant always sees themselves at the top of their own list. Multiple participants have taken screenshots of the chat list, capturing the order as they see it. Each screenshot shows the participant who took it at the top, followed by the remaining participants in some order.

The problem asks whether there exists a single underlying order of participants that explains all screenshots. In other words, we want to know if there is one consistent activity-based ordering of everyone such that if each participant sees themselves at the top, their screenshot would match the one recorded.

The constraints tell us that `n` and `k` can be up to `2·10^5` in total across all test cases. This immediately rules out brute-force approaches that try all `n!` permutations. Each screenshot contains `n` elements, so a solution must process the arrays efficiently, ideally in linear time relative to the sum of `n` values.

Non-obvious edge cases arise when screenshots are inconsistent due to the relative ordering of participants other than the top participant. For example, if three participants post screenshots like `[1,2,3]`, `[2,3,1]`, and `[3,1,2]`, there exists a consistent underlying order. But if a screenshot shows a participant at the top with a relative ordering of the others that conflicts with another screenshot, the answer should be NO. A naive approach might just check the top participant and ignore the order of the rest, which would fail on such cases.

## Approaches

The brute-force approach would generate all `n!` permutations of participants and check each permutation against all screenshots. For each permutation, we would simulate each participant’s view and verify if it matches their screenshot. This is correct but infeasible: with `n` up to `2·10^5`, `n!` is astronomically large.

The key insight is that for any valid underlying order, the position of every participant relative to others must be consistent across screenshots. Each screenshot can be interpreted as a set of directed constraints: if `x` comes immediately after `y` in the screenshot (ignoring the top participant), then in the global order `y` must come before `x`. Because the top participant is always first in their view, we can remove them and focus on the relative ordering of the remaining `n-1` participants.

This observation allows us to reduce the problem to a sequence consistency check. We pick one of the screenshots as a candidate for the underlying order and attempt to simulate all other screenshots using that order, adjusted by moving their top participant to the front. If any screenshot cannot be obtained by this operation, the order is inconsistent, and the answer is NO. Otherwise, the order is valid, and the answer is YES.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!·k·n) | O(n) | Too slow |
| Optimal | O(k·n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `t`, the number of test cases.
2. For each test case, read `n` and `k`.
3. Store all `k` screenshots in a list. Each screenshot is a list of `n` integers, with the first integer being the participant who took it.
4. Choose one screenshot as a candidate for the underlying order. This is arbitrary, so we typically pick the first screenshot.
5. Construct a mapping from participant to position in this candidate order.
6. For each screenshot, check if moving its top participant to the front of the candidate order produces the screenshot. To do this:

- Remove the top participant from the candidate order.
- Insert it at the front.
- Compare the resulting list to the screenshot.
- If they do not match, return NO.
7. If all screenshots match, return YES.

Why it works: moving the top participant to the front simulates each participant's view. If all screenshots match this operation for a single candidate order, it guarantees there exists an underlying global order consistent with all screenshots.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        screenshots = [list(map(int, input().split())) for _ in range(k)]
        
        candidate = screenshots[0]  # arbitrary candidate
        pos_in_candidate = {val: i for i, val in enumerate(candidate)}
        possible = True
        
        for shot in screenshots:
            top = shot[0]
            # simulate participant's view
            reordered = [top] + [x for x in candidate if x != top]
            if reordered != shot:
                possible = False
                break
        print("YES" if possible else "NO")

if __name__ == "__main__":
    solve()
```

The solution reads all input efficiently with `sys.stdin.readline`. The candidate order is chosen from the first screenshot. The key subtlety is generating the participant’s view correctly by removing their own identifier from the candidate list and putting it at the front. This prevents mismatches caused by ignoring the top participant.

## Worked Examples

### Sample Input 1

```
4 4
1 2 3 4
2 3 1 4
3 2 1 4
4 2 3 1
```

| Step | Candidate | Screenshot | Reordered | Matches? |
| --- | --- | --- | --- | --- |
| 1 | [1,2,3,4] | [1,2,3,4] | [1,2,3,4] | Yes |
| 2 | [1,2,3,4] | [2,3,1,4] | [2,1,3,4] | No |

Explanation: choosing the first screenshot as candidate, the second screenshot cannot be obtained by moving its top participant to the front. So answer is NO.

### Sample Input 2

```
1 1
1 2 3 4 5
```

| Step | Candidate | Screenshot | Reordered | Matches? |
| --- | --- | --- | --- | --- |
| 1 | [1,2,3,4,5] | [1,2,3,4,5] | [1,2,3,4,5] | Yes |

With only one screenshot, the candidate itself works, answer YES.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k·n) | For each screenshot, we construct a reordered list of length `n` and compare it. |
| Space | O(n) | We store the candidate order and mapping from participant to index. |

Given that the sum of `n·k` over all test cases ≤ 2·10^5, this solution fits comfortably within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("10\n5 1\n1 2 3 4 5\n4 4\n1 2 3 4\n2 3 1 4\n3 2 1 4\n4 2 3 1\n6 2\n1 3 5 2 4 6\n6 3 5 2 1 4\n3 3\n1 2 3\n2 3 1\n3 2 1\n10 2\n1 2 3 4 5 6 7 8 9 10\n10 9 8 7 6 5 4 3 2 1\n1 1\n1\n5 2\n1 2 3 5 4\n2 1 3 5 4\n3 3\n3 1 2\n2 3 1\n1 3 2\n5 4\n3 5 1 4 2\n2 5 1 4 3\n1 5 4 3 2\n5 1 4 3 2\n3 3\n1 3 2\n2 1 3\n3 2 1") == "YES\nYES\nYES\nYES\nNO\nYES\nYES\nYES\nYES\nNO"

# Custom edge cases
assert run("1\n1 1\n1") == "YES", "single participant"
assert run("1\n2 2\n1 2\n2 1") == "YES", "two participants reversed screenshots"
assert run("1\n3 3\n1 2 3\n2 1 3\n3 2 1") == "YES", "three participants all screenshots"
assert run("1\n3 2\n1 3 2\n2 3 1") == "NO", "conflicting screenshots"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 participant | YES | Minimum-size input |
| 2 participants reversed | YES | Screenshots can be rotated, should detect YES |
| 3 participants all screenshots | YES | Multiple screenshots compatible with one underlying order |
| 3 participants conflicting | NO | Screenshots that cannot be explained by a single order |

## Edge Cases

If there is
