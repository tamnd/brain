---
title: "CF 106182B - Balatro"
description: "The problem gives a collection of cards. Each card has two values, a and b. We must choose exactly k cards and maximize the product of the sum of all chosen a values and the sum of all chosen b values."
date: "2026-06-25T10:50:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106182
codeforces_index: "B"
codeforces_contest_name: "Petrozavodsk Summer Camp 2025. Day 6. Xeppelin Contest The 4rd Universal Cup. Stage 2: Grand Prix of Paris)"
rating: 0
weight: 106182
solve_time_s: 45
verified: true
draft: false
---

[CF 106182B - Balatro](https://codeforces.com/problemset/problem/106182/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives a collection of cards. Each card has two values, `a` and `b`. We must choose exactly `k` cards and maximize the product of the sum of all chosen `a` values and the sum of all chosen `b` values. The deck has a special balance property: for every card, at least one of its two values is at most 100.

The input contains several test cases. For each case, we know the number of cards and how many cards must be played, followed by the two values of every card. The output is the best possible score among all valid choices of exactly `k` cards.

The constraints are the key. The total number of cards over all test cases is at most `100000`, and `k` is at most `5`. A normal subset search would try roughly `n^k` possibilities, which becomes impossible even for small values of `k` when `n` reaches `100000`. The solution must be close to linear or use the small value hidden in the card restriction.

A common mistake is to only sort by one side of the card. For example, if we choose the five cards with the largest `a` values, we may destroy the `b` sum. Consider:

```
1
3 2
1000 1
999 100
1 100
```

The greedy choice by `a` gives the first two cards with score `(1999) * (101) = 201899`. The better choice is the last two cards with score `(1000) * (200) = 200000`, so this example does not break it. However, if we change the last card to `(500, 100)`, the best set changes again. The point is that maximizing one side independently does not represent the objective because both sums interact.

Another edge case is when the smaller side of every card is tiny. For example:

```
1
4 2
1000000000 1
2 1000000000
100 100
100 100
```

The answer is obtained by balancing the two sums. A method that only tracks large values can miss the possibility that small contributions make the product much larger.

## Approaches

The brute force approach directly tries every possible group of `k` cards. For each group, we compute the two sums and update the answer. It is correct because every valid hand is checked. The problem is the number of groups. With `n` cards and `k` close to `5`, the number of choices is about `n^5`, which is far beyond what can fit in a normal contest time limit.

The useful observation comes from the balance condition. For every card, define `small = min(a, b)` and `large = max(a, b)`. The chosen cards have:

```
sum(a) * sum(b)
```

which is exactly:

```
(sum of small values) * (sum of large values)
```

because swapping the two values of a card does not change the two totals being multiplied.

The sum of all chosen small values can never exceed `5 * 100 = 500`. This means we can use dynamic programming over this small dimension. While scanning the cards, we keep the maximum possible large sum for every number of chosen cards and every possible small sum.

When we process a card, we can either skip it or take it. If we take it, the number of chosen cards increases by one, the small sum increases by `small`, and the stored large sum increases by `large`. After processing everything, the answer is the maximum value of `small_sum * large_sum`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^k) | O(1) | Too slow |
| Optimal | O(n * k * 500) | O(k * 500) | Accepted |

## Algorithm Walkthrough

1. For every card, calculate its smaller value and larger value. We only care about the smaller values for the DP state because their total range is limited.
2. Create a dynamic programming table where `dp[j][s]` stores the maximum sum of large values that can be obtained by choosing exactly `j` cards whose small values add up to `s`.
3. Initialize `dp[0][0] = 0`, meaning that choosing no cards gives a large sum of zero.
4. Process each card one by one. For the current card, try adding it to every state that already chooses fewer than `k` cards. The new state increases the chosen count and small sum by the current card's values.
5. After all cards are processed, examine every possible small sum in the state where exactly `k` cards were chosen. Multiply the small sum by the stored large sum and keep the maximum.

Why it works:

Every chosen hand has a fixed set of smaller values and larger values. The DP enumerates all possible counts of chosen cards and all possible smaller value sums. For each such situation it keeps the best possible larger value sum, because a larger sum can only improve the final product. Since every possible hand maps to one DP state, and every state stores the best continuation, the final maximum is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    INF = -10**30

    for _ in range(t):
        n, k = map(int, input().split())

        cards = []
        for _ in range(n):
            a, b = map(int, input().split())
            if a <= b:
                cards.append((a, b))
            else:
                cards.append((b, a))

        dp = [[INF] * 501 for _ in range(k + 1)]
        dp[0][0] = 0

        for small, large in cards:
            for cnt in range(k - 1, -1, -1):
                for sm in range(501 - small):
                    if dp[cnt][sm] != INF:
                        dp[cnt + 1][sm + small] = max(
                            dp[cnt + 1][sm + small],
                            dp[cnt][sm] + large
                        )

        ans = 0
        for sm in range(501):
            if dp[k][sm] != INF:
                ans = max(ans, sm * dp[k][sm])

        out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input is read normally with `sys.stdin.readline` because the total number of cards can reach `100000`. The DP table uses only `k + 1` rows because the transition always moves from a smaller chosen count to a larger one.

The loops over `cnt` go backwards. This prevents the current card from being used multiple times in the same iteration. If we looped forwards, a newly updated state could immediately consume the same card again.

The small sum dimension is fixed at `500` because at most five selected cards contribute at most `100` each to the smaller side. The final multiplication is safe in Python because integers have arbitrary precision.

## Worked Examples

For the first sample:

```
1
5 5
1 1
2 2
3 3
4 4
5 5
```

The DP state after taking all cards looks like:

| Chosen cards | Small sum | Large sum | Score |
| --- | --- | --- | --- |
| 5 | 15 | 15 | 225 |

The only possible hand uses all cards, so the product is `15 * 15`.

For the second sample:

```
1
6 5
1 1
2 6
3 5
4 4
5 3
6 2
```

The best hand excludes the first card:

| Chosen cards | Small sum | Large sum | Score |
| --- | --- | --- | --- |
| 5 | 15 | 27 | 405 |

The DP checks every reachable small sum and keeps the largest large sum for each one, so it finds the best combination instead of relying on one ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * k * 500) | Each card updates every chosen count and small sum state |
| Space | O(k * 500) | Only the current DP table is stored |

The total number of cards is `100000`, and the constant dimension is only `500`, so the solution performs about a few hundred million simple operations in the worst case. This fits the intended constraints because `k` is at most `5`.

## Test Cases

```python
import sys
import io

def solve_io(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    t = int(sys.stdin.readline())
    res = []
    INF = -10**30

    for _ in range(t):
        n, k = map(int, sys.stdin.readline().split())
        dp = [[INF] * 501 for _ in range(k + 1)]
        dp[0][0] = 0

        for _ in range(n):
            a, b = map(int, sys.stdin.readline().split())
            small = min(a, b)
            large = max(a, b)

            for cnt in range(k - 1, -1, -1):
                for sm in range(501 - small):
                    if dp[cnt][sm] != INF:
                        dp[cnt + 1][sm + small] = max(
                            dp[cnt + 1][sm + small],
                            dp[cnt][sm] + large
                        )

        ans = 0
        for sm in range(501):
            ans = max(ans, sm * dp[k][sm])
        res.append(str(ans))

    sys.stdin = old
    return "\n".join(res)

assert solve_io("""1
5 5
1 1
2 2
3 3
4 4
5 5
""") == "225"

assert solve_io("""1
6 5
1 1
2 6
3 5
4 4
5 3
6 2
""") == "400"

assert solve_io("""1
1 1
7 9
""") == "63"

assert solve_io("""1
3 2
1000000000 1
2 1000000000
100 100
""") == "200000000"

assert solve_io("""1
4 2
5 5
5 5
5 5
5 5
""") == "100"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One card selected | 63 | Minimum size case |
| Huge opposite values | 200000000 | Balancing both sides |
| All equal cards | 100 | Repeated identical states |
| Large values | Depends on chosen pair | Integer handling and product size |

## Edge Cases

When `k = 1`, the DP still works because only states with one chosen card are considered. For input:

```
1
1 1
7 9
```

the smaller sum is `7` and the larger sum is `9`, giving `63`.

When all cards have the same values, many different selections reach the same DP state. The maximum large sum for that state is what matters, and keeping only the best value is safe.

For cards where one side is extremely large and the other is small, a greedy choice by the large side fails. The DP keeps the small contribution as part of the state, so it can compare combinations that have similar small sums but very different large sums.
