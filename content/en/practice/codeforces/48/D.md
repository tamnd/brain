---
title: "CF 48D - Permutations"
description: "We are given a shuffled array that originally came from concatenating several permutations. Each permutation may have a different size. After concatenation, all numbers were mixed together, so the original grouping disappeared."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 48
codeforces_index: "D"
codeforces_contest_name: "School Personal Contest #3 (Winter Computer School 2010/11) - Codeforces Beta Round 45 (ACM-ICPC Rules)"
rating: 1500
weight: 48
solve_time_s: 123
verified: false
draft: false
---

[CF 48D - Permutations](https://codeforces.com/problemset/problem/48/D)

**Rating:** 1500  
**Tags:** greedy  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a shuffled array that originally came from concatenating several permutations. Each permutation may have a different size. After concatenation, all numbers were mixed together, so the original grouping disappeared.

Our task is to assign every array element to some permutation so that each group forms a valid permutation. A valid permutation of size `k` contains every integer from `1` to `k` exactly once.

For example, if a group contains `{1,2,3,4}`, it is a permutation. If it contains `{1,2,4}`, it is not, because `3` is missing. If it contains `{1,1,2}`, it is also invalid because of repetition.

The input only gives the shuffled numbers. We must reconstruct any valid grouping, or report that no such decomposition exists.

The constraint `n ≤ 10^5` immediately rules out anything quadratic. A solution that repeatedly scans all existing groups for every number would perform around `10^10` operations in the worst case, which is far beyond the time limit. We need something close to linear or `O(n log n)`.

The tricky part is understanding what conditions make a decomposition possible at all.

Suppose the value `x` appears `cnt[x]` times. Every permutation containing `x` must also contain all numbers from `1` to `x-1`. That means:

- The number of permutations containing `x` equals `cnt[x]`.
- Those same permutations must also contain `1,2,...,x-1`.

So the counts must satisfy:

```
cnt[1] ≥ cnt[2] ≥ cnt[3] ≥ ...
```

If this monotonicity fails anywhere, reconstruction is impossible.

A few edge cases are easy to mishandle.

Consider:

```
3
2 2 1
```

There are two copies of `2`, so we would need two permutations containing `2`. But every permutation containing `2` must also contain `1`. Since there is only one `1`, the answer is impossible.

Another dangerous case is:

```
5
1 3 1 2 2
```

The counts are:

```
cnt[1] = 2
cnt[2] = 2
cnt[3] = 1
```

This is valid. One possible decomposition is:

```
(1,2,3)
(1,2)
```

A careless greedy strategy that places numbers arbitrarily might create duplicate values inside a group and fail even though a valid solution exists.

The smallest case also matters:

```
1
1
```

This is already a valid permutation of size `1`.

But:

```
1
2
```

is impossible because no permutation can contain `2` without also containing `1`.

## Approaches

A brute-force approach would try to explicitly build permutations one by one. For every number in the array, we could scan all existing groups and place it into a group that does not already contain that value and still could become a valid permutation later.

This works conceptually because the only requirement is uniqueness inside each permutation and presence of smaller values. But the implementation quickly becomes expensive. If we have up to `10^5` groups and scan many of them for every element, the complexity becomes `O(n^2)`.

The structure of permutations gives a much stronger property.

If a permutation contains `x`, then it must contain every smaller positive integer. That means the set of permutations containing `x+1` is always a subset of the set containing `x`.

This turns the problem into a counting condition.

Suppose value `x` appears `k` times. Then exactly `k` permutations must contain `x`. Since every permutation containing `x+1` also contains `x`, we must have:

```
cnt[x] ≥ cnt[x+1]
```

Once this condition holds for all values, construction becomes easy.

We can create exactly `cnt[1]` permutations. Then for every value `x`, we distribute its occurrences among the first `cnt[x]` permutations. Because the counts are non-increasing, any permutation receiving `x` already received all smaller values earlier.

This greedy assignment is enough to guarantee validity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array and count the frequency of every value.

Let `cnt[x]` be the number of occurrences of value `x`.
2. Check whether the frequencies are non-increasing.

For every `x > 1`, verify:

```
cnt[x] ≤ cnt[x-1]
```

If this fails, print `-1`.

The reason is structural. Every permutation containing `x` must also contain `x-1`, so there cannot be more copies of `x` than copies of `x-1`.
3. Create `cnt[1]` permutations.

Every valid permutation must contain `1`, so the number of permutations is forced to equal the number of ones.
4. Assign occurrences greedily.

For each value `x`, distribute its occurrences among permutations `1` through `cnt[x]`.

Concretely, if `x` appears three times, assign them to permutations `1`, `2`, and `3`.
5. Produce answers for the original array order.

Since the array was shuffled, we need an assignment for each occurrence individually. Store a queue of permutation IDs for every value. When traversing the original array, pop one ID from the corresponding queue.

### Why it works

The key invariant is:

```
If permutation p receives value x, then it has already received every value from 1 to x-1.
```

This stays true because values are processed in increasing order, and value `x` is assigned only to the first `cnt[x]` permutations. Since:

```
cnt[x] ≤ cnt[x-1]
```

those permutations already received `x-1`.

Each permutation ends up containing exactly:

```
1,2,...,k
```

for some `k`, which is precisely a valid permutation.

## Python Solution

```python
import sys
from collections import defaultdict, deque

input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    freq = defaultdict(int)

    for x in a:
        freq[x] += 1

    mx = max(a)

    for x in range(2, mx + 1):
        if freq[x] > freq[x - 1]:
            print(-1)
            return

    groups = freq[1]

    assign = defaultdict(deque)

    for x in range(1, mx + 1):
        for group_id in range(1, freq[x] + 1):
            assign[x].append(group_id)

    ans = []

    for x in a:
        ans.append(assign[x].popleft())

    print(groups)
    print(*ans)

solve()
```

The first section counts frequencies. Using `defaultdict(int)` avoids manual existence checks and keeps the code clean.

The monotonicity check is the entire feasibility test. If some value appears more times than the previous value, reconstruction is impossible because every copy of the larger value requires a distinct copy of the smaller one in the same permutation.

The number of permutations is fixed as `freq[1]`. Every valid permutation must contain `1`, so there cannot be more permutations than ones, and every one belongs to a different permutation.

The assignment structure is subtle. For every value `x`, we precompute which permutation IDs should receive it:

```
1, 2, ..., freq[x]
```

Later, while traversing the original array order, we consume these IDs one by one using `popleft()`.

This preserves correctness even when equal values appear scattered throughout the array.

A common mistake is trying to assign directly during the first traversal without separating occurrences. That often creates duplicate values inside the same permutation.

## Worked Examples

### Example 1

Input:

```
9
1 2 3 1 2 1 4 2 5
```

Frequencies:

```
cnt[1] = 3
cnt[2] = 3
cnt[3] = 1
cnt[4] = 1
cnt[5] = 1
```

The counts are non-increasing, so construction is possible.

Assignments prepared:

```
1 -> [1,2,3]
2 -> [1,2,3]
3 -> [1]
4 -> [1]
5 -> [1]
```

Processing the original array:

| Position | Value | Assigned permutation | Remaining queue |
| --- | --- | --- | --- |
| 1 | 1 | 1 | [2,3] |
| 2 | 2 | 1 | [2,3] |
| 3 | 3 | 1 | [] |
| 4 | 1 | 2 | [3] |
| 5 | 2 | 2 | [3] |
| 6 | 1 | 3 | [] |
| 7 | 4 | 1 | [] |
| 8 | 2 | 3 | [] |
| 9 | 5 | 1 | [] |

Final output:

```
3
1 1 1 2 2 3 1 3 1
```

This trace shows the central invariant. Every permutation receiving a larger number already received all smaller numbers.

### Example 2

Input:

```
3
2 2 1
```

Frequencies:

| Value | Count |
| --- | --- |
| 1 | 1 |
| 2 | 2 |

Now:

```
cnt[2] > cnt[1]
```

So reconstruction is impossible.

Output:

```
-1
```

This demonstrates why the frequency condition is necessary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every element is counted and assigned once |
| Space | O(n) | Frequency tables and assignment queues store at most n values |

The solution comfortably fits the constraints. With `n = 10^5`, linear processing is easily fast enough within a 1 second limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict, deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    def solve():
        n = int(input())
        a = list(map(int, input().split()))

        freq = defaultdict(int)

        for x in a:
            freq[x] += 1

        mx = max(a)

        for x in range(2, mx + 1):
            if freq[x] > freq[x - 1]:
                print(-1)
                return

        groups = freq[1]

        assign = defaultdict(deque)

        for x in range(1, mx + 1):
            for group_id in range(1, freq[x] + 1):
                assign[x].append(group_id)

        ans = []

        for x in a:
            ans.append(assign[x].popleft())

        print(groups)
        print(*ans)

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided-style sample
assert run(
"""9
1 2 3 1 2 1 4 2 5
"""
).splitlines()[0] == "3"

# minimum valid case
assert run(
"""1
1
"""
) == """1
1"""

# impossible because 2 appears without enough 1s
assert run(
"""3
2 2 1
"""
) == "-1"

# all equal ones, each forms its own permutation
assert run(
"""4
1 1 1 1
"""
).splitlines()[0] == "4"

# exact single permutation
assert run(
"""5
1 2 3 4 5
"""
) == """1
1 1 1 1 1"""

# boundary monotonicity failure
assert run(
"""5
1 2 2 3 3
"""
) == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | One permutation | Minimum valid input |
| `2 2 1` | `-1` | Missing smaller values |
| `1 1 1 1` | Four permutations | Multiple size-1 permutations |
| `1 2 3 4 5` | One permutation | Single complete permutation |
| `1 2 2 3 3` | `-1` | Frequency monotonicity violation |

## Edge Cases

Consider:

```
3
2 2 1
```

Frequencies become:

```
cnt[1] = 1
cnt[2] = 2
```

During validation, the algorithm checks:

```
2 > 1
```

and immediately rejects the input.

This is correct because every permutation containing `2` must also contain `1`. Two copies of `2` would require two copies of `1`.

Now consider:

```
5
1 3 1 2 2
```

Frequencies:

```
cnt[1] = 2
cnt[2] = 2
cnt[3] = 1
```

Assignments:

```
1 -> [1,2]
2 -> [1,2]
3 -> [1]
```

Processing order:

| Value | Assigned permutation |
| --- | --- |
| 1 | 1 |
| 3 | 1 |
| 1 | 2 |
| 2 | 1 |
| 2 | 2 |

Permutation 1 becomes:

```
(1,2,3)
```

Permutation 2 becomes:

```
(1,2)
```

Even though the array order is shuffled, the construction still succeeds because assignments depend only on frequencies.

Finally, examine:

```
1
2
```

We get:

```
cnt[1] = 0
cnt[2] = 1
```

The monotonicity condition fails immediately:

```
1 > 0
```

No permutation can start at `2`, so the algorithm correctly outputs `-1`.
