# Twitter Clone: RDB vs. Key-Value Store Performance Analysis

A database performance benchmarking project that simulates core Twitter functionality — posting tweets and fetching home timelines — to evaluate MySQL's throughput against Twitter's real-world scale requirements.

---

## Overview

Twitter processes an estimated 6,000–10,000 post requests and 200,000–300,000 timeline reads per second at peak load. This project builds a simplified version of that system in MySQL and measures how far a single-machine relational database can get before hitting its limits.

The goal was not to replicate Twitter — it was to understand at what point relational databases break down for high-throughput social media workloads, and why.

---

## Results

| Operation | Throughput |
|---|---|
| `post_tweet` | ~178 calls/sec |
| `get_home_timeline` | ~16.69 calls/sec |

Against Twitter's requirements of 6,000–10,000 writes/sec and 200,000–300,000 reads/sec, a single MySQL instance falls roughly **35x short on writes** and **12,000x short on reads**.

The timeline read bottleneck is expected — fetching a user's home timeline requires joining tweets across all followed accounts, which scales poorly as follower counts grow. Indexing `user_id` in the tweets table and `follower_id` in the follows table improved read performance at the cost of insert speed.

---

## Schema

```
users       (user_id, username, created_at)
tweets      (tweet_id, user_id*, content, created_at)   -- indexed on user_id
follows     (follower_id*, followee_id)                  -- indexed on follower_id
```

The schema mirrors Twitter's core data model. The `get_home_timeline` query joins tweets against the follows table to fetch all tweets from accounts a user follows, ordered by recency.

---

## Why This Matters

Real systems like Twitter solve this with:
- **Key-value stores (Redis)** — caching precomputed timelines so reads are O(1) lookups
- **Write fanout** — pushing new tweets to follower timelines at write time rather than computing them at read time
- **Horizontal sharding** — distributing data across many database nodes

This benchmark makes the case for those architectural decisions concrete — the numbers show exactly where a naive relational approach breaks down.

---

## Hardware & Software

| Component | Spec |
|---|---|
| CPU | Intel Core i5-1135G7 @ 2.40GHz (4 core) |
| RAM | 15.71 GB |
| Disk | SK Hynix 512GB NVMe SSD |
| Database | MySQL 8.0.44 |
| Language | Python 3.9 |

---

## Takeaways

A single MySQL instance on consumer hardware can handle roughly 178 writes and 17 reads per second for a Twitter-like workload. Indexing improved read performance but hurt write throughput — a classic tradeoff in database design. At scale, a hybrid architecture combining a relational store with Redis caching would be necessary to approach Twitter's requirements.

---

*Built for DS 4300 — Large-Scale Storage and Retrieval, Northeastern University.*
