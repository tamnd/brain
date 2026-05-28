---
title: "CF 47B - Coins"
description: "We have three coins labeled A, B, and C. Every pair of coins has already been compared once using a balance scale, and each comparison tells us which coin is heavier."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 47
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 44 (Div. 2)"
rating: 1200
weight: 47
solve_time_s: 102
verified: true
draft: false
---
[CF 47B - Coins](https://codeforces.com/problemset/problem/47/B)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three coins labeled `A`, `B`, and `C`. Every pair of coins has already been compared once using a balance scale, and each comparison tells us which coin is heavier.

A line like `A>B` means coin `A` is heavier than coin `B`. Since heavier coins are assumed to have larger denominations, the task is really about recovering the complete ordering of the three coins from lightest to heaviest.

The input always contains exactly three comparisons, one for each pair among the three coins. The output should be a string of length three representing the coins from smallest weight to largest weight. If the comparisons contradict each other and no valid ordering exists, we print `Impossible`.

The constraints are tiny because there are only three coins. Any reasonable algorithm will fit easily within the limits. Even checking every possible ordering is effectively constant time because there are only `3! = 6` permutations. The challenge is not performance but correctly detecting contradictions.

The tricky part is that some comparison sets form cycles. For example:

```
A>B
B>C
C>A
```

This says `A` is heavier than `B`, `B` is heavier than `C`, and `C` is heavier than `A`. No ordering can satisfy all three conditions simultaneously. A careless implementation that only counts wins or losses might accidentally produce an invalid order instead of detecting the contradiction.

Another subtle case is when the comparisons are already given in mixed directions:

```
A<B
C<B
A<C
```

The correct order is `ACB`. If we only track direct relationships without considering the full ordering, we may incorrectly place `B` too early because it appears on both sides of comparisons.

A third edge case is when two coins appear equally constrained:

```
A>B
A>C
B<C
```

The correct order is `BCA`. The strongest coin is easy to identify, but the remaining two still need to be ordered carefully. Sorting by only "number of victories" works here, but only because the graph is acyclic. Without contradiction checks, the same logic breaks on cyclic inputs.

## Approaches

The most direct brute-force solution is to generate all six possible orderings of the three coins and test each one against the comparisons.

Suppose we try the permutation `CAB`. This means `C < A < B`. For every input relation, we verify whether it agrees with the positions inside the permutation. If all three comparisons match, we have found the answer.

This approach is correct because every valid total ordering must appear among the six permutations. The algorithm simply checks all candidates until one satisfies every condition.

With only six permutations, the running time is effectively constant. Even though brute force is completely acceptable here, it is still useful to think about why it works. We are validating global consistency directly instead of trying to infer the order incrementally.

There is also a cleaner observation-based solution.

Each comparison gives one directed relation between coins. If we count how many times each coin is heavier than another coin, the lightest coin will have zero wins, the middle coin will have one win, and the heaviest coin will have two wins, assuming the comparisons are consistent.

For example:

```
A>B
C<B
A>C
```

Coin `A` wins twice, `C` wins once, and `B` wins zero times. Sorting by the number of wins gives `BCA`, but that is from weakest to strongest in terms of victories. Since victories correspond to heavier coins, we reverse the interpretation and obtain `CBA` as the increasing order of weight.

The useful insight is that with exactly three distinct elements, a valid ordering forms a strict chain. The outdegree counts uniquely determine the position of every coin unless a contradiction exists.

The contradiction case appears naturally. In a cycle like:

```
A>B
B>C
C>A
```

every coin has exactly one win. No unique ordering exists because all counts are identical. Detecting duplicate counts immediately reveals inconsistency.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(6 × 3) | O(1) | Accepted |
| Optimal | O(3) | O(1) | Accepted |

## Algorithm Walkthrough

1. Create a dictionary storing the number of wins for each coin: `A`, `B`, and `C`.
2. Read the three comparisons one by one.
3. For each comparison:

If the relation is `X>Y`, increment the win count of `X`.

If the relation is `X<Y`, increment the win count of `Y`.

The heavier coin gains one victory because it dominates the lighter coin.
4. After processing all comparisons, examine the three win counts.
5. In a valid ordering, the counts must be exactly `0`, `1`, and `2` in some order.

If two coins share the same count, the relations are contradictory, so print `Impossible`.
6. Otherwise, sort the coins by increasing number of wins.

A coin with fewer wins is lighter because it was heavier than fewer other coins.
7. Output the sorted sequence as a string.

### Why it works

Every valid ordering of three distinct coins forms a strict ranking. The lightest coin is heavier than nobody, so it gets `0` wins. The middle coin is heavier than exactly one coin, so it gets `1` win. The heaviest coin is heavier than both others, so it gets `2` wins.

A contradiction creates a cycle, which prevents these counts from being unique. In a cycle, no coin can consistently occupy a unique position in the ranking. Since the algorithm only accepts the distinct pattern `0,1,2`, it rejects every contradictory configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

wins = {'A': 0, 'B': 0, 'C': 0}

for _ in range(3):
    s = input().strip()

    if s[1] == '>':
        wins[s[0]] += 1
    else:
        wins[s[2]] += 1

values = list(wins.values())

if len(set(values)) < 3:
    print("Impossible")
else:
    order = sorted(wins.keys(), key=lambda x: wins[x])
    print(''.join(order))
```

The dictionary `wins` stores how many times each coin appeared as the heavier coin.

Each comparison has length three, so `s[0]` and `s[2]` are the coin labels while `s[1]` is either `<` or `>`.

When the relation is `A>B`, coin `A` gains one win because it is heavier. When the relation is `A<B`, coin `B` gains one win instead.

After all comparisons are processed, the solution checks whether all counts are distinct. A valid chain of three elements must produce counts `{0,1,2}`. Any repeated value indicates a cycle or contradiction.

The sorting step is subtle. We sort in increasing order of wins because fewer wins means lighter weight. If we accidentally sort in descending order, the output would become heaviest-to-lightest instead of the required lightest-to-heaviest.

No extra graph structure is necessary because there are only three nodes and the outdegree counts fully determine the order.

## Worked Examples

### Example 1

Input:

```
A>B
C<B
A>C
```

| Step | Comparison | Wins A | Wins B | Wins C |
| --- | --- | --- | --- | --- |
| Initial | - | 0 | 0 | 0 |
| 1 | A>B | 1 | 0 | 0 |
| 2 | C<B | 1 | 1 | 0 |
| 3 | A>C | 2 | 1 | 0 |

Sorting by increasing wins gives:

```
C B A
```

Output:

```
CBA
```

This trace demonstrates the clean ranking structure `0,1,2`. Every coin occupies a unique position, so the ordering is valid.

### Example 2

Input:

```
A>B
B>C
C>A
```

| Step | Comparison | Wins A | Wins B | Wins C |
| --- | --- | --- | --- | --- |
| Initial | - | 0 | 0 | 0 |
| 1 | A>B | 1 | 0 | 0 |
| 2 | B>C | 1 | 1 | 0 |
| 3 | C>A | 1 | 1 | 1 |

The counts are all identical.

Since the values are not distinct, the algorithm prints:

```
Impossible
```

This example shows how cycles destroy the unique ranking required for a valid ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only three comparisons and three coins are processed |
| Space | O(1) | The dictionary stores data for exactly three coins |

The input size never grows beyond a tiny constant, so the solution runs instantly within the limits. Memory usage is also constant because only a few integers and characters are stored.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    wins = {'A': 0, 'B': 0, 'C': 0}

    for _ in range(3):
        s = input().strip()

        if s[1] == '>':
            wins[s[0]] += 1
        else:
            wins[s[2]] += 1

    if len(set(wins.values())) < 3:
        print("Impossible")
    else:
        order = sorted(wins.keys(), key=lambda x: wins[x])
        print(''.join(order))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("A>B\nC<B\nA>C\n") == "CBA", "sample 1"

# cyclic contradiction
assert run("A>B\nB>C\nC>A\n") == "Impossible", "cycle detection"

# already increasing
assert run("A<B\nB<C\nA<C\n") == "ABC", "simple sorted order"

# reverse order
assert run("A>B\nA>C\nB>C\n") == "CBA", "fully descending"

# mixed relations
assert run("A<C\nB>A\nB<C\n") == "ABC", "mixed direction comparisons"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A>B, B>C, C>A` | `Impossible` | Detects cyclic contradictions |
| `A<B, B<C, A<C` | `ABC` | Handles already sorted ordering |
| `A>B, A>C, B>C` | `CBA` | Handles fully reversed ranking |
| `A<C, B>A, B<C` | `ABC` | Verifies mixed comparison directions |

## Edge Cases

Consider the contradictory cycle:

```
A>B
B>C
C>A
```

The algorithm counts wins:

```
A = 1
B = 1
C = 1
```

Since the counts are not unique, the algorithm immediately prints `Impossible`. This correctly rejects the impossible ordering.

Now consider a case where comparisons are written in mixed directions:

```
A<B
C<B
A<C
```

Processing the comparisons gives:

```
A = 0
C = 1
B = 2
```

Sorting by wins produces `ACB`, which matches the true lightest-to-heaviest order. The algorithm does not care about input direction because it always increments the heavier coin.

Finally, consider:

```
A>B
A>C
B<C
```

The win counts become:

```
C = 0
B = 1
A = 2
```

The output is `CBA`. This case confirms that the middle coin is determined correctly even when the strongest coin is obvious from the start.
