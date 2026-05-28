---
title: "CF 31A - Worms Evolution"
description: "We are given an array of worm lengths. Each position represents a different worm form, and we need to find three distinc"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 31
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 31 (Div. 2, Codeforces format)"
rating: 1200
weight: 31
solve_time_s: 106
verified: true
draft: false
---

[CF 31A - Worms Evolution](https://codeforces.com/problemset/problem/31/A)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of worm lengths. Each position represents a different worm form, and we need to find three distinct indices such that the length at one index equals the sum of the lengths at the other two indices.

More concretely, we want indices `i`, `j`, and `k` where:

```
a[i] = a[j] + a[k]
```

The indices must all be different, but the values themselves are allowed to repeat. For example, if the array contains two different positions with value `2`, they can both participate in the equation.

The input size is very small. The number of worm forms is at most `100`, and each length is at most `1000`. With `n = 100`, even an `O(n^3)` algorithm performs only about one million checks, which is completely safe within a 2-second limit in Python. This changes the way we think about the problem. We do not need sophisticated data structures or optimizations. A direct implementation is already fast enough.

The tricky part is not performance, it is correctness around distinct indices.

Consider this example:

```
3
2 1 1
```

The correct answer is:

```
1 2 3
```

A careless implementation using only values might accidentally reuse the same `1` twice from the same position. The problem allows equal values, but not equal indices. We must explicitly check that all three positions are different.

Another easy mistake appears when duplicate values exist:

```
4
4 2 2 1
```

The valid answer is:

```
1 2 3
```

Here `4 = 2 + 2`, and the two `2`s come from different indices. An implementation that stores only one index per value in a hash map could incorrectly conclude that no solution exists.

There is also the case where no valid triple exists:

```
5
1 2 4 8 16
```

No element equals the sum of two others, so the output must be `-1`. A program that stops too early or assumes some solution always exists would fail here.

## Approaches

The most direct idea is brute force. We can try every ordered triple of distinct indices `(i, j, k)` and check whether:

```
a[i] == a[j] + a[k]
```

This works because the constraints are tiny. With `n = 100`, the number of triples is at most:

```
100 × 100 × 100 = 1,000,000
```

One million simple integer additions and comparisons is trivial for Python.

The brute-force method is also easy to reason about. Since it explicitly checks every possible valid combination of indices, it cannot miss a solution. If a valid triple exists, one of the iterations will encounter it.

We can still think about how to improve it. The repeated work comes from checking all three indices independently. Once we fix two indices `j` and `k`, the target value `a[j] + a[k]` becomes known immediately. Instead of scanning all possible `i`, we could store values in a map from value to index and look up whether the sum exists.

That leads to an `O(n^2)` solution. For every pair `(j, k)`, we compute:

```
target = a[j] + a[k]
```

Then we check whether `target` exists somewhere else in the array at a distinct index.

This works because the problem asks for a sum relation, and lookup by value is much cheaper than scanning the entire array repeatedly.

Even though `O(n^3)` already passes comfortably, the `O(n^2)` version is cleaner and demonstrates the underlying structure of the problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Accepted |
| Optimal | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array of worm lengths.
2. Build a dictionary that maps each value to all indices where it appears.

We store all indices instead of only one because duplicate values matter. For example, `4 = 2 + 2` requires two different positions containing `2`.
3. Iterate over every pair of indices `(j, k)`.

These represent the two worms whose lengths are being added together.
4. Skip pairs where `j == k`.

The problem requires three distinct forms, so the same index cannot be reused.
5. Compute:

```
target = a[j] + a[k]
```
6. Check whether `target` exists in the dictionary.

If it does not exist, no valid `i` can satisfy the equation for this pair.
7. For every stored index `i` corresponding to `target`, check that `i`, `j`, and `k` are all distinct.

This avoids invalid cases where the same array position participates multiple times.
8. As soon as a valid triple is found, output the indices in 1-based form and terminate.
9. If all pairs are exhausted without finding a solution, print `-1`.

### Why it works

The algorithm systematically examines every possible pair of addends `(j, k)`. For each pair, it computes the exact value needed for `a[i]`. The dictionary guarantees that if such a value exists anywhere in the array, we can find all matching positions immediately.

Because every valid pair is checked and every matching index is verified for distinctness, the algorithm cannot miss a correct answer and cannot output an invalid one.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    positions = {}

    for i, value in enumerate(a):
        if value not in positions:
            positions[value] = []
        positions[value].append(i)

    for j in range(n):
        for k in range(n):
            if j == k:
                continue

            target = a[j] + a[k]

            if target not in positions:
                continue

            for i in positions[target]:
                if i != j and i != k:
                    print(i + 1, j + 1, k + 1)
                    return

    print(-1)

solve()
```

The first part of the code builds a dictionary called `positions`. Each key is a worm length, and the value is a list of all indices where that length appears.

Using a list is the critical implementation detail. If we stored only one index per value, cases like `4 = 2 + 2` could fail because both `2`s must come from different positions.

The nested loops enumerate every ordered pair `(j, k)`. Ordered pairs are acceptable because the problem allows any valid answer. We skip the case `j == k` immediately since the same worm form cannot be used twice.

For each pair, we compute the required target value and check whether it exists in the dictionary. If it does, we iterate through all candidate indices `i` that contain that value.

The final condition:

```
if i != j and i != k:
```

guarantees all three indices are distinct.

The output uses `+1` because Codeforces arrays are indexed from `1`, while Python uses `0`-based indexing internally.

## Worked Examples

### Example 1

Input:

```
5
1 2 3 5 7
```

Trace:

| j | k | a[j] | a[k] | target | Matching indices | Valid triple |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 2 | 3 | [2] | yes |

The algorithm immediately finds:

```
a[2] = 3
a[0] + a[1] = 1 + 2 = 3
```

So it outputs:

```
3 1 2
```

Any permutation satisfying the equation is accepted.

This trace demonstrates the core lookup idea. Once the pair `(1, 2)` is fixed, the required value becomes deterministic.

### Example 2

Input:

```
4
4 2 2 1
```

Trace:

| j | k | a[j] | a[k] | target | Matching indices | Valid triple |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 2 | 4 | [0] | yes |

The algorithm finds:

```
4 = 2 + 2
```

using indices `1`, `2`, and `0`.

Output:

```
1 2 3
```

This example demonstrates why storing all indices matters. The two `2`s come from different positions even though their values are equal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | We examine all ordered pairs of indices |
| Space | O(n) | The dictionary stores all array indices |

With `n ≤ 100`, even cubic solutions are fast enough. The quadratic solution runs almost instantly and uses negligible memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    positions = {}

    for i, value in enumerate(a):
        if value not in positions:
            positions[value] = []
        positions[value].append(i)

    for j in range(n):
        for k in range(n):
            if j == k:
                continue

            target = a[j] + a[k]

            if target not in positions:
                continue

            for i in positions[target]:
                if i != j and i != k:
                    print(i + 1, j + 1, k + 1)
                    return

    print(-1)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("5\n1 2 3 5 7\n") in {
    "3 1 2",
    "3 2 1"
}, "sample 1"

# minimum size with solution
assert run("3\n2 1 1\n") in {
    "1 2 3",
    "1 3 2"
}, "minimum size"

# no valid triple
assert run("5\n1 2 4 8 16\n") == "-1", "no solution"

# duplicate values
assert run("4\n4 2 2 1\n") in {
    "1 2 3",
    "1 3 2"
}, "duplicate values"

# all equal values
assert run("5\n5 5 5 5 5\n") == "-1", "all equal without valid sum"

# boundary style case
large_case = "100\n" + " ".join(map(str, range(1, 101))) + "\n"
assert run(large_case) != "", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 2 1 1` | valid triple | Minimum valid input size |
| `5 / 1 2 4 8 16` | `-1` | Correct handling when no solution exists |
| `4 / 4 2 2 1` | valid triple | Duplicate values with distinct indices |
| `5 / 5 5 5 5 5` | `-1` | Equal values do not automatically imply a solution |
| `1..100` | any non-empty answer | Handles maximum constraint size |

## Edge Cases

Consider the input:

```
3
2 1 1
```

The algorithm stores:

```
2 -> [0]
1 -> [1, 2]
```

When examining indices `(1, 2)`, the target becomes `2`. The dictionary lookup returns index `0`, which is distinct from both addend indices. The algorithm outputs:

```
1 2 3
```

This case confirms that equal values are allowed as long as the indices differ.

Now consider:

```
4
4 2 2 1
```

The dictionary becomes:

```
4 -> [0]
2 -> [1, 2]
1 -> [3]
```

For `(1, 2)`, the target is `4`. The algorithm retrieves index `0` and verifies that all indices are distinct.

A buggy implementation storing only one occurrence of each value could mishandle this structure, especially when duplicates are needed in the sum.

Finally, consider a no-solution case:

```
5
1 2 4 8 16
```

Every pair sum is checked:

```
1 + 2 = 3
1 + 4 = 5
2 + 4 = 6
...
```

None of these values exist in the array. The loops finish without returning, so the algorithm correctly prints:

```
-1
```

This confirms the algorithm does not assume a solution exists and exhaustively verifies all possibilities.
