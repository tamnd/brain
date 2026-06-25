---
title: "CF 105809G - Game of Marbles"
description: "We have a collection of marbles, each containing an integer. One player, Sebastian, takes every marble whose number is odd. The other player, Sebastiàn, takes every marble whose number is even. The winner is determined only by how many marbles each player receives."
date: "2026-06-25T15:29:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105809
codeforces_index: "G"
codeforces_contest_name: "Code Rush 2025"
rating: 0
weight: 105809
solve_time_s: 36
verified: true
draft: false
---

[CF 105809G - Game of Marbles](https://codeforces.com/problemset/problem/105809/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of marbles, each containing an integer. One player, Sebastian, takes every marble whose number is odd. The other player, Sebastiàn, takes every marble whose number is even.

The winner is determined only by how many marbles each player receives. If the counts are equal, Sebastian wins the tie. We must output `"Sebastian"` if Sebastiàn has strictly more marbles than Sebastian. Otherwise we output `"Notbastian"`.

The input consists of an integer `n`, followed by `n` marble values. The actual values can be as large as `10^9`, but only their parity matters. Since `n` is at most `10^6`, any algorithm that examines each marble once is easily fast enough, while anything significantly more expensive than linear time would be unnecessary. With one million numbers, an `O(n)` scan performs about one million operations, which is trivial within the limits.

The main source of mistakes is the tie rule.

Consider:

```
4
1 1 2 2
```

There are two odd marbles and two even marbles. Since the counts are equal, Sebastian wins, meaning Sebastiàn does not keep the name. The correct output is:

```
Notbastian
```

A careless implementation that checks `even_count >= odd_count` would incorrectly print `"Sebastian"`.

Another easy-to-miss case is when all marbles belong to one player.

```
3
2 4 6
```

Sebastiàn gets all three marbles and Sebastian gets none, so the correct output is:

```
Sebastian
```

Likewise:

```
3
1 3 5
```

gives

```
Notbastian
```

because Sebastiàn receives zero marbles.

## Approaches

The most direct solution is to simulate the rules exactly. For every marble, determine whether its number is even or odd and increment the corresponding counter. At the end, compare the two counters according to the game's winning condition.

One could imagine a brute-force interpretation that explicitly stores Sebastian's marbles and Sebastiàn's marbles in separate arrays and then compares their sizes. This is correct because the game outcome depends only on how many marbles each player receives. The extra storage is unnecessary, however, because only the counts matter.

The key observation is that the marble values themselves never influence the result beyond parity. We do not care whether a marble contains `2` or `1000000000`, only whether it is even. Once we recognize this, the entire problem reduces to counting even and odd numbers.

After counting, Sebastiàn keeps the name only when the number of even marbles is strictly greater than the number of odd marbles. Every other situation, including ties, produces `"Notbastian"`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Store both players' marbles explicitly | O(n) | O(n) | Accepted but unnecessary |
| Count evens and odds | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and the `n` marble values.
2. Initialize `even_count = 0` and `odd_count = 0`.
3. Scan through every marble value.
4. If the value is even, increment `even_count`; otherwise increment `odd_count`.
5. After processing all marbles, compare the counts.
6. If `even_count > odd_count`, print `"Sebastian"` because Sebastiàn has more marbles.
7. Otherwise print `"Notbastian"`. This includes the tie case, where Sebastian wins by rule.

### Why it works

Every marble belongs to exactly one player based solely on parity. Counting even numbers gives the number of marbles received by Sebastiàn, and counting odd numbers gives the number received by Sebastian. The winner is defined entirely by comparing these counts, with ties awarded to Sebastian. Since the algorithm computes exactly these two quantities and applies the stated comparison rule, it always produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

even_count = 0

for x in a:
    if x % 2 == 0:
        even_count += 1

odd_count = n - even_count

if even_count > odd_count:
    print("Sebastian")
else:
    print("Notbastian")
```

The solution performs a single pass through the array and counts even values. Since every marble is either even or odd, the odd count can be computed as `n - even_count`.

The comparison at the end is strict. This is the most important implementation detail. Using `>=` would incorrectly award ties to Sebastiàn, contradicting the statement.

No overflow issues exist because the counts never exceed `n`, which is at most `10^6`.

## Worked Examples

### Example 1

Input:

```
4
1 2 2 4
```

| Marble | Parity | even_count | odd_count |
| --- | --- | --- | --- |
| 1 | Odd | 0 | 1 |
| 2 | Even | 1 | 1 |
| 2 | Even | 2 | 1 |
| 4 | Even | 3 | 1 |

Final comparison: `3 > 1`.

Output:

```
Sebastian
```

This demonstrates the normal winning case for Sebastiàn, who receives more marbles than Sebastian.

### Example 2

Input:

```
4
1 1 2 2
```

| Marble | Parity | even_count | odd_count |
| --- | --- | --- | --- |
| 1 | Odd | 0 | 1 |
| 1 | Odd | 0 | 2 |
| 2 | Even | 1 | 2 |
| 2 | Even | 2 | 2 |

Final comparison: `2 = 2`.

Output:

```
Notbastian
```

This example highlights the tie rule. Even though both players receive the same number of marbles, Sebastian wins ties, so Sebastiàn must change his name.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each marble is examined exactly once |
| Space | O(1) | Only a few counters are stored |

With up to `10^6` marbles, a linear scan is easily fast enough. Memory usage remains constant regardless of input size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    a = list(map(int, input().split()))

    even_count = sum(x % 2 == 0 for x in a)
    odd_count = n - even_count

    if even_count > odd_count:
        return "Sebastian\n"
    return "Notbastian\n"

# provided samples
assert run("4\n1 2 2 4\n") == "Sebastian\n", "sample 1"
assert run("4\n1 1 2 2\n") == "Notbastian\n", "sample 2"

# custom cases
assert run("1\n2\n") == "Sebastian\n", "single even marble"
assert run("1\n1\n") == "Notbastian\n", "single odd marble"
assert run("5\n2 4 6 8 10\n") == "Sebastian\n", "all even"
assert run("5\n1 3 5 7 9\n") == "Notbastian\n", "all odd"
assert run("6\n1 2 3 4 5 6\n") == "Notbastian\n", "tie case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 2` | `Sebastian` | Minimum size, even marble |
| `1 / 1` | `Notbastian` | Minimum size, odd marble |
| All even values | `Sebastian` | Sebastiàn receives every marble |
| All odd values | `Notbastian` | Sebastiàn receives none |
| Equal odd and even counts | `Notbastian` | Correct handling of ties |

## Edge Cases

Consider the tie scenario:

```
4
1 1 2 2
```

The algorithm counts two odd marbles and two even marbles. Since `even_count > odd_count` is false, it prints `"Notbastian"`. This exactly matches the special tie rule.

Consider a case where Sebastiàn receives every marble:

```
3
2 4 6
```

The scan produces `even_count = 3` and `odd_count = 0`. The comparison succeeds, so the output is:

```
Sebastian
```

Consider the opposite extreme:

```
3
1 3 5
```

The scan produces `even_count = 0` and `odd_count = 3`. The comparison fails, so the output is:

```
Notbastian
```

These cases cover the only subtle aspect of the problem, the distinction between a strict win and a tie. The counting approach handles all of them naturally.
