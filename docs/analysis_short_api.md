# Short 模試 分析レポート API

Full と同様 **各 `items[]` に `tag` が必須**. Listening Part 別・文法カテゴリ別・Reading タイプ別の正答率は **tag をキーに算出**する. 認証は `ANALYSIS_API_KEY`.

## 前提

- **L / S / R それぞれ 1 問以上** の `items` が必要.
- **passages**: 1 件以上. 各 `{ "theme", "question_ids": [ ... 1 本以上 ] }`. **passages 間で question_id 重複なし**. いずれも **Reading 設問** の ID のみ.

## tag の正規化 (任意)

`short_conv`→`shortConv` 等は [report_generator_short.py](../app/services/analysis/report_generator_short.py) の `TAG_ALIASES` / `KNOWN_TAGS` 参照. それ以外の文字列は **そのまま** tag キーになる.

## POST /api/v1/analysis/short/jobs

**レスポンス (202)**: `{ "job_id", "job_type": "short", "status": "queued" }`

## GET result (job_type=short)

| フィールド | 説明 |
|------------|------|
| `tag_accuracy` | `{ "listening": { tag: % }, "grammar": { ... }, "reading": { ... } }` |
| `latest` | 上記をフラットにした tag→% (UI 互換) |
| `passages` | `{ "theme", "score", "max" }`（max はその passage の設問数） |
| `scores` / `meta` / `narratives` | 従来どおり |

## エラー

- `tag` 空・L/S/R 欠落・passage が Reading 外 ID・passages 内重複 → 422 またはジョブ `failed`.
