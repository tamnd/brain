---
title: "CF 104239A - \u041b\u0430\u0431\u043e\u0440\u0430\u0442\u043e\u0440\u043d\u044b\u0435 \u0440\u0430\u0431\u043e\u0442\u044b"
description: "The semester is modeled as a single continuous timeline of days. Each laboratory occupies a consecutive block of days, and these blocks do not overlap. If the first lab lasts $a1$ days, then it spans days $1$ through $a1$."
date: "2026-07-01T23:16:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104239
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2022-2023, \u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104239
solve_time_s: 53
verified: true
draft: false
---

[CF 104239A - \u041b\u0430\u0431\u043e\u0440\u0430\u0442\u043e\u0440\u043d\u044b\u0435 \u0440\u0430\u0431\u043e\u0442\u044b](https://codeforces.com/problemset/problem/104239/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

The semester is modeled as a single continuous timeline of days. Each laboratory occupies a consecutive block of days, and these blocks do not overlap. If the first lab lasts $a_1$ days, then it spans days $1$ through $a_1$. The second lab starts immediately after and runs for $a_2$ days, and so on until the $n$-th lab finishes the semester.

A student named Vlad participates only on specific days: every $k$-th day starting from day $k$, so the active days are $k, 2k, 3k, \dots$. Whenever one of these days falls inside a laboratory’s time interval, Vlad contributes at least one solved problem for that lab. The task is to count how many laboratory intervals contain at least one multiple of $k$.

The key structure is that we are not asked to simulate day by day. The total number of days in the semester can be as large as $10^{18}$, so any approach iterating over days is impossible. The only feasible approach must work with interval arithmetic.

A subtle edge case arises when a laboratory interval is entirely between two consecutive multiples of $k$. For example, if $k = 10$, a lab running from day 11 to day 19 contains no active day. Conversely, even a very short lab of length 1 can still be counted if it contains a multiple of $k$, such as a lab covering day 20 when $k = 10$.

## Approaches

The brute-force interpretation is straightforward. We compute the exact day interval for each laboratory, then iterate over all multiples of $k$ up to the end of the semester and check whether each multiple falls into each interval. This leads to a nested structure: for each lab, we would potentially scan many multiples of $k$, or equivalently scan all days and check membership. Since the total number of days is the sum of all $a_i$, which can reach $10^{18}$, this is immediately infeasible.

The key observation is to flip the perspective. Instead of asking whether a lab contains a multiple of $k$, we ask how many multiples of $k$ fall inside a prefix of the timeline. Each lab corresponds to a prefix interval on the global day axis. The number of multiples of $k$ up to a day $x$ is simply $\lfloor x / k \rfloor$. Therefore, for a lab spanning $[L, R]$, the number of active days inside it is $\lfloor R/k \rfloor - \lfloor (L-1)/k \rfloor$. The lab contributes if this difference is greater than zero.

This reduces the problem to maintaining running prefix sums of lab durations while evaluating a simple arithmetic condition per lab.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over days or multiples | $O(\sum a_i)$ or worse | $O(1)$ | Too slow |
| Prefix interval + division check | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Maintain a running variable `cur` representing the last day of the previous laboratory. Initially `cur = 0`. This gives us a direct way to compute each lab’s interval.
2. For each laboratory $i$, compute its interval as $[cur + 1, cur + a_i]$. Then update `cur += a_i`. This converts the segmented structure into explicit numeric intervals without storing them.
3. For each interval $[L, R]$, compute how many multiples of $k$ lie inside it using integer division: `R // k - (L - 1) // k`.
4. If the result is positive, increment the answer by one. This directly checks whether at least one valid day exists in the interval.
5. After processing all labs, output the final count.

The critical idea is that multiples of $k$ are evenly spaced and counting them inside any prefix interval can be reduced to a constant-time arithmetic expression.

### Why it works

Each laboratory corresponds to a contiguous segment on the number line. The sequence of valid participation days is also a fixed arithmetic progression. Counting intersection between a segment and an arithmetic progression reduces to comparing prefix counts at the endpoints. The expression $\lfloor R/k \rfloor - \lfloor (L-1)/k \rfloor$ exactly counts how many terms of the form $t \cdot k$ lie in $[L, R]$, so the condition “Vlad participates in this lab” is equivalent to this count being nonzero. Since every lab is processed independently and exactly once, the total count is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    cur = 0
    ans = 0
    
    for x in a:
        L = cur + 1
        R = cur + x
        cur = R
        
        if R // k - (L - 1) // k > 0:
            ans += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution keeps only a running endpoint `cur`, so it never explicitly stores or iterates over days. Each lab is processed in constant time using arithmetic.

The expression `(L - 1) // k` is essential to correctly handle boundaries. Without subtracting 1, cases where `L` itself is a multiple of `k` would be miscounted, since floor division would shift the boundary incorrectly.

## Worked Examples

### Example 1

Input:

```
5 2
1 2 1 2 1
```

We track lab intervals and participation:

| Lab | L | R | R//k | (L-1)//k | Count | Taken |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | 0 | 0 | No |
| 2 | 2 | 3 | 1 | 0 | 1 | Yes |
| 3 | 4 | 4 | 2 | 1 | 1 | Yes |
| 4 | 5 | 6 | 3 | 2 | 1 | Yes |
| 5 | 7 | 7 | 3 | 3 | 0 | No |

Final answer is 3.

This demonstrates that participation depends purely on whether a multiple of $k$ lands inside each interval, not on interval length.

### Example 2

Input:

```
6 5
6 10 3 1 2 7
```

| Lab | L | R | R//k | (L-1)//k | Count | Taken |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 6 | 1 | 0 | 1 | Yes |
| 2 | 7 | 16 | 3 | 1 | 2 | Yes |
| 3 | 17 | 19 | 3 | 3 | 0 | No |
| 4 | 20 | 20 | 4 | 3 | 1 | Yes |
| 5 | 21 | 22 | 4 | 4 | 0 | No |
| 6 | 23 | 29 | 5 | 4 | 1 | Yes |

Final answer is 4.

This trace shows how large intervals may contain multiple multiples of $k$, while very small intervals can still contain exactly one if they align precisely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each laboratory is processed once with constant-time arithmetic |
| Space | $O(1)$ | Only a few running variables are stored |

The constraints allow up to $2 \cdot 10^5$ labs, so linear processing is sufficient. The arithmetic uses 64-bit-safe operations since values can reach $10^{18}$, but Python handles this naturally.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    cur = 0
    ans = 0
    
    for x in a:
        L = cur + 1
        R = cur + x
        cur = R
        if R // k - (L - 1) // k > 0:
            ans += 1
    
    return str(ans)

# provided samples
assert run("5 2\n1 2 1 2 1\n") == "3"
assert run("3 10\n1 2 3\n") == "0"

# custom cases
assert run("1 1\n1\n") == "1"
assert run("1 5\n4\n") == "0"
assert run("2 3\n2 2\n") == "1"
assert run("3 2\n1 1 1\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single tiny interval hitting k | 1 | minimum boundary case |
| Single interval not hitting k | 0 | no-hit case |
| Small multiple labs sparse hits | 1 | sparse alignment |
| Continuous small labs | 2 | repeated boundary crossings |

## Edge Cases

One important edge case is when a laboratory starts exactly at a multiple of $k$. For example, with $k = 5$, a lab starting at day 10 must be counted immediately.

For input:

```
1 5
10
```

The interval is $[1, 10]$. We compute:

$10 // 5 = 2$, $(1 - 1) // 5 = 0$, so count is 2, meaning multiples 5 and 10 are both inside the lab, and the lab is correctly counted.

Another edge case is when a lab ends exactly at a multiple of $k$ but starts just after the previous one. For $k = 4$, interval $[5, 8]$ still contains 8 as a valid day. The computation:

$8 // 4 = 2$, $4 // 4 = 1$, gives count 1, correctly marking participation.

These cases confirm that boundary handling with $(L-1)$ is essential for correctness.
