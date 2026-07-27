---
title: "CF 102775D - \u0420\u0430\u0437\u043b\u0438\u0447\u043d\u044b\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u044b"
description: "The task is to look through a sequence of numbers and count how many different values satisfy a strict range condition. A value is included only when it is greater than x and smaller than y. If the same valid number appears several times, it contributes only once to the answer."
date: "2026-07-27T20:37:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102775
codeforces_index: "D"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 20), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102775
solve_time_s: 43
verified: true
draft: false
---

[CF 102775D - \u0420\u0430\u0437\u043b\u0438\u0447\u043d\u044b\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u044b](https://codeforces.com/problemset/problem/102775/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to look through a sequence of numbers and count how many different values satisfy a strict range condition. A value is included only when it is greater than `x` and smaller than `y`. If the same valid number appears several times, it contributes only once to the answer.

The input contains the size of the array, the two borders of the allowed range, and the array itself. The output is a single integer representing the number of unique array values that lie strictly between those two borders.

The array can contain up to 150000 elements. A solution that checks every pair of values or repeatedly searches the array would perform too many operations at this size. With around 100000 to 200000 elements, we usually need an approach close to linear time, because quadratic work can reach billions of operations and will not fit into a typical one second limit.

The values themselves can be as large as two billion in either direction, so the algorithm must compare integers correctly without relying on small fixed ranges. In Python this is handled naturally because integers have arbitrary precision.

Several boundary cases can break an incorrect solution. The first common mistake is treating the borders as inclusive. For example:

```
5
1 5
1 2 3 5 6
```

The correct output is:

```
3
```

The valid values are `2`, `3`, and `?` Actually, because the condition is strict, only `2` and `3` are valid, so the correct output is:

```
2
```

A careless implementation using `x <= ai <= y` would count `1` and `5` and return the wrong answer.

Another issue is counting occurrences instead of different values. For example:

```
6
0 10
3 3 3 7 7 11
```

The correct output is:

```
2
```

The valid numbers are `3` and `7`. Counting every occurrence would produce `5`, which does not match the requirement.

A final edge case is when no value belongs to the range:

```
4
5 8
1 2 5 8
```

The correct output is:

```
0
```

The values equal to the boundaries are excluded, so the answer is zero.

## Approaches

A direct solution would inspect every element and maintain the set of values that satisfy the condition. This is already a good solution idea because the operation needed for each number is simple: compare it with the two boundaries and insert it if it is valid. The only work is deciding how to avoid counting duplicates. A set naturally represents the collection of different valid values.

A slower brute force interpretation would compare every value with every other value to determine whether it has appeared before. That approach is correct because it can detect duplicates explicitly, but for `N = 150000` it would perform about `N * N`, or roughly 22500000000, comparisons in the worst case. This is far beyond what the time limit allows.

The key observation is that duplicate detection does not require searching through all previous elements. The problem only asks for the number of different valid values, and a set is exactly the data structure that stores unique elements while supporting fast insertion. Each array element can be processed independently. If it is inside the range, it is added to the set, and repeated values simply leave the set unchanged.

The brute force works because it can identify duplicates by checking everything against everything else, but fails because the number of comparisons grows too quickly. The observation that uniqueness can be handled directly by a hash set reduces the task to a single pass through the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Optimal | O(N) average | O(K) | Accepted |

## Algorithm Walkthrough

1. Read the array size, the two range borders, and all array values. The algorithm only needs to inspect each value once, so the input can be processed as a simple sequence.
2. Create an empty set that will store all values satisfying the condition. The set is used because the answer depends on how many different values exist, not how many positions contain those values.
3. Traverse every number in the array. If the number is greater than `x` and smaller than `y`, insert it into the set. The strict comparisons are necessary because values equal to either border must be ignored.
4. After all numbers have been processed, output the size of the set. Every element in the set represents exactly one distinct valid value, so its size is the required answer.

Why it works: During the traversal, the set always contains exactly the distinct values seen so far that satisfy the range condition. Adding a new valid value preserves this property because sets discard duplicates automatically. Ignoring invalid values also preserves the property because they can never contribute to the final answer. After the entire array has been examined, the invariant applies to the whole input, so the set size is exactly the number of required elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    x, y = map(int, input().split())
    a = list(map(int, input().split()))

    values = set()

    for value in a:
        if x < value < y:
            values.add(value)

    print(len(values))

if __name__ == "__main__":
    solve()
```

The program reads all array values once and stores valid values in `values`. Python's set implementation handles insertion and duplicate removal automatically, matching the mathematical definition of distinct elements.

The condition `x < value < y` is written as a chained comparison, which directly expresses the strict range requirement. Using `<=` here would introduce an off by one error by including the borders.

The final answer is obtained with `len(values)`, because every stored element corresponds to exactly one unique number. No extra counting logic is needed, and repeated values never affect the result.

Python integers are safe for the given limits, so no special handling is required for values near two billion.

## Worked Examples

Using the first custom interpretation of the statement:

Input:

```
5
1 5
1 2 3 5 6
```

The trace is:

| Current value | Inside range? | Set after processing |
| --- | --- | --- |
| 1 | No | `{}` |
| 2 | Yes | `{2}` |
| 3 | Yes | `{2, 3}` |
| 5 | No | `{2, 3}` |
| 6 | No | `{2, 3}` |

The final set contains two values, so the output is `2`. This trace shows why the borders are excluded.

Second example:

Input:

```
6
0 10
3 3 3 7 7 11
```

The trace is:

| Current value | Inside range? | Set after processing |
| --- | --- | --- |
| 3 | Yes | `{3}` |
| 3 | Yes | `{3}` |
| 3 | Yes | `{3}` |
| 7 | Yes | `{3, 7}` |
| 7 | Yes | `{3, 7}` |
| 11 | No | `{3, 7}` |

The duplicate values do not increase the set size. The final answer is `2`, which demonstrates why counting occurrences would be incorrect.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) average | Each array element is checked once, and set insertion takes average constant time. |
| Space | O(K) | The set stores only the distinct valid values, where K is the number of such values. |

The maximum array size is 150000, so a linear scan performs a small number of operations per element and fits comfortably within the limits. The memory usage is also bounded by the number of distinct values that can appear in the answer.

## Test Cases

```python
import sys
import io

def solve(data):
    input = io.StringIO(data).readline

    n = int(input())
    x, y = map(int, input().split())
    a = list(map(int, input().split()))

    values = set()
    for value in a:
        if x < value < y:
            values.add(value)

    return str(len(values))

def run(inp: str) -> str:
    return solve(inp)

assert run("""5
1 5
1 2 3 5 6
""") == "2", "sample style 1"

assert run("""6
0 10
3 3 3 7 7 11
""") == "2", "sample style 2"

assert run("""1
0 10
5
""") == "1", "single valid element"

assert run("""5
1 2
1 2 3 4 5
""") == "0", "exclusive boundaries"

assert run("""8
-5 5
-5 -4 -4 0 0 4 5 6
""") == "3", "negative values and duplicates"

assert run("""10
0 100
42 42 42 42 42 42 42 42 42 42
""") == "1", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 / 1 5 / 1 2 3 5 6` | 2 | Strict boundary handling |
| `6 / 0 10 / 3 3 3 7 7 11` | 2 | Duplicate removal |
| `1 / 0 10 / 5` | 1 | Minimum size input |
| `5 / 1 2 / 1 2 3 4 5` | 0 | Empty valid range |
| `8 / -5 5 / -5 -4 -4 0 0 4 5 6` | 3 | Negative numbers and edge values |
| `10 / 0 100 / ten copies of 42` | 1 | All elements equal |

## Edge Cases

For the strict boundary case:

```
5
1 5
1 2 3 5 6
```

The algorithm checks each value. `1` is rejected because it is not greater than `1`. `5` is rejected because it is not smaller than `5`. The set receives only `2` and `3`, producing `2`.

For the duplicate case:

```
6
0 10
3 3 3 7 7 11
```

The first `3` is inserted, while the next two `3` values are ignored by the set because they already exist. The same happens for `7`. The value `11` fails the range check. The resulting set is `{3, 7}`, so the answer is `2`.

For the case with no valid values:

```
4
5 8
1 2 5 8
```

Every number fails the strict comparison. The set remains empty from start to finish, and the algorithm correctly outputs `0`.

For the case with negative numbers:

```
8
-5 5
-5 -4 -4 0 0 4 5 6
```

The values `-5` and `5` are excluded because they match the boundaries. The values `-4`, `0`, and `4` are inserted, while `6` is too large. The final set contains three elements, so the answer is `3`.
