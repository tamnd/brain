---
title: "CF 104412D - Draconis Subarrays"
description: "We are given two integer arrays. The first array, call it the pattern array, has length $M$. The second array, call it the source array, has length $N$."
date: "2026-06-30T22:50:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104412
codeforces_index: "D"
codeforces_contest_name: "2023 ICPC Gran Premio de Mexico 2da Fecha"
rating: 0
weight: 104412
solve_time_s: 59
verified: true
draft: false
---

[CF 104412D - Draconis Subarrays](https://codeforces.com/problemset/problem/104412/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two integer arrays. The first array, call it the pattern array, has length $M$. The second array, call it the source array, has length $N$. We want to count how many contiguous segments of the source array can be transformed into the pattern array by adding the same constant value to every element of that segment.

In other words, a segment of $N$ matches $M$ if the shape of values is identical, up to a vertical shift. The absolute values do not matter, only how values change from one position to the next.

The key constraint is that both arrays can be very large, up to $10^6$ elements. This rules out any quadratic comparison between every subarray of $N$ and $M$, since that would require checking roughly $N \cdot M$ elements in the worst case, which is far beyond $10^6$ operations.

A naive approach would compare every length-$M$ subarray of $N$ directly against $M$, but even a single comparison costs $O(M)$, leading to $O(NM)$ overall, which is up to $10^{12}$ operations in the worst case.

A subtle edge case arises when all elements in $M$ are identical. In that situation, every valid match requires the chosen subarray of $N$ to also consist of identical values, but shifted versions can still match. If one incorrectly compares raw values instead of relative differences, identical-shape cases would be missed. For example, $M = [1,1,1]$ and a subarray $[5,5,5]$ should match, but direct comparison would fail.

Another corner case is when $M$ has length $1$. Every single element subarray of $N$ is valid because any value can be shifted to match a single number. The answer is simply $N$, which is easy to overlook if the method always assumes differences exist.

## Approaches

The central observation is that “equal up to a constant shift” removes absolute values and leaves only relative structure. If we subtract consecutive elements, the constant shift disappears completely.

For any array $A$, define its difference representation:

$$D_A[i] = A[i+1] - A[i]$$

Two arrays are shift-equivalent if and only if their difference arrays are identical. This transforms the problem into a pattern matching task: we are no longer matching values, but matching a sequence of differences.

The brute-force solution would iterate over every subarray of $N$ of length $M$, compute its difference sequence, and compare it to that of $M$. Each comparison costs $O(M)$, and there are $O(N)$ candidates, so the total complexity is $O(NM)$. This is too slow when both arrays reach $10^6$.

Once the problem is reduced to matching two sequences, it becomes a standard substring search problem: we need to count occurrences of one array inside another. This can be solved in linear time using a rolling hash or prefix-function (KMP). The structure is important: we are matching a fixed pattern inside a large text, and the alphabet is arbitrary integers, so hashing is a natural fit.

After converting both arrays into their difference forms, we search for occurrences of the pattern difference array inside the text difference array. Each match corresponds to one valid subarray in the original array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NM)$ | $O(1)$ extra | Too slow |
| Difference + KMP/Hash | $O(N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. If $M = 1$, return $N$. Any single element subarray can be shifted to match a single value, so every position is valid.
2. Build the difference array for $M$, where each entry is $m[i+1] - m[i]$. This encodes its structure independently of absolute values. This step reduces the pattern size to $M-1$.
3. Build the difference array for $N$, similarly computing $n[i+1] - n[i]$. This converts the problem into finding occurrences of one sequence inside another.
4. If $M > N$, return $0$. A longer pattern cannot fit into a shorter sequence.
5. Use a linear-time pattern matching algorithm such as KMP to count how many times the pattern difference array appears inside the text difference array. Each match corresponds to a valid starting index in the original array.
6. Return the number of matches found.

### Why it works

A constant shift affects all elements equally, so it cancels out when taking adjacent differences. This means any two arrays that differ only by a constant produce identical difference arrays. Conversely, if two arrays have identical difference arrays, their values must differ by a constant offset, because reconstructing from a fixed starting value yields the same relative structure. Thus, matching difference arrays is exactly equivalent to the original similarity condition. Every valid subarray match in the difference space corresponds one-to-one with a valid shifted match in the original array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_diff(arr):
    return [arr[i+1] - arr[i] for i in range(len(arr) - 1)]

def kmp_prefix(p):
    pi = [0] * len(p)
    j = 0
    for i in range(1, len(p)):
        while j > 0 and p[i] != p[j]:
            j = pi[j - 1]
        if p[i] == p[j]:
            j += 1
            pi[i] = j
    return pi

def kmp_count(text, pat):
    if not pat:
        return len(text) + 1

    pi = kmp_prefix(pat)
    j = 0
    count = 0

    for i in range(len(text)):
        while j > 0 and text[i] != pat[j]:
            j = pi[j - 1]
        if text[i] == pat[j]:
            j += 1
        if j == len(pat):
            count += 1
            j = pi[j - 1]

    return count

def solve():
    M, N = map(int, input().split())
    m = list(map(int, input().split()))
    n = list(map(int, input().split()))

    if M == 1:
        print(N)
        return

    if M > N:
        print(0)
        return

    dm = build_diff(m)
    dn = build_diff(n)

    print(kmp_count(dn, dm))

if __name__ == "__main__":
    solve()
```

The solution begins by handling degenerate cases where the pattern length is 1 or larger than the text. The transformation step computes difference arrays, shrinking the matching problem into one over length $M-1$ and $N-1$.

The KMP routine is used to efficiently count pattern occurrences in linear time. The prefix array encodes how far we can safely fall back when a mismatch occurs, preventing re-examination of already-verified structure. The matching loop increments a counter whenever the full pattern is matched, then continues from the longest valid border.

A subtle point is that we do not compare raw arrays at all after preprocessing. All correctness depends entirely on the fact that difference arrays preserve equivalence under translation.

## Worked Examples

### Example 1

Input:

```
M = 4, N = 6
M = [1,2,3,4]
N = [10,11,12,13,14,15]
```

Difference arrays:

```
dm = [1,1,1]
dn = [1,1,1,1,1]
```

| i | dn window | match state j | action |
| --- | --- | --- | --- |
| 0 | [1,1,1] | 0 → 1 → 2 → 3 | full match |
| 1 | [1,1,1] | reset | match |
| 2 | [1,1,1] | reset | match |

We count 3 matches starting at indices 0, 1, and 2.

This confirms that every consecutive block of length 4 in a constant-step sequence matches the pattern.

### Example 2

Input:

```
M = 3, N = 10
M = [1,1,1]
N = [2,2,2,3,3,3,4,4,4,4]
```

Difference arrays:

```
dm = [0,0]
dn = [0,0,0,0,0,0,0,0,0]
```

| i | dn window | j | action |
| --- | --- | --- | --- |
| 0 | [0,0] | 0 → 1 → 2 | match |
| 1 | [0,0] | reset | match |
| 2 | [0,0] | reset | match |
| 3 | [0,0] | reset | match |
| 4 | [0,0] | reset | match |

We obtain 4 matches, corresponding to every length-3 constant segment.

This shows the algorithm correctly handles the all-equal case where differences collapse to zeros.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N + M)$ | building difference arrays and KMP scanning are both linear |
| Space | $O(N + M)$ | storing difference arrays and prefix table |

The constraints allow up to $10^6$ elements, so a linear-time solution fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("""4 6
1 2 3 4
10 11 12 13 14 15
""") == "3"

# sample 2
assert run("""3 10
1 1 1
2 2 2 3 3 3 4 4 4 4
""") == "4"

# sample 3
assert run("""2 6
5 8
10 12 1 4 3 9
""") == "1"

# minimum size M = 1
assert run("""1 5
7
1 2 3 4 5
""") == "5"

# all equal large block
assert run("""4 6
5 5 5 5
1 1 1 1 1 1
""") == "3"

# no match
assert run("""3 5
1 2 3
10 20 30 40 50
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| M=1 case | N | single element always matches |
| all equal arrays | 3 | zero-difference pattern matching |
| no match | 0 | correctness under mismatch |

## Edge Cases

For the case $M = 1$, the algorithm directly returns $N$. This aligns with the fact that the difference array becomes empty, and every position trivially matches an empty pattern. For example, input $M=[7]$, $N=[1,2,3]$ produces 3 matches, since every single element subarray can be shifted to 7.

For uniform arrays such as $M=[5,5,5]$ and $N=[1,1,1,1]$, the difference arrays are entirely zeros. The KMP process matches a zero pattern repeatedly across the zero text, producing $N-M+1$ valid matches. This confirms that the algorithm correctly handles cases where value information disappears entirely after differencing.

For non-matching structures like $M=[1,2,3]$ and $N=[10,20,30]$, the difference arrays differ as $[1,1]$ versus $[10,10]$, so no substring match occurs, producing zero as expected.
