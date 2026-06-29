---
title: "CF 104617C - Sweet Selections"
description: "We are given three independent collections of strings: ice cream flavors, drizzles, and toppings. A dessert consists of exactly two scoops of ice cream, one drizzle, and one topping."
date: "2026-06-29T17:33:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104617
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 09-22-23 Div. 2 (Beginner)"
rating: 0
weight: 104617
solve_time_s: 66
verified: true
draft: false
---

[CF 104617C - Sweet Selections](https://codeforces.com/problemset/problem/104617/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three independent collections of strings: ice cream flavors, drizzles, and toppings. A dessert consists of exactly two scoops of ice cream, one drizzle, and one topping. The two scoops are chosen from the flavor list, and they can be the same flavor or two different flavors. The order of the two scoops does not matter, so choosing A then B is identical to choosing B then A.

The task is to count how many distinct desserts can be formed under these rules. Two desserts are considered different if any of the chosen components differ, meaning either the scoop pair, the drizzle, or the topping is different.

The key observation about constraints is that each list has at most 100 items. This makes it feasible to consider all pairs of flavors explicitly, since the number of unordered pairs with repetition is at most 5050. Multiplying by up to 100 drizzles and 100 toppings gives about 50 million combinations in the absolute worst case, which is already borderline for Python if implemented naively, but still manageable if computed using arithmetic instead of enumeration.

A naive mistake is to try to explicitly construct every dessert combination as a tuple of strings and store them in a set. That approach is correct logically but risks unnecessary overhead from string handling and hashing millions of tuples.

A second subtle pitfall comes from misunderstanding the scoop pairing. For example, with flavors A, B, C, the valid pairs are AA, AB, AC, BB, BC, CC. Treating AB and BA as different would double count and inflate the answer incorrectly.

No other structural constraints exist, so the problem reduces to counting combinations rather than searching or optimizing over dependencies.

## Approaches

A brute-force solution would explicitly iterate over all ways to pick two flavors (with replacement), then iterate over all drizzles, and then all toppings. For each selection, we would build a representation of the dessert and insert it into a set to ensure uniqueness. This works because the set naturally removes duplicates caused by symmetry in scoop order.

The flaw is that this method performs explicit construction of every triple combination. With 100 flavors, there are 100 × 100 = 10000 ordered pairs, but only about 5050 unordered pairs. Even if we fix ordering, we still end up iterating up to 10000 pairs. Multiplying by 100 drizzles and 100 toppings yields up to 100 million iterations. Each iteration involves tuple creation and hashing, which is too slow in Python.

The structure of the problem removes any interaction between the three components. The scoop pair choice is independent from drizzle choice and topping choice. This separability means the total answer is the product of independent counts.

So the task reduces to:

Count unordered pairs of flavors with repetition allowed, then multiply by the number of drizzles and toppings.

The only non-trivial part is correctly counting flavor pairs.

Let n be the number of flavors. The number of valid unordered pairs with repetition is n(n+1)/2. This comes from choosing two indices i ≤ j.

Once that is computed, we multiply it by d × t.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² · d · t) | O(n² · d · t) | Too slow |
| Optimal | O(n + d + t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the list of flavors and count how many there are. Call this n. This matters because we only need the count, not the actual strings.
2. Compute the number of unordered flavor pairs with repetition allowed using n × (n + 1) / 2. This directly counts all pairs (i, j) where i ≤ j.
3. Read the list of drizzles and count them as d.
4. Read the list of toppings and count them as t.
5. Multiply the three independent choices: flavor pairs × d × t, and output the result.

### Why it works

Every valid dessert is uniquely determined by three independent decisions: a multiset of size two from flavors, one drizzle, and one topping. The flavor selection forms a combinatorial multiset of size two, and the standard counting formula n(n+1)/2 enumerates each such multiset exactly once. Since drizzle and topping choices do not interact with each other or with flavor selection, the multiplication principle applies directly. No combination is double counted or missed because each component is chosen independently and all combinations are valid.

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

    pairs = n * (n + 1) // 2
    print(pairs * d * t)

if __name__ == "__main__":
    main()
```

The solution reads each line and immediately converts it into a list of tokens using `split`, avoiding any need for parsing logic beyond whitespace separation. Only the lengths matter, so no storage beyond these lists is required.

The critical computation is `n * (n + 1) // 2`, which counts unordered pairs with repetition. Using integer division ensures correctness for both even and odd n. The final multiplication combines independent combinatorial choices.

## Worked Examples

### Sample Input

```
Grass Licorice
Motor-Oil
Bone-Dust
```

Here we have 2 flavors, 1 drizzle, and 1 topping.

| Step | Value |
| --- | --- |
| flavors (n) | 2 |
| drizzles (d) | 1 |
| toppings (t) | 1 |
| flavor pairs | 2 × 3 / 2 = 3 |
| result | 3 × 1 × 1 = 3 |

This matches the three possible scoop combinations: (Grass,Grass), (Grass,Licorice), (Licorice,Licorice).

### Custom Input

```
A B C
X Y
Z
```

| Step | Value |
| --- | --- |
| n | 3 |
| d | 2 |
| t | 1 |
| flavor pairs | 3 × 4 / 2 = 6 |
| result | 6 × 2 × 1 = 12 |

This confirms that each of the six scoop pairs can be combined with each of the two drizzles.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + d + t) | Each line is scanned once to count tokens, followed by constant-time arithmetic |
| Space | O(1) | Only counts are stored; no combinational structures are built |

The input sizes are small, but even if they were maximal, the solution remains trivially within limits because it avoids enumeration entirely and reduces everything to constant-time arithmetic after parsing.

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

# provided sample
assert run("Grass Licorice\nMotor-Oil\nBone-Dust\n") == "3"

# single flavor, single drizzle, single topping
assert run("Vanilla\nChocolate\nSprinkles\n") == "1"

# two flavors, no distinct pairing variety
assert run("A B\nX\nY Z\n") == "3"

# three flavors, all components large enough to test multiplication
assert run("A B C\nD E F\nG H\n") == "36"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 flavor each | 1 | Handles n = 1 correctly |
| 2 flavors | 3 | Validates combination counting |
| 3×3×2 case | 36 | Checks full multiplicative structure |

## Edge Cases

A subtle edge case is when there is only one flavor. For input:

```
Vanilla
Chocolate
Sprinkles
```

we have n = 1, so flavor pairs = 1 × 2 / 2 = 1. The only valid scoop choice is (Vanilla, Vanilla). The algorithm correctly handles this without any special branching.

Another case is when all lists are minimal:

```
A
B
C
```

Here the result is still 1, since each category has exactly one option. The multiplication still holds because the pair count remains valid and no division or zero-edge behavior occurs.

Finally, when flavors are larger but drizzles or toppings are single-element lists, the formula naturally collapses those dimensions without breaking correctness, since multiplying by 1 preserves the count and does not require conditional handling.
