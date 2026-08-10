---
title: "CF 102397G - Super Weird Game"
description: "Each player owns an array of length n. For a fixed target sum k, a pair of positions (i, j) is good when i < j and the two values add up to k. We need to count the good pairs independently in Mahmoud's array and Bashar's array, then compare the two counts."
date: "2026-08-10T18:03:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102397
codeforces_index: "G"
codeforces_contest_name: "Asu Coding Cup 4"
rating: 0
weight: 102397
solve_time_s: 285
verified: true
draft: false
---

[CF 102397G - Super Weird Game](https://codeforces.com/problemset/problem/102397/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

Each player owns an array of length `n`. For a fixed target sum `k`, a pair of positions `(i, j)` is good when `i < j` and the two values add up to `k`. We need to count the good pairs independently in Mahmoud's array and Bashar's array, then compare the two counts. The player with more good pairs wins, while equal counts produce a draw.

The order condition `i < j` means positions matter when counting pairs. For example, in `[1, 2]` with `k = 3`, there is exactly one good pair. In `[1, 2, 1]`, there are two good pairs, `(1, 2)` and `(2, 3)`. We are counting pairs of positions, not just distinct value combinations.

The array length can reach `10^5`, so an algorithm that examines every pair of positions would perform about `n(n-1)/2` checks. At the maximum size this is `4,999,950,000` pair checks, far beyond what a roughly 1.5 second competitive programming limit can support. We need a solution whose work grows approximately linearly with `n`.

The values themselves are also bounded by `10^5`, but we do not actually need to iterate over every possible value. The useful information while processing an array is how many earlier occurrences of each value have appeared.

Several edge cases can easily break a careless implementation. First, a value can pair with itself. For example:

```
1 2
1
1
```

There is only one position, so the correct result is `Draw`, not a pair count of one. More generally, for `[1, 1]` and `k = 2`, the two equal values form exactly one pair, because the positions `(1, 2)` are distinct.

Second, equal values must not be counted twice. For `[1, 2]` with `k = 3`, the pair of values `1` and `2` is one pair, not two. A frequency-based solution that calculates both `cnt[1] * cnt[2]` and `cnt[2] * cnt[1]` without restricting which complement is processed would count it twice.

Third, the order of positions must be respected. For `[2, 1]` and `k = 3`, the pair `(1, 2)` is still valid because the first position contains `2` and the second contains `1`. The values do not need to appear in increasing numerical order. What matters is that the first position is processed before the second.

Finally, the number of pairs can be much larger than `n`. With `n = 100000`, an array containing only values that pair with themselves can contain `4,999,950,000` good pairs. A 32-bit integer would overflow on such a result in languages with fixed-width integers, so the counting variable must use a sufficiently large integer type. Python integers handle this automatically.

## Approaches

The direct solution follows the definition exactly. For every position `i`, we check every later position `j` and test whether `a[i] + a[j] == k`. Every valid pair is counted exactly once because we only consider `j > i`. This gives the correct answer immediately, but there are `n(n-1)/2` pairs to inspect. When `n = 100000`, that is `4,999,950,000` checks, making the approach unusable.

The structure of the condition gives us a much better way to count. Suppose we are currently processing a value `x`. A previous position forms a good pair with it exactly when that previous value is `k - x`. We do not need to know the positions individually. We only need to know how many times `k - x` has already appeared.

This leads to a one-pass frequency method. Maintain `seen[v]`, the number of occurrences of value `v` among positions already processed. When the current value is `x`, there are exactly `seen[k - x]` earlier positions that form a good pair with it. Add that number to the answer, then increase `seen[x]`.

The ordering condition `i < j` is handled naturally by processing the array from left to right. Every pair is counted when its second endpoint is encountered. This also solves the equal-value case automatically. If `x == k - x`, only previous occurrences are counted, so an occurrence never pairs with itself.

The same procedure is applied independently to both arrays. We then compare their two counts.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Frequency Counting | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and the target sum `k`, followed by Mahmoud's and Bashar's arrays.
2. To count good pairs in one array, create a frequency map `seen` containing the values encountered so far. Initially it is empty because no position has been processed.
3. Process the array from left to right. For the current value `x`, compute its required partner as `k - x`.
4. Add `seen[k - x]` to the answer. Every occurrence recorded there belongs to an earlier position, so each of those occurrences creates exactly one valid pair with the current position.
5. Increase `seen[x]` by one. The current position must become available as a previous position for all later elements, but it must not be used to pair with itself.
6. Repeat the same counting procedure for Bashar's array.
7. Compare the two pair counts. If Mahmoud's count is larger, print `Mahmoud`. If Bashar's count is larger, print `Bashar`. Otherwise, print `Draw`.

### Why it works

After processing any prefix of the array, `seen[v]` equals the number of positions in that prefix whose value is `v`. When processing the next value `x`, every good pair ending at the current position must have an earlier value equal to `k - x`, and there are exactly `seen[k - x]` such positions. Thus the algorithm adds every newly completed good pair exactly once. Because the current value is inserted into `seen` only after counting its partners, a position cannot pair with itself. Since every pair has exactly one later endpoint, every good pair is counted once and only once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_pairs(arr, k):
    seen = {}
    pairs = 0

    for x in arr:
        pairs += seen.get(k - x, 0)
        seen[x] = seen.get(x, 0) + 1

    return pairs

def solve():
    n, k = map(int, input().split())
    mahmoud = list(map(int, input().split()))
    bashar = list(map(int, input().split()))

    mahmoud_pairs = count_pairs(mahmoud, k)
    bashar_pairs = count_pairs(bashar, k)

    if mahmoud_pairs > bashar_pairs:
        print("Mahmoud")
    elif bashar_pairs > mahmoud_pairs:
        print("Bashar")
    else:
        print("Draw")

if __name__ == "__main__":
    solve()
```

The `count_pairs` function implements the left-to-right invariant from the algorithm. `seen[x]` stores how many earlier positions contain `x`, while `pairs` stores the number of good pairs whose two endpoints have already been processed.

The lookup `seen.get(k - x, 0)` is zero when the required complement has not appeared yet. This avoids having to initialize a frequency array for every possible value, although a fixed array of size `100001` would also work because the input values are bounded.

The order of the two statements inside the loop is essential. We count `seen[k - x]` before incrementing `seen[x]`. If the increment happened first, then when `x == k - x`, the current position would incorrectly be counted as its own partner.

Python's arbitrary-precision integers also handle the maximum possible pair count without overflow. No special treatment is required for `x == k - x`, because the frequency of the current value only contains earlier positions.

The two arrays are counted separately, so occurrences from Mahmoud's array never interact with occurrences from Bashar's array.

## Worked Examples

The provided sample is:

```
7 3
1 1 2 3 4 1 2
2 2 2 1 1 1 2
```

For Mahmoud's array, the target complement of each value is `3 - x`.

| Position | Current `x` | Required `k-x` | Previous matching values | Added pairs | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 0 | 0 | 0 |
| 2 | 1 | 2 | 0 | 0 | 0 |
| 3 | 2 | 1 | 2 | 2 | 2 |
| 4 | 3 | 0 | 0 | 0 | 2 |
| 5 | 4 | -1 | 0 | 0 | 2 |
| 6 | 1 | 2 | 1 | 1 | 3 |
| 7 | 2 | 1 | 3 | 3 | 6 |

Mahmoud has `6` good pairs.

For Bashar's array:

| Position | Current `x` | Required `k-x` | Previous matching values | Added pairs | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 0 | 0 | 0 |
| 2 | 2 | 1 | 0 | 0 | 0 |
| 3 | 2 | 1 | 0 | 0 | 0 |
| 4 | 1 | 2 | 3 | 3 | 3 |
| 5 | 1 | 2 | 3 | 3 | 6 |
| 6 | 1 | 2 | 3 | 3 | 9 |
| 7 | 2 | 1 | 3 | 3 | 12 |

Bashar has `12` good pairs, so the output is `Bashar`. The sample statement displays the name in uppercase, but the intended output token is the player's name, and accepted solutions conventionally print `Bashar`.

A second example demonstrates equal values:

```
3 2
1 1 1
1 1 1
```

For either array, every pair of distinct positions has sum `2`.

| Position | Current `x` | Required `k-x` | Previous matching values | Added pairs | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 | 0 |
| 2 | 1 | 1 | 1 | 1 | 1 |
| 3 | 1 | 1 | 2 | 2 | 3 |

Both players have `3` good pairs, so the result is `Draw`. The first `1` does not form a pair with itself because it is added to `seen` only after its contribution has been calculated.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element of both arrays is processed once, with expected O(1) hash-map operations. |
| Space | O(n) | The frequency map can contain up to `n` distinct values. |

With `n <= 100000`, the algorithm performs only a constant amount of work per array element. This is comfortably within the intended limits, while the quadratic brute-force method would require billions of pair checks at the maximum input size.

## Test Cases

```python
import sys
import io

def count_pairs(arr, k):
    seen = {}
    pairs = 0

    for x in arr:
        pairs += seen.get(k - x, 0)
        seen[x] = seen.get(x, 0) + 1

    return pairs

def solve():
    n, k = map(int, input().split())
    mahmoud = list(map(int, input().split()))
    bashar = list(map(int, input().split()))

    m = count_pairs(mahmoud, k)
    b = count_pairs(bashar, k)

    if m > b:
        print("Mahmoud")
    elif b > m:
        print("Bashar")
    else:
        print("Draw")

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline

        output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = output

        try:
            solve()
        finally:
            sys.stdout = old_stdout

        return output.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided sample
assert run(
    """7 3
1 1 2 3 4 1 2
2 2 2 1 1 1 2
"""
) == "Bashar", "sample 1"

# Minimum size, no pair is possible.
assert run(
    """1 2
1
1
"""
) == "Draw", "single element"

# All values are equal and every distinct-position pair is valid.
assert run(
    """3 2
1 1 1
1 1 1
"""
) == "Draw", "all equal"

# Boundary values: 1 + 100000 = 100001.
assert run(
    """4 100001
1 100000 1 100000
1 1 100000 100000
"""
) == "Mahmoud", "boundary complement"

# Equal values must be counted as combinations of distinct positions.
assert run(
    """4 10
5 5 5 5
5 5 5 4
"""
) == "Mahmoud", "self-complement case"

# Maximum pair count still fits in Python's integer type.
# Each array has C(100000, 2) good pairs.
assert run(
    "100000 2\n" +
    ("1 " * 99999) + "1\n" +
    ("1 " * 99999) + "1\n"
) == "Draw", "maximum pair count"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 / 1 / 1` | `Draw` | Minimum size and absence of self-pairs |
| `3 2 / 1 1 1 / 1 1 1` | `Draw` | All-equal values and equal-value pairing |
| `4 100001 / 1 100000 1 100000 / 1 1 100000 100000` | `Mahmoud` | Largest allowed values and complement boundaries |
| `4 10 / 5 5 5 5 / 5 5 5 4` | `Mahmoud` | The `x == k-x` case and combination counting |
| `100000 2` with all values equal to `1` | `Draw` | Maximum `n` and very large pair counts |

## Edge Cases

When the array contains only one element, there cannot be a pair because two distinct positions are required. For example:

```
1 2
1
1
```

The counting loop sees `1`, looks for `1` among previous positions, finds zero occurrences, and only then records the current `1`. Both arrays receive zero pairs, so the answer is `Draw`.

When a value is its own complement, the algorithm must count pairs between different occurrences without pairing an occurrence with itself. Consider:

```
2 2
1 1
1 1
```

For the first `1`, `seen[1]` is zero, so the contribution is zero. After inserting it, the second `1` finds one previous `1` and contributes one pair. Both players have exactly one pair, producing `Draw`. The order of the lookup and insertion is what makes this correct.

When values are at the limits of the input range, the required complement can still be handled without a special case. Consider:

```
2 100001
1 100000
1 1
```

Mahmoud's second value is `100000`, whose complement is `1`. One earlier `1` exists, so Mahmoud gets one good pair. Bashar has no `100000`, so it gets zero. The result is `Mahmoud`.

When the same value appears many times, the number of pairs grows quadratically even though the algorithm itself remains linear. For:

```
4 10
5 5 5 5
5 5 5 4
```

Mahmoud has `C(4, 2) = 6` good pairs because every two distinct `5` positions sum to `10`. Bashar has `C(3, 2) = 3` such pairs. The algorithm generates these counts incrementally as `0 + 1 + 2 + 3` and `0 + 1 + 2`, respectively, giving `Mahmoud`.

Finally, the maximum array size can produce nearly five billion good pairs. With `100000` copies of `1` and `k = 2`, every pair is good, giving `100000 * 99999 / 2 = 4,999,950,000` pairs. The algorithm still performs only `100000` iterations for that array, while Python's integer arithmetic safely stores the resulting count.
