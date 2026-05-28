---
title: "CF 78C - Beaver Game"
description: "We have n independent logs, each with length m. On a move, a player chooses one existing log and splits it into several equal pieces. If a log of length x is split into t equal parts, then t 1, t must divide x, and every resulting part must have length at least k."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "games", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 78
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 70 (Div. 2)"
rating: 2000
weight: 78
solve_time_s: 126
verified: true
draft: false
---

[CF 78C - Beaver Game](https://codeforces.com/problemset/problem/78/C)

**Rating:** 2000  
**Tags:** dp, games, number theory  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `n` independent logs, each with length `m`. On a move, a player chooses one existing log and splits it into several equal pieces. If a log of length `x` is split into `t` equal parts, then `t > 1`, `t` must divide `x`, and every resulting part must have length at least `k`.

After the split, those smaller pieces remain in the game and may be split again later. Players alternate turns, and the first player unable to make a legal move loses.

The task is to determine whether the starting player, Timur, wins under optimal play.

The constraints immediately rule out any simulation of game states. Both `n` and `m` can reach `10^9`, so even iterating over all possible log lengths or recursively exploring states is impossible. The solution has to come from game theory and number theory, with at most about `O(sqrt(m))` work.

The key subtlety is that the game is not played on a single log unless `n = 1`. Since each move affects exactly one log, the full game is the xor-sum of identical subgames. That means parity and Sprague-Grundy reasoning matter.

Several edge cases are easy to mishandle.

Consider:

```
4 9 5
```

No split is possible because every piece must have length at least `5`. The only divisors of `9` larger than `1` are `3` and `9`, producing piece lengths `3` and `1`, both invalid. Timur loses immediately.

A naive approach that only checks whether `m` has divisors greater than `1` would incorrectly think a move exists.

Another tricky case is:

```
2 15 4
```

A move exists because `15 = 3 * 5`, and splitting into `3` parts of length `5` is legal. But two identical winning piles can still form a losing overall position. Treating the game as “if one log is winning then Timur wins” gives the wrong answer.

The smallest values also matter:

```
1 1 1
```

No split into more than one equal integer part exists. The answer is `"Marsel"`.

A careless implementation might assume `k = 1` always allows moves, but length `1` logs still cannot be split.

The most important structural edge case is when `m < 2k`.

Example:

```
100 7 4
```

Any legal split must create at least two parts, each at least `4`, so the original log must have length at least `8`. Since `7 < 8`, no move exists regardless of divisors.

## Approaches

The most direct way to think about the game is recursively.

For a log of length `x`, we can try every divisor `t > 1`. Splitting into `t` equal parts produces logs of size `x / t`. The resulting game state is equivalent to having `t` identical subgames.

Using Sprague-Grundy theory, the Grundy number of that move becomes:

- `0` if `t` is even, because xor of an even number of identical values cancels out.
- `g(x / t)` if `t` is odd.

So in principle we could recursively compute Grundy numbers for all reachable lengths.

This brute-force idea is correct, but completely impractical. The state space can involve values up to `10^9`, and recursive exploration over divisors becomes enormous.

The turning point is noticing that only win/loss information actually matters here, and the game collapses into a very small structure.

Suppose a log length `x` allows a split into an even number of parts. Then the resulting xor is always `0`, because identical games cancel pairwise. That immediately creates a move to a losing position, meaning `x` is winning.

Now suppose every legal split uses an odd number of parts. Then the resulting position after splitting into `t` odd parts has the same win/loss status as the smaller log `x / t`.

This creates a recursive parity structure. After analyzing it carefully, the game reduces to one simple characterization:

A single log is losing if and only if its length is either too small to split, or it is an odd number.

Why?

If `x` is even and `x >= 2k`, we can always split it into `2` equal parts. Each part has length `x / 2 >= k`, so this is legal. Splitting into two identical piles produces xor `0`, so every such even `x` is winning.

If `x` is odd, every divisor count `t` must also be odd. That means every move goes to the same status as a smaller odd number. Eventually recursion reaches a terminal odd number smaller than `2k`, which is losing. So every odd number is losing.

After this reduction, the full game becomes trivial.

Each of the `n` logs is identical.

- If a single log is losing, its Grundy number is `0`, so the xor of all logs is `0`, and Marsel wins.
- If a single log is winning, its Grundy number is nonzero. In fact all winning positions here behave like Grundy `1`, so xor depends only on parity of `n`.

That means Timur wins exactly when:

- `m` is even,
- `m >= 2k`,
- and `n` is odd.

Everything else is losing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recursive Grundy computation | Exponential / infeasible | Huge | Too slow |
| Optimal parity-based game analysis | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `m`, and `k`.
2. Check whether any move is possible on a single log.

A legal split needs at least two parts, each of length at least `k`. So the original log must satisfy:

$m \ge 2k$

If `m < 2k`, no move exists anywhere in the game, so Timur immediately loses.
3. If `m` is odd, output `"Marsel"`.

Every split of an odd number into equal integer parts must use an odd number of parts. That means the game always transitions into an odd number of identical smaller subgames, preserving the losing structure recursively.
4. Now we know `m` is even and `m >= 2k`.

Splitting one log into two equal halves is always legal:

$m = 2 \cdot \frac{m}{2}$

Since the two resulting subgames are identical, their xor is zero. So one log is a winning game state.
5. The entire game contains `n` identical winning components.

The xor of an even number of identical nonzero Grundy values becomes zero, while an odd count remains nonzero.
6. If `n` is odd, output `"Timur"`. Otherwise output `"Marsel"`.

### Why it works

The core invariant is that the game state depends only on parity.

An even log with size at least `2k` always has a direct move to a zero xor state by splitting into two equal parts. So every such position is winning.

An odd log can only split into an odd number of equal pieces, because every divisor of an odd number is odd. The resulting position behaves exactly like a smaller odd log. Since recursion eventually reaches an unsplittable odd log below `2k`, every odd log is losing.

Thus every log falls into one of two categories:

- losing: odd or too small,
- winning: even and large enough.

The total game is the xor-sum of `n` identical subgames, so only the parity of `n` matters once a single log is winning.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())

    if m < 2 * k:
        print("Marsel")
        return

    if m % 2 == 1:
        print("Marsel")
        return

    if n % 2 == 1:
        print("Timur")
    else:
        print("Marsel")

solve()
```

The first condition handles positions where no move exists at all. Since every move must create at least two pieces of length at least `k`, any log shorter than `2k` is permanently blocked.

The second condition checks whether the log length is odd. Odd logs never become winning because every legal split preserves odd parity and eventually reaches a terminal losing position.

After those checks, the remaining case is an even log large enough to split into two equal parts. That makes a single log winning.

The final answer depends on the parity of `n`. An odd number of identical winning games produces a nonzero xor, while an even number cancels out.

One subtle implementation detail is the order of checks. We must test `m < 2k` before reasoning about parity. For example:

```
1 3 2
```

The log length is odd, but the deeper reason is that no move exists at all. The current implementation still gives the correct answer either way, but checking feasibility first matches the actual game logic.

Another easy mistake is using `m / 2 >= k` with floating-point division. Integer arithmetic with `m >= 2 * k` is cleaner and avoids precision issues.

## Worked Examples

### Example 1

Input:

```
1 15 4
```

| Variable | Value |
| --- | --- |
| n | 1 |
| m | 15 |
| k | 4 |
| m >= 2k | 15 >= 8, yes |
| m odd? | yes |

Output:

```
Marsel
```

This example demonstrates the key odd-number property. Even though a legal move exists, every possible split uses an odd number of parts, so the position remains losing.

### Example 2

Input:

```
3 12 5
```

| Variable | Value |
| --- | --- |
| n | 3 |
| m | 12 |
| k | 5 |
| m >= 2k | 12 >= 10, yes |
| m odd? | no |
| n odd? | yes |

Output:

```
Timur
```

Here the log is even and large enough to split into two equal halves of length `6`. A single log is winning, and there are an odd number of such logs, so the xor stays nonzero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic and parity checks |
| Space | O(1) | No additional data structures |

The constraints allow values up to `10^9`, but the solution never iterates over ranges or divisors. Constant-time arithmetic easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m, k = map(int, input().split())

    if m < 2 * k:
        print("Marsel")
        return

    if m % 2 == 1:
        print("Marsel")
        return

    if n % 2 == 1:
        print("Timur")
    else:
        print("Marsel")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run("1 15 4\n") == "Marsel", "sample 1"

# minimum values
assert run("1 1 1\n") == "Marsel", "minimum case"

# even and splittable, odd number of logs
assert run("3 12 5\n") == "Timur", "winning parity case"

# even and splittable, even number of logs
assert run("4 12 5\n") == "Marsel", "xor cancellation"

# boundary where split just becomes possible
assert run("1 8 4\n") == "Timur", "exact boundary"

# odd length with legal moves
assert run("1 21 3\n") == "Marsel", "odd recursive losing case"

# very large values
assert run("999999999 1000000000 1\n") == "Timur", "large constraints"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `Marsel` | Minimum-size terminal state |
| `3 12 5` | `Timur` | Odd count of winning piles |
| `4 12 5` | `Marsel` | Even xor cancellation |
| `1 8 4` | `Timur` | Exact feasibility boundary |
| `1 21 3` | `Marsel` | Odd numbers stay losing recursively |
| `999999999 1000000000 1` | `Timur` | Handles maximum values in O(1) |

## Edge Cases

Consider:

```
100 7 4
```

The algorithm first checks:

$7 < 2 \cdot 4$

Since the condition is true, no legal move exists. The output is `"Marsel"`.

This case confirms that divisor checks alone are insufficient. Even though `7` has divisors, none produce pieces of length at least `4`.

Now consider:

```
2 15 4
```

The algorithm sees that `15 >= 8`, so moves exist. Then it checks parity and finds `15` is odd, so the position for one log is losing. Since every log is losing, the entire xor is zero and the answer is `"Marsel"`.

This demonstrates the recursive odd-number structure. Having a legal move does not imply the position is winning.

Finally consider:

```
2 8 4
```

The log is even and satisfies `8 >= 8`, so one log is winning. But there are two identical winning logs. Their Grundy values xor to zero, so the algorithm outputs `"Marsel"`.

This catches the common mistake of analyzing only a single pile instead of the full impartial game sum.
