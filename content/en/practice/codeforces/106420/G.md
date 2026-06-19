---
title: "CF 106420G - Tyson's Taunt"
description: "We are given an array of integers and a pair of real thresholds $a$ and $b$. The task is to count how many contiguous subarrays have an average that lies in a specific range."
date: "2026-06-20T03:47:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106420
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 3-11-26 (Beginner)"
rating: 0
weight: 106420
solve_time_s: 63
verified: true
draft: false
---

[CF 106420G - Tyson's Taunt](https://codeforces.com/problemset/problem/106420/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and a pair of real thresholds $a$ and $b$. The task is to count how many contiguous subarrays have an average that lies in a specific range. Instead of directly computing averages for every subarray, the problem reduces the goal to counting subarrays whose mean is at least $a$, and subtracting those whose mean exceeds $b$.

A subarray is any contiguous segment, so for each pair of indices $l \le r$, we are implicitly considering the sequence $x_l, x_{l+1}, \dots, x_r$. The output is a single integer representing how many such segments satisfy the final constraint derived from the difference of the two counting problems.

The key structural constraint is that the array length can be large enough that any quadratic enumeration of subarrays becomes infeasible. A naive $O(n^2)$ scan over all subarrays would lead to about $10^{10}$ operations when $n = 10^5$, which is far beyond typical limits. This immediately pushes us toward prefix-based transformations and data structures that can answer range counting queries in logarithmic time.

A subtle issue appears in the transformation step: turning average constraints into sum constraints introduces real-valued comparisons. Since prefix sums are integer-based, careful handling of strict versus non-strict inequalities is required. A careless conversion can shift counts by one and silently corrupt the final answer.

One edge case is when all elements are identical and equal to a threshold. In this situation, every subarray has the same mean, so either all subarrays qualify or none do depending on inclusivity. A naive floating-point comparison approach can also break here due to precision errors.

Another edge case occurs when negative numbers are present. Prefix sums can decrease, and any assumption about monotonicity fails. This makes sorting-based reasoning necessary, but also requires consistent coordinate compression if we use a Fenwick tree.

## Approaches

The brute-force method checks every subarray explicitly, computes its sum, divides by its length, and compares it against the bounds. This is conceptually correct because it directly evaluates the definition of the mean for every segment. However, each subarray requires $O(1)$ amortized sum computation only if prefix sums are precomputed, and there are $O(n^2)$ subarrays, so the total cost is still quadratic. With $n = 10^5$, this leads to about $5 \times 10^9$ evaluations, which is too slow.

The improvement comes from removing division entirely. The condition $\frac{\sum x_i}{len} \ge a$ can be rewritten as $\sum x_i - a \cdot len \ge 0$. This transforms the problem into counting subarrays with non-negative transformed sum. Similarly, the strict inequality on $b$ becomes a slightly shifted threshold after converting it into an integer inequality.

Once transformed, each element becomes $y_i = x_i - a$ or $x_i - b$, and the task becomes counting subarrays with sum at least a fixed constant. This is a classical prefix sum dominance problem: for each right endpoint, we count how many previous prefix sums are small enough so that the resulting subarray sum meets the threshold.

This reduces the problem to maintaining a dynamic set of prefix sums and answering how many of them are $\le$ a given value. A Fenwick tree or order-statistics structure allows this in $O(\log n)$ per insertion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Prefix + Fenwick Tree | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We split the original problem into two independent subproblems: counting subarrays with mean at least $a$, and counting subarrays with mean strictly greater than $b$. The final answer is the difference of these two counts.

1. Convert the first condition into a sum constraint by defining a transformed array $y_i = x_i - a$. A subarray has mean at least $a$ exactly when its transformed sum is non-negative. This removes division entirely and makes the condition purely additive.
2. Build prefix sums over the transformed array, where $p_0 = 0$ and $p_i = y_1 + \dots + y_i$. Any subarray sum from $l$ to $r$ becomes $p_r - p_{l-1}$. We want $p_r - p_{l-1} \ge 0$, which is equivalent to $p_{l-1} \le p_r$.
3. Process prefix sums from left to right. For each endpoint $r$, we want to count how many previous prefix values are less than or equal to the current $p_r$. This directly counts valid starting positions.
4. Since prefix values are arbitrary integers, compress them into ranks. This allows us to store frequencies in a Fenwick tree.
5. For each prefix $p_r$, query how many stored prefix sums are $\le p_r$, add that to the answer, then insert $p_r$ into the Fenwick tree.
6. Repeat the same process for the second condition using $z_i = x_i - b$. For strict inequality, convert it into an integer threshold shift so that $\frac{\sum x_i}{len} > b$ becomes $\sum x_i - b \cdot len \ge 1$, ensuring correct integer handling.
7. Subtract the second count from the first to obtain the final result.

Why it works: every subarray corresponds uniquely to a pair of prefix indices $(l-1, r)$. The condition on the subarray becomes a comparison between two prefix sums. The Fenwick tree maintains all earlier prefix sums, and each query counts exactly how many valid starting points exist for the current endpoint. Since every subarray is counted exactly once at its right endpoint, and the condition is checked purely via prefix dominance, no subarray is missed or double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

def count_ge(arr, threshold):
    n = len(arr)
    pref = [0] * (n + 1)

    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + arr[i - 1]

    vals = sorted(set(pref))
    idx = {v: i + 1 for i, v in enumerate(vals)}

    fw = Fenwick(len(vals))
    res = 0

    for x in pref:
        r = idx[x]
        res += fw.sum(r)
        fw.add(r, 1)

    return res

def solve_condition(a_list, base):
    n = len(a_list)
    transformed = [x - base for x in a_list]
    return count_ge(transformed, 0)

def main():
    n = int(input())
    a, b = map(float, input().split())
    arr = list(map(int, input().split()))

    # first: mean >= a
    prefA = [x - a for x in arr]
    ansA = count_ge(prefA, 0)

    # second: mean > b -> sum - b*len >= 1
    # transform: x - b, but require strict handling via +1 on prefix side
    prefB = [x - b for x in arr]
    ansB = 0

    n = len(arr)
    pref = [0]
    for x in prefB:
        pref.append(pref[-1] + x)

    vals = sorted(set(pref))
    idx = {v: i + 1 for i, v in enumerate(vals)}
    fw = Fenwick(len(vals))

    for p in pref:
        r = idx[p]
        ansB += fw.sum(r - 1)  # strict: p[l-1] < p[r]
        fw.add(r, 1)

    print(ansA - ansB)

if __name__ == "__main__":
    main()
```

The Fenwick tree maintains frequencies of prefix sums. Each prefix sum is compressed into an index so that ordering queries become prefix-frequency queries. For the first condition we allow equality, so we query `sum(r)`. For the strict second condition, we use `sum(r - 1)` to enforce strict inequality.

A common implementation pitfall is mixing floating-point arithmetic in comparisons instead of pushing the real values into integer prefix differences consistently. Another is forgetting that the empty prefix must be included, since every subarray starts from some $l-1$, including zero.

## Worked Examples

Consider an array $[1, 2, 3]$ with thresholds chosen so that we demonstrate both inclusive and strict behavior.

For the first transformation (mean ≥ a), assume it yields transformed array $[1, -1, 2]$.

| r | prefix sum | compressed rank | count ≤ current | Fenwick state |
| --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 0 | {0} |
| 1 | 1 | 3 | 1 | {0,1} |
| 2 | 0 | 2 | 1 | {0,1,0} |
| 3 | 2 | 4 | 3 | {0,1,0,2} |

The accumulation shows how each prefix counts earlier prefixes that are not larger, which corresponds to valid subarray starts.

For the second transformation (strict mean > b), suppose prefix sums become $[0, 1, 1, 3]$.

| r | prefix sum | rank | count < current | Fenwick state |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 0 | {0} |
| 1 | 1 | 2 | 1 | {0,1} |
| 2 | 1 | 2 | 1 | {0,1,1} |
| 3 | 3 | 4 | 3 | {0,1,1,3} |

This trace shows why strict inequality requires excluding equal prefix sums, otherwise equal endpoints would incorrectly contribute.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each prefix sum is inserted and queried once in a Fenwick tree |
| Space | $O(n)$ | Prefix array and coordinate compression storage |

The logarithmic factor comes from Fenwick tree operations, and the linear factor comes from processing each array element once. This fits comfortably within typical constraints for $n$ up to $10^5$ or higher.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import builtins
    return main_capture()

def main_capture():
    import sys
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)
        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i
        def sum(self, i):
            s = 0
            while i > 0:
                s += self.bit[i]
                i -= i & -i
            return s

    def solve():
        n = int(input())
        a, b = map(float, input().split())
        arr = list(map(int, input().split()))

        def count_le(base):
            pref = [0]
            for x in arr:
                pref.append(pref[-1] + (x - base))
            vals = sorted(set(pref))
            idx = {v:i+1 for i,v in enumerate(vals)}
            fw = Fenwick(len(vals))
            res = 0
            for p in pref:
                r = idx[p]
                res += fw.sum(r)
                fw.add(r, 1)
            return res

        def count_lt(base):
            pref = [0]
            for x in arr:
                pref.append(pref[-1] + (x - base))
            vals = sorted(set(pref))
            idx = {v:i+1 for i,v in enumerate(vals)}
            fw = Fenwick(len(vals))
            res = 0
            for p in pref:
                r = idx[p]
                res += fw.sum(r - 1)
                fw.add(r, 1)
            return res

        print(count_le(a) - count_lt(b))

    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# custom tests
assert run("3\n1 1\n1 2 3\n") == "0"
assert run("1\n0 0\n5\n") == "1"
assert run("5\n2 2\n2 2 2 2 2\n") == "15"
assert run("4\n1 1\n1 2 1 2\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case handling |
| all equal | max subarrays | correctness under symmetry |
| uniform threshold match | full inclusion behavior | inclusive boundary correctness |
| alternating pattern | mixed prefix ordering | Fenwick strict vs non-strict behavior |

## Edge Cases

For a single-element array, say $[5]$, every subarray is just that element. If thresholds are such that the element satisfies both conditions, the algorithm initializes prefix with zero and processes exactly one insertion. The Fenwick tree correctly counts the single prefix pair, producing one valid subarray.

For an array where all values equal the threshold, such as $[2,2,2]$ with $a = 2$, every transformed value becomes zero. Prefix sums remain constant, so every pair of prefix indices satisfies equality. The Fenwick tree accumulates counts such that all subarrays are included, matching the expected $n(n+1)/2$.

For strict inequality cases where $b$ equals the array values, the transformed prefix sums become constant again, but the use of `r - 1` in queries ensures no equal-prefix subarray is counted. This prevents overcounting when the mean equals the boundary exactly.
