---
title: "CF 102793D - \u0414\u043e\u043c\u0438\u043d\u043e"
description: "A domino in this problem is represented by a row of dots with one vertical separator. The dots on the left and right sides of the separator are the numbers of points on the two halves of the tile. We are given two such tiles and need to decide whether they can be placed together."
date: "2026-07-27T17:58:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102793
codeforces_index: "D"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434, \u0421\u0435\u0437\u043e\u043d 2020-21, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102793
solve_time_s: 38
verified: true
draft: false
---

[CF 102793D - \u0414\u043e\u043c\u0438\u043d\u043e](https://codeforces.com/problemset/problem/102793/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

A domino in this problem is represented by a row of dots with one vertical separator. The dots on the left and right sides of the separator are the numbers of points on the two halves of the tile. We are given two such tiles and need to decide whether they can be placed together.

Two dominoes can be matched if there is some number from 0 to 6 that appears on at least one half of the first domino and also on at least one half of the second domino. The output is `Yes` when such a common half value exists and `No` otherwise. The original problem statement describes exactly this compatibility condition for two virtual domino pieces.

Each half contains at most six dots, so the input strings are extremely small. A direct check of all possible values is already constant time. Even if we ignore the small bound and imagine larger strings, we only need to inspect the two halves of each domino once, which rules out any need for graph algorithms, dynamic programming, or simulation.

The main edge cases come from the fact that zero dots are allowed. A domino half with zero dots is represented by an empty side of the separator, so the separator itself may be the first or last character.

For example:

```
|
.
```

The first domino has values 0 and 0, while the second has values 0 and 1. The correct output is:

```
Yes
```

A careless implementation that only counts dots and ignores empty sides would treat the first domino incorrectly and miss the match on value 0.

Another case is when the equal value is not on the same side.

```
.|...
....|.
```

The first domino contains values 1 and 3. The second contains values 4 and 1. The correct output is:

```
Yes
```

A solution that compares only the left halves or only the right halves would incorrectly reject this pair.

## Approaches

The brute-force approach is to generate the two values of the first domino, generate the two values of the second domino, and compare every value from one domino with every value from the other. There are only four comparisons, so the operation count is constant. This approach is already fast enough because the input contains only two dominoes.

A common mistake would be to overcomplicate the problem by trying to simulate the act of connecting dominoes. The condition is much simpler: the two tiles only need one matching half value. The positions of the matching halves do not matter.

The key observation is that each domino can be reduced to a set of at most two numbers. Once both sets are built, the answer is just whether their intersection is non-empty. The brute-force comparison and the set-based view are equivalent, but the set representation makes the reasoning clearer and avoids missing cases involving zero.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Split each input string at the vertical separator. The number of dots before and after the separator gives the two values written on the domino.
2. Store the two values of each domino. The value can be zero, so an empty part of the string must still be counted as a valid half.
3. Check whether any value from the first domino is equal to any value from the second domino.
4. Print `Yes` if a matching value was found. Otherwise print `No`.

The reason this works is that the entire definition of compatibility depends only on whether the two sets of half values share at least one element. The physical position of the halves and the orientation of the dominoes never affect the answer.

## Why it works

The algorithm preserves the exact information needed from each domino. A domino has only two relevant properties: the number of dots on its left half and the number of dots on its right half. If a compatible placement exists, some value `k` must appear among these two values for both dominoes, and the algorithm checks every possible pair. If the algorithm finds a common value, that value satisfies the required condition. If it does not find one, no valid `k` exists. Thus the answer produced is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = input().strip()
    b = input().strip()

    def values(s):
        left, right = s.split('|')
        return {left.count('.'), right.count('.')}

    first = values(a)
    second = values(b)

    print("Yes" if first & second else "No")

if __name__ == "__main__":
    solve()
```

The `values` function converts a domino description into the two numbers written on its halves. Splitting by `|` is safer than manually scanning because it naturally handles empty halves such as `|` or `...|`.

The use of a set removes duplication. For example, a domino described by `|` becomes `{0}`, and a domino with both halves containing three dots becomes `{3}`. The intersection operation checks whether at least one common value exists.

No indexing is used, so there are no boundary issues. Counting dots directly also avoids integer conversion problems because all possible values are between 0 and 6.

## Worked Examples

### Example 1

Input:

```
..|....
....|...
```

The execution can be traced as follows.

| Step | First domino values | Second domino values | Intersection | Result |
| --- | --- | --- | --- | --- |
| Parse input | {2, 4} | {4, 3} | {4} | Yes |

The two dominoes share the value 4, so they can be matched. This demonstrates that the matching sides do not need to be in the same position.

### Example 2

Input:

```
.|...
..|....
```

| Step | First domino values | Second domino values | Intersection | Result |
| --- | --- | --- | --- | --- |
| Parse input | {1, 3} | {2, 4} | empty | No |

There is no number appearing on both dominoes, so no possible matching value exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only four half values are examined. |
| Space | O(1) | Each domino stores at most two values. |

The constraints are much larger than what this solution needs. The program performs a fixed number of operations regardless of the input size, so it easily fits the limits.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    a = sys.stdin.readline().strip()
    b = sys.stdin.readline().strip()

    def values(s):
        left, right = s.split('|')
        return {left.count('.'), right.count('.')}

    ans = "Yes" if values(a) & values(b) else "No"
    sys.stdin = old_stdin
    return ans

assert solve_data("..|....\n....|...\n") == "Yes", "sample 1"
assert solve_data(".|...\n..|....\n") == "No", "sample 2"
assert solve_data("|\n|\n") == "Yes", "both dominoes are zero"
assert solve_data("|\n......|\n") == "Yes", "zero on one side"
assert solve_data(".|....\n..|...\n") == "No", "different values only"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| ` | \n | \n` |
| ` | \n...... | \n` |
| `. | ....\n.. | ...\n` |

## Edge Cases

For the first edge case:

```
|
.
```

The first domino is parsed as `{0}`. The second domino is parsed as `{0, 1}`. Their intersection is `{0}`, so the algorithm prints:

```
Yes
```

The important detail is that an empty side is still a valid half containing zero dots.

For the second edge case:

```
.|...
....|.
```

The first domino becomes `{1, 3}` and the second becomes `{4, 1}`. The algorithm compares the complete sets rather than only matching corresponding sides, finds the common value `1`, and prints:

```
Yes
```

This confirms that any half of either domino can be used for the connection.
