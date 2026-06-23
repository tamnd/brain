---
title: "CF 105346B - Ternary Nightmare"
description: "We are given a sequence of characters consisting only of 0, 1, and 2. We want to choose a contiguous segment of this sequence such that within that segment, the number of 2 characters does not exceed a given limit k."
date: "2026-06-23T15:33:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105346
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 09-13-24 Div. 2 (Beginner)"
rating: 0
weight: 105346
solve_time_s: 81
verified: false
draft: false
---

[CF 105346B - Ternary Nightmare](https://codeforces.com/problemset/problem/105346/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of characters consisting only of `0`, `1`, and `2`. We want to choose a contiguous segment of this sequence such that within that segment, the number of `2` characters does not exceed a given limit `k`. Among all such valid segments, we want the maximum possible length.

In other words, we slide a window over the string and look for the longest stretch where the count of the digit `2` stays within the allowed budget.

The input size goes up to $10^5$, which immediately rules out any solution that tries all substrings explicitly. A brute force approach would consider $O(n^2)$ substrings, and even counting the number of `2`s inside each would push it toward $O(n^3)$ or $O(n^2)$, which is too slow for a 1 second limit. We therefore need a linear or near-linear method, typically something that processes the string in one pass.

The main subtle failure case for naive reasoning is forgetting that the best segment may include multiple stretches of valid windows, and that shrinking from the wrong side can lose optimal answers. For example, if `k = 1` and the string is `220202`, a naive approach might greedily skip too many positions and miss longer valid windows that start after removing early `2`s.

## Approaches

The brute-force strategy is straightforward: enumerate every possible substring, count how many `2`s it contains, and track the maximum length among those where the count is at most `k`. For each starting index, we extend the end pointer and maintain a counter. This leads to roughly $n$ starting positions, and for each we may scan up to $n$ characters, resulting in $O(n^2)$ time. This is already too large when $n = 10^5$, since it would require on the order of $10^{10}$ operations.

The structure of the problem suggests a more efficient approach because the condition we enforce is monotonic: once a segment becomes invalid by exceeding `k` occurrences of `2`, extending it further only makes it worse. This is exactly the setting where a sliding window works well. Instead of recomputing counts for every substring, we maintain a single window `[l, r]` and track how many `2`s are inside it. We expand `r` step by step, and whenever the window violates the constraint, we move `l` forward until it becomes valid again.

This turns the problem into a single linear scan where each character enters and leaves the window at most once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Sliding Window | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We maintain a window `[l, r]` over the string and a counter `cnt2` storing how many `2`s are currently inside the window.

1. Initialize `l = 0`, `cnt2 = 0`, and `best = 0`. We start with an empty window and gradually build valid segments.
2. Iterate `r` from `0` to `n - 1`. Each time we include `s[r]` into the current window.
3. If `s[r] == '2'`, increment `cnt2`. This tracks whether we are consuming part of our limited budget.
4. If `cnt2 > k`, the window is invalid. We must shrink it from the left until it becomes valid again. We do this by moving `l` forward and subtracting from `cnt2` whenever we remove a `2`.
5. After restoring validity, the current window `[l, r]` satisfies the constraint, so we update `best = max(best, r - l + 1)`.
6. Continue until `r` reaches the end of the string. The answer is `best`.

The key idea is that `l` only moves forward, never backward, which ensures linear behavior.

### Why it works

At every position `r`, the algorithm maintains the invariant that the window `[l, r]` contains at most `k` occurrences of `2`, and that `l` is the smallest index that makes this true for the current `r`. Because any larger window ending at `r` would only increase or maintain the number of `2`s, any invalid extension must be corrected by moving `l` right. This guarantees that no valid candidate window ending at `r` is missed, since all smaller valid prefixes are implicitly considered as `l` advances.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    s = input().strip()

    l = 0
    cnt2 = 0
    best = 0

    for r in range(n):
        if s[r] == '2':
            cnt2 += 1

        while cnt2 > k:
            if s[l] == '2':
                cnt2 -= 1
            l += 1

        best = max(best, r - l + 1)

    print(best)

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the sliding window logic. The only detail that matters is that the shrinking loop must fully restore validity before updating the answer, otherwise we might count invalid segments. The pointer `l` is never reset, which preserves linear complexity.

## Worked Examples

### Example 1

Input:

```
n = 6, k = 1
s = 120202
```

We track the window as `r` increases.

| r | char | l | cnt2 | window | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 1 | 1 |
| 1 | 2 | 0 | 1 | 12 | 2 |
| 2 | 0 | 0 | 1 | 120 | 3 |
| 3 | 2 | 0 | 2 → shrink | 1 | 3 |
|  |  | 1 | 1 | 202 | 3 |
| 4 | 0 | 1 | 1 | 2020 | 4 |
| 5 | 2 | 1 | 2 → shrink | 2 | 4 |
|  |  | 2 | 1 | 0202 | 4 |

The best valid window length is 4. This shows how invalid windows are repaired by moving `l` forward until the constraint is restored.

### Example 2

Input:

```
n = 5, k = 0
s = 10202
```

| r | char | l | cnt2 | window | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 1 | 1 |
| 1 | 0 | 0 | 0 | 10 | 2 |
| 2 | 2 | 2 | 0 | 2 | 2 |
| 3 | 0 | 2 | 0 | 20 | 2 |
| 4 | 2 | 4 | 0 | 2 | 2 |

This trace shows that when `k = 0`, every `2` forces a full reset of the window start.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each index is visited at most twice, once by `r` and once by `l` |
| Space | $O(1)$ | Only counters and pointers are used |

The linear scan fits comfortably within the $10^5$ constraint and easily meets the time limit since each character triggers only constant work.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    s = input().strip()

    l = 0
    cnt2 = 0
    best = 0

    for r in range(n):
        if s[r] == '2':
            cnt2 += 1
        while cnt2 > k:
            if s[l] == '2':
                cnt2 -= 1
            l += 1
        best = max(best, r - l + 1)

    return str(best)

assert run("16 3\n1201012200120012\n") == "13", "sample 1"

assert run("1 0\n0\n") == "1", "single zero"
assert run("5 0\n11111\n") == "5", "no twos at all"
assert run("5 1\n22222\n") == "1", "all twos k=1"
assert run("6 2\n221221\n") == "6", "full window allowed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single zero | 1 | minimal length case |
| no twos | 5 | window never shrinks |
| all twos k=1 | 1 | constant shrinking behavior |
| full window allowed | 6 | no shrink needed |

## Edge Cases

A key edge case is when `k = 0`, meaning no `2` is allowed at all. For an input like `10202`, the algorithm continuously shrinks whenever a `2` is encountered. At `r = 2`, we hit the first `2`, forcing `l` to move to `2`, and the window resets. This shows the algorithm does not accumulate invalid state, since `cnt2` is immediately corrected.

Another case is when the string contains fewer than or equal to `k` occurrences of `2` in total, such as `s = 1112011` with `k = 2`. In this situation, `cnt2` never exceeds `k`, so `l` never moves. The algorithm effectively returns `n`, since the entire string is valid.
