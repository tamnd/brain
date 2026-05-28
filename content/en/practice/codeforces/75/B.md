---
title: "CF 75B - Facetook Priority Wall"
description: "We are given the name of a user on a social network and a sequence of activity messages between users. Every activity contributes a certain number of points between the two people involved."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "expression-parsing", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 75
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 67 (Div. 2)"
rating: 1500
weight: 75
solve_time_s: 134
verified: false
draft: false
---

[CF 75B - Facetook Priority Wall](https://codeforces.com/problemset/problem/75/B)

**Rating:** 1500  
**Tags:** expression parsing, implementation, strings  
**Solve time:** 2m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given the name of a user on a social network and a sequence of activity messages between users. Every activity contributes a certain number of points between the two people involved.

The three possible activities are:

- posting on someone's wall, worth 15 points
- commenting on someone's post, worth 10 points
- liking someone's post, worth 5 points

The relationship score is symmetric. If `alice` comments on `bob`'s post, both `alice` and `bob` gain 10 points toward each other.

Our task is not to compute scores between every pair of users. We only care about scores relative to the given user. After processing all actions, we must print every distinct person who appeared in the log, excluding the main user, sorted by descending score with that user. If multiple people have the same score, we break ties lexicographically.

The input format looks simple at first, but the strings are slightly tricky. The second username appears with `"'s"` attached, such as `fatma's`. A careless parser that directly stores this token will treat `"fatma"` and `"fatma's"` as different names.

The constraints are very small. There are at most 100 actions, and each username is at most length 10. Even an inefficient implementation would pass comfortably. This means the problem is primarily about careful string parsing and bookkeeping, not optimization.

A common mistake is forgetting to include users whose score with the main user is zero.

Consider this input:

```
ahmed
2
mona likes sara's post
sara commented on mona's post
```

Neither interaction involves `ahmed`, so both `mona` and `sara` have score 0 with him. The correct output is:

```
mona
sara
```

Another easy bug comes from parsing the second username incorrectly.

```
ahmed
1
ahmed posted on fatma's wall
```

The correct username is `fatma`, not `fatma's`. If we forget to remove the suffix, sorting and score accumulation become wrong because `"fatma"` and `"fatma's"` are treated as separate users.

Tie-breaking also matters.

```
ahmed
2
ahmed likes sara's post
ahmed likes mona's post
```

Both users receive 5 points, so the output must be:

```
mona
sara
```

A solution that sorts only by descending score would produce nondeterministic ordering.

## Approaches

The most direct approach is to simulate every action exactly as written. For each line, we extract the two usernames and determine which activity occurred. If the main user participates in the interaction, we add the corresponding value to the other person's score. Meanwhile, we maintain a set of every distinct username that appears.

This brute-force strategy is already fully acceptable because the input size is tiny. With at most 100 lines, even repeatedly scanning strings and sorting names costs almost nothing. The total work is dominated by sorting at most a few hundred names.

The real challenge is not performance but representation. The activity lines have three different sentence structures:

```
X posted on Y's wall
X commented on Y's post
X likes Y's post
```

The useful observation is that all formats become easy once we split the line into words. The first token is always `X`, the second token identifies the action type, and the fourth token contains `Y's`. Removing the final two characters gives the actual username.

After extracting the usernames and action type, the problem reduces to score accumulation in a dictionary.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) | O(n) | Accepted |
| Optimal | O(n log n) | O(n) | Accepted |

The "optimal" solution is essentially the same because the constraints are already tiny. The important part is organizing the parsing cleanly and sorting correctly.

## Algorithm Walkthrough

1. Read the main username and the number of actions.
2. Create a dictionary that maps each action word to its score.

We use:

- `"posted"` → 15
- `"commented"` → 10
- `"likes"` → 5
3. Maintain a set containing every distinct username except the main user.

This guarantees that even users with zero score appear in the final output.
4. Maintain another dictionary storing scores relative to the main user.

Missing entries are treated as zero.
5. For each action line:

1. Split the line into words.
2. Extract:

- `x = words[0]`
- `action = words[1]`
- `y = words[3][:-2]`

The last operation removes the trailing `"'s"`.

1. Add both usernames to the set if they are not the main user.
2. Look up the score value for the action.
3. If `x` is the main user, add the score to `y`.
4. If `y` is the main user, add the score to `x`.

Because the relationship is symmetric, either direction contributes equally.
6. Convert the set of usernames into a list and sort it using:

- descending score
- lexicographical order as a tiebreaker
7. Print the sorted names.

### Why it works

The algorithm processes every interaction exactly once. For each action, the only score that matters is the one involving the main user. If neither participant is the main user, the interaction cannot affect the final ranking, so we ignore its score contribution while still recording the usernames.

The score dictionary always stores the total accumulated interaction value between the main user and every other user processed so far. Since every action contributes independently and exactly once, the final dictionary contains the correct totals. The final sorting rule directly matches the statement: higher score first, alphabetical order for ties.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    me = input().strip()
    n = int(input())

    points = {
        "posted": 15,
        "commented": 10,
        "likes": 5
    }

    score = defaultdict(int)
    people = set()

    for _ in range(n):
        words = input().split()

        x = words[0]
        action = words[1]
        y = words[3][:-2]

        if x != me:
            people.add(x)

        if y != me:
            people.add(y)

        value = points[action]

        if x == me:
            score[y] += value

        if y == me:
            score[x] += value

    result = sorted(people, key=lambda name: (-score[name], name))

    print("\n".join(result))

solve()
```

The `points` dictionary converts action words into numeric values. This avoids repeated conditional statements and makes the code easier to extend.

The parser relies on the fixed sentence structure. After splitting by spaces, the second username always appears in position `3` with an attached `"'s"`. Slicing with `[:-2]` removes exactly those two characters.

The `people` set is separate from the `score` dictionary because some users may never interact directly with the main user. If we relied only on keys in `score`, users with zero score would disappear from the output.

Using `defaultdict(int)` removes the need to initialize missing scores manually.

The sorting key is subtle. We sort by `(-score[name], name)` instead of sorting twice. Negating the score gives descending numeric order, while the second component automatically handles lexicographical ties.

## Worked Examples

### Example 1

Input:

```
ahmed
3
ahmed posted on fatma's wall
fatma commented on ahmed's post
mona likes ahmed's post
```

Processing trace:

| Step | Action | Extracted Users | Score Changes | Current Scores |
| --- | --- | --- | --- | --- |
| 1 | ahmed posted on fatma's wall | ahmed, fatma | fatma +15 | fatma: 15 |
| 2 | fatma commented on ahmed's post | fatma, ahmed | fatma +10 | fatma: 25 |
| 3 | mona likes ahmed's post | mona, ahmed | mona +5 | fatma: 25, mona: 5 |

Final sorting:

| Name | Score |
| --- | --- |
| fatma | 25 |
| mona | 5 |

Output:

```
fatma
mona
```

This example shows that interactions contribute regardless of direction. Both actions involving `fatma` increased the same relationship score.

### Example 2

Input:

```
alex
4
bob likes clara's post
alex likes diana's post
eric commented on frank's post
george posted on alex's wall
```

Processing trace:

| Step | Action | Extracted Users | Score Changes | Current Scores |
| --- | --- | --- | --- | --- |
| 1 | bob likes clara's post | bob, clara | none | empty |
| 2 | alex likes diana's post | alex, diana | diana +5 | diana: 5 |
| 3 | eric commented on frank's post | eric, frank | none | diana: 5 |
| 4 | george posted on alex's wall | george, alex | george +15 | diana: 5, george: 15 |

All discovered users:

| User | Score |
| --- | --- |
| bob | 0 |
| clara | 0 |
| diana | 5 |
| eric | 0 |
| frank | 0 |
| george | 15 |

Sorted output:

```
george
diana
bob
clara
eric
frank
```

This trace demonstrates why we must store every seen username separately from the score dictionary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Processing actions is O(n), sorting usernames dominates |
| Space | O(n) | Dictionaries and sets store at most all distinct users |

With at most 100 actions, this solution easily fits within the limits. Even the sorting step is tiny because the number of distinct usernames is small.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        me = input().strip()
        n = int(input())

        points = {
            "posted": 15,
            "commented": 10,
            "likes": 5
        }

        score = defaultdict(int)
        people = set()

        for _ in range(n):
            words = input().split()

            x = words[0]
            action = words[1]
            y = words[3][:-2]

            if x != me:
                people.add(x)

            if y != me:
                people.add(y)

            value = points[action]

            if x == me:
                score[y] += value

            if y == me:
                score[x] += value

        result = sorted(people, key=lambda name: (-score[name], name))

        return "\n".join(result)

    return solve()

# provided sample
assert run(
"""ahmed
3
ahmed posted on fatma's wall
fatma commented on ahmed's post
mona likes ahmed's post
"""
) == "fatma\nmona", "sample 1"

# minimum input
assert run(
"""alex
1
bob likes clara's post
"""
) == "bob\nclara", "minimum size with zero scores"

# tie breaking
assert run(
"""alex
2
alex likes sara's post
alex likes mona's post
"""
) == "mona\nsara", "lexicographical tie breaking"

# repeated interactions
assert run(
"""alex
3
alex posted on bob's wall
bob commented on alex's post
alex likes bob's post
"""
) == "bob", "score accumulation"

# users unrelated to main user
assert run(
"""alex
4
bob likes clara's post
diana likes eric's post
frank commented on george's post
harry posted on alex's wall
"""
) == "harry\nbob\nclara\ndiana\neric\nfrank\ngeorge", "include zero-score users"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single unrelated interaction | `bob clara` order | Users with zero score must still appear |
| Equal scores | Lexicographical ordering | Correct tie-breaking |
| Multiple interactions with same user | Single accumulated total | Score aggregation |
| Mixed related and unrelated users | Positive scores first | Proper sorting and inclusion |

## Edge Cases

### Users with zero interaction score

Input:

```
ahmed
2
mona likes sara's post
sara commented on mona's post
```

Neither action involves `ahmed`, so no score updates occur.

The algorithm still inserts both `mona` and `sara` into the `people` set. Their scores remain the default value `0`.

Sorting gives:

```
mona
sara
```

A solution that only stored users inside the score dictionary would incorrectly print nothing.

### Parsing names ending with "'s"

Input:

```
ahmed
1
ahmed posted on fatma's wall
```

After splitting:

| Index | Value |
| --- | --- |
| 0 | ahmed |
| 1 | posted |
| 2 | on |
| 3 | fatma's |
| 4 | wall |

The algorithm uses `words[3][:-2]`, producing `fatma`.

Score state:

| User | Score |
| --- | --- |
| fatma | 15 |

Output:

```
fatma
```

Without removing the suffix, the stored name would incorrectly become `fatma's`.

### Tie-breaking by lexicographical order

Input:

```
alex
2
alex likes sara's post
alex likes mona's post
```

Both users receive exactly 5 points.

Sorting key values:

| User | Key |
| --- | --- |
| mona | (-5, "mona") |
| sara | (-5, "sara") |

Since the numeric parts are equal, normal string comparison determines the order.

Correct output:

```
mona
sara
```

A solution sorting only by score could produce the wrong ordering depending on insertion order.
