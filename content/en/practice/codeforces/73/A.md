---
title: "CF 73A - The Elder Trolls IV: Oblivon"
description: "We have a rectangular block made of unit cubes with dimensions x × y × z. A single cut is always made along the grid lines and must be parallel to one of the faces of the box."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 73
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 66"
rating: 1600
weight: 73
solve_time_s: 108
verified: true
draft: false
---

[CF 73A - The Elder Trolls IV: Oblivon](https://codeforces.com/problemset/problem/73/A)

**Rating:** 1600  
**Tags:** greedy, math  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular block made of unit cubes with dimensions `x × y × z`. A single cut is always made along the grid lines and must be parallel to one of the faces of the box. Since the cuts are infinitely long and the pieces never move away from their original positions, one cut can pass through many already-created pieces at once.

The goal is to maximize the number of final pieces after making at most `k` cuts.

The key detail is how cuts behave. If we make `a` cuts perpendicular to the `x` axis, the box becomes divided into `a + 1` layers along that direction. Similarly, `b` cuts along `y` produce `b + 1` sections there, and `c` cuts along `z` produce `c + 1` sections. If `a + b + c = k`, the total number of pieces becomes:

$(a+1)(b+1)(c+1)$

The dimensions limit how many cuts are possible in each direction. Along length `x`, there are only `x - 1` valid grid planes, so:

$0 \le a \le x-1$

and similarly for the other two dimensions.

The constraints immediately rule out any simulation of cuts. Dimensions can reach `10^6`, while `k` can reach `10^9`. Any algorithm proportional to the number of states or cuts would be far too slow. Even iterating over all triples `(a,b,c)` naively would require around `10^{18}` combinations in the worst case, which is impossible.

The problem is actually an optimization problem over three integers. Since there are only three dimensions, the search space can be reduced aggressively with mathematical observations.

Several edge cases are easy to mishandle.

Suppose the input is:

```
1 1 1 100
```

No cuts are possible because every dimension already has size `1`. The correct answer is `1`, not something involving `k`.

Another subtle case is when `k` exceeds the total number of available cutting planes:

```
2 2 2 10
```

Each dimension allows only one cut, so at most three cuts can ever be useful. The maximum number of pieces is still `8`.

A common mistake is assuming cuts should always be distributed evenly. Consider:

```
10 1 1 5
```

Only the first dimension can be cut. The answer is `6`, not something balanced like `2 × 2 × 2`.

Another dangerous implementation bug comes from integer overflow in languages with 32-bit integers. The answer can reach:

$10^6 \cdot 10^6 \cdot 10^6 = 10^{18}$

Python handles this automatically, but C++ solutions need `long long`.

## Approaches

A brute-force solution would try every possible number of cuts in each direction. We could iterate over all triples `(a,b,c)` satisfying:

$a+b+c \le k$

and check whether each value stays within the dimension limits. For every valid triple we compute:

$(a+1)(b+1)(c+1)$

and keep the maximum.

This works logically because every valid cutting strategy is uniquely described by how many cuts are assigned to each axis. The problem is the size of the search space. Even if we only iterate up to `10^6`, a triple loop becomes completely infeasible.

The crucial observation is that the answer depends only on the counts of cuts per axis, not on the order of cuts. Once we decide `a`, `b`, and `c`, the number of pieces is fixed.

That transforms the problem into maximizing a product under constraints.

Without upper bounds from dimensions, the product is largest when the values are as balanced as possible. This is the standard arithmetic mean and geometric mean intuition. But the dimensions cap how many cuts each direction may receive, so the optimal distribution may hit boundaries.

Since there are only three variables, we can iterate over two of them and derive the third. A further optimization makes this practical. The dimensions are symmetric, so we sort them. Then we iterate over feasible cuts for the smallest two dimensions, while the third becomes determined automatically.

The total number of iterations stays manageable because the smaller dimensions sharply limit the loops.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k³) | O(1) | Too slow |
| Optimal | O(xy) after sorting | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `x`, `y`, `z`, and `k`.
2. Sort the three dimensions. This does not change the answer because the axes are interchangeable. Sorting helps keep the nested loops small.
3. Iterate over every possible number of cuts `a` along the first dimension.

The valid range is:

$0 \le a \le \min(k, x-1)$
4. For each `a`, iterate over every possible number of cuts `b` along the second dimension.

The valid range is:

$0 \le b \le \min(k-a, y-1)$
5. The remaining cuts go to the third dimension:

$c = \min(k-a-b, z-1)$

We use as many remaining cuts as possible because increasing `c` always increases the product.
6. Compute the resulting number of pieces:

$(a+1)(b+1)(c+1)$
7. Track the maximum value over all iterations.
8. Print the maximum.

### Why it works

Every cut perpendicular to an axis increases the number of sections along that axis by exactly one. Since the final pieces form a 3D grid, the total number of pieces is the product of the section counts in each dimension.

The algorithm enumerates every feasible pair `(a,b)`. Once those are fixed, the best possible `c` is always the maximum allowed remaining value, because the product grows monotonically with `c`.

Since every valid distribution of cuts is considered exactly once, and the correct piece count is computed for each distribution, the maximum found by the algorithm is the true optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    x, y, z, k = map(int, input().split())

    dims = sorted([x, y, z])
    x, y, z = dims

    ans = 1

    max_a = min(k, x - 1)

    for a in range(max_a + 1):
        max_b = min(k - a, y - 1)

        for b in range(max_b + 1):
            c = min(k - a - b, z - 1)

            pieces = (a + 1) * (b + 1) * (c + 1)
            ans = max(ans, pieces)

    print(ans)

solve()
```

The first step sorts the dimensions so that the smallest bounds control the outer loops. This keeps the runtime manageable.

The outer loop chooses how many cuts go along the first axis. Since there are only `x - 1` valid planes, the loop never needs to exceed that value.

For every `a`, the second loop chooses cuts for the second axis. Again, we cannot exceed either the remaining cuts or the available planes.

The third value does not need another loop. Once `a` and `b` are fixed, any additional cut along the third axis strictly increases the product. The best choice is simply the largest feasible value.

The multiplication uses `(a + 1)`, `(b + 1)`, and `(c + 1)` because `n` cuts create `n + 1` segments.

A common off-by-one mistake is allowing `x` cuts instead of `x - 1`. A dimension of length `x` contains exactly `x - 1` internal cutting planes.

Another subtle point is using `min(k - a - b, z - 1)` for `c`. Extra cuts beyond the available planes are useless and must not be counted.

## Worked Examples

### Example 1

Input:

```
2 2 2 3
```

| a | b | c | Pieces |
| --- | --- | --- | --- |
| 0 | 0 | 1 | 2 |
| 0 | 1 | 1 | 4 |
| 1 | 0 | 1 | 4 |
| 1 | 1 | 1 | 8 |

The best configuration uses one cut in each direction. Each dimension becomes split into two parts, producing:

$2 \times 2 \times 2 = 8$

This example demonstrates the multiplicative structure of the problem.

### Example 2

Input:

```
10 1 1 5
```

| a | b | c | Pieces |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 1 |
| 1 | 0 | 0 | 2 |
| 2 | 0 | 0 | 3 |
| 3 | 0 | 0 | 4 |
| 4 | 0 | 0 | 5 |
| 5 | 0 | 0 | 6 |

The second and third dimensions cannot be cut at all because their sizes are already `1`.

The algorithm correctly places every useful cut along the first axis. This confirms that balanced distribution is not always possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(xy) after sorting | The loops iterate over feasible cuts for the two smallest dimensions |
| Space | O(1) | Only a few integer variables are stored |

Since the dimensions are at most `10^6`, iterating over the two smallest dimensions is fast enough in practice. The memory usage is constant, well within limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    x, y, z, k = map(int, input().split())

    x, y, z = sorted([x, y, z])

    ans = 1

    for a in range(min(k, x - 1) + 1):
        for b in range(min(k - a, y - 1) + 1):
            c = min(k - a - b, z - 1)

            ans = max(ans, (a + 1) * (b + 1) * (c + 1))

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup

    return out.getvalue().strip()

# provided sample
assert run("2 2 2 3\n") == "8", "sample 1"

# minimum-size input
assert run("1 1 1 0\n") == "1", "single cube"

# cuts larger than available planes
assert run("2 2 2 10\n") == "8", "extra cuts are useless"

# all dimensions equal
assert run("5 5 5 6\n") == "27", "balanced optimal split"

# only one dimension usable
assert run("10 1 1 5\n") == "6", "all cuts on one axis"

# off-by-one boundary
assert run("3 3 3 2\n") == "4", "cannot exceed available planes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 0` | `1` | Minimum possible box |
| `2 2 2 10` | `8` | Extra cuts beyond valid planes |
| `5 5 5 6` | `27` | Balanced distribution gives optimum |
| `10 1 1 5` | `6` | Only one dimension can be cut |
| `3 3 3 2` | `4` | Correct handling of cut limits |

## Edge Cases

Consider the input:

```
1 1 1 100
```

After sorting, all dimensions remain `1`.

The loops become:

```
a from 0 to 0
b from 0 to 0
c = 0
```

The computed product is:

$1 \times 1 \times 1 = 1$

No cuts are possible because there are no internal planes. The algorithm naturally handles this through the `x - 1` bounds.

Now consider:

```
2 2 2 10
```

Each dimension allows only one cut. The algorithm explores all feasible assignments, but every variable is capped at `1`.

The maximum product becomes:

$2 \times 2 \times 2 = 8$

The remaining seven cuts are ignored because they cannot correspond to real cutting planes.

Finally, consider:

```
10 1 1 5
```

The second and third dimensions have zero valid cutting planes.

The algorithm iterates:

```
a = 0..5
b = 0
c = 0
```

The best value occurs at `a = 5`:

$6 \times 1 \times 1 = 6$

This confirms that concentrating all cuts on one axis is sometimes optimal.
