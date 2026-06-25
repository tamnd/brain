---
title: "CF 106182D - Digit Division"
description: "The task is to split a string of digits into consecutive pieces so that the pieces, when interpreted as integers, form a strictly increasing sequence. We need to create at least two pieces, and the order of digits cannot change. If a valid split exists, we output any one of them."
date: "2026-06-25T10:51:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106182
codeforces_index: "D"
codeforces_contest_name: "Petrozavodsk Summer Camp 2025. Day 6. Xeppelin Contest The 4rd Universal Cup. Stage 2: Grand Prix of Paris)"
rating: 0
weight: 106182
solve_time_s: 32
verified: true
draft: false
---

[CF 106182D - Digit Division](https://codeforces.com/problemset/problem/106182/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 32s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to split a string of digits into consecutive pieces so that the pieces, when interpreted as integers, form a strictly increasing sequence. We need to create at least two pieces, and the order of digits cannot change. If a valid split exists, we output any one of them.

Each query gives a length and a digit string. The length can be as large as 300 and there can be up to 300 queries. These limits are small enough that a linear scan per query is easily acceptable. An algorithm with quadratic or cubic string operations would still be unnecessary, because the structure of the problem allows a constant time decision after reading the string.

The tricky part is not the length of the string, but understanding when a split can fail. A careless solution may try arbitrary split positions or compare the whole string numerically, which is unnecessary and can also create mistakes with long strings.

For example, consider:

```
2
99
```

The only possible split is `9 | 9`. The two numbers are equal, so the answer is:

```
NO
```

A solution that only checks whether the string contains multiple digits might incorrectly accept it.

Another boundary case is:

```
2
12
```

The only split is `1 | 2`, and because `1 < 2`, the correct output is any valid representation such as:

```
YES
2
1 2
```

The case where the length is greater than two behaves differently. For example:

```
3
654
```

Splitting as `6 | 54` works because every two digit number made from these digits is at least 11, which is always larger than a single digit number.

## Approaches

A direct approach is to try every possible place to insert separators. For each split, we would build the resulting numbers and check whether every number is smaller than the next one. This is correct because it examines every possible division, but there are up to `n - 1` separator positions and many resulting pieces to compare. With larger constraints, repeatedly converting substrings into numbers can make the implementation unnecessarily expensive.

The key observation is that the first split is enough. If the string has more than two digits, divide it into the first digit and the remaining suffix. The first part is a single digit, so its value is at most 9. The second part has at least two digits, and every digit is from 1 to 9, so its value is at least 11. The second part is guaranteed to be larger.

The only situation where this construction does not automatically work is when the string length is exactly two. In that case, the only possible division is the two individual digits, so we only need to compare them.

The brute force works because it searches all valid cuts. The observation above removes the search entirely by proving that almost every string has one obvious valid cut.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Unnecessary |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the digit string for the current query. The length of the string determines whether the automatic split can be used.
2. If the length is exactly two, compare the first digit and the second digit. If the first digit is smaller, the split into two single digit parts is valid. Otherwise, no valid split exists.
3. If the length is greater than two, split after the first digit. The two resulting parts are the first character and the remaining suffix. This always works because the suffix has at least two digits and therefore represents a number larger than any single digit.
4. Output the constructed division.

Why it works: the algorithm maintains the property that every produced adjacent pair of parts is increasing. For the length two case, there are no alternative divisions, so the direct comparison decides the answer. For longer strings, the first part has maximum value 9 while the second part has minimum value 11, so the chosen split is always valid.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        if n == 2:
            if s[0] < s[1]:
                ans.append("YES")
                ans.append("2")
                ans.append(s[0] + " " + s[1])
            else:
                ans.append("NO")
        else:
            ans.append("YES")
            ans.append("2")
            ans.append(s[0] + " " + s[1:])

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The code processes each query independently. The special case `n == 2` is handled first because the general construction requires the second part to contain at least two digits.

For longer strings, the expression `s[1:]` creates the suffix after the first digit. No numeric conversion is needed, which avoids problems with large values and keeps the solution linear.

The comparison in the two digit case uses characters instead of integers. Since both characters represent single digits, lexicographical comparison gives exactly the same result as numerical comparison.

## Worked Examples

### Sample 1

Input:

```
4
6
654321
4
1337
2
33
4
2122
```

For the first query:

| Step | String | Condition | Action |
| --- | --- | --- | --- |
| 1 | 654321 | Length is greater than 2 | Split after first digit |
| 2 | 6, 54321 | 54321 > 6 | Accept split |

For the second query:

| Step | String | Condition | Action |
| --- | --- | --- | --- |
| 1 | 1337 | Length is greater than 2 | Split after first digit |
| 2 | 1, 337 | 337 > 1 | Accept split |

For the third query:

| Step | String | Condition | Action |
| --- | --- | --- | --- |
| 1 | 33 | Length is 2 | Compare digits |
| 2 | 3, 3 | 3 is not smaller than 3 | Reject |

For the fourth query:

| Step | String | Condition | Action |
| --- | --- | --- | --- |
| 1 | 2122 | Length is greater than 2 | Split after first digit |
| 2 | 2, 122 | 122 > 2 | Accept split |

The trace shows why only the two digit case needs real checking. Longer strings are resolved immediately by the size difference between one digit and multiple digits.

### Custom Example

Input:

```
3
2
12
5
98765
2
98
```

| Step | String | Condition | Action |
| --- | --- | --- | --- |
| 1 | 12 | Length is 2 | Compare 1 and 2 |
| 2 | 1, 2 | Increasing | Accept |
| 3 | 98765 | Length is greater than 2 | Split as 9 and 8765 |
| 4 | 98 | Length is 2 | Compare 9 and 8 |
| 5 | 9, 8 | Not increasing | Reject |

This example exercises the smallest valid split, the automatic long string split, and the failing two digit case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each digit string is read once and only a constant amount of work is done after reading it. |
| Space | O(1) | Apart from the output storage, the algorithm uses only a few variables. |

The largest string length is small, but the solution also scales naturally because it never tries multiple split positions or performs large numeric operations.

## Test Cases

```python
import sys
import io

def solve_data(data: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(data)
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        if n == 2:
            if s[0] < s[1]:
                ans.append("YES")
                ans.append("2")
                ans.append(s[0] + " " + s[1])
            else:
                ans.append("NO")
        else:
            ans.append("YES")
            ans.append("2")
            ans.append(s[0] + " " + s[1:])

    sys.stdin = old_stdin
    return "\n".join(ans)

assert solve_data("""4
6
654321
4
1337
2
33
4
2122
""") == """YES
2
6 54321
YES
2
1 337
NO
YES
2
2 122""", "sample"

assert solve_data("""1
2
12
""") == """YES
2
1 2""", "smallest valid case"

assert solve_data("""1
2
99
""") == "NO", "equal two digits"

assert solve_data("""1
300
""" + "9" * 300 + "\n") == """YES
2
9 """ + "9" * 299, "large length case"

assert solve_data("""1
3
111
""") == """YES
2
1 11""", "all equal digits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 12` | `YES` | Minimum length with a valid split |
| `2 / 99` | `NO` | Equal digits cannot be increasing |
| Length `300` string | `YES` | Large input handling |
| `111` | `YES` | All digits equal with length greater than two |

## Edge Cases

For a two digit string with equal digits, such as:

```
2
55
```

the algorithm enters the special case and compares `5` with `5`. Since the first digit is not smaller, it prints `NO`. This avoids the common mistake of assuming every string with at least two digits can be divided.

For a two digit string where the first digit is smaller, such as:

```
2
34
```

the algorithm compares `3` and `4`, finds the required increasing order, and outputs the two individual digits.

For a longer string containing repeated large digits, such as:

```
5
99999
```

the algorithm does not compare the whole suffix numerically. It simply uses `9 | 9999`. The suffix has four digits, so its value is greater than 9. The same reasoning works for every length greater than two.
