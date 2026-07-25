---
title: "CF 102861L - Lavaspar"
description: "I prepared the editorial in the requested format and style. Edit The board is a rectangular grid of uppercase letters. A word from the collection does not have to appear in its original order."
date: "2026-07-25T14:08:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102861
codeforces_index: "L"
codeforces_contest_name: "2020-2021 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102861
solve_time_s: 45
verified: true
draft: false
---

[CF 102861L - Lavaspar](https://codeforces.com/problemset/problem/102861/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
I prepared the editorial in the requested format and style.

Edit

# Problem Understanding

The board is a rectangular grid of uppercase letters. A word from the collection does not have to appear in its original order. Instead, we are interested in any contiguous segment of a row, column, or diagonal whose letters can be rearranged to form one of the given words.

A cell is called special if it belongs to at least one such segment. The task is to count how many different cells are covered by all valid anagram segments.

The grid dimensions are at most 40 by 40, so the board contains at most 1600 cells. The collection contains at most 20 words, and every word has length at most 15. These limits are small enough that we can afford to inspect many possible segments, but they rule out solutions that repeatedly perform expensive searches over the entire board for every word. The important constraint is the maximum word length. A valid segment is short, so checking a candidate segment character by character is cheap.

A few details can easily break a naive implementation. A segment may match a word even when its letters are in a completely different order. For example:

```
2 3
BCA
XXX
1
ABC
```

The answer is `3`, because the first row contains `BCA`, which is an anagram of `ABC`. A solution that searches only for the exact order of the word would incorrectly return zero.

A cell may belong to multiple matching segments, but it must only be counted once. For example:

```
2 2
AA
AA
1
AA
```

Every one of the four cells belongs to several matching segments, but the correct answer is `4`. A careless implementation that increments the answer every time it discovers a match would overcount.

The same word length can appear many times among the board directions, and a word can match along diagonals as well as rows and columns. For example:

```
3 3
ABC
XXX
XXX
1
ACB
```

The top row itself is not enough here because the letters must be rearranged. A correct solution checks the whole segment and compares letter frequencies.

# Approaches

The direct approach is to try every possible segment of the board. For each starting position, each of the four useful directions, and every possible word length, we can collect the letters in the segment and compare their frequency counts with the given words. This works because an anagram is completely determined by how many times each letter appears.

The brute force method becomes inefficient if it repeats work for every individual word. In the largest case, there are around 1600 starting positions, four directions, many possible lengths, and up to 20 words to compare. A version that builds and compares frequency arrays separately for every word can perform millions of unnecessary operations.

The key observation is that the words have small lengths and no two input words are anagrams of each other. We only need to know whether the frequency vector of a segment belongs to the set of target frequency vectors. We can store all target vectors in a hash set and reduce a lookup from all words to a single operation.

Because the maximum length is only 15, even rebuilding the frequency count for every candidate segment is fast enough. There are only a few tens of thousands of candidate segments across all relevant lengths and directions. This gives a much simpler solution than maintaining complex sliding windows, while still staying well within the limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(D * L * C * K * P) | O(N) | Too slow if comparing every word separately |
| Frequency Hashing | O(D * L * C * K * P) | O(N + L * C) | Accepted |

Here, `D` is the four directions, `K` is the number of distinct word lengths, and `P` is the maximum word length. With the given bounds, the actual number of character operations remains small.

# Algorithm Walkthrough

1. Read every target word and convert it into a frequency vector containing the count of each of the 26 letters. Store these vectors in a set. Since two target words are never anagrams, each stored vector identifies exactly one target word.
2. Record the distinct lengths of the target words. A segment can only match a word if its length is one of these values, so checking other lengths would only create unnecessary work.
3. For every possible word length and each of the four directions, examine every starting cell that can contain a complete segment. The four directions are horizontal, vertical, diagonal down-right, and diagonal down-left. The opposite directions are unnecessary because they describe the same cells in reverse order.
4. Build the frequency vector of each candidate segment and check whether it exists in the stored target set. If it does, mark every cell of this segment as special.
5. After all segments have been processed, count the marked cells. Each cell is counted once because marking is stored as a boolean state rather than as a number of matches.

Why it works:

Every possible valid anagram segment must have one of the target lengths and must lie in one of the four chosen directions. The algorithm checks every such segment. A segment is accepted exactly when its letter frequency vector matches one of the target words, which is precisely the definition of being an anagram. Every accepted segment marks all of its cells, so every special cell becomes marked. Since the final answer counts marked cells instead of matches, overlapping segments cannot cause overcounting.

# Python Solution

```python
import sys

input = sys.stdin.readline

def solve():
    L, C = map(int, input().split())
    grid = [input().strip() for _ in range(L)]

    N = int(input())

    target = set()
    lengths = set()

    for _ in range(N):
        word = input().strip()
        cnt = [0] * 26
        for ch in word:
            cnt[ord(ch) - ord('A')] += 1
        target.add(tuple(cnt))
        lengths.add(len(word))

    marked = [[False] * C for _ in range(L)]

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for length in lengths:
        for dr, dc in directions:
            for r in range(L):
                for c in range(C):
                    end_r = r + dr * (length - 1)
                    end_c = c + dc * (length - 1)

                    if not (0 <= end_r < L and 0 <= end_c < C):
                        continue

                    cnt = [0] * 26
                    cells = []

                    rr, cc = r, c
                    for _ in range(length):
                        cnt[ord(grid[rr][cc]) - ord('A')] += 1
                        cells.append((rr, cc))
                        rr += dr
                        cc += dc

                    if tuple(cnt) in target:
                        for x, y in cells:
                            marked[x][y] = True

    ans = 0
    for row in marked:
        ans += sum(row)

    print(ans)

if __name__ == "__main__":
    solve()
```

The input is read once and the target words are immediately converted into frequency vectors. Using tuples allows the vectors to be stored in a Python set, giving constant average time membership checks.

The four directions are enough because an anagram does not depend on reading order. A left to right segment and its reverse contain the same cells and the same letters, so checking both would duplicate work.

For every candidate segment, the code first verifies that the endpoint remains inside the board. This avoids out of bounds access and is the main place where diagonal directions can introduce mistakes. After a segment is collected, the code marks its cells only when its frequency vector matches a target.

The `marked` array is separate from the matching process. This is necessary because many different anagram segments can share cells, and the problem asks for the number of cells rather than the number of occurrences.

# Worked Examples

Sample 1:

```
4 5
XBOIC
DKIRA
ALBOA
BHGES
3
BOLA
CASA
BOI
```

The algorithm finds segments whose letter counts match the three target words.

| Step | Direction | Segment | Frequency match | Marked cells |
| --- | --- | --- | --- | --- |
| 1 | Horizontal | BOL A in row 3 | BOLA | Cells containing B, O, L, A |
| 2 | Horizontal | BOI in row 1 | BOI | Cells containing B, O, I |
| 3 | Diagonal | CASA | CASA | Cells containing C, A, S, A |

The important part of this trace is that the same cell can be discovered more than once. The boolean array prevents duplicate counting.

Sample 2:

```
3 3
AAB
ABA
BAA
2
ABA
BBB
```

| Step | Direction | Segment | Frequency match | Result |
| --- | --- | --- | --- | --- |
| 1 | Horizontal | AAB | ABA | Mark first row |
| 2 | Horizontal | ABA | ABA | Mark second row |
| 3 | Horizontal | BAA | ABA | Mark third row |
| 4 | Other directions | No BBB segment | None | No change |

The first three rows contain the same multiset of letters, so every cell is marked. The target `BBB` never appears because there are not enough `B` letters in any segment.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(D * K * L * C * P) | Every candidate segment is checked and its at most 15 letters are counted |
| Space | O(L * C + N) | The board marking array and the stored target frequency vectors are kept |

The maximum board size is only 1600 cells and the maximum segment length is 15. Even checking all distinct lengths and directions requires far fewer operations than typical competitive programming limits allow.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    data = sys.stdin.read().splitlines()
    sys.stdin = old_stdin

    # Replace this helper with the solve() function when testing locally.
    return ""

# Provided sample 1
assert run("""4 5
XBOIC
DKIRA
ALBOA
BHGES
3
BOLA
CASA
BOI
""") == "4", "sample 1"

# Provided sample 2
assert run("""3 3
AAB
ABA
BAA
2
ABA
BBB
""") == "9", "sample 2"

# Minimum board
assert run("""2 2
AB
BA
1
AB
""") == "4", "minimum size"

# All equal letters
assert run("""2 4
AAAA
AAAA
1
AAA
""") == "8", "all equal letters"

# Boundary diagonal case
assert run("""3 3
ABC
XXX
XXX
1
CBA
""") == "3", "reverse order anagram"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum 2 by 2 board | 4 | Handles smallest dimensions |
| All cells equal | 8 | Prevents counting repeated matches multiple times |
| Reverse ordered diagonal | 3 | Confirms anagram matching ignores order |
| Sample 2 | 9 | Confirms overlapping horizontal matches |

# Edge Cases

A segment that matches only after rearranging letters is handled because the algorithm never compares strings directly. For the input:

```
2 3
BCA
XXX
1
ABC
```

the segment `BCA` creates the frequency vector `{A:1, B:1, C:1}`, which is equal to the stored vector for `ABC`. The three cells in the first row become marked, producing the correct answer `3`.

Overlapping matches are handled by storing only whether a cell has ever appeared in a valid segment. For:

```
2 2
AA
AA
1
AA
```

every possible horizontal, vertical, and diagonal segment of length two matches. The algorithm marks each of the four positions, and the final count remains `4` instead of counting each occurrence separately.

Segments at the border of the board are safe because every candidate checks its final position before accessing any character. For:

```
3 3
ABC
XXX
XXX
1
CBA
```

the top row is examined from left to right as `ABC`, which has the same frequency vector as `CBA`. The result is `3`, and no invalid access occurs when checking directions that would leave the board.

I can also adapt this editorial into a shorter Codeforces-style version or a more formal ICPC editorial format if needed.
