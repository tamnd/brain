---
title: "CF 102392I - Absolute Game"
description: "Alice and Bob each start with an array of (n) integers. On every turn, a player deletes one value from their own array, with Alice moving first. Deletions continue until each array contains exactly one value."
date: "2026-08-10T21:13:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102392
codeforces_index: "I"
codeforces_contest_name: "2019-2020 ICPC Southeastern European Regional Programming Contest (SEERC 2019)"
rating: 0
weight: 102392
solve_time_s: 76
verified: true
draft: false
---

[CF 102392I - Absolute Game](https://codeforces.com/problemset/problem/102392/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

Alice and Bob each start with an array of (n) integers. On every turn, a player deletes one value from their own array, with Alice moving first. Deletions continue until each array contains exactly one value. If those surviving values are (x) and (y), Alice wants to make (|x-y|) as large as possible, while Bob wants to make it as small as possible.

The input gives (n), Alice's array (a), and Bob's array (b). We need the value of (|x-y|) under optimal play.

The key difficulty is that the players do not delete from the same array. Alice can never remove a value from (b), and Bob can never remove a value from (a). That independence looks simple, but the alternating order creates a game-theoretic interaction: Bob gets to react to every deletion Alice makes.

Here (n\le 1000), so an (O(n^2)) solution already performs at most about one million pairwise operations and is easily practical. An exponential or factorial simulation of the game is completely out of the question. The values can reach (10^9), so the implementation must also handle differences safely, although Python integers have no overflow issue.

There are several boundary cases that can silently break an implementation. If (n=1), there are no moves at all. For example,

```
1
14
42
```

has answer (28). A solution that assumes at least one deletion will mishandle this case.

A second issue occurs when every value of (b) lies on one side of a value from (a). For example,

```
2
10 20
1 2
```

For (10), the closest value in (b) is (2), giving distance (8). For (20), it is again (2), giving distance (18), so the answer is (18). A binary-search implementation that checks only the element at the insertion position can fail when that position is at the end.

The opposite boundary has the same issue. For

```
2
1 20
5 15
```

the closest distances are (4) and (5), so the answer is (5). When searching for (1), the insertion position is the beginning of the sorted array, so the predecessor does not exist.

Duplicate values are another useful check. With

```
4
7 7 7 7
7 7 7 7
```

the answer is (0). Treating equal values as separate game choices does not change the value, and any solution based on sorted positions must still handle duplicates correctly.

## Approaches

A literal brute-force minimax follows every possible deletion sequence. At a state with (k) values remaining in a player's array, that player has (k) possible deletions. A complete deletion order for one array is a permutation of its (n) elements, because choosing the first (n-1) deleted elements uniquely determines the final survivor. Thus there are (n!) possible deletion histories for Alice and (n!) for Bob, giving ((n!)^2) paired terminal histories in the literal game tree. Even (n=10) already gives (10!^2\approx1.3\times10^{13}) terminal histories, so direct minimax is unusable long before the maximum (n=1000).

The brute force works because it explicitly considers every possible way the players can influence the final survivors, but it wastes almost all of its work on the order in which values are deleted. The actual payoff depends only on the two final values. The central observation is that for every Alice value (a_i), we only need to know the closest value Bob could leave against it.

Define

[
d_i=\min_j |a_i-b_j|.
]

Suppose Alice wants (a_i) to be the final value. She can simply keep (a_i) and delete every other value from her array. Bob then wants to leave a value of (b) as close as possible to (a_i). The relevant distance is exactly (d_i).

The remaining question is whether the alternating deletion order gives Bob enough control to realize that minimum. It does. Fix, for every (a_i), one Bob value (b_{f(i)}) achieving (d_i). After Alice deletes a value, suppose (k) Alice values remain. Bob has (k+1) values at that moment. At most (k) of Bob's values are currently needed as witnesses (b_{f(i)}) for the remaining Alice values. Consequently, at least one Bob value is not needed by any remaining Alice value, and Bob can safely delete that one.

Repeating this strategy lets Bob preserve a suitable witness for whichever Alice value survives. Thus Bob can always guarantee a final distance of at most (d_i) for the surviving (a_i). Alice, on the other hand, can choose the (a_i) with the largest (d_i) and keep it alive. The game value is consequently

[
\boxed{\max_i \min_j |a_i-b_j|}.
]

This reduces the game to a nearest-neighbor problem. We can compute it directly in (O(n^2)), which is already sufficient for (n\le1000). We can also sort (b), then find the closest value to every (a_i) with binary search, reducing the complexity to (O(n\log n)).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O((n!)^2)) terminal histories | Exponential recursion state | Too slow |
| Pairwise reduction | (O(n^2)) | (O(n)) | Accepted |
| Sorted nearest-neighbor | (O(n\log n)) | (O(n)) | Accepted |

The implementation below uses the sorted (O(n\log n)) version. The same game-theoretic reduction can also be implemented with the simpler (O(n^2)) pairwise scan.

## Algorithm Walkthrough

1. Read Alice's array (a) and Bob's array (b), then sort (b) in increasing order. Sorting lets us find the closest Bob value to any Alice value without checking every pair.
2. For each Alice value (x), use binary search to find the first value in (b) that is at least (x). Call its position `pos`.
3. If `pos` is inside the array, compare (x) with `b[pos]`. This is the smallest Bob value that is not below (x), so among all values on that side it is the only possible closest candidate.
4. If `pos > 0`, also compare (x) with `b[pos - 1]`. This is the largest Bob value below (x), so it is the only possible closest candidate on the other side.
5. Take the smaller of these available distances. That value is (\min_j |x-b_j|), the best distance Bob can force if Alice leaves (x).
6. Maintain the maximum of these nearest distances over all (x\in a). Alice can choose the corresponding (x) as her survivor, so this maximum is the game value.
7. Print the maximum distance.

### Why it works

Let

[
T=\max_{x\in A}\min_{y\in B}|x-y|.
]

Alice can select an (x) attaining this maximum and never delete it. Her final value is then (x), regardless of Bob's deletions.

For Bob, choose for every Alice value (x) one Bob value (f(x)) satisfying (|x-f(x)|\le T). Whenever Alice has just made a deletion and (k) values remain in her array, Bob has (k+1) values remaining. The witnesses (f(x)) for those (k) remaining Alice values use at most (k) distinct Bob values, so at least one Bob value is not a witness for any remaining Alice value. Bob deletes such an unnecessary value. This preserves a valid witness for every possible future Alice survivor.

At the end, if Alice leaves (x), Bob still has a witness (f(x)) with distance at most (T). Hence Bob guarantees a result no larger than (T), while Alice guarantees a result no smaller than (T). The game value is exactly (T).

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    b.sort()

    answer = 0

    for x in a:
        pos = bisect_left(b, x)
        best = 10**30

        if pos < n:
            best = min(best, abs(x - b[pos]))

        if pos > 0:
            best = min(best, abs(x - b[pos - 1]))

        answer = max(answer, best)

    print(answer)

if __name__ == "__main__":
    solve()
```

The input is read exactly once for each array, then Bob's array is sorted. The `bisect_left` call finds the first position whose value is at least the current Alice value.

Only two candidates need to be checked. If `pos < n`, `b[pos]` is the closest candidate on the right. If `pos > 0`, `b[pos - 1]` is the closest candidate on the left. No other element can be closer because the array is sorted.

The two boundary checks are deliberately independent. When `pos == 0`, there is no predecessor. When `pos == n`, there is no element on the right. Handling both cases explicitly avoids indexing outside the array.

`best` starts at a value much larger than any possible answer. Since all input values are at most (10^9), every absolute difference is at most (10^9-1). Python integers also make overflow irrelevant.

Finally, `answer` takes the maximum nearest-neighbor distance, matching the (\max_i\min_j) expression proved above.

## Worked Examples

For the first sample,

```
4
2 14 7 14
5 10 9 22
```

Bob's array becomes `[5, 9, 10, 22]`.

| Alice value (x) | `pos` | Right candidate | Left candidate | Nearest distance | `answer` |
| --- | --- | --- | --- | --- | --- |
| 2 | 0 | 5 | none | 3 | 3 |
| 14 | 3 | 22 | 10 | 4 | 4 |
| 7 | 1 | 9 | 5 | 2 | 4 |
| 14 | 3 | 22 | 10 | 4 | 4 |

The maximum nearest distance is (4). Alice can keep (14), while Bob can preserve (10), giving the final difference (4). The other Alice values allow Bob to get closer, so Alice prefers (14).

For the second sample,

```
1
14
42
```

there are no deletions because both arrays already contain one value.

| Alice value (x) | `pos` | Right candidate | Left candidate | Nearest distance | `answer` |
| --- | --- | --- | --- | --- | --- |
| 14 | 0 | 42 | none | 28 | 28 |

The answer is (28), directly matching the only possible final pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Sorting (b) costs (O(n\log n)), then (n) binary searches cost another (O(n\log n)) |
| Space | (O(n)) | The arrays and sorted copy of (b) require linear space |

With (n\le1000), even the simpler (O(n^2)) implementation would perform only about (10^6) distance checks. The presented (O(n\log n)) solution is comfortably within the 1 second and 256 MB limits.

## Test Cases

```python
import sys
import io
from bisect import bisect_left

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]

    b.sort()

    answer = 0

    for x in a:
        pos = bisect_left(b, x)
        best = 10**30

        if pos < n:
            best = min(best, abs(x - b[pos]))

        if pos > 0:
            best = min(best, abs(x - b[pos - 1]))

        answer = max(answer, best)

    return str(answer)

def run(inp: str) -> str:
    return solve_data(inp)

# Provided sample 1
assert run("""4
2 14 7 14
5 10 9 22
""") == "4", "sample 1"

# Provided sample 2
assert run("""1
14
42
""") == "28", "sample 2"

# Minimum size, no moves
assert run("""1
5
5
""") == "0", "minimum size"

# All values equal
assert run("""4
7 7 7 7
7 7 7 7
""") == "0", "all equal values"

# Both lower and upper binary-search boundaries
assert run("""2
1 20
5 15
""") == "5", "boundary positions"

# All Bob values below Alice values
assert run("""2
10 20
1 2
""") == "18", "lower boundary"

# Maximum n and maximum value difference
n = 1000
a = " ".join(["1000000000"] * n)
b = " ".join(["1"] * n)
max_case = f"{n}\n{a}\n{b}\n"
assert run(max_case) == "999999999", "maximum size and values"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5 / 5` | `0` | Minimum size and immediate termination |
| `4 / 7 7 7 7 / 7 7 7 7` | `0` | Duplicate and equal values |
| `2 / 1 20 / 5 15` | `5` | `bisect_left` at the beginning and end |
| `2 / 10 20 / 1 2` | `18` | No right-side binary-search candidate |
| (n=1000), all (a_i=10^9), all (b_i=1) | `999999999` | Maximum input size and value range |

## Edge Cases

The (n=1) case requires no game simulation. For

```
1
14
42
```

the only surviving values are already (14) and (42). `bisect_left([42], 14)` returns `0`, so only the right candidate is checked and the nearest distance is (28). The maximum over the one Alice value is also (28).

When the insertion position is at the beginning, the predecessor does not exist. For

```
2
1 20
5 15
```

the search for (1) returns position `0`, giving distance (4) to `5`. The search for (20) returns position `2`, so there is no right candidate and only `15` is checked, giving distance (5). The final answer is (5). These two values exercise both ends of the sorted array.

When every Bob value is smaller than the Alice value, the insertion position is always `n`. For

```
2
10 20
1 2
```

the nearest Bob value to (10) is (2), with distance (8), while the nearest value to (20) is also (2), with distance (18). The answer is (18). The `pos < n` check prevents an invalid access to `b[n]`.

Duplicate values do not create additional strategic power. With

```
4
7 7 7 7
7 7 7 7
```

every Alice value has a Bob value at distance (0). The computed nearest distance is (0) for every iteration, so the answer is (0). This also demonstrates why the argument is about values and their nearest distances, not about unique indices.

The maximum-value case is safe as well. If Alice contains only (10^9) and Bob contains only (1), the resulting difference is (999999999). The algorithm computes this directly without overflow, and the result remains within Python's integer range.
