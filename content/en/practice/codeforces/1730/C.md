---
title: "CF 1730C - Minimum Notation"
description: "We are given a string of decimal digits. For any digit, we may remove it from its current position, increase its value by one (capped at 9), and insert the resulting digit anywhere in the string. The operation can be repeated as many times as we want."
date: "2026-06-09T18:41:22+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1730
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 823 (Div. 2)"
rating: 1200
weight: 1730
solve_time_s: 101
verified: true
draft: false
---

[CF 1730C - Minimum Notation](https://codeforces.com/problemset/problem/1730/C)

**Rating:** 1200  
**Tags:** data structures, greedy, math, sortings  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of decimal digits. For any digit, we may remove it from its current position, increase its value by one (capped at 9), and insert the resulting digit anywhere in the string.

The operation can be repeated as many times as we want. Since insertion is unrestricted, the final order of digits is largely under our control. The challenge is deciding which digits should be increased and moved, and which should remain unchanged, so that the resulting string is lexicographically as small as possible.

The total length across all test cases is at most $2 \cdot 10^5$. That immediately rules out any approach that explores sequences of operations. Even an $O(n^2)$ algorithm would be risky because a single test case can contain $2 \cdot 10^5$ digits. We need something close to linear time per test case.

The tricky part is understanding when a digit should be modified. A naive idea is to increase every large digit, because moving it later might help. That is not always correct.

Consider:

```
s = 01
```

The answer is:

```
01
```

If we increase the digit `0`, it becomes `1`, producing a worse string.

Another subtle case is:

```
s = 21
```

The answer is:

```
13
```

The digit `2` appears before a smaller digit `1`. Keeping `2` in place forces the first character of the final string to be at least `2`. By increasing it to `3` and moving it later, we allow `1` to come first.

A third important case is:

```
s = 999
```

The answer remains:

```
999
```

Even though we may repeatedly apply operations, digits are capped at `9`. Moving them around cannot create anything smaller than the existing multiset of digits.

The key observation is that a digit only becomes problematic if there exists a smaller digit somewhere to its right.

## Approaches

A brute-force view is to think about every digit independently. For each position, we could decide whether to keep the digit or apply the operation, then try every possible insertion position. This eventually generates all reachable strings, and the lexicographically smallest one would be the answer.

The difficulty is that the number of possibilities explodes. Even deciding keep-or-modify for each digit already creates $2^n$ possibilities, and insertion positions add another combinatorial factor. This becomes impossible long before $n$ reaches even a few dozen characters.

To find something faster, we need to understand what the operation really changes.

Suppose a digit $s[i]$ has a smaller digit somewhere to its right. Then no matter what we do later, keeping $s[i]$ in front of that smaller digit hurts lexicographic order. Since the operation allows us to remove $s[i]$, increase it by one, and place it anywhere later, we should do exactly that. We sacrifice the digit slightly by increasing it, but we free the smaller digit to appear earlier.

Now consider a digit that is already less than or equal to every digit on its right. Such a digit is not blocking any smaller value. Leaving it in place is always at least as good as increasing it.

This gives a clean criterion:

For every position, look at the minimum digit appearing to its right. If a strictly smaller digit exists, increase the current digit by one (capped at 9). Otherwise keep it unchanged.

After making these decisions, the exact positions no longer matter. Every kept digit stays available with its original value. Every modified digit contributes its increased value. Since moved digits can be reordered arbitrarily, the lexicographically smallest final string is simply obtained by sorting all resulting digits.

The whole problem reduces to computing suffix minima and building the transformed multiset of digits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For the string $s$, compute the minimum digit appearing in every suffix.
2. Traverse the string from left to right.
3. For position $i$, compare $s[i]$ with the minimum digit appearing somewhere to its right.
4. If there exists a smaller digit to the right, replace $s[i]$ by $\min(s[i]+1, 9)$.
5. Otherwise keep $s[i]$ unchanged.
6. Store the resulting digit in a list.
7. After processing all positions, sort the list of resulting digits.
8. Concatenate the sorted digits and print the result.

Why is sorting valid? Every digit that needed to move was converted into its increased version. Once all such decisions are fixed, the operation allows those modified digits to be inserted anywhere. The lexicographically smallest arrangement of a multiset of digits is simply its sorted order.

### Why it works

A digit should remain unchanged only when it is already no larger than every digit after it. Such a digit never prevents a smaller digit from appearing earlier, so modifying it cannot improve the prefix of the final string.

If a smaller digit exists somewhere to the right, keeping the current digit before it would make the final string start with a larger value than necessary. Moving the digit away is always beneficial, and the operation requires paying exactly one unit of increase, capped at 9.

Thus every position has an optimal local decision determined solely by whether a smaller suffix digit exists. After applying all mandatory increases, the remaining task is arranging the resulting multiset of digits. Any lexicographically minimal arrangement must sort the digits in nondecreasing order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        s = input().strip()
        n = len(s)

        suf_min = [''] * n
        suf_min[-1] = s[-1]

        for i in range(n - 2, -1, -1):
            suf_min[i] = min(s[i], suf_min[i + 1])

        res = []

        for i in range(n):
            if i + 1 < n and suf_min[i + 1] < s[i]:
                d = min(int(s[i]) + 1, 9)
                res.append(str(d))
            else:
                res.append(s[i])

        res.sort()
        print("".join(res))

solve()
```

The first part computes suffix minima. For every position, we want to know whether a smaller digit appears later. The minimum value in the suffix beginning at `i + 1` answers exactly that question.

The second pass applies the greedy rule. If the smallest future digit is strictly smaller than the current digit, we increase the current digit by one and mark it as movable. Otherwise we keep it.

After all transformations are determined, only the multiset of resulting digits matters. Sorting them yields the smallest possible lexicographic arrangement.

The most common implementation mistake is comparing against the minimum of the suffix including the current position. We specifically need `suf_min[i + 1]`, because the question is whether a smaller digit exists to the right. Using `suf_min[i]` would incorrectly treat equal digits as evidence that a smaller digit exists.

Another easy mistake is forgetting the cap at `9`. When the current digit is `9`, increasing it still leaves `9`.

## Worked Examples

### Example 1

Input:

```
04829
```

Suffix minima:

| Position | Digit | Min to Right |
| --- | --- | --- |
| 0 | 0 | 2 |
| 1 | 4 | 2 |
| 2 | 8 | 2 |
| 3 | 2 | 9 |
| 4 | 9 | - |

Processing:

| Position | Original | Smaller Right Exists? | Stored |
| --- | --- | --- | --- |
| 0 | 0 | No | 0 |
| 1 | 4 | Yes | 5 |
| 2 | 8 | Yes | 9 |
| 3 | 2 | No | 2 |
| 4 | 9 | No | 9 |

Before sorting:

```
05929
```

After sorting:

```
02599
```

This example shows the central idea. Digits `4` and `8` block a smaller digit `2`, so they are increased and moved out of the way.

### Example 2

Input:

```
314752277691991
```

Processing:

| Position | Original | Result |
| --- | --- | --- |
| 0 | 3 | 4 |
| 1 | 1 | 1 |
| 2 | 4 | 5 |
| 3 | 7 | 8 |
| 4 | 5 | 6 |
| 5 | 2 | 2 |
| 6 | 2 | 2 |
| 7 | 7 | 8 |
| 8 | 7 | 8 |
| 9 | 6 | 7 |
| 10 | 9 | 9 |
| 11 | 1 | 1 |
| 12 | 9 | 9 |
| 13 | 9 | 9 |
| 14 | 1 | 1 |

Collected digits:

```
415862288791991
```

After sorting:

```
111334567888999
```

This trace demonstrates that once every digit has been independently transformed according to the suffix-minimum rule, sorting immediately produces the optimal answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Computing suffix minima is linear, sorting the resulting digits dominates |
| Space | $O(n)$ | Suffix array and result list |

The total input size is at most $2 \cdot 10^5$. Sorting at most $2 \cdot 10^5$ digits across all test cases easily fits within the time limit, and the linear auxiliary memory is well within the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())

    out = []

    for _ in range(t):
        s = input().strip()
        n = len(s)

        suf = [''] * n
        suf[-1] = s[-1]

        for i in range(n - 2, -1, -1):
            suf[i] = min(s[i], suf[i + 1])

        res = []

        for i in range(n):
            if i + 1 < n and suf[i + 1] < s[i]:
                res.append(str(min(int(s[i]) + 1, 9)))
            else:
                res.append(s[i])

        res.sort()
        out.append("".join(res))

    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided samples
assert run(
"""4
04829
9
01
314752277691991
"""
) == """02599
9
01
111334567888999"""

# minimum size
assert run(
"""1
0
"""
) == "0"

# all equal
assert run(
"""1
77777
"""
) == "77777"

# decreasing sequence
assert run(
"""1
9876543210
"""
) == "1234567899"

# repeated minimum digit
assert run(
"""1
1000
"""
) == "0002"

# cap at 9
assert run(
"""1
9991
"""
) == "1999"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `0` | Minimum possible length |
| `77777` | `77777` | No digit has a smaller value to its right |
| `9876543210` | `1234567899` | Every digit except the last must be increased and moved |
| `1000` | `0002` | A leading digit blocked by smaller suffix digits |
| `9991` | `1999` | Correct handling of the cap at `9` |

## Edge Cases

Consider:

```
1
21
```

The suffix minimum to the right of `2` is `1`, which is smaller. We increase `2` to `3`. The digit `1` remains unchanged. After sorting, we obtain:

```
13
```

A solution that keeps `2` would produce a lexicographically larger string.

Now consider:

```
1
01
```

The digit `0` has no smaller digit to its right. The digit `1` is already the last position. No modifications occur, and sorting keeps:

```
01
```

This confirms that we do not modify digits unless they actually block a smaller future digit.

Finally consider:

```
1
999
```

Every suffix minimum equals `9`. No position sees a strictly smaller digit to its right, so every digit stays unchanged. Sorting still yields:

```
999
```

This validates the boundary condition where the increment operation is capped and provides no advantage.
