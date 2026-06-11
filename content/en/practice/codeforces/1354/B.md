---
title: "CF 1354B - Ternary String"
description: "We are given multiple test cases, and each test case is a string made only of the characters 1, 2, and 3. For each string, we need to find the shortest continuous segment (substring) that contains at least one occurrence of each of the three characters."
date: "2026-06-11T13:54:17+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1354
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 87 (Rated for Div. 2)"
rating: 1200
weight: 1354
solve_time_s: 107
verified: true
draft: false
---

[CF 1354B - Ternary String](https://codeforces.com/problemset/problem/1354/B)

**Rating:** 1200  
**Tags:** binary search, dp, implementation, two pointers  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given multiple test cases, and each test case is a string made only of the characters `1`, `2`, and `3`. For each string, we need to find the shortest continuous segment (substring) that contains at least one occurrence of each of the three characters. If the string is missing any one of the digits entirely, then it is impossible to form such a substring, and the answer is zero.

A substring here is a contiguous slice of the string, so we are allowed to choose a starting index and an ending index and take everything in between. The goal is to minimize that length while still ensuring all three symbols appear at least once inside it.

The constraints are large in aggregate: the total length of all strings across test cases is up to 200,000. That immediately rules out any solution that checks all substrings explicitly. A brute-force approach that tries every pair of endpoints would require O(n²) per test case in the worst case, which is far too slow.

Edge cases appear when one or more digits are missing entirely. For example, if `s = "111111"`, the correct output is `0` because there is no `2` or `3`. Similarly, if a string contains only two of the three digits, such as `s = "112211"`, no substring can satisfy the condition.

Another subtle case is when the valid substring is not obvious from local structure. For instance, in `s = "1212123"`, the optimal segment might include a `3` that appears only once near the end, forcing the window to stretch far back.

## Approaches

A brute-force approach would examine every possible substring and check whether it contains `1`, `2`, and `3`. For each starting index `i`, we would extend the end index `j` and track whether all required characters are present. Even if we maintain frequency counts incrementally, we still examine O(n²) substrings in the worst case per test, which leads to about 10¹⁰ operations in the worst scenario. This cannot pass under the given constraints.

The key observation is that we do not need to examine all substrings independently. Instead, we only care about the shortest window that covers all three characters. This is a classic sliding window problem: once we fix a left boundary, we can move the right boundary until all characters appear, then try to shrink the window from the left while maintaining validity.

The structure of the problem guarantees that expanding the window monotonically increases coverage, and shrinking it can only reduce redundancy without losing validity until a constraint is violated. This makes a two-pointer technique sufficient. We maintain frequency counts of `1`, `2`, and `3` in the current window and adjust pointers in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) per test | O(1) | Too slow |
| Sliding Window | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently using a two-pointer sliding window.

1. Initialize two pointers `l = 0` and `r = 0`, and a frequency array `cnt` of size 4 to track occurrences of `1`, `2`, and `3`. We also keep a variable `best` initialized to a large number.
2. Expand the right pointer `r` step by step, adding `s[r]` into the frequency array. This gradually builds a candidate window.
3. After each expansion, check whether the current window contains at least one of each digit. This condition is equivalent to `cnt[1] > 0 and cnt[2] > 0 and cnt[3] > 0`.
4. Once the condition is satisfied, try shrinking the window from the left by moving `l` forward while still keeping all three digits present. Each valid shrink represents a better (or equal) candidate answer.
5. During this shrinking process, update the answer with the current window length `r - l + 1` whenever the window remains valid.
6. When the window becomes invalid again after shrinking, stop shrinking and continue expanding `r`.
7. If no valid window is ever found, return `0`.

The key idea is that every time we move `l` or `r`, we are doing so monotonically across the string, so each index is processed at most a constant number of times.

Why it works comes down to the structure of minimal windows. For any fixed right endpoint, the best possible substring ending there is obtained by pushing the left boundary as far right as possible while preserving all required characters. If we did not shrink maximally, we would carry unnecessary characters, and any shorter valid substring ending at the same `r` would be missed. Since we try all `r`, we cover all possible right boundaries for optimal substrings.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        s = input().strip()
        
        cnt = [0] * 4
        l = 0
        best = 10**9
        
        for r, ch in enumerate(s):
            x = ord(ch) - 48
            cnt[x] += 1
            
            while cnt[1] > 0 and cnt[2] > 0 and cnt[3] > 0:
                best = min(best, r - l + 1)
                cnt[ord(s[l]) - 48] -= 1
                l += 1
        
        if best == 10**9:
            print(0)
        else:
            print(best)

if __name__ == "__main__":
    solve()
```

The implementation maintains a frequency array indexed directly by digit value, which avoids any mapping overhead. The left pointer only moves forward when the window is valid, ensuring correctness while keeping the complexity linear.

A subtle detail is the update of `best` before shrinking. This ensures we record the smallest valid window for each right endpoint before potentially breaking validity by moving `l`. Another important point is initializing `best` with a sentinel value, since a valid substring might never be found.

## Worked Examples

Consider `s = "12222133333332"`.

We track how the window evolves until it first becomes valid and then shrinks.

| r | s[r] | l | window | counts (1,2,3) | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | (1,0,0) | expand |
| 1 | 2 | 0 | 12 | (1,1,0) | expand |
| 6 | 1 | 0 | 122221 | (2,4,0) | expand |
| 7 | 3 | 0 | 1222213 | (2,4,1) | valid, start shrinking |
| 7 | 3 | 1 | 222213 | (1,4,1) | still valid |
| 7 | 3 | 2 | 22213 | (1,3,1) | still valid |
| 7 | 3 | 3 | 2213 | (1,2,1) | still valid |
| 7 | 3 | 4 | 213 | (1,1,1) | record answer |

This shows how shrinking aggressively finds the true minimal window ending at `r = 7`.

Now consider `s = "31121"`.

| r | s[r] | l | window | counts (1,2,3) | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 0 | 3 | (0,0,1) | expand |
| 1 | 1 | 0 | 31 | (1,0,1) | expand |
| 2 | 1 | 0 | 311 | (2,0,1) | expand |
| 3 | 2 | 0 | 3112 | (2,1,1) | valid, shrink |
| 3 | 1 | 1 | 112 | (2,1,0) | invalid |

At this point, we recorded length 4, and later expansions do not produce a smaller valid window. This confirms the optimal answer is found by minimizing per right endpoint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | each pointer moves at most n times |
| Space | O(1) | fixed-size frequency array |

The total length across all test cases is bounded by 200,000, so a linear scan over all characters combined is sufficient. The algorithm processes each character a constant number of times, fitting comfortably within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    import sys
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            s = input().strip()
            cnt = [0]*4
            l = 0
            best = 10**9
            for r, ch in enumerate(s):
                cnt[ord(ch)-48] += 1
                while cnt[1] and cnt[2] and cnt[3]:
                    best = min(best, r-l+1)
                    cnt[ord(s[l])-48] -= 1
                    l += 1
            out.append("0" if best == 10**9 else str(best))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""7
123
12222133333332
112233
332211
12121212
333333
31121
""") == """3
3
4
4
0
0
4"""

# all same character
assert run("""1
111111
""") == "0"

# missing one digit
assert run("""1
112211
""") == "0"

# already minimal
assert run("""1
123
""") == "3"

# scattered pattern
assert run("""1
321321
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all same digits | 0 | missing required characters |
| two digits only | 0 | impossible case |
| already optimal | 3 | minimal window exists immediately |
| alternating full set | 3 | sliding window contraction correctness |

## Edge Cases

When the string lacks one of the digits entirely, the frequency condition is never satisfied, so the algorithm never enters the shrinking phase and `best` remains unchanged. For `s = "333333"`, the loop only increments counts for `3`, and no valid window is ever recorded, producing output `0`.

When the valid window exists but is much larger than the minimal one, the algorithm relies on aggressive shrinking. In `s = "12222133333332"`, once a `3` is included, the left pointer advances until the last required occurrence of `1` or `2` would be lost, ensuring the window is minimal for that right boundary. This guarantees that no redundant prefix is kept, and every candidate optimal substring is discovered during the scan.
