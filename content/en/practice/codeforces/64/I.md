---
title: "CF 64I - Sort the Table"
description: "We are given a table where every row contains several string fields, and the first input line tells us the name of each column. Another line describes how the rows should be ordered. Each rule has the form COLUMNNAME ASC or COLUMNNAME DESC."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "sortings"]
categories: ["algorithms"]
codeforces_contest: 64
codeforces_index: "I"
codeforces_contest_name: "Unknown Language Round 1"
rating: 2400
weight: 64
solve_time_s: 110
verified: true
draft: false
---

[CF 64I - Sort the Table](https://codeforces.com/problemset/problem/64/I)

**Rating:** 2400  
**Tags:** *special, sortings  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a table where every row contains several string fields, and the first input line tells us the name of each column. Another line describes how the rows should be ordered. Each rule has the form `COLUMN_NAME ASC` or `COLUMN_NAME DESC`.

The sorting behaves exactly like a database `ORDER BY` clause. The first rule has the highest priority. If two rows are equal according to that rule, we compare them using the second rule, and so on. If all rules consider two rows equal, their original order must stay unchanged. That last requirement means the sort must be stable.

The table size is tiny by competitive programming standards. Both the number of rows and columns are at most 100. Even an `O(n^2)` or `O(n^2 log n)` solution is completely safe here. The expensive part is not the number of rows but handling multiple sort keys with different directions while preserving stability.

The tricky part is not performance, it is correctness. A careless implementation can easily break the ordering rules.

Consider this example:

```
A B
A ASC, B DESC
x 1
x 3
x 2
```

Correct output:

```
x 3
x 2
x 1
```

If we sort only by the first key `A`, the rows stay unchanged because all values are equal. The second key still matters.

Another subtle case is stability:

```
A
A ASC
x
x
x
```

Correct output:

```
x
x
x
```

A stable sort preserves the original order of equal elements. Some custom comparator implementations accidentally reorder equal rows because they return inconsistent results.

Mixed directions are another common source of bugs:

```
A B
A DESC, B ASC
1 z
2 y
2 x
```

Correct output:

```
2 x
2 y
1 z
```

The first key is descending, but the second key is ascending. If we reverse the entire comparison result instead of handling each key independently, the ordering becomes wrong.

Finally, parsing the rules line requires care. The rules are separated by `", "`, not just commas. Splitting incorrectly may leave extra spaces attached to field names or directions.

## Approaches

The most direct solution is to compare rows manually. For every pair of rows, we inspect the rules one by one until we find a field where the rows differ. If the current rule is ascending, we use normal lexicographic order. If it is descending, we reverse the comparison. If all rules match, the rows are considered equal and their original order should stay unchanged.

This approach is conceptually simple because it mirrors the statement exactly. We can plug such a comparator into a sorting algorithm. With at most 100 rows, even a quadratic stable sort like bubble sort would pass comfortably. The worst case is around `100^2 * 100`, which is only one million field comparisons.

Still, Python already gives us a stable sorting algorithm, TimSort. Using it properly makes the implementation cleaner and less error-prone.

The key observation is that stable sorting allows us to process rules from lowest priority to highest priority. Suppose the rules are:

```
A ASC, B DESC, C ASC
```

We first sort by `C`, then by `B`, then by `A`.

Why does this work? After sorting by `C`, rows are correctly ordered by the lowest-priority key. When we later sort by `B`, rows with different `B` values are reordered correctly, while rows with equal `B` keep their previous `C` ordering because Python's sort is stable. Repeating this process eventually produces the exact lexicographic multi-key ordering we want.

This removes the need for a custom comparator entirely. Each sorting pass uses a single field and a simple `reverse=True/False`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force comparator sort | O(r² × k) | O(1) | Accepted |
| Stable multi-pass sort | O(k × r log r) | O(r) | Accepted |

Here, `r` is the number of rows and `k` is the number of sorting rules.

## Algorithm Walkthrough

1. Read the column names and store the position of each column in a dictionary.

This lets us convert a field name like `"AGE"` into its column index in constant time.
2. Read the rules line and split it by `", "`.

Each piece looks like `"FIELD ASC"` or `"FIELD DESC"`.
3. Parse every rule into two values: the column index and whether the order is descending.

For example, `"AGE DESC"` becomes `(2, True)` if `AGE` is the third column.
4. Read all remaining lines as table rows.

Each row is stored as a list of strings.
5. Process the rules in reverse order.

The least important rule must be applied first because later stable sorts preserve earlier tie-breaking decisions.
6. For each rule, sort the rows using the corresponding column as the key.

Use `reverse=True` for descending order and `reverse=False` for ascending order.
7. Print the rows in their final order.

### Why it works

After processing the last rule, rows are correctly ordered according to the lowest-priority condition.

Assume that after processing rules from position `i + 1` onward, rows are already correctly ordered according to all lower-priority rules. When we stably sort by rule `i`, rows with different values for rule `i` move into correct relative order. Rows with equal values for rule `i` keep their previous ordering because the sort is stable. That preserved ordering already satisfies every lower-priority rule.

By induction, after processing all rules, the rows satisfy the complete lexicographic ordering required by the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    columns = input().split()

    pos = {}
    for i, name in enumerate(columns):
        pos[name] = i

    rules_line = input().strip()
    rules_raw = rules_line.split(", ")

    rules = []

    for rule in rules_raw:
        field, order = rule.split()
        rules.append((pos[field], order == "DESC"))

    rows = []

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        rows.append(line.split())

    for col, rev in reversed(rules):
        rows.sort(key=lambda row: row[col], reverse=rev)

    for row in rows:
        print(*row)

solve()
```

The first part builds a mapping from column names to indices. This avoids repeated linear searches whenever a rule references a field.

The rules are stored as pairs `(column_index, is_descending)`. Converting everything into indices early keeps the sorting loop simple.

Reading rows until EOF matches the input format naturally because the number of rows is not given explicitly.

The most important implementation detail is iterating over `reversed(rules)`. Processing them in the original order would destroy previously established higher-priority ordering.

The call:

```
rows.sort(key=lambda row: row[col], reverse=rev)
```

works because Python sorting is stable. Equal elements keep their earlier order automatically.

All comparisons are lexicographic string comparisons, exactly as required by the statement. We never convert values into integers.

## Worked Examples

### Example 1

Input:

```
NAME GROUP AGE
GROUP ASC, AGE DESC
Alex 412 19
Peter 422 19
Sergey 412 18
Andrey 311 18
```

Rules after parsing:

| Rule Priority | Column | Order |
| --- | --- | --- |
| 1 | GROUP | ASC |
| 2 | AGE | DESC |

We process them in reverse order.

#### Sort by AGE DESC

| Row | AGE |
| --- | --- |
| Alex 412 19 | 19 |
| Peter 422 19 | 19 |
| Sergey 412 18 | 18 |
| Andrey 311 18 | 18 |

State after sorting:

| Position | Row |
| --- | --- |
| 1 | Alex 412 19 |
| 2 | Peter 422 19 |
| 3 | Sergey 412 18 |
| 4 | Andrey 311 18 |

#### Sort by GROUP ASC

| Row | GROUP |
| --- | --- |
| Alex 412 19 | 412 |
| Peter 422 19 | 422 |
| Sergey 412 18 | 412 |
| Andrey 311 18 | 311 |

Final order:

| Position | Row |
| --- | --- |
| 1 | Andrey 311 18 |
| 2 | Alex 412 19 |
| 3 | Sergey 412 18 |
| 4 | Peter 422 19 |

This trace shows why stability matters. Both rows with group `412` remain ordered by descending age because that ordering was established earlier.

### Example 2

Input:

```
A B
A DESC, B ASC
1 z
2 y
2 x
```

Rules after parsing:

| Rule Priority | Column | Order |
| --- | --- | --- |
| 1 | A | DESC |
| 2 | B | ASC |

#### Sort by B ASC

| Position | Row |
| --- | --- |
| 1 | 2 x |
| 2 | 2 y |
| 3 | 1 z |

#### Sort by A DESC

| Position | Row |
| --- | --- |
| 1 | 2 x |
| 2 | 2 y |
| 3 | 1 z |

The rows with `A = 2` preserve their earlier `B ASC` ordering because the second sort is stable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k × r log r) | We perform one sort per rule |
| Space | O(r) | Python sorting may use auxiliary memory |

Here, `r` is the number of rows and `k` is the number of rules.

With at most 100 rows and 100 columns, this runs instantly. Even several full sorting passes are negligible within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    columns = input().split()

    pos = {}
    for i, name in enumerate(columns):
        pos[name] = i

    rules_line = input().strip()
    rules_raw = rules_line.split(", ")

    rules = []

    for rule in rules_raw:
        field, order = rule.split()
        rules.append((pos[field], order == "DESC"))

    rows = []

    for line in sys.stdin:
        line = line.strip()

        if not line:
            continue

        rows.append(line.split())

    for col, rev in reversed(rules):
        rows.sort(key=lambda row: row[col], reverse=rev)

    out = []

    for row in rows:
        out.append(" ".join(row))

    print("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run(
"""NAME GROUP AGE
GROUP ASC, AGE DESC
Alex 412 19
Peter 422 19
Sergey 412 18
Andrey 311 18
"""
) == (
"""Andrey 311 18
Alex 412 19
Sergey 412 18
Peter 422 19
"""
), "sample 1"

# minimum size
assert run(
"""A
A ASC
x
"""
) == (
"""x
"""
), "single row"

# stability check
assert run(
"""A B
A ASC
x 1
x 2
x 3
"""
) == (
"""x 1
x 2
x 3
"""
), "stable ordering"

# mixed ascending and descending
assert run(
"""A B
A DESC, B ASC
1 z
2 y
2 x
"""
) == (
"""2 x
2 y
1 z
"""
), "mixed directions"

# lexicographic comparison
assert run(
"""A
A ASC
10
2
9
"""
) == (
"""10
2
9
"""
), "strings not integers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single row table | Same single row | Minimum input size |
| All equal primary keys | Original order preserved | Stable sorting |
| Mixed ASC and DESC | Correct layered ordering | Direction handling |
| Values `10`, `2`, `9` | Lexicographic order | Strings are not integers |

## Edge Cases

Consider rows equal under every rule:

```
A B
A ASC, B DESC
x 1
x 1
x 1
```

The algorithm first sorts by `B DESC`, which changes nothing because all values are equal. It then sorts by `A ASC`, which also changes nothing. Since Python sorting is stable, the original order is preserved exactly.

Now consider conflicting directions:

```
A B
A DESC, B ASC
2 z
2 x
1 y
```

The algorithm first sorts by `B ASC`:

```
2 x
1 y
2 z
```

Then it sorts by `A DESC`:

```
2 x
2 z
1 y
```

Among rows where `A = 2`, the previous `B ASC` ordering survives because the second sort is stable.

Finally, consider lexicographic behavior:

```
A
A ASC
2
10
9
```

String comparison gives:

```
10
2
9
```

because `"10"` comes before `"2"` lexicographically. The algorithm handles this automatically since it never converts strings into numbers.
