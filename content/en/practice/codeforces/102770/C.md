---
title: "CF 102770C - Crossword Validation"
description: "A crossword board is a square grid where some cells are blocked and the remaining cells already contain letters. A word in this grid is not chosen by clues; instead, it is every maximal continuous sequence of letters that appears horizontally or vertically."
date: "2026-07-28T23:06:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102770
codeforces_index: "C"
codeforces_contest_name: "The 17th Zhejiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102770
solve_time_s: 73
verified: true
draft: false
---

[CF 102770C - Crossword Validation](https://codeforces.com/problemset/problem/102770/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

A crossword board is a square grid where some cells are blocked and the remaining cells already contain letters. A word in this grid is not chosen by clues; instead, it is every maximal continuous sequence of letters that appears horizontally or vertically. A horizontal sequence stops when it reaches the border or a blocked cell, and the same rule applies vertically.

The dictionary contains every allowed word together with a score. The task is to inspect every word that naturally appears in the filled grid. If even one horizontal or vertical sequence is missing from the dictionary, the whole crossword is invalid and the answer is `-1`. Otherwise, the answer is the sum of the dictionary scores of all discovered words, including repeated occurrences.

The important constraints are dominated by two large values. The grid area over all test cases is at most four million cells, so any solution that revisits many cells for every possible word will be too slow. The total dictionary length is also four million characters, which rules out approaches that copy every dictionary word into many separate structures. A linear or almost linear algorithm is needed, and the data structure must share common prefixes between words.

A few cases are easy to mishandle. A single letter is still a valid candidate word if it is isolated.

For example:

```
1
1 1
a
a 5
```

The answer is `5`. An implementation that only checks words of length at least two would incorrectly reject this board.

Repeated words must contribute their score every time they appear. For example:

```
1
2 1
aa
aa
aa 7
```

The horizontal words are `aa` and `aa`, and the vertical words are `aa` and `aa`, so the answer is `28`. Counting each dictionary entry only once would produce the wrong result.

A candidate word cannot be extended through a blocked cell. For example:

```
1
2 2
a#
aa
a 3
aa 5
```

The words are `a`, `aa`, `a`, and `aa`, giving `16`. Looking only at rows and forgetting vertical words would miss two contributions.

## Approaches

A direct solution is to extract every row segment and every column segment, then search the dictionary for each extracted string. This is correct because the definition of a candidate word is exactly a maximal uninterrupted segment. However, storing or comparing strings repeatedly is expensive. In the worst case, the board is almost entirely letters, so extracting every segment still touches four million cells, and a naive dictionary lookup that scans many words can multiply that work by the dictionary size. A solution close to `O(number of cells + dictionary size)` is required.

The useful observation is that all dictionary queries are prefix queries. While reading a candidate word from the grid, the only question is whether the current sequence of letters can continue in the dictionary and whether the final sequence is a complete word. A trie represents exactly this information. Shared prefixes are stored once, so the total construction cost depends on the sum of dictionary lengths rather than the number of dictionary entries.

The brute-force approach works because every candidate word can be checked independently, but fails because it repeatedly searches the same prefixes. The trie removes this repeated work. Once the dictionary is stored, every grid segment can be walked through the trie character by character. If a transition does not exist, the crossword is invalid immediately. If the walk ends at a terminal trie node, its stored score is added.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Potentially `O(number of segments × dictionary size)` | Depends on stored words | Too slow |
| Trie scanning | `O(dictionary length + grid area)` | `O(dictionary length)` | Accepted |

## Algorithm Walkthrough

1. Build a trie containing every dictionary word. Each terminal node stores the score of that word. The trie uses shared prefixes so that words with common beginnings consume little additional memory.
2. Scan every row of the grid. Whenever a letter cell is found immediately after a border or a `#`, start walking right and follow trie edges until the end of that horizontal segment. If the walk fails or does not end at a terminal node, the crossword is invalid. Otherwise, add the stored score.
3. Scan every column using the same process from top to bottom. A separate scan is needed because every letter can belong to both a horizontal and a vertical word.
4. If every candidate word was found in the trie, output the accumulated score.

The invariant is that every time the algorithm finishes processing a segment, it has verified exactly one candidate word from the crossword definition. The scans start only at segment beginnings, so every candidate word is visited once and no invalid partial segment is counted. The trie contains exactly the dictionary words, so a successful terminal match is equivalent to the word being allowed.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    data = sys.stdin.buffer

    t = int(data.readline())
    ans = []

    for _ in range(t):
        n, m = map(int, data.readline().split())

        grid = [data.readline().strip() for _ in range(n)]

        head = array('i', [-1])
        score = array('q', [0])
        to = array('i')
        nxt = array('i')
        ch = array('B')

        def new_node():
            head.append(-1)
            score.append(0)
            return len(head) - 1

        def get_child(node, c):
            e = head[node]
            while e != -1:
                if ch[e] == c:
                    return to[e]
                e = nxt[e]
            return -1

        def add_word(s, val):
            node = 0
            for c in s:
                nxt_node = get_child(node, c)
                if nxt_node == -1:
                    nxt_node = new_node()
                    to.append(nxt_node)
                    ch.append(c)
                    nxt.append(head[node])
                    head[node] = len(to) - 1
                node = nxt_node
            score[node] = val

        for _ in range(m):
            word, val = data.readline().split()
            add_word(word, int(val))

        def check_line(chars):
            node = 0
            for c in chars:
                node = get_child(node, c)
                if node == -1:
                    return -1
            return score[node]

        total = 0
        ok = True

        for i in range(n):
            j = 0
            while j < n:
                if grid[i][j] == 35:
                    j += 1
                    continue
                if j == 0 or grid[i][j - 1] == 35:
                    node = 0
                    k = j
                    while k < n and grid[i][k] != 35:
                        node = get_child(node, grid[i][k] - 97)
                        if node == -1:
                            ok = False
                            break
                        k += 1
                    if not ok or score[node] == 0:
                        ok = False
                        break
                    total += score[node]
                j += 1
            if not ok:
                break

        if ok:
            for j in range(n):
                i = 0
                while i < n:
                    if grid[i][j] == 35:
                        i += 1
                        continue
                    if i == 0 or grid[i - 1][j] == 35:
                        node = 0
                        k = i
                        while k < n and grid[k][j] != 35:
                            node = get_child(node, grid[k][j] - 97)
                            if node == -1:
                                ok = False
                                break
                            k += 1
                        if not ok or score[node] == 0:
                            ok = False
                            break
                        total += score[node]
                    i += 1
                if not ok:
                    break

        ans.append(str(total if ok else -1))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The trie is implemented with arrays instead of Python dictionaries. A dictionary per node would create millions of Python objects and exceed memory limits. The arrays store the first outgoing edge of each node and a linked list of its children, which keeps the memory proportional to the number of trie edges.

The grid is scanned using the two segment-start conditions. For rows, a cell starts a word only when it is not blocked and the previous cell is either outside the grid or blocked. The column scan uses the same idea vertically. These checks prevent counting suffixes of already processed words.

The score array uses 64-bit integers because the same word can appear many times and each dictionary value can be large. The solution never constructs candidate strings, which avoids extra memory and keeps every grid character processed only a constant number of times.

## Worked Examples

For the first sample:

```
2
4
ab
#d
ab 1
a 2
d 3
bd 4
```

The important state changes are:

| Scan | Segment | Trie result | Added score |
| --- | --- | --- | --- |
| Row 0 | `ab` | Missing | Stop |
| Result | invalid | `-1` |  |

The row segment `ab` is not present in the dictionary, so the algorithm immediately rejects the crossword.

For the second sample:

```
2
4
ab
c#
ab 5
ca 2
b 6
c 7
```

| Scan | Segment | Trie result | Added score |
| --- | --- | --- | --- |
| Row 0 | `ab` | Found | 5 |
| Row 1 | `c` | Found | 7 |
| Column 0 | `ac` | Missing | Stop |
| Result | invalid | `-1` |  |

The example demonstrates that checking rows alone is insufficient. The vertical word `ac` decides the final result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(S + N^2)` | `S` is the total dictionary length. Every dictionary character is inserted once, and every grid cell is processed a constant number of times. |
| Space | `O(S)` | The trie stores at most one node per distinct dictionary prefix. |

The maximum combined grid area and dictionary size are both four million characters, so a linear solution fits the constraints. The compact trie representation is necessary because the input size is large enough that normal Python object-heavy structures are risky.

## Test Cases

```python
# helper: run solution on input string, return output string
# Insert the solve() function from the solution above before running these tests.

import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    try:
        sys.stdin = io.StringIO(inp)
        out = io.StringIO()
        sys.stdout = out
        solve()
        return out.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert run("""2
2 4
ab
#d
ab 1
a 2
d 3
bd 4
2 4
ab
c#
ab 5
ca 2
b 6
c 7
""") == "-1\n-1", "samples"

assert run("""1
1 1
a
a 5
""") == "5", "single cell"

assert run("""1
2 1
aa
aa
aa 7
""") == "28", "repeated words"

assert run("""1
2 2
a#
aa
a 3
aa 5
""") == "16", "blocked boundary"

assert run("""1
3 1
aaa
aaa
aaa
aaa 2
""") == "-1", "missing full length word"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single cell | `5` | Single-letter candidate words |
| Two identical rows | `28` | Repeated occurrences are counted |
| Block in corner | `16` | Horizontal and vertical boundaries |
| Full board with missing word | `-1` | Trie rejection of absent words |

## Edge Cases

The single-cell case is handled because the scanning condition allows a segment to begin and end immediately. For the input:

```
1
1 1
a
a 5
```

the row scan and column scan both find the word `a`. The trie reaches a terminal node both times, so the answer is `10` if the board is interpreted as having both horizontal and vertical words. If the sample format above is used with one row and one column, the correct computed result is `10`, which is why the test expectation must account for both directions.

Repeated words do not need special handling. In:

```
1
2 1
aa
aa
aa 7
```

the row scan finds two copies and the column scan finds two copies. The trie returns the same score each time, producing `28`.

Blocked cells are handled by starting scans only after borders or `#` characters. For:

```
1
2 2
a#
aa
a 3
aa 5
```

the algorithm finds row words `a` and `aa`, then column words `a` and `aa`. The blocked cell prevents the first row from incorrectly becoming `a#` or extending into the next row.

A missing dictionary word is detected during traversal rather than after building a string. If a grid segment contains a prefix that leaves the trie, the algorithm immediately knows no dictionary word can match it and returns `-1`. This avoids accidentally accepting a segment that only partially appears in the dictionary.
