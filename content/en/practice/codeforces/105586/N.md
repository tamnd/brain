---
title: "CF 105586N - \u54e5\u4f26\u6bd4\u4e9a\u5927\u9009"
description: "We are given a small list of candidates in a presidential election, where each candidate has a name and a number representing how many supporters they have. The task is to determine which candidate has the largest number of supporters and output that candidate’s name."
date: "2026-06-22T14:46:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105586
codeforces_index: "N"
codeforces_contest_name: "\u201c\u534e\u4e3a\u676f\u201d 2024 \u5e74\u5e7f\u4e1c\u5de5\u4e1a\u5927\u5b66 ACM \u65b0\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\uff08\u51b3\u8d5b\uff09"
rating: 0
weight: 105586
solve_time_s: 39
verified: true
draft: false
---

[CF 105586N - \u54e5\u4f26\u6bd4\u4e9a\u5927\u9009](https://codeforces.com/problemset/problem/105586/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small list of candidates in a presidential election, where each candidate has a name and a number representing how many supporters they have. The task is to determine which candidate has the largest number of supporters and output that candidate’s name.

The input consists of a single integer $n$, followed by $n$ lines. Each line describes one candidate using a string for the name and an integer for their supporter count. The guarantee that all names are distinct and all supporter counts are distinct removes any ambiguity about ties, so there is always exactly one unique winner.

From a computational perspective, $n \le 10$, which is extremely small. Even a naive $O(n^2)$ or worse approach would be trivially fast, but the structure of the problem suggests a direct linear scan is sufficient. The only meaningful constraint is that the parsing of input must be correct and that we maintain the maximum correctly.

There are no tricky structural edge cases involving duplicates because both names and values are guaranteed unique. The only subtle failure mode is incorrectly initializing the maximum tracker or mishandling the first element, which can lead to missing the true maximum when all values are negative or small, though here values are positive.

A representative edge case is:

Input:

```
3
A 10
B 20
C 15
```

The correct output is `B`. A careless approach might incorrectly initialize the maximum supporter count to 0 and fail if all values were negative in a variant problem, but here values are at least 1, so that particular bug is harmless but still a common pattern issue in similar problems.

## Approaches

The most direct strategy is to read each candidate one by one, keeping track of the best candidate seen so far. For each entry, we compare its supporter count with the current maximum. If it exceeds the current best, we update both the maximum value and the stored name.

A brute-force interpretation would be to, for each candidate, scan all others to check if any have more supporters. That would involve $O(n^2)$ comparisons, which is still completely fine for $n \le 10$, but it introduces unnecessary repeated work and more complex code without any benefit.

The key observation is that the problem is a classic single-pass maximum selection. Since we only need the global maximum of a small collection of pairs, we do not need any sorting or repeated comparisons. One traversal is enough to maintain correctness because the maximum of a prefix can always be updated incrementally when a larger value appears.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted but unnecessary |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process candidates sequentially and maintain the best seen so far.

1. Read the number of candidates $n$. This tells us how many updates we will perform in our scan.
2. Read the first candidate and initialize both the current best name and best supporter count with this value. This avoids having to invent a sentinel value and guarantees correctness even if all values are small.
3. For each remaining candidate, read its name and supporter count.
4. Compare the supporter count with the current best value. If it is larger, replace both the stored best value and the associated name. This ensures that the best candidate always corresponds to the maximum value seen so far.
5. After processing all candidates, output the stored best name.

### Why it works

At any moment during the scan, the algorithm maintains the invariant that the stored pair is the maximum among all candidates processed so far. Each new candidate either preserves this invariant (if it is not larger) or restores it by replacing the stored pair with a strictly larger supporter count. Since every candidate is processed exactly once, by the end the invariant extends to the entire input, meaning the stored candidate is the global maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())

best_name = ""
best_count = -1

for i in range(n):
    name, cnt = input().split()
    cnt = int(cnt)
    
    if i == 0 or cnt > best_count:
        best_count = cnt
        best_name = name

print(best_name)
```

The implementation relies on a simple linear scan. We initialize the best tracker using the first element or a sentinel pair where the count is set to -1. This guarantees that any valid input value will replace it immediately if needed.

The conditional `i == 0` ensures that we always correctly initialize from actual data rather than relying purely on sentinel logic. The comparison `cnt > best_count` enforces strict maximum tracking, which is safe because all counts are distinct.

## Worked Examples

### Example 1

Input:

```
5
A 10
B 50
C 20
D 80
E 30
```

| Step | Name | Count | Best Name | Best Count |
| --- | --- | --- | --- | --- |
| 1 | A | 10 | A | 10 |
| 2 | B | 50 | B | 50 |
| 3 | C | 20 | B | 50 |
| 4 | D | 80 | D | 80 |
| 5 | E | 30 | D | 80 |

The maximum is updated whenever a larger supporter count appears. The final stored candidate is D, which correctly corresponds to the largest value.

### Example 2

Input:

```
4
X 5
Y 3
Z 9
W 8
```

| Step | Name | Count | Best Name | Best Count |
| --- | --- | --- | --- | --- |
| 1 | X | 5 | X | 5 |
| 2 | Y | 3 | X | 5 |
| 3 | Z | 9 | Z | 9 |
| 4 | W | 8 | Z | 9 |

The scan demonstrates that the algorithm only updates when a strictly larger value appears, ensuring correct tracking of the global maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each candidate is processed exactly once with constant-time comparison |
| Space | O(1) | Only a fixed number of variables are stored |

Given $n \le 10$, the runtime is effectively instantaneous. Even if the constraint were much larger, the same linear scan strategy would remain optimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    n = int(input().strip())
    best_name = ""
    best_count = -1
    
    for i in range(n):
        name, cnt = input().split()
        cnt = int(cnt)
        if i == 0 or cnt > best_count:
            best_count = cnt
            best_name = name
    
    return best_name

# provided sample
assert run("""6
Keqing 1
LuoXuan 321
XianYa 333
XuFeichi 233
CZY 777
PangXiang 888
MarkMax 1000
""") == "MarkMax"

# minimum size
assert run("""1
Solo 42
""") == "Solo"

# increasing order
assert run("""3
A 1
B 2
C 3
""") == "C"

# decreasing order
assert run("""3
A 3
B 2
C 1
""") == "A"

# mixed values
assert run("""4
A 10
B 5
C 15
D 12
""") == "C"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | Solo | single candidate edge case |
| increasing order | C | repeated updates |
| decreasing order | A | no update after first |
| mixed values | C | non-monotonic tracking |

## Edge Cases

Since the constraints guarantee at least one candidate, the only structural edge case is handling $n = 1$. In that case, initialization from the first element immediately makes it both the first and best candidate, and the loop does not modify it.

For example:

```
1
Solo 42
```

The algorithm sets `best_name = Solo`, `best_count = 42`, and skips all updates. The output remains `Solo`, which is correct by definition.

No other edge cases affect correctness because there are no ties and no missing values, so every comparison is strictly deterministic.
