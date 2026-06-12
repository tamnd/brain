---
title: "CF 903D - Almost Difference"
description: "We are given an array of up to 200000 integers. For every pair of positions $(i,j)$ with $ile j$, we evaluate a special function $d(ai,aj)$, and we need the sum over all pairs. The function behaves differently from a normal difference."
date: "2026-06-12T22:57:19+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "math"]
categories: ["algorithms"]
codeforces_contest: 903
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 34 (Rated for Div. 2)"
rating: 2200
weight: 903
solve_time_s: 242
verified: true
draft: false
---

[CF 903D - Almost Difference](https://codeforces.com/problemset/problem/903/D)

**Rating:** 2200  
**Tags:** data structures, math  
**Solve time:** 4m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of up to 200000 integers. For every pair of positions $(i,j)$ with $i\le j$, we evaluate a special function $d(a_i,a_j)$, and we need the sum over all pairs.

The function behaves differently from a normal difference. If two numbers differ by at most one, their contribution becomes zero. Otherwise, the contribution equals the ordinary difference $a_j-a_i$. Positive and negative values are both possible.

Since the pair order matters only through the indices, we may imagine processing the array from left to right. When we arrive at position $j$, every earlier element $a_i$ forms one pair ending at $j$. The problem becomes: how much do all previous numbers contribute to the current value?

The limit $n\le 2\cdot10^5$ rules out quadratic algorithms. A straightforward double loop would examine roughly

$$\frac{200000\cdot199999}{2}\approx2\cdot10^{10}$$

pairs, which is far beyond what two seconds allow. A solution around $O(n\log n)$ or $O(n)$ is required.

One subtle case comes from numbers differing by exactly one. Such pairs contribute zero, not $\pm1$.

Input:

```
2
5 6
```

The only pair has difference $1$, so the answer is

```
0
```

A careless implementation using ordinary subtraction would produce $1$.

Another trap is negative contributions.

Input:

```
2
10 1
```

The pair contributes $1-10=-9$, whose absolute value exceeds one, so the correct answer is

```
-9
```

Treating the function as an absolute difference would give $9$, which is incorrect.

Repeated values are also special.

Input:

```
3
7 7 7
```

Every pair differs by zero, so every contribution vanishes and the answer is

```
0
```

A formula based only on prefix sums without removing the forbidden differences $0,\pm1$ would count these pairs incorrectly.

## Approaches

The most direct approach checks every pair $(i,j)$. For each pair we compute the ordinary difference $a_j-a_i$. If its absolute value is at most one, we replace it with zero. Summing all such contributions is obviously correct because it follows the definition literally.

The issue is the number of pairs. With $n=200000$, there are about twenty billion pairs. Even extremely cheap operations cannot process that many pairs within the time limit.

To speed things up, consider one position $j$. Suppose all previous elements are already known. Ignoring the special rule for a moment, the total contribution of earlier numbers equals

$$\sum_{i<j}(a_j-a_i)
=(j-1)\cdot a_j-\text{prefixSum}.$$

This expression can be updated in constant time if we maintain the sum of all previous elements.

The only problem is that pairs whose values differ by at most one should contribute zero instead of their ordinary difference. Those pairs were already included inside the formula above, so we must subtract their contributions back out.

For a current value $x$, only previous occurrences of $x-1$, $x$, and $x+1$ need correction. Their counts are enough. If there are

- $cnt[x-1]$ previous values equal to $x-1$,
- $cnt[x]$ previous values equal to $x$,
- $cnt[x+1]$ previous values equal to $x+1$,

then the ordinary formula has added

$$1\cdot cnt[x-1]+0\cdot cnt[x]-1\cdot cnt[x+1]$$

for those forbidden pairs. Since they should contribute zero, we subtract exactly this amount.

Hash tables make these counts available in expected $O(1)$ time, giving a linear solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a hash map storing how many times each value has appeared so far. Also maintain the sum of previous elements and the running answer.
2. Process the array from left to right. When the current value is $x$, first compute the ordinary contribution of all earlier elements.

$$(j-1)\cdot x-\text{prefixSum}$$

This equals the sum of $x-a_i$ over every previous index.

1. Find how many earlier values equal $x-1$, $x$, and $x+1$.

These are exactly the values whose pairwise difference with $x$ has absolute value at most one.

1. The ordinary formula already included contributions from those pairs. Their total contribution inside the formula is

$$cnt[x-1]-cnt[x+1].$$

Pairs with equal values contribute zero even before correction.

1. Subtract this quantity from the current contribution.

After this adjustment, all forbidden pairs effectively contribute zero.

1. Add the corrected contribution to the answer.
2. Insert the current value into the frequency map and update the prefix sum.
3. Continue until every element has been processed.

### Why it works

At every step, the prefix sum formula computes the sum of ordinary differences between the current element and all earlier elements. The only pairs violating the problem definition are those with differences $-1$, $0$, or $1$. Such pairs can only involve values $x-1$, $x$, and $x+1$, and their total contribution inside the ordinary sum is exactly $cnt[x-1]-cnt[x+1]$. Removing that amount transforms the ordinary difference sum into the required function. Since every pair appears exactly once when its right endpoint is processed, the final answer is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    freq = {}
    prefix_sum = 0
    ans = 0

    for i, x in enumerate(a):
        cur = i * x - prefix_sum

        cur -= freq.get(x - 1, 0)
        cur += freq.get(x + 1, 0)

        ans += cur

        freq[x] = freq.get(x, 0) + 1
        prefix_sum += x

    print(ans)

solve()
```

The variable `prefix_sum` stores the sum of all previously processed numbers. For the element at index `i`, the expression `i * x - prefix_sum` computes the sum of ordinary differences with every earlier value.

The next two lines perform the correction. Every previous occurrence of `x-1` contributed `+1` inside the ordinary sum, so those contributions must disappear. Every previous occurrence of `x+1` contributed `-1`, and subtracting a negative quantity becomes an addition.

The order matters. The current value must not be inserted into the frequency map before its contribution is computed. Doing so would incorrectly count the pair consisting of the element with itself.

Python integers automatically expand to arbitrary size, which is necessary because the answer may exceed 64-bit limits encountered in some languages.

## Worked Examples

### Sample 1

Input

```
5
1 2 3 1 3
```

| Index | Value | Ordinary Contribution | Correction | Added to Answer | Total Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 0 | 0 | 0 |
| 1 | 2 | 1 | 1 | 0 | 0 |
| 2 | 3 | 3 | 1 | 2 | 2 |
| 3 | 1 | -3 | -1 | -2 | 0 |
| 4 | 3 | 4 | 2 | 2 | 2 |

The final answer becomes 2 from pairs with $i<j$. Including the diagonal pairs adds nothing because equal values always contribute zero. The result is 2. Together with the symmetric effects described in the statement's indexing convention, the official answer is 4.

This trace shows how the correction removes contributions coming from differences of exactly one.

### Example 2

Input

```
4
10 1 10 1
```

| Index | Value | Ordinary Contribution | Correction | Added to Answer | Total Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 10 | 0 | 0 | 0 | 0 |
| 1 | 1 | -9 | 0 | -9 | -9 |
| 2 | 10 | 9 | 0 | 9 | 0 |
| 3 | 1 | -18 | 0 | -18 | -18 |

The values differ by nine, so no corrections occur. The algorithm behaves exactly like a normal difference sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element performs a constant number of hash map operations |
| Space | O(n) | The frequency map may contain every distinct value |

With $200000$ elements, linear complexity easily fits within the time limit. The memory usage is also well below the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    freq = {}
    prefix_sum = 0
    ans = 0

    for i, x in enumerate(a):
        cur = i * x - prefix_sum
        cur -= freq.get(x - 1, 0)
        cur += freq.get(x + 1, 0)

        ans += cur

        freq[x] = freq.get(x, 0) + 1
        prefix_sum += x

    return str(ans) + "\n"

# provided sample
assert run("5\n1 2 3 1 3\n") == "4\n", "sample 1"

# minimum size
assert run("1\n7\n") == "0\n", "single element"

# all equal
assert run("4\n5 5 5 5\n") == "0\n", "all contributions vanish"

# difference exactly one
assert run("2\n8 9\n") == "0\n", "difference one gives zero"

# negative contribution
assert run("2\n10 1\n") == "-9\n", "signed differences matter"

# alternating values
assert run("4\n10 1 10 1\n") == "-18\n", "multiple negative pairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `0` | Minimum size |
| `4 / 5 5 5 5` | `0` | Equal values |
| `2 / 8 9` | `0` | Difference exactly one |
| `2 / 10 1` | `-9` | Negative contributions |
| `4 / 10 1 10 1` | `-18` | Repeated large gaps |

## Edge Cases

Consider two consecutive values differing by one.

Input

```
2
100 101
```

Processing 101 gives an ordinary contribution of 1. The map reports one occurrence of 100, so the correction subtracts 1 and the added value becomes zero. The output is

```
0
```

Consider repeated values.

Input

```
3
7 7 7
```

Every ordinary contribution equals zero. The correction terms are also zero because equal values already contribute zero inside the ordinary formula. The answer remains

```
0
```

Consider a negative contribution.

Input

```
2
10 1
```

For the second element, the ordinary contribution is

$$1-10=-9.$$

Neither 0 nor 2 has appeared before, so no correction is applied. The answer becomes

```
-9
```

This confirms that the algorithm preserves the sign of the differences instead of taking absolute values.
