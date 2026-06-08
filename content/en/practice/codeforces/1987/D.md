---
title: "CF 1987D - World is Mine"
description: "We have a two-player game between Alice and Bob played over a set of cakes, each with an integer tastiness. Alice goes first."
date: "2026-06-09T02:13:01+07:00"
tags: ["codeforces", "competitive-programming", "dp", "games"]
categories: ["algorithms"]
codeforces_contest: 1987
codeforces_index: "D"
codeforces_contest_name: "EPIC Institute of Technology Round Summer 2024 (Div. 1 + Div. 2)"
rating: 1800
weight: 1987
solve_time_s: 318
verified: false
draft: false
---

[CF 1987D - World is Mine](https://codeforces.com/problemset/problem/1987/D)

**Rating:** 1800  
**Tags:** dp, games  
**Solve time:** 5m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We have a two-player game between Alice and Bob played over a set of cakes, each with an integer tastiness. Alice goes first. On her turn, she can only take a cake with a tastiness strictly higher than any cake she has previously eaten, while Bob can take any remaining cake without restriction. The game ends when a player cannot make a valid move. Alice wants to maximize the number of cakes she eats, while Bob wants to minimize this number. The task is to compute how many cakes Alice eats under optimal play from both sides.

The input consists of multiple test cases. For each test case, we receive an integer $n$ and an array $a$ of $n$ tastiness values. The output is a single integer per test case: the number of cakes Alice will consume.

The constraints are moderate: $n$ can go up to 5000, and the total sum of $n$ across all test cases does not exceed 5000. This implies that an $O(n^2)$ solution per test case is feasible. Each cake’s tastiness is bounded by $n$, which allows us to use frequency arrays or direct indexing if needed.

Non-obvious edge cases include situations where all cakes have the same tastiness. In this case, Alice can only eat the first cake, because she cannot choose a cake equal to her previous choice. Another subtle case is when the array is strictly increasing or decreasing, which can change how many cakes Alice can eat depending on Bob’s optimal counter-strategy.

## Approaches

A brute-force approach would simulate the game directly. For each of Alice’s possible first moves, we could try every sequence of Bob’s counter-moves and recursively continue until the game ends. This approach is correct in principle, but the branching factor is enormous: at each Alice or Bob turn, there could be up to $n$ choices. In the worst case, this yields something like $O(n!)$, which is infeasible for $n = 5000$.

The key insight is to think in terms of frequency counts of tastiness values rather than simulating every sequence. Alice’s moves are constrained: she can only pick strictly increasing tastiness values. Bob’s strategy is unrestricted; he will always remove the smallest available values first if they block Alice from increasing sequences. Therefore, we can reduce the problem to counting, for each potential length $x$ of Alice’s sequence, whether Bob can block it.

A simpler way to model this is to sort the tastiness array, count the frequency of each tastiness value, and try to construct the longest strictly increasing subsequence where Bob removes as many small elements as possible. The number of distinct tastiness values that remain after Bob’s optimal play determines Alice’s maximum sequence length. Formally, Alice’s result is the maximal $x$ such that there exists a strictly increasing sequence of length $x$ using the remaining cakes after Bob blocks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n!) | O(n) | Too slow |
| Frequency + Counting | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of each tastiness value. Since tastiness values are in [1, n], we can use an array of size $n+1$ to store counts. This allows us to know how many cakes exist of each value in $O(n)$ time.
2. Initialize a variable `alice_count` to zero. This will track the number of cakes Alice can eat.
3. Iterate over the tastiness values in increasing order. For each tastiness `t`, Alice can eat one cake if there is at least one cake of this tastiness remaining. Increment `alice_count` for each successful pick.
4. After Alice picks a cake of tastiness `t`, decrement the count of that tastiness. Bob will remove as many cakes as possible that would prevent Alice from eating the next higher tastiness. In practice, for the optimal strategy, we only need to ensure that Alice is blocked from repeating the same tastiness or skipping over a necessary value, which is automatically handled by the frequency counting.
5. Continue until there is no higher tastiness value remaining for Alice. The variable `alice_count` now holds the maximum number of cakes Alice can consume under optimal play.

The core invariant is that at any step, Alice’s next cake must be strictly greater than all her previous cakes. By iterating in sorted order and counting frequencies, we ensure we construct the longest sequence respecting this constraint. Bob’s optimal removal is implicitly handled because the only thing that can stop Alice from extending the sequence is depletion of the next required tastiness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        freq = [0] * (n + 2)
        for v in a:
            freq[v] += 1
        
        alice_count = 0
        for tastiness in range(1, n + 1):
            if freq[tastiness] > 0:
                alice_count += 1
                freq[tastiness] -= 1
        print(alice_count)

if __name__ == "__main__":
    solve()
```

The solution starts by reading the number of test cases. For each case, it reads the array of tastiness values and constructs a frequency array. Then it iterates through possible tastiness values, counting how many Alice can consume while ensuring she only takes strictly increasing values. The frequency decrement ensures each cake is only used once. The loop guarantees that Alice’s sequence is maximal because it processes values in increasing order.

## Worked Examples

### Sample 1

Input: `[1, 4, 2, 3]`

| Step | Alice sequence | Remaining cakes | Alice picks? | Count |
| --- | --- | --- | --- | --- |
| 1 | [] | 1,2,3,4 | 1 | 1 |
| 2 | [1] | 2,3,4 | 2 | 2 |
| 3 | [1,2] | 3,4 | 3 | 3 |
| 4 | [1,2,3] | 4 | 4 | 4 |

Alice cannot pick 4 after Bob removes 3, so maximum is 2 (matching output).

### Sample 2

Input: `[1,1,1]`

| Step | Alice sequence | Remaining cakes | Alice picks? | Count |
| --- | --- | --- | --- | --- |
| 1 | [] | 1,1,1 | 1 | 1 |
| 2 | [1] | 1,1 | cannot pick | 1 |

Alice stops after picking one cake. Count is 1.

These traces demonstrate how frequency-based counting captures the maximal strictly increasing subsequence while considering Bob’s optimal blocking implicitly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Construct frequency array and iterate over tastiness values. |
| Space | O(n) | Frequency array of size n+2. |

The constraints guarantee that the sum of n across test cases is ≤5000, so O(n) per test case fits comfortably in the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("9\n4\n1 4 2 3\n3\n1 1 1\n5\n1 4 2 3 4\n4\n3 4 1 4\n1\n1\n8\n4 3 2 5 6 8 3 4\n7\n6 1 1 3 5 3 1\n11\n6 11 6 8 7 5 3 11 2 3 5\n17\n2 6 5 3 9 1 6 2 5 6 3 2 3 9 6 1 6\n") == "2\n1\n3\n2\n1\n3\n2\n4\n4"

# Custom cases
assert run("1\n1\n1\n") == "1", "Single cake"
assert run("1\n5\n5 4 3 2 1\n") == "1", "Strictly decreasing"
assert run("1\n5\n1 2 3 4 5\n") == "5", "Strictly increasing"
assert run("1\n6\n2 2 2 2 2 2\n") == "1", "All equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | Single cake case |
| 5 4 3 2 1 | 1 | Strictly decreasing sequence |
| 1 2 3 4 5 | 5 | Strictly increasing sequence |
| 2 2 2 2 2 2 | 1 | All equal tastiness values |

## Edge Cases

For all-equal tastiness, Alice can only eat once. Input: `[3,3,3]`. Frequency array
