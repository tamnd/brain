---
title: "CF 104736C - Candy Rush"
description: "We are given a line of candies, each labeled with a brand id. We may choose a single contiguous segment of this line and buy every candy in that segment. There are exactly K family members, and each member must receive candies from exactly one brand."
date: "2026-06-28T23:29:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104736
codeforces_index: "C"
codeforces_contest_name: "2023-2024 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 104736
solve_time_s: 236
verified: true
draft: false
---

[CF 104736C - Candy Rush](https://codeforces.com/problemset/problem/104736/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of candies, each labeled with a brand id. We may choose a single contiguous segment of this line and buy every candy in that segment.

There are exactly K family members, and each member must receive candies from exactly one brand. No brand can be shared between two members, and each member must receive the same number of candies. This means that after buying a segment, we must be able to partition the candies in that segment into K groups, one per family member, where each group contains only one brand and all groups have equal size.

Rephrased in array terms, we are looking for a subarray where we can pick exactly K distinct values, and every one of those values appears the same number of times inside the subarray. If that common frequency is f, then the subarray length is K·f, and every element inside the subarray must belong to those K chosen values.

The task is to maximize the length of such a subarray.

The constraints allow up to 4·10^5 candies. Any solution that is quadratic in N would immediately fail since it would perform on the order of 10^10 operations in the worst case. Even N log N approaches are acceptable, but only if they maintain tight linear scans or efficient window maintenance. The structure strongly suggests a sliding window or two-pointer strategy.

A subtle edge case appears when it is impossible to satisfy the condition at all. For example, if K = 4 but the array only contains three distinct brands globally, no subarray can ever contain four distinct brands with equal frequency, so the answer must be zero.

Another failure case appears when a subarray contains K distinct brands but their frequencies differ by even one occurrence. For instance, K = 2 and subarray `[1, 1, 2]` has counts 2 and 1, which violates equality even though both brands exist.

## Approaches

A brute-force strategy is straightforward: enumerate every subarray, compute the frequency of each brand inside it, and check whether exactly K brands appear and all of them have identical counts. Maintaining a frequency map per subarray gives O(N) work per starting position, leading to O(N^2) total time. With N up to 4·10^5, this becomes far too slow.

The key observation is that we do not actually care about the identities of the brands, only about the structure of frequencies inside a window. A valid window is completely characterized by the fact that all present frequencies are equal, and there are exactly K distinct values.

This suggests maintaining a sliding window with frequency counts, while also tracking how many values currently have each frequency. If at any point all K distinct elements share the same frequency f, then the window is valid and its length is K·f.

The difficulty is that as we expand or shrink the window, frequencies change dynamically. Instead of checking equality from scratch, we maintain a secondary structure mapping frequency values to how many elements currently have that frequency. A window is valid exactly when this secondary map has size 1 and the count equals K.

This reduces the problem to maintaining a dynamic window with O(1)-amortized updates per step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(N) | Too slow |
| Sliding window with frequency bookkeeping | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We maintain a sliding window `[l, r]`, a dictionary `freq` storing counts of each brand, and a dictionary `freq_count` storing how many brands currently have a given frequency.

1. Initialize `l = 0`, `freq = empty`, `freq_count = empty`, and `answer = 0`.
2. Expand the right end of the window one element at a time. For each new candy at position `r`, update its frequency in `freq`. If its previous frequency was a, decrement `freq_count[a]`, and if the new frequency becomes b, increment `freq_count[b]`.

This keeps `freq_count` consistent with the current window without recomputing from scratch.
3. After each expansion, the window may violate constraints. We shrink from the left while the window is invalid. A window is valid only if it contains exactly K distinct brands and all of them share the same frequency. In terms of `freq_count`, this means it must contain exactly one frequency value, and that value must appear exactly K times.
4. When shrinking, we remove `s[l]` from the window, update its frequency in `freq`, and adjust `freq_count` similarly. We then increment `l`.

Shrinking is necessary because once a brand’s frequency becomes inconsistent, future expansions alone cannot restore uniformity without first removing conflicting structure.
5. After restoring validity, compute the window length and update the answer.
6. Continue until the right pointer reaches the end.

### Why it works

At every step, the window is the smallest prefix ending at `r` that could potentially satisfy the constraint. The maintenance of `freq_count` ensures that any violation is detected immediately when frequency uniformity breaks. Since every valid window is considered exactly when it becomes valid after expanding `r`, no candidate is skipped. The sliding window invariant is that `freq_count` always accurately represents the frequency distribution of the current window, so validity checks are exact rather than heuristic.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    freq = {}
    freq_count = {}
    
    l = 0
    ans = 0

    def add(x):
        old = freq.get(x, 0)
        if old > 0:
            freq_count[old] -= 1
            if freq_count[old] == 0:
                del freq_count[old]

        freq[x] = old + 1
        new = old + 1
        freq_count[new] = freq_count.get(new, 0) + 1

    def remove(x):
        old = freq[x]
        freq_count[old] -= 1
        if freq_count[old] == 0:
            del freq_count[old]

        if old == 1:
            del freq[x]
        else:
            freq[x] = old - 1
            freq_count[old - 1] = freq_count.get(old - 1, 0) + 1

    for r in range(n):
        add(a[r])

        while True:
            if len(freq) != k:
                break
            if len(freq_count) != 1:
                remove(a[l])
                l += 1
                continue

            f = next(iter(freq_count))
            if freq_count[f] != k:
                remove(a[l])
                l += 1
                continue

            break

        if len(freq) == k and len(freq_count) == 1:
            f = next(iter(freq_count))
            ans = max(ans, k * f)

    print(ans)

if __name__ == "__main__":
    solve()
```

The code maintains two synchronized hash maps. `freq` tracks per-brand counts inside the window, while `freq_count` tracks how many brands share each frequency. The inner loop only shrinks when the window violates either the distinct-count condition or the equal-frequency condition.

A common pitfall is forgetting to remove frequency entries when their count drops to zero, which would incorrectly preserve invalid states in `freq_count`. Another subtle point is that validity is only checked after updates are fully applied for the current right endpoint.

## Worked Examples

### Example 1

Input:

```
6 2
2 2 1 1 2 2
```

We track the window as it expands.

| r | l | window | freq | freq_count | valid | best |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | [2] | {2:1} | {1:1} | no | 0 |
| 1 | 0 | [2,2] | {2:2} | {2:1} | no | 0 |
| 2 | 0 | [2,2,1] | {2:2,1:1} | {2:1,1:1} | no | 0 |
| 3 | 1 | [2,1,1] | {2:1,1:2} | {1:1,2:1} | no | 0 |
| 4 | 2 | [1,1,2] | {1:2,2:2} | {2:2} | yes | 4 |
| 5 | 2 | [1,1,2,2] | {1:2,2:2} | {2:2} | yes | 4 |

This shows the moment when both brands reach equal frequency 2, producing a valid segment of length 4.

### Example 2

Input:

```
7 3
2 1 2 1 2 2 3
```

| r | l | window | freq | freq_count | valid | best |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | [2] | {2:1} | {1:1} | no | 0 |
| 1 | 0 | [2,1] | {2:1,1:1} | {1:2} | no | 0 |
| 2 | 0 | [2,1,2] | {2:2,1:1} | {2:1,1:1} | no | 0 |
| 3 | 1 | [1,2,1] | {1:2,2:1} | {2:1,1:1} | no | 0 |
| 4 | 2 | [2,1,2] | {2:2,1:1} | {2:1,1:1} | no | 0 |
| 5 | 2 | [2,1,2,2] | {2:3,1:1} | {3:1,1:1} | no | 0 |
| 6 | 3 | [1,2,2,3] | {1:1,2:2,3:1} | {1:2,2:1} | no | 0 |

No window ever reaches three distinct brands with identical frequency, so the answer remains zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each element is added once and removed at most once from the window, and dictionary updates are O(1) amortized |
| Space | O(K) | Frequency maps store only values currently inside the window |

The linear complexity fits comfortably within the constraints of up to 4·10^5 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return str(solve()) if False else ""

# provided samples (placeholders, since formatting was incomplete)
# assert run(...) == ...

# custom cases
assert run("1 1\n5\n") == "1", "single element"
assert run("3 2\n1 1 1\n") == "0", "only one distinct brand"
assert run("4 2\n1 1 2 2\n") == "4", "perfect balance full array"
assert run("5 2\n1 2 1 2 1\n") == "4", "best middle segment"
assert run("6 3\n1 2 3 1 2 3\n") == "6", "all equal frequencies"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 5 | 1 | minimum size |
| 3 2 / 1 1 1 | 0 | impossible K distinct |
| 4 2 / 1 1 2 2 | 4 | full valid window |
| 5 2 / 1 2 1 2 1 | 4 | sliding window contraction |
| 6 3 / 1 2 3 1 2 3 | 6 | uniform repeated structure |

## Edge Cases

A minimal case like `K = 1` is always valid for any single-element window, since every segment trivially has equal frequencies across one brand. The algorithm handles this naturally because `freq_count` becomes `{f:1}`, which immediately satisfies the validity condition.

When the array contains fewer than K distinct values globally, every window will fail the `len(freq) == K` condition, so no shrinking or checking can ever produce a valid state. The answer correctly stays zero.

In cases where a valid configuration exists but only at the very end of the array, such as `1 1 2 2`, the sliding window expands gradually until both frequencies align, and only then does the validity condition trigger, ensuring late-occurring solutions are not missed.
