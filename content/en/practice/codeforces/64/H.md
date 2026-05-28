---
title: "CF 64H - Table Bowling"
description: "We are given the final standings of a table bowling tournament. Every participant has a unique name and an integer score. The task is not just to sort the players, but also to assign ranking labels in the style used in real tournaments."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "sortings"]
categories: ["algorithms"]
codeforces_contest: 64
codeforces_index: "H"
codeforces_contest_name: "Unknown Language Round 1"
rating: 2300
weight: 64
solve_time_s: 112
verified: true
draft: false
---

[CF 64H - Table Bowling](https://codeforces.com/problemset/problem/64/H)

**Rating:** 2300  
**Tags:** *special, sortings  
**Solve time:** 1m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the final standings of a table bowling tournament. Every participant has a unique name and an integer score. The task is not just to sort the players, but also to assign ranking labels in the style used in real tournaments.

Players are ordered primarily by decreasing score. If two players have the same score, their names decide the order lexicographically. After sorting, we must output each participant together with their place.

The tricky part is handling ties correctly. If several players share the same score, they also share the same range of places. For example, if three players occupy positions 5, 6, and 7 because they all have score 100, then every one of them must receive the label `5-7`.

The input size is tiny. At most 100 participants exist, so even quadratic solutions are completely safe. A simple sort already solves almost all of the problem. The real challenge is formatting the ranking intervals correctly.

The dangerous edge cases are all related to ties.

Consider this input:

```
3
alice 10
bob 10
carol 10
```

All three players share positions 1 through 3, so the correct output is:

```
1-3 alice
1-3 bob
1-3 carol
```

A careless implementation might instead print:

```
1 alice
2 bob
3 carol
```

That would incorrectly assign distinct ranks to tied scores.

Another subtle case appears when a tie occurs in the middle of the table:

```
5
anna 100
bella 90
claire 90
diana 80
eva 70
```

The correct output is:

```
1 anna
2-3 bella
2-3 claire
4 diana
5 eva
```

The next rank after the tie must continue from the actual occupied positions. After places 2 and 3 are shared, the next participant receives place 4, not 3.

One more case that often causes off-by-one mistakes is a tie at the end:

```
4
a 5
b 4
c 1
d 1
```

The correct output is:

```
1 a
2 b
3-4 c
3-4 d
```

When processing grouped scores, we must compute the interval boundaries carefully.

## Approaches

The brute-force idea is straightforward. First sort all participants by descending score and ascending name. Then, for every participant, scan the entire array to count how many players share the same score and determine the first and last positions of that score group.

This works because the constraints are tiny. With at most 100 players, an `O(n^2)` scan performs only about 10,000 comparisons in the worst case.

Still, the repeated rescanning is unnecessary. After sorting, equal scores become consecutive. That observation changes the problem from "search globally for matching scores" into "process contiguous groups."

Once the array is sorted, we can walk through it from left to right. Suppose indices `i ... j` all share the same score. Then these players occupy positions `i + 1 ... j + 1` in the ranking because rankings are 1-based.

If `i == j`, the player has a unique rank, so we print a single number. Otherwise, the whole group shares the interval `i+1 - j+1`.

The reason this grouping works is that sorting already guarantees two properties simultaneously. Scores appear in ranking order, and equal scores form one continuous block. That means every tied group can be processed independently in one pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all participants into an array of `(name, score)` pairs.
2. Sort the array using two keys:

- score in descending order
- name in ascending lexicographical order

This produces the exact output ordering required by the statement.
3. Initialize an index `i = 0`.
4. While `i < n`, find the maximal segment of players having the same score.

Start another pointer `j = i`, then move `j` forward while the next participant has the same score.
5. The players in indices `i ... j` occupy ranking positions `i + 1 ... j + 1`.

Rankings are 1-based, so array index 0 corresponds to place 1.
6. If `i == j`, print:

```
place name
```

Otherwise, print:

```
start-end name
```

for every participant in the group.
7. Set `i = j + 1` and continue processing the next score group.

### Why it works

After sorting, every participant with a higher score appears earlier in the array. Participants with equal scores appear consecutively because they compare equally on the primary sorting key.

For a group occupying indices `i ... j`, exactly `i` participants have strictly higher scores, so the first valid place is `i + 1`. Exactly `j + 1` participants have scores at least as high, so the last occupied place is `j + 1`.

Every member of the group receives the same interval, which matches the tournament ranking definition. Since every participant belongs to exactly one contiguous score group, the algorithm assigns correct places to all players.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    players = []
    
    for _ in range(n):
        name, score = input().split()
        players.append((name, int(score)))
    
    players.sort(key=lambda x: (-x[1], x[0]))
    
    ans = []
    
    i = 0
    
    while i < n:
        j = i
        
        while j + 1 < n and players[j + 1][1] == players[i][1]:
            j += 1
        
        left = i + 1
        right = j + 1
        
        for k in range(i, j + 1):
            name = players[k][0]
            
            if left == right:
                ans.append(f"{left} {name}")
            else:
                ans.append(f"{left}-{right} {name}")
        
        i = j + 1
    
    print("\n".join(ans))

solve()
```

The first stage reads all participants into a list of pairs. Using tuples keeps both the name and score together during sorting and processing.

The sorting key deserves attention. We want higher scores first, so the score is negated. Names remain in normal ascending order, which automatically resolves ties lexicographically.

The main loop processes one score group at a time. Pointer `i` marks the beginning of the current group, while `j` expands to the last participant sharing the same score.

The ranking interval comes directly from the indices. Since rankings start at 1 instead of 0, both boundaries add one to the indices.

The condition `left == right` distinguishes unique ranks from shared ranges. Without this check, a single player would incorrectly receive output like `3-3 alice`.

Finally, `i = j + 1` jumps directly to the next unprocessed score group.

## Worked Examples

### Example 1

Input:

```
5
vasya 10
ted 11
petya 10
katya 33
mike 44
```

After sorting:

| Index | Name | Score |
| --- | --- | --- |
| 0 | mike | 44 |
| 1 | katya | 33 |
| 2 | ted | 11 |
| 3 | petya | 10 |
| 4 | vasya | 10 |

Processing trace:

| i | j | Score Group | Rank Interval | Output |
| --- | --- | --- | --- | --- |
| 0 | 0 | mike | 1 | 1 mike |
| 1 | 1 | katya | 2 | 2 katya |
| 2 | 2 | ted | 3 | 3 ted |
| 3 | 4 | petya, vasya | 4-5 | 4-5 petya, 4-5 vasya |

Final output:

```
1 mike
2 katya
3 ted
4-5 petya
4-5 vasya
```

This trace demonstrates how equal scores naturally become one contiguous block after sorting. The final two players share positions 4 and 5.

### Example 2

Input:

```
6
anna 50
bella 50
claire 50
diana 20
eva 10
flora 10
```

After sorting:

| Index | Name | Score |
| --- | --- | --- |
| 0 | anna | 50 |
| 1 | bella | 50 |
| 2 | claire | 50 |
| 3 | diana | 20 |
| 4 | eva | 10 |
| 5 | flora | 10 |

Processing trace:

| i | j | Score Group | Rank Interval | Output |
| --- | --- | --- | --- | --- |
| 0 | 2 | anna, bella, claire | 1-3 | shared |
| 3 | 3 | diana | 4 | unique |
| 4 | 5 | eva, flora | 5-6 | shared |

Final output:

```
1-3 anna
1-3 bella
1-3 claire
4 diana
5-6 eva
5-6 flora
```

This example exercises two different tie groups and confirms that the next rank continues correctly after a shared interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the running time |
| Space | O(n) | The participant list and output list store all players |

With only 100 participants, the solution easily fits within the limits. Even much slower approaches would pass comfortably, but the grouped linear scan after sorting is clean and scalable.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    input = sys.stdin.readline
    
    def solve():
        n = int(input())
        
        players = []
        
        for _ in range(n):
            name, score = input().split()
            players.append((name, int(score)))
        
        players.sort(key=lambda x: (-x[1], x[0]))
        
        ans = []
        
        i = 0
        
        while i < n:
            j = i
            
            while j + 1 < n and players[j + 1][1] == players[i][1]:
                j += 1
            
            left = i + 1
            right = j + 1
            
            for k in range(i, j + 1):
                name = players[k][0]
                
                if left == right:
                    ans.append(f"{left} {name}")
                else:
                    ans.append(f"{left}-{right} {name}")
            
            i = j + 1
        
        return "\n".join(ans)
    
    return solve()

# provided sample
assert run(
"""5
vasya 10
ted 11
petya 10
katya 33
mike 44
"""
) == (
"""1 mike
2 katya
3 ted
4-5 petya
4-5 vasya"""
), "sample 1"

# minimum size
assert run(
"""1
alice 100
"""
) == (
"""1 alice"""
), "single participant"

# all equal scores
assert run(
"""3
c 5
a 5
b 5
"""
) == (
"""1-3 a
1-3 b
1-3 c"""
), "all tied"

# tie in the middle
assert run(
"""5
anna 100
bella 90
claire 90
diana 80
eva 70
"""
) == (
"""1 anna
2-3 bella
2-3 claire
4 diana
5 eva"""
), "middle tie"

# tie at the end
assert run(
"""4
a 5
b 4
c 1
d 1
"""
) == (
"""1 a
2 b
3-4 c
3-4 d"""
), "ending tie"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single participant | `1 alice` | Minimum input size |
| All equal scores | `1-3 ...` | Entire table sharing one rank range |
| Tie in the middle | `2-3 ...` | Correct continuation after ties |
| Tie at the end | `3-4 ...` | Off-by-one correctness for final group |

## Edge Cases

Consider the case where every participant has the same score:

```
4
dan 50
anna 50
mike 50
bob 50
```

After sorting lexicographically within equal scores:

```
anna 50
bob 50
dan 50
mike 50
```

The algorithm starts with `i = 0` and expands `j` until `j = 3` because every score matches. The interval becomes `1-4`, which is printed for every participant:

```
1-4 anna
1-4 bob
1-4 dan
1-4 mike
```

This confirms that one large score block is handled correctly.

Now consider a tie only at the beginning:

```
4
alice 100
bob 100
carol 90
dave 80
```

The first group occupies indices `0..1`, so both players receive `1-2`. The next participant starts at index `2`, which corresponds to place `3`.

Output:

```
1-2 alice
1-2 bob
3 carol
4 dave
```

This validates that rankings continue after the full size of the tie group, not after its first position.

Finally, consider lexicographical ordering inside ties:

```
3
zack 10
anna 10
mike 10
```

All scores are equal, so names determine the order:

```
anna
mike
zack
```

The algorithm outputs:

```
1-3 anna
1-3 mike
1-3 zack
```

Without the secondary sort by name, the output order would be incorrect even though the ranking intervals themselves were correct.
