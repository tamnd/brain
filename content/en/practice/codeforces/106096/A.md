---
title: "CF 106096A - Deck Building"
description: "The problem is about building a Clash Royale deck from paired cards. We have two arrays, where index i describes a pair of cards with costs a[i] and b[i]. When building the deck, we cannot take only one card from a pair."
date: "2026-06-25T11:59:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106096
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 10-1-25 Div. 2 (Beginner)"
rating: 0
weight: 106096
solve_time_s: 41
verified: true
draft: false
---

[CF 106096A - Deck Building](https://codeforces.com/problemset/problem/106096/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem is about building a Clash Royale deck from paired cards. We have two arrays, where index `i` describes a pair of cards with costs `a[i]` and `b[i]`. When building the deck, we cannot take only one card from a pair. Choosing an index means both cards from that index are added. Exactly four indices must be chosen, because each chosen pair contributes two cards and the final deck must contain eight cards. The goal is to find the minimum possible total elixir cost of the eight selected cards.

The important part of the constraints is that the number of pairs can be up to 100. That is small enough for a quadratic or cubic approach, but too large for enumerating every possible group of four indices. Choosing four indices directly has about `n^4` possibilities, which becomes around 100 million combinations when `n = 100`, and each combination would still require checking its cost. We need to use the fact that four is a fixed small number and reduce the search space.

The edge cases come from treating a pair as two separate cards or forgetting that every chosen index contributes both cards. For example, if the input is:

```
4
1 2 3 4
4 3 2 1
```

Choosing the first four indices is the only possible deck, and the answer is:

```
20
```

A careless solution that sorts all eight individual cards and tries to pick the smallest ones would incorrectly choose only one card from some pairs.

Another tricky case is when the best four indices are not the four smallest pair sums. For example:

```
5
1 100 1 100 1
100 1 100 1 1
```

The pair sums are all `101, 101, 101, 101, 2`. The minimum deck must include the index with sum `2` and three of the other indices, but choosing only by individual card values can lead to an invalid selection.

## Approaches

A direct approach would try every possible set of four indices. For each set, we add the two cards from each chosen index and keep the smallest total. This is correct because every valid deck corresponds to exactly one group of four indices. However, the number of choices is `C(n,4)`. With `n = 100`, that is about 3.9 million groups. This is not catastrophic, but the implementation becomes unnecessarily heavy, and the constraints are designed around noticing a simpler transformation.

The key observation is that a chosen index always contributes `a[i] + b[i]` to the total. The internal order of the two cards does not matter because both must be included. The problem becomes choosing exactly four values from the array of pair sums. Once we compute these sums, the answer is simply the sum of the four smallest values.

The brute force works because it examines every valid deck. The improvement comes from recognizing that all information about an index can be compressed into one number, its contribution to the final score.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) | O(1) | Too slow / unnecessary |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of card pairs and the two arrays containing the card costs.
2. Create a new list where each element is `a[i] + b[i]`. This works because selecting an index always places both cards from that index into the deck, so the only value that matters is the total contribution.
3. Sort the list of pair sums. Sorting allows us to consider the cheapest possible contributions first.
4. Add the first four values from the sorted list. These four indices produce the minimum possible eight card deck because replacing any selected larger contribution with a smaller unused contribution can only reduce the total.
5. Print the resulting minimum total cost.

Why it works: every valid deck is exactly a choice of four indices, and each chosen index has a fixed cost equal to the sum of its two cards. After converting the problem into choosing four numbers, the optimal choice is always the four smallest numbers. If a chosen set contained a larger value while an unchosen value was smaller, swapping them would create a cheaper valid deck, which contradicts optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    costs = []
    for i in range(n):
        costs.append(a[i] + b[i])

    costs.sort()

    print(sum(costs[:4]))

if __name__ == "__main__":
    solve()
```

The first part of the code reads the two arrays. The arrays are kept separate because the input format provides them separately, but the algorithm immediately combines them into the only values that matter.

The loop builds the contribution list. There is no need to store the chosen indices because only the minimum total cost is required, not the actual deck.

After sorting, taking `costs[:4]` is the same as selecting the four cheapest possible pairs. The slice boundary is fixed because the final deck always requires exactly four indices.

Python integers handle the possible sums safely. Since each card cost is at most 1000 and only eight cards are added, overflow is not a concern.

## Worked Examples

### Sample 1

Input:

```
6
4 3 9 2 9 2
1 3 8 3 1 5
```

| Step | Pair sums | Sorted sums | Current answer |
| --- | --- | --- | --- |
| Create sums | 5, 6, 17, 5, 10, 7 |  | 0 |
| Sort |  | 5, 5, 6, 7, 10, 17 | 0 |
| Take four smallest |  |  | 23 |

The algorithm chooses the pairs with contributions `5, 5, 6, 7`, giving a total of `23`. This demonstrates that the pair is the true unit of choice.

### Sample 2

Input:

```
4
1 2 4 8
1 2 4 8
```

| Step | Pair sums | Sorted sums | Current answer |
| --- | --- | --- | --- |
| Create sums | 2, 4, 8, 16 |  | 0 |
| Sort |  | 2, 4, 8, 16 | 0 |
| Take four smallest |  |  | 30 |

All four indices must be used because there are exactly four available pairs. The result is the total of all eight cards.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | We compute all pair sums and sort them |
| Space | O(n) | We store the list of pair contributions |

The maximum input size is only 100 pairs, so sorting is easily fast enough. The memory usage is also minimal because the stored list has one value per index.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    costs = [a[i] + b[i] for i in range(n)]
    costs.sort()

    return str(sum(costs[:4])) + "\n"

assert solve("""6
4 3 9 2 9 2
1 3 8 3 1 5
""") == "23\n", "sample 1"

assert solve("""4
1 2 4 8
1 2 4 8
""") == "30\n", "sample 2"

assert solve("""4
1 2 3 4
4 3 2 1
""") == "20\n", "all pairs must be chosen"

assert solve("""5
1 100 1 100 1
100 1 100 1 1
""") == "305\n", "pair constraint"

assert solve("""100
""" + " ".join(["1000"] * 100) + "\n" + " ".join(["1000"] * 100) + "\n") == "8000\n", "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Four pairs with equal totals | 20 | Handles the case where every pair must be selected |
| Mixed large and small cards | 305 | Confirms that pairs cannot be split |
| 100 identical pairs | 8000 | Confirms the maximum input size |

## Edge Cases

For the first edge case, consider:

```
4
1 2 3 4
4 3 2 1
```

The pair sums become `[5, 5, 5, 5]`. The algorithm sorts them and takes all four values, producing `20`. It does not try to choose the individual cards `1, 2, 2, 3` because those cards come from different invalid combinations.

For the second edge case:

```
5
1 100 1 100 1
100 1 100 1 1
```

The pair sums are `[101, 101, 101, 101, 2]`. Sorting gives `[2, 101, 101, 101, 101]`. The chosen deck has cost `305`. The algorithm succeeds because it compares whole pair contributions instead of individual cards.
