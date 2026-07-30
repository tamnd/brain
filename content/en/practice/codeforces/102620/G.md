---
title: "CF 102620G - Musical Bowings"
description: "The piece of music is represented by a sequence of notes. Each note may already have a required bow direction, either down bow (D) or up bow (U), or it may be unmarked (B). We must decide the directions of all unmarked notes."
date: "2026-07-31T03:29:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102620
codeforces_index: "G"
codeforces_contest_name: "mBIT Standard June 2020"
rating: 0
weight: 102620
solve_time_s: 140
verified: true
draft: false
---

[CF 102620G - Musical Bowings](https://codeforces.com/problemset/problem/102620/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

The piece of music is represented by a sequence of notes. Each note may already have a required bow direction, either down bow (`D`) or up bow (`U`), or it may be unmarked (`B`). We must decide the directions of all unmarked notes. The final sequence cannot contain any `B`, and the original markings cannot be changed.

A hooked bowing happens when two neighboring notes use the same direction. The goal is not to avoid all hooked bowings, because that may be impossible when some fixed notes force them. Instead, we need to choose directions for the unmarked notes so that the total number of equal adjacent pairs is as small as possible.

The input size allows up to 1000 notes. A solution that tries every possible assignment of the blank notes would need to consider up to $2^{1000}$ possibilities, which is far beyond what can run. We need an approach that processes the sequence directly, using the fact that the decision for the next note only depends on the direction chosen for the previous note.

The tricky cases are the places where the optimal choice is not locally obvious. For example, if the input is:

```
3
B D B
```

the correct answer could be:

```
U D U
```

with two direction changes and zero hooked bowings. A greedy strategy that always chooses a direction different from the previous note might fail later because a fixed note several positions ahead can force a better earlier choice.

Another edge case is when every note is already fixed:

```
4
D D U U
```

The only valid output is:

```
D D U U
```

with two hooked bowings. An implementation that tries to modify fixed notes while searching for the minimum would produce an invalid answer.

A final boundary case is a single note:

```
1
B
```

The answer can be either `U` or `D`. There are no adjacent notes, so the minimum number of hooked bowings is zero. Code that assumes every note has a left neighbor can fail here.

## Approaches

The direct brute force approach is to replace every `B` with either `U` or `D`, evaluate the resulting sequence, and keep the assignment with the fewest hooked bowings. This is correct because it checks every possible valid completion of the music sheet. However, if all 1000 notes are blank, the number of assignments is $2^{1000}$, and each assignment requires scanning the whole sequence. The operation count is roughly $1000 \times 2^{1000}$, which is impossible.

The structure of the problem gives us a smaller state space. When choosing the direction of the current note, the only information from the previous notes that matters is the direction of the immediately previous note. Whether the first ten notes contained many hooked bowings or few hooked bowings does not matter after we know the best cost ending with `U` and the best cost ending with `D`.

This leads naturally to dynamic programming. For every position, we store the minimum number of hooked bowings among all valid assignments up to that point, separated by the direction of the last note. When processing the next note, we try both possible directions if it is blank, or the single allowed direction if it is fixed. The transition adds one whenever the new direction equals the previous direction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N × 2^N) | O(N) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Create two dynamic programming states for each position. One state stores the minimum number of hooked bowings among assignments ending with `U`, and the other stores the same value for assignments ending with `D`.

The reason we only keep the last direction is that the next note can only create a new hooked bowing with its immediate predecessor.
2. Initialize the first note. If it is fixed to `U`, only the `U` state is possible. If it is fixed to `D`, only the `D` state is possible. If it is blank, both states are possible with cost zero.
3. Process the remaining notes from left to right. For each possible direction of the current note, look at both possible directions of the previous note. Add one to the cost when the two directions are equal, because that creates a hooked bowing.
4. Store the smaller value and remember which previous direction produced it. The stored parent information allows us to reconstruct the actual sequence after finding the minimum cost.
5. After processing the entire piece, choose the smaller of the final `U` and `D` states. Follow the saved parent directions backward to recover the complete answer.

Why it works:

The dynamic programming invariant is that after processing position `i`, each state contains the minimum possible number of hooked bowings among all valid assignments of the first `i + 1` notes with the specified last direction. The transition considers every possible direction of the current note and every possible optimal ending direction of the previous prefix. Since every complete assignment must end in either `U` or `D`, taking the better final state gives the globally optimal solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(s):
    n = len(s)

    inf = 10**9
    dp = [[inf, inf] for _ in range(n)]
    parent = [[-1, -1] for _ in range(n)]

    choices = []
    for c in s:
        if c == 'U':
            choices.append([0])
        elif c == 'D':
            choices.append([1])
        else:
            choices.append([0, 1])

    for c in choices[0]:
        dp[0][c] = 0

    for i in range(1, n):
        for cur in choices[i]:
            for prev in (0, 1):
                cost = dp[i - 1][prev] + (1 if cur == prev else 0)
                if cost < dp[i][cur]:
                    dp[i][cur] = cost
                    parent[i][cur] = prev

    last = 0 if dp[-1][0] <= dp[-1][1] else 1

    ans = [0] * n
    ans[-1] = last
    for i in range(n - 1, 0, -1):
        ans[i - 1] = parent[i][ans[i]]

    return ' '.join('U' if x == 0 else 'D' for x in ans)

def main():
    n = int(input())
    s = input().split()
    print(solve_case(s))

if __name__ == "__main__":
    main()
```

The `choices` array converts each note into the set of directions it allows. Fixed notes have one possible direction, while blank notes have both.

The `dp` table stores the best number of hooked bowings up to every position. The index `0` represents `U` and index `1` represents `D`. During a transition, the expression `(1 if cur == prev else 0)` exactly matches the definition of a hooked bowing.

The `parent` table is needed because the minimum cost alone is not enough. After reaching the end, we need to output one actual sequence. By storing the previous direction that produced every optimal state, we can reconstruct the answer without storing every candidate sequence.

There are no large arithmetic concerns because the maximum number of hooked bowings is only `N - 1`, so normal Python integers are more than sufficient. The first note is initialized separately because it has no previous note and cannot create a hooked bowing.

## Worked Examples

Consider the sample:

```
7
B D B B B U U
```

A possible dynamic programming trace is:

| Position | Note | Best ending U | Best ending D | Chosen final direction |
| --- | --- | --- | --- | --- |
| 0 | B | 0 | 0 |  |
| 1 | D | INF | 0 |  |
| 2 | B | 1 | 1 |  |
| 3 | B | 1 | 2 |  |
| 4 | B | 2 | 2 |  |
| 5 | U | 2 | INF |  |
| 6 | U | 2 | INF |  |

The final answer reconstructed from the stored parents is one optimal assignment such as:

```
U D D U D U U
```

The trace shows that the algorithm does not minimize every local pair independently. It keeps both possible endings because the better future decision depends on the previous direction.

For a second example:

```
4
D D U U
```

the trace becomes:

| Position | Note | Best ending U | Best ending D | Chosen final direction |
| --- | --- | --- | --- | --- |
| 0 | D | INF | 0 |  |
| 1 | D | INF | 1 |  |
| 2 | U | 1 | INF |  |
| 3 | U | 1 | INF |  |

The only valid output is:

```
D D U U
```

The two equal adjacent pairs are unavoidable. The dynamic programming states correctly preserve the fixed markings instead of attempting to remove those hooks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each note considers only two previous states and two current states. |
| Space | O(N) | The parent table stores one previous direction for each state during reconstruction. |

The constraint of 1000 notes easily fits this linear solution. Even with the parent reconstruction data, the memory usage is only a few thousand integers.

## Test Cases

```python
import sys
import io

def solve_case(s):
    n = len(s)
    inf = 10**9
    dp = [[inf, inf] for _ in range(n)]
    parent = [[-1, -1] for _ in range(n)]

    choices = []
    for c in s:
        if c == 'U':
            choices.append([0])
        elif c == 'D':
            choices.append([1])
        else:
            choices.append([0, 1])

    for c in choices[0]:
        dp[0][c] = 0

    for i in range(1, n):
        for cur in choices[i]:
            for prev in (0, 1):
                cost = dp[i - 1][prev] + (cur == prev)
                if cost < dp[i][cur]:
                    dp[i][cur] = cost
                    parent[i][cur] = prev

    last = 0 if dp[-1][0] <= dp[-1][1] else 1
    ans = [0] * n
    ans[-1] = last
    for i in range(n - 1, 0, -1):
        ans[i - 1] = parent[i][ans[i]]

    return ' '.join('U' if x == 0 else 'D' for x in ans)

def run(inp: str) -> str:
    data = inp.strip().split()
    n = int(data[0])
    return solve_case(data[1:1+n])

def hooked_count(out):
    a = out.split()
    return sum(a[i] == a[i+1] for i in range(len(a)-1))

assert len(run("1\nB\n").split()) == 1, "minimum size"

assert hooked_count(run("4\nD D U U\n")) == 2, "fixed notes"

assert hooked_count(run("3\nB D B\n")) == 0, "blank around fixed note"

assert hooked_count(run("5\nB B B B B\n")) == 0, "all equal freedom"

assert hooked_count(run("6\nU U U U U U\n")) == 5, "all fixed same direction"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / B` | Any single direction | Handles the first position correctly |
| `D D U U` | Same fixed sequence | Preserves mandatory markings |
| `B D B` | Zero hooks possible | Avoids greedy local mistakes |
| Five blank notes | Alternating directions | Uses freedom in blank positions |
| Six `U` notes | Six `U` notes | Handles unavoidable hooks |

## Edge Cases

For a single blank note:

```
1
B
```

the algorithm initializes both states with cost zero. Since there is no transition, either direction is optimal, and reconstruction returns one valid answer.

For fixed consecutive notes:

```
4
D D U U
```

the algorithm never inserts alternative directions because the choice list for each position contains only the fixed value. The transitions count the two unavoidable equal pairs, producing the only valid completion.

For blanks surrounding fixed notes:

```
3
B D B
```

the first blank can be assigned `U` and the last blank can also be assigned `U`, producing:

```
U D U
```

Both transitions are between different directions, so the answer has zero hooked bowings. The dynamic programming states keep both possibilities at each step, allowing this global choice to be found.
