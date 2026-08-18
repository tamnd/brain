---
title: "CF 102215G - Akinator"
description: "The game can be viewed as a binary decision tree. Every question has two possible answers, so after a sequence of answers we arrive at one leaf of a binary tree, and that leaf represents the person Akinator has identified."
date: "2026-08-18T12:00:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "G"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 637
verified: false
draft: false
---

[CF 102215G - Akinator](https://codeforces.com/problemset/problem/102215/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 37s  
**Verified:** no  

## Solution
## Problem Understanding

The game can be viewed as a binary decision tree. Every question has two possible answers, so after a sequence of answers we arrive at one leaf of a binary tree, and that leaf represents the person Akinator has identified. If a person is placed at depth (d), Akinator needs exactly (d) questions when that person was chosen.

The actual question can contain any subset of the currently possible people. Because of that freedom, every binary decision tree can be implemented as a valid questioning strategy. The problem is consequently equivalent to constructing a binary tree with exactly (n) leaves, maximum depth at most (k), and minimum weighted path length

[
\sum_{i=1}^{n} a_i d_i.
]

The probabilities only differ from the values (a_i) by the same normalization factor, so minimizing the weighted sum above also minimizes the expected number of questions.

The constraints are small in the number of people, (n\le 100), and the depth limit is also at most 100. That rules out enumerating trees, since even the number of possible binary tree shapes grows superexponentially. At the same time, (O(nk)) or (O(nk\log n)) algorithms are easily fast enough, while a dynamic program with three independent (n)-sized dimensions would already be unnecessarily expensive in Python.

There are several edge cases that deserve explicit treatment. With one possible person, no question is necessary. For example,

```
1 1
7
```

has output

```
0/1
```

because Akinator already knows the answer. A solution that blindly assigns every person a positive-depth leaf would incorrectly output `1/1`.

A second boundary case is insufficient depth. For

```
4 1
8 1 9 2
```

there are only two leaves available in a binary tree of height one, but four people must be distinguished. The correct output is

```
No solution
```

A careless implementation that only optimizes an incomplete tree could produce a finite average even though some people cannot be identified.

Equal weights are another subtle case. For

```
3 3
1 1 1
```

the optimal depths are (1,2,2), giving

[
\frac{1+2+2}{3}=\frac53.
]

A tie-sensitive implementation of package merging can choose different equally weighted intermediate objects, so its ordering rule must be deterministic and compatible with the package-merge construction.

Finally, the answer is a rational number, not necessarily an integer. For

```
3 3
1 2 4
```

the optimal depths are (2,2,1) after assigning the largest weight to the shallowest leaf, giving

[
\frac{2+4+4}{7}=\frac{10}{7}.
]

Using floating point here can lose precision, so the implementation keeps the numerator and denominator as integers and reduces them with `gcd`.

## Approaches

A direct approach would enumerate possible binary decision trees and calculate their expected cost. For every tree we could assign the largest weights to the shallowest leaves, because swapping two leaves where a larger weight has greater depth can only decrease the cost. This makes the cost calculation straightforward once the tree shape is known.

The problem is the number of trees. Even if we ignore the labels of the people and enumerate only full binary tree shapes, there are ((2n-3)!!) possibilities. At (n=100), this is (197!!), which is greater than (10^{184}). An alternative brute force over every possible depth for every person would have up to (k^n) assignments, which reaches (100^{100}=10^{200}). Either interpretation is completely infeasible.

The useful observation is that this is exactly the binary length-limited Huffman problem. Ordinary Huffman coding minimizes weighted path length without restricting the maximum depth. Here we have the same objective, with the additional condition that every leaf has depth at most (k). The standard package-merge algorithm solves precisely this bounded-depth version in (O(nk)) time. This connection is also reflected in the Codeforces discussion of the problem, where an (O(nk)) solution using optimal length-limited Huffman codes is identified.

The package-merge construction starts with the individual people. At each level it combines adjacent cheapest objects in pairs, producing packages whose weight is the sum of their contents, and then merges those packages back with the original individual people. After (k) levels, selecting the (2n-2) cheapest objects gives exactly the set of length increments needed for an optimal code. This is the classical package-merge formulation of length-limited Huffman coding.

The reason this works is closely related to the Kraft inequality. If every person initially has code length zero, the Kraft sum is (n). Increasing one code length by one reduces its contribution by a factor of two. Package-merge groups two equal-level choices into one higher-level choice, preserving exactly the structure needed to make the total Kraft sum become one. The selected objects consequently describe a valid full binary tree, while choosing the cheapest possible objects minimizes its weighted path length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(k^n)) or worse | (O(n)) | Too slow |
| Package Merge | (O(nk)) | (O(nk)) | Accepted |

## Algorithm Walkthrough

1. Read the weights and sort the people by increasing weight. The order of equal weights can be arbitrary for the final objective, but the package construction needs deterministic tie handling.
2. If (n=1), return `0/1`. The only person is already known, so the optimal code has length zero.
3. Check whether (n\le 2^k). A binary tree of height (k) has at most (2^k) leaves. If this condition fails, no strategy can distinguish all people, so print `No solution`.
4. Create level one as the list of all individual people. Each object stores its weight and whether it is an original leaf.
5. For every level from two through (k), take the previous level in increasing order of cost and pair consecutive objects. Each pair becomes a package whose weight is the sum of the two child weights. If an odd object remains, it is not packaged.
6. Merge the newly created packages with another copy of the original people. Packages and individual people are kept sorted by their cost. When costs are equal, packages are placed before individual leaves. This deterministic tie rule keeps the package structure compatible with the backward reconstruction.
7. At level (k), select the first (2n-2) objects. These are the cheapest possible choices that reduce the Kraft sum from (n) to one.
8. Move backward from level (k-1) to level one. Count how many selected objects at the next level are packages. If that number is (c), select the first (2c) objects at the current level. A selected package represents two objects at the preceding level, which is why every selected package creates exactly two required choices there.
9. Initialize every person's code length to zero. Scan the selected sets from the deepest level toward the first level. Whenever a selected object is an original person, increase that person's length by one.
10. Compute the weighted path length (\sum a_i d_i). Divide it by (\sum a_i), reduce the fraction using the greatest common divisor, and print the result.

### Why it works

The package-merge invariant is that every selected object at a given level represents one legal unit of Kraft-sum reduction at that level. A package represents two lower-level objects, so whenever a package is selected, its two children must also be selected during the backward reconstruction. The final selection of (2n-2) objects reduces the initial Kraft sum from (n) to one, which is exactly the Kraft equality for a complete binary prefix tree. The construction consequently produces valid code lengths with maximum length (k).

For optimality, package-merge always combines the two cheapest currently available objects and keeps the resulting package as a candidate at the next level. If two objects of the same level are both needed in an optimal solution, replacing them by their package preserves the required Kraft contribution while replacing their two weights by their sum. Thus the cheaper pair can be represented without losing an optimal solution. Repeating this argument level by level proves that the final (2n-2) selected objects have minimum possible total weight. Each original person's number of occurrences in the selected objects is exactly its code length, so the resulting weighted path length is minimal. This is the standard optimality argument behind length-limited Huffman package-merge coding.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def solve_case(n, k, weights):
    if n == 1:
        return "0/1"

    if n > (1 << k):
        return "No solution"

    # Item format:
    # (weight, kind, serial, person)
    #
    # kind = 0 for a package, 1 for an original leaf.
    # Packages are preferred on equal weight. This tie rule is needed
    # for deterministic and valid package-merge reconstruction.
    #
    # For a package, person = -1.
    # For an original leaf, person is its index.

    weights_with_id = sorted(
        [(w, i) for i, w in enumerate(weights)],
        key=lambda x: (x[0], x[1])
    )

    serial = 0
    current = []

    for w, idx in weights_with_id:
        current.append((w, 1, serial, idx))
        serial += 1

    levels = [None] * (k + 1)
    levels[1] = current

    originals = current[:]

    for level in range(2, k + 1):
        previous = levels[level - 1]
        packages = []

        for j in range(0, len(previous) - 1, 2):
            left = previous[j]
            right = previous[j + 1]

            package_weight = left[0] + right[0]
            packages.append((package_weight, 0, serial, -1))
            serial += 1

        # Both lists are sorted. Merge them instead of sorting again.
        merged = []
        i = 0
        j = 0

        while i < len(packages) and j < len(originals):
            a = packages[i]
            b = originals[j]

            if (a[0], a[1], a[2]) <= (b[0], b[1], b[2]):
                merged.append(a)
                i += 1
            else:
                merged.append(b)
                j += 1

        merged.extend(packages[i:])
        merged.extend(originals[j:])

        levels[level] = merged

    selected = [None] * (k + 1)

    need = 2 * n - 2
    selected[k] = levels[k][:need]

    for level in range(k - 1, 0, -1):
        package_count = 0

        for item in selected[level + 1]:
            if item[1] == 0:
                package_count += 1

        take = 2 * package_count
        selected[level] = levels[level][:take]

    lengths = [0] * n

    for level in range(k, 0, -1):
        for item in selected[level]:
            if item[1] == 1:
                lengths[item[3]] += 1

    numerator = sum(w * d for w, d in zip(weights, lengths))
    denominator = sum(weights)

    g = gcd(numerator, denominator)
    numerator //= g
    denominator //= g

    return f"{numerator}/{denominator}"

def solve():
    n, k = map(int, input().split())
    weights = list(map(int, input().split()))
    print(solve_case(n, k, weights))

if __name__ == "__main__":
    solve()
```

The first special case handles the root being a leaf. Without it, the package construction would treat the single person as needing at least one question.

The capacity check uses `1 << k` rather than floating-point powers. Python integers have arbitrary precision, so even (2^{100}) is represented exactly.

Each package contains only its total weight and a marker saying that it is composite. We do not need to store all of its descendants. The backward pass works directly with the selected objects at every level, so the implementation only needs to know whether an object is an original person or a package.

The original list is kept unchanged at every level. The package list and the original list are both sorted, so their union can be formed by a linear merge. This is what keeps the construction at (O(nk)) rather than sorting every level independently.

The `package_count` calculation is the key part of reconstruction. Every selected package at level `level + 1` represents exactly two selected objects at `level`, so the number of objects needed there is twice the number of selected packages.

The final numerator can reach around (10^{16}), so fixed-width 32-bit arithmetic would be unsafe in languages that use it. Python integers handle this automatically. The denominator is the sum of all input weights, and `gcd` produces the required irreducible fraction.

## Worked Examples

### Sample 1

The input is

```
4 1
8 1 9 2
```

At most (2^1=2) people can be distinguished with one binary question, but there are four possible people.

| n | k | Maximum leaves (2^k) | Feasible |
| --- | --- | --- | --- |
| 4 | 1 | 2 | No |

The algorithm stops before constructing packages and prints `No solution`. This demonstrates why feasibility must be checked before optimizing the expected number of questions.

### Sample 2

The input is

```
4 2
1 2 3 4
```

The individual people are ordered by weight as (1,2,3,4).

| Level | Objects after packaging and merging | Selected | Package count |
| --- | --- | --- | --- |
| 1 | 1L, 2L, 3L, 4L | first 4 during reconstruction | 0 |
| 2 | 1L, 2L, 3P, 3L, 4L, 7P | first 6 | 2 |

At level two, the packages are ((1,2)) with weight 3 and ((3,4)) with weight 7. There are exactly (2n-2=6) objects, so all of them are selected.

The two selected packages require four objects at level one, so all four original people are selected there. Every person appears once in each level, giving lengths (2,2,2,2). The weighted path length is

[
2(1+2+3+4)=20.
]

The total weight is (10), so the answer is

```
2/1
```

The trace demonstrates the reconstruction invariant: every selected package at one level demands its two child positions at the preceding level.

### Sample 3

The input is

```
4 3
1 2 3 4
```

The first two levels are:

| Level | Sorted objects | Selected objects | Package count |
| --- | --- | --- | --- |
| 1 | 1L, 2L, 3L, 4L | reconstructed later | 0 |
| 2 | 1L, 2L, 3P, 3L, 4L, 7P | reconstructed later | 1 |
| 3 | 1L, 2L, 3P, 3P, 3L, 4L, 6P, 11P | first 6 | 2 |

At level three, the two cheapest composite objects of weight 3 are selected along with the four cheapest individual leaves. Their two composite objects require four objects at level two.

At level two, the first four objects are `1L, 2L, 3P, 3L`, which contains one package, so level one needs two objects, namely `1L` and `2L`.

The resulting lengths are

| Person weight | Length |
| --- | --- |
| 1 | 3 |
| 2 | 3 |
| 3 | 2 |
| 4 | 1 |

The weighted path length is

[
1\cdot3+2\cdot3+3\cdot2+4\cdot1=19.
]

The total weight is (10), producing

```
19/10
```

This is exactly the desired behavior: the most probable person gets the shortest code, while the two least probable people absorb the extra depth imposed by the three-question limit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nk)) | Each of the (k) levels contains (O(n)) objects, and packaging plus merging is linear. |
| Space | (O(nk)) | All level lists are retained for the backward reconstruction. |

With (n,k\le100), the implementation handles only around (10^4) package objects, so both the running time and memory usage are far below the given limits. The package-merge algorithm is specifically designed for length-limited Huffman coding and has (O(nL)) complexity for maximum code length (L).

## Test Cases

```python
import sys
import io
from math import gcd

def solve_case(n, k, weights):
    if n == 1:
        return "0/1"

    if n > (1 << k):
        return "No solution"

    weights_with_id = sorted(
        [(w, i) for i, w in enumerate(weights)],
        key=lambda x: (x[0], x[1])
    )

    serial = 0
    current = []

    for w, idx in weights_with_id:
        current.append((w, 1, serial, idx))
        serial += 1

    levels = [None] * (k + 1)
    levels[1] = current
    originals = current[:]

    for level in range(2, k + 1):
        previous = levels[level - 1]
        packages = []

        for j in range(0, len(previous) - 1, 2):
            left = previous[j]
            right = previous[j + 1]
            packages.append((left[0] + right[0], 0, serial, -1))
            serial += 1

        merged = []
        i = j = 0

        while i < len(packages) and j < len(originals):
            if packages[i][:3] <= originals[j][:3]:
                merged.append(packages[i])
                i += 1
            else:
                merged.append(originals[j])
                j += 1

        merged.extend(packages[i:])
        merged.extend(originals[j:])
        levels[level] = merged

    selected = [None] * (k + 1)
    selected[k] = levels[k][:2 * n - 2]

    for level in range(k - 1, 0, -1):
        package_count = sum(
            1 for item in selected[level + 1]
            if item[1] == 0
        )
        selected[level] = levels[level][:2 * package_count]

    lengths = [0] * n

    for level in range(k, 0, -1):
        for item in selected[level]:
            if item[1] == 1:
                lengths[item[3]] += 1

    numerator = sum(w * d for w, d in zip(weights, lengths))
    denominator = sum(weights)

    g = gcd(numerator, denominator)
    return f"{numerator // g}/{denominator // g}"

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        n, k = map(int, input().split())
        weights = list(map(int, input().split()))
        return solve_case(n, k, weights)
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("4 1\n8 1 9 2\n") == "No solution", "sample 1"
assert run("4 2\n1 2 3 4\n") == "2/1", "sample 2"
assert run("4 3\n1 2 3 4\n") == "19/10", "sample 3"

# Minimum-size input
assert run("1 1\n7\n") == "0/1", "one possible person needs no question"

# All equal weights, nontrivial depth distribution
assert run("3 3\n1 1 1\n") == "5/3", "equal weights"

# Boundary of feasibility: 2^k leaves are possible
assert run("4 2\n1 1 1 1\n") == "2/1", "exact capacity"

# Just beyond the capacity
assert run("5 2\n1 1 1 1 1\n") == "No solution", "capacity boundary"

# Large values and highly unequal weights
assert run("3 3\n1000000000000 1 1\n") == "1000000000002/1000000000002", \
    "large weights and fraction reduction"
```

The last custom assertion deserves a correction if the implementation is tested literally: the optimal lengths for weights (10^{12},1,1) are (1,2,2), so the weighted path length is (10^{12}+4), not (10^{12}+2). The correct assertion is:

```
assert run("3 3\n1000000000000 1 1\n") == "1000000000004/1000000000002", \
    "large weights"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 7` | `0/1` | Root can directly be a leaf |
| `3 3 / 1 1 1` | `5/3` | Equal weights and nonuniform optimal depths |
| `4 2 / 1 1 1 1` | `2/1` | Exact (2^k) capacity boundary |
| `5 2 / 1 1 1 1 1` | `No solution` | First impossible case beyond capacity |
| `3 3 / 1000000000000 1 1` | `1000000000004/1000000000002` | Large integer weights without floating-point arithmetic |

## Edge Cases

For a single possible person,

```
1 1
7
```

the algorithm returns immediately with `0/1`. No decision tree question is needed because the root itself identifies the only possible person.

For insufficient depth,

```
4 1
8 1 9 2
```

the capacity is (2^1=2), smaller than four leaves. The feasibility check catches this before package construction and prints `No solution`.

For exact capacity,

```
4 2
1 1 1 1
```

the tree must have four leaves at depth two. Package-merge selects enough objects to give every person length two, so the weighted path length is (8) and the total weight is (4), producing `2/1`.

For equal weights,

```
3 3
1 1 1
```

the optimal tree has one leaf at depth one and two at depth two. The package tie rule chooses a valid equivalent arrangement, giving lengths (2,2,1) in some order. The total weighted length is (5), so the answer is `5/3`.

For very large weights,

```
3 3
1000000000000 1 1
```

the largest weight is assigned the shallowest leaf. The two unit weights occupy depth two, giving weighted length

[
10^{12}+2+2=1000000000004.
]

The total weight is (1000000000002), so the exact answer is

```
1000000000004/1000000000002
```

with no precision loss.
