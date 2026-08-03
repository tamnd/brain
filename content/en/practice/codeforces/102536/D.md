---
title: "CF 102536D - Move to Remove Confidential Blunders"
description: "The task is to decide whether a person can access a piece of content based on two pieces of information: the person's age and the content's rating category. The title itself does not affect the decision, it is only part of the input format."
date: "2026-08-03T21:24:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102536
codeforces_index: "D"
codeforces_contest_name: "2020 UP ACM Algolympics Final Round"
rating: 0
weight: 102536
solve_time_s: 641
verified: true
draft: false
---

[CF 102536D - Move to Remove Confidential Blunders](https://codeforces.com/problemset/problem/102536/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 10m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to decide whether a person can access a piece of content based on two pieces of information: the person's age and the content's rating category. The title itself does not affect the decision, it is only part of the input format. The rating determines the minimum age requirement, except for the special PG case where a younger person may enter if accompanied by a responsible adult.

The input contains one age value and one rating string on the first line, followed by the content title on the second line. The output describes the access decision. It can be a normal approval, a conditional approval that requires an accompanying adult, or a rejection.

The age can be as large as 10^9, but the decision only depends on comparing that age with a few fixed thresholds. The title length is at most 100 characters, so reading and storing it is trivial. A solution that scans the title or performs any computation proportional to the age would be unnecessary. The intended algorithm should use constant time after parsing the input.

The main cases that can break a careless implementation are the exact boundary ages. For example, a person aged exactly 13 should be allowed into R-13 content.

```
13 R-13
Example
```

The correct output is:

```
OK
```

A solution using `age > 13` instead of `age >= 13` would incorrectly reject this case.

Another important case is PG content with a young person. A one-year-old person is not rejected immediately because PG allows access when accompanied.

```
1 PG
Example
```

The correct output is:

```
OK IF ACCOMPANIED
```

A solution that treats every age below 13 as forbidden would produce the wrong result.

The G rating is also a special case because it has no age restriction.

```
0 G
Example
```

The correct output is:

```
OK
```

Any implementation that applies a minimum age check to every rating would fail here.

## Approaches

A direct approach is to create a set of conditions for every rating and check them one by one. This is already the natural brute force method because there are only five possible rating values. Its work is constant: it reads the input, compares the age with a threshold when necessary, and prints the corresponding result.

There is no meaningful slower brute force involving the title because the title has no role in the decision. A hypothetical approach that repeatedly examined every possible age value would perform up to 10^9 checks in the largest case, which is far beyond the available time. The structure of the problem tells us that only the relation between the age and a fixed cutoff matters.

The key observation is that every rating can be represented by a simple rule. G always succeeds. PG has one conditional result for ages below 13. R-13, R-16, and R-18 are all minimum age requirements. Once these rules are written explicitly, the entire problem becomes a constant number of comparisons.

The brute-force works because the number of possible categories is tiny, but the useful insight is recognizing that the input size does not require any general search or simulation. The observation that the rating system is a fixed decision table lets us reduce the solution to a few conditional checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the person's age and the requested rating. The title can also be consumed from input, but it does not influence the result.
2. If the rating is G, immediately return OK because this category has no age restriction.
3. If the rating is PG, compare the age with 13. Ages 13 and above are approved normally, while younger ages receive the accompanied approval message.
4. If the rating is R-13, R-16, or R-18, determine the required minimum age from the rating number and compare it with the person's age. The person is accepted only when the age is at least the required value.
5. Print the decision string that matches the result.

The reason this works is that the rating rules form a complete partition of all possible inputs. Each rating has exactly one rule, and each rule directly matches the condition described by the rating system.

Why it works:

For any input, the algorithm selects the rule corresponding to the given rating. For G, the rule accepts everyone, which matches the unrestricted category. For PG, the algorithm separates people into those who meet the normal age requirement and those who require accompaniment. For restricted ratings, the algorithm accepts exactly the ages that satisfy the minimum age condition. Since every possible rating is handled by its correct rule, the produced output always matches the required access decision.

## Python Solution

```python
import sys
input = sys.stdin.readline

age, rating = input().split()
age = int(age)

if rating == "G":
    print("OK")
elif rating == "PG":
    if age >= 13:
        print("OK")
    else:
        print("OK IF ACCOMPANIED")
else:
    limit = int(rating[2:])
    if age >= limit:
        print("OK")
    else:
        print("ACCESS DENIED")
```

The code first separates the age from the rating and converts the age into an integer so numeric comparisons can be performed. The title line is not needed after parsing because it contains no information used by the decision process.

The G branch comes first because it ignores age completely. The PG branch has two possible outcomes, using `age >= 13` so the boundary case of exactly 13 is handled correctly.

The remaining ratings all have the same format: R followed by a hyphen and a number. Extracting the substring after the first two characters gives the required minimum age. Python integers can handle the maximum age value without any overflow concerns.

## Worked Examples

For the first sample:

```
18 R-18
Frozen 3
```

| Step | Age | Rating | Required Age | Result |
| --- | --- | --- | --- | --- |
| 1 | 18 | R-18 | 18 | Check age >= 18 |
| 2 | 18 | R-18 | 18 | Print OK |

The person is exactly at the required boundary, which confirms that equality must be accepted.

For the second sample:

```
1 R-13
Star Wars: The Fall of Skywalker
```

| Step | Age | Rating | Required Age | Result |
| --- | --- | --- | --- | --- |
| 1 | 1 | R-13 | 13 | Check age >= 13 |
| 2 | 1 | R-13 | 13 | Print ACCESS DENIED |

The age is below the minimum requirement, so access is rejected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | The algorithm performs a fixed number of string operations and comparisons. |
| Space | O(1) | Only a few variables are stored. |

The largest possible age does not increase the amount of work because it is only compared against fixed constants. The title length is small and does not affect the computation, so the solution easily fits within the time and memory limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    age, rating = input().split()
    age = int(age)

    if rating == "G":
        return "OK"
    elif rating == "PG":
        if age >= 13:
            return "OK"
        return "OK IF ACCOMPANIED"
    else:
        limit = int(rating[2:])
        if age >= limit:
            return "OK"
        return "ACCESS DENIED"

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

assert run("18 R-18\nFrozen 3\n") == "OK", "sample 1"
assert run("1 R-13\nStar Wars: The Fall of Skywalker\n") == "ACCESS DENIED", "sample 2"
assert run("13 PG\nAgent Cody Banks\n") == "OK", "sample 3"

assert run("0 G\nAnything\n") == "OK", "minimum age with unrestricted rating"
assert run("12 PG\nMovie\n") == "OK IF ACCOMPANIED", "PG boundary below 13"
assert run("16 R-16\nMovie\n") == "OK", "exact restricted boundary"
assert run("1000000000 R-18\nMovie\n") == "OK", "maximum age value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 G` | `OK` | Handles the rating without an age requirement. |
| `12 PG` | `OK IF ACCOMPANIED` | Checks the special PG behavior below the threshold. |
| `16 R-16` | `OK` | Checks equality at a restricted rating boundary. |
| `1000000000 R-18` | `OK` | Confirms large age values are handled correctly. |

## Edge Cases

For a person exactly at the minimum age, the algorithm uses greater than or equal comparisons.

```
13 R-13
Movie
```

The rating is not G or PG, so the code extracts the limit as 13 and checks `13 >= 13`. The condition succeeds and the answer is `OK`.

For a PG rating with a child below 13, the algorithm does not reject immediately.

```
5 PG
Movie
```

The code enters the PG branch, checks `5 >= 13`, and finds it false. Since PG allows accompaniment, the correct answer is `OK IF ACCOMPANIED`.

For a G rating with a very young person, the algorithm never performs an age comparison.

```
0 G
Movie
```

The first condition matches and the answer is `OK`. This avoids incorrectly applying restrictions that belong to other categories.
