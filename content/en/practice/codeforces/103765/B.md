---
title: "CF 103765B - \u5b57\u7b26\u4e32"
description: "We are given a game played on a single string of lowercase letters. Two players alternate turns, starting with the first player."
date: "2026-07-02T08:54:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103765
codeforces_index: "B"
codeforces_contest_name: "2022 Collegiate Programming Contest of Xiangtan University"
rating: 0
weight: 103765
solve_time_s: 47
verified: true
draft: false
---

[CF 103765B - \u5b57\u7b26\u4e32](https://codeforces.com/problemset/problem/103765/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a game played on a single string of lowercase letters. Two players alternate turns, starting with the first player. A move consists of picking any adjacent pair of identical characters in the current string and deleting both of them, then stitching the remaining parts together. If a player cannot find such a pair on their turn, that player loses immediately.

The task is to determine, for each given starting string, whether the first player has a winning strategy assuming both players play optimally.

The constraints are tight enough that the total length across all test cases can reach one million. That rules out any approach that repeatedly simulates moves on the string in a naive way with linear scans per move, since in the worst case each deletion reduces the string by two characters and there can be O(n) such moves, leading to O(n²) behavior overall.

A subtle point is that the game is not about arbitrary deletions but only about removing adjacent equal pairs. This makes the structure highly local, but not independent across positions because deletions can create new adjacent pairs that were not originally present.

Edge cases that matter include strings with no adjacent equal pairs at all, strings where all characters are identical, and strings where deletions cascade. For example, in `"abccba"`, removing the middle `"cc"` creates a new opportunity structure, but not necessarily a win for the first player because parity of available moves matters more than local greed.

Another important corner case is when multiple disjoint pairs exist. A naive intuition might suggest each pair is an independent move, but that is incorrect because removing one pair can destroy or create other pairs.

## Approaches

The brute-force interpretation is straightforward: simulate the game state. For every possible move, remove one adjacent equal pair, recursively evaluate the resulting string, and decide if the current player can force a win. This is a classic game DP on strings.

However, the number of distinct states grows explosively. Even if we memoize by string configuration, each deletion changes adjacency globally, and the number of reachable states is exponential in the worst case. For a string like `"aaaaa...."`, every move reduces length but creates new adjacency configurations, still yielding a huge branching structure. This immediately exceeds any feasible complexity bound.

The key observation is that every move removes exactly two characters and never changes the relative order of remaining characters. More importantly, each move reduces the length by two, so the game always proceeds in a strictly decreasing sequence of even steps. This means the entire game is actually determined by how many moves are possible, not by which moves are chosen.

If we think in terms of a stack process, every deletion corresponds to popping a pair of identical adjacent characters. The process of repeatedly removing adjacent equal pairs is deterministic if we process greedily from left to right using a stack: whenever the current character equals the top of the stack, we remove the top instead of pushing.

This greedy reduction computes the final reduced string and implicitly counts how many deletions occur. Each deletion is a move in the game. Since each move reduces length by exactly 2, the total number of moves is fixed regardless of order. This collapses the game into a parity problem: if the number of possible deletions is odd, the first player wins, otherwise the second player wins.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force game DP | Exponential | Exponential | Too slow |
| Stack reduction + parity | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Initialize an empty stack that represents the current reduced form of the string. This stack models the invariant that no two adjacent characters in it are equal.
2. Scan the string from left to right character by character. For each character, compare it with the top of the stack if the stack is not empty.
3. If the stack is not empty and the top element equals the current character, pop the stack instead of pushing. This represents performing a deletion of an adjacent equal pair. The reason this is correct is that any adjacent equal pair must eventually be removed, and delaying its removal does not affect the total count of removals.
4. Otherwise, push the current character onto the stack, extending the current reduced structure.
5. Maintain a counter of how many deletions were performed. Each pop corresponding to a matching pair increases this counter by one.
6. After processing the entire string, check the parity of the deletion count. If it is odd, output "Yes" since the first player makes the last valid move. If it is even, output "No".

### Why it works

The key invariant is that after processing each prefix of the string with the stack rule, the stack represents the fully reduced form of that prefix under all possible optimal play sequences, and the number of removals performed is fixed regardless of the order of valid moves. This follows from the fact that removals only eliminate adjacent equal pairs and never create ambiguity in total count: every valid game sequence corresponds to removing disjoint pairs in some order, but the total number of removable pairs is invariant under reordering because each removal strictly reduces length by two and does not affect the parity of remaining structure in a way that changes total count.

Thus, the game reduces to counting how many such cancellations occur in the stack process and deciding the winner by parity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    out = []
    
    for _ in range(T):
        s = input().strip()
        stack = []
        moves = 0
        
        for ch in s:
            if stack and stack[-1] == ch:
                stack.pop()
                moves += 1
            else:
                stack.append(ch)
        
        if moves % 2 == 1:
            out.append("Yes")
        else:
            out.append("No")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution uses a stack to simulate cancellation of adjacent equal characters. Each cancellation corresponds exactly to one valid move in the game, so the variable `moves` tracks the total number of moves available under optimal play.

The critical detail is that we never need to reconsider earlier decisions. Once a pair is removed, it cannot affect future removals except by exposing new adjacency, and the stack naturally handles that.

The final decision is based purely on parity, which is why no further game-theoretic reasoning is needed.

## Worked Examples

### Example 1: `"funny"`

We simulate the stack.

| Step | Character | Stack | Moves |
| --- | --- | --- | --- |
| 1 | f | f | 0 |
| 2 | u | f u | 0 |
| 3 | n | f u n | 0 |
| 4 | n | f u | 1 |
| 5 | y | f u y | 1 |

Final moves = 1, which is odd, so output is `"Yes"`.

This shows a simple single cancellation, confirming that the algorithm counts only actual deletions, not potential ones.

### Example 2: `"abccba"`

| Step | Character | Stack | Moves |
| --- | --- | --- | --- |
| 1 | a | a | 0 |
| 2 | b | a b | 0 |
| 3 | c | a b c | 0 |
| 4 | c | a b | 1 |
| 5 | b | a | 2 |
| 6 | a | empty | 3 |

Final moves = 3, odd, so answer is `"Yes"`.

This demonstrates cascading deletions where removing a central pair exposes new adjacent pairs. The stack naturally captures this chain reaction without explicit backtracking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each character is pushed and popped at most once |
| Space | O(n) | Stack stores remaining unmatched characters |

Given that the total input size across all test cases is at most 10^6, this linear solution easily fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(sys.stdin.readline())
    res = []
    for _ in range(T):
        s = sys.stdin.readline().strip()
        stack = []
        moves = 0
        for ch in s:
            if stack and stack[-1] == ch:
                stack.pop()
                moves += 1
            else:
                stack.append(ch)
        res.append("Yes" if moves % 2 == 1 else "No")
    return "\n".join(res)

# provided samples
assert run("3\nxtu\nfunny\nabcdcba\n") == "No\nYes\nNo"
assert run("1\nabccba\n") == "Yes"

# custom cases
assert run("1\na") == "No", "single char"
assert run("1\naa") == "Yes", "single move"
assert run("1\naabb") == "No", "two independent deletions"
assert run("1\naaa") == "Yes", "chain reaction collapse"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"a"` | `No` | no moves possible |
| `"aa"` | `Yes` | single forced move |
| `"aabb"` | `No` | even number of deletions |
| `"aaa"` | `Yes` | cascading cancellations |

## Edge Cases

For a single character like `"a"`, the stack never performs a pop, so `moves = 0` and the output is `"No"`. The algorithm correctly identifies that no valid move exists.

For `"aaaa"`, the process is sequential: first two characters cancel, then the remaining two cancel, producing two moves total. The stack records exactly two pops, so parity is even and the result is `"No"`.

For alternating strings like `"ababab"`, no adjacent equal pairs ever form, so the stack only grows and never pops. The move count stays zero, correctly producing `"No"` since no legal move exists at any stage.
