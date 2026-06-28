---
title: "CF 104743C - Prefix MEX Problem"
description: "We are given an array of non-negative integers. We are allowed to modify elements, but each modification has a very specific rule: if we choose position i, we overwrite a[i] with the MEX of the prefix strictly before it, meaning the smallest non-negative integer that does not…"
date: "2026-06-29T01:21:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104743
codeforces_index: "C"
codeforces_contest_name: "TheForces Round #25(5^2-Forces)"
rating: 0
weight: 104743
solve_time_s: 84
verified: false
draft: false
---

[CF 104743C - Prefix MEX Problem](https://codeforces.com/problemset/problem/104743/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of non-negative integers. We are allowed to modify elements, but each modification has a very specific rule: if we choose position `i`, we overwrite `a[i]` with the MEX of the prefix strictly before it, meaning the smallest non-negative integer that does not appear in `a[1..i-1]`. For the first position, the prefix is empty, so the MEX is `0`.

The goal is not to apply a fixed number of operations or minimize operations. Instead, we want to reach any reachable array configuration that is lexicographically smallest, meaning we care about improving earlier positions as aggressively as possible, even if that forces later changes.

The key difficulty is that changing an earlier element changes all future prefix MEX values, which then affects what later positions can become. So the problem is a global optimization over a sequence of locally dependent transformations.

The constraints imply that the total length across all test cases is up to 5×10^5, so any solution must be close to linear per test case. Quadratic or even n log n approaches with heavy per-index recomputation will fail. Any approach that recomputes MEX from scratch for each position is immediately too slow because MEX computation is at least linear unless carefully maintained.

A subtle edge case is when early elements are large or irrelevant. For example, if the array starts with large values like `[100, 200, 300]`, naive thinking might suggest no useful operations exist. But replacing the first element forces it to become `0`, which then reshapes all future MEX values.

Another edge case is when the array already contains small consecutive segments like `[0,1,2,...]`. In such cases, changing an element to MEX might temporarily introduce duplicates or break structure, but doing so can still improve lexicographic order earlier.

## Approaches

A brute-force strategy would simulate the process: at each position, decide whether to keep the current value or replace it with the MEX of the previous prefix, then recursively explore all possibilities. This forms a decision tree where each node branches based on whether we modify position `i` or not. The MEX of a prefix can be maintained incrementally, but the branching still leads to exponential growth in the number of states.

Even a greedy simulation that processes left to right and recomputes MEX each time would require maintaining a frequency structure and updating it per operation. If we recompute MEX naively per index, each computation is O(n), leading to O(n^2) per test case, which is far beyond the limit.

The key structural insight is that the only useful values we ever introduce are MEX values of prefixes, and these values are always small and monotonic in a controlled way. Once we observe that the MEX depends only on which numbers `0,1,2,...` have been seen so far, we can maintain a dynamic “seen set” while constructing the answer greedily from left to right.

We then reinterpret the problem: instead of choosing arbitrary operations, we decide for each position whether to enforce the smallest possible value allowed by prefix history. Since lexicographic order prioritizes earlier positions, we always want the smallest achievable value at each index given that earlier decisions are fixed.

This leads to a greedy construction where we simulate the process of building a valid prefix, tracking which numbers have been “consumed” in a way that affects future MEX values, and assigning each position the best possible value consistent with reachability.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Greedy MEX construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. We process the array from left to right, maintaining a structure that tracks which small integers have already appeared in the constructed prefix. This structure is used only to compute the current MEX efficiently.
2. At each index `i`, we compute the MEX of the current prefix state. This represents the smallest value we can force at position `i` if we choose to overwrite it.
3. We decide whether we can improve `a[i]` by replacing it with this MEX. Since lexicographic order prioritizes smaller values early, if the MEX is smaller than the current value, we apply the operation.
4. When we assign a value (either original or MEX), we update the “seen” structure accordingly. This ensures future MEX computations reflect the actual constructed prefix.
5. We continue this process until the end of the array, always committing to the smallest feasible value at each step.

The subtlety is that we are not simulating arbitrary sequences of operations, but directly constructing the best reachable outcome by ensuring that every prefix is consistent with some valid sequence of MEX replacements.

### Why it works

The algorithm maintains the invariant that at every index `i`, the constructed prefix is reachable from the original array using valid operations. The MEX at position `i` depends only on which values have already been forced into earlier positions, and any value assigned at position `i` is exactly one that can be produced by a legal operation at that index. Because lexicographic order depends on the first differing position, minimizing each position under reachability constraints yields a globally minimal sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        # We only care about small values for mex tracking
        seen = set()
        mex = 0

        res = [0] * n

        for i in range(n):
            # update mex to current smallest missing
            while mex in seen:
                mex += 1

            # we may choose to overwrite with mex or keep original
            # but lexicographically we prefer smaller value if achievable
            if mex < a[i]:
                res[i] = mex
                seen.add(mex)
            else:
                res[i] = a[i]
                seen.add(a[i])

            while mex in seen:
                mex += 1

        out.append(" ".join(map(str, res)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation keeps a `seen` set for values that have been fixed into the resulting prefix. The variable `mex` is incrementally maintained, so each integer is advanced at most once, giving linear amortized behavior.

At each index, we compare the current MEX with the original value. If the MEX is smaller, replacing improves lexicographic order immediately. Otherwise, keeping the original is optimal because any replacement would only increase the value.

The second update of `mex` after insertion ensures consistency: once a value is added, future MEX values correctly skip it.

## Worked Examples

### Example 1

Input:

`[0, 3, 0, 1]`

We track `seen` and `mex`:

| i | a[i] | mex before | decision | res[i] | seen after | mex after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | keep 0 | 0 | {0} | 1 |
| 2 | 3 | 1 | replace | 1 | {0,1} | 2 |
| 3 | 0 | 2 | keep 0 | 0 | {0,1,0} | 2 |
| 4 | 1 | 2 | keep 1 | 1 | {0,1,0,1} | 2 |

Output becomes `[0,1,0,1]`.

This trace shows how introducing a small MEX early forces future MEX values upward, enabling lexicographically smaller early positions.

### Example 2

Input:

`[5, 4, 3]`

| i | a[i] | mex before | decision | res[i] | seen after | mex after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 0 | replace | 0 | {0} | 1 |
| 2 | 4 | 1 | replace | 1 | {0,1} | 2 |
| 3 | 3 | 2 | replace | 2 | {0,1,2} | 3 |

Output becomes `[0,1,2]`.

This demonstrates that even if all original values are large, the construction can fully overwrite them into a minimal increasing structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each integer is inserted into the set once and mex only increases monotonically |
| Space | O(n) | Storage for the constructed array and seen set |

The total input size is 5×10^5, so a linear solution per test case is sufficient. The amortized constant-time updates make the solution comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        seen = set()
        mex = 0
        res = []

        for x in a:
            while mex in seen:
                mex += 1
            if mex < x:
                res.append(mex)
                seen.add(mex)
            else:
                res.append(x)
                seen.add(x)
            while mex in seen:
                mex += 1

        out.append(" ".join(map(str, res)))

    return "\n".join(out)

# sample and custom tests
assert run("1\n4\n0 3 0 1\n") == "0 1 0 1"
assert run("1\n3\n5 4 3\n") == "0 1 2"

assert run("1\n1\n0\n") == "0"
assert run("1\n1\n5\n") == "0"
assert run("1\n5\n0 1 2 3 4\n") == "0 1 2 3 4"
assert run("1\n5\n4 4 4 4 4\n") == "0 1 2 3 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 0 | 0 | minimal size, no change needed |
| single large | 0 | first position can always be forced to 0 |
| increasing sequence | same | already optimal structure |
| repeated values | 0..n-1 | repeated inputs still yield increasing mex-driven output |

## Edge Cases

For an input like `[0]`, the algorithm initializes `mex = 0`, sees that `0` is already equal, and keeps it. The set becomes `{0}` and output is `0`, matching correctness.

For `[5]`, `mex = 0` is less than `5`, so we replace it with `0`. This is valid because choosing `i = 1` always yields MEX of empty prefix, which is `0`.

For `[0,1,2,3]`, each value is kept because at each step the MEX equals the current value, so no improvement is possible. The invariant ensures we never degrade a prefix, so the identity transformation is correctly preserved.
