---
title: "CF 102191E - Snake Moves"
description: "The move string describes a walk on the infinite integer grid. We start at one cell, and every character moves the current position by one cell in one of the four cardinal directions."
date: "2026-08-23T23:34:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102191
codeforces_index: "E"
codeforces_contest_name: "PSUT Coding Marathon 2019"
rating: 0
weight: 102191
solve_time_s: 1739
verified: true
draft: false
---

[CF 102191E - Snake Moves](https://codeforces.com/problemset/problem/102191/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 28m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

The move string describes a walk on the infinite integer grid. We start at one cell, and every character moves the current position by one cell in one of the four cardinal directions. For a chosen substring, the snake starts from a fresh starting cell and follows only those moves. The substring is valid exactly when every cell visited during that walk is different from every earlier cell. We need the maximum possible length of such a substring. The official problem uses the same formulation and gives (n) up to (10^6).

A useful way to represent the walk is with prefix positions. Let (P_i) be the grid cell reached after the first (i) moves of the entire string, with (P_0) being the starting cell. A substring from move (l+1) through move (r) corresponds to the sequence of positions (P_l,P_{l+1},\ldots,P_r). It is valid exactly when these prefix positions are all distinct. The answer is consequently the largest value of (r-l) for which that interval of prefix positions contains no duplicate coordinate.

With (n) as large as (10^6), an algorithm with quadratic or cubic behavior cannot fit a roughly two second time limit. Even (O(n^2)) means around (5\cdot10^{11}) iterations in the worst case, far beyond what can be processed in time. We need to inspect the string essentially a constant number of times, which points toward an (O(n)) solution.

There are several edge cases that can make a careless implementation wrong. First, a single move is always valid because it visits two different cells. For input `1` followed by `R`, the answer is `1`. An implementation that only checks whether the current position has appeared after making a move could accidentally return zero.

A second case is an immediate return to the starting cell. For `RL`, the walk goes from the starting cell to the right and then returns to the starting cell, so the answer is `1`, not `2`. The starting position must be treated as an already visited cell.

A third case occurs when a repeated position belongs to an older part of the walk that is no longer inside the current candidate substring. For `RRLL`, the prefix positions are (0,1,2,1,0). After seeing the repeated position (1), the valid window begins after its previous occurrence. Later, the position (0) is repeated, but its previous occurrence is even farther to the left and is already outside the current window. A sliding window implementation that blindly moves its left boundary backward can produce a wrong answer. The correct answer is `2`, coming from the final `LL`.

Finally, repeated directions do not imply repeated cells. For `RRRRR`, every move reaches a new cell, so the answer is `5`. A solution that tracks directions instead of actual coordinates would incorrectly reject this case.

## Approaches

The direct brute force is conceptually simple. Choose every possible starting position, then extend the substring one move at a time while maintaining a set of visited cells. As soon as a cell is visited twice, stop that starting position and continue with the next one. This is correct because the set explicitly represents every cell visited by the candidate substring.

The problem is the amount of repeated work. With a fresh simulation for every substring, the total number of move checks on a string where no collision occurs is

[
1+2+\cdots+n+\text{all shorter substring lengths}
=\frac{n(n+1)(n+2)}{6},
]

which is (\Theta(n^3)), about (1.67\cdot10^{17}) operations when (n=10^6). Even reusing the visited set for each starting position improves this only to (\Theta(n^2)), with (n(n+1)/2), about (5\cdot10^{11}), iterations in an all-right string. Both approaches are far too slow.

The key observation is that the walk of every substring is already encoded in the single prefix-position sequence (P_0,P_1,\ldots,P_n). A substring is valid precisely when the corresponding consecutive prefix positions are distinct. We have thus reduced the problem to finding the longest contiguous interval of this sequence containing no duplicate value.

That is exactly the structure handled by a sliding window. Maintain a left boundary such that every prefix position inside the current window is unique. When the new position has appeared before inside the window, move the left boundary just past its previous occurrence. Each prefix position enters the window once and leaves it at most once, so the whole process is linear.

The brute force works because it checks whether each candidate walk contains a repeated cell, but fails because it repeatedly reconstructs information that neighboring substrings share. The prefix-position representation exposes that shared information, and the sliding window lets us maintain the longest duplicate-free interval incrementally.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)), or (O(n^2)) with reuse | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Treat the initial cell as prefix position (P_0=(0,0)), and maintain the current coordinates ((x,y)). We will process the moves from left to right and construct (P_1,P_2,\ldots,P_n).
2. Maintain a dictionary `last` mapping each visited grid cell to the index of its most recent occurrence in the prefix-position sequence. Initially, `(0,0)` occurs at index `0`.
3. Maintain `left`, the smallest prefix index currently allowed in the sliding window. At every point, all positions (P_{\text{left}},\ldots,P_i) must be distinct.
4. For each move, update ((x,y)) to the new grid cell and increment the prefix index (i). Encode the coordinate as one integer and look it up in `last`.
5. If the coordinate has appeared before at index `p`, check whether `p >= left`. If so, the new position duplicates a cell currently inside the window, so the only way to restore uniqueness is to set `left = p + 1`. If `p < left`, the previous occurrence is already outside the current window, so it must not affect `left`.
6. Store the current index as the latest occurrence of this coordinate. Updating the stored index is necessary because a future duplicate should be compared against the most recent occurrence.
7. The prefix positions from `left` through `i` contain `i - left + 1` cells, which correspond to `i - left` moves. Update the answer with `i - left`.
8. After processing every move, print the largest value recorded in the answer.

The invariant is that immediately after every iteration, the prefix-position sequence from `left` through the current index contains no duplicate coordinate, and `left` is the smallest boundary that makes this true. When a duplicate appears, every window ending at the current index and starting at or before its previous occurrence is invalid, while the window starting immediately after that occurrence is valid with respect to the newly introduced duplicate. Thus moving `left` to `p+1` removes exactly the necessary part of the window. Since every valid substring corresponds to a duplicate-free interval of prefix positions, recording the largest window length finds the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def longest_valid(s):
    n = len(s)

    # Every coordinate lies in [-n, n].
    # Encode (x, y) into one integer to avoid the memory cost
    # of storing a tuple for every visited cell.
    base = 2 * n + 1

    x = 0
    y = 0
    key = n * base + n

    last = {key: 0}
    left = 0
    ans = 0

    for i, c in enumerate(s, 1):
        if c == 'R':
            x += 1
        elif c == 'L':
            x -= 1
        elif c == 'U':
            y += 1
        else:
            y -= 1

        key = (x + n) * base + (y + n)

        previous = last.get(key, -1)
        if previous >= left:
            left = previous + 1

        last[key] = i

        length = i - left
        if length > ans:
            ans = length

    return ans

def solve():
    n = int(input())
    s = input().strip()
    print(longest_valid(s))

if __name__ == "__main__":
    solve()
```

The `longest_valid` function is the complete sliding window described above. The dictionary starts with the origin at prefix index zero because the snake is not allowed to return to its starting cell during the selected substring.

The coordinate update happens before the dictionary lookup because `last` stores prefix positions, and prefix position (P_i) is the cell reached after performing move (i). The enumeration starts at one, so its index naturally matches the prefix index.

The expression `previous >= left` is the critical boundary condition. A previous occurrence before `left` belongs to a part of the prefix sequence that has already been excluded from the current substring. Moving `left` because of such an occurrence would incorrectly discard valid moves.

The answer is `i - left`, rather than `i - left + 1`, because the window contains prefix positions, while the requested answer counts moves. For example, prefix positions (P_2,P_3,P_4) contain three cells but represent only the two moves between them.

The coordinate encoding uses the fact that after at most (n) moves, both coordinates are between (-n) and (n). The factor `base = 2*n + 1` makes every pair map to a unique integer. Using one integer as the dictionary key is substantially more memory-conscious than storing a Python tuple `(x, y)` for up to one million positions, which matters under the 256 MB memory limit.

Python integers are unbounded, so the encoded coordinate cannot overflow. The largest encoded value is only on the order of (n^2), which is easily handled by Python's integer representation.

## Worked Examples

### Sample 1

For `RULD`, the prefix positions are obtained by starting at `(0, 0)` and applying one move at a time.

| Prefix index `i` | Move | Position | Previous index | `left` after update | Current length | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | start | `(0,0)` |  | 0 | 0 | 0 |
| 1 | R | `(1,0)` | none | 0 | 1 | 1 |
| 2 | U | `(1,1)` | none | 0 | 2 | 2 |
| 3 | L | `(0,1)` | none | 0 | 3 | 3 |
| 4 | D | `(0,0)` | 0 | 1 | 3 | 3 |

At prefix index four, the snake returns to the origin. The previous occurrence is at index zero, so the window must start at index one. The resulting window contains three moves, corresponding to the valid substring `ULD`. The complete four move sequence is invalid because it revisits the starting cell.

### Sample 2

For `RRDDLLUUURDDR`, the coordinates evolve as follows.

| Prefix index `i` | Move | Position | Previous index | `left` after update | Current length | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | start | `(0,0)` |  | 0 | 0 | 0 |
| 1 | R | `(1,0)` | none | 0 | 1 | 1 |
| 2 | R | `(2,0)` | none | 0 | 2 | 2 |
| 3 | D | `(2,1)` | none | 0 | 3 | 3 |
| 4 | D | `(2,2)` | none | 0 | 4 | 4 |
| 5 | L | `(1,2)` | none | 0 | 5 | 5 |
| 6 | L | `(0,2)` | none | 0 | 6 | 6 |
| 7 | U | `(0,1)` | none | 0 | 7 | 7 |
| 8 | U | `(0,0)` | 0 | 1 | 7 | 7 |
| 9 | U | `(0,-1)` | none | 1 | 8 | 8 |
| 10 | R | `(1,-1)` | none | 1 | 9 | 9 |
| 11 | D | `(1,0)` | 1 | 2 | 9 | 9 |
| 12 | D | `(1,1)` | none | 2 | 10 | 10 |
| 13 | R | `(2,1)` | 3 | 4 | 9 | 10 |

The maximum occurs at prefix index twelve. The window is (P_2) through (P_{12}), which contains eleven distinct cells and therefore represents ten moves. At index thirteen, `(2,1)` repeats the position from index three. Since index three is inside the current window, `left` moves to four, shrinking the candidate to nine moves. The answer remains ten.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Every move performs a constant number of coordinate updates and dictionary operations. |
| Space | (O(n)) | At most one dictionary entry is stored for each distinct visited grid cell. |

The input can contain one million moves, so linear processing is appropriate. The algorithm performs one pass over the string and stores at most one million prefix positions. The integer coordinate encoding keeps the dictionary representation considerably smaller than a dictionary keyed by two element tuples, making the approach suitable for the 256 MB memory limit.

## Test Cases

```python
import sys
import io

def longest_valid(s):
    n = len(s)
    base = 2 * n + 1

    x = 0
    y = 0
    key = n * base + n

    last = {key: 0}
    left = 0
    ans = 0

    for i, c in enumerate(s, 1):
        if c == 'R':
            x += 1
        elif c == 'L':
            x -= 1
        elif c == 'U':
            y += 1
        else:
            y -= 1

        key = (x + n) * base + (y + n)

        previous = last.get(key, -1)
        if previous >= left:
            left = previous + 1

        last[key] = i
        ans = max(ans, i - left)

    return ans

def run(inp: str) -> str:
    data = inp.split()
    n = int(data[0])
    s = data[1]
    assert len(s) == n
    return str(longest_valid(s)) + "\n"

assert run("4\nRULD\n") == "3\n", "sample 1"
assert run("13\nRRDDLLUUURDDR\n") == "10\n", "sample 2"
assert run("3\nRRU\n") == "3\n", "sample 3"

assert run("1\nR\n") == "1\n", "minimum-size input"
assert run("2\nRL\n") == "1\n", "immediate return to the origin"
assert run("4\nRRRR\n") == "4\n", "all equal moves"
assert run("4\nRRLL\n") == "2\n", "duplicate outside the current window"
assert run("1000000\n" + "R" * 1000000 + "\n") == "1000000\n", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / R` | `1` | Minimum input size and the fact that one move is always valid |
| `2 / RL` | `1` | Returning to the starting cell must be rejected |
| `4 / RRRR` | `4` | Repeated directions can still visit entirely different cells |
| `4 / RRLL` | `2` | A repeated position outside the active window must not move `left` backward |
| `1000000 / RRR...R` | `1000000` | Maximum input size and linear performance |

## Edge Cases

For the minimum-size case `1 / R`, the algorithm begins with `last[(0,0)] = 0`. After `R`, the position is `(1,0)`, which has never appeared, so `left` stays zero and the current length is `1 - 0 = 1`. The output is `1`.

For the immediate-return case `2 / RL`, the prefix positions are `(0,0)`, `(1,0)`, `(0,0)`. The second move finds `(0,0)` at prefix index zero. Since zero is inside the current window, `left` becomes one. The resulting length is `2 - 1 = 1`, so the output is `1`. This explicitly accounts for the starting cell as part of the visited cells.

For `4 / RRLL`, the prefix positions are `(0,0)`, `(1,0)`, `(2,0)`, `(1,0)`, `(0,0)`. At prefix index three, `(1,0)` was last seen at index one, so `left` becomes two. The current valid window represents one move. At prefix index four, `(0,0)` was last seen at index zero, which is smaller than `left = 2`. That old occurrence is no longer part of the candidate substring, so `left` remains two. The current window represents two moves, namely `LL`, and the output is `2`.

For the all-right input `5 / RRRRR`, the positions are `(0,0)`, `(1,0)`, `(2,0)`, `(3,0)`, `(4,0)`, `(5,0)`. Every coordinate is new, so `left` never changes. At the final position, the window length is `5 - 0 = 5`, giving output `5`. The example demonstrates why the algorithm tracks cells rather than move characters.

For the maximum input containing one million `R` moves, every prefix coordinate is distinct, so the dictionary receives one million entries and the answer reaches one million. There is no nested loop, and each move performs constant-time dictionary work, so the running time remains (O(n)) even in this worst case.
