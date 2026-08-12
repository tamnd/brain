---
title: "CF 102318H - Maximum NOI Subseq"
description: "The problem asks us to process an integer array and, for every possible value of (k), determine how many array elements can be selected into a collection of increasing subsequences. Every selected subsequence must contain at least (k) elements."
date: "2026-08-13T05:24:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102318
codeforces_index: "H"
codeforces_contest_name: "UCF Locals 2017"
rating: 0
weight: 102318
solve_time_s: 240
verified: true
draft: false
---

[CF 102318H - Maximum NOI Subseq](https://codeforces.com/problemset/problem/102318/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to process an integer array and, for every possible value of (k), determine how many array elements can be selected into a collection of increasing subsequences.

Every selected subsequence must contain at least (k) elements. Two selected subsequences must be non-overlapping in the original array. If one subsequence uses positions from (i) through (j), another subsequence cannot use any position between (i) and (j), even if that position is not itself selected. The objective is to maximize the total number of selected elements across all subsequences. The required output contains one answer for every (k) from (1) through (n). This is the exact formulation used by the original UCF Locals problem, where (n\le100) and there can be up to 50 test cases.

The small value (n\le100) changes the algorithmic target substantially. A cubic algorithm performs around (100^3=10^6) basic operations for one test case, which is entirely reasonable, even when repeated for all 50 cases in a compiled implementation. An exponential algorithm is already hopeless at (n=100), since (2^{100}) is about (1.27\times10^{30}). The intended solution consequently uses dynamic programming with (O(n^3)) work. The official contest review also describes an (O(n^3)) preprocessing phase for all interval LIS values followed by another (O(n^3)) dynamic program.

There are several edge cases that can make a simpler implementation incorrect. If the array has one element, for example `1 5`, the only valid answer is `1`, because for (k=1) that element forms a subsequence by itself. For (k>1) there is no valid subsequence, but there are no such values of (k) when (n=1), so the output is simply `1`. An implementation that initializes every answer to zero without handling single-element intervals would fail here.

Repeated values are another boundary case because the subsequences must be strictly increasing. For the input `3 / 1 1 1`, the correct output is `3 0 0`. For (k=1), each individual element can form its own subsequence, giving three selected elements. For (k=2), however, no two equal elements form a strictly increasing subsequence. A careless LIS transition using `<=` instead of `<` would incorrectly claim that the array contains an increasing subsequence of length three.

A third edge case occurs when the best collection does not use the final array element. Consider `5 / 2 9 1 3 4`. For (k=2), the subsequences `[2, 9]` and `[3, 4]` select four elements, while the last element is already part of `[3,4]` here. More generally, an optimal solution for a prefix may leave its final position unused. The prefix DP must consequently allow the transition `dp[i] = dp[i-1]`. An implementation that insists that the final element belongs to the final subsequence can lose valid solutions.

Finally, different subsequences cannot merely be disjoint in their selected indices. Their entire index ranges must be disjoint. In `2 1 9 3 4 4 5 6` with (k=2), the optimal solution is `[2,9]`, `[3,4]`, `[4,5,6]`, giving seven selected elements. The two occurrences of `4` belong to different subsequences, but their index ranges do not overlap. This is why the DP has to split the array into contiguous regions and take one increasing subsequence from each chosen region rather than independently choosing arbitrary disjoint index sets.

## Approaches

A direct brute-force solution could enumerate every subset of the array positions, then determine whether those selected positions can be divided into valid increasing subsequences of length at least (k), while also respecting the non-overlap condition. There are (2^n) subsets before we even check whether a particular subset is valid. If the validity check examines the selected positions and possible boundaries, it takes polynomial time, so the total work is at least (O(2^n n^2)). At (n=100), the subset count alone is approximately (1.27\times10^{30}), making exhaustive search impossible.

The brute force fails because it treats every choice of positions as unrelated to every other choice. The useful structure is that non-overlap gives us a natural left-to-right decomposition. Once the last subsequence is fixed, everything before its starting position is an independent smaller instance.

The next observation is that, if we decide that one subsequence occupies the interval from position (l) to position (r), there is never a reason to choose anything smaller than the longest increasing subsequence inside that interval. If that interval has an LIS of length (L), and (L\ge k), we can use all (L) elements. Using fewer elements would only reduce the objective and would not make the interval more compatible with another subsequence, because no other subsequence is allowed inside the interval anyway.

This reduces the problem to two dynamic programming layers. First, compute `lis[l][r]`, the length of the longest increasing subsequence contained entirely in the contiguous interval from (l) through (r). There are (O(n^2)) intervals, and a straightforward LIS DP computes all intervals in (O(n^3)) time. This is exactly the preprocessing strategy described in the official review.

Then fix (k). Let `dp[r]` be the maximum number of selected elements using only positions `0..r`. There are two possibilities. We can leave position (r) unused, giving `dp[r-1]`. Or the final subsequence starts at some position (l), occupies the whole interval `[l,r]`, and contributes `lis[l][r]` elements. This is allowed only when `lis[l][r] >= k`. Everything before (l) contributes `dp[l-1]`. Thus the transition is

[
dp[r]=\max\left(dp[r-1],\max_{0\le l\le r,;lis[l][r]\ge k}
\left(dp[l-1]+lis[l][r]\right)\right).
]

There are (n) possible values of (k), (n) possible right endpoints, and (n) possible starting points, so this second phase also takes (O(n^3)) time. The official editorial-style review presents the same decomposition, viewing the last chosen subsequence as an LIS of a suffix after some previous breakpoint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n n^2)) | (O(n)) | Too slow |
| Optimal | (O(n^3)) | (O(n^2)) | Accepted |

## Algorithm Walkthrough

1. Read the array and create a two-dimensional table `lis`, where `lis[l][r]` will eventually contain the LIS length of the interval `a[l:r+1]`. We need this information because every selected subsequence occupies a contiguous range of positions, even though the elements chosen inside that range need not be adjacent.
2. Fix the left endpoint `l` and extend the interval one position at a time. For each new right endpoint `r`, compute the longest increasing subsequence ending exactly at `r` using only positions `l..r`. For every earlier position `p`, the element at `p` can precede `a[r]` precisely when `a[p] < a[r]`. Taking the maximum over those predecessors and adding one gives the best increasing subsequence ending at `r`.
3. Keep the maximum LIS length seen so far while extending the interval. This gives `lis[l][r]`, because an LIS of `[l,r]` either ends at `r` or ends earlier.
4. Repeat the interval computation for every possible `l`. There are (O(n^2)) intervals, and the predecessor search over each interval gives an (O(n^3)) preprocessing phase.
5. For every (k) from `1` through `n`, create a prefix DP array. Let `dp[r]` represent the maximum number of elements that can be selected from positions `0..r` when every selected subsequence has length at least `k`.
6. Initialize the prefix DP by allowing the current position to remain unused. For `r > 0`, start with `dp[r] = dp[r-1]`. This handles solutions whose last subsequence finishes before position `r`.
7. Try every possible starting position `l` for the final subsequence ending at `r`. If `lis[l][r] >= k`, the interval can provide a valid final subsequence. Its contribution is `lis[l][r]`, while the prefix before it contributes `dp[l-1]`, or zero when `l=0`.
8. Take the largest value over all choices of `l`. After processing `r`, `dp[r]` is the optimal answer for the prefix through `r`.
9. Store `dp[n-1]` as the answer for this particular `k`, then repeat for the next value of `k`.

Why it works follows from the last-subsequence decomposition. Consider an optimal solution for a prefix ending at `r`. If it does not use position `r`, the solution is already represented by `dp[r-1]`. Otherwise, let its final subsequence occupy positions from `l` through `r`. No earlier selected subsequence can use any position in that interval, so all earlier selected elements lie completely inside `0..l-1` and are represented optimally by `dp[l-1]`. Inside `[l,r]`, replacing the final subsequence with an LIS cannot hurt because the interval is unavailable to every other subsequence and a longer increasing subsequence contributes more elements. The transition considers exactly these possibilities, so it contains the optimal solution and never constructs an invalid overlap.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(a):
    n = len(a)

    # lis[l][r] = LIS length inside a[l..r].
    lis = [[0] * n for _ in range(n)]

    for l in range(n):
        ending = [0] * n
        best = 0

        for r in range(l, n):
            cur = 1
            ar = a[r]

            for p in range(l, r):
                if a[p] < ar and ending[p] + 1 > cur:
                    cur = ending[p] + 1

            ending[r] = cur
            if cur > best:
                best = cur

            lis[l][r] = best

    answer = [0] * n

    # Solve the non-overlapping interval problem independently for
    # every required minimum subsequence length k.
    for k in range(1, n + 1):
        dp = [0] * n

        for r in range(n):
            # Leave position r unused.
            if r > 0:
                best = dp[r - 1]
            else:
                best = 0

            # Make [l, r] the interval occupied by the last subsequence.
            for l in range(r + 1):
                length = lis[l][r]

                if length >= k:
                    before = dp[l - 1] if l > 0 else 0
                    value = before + length

                    if value > best:
                        best = value

            dp[r] = best

        answer[k - 1] = dp[n - 1]

    return answer

def main():
    t = int(input())

    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        ans = solve_case(a)
        out.append(" ".join(map(str, ans)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The first nested section builds the interval LIS table. For a fixed `l`, `ending[r]` stores the longest increasing subsequence that ends exactly at position `r`. When `a[p] < a[r]`, an increasing subsequence ending at `p` can be extended by `a[r]`. The variable `best` is the maximum of all such ending lengths encountered so far, which is exactly the LIS of the current interval.

The second major section handles one value of `k` at a time. The assignment from `dp[r - 1]` is not optional bookkeeping. It represents the possibility that the optimal collection stops before `r`, which is a common source of incorrect solutions.

The expression `dp[l - 1] if l > 0 else 0` handles the first interval without requiring a sentinel element. This avoids an off-by-one special case in the `lis` table while keeping the recurrence close to its mathematical form.

The comparison `a[p] < ar` must be strict. Equal values cannot be consecutive elements of an increasing subsequence. Python integers also have arbitrary precision, so there is no integer-overflow issue.

The implementation computes every `k` separately because (n\le100). This keeps the state definition simple and makes the correctness argument transparent. The total number of prefix transitions is (O(n^3)), while the interval LIS preprocessing contributes another (O(n^3)).

## Worked Examples

### Sample 1

The first sample is

```
8
2 1 9 3 4 4 5 6
2
1 1
3
1 2 3
```

For the first test case, the array is `2 1 9 3 4 4 5 6`. Consider (k=2). The useful prefix DP evolves as follows.

| `r` | Interval ending at `r` used as final subsequence | `lis[l][r]` | `dp[r-1]` | Best `dp[r]` |
| --- | --- | --- | --- | --- |
| 0 | `[2]` | 1 | 0 | 0 |
| 1 | `[2,9]` | 2 | 0 | 2 |
| 2 | `[1,9]` | 2 | 2 | 2 |
| 3 | `[3,4]` | 2 | 2 | 4 |
| 4 | `[4,5]` | 2 | 4 | 4 |
| 5 | `[4,5]` or another valid interval | 2 | 4 | 4 |
| 6 | `[4,5]`-type interval | 3 | 4 | 7 |
| 7 | `[4,5,6]` | 3 | 4 | 7 |

The final value is `7`, obtained by `[2,9]`, `[3,4]`, and `[4,5,6]`. This demonstrates why simply computing one LIS for the entire array is insufficient. The global LIS is shorter than the total number of elements obtainable from several non-overlapping subsequences. The complete output for this test case is `8 7 6 5 5 0 0 0`.

### Sample 2

The second test case is

```
2
1 1
```

For (k=1), every individual element is a valid increasing subsequence, so both elements can be selected separately.

| `r` | `dp[r-1]` | Valid final interval | `lis[l][r]` | `dp[r]` |
| --- | --- | --- | --- | --- |
| 0 | 0 | `[1]` | 1 | 1 |
| 1 | 1 | `[1]` | 1 | 2 |

For (k=2), the only interval contains two equal values, so its strict LIS has length one. No valid subsequence exists, and the answer is zero.

| `r` | `dp[r-1]` | Valid interval of length at least 2 | `dp[r]` |
| --- | --- | --- | --- |
| 0 | 0 | none | 0 |
| 1 | 0 | none | 0 |

The resulting output is `2 0`. This case specifically confirms that equality must not count as an increasing transition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^3)) | Interval LIS preprocessing takes (O(n^3)), and all (n) prefix-DP problems together take another (O(n^3)). |
| Space | (O(n^2)) | The interval LIS table contains (n^2) values; the remaining DP arrays are only (O(n)). |

With (n\le100), the cubic bound is small enough for the intended solution. The official analysis explicitly identifies (O(n^3)) interval-LIS preprocessing as feasible for these limits. The Python implementation keeps the inner loops simple and avoids recursion, large temporary structures, and repeated recomputation of LIS values.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve_case(a):
    n = len(a)

    lis = [[0] * n for _ in range(n)]

    for l in range(n):
        ending = [0] * n
        best = 0

        for r in range(l, n):
            cur = 1
            ar = a[r]

            for p in range(l, r):
                if a[p] < ar and ending[p] + 1 > cur:
                    cur = ending[p] + 1

            ending[r] = cur
            if cur > best:
                best = cur

            lis[l][r] = best

    answer = [0] * n

    for k in range(1, n + 1):
        dp = [0] * n

        for r in range(n):
            best = dp[r - 1] if r > 0 else 0

            for l in range(r + 1):
                length = lis[l][r]

                if length >= k:
                    before = dp[l - 1] if l > 0 else 0
                    value = before + length

                    if value > best:
                        best = value

            dp[r] = best

        answer[k - 1] = dp[n - 1]

    return answer

def solution(inp):
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()

        input = sys.stdin.readline
        t = int(input())
        out = []

        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            out.append(" ".join(map(str, solve_case(a))))

        print("\n".join(out))
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
sample1 = """3
8
2 1 9 3 4 4 5 6
2
1 1
3
1 2 3
"""

assert solution(sample1) == """8 7 6 5 5 0 0 0
2 0
3 3 3
""", "provided samples"

# Minimum-size input
assert solution("""1
1
42
""") == "1\n", "single element"

# All equal values
assert solution("""1
3
1 1 1
""") == "3 0 0\n", "strictly increasing requirement"

# Boundary case where the best collection uses separate intervals
assert solution("""1
8
2 1 9 3 4 4 5 6
""") == "8 7 6 5 5 0 0 0\n", "non-overlapping subsequences"

# Maximum-size input, strictly increasing
a = list(range(1, 101))
expected = " ".join(["100"] * 100) + "\n"

assert solution(
    "1\n100\n" + " ".join(map(str, a)) + "\n"
) == expected, "maximum n and fully increasing array"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 42` | `1` | Minimum size and single valid subsequence |
| `3 / 1 1 1` | `3 0 0` | Strict inequality in the LIS transition |
| `8 / 2 1 9 3 4 4 5 6` | `8 7 6 5 5 0 0 0` | Multiple non-overlapping subsequences |
| `100 / 1 2 ... 100` | 100 copies of `100` | Maximum (n), large DP state, and fully increasing input |

## Edge Cases

For the single-element input

```
1
42
```

the interval table contains only `lis[0][0] = 1`. For (k=1), the DP considers `[0,0]`, sees an LIS of length one, and obtains `dp[0] = 1`. The output is `1`. There is no artificial zero-length subsequence involved.

For the all-equal input

```
3
1 1 1
```

every interval of length at least two has LIS length one because the comparison is strictly `<`. When (k=1), the DP can select each singleton interval independently, giving `3`. When (k=2`or`k=3`, every interval has LIS shorter than the required threshold, so the answer is zero. The output is `3 0 0`.

For the non-overlapping example

```
8
2 1 9 3 4 4 5 6
```

with (k=2), the DP can first take `[2,9]`, contributing two elements. It can then start after that interval and take `[3,4]`, contributing another two. Finally, `[4,5,6]` contributes three. The total is seven. The DP's prefix state records the best result before each starting position, so these intervals combine without ever allowing an earlier subsequence to intrude into a later interval.

For the maximum-size increasing input

```
100
1 2 3 ... 100
```

the entire array is increasing, so its LIS is 100. For every (k\le100), the whole array itself is a valid subsequence because its length is at least (k). Since no solution can select more than all 100 elements, every answer is exactly 100. This case exercises the largest DP dimensions while also providing a simple upper-bound check for correctness.
