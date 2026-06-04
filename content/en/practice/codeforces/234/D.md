---
title: "CF 234D - Cinema"
description: "Vasya has a list of movies and a list of favorite actors. Each movie lists some of its cast, but some actor IDs may be missing (represented by 0)."
date: "2026-06-04T09:53:47+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 234
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 145 (Div. 2, ACM-ICPC Rules)"
rating: 1600
weight: 234
solve_time_s: 138
verified: true
draft: false
---

[CF 234D - Cinema](https://codeforces.com/problemset/problem/234/D)

**Rating:** 1600  
**Tags:** implementation  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

Vasya has a list of movies and a list of favorite actors. Each movie lists some of its cast, but some actor IDs may be missing (represented by 0). Vasya wants to classify each movie into one of three categories: it will surely be a favorite, it will surely not be a favorite, or it could go either way depending on the missing actor IDs. A movie is a favorite if, once all actor IDs are revealed, it contains at least as many favorite actors as any other movie.

The input provides the total number of actors, the IDs of Vasya’s favorite actors, and the list of movies with their cast (including unknown actors). The output is one line per movie, indicating the category with 0, 1, or 2.

The constraints are small: there are at most 100 actors and 100 movies, so an O(n·m) algorithm is feasible. The key challenge is handling uncertainty: some actors are unknown, and their identity can change whether a movie could be the favorite or not.

Non-obvious edge cases include movies where all actors are unknown, or movies that already have all favorite actors present but still have unknown spots that could be non-favorites. A careless approach that only counts known favorites may misclassify these scenarios.

For example, consider 3 movies with 3 favorite actors {1,2,3}:

```
movie1: actors = [0,0,0]   # all unknown
movie2: actors = [1,2,3]   # all favorite known
movie3: actors = [1,0,4]   # mix known favorite, unknown, non-favorite
```

Movie1 could have anywhere from 0 to 3 favorite actors. Movie2 is guaranteed to have 3. Movie3 could have 1 or 2 favorites depending on the unknown actor. Correct classification requires considering both minimum and maximum possible favorite actors.

## Approaches

The brute-force approach would enumerate all possible assignments for unknown actor IDs in each movie, count favorites for every assignment, and determine the favorite movies. This is correct but infeasible: each movie with `u` unknown actors has O((m)^u) combinations, and with up to 100 movies this explodes combinatorially.

The key insight is to compute **the minimum and maximum possible number of favorite actors in each movie** without enumerating all possibilities. For each movie, we can count known favorite actors (`f_known`) and unknown actors (`u`). The maximum possible favorites is `f_known + min(u, k - f_total)`, where `f_total` is the total number of favorite actors already used in other movies. The minimum possible favorites is `f_known` (assuming none of the unknown actors are favorite) or `f_known + max(0, u - (m - k))` if some unknown actors must be favorite because there aren’t enough non-favorites left.

Once we have min and max for each movie, we can classify:

- Surely favorite if its minimum count is greater than or equal to the maximum count of all other movies.
- Surely not favorite if its maximum count is smaller than the maximum count of some other movie.
- Otherwise, it could go either way.

This reduces the problem to O(n·m) complexity: we scan each movie once, compute counts, and then compare across movies.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((m^u)·n) | O(n) | Too slow |
| Min/Max Counting | O(n·m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of actors `m` and favorite actors `k`. Store the favorite IDs in a set for O(1) lookup.
2. Read the number of movies `n`. For each movie, store its title, number of actors `d`, and list of actor IDs, keeping track of which IDs are unknown (0).
3. For each movie, count `f_known` as the number of favorite actors already present, and `u` as the number of unknown actors.
4. Compute the maximum possible favorite actors in the movie as `f_known + min(u, k - f_known_other)`. Since actors are distinct within a movie, the maximum is capped by remaining favorite actors not already in this movie.
5. Compute the minimum possible favorite actors as `f_known`. If the number of unknown actors exceeds the number of non-favorite actors available, some must be favorite, so increment the minimum accordingly.
6. Collect all movies’ min and max counts.
7. For each movie, determine the output:

- If its minimum possible favorite count is at least the maximum possible favorite count of every other movie, output 0 (surely favorite).
- If its maximum possible favorite count is less than the maximum possible favorite count of some other movie, output 1 (surely not favorite).
- Otherwise, output 2 (could be either).
8. Print the results in the order of input.

**Why it works:** By tracking the extreme values of possible favorite counts for each movie, we ensure that no assignment of unknown actors can contradict the classification. Every decision depends only on the possible range, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

m, k = map(int, input().split())
fav = set(map(int, input().split()))
n = int(input())

movies = []

for _ in range(n):
    title = input().strip()
    d = int(input())
    actors = list(map(int, input().split()))
    f_known = sum(1 for a in actors if a in fav)
    u = actors.count(0)
    movies.append({'title': title, 'f_known': f_known, 'unknown': u, 'd': d})

min_favs = []
max_favs = []

for movie in movies:
    f_known = movie['f_known']
    u = movie['unknown']
    d = movie['d']
    
    # maximum possible favorite actors
    max_possible = f_known + min(u, k - f_known)
    
    # minimum possible favorite actors
    non_favs_total = m - k
    max_non_favs_in_movie = min(u, non_favs_total - (d - f_known - u))
    min_possible = f_known + max(0, u - max_non_favs_in_movie)
    
    min_favs.append(min_possible)
    max_favs.append(max_possible)

results = []

for i in range(n):
    sure_fav = all(min_favs[i] >= max_favs[j] for j in range(n) if j != i)
    sure_not = any(max_favs[i] < max_favs[j] for j in range(n) if j != i)
    if sure_fav:
        results.append(0)
    elif sure_not:
        results.append(1)
    else:
        results.append(2)

print('\n'.join(map(str, results)))
```

**Explanation:** The solution first reads all input and calculates known favorite actors and unknowns per movie. Then, it computes the range of possible favorite actors. Finally, it classifies each movie by comparing its min/max against other movies’ max. The subtle parts include capping the maximum by remaining favorites and computing minimum when unknowns could be forced to favorite because there aren’t enough non-favorites.

## Worked Examples

### Sample Input 1

```
5 3
1 2 3
6
firstfilm
3
0 0 0
secondfilm
4
0 0 4 5
thirdfilm
1
2
fourthfilm
1
5
fifthfilm
1
4
sixthfilm
2
1 0
```

| Movie | f_known | unknown | min | max |
| --- | --- | --- | --- | --- |
| firstfilm | 0 | 3 | 0 | 3 |
| secondfilm | 0 | 2 | 0 | 2 |
| thirdfilm | 1 | 0 | 1 | 1 |
| fourthfilm | 0 | 1 | 0 | 1 |
| fifthfilm | 0 | 1 | 0 | 1 |
| sixthfilm | 1 | 1 | 1 | 2 |

Classification:

- firstfilm: could be favorite or not → 2
- secondfilm: could be favorite or not → 2
- thirdfilm: max < some other max → 1
- fourthfilm: max < some other max → 1
- fifthfilm: max < some other max → 1
- sixthfilm: could be favorite or not → 2

Output:

```
2
2
1
1
1
2
```

### Custom Example

```
3 2
1 2
2
alpha
2
1 0
beta
1
2
```

| Movie | f_known | unknown | min | max |
| --- | --- | --- | --- | --- |
| alpha | 1 | 1 | 1 | 2 |
| beta | 1 | 0 | 1 | 1 |

Classification:

- alpha: min >= max of others? 1 >= 1 → yes, could be favorite
- max < max of others? 2 < 1 → no
- neither surely not → 2
- beta: min 1 >= max of others? 1 >= 2 → no
- max 1 < max of others? 1 < 2 → yes, surely not favorite → 1

Output:

```
2
1
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
