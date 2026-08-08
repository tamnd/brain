---
title: "CF 102443A - Attractive Flowers"
description: "For every flower type, the bouquet can contain some number of flowers of that type, and whenever a type is used, its chosen count must be odd. We want the largest possible total number of flowers."
date: "2026-08-09T01:41:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102443
codeforces_index: "A"
codeforces_contest_name: "2019-2020 Russia Team Open, High School Programming Contest (VKOSHP 19)"
rating: 0
weight: 102443
solve_time_s: 273
verified: true
draft: false
---

[CF 102443A - Attractive Flowers](https://codeforces.com/problemset/problem/102443/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 33s  
**Verified:** yes  

## Solution
## Problem Understanding

For every flower type, the bouquet can contain some number of flowers of that type, and whenever a type is used, its chosen count must be odd. We want the largest possible total number of flowers. A type does not have to appear in the bouquet at all, so its contribution may be zero.

For one type with `a_i` available flowers, the best possible odd contribution is simply the largest odd number not exceeding `a_i`. If `a_i` is already odd, we can use all of them. If `a_i` is even, one flower must be left behind, so the contribution becomes `a_i - 1`.

After making this adjustment independently for every type, every nonzero contribution is odd. The parity of the total now depends only on how many types we use. An odd number of odd values has an odd sum, while an even number of odd values has an even sum. Consequently, if `n` is odd, we can keep every type. If `n` is even, we must omit one type entirely. To lose as little as possible, we omit the type whose adjusted contribution is smallest.

The constraint `n <= 100000` means the solution should process the array in roughly linear time. An `O(n^2)` method could perform around `10^10` operations at the upper bound, which is far beyond the one-second limit. Even an `O(n log n)` method is unnecessary here because the answer only needs a sum and a minimum. The individual values satisfy `a_i <= 1000`, so the answer easily fits in a standard 32-bit integer, although Python integers also handle it naturally.

There are several edge cases that can fool an implementation that focuses only on making every chosen count odd. With one type, for example,

```
1
2
```

the largest valid bouquet contains `1` flower, not `2`, because the only usable count must be odd.

When the number of types is even, we must remove one entire type. For example,

```
2
2 3
```

becomes adjusted counts `1` and `3`. Keeping both gives `4`, which is even, so the correct answer is `3`. A careless solution that merely sums the largest odd count for every type would output `4`.

The type we remove should be chosen after adjusting its available count to an odd value. For example,

```
4
2 7 4 9
```

becomes `1, 7, 3, 9`. Since there are four types, one must be omitted, and removing the contribution `1` gives the maximum answer `19`. Choosing a type based on its original `a_i` without considering the odd adjustment can make the wrong choice.

## Approaches

A direct brute-force approach can consider every subset of flower types. For each subset, we would take the largest odd possible number from every selected type, sum those contributions, check whether the number of selected types is odd, and keep the largest valid total. This is correct because once the set of selected types is fixed, taking fewer flowers from any selected type can only make the bouquet smaller.

The problem is the number of subsets. With `n` types there are `2^n` possible subsets. At `n = 100000`, this is about `10^30103` possibilities, so even inspecting one subset in constant time would be hopeless. The brute force works because it explicitly explores every possible collection of types, but it fails when the number of types becomes large.

The key observation removes almost all of those choices. For each type, there is never a reason to take anything except its largest available odd count. After that adjustment, every used type contributes an odd number. Thus the only remaining decision is how many types to use. If `n` is odd, using all types already gives an odd total. If `n` is even, using all types gives an even total, so exactly one type must be omitted. Since all adjusted contributions are positive, omitting more than one type would only make the answer smaller. The best omitted type is simply the one with the smallest adjusted contribution.

This reduces the entire problem to one pass through the array, maintaining the sum of adjusted odd counts and their minimum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(2^n * n)` | `O(n)` | Too slow |
| Optimal | `O(n)` | `O(1)` extra | Accepted |

## Algorithm Walkthrough

1. Read the `n` available flower counts and initialize the total sum and the minimum adjusted contribution.
2. For every `a_i`, convert it to the largest odd number not exceeding it. If `a_i` is even, subtract one. Add this adjusted value to the total and update the minimum.

This is optimal for an individual type because decreasing an odd contribution by any positive amount would either make it invalid or make the bouquet smaller.
3. If `n` is odd, keep the total as it is. Every adjusted contribution is odd, and there are an odd number of them, so their sum is odd.
4. If `n` is even, subtract the smallest adjusted contribution from the total. This effectively omits that entire flower type, leaving `n - 1` used types. Since `n - 1` is odd, the resulting sum is odd.

Removing exactly one type is optimal because all adjusted contributions are positive, and among all single types, removing the smallest one loses the fewest flowers.
5. Print the resulting total.

### Why it works

After adjustment, every type that we might include contributes a positive odd number, and that is the maximum valid contribution for that type. Any optimal bouquet therefore uses the maximum odd contribution for every type it includes.

The parity of a sum of odd numbers is determined by the number of terms. When `n` is odd, all adjusted contributions can be used and the total is automatically odd. When `n` is even, using all contributions produces an even sum, so an odd total requires an odd number of used types. The largest such number is `n - 1`, meaning exactly one type should be removed. Since every adjusted contribution is positive, removing more types cannot improve the answer, and removing the smallest contribution gives the largest remaining sum. Thus the algorithm always constructs an optimal bouquet.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    total = 0
    mn = 10**18

    for x in a:
        if x % 2 == 0:
            x -= 1

        total += x
        mn = min(mn, x)

    if n % 2 == 0:
        total -= mn

    print(total)

if __name__ == "__main__":
    solve()
```

The loop performs the first two algorithmic steps together. For an even `x`, subtracting one changes it to the largest odd value at most `x`. For an odd `x`, nothing changes. The adjusted value is then added to `total`, while `mn` records the cheapest type to remove if the number of types is even.

The parity check uses `n`, not `total`. Once every adjusted contribution is odd, the parity of their sum is completely determined by the number of contributions. An odd number of them gives an odd sum, while an even number gives an even sum.

When `n` is even, `mn` is guaranteed to exist because `n >= 1`, and every adjusted value is at least `1`. Subtracting `mn` removes the entire contribution of one type. There is no off-by-one issue in the even case because the remaining number of used types is exactly `n - 1`.

Python's integer type does not overflow, and the largest possible answer is below `100000 * 999`, so even a 32-bit signed integer would be sufficient.

## Worked Examples

### Sample 1

The input is:

```
3
3 5 8
```

The adjusted contribution of each type is obtained independently.

| Type | Available | Adjusted odd count | Total after type | Minimum |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 3 | 3 |
| 2 | 5 | 5 | 8 | 3 |
| 3 | 8 | 7 | 15 | 3 |

There are three types, which is odd, so no type needs to be removed. The answer is `15`.

This demonstrates the basic case where every type can contribute its largest odd count and the resulting number of terms already has the required parity.

### Sample 2

The input is:

```
3
1 1 1
```

All three values are already odd.

| Type | Available | Adjusted odd count | Total after type | Minimum |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 |
| 2 | 1 | 1 | 2 | 1 |
| 3 | 1 | 1 | 3 | 1 |

There are three types, so the total remains `3`. No adjustment for the parity of `n` is needed.

This example confirms that the algorithm does not unnecessarily remove flowers when all values are already at their smallest possible odd counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Every flower type is processed exactly once. |
| Space | `O(n)` for the input array, `O(1)` extra | The algorithm stores the input values and only maintains the sum and minimum while processing them. |

With `n <= 100000`, a linear scan performs only about one hundred thousand iterations, comfortably within the one-second limit. The memory usage is also small compared with the 512 MB limit.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    total = 0
    mn = 10**18

    for x in a:
        if x % 2 == 0:
            x -= 1
        total += x
        mn = min(mn, x)

    if n % 2 == 0:
        total -= mn

    print(total)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("3\n3 5 8\n") == "15", "sample 1"
assert run("3\n1 1 1\n") == "3", "sample 2"

# Minimum-size input
assert run("1\n1\n") == "1", "single type with one flower"

# Even number of types, smallest adjusted value must be removed
assert run("2\n2 3\n") == "3", "remove adjusted contribution 1"

# All equal values with an even number of types
assert run("4\n7 7 7 7\n") == "21", "remove one 7"

# Boundary case with an even value of 1000
assert run("2\n1 1000\n") == "999", "1000 becomes 999 and type 1 is removed"

# Maximum-size case
assert run("100000\n" + "1000 " * 100000 + "\n") == "99899001", "maximum n and ai"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `1` | Minimum `n` and smallest possible contribution |
| `2 / 2 3` | `3` | Even number of types and removal of the minimum adjusted value |
| `4 / 7 7 7 7` | `21` | All equal values and even `n` |
| `2 / 1 1000` | `999` | Conversion of the even boundary value `1000` to `999` |
| `100000 / all 1000` | `99899001` | Maximum input size and linear processing |

## Edge Cases

With a single type, there is no parity adjustment involving omitted types because `n` is already odd. For

```
1
2
```

the value `2` is reduced to `1`, giving the answer `1`. Taking both flowers would violate the requirement that the chosen count for that type be odd.

When the number of types is even, keeping every adjusted contribution always produces an even total. Consider

```
2
2 3
```

The adjusted values are `1` and `3`, whose sum is `4`. The algorithm finds the minimum contribution `1` and subtracts it, leaving `3`. The resulting bouquet uses one type, has an odd number of flowers, and is maximal.

The minimum adjusted contribution may come from a type whose original count is even. For

```
4
2 7 4 9
```

the adjusted values are `1, 7, 3, 9`. The smallest is `1`, so the algorithm removes that type and returns `19`. Looking at the original values alone could incorrectly suggest that `2` is not a meaningful candidate because it was even, but after enforcing the odd-count requirement its actual contribution is `1`.

Finally, the largest available count is itself even in the boundary case `a_i = 1000`. For

```
2
1 1000
```

the adjusted contributions are `1` and `999`. Since there are two types, one must be omitted, and removing the contribution `1` gives `999`. This checks both the even-value conversion and the minimum-removal logic at the maximum allowed `a_i`.
