---
title: "CF 2063A - Minimal Coprime"
description: "We are given an integer segment $[l,r]$. A segment $[a,b]$ is called coprime when the two endpoints $a$ and $b$ have greatest common divisor equal to $1$. Among all coprime segments, we only care about those that are minimal."
date: "2026-06-08T07:28:07+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2063
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1000 (Div. 2)"
rating: 800
weight: 2063
solve_time_s: 110
verified: true
draft: false
---

[CF 2063A - Minimal Coprime](https://codeforces.com/problemset/problem/2063/A)

**Rating:** 800  
**Tags:** math, number theory  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an integer segment $[l,r]$. A segment $[a,b]$ is called coprime when the two endpoints $a$ and $b$ have greatest common divisor equal to $1$.

Among all coprime segments, we only care about those that are minimal. A coprime segment is minimal if there is no strictly smaller coprime segment completely contained inside it.

For each test case, we must count how many minimal coprime segments are contained inside the given range $[l,r]$.

The constraints are very revealing. The endpoints can be as large as $10^9$, which means any solution that iterates through all subsegments is impossible. Even a single interval of length $10^9$ contains roughly $10^{18}$ subsegments. Since there are up to 100 test cases, the intended solution must run in constant time per test case.

The tricky part is understanding what minimal coprime segments actually look like.

Consider the segment $[2,3]$. Since $\gcd(2,3)=1$, it is coprime. Its only proper contained segments are $[2,2]$ and $[3,3]$, neither of which is coprime because $\gcd(2,2)=2$ and $\gcd(3,3)=3$. Thus $[2,3]$ is minimal.

Now consider $[2,5]$. It is coprime because $\gcd(2,5)=1$, but it contains $[2,3]$, which is already a coprime segment. Hence $[2,5]$ cannot be minimal.

A particularly easy-to-miss case is the number 1. The segment $[1,1]$ is coprime because $\gcd(1,1)=1$. Since it contains no smaller segment, it is minimal.

For example:

Input:

```
1 1
```

Output:

```
1
```

A careless solution that assumes every length-1 segment is non-coprime would incorrectly return 0.

Another important case is:

Input:

```
2 2
```

Output:

```
0
```

Here $\gcd(2,2)=2$, so the segment is not coprime.

One more example:

Input:

```
2 4
```

The minimal coprime segments are only $[2,3]$ and $[3,4]$, so the answer is 2.

A naive attempt might count all coprime pairs, including $[2,4]$, but that segment contains $[2,3]$ and is not minimal.

## Approaches

The brute-force idea is straightforward. Enumerate every contained segment $[a,b]$, check whether $\gcd(a,b)=1$, and then verify whether it contains another coprime segment.

This is correct because it directly follows the definition. Unfortunately, a range of length $n$ contains $O(n^2)$ subsegments. Even if $n$ were only $10^5$, this would already mean about $5 \times 10^9$ segments. With endpoints up to $10^9$, brute force is completely infeasible.

The key observation is that minimal coprime segments have an extremely rigid structure.

Suppose $[a,b]$ is minimal and $a<b$.

If $b-a\ge 2$, then the contained segment $[a,a+1]$ lies inside it. Consecutive integers are always coprime:

$$\gcd(a,a+1)=1$$

So $[a,a+1]$ is a coprime segment contained inside $[a,b]$. That contradicts minimality.

Thus every minimal coprime segment must have length 0 or 1.

Length 0 means $[x,x]$. Such a segment is coprime only when $x=1$, because

$$\gcd(x,x)=x.$$

Therefore the only minimal segment of length 0 is $[1,1]$.

Length 1 means $[x,x+1]$. Consecutive integers are always coprime, and the only contained segments are $[x,x]$ and $[x+1,x+1]$. For $x\ge2$, neither of those is coprime, so $[x,x+1]$ is minimal.

The case $x=1$ is special. The segment $[1,2]$ contains $[1,1]$, which is coprime, so $[1,2]$ is not minimal.

We have completely characterized all minimal coprime segments:

1. $[1,1]$
2. $[x,x+1]$ for every $x\ge2$

Now counting becomes easy.

Every adjacent pair $[x,x+1]$ inside $[l,r]$ contributes one minimal segment. Such pairs exist for all

$$x \in [l,r-1].$$

There are $r-l$ of them.

The only adjustment is when the range contains the special segment $[1,1]$. That happens exactly when $l=1$.

If $l=r=1$, the answer is 1.

Otherwise, when $l=1$, the pair $[1,2]$ is included in the count $r-l$, but it is not minimal. We must replace it with $[1,1]$. The total remains $r-l$.

This leads to a remarkably simple formula:

If $(l,r)=(1,1)$, answer 1.

Otherwise, answer $r-l$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((r-l+1)^2)$ or worse | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read $l$ and $r$.
2. Check whether $l=r=1$.

This is the only range whose answer is not covered by the simple difference formula.
3. If $l=r=1$, print 1.
4. Otherwise, print $r-l$.

The reason step 4 works is that every minimal coprime segment inside the interval corresponds to exactly one adjacent pair $[x,x+1]$ with $x\ge2$, plus the special singleton $[1,1]$. The count always simplifies to $r-l$ for every interval except $[1,1]$.

### Why it works

Any coprime segment of length at least 2 contains a consecutive pair $[x,x+1]$, which is itself coprime. Such a segment cannot be minimal.

Hence every minimal coprime segment has length 0 or 1.

Among length-0 segments, only $[1,1]$ is coprime.

Among length-1 segments, every $[x,x+1]$ is coprime. It is minimal exactly when $x\ge2$, because $[1,2]$ contains the coprime segment $[1,1]$.

These are all possible minimal coprime segments, so counting them inside $[l,r]$ yields the formula above.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    l, r = map(int, input().split())

    if l == 1 and r == 1:
        print(1)
    else:
        print(r - l)
```

The implementation directly follows the characterization proved above.

The first condition handles the unique interval consisting only of the number 1. Its answer is 1 because the segment $[1,1]$ is minimal coprime.

Every other interval uses the formula $r-l$. Since $l$ and $r$ are at most $10^9$, ordinary integer arithmetic is sufficient. Python integers easily handle these values.

The most common mistake is overcomplicating the counting and trying to reason about gcd values throughout the interval. Once the structure of minimal segments is understood, only the special case $[1,1]$ remains.

## Worked Examples

### Example 1

Input:

```
1 10
```

| Variable | Value |
| --- | --- |
| l | 1 |
| r | 10 |
| l == 1 and r == 1 | False |
| Answer | 10 - 1 = 9 |

Output:

```
9
```

The minimal coprime segments are:

$$[1,1],
[2,3],
[3,4],
\dots,
[9,10]$$

There are exactly 9 of them.

### Example 2

Input:

```
49 49
```

| Variable | Value |
| --- | --- |
| l | 49 |
| r | 49 |
| l == 1 and r == 1 | False |
| Answer | 49 - 49 = 0 |

Output:

```
0
```

The only contained segment is $[49,49]$. Since $\gcd(49,49)=49$, it is not coprime, so no minimal coprime segments exist.

This example demonstrates that most singleton segments contribute nothing. Only $[1,1]$ is special.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ per test case | Only a few comparisons and one subtraction |
| Space | $O(1)$ | No auxiliary data structures |

With at most 100 test cases, the total running time is effectively instantaneous and easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        l, r = map(int, input().split())

        if l == 1 and r == 1:
            ans.append("1")
        else:
            ans.append(str(r - l))

    print("\n".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""6
1 2
1 10
49 49
69 420
1 1
9982 44353
"""
) == """1
9
0
351
1
34371
"""

# minimum interval containing 1
assert run(
"""1
1 1
"""
) == """1
"""

# singleton interval not equal to 1
assert run(
"""1
2 2
"""
) == """0
"""

# smallest adjacent pair after 1
assert run(
"""1
2 3
"""
) == """1
"""

# large boundary values
assert run(
"""1
1 1000000000
"""
) == """999999999
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Special singleton segment |
| `2 2` | `0` | Non-coprime singleton |
| `2 3` | `1` | One minimal adjacent pair |
| `1 1000000000` | `999999999` | Maximum-range arithmetic |
| Sample input | Sample output | Matches official examples |

## Edge Cases

### Edge Case 1: The special segment [1,1]

Input:

```
1
1 1
```

Execution:

| Step | Value |
| --- | --- |
| Check `l == 1 and r == 1` | True |
| Output | 1 |

The segment $[1,1]$ is coprime because $\gcd(1,1)=1$. Since it contains no smaller segment, it is minimal.

### Edge Case 2: Singleton interval larger than 1

Input:

```
1
7 7
```

Execution:

| Step | Value |
| --- | --- |
| Check special case | False |
| Compute `r - l` | 0 |
| Output | 0 |

The only contained segment is $[7,7]$, and $\gcd(7,7)=7$, so there are no minimal coprime segments.

### Edge Case 3: Interval beginning at 1

Input:

```
1
1 2
```

Execution:

| Step | Value |
| --- | --- |
| Check special case | False |
| Compute `r - l` | 1 |
| Output | 1 |

The only minimal coprime segment is $[1,1]$. The segment $[1,2]$ is coprime but not minimal because it contains $[1,1]$.

### Edge Case 4: Long interval

Input:

```
1
5 100
```

Execution:

| Step | Value |
| --- | --- |
| Check special case | False |
| Compute `r - l` | 95 |
| Output | 95 |

Every adjacent pair $[x,x+1]$ for $x=5,6,\dots,99$ contributes one minimal coprime segment, giving exactly $100-5=95$ segments. No longer segment can be minimal because it contains one of these adjacent coprime pairs.
