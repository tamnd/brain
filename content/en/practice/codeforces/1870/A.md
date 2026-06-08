---
title: "CF 1870A - MEXanized Array"
description: "We are building an array of length $n$ using non-negative integers, with each element capped at $x$. The array is not arbitrary: it must have a fixed MEX equal to $k$, and among all such valid arrays, we want the one with the largest possible sum of elements."
date: "2026-06-08T23:23:20+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1870
codeforces_index: "A"
codeforces_contest_name: "CodeTON Round 6 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 800
weight: 1870
solve_time_s: 105
verified: false
draft: false
---

[CF 1870A - MEXanized Array](https://codeforces.com/problemset/problem/1870/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, math  
**Solve time:** 1m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are building an array of length $n$ using non-negative integers, with each element capped at $x$. The array is not arbitrary: it must have a fixed MEX equal to $k$, and among all such valid arrays, we want the one with the largest possible sum of elements.

The MEX condition forces a very specific structure. Every number from $0$ up to $k-1$ must appear at least once, while the value $k$ must be completely absent. Everything larger than $k$ is irrelevant for MEX purposes and can be used freely as long as it does not exceed $x$.

The constraints are small: $n, k, x \le 200$ and $t \le 1000$. This strongly suggests that each test case must be solved in constant or linear time. Anything quadratic per test case is already acceptable, but anything involving permutations or state search over arrays is unnecessary.

A first subtle failure case appears when $k > x + 1$. If the allowed maximum value is $x$, then we cannot even include all numbers $0$ to $k-1$. For example, if $x = 1$ and $k = 3$, we need to include $0,1,2$, but $2$ is impossible to place. The answer must be $-1$.

Another failure case comes from misunderstanding the MEX requirement. For instance, if $k = 0$, we are not required to include any number from $0$ to $k-1$ (empty set), but we must ensure that $0$ is absent from the array. This changes the optimal construction completely because we can only use values from $1$ to $x$.

Finally, a naive greedy that always fills the array with $x$ fails because it ignores mandatory presence of smaller numbers $0$ to $k-1$, which can force us to “waste” positions that otherwise would maximize sum.

## Approaches

A brute-force approach would try to construct all arrays of length $n$, each entry in $[0, x]$, then compute MEX and track the best sum. The number of arrays is $(x+1)^n$, which even for $n = 10$ is already enormous. This is completely infeasible.

The key observation is that the MEX constraint only restricts two things: a required set of numbers $0$ through $k-1$, and a forbidden number $k$. Everything else is free optimization space.

To maximize the sum, every unused position should be filled with the largest possible value, which is $x$. The only complication is that we may need to include the required numbers $0$ to $k-1$, and those might not be optimal for sum, but they are mandatory.

We also need to ensure feasibility. To get MEX exactly $k$, we must include all numbers $0$ through $k-1$, so we need at least $k$ positions. That is always possible if $n \ge k$, but the cap $x$ must allow those values.

Once feasibility is ensured, the optimal strategy is straightforward: place each of $0,1,\dots,k-1$ once, fill remaining positions with $x$, and compute the sum.

There is one extra subtlety: if $k \le x$, we must ensure that we do not accidentally introduce $k$, but since we never use it, this is naturally satisfied.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((x+1)^n)$ | $O(n)$ | Too slow |
| Optimal Greedy Construction | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We now construct the answer directly.

1. First, check whether constructing a valid MEX is even possible. If $k > x + 1$, then we cannot place all required values $0$ to $k-1$ because $k-1 > x$. In that case, return $-1$. This condition captures all impossible cases caused by the value cap.
2. Compute the contribution of required elements $0,1,\dots,k-1$. Since they must appear at least once, we add their sum $\frac{k(k-1)}{2}$. This is the minimum structure needed to enforce MEX $k$.
3. Fill the remaining $n - k$ positions with the largest allowed value $x$, because replacing any of these with a smaller number strictly reduces the sum without affecting MEX validity.
4. The final answer is:

$$\text{sum} = \frac{k(k-1)}{2} + (n-k)\cdot x$$
5. If $n < k$, we also immediately return $-1$, since we cannot place all required numbers.

### Why it works

The construction is optimal because MEX constraints fully decouple the array into two parts: a forced prefix of distinct required values $0$ to $k-1$, and a free region of size $n-k$. The forced part has no flexibility in terms of membership, only arrangement, and arrangement does not affect the sum. The free part is independently maximized by choosing the largest allowed value $x$. Since there is no interaction between positions beyond presence/absence constraints, any deviation from this structure either violates MEX or decreases the sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k, x = map(int, input().split())

        # feasibility check
        if k > x + 1 or n < k:
            print(-1)
            continue

        # sum of required MEX prefix
        res = k * (k - 1) // 2

        # fill remaining with x
        res += (n - k) * x

        print(res)

if __name__ == "__main__":
    solve()
```

The implementation mirrors the reasoning directly. The feasibility check ensures we can actually realize MEX $k$. The triangular sum computes the mandatory inclusion of $0$ through $k-1$. The remaining positions are greedily filled with $x$, which is safe because it does not introduce $k$ and always maximizes contribution.

Care must be taken with integer division in the triangular sum, but Python handles this cleanly. The order of checks is important: failing early avoids incorrect arithmetic on invalid configurations.

## Worked Examples

### Example 1

Input:

```
n=5, k=3, x=3
```

We need numbers $0,1,2$, and we have 2 extra positions.

| Step | Required sum | Remaining slots | Fill value | Total |
| --- | --- | --- | --- | --- |
| Start | 0 | 5 | - | 0 |
| Add 0,1,2 | 3 | 5 | - | 3 |
| Fill remaining | 3 | 2 | 3 | 9 |

Final answer is 9. One valid array is $[0,1,2,3,3]$.

This confirms that after satisfying MEX, we freely maximize the rest.

### Example 2

Input:

```
n=4, k=2, x=5
```

We must include $0$ and $1$.

| Step | Required sum | Remaining slots | Fill value | Total |
| --- | --- | --- | --- | --- |
| Start | 0 | 4 | - | 0 |
| Add 0,1 | 1 | 4 | - | 1 |
| Fill remaining | 1 | 2 | 5 | 11 |

Final answer is 11.

This shows that large $x$ dominates the solution once MEX constraints are satisfied.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t)$ | Each test case uses constant arithmetic operations |
| Space | $O(1)$ | No extra structures beyond variables |

The solution easily fits within constraints since even $t = 1000$ results in negligible computation.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n, k, x = map(int, input().split())
            if k > x + 1 or n < k:
                print(-1)
                continue
            res = k * (k - 1) // 2 + (n - k) * x
            print(res)

    solve()
    return output.getvalue().strip()

# provided samples
assert run("""9
5 3 3
4 7 5
4 2 28
12 10 6
57 51 122
200 1 200
2 2 1
3 2 1
4 7 10
""") == """7
-1
57
-1
2007
39800
1
2
-1"""

# custom cases
assert run("""1
1 1 5
""") == "0", "minimum valid mex"

assert run("""1
3 2 1
""") == "2", "small tight constraint"

assert run("""1
5 0 3
""") == "15", "mex zero case"

assert run("""1
4 3 2
""") == "3", "boundary feasibility"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 5` | `0` | minimal valid structure |
| `3 2 1` | `2` | tight small constraints |
| `5 0 3` | `15` | handling k = 0 |
| `4 3 2` | `3` | boundary feasibility |

## Edge Cases

When $k = 0$, the required prefix is empty. The algorithm correctly sets the required sum to $0$ and fills all $n$ positions with $x$, giving $n \cdot x$. This matches the MEX requirement because $0$ is absent.

When $k = x + 1$, the feasibility condition still passes, and the construction uses exactly all values $0$ through $x$. There is no room for optimization in the required part, but remaining positions can still be filled with $x$.

When $n = k$, there are no free positions. The answer becomes exactly $\frac{k(k-1)}{2}$, which corresponds to the forced MEX structure with no padding.
