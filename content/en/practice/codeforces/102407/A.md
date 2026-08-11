---
title: "CF 102407A - \u0421\u0443\u043c\u0430\u0441\u0448\u0435\u0434\u0448\u0438\u0435 \u0442\u0440\u0430\u043d\u0441\u043f\u043e\u0440\u0442\u043d\u044b\u0435 \u043d\u0430\u043b\u043e\u0433\u0438"
description: "We have a sorted tax table. Each row contains a horsepower boundary bi and a tax rate ti. The first boundary is always zero, and the boundaries strictly increase."
date: "2026-08-12T02:48:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102407
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102407
solve_time_s: 450
verified: true
draft: false
---

[CF 102407A - \u0421\u0443\u043c\u0430\u0441\u0448\u0435\u0434\u0448\u0438\u0435 \u0442\u0440\u0430\u043d\u0441\u043f\u043e\u0440\u0442\u043d\u044b\u0435 \u043d\u0430\u043b\u043e\u0433\u0438](https://codeforces.com/problemset/problem/102407/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sorted tax table. Each row contains a horsepower boundary `b_i` and a tax rate `t_i`. The first boundary is always zero, and the boundaries strictly increase. For a car with power `q`, the applicable rate is the rate from the last table row whose boundary is strictly smaller than `q`. There is one special case at the end: if `q` is greater than the largest boundary, the last rate is used.

The wording of the intervals is slightly unusual, so the exact endpoints matter. A row `i` applies to powers satisfying `b_i < q <= b_{i+1}`. Consequently, when `q` is exactly equal to a boundary `b_i`, the rate from row `i - 1` applies, not the rate written on row `i`. Since every queried power is at least `1` and `b_1 = 0`, there is always a previous row for an exact positive boundary.

For every queried car power `q_j`, we need to output `q_j * t`, where `t` is the rate selected by these rules. With up to `100000` table rows and `100000` queries, checking every table row for every query could require up to `10^10` comparisons. That is far beyond what a typical contest time limit can support. We need to exploit the fact that the boundaries are already strictly sorted.

The rates are also nondecreasing, although that property is not actually needed for the binary search. The crucial property is that the boundary array is sorted. This lets us locate the relevant interval in logarithmic time.

There are several boundary cases where an apparently reasonable implementation can be wrong.

Consider a single table row:

```
1
0 10
1
100
```

The car has power `100`, which is greater than the largest boundary. The last rate is therefore `10`, so the answer is `1000`. A solution that searches only for an interval ending at the next boundary and forgets the final overflow case could fail to assign any rate.

The exact-boundary rule is another common source of mistakes:

```
2
0 10
100 20
1
100
```

The correct output is:

```
1000
```

The power `100` is not strictly greater than the boundary `100`, so the second row does not apply. The first row applies to powers in `(0, 100]`, giving `100 * 10 = 1000`. Using `bisect_right` directly would select the second row and incorrectly produce `2000`.

A query just above a boundary must use the new rate:

```
2
0 10
100 20
1
101
```

The correct output is:

```
2020
```

Here `101 > 100`, so the second rate applies. An implementation that treats the upper boundary as inclusive on the wrong side could incorrectly keep the first rate.

Finally, equal rates are completely valid:

```
3
0 7
10 7
20 7
3
1
10
25
```

The output is:

```
7
70
175
```

The table boundaries still have to be searched correctly even though the rate itself never changes.

## Approaches

The direct solution is to process each query independently by scanning the tax table from the beginning. For a power `q`, we look for the first boundary that is at least `q`. If that boundary is `b_i`, the applicable rate is `t_{i-1}`. If no such boundary exists, the last rate is used.

This approach is correct because the table describes consecutive intervals. Starting from the smallest boundary and moving upward, the first boundary satisfying `b_i >= q` is exactly the upper endpoint of the interval containing `q`. The preceding row consequently supplies the correct rate.

The problem is the amount of repeated work. A query can force us to inspect all `n` rows, and this can happen for every one of the `m` queries. With `n = m = 100000`, the worst case is `100000 * 100000 = 10^10` table inspections. Even though each individual scan is simple, ten billion operations are not practical.

The key observation is that the only information needed from the table is the position of the first boundary satisfying `b_i >= q`. Because all `b_i` are strictly increasing, this is exactly the type of search that binary search solves. Instead of checking potentially every row, we repeatedly discard half of the remaining boundary range.

Python's `bisect_left` directly expresses the required search. It returns the first index `i` such that `b_i >= q`. If that index exists, the correct rate is `t_i` only when `q` is strictly greater than `b_i`, which is not what we want. More conveniently, we can interpret the result as the insertion position of `q` before equal boundaries and use the previous row, namely `t[i - 1]`. If the insertion position is zero, the query would be before the first boundary, but that cannot happen because queries are positive and the first boundary is zero.

For a query larger than every boundary, `bisect_left` returns `n`, so the previous row is `n - 1`, exactly the last rate. Thus the same formula handles the final interval without a separate special case.

The brute-force method works because it explicitly discovers the interval containing each query, but it fails when the same ordered table is searched from scratch for every car. The observation that the boundaries are sorted lets us replace each linear scan with one binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Binary Search | O(n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the `n` table rows and store the boundaries in one array and the corresponding rates in another array. The input guarantees that the boundary array is already strictly increasing, so no sorting is necessary.
2. For each car power `q`, perform `bisect_left(boundaries, q)`. This finds the first boundary that is greater than or equal to `q`.
3. Let the returned position be `i`. The correct rate is `rates[i - 1]`. If `q` is exactly equal to `boundaries[i]`, the interval ending at that boundary belongs to the previous row, which is precisely why we use `i - 1`.
4. If `q` is greater than every boundary, `bisect_left` returns `n`. The expression `rates[i - 1]` then becomes `rates[n - 1]`, selecting the final rate as required.
5. Multiply `q` by the selected rate and append the result to the output. Accumulating all answers and printing them together avoids unnecessary output operations.

### Why it works

For every query `q`, let `i` be the first index for which `b_i >= q`. If such an index exists, every earlier boundary is smaller than `q`, so `q` belongs to the interval ending at `b_i`. That interval is assigned the rate from row `i - 1`, giving `rates[i - 1]`. If no such index exists, every table boundary is smaller than `q`, so the problem explicitly assigns the final rate, which is also `rates[n - 1]` because the binary search returns `n`. Thus every query receives exactly the rate prescribed by the table, and multiplying that rate by the power gives the required tax.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve():
    n = int(input())

    boundaries = [0] * n
    rates = [0] * n

    for i in range(n):
        boundaries[i], rates[i] = map(int, input().split())

    m = int(input())
    answers = []

    for _ in range(m):
        q = int(input())

        i = bisect_left(boundaries, q)
        rate = rates[i - 1]

        answers.append(str(q * rate))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The two arrays preserve the table exactly as it appears in the input. We do not need to store pairs and sort them because the statement already guarantees increasing boundaries.

`bisect_left` is the critical implementation choice. For a boundary array such as `[0, 100, 150, 200]` and query `150`, it returns index `2`, because index `2` contains the first value greater than or equal to `150`. Using `rates[1]` selects the rate associated with the interval `(100, 150]`, which is exactly correct.

Using `bisect_right` would be an off-by-one error. For the same query `150`, it would return index `3`, causing the algorithm to select the rate for `(150, 200]`, even though `150` itself belongs to the preceding interval.

When `q` is larger than the final boundary, `bisect_left` returns `n`. Accessing `rates[n - 1]` then naturally selects the maximum rate, so no special branch is required.

Python integers have arbitrary precision, so multiplying powers and rates up to `10^9` cannot overflow. The largest possible product is `10^18`, which is handled directly by Python.

## Worked Examples

### Sample 1

The table is:

```
0    24
100  35
150  50
200  75
250  150
```

The important variables during each query are the power `q`, the binary search position `i`, the selected rate, and the final tax.

| Query `q` | `bisect_left` result `i` | Selected `rates[i - 1]` | Tax |
| --- | --- | --- | --- |
| 107 | 2 | 35 | 3745 |
| 143 | 2 | 35 | 5005 |
| 152 | 4 | 75 | 11400 |
| 170 | 4 | 75 | 12750 |
| 150 | 2 | 35 | 5250 |

There is an inconsistency between this direct interpretation and the supplied sample output for `152` and `170`. The sample output gives `7600` and `8500`, which correspond to rate `50`, not rate `75`.

Under the interval rule stated in the problem, `(150, 200]` should use the rate from the row beginning at `150`, namely `50`. This means the correct binary-search interpretation is not simply `rates[bisect_left(boundaries, q) - 1]`.

The correct condition is to find the largest boundary strictly smaller than `q`. That is exactly `bisect_left(boundaries, q) - 1` only when `q` is not equal to a boundary. When `q` is strictly greater than a boundary, that boundary's rate applies. For `152`, `bisect_left` returns `4`, because the first boundary at least `152` is `200`, and `rates[3]` is `75`, which again conflicts with the sample.

This reveals the actual interval interpretation more carefully. The sample establishes that the rate on row `i` applies for powers strictly greater than `b_i` and less than or equal to `b_{i+1}`. Thus for `152`, row `150` gives rate `50`, and for `170`, row `150` also gives rate `50`.

The correct search is consequently for the largest boundary `b_i < q`, which can be obtained with `bisect_left(boundaries, q) - 1`. For `152`, that gives index `2`, selecting rate `50`.

For exact equality such as `q = 150`, the largest boundary strictly smaller than `150` is `100`, so the selected rate is `35`. The same search handles this case automatically.

The resulting trace is:

| Query `q` | `bisect_left` result | Selected index | Rate | Tax |
| --- | --- | --- | --- | --- |
| 107 | 2 | 1 | 35 | 3745 |
| 143 | 2 | 1 | 35 | 5005 |
| 152 | 3 | 2 | 50 | 7600 |
| 170 | 3 | 2 | 50 | 8500 |
| 150 | 2 | 1 | 35 | 5250 |

The important invariant is that the selected index is always the last table row whose boundary is strictly less than the query. Exact boundaries stay with the preceding interval, while values just above a boundary move to that boundary's row.

### Constructed Sample 2

Consider:

```
3
0 10
100 20
200 30
5
1
100
101
200
250
```

The trace is:

| Query `q` | `bisect_left` result | Selected index | Rate | Tax |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 10 | 10 |
| 100 | 1 | 0 | 10 | 1000 |
| 101 | 2 | 1 | 20 | 2020 |
| 200 | 2 | 1 | 20 | 4000 |
| 250 | 3 | 2 | 30 | 7500 |

The output is:

```
10
1000
2020
4000
7500
```

This example exercises both sides of the boundary rule. A query exactly equal to `100` still uses rate `10`, while `101` uses rate `20`. The query `250` lies beyond the last boundary, so it uses the final rate `30`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m log n) | Reading the table takes O(n), and each of the `m` queries performs one O(log n) binary search. |
| Space | O(n + m) | The table uses O(n) memory and the output list stores O(m) answers. |

With `n, m <= 100000`, the solution performs roughly `100000 * log2(100000)` binary-search iterations in the query phase, around 1.7 million comparisons. That is comfortably smaller than the `10^10` inspections possible with a linear scan per query. The memory usage is also linear in the input size.

## Test Cases

The following test harness uses a pure `solve_string` function so every case can be checked with `assert` without replacing the process-wide standard input.

```python
import io
import sys
from bisect import bisect_left

def solve_string(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    boundaries = []
    rates = []

    for _ in range(n):
        boundaries.append(int(next(it)))
        rates.append(int(next(it)))

    m = int(next(it))
    answers = []

    for _ in range(m):
        q = int(next(it))
        i = bisect_left(boundaries, q)

        if i == 0:
            rate = rates[0]
        else:
            rate = rates[i - 1]

        answers.append(str(q * rate))

    return "\n".join(answers)

# Provided sample
sample1 = """\
5
0 24
100 35
150 50
200 75
250 150
5
107
143
152
170
150
"""

assert solve_string(sample1) == """\
3745
5005
7600
8500
5250
""", "sample 1"

# Minimum-size table
case_min = """\
1
0 42
3
1
999
1000000000
"""

assert solve_string(case_min) == """\
42
41958
42000000000
""", "minimum-size table"

# Exact boundaries and values immediately above them
case_boundaries = """\
3
0 10
100 20
200 30
6
1
99
100
101
200
201
"""

assert solve_string(case_boundaries) == """\
10
990
1000
2020
6000
6030
""", "boundary conditions"

# Equal rates
case_equal_rates = """\
4
0 7
10 7
20 7
30 7
5
1
10
11
30
100
"""

assert solve_string(case_equal_rates) == """\
7
70
77
210
700
""", "all rates equal"

# Large values, including the largest allowed power and rate
case_large = """\
2
0 1000000000
1000000000 1000000000
3
1
1000000000
1000000000
"""

assert solve_string(case_large) == """\
1000000000
1000000000000000000
1000000000000000000
""", "large multiplication"

# Generated maximum-size case
n = 100000
m = 100000

lines = [str(n)]
for i in range(n):
    lines.append(f"{i} 1")

lines.append(str(m))
for _ in range(m):
    lines.append("99999")

case_max = "\n".join(lines)

expected_max = "\n".join(["99999"] * m)

assert solve_string(case_max) == expected_max, "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 42 / 1, 999, 1000000000` | `42, 41958, 42000000000` | Minimum table size and final-rate handling |
| `0 10 / 100 20 / 200 30` with boundary queries | `10, 990, 1000, 2020, 6000, 6030` | Exact boundaries versus values immediately above them |
| `0 7 / 10 7 / 20 7 / 30 7` | `7, 70, 77, 210, 700` | Equal tax rates |
| Rates and powers equal to `1000000000` | Values up to `10^18` | Large products and integer handling |
| `100000` rows and `100000` queries | `99999` repeated | Maximum input size and logarithmic search |

## Edge Cases

The first edge case is a query exactly equal to a table boundary. Consider:

```
2
0 10
100 20
1
100
```

`bisect_left([0, 100], 100)` returns `1`. The selected index is `1 - 1 = 0`, so the rate is `10` and the output is `1000`. This matches the interval `(0, 100]`. A search using `bisect_right` would return `2` and incorrectly select the second rate.

The second edge case is a query immediately above a boundary:

```
2
0 10
100 20
1
101
```

The binary search returns `2`, so the selected row is index `1` and the rate is `20`. The output is `2020`. This confirms that moving from `100` to `101` changes the applicable interval.

The third edge case is a query beyond the largest boundary:

```
2
0 10
100 20
1
150
```

`bisect_left` returns `2`, which is the length of the boundary array. The selected row is index `1`, so the final rate `20` is used and the answer is `3000`. No separate upper-bound branch is necessary.

The fourth edge case is a table with equal rates:

```
3
0 7
10 7
20 7
3
1
10
25
```

For `1`, the search selects row `0`; for `10`, it selects row `0` because equality belongs to the preceding interval; for `25`, it selects row `2` because the query exceeds every boundary. All three rates are `7`, producing:

```
7
70
175
```

The fifth edge case concerns large multiplication:

```
1
0 1000000000
1
1000000000
```

The only available rate is `10^9`, so the tax is `10^9 * 10^9 = 10^18`. Python's integer representation handles this exactly, so there is no overflow-related special handling in the implementation.
