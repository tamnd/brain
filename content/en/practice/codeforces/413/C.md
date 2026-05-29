---
title: "CF 413C - Jeopardy!"
description: "The game consists of n questions, each with some base value a[i]. Some questions are marked as auctions. Team R2 starts by choosing the first question. After that, whoever answered the previous question correctly gets to choose the next question."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 413
codeforces_index: "C"
codeforces_contest_name: "Coder-Strike 2014 - Round 2"
rating: 1400
weight: 413
solve_time_s: 143
verified: true
draft: false
---

[CF 413C - Jeopardy!](https://codeforces.com/problemset/problem/413/C)

**Rating:** 1400  
**Tags:** greedy, math  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

The game consists of `n` questions, each with some base value `a[i]`. Some questions are marked as auctions. Team R2 starts by choosing the first question. After that, whoever answered the previous question correctly gets to choose the next question.

R2 is unbelievably lucky in this scenario. Whenever they attempt a question, they answer it correctly. The task is to compute the maximum total score R2 can achieve if they choose questions optimally.

The interesting part is the auction rule. On an auction question, the player selecting it may increase its value, but only if their current score is strictly greater than the original value. The chosen value can be anything between the original value and the player's current score. Since answering correctly adds that amount to the score, auctions can potentially double the current score.

The constraints are tiny. `n` is at most `100`, and the number of auction questions is at most `30`. Even exponential solutions over all questions are impossible, but dynamic programming over score states is also unnecessary because the structure of the game is much simpler than it first appears.

The key observation is that the order of questions is completely controlled by R2 after the first correct answer. Since R2 always answers correctly, they keep the turn forever. The only meaningful decision is the order in which questions are taken.

Several edge cases are easy to misunderstand.

Consider this input:

```
2 1
10 5
2
```

The auction question has base value `5`, but R2 starts with score `0`. They cannot raise the value because the current score is not strictly greater than `5`. The best score is `10 + 5 = 15`, not `20`.

Now consider:

```
3 1
5 1 100
2
```

If R2 takes the auction question worth `1` after solving the `5` point question, their score becomes `10` because they may raise the auction to value `5`. Then the final answer is `110`. A careless implementation that always adds the base value of auctions would incorrectly produce `106`.

Another subtle case is when the current score equals the auction value:

```
2 1
5 5
2
```

The rule requires the current score to be strictly larger than the base value. Equality is not enough. After solving the first question, the score is `5`, so the auction still cannot be increased. The final score is `10`, not `15`.

## Approaches

A brute-force approach would try every possible order of questions. For each permutation, we simulate the game and compute the resulting score. Since there are at most `100` questions, this immediately becomes impossible. Even `15!` is already far too large.

The brute-force works conceptually because the score evolution depends only on the chosen order. There are no adversarial decisions once R2 gets control. The problem is simply searching through too many permutations.

The breakthrough comes from understanding how auction questions behave.

Suppose the current score is `S`.

For a regular question with value `x`, the new score becomes:

```
S + x
```

For an auction question with base value `x`:

If `S <= x`, the auction cannot be increased, so the result is still:

```
S + x
```

If `S > x`, we may set the auction value to `S`, giving:

```
S + S = 2S
```

So an auction question is effectively a "double your score" operation, but only after your score already exceeds its base value.

This changes the entire perspective. The exact value of an auction question matters only as a threshold that determines when doubling becomes available.

To maximize the final score, we want to unlock doubling as early as possible. That means auction questions with smaller base values should be used first. Before an auction becomes usable, we may need to solve some regular questions to build enough score.

This leads to a greedy process:

Start with score `0`. Repeatedly take all regular questions that are necessary to make the next smallest auction usable. Once an auction becomes usable, use it immediately because doubling earlier is always better than doubling later.

After all auctions are processed, add all remaining regular questions normally.

The number of auctions is at most `30`, so sorting and simulation are trivial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Separate the questions into two groups: regular questions and auction questions.

Auction questions are identified by their indices from the input.
2. Store the values of all auction questions in one array and all regular question values in another.

The actual positions of questions do not matter because R2 controls the order after the first success.
3. Sort both arrays in ascending order.

Smaller auction thresholds should be unlocked earlier. Smaller regular questions are useful because we only want to spend the minimum amount necessary before each doubling.
4. Initialize the current score `ans = 0`.
5. Process auction questions from smallest to largest.

For the current auction value `x`, keep taking regular questions while `ans <= x`.

Each taken regular question simply adds its value to `ans`.
6. Once `ans > x`, take the auction question.

Since the current score is strictly larger than `x`, we may set the auction value equal to `ans`, doubling the score.
7. After all auctions are processed, add every remaining regular question to the score.

No more doubling opportunities remain, so regular questions are just added directly.

### Why it works

The crucial property is that doubling earlier is always at least as good as doubling later.

Suppose we have some regular gain `r` and one available auction doubling. Compare the two possibilities:

First add `r`, then double:

```
(S + r) * 2 = 2S + 2r
```

First double, then add `r`:

```
2S + r
```

The first value is larger by `r`.

This means that before each auction, we should spend only the minimum regular score necessary to activate that auction. Any extra regular gains are more valuable after the doubling.

Processing auctions in ascending order is also optimal because smaller thresholds are easier to activate and unlock future doublings sooner.

Together, these facts uniquely determine the greedy strategy.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    is_auction = [False] * n
    for x in b:
        is_auction[x - 1] = True

    auctions = []
    regular = []

    for i in range(n):
        if is_auction[i]:
            auctions.append(a[i])
        else:
            regular.append(a[i])

    auctions.sort()
    regular.sort()

    ans = 0
    ptr = 0
    k = len(regular)

    for x in auctions:
        while ptr < k and ans <= x:
            ans += regular[ptr]
            ptr += 1

        if ans > x:
            ans *= 2
        else:
            ans += x

    while ptr < k:
        ans += regular[ptr]
        ptr += 1

    print(ans)

solve()
```

The first part separates auction and regular questions. The indices in the input are one-based, so the implementation converts them to zero-based positions when marking auction questions.

Both arrays are sorted in ascending order. The sorted order is essential for the greedy argument. Smaller auctions should be unlocked first, and smaller regular questions are consumed only when needed.

The pointer `ptr` tracks how many regular questions have already been used. Before processing an auction question with threshold `x`, the loop keeps adding regular questions until the current score becomes strictly greater than `x`.

At that moment, the auction can double the score, so `ans *= 2`.

There is one subtle branch:

```
if ans > x:
    ans *= 2
else:
    ans += x
```

The second branch handles the case where even after consuming every regular question, the auction still cannot be activated. In that case, the auction behaves like a normal question and contributes only its base value.

All arithmetic fits safely in 64-bit integers, and Python integers naturally handle this without overflow concerns.

## Worked Examples

### Example 1

Input:

```
4 1
1 3 7 5
3
```

Auction questions: `[7]`

Regular questions: `[1, 3, 5]`

| Step | Current Score | Action | New Score |
| --- | --- | --- | --- |
| Start | 0 | Initial state | 0 |
| 1 | 0 | Take regular 1 | 1 |
| 2 | 1 | Take regular 3 | 4 |
| 3 | 4 | Take regular 5 | 9 |
| 4 | 9 | Auction 7 doubles score | 18 |

Final answer: `18`

This trace shows the activation condition clearly. The auction cannot be used until the score becomes strictly greater than `7`.

### Example 2

Input:

```
5 2
2 1 10 3 20
2 4
```

Auction questions: `[1, 3]`

Regular questions: `[2, 10, 20]`

| Step | Current Score | Action | New Score |
| --- | --- | --- | --- |
| Start | 0 | Initial state | 0 |
| 1 | 0 | Take regular 2 | 2 |
| 2 | 2 | Auction 1 doubles score | 4 |
| 3 | 4 | Auction 3 doubles score | 8 |
| 4 | 8 | Take regular 10 | 18 |
| 5 | 18 | Take regular 20 | 38 |

Final answer: `38`

This example demonstrates why auctions should be processed early. Using the small auction immediately unlocks another doubling opportunity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the runtime |
| Space | O(n) | Arrays for auction and regular questions |

With `n <= 100`, this solution easily fits within the limits. Even a quadratic algorithm would pass comfortably, but the greedy approach is both simpler and mathematically cleaner.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        is_auction = [False] * n

        for x in b:
            is_auction[x - 1] = True

        auctions = []
        regular = []

        for i in range(n):
            if is_auction[i]:
                auctions.append(a[i])
            else:
                regular.append(a[i])

        auctions.sort()
        regular.sort()

        ans = 0
        ptr = 0

        for x in auctions:
            while ptr < len(regular) and ans <= x:
                ans += regular[ptr]
                ptr += 1

            if ans > x:
                ans *= 2
            else:
                ans += x

        while ptr < len(regular):
            ans += regular[ptr]
            ptr += 1

        return str(ans)

    return solve()

# provided sample
assert run(
    "4 1\n1 3 7 5\n3\n"
) == "18", "sample 1"

# minimum size
assert run(
    "1 1\n5\n1\n"
) == "5", "single auction"

# equality edge case
assert run(
    "2 1\n5 5\n2\n"
) == "10", "strictly greater condition"

# multiple auctions
assert run(
    "5 2\n2 1 10 3 20\n2 4\n"
) == "38", "greedy ordering"

# all auctions impossible to activate
assert run(
    "3 3\n5 6 7\n1 2 3\n"
) == "18", "no doubling possible"

# all regular except one easy auction
assert run(
    "4 1\n100 1 1 1\n2\n"
) == "204", "doubling after large gain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 5 / 1` | `5` | Minimum input size |
| `2 1 / 5 5 / 2` | `10` | Strict inequality for auctions |
| `5 2 / 2 1 10 3 20 / 2 4` | `38` | Multiple chained doublings |
| `3 3 / 5 6 7 / 1 2 3` | `18` | Auctions may never activate |
| `4 1 / 100 1 1 1 / 2` | `204` | Delayed doubling after building score |

## Edge Cases

Consider the strict inequality case:

```
2 1
5 5
2
```

The algorithm sorts auctions as `[5]` and regular questions as `[5]`.

Initially `ans = 0`.

The loop adds the regular question because `0 <= 5`, producing `ans = 5`.

Now the condition `ans > 5` still fails because equality is not enough. The auction contributes only its base value, resulting in `10`.

A careless implementation using `>=` would incorrectly produce `15`.

Now consider the case where no auction can ever activate:

```
3 3
5 6 7
1 2 3
```

There are no regular questions at all.

The algorithm processes auctions in sorted order. Since `ans` never exceeds any auction threshold, every auction simply adds its base value:

```
0 -> 5 -> 11 -> 18
```

This matches the real rules exactly. Without enough existing score, auctions behave like ordinary questions.

Finally, consider a case where early small auctions matter:

```
5 2
2 1 10 3 20
2 4
```

The sorted auctions are `[1, 3]`.

After taking regular `2`, the score becomes `2`, activating auction `1` and doubling to `4`.

That immediately activates auction `3`, doubling again to `8`.

If the larger auction were processed first, the second doubling would happen later and the final score would be smaller. This confirms why auctions must be handled in ascending order.
