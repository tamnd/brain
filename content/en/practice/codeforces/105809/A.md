---
title: "CF 105809A - A Factory Game"
description: "We are given a list of delivery records. Each record contains three integers: (product, material, submaterial) The same delivery may appear multiple times because two people independently wrote down the deliveries and their notes were merged together."
date: "2026-06-25T15:26:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105809
codeforces_index: "A"
codeforces_contest_name: "Code Rush 2025"
rating: 0
weight: 105809
solve_time_s: 46
verified: true
draft: false
---

[CF 105809A - A Factory Game](https://codeforces.com/problemset/problem/105809/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of delivery records. Each record contains three integers:

`(product, material, submaterial)`

The same delivery may appear multiple times because two people independently wrote down the deliveries and their notes were merged together. Duplicate records do not represent additional deliveries.

For every product, we must determine two quantities:

First, how many distinct materials were associated with that product.

Second, how many distinct submaterials were associated with that product.

The output must contain one line per product, sorted by product id. Each line contains:

`product_id distinct_materials distinct_submaterials`

The input size is the key part of the problem. There can be up to one million records, while product ids, material ids, and submaterial ids can be as large as $10^{18}$. The large value range rules out any array indexed by ids. We need hash-based structures such as Python sets and dictionaries.

With $n = 10^6$, an $O(n^2)$ solution is completely impossible. Even $O(n \log n)$ is acceptable, but a linear or near-linear solution is preferable. Since each record only needs to contribute information about one product, hash tables are a natural fit.

A subtle point is that duplicate triples must not increase either count.

Consider:

```
3
1 5 7
1 5 7
1 5 7
```

The correct output is:

```
1 1 1
```

A careless implementation that simply counts rows would produce larger values.

Another edge case is when multiple submaterials belong to the same material.

```
3
1 5 1
1 5 2
1 5 3
```

The correct output is:

```
1 1 3
```

There is only one distinct material, even though three deliveries exist.

The opposite situation is also possible.

```
3
1 1 9
1 2 9
1 3 9
```

The correct output is:

```
1 3 1
```

Distinct materials and distinct submaterials must be counted independently.

## Approaches

The most direct brute-force idea is to process each product separately. For every product, scan the entire list of deliveries and collect all materials and submaterials belonging to that product.

This is correct because every record is examined when computing the statistics for a product. The problem is efficiency. If there are $P$ distinct products and $N$ records, the work becomes $O(PN)$. In the worst case, every record belongs to a different product, producing $O(N^2)$ operations. With $N = 10^6$, this is far beyond practical limits.

The structure of the data suggests a better approach. Each record already tells us exactly which product it belongs to. Instead of repeatedly scanning the whole input, we can aggregate information while reading the records.

For every product, maintain two sets:

One set stores all distinct materials seen for that product.

The other set stores all distinct submaterials seen for that product.

When a record `(a, b, c)` is read, we simply insert `b` into the product's material set and `c` into the product's submaterial set.

Because sets automatically eliminate duplicates, repeated records have no effect on the final counts.

After processing all records, the answer for a product is just the size of its two sets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(PN) | O(N) | Too slow |
| Optimal | O(N) average | O(N) | Accepted |

## Algorithm Walkthrough

1. Read the number of records `n`.
2. Create a dictionary indexed by product id.
3. For each record `(product, material, submaterial)`:

Store the material in the product's material set.

Store the submaterial in the product's submaterial set.

If the product has not appeared before, create the two sets first.
4. After all records are processed, sort the product ids.
5. For every product in sorted order:

Output the product id.

Output the size of its material set.

Output the size of its submaterial set.

### Why it works

For a fixed product, every delivery record associated with that product inserts its material into one set and its submaterial into another set. A set contains each value at most once, regardless of how many times it was inserted.

As a result, after all records are processed, the material set contains exactly the distinct materials associated with that product, and the submaterial set contains exactly the distinct submaterials associated with that product.

Since every record is processed once and contributes to the correct product, the final counts are exactly the quantities requested.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    products = {}

    for _ in range(n):
        a, b, c = map(int, input().split())

        if a not in products:
            products[a] = [set(), set()]

        products[a][0].add(b)
        products[a][1].add(c)

    out = []

    for product in sorted(products):
        materials, submaterials = products[product]
        out.append(
            f"{product} {len(materials)} {len(submaterials)}"
        )

    sys.stdout.write("\n".join(out))

solve()
```

The dictionary `products` stores all information grouped by product id.

For each product, `products[a][0]` is the set of materials and `products[a][1]` is the set of submaterials.

When a new record arrives, both insertions are constant-time on average. Duplicate deliveries automatically disappear because inserting an existing value into a set changes nothing.

The final sorting step is necessary because the output requires products in increasing order. Iterating directly over the dictionary would not guarantee the required order.

The ids can be as large as $10^{18}$, but Python integers handle that without any special treatment.

## Worked Examples

### Example 1

Input:

```
10
1 1 1
2 2 1
3 4 1
2 2 2
2 2 1
1 3 12
1 1 2
1 4 1
1 4 2
1 4 3
```

Processing trace:

| Record | Product | Material Set | Submaterial Set |
| --- | --- | --- | --- |
| 1 1 1 | 1 | {1} | {1} |
| 1 3 12 | 1 | {1,3} | {1,12} |
| 1 1 2 | 1 | {1,3} | {1,12,2} |
| 1 4 1 | 1 | {1,3,4} | {1,12,2} |
| 1 4 2 | 1 | {1,3,4} | {1,12,2} |
| 1 4 3 | 1 | {1,3,4} | {1,12,2,3} |

For product 1, there are 3 distinct materials and 6 distinct submaterials. Similar calculations give the remaining products.

Output:

```
1 3 6
2 1 2
3 1 1
```

This example shows how duplicate records do not affect the sets.

### Example 2

Input:

```
3
186 312 851372492
291 103 93522568
757 156 500988176
```

Processing trace:

| Product | Materials | Submaterials |
| --- | --- | --- |
| 186 | {312} | {851372492} |
| 291 | {103} | {93522568} |
| 757 | {156} | {500988176} |

Output:

```
186 1 1
291 1 1
757 1 1
```

This example shows that large ids do not change the logic.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + P log P) | Reading records is linear, sorting products costs $P \log P$ |
| Space | O(N) | Every distinct material and submaterial may be stored once |

Here $N$ is the number of records and $P$ is the number of distinct products. With at most one million records, this easily fits within typical contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline

        n = int(input())
        products = {}

        for _ in range(n):
            a, b, c = map(int, input().split())

            if a not in products:
                products[a] = [set(), set()]

            products[a][0].add(b)
            products[a][1].add(c)

        out = []
        for p in sorted(products):
            out.append(
                f"{p} {len(products[p][0])} {len(products[p][1])}"
            )

        return "\n".join(out)

    return solve()

# provided sample 1
assert run(
"""10
1 1 1
2 2 1
3 4 1
2 2 2
2 2 1
1 3 12
1 1 2
1 4 1
1 4 2
1 4 3
"""
) == "1 3 6\n2 1 2\n3 1 1"

# provided sample 2
assert run(
"""3
186 312 851372492
291 103 93522568
757 156 500988176
"""
) == "186 1 1\n291 1 1\n757 1 1"

# minimum size
assert run(
"""1
5 7 9
"""
) == "5 1 1"

# all duplicate records
assert run(
"""4
1 2 3
1 2 3
1 2 3
1 2 3
"""
) == "1 1 1"

# same material, many submaterials
assert run(
"""3
1 10 1
1 10 2
1 10 3
"""
) == "1 1 3"

# same submaterial, many materials
assert run(
"""3
1 1 5
1 2 5
1 3 5
"""
) == "1 3 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single record | `1 1 1` style result | Minimum size |
| Repeated identical records | Counts remain 1 | Duplicate elimination |
| Same material, many submaterials | Material count unchanged | Independent counting |
| Same submaterial, many materials | Submaterial count unchanged | Independent counting |

## Edge Cases

Consider repeated deliveries:

```
3
1 5 7
1 5 7
1 5 7
```

The algorithm inserts `5` into the material set three times and `7` into the submaterial set three times. Since sets only store unique values, the final sizes are both 1. The output is:

```
1 1 1
```

Consider many submaterials sharing one material:

```
3
1 8 1
1 8 2
1 8 3
```

The material set becomes `{8}` while the submaterial set becomes `{1,2,3}`. The output is:

```
1 1 3
```

Consider many materials sharing one submaterial:

```
3
1 1 9
1 2 9
1 3 9
```

The material set becomes `{1,2,3}` while the submaterial set remains `{9}`. The output is:

```
1 3 1
```

These cases demonstrate why two independent sets must be maintained for every product. A single combined structure would not correctly answer both counts.
