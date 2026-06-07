---
title: "CF 2074B - The Third Side"
description: "We start with an array of positive integers. While more than one number remains, we choose two values, replace them with a new positive integer $x$, and require that the three lengths form a non-degenerate triangle."
date: "2026-06-08T06:38:42+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2074
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1009 (Div. 3)"
rating: 800
weight: 2074
solve_time_s: 91
verified: true
draft: false
---

[CF 2074B - The Third Side](https://codeforces.com/problemset/problem/2074/B)

**Rating:** 800  
**Tags:** geometry, greedy, math  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array of positive integers. While more than one number remains, we choose two values, replace them with a new positive integer $x$, and require that the three lengths form a non-degenerate triangle.

For two sides $a$ and $b$, the triangle inequality tells us that the third side must satisfy

$$|a-b| < x < a+b.$$

Since $x$ must be an integer, the largest possible choice is always

$$x = a+b-1.$$

The process continues until only one number remains. Our goal is to maximize that final number.

The constraints are large enough that we need a very simple solution. The total number of array elements across all test cases is at most $2 \cdot 10^5$, which means an $O(n)$ or $O(n \log n)$ algorithm per test case is easily fast enough. Any approach that tries to explore different merge orders would become infeasible because the number of possible sequences of operations grows exponentially.

The main challenge is recognizing that the exact merge order does not matter once we understand how much value is lost at every operation.

A few edge cases are easy to miss.

Consider a single element:

```
1
10
```

No operation is performed, so the answer is simply `10`. A solution that blindly applies a formula involving the number of merges could accidentally modify the value.

Consider two elements:

```
2
5 7
```

The largest valid replacement is $5+7-1=11$, so the answer is `11`. A careless interpretation of the triangle inequality might incorrectly allow $x=12$, but that would create a degenerate triangle.

Consider all ones:

```
3
1 1 1
```

First merge gives $1+1-1=1$. Merging again gives $1+1-1=1$. The answer is `1`. This example shows that every merge necessarily loses exactly one unit from the sum.

## Approaches

A brute-force solution would try every possible pair at every step and every valid value of $x$. Since each operation changes the state of the array, the number of possible sequences explodes combinatorially. Even for small $n$, the search tree becomes enormous. Such an approach is completely impractical.

To find a pattern, focus on what happens to the array sum.

Suppose we merge values $a$ and $b$. To maximize the final answer, we should clearly choose the largest valid replacement:

$$x=a+b-1.$$

Before the operation, those two elements contribute $a+b$ to the total sum.

After the operation, they contribute $a+b-1$.

The total sum decreases by exactly one.

This observation is the entire problem.

Every operation removes exactly one element from the array, so reducing an array of size $n$ to size $1$ requires exactly $n-1$ merges.

Since each merge decreases the sum by exactly one, the final value must be

$$\left(\sum a_i\right) - (n-1).$$

Nothing else matters. The merge order is irrelevant because every optimal merge loses one unit and there are always exactly $n-1$ merges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the array and compute its sum $S$.
2. Let $n$ be the number of elements.
3. Observe that every optimal merge replaces $a$ and $b$ with $a+b-1$.
4. Each such merge decreases the total sum by exactly one.
5. Reducing $n$ elements to one element requires exactly $n-1$ merges.
6. After all merges, the final value equals

$$S-(n-1).$$

1. Output this value.

### Why it works

The largest possible replacement for a pair $(a,b)$ is $a+b-1$, because the third side of a non-degenerate triangle must be strictly less than $a+b$. Any smaller choice would only reduce future possibilities, so every optimal strategy chooses $a+b-1$.

Each optimal merge decreases the array sum by exactly one. Since the number of merges is fixed at $n-1$, the total decrease is also fixed at $n-1$. The final array contains a single value whose value equals the original sum minus this total decrease. No merge order can produce a different result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans.append(str(sum(a) - (n - 1)))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the mathematical observation.

The sum of the array is computed once. Since every merge reduces the sum by one and exactly $n-1$ merges occur, we subtract $n-1$ from the total.

There are no tricky boundary conditions. When $n=1$, the formula becomes

$$\text{sum}(a)-0,$$

which correctly returns the original value. Python integers easily handle the maximum possible sum, so overflow is not a concern.

## Worked Examples

### Example 1

Input:

```
3
998 244 353
```

Initial sum:

$$998+244+353=1595.$$

Number of merges:

$$3-1=2.$$

| Quantity | Value |
| --- | --- |
| Sum of array | 1595 |
| Number of merges | 2 |
| Total decrease | 2 |
| Final answer | 1593 |

The answer is:

```
1593
```

This demonstrates that only the total sum and the number of merges matter.

### Example 2

Input:

```
5
1 2 3 4 5
```

| Quantity | Value |
| --- | --- |
| Sum of array | 15 |
| Number of merges | 4 |
| Total decrease | 4 |
| Final answer | 11 |

The answer is:

```
11
```

This example shows that even with many possible merge orders, every optimal sequence ends with the same value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute the sum |
| Space | O(1) | Only a few variables besides the input array |

The total number of elements across all test cases is at most $2 \cdot 10^5$. A linear scan of each array is easily within the time limit, and the memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def input():
        return sys.stdin.readline()

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans.append(str(sum(a) - (n - 1)))

    return "\n".join(ans)

# provided samples
assert run(
"""4
1
10
3
998 244 353
5
1 2 3 4 5
9
9 9 8 2 4 4 3 5 3
"""
) == """10
1593
11
39""", "sample 1"

# minimum size
assert run(
"""1
1
7
"""
) == "7", "single element"

# two elements
assert run(
"""1
2
5 7
"""
) == "11", "single merge"

# all equal values
assert run(
"""1
4
1 1 1 1
"""
) == "1", "all ones"

# larger values
assert run(
"""1
5
1000 1000 1000 1000 1000
"""
) == "4996", "large equal values"

# boundary style case
assert run(
"""1
3
1 1000 1
"""
) == "1000", "sum minus n-1"
```

The helper reproduces the contest solution and allows direct verification with assertions.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `7` | No merges are performed |
| `5 7` | `11` | Correct handling of one merge |
| `1 1 1 1` | `1` | Repeated losses of exactly one |
| `1000 1000 1000 1000 1000` | `4996` | Large values and arithmetic correctness |
| `1 1000 1` | `1000` | Formula works regardless of value distribution |

## Edge Cases

Consider the smallest possible array:

```
1
10
```

The algorithm computes:

$$10-(1-1)=10.$$

No merges occur, which matches the real process exactly.

Consider two elements:

```
2
5 7
```

The algorithm computes:

$$12-1=11.$$

A direct simulation also gives $5+7-1=11$. This confirms that the strict triangle inequality is handled correctly.

Consider all ones:

```
3
1 1 1
```

The algorithm computes:

$$3-2=1.$$

A manual trace gives:

$$(1,1)\rightarrow 1,$$

then

$$(1,1)\rightarrow 1.$$

The final value is again `1`. This demonstrates the invariant that every merge reduces the total sum by exactly one.

Consider highly uneven values:

```
3
1 1000 1
```

The algorithm computes:

$$1002-2=1000.$$

One optimal sequence is:

$$1+1-1=1,$$

leaving `[1000, 1]`.

Then:

$$1000+1-1=1000.$$

The final value is `1000`, exactly matching the formula. This confirms that the result depends only on the total sum and the number of merges, not on the merge order.
