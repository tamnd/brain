---
title: "CF 102215G - Akinator"
description: "Think of the questioning strategy as a binary decision tree. Every internal node is one question, its two outgoing edges correspond to the answers \"Yes\" and \"No\", and every leaf identifies exactly one person."
date: "2026-08-18T22:02:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "G"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 451
verified: true
draft: false
---

[CF 102215G - Akinator](https://codeforces.com/problemset/problem/102215/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

Think of the questioning strategy as a binary decision tree. Every internal node is one question, its two outgoing edges correspond to the answers "Yes" and "No", and every leaf identifies exactly one person. Because a question may contain any subset of the currently possible people, any binary partition of the candidates can be used at a node. Thus the original game is exactly the problem of building a binary prefix tree.

If person (i) ends up at depth (l_i), Akinator asks exactly (l_i) questions when that person was chosen. Since (p_i=a_i/\sum a_j), the expected number of questions is

[
\frac{\sum_i a_i l_i}{\sum_i a_i}.
]

The denominator is fixed, so the real optimization target is the integer

[
\sum_i a_i l_i.
]

The tree must have maximum depth at most (k). A binary tree with (n) leaves and height at most (k) exists exactly when (n\le 2^k). If this fails, no questioning strategy can distinguish all people in the allowed number of questions. The same condition is the Kraft bound for binary prefix codes.

The constraints are small in (n), but they do not permit enumerating trees or subsets. With (n\le100), even (O(n^3)) is harmless, while anything exponential in (n) is completely infeasible. The probabilities are represented by integers as large as (10^{12}), so the implementation should work entirely with exact integers rather than floating point.

There are several boundary cases that can fool a naive implementation. With one possible person, no question is needed. For example,

```
1 1
1000000000000
```

has answer `0/1`. A solution that assumes every person needs at least one question would incorrectly output a positive value.

The depth bound can make an otherwise ordinary Huffman construction impossible. For example,

```
3 1
1 2 3
```

has output `No solution`, because one binary question has only two possible answer sequences. Running ordinary Huffman coding without checking the height constraint can silently produce a tree of depth two.

The opposite boundary is when (n=2^k). Then every leaf must be exactly at depth (k), regardless of the weights. For example,

```
4 2
1 2 3 4
```

has weighted cost (2(1+2+3+4)=20), so the answer is `2/1`. A strategy that tries to give one person a shorter code cannot do so without making another person deeper than two questions.

Finally, equal weights are useful for detecting ordering mistakes. With

```
3 2
1 1 1
```

the optimal depths are (1,2,2), giving total cost (5) and answer `5/3`. The most frequent person is not special here, so any correct tie handling must still produce the same total.

## Approaches

A direct approach would try every possible binary decision tree. At a set (S) of currently possible people, a question chooses a nonempty proper subset (A\subset S), with (A) becoming the Yes branch and (S\setminus A) becoming the No branch. A recursive dynamic program over subsets could remember the best cost for every subset and remaining depth.

This is correct because every possible questioning strategy has exactly such a first partition, and the two resulting subproblems are independent after the first question. Unfortunately, there are (2^n) subsets, and considering all possible splits gives exponential work on top of that. Across all subsets, the number of ordered nontrivial splits is

[
\sum_{S\ne\varnothing} (2^{|S|}-2)
=3^n-2^{n+1}+1.
]

For (n=100), (3^{100}) is about (5.15\cdot10^{47}), so this approach is not remotely viable.

The useful observation is that we do not actually care which person goes to which exact binary string. We only care about the depths (l_i). A set of depths is realizable by a binary prefix tree exactly when it satisfies the Kraft inequality

[
\sum_i2^{-l_i}\le1.
]

For an optimal tree, equality holds, because if the sum were smaller we could shorten some code without violating the constraint. Thus the problem becomes a length-limited Huffman coding problem: minimize (\sum a_i l_i) subject to (1\le l_i\le k) and (\sum 2^{-l_i}=1).

There is a particularly clean way to solve this constrained Huffman problem. Imagine that every person initially has length zero. The Kraft sum is then (n). Increasing person (i)'s length from (l-1) to (l) decreases the Kraft sum by (2^{-l}), and costs exactly (a_i). We need to perform length increases whose total Kraft reduction is (n-1).

This turns the problem into a binary coin-collector problem. For every person (i), create (k) coins with denominations

[
2^{-1},2^{-2},\ldots,2^{-k},
]

and give every one of those coins value (a_i). We need a minimum-value collection whose denominations sum to (n-1). If the coin corresponding to level (l) is selected, that represents increasing the person's code length through level (l). This is the standard reduction behind package-merge for length-limited Huffman coding.

Because all denominations are powers of two, the coin problem has a greedy solution. At the smallest denomination, any selected coins must occur in pairs, since every larger denomination is twice as large. The cheapest possible pair is formed from the two cheapest available coins. That pair can then be treated as one coin of the next denomination. If one coin is left over, it can never participate in an exact solution, so the most expensive leftover coin can be discarded. Repeating this process produces the package-merge algorithm.

The brute force works because it explicitly explores all binary partitions. The package-merge observation lets us replace all those trees by only (k) sorted lists containing the cheapest relevant packages. Since (n,k\le100), even the straightforward (O(nk)) implementation is easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(3^n)) | (O(2^n)) | Too slow |
| Optimal package-merge | (O(nk)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Sort the weights (a_i) in nondecreasing order. Equal weights may be placed in any order. The package-merge algorithm always needs items in increasing value order, and a package formed from two adjacent sorted items has a value no smaller than the previous package.
2. Check whether (n\le2^k). If not, there cannot be (n) different leaves within depth (k), so print `No solution`.
3. Regard the sorted weights as the initial list of coins of denomination (2^{-k}). These are the smallest coins, so they are the first ones that can be paired.
4. Repeat the following process (k-1) times. Pair consecutive elements of the current sorted list, starting with the two cheapest. Each pair becomes a package whose value is the sum of its two elements. Then merge the package list with another copy of the original weights, and sort the result.

The original weights represent ordinary coins of the new, twice-as-large denomination. The packages represent two smaller coins that have been combined into exactly that same denomination. Keeping both choices in one sorted list is what lets later decisions choose between a single expensive coin and a cheaper package.
5. After those (k-1) rounds, pair consecutive elements one final time, but do not merge the resulting packages with the original weights. These packages now have denomination (1).
6. Select the (n-1) cheapest final packages and add their values. This sum is the minimum possible weighted number of questions.
7. Divide the resulting integer by (S=\sum a_i). Compute the greatest common divisor of the numerator and (S), divide both by it, and print the reduced fraction.

### Why it works

Let (l_i) be the final depth assigned to person (i). Starting with every (l_i=0), the Kraft sum is (n). Increasing (l_i) from (l_i-1) to (l_i) decreases that sum by (2^{-l_i}), while increasing the objective by (a_i). Reaching a valid complete binary tree requires the Kraft sum to become exactly (1), so the selected reductions must have total value (n-1).

The package-merge construction solves precisely this minimum-value selection problem. At every denomination, a valid solution can use the smallest denomination only an even number of times. If it uses (2r) such coins, it is always optimal to use the (2r) cheapest ones, and those can be grouped into (r) consecutive pairs. Replacing each pair by one package preserves both its total denomination and its total value. Thus solving the smaller-denomination layer greedily produces exactly the set of choices needed by the next layer.

At the final layer, every selected item has denomination (1), so choosing (n-1) of them gives total denomination (n-1). Expanding the packages gives one selected coin for every unit increase of every code length, so the total package value is exactly (\sum_i a_i l_i). Since package-merge minimizes that value, the resulting code has minimum expected number of questions. The resulting lengths satisfy Kraft equality and are at most (k), so a binary prefix tree realizing them exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def merge_sorted(a, b):
    """Merge two already sorted lists."""
    res = []
    i = 0
    j = 0

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1

    if i < len(a):
        res.extend(a[i:])
    if j < len(b):
        res.extend(b[j:])

    return res

def solve():
    n, k = map(int, input().split())
    weights = list(map(int, input().split()))
    weights.sort()

    if n > (1 << k):
        print("No solution")
        return

    current = weights[:]

    # Move from denomination 2^(-k) up to denomination 2^(-1).
    # At every intermediate level, packages are merged with
    # the original coins of the new denomination.
    for _ in range(k - 1):
        packages = []
        for i in range(0, len(current) - 1, 2):
            packages.append(current[i] + current[i + 1])

        current = merge_sorted(weights, packages)

    # One final packaging step creates denomination-1 items.
    final_packages = []
    for i in range(0, len(current) - 1, 2):
        final_packages.append(current[i] + current[i + 1])

    # final_packages is already sorted.
    numerator = sum(final_packages[:n - 1])
    denominator = sum(weights)

    g = __import__("math").gcd(numerator, denominator)
    numerator //= g
    denominator //= g

    print(f"{numerator}/{denominator}")

if __name__ == "__main__":
    solve()
```

The input weights are sorted once at the beginning. Sorting is enough because package values are formed by adding adjacent elements of a sorted list, so the resulting package list is also sorted.

The `merge_sorted` function exploits this property. It merges the (n) original weights with the current package list in linear time. Re-sorting the whole list at every level would still pass comfortably for (n,k\le100), but the merge makes the intended (O(nk)) complexity explicit.

The loop runs only through the first (k-1) levels. The final level is deliberately handled separately because the final packages have denomination (1), and no original coins of denomination (1) exist. Mixing the original weights into that final list would create an off-by-one error in the denomination structure.

The range used when creating pairs is `range(0, len(current) - 1, 2)`. If the current list has an odd number of elements, its last element is left unused. Since the list is sorted, that element is the most expensive one, which is exactly the item that package-merge discards.

The feasibility check uses `1 << k`, so there is no floating-point logarithm and no rounding issue. Python integers also handle the largest possible intermediate values safely. The largest relevant weighted cost is on the order of (n^2\cdot10^{12}), far below what Python's arbitrary-precision integers can handle comfortably.

The final package list is already sorted because `current` is sorted and the sum of each consecutive pair is nondecreasing. Hence the (n-1) cheapest packages are simply its first (n-1) elements.

For (n=1), that slice is empty, giving numerator zero. The denominator is positive, so the reduced answer is correctly `0/1`.

## Worked Examples

### Sample 1

The input is

```
4 1
8 1 9 2
```

There are four people but only one question. A single binary question has only two possible answer sequences, so four different people cannot all be distinguished.

| Variable | Value |
| --- | --- |
| (n) | 4 |
| (k) | 1 |
| (2^k) | 2 |
| Feasible? | No |

The algorithm stops before constructing any packages and prints `No solution`. This confirms that the capacity check is necessary and also avoids meaningless package processing when the tree cannot exist.

### Sample 2

The input is

```
4 2
1 2 3 4
```

The sorted weights are already `[1, 2, 3, 4]`.

| Stage | Current list | Packages produced |
| --- | --- | --- |
| Initial | `[1, 2, 3, 4]` | `[3, 7]` |
| After merge | `[1, 2, 3, 3, 4, 7]` | `[3, 6, 11]` |
| Final selection | `[3, 6, 11]` | `3 + 6 + 11 = 20` |

There are (n-1=3) final packages, so all three are selected. The weighted cost is (20), while the total weight is (1+2+3+4=10). The reduced fraction is (20/10=2/1).

The corresponding optimal lengths are (2,2,2,2). The Kraft sum is (4\cdot2^{-2}=1), and every person is found in exactly two questions.

### Sample 3

For

```
4 3
1 2 3 4
```

the first intermediate list is

```
[1, 2, 3, 3, 4, 7]
```

The next packaging step gives `[3, 6, 11]`, which is merged with the original weights:

```
[1, 2, 3, 3, 4, 6, 7, 11]
```

The final packages are then `[3, 6, 10, 18]`.

| Stage | Current list | Packages |
| --- | --- | --- |
| Initial | `[1, 2, 3, 4]` | `[3, 7]` |
| Level 2 | `[1, 2, 3, 3, 4, 7]` | `[3, 6, 11]` |
| Level 3 | `[1, 2, 3, 3, 4, 6, 7, 11]` | `[3, 6, 10, 18]` |
| Select 3 cheapest | `[3, 6, 10]` | `19` |

The weighted cost is (19), and the total weight is (10), so the answer is `19/10`.

The selected packages correspond to lengths (3,3,3,3) for the weights (1,2,3) and a shorter length for weight (4). The resulting strategy can ask about person 4 first, then person 3 if necessary, and finally distinguish persons 1 and 2, exactly matching the optimal structure described by the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nk)) | Each of the (k) levels creates (O(n)) packages and merges two sorted lists of (O(n)) elements. |
| Space | (O(n)) | Only the original weights, the current list, and one package list are stored. |

With (n,k\le100), the algorithm performs only around (10^4) list-level operations up to constant factors. The integer values are also small enough that exact arbitrary-precision arithmetic is inexpensive, so the solution fits comfortably within the 2 second and 256 MB limits.

## Test Cases

```python
import sys
import io
import math

def merge_sorted(a, b):
    res = []
    i = 0
    j = 0

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1

    res.extend(a[i:])
    res.extend(b[j:])
    return res

def solve_text(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline

        n, k = map(int, input().split())
        weights = list(map(int, input().split()))
        weights.sort()

        if n > (1 << k):
            return "No solution"

        current = weights[:]

        for _ in range(k - 1):
            packages = [
                current[i] + current[i + 1]
                for i in range(0, len(current) - 1, 2)
            ]
            current = merge_sorted(weights, packages)

        final_packages = [
            current[i] + current[i + 1]
            for i in range(0, len(current) - 1, 2)
        ]

        numerator = sum(final_packages[:n - 1])
        denominator = sum(weights)

        g = math.gcd(numerator, denominator)
        return f"{numerator // g}/{denominator // g}"
    finally:
        sys.stdin = old_stdin

def run(inp: str) -> str:
    return solve_text(inp)

# Provided samples
assert run("4 1\n8 1 9 2\n") == "No solution", "sample 1"
assert run("4 2\n1 2 3 4\n") == "2/1", "sample 2"
assert run("4 3\n1 2 3 4\n") == "19/10", "sample 3"

# Minimum-size input
assert run("1 1\n1000000000000\n") == "0/1", "single person needs no questions"

# Boundary where exactly 2^k people fit
assert run("4 2\n1 1 1 1\n") == "2/1", "all leaves must have depth 2"

# Smallest impossible case
assert run("3 1\n1 2 3\n") == "No solution", "three people cannot fit at depth 1"

# All equal weights with a non-complete power of two
assert run("3 2\n1 1 1\n") == "5/3", "optimal lengths are 1, 2, 2"

# Maximum-size case
assert run("100 100\n" + " ".join(["1"] * 100) + "\n") == "168/25", \
    "100 equal weights require total length 672"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1000000000000` | `0/1` | Minimum-size case and zero-question answer |
| `4 2 / 1 1 1 1` | `2/1` | Exact (n=2^k) boundary |
| `3 1 / 1 2 3` | `No solution` | Capacity check and depth boundary |
| `3 2 / 1 1 1` | `5/3` | Uneven optimal depths and equal weights |
| `100 100 / 100 ones` | `168/25` | Maximum (n), large (k), and exact integer arithmetic |

## Edge Cases

For a single person, the input

```
1 1
1000000000000
```

passes the capacity check. The initial list contains one value, and there are no pairs to form. The final package list is empty, so selecting the (n-1=0) cheapest packages costs zero. The denominator is positive, giving `0/1`. This matches the fact that Akinator already knows who the person must be.

For too many people, consider

```
3 1
1 2 3
```

The algorithm checks (3>2^1) immediately. No binary tree of height one can have three leaves, so it prints `No solution`. This prevents an incomplete final package list from being mistaken for a valid code.

For the exact capacity boundary,

```
4 2
1 1 1 1
```

the four leaves must occupy all four positions at depth two. The first packaging creates two packages of value (2), the final packaging creates one package of value (4) only after the intermediate list is formed, and the resulting selected cost is (8). Dividing by the total weight (4) gives `2/1`. There is no room for a shorter codeword because shortening one leaf would force another leaf beyond depth two.

For equal weights with three people,

```
3 2
1 1 1
```

the first package list is `[2]`, which is merged with the original weights to obtain `[1,1,1,2]`. The final packages are `[2,3]`, both of which must be selected. Their total value is (5), while the total probability weight is (3), giving `5/3`. The corresponding lengths are (1,2,2), whose Kraft sum is (1/2+1/4+1/4=1).

For the largest input size,

```
100 100
1 1 1 ... 1
```

with one hundred weights equal to one, the generous depth limit does not bind. The optimal equal-weight binary tree has 28 leaves at depth 6 and 72 leaves at depth 7, giving

[
28\cdot6+72\cdot7=672.
]

The expected number of questions is (672/100=168/25). The test confirms that the package construction continues correctly for many levels and that the final fraction is reduced exactly.
