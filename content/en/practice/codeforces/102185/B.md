---
title: "CF 102185B - \u0424\u0438\u043a\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u0446\u0435\u043d\u0430"
description: "The store has one fixed price P. For each product, we know the required number of units A and the market price of one unit S. The store behaves differently depending on whether one unit is already worth at least P. If S = P, individual units are available, each costing exactly P."
date: "2026-08-19T06:24:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102185
codeforces_index: "B"
codeforces_contest_name: "Southern Russia Open Championship \u2013 ContestSFedU 2019, Team Final."
rating: 0
weight: 102185
solve_time_s: 78
verified: true
draft: false
---

[CF 102185B - \u0424\u0438\u043a\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0430\u044f \u0446\u0435\u043d\u0430](https://codeforces.com/problemset/problem/102185/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The store has one fixed price `P`. For each product, we know the required number of units `A` and the market price of one unit `S`.

The store behaves differently depending on whether one unit is already worth at least `P`. If `S >= P`, individual units are available, each costing exactly `P`. To obtain at least `A` units, we simply buy `A` units, so the cost is `A * P`.

If `S < P`, individual units cannot be bought. Instead, one package costs `P` and contains

`ceil(P / S)`

units. We may buy any number of complete packages, so the task becomes finding the smallest number of packages whose total number of units is at least `A`.

For example, with `P = 100` and `S = 51`, one package contains `ceil(100 / 51) = 2` units. To obtain at least `6` units, we need `ceil(6 / 2) = 3` packages, costing `300`.

There are at most `1000` products, and every `A` and `S` is at most `1000`. These bounds are small enough that even a simulation requiring up to `1000` iterations per product would perform at most about `10^6` iterations. Such a solution would pass comfortably. However, the structure of the purchase rule lets us solve every product in constant time, giving an especially simple `O(N)` solution.

The main edge cases come from the boundaries in the two pricing rules. When `S = P`, the product is sold individually, so for input

```
1 1004 100
```

the answer is `400`. A careless implementation using the package formula might compute a package size of `1` and still happen to get the same result, but treating `S = P` as the package case can obscure the actual rule and cause errors if the implementation assumes packages contain more than one unit.

The second edge case is when `P` is not divisible by `S`. For

```
1 1006 30
```

one package contains `ceil(100 / 30) = 4` units. Two packages give `8` units, so the answer is `200`. Using integer division `100 // 30 = 3` would incorrectly conclude that a package contains only three units and produce `200` here by coincidence for six required units, but for

```
1 1007 30
```

the correct answer is still `200`, whereas using the wrong package size of three would produce `300`.

A third boundary occurs when the required quantity is already smaller than one package. For

```
1 1001 40
```

one package contains `ceil(100 / 40) = 3` units, so buying one package is enough and the answer is `100`. Multiplying the required quantity by the fixed price would incorrectly give `40` in terms of package count, or `100` only if the distinction is handled correctly.

## Approaches

A direct simulation can solve the problem by repeatedly adding one package until the accumulated number of units reaches `A`. For a product with `S < P`, we first calculate the package size `K = ceil(P / S)`, then repeatedly add `K` until we have enough units. In the worst case, `K = 1`, so this loop performs at most `A <= 1000` iterations for one product. With `N <= 1000`, that is at most `10^6` iterations in total. Consequently, this brute-force simulation is actually fast enough for the given constraints.

The observation that removes the loop is that every package has exactly the same size and price. If each package contributes `K` units, then after buying `x` packages we have exactly `xK` units. We need the smallest integer `x` satisfying `xK >= A`, which is precisely `ceil(A / K)`. Thus the entire simulation can be replaced by one ceiling division.

The two cases can be combined into a very small calculation. If `S >= P`, one purchase gives one unit, so the number of purchases is `A`. Otherwise, one purchase gives `K = ceil(P / S)` units, so the number of purchases is `ceil(A / K)`. Every purchase costs `P`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | `O(sum A_i)`, at most `10^6` iterations | `O(1)` | Accepted |
| Optimal ceiling division | `O(N)` | `O(1)` | Accepted |

The optimal approach is preferable because it directly expresses the mathematical condition instead of simulating purchases. It is also easier to prove correct and has no loop whose iteration count depends on the requested quantity.

## Algorithm Walkthrough

1. Read `N` and the fixed price `P`. Each of the next `N` lines describes one independent product, so products can be processed separately.
2. For a product, read the required quantity `A` and the market price `S`.
3. If `S >= P`, set the number of purchases to `A`. The store sells individual units in this case, and each unit costs `P`.
4. Otherwise, calculate the number of units in one package as `K = ceil(P / S)`. Since all values are integers, ceiling division can be written as `(P + S - 1) // S`.
5. Calculate the required number of packages as `ceil(A / K)`, again using integer arithmetic as `(A + K - 1) // K`.
6. Multiply the number of purchases by `P` and output that value.
7. Repeat the calculation independently for all products and print the resulting costs.

### Why it works

For `S >= P`, the store sells exactly one unit for each payment of `P`, so purchasing `A` units requires exactly `A` payments.

For `S < P`, every package contains exactly `K = ceil(P / S)` units. After purchasing `x` packages, we have `xK` units. The algorithm chooses the smallest integer `x` for which `xK >= A`, namely `ceil(A / K)`. Thus it buys enough units, while one fewer package would provide fewer than `A` units. Since every package has the same price `P`, this minimum number of packages also gives the minimum possible cost.

## Python Solution

```python
Pythonimport sysinput = sys.stdin.readline

def solve():    n, p = map(int, input().split())    ans = []
    for _ in range(n):        a, s = map(int, input().split())
        if s >= p:            purchases = a        else:            package_size = (p + s - 1) // s            purchases = (a + package_size - 1) // package_size
        ans.append(purchases * p)
    print(*ans)

if __name__ == "__main__":    solve()
```

The program first reads the number of products and the common fixed price. The answer is accumulated in a list so that all costs can be printed on one line at the end.

The condition `s >= p` follows the statement's boundary exactly. Equality belongs to the individual-unit case, although the formula would also produce a package size of one when `s == p`.

For the package case, `(p + s - 1) // s` performs integer ceiling division. Writing `p // s` would round downward and could underestimate the number of units in a package.

The second ceiling division computes how many packages are necessary to reach at least `a` units. The multiplication by `p` is performed only after the number of required purchases has been determined.

Python integers have arbitrary precision, so there is no integer-overflow concern. With the given constraints, the largest possible answer is also very small: at most `1000 * 1000 = 10^6` for individually sold units.

## Worked Examples

The provided sample is

```
5 1001 1016 5111 1012 94 100
```

The processing can be traced as follows.

| `A` | `S` | Case | Package size `K` | Purchases | Cost |
| --- | --- | --- | --- | --- | --- |
| 1 | 101 | Individual | 1 | 1 | 100 |
| 6 | 51 | Packages | 2 | 3 | 300 |
| 11 | 10 | Packages | 10 | 2 | 200 |
| 12 | 9 | Packages | 12 | 1 | 100 |
| 4 | 100 | Individual | 1 | 4 | 400 |

For the second product, `ceil(100 / 51) = 2`, so three packages provide six units exactly. For the third product, each package contains ten units, so two packages provide twenty units, which is enough for the required eleven. The resulting output is

```
100 300 200 100 400
```

A second example exercises several boundaries:

```
4 1001 407 3010 1001000 1
```

| `A` | `S` | Case | Package size `K` | Purchases | Cost |
| --- | --- | --- | --- | --- | --- |
| 1 | 40 | Packages | 3 | 1 | 100 |
| 7 | 30 | Packages | 4 | 2 | 200 |
| 10 | 100 | Individual | 1 | 10 | 1000 |
| 1000 | 1 | Packages | 100 | 10 | 1000 |

The first product demonstrates that needing only one unit still requires an entire package. The second demonstrates ceiling division when `P` is not divisible by `S`. The third checks the exact `S = P` boundary. The last shows that even a large required quantity is handled by constant-time arithmetic rather than a purchase simulation.

The output is

```
100 200 1000 1000
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N)` | Every product requires a constant number of arithmetic operations. |
| Space | `O(N)` | The output list stores one answer per product. |

With at most `1000` products, the algorithm performs only a few thousand arithmetic operations. It is far below the available time and memory limits.

The output list could also be avoided by printing each answer immediately, reducing auxiliary space to `O(1)`. Keeping the answers in a list makes it straightforward to produce the required space-separated output.

## Test Cases

```python
Python# helper: run solution on input string, return output stringimport sysimport io

def solve():    input = sys.stdin.readline    n, p = map(int, input().split())    ans = []
    for _ in range(n):        a, s = map(int, input().split())
        if s >= p:            purchases = a        else:            package_size = (p + s - 1) // s            purchases = (a + package_size - 1) // package_size
        ans.append(purchases * p)
    print(*ans)

def run(inp: str) -> str:    old_stdin = sys.stdin    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)    sys.stdout = io.StringIO()
    try:        solve()        return sys.stdout.getvalue().strip()    finally:        sys.stdin = old_stdin        sys.stdout = old_stdout

# Provided sampleassert run(    """5 1001 1016 5111 1012 94 100""") == "100 300 200 100 400", "sample 1"
# Minimum-size inputassert run(    """1 11 1""") == "1", "minimum values"
# Exact boundary S = Passert run(    """3 1001 1005 1001000 100""") == "100 500 100000", "S = P boundary"
# Ceiling division boundariesassert run(    """4 1001 403 404 407 30""") == "100 100 200 200", "ceiling division"
# All values equalassert run(    """4 5050 5050 5050 5050 50""") == "2500 2500 2500 2500", "all equal"
# Maximum-size valuesassert run(    """3 10001000 11000 9991000 1000""") == "10000 2000 1000000", "maximum values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 1` | `1` | Minimum allowed values |
| `1 100 / 1 100` and related cases | `100 500 100000` | Exact `S = P` boundary |
| `1 40`, `3 40`, `4 40`, `7 30` | `100 100 200 200` | Ceiling division and exact package boundaries |
| Four products with `A = S = 50` | `2500 2500 2500 2500` | Repeated equal values and individual-unit pricing |
| `P = 1000`, maximum `A` and extreme `S` values | `10000 2000 1000000` | Maximum constraints and large arithmetic |

## Edge Cases

When `S = P`, the store sells individual units. For

```
1 1004 100
```

the condition `S >= P` is true, so the algorithm sets `purchases = 4` and outputs `400`. There is no need to create a package in this case.

When `S` does not divide `P`, ceiling division is essential. For

```
1 1007 30
```

the package size is `(100 + 30 - 1) // 30 = 4`. Two packages contain eight units, enough for the required seven, so the answer is `200`. A floor division would incorrectly calculate the package size as three.

When `A` is smaller than the package size, one whole package is still required. For

```
1 1001 40
```

the package contains three units, but only one unit is requested. Since packages cannot be split, `ceil(1 / 3) = 1`, giving a cost of `100`.

When the requested amount is exactly divisible by the package size, the second ceiling division must not add an unnecessary package. For

```
1 1006 50
```

one package contains `2` units, and `6 / 2 = 3` exactly. The algorithm computes `(6 + 2 - 1) // 2 = 3`, so the answer is `300`, not `400`.

The final boundary is `S > P`. For

```
1 1001 101
```

the product is sold as one individual unit for `100`, even though its market price is higher. The algorithm follows the `S >= P` branch and outputs `100`.
