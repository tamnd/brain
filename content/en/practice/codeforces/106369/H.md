---
title: "CF 106369H - The Duel of Smokin' Joe"
description: "The game starts with a permutation of the numbers from 1 to n. Two players repeatedly choose two positions that are not already correct and swap the values in those positions. A value that reaches its own position becomes locked and cannot participate in later swaps."
date: "2026-06-26T09:02:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106369
codeforces_index: "H"
codeforces_contest_name: "2023 UCF Local Programming Contest"
rating: 0
weight: 106369
solve_time_s: 50
verified: true
draft: false
---

[CF 106369H - The Duel of Smokin' Joe](https://codeforces.com/problemset/problem/106369/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The game starts with a permutation of the numbers from `1` to `n`. Two players repeatedly choose two positions that are not already correct and swap the values in those positions. A value that reaches its own position becomes locked and cannot participate in later swaps. The player who performs the swap that finally makes the whole permutation sorted wins. Smokin Joe moves first.

The input contains the size of the permutation and the current arrangement of values. The output asks which player has a winning strategy assuming both players choose moves that maximize their chance of winning.

The main constraint is that `n` can reach `10^6`. This immediately rules out simulations, dynamic programming over states, or any approach that tries to explore possible moves. The number of possible permutations is enormous, so the solution must extract a mathematical property of the starting permutation and compute it in linear time.

The tricky part is that players are allowed to make swaps that do not immediately improve the permutation. A solution that only counts the minimum number of swaps needed to sort is not enough. For example, the permutation

```
3
2 3 1
```

can be sorted in two swaps, so a careless approach might say the second player wins. However, the real reason is deeper: every valid game ending at the sorted permutation has the same parity of moves. The minimum number of swaps happens to match that parity here, but the proof must consider all possible choices.

Another edge case is a permutation made of several independent cycles. For example:

```
4
4 3 2 1
```

The correct output is:

```
Oh No!
```

The permutation is two swaps away from sorted in the usual sense. Since the total parity of the permutation is even, the number of moves needed to reach the sorted state must also be even, meaning the second player gets the final move.

A final common mistake is handling already correct positions incorrectly. Consider:

```
3
1 3 2
```

The first position is already fixed and cannot be touched. The remaining two positions form one swap, so the answer is:

```
Smokin Joe!
```

An implementation that counts all positions as available would not reflect the actual rules.

## Approaches

The direct approach is to model the duel itself. From the current permutation, we could generate every possible swap between movable positions, recursively solve every resulting state, and mark states where the current player can force a win. This is correct because it follows the exact game rules.

The problem is the number of states. A permutation of length `n` can have `n!` different arrangements, and even a single state can have many possible swaps. For `n = 10^6`, even checking all possible swaps once is already impossible.

The key observation comes from looking at permutation parity. Every swap changes the parity of a permutation. The sorted permutation is the identity permutation, which always has even parity. Therefore, if the initial permutation has odd parity, every path that reaches the sorted state must contain an odd number of moves. If it has even parity, every path must contain an even number of moves.

The locking rule does not change this argument. A locked element is simply a fixed point of the current permutation. Every legal move is still a transposition of two currently movable positions, so it still flips the parity. Since the game must end at the identity permutation, the parity of the number of moves is already determined before the first move.

If the number of moves must be odd, the first player makes the last move. If it must be even, the second player does.

The parity of a permutation can be found from its cycle decomposition. A cycle of length `k` contributes `k - 1` swaps to the parity, so the total parity is:

```
(n - number_of_cycles) mod 2
```

Finding the cycles takes linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n) | O(n!) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Traverse the permutation and count how many cycles it contains. Start from an unvisited position and repeatedly follow the value stored there until returning to a visited position. Marking every visited position once gives all cycles in linear time.
2. Compute `n - cycles`. Each cycle of length `k` requires `k - 1` transpositions to break into fixed points, so summing these values over all cycles gives the exponent of the permutation sign.
3. Check the parity of that value. An odd value means the starting permutation has odd parity, so every valid game has an odd number of swaps and Smokin Joe makes the final move.
4. If the value is even, every valid game has an even number of swaps and The Outlaw makes the final move.

Why it works:

The invariant is the parity of the permutation. A swap always changes this parity because every transposition reverses the sign of a permutation. The only terminal state is the sorted permutation, whose parity is even. Therefore the parity of the number of swaps made during any completed duel must exactly match the initial parity of the permutation. Since players only decide which valid sequence is played, not the parity of its length, the winner is determined entirely by the initial permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(int, input().split()))

    visited = [False] * n
    cycles = 0

    for i in range(n):
        if not visited[i]:
            cycles += 1
            cur = i
            while not visited[cur]:
                visited[cur] = True
                cur = p[cur] - 1

    if (n - cycles) & 1:
        print("Smokin Joe!")
    else:
        print("Oh No!")

if __name__ == "__main__":
    solve()
```

The array is stored using zero-based indices, so the value `p[cur]` is converted to `p[cur] - 1` when following a cycle. The cycle count is the only information needed, so there is no need to modify the permutation or simulate swaps.

The `visited` array prevents repeatedly walking through the same cycle. Each position is entered exactly once, which is why the traversal remains linear even for the maximum input size.

The final condition uses the parity of `n - cycles`. This quantity can be large, but Python integers handle it safely. Only the lowest bit matters, so checking with `& 1` avoids unnecessary work.

## Worked Examples

### Sample 1

Input:

```
3
1 3 2
```

The cycle decomposition is `(1)(2 3)`.

| Step | Current index | Action | Cycles counted |
| --- | --- | --- | --- |
| 1 | 1 | Single element cycle | 1 |
| 2 | 2 | Follow to position 3 | 2 |
| 3 | 3 | Already visited | 2 |

The calculation is:

```
n - cycles = 3 - 2 = 1
```

The value is odd, so the game contains an odd number of moves. Smokin Joe makes the final swap.

Output:

```
Smokin Joe!
```

### Sample 2

Input:

```
4
4 3 2 1
```

The cycle decomposition is `(1 4)(2 3)`.

| Step | Current index | Action | Cycles counted |
| --- | --- | --- | --- |
| 1 | 1 | Follow 1 -> 4 -> 1 | 1 |
| 2 | 2 | Follow 2 -> 3 -> 2 | 2 |
| 3 | 3 | Already visited | 2 |
| 4 | 4 | Already visited | 2 |

The calculation is:

```
n - cycles = 4 - 2 = 2
```

The value is even, so the second player makes the last move.

Output:

```
Oh No!
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every position is visited exactly once while finding cycles. |
| Space | O(n) | The visited array stores one boolean per position. |

The input size can reach one million elements, so a linear solution is required. The algorithm performs only a few operations per element and fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    p = list(map(int, sys.stdin.readline().split()))

    visited = [False] * n
    cycles = 0

    for i in range(n):
        if not visited[i]:
            cycles += 1
            cur = i
            while not visited[cur]:
                visited[cur] = True
                cur = p[cur] - 1

    ans = "Smokin Joe!\n" if (n - cycles) & 1 else "Oh No!\n"

    sys.stdin = old_stdin
    return ans

assert run("""3
1 3 2
""") == "Smokin Joe!\n", "sample 1"

assert run("""4
4 3 2 1
""") == "Oh No!\n", "sample 2"

assert run("""2
2 1
""") == "Smokin Joe!\n", "single swap"

assert run("""5
1 2 3 5 4
""") == "Smokin Joe!\n", "fixed positions"

assert run("""6
2 1 4 3 6 5
""") == "Oh No!\n", "three independent swaps"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 2 1` | `Smokin Joe!` | Smallest nontrivial cycle |
| `5 / 1 2 3 5 4` | `Smokin Joe!` | Already fixed positions |
| `6 / 2 1 4 3 6 5` | `Oh No!` | Multiple even cycles with even total parity |

## Edge Cases

For the input

```
3
1 3 2
```

the first position is already correct, so the only active cycle is the swap between positions two and three. The algorithm finds two cycles in total, computes `3 - 2 = 1`, and predicts an odd number of moves. The first player wins.

For the input

```
4
4 3 2 1
```

the permutation contains two separate cycles of length two. Each cycle contributes one to the swap parity, giving two total. The algorithm computes an even value, which means the final move belongs to the second player.

For an already almost sorted permutation with many fixed points, such as

```
5
1 2 3 5 4
```

the cycle traversal ignores the fixed positions naturally because each fixed position is simply a cycle of length one. Only the nontrivial swap affects the parity calculation, so the answer remains correct.
