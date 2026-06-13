---
title: "CF 1654E - Arithmetic Operations"
description: "We want to change as few array elements as possible so that the final array becomes an arithmetic progression. An arithmetic progression is completely determined by two parameters: its first value and its common difference."
date: "2026-06-10T03:43:20+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "graphs", "math"]
categories: ["algorithms"]
codeforces_contest: 1654
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 778 (Div. 1 + Div. 2, based on Technocup 2022 Final Round)"
rating: 2300
weight: 1654
solve_time_s: 160
verified: true
draft: false
---

[CF 1654E - Arithmetic Operations](https://codeforces.com/problemset/problem/1654/E)

**Rating:** 2300  
**Tags:** brute force, data structures, graphs, math  
**Solve time:** 2m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We want to change as few array elements as possible so that the final array becomes an arithmetic progression.

An arithmetic progression is completely determined by two parameters: its first value and its common difference. If we write the progression as

$$a_i = b + d \cdot i$$

then every position that already satisfies this formula can be left unchanged, while every position that does not satisfy it must be modified.

That turns the problem into a maximization problem. Instead of directly minimizing the number of changes, we look for an arithmetic progression that already matches the largest number of positions. If that progression matches $k$ positions, then the remaining $n-k$ positions must be changed.

The array length can reach $10^5$, which immediately rules out anything close to $O(n^2)$. A quadratic algorithm would perform roughly $10^{10}$ operations, far beyond the limit. We need something around $O(n\sqrt n)$ or $O(n \log n)$.

Several edge cases make naive reasoning dangerous.

Consider

```
3
5 5 5
```

The array is already an arithmetic progression with common difference $0$. The answer is $0$. Any solution that only examines non-zero differences will fail here.

Consider

```
4
1 100000 1 100000
```

The optimal progression may have a very large positive or negative common difference. Restricting the search to small differences misses valid answers.

Consider

```
1
42
```

A single element is always an arithmetic progression. The answer must be $0$.

The most subtle issue comes from the value bounds. Every original value lies between $1$ and $100000$, but the target progression may contain negative numbers or values larger than $100000$. A solution must reason only about which existing points already lie on a progression, not about the range of the final progression.

## Approaches

A useful geometric view is to treat every array element as a point $(i,a_i)$.

An arithmetic progression has the form

$$a_i=b+d\,i$$

which is exactly the equation of a line. The problem becomes:

Find a line that passes through the maximum number of points $(i,a_i)$.

If a line contains $k$ points, those $k$ positions already match the progression represented by that line.

The brute-force idea is straightforward. Pick every pair of points, determine the unique line through them, and count how many points lie on that line. The best line gives the answer.

This is correct because every arithmetic progression corresponds to a line and every line is determined by two points.

The problem is the cost. There are $O(n^2)$ pairs, and even storing or counting them becomes impossible for $n=10^5$.

The key observation comes from the bound $a_i \le 100000$.

Let $B \approx \sqrt{100000}$, about $320$.

We split the common difference $d$ into two categories.

For small slopes, $|d| \le B$, there are only about $2B+1$ possible values. For a fixed $d$,

$$a_i = b + d i$$

implies

$$b = a_i - d i.$$

All points on the same progression with difference $d$ have the same value of $a_i-di$. We can count frequencies of $a_i-di$ for every small $d$.

For large slopes, $|d| > B$, something special happens. Since all original values lie in $[1,100000]$,

$$|a_j-a_i| \le 100000.$$

If two points belong to a progression with $|d|>B$, then

$$|j-i| \le \frac{100000}{|d|} < \frac{100000}{B}.$$

Choosing $B \approx \sqrt{100000}$ makes this distance at most about $320$.

So every pair of points belonging to a large-slope progression must be close in index. We only need to inspect a short window of length $B$ ahead of each position.

This converts the problem into an $O(nB)$ solution, which is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ or worse | $O(n^2)$ | Too slow |
| Optimal | $O(n\sqrt A)$, where $A=100000$ | $O(\sqrt A)$ average hash usage | Accepted |

## Algorithm Walkthrough

1. Let $B=\lfloor\sqrt{100000}\rfloor+1$.
2. Maintain `best`, the maximum number of positions already lying on a common arithmetic progression.
3. Handle all small differences $|d|\le B$.

For each integer $d$ in that range, compute

$$a_i-di$$

for every position $i$.

Positions belonging to the same progression with common difference $d$ produce the same value. Count frequencies with a hash map and update `best`.
4. Handle all large differences $|d|>B$.

For every starting index $i$, examine only positions

$$j=i+1,\dots,\min(n-1,i+B).$$

Any valid large-slope progression containing both $i$ and $j$ must satisfy

$$a_j-a_i=d(j-i).$$

If $(a_j-a_i)$ is divisible by $(j-i)$, compute the integer slope

$$d=\frac{a_j-a_i}{j-i}.$$
5. Ignore slopes with $|d|\le B$, because they were already processed.
6. For the remaining slopes, count how many nearby points produce the same $d$ with the fixed starting index $i$.

If a slope appears $c$ times, then the corresponding line contains $c+1$ points including $i$.

Update `best`.
7. The answer is

$$n-\text{best}.$$

### Why it works

Every arithmetic progression corresponds to a line $a_i=b+di$.

The small-slope phase explicitly checks every possible slope with $|d|\le B$. For a fixed slope, points lie on the same progression exactly when they share the same intercept value $a_i-di$, so the frequency count gives the exact number of matching positions.

For large slopes, the value bound forces any two matching points to be close in index. The maximum possible index gap is less than $100000/B$, which is at most $B$. Hence every pair of points belonging to a large-slope progression is discovered inside the local window. When processing the smallest index on that progression, all other points on the progression contribute the same slope $d$, and the count recovers the exact size of the progression.

Since every possible progression falls into either the small-slope or large-slope category, the algorithm finds the maximum number of unchanged positions. The minimum number of modifications is the complement of that maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    if n <= 2:
        print(0)
        return

    MAX_A = 100000
    B = int(MAX_A ** 0.5) + 1

    best = 1

    # Small slopes: |d| <= B
    for d in range(-B, B + 1):
        freq = {}
        cur_best = 0

        for i, x in enumerate(a):
            key = x - d * i
            val = freq.get(key, 0) + 1
            freq[key] = val
            if val > cur_best:
                cur_best = val

        if cur_best > best:
            best = cur_best

    # Large slopes: |d| > B
    for i in range(n):
        cnt = {}

        limit = min(n, i + B + 1)

        for j in range(i + 1, limit):
            diff = a[j] - a[i]
            dist = j - i

            if diff % dist != 0:
                continue

            d = diff // dist

            if -B <= d <= B:
                continue

            cnt[d] = cnt.get(d, 0) + 1

        for c in cnt.values():
            if c + 1 > best:
                best = c + 1

    print(n - best)

if __name__ == "__main__":
    solve()
```

The first phase enumerates every small common difference. For each one, the quantity `a[i] - d * i` acts as the intercept of the line. Equal intercepts mean the corresponding points already lie on the same arithmetic progression.

The second phase is where the value bound is exploited. For a fixed position `i`, only the next `B` indices need to be inspected. Any progression with a larger slope cannot stretch farther than that because the original values are confined to a range of width `100000`.

A common implementation mistake is forgetting that indices in the mathematical derivation are 1-based while Python uses 0-based indexing. The expression `a[i] - d * i` works perfectly with 0-based indexing because changing all indices by a constant merely shifts the intercept and does not affect equality.

Another easy mistake is counting large slopes globally. The hash map must be rebuilt for every starting index `i`. Otherwise unrelated lines with the same slope become mixed together.

## Worked Examples

### Example 1

Input:

```
9
3 2 7 8 6 9 5 4 1
```

One of the optimal progressions is:

$$11,10,9,8,7,6,5,4,3$$

with common difference $-1$.

For $d=-1$, compute $a_i-di=a_i+i$.

| i | a[i] | a[i] + i |
| --- | --- | --- |
| 0 | 3 | 3 |
| 1 | 2 | 3 |
| 2 | 7 | 9 |
| 3 | 8 | 11 |
| 4 | 6 | 10 |
| 5 | 9 | 14 |
| 6 | 5 | 11 |
| 7 | 4 | 11 |
| 8 | 1 | 9 |

The highest frequency is 3, coming from intercept values 9 and 11.

Other slopes are checked as well. The maximum line found contains 3 points, so:

| Quantity | Value |
| --- | --- |
| n | 9 |
| best | 3 |
| answer | 6 |

The trace shows how the algorithm searches over all possible slopes and keeps the largest group of already-correct positions.

### Example 2

Consider

```
5
1 3 5 7 9
```

For $d=2$:

| i | a[i] | a[i] - 2i |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 3 | 1 |
| 2 | 5 | 1 |
| 3 | 7 | 1 |
| 4 | 9 | 1 |

Every value is identical.

| Quantity | Value |
| --- | --- |
| n | 5 |
| best | 5 |
| answer | 0 |

The entire array already lies on one arithmetic progression.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n\sqrt{100000})$ | Small slopes and large slopes each perform $O(nB)$ work |
| Space | $O(B)$ average | Hash maps store counts for one slope or one index window at a time |

With $B \approx 317$, the total work is roughly a few times $10^7$ simple operations, which comfortably fits within the limits for $n=10^5$.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    input_data = io.StringIO(inp)
    output = io.StringIO()

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = input_data
    sys.stdout = output

    try:
        import math

        input = sys.stdin.readline

        n = int(input())
        a = list(map(int, input().split()))

        if n <= 2:
            print(0)
        else:
            MAX_A = 100000
            B = int(MAX_A ** 0.5) + 1

            best = 1

            for d in range(-B, B + 1):
                freq = {}
                for i, x in enumerate(a):
                    key = x - d * i
                    freq[key] = freq.get(key, 0) + 1
                    best = max(best, freq[key])

            for i in range(n):
                cnt = {}
                for j in range(i + 1, min(n, i + B + 1)):
                    diff = a[j] - a[i]
                    dist = j - i

                    if diff % dist:
                        continue

                    d = diff // dist

                    if -B <= d <= B:
                        continue

                    cnt[d] = cnt.get(d, 0) + 1

                for v in cnt.values():
                    best = max(best, v + 1)

            print(n - best)

        return output.getvalue()

    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# minimum size
assert run("1\n42\n") == "0\n"

# two elements always form an AP
assert run("2\n5 100\n") == "0\n"

# already arithmetic
assert run("5\n1 3 5 7 9\n") == "0\n"

# all equal
assert run("6\n7 7 7 7 7 7\n") == "0\n"

# one wrong element
assert run("5\n1 3 100 7 9\n") == "1\n"

# large slope progression
assert run("4\n1 100000 199999 299998\n") == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 42` | `0` | Single-element array |
| `2 / 5 100` | `0` | Any two elements form an AP |
| `1 3 5 7 9` | `0` | Already arithmetic |
| `7 7 7 7 7 7` | `0` | Difference zero |
| `1 3 100 7 9` | `1` | One modification needed |
| `1 100000 199999 299998` | `0` | Large-slope handling |

## Edge Cases

Consider

```
1
42
```

The algorithm immediately returns `0` because an array of length one is already an arithmetic progression. No slope processing is needed.

Consider

```
6
7 7 7 7 7 7
```

For slope $d=0$, every value of $a_i-di$ equals $7$. The frequency becomes $6$, so `best = 6` and the answer is `0`. This correctly handles constant progressions.

Consider

```
5
1 3 100 7 9
```

For slope $d=2$, the intercept values are:

| i | a[i] - 2i |
| --- | --- |
| 0 | 1 |
| 1 | 1 |
| 2 | 96 |
| 3 | 1 |
| 4 | 1 |

The intercept `1` appears four times, meaning four positions already lie on the progression $1,3,5,7,9$. The answer becomes $5-4=1$.

Consider

```
4
1 100000 199999 299998
```

The common difference is $99999$, much larger than $B$. The small-slope phase cannot detect it. The large-slope phase examines nearby indices, computes the exact slope from divisibility checks, groups equal slopes together, and recovers all four points on the same progression. The answer is `0`.
