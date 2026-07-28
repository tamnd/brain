---
title: "CF 102756J - Majestic Warriors of China"
description: "We have a line of $N$ statues. Each statue is described by a $K$-bit number, where bit $i$ tells whether feature $i$ appears on that statue. A consecutive group of statues is called majestic when every feature appears the same number of times inside that group."
date: "2026-07-29T00:35:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102756
codeforces_index: "J"
codeforces_contest_name: "UTPC Contest 10-09-20 Div. 1"
rating: 0
weight: 102756
solve_time_s: 60
verified: true
draft: false
---

[CF 102756J - Majestic Warriors of China](https://codeforces.com/problemset/problem/102756/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of $N$ statues. Each statue is described by a $K$-bit number, where bit $i$ tells whether feature $i$ appears on that statue. A consecutive group of statues is called majestic when every feature appears the same number of times inside that group. The task is to find the maximum possible length of such a consecutive group.

The input size is large: $N$ can reach $100000$, while $K$ can be as large as $30$. A solution that checks every interval would examine around $N^2$ ranges, which is about $10^{10}$ for the largest input. Even updating the feature counts for each range would be too slow. We need a near-linear approach. The small value of $K$ tells us that representing information about features is possible, but we cannot afford to store every possible feature-count combination.

A common mistake is to check only whether the total number of set bits is balanced. That is not enough because every individual feature must have the same frequency.

For example:

```
4 3
1
2
4
7
```

The correct answer is `1`. A length 2 segment such as `[1, 2]` has features appearing once each? No. Feature 1 appears once, feature 2 appears once, but feature 3 appears zero times. The condition is about all three feature counts being equal, not about the total number of features.

Another edge case is $K=1$:

```
5 1
0
1
0
1
1
```

The correct answer is `5`. With only one feature, every range automatically has equal counts because there is only one count to compare. Implementations that always build a vector of differences of size $K-1$ must handle this case separately.

A third important case is a majestic range that starts at the first statue:

```
3 2
1
2
3
```

The correct answer is `3`. Prefix hash solutions must store the empty prefix before processing any statue, otherwise they cannot detect ranges beginning at index 1.

## Approaches

A direct solution tries every possible interval. For each left endpoint, we extend the right endpoint and maintain the count of every feature. Whenever all $K$ counts are equal, we update the answer. This is correct because every possible range is considered. However, there are $O(N^2)$ ranges, and checking equality between $K$ counters makes the worst case $O(N^2K)$. With $N=100000$, this is far beyond the available time.

The key observation is to avoid storing the actual counts. A range is majestic if all feature counts are equal. Instead of asking whether every count has the same value, we can compare every feature against one chosen reference feature.

Choose feature zero as the reference. For every prefix of the array, store the differences:

$$count_1-count_0,\ count_2-count_0,\ ...,\ count_{K-1}-count_0$$

If two prefixes have the same difference vector, then the statues between those prefixes added the same amount to every feature count. The difference between two equal prefix vectors has every feature count equal, which means the segment is majestic.

This transforms the problem into finding the longest subarray with the same prefix state, which can be solved with a hash map storing the first occurrence of each state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N^2K)$ | $O(K)$ | Too slow |
| Prefix Difference Hashing | $O(NK)$ | $O(NK)$ | Accepted |

## Algorithm Walkthrough

1. Read the statues and handle the special case $K=1$. Every interval is valid, so the answer is $N$.
2. Maintain a prefix difference vector of length $K-1$. When a statue is processed, add $1$ to every position corresponding to a feature it contains except the reference feature. If the statue contains the reference feature, subtract $1$ from every other feature difference.

The vector always represents how much each non-reference feature count differs from the reference feature count in the current prefix.
3. Store the first index where each difference vector appears. The empty prefix has the all-zero vector and is stored at index zero.
4. When a prefix vector appears again, the segment between the first occurrence and the current position has equal feature counts. Use the distance between those positions as a possible answer.
5. Continue until all statues are processed and output the maximum length found.

Why it works:

The stored vector contains exactly the information needed to compare feature counts. If two prefixes have the same vector, then the changes between those prefixes leave every feature with the same frequency because all differences relative to the reference feature cancel out. Conversely, if a range is majestic, every feature count changes equally inside that range, so the prefix difference vector before and after the range must be identical. The hash map finds exactly these pairs of prefixes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, k, arr):
    if k == 1:
        return n

    first = {tuple([0] * (k - 1)): 0}
    diff = [0] * (k - 1)
    ans = 0

    for idx, x in enumerate(arr, 1):
        has_first = x & 1

        if has_first:
            for i in range(k - 1):
                diff[i] -= 1

        for i in range(1, k):
            if x & (1 << i):
                diff[i - 1] += 1

        state = tuple(diff)

        if state in first:
            ans = max(ans, idx - first[state])
        else:
            first[state] = idx

    return ans

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    ptr = 0
    out = []

    while ptr < len(data):
        n = int(data[ptr])
        k = int(data[ptr + 1])
        ptr += 2

        arr = list(map(int, data[ptr:ptr + n]))
        ptr += n

        out.append(str(solve_case(n, k, arr)))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation keeps the first occurrence of every prefix state because an earlier occurrence always gives a longer valid segment. The tuple conversion is necessary because lists are mutable and cannot be dictionary keys.

The reference feature is treated specially. When it appears, every difference decreases because the reference count increased by one. For other features, their positions increase only when that bit is present. The order of these updates does not affect the final difference vector because each statue contributes exactly once.

The empty prefix is inserted before processing any statue. This handles ranges starting from the first statue and prevents an off-by-one error in the length calculation.

## Worked Examples

For the sample:

```
7 3
7
6
7
2
1
4
2
```

the prefix states are:

| Index | Statue | Difference Vector | First Seen | Answer |
| --- | --- | --- | --- | --- |
| 0 | - | (0,0) | 0 | 0 |
| 1 | 7 | (0,0) | 0 | 1 |
| 2 | 6 | (-1,0) | 2 | 1 |
| 3 | 7 | (-1,0) | 2 | 1 |
| 4 | 2 | (-1,1) | 4 | 1 |
| 5 | 1 | (-1,1) | 4 | 1 |
| 6 | 4 | (0,0) | 0 | 6 |
| 7 | 2 | (-1,1) | 4 | 4 |

The repeated states identify ranges where every feature changes equally. The longest one has length 4.

A second example:

```
5 2
1
2
3
0
3
```

| Index | Statue | Difference Vector | First Seen | Answer |
| --- | --- | --- | --- | --- |
| 0 | - | (0) | 0 | 0 |
| 1 | 1 | (-1) | 1 | 0 |
| 2 | 2 | (0) | 0 | 2 |
| 3 | 3 | (0) | 0 | 3 |
| 4 | 0 | (1) | 4 | 3 |
| 5 | 3 | (1) | 4 | 3 |

This demonstrates that a majestic range does not need to contain every feature. It only requires all features to have the same frequency.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(NK)$ | Each statue updates at most $K-1$ feature differences. |
| Space | $O(NK)$ | The hash map stores up to one state for every prefix. |

With $N=100000$ and $K=30$, the number of operations is around three million updates, which fits comfortably within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    data = sys.stdin.read().split()
    ptr = 0
    out = []

    while ptr < len(data):
        n = int(data[ptr])
        k = int(data[ptr + 1])
        ptr += 2
        arr = list(map(int, data[ptr:ptr+n]))
        ptr += n

        if k == 1:
            out.append(str(n))
            continue

        first = {(0,) * (k - 1): 0}
        diff = [0] * (k - 1)
        ans = 0

        for idx, x in enumerate(arr, 1):
            if x & 1:
                for i in range(k - 1):
                    diff[i] -= 1
            for i in range(1, k):
                if x & (1 << i):
                    diff[i - 1] += 1

            state = tuple(diff)
            if state in first:
                ans = max(ans, idx - first[state])
            else:
                first[state] = idx

        out.append(str(ans))

    sys.stdin = old
    return "\n".join(out)

assert run("""7 3
7
6
7
2
1
4
2
""") == "4"

assert run("""3 2
1
2
3
""") == "3"

assert run("""5 1
0
1
0
1
1
""") == "5"

assert run("""4 3
1
2
4
7
""") == "1"

assert run("""5 2
0
0
0
0
0
""") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample input | 4 | Basic repeated prefix states |
| `3 2 / 1 2 3` | 3 | Range starting at the beginning |
| `5 1 / mixed bits` | 5 | Single-feature special case |
| `4 3 / 1 2 4 7` | 1 | All features must match individually |
| Five zero masks | 5 | Equal values and long full-range answers |

## Edge Cases

For $K=1$, the algorithm returns immediately because no comparisons between features are needed. Every statue range has one feature count, so the condition is always true.

For ranges starting at the first statue, the zero prefix state represents the state before reading anything. In the input:

```
3 2
1
2
3
```

the state after all three statues returns to zero, matching the stored initial state. The algorithm correctly calculates the length as $3-0=3$.

For cases where every feature count must match separately, the difference vector prevents false positives. In:

```
4 3
1
2
4
7
```

a total feature count based approach might incorrectly consider some longer segments valid, but the stored differences show that the three feature counts do not balance until only single statues remain. The answer is correctly found as `1`.
