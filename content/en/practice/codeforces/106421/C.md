---
title: "CF 106421C - Champion's Meeting (Easy)"
description: "We have two ordered teams of racers. Each team has a list of prestige levels, and we need build a single team by taking racers from both lists while keeping the original order inside each team."
date: "2026-06-25T09:41:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106421
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 3-11-2026 Div. 2 (Advanced)"
rating: 0
weight: 106421
solve_time_s: 35
verified: true
draft: false
---

[CF 106421C - Champion's Meeting (Easy)](https://codeforces.com/problemset/problem/106421/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two ordered teams of racers. Each team has a list of prestige levels, and we need build a single team by taking racers from both lists while keeping the original order inside each team. The output is not the merged prestige sequence itself, but the choices that create it: each character tells whether the next racer comes from Team A or Team B.

The goal is to make the resulting prestige sequence lexicographically smallest. Since smaller prestige numbers mean a more prestigious racer, a sequence is considered better when it puts smaller numbers as early as possible.

The easy version has `k = n + m`, and every racer has a unique prestige level. This uniqueness is the key constraint. The total number of racers can be as large as `400000`, so an algorithm that repeatedly scans the remaining racers or tries all possible interleavings would perform far too many operations. We need a linear solution where each racer is processed only a constant number of times.

A common mistake is to think about future positions instead of the current choice. For example, consider:

```
n = 2, m = 2
A = [1, 4]
B = [2, 3]
```

The correct output is:

```
AABB
```

because the merged sequence becomes `[1,2,3,4]`. A strategy that chooses from B because it sees that B has two small values remaining would already lose, since the first element would become `2` instead of `1`.

Another edge case is when one team runs out of racers:

```
n = 2, m = 1
A = [2, 3]
B = [1]
```

The correct output is:

```
BAA
```

After taking the `1` from Team B, only Team A remains. A careless implementation that assumes both current positions always exist could access invalid indices or fail to append the remaining racers.

The last important case is already handled by the constraints, but it explains why the easy version is simpler:

```
n = 2, m = 2
A = [1, 2]
B = [1, 3]
```

If duplicate prestige levels were allowed, comparing only the current racers would not always decide correctly because equal values require looking deeper into the remaining suffixes. The easy version removes this problem because every prestige level appears exactly once.

## Approaches

The brute-force approach is to generate every possible valid interleaving of the two teams, calculate the resulting prestige sequence, and keep the lexicographically smallest one. This is correct because it directly checks every possible answer. However, the number of interleavings is enormous. Choosing which `n` positions belong to Team A among `n+m` positions gives `C(n+m,n)` possibilities. Even for a few dozen racers this becomes impossible, and with hundreds of thousands of racers it is not remotely feasible.

The structure of the easy version gives a much simpler approach. At any point, the next racer in the merged team must be either the current racer of Team A or the current racer of Team B. Since all prestige levels are distinct, these two values cannot be equal. The smaller one must be chosen, because the first position where two possible answers differ determines which sequence is lexicographically smaller.

The brute-force method works because it explores every choice, but fails because the choice space grows exponentially. The observation that the first differing position completely decides the comparison lets us make each decision greedily and discard all worse choices immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n+m,n) * (n+m)) | O(n+m) | Too slow |
| Optimal | O(n+m) | O(1) besides output | Accepted |

## Algorithm Walkthrough

1. Keep two pointers, one pointing to the next unused racer in Team A and one pointing to the next unused racer in Team B.
2. While both teams still have racers available, compare the two current prestige levels. Append `A` if Team A's racer has the smaller value, otherwise append `B`. This places the smallest possible racer at the earliest undecided position.
3. When one team has no racers left, append the remaining choices from the other team. There is no longer a decision to make because every remaining racer must appear.
4. Print the constructed sequence of `A` and `B` characters.

Why it works: At every position in the answer, the only possible next elements are the two current racers. If we choose the larger one, the alternative sequence immediately has a smaller value at this exact position, so our choice cannot be lexicographically minimal. Because every choice preserves the original order of both teams, repeatedly making the smallest available choice produces the globally smallest valid merge.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    i = 0
    j = 0
    ans = []

    while i < n and j < m:
        if a[i] < b[j]:
            ans.append('A')
            i += 1
        else:
            ans.append('B')
            j += 1

    while i < n:
        ans.append('A')
        i += 1

    while j < m:
        ans.append('B')
        j += 1

    print(''.join(ans))

if __name__ == "__main__":
    solve()
```

The code follows the greedy process directly. The variables `i` and `j` always refer to the next unused racer in their respective teams. The first loop handles the only interesting case, where both choices are available.

The second and third loops are separated because after one side is exhausted there is no comparison to perform. This also avoids boundary errors from trying to access `a[i]` or `b[j]` after reaching the end of a list.

The value of `k` is read because it belongs to the input format, but it is not needed in the easy version. The fact that `k = n + m` guarantees that all prestige values are unique, which is exactly the property used by the greedy comparison.

## Worked Examples

Consider:

```
3 2 5
1 4 5
2 3
```

The trace is:

| Step | Team A pointer | Team B pointer | Current A | Current B | Choice | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 2 | A | A |
| 2 | 1 | 0 | 4 | 2 | B | AB |
| 3 | 1 | 1 | 4 | 3 | B | ABB |
| 4 | 1 | 2 | 4 | none | A | ABBA |
| 5 | 2 | 2 | 5 | none | A | ABBAA |

The result is `ABBAA`, creating the merged prestige sequence `[1,2,3,4,5]`. This demonstrates that once one side is empty, the rest of the answer is forced.

Another example:

```
2 3 5
2 5
1 3 4
```

The trace is:

| Step | Team A pointer | Team B pointer | Current A | Current B | Choice | Answer |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 2 | 1 | B | B |
| 2 | 0 | 1 | 2 | 3 | A | BA |
| 3 | 1 | 1 | 5 | 3 | B | BAB |
| 4 | 1 | 2 | 5 | 4 | B | BABB |
| 5 | 1 | 3 | 5 | none | A | BABBA |

The output is `BABBA`. The algorithm always picks the smallest currently available prestige level, producing `[1,2,3,4,5]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n+m) | Every racer is considered once and contributes one character to the answer. |
| Space | O(n+m) | The output string stores exactly one character per racer. |

The maximum input size is hundreds of thousands of racers, so a linear scan is necessary. The solution performs only simple comparisons and appends, which fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def solve(data):
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(data)
    out = io.StringIO()
    sys.stdout = out

    input = sys.stdin.readline

    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    i = 0
    j = 0
    ans = []

    while i < n and j < m:
        if a[i] < b[j]:
            ans.append('A')
            i += 1
        else:
            ans.append('B')
            j += 1

    while i < n:
        ans.append('A')
        i += 1

    while j < m:
        ans.append('B')
        j += 1

    print(''.join(ans))

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

assert solve("""3 2 5
1 4 5
2 3
""") == "ABBAA\n", "basic merge"

assert solve("""2 3 5
2 5
1 3 4
""") == "BABBA\n", "smallest starts from B"

assert solve("""1 1 2
2
1
""") == "BA\n", "minimum size"

assert solve("""5 1 6
1 2 3 4 6
5
""") == "AAAABA\n", "boundary with one racer in B"

assert solve("""4 4 8
1 3 5 7
2 4 6 8
""") == "ABABABAB\n", "alternating values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 2 5 / 1 4 5 / 2 3` | `ABBAA` | Normal greedy merging |
| `2 3 5 / 2 5 / 1 3 4` | `BABBA` | The second team can provide the first racer |
| `1 1 2 / 2 / 1` | `BA` | Minimum input size and immediate comparison |
| `5 1 6 / 1 2 3 4 6 / 5` | `AAAABA` | Correct handling when one team is almost empty |
| `4 4 8 / 1 3 5 7 / 2 4 6 8` | `ABABABAB` | Repeated boundary choices |

## Edge Cases

For the first edge case:

```
2 2 4
1 4
2 3
```

The algorithm compares `1` and `2`, chooses `A`, then compares `4` and `2`, chooses `B`, then compares `4` and `3`, chooses `B`, and finally appends the remaining `A`. The output is `ABBA`. The greedy decision is correct because choosing `B` first would make the merged sequence begin with `2`, which is worse than beginning with `1`.

For the exhausted-team case:

```
2 1 3
2 3
1
```

The first comparison chooses `B` because `1` is smaller than `2`. Team B is then empty, so the algorithm appends the two remaining Team A racers. The output is `BAA`, and the merged sequence is `[1,2,3]`.

For the duplicate-value situation that would appear in a harder version:

```
2 2 3
1 2
1 3
```

A comparison of only the current values would not be enough because both choices begin with `1`. The easy version avoids this ambiguity because all values are unique, allowing the current comparison alone to determine the correct decision.
