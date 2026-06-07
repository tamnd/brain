---
title: "CF 2185B - Prefix Max"
description: "We are given an array. For every position, we look at the prefix ending there and take the maximum value seen so far. The score of the array is the sum of all those prefix maxima. We may swap any two elements at most once, or choose not to swap at all."
date: "2026-06-07T21:28:30+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2185
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1074 (Div. 4)"
rating: 800
weight: 2185
solve_time_s: 105
verified: true
draft: false
---

[CF 2185B - Prefix Max](https://codeforces.com/problemset/problem/2185/B)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array. For every position, we look at the prefix ending there and take the maximum value seen so far. The score of the array is the sum of all those prefix maxima.

We may swap any two elements at most once, or choose not to swap at all. The task is to maximize the resulting score.

To understand the score, consider:

```
[2, 1, 4, 5, 3]

prefix maxima:
2
2
4
5
5

score = 2 + 2 + 4 + 5 + 5 = 18
```

The constraints are extremely small. There are at most 100 test cases, and each array has length at most 50. Even an algorithm that tries every possible swap is practical.

With $n=50$, the number of possible swaps is only

$$\frac{50 \cdot 49}{2} = 1225$$

and computing the score of one array takes $O(n)$. That means a complete brute-force search costs roughly $1225 \cdot 50 \approx 6 \times 10^4$ operations per test case, which is tiny.

The main challenge is recognizing that the constraints allow a direct search instead of looking for a more complicated greedy observation.

A few edge cases deserve attention.

Consider an array where the largest value is already first:

```
5 1
```

Its score is:

```
5 + 5 = 10
```

Swapping produces:

```
1 5
```

whose score is only:

```
1 + 5 = 6
```

The correct answer is 10 because we are allowed to perform zero swaps. A solution that always performs exactly one swap would fail.

Consider an array with repeated values:

```
4 4 4
```

Every swap leaves the array unchanged, and the score remains 12. A solution must evaluate all possibilities including equivalent arrays.

Consider a case where moving the maximum element to the front is optimal:

```
2 1 4 5 3
```

Swapping 2 and 5 gives:

```
5 1 4 2 3
```

Every prefix maximum becomes 5, producing score 25. This demonstrates why a locally appealing swap is not necessarily the best one. We must compare all candidates.

## Approaches

The most direct approach is to try every possible action.

For each pair of indices $(i,j)$, swap the two elements, compute the score of the resulting array, and keep the best value found. We should also consider the possibility of making no swap.

Computing the score of an array is straightforward. We scan from left to right while maintaining the current prefix maximum. At each position we add that maximum to the answer.

The brute-force method is obviously correct because it explicitly evaluates every array obtainable with at most one swap. If the optimal answer exists, it must appear among the tested configurations.

In many Codeforces problems, trying all swaps would be impossible because $n$ might be $10^5$ or larger. Here $n\le 50$, so the search space is tiny. The key observation is not a clever greedy trick but recognizing that the constraints make exhaustive search completely acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all swaps | $O(n^3)$ | $O(1)$ | Accepted |
| Any more complicated optimization | Unnecessary | Unnecessary | Accepted but overengineered |

Since $n\le 50$, $O(n^3)$ is only $125000$ operations per test case, well within the limits.

## Algorithm Walkthrough

1. Compute the score of the original array and store it as the current best answer.
2. For every pair of indices $i<j$, swap the two elements.
3. Scan the modified array from left to right.

Maintain the maximum value seen so far and accumulate the prefix maxima sum.
4. Update the best answer if the current score is larger.
5. Undo the swap so the array returns to its original state before testing the next pair.
6. After all pairs have been examined, output the best score found.

### Why it works

The set of arrays reachable with at most one swap consists of the original array plus every array obtained by swapping one pair of positions. The algorithm evaluates the score of each such array exactly once and records the maximum score encountered.

Because every legal result is checked, the largest score found by the algorithm is exactly the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def value(a):
    mx = 0
    total = 0
    for x in a:
        mx = max(mx, x)
        total += mx
    return total

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    ans = value(a)

    for i in range(n):
        for j in range(i + 1, n):
            a[i], a[j] = a[j], a[i]

            ans = max(ans, value(a))

            a[i], a[j] = a[j], a[i]

    print(ans)
```

The helper function `value()` computes the score of an array. It maintains the current prefix maximum and adds it to the running total at each position.

The main loop first evaluates the original array. This handles the "no swap" option automatically.

Each pair of positions is then swapped temporarily. After computing the score, the swap is undone immediately. Restoring the original order is essential because every candidate swap must be tested on the same starting array.

The score can become as large as $50 \times 10000 = 500000$, which easily fits in Python integers.

## Worked Examples

### Example 1

Input array:

```
2 1 4 5 3
```

Original score:

| Position | Value | Prefix Max | Running Sum |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 2 |
| 2 | 1 | 2 | 4 |
| 3 | 4 | 4 | 8 |
| 4 | 5 | 5 | 13 |
| 5 | 3 | 5 | 18 |

Now test swap positions 1 and 4:

```
5 1 4 2 3
```

| Position | Value | Prefix Max | Running Sum |
| --- | --- | --- | --- |
| 1 | 5 | 5 | 5 |
| 2 | 1 | 5 | 10 |
| 3 | 4 | 5 | 15 |
| 4 | 2 | 5 | 20 |
| 5 | 3 | 5 | 25 |

The score becomes 25, which is the maximum possible answer.

This example shows why bringing a large element earlier can improve many prefixes simultaneously.

### Example 2

Input array:

```
5 1
```

Original score:

| Position | Value | Prefix Max | Running Sum |
| --- | --- | --- | --- |
| 1 | 5 | 5 | 5 |
| 2 | 1 | 5 | 10 |

Swap the two positions:

```
1 5
```

| Position | Value | Prefix Max | Running Sum |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 5 | 5 | 6 |

The best score remains 10.

This example demonstrates why the algorithm must include the no-swap configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^3)$ | $O(n^2)$ swaps, each score computation costs $O(n)$ |
| Space | $O(1)$ | Only a few variables are used |

With $n \le 50$, the worst-case work is roughly $50^3 = 125000$ operations per test case, which is comfortably inside the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    def value(a):
        mx = 0
        total = 0
        for x in a:
            mx = max(mx, x)
            total += mx
        return total

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        ans = value(a)

        for i in range(n):
            for j in range(i + 1, n):
                a[i], a[j] = a[j], a[i]
                ans = max(ans, value(a))
                a[i], a[j] = a[j], a[i]

        out.append(str(ans))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# provided sample
assert run(
"""4
5
2 1 4 5 3
2
5 1
3
3 2 1
2
6 7
"""
) == """25
10
9
14
"""

# minimum size
assert run(
"""1
2
1 2
"""
) == """4
"""

# all equal
assert run(
"""1
4
7 7 7 7
"""
) == """28
"""

# maximum already first
assert run(
"""1
5
10 1 2 3 4
"""
) == """50
"""

# increasing array
assert run(
"""1
4
1 2 3 4
"""
) == """16
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2` | `4` | Smallest allowed array |
| `7 7 7 7` | `28` | Repeated values and redundant swaps |
| `10 1 2 3 4` | `50` | No swap is optimal |
| `1 2 3 4` | `16` | Moving the largest value forward improves many prefixes |

## Edge Cases

Consider:

```
1
2
5 1
```

The original score is 10. The only possible swap produces score 6. The algorithm begins with the original score as the current answer, then checks the swap and keeps the larger value. The final answer is 10.

Consider:

```
1
3
4 4 4
```

The original score is:

```
4 + 4 + 4 = 12
```

Every swap leaves the array unchanged. The algorithm evaluates all possibilities and always obtains 12, so the output remains correct.

Consider:

```
1
5
2 1 4 5 3
```

The best move is swapping 2 and 5, yielding:

```
5 1 4 2 3
```

whose score is 25. Since the algorithm checks every pair of indices, this swap is guaranteed to be examined, and the maximum score is found.
