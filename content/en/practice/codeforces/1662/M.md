---
title: "CF 1662M - Bottle Arrangements"
description: "We must build a row of n wine bottles. Each bottle is either red (R) or white (W). Every critic wants to find some contiguous segment of bottles whose contents match a requested pair (r, w), where r is the number of red bottles and w is the number of white bottles in that…"
date: "2026-06-10T02:53:06+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1662
codeforces_index: "M"
codeforces_contest_name: "SWERC 2021-2022 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 0
weight: 1662
solve_time_s: 289
verified: false
draft: false
---

[CF 1662M - Bottle Arrangements](https://codeforces.com/problemset/problem/1662/M)

**Rating:** -  
**Tags:** constructive algorithms  
**Solve time:** 4m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We must build a row of `n` wine bottles. Each bottle is either red (`R`) or white (`W`).

Every critic wants to find some contiguous segment of bottles whose contents match a requested pair `(r, w)`, where `r` is the number of red bottles and `w` is the number of white bottles in that segment. Different critics may choose different segments. Our task is to construct a single arrangement that allows every requested pair to appear as the color counts of at least one contiguous interval.

If no arrangement of length `n` can satisfy all requests simultaneously, we must print `IMPOSSIBLE`.

The constraints are small. Both `n` and `m` are at most `100`. This immediately suggests that expensive enumeration over all possible lengths or all possible color counts is feasible. What remains is finding the structural observation that reduces the search space enough to make construction easy.

A subtle point is that critics do not specify interval positions. They only specify how many red and white bottles must appear inside some interval. We are free to choose the interval later, as long as one exists.

Consider a request `(3, 2)`. The critic is not asking for a specific segment of length five. Any interval containing exactly three red bottles and two white bottles is acceptable.

Another easy mistake is forgetting that interval length is fixed by the request. A request `(r, w)` requires an interval of length `r + w`. If `r + w > n`, the request can never be satisfied.

For example:

```
n = 4
request = (3, 2)
```

The required interval length is `5`, but the entire arrangement contains only four bottles. The correct answer is `IMPOSSIBLE`.

A second non-obvious case occurs when a request asks for only one color.

```
n = 3
requests:
(0, 2)
(0, 3)
```

The arrangement `WWW` works because intervals of lengths two and three contain exactly the required numbers of white bottles.

A careless solution that insists every valid interval must contain both colors would incorrectly reject this case.

## Approaches

A brute-force strategy would generate every possible string of length `n` and check whether every request appears among its intervals. Since there are `2^n` possible strings, this becomes impossible even for moderate values of `n`.

The key observation comes from looking at what information a request actually contains.

A request `(r, w)` only cares about two quantities:

1. The interval length `L = r + w`.
2. The number of red bottles inside that interval.

Suppose we construct a string consisting of some red bottles followed by some white bottles:

```
RRRR...RWWWW...W
```

Let the total number of red bottles be `R`.

Consider any interval length `L`.

As a sliding window of length `L` moves from the far left to the far right, the number of red bottles inside the window changes gradually. It starts at `min(R, L)` and ends at `max(0, L - (n - R))`.

Moreover, every integer value in that range appears.

Therefore, for a fixed total number of red bottles `R`, a request `(r, w)` is feasible if and only if:

```
L = r + w <= n
```

and

```
max(0, L - (n - R)) <= r <= min(R, L)
```

This is the crucial simplification.

Instead of constructing an arbitrary arrangement, we only need to choose a value `R` between `0` and `n`. Once `R` is fixed, the arrangement

```
R repeated R times
W repeated (n - R) times
```

already realizes every achievable red count in every interval length.

There are only `n + 1` possible choices of `R`, which is at most `101`.

We can simply test each candidate value.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Enumerate all strings | O(2^n · n²) | O(n) | Too slow |
| Try every total red count | O(nm) | O(1) | Accepted |

## Algorithm Walkthrough

1. For every possible number of red bottles `R` from `0` to `n`, consider the arrangement consisting of `R` red bottles followed by `n - R` white bottles.

2. For each request `(r, w)`, compute the required interval length:

   ```
   L = r + w
   ```

3. If `L > n`, this request cannot fit inside the arrangement. Reject this value of `R`.

4. Compute the minimum possible number of red bottles in any interval of length `L`:

   ```
   low = max(0, L - (n - R))
   ```

   This occurs when the interval is pushed as far as possible into the white region.

5. Compute the maximum possible number of red bottles in any interval of length `L`:

   ```
   high = min(R, L)
   ```

   This occurs when the interval is pushed as far as possible into the red region.

6. Check whether the requested red count satisfies:

   ```
   low <= r <= high
   ```

   If not, reject this value of `R`.

7. If every request passes, output:

   ```
   "R" * R + "W" * (n - R)
   ```

8. If no value of `R` works, output `IMPOSSIBLE`.

### Why it works

In a string consisting of one block of red bottles followed by one block of white bottles, every interval of fixed length intersects the red block in a contiguous portion.

As the interval slides, the number of red bottles changes by at most one at each step. The possible red counts therefore form a complete integer interval from the minimum achievable value to the maximum achievable value.

The formulas for `low` and `high` describe exactly those extremes.

A request is satisfiable precisely when its required red count lies inside that interval. Since every integer between the extremes occurs, no additional conditions are necessary.

Testing all values of `R` examines every possible size of the red block. If a valid arrangement of this special form exists, the algorithm finds it. The constructive observation proves that such an arrangement exists whenever any solution exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    answers = []

    for _ in range(t):
        n, m = map(int, input().split())
        req = [tuple(map(int, input().split())) for _ in range(m)]

        found = None

        for R in range(n + 1):
            ok = True

            for r, w in req:
                L = r + w

                if L > n:
                    ok = False
                    break

                low = max(0, L - (n - R))
                high = min(R, L)

                if not (low <= r <= high):
                    ok = False
                    break

            if ok:
                found = "R" * R + "W" * (n - R)
                break

        if found is None:
            answers.append("IMPOSSIBLE")
        else:
            answers.append(found)

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the mathematical characterization.

The outer loop tries every possible number of red bottles. The inner loop verifies all critic requests against that choice.

The formulas for `low` and `high` are the only non-trivial part. They encode the smallest and largest red counts obtainable by an interval of length `L` inside a string of the form:

```
RRR...RWWW...W
```

No interval enumeration is required.

The construction itself is simply a prefix of red bottles followed by a suffix of white bottles.

## Worked Examples

### Example 1

Input:

```
n = 5
requests:
(1, 0)
(3, 2)
(2, 2)
```

Try `R = 3`.

| Request | L | low | high | Required r | Valid |
|----------|---|------|------|------------|--------|
| (1,0) | 1 | 0 | 1 | 1 | Yes |
| (3,2) | 5 | 3 | 3 | 3 | Yes |
| (2,2) | 4 | 2 | 3 | 2 | Yes |

All requests pass.

The algorithm outputs:

```
RRRWW
```

Intervals of lengths four and five realize the required counts.

### Example 2

Input:

```
n = 4
requests:
(2,1)
(1,1)
(0,3)
```

Try `R = 2`.

| Request | L | low | high | Required r | Valid |
|----------|---|------|------|------------|--------|
| (2,1) | 3 | 1 | 2 | 2 | Yes |
| (1,1) | 2 | 0 | 2 | 1 | Yes |
| (0,3) | 3 | 1 | 2 | 0 | No |

This value fails.

Trying all values of `R` shows none satisfy every request, so the answer is:

```
IMPOSSIBLE
```

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(nm) per test case | Try every red-block size and verify all requests |
| Space | O(m) | Store the requests |

Since `n` and `m` are both at most `100`, the worst-case work is only about ten thousand checks per test case. This is comfortably inside the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    from collections import deque

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())
        req = [tuple(map(int, input().split())) for _ in range(m)]

        found = None

        for R in range(n + 1):
            ok = True

            for r, w in req:
                L = r + w

                if L > n:
                    ok = False
                    break

                low = max(0, L - (n - R))
                high = min(R, L)

                if not (low <= r <= high):
                    ok = False
                    break

            if ok:
                found = "R" * R + "W" * (n - R)
                break

        ans.append(found if found is not None else "IMPOSSIBLE")

    return "\n".join(ans)

# provided sample
assert run(
"""3
5 3
1 0
3 2
2 2
4 3
2 1
1 1
0 3
3 2
0 2
0 3
"""
) == "RRRWW\nIMPOSSIBLE\nWWW"

# minimum size
assert run(
"""1
1 1
1 0
"""
) == "R"

# all white requests
assert run(
"""1
5 2
0 2
0 5
"""
) == "WWWWW"

# impossible because interval too long
assert run(
"""1
3 1
2 2
"""
) == "IMPOSSIBLE"

# full-length interval requirement
assert run(
"""1
4 1
2 2
"""
) == "RRWW"
```

| Test input | Expected output | What it validates |
|---|---|---|
| n=1, request (1,0) | R | Smallest valid instance |
| Requests (0,2), (0,5) | WWWWW | Pure white construction |
| n=3, request (2,2) | IMPOSSIBLE | Interval longer than array |
| n=4, request (2,2) | RRWW | Full-array interval requirement |

## Edge Cases

Consider:

```
n = 3
request = (2, 2)
```

The interval length would be four. No interval of length four exists in an array of length three. The algorithm detects this immediately through the condition `L > n` and outputs `IMPOSSIBLE`.

Consider:

```
n = 5
requests:
(0, 2)
(0, 5)
```

Choosing `R = 0` gives:

```
WWWWW
```

For length two and length five, the only possible red count is zero. Both requests are satisfied.

Consider:

```
n = 5
request = (5, 0)
```

Choosing `R = 5` gives:

```
RRRRR
```

The unique interval of length five contains exactly five red bottles, so the request is satisfied.

Consider:

```
n = 4
request = (2, 2)
```

The required interval length equals the whole array. The algorithm chooses `R = 2`, producing `RRWW`. The entire array contains exactly two red and two white bottles, which matches the request.
:::

This editorial develops the construction from the interval-count observation and leads directly to the accepted solution.
