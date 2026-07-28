---
title: "CF 102767D - Singhal and Permutations"
description: "We have a multiset of numbers and we want to count how many different arrays can be formed by rearranging those numbers such that the array has a single peak. The peak is the maximum value in the array."
date: "2026-07-28T23:30:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102767
codeforces_index: "D"
codeforces_contest_name: "Codedigger Training Contest -Number Theory"
rating: 0
weight: 102767
solve_time_s: 78
verified: true
draft: false
---

[CF 102767D - Singhal and Permutations](https://codeforces.com/problemset/problem/102767/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a multiset of numbers and we want to count how many different arrays can be formed by rearranging those numbers such that the array has a single peak. The peak is the maximum value in the array. Everything before this maximum must be strictly increasing, and everything after it must be strictly decreasing.

For example, if the multiset is `{1, 2, 3, 1}`, the maximum value is `3`, so the only possible shape is some increasing sequence ending at `3`, followed by a decreasing sequence. The array `(1,2,3,1)` works because the left side grows strictly and the right side falls strictly.

The input gives the size of the array and the values that must be rearranged. The output is the number of distinct arrays satisfying the peak condition.

The key constraint is that the number of elements can be large enough that trying every permutation is impossible. With `n` elements, brute force would examine up to `n!` arrangements, which becomes unusable even for very small values of `n`. The solution needs to inspect the frequencies of values and count valid constructions directly.

The tricky part is handling duplicate values. A value smaller than the maximum can appear on the left side, the right side, or both, but each side must be strictly monotonic, so no side can contain the same value twice. The maximum value itself is special because it must be the only peak.

Consider the multiset:

```
3
1 2 2
```

The correct output is:

```
0
```

A careless approach might put one `2` as the peak and the other `2` on one side. However, either `(1,2,2)` or `(2,2,1)` contains equal adjacent maximum values, so there is no unique peak.

Another edge case is a value appearing three times below the maximum:

```
5
1 2 2 2 3
```

The correct output is:

```
0
```

The value `2` would need to be distributed between the two sides of the peak. Since each side can contain it at most once, three copies cannot be placed.

A final boundary case is when all non-maximum values are unique:

```
4
1 2 3 4
```

The correct output is:

```
8
```

Each of `1`, `2`, and `3` can independently be assigned to the increasing side or the decreasing side. Every assignment produces a different valid array.

## Approaches

The direct approach is to generate every permutation of the input multiset and check whether it is awesome. For a candidate permutation, we can find the maximum position and verify that values increase before it and decrease after it. This correctly counts all answers because every possible arrangement is tested.

The problem is the number of permutations. With `n` distinct values there are `n!` possible arrangements. Even `10!` is already millions of possibilities, and the factorial growth quickly makes this impossible.

The structure of an awesome array gives a much smaller way to think about the problem. Once the maximum value is fixed in the middle, the remaining values only need to be assigned to one of two sides. The left side will automatically be sorted in increasing order, and the right side will automatically be sorted in decreasing order.

For a value smaller than the maximum, the strict ordering rule means that each side can contain this value at most once. If a value appears once, we may choose either side. If it appears twice, one copy must go to each side. If it appears more than twice, there is no valid placement.

The maximum value cannot appear more than once. A second copy would have to be placed on one of the two sides, but it would create another maximum value and violate the single peak structure.

This reduces the problem from permutation generation to frequency counting. We only need to count how many values occur exactly once below the maximum, because each of those contributes two independent choices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of every value in the array.

The frequency information is enough because the final ordering of each side is forced. We only need to know how many ways each value can be distributed.
2. Find the maximum value and check its frequency.

If the maximum appears more than once, the answer is zero because an awesome array requires a single peak.
3. Examine every value smaller than the maximum.

If a value appears more than two times, the answer is zero because two monotonic sides cannot hold three copies of the same value.

If a value appears exactly twice, it must appear once on each side. This creates no choice.

If a value appears exactly once, it can be placed either before the maximum or after the maximum. Multiply the answer by two for this value.
4. Output the accumulated number of choices.

The number of choices is always a power of two because every flexible value contributes one independent binary decision.

Why it works:

The maximum element fixes the center of every valid array. After choosing which smaller values belong to the left and right sides, the ordering is forced because the left side must be increasing and the right side must be decreasing. The frequency rules describe exactly when a value can be placed on those sides. Every valid awesome array corresponds to one unique assignment of values to sides, and every valid assignment creates one awesome array, so the counting is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1

        mx = max(a)

        if freq[mx] > 1:
            ans.append("0")
            continue

        ways = 1
        possible = True

        for x, c in freq.items():
            if x == mx:
                continue
            if c > 2:
                possible = False
                break
            if c == 1:
                ways *= 2

        ans.append(str(ways if possible else 0))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The dictionary `freq` stores how many copies of each value exist. This avoids depending on the order of the original array because only the multiset matters.

The maximum value is checked first. This handles the special peak requirement before processing smaller values.

For smaller values, a frequency of two means the value must appear once on both sides of the maximum, while a frequency of one gives two possible placements. The multiplication happens only for these single occurrences.

Python integers do not overflow, so the repeated doubling is safe. The iteration over the frequency map also keeps the solution linear in the number of input values.

## Worked Examples

Example 1:

Input:

```
4
1 2 3 4
```

| Step | Value checked | Frequency | Current ways |
| --- | --- | --- | --- |
| Initial | Maximum = 4 | 1 | 1 |
| Check 1 | 1 | 1 | 2 |
| Check 2 | 2 | 1 | 4 |
| Check 3 | 3 | 1 | 8 |

The three smaller values are all unique, so each can independently move to either side of the maximum. The answer is:

```
8
```

Example 2:

Input:

```
5
1 2 2 3 3
```

| Step | Value checked | Frequency | Current ways |
| --- | --- | --- | --- |
| Initial | Maximum = 3 | 2 | 0 |

The maximum appears twice, so no valid awesome array exists. The answer is:

```
0
```

This trace shows why the maximum check must happen before counting choices. A duplicated maximum cannot be repaired by distributing it across the two sides.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each number is inserted into the frequency map once and each distinct value is inspected once. |
| Space | O(n) | The frequency map can contain every distinct input value. |

The total number of elements across test cases is small enough for a linear solution. The algorithm avoids permutation generation entirely, which is the only practical way to handle large inputs.

## Test Cases

```python
import sys
import io

def solve(inp):
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1

        mx = max(a)

        if freq[mx] > 1:
            out.append("0")
            continue

        ways = 1
        ok = True

        for x, c in freq.items():
            if x == mx:
                continue
            if c > 2:
                ok = False
                break
            if c == 1:
                ways *= 2

        out.append(str(ways if ok else 0))

    return "\n".join(out)

assert solve("""5
4
1 2 3 4
3
1 2 2
5
1 2 2 2 3
5
1 2 2 3 3
3
5 4 3
""") == """8
0
0
0
4"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3 4` | `8` | All values are unique and every smaller value creates a choice. |
| `1 2 2` | `0` | Duplicate maximum-side conflict. |
| `1 2 2 2 3` | `0` | More than two copies of a non-maximum value. |
| `1 2 2 3 3` | `0` | Repeated maximum handling. |
| `5 4 3` | `4` | Maximum at an end and all unique smaller values. |

## Edge Cases

For the input:

```
3
1 2 2
```

the frequency of the maximum value `2` is two. The algorithm immediately returns zero. This matches the requirement that an awesome array has one peak, not multiple occurrences of the maximum.

For the input:

```
5
1 2 2 2 3
```

the maximum is unique, but the value `2` appears three times. The algorithm detects that two sides are not enough to separate all copies while keeping both sides strictly ordered, so it returns zero.

For the input:

```
4
1 2 3 4
```

the maximum is unique and every smaller value appears once. The algorithm doubles the count three times, producing `2 * 2 * 2 = 8`. Each result corresponds to choosing the side of the peak for each smaller value, and the ordering is then determined automatically.
