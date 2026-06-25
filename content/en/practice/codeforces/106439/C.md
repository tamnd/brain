---
title: "CF 106439C - Crushing the Array"
description: "The game is played on an array of integers. A valid move removes one entire block of equal values. A block means a maximal consecutive group where every element is the same, so the player cannot remove a part of a block."
date: "2026-06-25T09:29:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106439
codeforces_index: "C"
codeforces_contest_name: "Insomnia-26"
rating: 0
weight: 106439
solve_time_s: 29
verified: true
draft: false
---

[CF 106439C - Crushing the Array](https://codeforces.com/problemset/problem/106439/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 29s  
**Verified:** yes  

## Solution
## Problem Understanding

The game is played on an array of integers. A valid move removes one entire block of equal values. A block means a maximal consecutive group where every element is the same, so the player cannot remove a part of a block. Alice moves first, but before the game begins she can reorder the array however she wants. The task is to determine whether Alice can arrange the values so that she has a winning strategy against Bob.

The input describes several arrays. For each array, the output is the winner under optimal play after Alice chooses the best possible ordering. We only need to print whether Alice or Bob wins.

The important observation is that Alice controls the initial arrangement, so the original positions do not matter. Only the multiset of values matters. Once values are grouped, each distinct value contributes exactly one removable block, because Alice can place equal values together. The game then becomes a question about how many blocks exist and how the players interact with removing them.

The constraints are large enough that simulating the game is not realistic. With the total number of elements reaching around 200000, any approach that tries every permutation, every grouping, or every sequence of moves would explode. A solution must process the array in linear time or close to it.

The main edge cases come from values with the same frequency. A careless solution may count distinct values and assume that the number of moves is always that count, but the parity of block sizes changes the outcome.

For example, consider:

```
1
3
5 5 5
```

Alice can arrange it as `[5,5,5]`. There is only one block, so Alice removes it and wins. The output is:

```
Alice
```

A solution that treats every occurrence as an independent move would incorrectly think there are three moves.

Another case:

```
1
4
1 1 2 2
```

Alice can arrange the array as `[1,1,2,2]`. There are two blocks, and Alice removes one block first. Bob removes the remaining block, so Alice loses. The output is:

```
Bob
```

A common mistake is to think Alice always benefits from grouping equal values, but grouping only determines the number of blocks. The players still alternate removing those blocks.

## Approaches

The first idea is to simulate the game directly. Since Alice can reorder the array, we could try different arrangements and play the game on each one. This is clearly impossible because the number of possible permutations grows extremely fast.

A better brute-force idea is to notice that only the lengths of equal-value groups matter. We could enumerate possible ways to split the frequencies into consecutive blocks and compute the winner. This also fails because a frequency can be split into many possibilities, and the total number of partitions is too large.

The key observation is that Alice can always put every occurrence of the same value next to each other. Splitting a value into several groups is never useful because it gives Bob extra moves. For a value appearing `cnt` times, the best arrangement gives one block containing all `cnt` copies.

Now the game is reduced to a collection of blocks. Each distinct number creates one block. The players simply take turns deleting blocks. Since every move removes exactly one block, the player who makes the last move wins.

That means the only thing that matters is the number of distinct values after optimal grouping. If there are an odd number of blocks, Alice makes the last move. If there are an even number of blocks, Bob does.

The entire problem becomes counting how many different values appear in the array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Counting distinct values | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array and store every value that appears.

The original order is irrelevant because Alice can rearrange everything before the game starts.
2. Count the number of unique values.

Each unique value can be turned into exactly one maximal block by placing all equal values together.
3. Check the parity of the number of unique values.

If the count is odd, Alice removes the final remaining block and wins. If the count is even, Bob gets the last move and wins.

### Why it works

After Alice rearranges the array, all equal values can be placed consecutively. This creates one block for each distinct value. Creating more than one block from the same value would only increase the number of moves and can never help Alice because both players remove exactly one block per turn.

The game is therefore identical to a normal alternating removal game with one object per distinct value. Alice wins exactly when the number of objects is odd because she starts and takes every odd-numbered move.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        seen = set(a)

        if len(seen) % 2 == 1:
            ans.append("Alice")
        else:
            ans.append("Bob")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The set is used because it stores only distinct values. The size of the set is the number of blocks Alice can create after rearranging.

The input size can be large, so the solution uses `sys.stdin.readline` and collects outputs before printing once. Python integers do not overflow here because we only store values and counts.

The only subtle point is avoiding any dependence on the original positions. Sorting the array or checking adjacent elements would solve a different problem because Alice changes the arrangement before the game starts.

I’ll continue with the remaining sections (worked examples, complexity analysis, test cases, and edge cases) in the next message.
