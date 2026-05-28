---
title: "CF 140B - New Year Cards"
description: "Alexander receives cards from friends one by one. Friend i sends card i, so card numbers and friend numbers are the same thing. At any moment Alexander may decide to send cards to some friends. He never creates new cards, he only reuses cards he has already received."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 140
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 100"
rating: 1800
weight: 140
solve_time_s: 161
verified: false
draft: false
---

[CF 140B - New Year Cards](https://codeforces.com/problemset/problem/140/B)

**Rating:** 1800  
**Tags:** brute force, greedy, implementation  
**Solve time:** 2m 41s  
**Verified:** no  

## Solution
## Problem Understanding

Alexander receives cards from friends one by one. Friend `i` sends card `i`, so card numbers and friend numbers are the same thing. At any moment Alexander may decide to send cards to some friends. He never creates new cards, he only reuses cards he has already received.

When Alexander sends a card to friend `i`, two rules apply. He cannot send card `i` back to that friend, and among all remaining cards he currently owns, he always picks the one he personally likes the most.

Each friend also has their own ranking of cards. We want every friend to receive the best card they could possibly get under Alexander's behavior. Our task is not to choose the card directly, because Alexander's choice is forced. Instead, we choose the moment when each friend receives their card. The output asks for these moments in a compressed form: for every friend `i`, print some friend `k` such that Alexander sends the card to `i` immediately after receiving card `k`.

The constraints are small enough to allow fairly direct simulation. `n` is at most `300`, so even cubic algorithms are fine. An `O(n^3)` solution performs around `27 million` operations in the worst case, which is comfortable in Python under a 2 second limit. This means we do not need advanced graph algorithms or flow techniques. The challenge is understanding the structure of the process and proving that a greedy construction is valid.

There are several subtle cases that easily break naive reasoning.

One common mistake is assuming that each friend should receive their favorite card among all cards except their own. That ignores Alexander's preferences and card availability.

Consider:

```
n = 3

Friend 1: 2 3 1
Friend 2: 1 3 2
Friend 3: 1 2 3

Alexander: 3 2 1
```

Friend 1 would love card `2`, but Alexander prefers card `3` more. Once card `3` becomes available, Alexander must send it instead of `2`. So timing matters more than the final set of available cards.

Another easy bug is forgetting that cards appear over time.

```
n = 3

Friend 1: 3 2 1
Friend 2: 3 1 2
Friend 3: 1 2 3

Alexander: 3 1 2
```

Friends `1` and `2` both want card `3`, but nobody can receive it before Alexander gets card `3` from friend `3`. A solution that only reasons about rankings without respecting arrival times will generate impossible schedules.

A third trap is assuming every send operation must happen at a distinct moment. The statement explicitly allows Alexander to send cards to multiple friends immediately after receiving the same card. This matters because many friends may optimally receive the same card at the same time.

For example:

```
n = 4

Alexander: 4 3 2 1
```

If card `4` is available and valid for several friends, all of them may receive it immediately after friend `4` sends their card.

## Approaches

The brute force idea is to simulate every possible schedule of receiving and sending cards. After each received card, Alexander may send cards to any subset of unsatisfied friends. For each friend we could test which card they eventually receive and keep the best schedule.

This quickly becomes impossible. Even after each of the `n` receiving events there are exponentially many choices of which friends to process. The total number of schedules explodes far beyond anything manageable.

The key observation is that Alexander's behavior is completely deterministic once we know which cards are currently available.

Suppose Alexander has already received some set of cards. For friend `i`, Alexander scans his own preference order from best to worst and picks the first available card that is not `i`.

So for every friend `i`, their received card depends only on the set of cards Alexander currently owns.

Now think about what sets are actually possible. After receiving cards `1...k`, Alexander owns exactly those cards. No other state can occur. This means the process has only `n` meaningful moments:

```
after receiving 1
after receiving 2
...
after receiving n
```

For each friend and each prefix `1...k`, we can compute which card Alexander would send at that moment.

Among all these moments, we choose the one that gives the friend the highest-ranked card according to that friend's preference list.

This turns the problem into pure brute force over prefixes.

For friend `i` and time `k`:

```
available cards = {1,2,...,k}
chosen card = highest-ranked available card in Alexander's order, excluding i
```

Then we compare all possible `k` and pick the best outcome for friend `i`.

The brute force becomes feasible because there are only `n^2` states, and evaluating each state takes at most `O(n)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Exhaustive schedule search | Exponential | Exponential | Too slow |
| Prefix simulation | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read every friend's preference permutation.
2. Read Alexander's preference permutation.
3. Build a position table for every friend.

`rank[i][x]` stores how much friend `i` likes card `x`. Smaller values mean better cards.
4. For every prefix length `k` from `1` to `n`, determine which card Alexander would send to each friend if he sent the card immediately after receiving card `k`.

At this moment Alexander owns cards `1...k`.
5. To determine the sent card for friend `i`, scan Alexander's preference order from best to worst.

The first card satisfying both conditions is selected:

`card <= k`, meaning the card is already available.

`card != i`, because Alexander cannot return a friend's own card.
6. Compare this candidate card against the best card already found for friend `i`.

Use the friend's ranking table to decide which card they prefer more.
7. If the new card is better, store:

the card itself,

and the moment `k` when it becomes achievable.
8. After processing all prefixes, output the chosen moments for all friends.

### Why it works

At any moment after receiving card `k`, the available cards are exactly `{1,2,...,k}`. Alexander's choice among those cards is deterministic because he always picks his favorite valid card.

So every feasible outcome for a friend corresponds to exactly one prefix length `k`. Our algorithm explicitly checks all such prefixes.

For each friend we keep the best achievable card according to that friend's preferences. Since every possible sending moment is examined, no better outcome can exist outside our search. The stored prefix is therefore optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    prefs = [list(map(int, input().split())) for _ in range(n)]
    alex = list(map(int, input().split()))

    rank = [[0] * (n + 1) for _ in range(n)]

    for i in range(n):
        for pos, card in enumerate(prefs[i]):
            rank[i][card] = pos

    best_card = [-1] * n
    answer = [1] * n

    for k in range(1, n + 1):

        for i in range(n):

            chosen = -1

            for card in alex:
                if card <= k and card != i + 1:
                    chosen = card
                    break

            if best_card[i] == -1 or rank[i][chosen] < rank[i][best_card[i]]:
                best_card[i] = chosen
                answer[i] = k

    print(*answer)

solve()
```

The first part reads the permutations and builds `rank`. Instead of repeatedly searching inside a preference list, we precompute positions. This turns comparisons like “does friend `i` prefer card `a` or card `b`?” into constant time operations.

The outer loop iterates over all prefixes `1...k`. That directly represents the moment after Alexander receives card `k`.

For every friend we simulate Alexander's forced choice. We scan Alexander's preference permutation from left to right because earlier cards are more preferred by Alexander. The first available card that is not the friend's own card is exactly what Alexander would send.

The comparison

```
rank[i][chosen] < rank[i][best_card[i]]
```

checks whether the friend prefers the new candidate more strongly.

One subtle detail is the indexing. Friends are stored with zero-based indices in arrays, but card numbers are one-based. The condition

```
card != i + 1
```

handles this conversion carefully.

Another subtle point is that we store the moment `k`, not the card itself. The output format asks for the friend whose card was just received before sending.

## Worked Examples

### Sample 1

Input:

```
4
1 2 3 4
4 1 3 2
4 3 1 2
3 4 2 1
3 1 2 4
```

Alexander's preference order is:

```
3 > 1 > 2 > 4
```

We process prefixes one by one.

| k | Available cards | Friend 1 gets | Friend 2 gets | Friend 3 gets | Friend 4 gets |
| --- | --- | --- | --- | --- | --- |
| 1 | {1} | none | 1 | 1 | 1 |
| 2 | {1,2} | 2 | 1 | 1 | 1 |
| 3 | {1,2,3} | 3 | 3 | 1 | 3 |
| 4 | {1,2,3,4} | 3 | 3 | 1 | 3 |

Now compare using each friend's preferences.

Friend `1` prefers `2` over `3`, so the best moment is `k=2`.

Friend `2` prefers `1` over `3`, so the best moment is `k=1`.

Friend `3` cannot receive card `3`, and prefers `1` over `4` and `2`, so `k=1`.

Friend `4` prefers `3`, achievable from `k=3`.

Final output:

```
2 1 1 3
```

The sample output uses `4` instead of `3` for the last friend, which is also valid because card `3` is still sent after receiving card `4`.

This trace demonstrates that delaying a send operation can make the result worse. Friend `1` should receive card `2` before card `3` becomes available.

### Custom Example

Input:

```
3
2 3 1
1 3 2
1 2 3
3 2 1
```

Alexander prefers:

```
3 > 2 > 1
```

| k | Available cards | Friend 1 gets | Friend 2 gets | Friend 3 gets |
| --- | --- | --- | --- | --- |
| 1 | {1} | 1 | 1 | none |
| 2 | {1,2} | 2 | 1 | 2 |
| 3 | {1,2,3} | 3 | 3 | 2 |

Now evaluate from each friend's perspective.

| Friend | Best card | Achieved at k |
| --- | --- | --- |
| 1 | 2 | 2 |
| 2 | 1 | 1 |
| 3 | 2 | 2 |

Output:

```
2 1 2
```

This example shows that a friend's optimal card may disappear once a more preferred card for Alexander becomes available.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | There are `n` prefixes, `n` friends, and up to `n` scans through Alexander's preference order |
| Space | O(n^2) | Preference rankings for all friends |

With `n ≤ 300`, the cubic runtime is easily fast enough. Around `27 million` simple operations is well within Python's limits for a 2 second contest setting.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n = int(input())

    prefs = [list(map(int, input().split())) for _ in range(n)]
    alex = list(map(int, input().split()))

    rank = [[0] * (n + 1) for _ in range(n)]

    for i in range(n):
        for pos, card in enumerate(prefs[i]):
            rank[i][card] = pos

    best_card = [-1] * n
    answer = [1] * n

    for k in range(1, n + 1):
        for i in range(n):

            chosen = -1

            for card in alex:
                if card <= k and card != i + 1:
                    chosen = card
                    break

            if best_card[i] == -1 or rank[i][chosen] < rank[i][best_card[i]]:
                best_card[i] = chosen
                answer[i] = k

    return " ".join(map(str, answer))

# provided sample
assert run(
"""4
1 2 3 4
4 1 3 2
4 3 1 2
3 4 2 1
3 1 2 4
"""
) in ["2 1 1 3", "2 1 1 4"]

# minimum size
assert run(
"""2
1 2
2 1
1 2
"""
) == "2 1"

# everyone likes highest available card
assert run(
"""3
3 2 1
3 2 1
3 2 1
3 2 1
"""
) == "2 1 2"

# delayed sending is worse
assert run(
"""3
2 3 1
1 3 2
1 2 3
3 2 1
"""
) == "2 1 2"

# boundary ordering
assert run(
"""4
2 1 3 4
1 2 3 4
4 3 2 1
3 4 1 2
4 3 2 1
"""
) == "2 1 1 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum `n=2` case | `2 1` | Smallest valid input |
| Everyone prefers strongest card | `2 1 2` | Multiple friends sharing the same optimal timing |
| Delayed sending hurts | `2 1 2` | Timing matters more than final availability |
| Boundary ordering case | `2 1 1 3` | Correct handling of self-card exclusion |

## Edge Cases

Consider the case where Alexander's favorite card eventually blocks a better outcome for some friend.

```
3
2 3 1
1 3 2
1 2 3
3 2 1
```

At `k=2`, friend `1` receives card `2`. At `k=3`, Alexander must switch to card `3` because it becomes available and is higher in his own ranking. Friend `1` actually prefers `2`, so the earlier moment is optimal. The algorithm handles this because it checks every prefix independently instead of assuming later is always better.

Now consider a case where several friends should be processed at the same moment.

```
4
4 1 2 3
4 1 2 3
4 1 2 3
1 2 3 4
4 3 2 1
```

As soon as card `4` appears, Alexander sends it to every friend except friend `4`. The algorithm naturally allows this because each friend independently records the same optimal prefix `k=4`.

Finally, consider the self-card restriction.

```
2
1 2
2 1
2 1
```

After receiving card `1`, friend `1` cannot receive it, so no valid send exists yet. After receiving card `2`, friend `1` receives card `2`. Friend `2` can receive card `1` immediately after `k=1`. The algorithm explicitly checks `card != i + 1`, so it never returns a friend's own card.
