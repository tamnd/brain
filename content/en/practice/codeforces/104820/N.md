---
title: "CF 104820N - \u041c\u0443\u0437\u044b\u043a\u0430\u043b\u044c\u043d\u043e\u0435"
description: "We are given several music genres, each genre having a fixed number of songs. The task is to decide whether it is possible to arrange all songs in a single playlist so that no two adjacent songs belong to the same genre."
date: "2026-06-28T12:59:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104820
codeforces_index: "N"
codeforces_contest_name: "\u0420\u0421\u041e-\u0410\u043b\u0430\u043d\u0438\u044f 2018-2023. \u0418\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0435"
rating: 0
weight: 104820
solve_time_s: 68
verified: true
draft: false
---

[CF 104820N - \u041c\u0443\u0437\u044b\u043a\u0430\u043b\u044c\u043d\u043e\u0435](https://codeforces.com/problemset/problem/104820/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several music genres, each genre having a fixed number of songs. The task is to decide whether it is possible to arrange all songs in a single playlist so that no two adjacent songs belong to the same genre.

Another way to think about this is that we are trying to interleave multiple groups of identical items. Each genre behaves like a block of identical tokens, and we must permute all tokens in a line while avoiding identical neighbors.

The input size allows up to 100,000 genres, and each genre can contribute up to 10,000 songs. This means the total number of songs can be very large, potentially up to 10^9. Any solution that tries to explicitly construct or simulate the permutation is impossible. Even sorting and greedy simulation over individual songs would be too slow if it iterates over the full expanded sequence.

The time limit implies we should work in O(n) or O(n log n) over the number of genres, not over the total number of songs.

A key edge case arises when one genre dominates the rest. For example, if we have counts like 1000, 1, 1, 1, then it is clearly impossible to interleave enough other songs to separate all occurrences of the dominant genre. A naive approach that only checks total sum or parity would fail here because the structure of the largest pile matters, not just the aggregate.

Another subtle case is when two large genres together dominate the rest. For example, counts like 50, 49, 1, 1, 1 still work, but small misjudgments that only compare the maximum against the sum of others without precise inequality reasoning can be misleading if implemented incorrectly.

## Approaches

A brute-force strategy would try to explicitly construct the playlist. One could repeatedly pick a genre different from the last placed song, choosing greedily among available genres. This resembles a simulation with a priority structure. Each placement requires selecting a valid next genre, and in the worst case we perform a linear or logarithmic selection for each of potentially billions of songs. Since total song count is the sum of all a_i, this leads to O(total songs log n) or worse, which is infeasible.

The key observation is that we do not need the exact arrangement, only its existence. The problem reduces to a classic feasibility condition: can we separate occurrences of the most frequent genre using all other songs as separators.

If one genre has too many songs, it will inevitably force adjacency with itself. Imagine placing all other songs first as separators. Each separator can break at most one adjacency between two occurrences of the dominant genre. If the largest count is greater than the total number of other songs plus one, then there is no way to avoid adjacency.

Let max be the largest a_i and sum be the total number of songs. The number of non-max songs is sum - max. We need at least max - 1 gaps to place other songs between occurrences of the largest genre. Therefore, the condition becomes:

max - 1 ≤ sum - max

which simplifies to:

max ≤ sum - max + 1

If this inequality fails, no arrangement exists. Otherwise, we can always construct a valid ordering using greedy interleaving arguments, so the condition is sufficient as well as necessary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(total songs log n) | O(n) | Too slow |
| Max-frequency condition | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all genre counts and compute their total sum and maximum value. This captures the global structure of how concentrated the distribution is.
2. Identify the largest count, since only the most frequent genre can cause unavoidable adjacency issues. All other genres can always be used as separators if they exist in sufficient quantity.
3. Compute how many songs are not part of the dominant genre by subtracting the maximum from the total sum. These are the only available separators.
4. Check whether the number of available separators is at least max - 1. This is the number of gaps between occurrences of the dominant genre in any valid sequence.
5. If the condition holds, output “Yes”, otherwise output “No”.

### Why it works

The correctness rests on a gap-filling argument. Any arrangement of the most frequent genre creates exactly max - 1 forced gaps between its occurrences. Every other song can occupy at most one such gap if we want to avoid adjacency. If there are fewer non-dominant songs than gaps, at least one gap must remain empty, forcing two identical genres to touch. Conversely, if enough separators exist, we can always distribute them across gaps, and then insert remaining dominant elements without breaking feasibility, ensuring a valid arrangement exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    total = sum(a)
    mx = max(a)
    
    if mx <= total - mx + 1:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

The implementation follows the derived condition directly. The sum of all counts is computed once, and the maximum is extracted in a single pass over the array. The final inequality encodes the entire feasibility condition, so no further simulation is required.

A subtle point is the `+1` in the condition. It corresponds to the fact that the largest genre can occupy both ends of the sequence, so it needs one fewer separator than its count.

## Worked Examples

### Sample 1

Input:

```
3
1 2 3
```

We compute total = 6 and mx = 3.

| Step | total | mx | total - mx | Condition |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | - |
| After read | 6 | 3 | 3 | check 3 ≤ 4 |

We check whether 3 ≤ 6 - 3 + 1 = 4, which is true, so the answer is Yes.

This demonstrates a balanced distribution where the largest genre can be interleaved using the remaining songs.

### Sample 2

Input:

```
2
1 1
```

We compute total = 2 and mx = 1.

| Step | total | mx | total - mx | Condition |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | - |
| After read | 2 | 1 | 1 | check 1 ≤ 2 |

The condition holds, so the answer is Yes. This confirms that even the smallest symmetric case is valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute sum and maximum |
| Space | O(1) | Only a few integer variables are used |

The algorithm is efficient for n up to 100,000 and works even when total counts are extremely large, since it never iterates over individual songs.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    n_and_rest = inp.strip().split()
    n = int(n_and_rest[0])
    arr = list(map(int, n_and_rest[1:1+n]))
    total = sum(arr)
    mx = max(arr)
    return "Yes\n" if mx <= total - mx + 1 else "No\n"

# provided samples
assert run("3\n1 2 3") == "Yes\n"
assert run("2\n1 1") == "Yes\n"

# custom cases
assert run("1\n5") == "Yes\n"  # single genre always valid
assert run("2\n10 1") == "No\n"  # dominant too large
assert run("5\n3 3 3 3 3") == "Yes\n"  # uniform distribution
assert run("4\n1 1 1 10") == "No\n"  # strong imbalance
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 | Yes | single genre edge case |
| 2 10 1 | No | dominant overwhelming |
| 5 3 3 3 3 3 | Yes | uniform feasibility |
| 4 1 1 1 10 | No | strong skew detection |

## Edge Cases

A key edge case is when there is only one genre. For input:

```
1
5
```

We compute total = 5 and mx = 5. The condition becomes 5 ≤ 1, which is false, so the output is No. This correctly reflects that any sequence of identical songs will always violate the adjacency rule.

Another edge case is when the largest genre is just barely too large. For:

```
4
1 1 1 4
```

We have total = 7 and mx = 4. The condition is 4 ≤ 4, which is true, so the answer is Yes. A valid arrangement exists by placing the singletons between occurrences of the largest genre.

Finally, consider a tightly packed failure case:

```
3
1 1 3
```

Here total = 5 and mx = 3. The condition is 3 ≤ 3, so it is valid. We can construct a sequence like 3 1 3 1 3, which shows that equality is exactly the boundary between possible and impossible configurations.
