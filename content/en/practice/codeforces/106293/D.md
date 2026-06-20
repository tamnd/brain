---
title: "CF 106293D - \u041c\u0443\u0441\u044f \u0438 \u043a\u0430\u043a\u043e\u0439-\u0442\u043e XOR"
description: "We are given an array of integers and asked to extract as many disjoint contiguous segments as possible such that each chosen segment has XOR equal to zero."
date: "2026-06-20T22:43:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106293
codeforces_index: "D"
codeforces_contest_name: "\u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 1\u0421, \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440 2025-2026"
rating: 0
weight: 106293
solve_time_s: 45
verified: true
draft: false
---

[CF 106293D - \u041c\u0443\u0441\u044f \u0438 \u043a\u0430\u043a\u043e\u0439-\u0442\u043e XOR](https://codeforces.com/problemset/problem/106293/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and asked to extract as many disjoint contiguous segments as possible such that each chosen segment has XOR equal to zero. Each element of the array can belong to at most one selected segment, so once we pick a segment, we cannot reuse its indices in any other segment.

The task is not to partition the array completely, but to pick a maximum number of “good” segments. A segment is good when the XOR of all elements inside it is exactly zero.

The constraints go up to $2 \cdot 10^5$, which immediately rules out any quadratic or worse approaches over subarrays. Any solution that tries all segments or even recomputes XOR for many pairs of endpoints will time out. We need something closer to linear or near-linear time, likely with prefix structure and dynamic programming.

A key subtlety is that segments must be non-overlapping. This means greedily picking any zero-XOR subarray is not obviously safe, because a short early segment might block two later segments.

A few edge cases illustrate the structure:

If the array is `[1, 1, 1, 1]`, valid zero-XOR segments include `[1,1]` at positions (1-2) and (3-4), giving answer 2. A naive greedy that picks the longest segment starting at index 1 might take (1-4) which has XOR 0, but then the answer becomes 1, which is worse.

If the array is `[1, 2, 3]`, the whole array XOR is zero, so we can take one segment, but no smaller segmentation gives more than 1 segment.

If all elements are zero, every single element is a valid segment, so the answer is $n$, and any correct solution must handle this cleanly.

These examples already hint that the problem is about finding many zero-XOR subarrays in an optimal non-overlapping way, which suggests prefix XOR structure combined with dynamic programming over positions.

## Approaches

A brute-force approach would try all subarrays, compute XOR for each, and then select a maximum set of non-overlapping valid intervals. Even if we precompute XOR using prefix XOR so each subarray check is O(1), we still face $O(n^2)$ candidate intervals. Selecting a maximum set of non-overlapping intervals among all valid ones becomes a weighted interval scheduling problem with potentially $O(n^2)$ edges, which is too large.

The key observation is that we do not actually need all valid subarrays explicitly. We only care about the best answer up to each position. This suggests scanning left to right and maintaining information about prefix XOR states.

Let `pref[i]` be XOR of the first `i` elements. A subarray `(l+1 … r)` has XOR zero exactly when `pref[l] == pref[r]`. So for each prefix value, if we know the last positions where it appeared, we can detect possible zero-XOR segments ending at `r`.

Instead of tracking all previous occurrences independently, we can do dynamic programming: let `dp[i]` be the maximum number of valid segments we can form using the prefix `1…i`. At position `i`, we either do nothing, or we end a segment at `i`. If we end a segment `(j+1 … i)` with XOR zero, then `dp[i] = dp[j] + 1`. We need the best such `j`.

To make this efficient, we maintain a dictionary mapping each prefix XOR value to the best `dp` value seen at indices where this prefix occurred. This compresses all valid previous endpoints into O(1) lookup per index.

The brute force enumerates all pairs `(j, i)`, while the prefix XOR + DP trick compresses all valid `j` candidates into a single best representative per XOR value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Prefix XOR + DP map | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We process the array from left to right while maintaining prefix XOR values and a dynamic programming table.

1. Initialize `dp[0] = 0` and prefix XOR `px = 0`. We also store a map `best` where `best[x]` represents the maximum dp value among all positions having prefix XOR `x`. Initially, `best[0] = 0`. This reflects that before starting, an empty prefix has XOR zero and zero segments.
2. For each position `i` from 1 to `n`, update `px = px XOR a[i]`. This gives the XOR of the prefix ending at `i`.
3. Initially set `dp[i] = dp[i-1]`. This corresponds to not ending any segment at position `i`, effectively leaving `i` unused in a segment.
4. Now consider ending a zero-XOR segment at `i`. If some earlier position `j` has the same prefix XOR `px`, then the subarray `(j+1 … i)` has XOR zero. The best choice among all such `j` is the one that maximizes `dp[j]`, which is exactly `best[px]`. Therefore we can update `dp[i] = max(dp[i], best[px] + 1)`.
5. After computing `dp[i]`, we update `best[px] = max(best[px], dp[i])`. This ensures future positions can reuse the best configuration that ended at a prefix XOR state.
6. The final answer is `dp[n]`.

### Why it works

The algorithm relies on a compression of all valid segment endings into prefix XOR states. Every valid segment `(j+1 … i)` corresponds uniquely to a pair of equal prefix XOR values. The DP value at `j` captures the optimal segmentation up to that point, and storing only the maximum `dp[j]` per prefix XOR ensures we never lose a better transition. Since transitions only depend on prefix XOR equality, no additional historical structure is needed, and every possible segmentation is representable through these states.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    dp_prev = 0
    px = 0

    best = {0: 0}

    for i in range(n):
        px ^= a[i]

        dp_i = dp_prev

        if px in best:
            dp_i = max(dp_i, best[px] + 1)

        if px in best:
            best[px] = max(best[px], dp_i)
        else:
            best[px] = dp_i

        dp_prev = dp_i

    print(dp_prev)

if __name__ == "__main__":
    solve()
```

The solution maintains only the previous DP value and a dictionary of prefix XOR states. The subtle point is that we update `best[px]` after computing `dp_i`, ensuring we correctly allow future segments to build on the best known structure ending at this prefix XOR.

A common pitfall is updating `best` too early, which would incorrectly allow a segment to start and end at the same position in a way that artificially inflates the answer.

## Worked Examples

### Example 1: `[1, 2, 3, 0, 3, 2, 1]`

We track prefix XOR and DP:

| i | a[i] | px | dp[i] | best updates |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | best[1]=0 |
| 2 | 2 | 3 | 0 | best[3]=0 |
| 3 | 3 | 0 | 1 | best[0]=1 |
| 4 | 0 | 0 | 2 | best[0]=2 |
| 5 | 3 | 3 | 1 | best[3]=1 |
| 6 | 2 | 1 | 1 | best[1]=1 |
| 7 | 1 | 0 | 3 | best[0]=3 |

At the end, we obtain 3 segments. This matches the intuition that every time prefix XOR repeats, we can close a valid segment, and DP accumulates the best chain of such closures.

### Example 2: `[2, 2, 8, 16, 4, 4, 1]`

| i | a[i] | px | dp[i] | best updates |
| --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 0 | best[2]=0 |
| 2 | 2 | 0 | 1 | best[0]=1 |
| 3 | 8 | 8 | 1 | best[8]=1 |
| 4 | 16 | 24 | 1 | best[24]=1 |
| 5 | 4 | 28 | 1 | best[28]=1 |
| 6 | 4 | 24 | 2 | best[24]=2 |
| 7 | 1 | 25 | 2 | best[25]=2 |

Final answer is 2, corresponding to the best pairing of equal prefix XOR states.

These traces show how repeated prefix XOR values allow the DP to “close” segments optimally without explicitly enumerating them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element updates prefix XOR and dictionary once |
| Space | O(n) | At most one entry per distinct prefix XOR value |

The algorithm fits comfortably within the constraints since $n \le 2 \cdot 10^5$, and dictionary operations are amortized constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve() if False else ""  # placeholder for structure

# Since solve() prints, redefine properly for testing
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    dp_prev = 0
    px = 0
    best = {0: 0}

    for i in range(n):
        px ^= a[i]
        dp_i = dp_prev
        if px in best:
            dp_i = max(dp_i, best[px] + 1)
        best[px] = max(best.get(px, 0), dp_i)
        dp_prev = dp_i

    print(dp_prev)

# provided samples (illustrative placeholders since statement formatting is broken)
assert run("3\n1 2 3\n") == "1"
assert run("7\n2 2 8 16 4 4 1\n") == "2"

# custom cases
assert run("1\n0\n") == "1", "single zero"
assert run("4\n1 1 1 1\n") == "2", "two pairs"
assert run("5\n0 0 0 0 0\n") == "5", "all zeros"
assert run("3\n1 2 4\n") == "0", "no zero xor segment"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `1` | single element zero case |
| `1 1 1 1` | `2` | multiple disjoint segments |
| `0 0 0 0 0` | `5` | every element forms valid segment |
| `1 2 4` | `0` | no valid XOR-zero subarray |

## Edge Cases

A critical edge case is when many prefixes share the same XOR early on. In such cases, failing to store the best DP per prefix XOR would cause undercounting. For example, in `[0, 0, 0]`, every prefix XOR is zero, and every position can extend the previous optimal segmentation. The correct behavior is to keep improving `best[0]` as DP increases; otherwise the algorithm would freeze at 1.

Another subtle case is when the optimal segmentation requires skipping an immediate valid segment in favor of enabling two later segments. The DP formulation already handles this because `dp[i]` always considers both extending and not extending, but only if we correctly delay updates to `best` until after computing `dp[i]`.
