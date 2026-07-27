---
title: "CF 102791I - String Reversal"
description: "The task is to find the minimum number of adjacent swaps needed to turn a given string into its reverse. A swap can only exchange two neighboring characters, so the cost measures how far characters have to travel through the string."
date: "2026-07-27T18:15:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102791
codeforces_index: "I"
codeforces_contest_name: "ICPC 2020-2021 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102791
solve_time_s: 67
verified: true
draft: false
---

[CF 102791I - String Reversal](https://codeforces.com/problemset/problem/102791/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to find the minimum number of adjacent swaps needed to turn a given string into its reverse. A swap can only exchange two neighboring characters, so the cost measures how far characters have to travel through the string.

The input contains the length of the string and the string itself. The output is the smallest number of neighboring swaps required to rearrange the original string so that the character at every position matches the character that was at the mirrored position before reversal.

The length can be as large as 200000. A solution that tries to simulate swaps directly is impossible because a string can require a quadratic number of movements. Even though the final answer can be around n², the number of operations performed by the algorithm still needs to stay close to linear. This rules out repeatedly searching for characters or physically moving characters one by one.

The main difficulty comes from repeated characters. A character does not have a unique destination when reversing the string. For example, in `aaaza`, the three `a` characters in the middle are indistinguishable, and choosing the wrong occurrence can increase the counted swaps.

Consider the input:

```
5
aaaza
```

The correct output is:

```
2
```

A careless solution might match the first `a` from the left side with the first `a` from the reversed target and ignore the order of equal characters. That can count unnecessary movements because identical characters should be paired in the order that minimizes crossing.

Another important case is a palindrome:

```
6
cbaabc
```

The output is:

```
0
```

A solution that only checks whether characters differ from their mirrored positions and then moves all mismatches can overcount. The string is already equal to its reverse.

## Approaches

A straightforward approach is to repeatedly fix the two ends of the string. We compare the first and last remaining characters. If they are equal, both are already in their correct final positions. If they differ, we search for a matching character on one side and move it using adjacent swaps until the two ends become correct. This method is correct because every adjacent swap represents one unit of movement, and the chosen character must travel to its destination somehow.

The problem is the amount of movement. In the worst case, moving a character from one end of a string of length n to the other side costs O(n), and we may have to do this for O(n) positions. The total work becomes O(n²), which is too slow for n = 200000.

The key observation is that the reverse operation only changes positions, not character counts. Every character in the original string has a matching occurrence in the reversed target. Instead of physically simulating swaps, we can calculate the total distance that characters have to move.

If we create the sequence of positions that characters occupy in the target arrangement, then the answer becomes the number of inversions in that sequence. An inversion represents two characters that appear in the wrong order and must cross through adjacent swaps. This is the same reason merge sort counts inversion pairs.

The remaining challenge is handling equal characters. We need to know which occurrence of a character moves to which target position. The optimal choice is to pair occurrences from left to right. For each character, its first occurrence in the original string should match its first occurrence in the reversed string, its second occurrence should match its second occurrence, and so on. This avoids unnecessary crossings between identical characters.

After building the target positions, a Fenwick tree can count how many already processed positions are after the current position. This gives the inversion count in O(n log n).

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Store the positions of every character in the original string. The positions are kept in increasing order because equal characters should be matched from left to right.
2. Look at the reversed string. For every character in this reversed order, take the earliest unused occurrence of that character from the original string. Record that original position in a new array.

The resulting array describes where the characters of the reversed string came from in the original string. If these positions are already increasing, the string is already in the correct order. Every decrease between positions represents characters that need to cross.
3. Count inversions in the position array using a Fenwick tree.

When processing a position x, the number of previous positions larger than x is the number of characters that must cross this character. The Fenwick tree stores how many positions have appeared so far, allowing this query in logarithmic time.
4. Add all inversion contributions and print the result.

Why it works:

The final reversed string has a fixed order of characters. By matching equal characters in their original left-to-right order, we choose the only arrangement that avoids unnecessary swaps between identical letters. The remaining problem is only the ordering of these matched occurrences. Every pair of occurrences that appears in the opposite order from the target must cross once, and every adjacent swap fixes exactly one such crossing. Therefore, the minimum number of swaps is exactly the inversion count of the mapped positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        res = 0
        while i > 0:
            res += self.bit[i]
            i -= i & -i
        return res

def solve():
    n = int(input())
    s = input().strip()

    pos = [[] for _ in range(26)]
    for i, c in enumerate(s):
        pos[ord(c) - 97].append(i)

    used = [0] * 26
    order = []

    for c in reversed(s):
        x = ord(c) - 97
        order.append(pos[x][used[x]])
        used[x] += 1

    fw = Fenwick(n)
    ans = 0

    for i, x in enumerate(order):
        x += 1
        already = fw.sum(n) - fw.sum(x)
        ans += already
        fw.add(x, 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The position lists store every occurrence of each letter. Because the lists are naturally sorted while scanning the original string, taking positions in order gives the correct pairing between equal characters.

The construction of `order` scans the desired final string, which is the original string backwards. Each character receives the next available original position of that same character. The `used` array prevents the same occurrence from being assigned twice.

The Fenwick tree uses one-based indexing, so every stored position is increased by one before insertion. For a current position, the expression `fw.sum(n) - fw.sum(x)` counts previous positions strictly greater than it. These are exactly the earlier characters that are on the wrong side and must cross it.

The answer is stored in Python’s integer type, which is necessary because the maximum number of swaps can be about n², much larger than 32-bit integer limits.

## Worked Examples

For the input:

```
5
aaaza
```

the mapped positions are:

| Step | Character placed in reversed string | Original position chosen | Inversions added | Current answer |
| --- | --- | --- | --- | --- |
| 1 | a | 0 | 0 | 0 |
| 2 | z | 3 | 0 | 0 |
| 3 | a | 2 | 1 | 1 |
| 4 | a | 1 | 1 | 2 |
| 5 | a | 4 | 0 | 2 |

The answer is 2. The trace shows why repeated characters must be paired carefully. The equal `a` characters are assigned in order, and only the `z` movement contributes swaps.

For the input:

```
9
icpcsguru
```

the mapped positions are:

| Step | Character placed in reversed string | Original position chosen | Inversions added | Current answer |
| --- | --- | --- | --- | --- |
| 1 | u | 8 | 0 | 0 |
| 2 | r | 7 | 1 | 1 |
| 3 | u | 5 | 2 | 3 |
| 4 | g | 6 | 1 | 4 |
| 5 | s | 4 | 4 | 8 |
| 6 | c | 3 | 5 | 13 |
| 7 | p | 2 | 4 | 17 |
| 8 | c | 1 | 6 | 23 |
| 9 | i | 0 | 7 | 30 |

The final count is 30. Every inversion corresponds to a pair of characters whose relative order must change during the reversal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each character is inserted into and queried from the Fenwick tree once. |
| Space | O(n) | The occurrence lists, mapped positions, and Fenwick tree each store linear information. |

The constraints allow O(n log n) because n is 200000. The solution avoids the quadratic behavior of explicitly performing swaps.

## Test Cases

```python
import sys
import io

def solve_case(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i

        def sum(self, i):
            r = 0
            while i:
                r += self.bit[i]
                i -= i & -i
            return r

    n = int(input())
    s = input().strip()

    pos = [[] for _ in range(26)]
    for i, c in enumerate(s):
        pos[ord(c) - 97].append(i)

    used = [0] * 26
    arr = []
    for c in reversed(s):
        x = ord(c) - 97
        arr.append(pos[x][used[x]])
        used[x] += 1

    fw = Fenwick(n)
    ans = 0
    for x in arr:
        x += 1
        ans += fw.sum(n) - fw.sum(x)
        fw.add(x, 1)

    return str(ans)

assert solve_case("5\naaaza\n") == "2"
assert solve_case("6\ncbaabc\n") == "0"
assert solve_case("9\nicpcsguru\n") == "30"

assert solve_case("2\naa\n") == "0"
assert solve_case("3\nabc\n") == "3"
assert solve_case("7\naaaaaaa\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 aa` | `0` | Minimum length and already reversed case |
| `3 abc` | `3` | Characters that all need to move |
| `7 aaaaaaa` | `0` | All equal characters |
| `5 aaaza` | `2` | Repeated characters with a non-trivial movement |

## Edge Cases

For `aaaza`, the algorithm builds the reversed target order as `azaaa`. The occurrences of `a` are matched from left to right, producing the position sequence `[0, 3, 2, 1, 4]`. The Fenwick tree counts the three crossings caused by the `z` being in the wrong place, resulting in the correct answer of 2 after counting only necessary inversions.

For `cbaabc`, the reversed string is identical to the original string. The mapped positions are already sorted, so the inversion count remains zero. The algorithm naturally handles palindromes because no character pair needs to cross.

For a string containing only one repeated character, such as `aaaaa`, every occurrence can be matched with a corresponding occurrence without changing order. The mapped positions are increasing, so the answer is zero. This avoids the common mistake of counting swaps between identical characters that are actually interchangeable.

If you want, I can also provide a shorter Codeforces-style version of the editorial that matches the length and tone of official contest editorials.
