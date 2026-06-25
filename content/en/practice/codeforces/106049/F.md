---
title: "CF 106049F - RBS Game"
description: "This game builds a bracket sequence in blocks. Alice controls every odd turn, including the last one, and each of her turns adds exactly a brackets. Bob controls every even turn and adds exactly b brackets."
date: "2026-06-25T12:34:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106049
codeforces_index: "F"
codeforces_contest_name: "TheForces Round #44 (DIV3.5-Forces)"
rating: 0
weight: 106049
solve_time_s: 44
verified: true
draft: false
---

[CF 106049F - RBS Game](https://codeforces.com/problemset/problem/106049/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

This game builds a bracket sequence in blocks. Alice controls every odd turn, including the last one, and each of her turns adds exactly `a` brackets. Bob controls every even turn and adds exactly `b` brackets. After all turns, Alice wins only if the whole sequence is a regular bracket sequence, meaning every prefix has at least as many opening brackets as closing brackets and the final balance is zero.

The hacked version asks us only to decide which player Alice should choose to play as. We need to determine whether Alice has a strategy that guarantees a regular bracket sequence, or whether Bob can always prevent it. The constraints are small, but the intended solution is not simulation. A strategy must work against every possible move from the opponent, so checking possible bracket strings would be exponential. The number of possible strings in a single move is already large because a block of brackets can have many different arrangements.

The key difficulty is that a regular bracket sequence has two requirements at once. The final number of opening and closing brackets must match, and every prefix must remain valid. A construction that only fixes the final balance can still fail if an early prefix becomes negative.

There are two important cases that break naive solutions. Consider:

```
1
3 2 4
```

If Alice tries to play, she can start with at most two more opening brackets than closing brackets. Bob can answer with four closing brackets. Even if Alice starts with `((', Bob can append `))))`, making the prefix invalid. The output is:

```
0
```

A careless approach that only checks the total number of brackets might miss this because Alice still gets a final move.

Another case is:

```
1
3 4 2
```

Here Alice can start with four opening brackets, Bob cannot remove all of that safety margin in one move, and Alice can repair the balance on her last turn. The output is:

```
1
```

An approach that ignores the order of turns and only compares total counts could make the wrong decision.

## Approaches

The brute-force way is to imagine every possible choice of player and every possible bracket block they can place. For each complete game, we could check whether the resulting sequence is regular. This is correct because it directly follows the definition of the game, but it is completely impractical. A move of length 50 has an enormous number of possible bracket strings, and the game has up to 49 turns, so the number of possible games grows exponentially.

The useful observation comes from looking at the balance instead of the exact sequence. The balance is the number of opening brackets minus closing brackets. A regular sequence must never let this value become negative.

If Alice chooses to play, she can always start with only opening brackets. After this, she wants to keep enough positive balance so that Bob cannot make the sequence invalid. Since Alice moves after every Bob move and also makes the last move, she can restore the balance after Bob's attack whenever her block size is at least as large as Bob's block size.

Suppose `a >= b`. After each Bob move, Bob can decrease the current balance by at most `b`. Alice can then add `a` opening brackets or closing brackets in a way that restores a safe state. She can maintain the invariant that after every Alice move the balance is exactly `a`. The last Alice move can close everything and finish with balance zero.

If `a < b`, Alice cannot guarantee safety. No matter what she puts on the first move, Bob can choose a block of only closing brackets. Since Bob's block is larger, he can decrease the balance below zero immediately. Once a prefix becomes invalid, the final sequence cannot be regular.

The whole problem reduces to comparing the two block sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `a`, and `b` for each test case. The value of `n` does not affect the decision because the same comparison between Alice's and Bob's power holds for every odd number of rounds.
2. Compare `a` and `b`. If Alice's block size is at least Bob's block size, Alice can always maintain a safe positive balance, so output `1`.
3. If Bob's block size is larger, output `0` because Bob can force the prefix balance to become negative.

Why it works:

The invariant behind Alice's strategy is that after every Alice turn the sequence can be kept at a safe positive balance. Bob's strongest possible attack is to make every bracket in his block a closing bracket, which reduces the balance by exactly `b`. Alice's next block can compensate for this loss only if it has size at least `b`. When `a >= b`, Alice can always recover. When `a < b`, Bob can make the very first prefix after his move invalid, so Alice has no winning strategy.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []
    for _ in range(t):
        n, a, b = map(int, input().split())
        if a >= b:
            ans.append("1")
        else:
            ans.append("0")
    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The solution reads each test case and only uses the relationship between the two block lengths. The number of rounds is not needed because `n` is always odd, meaning Alice always has the final move.

The comparison uses `>=` rather than `>`. When `a` and `b` are equal, Alice can exactly restore the balance after Bob's move, so equality is a winning case.

There are no array indices or simulations involved, which avoids any off-by-one issues. The arithmetic values are small, but the same logic also works for larger integers.

## Worked Examples

For the first example:

Input:

```
1
3 2 4
```

The trace is:

| Step | a | b | Decision |
| --- | --- | --- | --- |
| Read values | 2 | 4 | Alice's move is smaller |
| Compare | 2 | 4 | Bob can break the prefix |
| Output |  |  | 0 |

This demonstrates the losing case. Bob's block is larger, so he can always create a negative prefix.

For the second example:

Input:

```
1
3 4 2
```

The trace is:

| Step | a | b | Decision |
| --- | --- | --- | --- |
| Read values | 4 | 2 | Alice's move is larger |
| Compare | 4 | 2 | Alice can restore balance |
| Output |  |  | 1 |

This demonstrates the winning case. Alice can maintain enough balance after every turn and finish with a valid bracket sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires one comparison. |
| Space | O(1) | Only the current values are stored. |

The solution fits easily within the limits because it avoids generating any bracket sequences and performs constant work per test case.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, a, b = map(int, input().split())
        out.append("1" if a >= b else "0")
    return "\n".join(out)

# samples
assert solution("""2
3 2 2
3 4 2
""") == """1
1""", "sample"

# minimum size
assert solution("""1
3 2 4
""") == "0", "minimum losing case"

# equal moves
assert solution("""1
49 50 50
""") == "1", "equal block sizes"

# large values
assert solution("""1
49 50 2
""") == "1", "alice much stronger"

# boundary where bob is slightly stronger
assert solution("""1
5 48 50
""") == "0", "bob stronger by two"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 2 4` | `0` | Bob can destroy the prefix balance |
| `49 50 50` | `1` | Equality is still winning |
| `49 50 2` | `1` | Alice can easily recover |
| `5 48 50` | `0` | Small difference still matters |

## Edge Cases

For the losing edge case:

```
1
3 2 4
```

Alice's first move can create at most balance `2` by placing only opening brackets. Bob can answer with four closing brackets, reducing the balance by four. The prefix becomes invalid immediately. Since a regular bracket sequence cannot contain a negative prefix balance, Alice cannot recover.

For the equal-size case:

```
1
3 4 4
```

Alice starts with four opening brackets. Bob can reduce the balance by four, but Alice's final move has the same size and can restore the sequence exactly. The invariant still holds because Alice never has less power than Bob.

For the strongest Alice case:

```
1
49 50 2
```

Every Bob move can remove only two units of balance while Alice can restore up to fifty brackets. Alice has enough control to keep the sequence valid throughout the whole game.
