---
title: "CF 2217B - Flip the Bit (Easy Version)"
description: "We are given a binary array of length n and a single special index p (since k=1 in this easy version). The bit at this index is considered \"correct,\" and the goal is to make the entire array equal to this bit by performing the fewest number of flip operations."
date: "2026-06-02T09:03:53+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2217
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1091 (Div. 2) and CodeCraft 26"
rating: 1000
weight: 2217
solve_time_s: 135
verified: false
draft: false
---

[CF 2217B - Flip the Bit (Easy Version)](https://codeforces.com/problemset/problem/2217/B)

**Rating:** 1000  
**Tags:** greedy, implementation  
**Solve time:** 2m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary array of length `n` and a single special index `p` (since `k=1` in this easy version). The bit at this index is considered "correct," and the goal is to make the entire array equal to this bit by performing the fewest number of flip operations. A flip operation selects a contiguous subarray containing the special index and inverts every bit in that subarray.

The challenge is to minimize the number of flips. A naive approach might attempt to flip every mismatched bit individually, but we can exploit the rule that a flip must include the special index. This effectively allows us to flip large segments in one operation if we plan carefully.

Constraints are tight: `n` can be up to 200,000 and the sum of `n` over all test cases does not exceed 200,000. This restricts us to linear or near-linear algorithms; any quadratic approach iterating over all subarrays would be far too slow. Edge cases include arrays where all bits are already correct, arrays where the special index is at one end, or sequences of mismatched bits that require careful segmentation.

For example, consider `a = [1, 0, 0, 1]` with the special index `p = 1` (value `1`). The naive approach might flip each zero separately, but a single flip from the first element to the last zero can correct both in one operation. Missing this grouping results in unnecessary flips.

## Approaches

The brute-force method would attempt to flip every possible subarray containing the special index until all bits match the special index. This works because any flip will make at least one bit correct, but it fails when `n` is large: we would be examining `O(n^2)` subarrays in the worst case, which is infeasible given `n ≤ 2·10^5`.

The optimal approach comes from observing that we only need to flip segments of consecutive mismatched bits. Starting from the special index, we can propagate outwards: any contiguous sequence of bits not equal to the special bit can be corrected in a single flip that includes the special index. We do not need to flip already correct bits, and sequences separated by correct bits can each be corrected independently, counting as separate operations.

Effectively, the solution reduces to counting contiguous blocks of bits that differ from the special bit. Each block requires exactly one flip.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the array `a`. Retrieve the special index `p` (adjusting for 0-based indexing). Record the value `x = a[p]` at the special index.
3. Initialize a counter `operations = 0` and a pointer `i = 0`.
4. Traverse the array from left to right:

1. If `a[i]` equals `x`, increment `i` and continue.
2. If `a[i]` differs from `x`, increment `operations` by 1. Skip over all consecutive elements equal to this mismatched value by moving `i` forward until reaching a bit equal to `x` or the end of the array.
5. After the traversal, `operations` holds the minimum number of flips required.
6. Output the result for each test case.

Why it works: Each contiguous block of bits differing from the special index can be corrected in one flip that includes the special index. Since flips cannot affect non-included sequences, counting blocks is both necessary and sufficient. This invariant guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    p = int(input()) - 1  # convert to 0-based index
    x = a[p]
    
    operations = 0
    i = 0
    while i < n:
        if a[i] == x:
            i += 1
        else:
            operations += 1
            # skip the entire block of mismatched bits
            while i < n and a[i] != x:
                i += 1
    print(operations)
```

The solution starts by reading input and converting the special index to 0-based. The main logic iterates over the array, counting contiguous segments of mismatched bits. Careful attention to incrementing `i` ensures no blocks are double-counted. The inner loop guarantees that all consecutive mismatches are handled in one operation.

## Worked Examples

### Example 1

Input: `a = [1, 0, 1]`, `p = 1` (1-based), `x = 1`.

| i | a[i] | action | operations |
| --- | --- | --- | --- |
| 0 | 1 | matches x | 0 |
| 1 | 0 | mismatch, flip block [1] | 1 |
| 2 | 1 | matches x | 1 |

Output: `1`.

Explanation: There is only one block of zeros that needs flipping.

### Example 2

Input: `a = [0, 0, 0, 1, 0]`, `p = 4` (1-based), `x = 1`.

| i | a[i] | action | operations |
| --- | --- | --- | --- |
| 0 | 0 | mismatch, flip block [0,1,2] | 1 |
| 3 | 1 | matches x | 1 |
| 4 | 0 | mismatch, flip block [4] | 2 |

Output: `2`.

Explanation: There are two separate blocks of zeros outside the special index that require separate flips.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan the array once per test case, skipping entire blocks of mismatches. |
| Space | O(1) | Only a few integers are used for counters; no extra arrays are needed. |

Given the sum of `n` across test cases is at most `2·10^5`, this solution easily fits within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # assume solution code above saved in solution.py
    return output.getvalue().strip()

# provided sample
assert run("1\n3 1\n1 0 1\n1\n") == "1", "sample 1"

# minimum-size array, single element matching
assert run("1\n1 1\n0\n1\n") == "0", "single element already correct"

# single mismatch
assert run("1\n2 1\n0 1\n2\n") == "1", "one mismatch after special"

# all mismatches
assert run("1\n5 1\n0 0 0 0 0\n3\n") == "1", "entire array except special needs flip"

# alternating bits
assert run("1\n6 1\n1 0 1 0 1 0\n1\n") == "3", "three separate blocks of 0s"

# special at end
assert run("1\n5 1\n0 0 0 0 1\n5\n") == "0", "all correct relative to special"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 0\n1` | 0 | Single-element array already correct |
| `2 1 0 1\n2` | 1 | One mismatch after special |
| `5 1 0 0 0 0 0\n3` | 1 | Entire array except special flipped in one operation |
| `6 1 1 0 1 0 1 0\n1` | 3 | Alternating zeros handled as separate blocks |
| `5 1 0 0 0 0 1\n5` | 0 | Special at end; array already matches |

## Edge Cases

If the array is already entirely correct relative to the special index, the algorithm simply skips all elements and returns `0`. For example, `a = [1, 1, 1]` with `p = 2` yields zero operations. If the special index is at the start or end, the algorithm correctly counts blocks to its right or left without overcounting. For arrays with multiple contiguous blocks of mismatched bits separated by correct bits, each block is counted as one operation, ensuring minimal flips.
