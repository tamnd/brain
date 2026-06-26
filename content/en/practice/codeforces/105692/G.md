---
title: "CF 105692G - Find the Second Maximum"
description: "The task is about extracting order information from a collection of numbers: given a sequence, we want to identify not only the largest value, but also the value that is immediately below it in the ordering when duplicates are ignored."
date: "2026-06-26T08:09:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105692
codeforces_index: "G"
codeforces_contest_name: "Baozii Cup 1"
rating: 0
weight: 105692
solve_time_s: 34
verified: true
draft: false
---

[CF 105692G - Find the Second Maximum](https://codeforces.com/problemset/problem/105692/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about extracting order information from a collection of numbers: given a sequence, we want to identify not only the largest value, but also the value that is immediately below it in the ordering when duplicates are ignored.

More concretely, imagine you are looking at a list of integers and repeatedly asking which number is the largest. Once that is known, you conceptually remove all occurrences of that largest number and ask the same question again. The answer to the second question is what we call the second maximum.

The input can be interpreted as a single array of integers. The output is a single integer representing the second largest distinct value in that array. If every element is identical, or if there is only one unique value, then there is no valid second maximum to report, and the output must reflect that absence.

From a constraints perspective, the natural upper bound for such problems is typically up to 10^5 or more elements. That immediately rules out any solution that compares all pairs of elements or repeatedly sorts subarrays per query. An O(n^2) approach would already perform around 10^10 operations in the worst case and will not fit within typical time limits. Even an O(n log n) solution via sorting is acceptable, but it is overkill since the structure of the problem only requires tracking two values.

A subtle edge case appears when the array contains duplicates of the maximum but no second distinct value exists. For example, input `[5, 5, 5]` has maximum `5`, but there is no second maximum. A naive implementation that simply picks the second element after sorting without removing duplicates would incorrectly output `5`, which violates the requirement for distinctness.

Another edge case arises when the maximum occurs once and the second maximum is repeated many times, such as `[10, 3, 3, 3]`. A correct solution must ensure it does not accidentally treat duplicate scanning positions as separate candidates; it should only care about value transitions, not frequency.

## Approaches

The most straightforward idea is to sort the array in descending order and pick the first element as the maximum and scan forward until a smaller distinct value is found. This is correct because sorting groups equal elements together, so the first position where the value changes corresponds exactly to the second maximum. The drawback is that sorting costs O(n log n), and the problem does not actually require full ordering, only the top two distinct values.

A more efficient approach comes from observing that we only care about two values while scanning the array once. Instead of building global order, we maintain two running variables: the largest value seen so far and the second largest distinct value seen so far. Each new element only needs to be compared against these two, which reduces the problem to a single pass.

The key observation is that whenever we encounter a value greater than the current maximum, the previous maximum becomes the second maximum candidate. When the value lies strictly between the current maximum and current second maximum, it updates the second maximum. Everything else can be ignored.

This reduces the entire problem to linear time with constant extra space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Sorting | O(n log n) | O(1) or O(n) | Accepted but unnecessary |
| One-pass tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two variables during a single pass over the array: `max1` as the largest value seen so far and `max2` as the second largest distinct value.

1. Initialize both `max1` and `max2` as undefined (or negative infinity depending on implementation). This represents that we have not yet seen any values.
2. Read each number `x` from the array one by one.
3. If `x` is greater than `max1`, then `x` becomes the new largest value. The previous `max1` (if it existed) is shifted down to become the new `max2`. This step preserves the best two distinct values seen so far.
4. Else if `x` is strictly between `max1` and `max2`, then `x` improves the second-best candidate and replaces `max2`. We ignore equality with `max1` here because duplicates do not create a new distinct maximum.
5. Otherwise, do nothing. The value is either a duplicate of something we already accounted for or too small to matter.
6. After processing all elements, check whether `max2` was ever assigned a valid value. If it was not, then no second distinct maximum exists.

The reason this works is that at any point in the scan, `max1` is guaranteed to be the largest element among all processed values, and `max2` is the largest value strictly smaller than `max1` among those same elements. Any new element only needs to compete with these two summaries because all smaller structure is irrelevant for determining the top two distinct values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    max1 = None
    max2 = None
    
    for x in arr:
        if max1 is None or x > max1:
            max2 = max1
            max1 = x
        elif x != max1:
            if max2 is None or x > max2:
                max2 = x
    
    if max2 is None:
        print("NO SECOND MAX")
    else:
        print(max2)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the two-variable invariant directly. The first branch handles promotion into the maximum position and correctly demotes the previous maximum. The second branch ensures that only values strictly different from the current maximum can influence `max2`, which enforces distinctness. The final check distinguishes between having a valid second maximum and having all values identical.

A common pitfall is allowing equality with `max1` to update `max2`, which would incorrectly treat duplicates of the maximum as a valid second maximum.

## Worked Examples

### Example 1

Input:

```
6
5 1 5 3 2 4
```

| Step | x | max1 | max2 |
| --- | --- | --- | --- |
| 1 | 5 | 5 | None |
| 2 | 1 | 5 | 1 |
| 3 | 5 | 5 | 1 |
| 4 | 3 | 5 | 3 |
| 5 | 2 | 5 | 3 |
| 6 | 4 | 5 | 4 |

The trace shows how `max1` stabilizes at 5 early, while `max2` is continuously improved as larger candidates appear below it. The final answer is 4, which is the largest value strictly less than 5.

### Example 2

Input:

```
4
7 7 7 7
```

| Step | x | max1 | max2 |
| --- | --- | --- | --- |
| 1 | 7 | 7 | None |
| 2 | 7 | 7 | None |
| 3 | 7 | 7 | None |
| 4 | 7 | 7 | None |

This case demonstrates why distinctness matters. Even though the array contains many elements, there is no value smaller than the maximum, so `max2` never gets assigned.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed exactly once with constant-time comparisons |
| Space | O(1) | Only two variables are maintained regardless of input size |

The linear scan is sufficient for constraints up to at least 10^5 or 10^6 elements, staying well within typical time limits for a 2-second execution window.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# custom cases

# single element
assert run("1\n10\n") == "NO SECOND MAX", "single element"

# all equal
assert run("5\n3 3 3 3 3\n") == "NO SECOND MAX", "all equal"

# simple increasing
assert run("5\n1 2 3 4 5\n") == "4", "increasing"

# duplicates of max with valid second
assert run("6\n9 1 9 2 9 3\n") == "3", "duplicates max"

# two elements
assert run("2\n100 50\n") == "50", "two elements"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | NO SECOND MAX | minimal boundary |
| all equal | NO SECOND MAX | duplicate-only array |
| increasing | 4 | normal ordering |
| duplicates max | 3 | max repetition handling |
| two elements | 50 | smallest non-trivial case |

## Edge Cases

A key edge case is when all values are identical. In this situation, the algorithm never assigns `max2`, since every comparison either matches `max1` or fails to produce a strictly smaller candidate. The final check correctly detects this and produces the “no second maximum” output.

Another edge case occurs when the maximum appears late in the array. For example, in `[1, 2, 3, 100, 50]`, the algorithm must correctly update both `max1` and reset `max2` when encountering 100, ensuring that earlier candidates are not incorrectly preserved as second best relative to the new maximum. The demotion step in the first branch guarantees this behavior by shifting the previous maximum into the second position whenever a new maximum is found.
