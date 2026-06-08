---
title: "CF 2051C - Preparing for the Exam"
description: "There are $n$ possible exam questions. Each available exam version contains all questions except one. The value $ai$ tells us which question is omitted from the $i$-th version. Monocarp knows a set of $k$ questions."
date: "2026-06-08T08:40:17+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2051
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 995 (Div. 3)"
rating: 1000
weight: 2051
solve_time_s: 119
verified: true
draft: false
---

[CF 2051C - Preparing for the Exam](https://codeforces.com/problemset/problem/2051/C)

**Rating:** 1000  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

There are $n$ possible exam questions. Each available exam version contains all questions except one. The value $a_i$ tells us which question is omitted from the $i$-th version.

Monocarp knows a set of $k$ questions. For every exam version, we must decide whether every question appearing in that version is among the questions he knows.

The output is a binary string of length $m$. The $i$-th character is `1` if Monocarp passes the exam version that omits question $a_i$, otherwise `0`.

The constraints are large. The sum of all $n$ values across test cases reaches $3 \cdot 10^5$, so any algorithm that explicitly examines all $n-1$ questions inside every exam version would require $O(nm)$ work and would be far too slow. We need a solution that processes each test case essentially in linear time.

A subtle observation is that every exam version differs from the full set of questions by exactly one missing question. That drastically limits the number of situations that can occur.

Consider the following edge case:

```
n = 5
known = {1,2,3}
```

There are two unknown questions, namely 4 and 5. Any exam version omits only one question. Even if the omitted question is 4, question 5 still appears in the exam and Monocarp does not know it. Every answer must be `0`.

Another important case is:

```
n = 5
known = {1,2,3,4}
```

Now there is exactly one unknown question, namely 5. The only exam version Monocarp can pass is the one that omits question 5. Every other version still contains question 5.

Finally, if Monocarp knows all questions, he passes every version.

## Approaches

A direct approach would construct each exam version and verify whether all of its $n-1$ questions belong to the known set. Since there are $m$ versions, this costs $O(nm)$. With $n$ and $m$ both reaching hundreds of thousands across the input, this is not feasible.

The key observation is that only the number of unknown questions matters.

Let

$$U = n-k$$

be the number of questions Monocarp does not know.

If $U \ge 2$, every exam version omits only one question, so at least one unknown question remains inside the exam. Passing is impossible.

If $U = 1$, let the unique unknown question be $x$. Monocarp passes exactly those exam versions that omit $x$.

If $U = 0$, Monocarp knows everything and passes all versions.

This reduces the entire problem to identifying how many questions are unknown and, in one special case, finding the unique unknown question.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(n)$ | Too slow |
| Optimal | $O(n+m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the set of known questions.
2. Compute the number of unknown questions:

$$U = n-k$$
3. If $U = 0$, output a string of $m$ ones because every exam version is passable.
4. If $U \ge 2$, output a string of $m$ zeros because every exam version still contains at least one unknown question.
5. If $U = 1$, find the unique unknown question $x$.
6. For every value $a_i$:

- Output `1` if $a_i = x$.
- Output `0` otherwise.

The reason is that the exam version omitting $x$ is the only version that removes the sole question Monocarp does not know.

### Why it works

Suppose there are at least two unknown questions. Since each exam version removes only one question, at least one unknown question always remains in the exam. Passing is impossible.

Suppose there is exactly one unknown question $x$. Any exam version that does not omit $x$ still contains $x$, so Monocarp fails. The version omitting $x$ contains only known questions, so Monocarp passes.

Suppose there are no unknown questions. Every question in every exam version is known, so Monocarp always passes.

These three cases cover all possibilities, so the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))
        q = list(map(int, input().split()))

        known = set(q)
        missing_cnt = n - k

        if missing_cnt == 0:
            ans.append("1" * m)
            continue

        if missing_cnt >= 2:
            ans.append("0" * m)
            continue

        unknown = -1
        for x in range(1, n + 1):
            if x not in known:
                unknown = x
                break

        res = []
        for x in a:
            res.append('1' if x == unknown else '0')

        ans.append(''.join(res))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The implementation follows the three-case analysis directly.

The only nontrivial step is locating the unique unknown question when $n-k=1$. A hash set gives $O(1)$ average membership checks, so scanning from 1 to $n$ finds it in linear time.

No integer overflow issues exist because we only manipulate indices and counts. The total work over all test cases is bounded by the sum of all $n$, which satisfies the problem limits.

## Worked Examples

### Example 1

Input:

```
n = 4
a = [1,2,3,4]
known = [1,3,4]
```

| Quantity | Value |
| --- | --- |
| n | 4 |
| k | 3 |
| Unknown questions | {2} |
| Unique unknown | 2 |

Now evaluate every exam version.

| Missing question $a_i$ | Pass? |
| --- | --- |
| 1 | No |
| 2 | Yes |
| 3 | No |
| 4 | No |

Output:

```
0100
```

This demonstrates the case $n-k=1$.

### Example 2

Input:

```
n = 5
known = [1,3,4]
```

| Quantity | Value |
| --- | --- |
| n | 5 |
| k | 3 |
| Unknown questions | {2,5} |
| Count of unknowns | 2 |

Since there are at least two unknown questions, every exam version still contains an unknown question after removing only one question.

| Exam version | Pass? |
| --- | --- |
| Any version | No |

Output:

```
0000
```

This demonstrates the case $n-k \ge 2$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n+m)$ per test case | Build the set, find the unique unknown if needed, generate the answer |
| Space | $O(k)$ | Storage of known questions |

Because the sum of all $n$ over the input is at most $3 \cdot 10^5$, the total running time remains linear in the input size and comfortably fits within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        out = []

        for _ in range(t):
            n, m, k = map(int, input().split())
            a = list(map(int, input().split()))
            q = list(map(int, input().split()))

            known = set(q)

            if k == n:
                out.append("1" * m)
                continue

            if n - k >= 2:
                out.append("0" * m)
                continue

            unknown = next(x for x in range(1, n + 1) if x not in known)
            out.append("".join('1' if x == unknown else '0' for x in a))

        return "\n".join(out)

    return solve()

# provided sample
assert run(
"""4
4 4 3
1 2 3 4
1 3 4
5 4 3
1 2 3 4
1 3 4
4 4 4
1 2 3 4
1 2 3 4
2 2 1
1 2
2
"""
) == "0100\n0000\n1111\n10"

# minimum size
assert run(
"""1
2 2 2
1 2
1 2
"""
) == "11"

# exactly one unknown
assert run(
"""1
5 5 4
1 2 3 4 5
1 2 3 4
"""
) == "00001"

# two unknowns
assert run(
"""1
5 5 3
1 2 3 4 5
1 2 3
"""
) == "00000"

# unknown question appears first
assert run(
"""1
4 4 3
1 2 3 4
2 3 4
"""
) == "1000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| $n=2,k=2$ | `11` | All questions known |
| One unknown question | `00001` | Exactly one passable version |
| Two unknown questions | `00000` | No version can succeed |
| Unknown question is 1 | `1000` | Boundary value handling |

## Edge Cases

Consider:

```
1
4 4 4
1 2 3 4
1 2 3 4
```

Monocarp knows every question. The algorithm enters the $n-k=0$ branch and outputs `1111`. Every exam version is passable because every question that appears is known.

Consider:

```
1
5 5 4
1 2 3 4 5
1 2 3 4
```

Question 5 is the only unknown question. The algorithm finds `unknown = 5` and marks only the version with `a_i = 5` as passable. The output is `00001`.

Consider:

```
1
5 5 3
1 2 3 4 5
1 2 3
```

Questions 4 and 5 are both unknown. The algorithm detects $n-k=2$ and immediately outputs `00000`. Removing one question cannot eliminate both unknown questions from the exam simultaneously, so every version fails.
