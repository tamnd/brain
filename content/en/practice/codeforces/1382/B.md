---
problem: 1382B
contest_id: 1382
problem_index: B
name: "Sequential Nim"
contest_name: "Codeforces Round 658 (Div. 2)"
rating: 1100
tags: ["dp", "games"]
answer: passed_samples
verified: true
solve_time_s: 283
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e6ef5-142c-83ec-96d7-74def36b8cb3
---

# CF 1382B - Sequential Nim

**Rating:** 1100  
**Tags:** dp, games  
**Model:** gpt-5-3-mini  
**Solve time:** 4m 43s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e6ef5-142c-83ec-96d7-74def36b8cb3  

---

## Solution

## Problem Understanding

The game is played on a row of piles. On each move, only the leftmost pile that still contains stones matters, and the player may remove any positive number of stones from that pile. Once a pile becomes empty, play continues with the next pile in the same way. Players alternate turns, and the player who cannot move because all piles are empty loses.

Although this looks like multiple independent piles, the leftmost restriction turns it into a single evolving sequence where piles get exhausted one after another, and each exhaustion may or may not “flip” the strategic situation depending on how many moves were spent inside that pile.

The input consists of several independent games. For each game, we must decide whether the first player has a forced win under optimal play.

The constraints allow up to one hundred thousand total piles across all test cases. This immediately rules out any simulation that processes each stone or even each move individually. Any solution must scan each test case in linear time, since quadratic or per-move reasoning would exceed limits by several orders of magnitude.

A subtle edge case arises when all piles contain exactly one stone. In that situation, every move completely empties a pile, so the game reduces to a simple alternation across piles. For example, for `[1, 1, 1]`, the first player wins, while for `[1, 1, 1, 1]`, the second player wins. A naive intuition might incorrectly focus on total parity of stones, but that is not what governs the game.

Another important edge case appears when a pile greater than one exists early in the sequence. For instance, in `[2, 5, 4]`, the first player wins immediately by controlling how the first pile is reduced. However, if that first larger pile appears later, such as `[1, 1, 2, ...]`, the parity shifts depending on its position rather than its value alone.

These two behaviors, “all ones” versus “first non-one pile,” are the only structural cases that matter.

## Approaches

A brute-force approach would simulate the game move by move. We would maintain the current pile index and repeatedly subtract from it, alternating players until all piles are empty. In the worst case, a pile can contain up to one billion stones, meaning a single test case could require up to $10^9$ operations, which is far beyond feasible limits. Even if we only simulate pile transitions, we still risk linear work per pile per move, which is unnecessary.

The key observation is that within a pile, the exact number of stones does not matter beyond whether it is equal to one or greater than one. If a pile has size exactly one, it is forced: whoever plays on it removes it and immediately passes control to the next pile. If a pile has size greater than one, the first time a player reaches it, that player can control how many internal moves occur before it becomes size one, effectively deciding whether the “turn parity” flips at that boundary or not.

This reduces the entire game to locating the first pile that is not equal to one. If all piles are one, the outcome depends only on how many such forced moves exist. Otherwise, the position of the first non-one pile determines whether the first player can maintain control or loses it.

We therefore reduce the problem to a single linear scan per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(total stones) | O(1) | Too slow |
| Linear Scan Reduction | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan piles from left to right while checking whether each pile has exactly one stone. This identifies whether we are still in a forced-move segment where no decision exists.
2. Stop at the first pile whose size is greater than one. This position is critical because it is the first point where a player gains control over how long the game stays in a single pile.
3. If such a pile exists at index i, determine the winner based on whether i is odd or even. If i is odd, the first player wins because they reach the first controllable pile in a favorable turn parity. If i is even, the second player inherits that advantage.
4. If no such pile exists, meaning every pile has exactly one stone, compute the winner based on n. If n is odd, the first player wins because they make the final move. If n is even, the second player makes the last move and wins.

The reason parity alone is sufficient is that every pile of size one consumes exactly one move and flips the player. Only the first pile with size greater than one can break this forced alternation by introducing a controllable segment, and its position determines whether the parity advantage remains with the first player or shifts.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        idx = -1
        for i, v in enumerate(a):
            if v > 1:
                idx = i
                break
        
        if idx == -1:
            out.append("First" if n % 2 == 1 else "Second")
        else:
            out.append("First" if idx % 2 == 0 else "Second")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads each test case and performs a single pass over the array. The loop searches for the first pile that is not equal to one, storing its index. If none exists, the decision depends only on whether the number of piles is odd. Otherwise, the index parity determines the winner.

The key implementation detail is zero-based indexing. The reasoning uses 1-based positions conceptually, so the code directly applies even or odd checks on the zero-based index without adjustment.

## Worked Examples

### Example 1

Input:

`[2, 5, 4]`

| Step | Index | Value | First non-1 found | Decision |
| --- | --- | --- | --- | --- |
| 1 | 0 | 2 | yes | stop |

The first pile already contains more than one stone, so the first player immediately controls the critical decision point. Since this occurs at index 0, the first player wins.

This demonstrates that an early large pile guarantees immediate strategic control.

### Example 2

Input:

`[1, 2, 3, 4, 5, 6]`

| Step | Index | Value | First non-1 found | Decision |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | no | continue |
| 2 | 1 | 2 | yes | stop |

The first non-trivial pile appears at index 1. That means the second player reaches the first meaningful decision point, shifting control away from the first player. The result is a win for the second player.

This shows how a single leading block of ones delays control transfer and flips the outcome.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each pile is inspected once until the first non-one is found |
| Space | O(1) | Only a few variables are stored regardless of input size |

The total work across all test cases is linear in the total number of piles, which fits comfortably within the constraints of $10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        idx = -1
        for i, v in enumerate(a):
            if v > 1:
                idx = i
                break
        if idx == -1:
            res.append("First" if n % 2 == 1 else "Second")
        else:
            res.append("First" if idx % 2 == 0 else "Second")
    return "\n".join(res)

# provided samples
assert run("""7
3
2 5 4
8
1 1 1 1 1 1 1 1
6
1 2 3 4 5 6
6
1 1 2 1 2 2
1
1000000000
5
1 2 2 1 1
3
1 1 1
""") == """First
Second
Second
First
First
Second
First"""

# all ones edge case
assert run("""1
4
1 1 1 1
""") == "Second"

# single pile large
assert run("""1
1
1000000000
""") == "First"

# first element large
assert run("""1
3
5 1 1
""") == "First"

# delayed large pile
assert run("""1
5
1 1 1 2 1
""") == "Second"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | Second | parity rule when no branching exists |
| single large pile | First | minimal case |
| leading large pile | First | immediate control |
| delayed non-one pile | Second | index parity effect |

## Edge Cases

When all piles contain exactly one stone, the game becomes a strict alternation of moves across piles. For input `[1, 1, 1, 1]`, the algorithm detects no pile greater than one, so it falls back to checking parity of 4 and correctly returns Second. The sequence of forced moves ensures the second player makes the final move.

When the first pile itself is greater than one, such as `[7, 1, 1]`, the scan stops at index 0. Since index 0 is even, the algorithm returns First. In this case, the first player never loses control of parity because no forced single-stone chain precedes the decision point.

When a non-one pile appears later, such as `[1, 1, 1, 5, 1]`, the scan stops at index 3. The algorithm returns First because 3 is odd in zero-based indexing, meaning the second player reaches the first controllable pile and parity shifts against them.