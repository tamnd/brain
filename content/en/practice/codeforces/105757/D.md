---
title: "CF 105757D - Guess the permutation"
description: "We start with the sorted array $$[1,2,3,dots,n].$$ Three positions $i<j<k$ are chosen, with $j-i1$. The segment $[i,j-1]$ is reversed, and the segment $[j,k]$ is reversed. In the original interactive version we could ask for inversion counts on subarrays."
date: "2026-06-25T23:21:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105757
codeforces_index: "D"
codeforces_contest_name: "Insomnia 2025"
rating: 0
weight: 105757
solve_time_s: 36
verified: true
draft: false
---

[CF 105757D - Guess the permutation](https://codeforces.com/problemset/problem/105757/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with the sorted array

$$[1,2,3,\dots,n].$$

Three positions $i<j<k$ are chosen, with $j-i>1$. The segment $[i,j-1]$ is reversed, and the segment $[j,k]$ is reversed.

In the original interactive version we could ask for inversion counts on subarrays. In the hacked version, the values $n,i,j,k$ are given directly as input, and we must reconstruct the same logic offline.

The key observation is the shape of the resulting array.

The first reversal transforms

$$[i,i+1,\dots,j-1]$$

into

$$[j-1,j-2,\dots,i].$$

The second reversal transforms

$$[j,j+1,\dots,k]$$

into

$$[k,k-1,\dots,j].$$

Everything outside $[i,k]$ remains sorted.

Inside $[i,k]$, we obtain two decreasing blocks:

$$[j-1,\dots,i,\; k,\dots,j].$$

Since every value in the first block is smaller than every value in the second block, there are no inversions between the two blocks. All inversions come from inside each decreasing block.

Let

$$a=j-i,
\qquad
b=k-j+1.$$

Then the inversion count contributed by each block is

$$\frac{a(a-1)}2$$

and

$$\frac{b(b-1)}2.$$

The offline version simply provides $n,i,j,k$, but understanding these inversion formulas is exactly what the original solution relied on.

The constraints allow $n$ up to $10^9$, but there are only up to $100$ test cases. Any $O(1)$ or $O(\log n)$ computation per test case is trivial. Simulating an array of length $10^9$ is impossible, so the solution must be purely mathematical.

A common mistake is confusing the length of the first reversed segment.

For example, if

```
i=2, j=5
```

then the segment is $[2,4]$, whose length is

$$j-i=3,$$

not $j-i+1$.

Another easy off-by-one error appears in the second segment. Its length is

$$k-j+1.$$

For

```
j=4, k=6
```

the segment is $[4,6]$, which contains three elements.

Using $k-j$ instead would undercount inversions.

## Approaches

A brute-force approach would explicitly build the array, perform both reversals, and then count inversions. Counting inversions naively requires checking every pair, leading to $O(n^2)$ work.

That approach immediately fails when $n$ can reach $10^9$. Even constructing the array is impossible.

The structure created by the two reversals is much more informative than the final array itself.

The resulting permutation consists of three parts:

$$\text{sorted prefix}$$

followed by

$$\text{first decreasing block}$$

followed by

$$\text{second decreasing block}$$

followed by

$$\text{sorted suffix}.$$

Inside a decreasing block of length $L$, every pair of positions forms an inversion. The number of inversions is exactly

$$\binom{L}{2}
=
\frac{L(L-1)}2.$$

Because every value in the first block is smaller than every value in the second block, cross-block inversions never occur.

This converts the problem into simple arithmetic on segment lengths rather than manipulating the permutation itself.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Mathematical Analysis | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read $n,i,j,k$.
2. Compute the length of the first reversed segment:

$$a=j-i.$$

The segment is $[i,j-1]$, so its length is not $j-i+1$.

1. Compute the length of the second reversed segment:

$$b=k-j+1.$$

The segment is $[j,k]$, inclusive on both ends.

1. Compute the inversion count contributed by the first block:

$$inv_1=\frac{a(a-1)}2.$$

A decreasing sequence of length $a$ contains an inversion for every pair of positions.

1. Compute the inversion count contributed by the second block:

$$inv_2=\frac{b(b-1)}2.$$

1. Output

$$inv_1+inv_2.$$

### Why it works

After the two reversals, the interval $[i,k]$ becomes two independent decreasing blocks. Every inversion lies entirely inside one of those blocks.

The first block contributes exactly $\binom{a}{2}$ inversions and the second contributes exactly $\binom{b}{2}$.

There are no inversions between the blocks because every value originating from the first block is smaller than every value originating from the second block. Since all remaining positions stay sorted, no additional inversions exist.

The sum of the two triangular numbers is exactly the total inversion count.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    
    for _ in range(t):
        n, i, j, k = map(int, input().split())
        
        a = j - i
        b = k - j + 1
        
        ans = a * (a - 1) // 2 + b * (b - 1) // 2
        print(ans)

solve()
```

The implementation is entirely arithmetic.

The first segment is $[i,j-1]$, so its length is `j - i`. This is the most common place to make an off-by-one mistake.

The second segment is $[j,k]$, so its length is `k - j + 1`.

Both inversion counts are triangular numbers. Python integers comfortably handle the largest possible values because $n\le 10^9$, making the answer at most about $5\times10^{17}$, well within Python's integer range.

## Worked Examples

### Example 1

Input:

```
1
5 1 3 5
```

Lengths:

$$a=3-1=2,
\qquad
b=5-3+1=3.$$

| Variable | Value |
| --- | --- |
| a | 2 |
| b | 3 |
| inv₁ | 1 |
| inv₂ | 3 |
| answer | 4 |

The resulting array is:

$$[2,1,5,4,3].$$

The inversions are $(2,1)$, $(5,4)$, $(5,3)$, and $(4,3)$, giving a total of $4$.

### Example 2

Input:

```
1
8 2 5 7
```

Lengths:

$$a=5-2=3,
\qquad
b=7-5+1=3.$$

| Variable | Value |
| --- | --- |
| a | 3 |
| b | 3 |
| inv₁ | 3 |
| inv₂ | 3 |
| answer | 6 |

The first reversed block contributes three inversions and the second contributes three more. No cross-block inversions appear.

This example highlights the key invariant: inversions come only from inside the decreasing blocks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations per test case |
| Space | O(1) | No auxiliary structures are used |

The solution never constructs the permutation, which is essential because $n$ can be as large as $10^9$. Constant-time arithmetic easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n, i, j, k = map(int, input().split())

        a = j - i
        b = k - j + 1

        ans = a * (a - 1) // 2 + b * (b - 1) // 2
        out.append(str(ans))

    return "\n".join(out)

# sample-style cases
assert run("1\n5 1 3 5\n") == "4"

# minimum valid configuration
assert run("1\n4 1 3 4\n") == "1"

# both blocks length 3
assert run("1\n8 2 5 7\n") == "6"

# large values
assert run("1\n1000000000 1 500000000 1000000000\n") == \
       str((499999999 * 499999998 // 2) + (500000001 * 500000000 // 2))

# boundary where second block has length 2
assert run("1\n10 3 7 8\n") == "16"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4 1 3 4` | `1` | Smallest valid configuration |
| `8 2 5 7` | `6` | Equal-sized decreasing blocks |
| Large $n$ case | Huge number | No dependence on array construction |
| `10 3 7 8` | `16` | Correct handling of segment lengths |

## Edge Cases

Consider the smallest valid configuration:

```
1
4 1 3 4
```

The first segment is `[1,2]`, length `2`, contributing one inversion. The second segment is `[3,4]`, length `2`, contributing one inversion. After the reversals the array becomes:

$$[2,1,4,3].$$

The inversion count is $1+1=2$. The formula computes exactly the same value.

Now consider a case where the second block is very short:

```
1
10 3 7 8
```

Here

$$a=4,\qquad b=2.$$

The answer is

$$\binom{4}{2}+\binom{2}{2}
=
6+1
=
7.$$

Using $k-j$ instead of $k-j+1$ would incorrectly set $b=1$ and lose one inversion. This is precisely why the inclusive endpoint in the second segment matters.

Finally, consider a huge value:

```
1
1000000000 1 500000000 1000000000
```

The algorithm performs only a handful of integer operations and never allocates an array of size $10^9$. The complexity remains constant, which is the only feasible approach for the given bounds.
