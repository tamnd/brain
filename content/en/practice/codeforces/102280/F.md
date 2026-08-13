---
title: "CF 102280F - \u041d\u0435\u043e\u0436\u0438\u0434\u0430\u043d\u043d\u0430\u044f \u0437\u0438\u043c\u0430"
description: "Each line in the notebook contains only a driver's surname. A driver writes the surname once when leaving the garage and once when returning. The notebook does not tell us which occurrence is a departure and which is a return."
date: "2026-08-13T15:59:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102280
codeforces_index: "F"
codeforces_contest_name: "2010, \u0422\u0440\u0435\u043d\u0438\u0440\u043e\u0432\u043a\u0430 \u0421\u0413\u0410\u0423 aka \u041a\u043e\u043d\u0442\u0435\u0441\u0442 \u043f\u0440\u043e \u043c\u0430\u0440\u0448\u0440\u0443\u0442\u043a\u0438"
rating: 0
weight: 102280
solve_time_s: 146
verified: true
draft: false
---

[CF 102280F - \u041d\u0435\u043e\u0436\u0438\u0434\u0430\u043d\u043d\u0430\u044f \u0437\u0438\u043c\u0430](https://codeforces.com/problemset/problem/102280/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

Each line in the notebook contains only a driver's surname. A driver writes the surname once when leaving the garage and once when returning. The notebook does not tell us which occurrence is a departure and which is a return.

For a driver who completed all trips, the surname appears an even number of times. The driver who is still stuck somewhere has one unmatched departure, so that surname appears an odd number of times. The task is to find that surname. If there is no unmatched surname, the required output is `FAIL`.

For example, if the notebook contains

```
Yakubov
Abramov
Yakubov
```

then `Yakubov` has two records and `Abramov` has one, so `Abramov` is the driver who did not return.

The value of `n` can reach 150000, and the surname can contain up to 255 characters. An algorithm that compares many pairs of records is too expensive. With 150000 records, a quadratic algorithm performs roughly

[
\frac{150000\cdot149999}{2}\approx 11.25\cdot10^9
]

comparisons, far beyond what fits into a two-second limit. We need to process each record only a constant number of times, giving an expected linear-time solution.

There are several edge cases that can make a careless implementation fail. The smallest possible input is a single record:

```
1
Petrov
```

The answer is `Petrov`, because that single occurrence cannot be paired with another record.

Repeated surnames must also be handled correctly. For

```
5
Ivanov
Ivanov
Ivanov
Ivanov
Ivanov
```

the answer is `Ivanov`, because five occurrences leave one unmatched record. An implementation that merely looks for a surname occurring exactly once would incorrectly reject this case.

The surname can be as long as 255 characters, so it must be treated as an arbitrary string rather than as a character or a small numeric value. For example,

```
1
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

contains one valid surname of maximum length, and that exact string must be printed.

Finally, the answer is determined by parity, not by the order of the records. The sequence

```
Askerov
Shumacher
Askerov
Abalkin
Abalkin
```

has three relevant pairs or unmatched occurrences regardless of where those lines appear. The correct answer is `Shumacher`.

## Approaches

A direct approach is to take every surname and search for another identical surname that can be paired with it. Once a pair is found, both records can be removed, and the remaining record identifies the driver who did not return. This is correct because every completed trip contributes exactly two equal surnames.

The problem is the cost of searching. In the worst case, we may inspect almost every other record for every record. With `n = 150000`, this gives approximately 11.25 billion comparisons. Even though each comparison is simple, that amount of work is far beyond the time limit.

The useful observation is that the actual order of the notebook entries does not matter. What matters is how many times each surname occurs. Every completed driver contributes an even count, while the missing return changes one count from even to odd.

We can exploit this directly with a set. When a surname appears for the first time, put it into the set. When it appears again, remove it. After processing any prefix of the input, a surname is in the set exactly when it has appeared an odd number of times so far. After all records have been processed, the set contains precisely the surnames with odd total frequency.

Under the intended input conditions, there is one such surname. If the set contains exactly one value, that is the answer. If it is empty, all records were paired and we print `FAIL`. If malformed input produced several odd-frequency surnames, returning `FAIL` is also the safe behavior because there is no unique driver to identify.

The same idea can be implemented with a frequency dictionary, but the toggling set is simpler because we never need the exact count. We only need to know whether the current count is odd or even.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) expected | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and create an empty set called `odd`.
2. Process each surname one at a time. If the surname is not in `odd`, insert it. If it is already there, remove it. The two cases correspond exactly to changing its occurrence count from even to odd or from odd to even.
3. After all `n` records have been processed, inspect `odd`. Every surname that remains has appeared an odd number of times.
4. If exactly one surname remains, print it. That surname has one unmatched occurrence, so its driver has not returned.
5. If the set is empty, print `FAIL`. Every surname occurred an even number of times, so every notebook record can be paired with an identical record.
6. If several surnames remain, also print `FAIL`, because the input does not identify a unique unmatched driver.

### Why it works

The invariant is that after processing any number of records, a surname belongs to `odd` exactly when its number of processed occurrences is odd. Initially every count is zero, so the invariant holds. Reading a surname changes its parity by one. If the previous count was even, the surname is inserted, and if it was odd, the surname is removed. Thus the invariant remains true after every record.

At the end, every driver who completed all trips has an even number of notebook records and is absent from the set. The driver who did not return has an odd number of records and remains in the set. Consequently, when there is one remaining surname, it is exactly the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    odd = set()

    for _ in range(n):
        surname = input().strip()

        if surname in odd:
            odd.remove(surname)
        else:
            odd.add(surname)

    if len(odd) == 1:
        print(next(iter(odd)))
    else:
        print("FAIL")

if __name__ == "__main__":
    solve()
```

The set `odd` stores only the surnames whose current frequency is odd. The membership test and insertion or removal are expected O(1), so processing one record takes constant expected time.

Using `input().strip()` removes the newline left by `readline()`. It does not alter the letters inside the surname, so case remains significant. For example, `Ivanov` and `ivanov` are different strings and must be treated as different drivers.

There is no integer arithmetic involving `n` beyond the loop counter, so integer overflow is not an issue in Python. The loop runs exactly `n` times, which avoids any off-by-one ambiguity.

The condition `len(odd) == 1` is preferable to simply taking an arbitrary element. The latter would hide malformed input containing multiple odd-frequency surnames. The empty-set case corresponds directly to the requested `FAIL` output.

## Worked Examples

### Sample 1

The first sample contains three records:

```
3
Yakubov
Yakubov
Abramov
```

The state of the set changes as follows.

| Record | Surname | Action | `odd` after record |
| --- | --- | --- | --- |
| 1 | `Yakubov` | insert | `{Yakubov}` |
| 2 | `Yakubov` | remove | `{}` |
| 3 | `Abramov` | insert | `{Abramov}` |

`Yakubov` occurs twice, so its two records cancel each other. `Abramov` occurs once and remains in the set, giving the output `Abramov`.

### Sample 2

The second sample is

```
7
Askerov
Shumacher
Askerov
Askerov
Shumacher
Abalkin
Abalkin
```

The state evolves like this.

| Record | Surname | Action | `odd` after record |
| --- | --- | --- | --- |
| 1 | `Askerov` | insert | `{Askerov}` |
| 2 | `Shumacher` | insert | `{Askerov, Shumacher}` |
| 3 | `Askerov` | remove | `{Shumacher}` |
| 4 | `Askerov` | insert | `{Shumacher, Askerov}` |
| 5 | `Shumacher` | remove | `{Askerov}` |
| 6 | `Abalkin` | insert | `{Askerov, Abalkin}` |
| 7 | `Abalkin` | remove | `{Askerov}` |

`Shumacher` appears twice and `Abalkin` appears twice. `Askerov` appears three times, so exactly one occurrence remains unmatched. The output is `Askerov`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) expected | Each surname is processed once, with expected O(1) set operations. |
| Space | O(n) | In the worst case, many different surnames can have odd frequency and remain in the set. |

With `n` at most 150000, an expected linear-time algorithm performs only a few hash-table operations per input line. That is comfortably within the intended algorithmic complexity for a two-second limit. The memory usage grows with the number of distinct surnames rather than with the number of records stored separately.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())
    odd = set()

    for _ in range(n):
        surname = input().strip()
        if surname in odd:
            odd.remove(surname)
        else:
            odd.add(surname)

    if len(odd) == 1:
        print(next(iter(odd)))
    else:
        print("FAIL")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """3
Yakubov
Yakubov
Abramov
"""
) == "Abramov", "sample 1"

# Provided sample 2
assert run(
    """7
Askerov
Shumacher
Askerov
Askerov
Shumacher
Abalkin
Abalkin
"""
) == "Askerov", "sample 2"

# Minimum-size input
assert run(
    """1
Petrov
"""
) == "Petrov", "minimum n"

# All records have the same surname, with an odd number of occurrences
assert run(
    """5
Ivanov
Ivanov
Ivanov
Ivanov
Ivanov
"""
) == "Ivanov", "all equal values"

# Maximum valid odd n, all records have the same surname
max_n = 149999
assert run(
    str(max_n) + "\n" + ("Z" * 255 + "\n") * max_n
) == "Z" * 255, "maximum n and maximum surname length"

# No unique unmatched surname, representing the FAIL case
assert run(
    """6
A
B
A
B
C
C
"""
) == "FAIL", "all records paired"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / Petrov` | `Petrov` | Minimum valid input and a single unmatched record |
| Five copies of `Ivanov` | `Ivanov` | Repeated occurrences and parity rather than frequency equal to one |
| 149999 copies of a 255-character surname | The same surname | Maximum valid odd `n` and maximum surname length |
| `A B A B C C` | `FAIL` | Every occurrence is paired and the set becomes empty |

## Edge Cases

The minimum case is

```
1
Petrov
```

The set starts empty. `Petrov` is inserted, so after the only record the set is `{Petrov}`. Its size is one, and the algorithm prints `Petrov`.

A surname does not have to occur exactly once to be the answer. Consider

```
5
Ivanov
Ivanov
Ivanov
Ivanov
Ivanov
```

The first occurrence inserts `Ivanov`, the second removes it, the third inserts it again, the fourth removes it, and the fifth inserts it. The final set contains `Ivanov`, so the answer is `Ivanov`. This is why tracking parity is more appropriate than searching specifically for a frequency of one.

The all-returned case can be represented by

```
6
A
B
A
B
C
C
```

`A` is inserted and removed, then `B` is inserted and removed, and finally `C` is inserted and removed. The final set is empty, so the program prints `FAIL`.

A maximum-length surname is handled as an ordinary Python string. For example,

```
1
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
```

produces the entire surname unchanged. The algorithm never indexes into the surname or assumes anything about its length, so the 255-character boundary requires no special branch.

The order of records also has no effect. For

```
5
Askerov
Abalkin
Askerov
Abalkin
Shumacher
```

the two pairs cancel regardless of their positions. After the first four records the set is empty, and `Shumacher` is inserted by the last record. The result is `Shumacher`.

Finally, the declared input size is odd. Under the story's valid conditions, every completely finished trip contributes two records, while exactly one unfinished trip contributes one extra record, so there must be exactly one odd-frequency surname. The `FAIL` branch is retained because the output specification explicitly allows it and because checking the final set size makes the implementation robust if the input does not satisfy that intended structure.
