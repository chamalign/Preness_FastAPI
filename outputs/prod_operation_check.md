# 本番運用チェック結果

- 実行日時: 2026-03-25 15:16:14
- 対象: FastAPI カレントディレクトリ

## 1) 自動チェック結果

### A. 単体/結線テスト
- コマンド: `.venv-py313/bin/python -m pytest tests/ -v`
- 結果: **PASS (8/8)**
  - `tests/test_import_pipeline.py` 5件
  - `tests/test_report_generator_short.py` 3件

### B. ルート登録
- コマンド: app 起動時ルート列挙
- 結果: **PASS**
- 確認済み import ルート:
  - `/api/v1/import/full_mock`
  - `/api/v1/import/short_mock`
  - `/api/v1/import/practice`

### C. 参考
- 上記はローカルコード/モック範囲での成功。
- OpenAI/Azure/S3/Redis/PostgreSQL を実際に叩く E2E は未実行。

## 2) 本番E2Eで通すべき最終チェック（未実行）

1. DB/Redis 到達性 (`DATABASE_URL`, `REDIS_URL`)
2. 認証 (CONTENT_SOURCE_API_KEY / ANALYSIS_API_KEY)
3. `POST /api/v1/import/full_mock` 実投入で 201 + `mock_id`
4. `POST /api/v1/import/short_mock` 実投入で 201 + `mock_id`
5. `POST /api/v1/import/practice` 実投入で 201 + `exercise_ids`
6. `GET /api/v1/mocks/{id}` / `GET /api/v1/exercises/{id}` で URL 含むデータ取得
7. `POST /api/v1/generation/jobs` -> `GET /api/v1/generation/jobs/{job_id}` completed
8. `POST /api/v1/analysis/jobs` & `/analysis/short/jobs` -> `GET /analysis/jobs/{job_id}` result

## 3) Rails に渡す形式（FastAPI から取得する形）

### FM/SM（Mock）
- 取得: `GET /api/v1/mocks/{mock_id}`
- 形: `MockCreate`
```json
{
  "title": "...",
  "sections": [
    {
      "section_type": "listening|structure|reading",
      "display_order": 1,
      "parts": [
        {
          "part_type": "part_a|part_b|part_c|passages",
          "question_sets": [
            {
              "conversation_audio_url": "https://...",
              "questions": [{ "question_audio_url": "https://...", "correct_choice": "a" }]
            }
          ]
        }
      ]
    }
  ]
}
```

### P（Exercise）
- 取得: `GET /api/v1/exercises/{exercise_id}`
- 形: `ExerciseCreate`
```json
{
  "section_type": "listening|structure|reading",
  "part_type": "part_a|part_b|part_c|passages",
  "question_sets": [
    {
      "conversation_audio_url": "https://...",
      "questions": [{ "question_audio_url": "https://..." }]
    }
  ]
}
```

### 分析レポート（FM/SM）
- 取得: `GET /api/v1/analysis/jobs/{job_id}`
- 形: `AnalysisJobStatus`
```json
{
  "job_id": "uuid",
  "job_type": "full|short",
  "status": "queued|running|completed|failed",
  "result": {
    "meta": { "title": "..." },
    "scores": { "total": 0 },
    "tag_accuracy": {}
  },
  "error_message": null
}
```

## 4) 判定

- **コード実装/ローカルテスト範囲: 合格**
- **本番運用の最終合格: 外部依存を含む E2E の実行結果待ち**
