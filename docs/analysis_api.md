# 分析レポート API (Full 模試)

Rails (Horiba_Preness) から **Full 模試** 終了後に呼び出す API. **Short 模試** は別途 [analysis_short_api.md](analysis_short_api.md) の `POST /api/v1/analysis/short/jobs` を使用する. ジョブは同一 `analysis_jobs` テーブルに保存され, `job_type` が `full` / `short` で区別される.

## 認証

- 問題投入 API とは **別の API キー** を使用する.
- 環境変数: `ANALYSIS_API_KEY`
- ヘッダ: `Authorization: Bearer <ANALYSIS_API_KEY>` または `X-Api-Key: <ANALYSIS_API_KEY>`

## エンドポイント

| メソッド | パス | 説明 |
|----------|------|------|
| POST | /api/v1/analysis/jobs | Full 分析ジョブを 1 件投入. 202 + job_id, job_type=full |
| POST | /api/v1/analysis/short/jobs | Short 分析ジョブ (別仕様). 詳細は analysis_short_api.md |
| GET | /api/v1/analysis/jobs/{job_id} | ジョブの状態と結果を取得. `job_type` と result の形に注意 |

## POST /api/v1/analysis/jobs

**リクエスト例**

```json
{
  "attempt_id": "123",
  "exam_type": "full",
  "student_name": "山田 太郎",
  "exam_date": "2026-02-10",
  "answers": [
    { "question_id": "456", "selected_choice": "B", "skipped": false }
  ],
  "items": [
    {
      "item_id": "456",
      "question_id": "456",
      "section_id": "L",
      "section_type": "listening",
      "part": "Part_A",
      "tag": "shortConv",
      "correct_choice": "B"
    }
  ]
}
```

- `item_id` と `question_id` は Rails の `question.id` を文字列で揃える.
- `section_id`: L / S / R または `section_type` から自動正規化（**必須**. 欠けるとエラー）.
- **`tag` は必須**（空不可）. Listening Part 別・文法カテゴリ別・Reading タイプ別の正答率は **tag をキー** に算出する.

**レスポンス (202 Accepted)**

```json
{
  "job_id": "uuid",
  "job_type": "full",
  "status": "queued"
}
```

## GET /api/v1/analysis/jobs/{job_id}

**レスポンス (200)**

- `job_type`: `full` | `short`
- `status`: `queued` | `running` | `completed` | `failed`
- `result`: `completed` のときのみ. **full**: meta / scores / **tag_accuracy** (listening・grammar・reading 配下が tag→正答率%) / narratives. **short**: tag_accuracy / latest / passages 等 (analysis_short_api.md).
- `error_message`: `failed` のときのみ.

## エラー形式 (問題投入 API と同じ)

- 404 Job not found: `{ "status": "error", "errors": ["Job not found"] }`
- 422 Validation: `{ "status": "error", "errors": ["Validation failed: ..."] }`

## 環境・起動

1. `.env` に `ANALYSIS_API_KEY`, `DATABASE_URL`, `REDIS_URL`, `OPENAI_API_KEY`(任意) を設定.
2. PostgreSQL と Redis を起動.
3. API サーバー: `uvicorn app.main:app --reload`
4. ワーカー: `celery -A app.workers.celery_app worker --loglevel=info`

初回起動時に `analysis_jobs` テーブルが自動作成される.
