---
title: "CF 264C - Choosing Balls"
description: "We have a sequence of balls, each with a color and a value. We may pick any subsequence while preserving order. The score of the chosen subsequence depends on how consecutive chosen balls relate by color."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 264
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 162 (Div. 1)"
rating: 2000
weight: 264
solve_time_s: 139
verified: true
draft: false
---

[CF 264C - Choosing Balls](https://codeforces.com/problemset/problem/264/C)

**Rating:** 2000  
**Tags:** dp  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a sequence of balls, each with a color and a value. We may pick any subsequence while preserving order. The score of the chosen subsequence depends on how consecutive chosen balls relate by color.

If a chosen ball continues the same color as the previous chosen ball, its contribution is `value × a`. Otherwise, its contribution is `value × b`.

Each query gives a different pair `(a, b)`, and we must compute the best possible subsequence score for that query.

The important detail is that the contribution of a ball depends on the color of the previously chosen ball, not the previous ball in the original array. This makes the problem a dynamic programming problem over subsequences.

The constraints shape the entire solution. We have up to `10^5` balls and `500` queries. A quadratic DP per query would require around `10^10` operations, which is completely impossible. Even `O(n * number_of_colors)` per query is too slow in the worst case because colors can also reach `10^5`.

The target complexity must stay close to linear per query. Something around `O(n)` or `O(n log n)` per query is acceptable because `10^5 × 500 = 5 × 10^7`, which is already large but manageable in optimized Python if the constant factors stay small.

Several edge cases break naive implementations.

Consider this input:

```
3 1
5 -100 5
1 1 1
10 1
```

The correct answer is:

```
100
```

We should take only the first and third balls. A careless DP that always extends an existing subsequence of the same color would incorrectly include `-100`.

Another subtle case appears when all useful subsequences start with coefficient `b`, not `a`.

```
2 1
10 10
1 2
100 -1
```

The correct answer is:

```
-10
```

Actually, the empty subsequence gives `0`, so the real answer is:

```
0
```

If we force taking at least one ball, we get the wrong result. The empty subsequence must always remain available.

A more dangerous issue happens when the best transition comes from the same color as the current ball.

```
3 1
5 5 5
1 1 2
100 1
```

When processing the third ball, the global best subsequence already ends with color `1`. We cannot blindly transition from the global best using coefficient `b`, because switching colors is required for `b`. We need special handling to avoid using the same color twice incorrectly.

## Approaches

The brute-force viewpoint is straightforward. For every query, define a DP over subsequences.

Suppose `dp[i]` means the best score of a valid chosen subsequence ending at ball `i`. To compute it, we try every earlier chosen endpoint `j`.

If `c[j] == c[i]`, then ball `i` contributes `v[i] * a`.

Otherwise, it contributes `v[i] * b`.

This gives:

```
dp[i] = max(
    v[i] * b,
    dp[j] + v[i] * a if same color,
    dp[j] + v[i] * b if different color
)
```

The answer is the maximum among all `dp[i]` and `0`.

This works because every subsequence ending at `i` must come from some earlier endpoint. The issue is complexity. For each query we examine every pair `(j, i)`, leading to `O(n^2)` transitions. With `n = 10^5`, this becomes around `10^10` operations.

The key observation is that transitions only care about the color of the previous endpoint, not its exact position.

Suppose we maintain:

```
best[color] = best score of a subsequence ending with this color
```

Now the same-color transition becomes easy:

```
best[color] + v[i] * a
```

The different-color transition still seems expensive because we need the best subsequence among all other colors.

The breakthrough is that we only need the top two global DP values.

Maintain:

```
(mx1_value, mx1_color) = best subsequence overall
(mx2_value, mx2_color) = second best subsequence overall
```

When processing a ball of color `c`:

If the global best ends with a different color, we may extend it using coefficient `b`.

Otherwise, we must use the second-best global value.

This reduces every transition to constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(qn²) | O(n) | Too slow |
| Optimal | O(qn) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each query `(a, b)`, create an array `best` where `best[c]` stores the maximum score of any subsequence ending with color `c`.
2. Initialize every entry of `best` to negative infinity because initially no subsequence exists.
3. Maintain two global maxima:

`mx1 = (best_value, color)`

`mx2 = (second_best_value, color)`

These represent the best and second-best subsequences processed so far.
4. Process balls from left to right.
5. For the current ball with color `c` and value `v`, compute the candidate obtained by extending a subsequence of the same color:

```
same = best[c] + v * a
```

If no such subsequence exists yet, this value stays invalid.
6. Compute the candidate obtained by switching from another color.

If `mx1.color != c`, we may use:

```
diff = mx1.value + v * b
```

Otherwise we must use:

```
diff = mx2.value + v * b
```
7. Starting a brand-new subsequence with this ball is also valid:

```
start = v * b
```
8. The best subsequence ending at this ball is:

```
cur = max(start, same, diff)
```
9. Update:

```
best[c] = max(best[c], cur)
```
10. Update the two global maxima carefully.

If `best[c]` becomes larger than the current maximum, shift the old maximum into second place.

Otherwise update the second maximum if needed.
11. After processing all balls, the answer is:

```
max(0, mx1.value)
```

### Why it works

At every position, `best[c]` stores the optimal score among all subsequences ending with color `c` using only processed balls.

Every valid subsequence ending at the current ball falls into exactly one of three categories.

It either starts here, extends a subsequence of the same color, or extends a subsequence of a different color.

The algorithm explicitly evaluates all three possibilities and keeps the maximum. Since the global maxima always represent the best subsequences seen so far, the different-color transition is always computed correctly in constant time.

Because updates happen left to right, every transition only uses earlier positions, preserving subsequence order.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**30

def solve():
    n, q = map(int, input().split())

    values = list(map(int, input().split()))
    colors = list(map(int, input().split()))

    for _ in range(q):
        a, b = map(int, input().split())

        best = [-INF] * (n + 1)

        mx1_val = 0
        mx1_col = -1

        mx2_val = 0
        mx2_col = -1

        for v, c in zip(values, colors):

            cur = v * b

            if best[c] != -INF:
                cur = max(cur, best[c] + v * a)

            if mx1_col != c:
                cur = max(cur, mx1_val + v * b)
            else:
                cur = max(cur, mx2_val + v * b)

            if cur > best[c]:
                best[c] = cur

                if mx1_col == c:
                    mx1_val = best[c]

                elif best[c] > mx1_val:
                    mx2_val, mx2_col = mx1_val, mx1_col
                    mx1_val, mx1_col = best[c], c

                elif best[c] > mx2_val:
                    mx2_val, mx2_col = best[c], c

        print(mx1_val)

if __name__ == "__main__":
    solve()
```

The array `best` is the core DP state. Each entry represents the best subsequence ending with that color.

The variables `mx1` and `mx2` are what make the solution fast. Without them, every different-color transition would require scanning all colors.

The initialization to negative infinity is important. Using `0` would incorrectly allow nonexistent subsequences to behave as valid transitions.

The answer automatically handles the empty subsequence because `mx1_val` starts at `0`. If every possible subsequence has negative value, the algorithm never replaces this initial value.

The update order matters. We first compute `cur` using only previously processed information, then update `best[c]`, then refresh the global maxima.

Another subtle detail is handling the case where the current color already owns the global maximum. Then the second-best global value must be used for the different-color transition.

## Worked Examples

### Example 1

Input:

```
6 1
1 -2 3 4 0 -1
1 2 1 2 1 1
5 1
```

We process one query with `a = 5`, `b = 1`.

| i | value | color | same-color | diff-color | start | cur | best[color] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | invalid | 1 | 1 | 1 | 1 |
| 2 | -2 | 2 | invalid | -1 | -2 | -1 | -1 |
| 3 | 3 | 1 | 16 | 3 | 3 | 16 | 16 |
| 4 | 4 | 2 | 19 | 20 | 4 | 20 | 20 |
| 5 | 0 | 1 | 16 | 20 | 0 | 20 | 20 |
| 6 | -1 | 1 | 15 | 19 | -1 | 19 | 20 |

Final answer:

```
20
```

The best subsequence becomes balls `1, 3, 4`.

The trace shows why keeping only the best value per color is enough. Earlier weaker subsequences ending with the same color never matter again.

### Example 2

Input:

```
3 1
5 -100 5
1 1 1
10 1
```

| i | value | color | same-color | diff-color | start | cur | best[color] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 1 | invalid | 5 | 5 | 5 | 5 |
| 2 | -100 | 1 | -995 | -100 | -100 | -100 | 5 |
| 3 | 5 | 1 | 55 | 5 | 5 | 55 | 55 |

Final answer:

```
55
```

The optimal subsequence skips the negative middle ball. The DP never forces extension, it only keeps the best achievable value for each color.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(qn) | Each query scans all balls once |
| Space | O(n) | The `best` array stores one value per color |

With `n = 10^5` and `q = 500`, the algorithm performs about `5 × 10^7` constant-time transitions. This is large but acceptable in optimized Python because every iteration only performs a few arithmetic operations and comparisons.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

INF = 10**30

def solve():
    input = sys.stdin.readline

    n, q = map(int, input().split())

    values = list(map(int, input().split()))
    colors = list(map(int, input().split()))

    out = []

    for _ in range(q):
        a, b = map(int, input().split())

        best = [-INF] * (n + 1)

        mx1_val = 0
        mx1_col = -1

        mx2_val = 0
        mx2_col = -1

        for v, c in zip(values, colors):

            cur = v * b

            if best[c] != -INF:
                cur = max(cur, best[c] + v * a)

            if mx1_col != c:
                cur = max(cur, mx1_val + v * b)
            else:
                cur = max(cur, mx2_val + v * b)

            if cur > best[c]:
                best[c] = cur

                if mx1_col == c:
                    mx1_val = best[c]

                elif best[c] > mx1_val:
                    mx2_val, mx2_col = mx1_val, mx1_col
                    mx1_val, mx1_col = best[c], c

                elif best[c] > mx2_val:
                    mx2_val, mx2_col = best[c], c

        out.append(str(mx1_val))

    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run(
"""6 3
1 -2 3 4 0 -1
1 2 1 2 1 1
5 1
-2 1
1 0
"""
) == "20\n9\n4"

# minimum size
assert run(
"""1 1
5
1
2 3
"""
) == "15"

# empty subsequence is optimal
assert run(
"""2 1
10 10
1 2
100 -1
"""
) == "0"

# skipping bad middle element
assert run(
"""3 1
5 -100 5
1 1 1
10 1
"""
) == "55"

# alternating colors
assert run(
"""4 1
1 2 3 4
1 2 1 2
2 10
"""
) == "100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single ball | 15 | Base case |
| All choices negative | 0 | Empty subsequence handling |
| Large negative middle | 55 | DP must skip harmful extensions |
| Alternating colors | 100 | Correct different-color transitions |

## Edge Cases

Consider again the case where every subsequence is negative.

```
2 1
10 10
1 2
100 -1
```

Processing the first ball gives `-10`. Processing the second also gives `-10`. Since `mx1_val` starts at `0`, neither update replaces it. The final answer stays `0`, correctly representing the empty subsequence.

Now consider the case where extending the same color is harmful.

```
3 1
5 -100 5
1 1 1
10 1
```

After the first ball, `best[1] = 5`.

At the second ball:

```
same = 5 + (-100)*10 = -995
start = -100
```

The DP chooses `-100`, but does not overwrite `best[1]` because `5` is larger.

At the third ball:

```
same = 5 + 5*10 = 55
```

The earlier good subsequence survives, allowing the optimal answer.

Finally, consider the dangerous global-maximum case.

```
3 1
5 5 5
1 1 2
100 1
```

Before the third ball:

```
mx1 = 505 with color 1
```

If we incorrectly used `mx1` for a different-color transition, we would pretend we switched colors from color `1` to color `2` even when the previous subsequence already ended with color `2`.

The algorithm prevents this by checking colors explicitly and falling back to `mx2` when needed.
