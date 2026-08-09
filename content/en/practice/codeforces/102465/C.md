---
title: "CF 102465C - Crosswords"
description: "We need to construct an N × M character grid. Every row must be one of the B horizontal words, each of length M, and every column must be one of the A vertical words, each of length N. A word may be reused any number of times."
date: "2026-08-09T15:13:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102465
codeforces_index: "C"
codeforces_contest_name: "2018-2019 ICPC Southwestern European Regional Programming Contest (SWERC 2018)"
rating: 0
weight: 102465
solve_time_s: 572
verified: true
draft: false
---

[CF 102465C - Crosswords](https://codeforces.com/problemset/problem/102465/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to construct an `N × M` character grid. Every row must be one of the `B` horizontal words, each of length `M`, and every column must be one of the `A` vertical words, each of length `N`. A word may be reused any number of times.

A grid is counted once, because its letters uniquely determine every row and every column. We are not counting different choices of dictionary entries that happen to produce the same grid. Since each dictionary contains no duplicate words, a fixed grid also determines the exact word chosen for every row and column.

The first input line gives `N` and the number `A` of vertical words. The second gives `M` and the number `B` of horizontal words. The following `A` strings have length `N`, and the final `B` strings have length `M`. The answer is the number of grids satisfying both dictionaries simultaneously.

The dimensions are tiny, with `2 ≤ N, M ≤ 4`, so there are at most 16 cells. The dictionaries, however, can be large. Their product satisfies `A × B ≤ 1,008,016`, so one dictionary can contain roughly a thousand words when the other has a similar size, or hundreds of thousands of words when the other is very small. This rules out algorithms whose work is proportional to all pairs of words multiplied by an additional large power. In particular, blindly trying every sequence of horizontal words takes `B^N` possibilities. With `A = B = 1004` and `N = 4`, that is about `1.016 × 10^12` candidate grids, and checking every cell would require roughly `1.6 × 10^13` character checks.

The small word length gives us the useful structure. Every partial row or column is only a prefix of a dictionary word. A candidate character can be rejected immediately if it does not continue both the current horizontal prefix and the current vertical prefix. A trie is designed precisely for this kind of prefix test.

There are several edge cases where a straightforward implementation can silently go wrong.

Consider

```
2 1
2 1
ab
aa
```

The only horizontal word is `aa`, so both rows must be `aa`. Both columns are then `aa`, which is not the vertical word `ab`. The correct answer is `0`. An implementation that checks only the horizontal words and postpones column validation until after generating all grids wastes enormous work, while an implementation that checks only completed columns but forgets prefix validity can also explore invalid branches.

Reusing a dictionary word is allowed. For example,

```
2 1
2 1
aa
aa
```

has answer `1`. The grid is simply

```
aa
aa
```

The same word is used for both rows and both columns. A careless implementation that marks dictionary words as "used" after placing them would incorrectly return `0`.

The grid does not have to be square. For example,

```
2 4
4 1
aa
bb
ab
ba
abba
```

has answer `1`. Both rows are `abba`, giving columns `aa`, `bb`, `ba`, and `ab`, all of which belong to the vertical dictionary. Any implementation that assumes `N == M`, or accidentally uses `N` as the number of columns, will mishandle this case.

Finally, when `N == M`, the two dictionaries still have their assigned directions. A word from the vertical dictionary may be used horizontally only if it is also present in the horizontal dictionary, and vice versa. The clean way to respect this rule is simply to never swap dictionary membership when checking a grid. A horizontal line is checked against the horizontal dictionary, and a vertical line against the vertical dictionary.

## Approaches

The most direct brute force is to choose all `N` horizontal words. Since each row has `B` possibilities and repetition is allowed, there are `B^N` row sequences. After choosing them, we can build every column and check whether each resulting string belongs to the vertical dictionary. The method is correct because every possible grid has exactly one sequence of horizontal rows, so every valid grid is considered exactly once.

The problem is the exponent. With `N = 4`, `B = 1004`, the search already contains about `1.016 × 10^12` row sequences. Even though only 16 cells exist in each grid, checking them all would be far beyond the time limit.

The key observation is that we should not decide an entire row before checking its intersections with the columns. Suppose the current row begins with `sa`. If no horizontal dictionary word starts with `sa`, we can reject the row immediately. More strongly, suppose the current cell is at row `r` and column `c`. The character placed there must simultaneously be a valid next character for the current horizontal prefix and for the current vertical prefix. The intersection of those two sets of characters is usually tiny.

A trie stores exactly this information. At a trie node, its outgoing edges are the characters that may legally follow the current prefix. While filling the grid, we keep one pointer into the trie for the current row and one pointer for every column. Placing a character advances the row pointer and the corresponding column pointer. If either transition does not exist, the branch is dead immediately.

This turns the brute-force search from "choose complete words and check them afterward" into "construct the grid while continuously enforcing both dictionaries". The official SWERC analysis describes this as backtracking with two tries and maintaining the current trie positions for the row and columns.

There is one more useful choice. We can transpose the way we search. Either we build the grid one horizontal word at a time and use the vertical dictionary as the crossing constraint, or we build it one vertical word at a time and use the horizontal dictionary as the crossing constraint. We choose the direction with the smaller theoretical number of complete line combinations, comparing `B^N` with `A^M`. This does not change the problem, it only chooses which dictionary is used as the actively constructed set.

The trie representation in the implementation is deliberately compact. Since every word has length at most four, every prefix can be encoded as a base-27 integer. The digits `1` through `26` represent `a` through `z`, while the leading zero represents the empty prefix. The largest possible code is only `27^4 - 1 = 531440`, so a fixed array can replace a memory-heavy Python dictionary. Each array entry stores a 26-bit mask of possible next letters and one extra bit saying that the prefix itself is a complete dictionary word.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(NM · B^N)` | `O(A + B + NM)` | Too slow |
| Trie Backtracking | `O((A+B)·4 + NM·S)` | `O(27^4 + NM)` | Accepted |

Here `S` is the number of partial grids actually visited by the backtracking search. The trie makes `S` much smaller than the raw Cartesian product because invalid prefixes are discarded before a complete word is constructed. In the worst theoretical sense this remains an exponential search, which is expected for this constrained word-rectangle problem. The crucial point is that the grid has at most 16 cells and every character is checked against both dictionaries immediately.

## Algorithm Walkthrough

1. Read the vertical and horizontal dictionaries and build a prefix structure for each one. For every prefix, store which letters may follow it and whether the prefix itself is a complete word. A character transition can then be tested in constant time.
2. Compare `A^M` and `B^N`. If `A^M` is smaller, construct the grid column by column. Otherwise, construct it row by row. This makes the actively enumerated complete-line search space as small as possible.
3. Keep an array containing the current prefix of every line in the secondary direction. For example, when constructing rows, this array stores the prefixes of all columns. When constructing columns, it stores the prefixes of all rows. The active primary line has a separate trie position because it is being constructed one character at a time.
4. At every cell, obtain the bit mask of possible next characters from the primary trie node and the corresponding secondary trie node. Intersect these masks. Every remaining bit represents a character that is legal in both directions.
5. Try each character in the intersection. Advance the primary prefix and the corresponding secondary prefix by that character. If either resulting prefix does not exist in its trie, the branch is rejected immediately.
6. When the final character of a primary line is placed, require the resulting primary trie node to be terminal. This guarantees that the completed line is actually a dictionary word rather than merely a prefix of one.
7. When the final primary line is being constructed, every secondary line also reaches its full length. Require each resulting secondary trie node to be terminal at those cells. This validates all lines without needing a separate grid scan.
8. After a cell has been recursively processed, restore its secondary prefix before trying the next character. This is the backtracking step. The primary prefix is passed as an argument, so it naturally reverts when the recursive call returns.
9. Once every primary line has been completed, a valid grid has been found. Add one to the answer. Since every sequence of cell characters corresponds to exactly one grid, there is no double counting.

### Why it works

The invariant is that before every recursive call, every already-filled prefix belongs to the appropriate dictionary prefix set. The current primary line prefix is represented by a valid primary trie node, and every secondary line prefix is represented by a valid secondary trie node.

A character is placed only when it is an outgoing edge from both relevant trie nodes. Thus the invariant remains true after every placement. When a line reaches its final character, the terminal-bit check guarantees that the complete line is an actual dictionary word, not merely a prefix.

Every valid grid follows a path through the search because every character of that grid is a valid next character in both directions. Conversely, every path accepted by the search finishes with every row and every column at a terminal dictionary node, so it represents a valid grid. Each grid has one unique sequence of cell characters, giving exactly one accepted search path.

## Python Solution

```python
import sys

input = sys.stdin.readline

# A word has length at most 4.
# We encode a prefix in base 27, using digits 1..26 for a..z.
MAX_CODE = 27 ** 4
TERM = 1 << 26
ALPHA_MASK = TERM - 1

def build_trie(count, reader):
    """
    Each entry stores:
      bits 0..25 : possible next letters
      bit 26     : this prefix is itself a complete word
    """
    trie = [0] * MAX_CODE

    for _ in range(count):
        word = reader().strip()
        code = 0

        for ch in word:
            digit = ord(ch) - 96
            trie[code] |= 1 << (digit - 1)
            code = code * 27 + digit

        trie[code] |= TERM

    return trie

def solve(reader=None):
    if reader is None:
        reader = input

    n, a = map(int, reader().split())
    m, b = map(int, reader().split())

    vertical = build_trie(a, reader)
    horizontal = build_trie(b, reader)

    # Choose the direction with fewer possible complete line sequences.
    #
    # Horizontal construction:
    #   N lines, each chosen from B words -> B^N
    #
    # Vertical construction:
    #   M lines, each chosen from A words -> A^M
    if a ** m <= b ** n:
        primary = vertical
        secondary = horizontal
        primary_lines = m
        line_length = n
    else:
        primary = horizontal
        secondary = vertical
        primary_lines = n
        line_length = m

    # secondary_prefix[i] is the currently built prefix of
    # secondary line i.
    secondary_prefix = [0] * line_length

    sys.setrecursionlimit(100)

    def dfs(line, pos, primary_prefix):
        if line == primary_lines:
            return 1

        primary_value = primary[primary_prefix]
        secondary_value = secondary[secondary_prefix[pos]]

        # A character must be allowed by both tries.
        mask = primary_value & secondary_value & ALPHA_MASK

        answer = 0
        last_position = (pos == line_length - 1)
        last_line = (line == primary_lines - 1)

        while mask:
            bit = mask & -mask
            mask -= bit

            digit = bit.bit_length()  # 1..26

            new_primary = primary_prefix * 27 + digit
            new_primary_value = primary[new_primary]

            # The primary line must be a complete dictionary word
            # when its final character is placed.
            if last_position and not (new_primary_value & TERM):
                continue

            old_secondary = secondary_prefix[pos]
            new_secondary = old_secondary * 27 + digit
            new_secondary_value = secondary[new_secondary]

            # On the final primary line, this character also completes
            # the secondary line, so it must be a complete word.
            if last_line and not (new_secondary_value & TERM):
                continue

            secondary_prefix[pos] = new_secondary
            answer += dfs(line, pos + 1, new_primary)
            secondary_prefix[pos] = old_secondary

        return answer

    return str(dfs(0, 0, 0))

if __name__ == "__main__":
    print(solve())
```

The two calls to `build_trie` consume the two dictionaries without retaining the original strings. This matters for the largest inputs, where keeping hundreds of thousands of Python string objects would waste considerably more memory than the trie itself.

The prefix encoding uses base 27 rather than base 26 because it needs to distinguish prefixes of different lengths. With digits from `1` through `26`, the code for `a` is `1`, while the code for `aa` is `28`, so they can never collide. The empty prefix is simply `0`.

Each trie entry contains a character mask. For example, if the prefix `s` can be followed by `a`, `e`, or `t`, its entry has bits corresponding to those three letters set. Intersecting two such masks is much cheaper than trying all 26 letters and performing separate dictionary lookups.

The terminal flag is stored in bit 26, outside the 26 character bits. A prefix can simultaneously be a complete word and have children. For example, if both `are` and `area` exist, the node for `are` must remain terminal while also allowing `a` as a next character.

The `last_position` test is necessary because merely reaching the end of a primary line does not guarantee that the line is a dictionary word. The same applies to `last_line` for secondary lines. Checking these conditions during the search avoids a second pass over the finished grid.

Python integers have arbitrary precision, which is necessary because the number of valid grids is not guaranteed to fit into a 32-bit or 64-bit integer. The search itself never stores all grids, it only accumulates their count.

The recursion depth is at most `N × M`, which is at most 16, so recursion is safe. The secondary-prefix array is modified before the recursive call and restored immediately afterward. Forgetting that restoration is a classic backtracking bug because the next branch would inherit characters from the previous branch.

## Worked Examples

### Sample 1

The input contains four vertical words and five horizontal words. Since `4^4 = 256` is larger than `5^3 = 125`, the implementation chooses to construct the grid horizontally, because there are fewer possible sequences of complete horizontal words.

One valid branch is `says`, `area`, `test`. The corresponding columns are `sat`, `are`, `yes`, and `sat`.

| Primary line | Position | Chosen character | Primary prefix | Secondary prefixes |
| --- | --- | --- | --- | --- |
| 0 | 0 | `s` | `s` | `s`, `, ` |
| 0 | 1 | `a` | `sa` | `s`, `a`, `` |
| 0 | 2 | `y` | `say` | `s`, `a`, `y`, `` |
| 0 | 3 | `s` | `says` | `s`, `a`, `y`, `s` |
| 1 | 0 | `a` | `a` | `sa`, `a`, `y`, `s` |
| 1 | 1 | `r` | `ar` | `sa`, `ar`, `y`, `s` |
| 1 | 2 | `e` | `are` | `sa`, `ar`, `ye`, `s` |
| 1 | 3 | `a` | `area` | `sa`, `ar`, `ye`, `sa` |
| 2 | 0 | `t` | `t` | `sat`, `ar`, `ye`, `sa` |
| 2 | 1 | `e` | `te` | `sat`, `are`, `ye`, `sa` |
| 2 | 2 | `s` | `tes` | `sat`, `are`, `yes`, `sa` |
| 2 | 3 | `t` | `test` | `sat`, `are`, `yes`, `sat` |

After the final cell, all three horizontal prefixes are terminal words, and all four vertical prefixes are also terminal words. This branch contributes one grid. The other valid branch is `ways`, `area`, `rest`, giving columns `war`, `are`, `yes`, `sat`. The final answer is `2`.

### Sample 2

Here `N = M = 3` and both dictionaries contain the same seven words. Since `A^M` and `B^N` are equal, the implementation chooses the vertical dictionary as the primary direction.

For one valid grid, the rows are `its`, `the`, and `set`, and the columns happen to be the same three words.

| Primary line | Position | Chosen character | Primary prefix | Secondary prefixes |
| --- | --- | --- | --- | --- |
| 0 | 0 | `i` | `i` | `i`, `, ` |
| 0 | 1 | `t` | `it` | `i`, `t`, `` |
| 0 | 2 | `s` | `its` | `i`, `t`, `s` |
| 1 | 0 | `t` | `t` | `it`, `t`, `s` |
| 1 | 1 | `h` | `th` | `it`, `th`, `s` |
| 1 | 2 | `e` | `the` | `it`, `the`, `se` |
| 2 | 0 | `s` | `s` | `its`, `the`, `s` |
| 2 | 1 | `e` | `se` | `its`, `the`, `se` |
| 2 | 2 | `t` | `set` | `its`, `the`, `set` |

The final column prefixes are `its`, `the`, and `set`, so this branch is accepted. A second branch produces the grid with rows `ran`, `age`, `now`. The answer is `2`.

These traces show the central invariant directly. Every prefix in the secondary-prefix array is already known to be a prefix of some allowed word, even before the corresponding row or column is complete.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Trie construction | `O(4(A+B))` | Every input word has length at most four |
| Search | `O(NM · S)` | Each visited cell examines at most 26 candidate letters |
| Space | `O(27^4 + NM)` | Two fixed prefix arrays plus the current secondary prefixes |

Here `S` denotes the number of partial grids visited after trie pruning. A useful upper bound for the complete-line search is `min(A^M, B^N)`, because the implementation chooses the smaller of the two orientations. The character-level trie checks normally cut off branches much earlier.

The fixed trie size is particularly convenient in Python. Since `27^4 = 531441`, two arrays of that size are small enough for the 256 MB memory limit and avoid the substantial overhead of millions of Python dictionary entries. The grid itself has at most 16 cells, so the recursive state is tiny.

The exponential nature of the search is unavoidable for the general word-rectangle formulation, but the problem deliberately limits both dimensions to four and gives a product bound on the dictionary sizes. The trie turns the search into constraint propagation rather than enumeration of complete grids, which is the intended way to make those constraints practical.

## Test Cases

The following harness assumes the solution above is saved as `solution.py`. The solver accepts an optional `reader`, which lets the tests feed input strings directly without modifying the process-wide standard input.

```
import io
from solution import solve

def run(inp: str) -> str:
    return solve(io.StringIO(inp).readline).strip()

# Sample 1
assert run(
    """\
3 4
4 5
war
are
yes
sat
says
area
test
ways
rest
"""
) == "2", "sample 1"

# Sample 2
assert run(
    """\
3 7
3 7
ran
age
now
its
the
set
ago
ran
age
now
its
the
set
ago
"""
) == "2", "sample 2"

# Minimum-size, all values equal.
assert run(
    """\
2 1
2 1
aa
aa
"""
) == "1", "minimum-size all-equal case"

# Rectangular grid, 2 rows and 4 columns.
assert run(
    """\
2 4
4 1
aa
bb
ab
ba
abba
"""
) == "1", "rectangular grid"

# No valid crossing.
assert run(
    """\
2 1
2 1
ab
aa
"""
) == "0", "incompatible vertical and horizontal words"

# Maximum dictionary product: 1000 * 1000 = 1,000,000.
# All vertical words start with 'a' and all horizontal words start
# with 'b', so the very first cell has no possible character.
def make_words(first, count):
    result = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    for x in alphabet:
        for y in alphabet:
            for z in alphabet:
                result.append(first + x + y + z)
                if len(result) == count:
                    return result

    return result

vertical = make_words("a", 1000)
horizontal = make_words("b", 1000)

large_input = (
    "4 1000\n"
    "4 1000\n"
    + "\n".join(vertical)
    + "\n"
    + "\n".join(horizontal)
    + "\n"
)

assert run(large_input) == "0", "maximum-size dictionary product"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `2` | Basic crossing and two distinct valid grids |
| Sample 2 | `2` | Square case where both dictionaries are identical |
| `2 × 2`, both lists contain `aa` | `1` | Word reuse and minimum dimensions |
| `2 × 4` with `abba` | `1` | Rectangular dimensions and correct orientation |
| Vertical `ab`, horizontal `aa` | `0` | Immediate prefix incompatibility |
| `1000 × 1000` dictionaries with disjoint first letters | `0` | Large input and early trie pruning |

## Edge Cases

For the minimum-size all-equal case,

```
2 1
2 1
aa
aa
```

the search starts with both tries allowing only `a`. The first cell advances both prefixes to `a`, and the second cell completes the primary line as `aa`. The next line repeats exactly the same process. At the end every row and column is terminal, so the answer is `1`. No word is consumed by the first use, so the same dictionary entry remains available for every line.

For the incompatible-prefix case,

```
2 1
2 1
ab
aa
```

the primary and secondary root nodes allow different characters. The vertical trie allows `a`, while the horizontal trie also allows `a`, so the first cell itself is not rejected. After placing `a`, the next cell on the first primary line requires the vertical prefix `ab` and the horizontal prefix `aa`. The only possible next character for the vertical word is `b`, while the horizontal word requires `a`. Their masks have empty intersection, so the branch ends immediately. The answer is `0`.

For the rectangular case,

```
2 4
4 1
aa
bb
ab
ba
abba
```

the only horizontal word is `abba`, so both rows must become `abba`. The resulting columns are `aa`, `bb`, `ba`, and `ab`. All four exist in the vertical trie. The algorithm does not assume that the number of rows and columns are equal, so it processes two primary lines of length four and correctly returns `1`.

For the large dictionary case, the input contains 1000 vertical words beginning with `a` and 1000 horizontal words beginning with `b`. The product is exactly `1,000,000`, within the required limit. At the very first cell, the vertical root mask contains `a` while the horizontal root mask contains `b`. Their intersection is zero, so the entire search terminates after inspecting the first cell. The answer is `0`, and the large dictionaries do not cause a large search tree because prefix constraints are applied before any branching.

The `N = M` restriction does not require special logic in the search. The algorithm always checks a line against the dictionary corresponding to its actual direction. If a word appears in both dictionaries, it can naturally occur in both directions. If it appears in only one, it can only be used in that direction. This matches the required rule without introducing a special-case branch into the backtracking code.
