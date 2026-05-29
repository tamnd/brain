---
title: "CF 254A - Cards with Numbers"
description: "We have 2n cards laid out in a sequence. Every card has an integer written on it, and each card also has an index from 1 to 2n. The task is to divide all cards into exactly n pairs such that both cards inside every pair contain the same number."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "sortings"]
categories: ["algorithms"]
codeforces_contest: 254
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 155 (Div. 2)"
rating: 1200
weight: 254
solve_time_s: 150
verified: false
draft: false
---

[CF 254A - Cards with Numbers](https://codeforces.com/problemset/problem/254/A)

**Rating:** 1200  
**Tags:** constructive algorithms, sortings  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We have `2n` cards laid out in a sequence. Every card has an integer written on it, and each card also has an index from `1` to `2n`. The task is to divide all cards into exactly `n` pairs such that both cards inside every pair contain the same number.

The output does not ask for the values themselves. It asks for the indices of the cards that form valid pairs. If even one value appears an odd number of times, forming complete pairs becomes impossible and we must print `-1`.

The constraints immediately tell us the solution must be close to linear time. There are up to `6 * 10^5` cards in total, so anything quadratic would explode. A naive pair-searching approach that repeatedly scans the remaining cards would perform on the order of `(2n)^2` comparisons in the worst case, which is far too large for a one-second limit. On the other hand, hashing or grouping values by frequency easily fits because each card only needs to be processed a constant number of times.

There are a few edge cases that can silently break careless implementations.

Consider this input:

```
2
1 2 1 2
```

A correct answer is:

```
1 3
2 4
```

A buggy implementation might accidentally reuse an index after pairing it once, especially if it only tracks values and not which specific occurrences were consumed.

Another important case is when a value appears an odd number of times:

```
2
5 5 5 7
```

The value `5` appears three times, so one copy will always remain unmatched. The correct output is:

```
-1
```

A careless greedy solution might pair two `5`s and forget to verify that all occurrences were consumed.

There is also the case where all cards contain the same number:

```
3
9 9 9 9 9 9
```

Every index must still appear exactly once in the output. The valid pairing is arbitrary, but the implementation must avoid skipping or duplicating positions.

## Approaches

The brute-force idea is straightforward. For every unpaired card, scan the remaining cards until finding another card with the same value. Once found, mark both as used and continue.

This works because any valid solution only requires grouping equal values together. The problem is efficiency. In the worst case, every search may scan almost the entire remaining array. With up to `6 * 10^5` cards, the number of comparisons can reach roughly `3.6 * 10^11`, which is completely infeasible.

The key observation is that the actual positions matter only after grouping cards by value. If we know all indices where a particular number occurs, then forming pairs becomes trivial. We simply take those indices two at a time.

This transforms the problem from repeated searching into a grouping problem. We traverse the array once, store every index inside a bucket corresponding to its value, then verify that every bucket has even size. If any bucket size is odd, pairing is impossible. Otherwise, consecutive indices inside the bucket form valid pairs automatically.

The values are at most `5000`, so even an array of vectors would work, but a hash map is equally clean and general.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and the array of `2n` card values.
2. Create a dictionary where each key is a card value and the associated list stores all indices where that value appears.
3. Traverse the array from left to right.
4. For every position `i`, append index `i + 1` into the list corresponding to value `a[i]`.

We store `i + 1` because the problem uses 1-based indexing.
5. After grouping all indices, iterate through every value group.
6. If the size of any group is odd, print `-1` and terminate immediately.

An odd count means one card can never be matched with another identical card.
7. Otherwise, process the group's indices two at a time.
8. Print `(indices[0], indices[1])`, then `(indices[2], indices[3])`, and so on.

Since all indices inside the group belong to the same value, every produced pair is valid.

### Why it works

The algorithm maintains a simple invariant: every stored list contains exactly the indices of cards with the same value.

If a value occurs an odd number of times, at least one card remains unmatched in every possible arrangement, so no valid solution exists.

If a value occurs an even number of times, pairing consecutive indices inside that group always works because every pair contains identical values and no index is reused. Since the groups partition all indices of the array, every card appears in exactly one printed pair.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    pos = defaultdict(list)

    for i, x in enumerate(a, start=1):
        pos[x].append(i)

    ans = []

    for indices in pos.values():
        if len(indices) % 2 == 1:
            print(-1)
            return

        for i in range(0, len(indices), 2):
            ans.append((indices[i], indices[i + 1]))

    print("\n".join(f"{x} {y}" for x, y in ans))

solve()
```

The dictionary `pos` is the core structure of the solution. Each value maps to all indices where it appears. Because we append indices while scanning left to right, every occurrence is recorded exactly once.

The `enumerate(..., start=1)` call is important because the problem expects indices beginning from `1`. Forgetting this is one of the most common mistakes.

The parity check comes before creating pairs. Once a group has odd size, there is no reason to continue processing because the entire instance is impossible.

The pairing loop advances by `2` each iteration. This guarantees that every index is used exactly once and prevents accidental overlap between pairs.

The solution does not rely on sorting. The original order of indices already provides enough structure.

## Worked Examples

### Example 1

Input:

```
3
20 30 10 30 20 10
```

After grouping:

| Value | Indices |
| --- | --- |
| 20 | [1, 5] |
| 30 | [2, 4] |
| 10 | [3, 6] |

Pair construction:

| Current Group | Produced Pair |
| --- | --- |
| [1, 5] | (1, 5) |
| [2, 4] | (2, 4) |
| [3, 6] | (3, 6) |

Possible output:

```
1 5
2 4
3 6
```

This trace demonstrates the central invariant of the algorithm. Every group contains indices of exactly one value, so any consecutive pairing is automatically valid.

### Example 2

Input:

```
2
5 5 5 7
```

After grouping:

| Value | Indices |
| --- | --- |
| 5 | [1, 2, 3] |
| 7 | [4] |

Parity check:

| Value | Count | Even? |
| --- | --- | --- |
| 5 | 3 | No |
| 7 | 1 | No |

Output:

```
-1
```

This example shows why the parity condition is both necessary and sufficient. Once a value has odd frequency, one occurrence must remain unmatched.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each card index is inserted once and processed once more during pairing |
| Space | O(n) | The dictionary stores all `2n` indices |

The constraints allow up to `6 * 10^5` cards total, so linear complexity is easily fast enough. The memory usage is also safe because we only store the indices themselves.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    pos = defaultdict(list)

    for i, x in enumerate(a, start=1):
        pos[x].append(i)

    ans = []

    for indices in pos.values():
        if len(indices) % 2 == 1:
            print(-1)
            return

        for i in range(0, len(indices), 2):
            ans.append((indices[i], indices[i + 1]))

    print("\n".join(f"{x} {y}" for x, y in ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
out = run("3\n20 30 10 30 20 10\n")
pairs = set(tuple(map(int, line.split())) for line in out.splitlines())

assert len(pairs) == 3

# minimum size valid
assert run("1\n7 7\n") == "1 2"

# impossible because of odd frequency
assert run("2\n5 5 5 7\n") == "-1"

# all equal values
out = run("3\n9 9 9 9 9 9\n")
pairs = [tuple(map(int, line.split())) for line in out.splitlines()]
used = set()

for x, y in pairs:
    used.add(x)
    used.add(y)

assert len(pairs) == 3
assert used == {1, 2, 3, 4, 5, 6}

# alternating values
out = run("2\n1 2 1 2\n")
pairs = [tuple(map(int, line.split())) for line in out.splitlines()]
used = set()

for x, y in pairs:
    used.add(x)
    used.add(y)

assert len(pairs) == 2
assert used == {1, 2, 3, 4}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7 7` | `1 2` | Smallest valid input |
| `2 / 5 5 5 7` | `-1` | Odd frequency detection |
| `3 / 9 9 9 9 9 9` | Any full pairing | Repeated identical values |
| `2 / 1 2 1 2` | Any valid pairing | Non-adjacent matching indices |

## Edge Cases

Consider the input:

```
2
1 2 1 2
```

The groups become:

```
1 -> [1, 3]
2 -> [2, 4]
```

The algorithm pairs consecutive indices inside each group, producing:

```
1 3
2 4
```

Even though equal values are separated in the original array, grouping by value removes positional complications completely.

Now consider:

```
2
5 5 5 7
```

The stored groups are:

```
5 -> [1, 2, 3]
7 -> [4]
```

During validation, the algorithm detects that both groups have odd size. At that moment it immediately prints `-1`. No partial pairing is attempted, so the algorithm never produces an invalid incomplete answer.

Finally, consider the all-equal case:

```
3
9 9 9 9 9 9
```

The single group becomes:

```
9 -> [1, 2, 3, 4, 5, 6]
```

The pairing loop processes indices in steps of two:

```
(1, 2)
(3, 4)
(5, 6)
```

Every index is used exactly once, which confirms that the algorithm handles large duplicate groups correctly.
