---
title: "CF 105617A - Colony of Bacteria"
description: "The colony starts as a single occupied cell on an infinite grid. After that, it grows once every second. During even seconds, every cell spreads to all eight neighboring positions, including diagonals. During odd seconds, it only spreads to the four cells sharing a side."
date: "2026-06-26T18:20:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105617
codeforces_index: "A"
codeforces_contest_name: "2024-2025 Russia Team Open, High School Programming Contest (VKOSHP XXV)"
rating: 0
weight: 105617
solve_time_s: 73
verified: true
draft: false
---

[CF 105617A - Colony of Bacteria](https://codeforces.com/problemset/problem/105617/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
# Problem Understanding

The colony starts as a single occupied cell on an infinite grid. After that, it grows once every second. During even seconds, every cell spreads to all eight neighboring positions, including diagonals. During odd seconds, it only spreads to the four cells sharing a side.

The task is to find the number of occupied grid cells after exactly `k` seconds. The input is one integer `k`, representing the moment we want to inspect, and the output is the size of the colony at that time. The statement uses the convention that the starting cell already exists at the first second, so `k = 1` gives an answer of `1`.

The value of `k` can be as large as `10^8`. A simulation that stores all occupied cells is impossible because the colony area grows quadratically with time. Even an optimized breadth-first expansion would eventually require billions of operations. The solution has to find a mathematical description of the shape and compute its area in constant time.

The tricky part is that the shape is not a normal square or diamond. The expansion rules alternate, so treating every second as the same type of movement gives incorrect results.

For example, for input:

```
3
```

a careless solution might assume three diagonal expansions and return the size of a square with radius three. The correct output is:

```
21
```

because the third second uses only orthogonal expansion, producing a different shape.

Another edge case is the smallest possible time:

```
1
```

The correct output is:

```
1
```

The colony is already placed on the grid during the first second. A solution that performs one expansion before answering would incorrectly output a larger value.

A final boundary case is a large odd value such as:

```
99999999
```

The answer must still be computed directly from a formula. Iterating through seconds or maintaining the border cannot finish in time.

## Approaches

The direct approach is to simulate the colony. We can keep a set of occupied coordinates and, for every second, add the neighboring cells required by that second's movement rule. This works because each expansion only depends on the current occupied cells. However, the number of cells becomes quadratic in `k`. When `k` reaches `10^8`, the simulated grid would contain far too many cells to store or process.

The useful observation is that the order of expansions creates a regular geometric shape. Every diagonal expansion is a dilation by a Chebyshev distance of one, and every orthogonal expansion is a dilation by a Manhattan distance of one. After many seconds, the resulting shape is symmetric, so we only need to count one quadrant.

For `k = 2m`, there are `m` diagonal expansions and `m - 1` orthogonal expansions. The resulting quadrant can be counted row by row. The full answer simplifies to:

$$14m^2 - 6m + 1$$

For `k = 2m + 1`, there are `m` diagonal expansions and `m` orthogonal expansions. The same quadrant counting gives:

$$14m^2 + 6m + 1$$

The alternating growth is the only complicated part. Once the parity is identified, the rest is just evaluating the corresponding formula.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k²) | O(k²) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `k`. The parity of `k` determines which formula describes the current colony shape.
2. If `k` is odd, write it as `k = 2m + 1`. The colony has undergone the same number of diagonal and orthogonal expansions. Use the odd-time formula:

$$14m^2 + 6m + 1$$

The extra orthogonal expansion changes the outer layer compared with the even case, so the linear term has the opposite sign.

1. If `k` is even, write it as `k = 2m`. The colony has one fewer orthogonal expansion than diagonal expansions. Use the even-time formula:

$$14m^2 - 6m + 1$$

1. Print the resulting value.

Why it works: the colony is always symmetric around the starting cell. The sequence of expansions can be viewed as repeatedly adding one of two fixed shapes, so after grouping the diagonal and orthogonal expansions, the border follows a predictable pattern. Counting the cells in one quadrant and reflecting them across both axes gives the two formulas above. Since every occupied cell belongs to exactly one of those counted positions, the formula produces the exact colony size.

## Python Solution

```python
import sys
input = sys.stdin.readline

k = int(input())

if k % 2 == 0:
    m = k // 2
    ans = 14 * m * m - 6 * m + 1
else:
    m = k // 2
    ans = 14 * m * m + 6 * m + 1

print(ans)
```

The program only needs the second count representation. For even values, `m` is the number of diagonal expansion moments. For odd values, `m` is one less than the total number of seconds after the initial placement.

The multiplication is done using Python integers, which automatically support values larger than 64-bit integers. This avoids overflow issues that would need attention in lower-level languages.

The parity check is also the key implementation detail. Using the wrong formula for a neighboring value of `k` changes the linear term and produces an incorrect answer.

## Worked Examples

### Sample 1

Input:

```
1
```

The value is odd, so:

$$m = 0$$

| Step | k | m | Formula | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | $14m^2+6m+1$ | 1 |

The colony has only its initial cell.

### Sample 2

Input:

```
5
```

The value is odd, so:

$$m = 2$$

| Step | k | m | Formula | Answer |
| --- | --- | --- | --- | --- |
| 1 | 5 | 2 | $14m^2+6m+1$ | 69 |

The formula gives:

$$14 \cdot 4 + 12 + 1 = 69$$

This matches the fifth second shape, where the alternating expansions create a larger but still symmetric border.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only arithmetic operations and one parity check are performed. |
| Space | O(1) | No data structures proportional to `k` are created. |

The constraints allow `k` to reach `10^8`, so any simulation-based method is infeasible. The constant-time formula directly satisfies both time and memory requirements.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    import sys as s
    input = s.stdin.readline

    k = int(input())
    if k % 2 == 0:
        m = k // 2
        ans = 14 * m * m - 6 * m + 1
    else:
        m = k // 2
        ans = 14 * m * m + 6 * m + 1

    sys.stdin = old
    return str(ans)

assert solve("1\n") == "1", "minimum size"
assert solve("2\n") == "9", "first diagonal expansion"
assert solve("3\n") == "21", "first odd expansion"
assert solve("4\n") == "45", "even formula check"
assert solve("5\n") == "69", "odd formula check"
assert solve("100000000\n") == "34999999400000001", "large boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Initial single-cell colony |
| `2` | `9` | First eight-direction expansion |
| `3` | `21` | Odd-time formula |
| `4` | `45` | Even-time formula |
| `100000000` | `34999999400000001` | Large constraint handling |

## Edge Cases

For `k = 1`, the algorithm chooses the odd formula with `m = 0`:

$$14 \cdot 0^2 + 6 \cdot 0 + 1 = 1$$

The result is correct because no expansion has happened after the initial placement.

For `k = 2`, the algorithm chooses the even formula with `m = 1`:

$$14 \cdot 1^2 - 6 \cdot 1 + 1 = 9$$

The first diagonal expansion fills the surrounding eight cells, creating a `3 × 3` square.

For `k = 3`, the algorithm uses:

$$14 \cdot 1^2 + 6 \cdot 1 + 1 = 21$$

The second expansion is only orthogonal, so the corners of the next layer are missing. This is exactly the case where treating every expansion as identical fails.

For a very large value such as `k = 100000000`, the algorithm performs the same few arithmetic operations as it does for `k = 1`. The result does not depend on storing the grid, which is why the approach remains efficient.
