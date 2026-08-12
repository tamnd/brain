---
title: "CF 102448B - Beza's Hangover"
description: "The night can be viewed as an array of N positions. Position i stores the drink Beza consumed during the i-th hour. The bar provides M drink names, and each name has an associated alcohol volume. A type 1 query changes one array position to another drink."
date: "2026-08-12T08:20:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102448
codeforces_index: "B"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2020"
rating: 0
weight: 102448
solve_time_s: 172
verified: true
draft: false
---

[CF 102448B - Beza's Hangover](https://codeforces.com/problemset/problem/102448/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

The night can be viewed as an array of N positions. Position i stores the drink Beza consumed during the i-th hour. The bar provides M drink names, and each name has an associated alcohol volume.

A type 1 query changes one array position to another drink. A type 2 query asks about a contiguous subarray [L,R]: would the total alcohol consumed during those hours be enough to cause a hangover?

Suppose the interval contains K=R−L+1 hours. Beza spends 60K minutes drinking, so the maximum alcohol amount that does not cause a hangover is half of that, which is 30K. Consequently, the answer is `YES` exactly when

i=L ∑ R ​ V i ​ >30(R−L+1),

where V i ​ is the alcohol volume of the current drink at position i. Equality gives `NO`, because an amount equal to the limit is still safe.

The first N drink names describe the initial array. The following M lines form a dictionary from drink name to alcohol volume. There are then Q dynamic operations. The relevant quantities can all be as large as 2⋅10 5, so scanning an entire interval for every query can require roughly NQ=4⋅10 10 element visits in the worst case. That is far beyond what a 2 second limit permits. We need logarithmic work per update and query.

There are a few boundary cases that can quietly cause wrong answers. First, an interval of one hour must use a threshold of exactly 30, not 60. For example,

```
1 1 1
a
a 31
2 1 1
```

has output `YES`, because 31>30. A solution that compares against 60(R−L+1) would incorrectly print `NO`.

The equality case is also significant. Consider

```
1 1 1
a
a 30
2 1 1
```

The output is `NO`, since 30 liters is exactly the allowed amount. A careless implementation using `>=` instead of `>` would report a hangover incorrectly.

Updates must affect subsequent queries immediately. For example,

```
2 2 3
a a
a 30
b 100
1 1 b
2 1 1
```

produces

```
YES
```

because position 1 becomes `b`, whose value is 100. Using the original array instead of the current array would incorrectly answer `NO`.

Finally, both endpoints of an interval belong to the query. With

```
2 2 1
a b
a 30
b 31
2 1 2
```

the total is 61, while the threshold is 60, so the answer is `YES`. Accidentally querying a half-open interval such as [L,R) would miss the drink at position R.

## Approaches

The direct solution is to convert every drink name into its alcohol value and store those values in an array. For a type 1 query, we replace one array element. For a type 2 query, we loop from L through R, add all values, and compare the result with 30(R−L+1). This is correct because the query asks precisely for the sum of the current values in that interval.

The problem is the cost of the range query. One query can inspect N elements, and with Q queries the worst case is O(NQ). When N=Q=200000, that is up to 40,000,000,000 array accesses, before even considering the other operations. The 2 second limit rules this approach out.

The useful observation is that every type 2 query needs only a range sum, while every type 1 query changes exactly one value. This is exactly the operation pattern handled by a Fenwick tree. A Fenwick tree stores partial sums so that a point change and a prefix sum both take O(logN) time. Once prefix sums are available, the sum of [L,R] is obtained as `prefix(R) - prefix(L-1)`.

The key reduction is to rewrite the hangover condition as a comparison between two additive quantities. Instead of thinking about minutes separately, we can store only alcohol values in the data structure and calculate the threshold directly as 30(R−L+1). No other information about the drinks is needed after their names have been converted to values.

The brute-force works because directly summing the interval gives exactly the required quantity, but fails when many long intervals are queried. The observation that only point changes and range sums are needed lets us replace repeated scanning with a Fenwick tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NQ) worst case | O(N+M) | Too slow |
| Optimal | O((N+M+Q)logN) | O(N+M) | Accepted |

## Algorithm Walkthrough

1. Read the initial drink names and the M drink values. Store the mapping from each name to its alcohol volume because queries refer to drinks by name.
2. Convert every drink in the initial schedule into its numeric alcohol volume. Keeping numeric values in the array avoids repeated dictionary lookups while processing queries.
3. Build a Fenwick tree over the resulting array. The tree represents prefix sums, which lets us obtain any interval sum by subtracting two prefix sums.
4. For a type 1 query `1 X Y`, look up the alcohol value of drink `Y`. Let the old value at position X be `old` and the new value be `new`. Apply the difference `new - old` to the Fenwick tree at position X, then replace the stored array value with `new`.

Updating by the difference is sufficient because every Fenwick node containing position X only needs its stored sum changed by exactly that amount.
5. For a type 2 query `2 L R`, calculate

S=sum(L,R)

using the Fenwick tree. The interval contains R−L+1 hours, so its safe alcohol limit is

30(R−L+1).

Print `YES` if S>30(R−L+1), and `NO` otherwise.
6. Process all queries in their original order. An update changes the current schedule, so every later range query must use the modified Fenwick tree and array.

The invariant is that after every processed operation, the Fenwick tree contains the exact sum of the current alcohol values at every prefix, and the separate array contains the current value at every position. A point update changes both representations by the same amount, so the invariant survives updates. Since every range sum is obtained from two correct prefix sums, every type 2 query compares the exact current alcohol total with the exact 30-liters-per-hour limit.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, delta):
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def prefix_sum(self, i):
        result = 0
        while i > 0:
            result += self.bit[i]
            i -= i & -i
        return result

    def range_sum(self, l, r):
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

def solve():
    n, m, q = map(int, input().split())

    drinks = input().split()

    value = {}
    for _ in range(m):
        name, v = input().split()
        value[name] = int(v)

    arr = [value[name] for name in drinks]

    fw = Fenwick(n)

    for i, v in enumerate(arr, 1):
        fw.add(i, v)

    out = []

    for _ in range(q):
        query = input().split()
        t = int(query[0])

        if t == 1:
            x = int(query[1])
            y = query[2]

            new_value = value[y]
            old_value = arr[x - 1]

            fw.add(x, new_value - old_value)
            arr[x - 1] = new_value

        else:
            l = int(query[1])
            r = int(query[2])

            total = fw.range_sum(l, r)
            limit = 30 * (r - l + 1)

            if total > limit:
                out.append("YES")
            else:
                out.append("NO")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The dictionary `value` performs the name-to-alcohol conversion in expected O(1) time. The initial schedule is converted once, before any dynamic operations begin.

The `arr` array stores the current numeric value at every position. This is needed during an update because the Fenwick tree only stores aggregate sums, so we need the old value to calculate the difference that should be propagated.

The Fenwick tree is initialized by adding every array value. This takes O(NlogN) with the straightforward implementation above. An O(N) construction is possible, but it is unnecessary here because N≤2⋅10 5.

For an update at position `x`, the expression `new_value - old_value` can be positive, negative, or zero. A zero difference is harmless and correctly leaves all relevant sums unchanged.

The range query uses `prefix_sum(r) - prefix_sum(l - 1)`. The `l - 1` is what makes the interval inclusive on both sides. Since the input positions are 1-indexed, the Fenwick tree is also deliberately 1-indexed.

Python integers do not overflow, and the largest possible total is only 100⋅200000=20,000,000 anyway. The output is accumulated in a list and written once, which avoids excessive calls to `print`.

## Worked Examples

### Sample 1

The drink values are `vodka = 30`, `pitu = 35`, `beats = 15`, `whisky = 20`, and `cuba = 50`. The initial numeric array is therefore `[30, 35, 15, 20, 30, 50]`.

| Operation | Current relevant array | Range sum | Limit | Output |
| --- | --- | --- | --- | --- |
| `2 3 4` | `[30,35,15,20,30,50]` | 15+20=35 | 30⋅2=60 | `NO` |
| `1 3 cuba` | `[30,35,50,20,30,50]` |  |  |  |
| `2 3 3` | `[30,35,50,20,30,50]` | 50 | 30 | `YES` |
| `1 5 cuba` | `[30,35,50,20,50,50]` |  |  |  |
| `2 1 5` | `[30,35,50,20,50,50]` | 180 | 150 | `YES` |

The first query is safe because 35 is below the 60-liter limit. After position 3 changes from `beats` to `cuba`, its value becomes 50, making the one-hour query exceed the 30-liter limit. The second update changes position 5 from 30 to 50, raising the first five positions to 180, which exceeds 150.

### Constructed Example

Consider this small case:

```
4 2 5
a a b a
a 30
b 60
2 1 4
1 2 b
2 1 2
1 4 b
2 3 4
```

The initial array is `[30,30,60,30]`.

| Operation | Array after operation | Range sum | Limit | Output |
| --- | --- | --- | --- | --- |
| `2 1 4` | `[30,30,60,30]` | 150 | 120 | `YES` |
| `1 2 b` | `[30,60,60,30]` |  |  |  |
| `2 1 2` | `[30,60,60,30]` | 90 | 60 | `YES` |
| `1 4 b` | `[30,60,60,60]` |  |  |  |
| `2 3 4` | `[30,60,60,60]` | 120 | 60 | `YES` |

This trace demonstrates that updates are reflected immediately in subsequent range sums. It also checks the inclusive endpoint handling in the final query, where positions 3 and 4 both contribute.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N+M+Q)logN) | Drink mapping takes O(M), Fenwick initialization takes O(NlogN), and every update or range query takes O(logN). |
| Space | O(N+M) | The drink dictionary uses O(M), while the current array and Fenwick tree use O(N). |

With N,M,Q≤2⋅10 5, the solution performs only a few million logarithmic Fenwick operations instead of potentially tens of billions of interval scans. The memory usage is comfortably below 256 MB.

## Test Cases

The following test harness uses the same `solve()` implementation and temporarily replaces standard input and output. The maximum-size case uses 200000 positions and 200000 queries, which is enough to exercise the asymptotic behavior without embedding an enormous literal string in the editorial.

```python
import sys
import io

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, delta):
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def prefix_sum(self, i):
        result = 0
        while i > 0:
            result += self.bit[i]
            i -= i & -i
        return result

    def range_sum(self, l, r):
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

def solve():
    input = sys.stdin.readline

    n, m, q = map(int, input().split())
    drinks = input().split()

    value = {}
    for _ in range(m):
        name, v = input().split()
        value[name] = int(v)

    arr = [value[name] for name in drinks]

    fw = Fenwick(n)
    for i, v in enumerate(arr, 1):
        fw.add(i, v)

    out = []

    for _ in range(q):
        query = input().split()
        if query[0] == "1":
            x = int(query[1])
            y = query[2]

            new_value = value[y]
            old_value = arr[x - 1]

            fw.add(x, new_value - old_value)
            arr[x - 1] = new_value
        else:
            l = int(query[1])
            r = int(query[2])

            total = fw.range_sum(l, r)
            limit = 30 * (r - l + 1)

            out.append("YES" if total > limit else "NO")

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

sample1 = """\
6 6 5
vodka pitu beats whisky vodka cuba
vodka 30
caipirinha 10
pitu 35
beats 15
whisky 20
cuba 50
2 3 4
1 3 cuba
2 3 3
1 5 cuba
2 1 5
"""

assert run(sample1) == "NO\nYES\nYES", "sample 1"

minimum = """\
1 1 2
a
a 30
2 1 1
1 1 a
"""

assert run(minimum) == "NO", "minimum-size equality case"

boundary = """\
2 2 4
a b
a 30
b 31
2 1 2
2 2 2
1 1 b
2 1 1
"""

assert run(boundary) == "YES\nYES\nYES", "inclusive boundaries and update"

all_equal = """\
5 1 4
a a a a a
a 31
2 1 5
1 3 a
2 3 3
2 2 4
"""

assert run(all_equal) == "YES\nYES\nYES", "all-equal values"

n = 200000
q = 200000
max_input = (
    f"{n} 1 {q}\n"
    + " ".join(["a"] * n)
    + "\n"
    + "a 1\n"
    + "\n".join(["2 1 1"] * q)
    + "\n"
)

assert run(max_input) == ("NO\n" * q).rstrip("\n"), "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `NO`, `YES`, `YES` | The official sequence of queries and updates |
| `minimum` | `NO` | N=1 and exact equality with the safe limit |
| `boundary` | `YES`, `YES`, `YES` | Inclusive endpoints, one-element ranges, and a point update |
| `all_equal` | `YES`, `YES`, `YES` | Repeated identical values and queries over different interval lengths |
| `max_input` | `NO` repeated 200000 times | Large N and Q, stressing the logarithmic implementation |

## Edge Cases

The first edge case is a one-hour interval. For

```
1 1 1
a
a 31
2 1 1
```

the Fenwick tree returns 31 for `[1,1]`. The algorithm computes the limit as 30(1−1+1)=30, then checks 31>30, producing `YES`. The calculation uses the number of hours, not the number of minutes directly, because the conversion to minutes has already been incorporated into the factor 30.

The equality boundary behaves differently:

```
1 1 1
a
a 30
2 1 1
```

The range sum is 30, and the limit is also 30. The comparison is strictly `total > limit`, so the result is `NO`. This matches the rule that an amount not exceeding the limit is safe.

An update can replace a value with a much larger one:

```
2 2 1
a a
a 30
b 100
1 1 b
2 1 1
```

After the update, `arr[0]` becomes 100, and the Fenwick tree receives a difference of 100−30=70 at position 1. The subsequent query returns 100, compares it with 30, and prints `YES`. The old value never remains in any Fenwick prefix.

Inclusive endpoints are tested by

```
2 2 1
a b
a 30
b 31
2 1 2
```

The range `[1,2]` contains both values, giving 61. The threshold is 30⋅2=60, so the result is `YES`. The Fenwick expression `prefix(2) - prefix(0)` includes both positions, which is exactly what the query requires.

A final subtle case is a long interval whose sum is exactly the limit. For example,

```
3 1 1
a a a
a 30
2 1 3
```

gives a total of 90 and a limit of 30⋅3=90. The algorithm prints `NO`, confirming that the strict inequality is applied independently of the interval length.
