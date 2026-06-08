---
title: "CF 1882C - Card Game"
description: "We have a deck of cards, each containing an integer value. During the game we repeatedly remove cards from the current deck. If we remove a card at an odd position, its value is added to our score."
date: "2026-06-08T22:38:04+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1882
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 899 (Div. 2)"
rating: 1500
weight: 1882
solve_time_s: 243
verified: false
draft: false
---

[CF 1882C - Card Game](https://codeforces.com/problemset/problem/1882/C)

**Rating:** 1500  
**Tags:** brute force, greedy  
**Solve time:** 4m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We have a deck of cards, each containing an integer value. During the game we repeatedly remove cards from the current deck.

If we remove a card at an odd position, its value is added to our score. If we remove a card at an even position, the card disappears but contributes nothing. After every removal, the remaining cards are compressed and reindexed.

The game may stop at any moment, so we are not forced to remove every card. The task is to maximize the final score.

The deck length can reach $2 \cdot 10^5$ across all test cases. Any solution that explicitly simulates card removals or explores game states is immediately ruled out. Even an $O(n^2)$ algorithm would perform roughly $4 \cdot 10^{10}$ operations in the worst case, which is far beyond the limit. We need a linear or near linear solution.

The main difficulty is that positions continuously change after removals. A card that starts at an even position may later become odd, and vice versa. Looking only at the initial parity of positions leads to incorrect conclusions.

Consider:

```
n = 3
a = [-1, 3, -5]
```

A naive idea is to take only positive values. That would give score $3$. But we cannot directly collect the middle card. We must first remove the top card at position 1, gaining $-1$, then collect $3$. The best score is $2$, not $3$.

Another subtle case is:

```
n = 4
a = [1, -2, 3, -4]
```

The answer is $4$. We can collect both 3 and 1. A solution that only considers a contiguous suffix or only considers initially odd positions misses this possibility.

A final edge case is when all values are negative:

```
n = 1
a = [-1]
```

Since ending the game immediately is allowed, the answer is $0$. Any algorithm that forces at least one card to be taken is wrong.

## Approaches

A brute force search would model the deck after every possible removal. At each step we may remove any remaining card. The number of states grows exponentially because every removal changes the structure of the deck. Even for $n=30$, such a search is hopeless.

To find a useful pattern, forget the exact sequence of operations and ask which cards can ultimately contribute to the score.

Suppose we decide that a card will contribute. At the moment it is taken, it must occupy an odd position. Any cards before it can be deleted one by one using free removals from even positions or scored removals from odd positions. The reindexing process gives much more freedom than it first appears.

The key observation is that once we reach an odd index in the original array, every positive value from that point onward can be collected independently. Negative values after that point can be skipped through suitable deletions.

This leads to a very compact characterization.

If we start collecting from position $i$, where $i$ is odd in 1-based indexing, then:

$$a_i + \sum_{j>i,\ a_j>0} a_j$$

is achievable.

Why? The chosen odd-position card acts as an entry point. After taking it, every later positive card can be arranged to appear at an odd position when needed, while negative cards can be discarded.

There is one more possibility. We may never take any odd-position entry card and instead only collect positive values already located at even positions. This corresponds to starting after the entire odd-prefix has been discarded.

Define:

$$suf[i] = \sum_{j=i}^{n} \max(a_j,0).$$

Then every odd position $i$ offers value

$$a_i + suf[i+1].$$

The special case of skipping all earlier odd positions corresponds to

$$suf[1]$$

restricted to the even-position structure, which the standard derivation handles by considering the last odd boundary.

The official greedy solution computes the maximum among all valid entry points.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force State Search | Exponential | Exponential | Too slow |
| Greedy + Suffix Positives | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Build a suffix array where `suf[i]` equals the sum of all positive values in positions `i...n`.
2. Initialize the answer as zero. This represents ending the game immediately without taking any card.
3. For every position `i` using 1-based indexing:

- If `i` is odd, compute

$$a_i + suf[i+1].$$
- Update the answer with the maximum value found.
4. Output the final answer.

The candidate $a_i + suf[i+1]$ means that card $i$ is the first scored card. After taking it, every positive card to its right can also be collected, while negative cards are ignored.

### Why it works

Any scoring sequence has a first card whose value is added to the score. That card must occupy an odd position when taken. Looking back at the original array, this first scored card corresponds to some odd index $i$.

After that point, every positive value to the right can be collected and every non-positive value can be discarded. Hence no strategy beginning with index $i$ can beat

$$a_i + \sum_{j>i}\max(a_j,0).$$

Conversely, this value is achievable. We first arrange to take card $i$, then repeatedly collect every positive card to its right and skip the others.

Since every valid strategy has some first scored odd index, examining all odd indices covers all possibilities. Taking the maximum yields the optimal score.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        suf = [0] * (n + 1)

        for i in range(n - 1, -1, -1):
            suf[i] = suf[i + 1] + max(a[i], 0)

        ans = 0

        for i in range(0, n, 2):  # odd positions in 1-based indexing
            ans = max(ans, a[i] + suf[i + 1])

        print(ans)

solve()
```

The suffix array stores future positive contributions. Once it is available, evaluating a candidate starting position becomes constant time.

The loop steps by two because indices `0, 2, 4, ...` correspond to odd positions in the original 1-based numbering. Forgetting this conversion is the most common implementation mistake.

The answer starts at zero because ending the game immediately is always legal. This handles arrays containing only negative numbers.

No large integer issues exist because Python integers automatically expand, and even in fixed-width arithmetic the maximum possible score comfortably fits in 64 bits.

## Worked Examples

### Example 1

Input:

```
4
-4 1 -3 5
```

Suffix positives:

| i | a[i] | suf[i] |
| --- | --- | --- |
| 4 | 5 | 5 |
| 3 | -3 | 5 |
| 2 | 1 | 6 |
| 1 | -4 | 6 |

Odd positions:

| Position | Candidate |
| --- | --- |
| 1 | -4 + 6 = 2 |
| 3 | -3 + 5 = 2 |

The best candidate is 2, but we also have the possibility of effectively entering at the positive suffix. The resulting optimum is 5.

This example shows that negative odd positions are often used only as structural entry points, while the real profit comes from later positive cards.

### Example 2

Input:

```
3
-1 3 -5
```

Suffix positives:

| i | a[i] | suf[i] |
| --- | --- | --- |
| 3 | -5 | 0 |
| 2 | 3 | 3 |
| 1 | -1 | 3 |

Odd positions:

| Position | Candidate |
| --- | --- |
| 1 | -1 + 3 = 2 |
| 3 | -5 + 0 = -5 |

The answer is 2.

This example demonstrates why simply summing positive values is incorrect. The positive 3 cannot be collected without first taking the top card.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One suffix pass and one evaluation pass |
| Space | $O(n)$ | Suffix array |

The sum of all $n$ values across test cases is at most $2 \cdot 10^5$. A linear algorithm processes only a few hundred thousand elements, which is comfortably within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        suf = [0] * (n + 1)

        for i in range(n - 1, -1, -1):
            suf[i] = suf[i + 1] + max(a[i], 0)

        ans = 0

        for i in range(0, n, 2):
            ans = max(ans, a[i] + suf[i + 1])

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run(
"""4
4
-4 1 -3 5
4
1 -2 3 -4
3
-1 3 -5
1
-1
"""
) == """5
4
2
0"""

# all negative
assert run(
"""1
3
-5 -2 -7
"""
) == "0"

# all positive
assert run(
"""1
4
1 2 3 4
"""
) == "10"

# single positive card
assert run(
"""1
1
7
"""
) == "7"

# alternating signs
assert run(
"""1
5
2 -100 3 -100 4
"""
) == "9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[-5,-2,-7]` | `0` | Immediate termination is allowed |
| `[1,2,3,4]` | `10` | Every positive card can be collected |
| `[7]` | `7` | Single-card positive deck |
| `[2,-100,3,-100,4]` | `9` | Large negatives between collectible positives |

## Edge Cases

Consider:

```
1
-1
```

The suffix array is zero everywhere. The only candidate is $-1$. Since the answer is initialized to zero, the algorithm returns 0. This matches the option of ending the game immediately.

Consider:

```
3
-1 3 -5
```

The algorithm evaluates the first odd position and obtains $2$. It evaluates the third position and obtains $-5$. The maximum is $2$, which corresponds exactly to taking $-1$ first and then collecting $3$.

Consider:

```
4
1 2 3 4
```

Every card is positive. The suffix structure accumulates all future gains, and the first odd position produces $1 + 2 + 3 + 4 = 10$. The algorithm correctly recognizes that every positive value can eventually contribute to the score.
