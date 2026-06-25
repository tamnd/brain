---
title: "CF 106113K - Maraton de Peliculas"
description: "The problem describes a collection of movies. Each movie has a release year, a director name, and a rating. We need build the longest possible movie marathon by choosing some of the movies and arranging them in chronological order. A valid marathon has three restrictions."
date: "2026-06-25T11:39:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106113
codeforces_index: "K"
codeforces_contest_name: "Coding Cup TecNM 2025"
rating: 0
weight: 106113
solve_time_s: 30
verified: true
draft: false
---

[CF 106113K - Maraton de Peliculas](https://codeforces.com/problemset/problem/106113/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 30s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes a collection of movies. Each movie has a release year, a director name, and a rating. We need build the longest possible movie marathon by choosing some of the movies and arranging them in chronological order.

A valid marathon has three restrictions. The release years cannot decrease, the rating must strictly improve from one movie to the next, and two consecutive movies cannot have the same director. The task is to find the maximum number of movies that can appear in such a sequence.

The input gives the number of movies followed by the data of each movie. The output is a single integer representing the largest valid marathon length.

The number of movies is at most 3000. This immediately rules out algorithms that try every subset, because the number of possible subsets grows exponentially. A dynamic programming solution with a quadratic number of transitions is realistic because $3000^2 = 9 \times 10^6$, which is small enough for a compiled language and still acceptable in Python with simple operations.

The tricky part is not the size of the input but handling the ordering rules correctly. A common mistake is to only sort by year and assume every earlier movie can be a predecessor. The rating condition is strict, so a movie with the same or lower rating cannot extend a marathon.

Consider these cases:

```
3
2000 A 50
2001 A 60
2002 B 70
```

The correct output is:

```
2
```

A careless solution might choose all three because the years increase, but the first two movies have the same director and appear consecutively, which is forbidden.

Another example:

```
3
2000 A 50
2001 B 50
2002 C 60
```

The correct output is:

```
2
```

The first two movies cannot be consecutive because their ratings are equal. A solution using non-decreasing ratings instead of strictly increasing ratings would incorrectly return 3.

A final boundary case is when no movie can follow another:

```
2
2000 A 90
2001 B 80
```

The correct output is:

```
1
```

Every single movie is already a valid marathon of length one, so the answer can never become zero.

# Approaches

A direct approach is to try every possible ordering of movies and check whether it satisfies the conditions. This is correct because every possible marathon would eventually be considered. However, the number of possible subsets alone is $2^N$, and with $N=3000$ this is impossible.

A more reasonable brute force idea is to sort movies by year and use a dynamic programming transition. Even then, a naive recursive search over all choices still explores too many branches because many different choices lead to the same remaining state.

The key observation is that after sorting movies by time, the only information needed about a partial marathon is the last movie chosen. If we know the last movie, we know the current year, rating, and director, which are exactly the values needed to decide whether another movie can be appended.

Let `dp[i]` represent the longest valid marathon that ends with movie `i`. For every previous movie `j`, we check whether `j` can be immediately before `i`. If the year of `j` is not greater than the year of `i`, the rating of `j` is smaller than the rating of `i`, and the directors differ, then `dp[i]` can be updated from `dp[j]`.

The sorting step is what makes the transition simple. We sort by year and then rating. After sorting, every possible predecessor appears before its successor in the list, because a successor must have a year that is at least as large and a larger rating.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^N)$ | $O(N)$ | Too slow |
| Dynamic Programming after sorting | $O(N^2)$ | $O(N)$ | Accepted |

# Algorithm Walkthrough

1. Read all movies and store each one as a tuple containing year, director, and rating. Sort the movies by year first and rating second.

The sorted order creates a timeline where a valid previous movie can only appear before the current movie. The rating ordering inside the same year also prevents impossible transitions caused by equal or smaller ratings.

1. Create an array `dp` where `dp[i]` starts as 1 because every movie can form a marathon by itself.

This initialization handles cases where no other movie can be placed before a movie.

1. For every movie `i`, inspect every earlier movie `j`.

Movie `j` can extend a marathon ending at `j` if its year is not after `i`, its rating is smaller than `i`'s rating, and the directors are different.

1. When a valid transition exists, update:

$$dp[i] = \max(dp[i], dp[j] + 1)$$

The new movie is added after the best marathon that already ends at `j`.

1. The answer is the maximum value in `dp`.

The longest marathon might end at any movie, so we cannot only inspect the last element after sorting.

## Why it works

The invariant of the dynamic programming array is that `dp[i]` always stores the best possible marathon whose final movie is exactly movie `i`.

When considering movie `i`, every possible previous movie appears among the earlier indices. If a previous movie can legally connect to `i`, the transition considers the optimal marathon ending there and extends it by one. Since every possible final predecessor is checked, no valid marathon ending at `i` is missed. Taking the maximum over all endings gives the global optimum.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    movies = []

    for _ in range(n):
        y, director, p = input().split()
        movies.append((int(y), int(p), director))

    movies.sort()

    dp = [1] * n
    ans = 1

    for i in range(n):
        year_i, score_i, director_i = movies[i]

        for j in range(i):
            year_j, score_j, director_j = movies[j]

            if year_j <= year_i and score_j < score_i and director_j != director_i:
                dp[i] = max(dp[i], dp[j] + 1)

        ans = max(ans, dp[i])

    print(ans)

if __name__ == "__main__":
    solve()
```

The input is converted into tuples containing numeric values for the year and score so comparisons are direct. The director remains a string because only equality checks are needed.

Sorting uses `(year, score, director)` ordering. The director is included only as a final tie breaker and does not affect correctness because transitions still explicitly check all three marathon conditions.

The nested loops implement the dynamic programming transitions. The condition `score_j < score_i` is strict because ratings must improve. The condition on directors prevents consecutive movies by the same director.

No special integer handling is needed because the answer is at most 3000.

# Worked Examples

For the sample:

```
6
2001 Nolan10 60
2004 Miyazaki 65
2002 Coppola 55
1999 Tarantino 50
2003 Cuaron 70
2005 Jeunet 80
```

After sorting by year:

| Movie | Year | Score | Director | dp |
| --- | --- | --- | --- | --- |
| Tarantino | 1999 | 50 | Tarantino | 1 |
| Nolan10 | 2001 | 60 | Nolan10 | 2 |
| Coppola | 2002 | 55 | Coppola | 1 |
| Cuaron | 2003 | 70 | Cuaron | 3 |
| Miyazaki | 2004 | 65 | Miyazaki | 3 |
| Jeunet | 2005 | 80 | Jeunet | 4 |

The best chain is:

```
Tarantino -> Nolan10 -> Cuaron -> Jeunet
```

with length 4.

Another example:

```
3
2000 A 50
2001 A 60
2002 B 70
```

| Movie | Year | Score | Director | dp |
| --- | --- | --- | --- | --- |
| A | 2000 | 50 | A | 1 |
| A | 2001 | 60 | A | 2 |
| B | 2002 | 70 | B | 3 |

The table above shows the transitions if we ignore the director restriction. The actual transition from the first A movie to the second A movie is invalid, so the real values are:

| Movie | Valid previous movies | dp |
| --- | --- | --- |
| A 2000 50 | none | 1 |
| A 2001 60 | none | 1 |
| B 2002 70 | either A movie | 2 |

The answer is 2, demonstrating why the director condition must be checked during transitions.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N^2)$ | Each movie checks all earlier movies after sorting |
| Space | $O(N)$ | Stores the movies and the dynamic programming values |

With $N \leq 3000$, the quadratic number of transitions is about nine million checks, which fits comfortably within the intended limits.

# Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    movies = []

    for _ in range(n):
        y, director, p = input().split()
        movies.append((int(y), int(p), director))

    movies.sort()

    dp = [1] * n
    ans = 1

    for i in range(n):
        yi, pi, di = movies[i]
        for j in range(i):
            yj, pj, dj = movies[j]
            if yj <= yi and pj < pi and dj != di:
                dp[i] = max(dp[i], dp[j] + 1)
        ans = max(ans, dp[i])

    return str(ans)

assert solve("""6
2001 Nolan10 60
2004 Miyazaki 65
2002 Coppola 55
1999 Tarantino 50
2003 Cuaron 70
2005 Jeunet 80
""") == "4"

assert solve("""3
2000 A 50
2001 A 60
2002 B 70
""") == "2"

assert solve("""1
2000 A 100
""") == "1"

assert solve("""5
2000 A 10
2000 B 20
2000 C 30
2001 D 40
2002 E 50
""") == "5"

assert solve("""4
2000 A 90
2001 B 80
2002 C 70
2003 D 60
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Original sample | 4 | Normal chaining across years |
| Same director in consecutive candidates | 2 | Director restriction |
| One movie | 1 | Minimum input size |
| Increasing ratings with same year | 5 | Same-year ordering |
| Decreasing ratings | 1 | Strict rating improvement |

# Edge Cases

For the same-director case:

```
3
2000 A 50
2001 A 60
2002 B 70
```

The algorithm sorts the movies in chronological order. When processing the second movie, it sees that the first movie has a valid year and rating relationship but the same director, so the transition is rejected. The third movie can extend either single-movie marathon, giving an answer of 2.

For equal ratings:

```
3
2000 A 50
2001 B 50
2002 C 60
```

The first two movies cannot connect because the score does not increase. The last movie can follow either one because 50 is smaller than 60. The algorithm returns 2.

For a case where every transition fails:

```
2
2000 A 90
2001 B 80
```

The second movie has a later year but a lower rating, so it cannot extend the first movie. Both `dp` values remain 1, and the answer is 1.
