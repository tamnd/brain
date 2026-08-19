---
title: "CF 102163C - Hasan and his lazy students"
description: "For each test case, we have an array of (N) integers. A subsequence keeps the original left-to-right order, but may skip any number of elements. It is increasing only when every chosen value is strictly larger than the previous chosen value. The task has two parts."
date: "2026-08-19T23:52:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "C"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 664
verified: false
draft: false
---

[CF 102163C - Hasan and his lazy students](https://codeforces.com/problemset/problem/102163/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 11m 4s  
**Verified:** no  

## Solution
## Problem Understanding

For each test case, we have an array of (N) integers. A subsequence keeps the original left-to-right order, but may skip any number of elements. It is increasing only when every chosen value is strictly larger than the previous chosen value.

The task has two parts. We need the maximum possible length of an increasing subsequence, and we also need to count how many different subsequences attain that maximum length. Two subsequences are different when they select different positions in the array, even if the selected values happen to be equal. The count is printed modulo (10^9+7).

For example, in

```
1 2 1 4 3
```

the maximum length is (3). The subsequences using positions (1,2,4) and (1,2,5) give (1,2,4) and (1,2,3), so there are two LISs.

The array length is at most (1000), which makes an (O(N^2)) dynamic programming solution practical. An (O(N^3)) solution would already perform around (10^9) operations when (N=1000), which is too much for a 4 second limit. Enumerating subsequences is exponentially worse, since an array of length (N) has (2^N) possible position subsets.

The values (A_i) can be as large as (10^6), but this does not require coordinate compression or a special data structure because the dynamic programming transition only compares two values. The important distinction is strict inequality, so equal values must never extend an increasing subsequence.

Several small cases expose common mistakes. With

```
1
1
7
```

the answer is

```
1 1
```

because the single element itself is the only LIS. An implementation that initializes the number of ways to zero would lose this base case.

With

```
1
3
5 5 5
```

the answer is

```
1 3
```

because each position independently forms a length-one LIS. Treating the comparison as (A_j \le A_i) would incorrectly produce a longer subsequence.

With

```
1
3
1 2 3
```

the answer is

```
3 1
```

because there is exactly one way to select all three positions. A careless implementation that sums counts from every predecessor without checking whether the resulting length is the best length for the current position can overcount.

Finally, the count itself can become very large. For example, an array containing many repeated structures can have a large number of LISs, so the count must be reduced modulo (10^9+7) during the dynamic programming transitions.

## Approaches

The most direct solution is to enumerate every subsequence of the array, check whether it is strictly increasing, and keep the longest ones. There are exactly (2^N) position subsets. If we inspect up to (N) positions for each subset, the worst-case work is (O(N2^N)). For (N=1000), this is completely infeasible.

We can do better by asking a more local question. Instead of constructing every possible subsequence, consider an LIS whose final selected position is (i). Everything before (i) must itself be an increasing subsequence ending at some position (j<i), with (A_j<A_i). This means every valid subsequence ending at (i) can be built by extending a valid subsequence ending at an earlier position.

For every position (i), maintain two values. The first is the length of the longest increasing subsequence ending exactly at (i). The second is the number of such longest subsequences.

Suppose (j<i) and (A_j<A_i). If the best subsequence ending at (j) has length (L), appending (A_i) creates a subsequence of length (L+1). If this is better than anything previously found for (i), we replace the length and copy the number of ways from (j). If it ties the current best length, we add the number of ways from (j).

The brute-force solution works because every subsequence is explicitly considered, but it fails because there are exponentially many of them. The observation that every LIS ending at (i) has a unique previous selected position lets us summarize all earlier possibilities with two values per position. Since (N) is only (1000), checking every pair (j<i) gives an (O(N^2)) dynamic program.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N2^N)) | (O(N)) | Too slow |
| Optimal DP | (O(N^2)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Process the array from left to right. For every position (i), initialize `length[i] = 1` and `count[i] = 1`. A single element always forms an increasing subsequence of length one, so these are the correct base values.
2. For each position (i), inspect every earlier position (j<i). Only positions satisfying (A_j<A_i) can precede (i), because the subsequence must be strictly increasing.
3. For every valid predecessor (j), calculate the length obtained by extending its best subsequence:

[
candidate = length[j] + 1.
]

If `candidate` is greater than `length[i]`, replace `length[i]` with it and set `count[i]` to `count[j]`. All previously known shorter subsequences ending at (i) can be discarded because they can never become globally longest through this position.

1. If `candidate` equals `length[i]`, add `count[j]` to `count[i]`. These represent a new group of distinct subsequences with the same optimal length ending at (i). Take the sum modulo (10^9+7).
2. After processing every position, find the largest value in `length`. This is the global LIS length.
3. Sum `count[i]` over every position whose `length[i]` equals the global maximum. Every LIS has exactly one final position, so this sums every LIS exactly once. Again, take the result modulo (10^9+7).

### Why it works

The invariant is that after processing position (i), `length[i]` is exactly the maximum length of an increasing subsequence ending at (i), while `count[i]` is exactly the number of subsequences achieving that length.

Any increasing subsequence ending at (i) either consists only of (A_i), or has some final predecessor (j<i) with (A_j<A_i). In the second case, its prefix must be an increasing subsequence ending at (j). The transition considers every possible predecessor, so it considers every possible way an optimal subsequence can reach (i). When a longer length is found, only that longer family can remain optimal. When an equal length is found, its distinct subsequences must all be added.

At the end, every LIS has one and only one final position. Summing the counts for positions with maximum `length` therefore counts every LIS exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def main():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        length = [1] * n
        count = [1] * n

        for i in range(n):
            for j in range(i):
                if a[j] >= a[i]:
                    continue

                candidate = length[j] + 1

                if candidate > length[i]:
                    length[i] = candidate
                    count[i] = count[j]
                elif candidate == length[i]:
                    count[i] += count[j]
                    count[i] %= MOD

        best_length = max(length)

        total_count = 0
        for i in range(n):
            if length[i] == best_length:
                total_count += count[i]
                total_count %= MOD

        print(best_length, total_count)

if __name__ == "__main__":
    main()
```

The two arrays are the core of the dynamic programming state. `length[i]` describes the best subsequence ending at position `i`, and `count[i]` describes how many ways achieve that exact length.

The inner loop examines every earlier position. The condition `a[j] >= a[i]` rejects equal values as well as decreasing transitions, leaving exactly the strict inequality required by the problem.

When a strictly better predecessor is found, `count[i]` must be replaced rather than added to. A shorter subsequence ending at (i) cannot contribute to an LIS ending at (i). When the candidate ties the current best length, the counts are added because both predecessor choices produce distinct position subsequences.

All counts are reduced modulo (10^9+7). Python integers do not overflow, but taking the modulus keeps the values small and directly implements the required output convention.

The final loop is necessary because an LIS can finish at any position. Taking only `count[n - 1]`, for example, would be correct only when the final array element belongs to every LIS.

The indices in the transition satisfy `j < i`, so the original order of the array is automatically preserved. No sorting is performed, since sorting would destroy the subsequence ordering constraint.

## Worked Examples

Consider the first test case from the sample:

```
1 3 2 3 1
```

The state after each position is:

| Position (i) | (A_i) | `length[i]` | `count[i]` | Reason |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | Single element |
| 1 | 3 | 2 | 1 | Extend `1` |
| 2 | 2 | 2 | 1 | Extend `1` |
| 3 | 3 | 3 | 1 | Extend the best subsequence ending at `2` |
| 4 | 1 | 1 | 1 | Cannot extend any previous value |

The maximum length is (3), reached only at position (3). The answer is therefore `3 1`.

This trace shows why equal values cannot be used as predecessors. The second `3` cannot extend the first `3`, but it can extend the subsequence ending in `2`.

Now consider the third sample test case:

```
1 5 6 2 1 4 1
```

The resulting states are:

| Position (i) | (A_i) | `length[i]` | `count[i]` |
| --- | --- | --- | --- |
| 0 | 1 | 1 | 1 |
| 1 | 5 | 2 | 1 |
| 2 | 6 | 3 | 1 |
| 3 | 2 | 2 | 1 |
| 4 | 1 | 1 | 1 |
| 5 | 4 | 3 | 2 |
| 6 | 1 | 1 | 1 |

The maximum length is (3). It occurs twice, once through `1, 5, 6` and once through `1, 2, 4`. The counts at positions (2) and (5) are both one, so the final count is (2).

The state at position (5) demonstrates the counting transition. Both `1, 5, 4` is invalid because (5>4), but `1, 2, 4` and the other valid predecessor structure are considered independently. The DP keeps only predecessors that satisfy the strict comparison and then aggregates equal optimal lengths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N^2)) | Each position checks every earlier position once |
| Space | (O(N)) | Two DP arrays store one state per array position |

With (N\le1000), each test case performs at most about (500{,}000) predecessor comparisons. This is comfortably within the intended complexity for the 4 second limit, while the (O(N)) memory usage is far below the 256 MB limit.

## Test Cases

```python
import sys
import io

MOD = 10**9 + 7

def main():
    input = sys.stdin.readline
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        length = [1] * n
        count = [1] * n

        for i in range(n):
            for j in range(i):
                if a[j] >= a[i]:
                    continue

                candidate = length[j] + 1

                if candidate > length[i]:
                    length[i] = candidate
                    count[i] = count[j]
                elif candidate == length[i]:
                    count[i] = (count[i] + count[j]) % MOD

        best_length = max(length)
        total_count = sum(
            count[i] for i in range(n)
            if length[i] == best_length
        ) % MOD

        print(best_length, total_count)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        main()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert run(
    """3
5
1 3 2 3 1
3
1 2 3
7
1 5 6 2 1 4 1
"""
) == """3 1
3 1
3 2
""", "provided sample"

assert run(
    """1
1
7
"""
) == """1 1
""", "minimum-size input"

assert run(
    """1
5
4 4 4 4 4
"""
) == """1 5
""", "all equal values"

assert run(
    """1
6
1 2 3 4 5 6
"""
) == """6 1
""", "strictly increasing array"

assert run(
    """1
7
1 2 1 2 1 2 3
"""
) == """3 6
""", "multiple LIS choices"

assert run(
    """1
4
1000000 999999 1000000 999998
"""
) == """2 1
""", "value boundary and strict comparison"

n = 1000
increasing = " ".join(str(i) for i in range(1, n + 1))
assert run(f"""1
{n}
{increasing}
""") == """1000 1
""", "maximum-size increasing input"

equal_values = " ".join(["42"] * n)
assert run(f"""1
{n}
{equal_values}
""") == """1 1000
""", "maximum-size all-equal input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `1 1` | Single-element base case |
| `4 4 4 4 4` | `1 5` | Strict inequality and counting different positions |
| `1 2 3 4 5 6` | `6 1` | Unique LIS using the entire array |
| `1 2 1 2 1 2 3` | `3 6` | Multiple optimal subsequences |
| `1000000 999999 1000000 999998` | `2 1` | Large values and strict comparison |
| 1000 increasing values | `1000 1` | Maximum (N) and quadratic DP |
| 1000 equal values | `1 1000` | Maximum (N), duplicate values, and counting |

## Edge Cases

For a single element, consider

```
1
1
7
```

The DP starts with `length[0] = 1` and `count[0] = 1`. There is no earlier position to inspect, so these values remain unchanged. The global maximum length is (1), and its count is (1), giving `1 1`. This is why every DP state must start with one rather than zero.

For equal values, consider

```
1
3
5 5 5
```

Every position begins with a length-one subsequence. For every pair (j<i), the condition `a[j] >= a[i]` is true because the values are equal, so no transition is performed. All three positions remain states `(1, 1)`. The global LIS length is (1), and the final aggregation adds all three counts, producing `1 3`. This catches the common mistake of using `<=` instead of `<`.

For a strictly increasing array,

```
1
3
1 2 3
```

position (0) has `(1,1)`. Position (1) extends it to `(2,1)`, and position (2) extends the subsequence ending at position (1) to `(3,1)`. The only LIS selects all three positions, so the answer is `3 1`. This also demonstrates why the final answer cannot simply use the state of the last element in a general implementation, even though it happens to work here.

For multiple LISs, consider

```
1
7
1 2 1 2 1 2 3
```

The final `3` can be preceded by any length-two subsequence consisting of a `1` followed by a later `2`. There are six such position choices, so the final state for `3` has length (3) and count (6). The algorithm finds these through the repeated equal-length transitions and outputs `3 6`.

For values at the upper boundary, consider

```
1
4
1000000 999999 1000000 999998
```

The first `1000000` cannot be followed by anything larger, while `999999` can be followed by the later `1000000`. The best subsequence is thus `999999, 1000000`, with length (2) and one choice. The result is `2 1`. The actual magnitude of the values does not affect the DP, since only pairwise comparisons are needed.

For the maximum array size, an increasing array of (1000) elements produces exactly (1000) DP states and roughly (1000\cdot999/2) pair checks. The LIS length becomes (1000), with count (1). An all-equal array of (1000) elements performs the same number of comparisons but performs no transitions, leaving every state at `(1,1)`. The final aggregation produces `1 1000`. These cases demonstrate that the (O(N^2)) implementation handles the full input bound without relying on favorable array structure.
