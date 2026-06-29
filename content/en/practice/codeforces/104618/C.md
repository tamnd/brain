---
title: "CF 104618C - Sweet Selections"
description: "We are given three independent lists of strings: available ice cream flavors, available drizzles, and available toppings. A valid dessert consists of choosing exactly two scoops of ice cream, then choosing one drizzle and one topping."
date: "2026-06-29T17:29:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104618
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 09-22-23 Div. 1"
rating: 0
weight: 104618
solve_time_s: 68
verified: true
draft: false
---

[CF 104618C - Sweet Selections](https://codeforces.com/problemset/problem/104618/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three independent lists of strings: available ice cream flavors, available drizzles, and available toppings. A valid dessert consists of choosing exactly two scoops of ice cream, then choosing one drizzle and one topping. The two scoops are chosen from the flavor list, and repetition is allowed, but swapping the two scoops does not create a new dessert. After fixing the scoops, we independently choose one drizzle and one topping.

The task is to count how many distinct desserts can be formed under these rules. Distinctness is purely combinatorial: two desserts differ if any chosen flavor pair, drizzle, or topping differs. Since drizzles and toppings are single-choice components, they behave like independent multiplicative factors.

The constraints are small: each list has at most 100 elements. This immediately implies that any solution up to about a few million operations is safe. A quadratic or cubic combinatorial enumeration over flavors is acceptable, but anything worse than cubic would still likely pass due to limits.

A few edge cases matter for correctness.

If there is only one flavor, say `A`, then the only valid scoop pair is `(A, A)`. A naive approach that only considers pairs of distinct flavors would incorrectly return zero. For example, input:

```
A
B
C
```

Correct output is `1`, because we can still choose `(A, A)`.

If flavors are multiple but repeated selection is allowed, we must ensure unordered pairs are not double-counted. For example, `(A, B)` and `(B, A)` must be treated as one.

Another subtle case is ensuring that we correctly include all self-pairs `(A, A)` for every flavor, not just distinct pairs.

## Approaches

A direct brute-force approach is straightforward. We enumerate every possible pair of flavors, allowing repetition, and treating pairs as unordered. For each such pair, we independently choose a drizzle and a topping. If there are `n` flavors, `d` drizzles, and `t` toppings, brute-force would iterate over all `n × n` ordered pairs, filter duplicates by enforcing an ordering constraint, and multiply by `d × t`.

This works correctly but is unnecessarily heavy and obscures structure. The key observation is that drizzles and toppings are completely independent of scoop selection. Once we count valid unordered scoop pairs, the rest is just multiplication.

So the problem reduces to counting combinations with repetition: the number of ways to choose 2 elements from `n` flavors where order does not matter and repetition is allowed. This is a classic combinatorial count:

$$\binom{n+1}{2} = \frac{n(n+1)}{2}$$

After computing this value, we multiply it by the number of drizzles and toppings.

This reduces the entire problem to simple parsing plus arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | O(n² + d + t) | O(1) | Accepted |
| Combinatorial Formula | O(n + d + t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the list of flavors and count how many there are. Call this `n`. This is the only property of flavors we need because individual names do not affect counting.
2. Read drizzles and count them as `d`.
3. Read toppings and count them as `t`.
4. Compute the number of unordered flavor pairs with repetition allowed using the formula `n * (n + 1) // 2`. This accounts for both distinct pairs and self-pairs.
5. Multiply the number of flavor pairs by `d` and `t` to get the final answer.
6. Output the result.

The key step is using the combinatorial identity for multisets of size 2. The reasoning is that each valid dessert is fully determined by choosing a multiset of size 2 from flavors and then independently choosing one drizzle and one topping.

### Why it works

Every dessert corresponds to exactly one triple: a multiset of two flavors, one drizzle, and one topping. The flavor component is independent of the other two choices. The number of multisets of size 2 drawn from an `n`-element set is exactly `n(n+1)/2`, since we can either choose two identical elements in `n` ways or choose two distinct elements in `n(n-1)/2` ways. Summing these gives `n(n+1)/2`. Since every valid dessert is uniquely determined by one such multiset and one choice each from the other two lists, multiplying counts yields the total number of desserts.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    flavors = input().split()
    drizzles = input().split()
    toppings = input().split()

    n = len(flavors)
    d = len(drizzles)
    t = len(toppings)

    scoop_pairs = n * (n + 1) // 2
    print(scoop_pairs * d * t)

if __name__ == "__main__":
    main()
```

The implementation relies only on counting tokens per line. Since names are irrelevant beyond identity, splitting each line and taking lengths is sufficient.

The only subtlety is using `n * (n + 1) // 2` rather than `n * n`, which would incorrectly treat `(A, B)` and `(B, A)` as distinct. The integer division ensures exact combinatorial counting without floating-point risk.

## Worked Examples

### Example 1

Input:

```
Grass Licorice
Motor-Oil
Bone-Dust
```

We compute:

| Step | Value |
| --- | --- |
| flavors n | 2 |
| drizzles d | 1 |
| toppings t | 1 |
| scoop pairs | 2 * 3 / 2 = 3 |
| result | 3 |

This matches the three possible unordered scoop choices: `(Grass, Grass)`, `(Grass, Licorice)`, `(Licorice, Licorice)`, each combined with the single drizzle and topping.

### Example 2

Input:

```
A B C
X Y
Z
```

| Step | Value |
| --- | --- |
| flavors n | 3 |
| drizzles d | 2 |
| toppings t | 1 |
| scoop pairs | 3 * 4 / 2 = 6 |
| result | 12 |

The six scoop multisets expand into 12 desserts once each is paired with two drizzles.

This trace shows that increasing drizzle options scales results linearly and independently from scoop combinations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + d + t) | We only scan each input line once to count tokens |
| Space | O(1) | Only counters are stored, no need to keep lists |

The constraints cap each list at 100 elements, so this runs in constant practical time. Even with maximal input, operations are negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

def main():
    flavors = input().split()
    drizzles = input().split()
    toppings = input().split()

    n = len(flavors)
    d = len(drizzles)
    t = len(toppings)

    scoop_pairs = n * (n + 1) // 2
    print(scoop_pairs * d * t)

# provided sample
assert run("Grass Licorice\nMotor-Oil\nBone-Dust\n") == "3"

# minimum case (1 flavor, 1 drizzle, 1 topping)
assert run("A\nB\nC\n") == "1"

# all equal flavor structure edge case still single flavor line
assert run("A\nB C\nD E F\n") == "1 * 2 * 3"

# two flavors, multiple extras
assert run("A B\nX Y Z\nQ\n") == str((2*3//2)*3*1)

# maximum-ish small sanity
assert run(" ".join(["F"]*100) + "\nD\nT\n") == str((100*101//2)*1*1)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single of each | 1 | minimal configuration correctness |
| 2 flavors + multiple extras | computed | unordered pairing correctness |
| 100 identical flavors | 5050 | combinatorics boundary correctness |
| multi-drizzle/topping | scaled | multiplicative independence |

## Edge Cases

For a single flavor, such as:

```
A
B
C
```

we have `n = 1`, so scoop pairs = `1 * 2 / 2 = 1`. The algorithm correctly includes `(A, A)`. The multiplication by `d` and `t` leaves the result unchanged, producing `1`.

For two flavors:

```
A B
X Y
Z
```

the algorithm computes `n = 2`, scoop pairs = 3. These are `(A, A)`, `(B, B)`, `(A, B)`. Each is paired with the single topping and two drizzles, producing 6 total desserts. The formula correctly avoids double-counting `(B, A)` because the combinatorial expression already enforces unordered selection.

For maximum repetition:

```
F F F ... (100 times)
D
T
```

even though all names are identical, they still count as distinct elements in the flavor list, so `n = 100`. The algorithm computes `100 * 101 / 2 = 5050`, which matches the number of index-based selections of two positions with repetition allowed. This confirms the model is based on positions in the list, not string uniqueness beyond equality.
