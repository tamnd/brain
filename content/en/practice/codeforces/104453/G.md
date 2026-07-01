---
title: "CF 104453G - \u0421\u0431\u043e\u0440 \u0443\u0440\u043e\u0436\u0430\u044f"
description: "We are given several types of crops. For each crop type, we know how many kilograms were harvested and how much a single storage box can hold for that specific crop. The key restriction is that boxes are crop-specific, meaning you cannot mix different crops inside the same box."
date: "2026-06-30T14:35:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104453
codeforces_index: "G"
codeforces_contest_name: "ICPC Central Russia Regional Qualyfing Round, 2021"
rating: 0
weight: 104453
solve_time_s: 76
verified: true
draft: false
---

[CF 104453G - \u0421\u0431\u043e\u0440 \u0443\u0440\u043e\u0436\u0430\u044f](https://codeforces.com/problemset/problem/104453/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several types of crops. For each crop type, we know how many kilograms were harvested and how much a single storage box can hold for that specific crop. The key restriction is that boxes are crop-specific, meaning you cannot mix different crops inside the same box.

For each crop, we must determine how many identical boxes are needed to store all harvested weight of that crop. Since boxes are indivisible units, any leftover weight that does not fully fill a box still requires an additional box. After computing this per crop, we sum the number of boxes across all crops.

The input size can be up to 100,000 crops. This immediately rules out any approach that simulates filling boxes item by item or iterates over kilograms. Any solution must process each crop in constant time, giving an overall linear O(n) complexity.

A subtle edge case appears when the total harvested amount is exactly divisible by the box capacity. For example, if 20 kg is stored in boxes of size 4 kg, the answer is exactly 5 boxes. But if 21 kg is stored in boxes of size 4 kg, the answer is 6 boxes. A naive integer division without ceiling handling would incorrectly compute 5 in the second case.

Another corner case is when n equals zero. In this case, there are no crops, hence no boxes are needed, and the correct output is 0.

## Approaches

The most direct way to think about the problem is to handle each crop independently and simulate packing its harvest into boxes. For a single crop, we could repeatedly subtract the box capacity from the remaining weight and count how many times we do this until nothing remains. This correctly models the real process but is far too slow in the worst case. If a crop has 100,000 kg and box size is 1 kg, this simulation performs 100,000 operations for just one crop, and across 100,000 crops this becomes 10^10 operations, which is completely infeasible.

The key observation is that each crop is independent and follows a simple arithmetic structure. We are essentially computing how many groups of size b_i are needed to cover a_i items. This is exactly a ceiling division problem. Instead of simulating grouping, we can compute the number of full boxes directly using integer arithmetic.

For each crop, the number of boxes is:

ceil(a_i / b_i)

This can be computed efficiently as:

(a_i + b_i - 1) // b_i

This transformation works because adding b_i - 1 ensures that any non-zero remainder pushes the division up by one full box, while exact multiples remain unchanged.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation | O(total a_i / b_i) | O(1) | Too slow |
| Per-crop ceiling division | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of crop types n. If n is zero, the answer is immediately zero because there is nothing to store.
2. Initialize an accumulator variable total_boxes to zero. This will store the sum of required boxes across all crops.
3. For each crop i, read the pair (a_i, b_i), representing harvested weight and box capacity.
4. Compute the number of boxes needed for this crop using ceiling division: (a_i + b_i - 1) // b_i. This ensures that even partially filled final boxes are counted.
5. Add this value to total_boxes. Each crop contributes independently, so summation is valid without interaction between crops.
6. After processing all crops, output total_boxes.

### Why it works

Each crop reduces to a one-dimensional packing problem where we partition a fixed quantity a_i into groups of size b_i. Any valid packing must use at least floor(a_i / b_i) full boxes, and if a remainder exists, one additional box is unavoidable because we cannot split boxes or mix crops. The formula (a_i + b_i - 1) // b_i exactly captures this lower bound and no solution can use fewer boxes, making it both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    total = 0

    for _ in range(n):
        a, b = map(int, input().split())
        total += (a + b - 1) // b

    print(total)

if __name__ == "__main__":
    solve()
```

The solution reads each crop once and immediately converts it into its required number of boxes. The expression (a + b - 1) // b is the standard integer trick for ceiling division and avoids floating-point arithmetic entirely, which keeps the computation both fast and safe.

The accumulator total is maintained as a single integer, and since each operation is O(1), the overall complexity remains linear.

## Worked Examples

### Sample 1

Input:

```
3
10 2
20 4
40 3
```

We process each crop independently.

| Crop | a | b | Computation | Boxes |
| --- | --- | --- | --- | --- |
| 1 | 10 | 2 | (10+1)//2 = 11//2 | 5 |
| 2 | 20 | 4 | (20+3)//4 = 23//4 | 5 |
| 3 | 40 | 3 | (40+2)//3 = 42//3 | 14 |

Total boxes = 5 + 5 + 14 = 24.

This confirms that each crop is independent and the total is simply a sum of ceiling divisions.

### Sample 2

Input:

```
6
7 10
1 8
6 3
3 6
1 6
1 1
```

| Crop | a | b | Computation | Boxes |
| --- | --- | --- | --- | --- |
| 1 | 7 | 10 | (7+9)//10 = 16//10 | 1 |
| 2 | 1 | 8 | (1+7)//8 = 8//8 | 1 |
| 3 | 6 | 3 | (6+2)//3 = 8//3 | 2 |
| 4 | 3 | 6 | (3+5)//6 = 8//6 | 1 |
| 5 | 1 | 6 | (1+5)//6 = 6//6 | 1 |
| 6 | 1 | 1 | (1+0)//1 = 1//1 | 1 |

Total boxes = 7.

This example stresses both extremes: very small capacities and exact divisions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each crop is processed in constant time using one arithmetic operation |
| Space | O(1) | Only a running sum is stored regardless of input size |

The algorithm easily handles n up to 100,000 because it performs only a few integer operations per input line, well within typical contest limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""3
10 2
20 4
40 3
""") == "24"

assert run("""6
7 10
1 8
6 3
3 6
1 6
1 1
""") == "7"

# minimum input
assert run("0\n") == "0"

# exact division case
assert run("""2
10 5
20 4
""") == str((10//5) + ((20+3)//4))

# large remainder case
assert run("1\n100000 99999\n") == "2"

# all ones
assert run("""4
1 1
1 1
1 1
1 1
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=0 | 0 | empty case |
| 10 5, 20 4 | 2 + 5 | mixed exact and remainder division |
| 100000 99999 | 2 | large near-bound capacity |
| all 1 1 | 4 | uniform minimal case |

## Edge Cases

For n = 0, the loop never executes and total remains zero, so the output is correct without special handling.

For a crop where a_i is exactly divisible by b_i, such as 20 and 4, the formula gives (20 + 3) // 4 = 23 // 4 = 5, matching the expected exact packing. There is no extra box added because the remainder is zero and the addition of b_i - 1 does not cross a multiple of b_i.

For a crop like 7 and 10, where the harvest is smaller than the box capacity, (7 + 9) // 10 = 16 // 10 = 1, correctly reflecting that even a partially filled box is still required.
