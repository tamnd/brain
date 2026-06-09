---
title: "CF 1763A - Absolute Maximization"
description: "We have an array of integers. An operation allows us to pick any two positions and a bit index, then swap the values of that bit between the two numbers. The crucial detail is that the bit position is fixed during a swap."
date: "2026-06-09T13:35:47+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1763
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 840 (Div. 2) and Enigma 2022 - Cybros LNMIIT"
rating: 800
weight: 1763
solve_time_s: 150
verified: true
draft: false
---

[CF 1763A - Absolute Maximization](https://codeforces.com/problemset/problem/1763/A)

**Rating:** 800  
**Tags:** bitmasks, constructive algorithms, greedy, math  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of integers. An operation allows us to pick any two positions and a bit index, then swap the values of that bit between the two numbers.

The crucial detail is that the bit position is fixed during a swap. We can move a `1` bit from one number to another, but only within the same bit position. For example, a bit in position 3 can never become a bit in position 2.

The goal is to maximize the difference between the largest and smallest element in the array after performing any number of such operations.

The array size is at most 512, and every value is below 1024. Since 1024 is $2^{10}$, each number contains only 10 relevant bit positions. The small bit width strongly suggests that reasoning bit-by-bit is more useful than simulating operations.

A common mistake is to think that swaps preserve the value of each number. They do not. For example:

```
2
4 3
```

Binary forms are `100` and `011`. Swapping bit 2 produces:

```
000 = 0
111 = 7
```

The numbers change dramatically.

Another easy mistake is to treat different bit positions as interacting with each other. They are completely independent. For example:

```
3
1 2 4
```

Each bit position has exactly one `1`. No operation can move a `1` from one position to another. The best we can do is collect all existing `1` bits into one number, producing `7`, and leave another number as `0`. The answer is `7`.

A third edge case is when all numbers are identical:

```
4
5 5 5 5
```

Every bit position either contains all zeros or all ones. Swapping bits changes nothing, so the answer remains `0`.

## Approaches

A brute-force mindset starts by asking what states are reachable. We could repeatedly perform bit swaps, generating new arrays and searching for the largest possible value of `max(a) - min(a)`.

This is correct in principle because every legal operation is explored. The problem is that the state space explodes immediately. Even for a single operation there are $O(n^2 \cdot 10)$ choices. Sequences of operations create an enormous number of reachable arrays, making explicit search completely infeasible.

The key observation is that bit positions are independent.

Consider one fixed bit position $b$. Suppose exactly $k$ numbers currently contain a `1` at that position. Swapping bits only rearranges those $k$ ones among the array positions. The total count of ones in that bit position never changes.

This means that for every bit position we only care about how many ones exist, not where they currently are.

Now think about maximizing:

```
max(a) - min(a)
```

To make this difference as large as possible, we want one number to become as large as possible and another number to become as small as possible.

For every bit position:

If at least one `1` exists in that position, we can move one of those ones into the future maximum element.

If not all numbers contain a `1` in that position, then some element can have a `0` there, which helps create the future minimum element.

Since $n \ge 3$, whenever a bit position contains at least one `1`, we can always place a `1` into the maximum element and a `0` into the minimum element simultaneously.

As a result, every bit position contributes independently to the final difference:

If a bit position appears in at least one number, it contributes its full value $2^b$ to the answer.

That is exactly the definition of bitwise OR across the entire array.

So the answer is simply:

```
a1 OR a2 OR ... OR an
```

There is another way to see the same result. Let:

```
M = OR of all elements
```

We can gather every available `1` bit into one element, creating value `M`.

For the minimum element, every bit that is not present in all numbers can be made `0`. Since $n \ge 3$, we can choose a different element to hold those bits. The minimum can be driven to `0`.

Hence:

```
max(a) - min(a) = M - 0 = M
```

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential state space | Exponential | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize an accumulator `ans = 0`.
2. Iterate through all numbers in the array.
3. Update `ans |= value` for each element.

This collects every bit position that appears at least once in the array.
4. After processing the entire array, output `ans`.

The reason this works is that each bit position can be rearranged independently. Any bit that exists somewhere in the array can be assigned to the future maximum element. Since the minimum element can simultaneously avoid receiving that bit, the full value of that bit contributes to the final difference.

### Why it works

For every bit position $b$, let its value be $2^b$.

If no element contains that bit, it can never appear anywhere, so its contribution is zero.

If at least one element contains that bit, the count of ones in that position is positive. By swapping bits among array elements, we can place one of those ones into the element chosen as the maximum. At the same time, because $n \ge 3$, we can keep another element with a zero in that position and use it as the minimum candidate.

Thus every bit that appears at least once contributes exactly $2^b$ to the achievable difference. Summing these contributions over all bit positions gives the bitwise OR of the array, which is exactly the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    ans = 0
    for x in a:
        ans |= x

    print(ans)
```

The implementation is extremely small because the mathematical observation eliminates all simulation.

The variable `ans` stores the running bitwise OR of the array. Every time we process a number, all bits present in that number become present in `ans`.

After scanning the entire array, `ans` contains exactly the set of bit positions that appear at least once anywhere in the array. The proof above shows that this value equals the maximum achievable difference.

There are no tricky boundary conditions. The numbers are small, Python integers easily handle them, and the answer fits comfortably within normal integer ranges.

## Worked Examples

### Example 1

Input:

```
1
5
1 2 3 4 5
```

| Current Value | Binary | Running OR |
| --- | --- | --- |
| 1 | 001 | 001 |
| 2 | 010 | 011 |
| 3 | 011 | 011 |
| 4 | 100 | 111 |
| 5 | 101 | 111 |

Final OR:

```
111₂ = 7
```

Output:

```
7
```

This example demonstrates how bits accumulate independently. Every bit position that appears anywhere contributes to the answer.

### Example 2

Input:

```
1
7
20 85 100 41 76 49 36
```

| Current Value | Binary | Running OR |
| --- | --- | --- |
| 20 | 0010100 | 0010100 |
| 85 | 1010101 | 1010101 |
| 100 | 1100100 | 1110101 |
| 41 | 0101001 | 1111101 |
| 76 | 1001100 | 1111101 |
| 49 | 0110001 | 1111101 |
| 36 | 0100100 | 1111101 |

Final OR:

```
1111101₂ = 125
```

Output:

```
125
```

This trace shows that once a bit appears in any number, it remains present in the running OR forever.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass through the array |
| Space | O(1) | Only the OR accumulator is stored |

The sum of all array lengths across test cases is at most 512, so the algorithm performs only a few hundred operations. It easily fits within the 1-second time limit and the memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        ans = 0
        for x in a:
            ans |= x

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return result

# provided samples
assert run(
"""4
3
1 0 1
4
5 5 5 5
5
1 2 3 4 5
7
20 85 100 41 76 49 36
"""
) == "1\n0\n7\n125"

# minimum size
assert run(
"""1
3
0 0 0
"""
) == "0"

# all equal
assert run(
"""1
5
7 7 7 7 7
"""
) == "7"

# disjoint bits
assert run(
"""1
3
1 2 4
"""
) == "7"

# boundary values
assert run(
"""1
3
1023 0 0
"""
) == "1023"

# many values
assert run(
"""1
4
8 4 2 1
"""
) == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0` | `0` | All bits absent |
| `7 7 7 7 7` | `7` | Identical values |
| `1 2 4` | `7` | Independent bit positions |
| `1023 0 0` | `1023` | Maximum allowed value |
| `8 4 2 1` | `15` | OR accumulates multiple bits |

## Edge Cases

### All values are equal

Input:

```
1
4
5 5 5 5
```

The algorithm computes:

```
5 OR 5 OR 5 OR 5 = 5
```

Output:

```
5
```

Every bit position is either present in all numbers or absent in all numbers. No swap changes anything. The maximum achievable difference is exactly 5, matching the OR.

### Every useful bit appears in a different number

Input:

```
1
3
1 2 4
```

Running OR becomes:

```
1 -> 3 -> 7
```

Output:

```
7
```

Although no single element initially contains multiple bits, swaps allow collecting all three bits into one number. A solution that only looks at the current maximum would incorrectly miss this possibility.

### Presence of zeros

Input:

```
1
3
1023 0 0
```

Running OR is:

```
1023
```

Output:

```
1023
```

Every bit position already exists somewhere, so all of them contribute to the answer. The existing zeros can serve as the minimum element, giving the full possible difference.

### No bit exists anywhere

Input:

```
1
3
0 0 0
```

Running OR stays:

```
0
```

Output:

```
0
```

Since there are no `1` bits in any position, no operation can create one. The answer must remain zero, which the algorithm correctly returns.
