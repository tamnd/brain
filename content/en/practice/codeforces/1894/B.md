---
title: "CF 1894B - Two Out of Three"
description: "We are given an array a and must assign every position a label from {1, 2, 3}. The labels form another array b. The three conditions are based on equal values in a."
date: "2026-06-08T21:54:19+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1894
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 908 (Div. 2)"
rating: 1000
weight: 1894
solve_time_s: 390
verified: false
draft: false
---

[CF 1894B - Two Out of Three](https://codeforces.com/problemset/problem/1894/B)

**Rating:** 1000  
**Tags:** constructive algorithms  
**Solve time:** 6m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array `a` and must assign every position a label from `{1, 2, 3}`. The labels form another array `b`.

The three conditions are based on equal values in `a`. A condition becomes true if there exists at least one pair of positions containing the same value in `a`, while their labels in `b` are a specific pair among `(1,2)`, `(1,3)`, or `(2,3)`.

Our goal is to construct `b` so that exactly two of those three conditions are true. If no such assignment exists, we print `-1`.

The array length is at most 100, and values are also at most 100. The small constraints mean almost any reasonable frequency-based solution is fast enough. Even an `O(n²)` approach would pass comfortably, since the total work per test case is tiny. The challenge is not efficiency, but understanding the structure of the required labeling.

The main difficulty is that the conditions talk about the existence of equal values split across particular label pairs. A naive construction can easily make all three conditions true instead of exactly two.

Consider the array:

```
1 1 2 2
```

A valid answer is:

```
2 1 3 1
```

The value `1` creates a `(1,2)` pair, while the value `2` creates a `(1,3)` pair. No equal value is split between labels `2` and `3`, so exactly two conditions hold.

A common mistake is assigning labels independently for every repeated value. For example:

```
1 1 2 2
b = 1 2 1 3
```

Now `(1,2)` is satisfied by value `1`, `(1,3)` is satisfied by value `2`, and `(2,3)` may accidentally appear if another duplicated value is split differently. The construction must be controlled globally.

Another important edge case is when there is only one duplicated value:

```
1 2 1
```

Any split of that duplicated value can satisfy at most one condition. We need two conditions, so the correct output is:

```
-1
```

A final edge case is when all values are distinct:

```
1 2 3 4
```

No condition can ever become true because every condition requires equal values. The answer is again `-1`.

## Approaches

A brute-force viewpoint is to try every possible assignment of labels `1`, `2`, and `3` to all positions and check how many conditions become true. Since each position has three choices, there are `3ⁿ` assignments. Even for `n = 100`, this is completely infeasible.

The key observation is that a condition only depends on repeated values. Distinct values contribute nothing because the condition requires two equal elements.

Suppose a value appears at least twice. Then we can use two occurrences of that value to create exactly one desired condition. For example, assigning labels `1` and `2` to two occurrences creates condition `(1,2)`.

To make exactly two conditions true, we can intentionally create:

```
(1,2)
(1,3)
```

and avoid creating:

```
(2,3)
```

How can we do that?

Take one repeated value and split two of its occurrences between labels `1` and `2`. This guarantees condition `(1,2)`.

Take a different repeated value and split two of its occurrences between labels `1` and `3`. This guarantees condition `(1,3)`.

Assign label `1` everywhere else.

Now no duplicated value is ever split between labels `2` and `3`, because label `2` appears only inside the first chosen value and label `3` appears only inside the second chosen value. Thus condition `(2,3)` never becomes true.

This immediately reveals the feasibility condition. We need at least two distinct values that occur at least twice. If fewer than two values have frequency at least two, we cannot create two different conditions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3ⁿ · n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the occurrences of every value in the array.
2. Collect all values whose frequency is at least two.
3. If fewer than two such values exist, print `-1`.

We need two different repeated values, one to create condition `(1,2)` and another to create condition `(1,3)`.
4. Initialize the answer array `b` with all elements equal to `1`.

Label `1` acts as the default label and helps us avoid accidentally creating condition `(2,3)`.
5. Let the first repeated value be `x` and the second repeated value be `y`.
6. Scan the array from left to right.
7. For the first occurrence of `x` that we choose, assign label `2`.

All other occurrences of `x` remain label `1`, so value `x` creates condition `(1,2)`.
8. For the first occurrence of `y` that we choose, assign label `3`.

All other occurrences of `y` remain label `1`, so value `y` creates condition `(1,3)`.
9. Output the resulting array.

### Why it works

The construction explicitly creates condition `(1,2)` because value `x` appears at least twice and is split between labels `1` and `2`.

Similarly, value `y` appears at least twice and is split between labels `1` and `3`, creating condition `(1,3)`.

No value is ever split between labels `2` and `3`. Label `2` is used on exactly one occurrence of `x`, while label `3` is used on exactly one occurrence of `y`. Since the condition `(2,3)` requires equal values carrying labels `2` and `3`, it cannot occur.

Exactly two conditions are true, so the construction is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = {}
        for x in a:
            freq[x] = freq.get(x, 0) + 1

        repeated = [x for x, cnt in freq.items() if cnt >= 2]

        if len(repeated) < 2:
            print(-1)
            continue

        x = repeated[0]
        y = repeated[1]

        b = [1] * n

        used_x = False
        used_y = False

        for i in range(n):
            if a[i] == x and not used_x:
                b[i] = 2
                used_x = True
            elif a[i] == y and not used_y:
                b[i] = 3
                used_y = True

        print(*b)

solve()
```

The first section computes frequencies. We only care about values appearing at least twice because unique values can never help satisfy any condition.

The feasibility check is based on the central observation of the solution. If fewer than two values are duplicated, we cannot create both required conditions.

The answer starts as all ones. This is a deliberate design choice. Keeping every position at label `1` avoids creating any unwanted relationship. We then make exactly two controlled modifications.

The variables `used_x` and `used_y` guarantee that only one occurrence of each selected duplicated value receives the special label. Every remaining occurrence stays at label `1`, which creates the desired `(1,2)` and `(1,3)` splits.

No special handling is required for values appearing more than twice. Leaving the extra occurrences as label `1` preserves the same argument.

## Worked Examples

### Example 1

Input:

```
4
1 1 2 2
```

Frequencies:

| Value | Frequency |
| --- | --- |
| 1 | 2 |
| 2 | 2 |

Repeated values are `1` and `2`.

| Index | a[i] | Action | b |
| --- | --- | --- | --- |
| 0 | 1 | first chosen occurrence of x, assign 2 | [2,1,1,1] |
| 1 | 1 | leave as 1 | [2,1,1,1] |
| 2 | 2 | first chosen occurrence of y, assign 3 | [2,1,3,1] |
| 3 | 2 | leave as 1 | [2,1,3,1] |

Final answer:

```
2 1 3 1
```

Value `1` creates condition `(1,2)`. Value `2` creates condition `(1,3)`. No value creates `(2,3)`.

### Example 2

Input:

```
5
2 3 3 3 2
```

Frequencies:

| Value | Frequency |
| --- | --- |
| 2 | 2 |
| 3 | 3 |

Repeated values are `2` and `3`.

| Index | a[i] | Action | b |
| --- | --- | --- | --- |
| 0 | 2 | first chosen occurrence of x, assign 2 | [2,1,1,1,1] |
| 1 | 3 | first chosen occurrence of y, assign 3 | [2,3,1,1,1] |
| 2 | 3 | leave as 1 | [2,3,1,1,1] |
| 3 | 3 | leave as 1 | [2,3,1,1,1] |
| 4 | 2 | leave as 1 | [2,3,1,1,1] |

Final answer:

```
2 3 1 1 1
```

This example shows that frequencies larger than two do not require any extra work. Only one special occurrence is needed for each selected value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass for frequencies and one pass for construction |
| Space | O(n) | Frequency map and answer array |

The maximum array size is only 100, so this solution is far below the limits. Even across all test cases, the running time is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = []

    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = Counter(a)
        repeated = [x for x, c in freq.items() if c >= 2]

        if len(repeated) < 2:
            out.append("-1")
            continue

        x = repeated[0]
        y = repeated[1]

        b = [1] * n
        used_x = used_y = False

        for i in range(n):
            if a[i] == x and not used_x:
                b[i] = 2
                used_x = True
            elif a[i] == y and not used_y:
                b[i] = 3
                used_y = True

        out.append(" ".join(map(str, b)))

    return "\n".join(out)

# all distinct
assert run("1\n4\n1 2 3 4\n") == "-1"

# only one duplicated value
assert run("1\n3\n1 2 1\n") == "-1"

# exactly two duplicated values
assert run("1\n4\n1 1 2 2\n") == "2 1 3 1"

# all equal
assert run("1\n5\n7 7 7 7 7\n") == "-1"

# larger valid case
assert run("1\n6\n1 1 2 2 3 3\n") == "2 1 3 1 1 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3 4` | `-1` | No repeated values |
| `1 2 1` | `-1` | Only one duplicated value |
| `1 1 2 2` | Valid construction | Smallest solvable structure |
| `7 7 7 7 7` | `-1` | One value repeated many times |
| `1 1 2 2 3 3` | Valid construction | Multiple duplicated values |

## Edge Cases

Consider:

```
3
1 2 1
```

Only value `1` appears twice. The repeated-values list contains exactly one element. The algorithm immediately prints:

```
-1
```

This is correct because one duplicated value can create at most one of the required conditions.

Consider:

```
4
1 2 3 4
```

Every frequency equals one. No condition can ever become true because all three conditions require equal values. The repeated-values list is empty, so the algorithm prints:

```
-1
```

Consider:

```
5
7 7 7 7 7
```

Although there are many occurrences, there is only one distinct duplicated value. The algorithm still prints:

```
-1
```

This catches a subtle mistake. A large frequency of a single value does not help. We need two different duplicated values so that one can create `(1,2)` and another can create `(1,3)`.

Finally, consider:

```
6
1 1 1 2 2 2
```

The algorithm chooses value `1` for label `2` and value `2` for label `3`, producing:

```
2 1 1 3 1 1
```

Value `1` satisfies `(1,2)`, value `2` satisfies `(1,3)`, and no equal value is split between labels `2` and `3`. The construction remains valid even when frequencies exceed two.
