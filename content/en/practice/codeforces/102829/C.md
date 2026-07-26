---
title: "CF 102829C - Kevin's Meme Reacts"
description: "Kevin starts a meme reaction chain with one reaction on his post. Every night the current number of reactions doubles automatically. During mornings, Kevin can manually add one reaction, and that new reaction is counted immediately."
date: "2026-07-26T15:28:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102829
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 11-06-20 Div. 1 (Tryout)"
rating: 0
weight: 102829
solve_time_s: 32
verified: true
draft: false
---

[CF 102829C - Kevin's Meme Reacts](https://codeforces.com/problemset/problem/102829/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 32s  
**Verified:** yes  

## Solution
## Problem Understanding

Kevin starts a meme reaction chain with one reaction on his post. Every night the current number of reactions doubles automatically. During mornings, Kevin can manually add one reaction, and that new reaction is counted immediately. The goal is to reach exactly `n` total reactions while minimizing how many manual reactions Kevin makes, counting the first reaction that starts the chain. The problem asks for that minimum number of manual additions.

The key way to view the process is to look at the value contributed by each manual reaction. If Kevin adds a reaction and it survives through `k` nights of doubling, it contributes exactly `2^k` reactions to the final total. The initial reaction is simply one such contribution with `k = 0`.

The input contains a single integer `n`, representing the desired final number of reactions. The output is the minimum number of individual reactions Kevin must manually add to make that exact total possible.

The constraint `n <= 10^9` means we cannot simulate every possible sequence of mornings and nights. A search over all ways to place reactions would grow exponentially because every possible manual reaction can happen at a different time. We need a solution that performs only a small number of operations, ideally logarithmic in `n`, because `10^9` has only about 30 binary digits.

The main edge cases come from values that look like they require multiple steps but actually do not. For example, when the input is:

```
8
```

the correct output is:

```
1
```

A careless simulation might add extra reactions, but one initial reaction doubles three times to become `8`.

Another tricky case is when the answer is not the number of days needed. For example:

```
5
```

The correct output is:

```
2
```

The chain can reach `4` using one reaction and then Kevin adds one more reaction to get `5`. Counting the number of doublings would give the wrong quantity because the problem asks for manual reactions, not elapsed days.

A final boundary case is:

```
1
```

The correct output is:

```
1
```

The first reaction is mandatory because it is the starting point of the process. An implementation that treats the first reaction as free would incorrectly return zero.

## Approaches

The direct approach is to try different schedules of manual reactions. We could imagine deciding on each morning whether Kevin reacts or waits, then simulating the nightly doubling until the target is reached. This works for small values because every possible schedule can eventually be checked, but the number of schedules grows too quickly. For a target near `10^9`, exploring all choices would require far more than the available time.

The useful observation comes from ignoring the timeline and focusing only on the contribution of each manual reaction. Every manual reaction becomes a power of two in the final count. If Kevin reacts at the beginning, that reaction contributes `1`, `2`, `4`, `8`, and so on depending on how many nights pass. A later reaction contributes a smaller power of two.

This means the final number `n` must be built as a sum of powers of two. The minimum number of powers of two needed to form a number is exactly the number of `1` bits in its binary representation. Each set bit represents one power of two that must be contributed by a separate manual reaction.

For example, `13` in binary is `1101`, which means:

`13 = 8 + 4 + 1`

Those three powers of two correspond to three manual reactions. No arrangement can use fewer because each manual reaction contributes only one power-of-two component.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of possible reaction timings | O(1) | Too slow |
| Optimal | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the target number of reactions `n`.
2. Count how many bits equal `1` in the binary representation of `n`. Each such bit represents one power of two that must come from one manual reaction.
3. Output this count as the minimum number of reactions Kevin must make.

Why it works: every reaction Kevin manually adds contributes one power of two to the final total because the only future operation is doubling. The binary representation of `n` is its unique decomposition into powers of two. Since every set bit requires one contribution and the decomposition cannot be shortened, counting set bits gives the minimum number of manual reactions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    print(n.bit_count())

if __name__ == "__main__":
    solve()
```

The solution reads the target number and uses Python's built-in `bit_count()` operation to count the number of set bits in its binary representation. This directly matches the mathematical observation from the algorithm.

There are no simulation loops, so there are no timing calculations or boundary transitions to get wrong. The only important detail is that `n = 1` must produce `1`, which is handled naturally because the binary representation contains one set bit.

## Worked Examples

For the first example:

```
Input:
5
```

The binary representation is `101`.

| n | Binary form | Set bits counted | Answer |
| --- | --- | --- | --- |
| 5 | 101 | 2 | 2 |

The two set bits represent the contributions `4` and `1`. Kevin can let the first reaction double twice to reach `4`, then add one reaction manually.

For the second example:

```
Input:
8
```

The binary representation is `1000`.

| n | Binary form | Set bits counted | Answer |
| --- | --- | --- | --- |
| 8 | 1000 | 1 | 1 |

There is only one power of two in the decomposition. Kevin only needs the starting reaction and can wait for three doublings.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | The number of processed bits is proportional to the binary length of `n`. |
| Space | O(1) | Only the input value and the answer are stored. |

The largest possible value has only about 30 binary digits, so the algorithm easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# provided samples
assert run("5\n") == "2\n", "sample 1"
assert run("8\n") == "1\n", "sample 2"

# custom cases
assert run("1\n") == "1\n", "minimum value"
assert run("15\n") == "4\n", "all bits set"
assert run("1024\n") == "1\n", "single high bit"
assert run("1000000000\n") == "13\n", "large boundary value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | The initial reaction is counted. |
| `15` | `4` | Numbers with many set bits require multiple reactions. |
| `1024` | `1` | Pure powers of two need only one reaction. |
| `1000000000` | `13` | Large values are handled without simulation. |

## Edge Cases

For `n = 8`, the algorithm converts the number to binary form `1000` and counts one set bit. The result is `1`, matching the fact that the initial reaction alone can grow through doubling to reach the target.

For `n = 5`, the binary form is `101`, so there are two set bits. The algorithm identifies the required contributions as `4` and `1`, giving the correct answer `2`. A method based only on counting doubling steps would fail here because the final adjustment requires an additional manual reaction.

For `n = 1`, the binary form is `1`, so the answer is `1`. The algorithm keeps the starting reaction in the count, avoiding the common mistake of treating the initial reaction as free.
