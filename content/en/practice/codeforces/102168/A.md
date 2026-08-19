---
title: "CF 102168A - \u0421\u0440\u0435\u0434\u043d\u0435\u0435 \u0430\u0440\u0438\u0444\u043c\u0435\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0435"
description: "We maintain a multiset of nonnegative integers while processing operations in a fixed order. An addition operation inserts one occurrence of a value, while a deletion operation removes exactly one occurrence of a value that is currently present."
date: "2026-08-19T07:18:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102168
codeforces_index: "A"
codeforces_contest_name: "\u041b\u0438\u0447\u043d\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u043e\u0433\u043e \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442\u0430 \u0441\u0440\u0435\u0434\u0438 \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432 2018-2019"
rating: 0
weight: 102168
solve_time_s: 90
verified: true
draft: false
---

[CF 102168A - \u0421\u0440\u0435\u0434\u043d\u0435\u0435 \u0430\u0440\u0438\u0444\u043c\u0435\u0442\u0438\u0447\u0435\u0441\u043a\u043e\u0435](https://codeforces.com/problemset/problem/102168/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a multiset of nonnegative integers while processing operations in a fixed order. An addition operation inserts one occurrence of a value, while a deletion operation removes exactly one occurrence of a value that is currently present. Duplicate values are allowed, so removing one copy must not remove all copies unless there was only one.

After every operation, we need the arithmetic mean of all currently stored values. If the multiset becomes empty, the required answer is zero.

The direct mathematical definition is

[
\text{average}=\frac{\text{sum of all elements}}{\text{number of elements}}.
]

The key difficulty is that there can be up to 200,000 operations. With a two-second limit, an algorithm that scans the whole multiset after every operation would perform on the order of (n^2) work. For (n=200000), that can reach about 40 billion element visits, which is far beyond what is practical. We need each operation to require only constant or logarithmic work.

The value (x) can be as large as (10^9), and there can be 200,000 elements simultaneously. Their total sum can consequently reach (2\cdot10^{14}). Python integers handle this range exactly, and even a double-precision floating-point number can represent every integer up to (2^{53}), which is larger than (2\cdot10^{14}). The final division is also safe for the required relative or absolute error of (10^{-9}).

The first edge case is an empty multiset. For example,

```
1
+ 0
```

produces

```
0.0
```

because the only element is zero. More generally, after adding and then removing the only element,

```
2
+ 5
- 5
```

the answers are

```
5.0
0.0
```

A careless implementation that always divides by the current size without checking for zero would attempt division by zero after the second operation.

The second edge case is a multiset containing duplicate values. Consider

```
3
+ 2
+ 2
- 2
```

The correct output is

```
2.0
2.0
2.0
```

The deletion removes only one occurrence, so one `2` remains. An implementation that treats the structure as an ordinary set could remove the value entirely and incorrectly report zero.

The third edge case is a large value. For example,

```
2
+ 1000000000
+ 1000000000
```

has answers

```
1000000000.0
1000000000.0
```

A solution using an unnecessarily narrow integer type could overflow while computing the sum. Python's arbitrary-precision integers avoid that issue.

## Approaches

The brute-force approach follows the definition of an arithmetic mean literally. Keep the current elements, perform the requested insertion or deletion, then iterate over every remaining element to compute its sum and divide by the number of elements. This is correct because it reconstructs exactly the quantity requested after every operation.

The problem is the repeated scan. If the multiset contains roughly (n/2) elements for most of the (n) operations, the total amount of work is quadratic. In the worst case, the number of visited elements is on the order of

[
1+2+\dots+(n-1)=\frac{n(n-1)}2.
]

For (n=200000), this is about 20 billion visits even in this simple increasing-size scenario. A construction that keeps the multiset large throughout can still produce the same quadratic order. Such a solution cannot fit the time limit.

The observation that unlocks the faster solution is that an insertion or deletion changes the total sum and the total number of elements in only one place. We do not need to inspect the other elements because their contribution to both quantities remains unchanged.

Suppose the current sum is (S) and the current size is (C). Adding (x) changes them to (S+x) and (C+1). Removing one occurrence of (x) changes them to (S-x) and (C-1). The answer can then be calculated immediately as (S/C).

There is actually no need to store the entire multiset for this problem. The statement guarantees that every deletion is valid, so we do not need a data structure to verify whether (x) exists. We only need the aggregate sum and the number of elements. Duplicate values also require no special handling because every occurrence contributes independently to the sum and count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^2)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(1)) auxiliary space | Accepted |

## Algorithm Walkthrough

1. Initialize `total = 0` and `count = 0`. These variables represent the sum of all currently present occurrences and their total number.
2. Read the next operation and its value `x`. If the operation is `+`, add `x` to `total` and increase `count` by one. This exactly reflects inserting one new occurrence.
3. If the operation is `-`, subtract `x` from `total` and decrease `count` by one. The input guarantees that this occurrence can be removed, so no membership check or frequency map is required.
4. After applying the operation, check `count`. If it is zero, output `0.0`, because the arithmetic mean of the empty multiset is defined to be zero. Otherwise, output `total / count`.
5. Repeat this process for all (n) operations. Each operation uses only a constant number of arithmetic operations, so the complete processing is linear.

### Why it works

The invariant is that after every processed operation, `total` equals the sum of every occurrence currently in the multiset, while `count` equals the number of those occurrences. Initially both values are correct for the empty multiset. An insertion adds exactly (x) to the sum and exactly one occurrence to the count. A deletion removes exactly (x) from the sum and exactly one occurrence from the count. Thus the invariant remains true after every operation. When the multiset is nonempty, `total / count` is precisely its arithmetic mean, and when `count` is zero, the algorithm outputs the separately defined value zero.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    total = 0
    count = 0
    output = []

    for _ in range(n):
        op, x = input().split()
        x = int(x)

        if op == '+':
            total += x
            count += 1
        else:
            total -= x
            count -= 1

        if count == 0:
            output.append("0.0")
        else:
            output.append(str(total / count))

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The two state variables directly implement the invariant from the walkthrough. `total` is updated before calculating the answer, because the requested mean is for the multiset after the current operation, not before it.

The deletion branch uses `total -= x` and `count -= 1`. There is no frequency dictionary because the input explicitly guarantees that a deletion always refers to an existing occurrence. Maintaining unnecessary frequencies would increase memory usage without contributing to the answer.

The `count == 0` check must happen before division. The problem explicitly defines the mean of an empty multiset as zero, so this case cannot be handled by ordinary division.

Python's integer arithmetic keeps `total` exact even when it reaches (2\cdot10^{14}). The division produces a floating-point value. Its relative precision is comfortably within the required (10^{-9}) tolerance for the range of possible answers.

Collecting the answers in `output` and writing them once avoids performing a separate system-level output operation for every line. This is useful when there are 200,000 answers.

## Worked Examples

For Sample 1, the important state is the current sum and the number of occurrences. The individual elements never need to be stored.

| Operation | `total` | `count` | Average |
| --- | --- | --- | --- |
| `+ 1` | 1 | 1 | 1.0 |
| `+ 2` | 3 | 2 | 1.5 |
| `+ 2` | 5 | 3 | 1.6666666666666667 |
| `+ 0` | 5 | 4 | 1.25 |
| `+ 3` | 8 | 5 | 1.6 |
| `- 1` | 7 | 4 | 1.75 |
| `+ 4` | 11 | 5 | 2.2 |
| `- 2` | 9 | 4 | 2.25 |
| `- 0` | 9 | 3 | 3.0 |

The duplicate `2` values demonstrate why a multiset matters. After the third operation there are two separate occurrences of `2`, and after removing one of them there is still another `2` contributing to both `total` and `count`. The invariant tracks occurrences rather than distinct values, so it naturally handles this situation.

For Sample 2, every operation adds a consecutive value close to (10^9).

| Operation | `total` | `count` | Average |
| --- | --- | --- | --- |
| `+ 999999001` | 999999001 | 1 | 999999001.0 |
| `+ 999999002` | 1999998003 | 2 | 999999001.5 |
| `+ 999999003` | 2999997006 | 3 | 999999002.0 |
| `+ 999999004` | 3999996010 | 4 | 999999002.5 |
| `+ 999999005` | 4999995015 | 5 | 999999003.0 |

This example exercises the upper range of the values. The total remains an exact Python integer, and the final division gives the required average.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Every operation performs a constant amount of work. |
| Space | (O(n)) | The answer strings require (O(n)) memory; the algorithm itself uses (O(1)) auxiliary state. |

With (n\leq200000), linear processing means roughly one pass over the input and a constant amount of arithmetic per operation. This is easily compatible with the two-second limit. The stored output is also only linear in the number of operations, while no representation of the multiset itself is needed.

## Test Cases

The test harness below uses the same `solve()` logic while redirecting standard input. Since floating-point textual representations can differ while both satisfy the required error bound, the helper compares numeric answers rather than requiring identical decimal formatting. The provided samples are included, followed by cases for the empty multiset, duplicates, boundary values, and a maximum-size input.

```python
import sys
import io
import math

def solve():
    n = int(input())

    total = 0
    count = 0
    output = []

    for _ in range(n):
        op, x = input().split()
        x = int(x)

        if op == '+':
            total += x
            count += 1
        else:
            total -= x
            count -= 1

        if count == 0:
            output.append("0.0")
        else:
            output.append(str(total / count))

    sys.stdout.write("\n".join(output))

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            solve()
            return sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
    finally:
        sys.stdin = old_stdin
        input = old_input

def assert_output(inp: str, expected):
    actual = run(inp).strip().splitlines()
    assert len(actual) == len(expected)

    for a, e in zip(actual, expected):
        assert math.isclose(
            float(a),
            float(e),
            rel_tol=1e-9,
            abs_tol=1e-9
        ), f"expected {e}, got {a}"

# Sample 1
sample1 = """\
9
+ 1
+ 2
+ 2
+ 0
+ 3
- 1
+ 4
- 2
- 0
"""

assert_output(sample1, [
    "1.0",
    "1.5",
    "1.66666666667",
    "1.25",
    "1.6",
    "1.75",
    "2.2",
    "2.25",
    "3.0",
])

# Sample 2
sample2 = """\
5
+ 999999001
+ 999999002
+ 999999003
+ 999999004
+ 999999005
"""

assert_output(sample2, [
    "999999001.0",
    "999999001.5",
    "999999002.0",
    "999999002.5",
    "999999003.0",
])

# Minimum size
assert_output("""\
1
+ 0
""", ["0.0"])

# Empty multiset after deletion, followed by another insertion
assert_output("""\
4
+ 5
- 5
+ 10
- 10
""", ["5.0", "0.0", "10.0", "0.0"])

# All values equal, with duplicate deletion
assert_output("""\
6
+ 7
+ 7
+ 7
- 7
- 7
- 7
""", ["7.0", "7.0", "7.0", "7.0", "7.0", "0.0"])

# Boundary values
assert_output("""\
4
+ 1000000000
+ 0
- 1000000000
- 0
""", ["1000000000.0", "500000000.0", "0.0", "0.0"])

# Maximum-size case: 200000 equal elements.
# This checks that the implementation remains linear and handles
# the largest allowed number of operations.
n = 200000
max_case = str(n) + "\n" + "+ 1\n" * n
max_expected = ["1.0"] * n

assert_output(max_case, max_expected)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / + 0` | `0.0` | Minimum input and a zero-valued element |
| `+ 5, - 5, + 10, - 10` | `5.0, 0.0, 10.0, 0.0` | Empty multiset handling after deletions |
| Three additions and three deletions of `7` | Six answers equal to `7.0`, ending with `0.0` | Duplicate occurrences and the transition to empty |
| `+ 1000000000, + 0, - 1000000000, - 0` | `1000000000.0, 500000000.0, 0.0, 0.0` | Maximum value, zero, and deletion ordering |
| 200,000 additions of `1` | 200,000 answers equal to `1.0` | Maximum operation count and linear performance |

## Edge Cases

The empty multiset is handled explicitly. For the input

```
2
+ 5
- 5
```

the first operation gives `total = 5` and `count = 1`, so the answer is `5.0`. The second operation changes the state to `total = 0` and `count = 0`. The division is skipped and the algorithm outputs `0.0`, matching the special definition for an empty multiset.

Duplicate values are represented automatically because `count` counts occurrences rather than distinct numbers. For

```
3
+ 2
+ 2
- 2
```

the states are `(2, 1)`, `(4, 2)`, and `(2, 1)` for `(total, count)`. Every answer is `2.0`. There is no need to distinguish which physical occurrence was removed because equal values have identical contributions.

A zero value requires no special arithmetic treatment. For

```
2
+ 5
+ 0
```

the state changes from `(5, 1)` to `(5, 2)`, producing `5.0` and `2.5`. The zero increases the number of elements without changing the sum, exactly as the aggregate representation predicts.

The maximum value also causes no overflow in Python. With

```
2
+ 1000000000
+ 1000000000
```

the total becomes `2000000000`, and the count becomes `2`, giving `1000000000.0`. Across 200,000 such insertions the total can reach `200000000000000`, which Python represents exactly.

The maximum number of operations does not require a larger algorithmic structure. With 200,000 additions, every operation still consists of one update to `total`, one update to `count`, and one division. The total work grows linearly, which is the property that makes the solution suitable for the input limit.
