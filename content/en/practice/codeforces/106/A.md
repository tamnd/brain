---
title: "CF 106A - Card Game"
description: "We are given the trump suit for a game of Durak and two cards. The task is to decide whether the first card can beat the second card under the game rules. Each card has a rank and a suit. The ranks are ordered as: A card can beat another card in exactly two situations."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 106
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 82 (Div. 2)"
rating: 1000
weight: 106
solve_time_s: 97
verified: true
draft: false
---

[CF 106A - Card Game](https://codeforces.com/problemset/problem/106/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the trump suit for a game of Durak and two cards. The task is to decide whether the first card can beat the second card under the game rules.

Each card has a rank and a suit. The ranks are ordered as:

```
6 < 7 < 8 < 9 < T < J < Q < K < A
```

A card can beat another card in exactly two situations.

If both cards have the same suit, then the higher-ranked card wins.

If the suits are different, then the first card wins only if it belongs to the trump suit and the second card does not.

The input size is tiny, only two cards and one trump suit. There is no performance challenge here. Any constant-time implementation is easily fast enough within the limits.

The tricky part is handling the rules in the correct order. Several cases look similar but behave differently.

One easy mistake is forgetting that a trump card beats any non-trump card, regardless of rank.

For example:

```
Trump = H
6H  AS
```

The correct answer is:

```
YES
```

Even though Ace is much stronger than 6 in normal rank order, the heart card is trump.

Another common mistake is allowing a higher-ranked card of a different non-trump suit to win.

For example:

```
Trump = D
AS  KC
```

The correct answer is:

```
NO
```

The suits differ, and neither card is trump, so the first card cannot beat the second.

A third edge case is when both cards are trump cards. In that situation, rank comparison matters again.

For example:

```
Trump = S
7S  9S
```

The correct answer is:

```
NO
```

Both cards are trump, so we compare ranks normally, and 7 is weaker than 9.

## Approaches

A brute-force way to think about the problem is to manually encode every possible winning relationship between cards. Since there are only 36 cards, we could theoretically precompute which card beats which other card and then perform a lookup.

That approach works because the number of cards is extremely small. A full comparison table would contain at most:

```
36 × 36 = 1296
```

relationships.

Still, this is unnecessary. The game rules already describe a direct comparison process. Instead of storing every possible pair, we can evaluate the relationship between the two cards immediately.

The key observation is that only three facts matter:

First, whether the suits are equal.

Second, whether the first card is trump.

Third, the relative order of the ranks.

Once we organize the rules around those conditions, the implementation becomes straightforward.

If the suits are equal, we compare rank values.

If the suits differ, the first card wins only when it is trump and the second card is not.

Everything else loses.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(36²) preprocessing | O(36²) | Accepted but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the trump suit.
2. Read the two cards.
3. Separate each card into its rank and suit components.
4. Store the rank order in a string or mapping:

```
"6789TJQKA"
```

The index inside this string represents card strength.

1. Check whether both cards have the same suit.

If they do, compare their rank positions. The first card beats the second only if its rank index is larger.

1. If the suits are different, check whether the first card is trump and the second card is not trump.

If that condition holds, print `"YES"`.

1. In all remaining cases, print `"NO"`.

### Why it works

The algorithm directly mirrors the game rules.

When suits match, only rank matters, so comparing rank indices gives the correct winner.

When suits differ, the only way to beat another card is by using a trump card against a non-trump card. The algorithm checks exactly that condition.

No other winning situations exist in the rules, so every possible input is handled correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    trump = input().strip()
    first, second = input().split()

    rank_order = "6789TJQKA"

    r1, s1 = first[0], first[1]
    r2, s2 = second[0], second[1]

    if s1 == s2:
        if rank_order.index(r1) > rank_order.index(r2):
            print("YES")
        else:
            print("NO")
    else:
        if s1 == trump and s2 != trump:
            print("YES")
        else:
            print("NO")

solve()
```

The solution starts by reading the trump suit and the two cards. Each card is represented by exactly two characters, so extracting the rank and suit is simply indexing into the string.

The string `"6789TJQKA"` defines the rank hierarchy. A larger index means a stronger card. This avoids long chains of conditionals and keeps the comparison logic compact.

The first major branch checks whether the suits match. If they do, the game rules say only rank matters, so we compare indices.

If the suits differ, rank no longer matters unless trump is involved. The code checks whether the first card is trump while the second is not. That is the only cross-suit winning condition.

One subtle point is that a weaker trump still beats a stronger non-trump. The implementation handles this automatically because rank comparison is skipped when suits differ.

## Worked Examples

### Example 1

Input:

```
H
QH 9S
```

| Variable | Value |
| --- | --- |
| trump | H |
| first | QH |
| second | 9S |
| s1 | H |
| s2 | S |

The suits differ, so rank comparison is ignored.

The first card belongs to the trump suit, while the second does not.

Output:

```
YES
```

This example demonstrates the trump rule overriding normal rank order.

### Example 2

Input:

```
S
7S 9S
```

| Variable | Value |
| --- | --- |
| trump | S |
| first | 7S |
| second | 9S |
| s1 | S |
| s2 | S |
| rank(7) | 1 |
| rank(9) | 3 |

The suits are the same, so we compare ranks directly.

Since `1 < 3`, the first card is weaker.

Output:

```
NO
```

This example shows that when both cards share the same suit, even trump cards follow normal rank ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few comparisons and lookups are performed |
| Space | O(1) | The algorithm uses a constant amount of extra memory |

The solution easily fits within the limits because the amount of work never depends on input size. Only two cards are processed.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    trump = input().strip()
    first, second = input().split()

    rank_order = "6789TJQKA"

    r1, s1 = first[0], first[1]
    r2, s2 = second[0], second[1]

    if s1 == s2:
        if rank_order.index(r1) > rank_order.index(r2):
            print("YES")
        else:
            print("NO")
    else:
        if s1 == trump and s2 != trump:
            print("YES")
        else:
            print("NO")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue()

# provided sample
assert run("H\nQH 9S\n") == "YES\n", "sample 1"

# same suit, higher rank wins
assert run("D\nAH KH\n") == "YES\n", "same suit higher rank"

# same suit, lower rank loses
assert run("C\n7S TS\n") == "NO\n", "same suit lower rank"

# trump beats stronger non-trump
assert run("H\n6H AS\n") == "YES\n", "trump overrides rank"

# different suits, no trump involved
assert run("D\nAS KC\n") == "NO\n", "different non-trump suits"

# both trump cards, compare rank normally
assert run("S\nJS QS\n") == "NO\n", "both trump cards"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `H / QH 9S` | `YES` | Trump card beats non-trump |
| `D / AH KH` | `YES` | Same-suit rank comparison |
| `C / 7S TS` | `NO` | Lower rank loses within same suit |
| `H / 6H AS` | `YES` | Weak trump still beats strong non-trump |
| `D / AS KC` | `NO` | Different non-trump suits cannot beat each other |
| `S / JS QS` | `NO` | Trump vs trump still depends on rank |

## Edge Cases

Consider the case where a weak trump beats a strong non-trump.

Input:

```
H
6H AS
```

The algorithm first sees that the suits differ. It does not compare ranks. Instead, it checks the trump condition. Since `6H` is trump and `AS` is not, the answer becomes `"YES"`.

Now consider two different non-trump suits.

Input:

```
D
AS KC
```

The suits differ, so the algorithm checks whether the first card is trump. It is not. Since no winning rule applies, the output is `"NO"`.

Finally, consider two trump cards.

Input:

```
S
7S 9S
```

The suits are equal, so the algorithm compares ranks directly. The index of `7` is smaller than the index of `9`, so the first card loses and the output is `"NO"`.

These cases confirm that the implementation correctly separates same-suit logic from trump logic, which is the central detail of the problem.
