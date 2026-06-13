---
title: "CF 1692H - Gambling"
description: "We know the outcomes of the next $n$ dice rolls in advance. Marian chooses a value $a$, and a contiguous segment of rounds $[l,r]$. During every round in that segment he always guesses the same value $a$. Whenever the actual rolled value equals $a$, his money doubles."
date: "2026-06-09T23:06:15+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1692
codeforces_index: "H"
codeforces_contest_name: "Codeforces Round 799 (Div. 4)"
rating: 1700
weight: 1692
solve_time_s: 186
verified: false
draft: false
---

[CF 1692H - Gambling](https://codeforces.com/problemset/problem/1692/H)

**Rating:** 1700  
**Tags:** data structures, dp, greedy, math  
**Solve time:** 3m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We know the outcomes of the next $n$ dice rolls in advance. Marian chooses a value $a$, and a contiguous segment of rounds $[l,r]$. During every round in that segment he always guesses the same value $a$.

Whenever the actual rolled value equals $a$, his money doubles. Otherwise, it is halved.

Since Marian starts with exactly 1 dollar, we need to find the value $a$ and segment $[l,r]$ that maximize his final amount of money.

The first observation is that only powers of two ever appear. If a segment contains $k$ successful guesses and $m$ failed guesses, then the final amount is

$$2^k \cdot 2^{-m} = 2^{k-m}.$$

Maximizing money is exactly the same as maximizing the exponent $k-m$.

The total length of a segment is $k+m$, so

$$k-m = k-(\text{length}-k)=2k-\text{length}.$$

For a fixed value $a$, every occurrence of $a$ contributes $+1$ to $k$, while every non-$a$ position contributes $-1$ to the exponent. The challenge is to find the best value and the best segment.

The constraints are large. The sum of all $n$ values across test cases is at most $2 \cdot 10^5$. Any solution that examines all pairs $(l,r)$ is impossible because that would require roughly $n^2$ work. With $n=2\cdot10^5$, quadratic algorithms would perform tens of billions of operations.

We need something close to linear or $O(n \log n)$.

A subtle edge case appears when a value occurs only once.

Example:

```
1
5
1 2 3 4 5
```

The best answer is any single position. Choosing a longer segment introduces only losses. A solution that always tries to connect multiple occurrences would miss this case.

Another tricky situation occurs when two occurrences are very far apart.

```
1
5
7 1 1 1 7
```

Using the whole segment for value 7 gives exponent

$$2\cdot2-5=-1.$$

Using only one occurrence gives exponent $1$.

The optimal answer is a segment of length one, not the segment containing both occurrences.

A third pitfall is that the optimal segment for a value does not necessarily start and end at consecutive occurrences.

Consider:

```
1
7
5 2 5 3 4 5 5
```

The best segment for value 5 includes all four occurrences despite the gaps. We need a method that automatically decides which occurrences should belong to the optimal segment.

## Approaches

A brute-force solution would try every possible value $a$, every left endpoint, and every right endpoint. For each segment it would count how many positions equal $a$ and compute the resulting exponent.

This is correct because it explicitly evaluates every legal strategy.

The problem is the running time. There are $O(n^2)$ segments, and evaluating each segment naively costs another $O(n)$. Even after preprocessing frequencies, checking all segments remains $O(n^2)$, which is far beyond the limit.

The key observation comes from rewriting the score.

Fix some value $a$. Let its occurrence positions be

$$p_1 < p_2 < \cdots < p_m.$$

Suppose a segment starts at occurrence $p_i$ and ends at occurrence $p_j$. Any optimal segment for value $a$ can be assumed to start and end on occurrences of $a$, because extending beyond them only adds failures.

Inside this segment:

$$k = j-i+1.$$

The length is

$$p_j-p_i+1.$$

The exponent becomes

$$2(j-i+1) - (p_j-p_i+1).$$

Expanding:

$$(j-i+1) - (p_j-p_i).$$

Rearrange:

$$(p_i-i) - (p_j-j) + 1.$$

Now define

$$b_t = p_t - t.$$

For fixed $j$, maximizing the score means finding the largest previous value of $b_i$.

This becomes a maximum subarray style problem on the occurrence list of each distinct value.

Another way to view it is even simpler. Between two consecutive occurrences there are

$$p_t-p_{t-1}-1$$

non-$a$ elements. Connecting those occurrences changes the score by

$$1-(p_t-p_{t-1}-1) = 2-(p_t-p_{t-1}).$$

This gives a natural Kadane-like dynamic programming over the occurrences of each value.

Since every array position belongs to exactly one occurrence list, the total work across all values is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ to $O(n^3)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ per test case | $O(n)$ | Accepted |

## Algorithm Walkthrough

For each distinct value, collect all positions where it appears.

Let the positions be:

$$p_1,p_2,\ldots,p_m.$$

We run a Kadane-style DP on this occurrence list.

1. Start a segment at the first occurrence.
2. Let `cur` be the score of the best segment ending at the current occurrence.

A single occurrence contributes score 1 because one correct guess and zero failures gives exponent 1.
3. When moving from occurrence $p_{i-1}$ to $p_i$, the gain from extending the current segment equals

$$2-(p_i-p_{i-1}).$$

The term $2$ comes from gaining one more occurrence, while the distance subtracts the failures introduced between them.
4. If

$$cur + (2-(p_i-p_{i-1}))$$

is better than starting fresh with score 1, extend the current segment.
5. Otherwise, start a new segment at occurrence $p_i$.
6. After updating `cur`, compare it against the global best answer. If it is larger, store:

- the value $a$,
- the starting occurrence position,
- the ending occurrence position.
7. Repeat for every distinct value.

### Why it works

For a fixed value $a$, every candidate segment is uniquely determined by its first and last occurrence inside that segment. Extending from one occurrence to the next changes the exponent by exactly $2-(p_i-p_{i-1})$. The total exponent of a segment becomes the sum of these transition gains plus the initial contribution of 1 from the first occurrence.

That transforms the problem into finding a maximum-sum contiguous subsequence on the occurrence list. Kadane's algorithm is optimal for exactly this task. Since we solve the optimal segment independently for every value and then choose the overall best result, the final answer is globally optimal.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        pos = defaultdict(list)

        for i, x in enumerate(arr, start=1):
            pos[x].append(i)

        best_score = -10**18
        best_a = arr[0]
        best_l = 1
        best_r = 1

        for value, positions in pos.items():
            cur_score = 1
            cur_start = positions[0]

            if cur_score > best_score:
                best_score = cur_score
                best_a = value
                best_l = cur_start
                best_r = positions[0]

            for i in range(1, len(positions)):
                gain = 2 - (positions[i] - positions[i - 1])

                if cur_score + gain < 1:
                    cur_score = 1
                    cur_start = positions[i]
                else:
                    cur_score += gain

                if cur_score > best_score:
                    best_score = cur_score
                    best_a = value
                    best_l = cur_start
                    best_r = positions[i]

        out.append(f"{best_a} {best_l} {best_r}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part groups equal values and stores all their positions. This is the crucial preprocessing step because the optimization for a value depends only on where that value appears.

For each occurrence list, `cur_score` stores the best score among segments ending at the current occurrence. The transition gain `2 - gap` comes directly from the algebraic transformation of the exponent.

The restart condition is identical to Kadane's algorithm. If extending produces a score below the score of a fresh single-occurrence segment, we discard the previous segment and begin again at the current occurrence.

The stored boundaries are actual array positions, not indices inside the occurrence list. This detail is easy to get wrong.

No integer overflow issues exist because scores are at most $O(n)$, and Python integers are unbounded anyway.

## Worked Examples

### Example 1

Input:

```
5
4 4 3 4 4
```

Occurrences of value 4:

| Occurrence | Position | Gain | Current Score | Segment |
| --- | --- | --- | --- | --- |
| 1 | 1 | - | 1 | [1,1] |
| 2 | 2 | 1 | 2 | [1,2] |
| 3 | 4 | 0 | 2 | [1,4] |
| 4 | 5 | 1 | 3 | [1,5] |

The final score is 3, corresponding to exponent

$$2\cdot4-5=3.$$

Answer:

```
4 1 5
```

This trace shows how nearby occurrences create positive gains and remain in the same optimal segment.

### Example 2

Input:

```
5
11 1 11 1 11
```

Occurrences of value 11:

| Occurrence | Position | Gain | Current Score | Segment |
| --- | --- | --- | --- | --- |
| 1 | 1 | - | 1 | [1,1] |
| 2 | 3 | 0 | 1 | [1,3] |
| 3 | 5 | 0 | 1 | [1,5] |

Occurrences of value 1:

| Occurrence | Position | Gain | Current Score | Segment |
| --- | --- | --- | --- | --- |
| 1 | 2 | - | 1 | [2,2] |
| 2 | 4 | 0 | 1 | [2,4] |

The best score is only 1. Any single occurrence is optimal.

This demonstrates that having many occurrences does not automatically help. Large gaps can completely cancel the benefit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Every array position appears in exactly one occurrence list and is processed once |
| Space | $O(n)$ | Storage for occurrence positions |

The total $n$ across all test cases is at most $2 \cdot 10^5$. A linear scan of all occurrence lists easily fits within the 2-second limit, and storing all positions requires only linear memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        pos = defaultdict(list)

        for i, x in enumerate(arr, 1):
            pos[x].append(i)

        best_score = -10**18
        ans = None

        for value, positions in pos.items():
            cur = 1
            start = positions[0]

            if cur > best_score:
                best_score = cur
                ans = (value, start, positions[0])

            for i in range(1, len(positions)):
                gain = 2 - (positions[i] - positions[i - 1])

                if cur + gain < 1:
                    cur = 1
                    start = positions[i]
                else:
                    cur += gain

                if cur > best_score:
                    best_score = cur
                    ans = (value, start, positions[i])

        out.append(f"{ans[0]} {ans[1]} {ans[2]}")

    return "\n".join(out)

# minimum size
assert run("1\n1\n5\n") == "5 1 1"

# all equal
assert run("1\n5\n7 7 7 7 7\n") == "7 1 5"

# isolated repeats, best is single element
assert run("1\n5\n7 1 1 1 7\n") in {
    "7 1 1",
    "7 5 5",
    "1 2 2",
    "1 3 3",
    "1 4 4",
}

# adjacent occurrences should merge
assert run("1\n4\n9 9 9 9\n") == "9 1 4"

# off-by-one boundary
assert run("1\n5\n3 1 3 3 1\n") == "3 1 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[5]` | `5 1 1` | Minimum size array |
| `[7,7,7,7,7]` | `7 1 5` | Entire array is optimal |
| `[7,1,1,1,7]` | Any single occurrence segment | Restart logic |
| `[9,9,9,9]` | `9 1 4` | Consecutive positive gains |
| `[3,1,3,3,1]` | `3 1 4` | Correct boundary handling |

## Edge Cases

### A value appears only once

Input:

```
1
1
100
```

The occurrence list is `[1]`.

The algorithm initializes:

| Position | Score |
| --- | --- |
| 1 | 1 |

No transitions exist. The answer becomes:

```
100 1 1
```

A solution that assumes every optimal segment contains multiple occurrences would fail here.

### Repeated values separated by large gaps

Input:

```
1
5
7 1 1 1 7
```

For value 7:

| Occurrence | Position | Gain | Score |
| --- | --- | --- | --- |
| 1 | 1 | - | 1 |
| 2 | 5 | -2 | restart |

The extension score would be negative, so Kadane restarts at position 5.

The algorithm correctly returns a single-position segment because connecting the two occurrences introduces too many losses.

### Optimal segment starts in the middle

Input:

```
1
7
5 1 1 5 5 1 5
```

Occurrences of 5 are at positions:

```
1 4 5 7
```

The first gap is large and produces a negative contribution. The Kadane restart discards the early occurrence and begins a better segment later.

This is exactly why the algorithm stores the current segment start separately from the first occurrence of the value. Without that restart mechanism, the answer would be suboptimal.
