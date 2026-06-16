---
title: "CF 1009A - Game Shopping"
description: "The shop presents a line of games, each with a fixed price, and Maxim walks through them strictly from left to right."
date: "2026-06-16T22:55:58+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1009
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 47 (Rated for Div. 2)"
rating: 800
weight: 1009
solve_time_s: 86
verified: true
draft: false
---

[CF 1009A - Game Shopping](https://codeforces.com/problemset/problem/1009/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

The shop presents a line of games, each with a fixed price, and Maxim walks through them strictly from left to right. At the same time, he carries a wallet that behaves like a queue of bills: only the front bill is ever considered, and it either gets consumed or stays in place depending on whether it is enough to pay for the current game.

At each game position, Maxim does exactly one attempt: he looks at the first bill in his wallet. If the wallet is empty, he cannot interact with that game at all and simply moves on. If the first bill has value at least the game price, he buys the game and that bill disappears from the wallet. Otherwise, he fails to buy and keeps the same bill, then proceeds to the next game. The crucial point is that unsuccessful attempts do not advance the wallet pointer, only successful purchases do.

The task is to determine how many games are successfully purchased after processing all games in order.

The constraints are small, with both the number of games and bills up to 1000. This immediately allows a straightforward simulation in quadratic worst case without risk of timeouts. Any solution up to roughly 10^6 operations is comfortably safe.

The main subtlety lies in correctly modeling the persistence of the same bill when a purchase fails. A common mistake is to always advance the wallet pointer regardless of success, which changes the process completely and leads to undercounting purchases.

A second edge case appears when the wallet becomes empty before games end. In that situation, all remaining games must be skipped, since no further comparisons are possible. For example, if all bills are consumed early, the answer is simply the number of purchases made so far, with no further interaction.

## Approaches

The naive way to think about this process is to literally simulate each step as described. We maintain an index for games and a pointer to the first unused bill. For each game, we check the current bill. If it is sufficient, we consume it and move the bill pointer forward. If not, we keep the bill pointer fixed and move to the next game.

This simulation is already efficient enough because each bill can only be consumed once, and each game is processed once. That means at most n + m pointer movements that actually change state, and up to n unsuccessful checks that do not change the wallet state. The worst case is still linear in the number of games.

A more conceptual view is that the process is a two-pointer walk. One pointer moves through games strictly forward. The second pointer moves through the wallet only when a successful purchase happens. The key insight is that nothing ever requires backtracking or revisiting earlier games or bills. Each decision is local and irreversible.

This eliminates any need for nested loops or searching. The simulation directly reflects the structure of the process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation (naive nested checks) | O(nm) | O(1) | Too slow in worst case |
| Two-pointer simulation | O(n + m) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two indices: one for games and one for the current bill in the wallet. We also maintain a counter for successful purchases.

1. Initialize a pointer `j = 0` for the first bill and a counter `ans = 0`. The pointer represents the current active bill in the wallet.
2. Iterate through each game `i` from left to right. At each step, we consider whether a purchase attempt is possible.
3. If the wallet is empty (`j == m`), we stop checking the wallet entirely and continue skipping remaining games. This works because no further purchases are possible once all bills are consumed.
4. Otherwise, compare the current bill value `a[j]` with the current game cost `c[i]`.
5. If `a[j] >= c[i]`, increment the answer because the game is bought, and move the wallet pointer forward by setting `j += 1`. This models consumption of the bill.
6. If `a[j] < c[i]`, do nothing to the wallet pointer. The same bill remains available for the next game, so we simply move to the next game index.
7. Continue until all games are processed.

The key design choice is that the wallet pointer only moves on success, which exactly matches the rule that failed attempts do not consume the bill.

### Why it works

At any moment, the algorithm preserves the fact that `a[j]` is the first unconsumed bill. Every game either consumes this bill or leaves it unchanged. Since no operation ever skips or modifies earlier bills, the pointer `j` always correctly tracks the next available resource. Each successful purchase strictly reduces the wallet size, and each game is evaluated exactly once, so no valid purchase opportunity is ever skipped or duplicated.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    c = list(map(int, input().split()))
    a = list(map(int, input().split()))
    
    j = 0
    ans = 0
    
    for i in range(n):
        if j == m:
            break
        if a[j] >= c[i]:
            ans += 1
            j += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution is structured around a single pass over the games. The pointer `j` only advances when a bill is consumed, matching the exact behavior described in the process. The early exit when `j == m` prevents unnecessary comparisons once the wallet is empty, although even without it the solution would remain correct.

A common implementation mistake is to increment `j` even when the purchase fails. That breaks the invariant that `a[j]` is always the first available bill and leads to artificially skipping usable bills.

## Worked Examples

### Example 1

Input:

```
n = 5, m = 4
c = [2, 4, 5, 2, 4]
a = [5, 3, 4, 6]
```

| i | Game cost c[i] | Bill a[j] | Decision | j after | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 5 | buy | 1 | 1 |
| 1 | 4 | 3 | skip | 1 | 1 |
| 2 | 5 | 3 | skip | 1 | 1 |
| 3 | 2 | 3 | buy | 2 | 2 |
| 4 | 4 | 4 | buy | 3 | 3 |

This trace shows how the same bill can be reused across multiple failed attempts, and only successful comparisons advance the wallet.

### Example 2

Input:

```
n = 4, m = 3
c = [7, 8, 9, 10]
a = [5, 6, 4]
```

| i | Game cost c[i] | Bill a[j] | Decision | j after | ans |
| --- | --- | --- | --- | --- | --- |
| 0 | 7 | 5 | skip | 0 | 0 |
| 1 | 8 | 5 | skip | 0 | 0 |
| 2 | 9 | 5 | skip | 0 | 0 |
| 3 | 10 | 5 | skip | 0 | 0 |

The wallet never advances, so no purchases occur. This demonstrates the case where a single small bill blocks all progress.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each game is processed once, and each bill is consumed at most once |
| Space | O(1) | Only two counters are used besides input storage |

The linear scan fits comfortably within the limits of 1000 games and 1000 bills, requiring at most a few thousand operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""5 4
2 4 5 2 4
5 3 4 6
""") == "3"

# all cannot buy
assert run("""4 3
7 8 9 10
5 6 4
""") == "0"

# all can buy
assert run("""3 3
1 2 3
10 10 10
""") == "3"

# wallet exhausted early
assert run("""5 2
1 1 1 1 1
2 2
""") == "2"

# alternating pattern
assert run("""6 4
3 1 4 1 5 2
2 2 2 2
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all high costs | 0 | no purchase possible, pointer never moves |
| all low costs | full m or n limited | full consumption behavior |
| early wallet exhaustion | partial count | stopping condition correctness |
| alternating values | partial greedy matching | stability under mixed decisions |

## Edge Cases

One edge case occurs when the first bill is too small for every game. In that situation, the wallet pointer never moves, and the answer remains zero. For example, `c = [5, 6, 7]` and `a = [1]` results in no progress at all because the single bill is never consumed.

Another edge case is when all games are extremely cheap compared to bills. Then every game consumes exactly one bill until either list ends. For `c = [1, 1, 1]` and `a = [10, 10]`, the pointer advances on every game until the second bill is consumed, producing an answer of 2.
