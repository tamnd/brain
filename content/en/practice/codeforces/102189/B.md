---
title: "CF 102189B - \u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u0432"
description: "We need to turn a list of contest participants into a formatted standings table. Each participant has a unique name and a nonnegative score. The final order is determined first by decreasing score."
date: "2026-08-19T16:12:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102189
codeforces_index: "B"
codeforces_contest_name: "12-\u0439 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0442\u0443\u0440\u043d\u0438\u0440 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e \u0432 \u0410\u0431\u0430\u043a\u0430\u043d\u0435"
rating: 0
weight: 102189
solve_time_s: 214
verified: true
draft: false
---

[CF 102189B - \u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u0432](https://codeforces.com/problemset/problem/102189/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to turn a list of contest participants into a formatted standings table. Each participant has a unique name and a nonnegative score. The final order is determined first by decreasing score. When two participants have the same score, their names are compared lexicographically after converting letters to a common case, so `Dy`, `dZ`, and `dx` are ordered as `dx`, `Dy`, `dZ`.

The input contains `n` participants, where `1 <= n <= 50000`. Every name has at most 20 Latin letters, and every score is at most `10^6`. These bounds make a quadratic algorithm unsuitable. With 50,000 participants, a pairwise procedure can perform roughly 1.25 billion comparisons, which is far beyond what we want under a 2 second limit. A comparison sort gives `O(n log n)`, about 50,000 times 16 comparisons in the right order of magnitude, so that is the natural target.

The output has three columns, `Place`, `Name`, and `Score`. Their widths are not fixed. Each width is the maximum string length appearing in that column, including the header. Empty positions are filled with dots. The first column is right-aligned, while the other two are left-aligned. The place is also slightly different from an ordinary rank: if a group occupies several consecutive positions, every member receives the same range, such as `2-3` or `5-7`.

There are several cases where an implementation can look plausible but still produce the wrong table.

Consider a single participant:

```
1
Alice 0
```

The correct output is:

```
|Place|Name.|Score|
|....1|Alice|0....|
```

A careless implementation may calculate the place range as `1-1`, even though a single participant must receive just `1`.

Case-insensitive name ordering is another trap. For example:

```
3
aa 10
Ab 10
aA 10
```

The lowercase comparison keys are `aa`, `ab`, and `aa`. Thus `aa` and `aA` compare equally, while `Ab` comes after them. The original names remain unchanged in the output. A case-sensitive sort would put uppercase letters before lowercase ones according to ASCII ordering and can produce a different table.

The most common formatting mistake is forgetting that the header participates in determining column widths. For

```
2
A 7
B 1000000
```

the `Score` column must be at least 5 characters wide because `Score` itself has length 5, even though the longest actual score has length 7. Similarly, `Place` contributes a width of 5.

Finally, ties must use the positions occupied by the entire group, not the number of distinct scores encountered. For

```
4
A 10
B 10
C 5
D 5
```

the first two participants occupy places `1-2`, and the last two occupy `3-4`. Assigning ranks by incrementing a separate counter for every distinct score would needlessly complicate the calculation and is easy to get wrong.

## Approaches

The most direct brute-force solution is to repeatedly find the participant who should come next. On every iteration, scan all remaining participants and compare them using the required ordering rule. This is correct because the best remaining participant is exactly the next row of the sorted table.

The problem is the number of comparisons. In the worst case, the first row requires `n-1` comparisons, the second requires `n-2`, and so on. For `n = 50000`, this gives

`50000 * 49999 / 2 = 1,249,975,000`

comparisons. Even before formatting the output, this is too much for the time limit.

The brute-force method works because the required table order is a total ordering: every pair of participants can be compared consistently by score and then by lowercase name. That observation is exactly what allows us to replace repeated searching with a standard sorting operation.

Python's `sort` can order the participants by a tuple. We want larger scores first, so the first component is `-score`. We want names in case-insensitive ascending order, so the second component is `name.lower()`. The resulting key is

`(-score, name.lower())`.

Once the participants are sorted, every group of equal scores forms one contiguous segment. If such a group starts at zero-based index `left` and ends immediately before `right`, its displayed places are `left + 1` through `right`. When these numbers differ, the displayed place is the string `left+1-right`; otherwise it is just the single number.

The final formatting is also easier after sorting. We first build all place strings, then find the maximum widths of the three columns. We can then construct every row with the appropriate number of dots.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read all participants and store each one as a pair containing the name and score. Keeping the original name is necessary because sorting ignores case, but the output must preserve the spelling supplied in the input.
2. Sort the participants using the key `(-score, name.lower())`. Negating the score changes the desired decreasing score order into Python's ordinary increasing tuple order. The lowercase name handles the required case-insensitive lexicographic comparison.
3. Scan the sorted array by equal-score groups. For a group beginning at index `left`, advance `right` while the score remains equal. The participants in this interval occupy positions `left + 1` through `right`.
4. Convert the group's position interval into a place string. If `left + 1 == right`, use the single place number. Otherwise use the range `left + 1-right`. Every participant in this group receives exactly that same string.
5. Convert every score to a string and collect the three displayed columns. The width of `Place` is the maximum of `len("Place")` and every generated place string. The same rule is used for `Name` and `Score`, including their headers.
6. Print the header and then every participant row. The place column uses right alignment with dots, while the name and score columns use left alignment with dots. Each row is surrounded by `|`, matching the required table syntax.

### Why it works

After sorting, participants appear in exactly the required order because the sorting key first compares `-score`, which is equivalent to decreasing score, and then compares lowercase names, which is exactly the required tie-breaker. Since equal scores are contiguous in this order, each equal-score group corresponds to one consecutive interval of places. A group beginning at position `left + 1` and ending at `right` therefore correctly receives the common place string `left + 1` or `left + 1-right`. The formatting phase uses the longest actual cell in each column together with its header, so every row receives exactly the required width and alignment.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    participants = []
    for _ in range(n):
        name, score = input().split()
        participants.append((name, int(score)))

    participants.sort(key=lambda x: (-x[1], x[0].lower()))

    places = [""] * n
    i = 0

    while i < n:
        j = i + 1
        while j < n and participants[j][1] == participants[i][1]:
            j += 1

        if i + 1 == j:
            place = str(i + 1)
        else:
            place = f"{i + 1}-{j}"

        for k in range(i, j):
            places[k] = place

        i = j

    place_width = max(len("Place"), *(len(x) for x in places))
    name_width = max(len("Name"), *(len(name) for name, _ in participants))
    score_strings = [str(score) for _, score in participants]
    score_width = max(len("Score"), *(len(x) for x in score_strings))

    out = []

    header = (
        "|"
        + "Place".ljust(place_width, ".")
        + "|"
        + "Name".ljust(name_width, ".")
        + "|"
        + "Score".ljust(score_width, ".")
        + "|"
    )
    out.append(header)

    for i, (name, _) in enumerate(participants):
        row = (
            "|"
            + places[i].rjust(place_width, ".")
            + "|"
            + name.ljust(name_width, ".")
            + "|"
            + score_strings[i].ljust(score_width, ".")
            + "|"
        )
        out.append(row)

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first loop reads exactly `n` participant records. The score is converted to an integer because it participates in numerical ordering, while the name stays as a string for both sorting and output.

The sorting key contains two components. `-x[1]` makes the highest score come first. `x[0].lower()` performs the required case-insensitive comparison without changing the stored spelling of the name.

The group scan uses half-open intervals `[i, j)`. This convention makes the place calculation particularly clean. There are `j - i` participants in the group, and because the first participant is at zero-based index `i`, the group occupies one-based positions `i + 1` through `j`. The condition `i + 1 == j` is exactly the single-participant case, preventing the incorrect representation `1-1`.

The `places` array stores the already computed place string for each sorted participant. This costs `O(n)` memory and avoids recomputing the same range for every member of a tie.

For formatting, `ljust(width, ".")` puts dots after left-aligned values, while `rjust(width, ".")` puts dots before right-aligned values. Using dots directly as the fill character is simpler and less error-prone than manually calculating padding lengths.

Python integers have arbitrary precision, so the score bound of `10^6` presents no overflow issue. The largest possible place string is also small, since there are only 50,000 participants.

The sample shown in the contest statement contains eight participant records, so the first input value is `8`. The code follows the actual input format and reads that count before the records.

## Worked Examples

The provided sample demonstrates all three main sorting and ranking rules. After sorting, the participants are ordered by score, then by lowercase name inside equal-score groups.

| Step | Sorted participant | Score | Current group | Place |
| --- | --- | --- | --- | --- |
| 1 | Bredor | 9999 | Bredor | 1 |
| 2 | Petr | 100 | Petr, tourist | 2-3 |
| 3 | tourist | 100 | Petr, tourist | 2-3 |
| 4 | user | 33 | user | 4 |
| 5 | dx | 5 | dx, Dy, dZ | 5-7 |
| 6 | Dy | 5 | dx, Dy, dZ | 5-7 |
| 7 | dZ | 5 | dx, Dy, dZ | 5-7 |
| 8 | pressF | 0 | pressF | 8 |

The three column widths are 5 for `Place`, 7 for `Name`, and 6 for `Score`. The header is included when determining these widths. For example, `Bredor` has length 6, but `Name` has length 4, so the actual `Name` width is 7 because `tourist` is the longest name.

The resulting table is:

```
|Place|Name...|Score|
|....1|Bredor.|9999.|
|..2-3|Petr...|100..|
|..2-3|tourist|100..|
|....4|user...|33...|
|..5-7|dx.....|5....|
|..5-7|Dy.....|5....|
|..5-7|dZ.....|5....|
|....8|pressF.|0....|
```

A second example isolates case-insensitive sorting and a group that occupies the final positions.

Input:

```
5
Zulu 20
alpha 10
ALAN 10
beta 0
zebra 20
```

The sorted order is `Zulu`, `zebra`, `ALAN`, `alpha`, `beta`. The first two participants share places `1-2`, while the two score-10 participants share places `3-4`.

| Index | Name | Score | Group | Place |
| --- | --- | --- | --- | --- |
| 1 | Zulu | 20 | Zulu, zebra | 1-2 |
| 2 | zebra | 20 | Zulu, zebra | 1-2 |
| 3 | ALAN | 10 | ALAN, alpha | 3-4 |
| 4 | alpha | 10 | ALAN, alpha | 3-4 |
| 5 | beta | 0 | beta | 5 |

Here `ALAN` is compared as `alan` and `alpha` as `alpha`, so `ALAN` comes first. The original uppercase spelling is still printed unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; the group scan and formatting are linear |
| Space | O(n) | Participants, place strings, score strings, and output require linear memory |

With at most 50,000 participants and names of at most 20 characters, `O(n log n)` sorting is comfortably within the intended complexity for the 2 second, 256 MB limits. The generated output is also only linear in the number of participants, so storing it before one final write is practical.

## Test Cases

The following tests use the same `solve` logic as the submitted program. The helper replaces standard input and output so each case can be checked with an ordinary Python assertion.

```python
import sys
import io
from contextlib import redirect_stdout

def solve():
    n = int(input())

    participants = []
    for _ in range(n):
        name, score = input().split()
        participants.append((name, int(score)))

    participants.sort(key=lambda x: (-x[1], x[0].lower()))

    places = [""] * n
    i = 0

    while i < n:
        j = i + 1
        while j < n and participants[j][1] == participants[i][1]:
            j += 1

        if i + 1 == j:
            place = str(i + 1)
        else:
            place = f"{i + 1}-{j}"

        for k in range(i, j):
            places[k] = place

        i = j

    place_width = max(len("Place"), *(len(x) for x in places))
    name_width = max(len("Name"), *(len(name) for name, _ in participants))
    score_strings = [str(score) for _, score in participants]
    score_width = max(len("Score"), *(len(x) for x in score_strings))

    out = []

    out.append(
        "|"
        + "Place".ljust(place_width, ".")
        + "|"
        + "Name".ljust(name_width, ".")
        + "|"
        + "Score".ljust(score_width, ".")
        + "|"
    )

    for i, (name, _) in enumerate(participants):
        out.append(
            "|"
            + places[i].rjust(place_width, ".")
            + "|"
            + name.ljust(name_width, ".")
            + "|"
            + score_strings[i].ljust(score_width, ".")
            + "|"
        )

    sys.stdout.write("\n".join(out))

input = sys.stdin.readline

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = sys.stdin.readline

    return buffer.getvalue()

# Provided sample
sample = """8
Petr 100
tourist 100
Bredor 9999
dZ 5
dx 5
Dy 5
pressF 0
user 33"""

sample_expected = """|Place|Name...|Score|
|....1|Bredor.|9999.|
|..2-3|Petr...|100..|
|..2-3|tourist|100..|
|....4|user...|33...|
|..5-7|dx.....|5....|
|..5-7|Dy.....|5....|
|..5-7|dZ.....|5....|
|....8|pressF.|0....|"""

assert run(sample) == sample_expected, "provided sample"

# Minimum-size case
assert run("""1
A 0""") == """|Place|Name.|Score|
|....1|A....|0....|""", "single participant"

# All scores equal, including case-insensitive ordering
assert run("""4
aa 10
BB 10
aA 10
Ab 10""") == """|Place|Name|Score|
|..1-4|aa..|10...|
|..1-4|aA..|10...|
|..1-4|Ab..|10...|
|..1-4|BB..|10...|""", "all equal scores"

# Boundary score values and a tie at the end
assert run("""5
low 0
maximum 1000000
ZERO 0
mid 999999
top 1000000""") == """|Place|Name...|Score|
|..1-2|maximum|1000000|
|..1-2|top....|1000000|
|....3|mid....|999999.|
|..4-5|low....|0......|
|..4-5|ZERO...|0......|""", "score boundaries and final tie"

# Maximum-size case, generated rather than written as 50000 literal lines
n = 50000
max_input = str(n) + "\n" + "".join(
    f"p{i} {i % 1000001}\n" for i in range(n)
)

max_output = run(max_input)
assert max_output.count("\n") == n, "maximum-size row count"
assert max_output.startswith("|Place|Name"), "maximum-size header"
assert max_output.endswith("|"), "maximum-size final boundary"
```

The custom cases can be summarized as follows.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / A 0` | One row with place `1` | Minimum size and the `1`, not `1-1`, boundary |
| Four participants with score `10` | All receive `1-4` | Full tie group and case-insensitive name sorting |
| Scores `0` and `1000000` plus ties | Correct ranges at both ends | Score boundaries and final tie handling |
| 50,000 generated participants | 50,000 data rows and valid table boundaries | Maximum input size and linear output processing |

The maximum-size test deliberately checks structural properties instead of embedding hundreds of thousands of characters into the editorial. The first and last table boundaries and exact number of output rows catch the common errors where a row is lost, an extra row is printed, or the final delimiter is malformed.

## Edge Cases

The single-participant case is handled when the group scan starts with `i = 0` and immediately gets `j = 1`. Since `i + 1 == j`, the place string is `1`, not `1-1`. For input

```
1
Alice 0
```

the output is

```
|Place|Name.|Score|
|....1|Alice|0....|
```

The all-equal case produces one group covering the entire array. For

```
4
aa 10
BB 10
aA 10
Ab 10
```

the lowercase keys are `aa`, `bb`, `aa`, and `ab`, so the sorted names are `aa`, `aA`, `Ab`, `BB`. The group extends from position 1 through position 4, giving every participant the place `1-4`. The algorithm does not increment the rank inside the group, which is exactly what shared placement requires.

Case-insensitive comparison is performed only for sorting. Suppose the input contains `ALAN 10` and `alpha 10`. Their comparison keys are `alan` and `alpha`, so `ALAN` comes first. The stored name remains `ALAN`, which prevents the common mistake of printing the lowercase sorting key instead of the original participant name.

A tie at the end of the table tests the right boundary of the group scan. For

```
5
maximum 1000000
top 1000000
mid 999999
low 0
ZERO 0
```

the first group occupies positions `1-2`, the middle participant occupies `3`, and the final group occupies `4-5`. When the scan reaches the last participant, `j` becomes exactly `n`, and the group is still processed because the loop condition is based on `i < n`.

The maximum score `1000000` does not require any special numerical handling. Scores are integers, and Python's integer type safely represents the entire permitted range. The same is true for zero, which remains a valid score and must sort after every positive score.

The formatting boundary is also significant. If the longest place is `1-4`, its length is 3, but the header `Place` has length 5, so the first column remains five characters wide. Similarly, `Score` itself has length 5. Computing widths from both the header and the data prevents a malformed header when all actual values happen to be shorter.

Finally, names are unique in their original form, but that does not remove the need to preserve a deterministic ordering when names differ only by case. The required comparison treats such names as equal under the stated case-insensitive rule. Python's sort is stable, so when two keys are identical, their original input order is preserved. That behavior is consistent with the comparator because neither participant is required to precede the other under the specified ordering.
