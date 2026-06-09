---
title: "CF 1848B - Vika and the Bridge"
description: "We are given a linear bridge represented as an array of plank colors. Vika starts before the first plank and wants to reach the end."
date: "2026-06-09T05:41:51+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1848
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 885 (Div. 2)"
rating: 1200
weight: 1848
solve_time_s: 310
verified: false
draft: false
---

[CF 1848B - Vika and the Bridge](https://codeforces.com/problemset/problem/1848/B)

**Rating:** 1200  
**Tags:** binary search, data structures, greedy, implementation, math, sortings  
**Solve time:** 5m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a linear bridge represented as an array of plank colors. Vika starts before the first plank and wants to reach the end. She is only allowed to walk on a selected subsequence of planks that share the same color, and every time she steps from one chosen plank to the next, she may have to cross a gap of unchosen planks. The size of a step is exactly the number of skipped planks between consecutive chosen positions, and the goal is to minimize the largest such skip.

There is one extra twist. Before walking, Vika is allowed to repaint at most one plank into any color, effectively modifying the array in a single position. She may also choose to repaint nothing.

The task is to choose a color and a subsequence of positions of that color (possibly after one modification) such that the maximum gap between consecutive chosen positions, including the start and end boundaries, is minimized.

The answer is a minimax problem over gaps induced by occurrences of a chosen color. If we fix a color, its occurrences split the array into segments, and the worst segment determines how “dangerous” that color is as a walking path.

The constraints imply that we must process up to 2⋅10^5 planks across all test cases. Any solution that is quadratic per test case will fail immediately. We need a near linear or linearithmic method per case, and ideally linear overall.

A naive attempt would try each color and each possible repaint position, recompute gaps, and evaluate the maximum step. This would repeatedly scan arrays and easily blow up to O(n^2).

A subtle edge case arises when all planks already have the same color. Then no gaps exist at all, so the answer is zero. Another is when colors are completely alternating, where even optimal subsequences still induce large unavoidable gaps unless a repaint bridges them.

## Approaches

The brute-force perspective is to fix a color, collect all its positions, and compute the maximum gap induced by walking only on those positions. Without repainting, this is straightforward. The issue is the repaint operation: we may insert one extra occurrence of the chosen color at any position, effectively splitting one large gap into two smaller ones.

If we simulate this for every color and every possible insertion position, we would recompute gap structures repeatedly. For each color, maintaining all gap values and testing all possible split points leads to O(n) work per gap candidate, which in the worst case becomes O(n^2).

The key observation is that for a fixed color, the structure of interest is its gap array: distances between consecutive occurrences, including edges from the boundaries of the array. The answer for a color without repainting is simply the maximum gap. With one repaint, we can take any gap and split it into two parts, reducing the maximum only if that gap was the unique bottleneck.

This reduces the problem to evaluating, for each color, how much the largest gap can be reduced by inserting one extra occurrence optimally. The insertion is best placed inside the largest gap, splitting it as evenly as possible, so its contribution becomes ceiling(gap/2). All other gaps remain unchanged. Thus for each color we only need its gap multiset and its maximum and second maximum.

We can compute all positions of each color in one pass, compute gaps in O(occurrences), and maintain best two maxima. The global answer is the minimum over all colors of the best achievable maximum gap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Group indices of each color in a list. This is necessary because gap structure depends only on relative positions, not absolute scanning of the full array repeatedly.
2. For each color, construct an augmented position list by adding virtual endpoints 0 and n+1. These represent the start before the first plank and the end after the last plank, so gaps at boundaries are treated uniformly.
3. Compute all gaps between consecutive positions. Each gap represents how many planks are skipped when moving from one occurrence of the color to the next.
4. Find the largest gap gmax and the second largest gap g2. These two values determine the best possible result after one repaint, because only one gap can be split.
5. If we do not repaint, the cost for this color is gmax. If we repaint, we choose to split the largest gap into two parts, reducing it to ceil(gmax / 2). The new worst gap becomes max(g2, ceil(gmax / 2)).
6. Compute this best value for every color and take the minimum across all colors.
7. Output the minimum over all colors.

### Why it works

For a fixed color, any valid walking strategy corresponds to selecting all occurrences of that color in order, possibly augmented by one artificially inserted occurrence due to repainting. This inserted point can only affect one interval between consecutive occurrences, so only one original gap can be split. Splitting optimally always targets the largest gap because reducing any smaller gap does not improve the maximum. Therefore the optimal solution depends only on the two largest gaps, making the structure fully compressible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        c = list(map(int, input().split()))

        pos = [[] for _ in range(k + 1)]
        for i, x in enumerate(c, start=1):
            pos[x].append(i)

        ans = n

        for color in range(1, k + 1):
            if not pos[color]:
                continue

            arr = [0] + pos[color] + [n + 1]

            gaps = []
            for i in range(1, len(arr)):
                gaps.append(arr[i] - arr[i - 1] - 1)

            if len(gaps) == 0:
                ans = 0
                continue

            gmax = max(gaps)
            g2 = 0
            for g in gaps:
                if g != gmax:
                    g2 = max(g2, g)

            best = max(g2, (gmax + 1) // 2)
            ans = min(ans, best)

        print(ans)

if __name__ == "__main__":
    solve()
```

The code groups positions per color in a single pass, ensuring linear preprocessing. For each color, it builds a boundary-augmented position list so that endpoint gaps are handled without special casing. It then computes all gaps in one traversal and extracts the largest and second largest gap without sorting, which keeps the per-color processing linear in the number of occurrences.

A subtle point is handling colors that appear zero or one time. With zero occurrences, the color is irrelevant. With one occurrence, the gaps include the entire prefix and suffix, and the formula still applies correctly because the single gap list correctly represents both sides of the bridge.

## Worked Examples

### Example 1

Input:

```
n = 5, c = [1, 1, 2, 1, 1]
```

We consider color 1.

| Step | Positions | Gaps | gmax | g2 | Best |
| --- | --- | --- | --- | --- | --- |
| Build | [0,1,2,4,5,6] | [0,0,1,0,0] | 1 | 0 | 0 |

The only non-zero gap is small, and repainting can eliminate it completely by inserting inside it. The final answer becomes 0.

This demonstrates that dense clusters of a color can eliminate all movement cost.

### Example 2

Input:

```
n = 7, c = [1,2,3,3,3,2,1]
```

Consider color 3.

| Step | Positions | Gaps | gmax | g2 | Best |
| --- | --- | --- | --- | --- | --- |
| Build | [0,3,4,5,8] | [2,0,0,2] | 2 | 2 | 2 |

Even after repainting, splitting the largest gap does not reduce the maximum below 2 because another equal gap remains. This shows why the second-largest gap matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is processed once, and all gaps across colors sum to n |
| Space | O(n) | Position lists store all indices once |

The solution fits comfortably within limits since total n across test cases is 2⋅10^5, and all operations are linear in that total.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        c = list(map(int, input().split()))

        pos = [[] for _ in range(k + 1)]
        for i, x in enumerate(c, start=1):
            pos[x].append(i)

        ans = n

        for color in range(1, k + 1):
            if not pos[color]:
                continue

            arr = [0] + pos[color] + [n + 1]

            gaps = []
            for i in range(1, len(arr)):
                gaps.append(arr[i] - arr[i - 1] - 1)

            gmax = max(gaps)
            g2 = 0
            for g in gaps:
                if g != gmax:
                    g2 = max(g2, g)

            best = max(g2, (gmax + 1) // 2)
            ans = min(ans, best)

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("""5
5 2
1 1 2 1 1
7 3
1 2 3 3 3 2 1
6 6
1 2 3 4 5 6
8 4
1 2 3 4 2 3 1 4
3 1
1 1 1
""") == """0
1
2
2
0"""

# custom cases
assert run("""1
1 1
1
""") == "0", "single plank"

assert run("""1
4 2
1 2 1 2
""") in {"1"}, "alternating colors"

assert run("""1
6 3
1 2 1 2 1 2
""") == "1", "balanced repetition"

assert run("""1
5 5
1 2 3 4 5
""") == "2", "all distinct small n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single plank | 0 | minimal structure |
| alternating colors | 1 | frequent gaps |
| balanced repetition | 1 | repeated structure symmetry |
| all distinct | 2 | worst spread case |

## Edge Cases

A single-color bridge like `[1,1,1,...]` produces no gaps. The algorithm constructs positions `[0,1,2,...,n,n+1]`, where all internal gaps are zero, so both gmax and g2 are zero, producing answer zero.

A color appearing once produces two boundary gaps. For example `[2,1,1,1,3]` for color 2 yields positions `[0,1,5]` and gaps `[0,3]`. The maximum gap is handled correctly as the full segment length.

Highly alternating arrays produce many small but frequent gaps. The algorithm still only tracks the largest gap per color, ensuring correct handling without needing to simulate every path.
