---
title: "CF 102569K - Table"
description: "We have four bars that will become the four legs of a table. Their lengths determine the heights of the four corners of the tabletop because each leg reaches from the floor to the surface."
date: "2026-07-31T07:58:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102569
codeforces_index: "K"
codeforces_contest_name: "2020, XIII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102569
solve_time_s: 158
verified: true
draft: false
---

[CF 102569K - Table](https://codeforces.com/problemset/problem/102569/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have four bars that will become the four legs of a table. Their lengths determine the heights of the four corners of the tabletop because each leg reaches from the floor to the surface. The question is whether we can place these four heights at the corners of some rectangle so that one flat tabletop plane passes through all four endpoints.

A plane over a rectangle has a special structure. If we look at the four corners, the height changes independently along the two rectangle directions. This means the four corner heights cannot be arbitrary. The task is to decide whether the given four numbers can be arranged to satisfy that geometric condition. The output is `YES` if such an arrangement exists and `NO` otherwise.

Each bar length can be as large as $10^9$, but there are only four bars. The size of the values rules out approaches that depend on trying possible lengths or using coordinate-based simulation. Since the number of elements is fixed, the solution should rely on mathematical properties of the four values rather than on searching through a large state space. Sorting or checking a constant number of arrangements is easily within the limit.

The main edge cases come from assuming that the bars must all have the same length or that only equal pairs work. A careless implementation may miss valid sloping tables or accept invalid sets.

For example, the input `1 3 2 2` should produce `YES`. The four heights can be placed so that the opposite corners have equal sums: $1+3=2+2$. A solution that only accepts four equal values or two pairs of equal values would incorrectly reject this case.

Another case is `1 2 3 10`, which should produce `NO`. The smallest and largest values sum to $11$, while the middle values sum to $5$. No placement can make the opposite corner sums match, so no plane can pass through all four endpoints.

The case `5 5 5 5` should produce `YES`. A flat tabletop is simply a special case of a sloped tabletop, so requiring a nonzero slope would incorrectly reject this input.

## Approaches

A direct approach is to try every possible assignment of the four bars to the four rectangle corners. There are only $4! = 24$ permutations. For each arrangement, we can check whether the opposite corners have the same total height. This works because every valid rectangle placement corresponds to one of these assignments, so trying all of them cannot miss a solution.

The brute force approach is already fast enough because 24 checks is a constant amount of work. However, it hides the underlying structure. The real observation is that the four corner heights of any plane over a rectangle always satisfy a simple equality.

Suppose the rectangle corners have heights $x_1, x_2, x_3, x_4$, where opposite corners are paired. Moving across one rectangle direction adds the same amount to the height, and moving across the other direction also adds the same amount. The four values can be represented as:

$$c,\quad c+a,\quad c+b,\quad c+a+b$$

The sum of the first and last values is:

$$c + (c+a+b) = 2c+a+b$$

The sum of the two remaining values is:

$$(c+a)+(c+b)=2c+a+b$$

So the two opposite-corner sums must be equal. After sorting the four values as $a \leq b \leq c \leq d$, the only possible pairing of opposite corners is the smallest with the largest and the two middle values together. The condition becomes:

$$a+d=b+c$$

This gives a direct constant-time solution after sorting.

The brute-force method works because the search space contains only 24 possible layouts, but the equation above compresses all those checks into one comparison. The geometric constraint turns into an arithmetic property of the sorted values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(4!) | O(1) | Accepted, but unnecessary search |
| Optimal | O(4 log 4) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four bar lengths and sort them. Let the sorted values be $a, b, c, d$. Sorting removes the need to think about all possible placements because the smallest and largest values must form one opposite pair in any valid arrangement.
2. Check whether $a+d=b+c$. This compares the two possible opposite-corner sums after ordering the values. If they are equal, the four heights can be arranged as the corners of a rectangle with a plane touching all of them.
3. Print `YES` when the equality holds and `NO` otherwise. The equality is both necessary and sufficient, so there is no additional geometry to verify.

Why it works:

For any plane placed over a rectangle, the corner heights have the form $c, c+a, c+b, c+a+b$. The opposite corners always have equal sums, so every valid table must satisfy the sorted equality $a+d=b+c$. Conversely, if the equality holds, choose the sorted values as $a,b,c,d$ placed around the rectangle in that order. The differences between adjacent corners define consistent changes along the two rectangle directions, so a plane exists through all four points. The condition exactly characterizes valid tables.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a = list(map(int, input().split()))
    a.sort()

    if a[0] + a[3] == a[1] + a[2]:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()
```

The solution reads the four heights and sorts them so the geometric relationship can be checked without considering individual placements. The comparison uses the smallest and largest values on one side and the two middle values on the other side.

Python integers handle values up to $2 \times 10^9$ without any overflow issue, even though the input values themselves can reach $10^9$. There are no index boundary concerns because the array always contains exactly four numbers.

The order of operations matters because the formula relies on sorted positions. Checking the original order would only test one arbitrary placement and could reject a valid arrangement.

## Worked Examples

For the first sample, the input is `1 1 1 1`.

| Sorted values | Left side $a+d$ | Right side $b+c$ | Decision |
| --- | --- | --- | --- |
| 1, 1, 1, 1 | 2 | 2 | YES |

All four corners have the same height, so the tabletop is flat. The equality holds because both opposite-corner sums are identical.

For the second sample, the input is `1 5 1 5`.

| Sorted values | Left side $a+d$ | Right side $b+c$ | Decision |
| --- | --- | --- | --- |
| 1, 1, 5, 5 | 6 | 6 | YES |

The two shorter legs can occupy opposite corners, and the two taller legs occupy the other opposite corners. The equal sums allow the surface to be a sloped plane.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Sorting four numbers takes a fixed amount of work |
| Space | O(1) | Only four integers are stored |

The constraints are easily satisfied because the algorithm does not depend on the size of the values. It performs only a few arithmetic operations after sorting a fixed-size array.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    data = list(map(int, inp.split()))
    data.sort()
    return "YES\n" if data[0] + data[3] == data[1] + data[2] else "NO\n"

def run(inp: str) -> str:
    return solution(inp)

assert run("1 1 1 1") == "YES\n", "sample 1"
assert run("1 5 1 5") == "YES\n", "sample 2"
assert run("1 3 2 2") == "YES\n", "sample 3"

assert run("1 2 3 10") == "NO\n", "invalid opposite sums"
assert run("1000000000 1000000000 1000000000 1000000000") == "YES\n", "maximum equal values"
assert run("1 1 1 2") == "NO\n", "single different leg"
assert run("1 2 2 3") == "YES\n", "minimum non-flat slope"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3 10` | `NO` | Rejects cases where no opposite corner pairing works |
| `1000000000 1000000000 1000000000 1000000000` | `YES` | Handles maximum values and flat tables |
| `1 1 1 2` | `NO` | Checks that one unmatched height is not enough |
| `1 2 2 3` | `YES` | Confirms valid sloped surfaces with repeated middle values |

## Edge Cases

The input `1 3 2 2` demonstrates why equal pairs are not required. After sorting, the values become `1,2,2,3`. The algorithm checks $1+3=2+2$, which is true, so it returns `YES`. The corresponding tabletop is sloped because the heights are not all equal.

The input `1 2 3 10` demonstrates an invalid arrangement. Sorting gives `1,2,3,10`, and the algorithm checks $1+10=2+3$. Since `11` is not equal to `5`, the required plane cannot exist, so the answer is `NO`.

The input `5 5 5 5` demonstrates the flat-table case. Sorting leaves the values unchanged, and both sides of the equation equal `10`. The algorithm accepts it because a horizontal surface is simply a plane with zero slope.
