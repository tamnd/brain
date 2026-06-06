---
title: "CF 327A - Flipping Game"
description: "We are given a binary array, every element is either 0 or 1. We must choose exactly one contiguous segment and flip every value inside it. A flip changes 0 to 1 and 1 to 0. After performing this single operation, we want the resulting array to contain as many ones as possible."
date: "2026-06-06T08:55:11+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 327
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 191 (Div. 2)"
rating: 1200
weight: 327
solve_time_s: 83
verified: true
draft: false
---

[CF 327A - Flipping Game](https://codeforces.com/problemset/problem/327/A)

**Rating:** 1200  
**Tags:** brute force, dp, implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary array, every element is either `0` or `1`. We must choose exactly one contiguous segment and flip every value inside it. A flip changes `0` to `1` and `1` to `0`.

After performing this single operation, we want the resulting array to contain as many ones as possible. The task is to compute that maximum number.

The array length is at most 100, which is very small. Even an $O(n^3)$ solution would perform only about one million operations, which easily fits within the time limit. This means we do not need sophisticated data structures. Still, there is a cleaner way to think about the problem that reduces it to a classic maximum-subarray computation.

The most easily missed edge case is when the array already consists entirely of ones.

Input:

```
3
1 1 1
```

Output:

```
2
```

We are required to perform exactly one flip. Any chosen segment contains at least one `1`, and flipping it decreases the number of ones. A careless solution that allows "do nothing" would incorrectly output `3`.

Another common mistake is counting only the zeros inside the chosen segment.

Input:

```
5
1 0 1 0 1
```

If we flip positions 2 through 4, we gain two new ones from the zeros, but we also lose one existing one. The net improvement is only `+1`. Any approach that ignores the lost ones will overestimate the answer.

A third edge case is a segment of length one.

Input:

```
1
0
```

Output:

```
1
```

The only valid move flips the single element. Implementations that accidentally require a segment length greater than one would fail here.

## Approaches

The most direct solution is brute force. We can try every possible segment `[l, r]`, simulate flipping it, count the resulting number of ones, and keep the best answer. There are $O(n^2)$ possible segments, and counting the resulting ones takes $O(n)$ time, giving $O(n^3)$ overall complexity.

For $n \le 100$, even this approach is accepted. The interesting part of the problem is recognizing a much cleaner formulation.

Suppose the original array contains `base` ones.

When we flip a segment:

- Every `0` inside the segment becomes `1`, contributing `+1` to the total number of ones.
- Every `1` inside the segment becomes `0`, contributing `-1`.

For each position, we can assign a value:

- `+1` if the element is `0`
- `-1` if the element is `1`

The net change produced by flipping a segment is exactly the sum of these values over that segment.

Now the problem becomes:

> Find the contiguous segment with the maximum possible sum.

That is precisely the maximum subarray problem, which can be solved with Kadane's algorithm in linear time.

The final answer is:

$$\text{base ones} + \text{maximum subarray sum}$$

The all-ones case works automatically. Every transformed value becomes `-1`, so the maximum subarray sum is `-1`, meaning we lose exactly one one by flipping a single element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count the number of ones in the original array. Call this value `base`.
2. Transform the array into a gain array.

If an element is `0`, store `+1` because flipping it increases the number of ones by one.

If an element is `1`, store `-1` because flipping it decreases the number of ones by one.
3. Run Kadane's algorithm on the gain array to find the maximum subarray sum.

This value represents the largest possible improvement obtainable from a single flip.
4. Add that maximum gain to `base`.
5. Output the result.

### Why it works

For any chosen segment, every zero inside contributes one additional one after the flip, while every one inside contributes one fewer one after the flip. The net effect of the segment is exactly the sum of the transformed values over that segment.

Every possible flip corresponds to exactly one contiguous subarray in the gain array, and every contiguous subarray corresponds to exactly one valid flip. Maximizing the final number of ones is equivalent to maximizing this gain. Kadane's algorithm finds the maximum subarray sum, so adding that gain to the original number of ones produces the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    base = sum(a)

    cur = -10**9
    best = -10**9

    for x in a:
        gain = 1 if x == 0 else -1

        if cur < 0:
            cur = gain
        else:
            cur += gain

        best = max(best, cur)

    print(base + best)

solve()
```

The first step counts the original number of ones. This is the value we would have before performing any flip.

The loop then converts each element into its gain contribution without creating a separate array. A zero contributes `+1`, while a one contributes `-1`.

Kadane's algorithm maintains two values. `cur` stores the best subarray sum ending at the current position, and `best` stores the best subarray sum seen anywhere so far.

The initialization is important. We cannot start with zero because the problem requires exactly one flip. Using a standard non-empty-subarray version of Kadane's algorithm guarantees that at least one position is chosen. This is what makes the all-ones case produce the correct answer.

Finally, `base + best` gives the largest achievable number of ones.

## Worked Examples

### Example 1

Input:

```
5
1 0 0 1 0
```

Original ones count:

`base = 2`

Gain array:

`[-1, +1, +1, -1, +1]`

| Position | Value | Gain | Current Kadane | Best |
| --- | --- | --- | --- | --- |
| 1 | 1 | -1 | -1 | -1 |
| 2 | 0 | +1 | 1 | 1 |
| 3 | 0 | +1 | 2 | 2 |
| 4 | 1 | -1 | 1 | 2 |
| 5 | 0 | +1 | 2 | 2 |

The maximum gain is `2`.

Final answer:

`base + best = 2 + 2 = 4`

Output:

```
4
```

This trace shows that the optimal segment is the one whose gain sum equals `2`. Flipping it increases the number of ones by exactly two.

### Example 2

Input:

```
4
1 1 1 1
```

Original ones count:

`base = 4`

Gain array:

`[-1, -1, -1, -1]`

| Position | Value | Gain | Current Kadane | Best |
| --- | --- | --- | --- | --- |
| 1 | 1 | -1 | -1 | -1 |
| 2 | 1 | -1 | -1 | -1 |
| 3 | 1 | -1 | -1 | -1 |
| 4 | 1 | -1 | -1 | -1 |

Maximum gain is `-1`.

Final answer:

`4 + (-1) = 3`

Output:

```
3
```

This demonstrates the requirement that one flip must be performed. Every possible flip decreases the number of ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass counts ones and computes Kadane's algorithm |
| Space | O(1) | Only a few variables are stored |

With $n \le 100$, even cubic solutions would pass. The linear solution is simpler conceptually once the gain transformation is recognized, and it easily fits within all limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    a = list(map(int, input().split()))

    base = sum(a)

    cur = -10**9
    best = -10**9

    for x in a:
        gain = 1 if x == 0 else -1

        if cur < 0:
            cur = gain
        else:
            cur += gain

        best = max(best, cur)

    return str(base + best)

# provided sample
assert run("5\n1 0 0 1 0\n") == "4", "sample 1"

# minimum size, single zero
assert run("1\n0\n") == "1", "single element zero"

# minimum size, single one
assert run("1\n1\n") == "0", "single element one"

# all ones
assert run("4\n1 1 1 1\n") == "3", "must flip exactly once"

# all zeros
assert run("5\n0 0 0 0 0\n") == "5", "flip entire array"

# off-by-one boundary segment
assert run("5\n0 1 1 1 0\n") == "2", "best segment at an edge"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `1` | Smallest possible array |
| `1 / 1` | `0` | Exact-one-flip requirement |
| `1 1 1 1` | `3` | All elements equal to one |
| `0 0 0 0 0` | `5` | Entire array should be flipped |
| `0 1 1 1 0` | `2` | Boundary segments and Kadane reset logic |

## Edge Cases

### All Ones

Input:

```
3
1 1 1
```

The gain array becomes:

```
-1 -1 -1
```

Kadane's maximum subarray sum is `-1`, obtained by selecting any single position. The original number of ones is `3`, so the answer is:

```
3 + (-1) = 2
```

The algorithm correctly models the fact that one flip is mandatory.

### Single Element Zero

Input:

```
1
0
```

The gain array is:

```
+1
```

Maximum gain is `1`, original ones count is `0`, so the result is:

```
1
```

A length-one segment is treated exactly like any other segment.

### Mixed Values Where Gains and Losses Matter

Input:

```
5
1 0 1 0 1
```

The gain array is:

```
-1 +1 -1 +1 -1
```

The maximum subarray sum is `1`.

Original ones count is `3`, giving:

```
3 + 1 = 4
```

This confirms that the algorithm correctly subtracts the ones lost inside the flipped segment rather than counting only the zeros gained.

### Best Segment Touches an Edge

Input:

```
5
0 0 1 1 1
```

The gain array is:

```
+1 +1 -1 -1 -1
```

The maximum subarray is the prefix with sum `2`.

Original ones count is `3`, so the answer is:

```
3 + 2 = 5
```

The algorithm naturally handles segments that begin at the first position or end at the last position, avoiding off-by-one mistakes.
