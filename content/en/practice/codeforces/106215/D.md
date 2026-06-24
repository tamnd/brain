---
title: "CF 106215D - Distance Indicators"
description: "We are given an array a where each position represents a word and its assigned score. For every pair of indices (i, j) with i < j, the problem defines $$text{dist}(i,j)=ai+aj$$ A pair is considered beautiful when the distance exactly matches the difference between their…"
date: "2026-06-25T06:50:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106215
codeforces_index: "D"
codeforces_contest_name: "2025-2026 Whitney Young Practice Contest 1"
rating: 0
weight: 106215
solve_time_s: 43
verified: true
draft: false
---

[CF 106215D - Distance Indicators](https://codeforces.com/problemset/problem/106215/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array `a` where each position represents a word and its assigned score.

For every pair of indices `(i, j)` with `i < j`, the problem defines

$$\text{dist}(i,j)=a_i+a_j$$

A pair is considered beautiful when the distance exactly matches the difference between their positions:

$$j-i=a_i+a_j$$

For each test case, we must count how many pairs satisfy this equality.

The array length can be as large as `2 · 10^5`, and the sum of all `n` across test cases is also at most `2 · 10^5`. Any solution that checks every pair would require roughly

$$\frac{n(n-1)}2$$

comparisons. For `n = 2 · 10^5`, that is about `2 · 10^{10}` operations, which is completely infeasible.

The total input size strongly suggests that we need something close to linear time per test case, or at worst `O(n log n)`.

A subtle observation comes from the bounds on `a_i`. Since every score is positive, if `a_i >= n`, then no pair involving `i` can ever be beautiful because

$$a_i+a_j \ge a_i+1 > n-1$$

while the largest possible value of `j-i` is only `n-1`.

### Edge Case 1: No possible pairs

Input:

```
1
3
2025 2025 2025
```

Every score is much larger than any possible index difference. The answer is:

```
0
```

A naive implementation that does not exploit this fact remains correct, but wastes enormous time checking impossible pairs.

### Edge Case 2: Multiple valid pairs sharing indices

Input:

```
1
5
1 1 1 1 1
```

The valid pairs are `(1,3)`, `(2,4)`, and `(3,5)` because each has distance `2`.

Answer:

```
3
```

A careless counting strategy that marks an index as already used would undercount.

### Edge Case 3: Large values near the array boundary

Input:

```
1
4
3 1 1 1
```

For index `1`, every possible distance is at least `4`, but the maximum index difference is only `3`.

Answer:

```
0
```

This illustrates why many positions can be discarded immediately.

## Approaches

The most direct solution is to examine every pair `(i, j)`, compute `a_i + a_j`, compare it with `j - i`, and count matches.

The method is obviously correct because it checks the exact condition from the definition. The problem is its complexity. For `n = 2 · 10^5`, the number of pairs is roughly twenty billion, far beyond the limit.

To find something faster, rewrite the condition:

$$j-i=a_i+a_j$$

Move terms involving the same index to the same side:

$$j-a_j=i+a_i$$

Now the pair is beautiful exactly when the value

$$i+a_i$$

for the left endpoint equals

$$j-a_j$$

for the right endpoint.

This transforms the problem from checking pairs into counting equal values.

Suppose we process indices from left to right. When we arrive at position `j`, we need to know how many earlier positions `i` satisfy

$$i+a_i=j-a_j$$

If we maintain a frequency map of all previously seen values `i+a_i`, then the number of valid partners for `j` is simply the frequency of `j-a_j`.

Each index contributes exactly once, giving a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal Hash Map | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create an empty frequency map.
2. Process the array from left to right using 1-based indexing.
3. For the current position `j`, compute:

$$key = j - a_j$$

Every earlier index `i` satisfying `i + a_i = key` forms a beautiful pair with `j`.

1. Add the frequency of `key` to the answer.

This counts all valid earlier partners and no invalid ones because the transformed equation is exactly equivalent to the original condition.

1. Compute

$$store = j + a_j$$

and insert it into the frequency map.

Future positions may use this index as their left endpoint.

1. Continue until all positions are processed.

### Why it works

The frequency map always contains values `i + a_i` for indices strictly smaller than the current position.

When processing index `j`, every beautiful pair must satisfy

$$i+a_i=j-a_j$$

and every index in the map already has `i < j`. Thus the frequency of `j-a_j` is exactly the number of valid earlier indices. Every beautiful pair is counted once when its right endpoint is processed, and no invalid pair can satisfy the transformed equality. This establishes correctness.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = defaultdict(int)
        ans = 0

        for i in range(1, n + 1):
            x = a[i - 1]

            ans += freq[i - x]
            freq[i + x] += 1

        print(ans)

solve()
```

The solution follows the algebraic transformation directly.

The variable `freq` stores counts of values `i + a_i` from previously processed indices. For each position, we first query `freq[i - a_i]` because only earlier indices may form valid pairs. After counting contributions, we insert `i + a_i` into the map.

The order is important. If insertion happened first, the current index could incorrectly match itself when `a_i = 0`. The problem guarantees positive values, but maintaining the correct order keeps the logic mathematically precise.

Using 1-based indexing in the loop matches the original equation exactly and avoids extra adjustments during derivation.

## Worked Examples

### Example 1

Input:

```
1
5
1 1 1 1 1
```

| i | a[i] | i - a[i] | Matches Found | i + a[i] Stored | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 0 | 2 | 0 |
| 2 | 1 | 1 | 0 | 3 | 0 |
| 3 | 1 | 2 | 1 | 4 | 1 |
| 4 | 1 | 3 | 1 | 5 | 2 |
| 5 | 1 | 4 | 1 | 6 | 3 |

Final answer:

```
3
```

The three counted pairs are `(1,3)`, `(2,4)`, and `(3,5)`.

### Example 2

Input:

```
1
4
3 1 1 1
```

| i | a[i] | i - a[i] | Matches Found | i + a[i] Stored | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | -2 | 0 | 4 | 0 |
| 2 | 1 | 1 | 0 | 3 | 0 |
| 3 | 1 | 2 | 0 | 4 | 0 |
| 4 | 1 | 3 | 1 | 5 | 1 |

Final answer:

```
1
```

The only beautiful pair is `(2,4)` because

$$4-2=2$$

and

$$1+1=2.$$

This example demonstrates that the transformed equality detects the pair automatically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is processed once |
| Space | O(n) | The frequency map may store up to n distinct keys |

Since the sum of all array lengths across test cases is at most `2 · 10^5`, the total running time is linear in the input size. This easily fits within the contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = defaultdict(int)
        ans = 0

        for i in range(1, n + 1):
            ans += freq[i - a[i - 1]]
            freq[i + a[i - 1]] += 1

        out.append(str(ans))

    return "\n".join(out)

# custom cases

assert run("1\n1\n1\n") == "0", "minimum size"

assert run("1\n5\n1 1 1 1 1\n") == "3", "multiple matches"

assert run("1\n3\n2025 2025 2025\n") == "0", "all impossible"

assert run("1\n4\n3 1 1 1\n") == "1", "boundary example"

assert run("1\n6\n1 2 3 1 2 3\n") == "1", "general case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `0` | Minimum array size |
| `1 / 5 / 1 1 1 1 1` | `3` | Multiple valid pairs |
| `1 / 3 / 2025 2025 2025` | `0` | Very large values |
| `1 / 4 / 3 1 1 1` | `1` | Boundary differences |
| `1 / 6 / 1 2 3 1 2 3` | `1` | General mixed case |

## Edge Cases

Consider:

```
1
3
2025 2025 2025
```

Processing produces keys `-2024`, `-2023`, and `-2022`. None of these values ever appear as a stored value `i + a_i`, so every lookup returns zero. The algorithm outputs:

```
0
```

which is correct because no index difference can reach thousands.

Consider:

```
1
5
1 1 1 1 1
```

The stored values become `2, 3, 4, 5, 6`. At positions `3`, `4`, and `5`, the queried values are `2`, `3`, and `4`, each already present exactly once. The answer becomes `3`, correctly counting all valid pairs without double counting.

Consider:

```
1
4
3 1 1 1
```

The map evolves as:

```
after i=1: {4:1}
after i=2: {4:1,3:1}
after i=3: {4:2,3:1}
```

At `i=4`, the query value is `3`, which exists once. The answer increases by one and finishes at:

```
1
```

matching the only beautiful pair `(2,4)`.
