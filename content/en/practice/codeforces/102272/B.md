---
title: "CF 102272B - \u0110\u1ebfm Th\u1ecf"
description: "We have an array typ[1..N], where each position represents one rabbit and the value at that position identifies its species. For any contiguous interval [l, r], the score is the number of different species appearing inside that interval."
date: "2026-08-19T05:27:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102272
codeforces_index: "B"
codeforces_contest_name: "HCW 19 Individual Day 1"
rating: 0
weight: 102272
solve_time_s: 969
verified: false
draft: false
---

[CF 102272B - \u0110\u1ebfm Th\u1ecf](https://codeforces.com/problemset/problem/102272/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 16m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array `typ[1..N]`, where each position represents one rabbit and the value at that position identifies its species. For any contiguous interval `[l, r]`, the score is the number of different species appearing inside that interval. We need the sum of this score over every possible nonempty contiguous interval.

The input contains up to 10 test cases, and the total number of array elements across all test cases is at most `2 * 10^6`. A single test case can contain `10^6` elements, so an `O(N^2)` method is far beyond the available time. Even for one test case, there are about `N^2 / 2` intervals, which is roughly `5 * 10^11` when `N = 10^6`. An algorithm must be essentially linear, or at most close to linear, in `N`. The species identifiers can be as large as `10^9`, so using an array indexed directly by the identifier is not appropriate in general. A hash map is enough because we only need to remember the latest position of each species.

The answer can also become much larger than a 32-bit integer. If every rabbit has a different species, the answer is the sum of the lengths of all subarrays, which is `N(N+1)(N+2)/6`. For `N = 10^6`, this is `166667166667000000`, so the implementation must use an integer type capable of holding values of this magnitude. Python integers handle this automatically.

There are several boundary cases that are easy to mishandle. Consider the smallest input

```
1
1
7
```

There is only one interval, `[1,1]`, and it contains one species, so the answer is `1`. A solution that initializes its previous occurrence to `1` instead of `0`, or that forgets to include the current position, can incorrectly produce zero.

Repeated species also require careful treatment. For

```
1
3
1 1 1
```

every one of the six intervals contains exactly one species, so the answer is `6`. When the third `1` is processed, its previous occurrence is position `2`, not position `1`. Using the first occurrence instead of the most recent occurrence would count too many intervals.

A second boundary case is when every value is different:

```
1
3
1 2 3
```

The ten points contributed by all intervals are `1 + 2 + 2 + 3 = 10`. Every occurrence introduces its species for a whole range of possible left endpoints, so treating each position as contributing only once misses many intervals.

Finally, a repeated species does not stop contributing forever. For

```
1
4
1 2 1 2
```

the correct answer is `15`. A careless method that counts only globally new species would count species `1` and `2` once each and lose the contribution of those species to intervals beginning after their previous occurrences.

## Approaches

The direct approach is to enumerate every interval `[l, r]`, maintain a set of species while extending `r`, and add the set size to the answer. This is correct because the set contains exactly the distinct species in the current interval. However, there are `N(N+1)/2` intervals, and even if each extension is made efficient, there are still `Theta(N^2)` operations. At `N = 10^6`, that means about `5 * 10^11` intervals, which is completely infeasible.

A more useful way to think about the problem is to reverse the question. Instead of asking for the number of species inside each interval, ask how many intervals contain a particular occurrence as the representative occurrence of its species.

Suppose position `i` contains species `x`. Let `prev[i]` be the previous position containing `x`, or `0` if this is the first occurrence. Let `next[i]` be the next position containing `x`, or `N+1` if this is the last occurrence.

Position `i` represents species `x` in exactly those intervals `[l,r]` satisfying

`prev[i] < l <= i <= r < next[i]`.

The left endpoint has `i - prev[i]` choices, and the right endpoint has `next[i] - i` choices. Thus this occurrence contributes

`(i - prev[i]) * (next[i] - i)`

to the final answer.

There is an even simpler implementation that does not need the next occurrence array. Process the array from left to right. When position `i` with species `x` is reached, let `p` be the previous occurrence of `x`.

For every interval ending at `i`, the new occurrence at `i` increases the distinct count exactly when the left endpoint is greater than `p`. There are `i-p` such left endpoints. Therefore the total distinct-count sum among all intervals ending at `i` increases by `i-p`.

We can maintain `cur`, the total number of distinct species across all intervals ending at the current position. Then

`cur += i - p`

and we add `cur` to the global answer. The crucial point is that intervals whose left endpoint is at most `p` already contained species `x` before position `i`, while intervals beginning after `p` did not.

The two viewpoints are equivalent. The first assigns every species occurrence a rectangle of valid left and right endpoints. The second sweeps the right endpoint and maintains the total contribution of all intervals ending there. The sweep version requires only the latest occurrence of each species and is particularly compact.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(N^2)` | `O(N)` | Too slow |
| Optimal | `O(N)` | `O(N)` | Accepted |

## Algorithm Walkthrough

1. Initialize an empty map `last` that stores the latest position at which each species appeared. Use `0` as the previous position for a species that has not appeared before. This gives every first occurrence the correct boundary without a special case.
2. Initialize `cur = 0` and `answer = 0`. Here `cur` represents the sum of the number of distinct species over all intervals whose right endpoint is the current position. `answer` accumulates this value over every right endpoint.
3. Scan the array from left to right. At position `i`, read the previous occurrence `p = last.get(typ[i], 0)`.
4. Increase `cur` by `i - p`. Consider all intervals ending at `i`. Their left endpoints range from `1` through `i`. If the left endpoint is at most `p`, the same species already appeared inside the interval before reaching `i`, so this occurrence does not add a new species. If the left endpoint is in `p+1` through `i`, this is the first occurrence of the species inside the interval, so it adds exactly one distinct species. There are `i-p` such left endpoints.
5. Add `cur` to `answer`. Every interval has exactly one right endpoint, so after processing position `i`, all intervals ending at `i` have now contributed exactly once.
6. Set `last[typ[i]] = i`. The current position must become the previous occurrence for all future positions containing the same species. Using an older occurrence here would make the range of affected left endpoints too large.
7. After the scan finishes, print `answer`. Every nonempty interval has been considered exactly once, grouped according to its right endpoint.

### Why it works

The invariant after processing position `i` is that `cur` equals the sum of the number of distinct species over every interval ending at `i`.

When species `x = typ[i]` occurs at position `i`, let its previous occurrence be `p`. For an interval `[l,i]`, the occurrence at `i` introduces a new species exactly when `l > p`. There are precisely `i-p` possible values of `l`, so adding `i-p` to the previous total gives the correct total for all intervals ending at `i`. Updating `last[x]` to `i` preserves the same property for the next occurrence. Since the global answer adds the correct total for every possible right endpoint, every interval contributes exactly its number of distinct species once.

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

        last = {}
        cur = 0
        answer = 0

        for i, x in enumerate(a, 1):
            p = last.get(x, 0)

            cur += i - p
            answer += cur

            last[x] = i

        out.append(str(answer))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The map `last` corresponds directly to the previous-occurrence value used in the walkthrough. For the first occurrence of a species, `last.get(x, 0)` returns zero, so position `i` contributes `i` new species occurrences among intervals ending there.

The variable `cur` is not the number of distinct species in one particular interval. It is the sum of distinct-species counts over all intervals ending at the current position. This distinction is essential. For `1 2 2`, when processing the second `2`, `cur` becomes `3`, because the intervals ending there are `[2,2]`, containing one species, and `[1,2]`, containing two species.

The order of operations also matters. We read the old position from `last` before updating it. If the map were updated first, every repeated occurrence would incorrectly have itself as its previous occurrence, making its contribution zero.

Python's arbitrary-precision integers are useful here because the answer can reach roughly `1.67 * 10^17` for `N = 10^6`. In C++, a 64-bit integer would be required.

The input size can reach two million integers across all test cases, so the implementation stores one array and one dictionary per test case. `sys.stdin.readline` and a single buffered output write keep the Python I/O overhead small.

## Worked Examples

### Sample 1, first test case

For the array `1 2 3`, every species is new when encountered. The value `i-p` is consequently `1`, `2`, and `3`.

| Position `i` | Species | Previous `p` | `i-p` | `cur` | `answer` |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 | 1 |
| 2 | 2 | 0 | 2 | 3 | 4 |
| 3 | 3 | 0 | 3 | 6 | 10 |

After position `1`, the only interval is `[1,1]`, with one species. After position `2`, the two intervals ending there have scores `1` and `2`, giving `cur = 3`. After position `3`, the three intervals ending there have scores `1`, `2`, and `3`, giving `cur = 6`. The final answer is `1 + 3 + 6 = 10`.

### Sample 1, second test case

For `1 2 2 3`, the third position repeats species `2`. Its previous occurrence is position `2`, so only the interval `[3,3]` gains a new species from the occurrence at position `3`.

| Position `i` | Species | Previous `p` | `i-p` | `cur` | `answer` |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 | 1 |
| 2 | 2 | 0 | 2 | 3 | 4 |
| 3 | 2 | 2 | 1 | 4 | 8 |
| 4 | 3 | 0 | 4 | 8 | 16 |

At position `3`, the intervals ending there are `[3,3]`, `[2,3]`, and `[1,3]`, whose scores are `1`, `1`, and `2`. Their total is `4`, matching `cur`. At position `4`, species `3` is new globally, so all four intervals ending there gain one distinct species, increasing `cur` from `4` to `8`. The final result is `16`.

### Repeated species example

Consider `1 2 1 2`.

| Position `i` | Species | Previous `p` | `i-p` | `cur` | `answer` |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 | 1 | 1 |
| 2 | 2 | 0 | 2 | 3 | 4 |
| 3 | 1 | 1 | 2 | 5 | 9 |
| 4 | 2 | 2 | 2 | 7 | 16 |

At position `3`, species `1` last appeared at position `1`. The left endpoint can be `2` or `3`, so there are two intervals ending at `3` where this occurrence introduces species `1`. This gives the increment `3-1=2`. The final answer is `16`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N)` | Each array element is processed once and each hash-map operation is expected `O(1)`. |
| Space | `O(N)` | The array and the map can each contain up to `N` elements. |

Across all test cases, the total `N` is at most `2 * 10^6`, so the total expected running time is linear in the complete input size. The memory usage is also linear in the largest individual test case and remains within the 512 MB limit.

## Test Cases

```python
# The solution is copied into solve() so the tests can replace stdin.

import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        last = {}
        cur = 0
        answer = 0

        for i, x in enumerate(a, 1):
            p = last.get(x, 0)
            cur += i - p
            answer += cur
            last[x] = i

        out.append(str(answer))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run(
    """2
3
1 2 3
4
1 2 2 3
"""
) == "10\n16", "provided sample"

# Minimum size
assert run(
    """1
1
7
"""
) == "1", "single rabbit"

# All values equal
assert run(
    """1
4
5 5 5 5
"""
) == "10", "all intervals contain exactly one species"

# Alternating repeated values
assert run(
    """1
4
1 2 1 2
"""
) == "16", "repeated species with gaps"

# Every value is different
assert run(
    """1
4
1 2 3 4
"""
) == "20", "all species are different"

# Maximum-size test, all values equal.
# The answer is the number of nonempty subarrays.
n = 1_000_000
inp = "1\n{}\n{}\n".format(n, "1 " * (n - 1) + "1")
expected = n * (n + 1) // 2
assert run(inp) == str(expected), "maximum N with all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 7` | `1` | Minimum size and first-occurrence boundary |
| `1 / 4 / 5 5 5 5` | `10` | Repeated values and latest-occurrence handling |
| `1 / 4 / 1 2 1 2` | `16` | Repetitions separated by other species |
| `1 / 4 / 1 2 3 4` | `20` | Every occurrence is globally new |
| `N = 10^6`, all values `1` | `500000500000` | Maximum input size and large answer |

## Edge Cases

For a single rabbit, the input is

```
1
1
7
```

At position `1`, there is no previous occurrence, so `p = 0`. The increment is `1 - 0 = 1`, giving `cur = 1` and `answer = 1`. There is exactly one possible interval, so the result is correct.

For all equal species,

```
1
3
1 1 1
```

the execution is

| Position | Previous occurrence | Increment | `cur` | `answer` |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 1 |
| 2 | 1 | 1 | 2 | 3 |
| 3 | 2 | 1 | 3 | 6 |

Every interval contains exactly one species, and there are six intervals. The key boundary is that each repeated occurrence uses the immediately preceding position as `p`, so it adds exactly one to the total for intervals beginning at that occurrence.

For an array where every species is different,

```
1
3
1 2 3
```

all previous positions are zero. The increments are `1`, `2`, and `3`, producing `cur` values `1`, `3`, and `6`. The global answer is `10`. This verifies that the algorithm counts the contribution across all possible left endpoints instead of treating an occurrence as contributing to only one interval.

For repeated species separated by other values,

```
1
4
1 2 1 2
```

the third position has previous occurrence `1`, so its increment is `3-1=2`. The fourth position has previous occurrence `2`, so its increment is `4-2=2`. The resulting `cur` values are `1`, `3`, `5`, and `7`, and the answer is `16`. This catches the common mistake of storing the first occurrence instead of the latest one.

The large-value case also matters. For `N = 10^6` with all values distinct, the answer is

`N(N+1)(N+2)/6 = 166667166667000000`.

A 32-bit integer would overflow badly, while Python's integer representation stores the exact result. The algorithm itself does not need any special handling for this case because the same `i-p` formula applies with `p = 0` at every position.
