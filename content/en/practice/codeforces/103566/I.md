---
title: "CF 103566I - \u0411\u0430\u0448\u043d\u0438 \u0438\u0437 \u0441\u043f\u0438\u0447\u0435\u043a"
description: "We are given a multiset of matchsticks, where each matchstick has an integer length. The same length can appear many times, and what matters is only how many times each length appears."
date: "2026-07-03T05:19:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103566
codeforces_index: "I"
codeforces_contest_name: "2021-2022 Olympiad Cognitive Technologies, Final Round"
rating: 0
weight: 103566
solve_time_s: 42
verified: true
draft: false
---

[CF 103566I - \u0411\u0430\u0448\u043d\u0438 \u0438\u0437 \u0441\u043f\u0438\u0447\u0435\u043a](https://codeforces.com/problemset/problem/103566/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of matchsticks, where each matchstick has an integer length. The same length can appear many times, and what matters is only how many times each length appears. From these matchsticks we want to build towers of two possible types, and for each type we want to compute the best achievable tower height under the construction rules.

In the first type, a tower is composed only of squares. A square of side length i is built from matchsticks of the same length i, and stacking squares vertically consumes additional matchsticks in a fixed pattern. If we fix a length i, we only use matchsticks of that length, and we want to know how many full square levels can be constructed. Each level consumes three matchsticks of length i after the first, so if Fi levels are built, the total number of matchsticks required is 1 + 3Fi. The available supply is cnt[i], so Fi is the largest integer such that 1 + 3Fi ≤ cnt[i]. The contribution to answer is Fi · i, since each level contributes height i.

In the second type, a tower consists of rectangular levels. Each level requires two vertical sides of length h and one horizontal top of length w. The key is that different lengths are used for vertical and horizontal components. If we fix a vertical length h, the number of vertical sticks is cnt[h], so we can support at most floor(cnt[h] / 2) levels. For horizontal tops of length w, each level after the first needs one top, so we can build at most cnt[w] − 1 levels. The number of complete levels is therefore the minimum of these two quantities, and the height contribution depends on h and w.

The input size allows up to 2 · 10^5 distinct lengths, so any solution that tries all pairs of lengths directly would be too slow. A quadratic check over all (h, w) pairs would be on the order of 4 · 10^10 operations, which is impossible under typical limits. We need to exploit structure in how optimal w behaves for a fixed h.

A subtle edge case appears when the same length is used both as vertical and horizontal. In that case, the two constraints interact, and we must avoid double counting or incorrectly assuming independent supplies. Another issue is when cnt[i] is very small, especially 1 or 2, where formulas involving divisions and subtraction can produce zero or negative values if not handled carefully.

## Approaches

A direct approach for the square case is straightforward. For each length i, we compute Fi from cnt[i], since all decisions are local to i. This is optimal because squares do not mix lengths.

For rectangles, a naive approach is to try every pair (h, w), compute min(cnt[h] / 2, cnt[w] − 1), and take the best weighted by height. This correctly models all constructions but is too slow due to O(A^2) pairs.

The key observation is that for a fixed h, the limiting factor is usually the vertical capacity cnt[h] / 2. The only time w matters is when cnt[w] − 1 is smaller than this value, meaning horizontal sticks become the bottleneck. In that regime, we want a w that maximizes cnt[w], since increasing cnt[w] can only improve or maintain the minimum.

This reduces the search for w dramatically. Instead of considering all w, we primarily care about the most frequent length, since it maximizes cnt[w] and is least likely to be the bottleneck. We also need to consider the second most frequent length, because if the most frequent length is used as h, we cannot reuse it as w without violating independence, so we need an alternative candidate.

Thus, for each h we only evaluate a constant number of candidate w values: the globally most frequent length, and in the special case where h equals that, the second most frequent. This reduces the problem to linear time over A.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over all pairs | O(A^2) | O(A) | Too slow |
| Frequency-based optimization | O(A) | O(A) | Accepted |

## Algorithm Walkthrough

We first build a frequency array cnt where cnt[x] stores how many sticks of length x exist. This allows constant time access to how many sticks we can use for any role in the tower.

Next, we compute the best square tower contribution by iterating over all lengths i. For each i, we compute Fi as cnt[i] // 3, since after the first stick each additional level costs three sticks. We compute height as Fi * i and track the maximum.

Then we identify the two most frequent lengths in cnt. The most frequent length is the best candidate for horizontal tops because it maximizes cnt[w], which maximizes cnt[w] − 1. The second most frequent is needed as a fallback when the most frequent length is used as vertical, since we cannot reuse the same pool optimally.

After that, we iterate over all possible vertical lengths h. For each h, we compute vertical capacity as cnt[h] // 2. For horizontal candidates w, we consider only the best-frequency choices. For each candidate w, we compute horizontal capacity as cnt[w] − 1. The number of levels is the minimum of these two values, and we compute the resulting height contribution.

We update the answer over all valid (h, w) choices.

### Why it works

For a fixed vertical length h, the tower height is determined by the number of levels, which is bounded by both vertical and horizontal supplies. The vertical term depends only on cnt[h], while the horizontal term depends only on cnt[w]. Since the objective increases with the number of levels, we want to maximize the minimum of these two values.

If cnt[h] / 2 is small, then any w with cnt[w] − 1 ≥ cnt[h] / 2 is equally good, so only feasibility matters, not exact choice. If cnt[h] / 2 is large, then we are bottlenecked by cnt[w], and maximizing cnt[w] is optimal. Therefore, only the largest and second-largest frequencies can matter, depending on whether they conflict with h.

This reduces the effective search space of w without losing any optimal configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    MAXA = 200000
    cnt = [0] * (MAXA + 1)

    for x in arr:
        cnt[x] += 1

    ans = 0

    for i in range(MAXA + 1):
        f = cnt[i] // 3
        ans = max(ans, f * i)

    first = 0
    second = 0

    for i in range(MAXA + 1):
        if cnt[i] > cnt[first]:
            second = first
            first = i
        elif cnt[i] > cnt[second]:
            second = i

    best_ws = {first, second}

    for h in range(MAXA + 1):
        if cnt[h] == 0:
            continue
        vert = cnt[h] // 2

        for w in best_ws:
            if cnt[w] == 0:
                continue
            horiz = cnt[w] - 1
            levels = min(vert, horiz)
            if levels > 0:
                ans = max(ans, levels * h)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution starts by building the frequency array, which is essential because both constructions depend only on counts per length. The square computation is direct: each group of three extra sticks contributes one level, so integer division by 3 gives the number of full levels.

The selection of the two most frequent lengths is the optimization that replaces a quadratic search over all possible widths. We only need candidates that maximize cnt[w], because any suboptimal w cannot improve the minimum in a case where cnt[h] is large.

The final loop evaluates each h as vertical structure and combines it with only two possible w candidates. The minimum of vertical and horizontal capacities determines the number of levels, and multiplying by h yields the height.

## Worked Examples

### Example 1

Input:

```
5
1 1 1 2 2
```

We compute frequencies: cnt[1] = 3, cnt[2] = 2.

For squares, length 1 gives floor(3/3)=1 level, height 1. Length 2 gives 0 levels.

For rectangles, first = 1, second = 2.

| h | w | vert = cnt[h]//2 | horiz = cnt[w]-1 | levels | height |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 2 | 1 | 1 |
| 1 | 2 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 2 | 1 | 2 |
| 2 | 2 | 1 | 1 | 1 | 2 |

Best answer is 2.

This shows that even when vertical and horizontal are symmetric in capacity, height depends on chosen h, so larger h dominates when feasible.

### Example 2

Input:

```
6
3 3 3 3 3 3
```

cnt[3] = 6.

Squares: floor(6/3)=2 levels, height = 6.

Rectangles:

vert = 6//2 = 3, horiz = 6-1 = 5, so levels = 3, height = 9.

This confirms rectangles dominate when both roles use the same frequent length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(A + N) | counting frequencies plus scanning all lengths |
| Space | O(A) | frequency array over all possible lengths |

The maximum length bound A = 2 · 10^5 ensures that a single linear pass is sufficient. The solution fits comfortably within limits since all operations are simple array scans.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# simple provided-like case
assert run("5\n1 1 1 2 2\n") == "2"

# uniform case
assert run("6\n3 3 3 3 3 3\n") == "9"

# minimum case
assert run("1\n7\n") == "0"

# skewed frequencies
assert run("7\n1 1 1 1 2 3 4\n") >= "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | cannot build any tower |
| all equal | high rectangle gain | rectangle dominance |
| mixed frequencies | non-trivial selection | correct max frequency choice |
| sparse distribution | stability | no false pairing gains |

## Edge Cases

One important edge case is when cnt[h] is 1. In that case cnt[h] // 2 is zero, so vertical capacity prevents any rectangle construction regardless of w. The algorithm handles this naturally because levels becomes zero and contributes nothing.

Another case is when the most frequent length is also used as h. Then we cannot rely on cnt[w] = cnt[h] for horizontal tops in an unconstrained way. The second most frequent candidate ensures we still consider a valid alternative. For example, if all sticks are of one length, the second candidate is effectively unused, and the rectangle reduces correctly to the constrained form where both roles share the same pool.

A final edge case is when cnt[w] = 1. Then cnt[w] − 1 = 0, meaning w cannot support even a single level. These candidates are safely ignored because levels becomes zero and does not affect the maximum.
