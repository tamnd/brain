---
title: "CF 102440B - \u041f\u0435\u0440\u0435\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0443 \u043d\u0430 \u043f\u0440\u043e\u043a\u0430\u0447\u043a\u0443"
description: "We start with a permutation p of the numbers from 1 to n. We may delete any elements, but the remaining elements must stay in their original order, so every possible result is a subsequence of the permutation."
date: "2026-08-08T13:43:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102440
codeforces_index: "B"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Junior"
rating: 0
weight: 102440
solve_time_s: 138
verified: false
draft: false
---

[CF 102440B - \u041f\u0435\u0440\u0435\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0443 \u043d\u0430 \u043f\u0440\u043e\u043a\u0430\u0447\u043a\u0443](https://codeforces.com/problemset/problem/102440/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We start with a permutation `p` of the numbers from `1` to `n`. We may delete any elements, but the remaining elements must stay in their original order, so every possible result is a subsequence of the permutation.

For a chosen subsequence of length `m`, its beauty is `m` minus its number of inversions. An inversion is a pair of remaining elements where the earlier element is larger than the later one. Thus every element we keep gives us one point of beauty, while every inversion between kept elements removes one point.

The task is to choose a subsequence whose final value of

`number of kept elements - number of inversions`

is as large as possible.

The bound `n <= 2 * 10^5` immediately rules out algorithms that examine all subsequences, because there are `2^n` of them. Even a quadratic algorithm is generally too large at this scale. We need something around `O(n log n)` or, at worst, close to linear time. The fact that the input is a permutation is also useful because every value is distinct, so "increasing" means strictly increasing without any ambiguity about equal values.

There are several edge cases that can fool an implementation if the underlying observation is missed. For `n = 1`, the only possible subsequence is `[1]`, so the answer is `1`. A method that assumes at least one inversion exists could incorrectly return zero.

Consider

```
4
1 2 3 4
```

The whole permutation has no inversions, so its beauty is `4`. The answer is therefore `4`. An implementation that unnecessarily deletes elements whenever it sees a pattern might lose optimal elements.

Now consider

```
2
2 1
```

Keeping both elements gives length `2` and one inversion, so the beauty is `1`. Keeping only either element also gives beauty `1`. Thus the answer is `1`. A method that simply returns the original length would incorrectly return `2`.

A less obvious case is

```
5
3 1 2 5 4
```

The whole sequence has two inversions, so its beauty is `5 - 2 = 3`. The increasing subsequence `[1, 2, 5]` has length `3` and no inversions, so beauty `3`. This demonstrates that an optimal answer does not necessarily require keeping the maximum possible number of elements.

## Approaches

The direct brute-force approach is to consider every subsequence of the permutation. For each chosen subsequence, we count its inversions and calculate its beauty, then keep the maximum value. This is correct because every legal result is represented by exactly one subsequence.

The problem is the number of subsequences. There are `2^n` choices, and if we inspect up to `n` elements to construct a subsequence and then up to `n^2` pairs to count its inversions, the straightforward implementation can take `O(2^n n^2)` time. Even enumerating the subsequences alone is impossible for `n = 2 * 10^5`.

A more structured attempt would be to use dynamic programming over subsequences, but the inversion term couples every pair of selected elements. Choosing one element can affect the cost with many elements chosen later, so a simple longest-subsequence recurrence does not directly describe beauty.

The key observation removes that difficulty completely.

Suppose a chosen subsequence contains at least one inversion. Pick any element that participates in `k` inversions. If we delete that element, the subsequence length decreases by exactly `1`, while the inversion count decreases by exactly `k`.

Its beauty changes by

`(-1) - (-k) = k - 1`.

If `k >= 1`, deleting the element never decreases beauty. When `k > 1`, beauty actually increases. When `k = 1`, beauty stays unchanged.

We can repeatedly delete elements that belong to inversions. Eventually no inversions remain, so the resulting subsequence is strictly increasing. During this process the beauty never decreases.

This means every subsequence has an increasing subsequence whose beauty is at least as large as the original subsequence's beauty. An increasing subsequence has zero inversions, so its beauty is simply its length.

Consequently, the best possible beauty is exactly the maximum length of an increasing subsequence of the original permutation. In other words, the problem is equivalent to finding the LIS.

The standard `O(n log n)` LIS algorithm maintains an array `tails`, where `tails[k]` is the smallest possible ending value of an increasing subsequence of length `k + 1` seen so far. For every permutation value, binary search finds the first position whose value is at least the current value. Replacing that value preserves the best possible future potential. If the current value is larger than every stored tail, we extend the LIS.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^n n^2)` | `O(n)` per subsequence | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Create an empty array `tails`. Its length will always equal the length of the longest increasing subsequence found so far.
2. Process the permutation from left to right. For the current value `x`, binary search for the first position `pos` in `tails` such that `tails[pos] >= x`.
3. If such a position exists, replace `tails[pos]` with `x`. We do not change the length of the represented subsequence, but we obtain a smaller ending value, which gives more opportunities to extend it with future elements.
4. If no such position exists, `x` is larger than every current tail. Append it to `tails`, because an increasing subsequence can now be extended by one element.
5. After all values have been processed, return `len(tails)`. By the observation above, this LIS length is exactly the maximum achievable beauty.

The reason replacing a tail is safe is that we only care about the best possible ending value for each subsequence length. Suppose two increasing subsequences have the same length, but one ends in `4` and another ends in `7`. The subsequence ending in `4` is always at least as useful for extending later, because every future value that can follow `7` can also follow `4`. Thus keeping the smallest possible tail is the correct state compression.

### Why it works

Consider any subsequence with beauty `B`. If it contains an inversion, choose an element participating in at least one inversion and delete it. If that element participates in `k` inversions, the length drops by one and the inversion count drops by `k`, so the beauty changes by `k - 1 >= 0`. Repeating this process produces an increasing subsequence with beauty at least `B`. Hence no subsequence can have beauty greater than the length of the LIS.

Conversely, the LIS itself is increasing, so it has zero inversions. Its beauty is exactly its length. Thus the LIS length is both an achievable beauty and an upper bound on every possible beauty, making it the exact answer.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(int, input().split()))

    tails = []

    for x in p:
        pos = bisect_left(tails, x)

        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x

    print(len(tails))

if __name__ == "__main__":
    solve()
```

The input is read using `sys.stdin.readline`, which avoids unnecessary overhead when `n` is as large as `2 * 10^5`.

The `tails` array is initially empty. For every value `x`, `bisect_left` finds the first position containing a value greater than or equal to `x`. Because the original input is a permutation, all values are distinct, but `bisect_left` is still the correct choice because the desired subsequence is strictly increasing. If duplicate values were possible, using `bisect_right` would incorrectly allow equal values to extend the subsequence.

When `pos` equals `len(tails)`, `x` is larger than every current tail, so the represented LIS can be extended. Otherwise, replacing `tails[pos]` with `x` keeps the same subsequence length while lowering its ending value.

Python integers do not overflow, although the answer is at most `n` anyway. The binary search also handles the empty `tails` array correctly, so `n = 1` needs no special case.

## Worked Examples

### Sample 1

The input is

```
5
1 2 3 5 4
```

The algorithm processes each value and maintains the smallest possible tail for every increasing-subsequence length.

| Current value | `tails` after processing | LIS length |
| --- | --- | --- |
| `1` | `[1]` | `1` |
| `2` | `[1, 2]` | `2` |
| `3` | `[1, 2, 3]` | `3` |
| `5` | `[1, 2, 3, 5]` | `4` |
| `4` | `[1, 2, 3, 4]` | `4` |

When `4` arrives, it cannot extend the length four subsequence because `4 < 5`. Instead, it replaces `5` as the tail of a length four increasing subsequence. The actual subsequence is `[1, 2, 3, 4]`, which has no inversions and therefore has beauty `4`.

The answer is `4`.

### Sample 2

The input is

```
6
2 1 3 4 5 6
```

The state evolves as follows.

| Current value | `tails` after processing | LIS length |
| --- | --- | --- |
| `2` | `[2]` | `1` |
| `1` | `[1]` | `1` |
| `3` | `[1, 3]` | `2` |
| `4` | `[1, 3, 4]` | `3` |
| `5` | `[1, 3, 4, 5]` | `4` |
| `6` | `[1, 3, 4, 5, 6]` | `5` |

The first two elements cannot both belong to a strictly increasing subsequence. When `1` arrives, it replaces `2` as the smallest possible tail for a subsequence of length one. The later values can then extend that state to length five.

The resulting LIS is `[1, 3, 4, 5, 6]`. Its beauty is `5`, matching the output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Each of the `n` values performs one binary search in `tails`. |
| Space | `O(n)` | `tails` contains at most one value for every LIS length. |

With `n <= 2 * 10^5`, `O(n log n)` requires only a few million binary-search operations, which is appropriate for the constraint. The memory usage is linear and well within the expected limit.

## Test Cases

```python
import sys
import io
from bisect import bisect_left

def solve():
    input = sys.stdin.readline
    n = int(input())
    p = list(map(int, input().split()))

    tails = []

    for x in p:
        pos = bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x

    print(len(tails))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("""5
1 2 3 5 4
""") == "4", "sample 1"

assert run("""6
2 1 3 4 5 6
""") == "5", "sample 2"

# Minimum-size valid permutation
assert run("""1
1
""") == "1", "single element"

# Completely decreasing permutation
assert run("""5
5 4 3 2 1
""") == "1", "strictly decreasing"

# Completely increasing permutation
assert run("""5
1 2 3 4 5
""") == "5", "strictly increasing"

# Mixed case with several replacements in tails
assert run("""7
4 1 6 2 5 3 7
""") == "4", "multiple LIS tail replacements"

# Generalized robustness case with equal values.
# Equal values are not valid under the permutation guarantee,
# but bisect_left correctly computes a strictly increasing subsequence.
assert run("""4
2 2 2 2
""") == "1", "duplicate values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Minimum size and empty-binary-search boundary |
| `5 / 5 4 3 2 1` | `1` | No increasing pair exists |
| `5 / 1 2 3 4 5` | `5` | Entire permutation is already increasing |
| `7 / 4 1 6 2 5 3 7` | `4` | Replacing tails without changing LIS length |
| `4 / 2 2 2 2` | `1` | Strictness of LIS and `bisect_left`; outside the official permutation contract |

The all-equal case is deliberately marked as a robustness test rather than a valid problem instance. The statement guarantees a permutation, so equal values cannot occur in official input. Including the case is still useful for checking that the implementation's binary-search convention matches the definition of a strictly increasing subsequence.

## Edge Cases

For the single-element input

```
1
1
```

`tails` starts empty. The value `1` is inserted at position zero, producing `[1]`, and the answer is `1`. There is no inversion to subtract, so the only possible beauty is indeed `1`.

For the decreasing permutation

```
2
2 1
```

the first value creates `tails = [2]`. The value `1` replaces `2`, giving `tails = [1]`. The LIS length is `1`. The original two-element sequence has one inversion and beauty `2 - 1 = 1`, while deleting either element also gives beauty `1`. This confirms that the algorithm does not assume that keeping more elements always improves beauty.

For an already increasing permutation

```
4
1 2 3 4
```

every value is larger than the current final tail, so `tails` grows to `[1, 2, 3, 4]`. The answer is `4`. Since there are no inversions, the full sequence already realizes that beauty.

For a sequence where an inversion can be removed without losing beauty, consider

```
5
3 1 2 5 4
```

The whole sequence has two inversions, `(3,1)`, `(3,2)`, and also `(5,4)`, so its beauty is actually `5 - 3 = 2`. The LIS algorithm produces `tails` states `[3]`, `[1]`, `[1,2]`, `[1,2,5]`, and finally `[1,2,4]`, giving an LIS of length `3`. The subsequence `[1,2,4]` has no inversions and beauty `3`, which is strictly better than keeping everything. This case demonstrates why the objective cannot be reduced to maximizing subsequence length before accounting for inversions.

For the boundary value `n = 2 * 10^5`, the algorithm still performs exactly one binary search per input value. The size of `tails` is at most `2 * 10^5`, so every operation remains within the `O(log n)` bound. No recursion is used, avoiding recursion-depth concerns, and Python's integer representation is more than sufficient for the answer.
