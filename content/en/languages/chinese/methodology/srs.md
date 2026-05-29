---
title: "Spaced Repetition (SRS)"
description: "Complete guide to spaced repetition for Mandarin Chinese: Anki setup, optimal settings, what to put in SRS, Pleco integration, Skritter, and daily habit tips."
tags: ["chinese", "mandarin", "srs", "anki", "spaced repetition", "vocabulary", "methodology", "pleco", "skritter"]
cascade:
  type: docs
date: 2026-05-30T00:00:00+07:00
---

Spaced Repetition Systems (SRS) are the single highest-ROI study habit for Mandarin vocabulary. 15–20 minutes of consistent Anki practice daily outperforms hours of unfocused re-reading or passive review.

---

## What SRS Is and Why It Works

The **Ebbinghaus forgetting curve** (1885) describes how memory decays exponentially after initial learning. Without review, you forget ~70% of new material within 24 hours and ~90% within a week.

SRS exploits the **spacing effect**: reviewing information at the exact moment you are about to forget it is dramatically more efficient than massed repetition ("cramming"). Each successful review pushes the next review interval further into the future:

```
Day 0: Learn new card
Day 1: Review (interval extends to 3 days)
Day 4: Review (interval extends to 8 days)
Day 12: Review (interval extends to 21 days)
Day 33: Review (interval extends to ~2 months)
...
```

For Chinese vocabulary, this means a word you study today can be maintained with a single 10-second review every few months once it is deeply encoded — instead of re-learning it every week.

---

## Optimal Intervals for Chinese Vocabulary

Chinese vocabulary requires slightly more reinforcement than European language vocabulary because:
- Character forms must be memorized (not cognates)
- Tones must be memorized alongside the word
- Usage context is important (measure words, collocations)

**Recommended Anki settings:**

| Setting | Value | Reason |
|---------|-------|--------|
| New cards per day | 15–20 | Sustainable without backlog explosion |
| Maximum reviews per day | 200 | Cap prevents overwhelming days |
| Graduating interval | 1 day | Short initial spacing for new cards |
| Easy interval | 4 days | Prevents easy cards from disappearing |
| Starting ease | 250% | Standard; reduce to 230% if retention is low |
| Interval modifier | 100% (default) | Adjust if retention is consistently above 95% |

Target retention rate: **90–93%**. If you are consistently above 95%, your intervals are too short (increase interval modifier). Below 85%, reduce new card rate and let reviews catch up.

---

## Anki Setup Guide

### Step 1: Download Anki

- **Desktop** (Windows/Mac/Linux): Free at [apps.ankiweb.net](https://apps.ankiweb.net/)
- **Android**: AnkiDroid — Free on Google Play
- **iOS**: AnkiMobile — $24.99 one-time purchase (funds Anki development)

Sync with a free AnkiWeb account to keep all devices in sync.

### Step 2: Get the Best Deck

1. Open Anki → **Get Shared** (or visit [ankiweb.net/shared/decks](https://ankiweb.net/shared/decks/))
2. Search: **"HSK 3.0"** — choose a deck with audio, characters, and pinyin
3. Alternative: search **"Spoonfed Chinese"** for a sentence-level deck (better for intermediate learners)
4. Import the `.apkg` file

**Recommended decks:**
- HSK 3.0 Complete (vocabulary level, beginner-friendly)
- Spoonfed Chinese (sentence level, better grammar acquisition)
- Hanping Chinese (includes audio from Pleco)

### Step 3: Card Settings

Navigate to the deck → **Options**:

```
Daily Limits:
  New cards/day: 15
  Maximum reviews/day: 200

New Cards:
  Learning steps: 1m 10m
  Graduating interval: 1
  Easy interval: 4
  Starting ease: 250%

Reviews:
  Maximum interval: 36500 (100 years — no artificial cap)
  Easy bonus: 130%
  Interval modifier: 100%
```

### Step 4: Card Format

The ideal Chinese vocabulary card format:

**Front:**
```
[Simplified Chinese character(s)]
```

**Back:**
```
[Pinyin with tone marks]
[English translation]
[Example sentence in Chinese]
[Example sentence translation]
[Audio pronunciation]
```

Example:
- Front: 图书馆
- Back: túshūguǎn / library / 我在图书馆学习。/ I study in the library.

Seeing the character first (without pinyin) forces active recall — the most effective recall direction for reading Chinese.

---

## What to Put in SRS vs. Not

### Put in SRS

| Content | Why |
|---------|-----|
| New vocabulary (character + pinyin + meaning) | Core function of SRS |
| Grammar patterns as sentence examples | Internalizes structure through repetition |
| Measure word + noun pairs (一本书, 一张桌子) | These collocations must be memorized |
| Chengyu definitions and example sentences | High forgetting rate without spaced review |
| Commonly confused characters (买/卖, 已/己) | Targeted visual discrimination |

### Do NOT Put in SRS

| Content | Why Not |
|---------|---------|
| Stroke order | Use Skritter instead — it tests actual drawing |
| Grammar rule explanations | Rules are reference material, not recall targets |
| Pronunciation rules | Learn once; they apply systematically |
| Very simple words you already know | Wasted review time |
| Entire paragraphs | Too long for effective recall cards |

---

## Sentence Mining

Sentence mining means adding vocabulary cards from material you are actually reading or listening to. This is more effective than pre-made decks at intermediate+ level because:
- Words appear in context you care about
- The example sentence is one you already encountered
- Vocabulary density matches your current level

**Mining workflow with Du Chinese:**
1. Read an article in Du Chinese; tap unknown words
2. Du Chinese shows definition + example sentence
3. Export flagged words to CSV
4. Import CSV into Anki as new cards

**Mining workflow with Pleco:**
1. Encounter unknown word in any text
2. Copy word → Pleco lookup → tap star to add to flashcard list
3. Export Pleco flashcard list → import into Anki
4. (Or use Pleco's built-in flashcard system directly)

---

## Pleco Integration

[Pleco](https://www.pleco.com/) is the essential Chinese dictionary app. It has its own SRS flashcard system that can serve as an Anki alternative or supplement.

**Pleco → Anki export:**
1. In Pleco: **Flashcards** → **My Cards** → select cards to export
2. Export as text file (.txt) to your device
3. In Anki: **Import File** → map fields to Front/Back
4. Result: all Pleco-starred words become Anki cards with definitions

**Using Pleco's built-in flashcard system:**
- Simpler setup than Anki; fewer configuration options
- Good for learners who want minimal friction
- Lacks Anki's ecosystem (plugins, custom card types, statistics depth)

---

## Skritter

[Skritter](https://www.skritter.com/) is character-specific SRS with stroke feedback. Unlike Anki, it requires you to write the character by tracing strokes in correct order — the system detects errors.

**When to use Skritter:**
- If you need to handwrite Chinese (study in China, calligraphy, formal writing)
- To distinguish visually similar characters through motor memory
- As a supplement to Anki, not a replacement

**Skritter is not necessary if:**
- You only need to read and type Chinese (keyboard input does not require stroke memory)
- Budget is limited ($14.99/month subscription)

---

## Recovering From Falling Behind

Skipping even 3 days causes a significant review backlog. Missing a week with 20 new cards/day creates 140 overdue cards plus accumulated review cards — easily 300+ reviews.

**Recovery protocol:**
1. **Stop all new cards immediately** — set new cards/day to 0
2. **Clear the backlog first** — work through overdue reviews over several days
3. **Resume new cards slowly** — restart at 10/day, not your previous rate
4. **Never delete cards** — burying temporarily is better than deleting; buried cards return automatically

**Prevention:** Set a daily review alarm at the same time every day (morning is optimal — memory consolidation occurs overnight). Even 10 minutes is better than zero.

---

## Daily SRS Habit

**15–20 minutes every morning, before other study.**

This positioning matters:
- Reviews are due based on the previous day; doing them in the morning minimizes overdue time
- Willpower is highest in the morning
- Completing SRS first removes guilt and frees the rest of study time for input

**Habit stacking:** Attach Anki to an existing morning habit. Coffee + Anki. Commute + Anki (mobile). Breakfast + Anki. The trigger makes the habit automatic.

**Do not let the queue build.** A 300-card backlog takes ~40 minutes to clear and destroys motivation. The cost of one skipped day is steep. Consistency is more important than quantity per session.

---

## See Also

- [Roadmap](roadmap/) — When to add SRS into your study schedule
- [Common Mistakes](common-mistakes/) — Over-relying on SRS as the only study method
- [Vocabulary](../vocabulary/) — HSK vocabulary lists
- [Resources](../resources/) — Pleco, Skritter, and Anki links
