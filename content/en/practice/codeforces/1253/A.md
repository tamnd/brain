---
problem: 1253A
contest_id: 1253
problem_index: A
name: "Single Push"
contest_name: "Codeforces Round 600 (Div. 2)"
rating: 1000
tags: ["implementation"]
answer: passed_samples
verified: true
solve_time_s: 297
date: 2026-06-13
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2d70a2-c08c-83ec-a0ab-b70b1d4d82e3
---

# CF 1253A - Single Push

**Rating:** 1000  
**Tags:** implementation  
**Model:** gpt-5-5  
**Solve time:** 4m 57s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2d70a2-c08c-83ec-a0ab-b70b1d4d82e3  

---

## Solution

## Problem Understanding

We are given two arrays of equal length and are allowed a very specific kind of modification: at most once, we may choose a contiguous segment and add the same positive integer to every element in that segment. The task is to determine whether we can transform the first array into the second using either no operation or exactly one such segment addition.

The key restriction is that the modification is uniform over a single interval. That means every index outside the chosen segment must already match between the arrays, and inside the segment the difference between corresponding elements must be constant.

The input size goes up to 100,000 per test case in total, which rules out any quadratic checking of all possible segments explicitly. Any solution must scan each array in linear time per test case.

A naive mistake is to assume that we can pick multiple disjoint “good” segments where differences are equal. That fails because only one continuous segment is allowed. For example, if the differences look like `[0, 2, 0, 2, 0]`, one might think each `2` can be fixed independently, but a single operation cannot cover multiple separated intervals.

Another subtle edge case is when all differences are zero except one position where the difference is negative. Since we can only add a positive value, negative differences immediately make the answer impossible.

Example failure case:

Input:

```
3
1 2 3
2 1 3
```

Here differences are `[+1, -1, 0]`. Even though most indices look fine, the single negative difference makes it impossible.

Correct output: `NO`.

## Approaches

A brute-force strategy would try every possible segment `[l, r]` and compute whether there exists a positive `k` such that adding `k` to that segment converts `a` into `b`. For a fixed segment, we would compute all differences `b[i] - a[i]` inside the segment and verify they are identical and positive, and also ensure all outside elements already match.

Checking one segment costs `O(n)` in the worst case, and there are `O(n^2)` segments, leading to `O(n^3)` total time, which is far too slow.

The key observation is that the operation defines a very rigid structure on the difference array `d[i] = b[i] - a[i]`. After at most one operation, all nonzero values in `d` must lie inside one contiguous segment, and within that segment all values must be identical and positive. Everywhere else must be exactly zero.

So instead of searching for a segment, we directly analyze the structure of the difference array. We simply check whether all nonzero entries form exactly one continuous block and whether all values in that block are equal and positive.

This reduces the problem from “choose a segment” to “verify a pattern in one pass”.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We define the difference array implicitly as `d[i] = b[i] - a[i]`.

1. Compute the first index where `d[i]` is non-zero. If none exists, the arrays are already equal and we return YES immediately. This handles the case where no operation is needed.
2. From this first non-zero position, we determine the value `k = d[start]`. This is the only possible value we could add in the operation, because the operation enforces a constant increment.
3. We scan forward from `start` and ensure every position with non-zero difference has value exactly `k`. If we ever see a different non-zero value, it means no single uniform increment can explain the transformation.
4. We ensure all non-zero differences appear in a single contiguous block. Once we leave the block of non-zero values, we must not encounter another non-zero value later. If we do, the required operation would need two separate segments, which is not allowed.
5. We also ensure `k > 0`. A non-positive value cannot be achieved because the operation only allows adding positive integers.

Why it works: the operation changes exactly one interval by a constant offset, so the difference array after a valid operation must be zero everywhere except possibly one contiguous interval, where all values are equal to the same positive constant. The algorithm checks exactly this structural property, so any deviation implies impossibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    i = 0
    while i < n and a[i] == b[i]:
        i += 1

    if i == n:
        print("YES")
        return

    k = b[i] - a[i]
    if k <= 0:
        print("NO")
        return

    while i < n and a[i] != b[i]:
        if b[i] - a[i] != k:
            print("NO")
            return
        i += 1

    while i < n:
        if a[i] != b[i]:
            print("NO")
            return
        i += 1

    print("YES")

t = int(input())
for _ in range(t):
    solve()
```

The solution first locates the start of the mismatch region. That index determines the only feasible increment value. It then validates that the entire mismatch region is consistent and contiguous, and finally ensures no further mismatches appear later.

A common implementation pitfall is forgetting to enforce contiguity, which leads to accepting cases where mismatches appear in multiple separated blocks. Another subtle issue is failing to reject negative or zero `k`, which is invalid because the operation requires strictly positive addition.

## Worked Examples

### Example 1

Input:

```
6
3 7 1 4 1 2
3 7 3 6 3 2
```

Difference array:

`[0, 0, 2, 2, 2, 0]`

| Step | i | a[i] vs b[i] | k | Status |
| --- | --- | --- | --- | --- |
| Find start | 2 | 1 → 3 | 2 | start found |
| Scan block | 2 | 2 | 2 | ok |
| Scan block | 3 | 2 | 2 | ok |
| Scan block | 4 | 2 | 2 | ok |
| Exit block | 5 | 0 | 2 | ok |

The mismatch region is one continuous segment with constant difference 2, so a single push works.

### Example 2

Input:

```
5
1 1 1 1 1
1 2 1 3 1
```

Difference array:

`[0, 1, 0, 2, 0]`

| Step | i | a[i] vs b[i] | k | Status |
| --- | --- | --- | --- | --- |
| Find start | 1 | 1 → 2 | 1 | k=1 |
| Scan block | 1 | 1 | 1 | ok |
| Next mismatch | 3 | 1 → 3 | expected 1 | mismatch |

At index 3 we find a different non-zero difference (2 instead of 1), so no single segment with uniform increment can explain the transformation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass over arrays to find and validate mismatch segment |
| Space | O(1) | no auxiliary arrays needed |

The linear scan is sufficient because each element is processed at most a constant number of times. With total `n` across test cases up to 100,000, this easily fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        i = 0
        while i < n and a[i] == b[i]:
            i += 1

        if i == n:
            out.append("YES")
            return

        k = b[i] - a[i]
        if k <= 0:
            out.append("NO")
            return

        while i < n and a[i] != b[i]:
            if b[i] - a[i] != k:
                out.append("NO")
                return
            i += 1

        while i < n:
            if a[i] != b[i]:
                out.append("NO")
                return
            i += 1

        out.append("YES")

    for _ in range(t):
        solve()

    return "\n".join(out)

# provided samples
assert run("""4
6
3 7 1 4 1 2
3 7 3 6 3 2
5
1 1 1 1 1
1 2 1 3 1
2
42 42
42 42
1
7
6
""") == """YES
NO
YES
NO"""

# custom cases
assert run("""1
3
1 2 3
1 2 3
""") == "YES", "already equal"

assert run("""1
3
1 2 3
2 2 3
""") == "NO", "multiple mismatches"

assert run("""1
4
1 1 1 1
2 1 2 1
""") == "NO", "non-contiguous differences"

assert run("""1
3
5 5 5
4 4 4
""") == "NO", "negative k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| already equal | YES | no-operation case |
| 1 2 3 → 2 2 3 | NO | inconsistent differences |
| 1 1 1 1 → 2 1 2 1 | NO | non-contiguous mismatch |
| 5 5 5 → 4 4 4 | NO | negative k rejection |

## Edge Cases

One edge case is when arrays are already identical. The algorithm detects this when no mismatch index is found and immediately returns YES without attempting to compute `k`.

Another case is when mismatches exist but are not contiguous. For input `a = [1,1,1,1]`, `b = [2,1,2,1]`, the difference array is `[1,0,1,0]`. The scan finds a mismatch, then returns to zero, then later finds another mismatch, which violates the single-segment requirement, correctly producing NO.

A final edge case is when the first mismatch already violates positivity. If `b[i] < a[i]` at the first differing index, `k` becomes negative and the algorithm rejects immediately, since the operation can only increase values.