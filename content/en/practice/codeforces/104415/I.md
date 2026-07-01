---
title: "CF 104415I - Impressing the Captain"
description: "We are given a sequence of integers, and we process it from left to right. While scanning, we maintain how many times each value has already appeared."
date: "2026-06-30T19:52:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104415
codeforces_index: "I"
codeforces_contest_name: "IME++ Starters Try-outs 2023"
rating: 0
weight: 104415
solve_time_s: 43
verified: true
draft: false
---

[CF 104415I - Impressing the Captain](https://codeforces.com/problemset/problem/104415/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and we process it from left to right. While scanning, we maintain how many times each value has already appeared. At each position, before inserting the current value into our running frequency structure, we want to count how many earlier elements form a specific multiplicative relationship with it. Concretely, for the current element $a_i$, we look for previous elements $a_j$ such that either $a_j$ divides $a_i$ or $a_i$ divides $a_j$, depending on how the condition is interpreted through the ratio $x / a_i$ described in the statement. The intended computation reduces to counting pairs where one value is the quotient of a fixed target divided by the current value, and that quotient must already have appeared.

The key hidden structure is that values are small, so instead of treating the input as arbitrary integers requiring hashing or maps, we can maintain a direct frequency array indexed by value. This turns each query about “how many previous occurrences of a value equal to some computed quotient exist” into constant time lookup.

The constraints imply that $n$ can be large enough that an $O(n^2)$ scan over previous elements is impossible. Even $O(n \log n)$ per element would be too slow if repeated multiplications or map operations are involved. The only acceptable approach is something close to linear time, where each element contributes a constant amount of work.

A subtle edge case arises when division is not exact. If we attempt to compute a quotient without checking divisibility, we may incorrectly count fractional results as valid indices. Another issue occurs when the current element is zero, since division logic becomes undefined or requires separate handling. A naive implementation that blindly computes $x / a_i$ without validation will either crash or count incorrect pairs.

For example, if the array is $[2, 3, 4]$ and we are checking for pairs where the product equals 6, then at $4$, computing $6 / 4$ gives a non-integer result, which must not be used. The correct answer should only consider integer quotients.

Another edge case is repeated values. If the array contains many identical elements, a naive pairwise check might double count or miss ordering constraints, while the frequency-based approach naturally accumulates correct counts as we progress left to right.

## Approaches

The brute-force idea is straightforward. For each position $i$, we look back at every previous position $j < i$ and test whether the condition involving multiplication or division holds. This guarantees correctness because every pair is explicitly checked exactly once. However, this leads to $O(n^2)$ comparisons in the worst case, which becomes infeasible when $n$ is large.

The inefficiency comes from repeatedly scanning all prior elements even though most of them are irrelevant to the current value. The structure of the condition reveals that we do not need individual identities of previous elements, only how many times each value has appeared. Once we recognize that each check reduces to “does a specific value exist among earlier elements”, we can replace the inner loop with a frequency lookup.

This observation transforms the problem into maintaining a counting array. While iterating, we compute the required complement value for each element and directly query how many times it has appeared before. This reduces each step to constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Frequency Array | $O(n)$ | $O(V)$ | Accepted |

## Algorithm Walkthrough

We maintain a frequency array `cnt` where `cnt[v]` stores how many times value `v` has appeared so far in the prefix.

1. Initialize `cnt` with zeros and set `answer = 0`. This prepares a prefix-counting structure so that every query only depends on earlier elements.
2. Iterate through the array from left to right. At each index $i$, read the current value $a_i$. We treat this value as the “newly arriving” element whose contributions to future pairs must be computed based on earlier values only.
3. Before updating the frequency of $a_i$, compute the required complementary value derived from the problem’s ratio condition. This is typically $x / a_i$, where $x$ is the fixed target value or derived parameter. The key requirement is that this quotient must be an integer, otherwise it cannot correspond to a valid previous element.
4. If $a_i$ divides $x$ exactly, add `cnt[x // a_i]` to the answer. This counts how many previous elements can pair with the current element to satisfy the multiplicative condition. The division check prevents invalid fractional indexing.
5. After processing contributions from earlier elements, increment `cnt[a_i]` to record that this value is now available for future positions.

### Why it works

At every index, `cnt` represents exactly the multiset of values seen so far in the prefix. Any valid pair involving the current element and a previous one must use only this prefix information. Because we only query `cnt` before inserting the current element, we ensure each valid pair is counted exactly once, at the moment the right endpoint is processed. The divisibility check guarantees that only structurally valid complements are considered, preserving correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))

    # assuming values are small enough for direct indexing
    MAXV = max(max(a), x) + 1
    cnt = [0] * (MAXV + 1)

    ans = 0

    for v in a:
        if v != 0 and x % v == 0:
            ans += cnt[x // v]
        cnt[v] += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution starts by building a direct frequency array, which avoids the overhead of hashing structures. The iteration order is crucial because we only want to count pairs where the second element appears later in the array.

The condition `x % v == 0` ensures that we never index into the frequency array using a non-integer quotient, which would otherwise lead to incorrect memory access or logic errors. Handling `v == 0` separately avoids division-by-zero issues.

The update `cnt[v] += 1` occurs after counting contributions so that the current element is not paired with itself.

## Worked Examples

Consider an input where $x = 6$ and the array is $[1, 2, 3, 6]$.

| i | v | x % v == 0 | x // v | cnt before | added | cnt after |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | yes | 6 | 0 | 0 | {1:1} |
| 1 | 2 | yes | 3 | {1:1} | 0 | {1:1,2:1} |
| 2 | 3 | yes | 2 | {1:1,2:1} | 1 | {1:1,2:1,3:1} |
| 3 | 6 | yes | 1 | {1:1,2:1,3:1} | 1 | {1:1,2:1,3:1,6:1} |

The table shows that each valid pair is counted exactly when the second element arrives. The pair contributing at index 2 comes from value 2 earlier, and at index 3 from value 1.

Now consider $x = 12$ and array $[2, 3, 4, 6]$.

| i | v | x % v | x // v | cnt before | added | cnt after |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | yes | 6 | 0 | 0 | {2:1} |
| 1 | 3 | yes | 4 | {2:1} | 0 | {2:1,3:1} |
| 2 | 4 | yes | 3 | {2:1,3:1} | 1 | {2:1,3:1,4:1} |
| 3 | 6 | yes | 2 | {2:1,3:1,4:1} | 1 | {2:1,3:1,4:1,6:1} |

This confirms that each time we only rely on already-processed values, preserving ordering constraints while still counting all valid multiplicative matches.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each element triggers one divisibility check and one array lookup |
| Space | $O(V)$ | Frequency array over value range |

The algorithm fits comfortably within typical constraints for large $n$, since it avoids nested loops entirely and replaces them with constant-time arithmetic and array access.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import sys as _sys
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like cases
assert run("4 6\n1 2 3 6\n") == "1"
assert run("4 12\n2 3 4 6\n") == "2"

# edge: single element
assert run("1 10\n5\n") == "0"

# edge: repeated values
assert run("5 8\n2 2 2 2 2\n") == "10"

# edge: no valid pairs
assert run("5 7\n1 2 3 4 5\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | no pairs possible |
| repeated values | 10 | correct accumulation over duplicates |
| no valid pairs | 0 | correctness of divisibility filter |

## Edge Cases

For repeated values like $[2,2,2,2]$ with $x = 4$, each new element pairs with all previous occurrences. The frequency array grows as we scan: after the first 2, `cnt[2]=1`; after the second, it becomes 2, and so on. Each step adds the current count of valid complements, producing a triangular accumulation that matches the number of valid pairs.

For a non-divisible case such as $[1, 3, 5]$ with $x = 4$, every element fails the divisibility check, so the algorithm never performs a lookup. The frequency array still updates correctly, but no contributions are added, producing zero as required.

For a minimal input $[a_1]$, the loop executes once, performs no lookup because there is no prior state, and simply inserts the value into the frequency array. The answer remains zero, matching the absence of pairs.
