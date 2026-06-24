---
title: "CF 105636A - \u7f16\u8f91\u5b57\u7b26\u4e32"
description: "We have two binary strings of equal length. Some positions are marked as movable and some are locked. A move consists of swapping two adjacent characters, but only characters that are allowed to participate in swaps may be moved."
date: "2026-06-25T06:10:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105636
codeforces_index: "A"
codeforces_contest_name: "NOIP 2024"
rating: 0
weight: 105636
solve_time_s: 62
verified: true
draft: false
---

[CF 105636A - \u7f16\u8f91\u5b57\u7b26\u4e32](https://codeforces.com/problemset/problem/105636/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two binary strings of equal length. Some positions are marked as movable and some are locked.

A move consists of swapping two adjacent characters, but only characters that are allowed to participate in swaps may be moved. Since swaps are adjacent and can be repeated arbitrarily many times, every maximal consecutive segment of positions marked `1` in the mask behaves like a freely permutable block. Characters cannot cross a locked position.

After performing any number of such swaps on either string, we want to maximize the number of positions where the two final strings contain the same character.

The length of each string can reach $10^5$, and there are multiple test cases. Any solution that repeatedly simulates swaps or tries different rearrangements is immediately ruled out. We need something close to linear time per test case. An $O(n^2)$ approach would require around $10^{10}$ operations in the worst case, which is far beyond the limit.

The main subtlety is that movable characters are not free globally. A character can only move inside its own maximal segment of movable positions. Two segments separated by a locked position are completely independent.

Consider a simple example:

```
s1 = 01
s2 = 10
t1 = 11
t2 = 00
```

The second string is fixed. The first string can rearrange its two characters. By moving the `1` to the first position we obtain two matches. Treating movable positions independently would miss this possibility.

Another easy mistake is allowing characters to cross a locked position:

```
s1 = 101
t1 = 101
```

The middle position is locked. The two movable positions belong to different segments, so the two `1`s cannot exchange places through the center.

## Approaches

The brute force idea is to explicitly generate all reachable arrangements of both strings and check the maximum number of equal positions. Inside a movable segment of length $k$, any permutation is reachable, so the number of states grows factorially. Even a segment of length 15 already has more than $10^{12}$ permutations. This approach is hopeless.

The key observation is that inside a movable segment, only the counts of `0` and `1` matter. The exact order is irrelevant because any order can be produced.

We first decompose each string into components.

A locked position forms a component of size one whose value is fixed forever.

A maximal consecutive run of positions with mask value `1` forms a movable component. Inside such a component we only need to know how many `0`s and how many `1`s are available.

Now think about a position where one side is fixed and the other side belongs to a movable component. If the movable component still contains the required digit, matching here is always beneficial. A match contributes exactly one to the answer, and using a character now cannot reduce the maximum possible future contribution because every character can contribute at most once.

So we greedily process all positions where at least one side is fixed. Whenever a movable component can supply the needed digit, we consume one occurrence and count a match.

After that, only positions where both sides are movable remain. At such a position, if the two corresponding components still both contain a `0`, we can match a `0` here. Otherwise, if both still contain a `1`, we can match a `1`. If neither digit exists on both sides, this position can never become equal.

The remaining counts in every component completely describe the unused characters, so greedily creating a match whenever possible is optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal Greedy with Components | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

### Step 1

Build component ids for both strings.

A locked position gets its own component.

A maximal consecutive run of movable positions shares one component id.

For every movable component, store how many `0`s and how many `1`s it currently contains.

### Step 2

Process every position.

If both positions are locked, their values are fixed forever. Add one to the answer if the digits are already equal.

If the first side is locked and the second side is movable, check whether the second component still contains the required digit. If it does, consume one occurrence and add one to the answer.

If the second side is locked and the first side is movable, do the symmetric operation.

The reason for doing this first is that fixed positions have only one possible value. If a movable component can satisfy that value, taking the match immediately never hurts.

### Step 3

Process every position again.

Only consider positions where both sides are movable.

Let the corresponding movable components be $A$ and $B$.

If both still contain a `0`, consume one `0` from each and add one to the answer.

Otherwise, if both still contain a `1`, consume one `1` from each and add one to the answer.

Otherwise no match is possible at this position.

### Step 4

Output the accumulated answer.

### Why it works

Every movable component is completely characterized by the remaining counts of `0` and `1`.

When a position involves a fixed character, any successful match must use one occurrence of that fixed digit from the movable side. Delaying that match provides no advantage because the consumed character can contribute at most one match anywhere.

After all fixed-position demands are satisfied as much as possible, every remaining position has two movable sides. A match at such a position only requires that both components still possess the same digit. If a common digit exists, taking that match immediately consumes one character from each side and increases the answer by one. No future arrangement can extract more than one contribution from those two consumed characters.

Thus every greedy match is locally optimal and never reduces the maximum achievable number of future matches. Repeating this process produces a globally optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())

    for _ in range(T):
        n = int(input())
        s1 = input().strip()
        s2 = input().strip()
        t1 = input().strip()
        t2 = input().strip()

        comp1 = [-1] * n
        comp2 = [-1] * n

        cnt1 = []
        cnt2 = []

        cid = 0
        i = 0
        while i < n:
            if t1[i] == '0':
                comp1[i] = -1
                i += 1
            else:
                cnt1.append([0, 0])
                j = i
                while j < n and t1[j] == '1':
                    comp1[j] = cid
                    cnt1[cid][int(s1[j])] += 1
                    j += 1
                cid += 1
                i = j

        cid = 0
        i = 0
        while i < n:
            if t2[i] == '0':
                comp2[i] = -1
                i += 1
            else:
                cnt2.append([0, 0])
                j = i
                while j < n and t2[j] == '1':
                    comp2[j] = cid
                    cnt2[cid][int(s2[j])] += 1
                    j += 1
                cid += 1
                i = j

        ans = 0

        for i in range(n):
            a_fixed = (t1[i] == '0')
            b_fixed = (t2[i] == '0')

            if a_fixed and b_fixed:
                if s1[i] == s2[i]:
                    ans += 1

            elif a_fixed and not b_fixed:
                need = int(s1[i])
                c = comp2[i]
                if cnt2[c][need] > 0:
                    cnt2[c][need] -= 1
                    ans += 1

            elif not a_fixed and b_fixed:
                need = int(s2[i])
                c = comp1[i]
                if cnt1[c][need] > 0:
                    cnt1[c][need] -= 1
                    ans += 1

        for i in range(n):
            if t1[i] == '1' and t2[i] == '1':
                c1 = comp1[i]
                c2 = comp2[i]

                if cnt1[c1][0] > 0 and cnt2[c2][0] > 0:
                    cnt1[c1][0] -= 1
                    cnt2[c2][0] -= 1
                    ans += 1
                elif cnt1[c1][1] > 0 and cnt2[c2][1] > 0:
                    cnt1[c1][1] -= 1
                    cnt2[c2][1] -= 1
                    ans += 1

        print(ans)

solve()
```

The first phase constructs movable components and records how many `0`s and `1`s each component contains.

The second phase handles every position involving at least one fixed character. These matches are the most constrained because the fixed side cannot change value.

The third phase handles positions where both sides are movable. At that point all remaining counts correspond to characters not already committed to fixed-position matches.

The implementation uses component ids to access the correct count array in constant time. Each position is visited only a few times, giving linear complexity.

## Worked Examples

### Example 1

```
n = 3
s1 = 010
s2 = 000
t1 = 111
t2 = 000
```

The first string has one movable component containing two `0`s and one `1`.

| Position | Fixed side value | Available in component | Match |
| --- | --- | --- | --- |
| 1 | 0 | yes | 1 |
| 2 | 0 | yes | 1 |
| 3 | 0 | yes | 1 |

Answer becomes 3.

This example shows why a movable segment should be treated as a pool of available digits rather than position by position.

### Example 2

```
n = 4
s1 = 0011
s2 = 1100
t1 = 1111
t2 = 1111
```

Both strings consist of a single movable component.

After building counts:

| Component | Zeros | Ones |
| --- | --- | --- |
| s1 | 2 | 2 |
| s2 | 2 | 2 |

Processing movable-movable positions:

| Position | Common digit used | Remaining s1 | Remaining s2 | Match |
| --- | --- | --- | --- | --- |
| 1 | 0 | (1,2) | (1,2) | 1 |
| 2 | 0 | (0,2) | (0,2) | 1 |
| 3 | 1 | (0,1) | (0,1) | 1 |
| 4 | 1 | (0,0) | (0,0) | 1 |

Final answer is 4.

This demonstrates that only digit counts matter inside a movable component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each position is processed a constant number of times |
| Space | O(n) | Component ids and count arrays |

The total work grows linearly with the string length. With $n \le 10^5$, this easily fits within typical competitive programming limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    input_data = io.StringIO(inp)
    output_data = io.StringIO()

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = input_data
    sys.stdout = output_data

    try:
        import sys
        input = sys.stdin.readline

        T = int(input())
        for _ in range(T):
            n = int(input())
            s1 = input().strip()
            s2 = input().strip()
            t1 = input().strip()
            t2 = input().strip()

            comp1 = [-1] * n
            comp2 = [-1] * n
            cnt1 = []
            cnt2 = []

            cid = 0
            i = 0
            while i < n:
                if t1[i] == '0':
                    i += 1
                else:
                    cnt1.append([0, 0])
                    j = i
                    while j < n and t1[j] == '1':
                        comp1[j] = cid
                        cnt1[cid][int(s1[j])] += 1
                        j += 1
                    cid += 1
                    i = j

            cid = 0
            i = 0
            while i < n:
                if t2[i] == '0':
                    i += 1
                else:
                    cnt2.append([0, 0])
                    j = i
                    while j < n and t2[j] == '1':
                        comp2[j] = cid
                        cnt2[cid][int(s2[j])] += 1
                        j += 1
                    cid += 1
                    i = j

            ans = 0

            for i in range(n):
                a_fixed = t1[i] == '0'
                b_fixed = t2[i] == '0'

                if a_fixed and b_fixed:
                    ans += (s1[i] == s2[i])
                elif a_fixed:
                    d = int(s1[i])
                    c = comp2[i]
                    if cnt2[c][d]:
                        cnt2[c][d] -= 1
                        ans += 1
                elif b_fixed:
                    d = int(s2[i])
                    c = comp1[i]
                    if cnt1[c][d]:
                        cnt1[c][d] -= 1
                        ans += 1

            for i in range(n):
                if t1[i] == '1' and t2[i] == '1':
                    c1 = comp1[i]
                    c2 = comp2[i]
                    if cnt1[c1][0] and cnt2[c2][0]:
                        cnt1[c1][0] -= 1
                        cnt2[c2][0] -= 1
                        ans += 1
                    elif cnt1[c1][1] and cnt2[c2][1]:
                        cnt1[c1][1] -= 1
                        cnt2[c2][1] -= 1
                        ans += 1

            print(ans)

    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    return output_data.getvalue()

# provided sample
assert run(
"""1
6
011101
111010
111010
101101
"""
) == "4\n"

# minimum size
assert run(
"""1
1
0
0
0
0
"""
) == "1\n"

# all movable
assert run(
"""1
4
0011
1100
1111
1111
"""
) == "4\n"

# all fixed
assert run(
"""1
4
0101
0011
0000
0000
"""
) == "2\n"

# locked barrier separates segments
assert run(
"""1
3
101
111
101
111
"""
) == "2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single equal fixed character | 1 | Minimum size |
| All positions movable | 4 | Full rearrangement inside components |
| All positions fixed | 2 | No movement allowed |
| Barrier in the middle | 2 | Characters cannot cross locked positions |

## Edge Cases

Consider:

```
1
3
101
111
101
111
```

The middle position of the first string is locked. The two movable positions belong to different components.

The first component contains one `1`, the second component also contains one `1`. They cannot merge into a single pool. The algorithm assigns separate component ids and maintains separate counts, so no illegal cross-barrier movement is ever used.

Now consider:

```
1
2
01
10
11
00
```

The second string is fully fixed. The movable component of the first string contains one `0` and one `1`.

At position 1 the fixed value is `1`, so the algorithm consumes the available `1`.

At position 2 the fixed value is `0`, so the algorithm consumes the available `0`.

Both positions match and the answer is 2. Treating positions independently would miss this rearrangement.

Finally, consider:

```
1
4
0000
1111
1111
1111
```

Every position is movable on both sides, but the components contain only opposite digits. No common digit is available at any step, so the algorithm correctly returns 0.
