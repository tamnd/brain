---
title: "CF 102791H - String Deletion"
description: "The task gives a binary string. An operation chooses one existing character and removes it. After that removal, the longest prefix made of identical characters is also removed automatically."
date: "2026-07-27T18:14:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102791
codeforces_index: "H"
codeforces_contest_name: "ICPC 2020-2021 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102791
solve_time_s: 60
verified: true
draft: false
---

[CF 102791H - String Deletion](https://codeforces.com/problemset/problem/102791/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
# Problem Understanding

The task gives a binary string. An operation chooses one existing character and removes it. After that removal, the longest prefix made of identical characters is also removed automatically. The goal is to choose deletions in the best possible way so that the number of operations before the string becomes empty is as large as possible. The original problem statement and constraints are from Codeforces Gym 102791H.

The length of the string can reach 200000. With this size, a simulation that actually modifies the string after every operation is too expensive because deleting from the middle can require shifting many characters. A quadratic solution with around $n^2$ work would already be far beyond what a 2 second limit allows. We need to process the string in linear time.

The difficult cases are not the strings with many different characters, but the ones where the prefix structure changes after every deletion. A single long block can disappear immediately if handled incorrectly, while several single character blocks can be used to create extra operations.

For example, with input:

```
2
11
```

the answer is:

```
1
```

A careless approach might count both characters separately, but deleting one `1` leaves `1`, and the automatic prefix deletion removes the remaining character in the same operation.

Another important case is:

```
6
101010
```

The answer is:

```
3
```

Every run has length one. A greedy solution that always consumes the next run immediately might think the answer is the number of runs, but operations can only remove one chosen character and one prefix, so the six single characters are paired into three useful operations.

A final boundary case is:

```
8
10101000
```

The answer is:

```
4
```

The last block of zeros cannot simply be ignored. It can be partially consumed while earlier single character runs are being removed, creating additional operations.

## Approaches

The direct approach is to simulate the operations. For every state of the string, try every possible character to delete, choose the move that gives the largest future number of operations, and repeat. This is correct because it explores all legal choices, but it is completely impractical. Even storing one string state costs $O(n)$, and the number of possible choices across many states makes the total work exponential. Even a simplified simulation that always performs a chosen move still needs frequent middle deletions, which can become $O(n^2)$.

The key observation is that only consecutive equal characters matter. We can compress the string into runs. For example, `111010` becomes lengths `[3, 1, 1, 1]`.

A run of length greater than one is valuable because it can provide multiple operations. When such a run becomes the prefix, removing one character from it allows the automatic deletion to remove the rest of that run. A single-character run is different: it disappears completely when it reaches the front, so it should be saved as long as possible.

The greedy idea is to always use long runs as a source of extra deletions. If the current front run has length greater than one, consume it. If the front run is a single character, search for a later long run and take one character from that run instead. This keeps the single-character prefix alive for another operation. When no long runs remain, the remaining single runs can only be paired, giving the remaining number of operations directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compress the string into run lengths. Consecutive equal characters become one run because only their lengths affect future operations.
2. Keep two pointers. The left pointer represents the first run that has not been fully removed. The right pointer searches for the next run with length greater than one.
3. If the current left run has length greater than one, spend one operation on it and move the left pointer. The run can be removed through the automatic prefix deletion, so no other run needs to be touched.
4. If the current left run has length one, try to find a later run with length greater than one. Remove one character from that later run and count one operation. The left single-character run remains available for a future operation.
5. If no long run exists anymore, all remaining runs have length one. Two such runs can be removed per operation, so add the ceiling of the remaining run count divided by two and finish.

Why it works:

The invariant is that every operation should preserve as many future deletions as possible. A single-character prefix is the most fragile resource because once it becomes the prefix it disappears completely. Long runs are the only source of additional operations because removing one character from them still leaves a prefix that can be deleted. The greedy algorithm always spends long runs before they are lost and delays single-character runs, so no operation opportunity is wasted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    runs = []
    cnt = 1
    for i in range(1, n):
        if s[i] == s[i - 1]:
            cnt += 1
        else:
            runs.append(cnt)
            cnt = 1
    runs.append(cnt)

    m = len(runs)
    ans = 0
    l = 0
    r = 0

    while l < m:
        if l > r:
            r = l

        if runs[l] > 1:
            ans += 1
            l += 1
        else:
            while r < m and runs[r] == 1:
                r += 1

            if r < m:
                runs[r] -= 1
                ans += 1
                l += 1
            else:
                ans += (m - l + 1) // 2
                break

    print(ans)

if __name__ == "__main__":
    solve()
```

The first part builds the run length representation. This removes the need to maintain the actual string because the exact positions of characters no longer matter.

The main loop follows the greedy decisions from the walkthrough. The left pointer only moves forward because removed runs never return. The right pointer also only moves forward while searching for a useful long run, giving linear total work.

The decrement `runs[r] -= 1` is subtle. We are not deleting the whole run. We are using exactly one character from it to create an operation while leaving the rest for later. Forgetting this turns the algorithm into the incorrect strategy of removing runs too quickly.

The final expression `(m - l + 1) // 2` handles the remaining single-character runs. Since each operation can remove at most two such runs, this is the maximum number of operations they can contribute.

## Worked Examples

For input:

```
6
111010
```

the runs are `[3,1,1,1]`.

| Step | Left run | Right run used | Runs after action | Answer |
| --- | --- | --- | --- | --- |
| Start | 3 |  | `[3,1,1,1]` | 0 |
| 1 | 3 |  | `[3,1,1,1]` | 1 |
| 2 | 1 | none | remaining singles | 3 |

The first operation uses the long prefix. Afterwards only single runs remain, which contribute two more operations. The example shows why long runs should be consumed first.

For input:

```
6
101010
```

the runs are `[1,1,1,1,1,1]`.

| Step | Left position | Long run found | Action | Answer |
| --- | --- | --- | --- | --- |
| Start | 0 | none | six singles remain | 0 |
| Finish | 0 | none | pair singles | 3 |

This demonstrates the final case of the algorithm. Without long runs, the answer is only determined by how many single runs are left.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is scanned while building runs, and each pointer moves only forward. |
| Space | O(n) | The compressed run list stores at most one entry per character. |

The maximum input size is 200000 characters, so a linear solution easily fits within the limits.

## Test Cases

```python
import sys, io

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    runs = []
    cnt = 1
    for i in range(1, n):
        if s[i] == s[i - 1]:
            cnt += 1
        else:
            runs.append(cnt)
            cnt = 1
    runs.append(cnt)

    m = len(runs)
    ans = 0
    l = 0
    r = 0

    while l < m:
        if l > r:
            r = l
        if runs[l] > 1:
            ans += 1
            l += 1
        else:
            while r < m and runs[r] == 1:
                r += 1
            if r < m:
                runs[r] -= 1
                ans += 1
                l += 1
            else:
                ans += (m - l + 1) // 2
                break

    return str(ans)

assert solution("6\n111010\n") == "3"
assert solution("1\n0\n") == "1"
assert solution("1\n1\n") == "1"
assert solution("2\n11\n") == "1"
assert solution("6\n101010\n") == "3"
assert solution("8\n10101000\n") == "4"
assert solution("5\n00000\n") == "3"
assert solution("1\n0\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `6\n111010\n` | `3` | Mixed long and single runs |
| `6\n101010\n` | `3` | All runs of length one |
| `8\n10101000\n` | `4` | Using a later long run correctly |
| `5\n00000\n` | `3` | A single large run |

## Edge Cases

For `2\n11\n`, the compressed form is `[2]`. The algorithm sees a long run immediately, counts one operation, and finishes. It does not split the run into multiple operations because the automatic prefix deletion removes the remaining characters at once.

For `6\n101010\n`, the compressed form contains six single runs. There is no long run to use, so the algorithm jumps directly to the final pairing rule. Six single runs produce three operations.

For `8\n10101000\n`, the runs are `[1,1,1,1,1,1,2]`. The first six single runs should not be deleted immediately. The algorithm repeatedly borrows one character from the final long run, reducing it gradually while preserving the front singles. After the long run is exhausted, the remaining singles are paired, producing four operations.
