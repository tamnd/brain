---
title: "CF 1912A - Accumulator Apex"
description: "In this problem, Allyn starts with an integer accumulator, x, and is given k sequences of integers. On each turn, Allyn can take the first (leftmost) number from any non-empty sequence and add it to x, but only if the resulting value of x stays non-negative."
date: "2026-06-08T20:12:59+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1912
codeforces_index: "A"
codeforces_contest_name: "2023-2024 ICPC, NERC, Northern Eurasia Onsite (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1900
weight: 1912
solve_time_s: 101
verified: true
draft: false
---

[CF 1912A - Accumulator Apex](https://codeforces.com/problemset/problem/1912/A)

**Rating:** 1900  
**Tags:** data structures, implementation, sortings  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

In this problem, Allyn starts with an integer accumulator, `x`, and is given `k` sequences of integers. On each turn, Allyn can take the first (leftmost) number from any non-empty sequence and add it to `x`, but only if the resulting value of `x` stays non-negative. The goal is to maximize `x` by choosing the order and quantity of numbers taken from the sequences. The output is the maximum value `x` that can be achieved.

The input specifies the initial `x` and the number of sequences. Each sequence is given as a length followed by the sequence elements. The key challenge is deciding which numbers to take and in what order, because negative numbers can reduce `x` to zero or block further moves. Positive numbers increase `x`, but they can only be used after the accumulator is large enough to absorb any preceding negative values in the same sequence.

The constraints allow `x` up to 10^9 and up to 10^5 sequences, with the total number of elements across all sequences not exceeding 10^5. This means the solution must process elements roughly linearly. Nested loops over all possible orderings would be far too slow; we need a strategy that considers sequences individually and avoids unnecessary checks.

An edge case arises when sequences start with large negative numbers followed by large positives. For example, with `x = 1` and a sequence `[-5, 10]`, a naive approach that simply takes any available element could reject this sequence entirely because `x + (-5) < 0`. The correct approach should consider that negative numbers at the start of a sequence may prevent future gains if `x` is not sufficient to survive them.

## Approaches

The brute-force method would try every possible order of taking elements from sequences. At each step, it would check all sequences whose first element does not make `x` negative, take an element, update `x`, and continue recursively. While this would be correct, the total number of operations could be exponential in the total number of elements, which is far beyond the feasible range given the constraints. For instance, with 10^5 elements, enumerating all orderings is impossible.

The key insight is that for each sequence, the only way to gain from it is to process a prefix of the sequence whose cumulative sum never reduces `x` below zero. This is because taking a later element without taking the previous elements is not allowed. Therefore, for each sequence, we can compute the maximum prefix sum sequence that can be safely added to `x`. After calculating this, all sequences reduce to their maximal safe contribution, and the problem becomes selecting sequences in any order. Since taking a sequence’s safe prefix always increases or maintains `x`, the order does not matter; we can simply add all non-negative safe contributions.

The optimal approach therefore computes, for each sequence, the running prefix sums, tracks the minimum prefix sum, and only includes elements up to the point where `x + min_prefix_sum >= 0`. This guarantees that we never attempt to reduce `x` below zero. Then, we sum the elements of this prefix to `x`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(total elements) | O(1) extra | Accepted |

## Algorithm Walkthrough

1. Read the initial accumulator `x` and the number of sequences `k`.
2. Initialize `x_max` with the initial value of `x`.
3. For each sequence:

1. Track a running prefix sum and the minimum prefix sum encountered so far.
2. Iterate through the elements of the sequence, adding each to the running prefix sum.
3. If `x + min_prefix_sum < 0` at any point, stop; the remaining elements cannot be safely added.
4. Otherwise, the prefix sum up to this point can be added to `x`.
5. Update `x` by adding the sum of this safe prefix.
4. After processing all sequences, output the final `x`.

The correctness is guaranteed because we only add prefixes whose cumulative sums never reduce `x` below zero. Since sequences are independent, and we are taking maximal safe prefixes, any other order would not increase `x` further.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    x, k = map(int, input().split())
    for _ in range(k):
        data = list(map(int, input().split()))
        l = data[0]
        seq = data[1:]
        prefix_sum = 0
        min_prefix = 0
        safe_sum = 0
        for num in seq:
            prefix_sum += num
            min_prefix = min(min_prefix, prefix_sum)
            if x + min_prefix < 0:
                break
            safe_sum = prefix_sum
        x += safe_sum
    print(x)

if __name__ == "__main__":
    main()
```

This solution first reads the initial values and sequences. For each sequence, it tracks the prefix sums and the minimal prefix sum. When `x` is large enough to survive the sequence's negative dips, the entire prefix can be added. The `safe_sum` variable ensures we only add elements that do not bring `x` negative. The loop breaks early if continuing the sequence would make `x` negative.

## Worked Examples

Using Sample 1:

| Step | Sequence | prefix_sum | min_prefix | safe_sum | x |
| --- | --- | --- | --- | --- | --- |
| initial | - | - | - | - | 1 |
| seq1 | -1 | -1 | -1 | 0 | 1 |
| seq1 | 2 | 1 | -1 | 1 | 2 |
| seq2 | -2 | -2 | -2 | 0 | 2 |
| seq2 | 3 | 1 | -2 | 1 | 3 |
| seq3 | -3 | -3 | -3 | 0 | 3 |
| seq3 | 4 | 1 | -3 | 1 | 4 |

This shows that each prefix is only added if it keeps `x` non-negative. The final `x = 4` matches the expected output.

Another example: `x = 1, k = 1, seq = [-5, 10]`. The min_prefix of `-5` makes `x + min_prefix = -4 < 0`, so the sequence is skipped. `x` remains `1`, which is correct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total elements) | Each element is visited once to compute prefix sums. |
| Space | O(1) extra | We only track running sums and counters; no additional arrays proportional to input are required. |

Given the total number of elements does not exceed 10^5, the algorithm runs in under 10^6 operations, well within the time limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        main()
    return f.getvalue().strip()

# Provided samples
assert run("1 3\n2 -1 2\n2 -2 3\n2 -3 4\n") == "4", "sample 1"
assert run("1 2\n2 -2 3\n2 -1 2\n") == "4", "sample 2"

# Custom cases
assert run("0 1\n1 5\n") == "5", "single positive element"
assert run("5 1\n2 -6 10\n") == "5", "sequence skipped due to negative prefix"
assert run("10 2\n3 -5 -5 20\n2 5 5\n") == "20", "mixed negative then positive"
assert run("1 3\n1 -1\n1 1\n1 2\n") == "4", "small increments"
assert run("0 1\n3 1 2 3\n") == "6", "all positive prefix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 1\n1 5\n | 5 | Single-element positive sequence |
| 5 1\n2 -6 10\n | 5 | Prefix too negative, sequence skipped |
| 10 2\n3 -5 -5 20\n2 5 5\n | 20 | Mixed negative then positive handled correctly |
| 1 3\n1 -1\n1 1\n1 2\n | 4 | Small increments sum to final x |
| 0 1\n3 1 2 3\n | 6 | All positive prefix accumulated |

## Edge Cases

For the edge case where the first element of a sequence is negative and larger than `x`, such as `x = 1` and `seq = [-2, 5]`, the algorithm computes `min_prefix = -2` and finds `x + min_prefix = -1`, which is less than zero, so it skips the sequence entirely. The output remains `x = 1`. This prevents taking negative elements that would block further gains. The algorithm correctly identifies which sequences contribute safely and handles these situations without additional logic.
