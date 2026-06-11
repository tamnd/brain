---
title: "CF 1398B - Substring Removal Game"
description: "The game operates on a binary string that can be thought of as a sequence of adjacent blocks of identical characters. On each turn, a player removes a contiguous segment consisting of equal characters, and the two remaining parts of the string are stitched together."
date: "2026-06-11T09:07:30+07:00"
tags: ["codeforces", "competitive-programming", "games", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1398
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 93 (Rated for Div. 2)"
rating: 800
weight: 1398
solve_time_s: 78
verified: true
draft: false
---

[CF 1398B - Substring Removal Game](https://codeforces.com/problemset/problem/1398/B)

**Rating:** 800  
**Tags:** games, greedy, sortings  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The game operates on a binary string that can be thought of as a sequence of adjacent blocks of identical characters. On each turn, a player removes a contiguous segment consisting of equal characters, and the two remaining parts of the string are stitched together. The score is not about how many moves a player makes, but specifically how many `1` characters they personally delete over the entire process.

The key subtlety is that a move is not restricted to removing a single character. A player can remove an entire run of identical characters in one action, which means the game is fundamentally about choosing which blocks to eliminate and in what order, while the structure of the remaining runs keeps changing as blocks merge.

The input size is small per test case, with strings of length at most 100 and up to 500 test cases. This immediately rules out any exponential simulation of game states. Even a cubic or quadratic simulation over all substrings would be acceptable per test case, but anything that explores full game trees is unnecessary overkill.

A naive mistake arises from treating this as “count the ones Alice can grab in alternating blocks”. That fails because removals can merge separated parts of the string, creating new adjacency and new opportunities.

For example, consider `101`. If Alice greedily removes the first `1`, the string becomes `01`, but if she instead removes the middle `0`, the string becomes `11`, dramatically changing future scoring opportunities. A strategy that ignores structural changes will miscompute even on such tiny inputs.

Another failure case is alternating strings like `101010`. The best play depends on grouping effects after removals, and naive greedy removal of visible blocks does not preserve optimal structure.

## Approaches

The brute-force perspective is to simulate the entire game as a minimax search. Each state is a string, and each move chooses a run of identical characters to delete. The number of possible moves from a state is proportional to the number of runs, and after each move the string changes, producing a new state. This quickly becomes a full game tree.

Even though the string length is at most 100, the branching factor is roughly O(n) per move and the depth is also O(n), leading to an astronomically large number of states. Memoization helps in principle, but the number of distinct states is still exponential because deletions can reorder adjacency and merge runs in many ways.

The key observation is that the identity of individual characters does not matter as much as the structure of consecutive runs. Once we compress the string into blocks, the game becomes about how many `1`-blocks exist and how they interact with surrounding `0`-blocks. Each move always removes an entire block, and the only thing that matters is whether Alice or Bob gets to take a `1`-block before it becomes inaccessible or merged in a less favorable configuration.

A simpler and deeper view is that all `1` blocks are eventually deleted by someone, and players alternate taking whole blocks. Since each move removes exactly one contiguous block, the game reduces to selecting blocks in decreasing order of their positions after compression effects settle, and the optimal play aligns with processing block lengths in sorted order.

Once the string is compressed into runs, the process effectively becomes a turn-based selection of segment weights, where each `1`-run contributes its length to the player who gets it, and both players alternate picking from the largest available contributions in a greedy manner.

This reduces the problem from dynamic string manipulation to a static multiset game over run lengths.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (game tree) | Exponential | Exponential | Too slow |
| Run compression + greedy selection | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. First compress the string into maximal consecutive segments. Each segment is recorded as a pair consisting of its character and its length. This is necessary because every move deletes an entire contiguous equal block, so the natural atomic unit of the game is a run, not a character.
2. Extract only the lengths of segments that contain `1`. These represent all possible sources of Alice’s score, since only deletions of `1` contribute to her score.
3. Sort these `1`-segment lengths in descending order. The reason is that both players are effectively competing to take large scoring blocks early, since delaying a large block only allows the opponent to take it in an equally or more favorable position.
4. Simulate alternating turns over this sorted list. Alice takes the first, third, fifth, and so on largest available `1`-segments, while Bob takes the second, fourth, etc.
5. Sum the values taken by Alice to produce the final answer.

The crucial reasoning step is that once the string is reduced to independent blocks, the interaction between distant blocks no longer changes their contribution sizes. The game’s complexity collapses into a simple competitive allocation problem over independent weights.

### Why it works

Every move deletes exactly one maximal contiguous block. After full compression, the only meaningful decisions are which blocks are removed earlier. Since merging never increases the total number of `1`s in a block, each `1`-segment preserves its weight until removed. The alternating turn order fixes ownership of these weights in descending order, and no rearrangement of moves can improve Alice’s access to a smaller block without giving Bob access to an equal or larger one earlier. This locks the optimal strategy into greedy selection over sorted segment weights.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        s = input().strip()
        
        ones = []
        
        i = 0
        n = len(s)
        
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1
            
            if s[i] == '1':
                ones.append(j - i)
            
            i = j
        
        ones.sort(reverse=True)
        
        ans = 0
        for k in range(0, len(ones), 2):
            ans += ones[k]
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation starts by scanning the string and building run lengths. The inner loop identifies maximal contiguous segments, ensuring each block is treated atomically. Only segments of ones are stored because zero segments do not contribute to Alice’s score.

Sorting these segment lengths in descending order aligns with the greedy allocation strategy derived earlier. The loop that sums every second element starting from index zero corresponds directly to Alice taking the first, third, and subsequent best available blocks.

A common implementation pitfall is forgetting to compress runs and instead counting individual characters, which breaks the assumption that moves operate on whole blocks.

## Worked Examples

Consider the input `01111001`. The compression step produces segments `0 | 1111 | 00 | 1`. The `1`-segments have lengths `[4, 1]`.

| Step | Ones segments | Sorted | Alice picks | Running total |
| --- | --- | --- | --- | --- |
| Start | [4, 1] | [4, 1] | 4 | 4 |
| Next | [4, 1] | [4, 1] | 1 (Bob takes 1) | 4 |

Alice’s score becomes 4.

Now consider `101010`. Compression gives `1 | 0 | 1 | 0 | 1 | 0`, so ones segments are `[1, 1, 1]`.

| Step | Ones segments | Sorted | Alice picks | Running total |
| --- | --- | --- | --- | --- |
| Start | [1, 1, 1] | [1, 1, 1] | 1 | 1 |
| Next | [1, 1, 1] | [1, 1, 1] | 1 | 2 |
| Next | [1, 1, 1] | [1, 1, 1] | 1 | 3 |

This shows that in fully alternating structures, Alice still collects half-rounded up of total available `1`-block weight, consistent with greedy alternation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Compression is linear, sorting dominates |
| Space | O(n) | Stores run lengths of segments |

The string length is at most 100, so even the sorting step is negligible. With up to 500 test cases, this remains comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        s = input().strip()
        ones = []
        i = 0
        n = len(s)
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1
            if s[i] == '1':
                ones.append(j - i)
            i = j
        ones.sort(reverse=True)
        ans = sum(ones[k] for k in range(0, len(ones), 2))
        out.append(str(ans))
    return "\n".join(out)

assert run("5\n01111001\n0000\n111111\n101010101\n011011110111\n") == "4\n0\n6\n3\n6"
assert run("1\n0\n") == "0"
assert run("1\n1\n") == "1"
assert run("1\n101\n") == "1"
assert run("1\n110011\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `0` | no ones |
| `1` | `1` | single block |
| `101` | `1` | separated ones |
| `110011` | `2` | multiple blocks with zeros |

## Edge Cases

A fully zero string like `0000` produces no `1` segments, so the algorithm correctly returns zero because the list of scored blocks is empty and Alice never gains points.

A fully one string like `111111` compresses into a single segment of length six. Alice takes it immediately on her first move, and since there are no other segments, she receives the entire value without interference.

Alternating structures such as `1010101` produce multiple unit segments. Sorting preserves their independence, and alternating selection ensures Alice consistently captures every other segment without needing to simulate structural changes in the string.
