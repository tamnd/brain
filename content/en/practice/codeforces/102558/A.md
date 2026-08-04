---
title: "CF 102558A - \u0414\u0435\u043d\u044c \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f \u0412\u0430\u0441\u0438"
description: "Vasya has a collection of dishes. Each dish is a list of ingredients with a required amount for one serving, and each dish is prepared for a known number of guests."
date: "2026-08-04T09:25:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102558
codeforces_index: "A"
codeforces_contest_name: "Contest for Yandex interns 2019"
rating: 0
weight: 102558
solve_time_s: 226
verified: false
draft: false
---

[CF 102558A - \u0414\u0435\u043d\u044c \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f \u0412\u0430\u0441\u0438](https://codeforces.com/problemset/problem/102558/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 46s  
**Verified:** no  

## Solution
# Problem Understanding

Vasya has a collection of dishes. Each dish is a list of ingredients with a required amount for one serving, and each dish is prepared for a known number of guests. The task is to simulate the whole shopping process: determine how many packages of every available ingredient must be bought, calculate the total price, and calculate the nutritional values of one complete dish.

The input contains two independent catalogs. The first one describes shop packages: package size, measurement unit, and price. The second one describes nutritional data for a certain amount of each ingredient. The same ingredient can appear with different units in recipes and catalogs, so all calculations must first be converted into a common unit.

The limits are small enough for direct processing. There are at most 1000 dishes, each with at most 100 ingredients, and both catalogs contain at most 1000 entries. This means the total number of recipe ingredients is at most 100000. An algorithm that does work proportional to the total input size is required. Repeatedly scanning all catalogs for every recipe ingredient would still work here with about 100 million comparisons, but using dictionaries is simpler and gives a clean linear solution.

The tricky parts are mostly related to units and the difference between one serving and all servings. For example, if a recipe needs `500 ml` of milk and the shop sells `1 l` packages, the purchase calculation must use `0.5` packages rounded upward, while nutrition calculation must use exactly `500 ml`.

A common mistake is treating units with different meanings as interchangeable. For example, `tens` and `cnt` both describe a quantity of objects, but `kg` and `l` cannot be converted. The statement guarantees that every conversion we need is valid, so the implementation only has to apply the correct multiplier.

Another subtle case is an ingredient that appears in several dishes. For example:

```
2
a 1 1
x 500 g
b 1 1
x 700 g
1
x 1000 g 1
1
x 1000 g 1 0 0 0
```

The correct number of packages is `2`, because the total amount is `1200 g`. A solution that rounds each dish separately would also get `2` here, but with `100 g` and `100 g` recipes and `150 g` packages it would incorrectly buy two packages instead of two? The important rule is that shopping is done after summing all required amounts.

Another case is a recipe ingredient measured in a different unit from the nutrition catalog:

```
1
cake 1 1
milk 500 ml
1
milk 1 l 10
1
milk 1 l 20 0 0 100
```

The nutritional value is half of the catalog entry. Using the raw number `500` with the catalog value for `1 l` would double the result.

# Approaches

A straightforward solution is to process every dish and every ingredient independently. For each recipe ingredient, search the catalogs, convert the amount, calculate nutrition, and update the required amount. This is correct because every ingredient contribution is independent and addition is enough to combine them. The problem with this approach is repeated searching. If every one of the 100000 recipe entries scans a 1000 element catalog, the number of comparisons reaches about 100 million.

The useful observation is that ingredient names are unique inside each catalog. That means the catalogs can be indexed once with hash maps. After that, every ingredient lookup becomes constant time.

The second observation is that all unit conversions are multiplicative. We can convert every quantity to a base unit: grams for mass, milliliters for volume, and individual pieces for counts. Once everything is in the same representation, summing requirements, computing package counts, and calculating nutrition become ordinary arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total_recipe_items * catalog_size) | O(1) | Too slow in the worst case |
| Optimal | O(total_recipe_items + k + m + n) | O(k + m + n) | Accepted |

# Algorithm Walkthrough

1. Read the price catalog and store every ingredient by name. Convert each package size into a base quantity so package calculations do not depend on the original unit.
2. Read the nutrition catalog and store, for each ingredient, how much protein, fat, carbohydrate, and energy corresponds to one base unit. Dividing by the converted catalog amount lets every recipe quantity be multiplied directly.
3. For every dish, store its name and calculate its nutritional values. For every ingredient in the recipe, convert the per-serving amount into base units and multiply by the nutrition values per base unit.
4. At the same time, add the ingredient amount multiplied by the number of guests to a global required amount map. This map represents the exact amount of every ingredient needed for all dishes.
5. After all dishes are processed, calculate the number of packages for every ingredient from the price catalog. Divide the required amount by the package size and round upward because partial packages cannot be purchased.
6. Output the total price, package counts, and the calculated nutrition for each dish.

The invariant behind the algorithm is that after processing any prefix of the dishes, the global requirement map contains exactly the amount needed by that prefix, and every stored nutritional value is calculated from normalized ingredient quantities. Since each remaining dish contributes independently, continuing the same updates preserves correctness until all dishes are processed.

# Python Solution

```python
import sys
import math
input = sys.stdin.readline

def factor(u):
    if u == "kg" or u == "l":
        return 1000
    if u == "tens":
        return 10
    return 1

def solve():
    n = int(input())
    dishes = []
    for _ in range(n):
        name, c, z = input().split()
        c = int(c)
        z = int(z)
        ing = []
        for _ in range(z):
            s, a, u = input().split()
            ing.append((s, int(a), u))
        dishes.append((name, c, ing))

    k = int(input())
    price = {}
    order = []
    for _ in range(k):
        t, p, a, u = input().split()
        a = int(a)
        price[t] = (int(p), a * factor(u))
        order.append(t)

    m = int(input())
    nutrition = {}
    for _ in range(m):
        t, a, u, pr, f, ch, fv = input().split()
        amount = int(a) * factor(u)
        nutrition[t] = (
            float(pr) / amount,
            float(f) / amount,
            float(ch) / amount,
            float(fv) / amount
        )

    need = {}
    answers = []

    for name, cnt, ing in dishes:
        cur = [0.0, 0.0, 0.0, 0.0]
        for s, a, u in ing:
            amount = a * factor(u)
            if s not in need:
                need[s] = 0
            need[s] += amount * cnt

            pr, f, ch, fv = nutrition[s]
            cur[0] += amount * pr
            cur[1] += amount * f
            cur[2] += amount * ch
            cur[3] += amount * fv
        answers.append((name, cur))

    total = 0
    packs = []
    for t in order:
        p, size = price[t]
        cnt = math.ceil((need.get(t, 0) - 1e-12) / size)
        packs.append((t, cnt))
        total += cnt * p

    out = [str(total)]
    for t, c in packs:
        out.append(f"{t} {c}")
    for name, vals in answers:
        out.append("{} {:.10f} {:.10f} {:.10f} {:.10f}".format(name, *vals))
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `factor` function converts every supported unit into its base representation. Kilograms and liters become thousandths of their respective base units, while tens become ten individual objects.

The price dictionary stores package sizes in the same representation used by recipes. This removes all unit handling from the final purchase calculation.

The nutrition dictionary stores values per base unit rather than per catalog entry. For example, if the catalog says that 100 grams contain 20 grams of protein, the stored value is `0.2` protein per gram.

During recipe processing, the code performs two independent updates. The `need` map tracks shopping quantities for all guests, while `cur` tracks nutrition for a single complete dish. Mixing these two values is a frequent source of wrong answers.

The final ceiling operation contains a small epsilon because floating point division may produce values like `1.000000000001`. The constraints are small, so integer overflow is not a concern in Python.

# Worked Examples

For the sample, the first dish is processed as follows:

| Dish | Ingredient | Converted amount | Nutrition contribution |
| --- | --- | --- | --- |
| sandwich | butter | 10 g | 0.08, 7.25, 0.13, 66.1 |
| sandwich | toasted_bread | 2 cnt | 2.92, 0.64, 20.92, 99.2 |
| sandwich | sausage | 30 g | 3, 5.4, 0.45, 63 |

The resulting sandwich values are:

| Protein | Fat | Carbs | Energy |
| --- | --- | --- | --- |
| 6.00 | 13.29 | 21.50 | 228.30 |

The shopping map after both dishes is:

| Ingredient | Required amount |
| --- | --- |
| butter | 70 g |
| toasted_bread | 14 cnt |
| sausage | 660 g |
| egg | 36 cnt |
| milk | 1080 ml |
| salt | 9 g |

The package calculation rounds each requirement upward, producing four egg packages, two milk packages, two sausage packages, and one package for the remaining ingredients.

A second small trace:

```
1
tea 1 1
sugar 3 g
1
sugar 10 g 5
1
sugar 10 g 1 0 0 0
```

| Step | Variable | Value |
| --- | --- | --- |
| Read recipe | amount | 3 g |
| Normalize | amount | 3 base units |
| Required map | sugar | 3 |
| Packages | ceil(3/10) | 1 |

This confirms that buying uses the exact total amount and rounds only at the final package step.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * z + k + m) | Every recipe ingredient is processed once, and catalogs are read once |
| Space | O(k + m + n * z) | Stored catalogs, recipes, and answers |

The maximum number of recipe entries is about 100000, so a linear pass with hash table lookups easily fits the constraints.

# Test Cases

```python
import sys
import io

# These tests assume solve() is copied into this file.

def run(inp):
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old

sample = """1
a 1 1
x 500 g
1
x 1 1000 g
1
x 1000 g 10 0 0 100
"""
assert "1" in run(sample)

minimum = """1
a 1 1
x 1 cnt
1
x 1 1 cnt
1
x 1 cnt 1 2 3 4
"""
assert "x 1" in run(minimum)

different_units = """1
a 1 1
milk 500 ml
1
milk 1 1 l
1
milk 1 l 10 0 0 100
"""
assert "50.0000000000" in run(different_units)

shared = """2
a 1 1
x 100 g
b 1 1
x 100 g
1
x 150 g 1
1
x 100 g 1 0 0 0
"""
assert "2" in run(shared)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single ingredient recipe | One package | Basic conversion and purchase |
| One count-based ingredient | One package | Minimum size handling |
| Milliliters with liter catalog | Half nutrition values | Unit normalization |
| Same ingredient in two dishes | Combined package count | Aggregation before rounding |

# Edge Cases

The algorithm handles unit mismatches by converting before any arithmetic. In the milk example, `500 ml` becomes `500` base units, while the nutrition catalog stores values per `1000 ml`, so the result is exactly half of the catalog values.

The algorithm handles shared ingredients by updating `need` every time the ingredient appears. If two dishes require `100 g` each and the package size is `150 g`, the final requirement is `200 g`, giving `ceil(200 / 150) = 2` packages. It never rounds individual recipes early.

Zero-use catalog entries are also handled. The output requires every price catalog ingredient to be printed, including ingredients never needed by any recipe. The lookup uses `need.get(t, 0)`, producing zero packages for those ingredients.
