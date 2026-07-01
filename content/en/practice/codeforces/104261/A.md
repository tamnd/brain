---
title: "CF 104261A - Planetary Status"
description: "We are given a single integer $n$, which represents an estimated radius for Pluto in miles. The question is whether this value is large enough for Pluto to qualify as a planet under a specific geometric requirement."
date: "2026-07-01T23:06:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104261
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 03-24-23 Div. 2 (Beginner)"
rating: 0
weight: 104261
solve_time_s: 56
verified: true
draft: false
---

[CF 104261A - Planetary Status](https://codeforces.com/problemset/problem/104261/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer $n$, which represents an estimated radius for Pluto in miles. The question is whether this value is large enough for Pluto to qualify as a planet under a specific geometric requirement.

The requirement is based on comparison with a fixed reference object: a “star” that has radius 1000 miles. Pluto is modeled as a circle, and the star is treated as a five-pointed shape. The condition for Pluto to qualify is that a circle of radius $n$ must be large enough to completely contain the star. In simpler terms, Pluto’s radius must be at least as large as a threshold value that guarantees the star fits entirely inside it.

So the task reduces to deciding whether $n$ meets or exceeds the minimum radius required to enclose the star.

The only input is this integer $n$, and the output is a binary decision: print "YES" if Pluto qualifies as a planet, otherwise print "NO".

The constraint $1 \leq n \leq 10^9$ implies that the solution must run in constant time. Any solution that attempts geometric simulation or iterative construction of the star shape would be unnecessary and far too slow, even though the input size itself is small enough that correctness is the only real challenge.

Edge cases are limited but still worth noting. When $n = 1000$, Pluto is exactly at the threshold and should be accepted. When $n < 1000$, even by 1 unit such as $n = 999$, the answer must be rejection. The most common mistake here is using a strict inequality in the wrong direction or forgetting that equality is allowed.

## Approaches

A naive interpretation would try to reason about the actual geometry of a five-pointed star and compute its bounding circle exactly. That would involve deriving vertex coordinates, computing distances from a center, and then comparing against Pluto’s radius. While mathematically feasible, it is unnecessary because the problem already provides the critical insight: the star’s effective containment radius is fixed at 1000 miles.

The brute-force approach would simulate or reconstruct the star shape, compute all extremal points, and then determine the minimum enclosing circle radius. This would involve constant-factor-heavy geometry operations and floating-point comparisons. Even though the input size is irrelevant, the implementation complexity is high and introduces numerical stability risks.

The key simplification is recognizing that the star’s size is already summarized into a single scalar threshold: 1000 miles. Once that is accepted, the entire geometric problem collapses into a direct comparison between $n$ and 1000.

So instead of computing geometry, we simply compare the given radius against the threshold. If $n \geq 1000$, Pluto qualifies; otherwise it does not.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Geometry | O(1) with heavy constants | O(1) | Overkill and unnecessary |
| Direct Comparison | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$ from input. This is the estimated radius of Pluto.
2. Compare $n$ with 1000, which is the minimum radius required to fully contain the star.
3. If $n \geq 1000$, output "YES" because Pluto’s circle is large enough to satisfy the containment condition.
4. Otherwise, output "NO" because the circle is too small to fully contain the star.

### Why it works

The problem reduces all geometric complexity into a single threshold condition. The star’s required containment is entirely characterized by radius 1000, meaning any circle with radius below 1000 cannot fully enclose it, while any circle with radius at least 1000 can. The algorithm is correct because it directly evaluates this defining condition without approximation or transformation.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

if n >= 1000:
    print("YES")
else:
    print("NO")
```

The solution reads a single integer and performs one comparison. The key implementation detail is ensuring the comparison is inclusive, since equality is explicitly allowed by the condition “at least as large as 1000”.

There is no need for loops or additional parsing. The simplicity is intentional: any extra logic would only introduce opportunities for off-by-one or formatting mistakes.

## Worked Examples

### Example 1

Input:

```
1
```

| Step | n | Comparison with 1000 | Decision |
| --- | --- | --- | --- |
| 1 | 1 | 1 < 1000 | NO |

This case shows a clear failure against the threshold. Since 1 is far below 1000, the star cannot be enclosed in the circle.

Output:

```
NO
```

### Example 2

Input:

```
1414
```

| Step | n | Comparison with 1000 | Decision |
| --- | --- | --- | --- |
| 1 | 1414 | 1414 ≥ 1000 | YES |

Here the radius exceeds the threshold, so the containment condition is satisfied.

Output:

```
YES
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a single integer comparison is performed |
| Space | O(1) | No additional data structures are used |

The constraints allow values up to $10^9$, but since the computation is constant time, even multiple test cases would remain trivial under the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        n = int(sys.stdin.readline().strip())
        print("YES" if n >= 1000 else "NO")
    return out.getvalue().strip()

# provided samples
assert run("1\n") == "NO", "sample 1"
assert run("1414\n") == "YES", "sample 2"

# custom cases
assert run("999\n") == "NO", "just below threshold"
assert run("1000\n") == "YES", "exact threshold"
assert run("1001\n") == "YES", "just above threshold"
assert run("1\n") == "NO", "minimum edge"
assert run("1000000000\n") == "YES", "maximum value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 999 | NO | just-below threshold behavior |
| 1000 | YES | equality boundary |
| 1001 | YES | just-above threshold |
| 1 | NO | minimum input case |
| 1000000000 | YES | upper bound handling |

## Edge Cases

The only meaningful edge behavior is around the threshold value 1000.

For input $n = 999$, the algorithm reads the value and evaluates $999 \geq 1000$, which is false, so it outputs "NO". This correctly reflects that the circle is insufficient.

For input $n = 1000$, the comparison becomes $1000 \geq 1000$, which evaluates to true, producing "YES". This confirms that equality is treated as valid containment.

For large values like $n = 10^9$, the comparison remains a simple integer check with no overflow or precision concerns in Python, ensuring consistent correctness across the entire input range.
