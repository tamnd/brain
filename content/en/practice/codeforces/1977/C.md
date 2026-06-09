---
title: "CF 1977C - Nikita and LCM"
description: "We are given an array of integers. A subsequence is called special if the least common multiple of all its elements does not appear anywhere in the original array. The task is to find the maximum possible length of such a subsequence."
date: "2026-06-08T17:16:07+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp", "greedy", "math", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1977
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 948 (Div. 2)"
rating: 1900
weight: 1977
solve_time_s: 152
verified: true
draft: false
---

[CF 1977C - Nikita and LCM](https://codeforces.com/problemset/problem/1977/C)

**Rating:** 1900  
**Tags:** brute force, data structures, dp, greedy, math, number theory, sortings  
**Solve time:** 2m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers. A subsequence is called special if the least common multiple of all its elements does not appear anywhere in the original array.

The task is to find the maximum possible length of such a subsequence.

The order of elements inside a subsequence does not matter for the LCM. Only the chosen values matter. Since every element of the array may be either taken or skipped, there are exponentially many subsequences, so we need to exploit number-theoretic structure instead of enumerating them.

The array length can be as large as 2000, and the sum of all lengths over all test cases is also at most 2000. This is a very unusual constraint. It means we can afford roughly quadratic work per test case, but anything exponential is impossible. Even $O(n^3)$ would be uncomfortable in the worst case.

The values themselves can be as large as $10^9$, which rules out dynamic programming over values. Any solution must work directly with divisors and LCMs rather than building large tables indexed by value.

Several edge cases are easy to miss.

Consider:

```
1
5
1 2 4 8 16
```

Every non-empty subsequence has an LCM that is one of the array elements. The empty subsequence has LCM $0$, but its length is zero. The correct answer is 0.

A common mistake is to assume that if the LCM of the whole array belongs to the array then no answer exists. That is false.

For example:

```
1
4
2 3 6 12
```

The LCM of the whole array is 12, which is present. However the subsequence $[2,3]$ has LCM 6, which is also present, while $[2,12]$ has LCM 12. We must search much more carefully than simply checking the full-array LCM.

Another subtle case is:

```
1
3
2 3 5
```

The LCM of the whole array is 30, which is not present. Then taking all elements immediately gives a special subsequence of length 3. Missing this observation leads to unnecessary work.

## Approaches

The brute-force approach is straightforward. Enumerate all subsequences, compute their LCMs, and keep the largest length whose LCM does not appear in the array.

This is correct because it directly checks the definition. Unfortunately it requires examining $2^n$ subsequences. Even for $n=50$ this is already impossible, and here $n$ can reach 2000.

The key observation comes from looking at what LCMs can actually occur.

Let $M$ be the LCM of the entire array.

Any subsequence LCM must divide $M$. It can never contain a prime power larger than what already appears somewhere in the array.

Now consider two cases.

If $M$ itself does not appear in the array, then the whole array is already special. Its LCM equals $M$, which is absent from the array. The answer is immediately $n$.

The interesting case is when $M$ does appear in the array.

Then every special subsequence must have an LCM that is a proper divisor of $M$. Furthermore, if a value does not divide $M$, it cannot be the LCM of any subsequence.

The crucial fact is that every candidate special LCM must be a divisor of $M$ that does not appear in the array.

The number of divisors of a number up to $10^9$ is small. In fact, even the maximum possible divisor count is only around one thousand. This makes it feasible to enumerate all divisors of $M$.

For a fixed candidate divisor $d$, what is the largest subsequence whose LCM equals $d$?

Every chosen element must divide $d$. Any element not dividing $d$ would force the LCM to exceed $d$.

Among all elements dividing $d$, we simply take all of them. Their combined LCM can be computed. If that LCM equals $d$, then every such element may be included, giving the maximum possible length for this candidate.

We repeat this for every divisor $d$ of $M$ that is absent from the array and take the largest valid count.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \cdot \tau(M))$ | $O(\tau(M))$ | Accepted |

Here $\tau(M)$ denotes the number of divisors of $M$.

## Algorithm Walkthrough

1. Read the array and compute the LCM of all elements.
2. While computing the LCM, stop growing it once it exceeds the maximum array value.

This matters because the actual full-array LCM may become enormous. We only need to know whether it is larger than every array element.
3. Let `mx` be the maximum array value.
4. If the full-array LCM is greater than `mx`, then it cannot belong to the array.

In that situation the whole array is special, so output `n`.
5. Otherwise the full-array LCM equals some array value. Call this value `M`.
6. Enumerate every divisor of `M`.
7. For each divisor `d` that does not appear in the array:

1. Collect all array elements dividing `d`.
2. Count them.
3. Compute the LCM of all collected elements.
4. If the resulting LCM equals `d`, then this divisor can be realized as a subsequence LCM.
5. Update the answer with the count.
8. Output the largest count found.

### Why it works

Every subsequence LCM divides the full-array LCM $M$. If $M$ itself is absent from the array, taking every element already gives a special subsequence of maximum possible length.

Otherwise $M$ belongs to the array. Any special subsequence must have an LCM equal to some divisor $d$ of $M$ that does not appear in the array.

For a fixed divisor $d$, every chosen element must divide $d$. Including all such elements gives the largest possible subsequence that could realize $d$. If the LCM of all those eligible elements equals $d$, then $d$ is achievable. If not, no subset of them can produce $d$, because removing elements can only decrease available prime powers.

Thus every feasible special LCM is examined exactly once, and for each one we compute the maximum achievable length. The largest such length is the answer.

## Python Solution

```python
import sys
from math import gcd

input = sys.stdin.readline

def lcm(a, b):
    return a // gcd(a, b) * b

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        mx = max(a)
        s = set(a)

        cur_lcm = 1
        overflow = False

        for x in a:
            cur_lcm = lcm(cur_lcm, x)
            if cur_lcm > mx:
                overflow = True
                break

        if overflow:
            ans.append(str(n))
            continue

        M = cur_lcm

        divisors = []
        d = 1
        while d * d <= M:
            if M % d == 0:
                divisors.append(d)
                if d * d != M:
                    divisors.append(M // d)
            d += 1

        best = 0

        for target in divisors:
            if target in s:
                continue

            cnt = 0
            cur = 1

            for x in a:
                if target % x == 0:
                    cnt += 1
                    cur = lcm(cur, x)
                    if cur > target:
                        break

            if cur == target:
                best = max(best, cnt)

        ans.append(str(best))

    sys.stdout.write("\n".join(ans))

solve()
```

The first part computes the LCM of the entire array. We never allow it to grow unnecessarily. As soon as it exceeds the maximum array element, we already know it cannot appear in the array, so the answer becomes `n`.

The next phase only runs when the full-array LCM equals an array value. In that case we enumerate all divisors of that LCM.

For each candidate divisor, we examine exactly those array elements that divide it. Any element not dividing the candidate can never belong to a subsequence whose LCM equals that candidate.

The LCM calculation uses

```
a // gcd(a, b) * b
```

rather than `a * b // gcd(a, b)` to avoid intermediate overflow in languages with fixed-size integers. Python does not overflow, but this is still the standard competitive-programming implementation.

A subtle point is that we skip every divisor already present in the array. The problem requires the resulting LCM to be absent from the array.

## Worked Examples

### Example 1

Input:

```
5
1 2 4 8 16
```

The full-array LCM is 16.

| Step | Value |
| --- | --- |
| Maximum element | 16 |
| Full-array LCM | 16 |
| LCM present in array? | Yes |

Now we examine divisors not present in the array.

| Candidate | Present in array? | Achievable? |
| --- | --- | --- |
| 1 | Yes | Skip |
| 2 | Yes | Skip |
| 4 | Yes | Skip |
| 8 | Yes | Skip |
| 16 | Yes | Skip |

No valid special LCM exists.

Answer:

```
0
```

This example shows that having many divisors does not help when every possible LCM already appears in the array.

### Example 2

Input:

```
6
3 2 10 20 60 1
```

| Step | Value |
| --- | --- |
| Maximum element | 60 |
| Full-array LCM | 60 |
| LCM present in array? | Yes |

Consider divisor 30.

| Element | Divides 30? |
| --- | --- |
| 3 | Yes |
| 2 | Yes |
| 10 | Yes |
| 20 | No |
| 60 | No |
| 1 | Yes |

The chosen elements are:

```
3 2 10 1
```

Their LCM is 30.

Since 30 does not appear in the array, we obtain a special subsequence of length 4.

No larger valid candidate exists.

Answer:

```
4
```

This example demonstrates why we must inspect divisors of the global LCM rather than only the full-array LCM itself.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot \tau(M))$ | Each divisor is checked against all array elements |
| Space | $O(\tau(M))$ | Storage for divisors |

The sum of all array lengths is at most 2000. The number of divisors of an integer up to $10^9$ is small, well below a few thousand. The resulting workload is comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    from math import gcd

    def lcm(a, b):
        return a // gcd(a, b) * b

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        mx = max(a)
        s = set(a)

        cur = 1
        overflow = False

        for x in a:
            cur = lcm(cur, x)
            if cur > mx:
                overflow = True
                break

        if overflow:
            out.append(str(n))
            continue

        M = cur

        divs = []
        d = 1
        while d * d <= M:
            if M % d == 0:
                divs.append(d)
                if d * d != M:
                    divs.append(M // d)
            d += 1

        best = 0

        for target in divs:
            if target in s:
                continue

            cnt = 0
            cur_l = 1

            for x in a:
                if target % x == 0:
                    cnt += 1
                    cur_l = lcm(cur_l, x)

            if cur_l == target:
                best = max(best, cnt)

        out.append(str(best))

    return "\n".join(out)

# provided samples
assert run("""6
5
1 2 4 8 16
6
3 2 10 20 60 1
7
2 3 4 6 12 100003 1200036
9
2 42 7 3 6 7 7 1 6
8
4 99 57 179 10203 2 11 40812
1
1
""") == "0\n4\n4\n5\n8\n0"

# custom cases
assert run("""1
3
2 3 5
""") == "3"

assert run("""1
1
7
""") == "0"

assert run("""1
4
2 2 2 2
""") == "0"

assert run("""1
3
2 4 8
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[2,3,5]` | `3` | Full-array LCM absent, answer is all elements |
| `[7]` | `0` | Single-element boundary case |
| `[2,2,2,2]` | `0` | Repeated values |
| `[2,4,8]` | `0` | Every possible LCM already present |

## Edge Cases

Consider:

```
1
3
2 3 5
```

The full-array LCM is 30, while the maximum array value is 5. Since 30 exceeds every array element, it cannot be present. The algorithm immediately returns 3. No divisor enumeration is needed.

Now consider:

```
1
1
1
```

The full-array LCM is 1, which belongs to the array. The only divisor is also 1, and it is present in the array. No special subsequence exists, so the answer is 0.

Finally consider:

```
1
5
1 2 4 8 16
```

The full-array LCM equals 16 and belongs to the array. Every divisor of 16 is also present. Every possible subsequence LCM is one of these divisors, so none can be special. The algorithm checks all divisors, finds no valid target, and correctly outputs 0.
