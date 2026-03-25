# API仕様書

## 問題投入API

### 概要

- **データ投入元:** 外部の問題生成アプリケーション（FastAPI）からPOSTリクエストを受け取ります。
- **Rails 同期:** FastAPI が受け取った問題データを自 DB に保存し、Rails は GET API で FastAPI から取得して同期・参照する前提です。
- **管理画面:** 不要（問題の確認・編集もAPIのみで行い、DBに直接反映されます）
- **認証方式:** API キー（`Authorization: Bearer <key>` または `X-Api-Key`）。GET は Rails 同期用に同じ API キーまたは専用キーを利用可能。
- **許可IP:** 環境変数 `ALLOWED_CONTENT_SOURCE_IPS` で送信元制限を行う場合もある。

### エンドポイント一覧

| エンドポイント | 用途 |
| --- | --- |
| `POST /api/v1/mocks` | 模擬試験の問題投入 |
| `GET /api/v1/mocks` | 模擬試験一覧取得（Rails 同期用） |
| `GET /api/v1/mocks/{mock_id}` | 模擬試験 1 件取得（Rails 同期用） |
| `POST /api/v1/exercises` | セクション別演習の問題投入 |
| `GET /api/v1/exercises` | セクション別演習一覧取得（Rails 同期用） |
| `GET /api/v1/exercises/{exercise_id}` | セクション別演習 1 件取得（Rails 同期用） |

---

## POST /api/v1/mocks

模擬試験は投入されたセクション構成に従って表示されます。

### リクエストスキーマ

```json
{
  "title": "模擬試験 Vol.1",
  "sections": [
    {
      "section_type": "listening",
      "display_order": 1,
      "parts": [
        {
          "part_type": "part_a",
          "display_order": 1,
          "question_sets": [
            {
              "display_order": 1,
              "questions": [
                {
                  "display_order": 1,
                  "question_text": "What does the woman imply?",
                  "scripts": [
                    { "speaker": "narrator", "text": "Question 1." },
                    { "speaker": "man", "text": "Excuse me, do you know if this book is available?" },
                    { "speaker": "woman", "text": "It might be on reserve at the front desk." },
                    { "speaker": "narrator", "text": "What does the woman imply?" }
                  ],
                  "audio_url": "<https://preness-listening-audio.s3.ap-northeast-1.amazonaws.com/PartB_02.wav>",
                  "choice_a": "The man should buy the book online.",
                  "choice_b": "The book might be held at a specific location.",
                  "choice_c": "The library is closed for research.",
                  "choice_d": "She has the book in her dorm room.",
                  "correct_choice": "B",
                  "explanation": "女性は本が“on reserve”かもしれないと言っており、特定の場所（フロントデスク）に保管されている可能性を示唆している。", 
                  "tag": "shortConv",
                  "wrong_reason_a": "Reason A is wrong, or null if correct",
                  "wrong_reason_b": "Reason B is wrong, or null if correct",
                  "wrong_reason_c": "Reason C is wrong, or null if correct",
                  "wrong_reason_d": "Reason D is wrong, or null if correct"
                }
              ]
            }
          ]
        },
        {
          "part_type": "part_b",
          "display_order": 2,
          "question_sets": [
            {
              "display_order": 1,
              "audio_url": "<https://preness-listening-audio.s3.ap-northeast-1.amazonaws.com/PartB_02.wav>",
              "questions": [
                {
                  "display_order": 1,
                  "question_text": "What are the students mainly discussing?",
                  "choice_a": "Their plans for the upcoming weekend.",
                  "choice_b": "A research project for their biology class.",
                  "choice_c": "The requirements for a new scholarship.",
                  "choice_d": "How to organize a student study group.",
                  "correct_choice": "B",
                  "explanation": "会話の冒頭で生物学のプロジェクトについて話し合っているため。", 
                  "tag": "shortConv",
                  "wrong_reason_a": "Reason A is wrong, or null if correct",
                  "wrong_reason_b": "Reason B is wrong, or null if correct",
                  "wrong_reason_c": "Reason C is wrong, or null if correct",
                  "wrong_reason_d": "Reason D is wrong, or null if correct"
                }
              ]
            }
          ]
        },
        {
          "part_type": "part_c",
          "display_order": 3,
          "question_sets": [
            {
              "display_order": 1,
              "audio_url": "<https://preness-listening-audio.s3.ap-northeast-1.amazonaws.com/PartB_02.wav>",
              "questions": [
                {
                  "display_order": 1,
                  "question_text": "What is the purpose of the talk?",
                  "choice_a": "To introduce new students to the campus library.",
                  "choice_b": "To explain the history of the university.",
                  "choice_c": "To discuss the benefits of a specific major.",
                  "choice_d": "To announce a change in the graduation requirements.",
                  "correct_choice": "A",
                  "explanation": "話し手は図書館の利用方法について説明しているため。", 
                  "tag": "shortConv",
                  "wrong_reason_a": "Reason A is wrong, or null if correct",
                  "wrong_reason_b": "Reason B is wrong, or null if correct",
                  "wrong_reason_c": "Reason C is wrong, or null if correct",
                  "wrong_reason_d": "Reason D is wrong, or null if correct"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "section_type": "structure",
      "display_order": 2,
      "parts": [
        {
          "part_type": "part_a",
          "display_order": 1,
          "question_sets": [
            {
              "display_order": 1,
              "questions": [
                {
                  "display_order": 1,
                  "question_text": "The Eiffel Tower ------- in 1889 for the World's Fair.",
                  "choice_a": "was built",
                  "choice_b": "building",
                  "choice_c": "built",
                  "choice_d": "to build",
                  "correct_choice": "A",
                  "explanation": "受動態の形が必要。", 
                  "tag": "shortConv",
                  "wrong_reason_a": "Reason A is wrong, or null if correct",
                  "wrong_reason_b": "Reason B is wrong, or null if correct",
                  "wrong_reason_c": "Reason C is wrong, or null if correct",
                  "wrong_reason_d": "Reason D is wrong, or null if correct"
                }
              ]
            }
          ]
        },
        {
          "part_type": "part_b",
          "display_order": 2,
          "question_sets": [
            {
              "display_order": 1,
              "questions": [
                {
                  "display_order": 1,
                  "question_text": "The (A) beautifully flowers (B) in the garden (C) are blooming (D) now.",
                  "choice_a": "A",
                  "choice_b": "B",
                  "choice_c": "C",
                  "choice_d": "D",
                  "correct_choice": "A",
                  "explanation": "副詞 beautifully ではなく、形容詞 beautiful が名詞 flowers を修飾すべき。", 
                  "tag": "shortConv",
                  "wrong_reason_a": "Reason A is wrong, or null if correct",
                  "wrong_reason_b": "Reason B is wrong, or null if correct",
                  "wrong_reason_c": "Reason C is wrong, or null if correct",
                  "wrong_reason_d": "Reason D is wrong, or null if correct"
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "section_type": "reading",
      "display_order": 3,
      "parts": [
        {
          "part_type": "passages",
          "display_order": 1,
          "question_sets": [
            {
              "display_order": 1,
              "passage": "Modern computers are capable of performing billions of operations per second. This remarkable speed has revolutionized many fields, including science, engineering, and finance...",
              "questions": [
                {
                  "display_order": 1,
                  "question_text": "What is the main topic of the passage?",
                  "choice_a": "The history of vacuum tubes.",
                  "choice_b": "The speed and impact of modern computers.",
                  "choice_c": "How to repair a broken computer.",
                  "choice_d": "The cost of manufacturing microchips.",
                  "correct_choice": "B",
                  "explanation": "コンピュータの速度とその影響について述べられているため。",
                  "tag": "shortConv",
                  "wrong_reason_a": "Reason A is wrong, or null if correct",
                  "wrong_reason_b": "Reason B is wrong, or null if correct",
                  "wrong_reason_c": "Reason C is wrong, or null if correct",
                  "wrong_reason_d": "Reason D is wrong, or null if correct"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

- `scripts` は Listening セクション専用の任意フィールドです。`[{ "speaker": "narrator"|"man"|"woman"|"break", "text": "..." }, ...]` 形式で会話・ナレーション全文を保持します。

### フィールド説明

| フィールド | 必須 | 説明 |
| --- | --- | --- |
| `title` | ✅ | 模擬試験タイトル |
| `sections[].section_type` | ✅ | `listening` / `structure` / `reading` |
| `sections[].display_order` | ✅ | 表示順（1始まり） |
| `parts[].part_type` | ✅ | `part_a` / `part_b` / `part_c` / `passages` |
| `parts[].display_order` | ✅ | 表示順 |
| `question_sets[].passage` | 条件付き | readingのみ必須 |
| `question_sets[].audio_url` | 任意 | Part B / C のセット共通音声のS3 URL |
| `questions[].audio_url` | 任意 | 問題個別音声のS3 URL |
| `questions[].explanation` | 任意 | 解説文 |

### バリデーション

- `sections` に `listening` / `structure` / `reading` の3つが全て含まれること
- `correct_choice` は `A` / `B` / `C` / `D` のいずれか
- `audio_url` が指定された場合、そのままDBに保存する（Active Storageは使用しない）

### レスポンス（成功時）

```json
{
  "status": "success",
  "mock_id": 1,
  "title": "模擬試験 Vol.1"
}
```

### レスポンス（失敗時）

```json
{
  "status": "error",
  "errors": ["Validation failed: title can't be blank"]
}
```

---

## POST /api/v1/exercises

セクション別演習はパート単位で追加可能（3セクション揃っていなくても可）。

### リクエストスキーマ

```json
{
  "section_type": "listening",
  "part_type": "part_a",
  "question_sets": [
    {
      "display_order": 1,
      "questions": [
        {
          "display_order": 1,
          "question_text": "What does the woman suggest?",
          "audio_url": "<https://s3.example.com/audio/practice_q1.mp3>",
          "choice_a": "...",
          "choice_b": "...",
          "choice_c": "...",
          "choice_d": "...",
          "correct_choice": "A",
          "explanation": "..."
          "tag": "shortConv",
          "wrong_reason_a": "Reason A is wrong, or null if correct",
          "wrong_reason_b": "Reason B is wrong, or null if correct",
          "wrong_reason_c": "Reason C is wrong, or null if correct",
          "wrong_reason_d": "Reason D is wrong, or null if correct"
        }
      ]
    }
  ]
}
```

### フィールド説明

| フィールド | 必須 | 説明 |
| --- | --- | --- |
| `section_type` | ✅ | `listening` / `structure` / `reading` |
| `part_type` | ✅ | `part_a` / `part_b` / `part_c` / `passages` |
| `question_sets` | ✅ | 1件以上 |
| `question_sets[].passage` | 条件付き | `reading` かつ `passages` の場合は必須 |
| `question_sets[].audio_url` | 任意 | Part B / C のセット共通音声 |
| `questions[].audio_url` | 任意 | 個別音声 |

### バリデーション

- `section_type` と `part_type` の組み合わせが有効であること（例: listeningにpassagesは不可）

### レスポンス（成功時）

```json
{
  "status": "success",
  "exercise_ids": [1],
  "created_count": 1
}
```

### レスポンス（失敗時）

POST /api/v1/mocks と同様に `{"status": "error", "errors": ["..."]}` 形式で返す。

---

## GET /api/v1/mocks（一覧）

Rails 同期用。保存済み模擬試験の一覧を id 降順で返す。

- **認証:** POST と同様に API キー必須。
- **クエリ:** `limit`（1〜500, デフォルト 100）, `offset`（デフォルト 0）。
- **レスポンス:** `[{"id": 1, "title": "模擬試験 Vol.1"}, ...]`

---

## GET /api/v1/mocks/{mock_id}（1 件）

Rails 同期用。指定した mock_id の模擬試験を 1 件返す。レスポンス形式は POST のリクエストスキーマと同形（`title`, `sections`）なので、Rails はそのまま取り込める。

- **認証:** API キー必須。
- **404:** 存在しない mock_id の場合は 404 を返す。

---

## GET /api/v1/exercises（一覧）

Rails 同期用。保存済みセクション別演習の一覧を id 降順で返す。

- **認証:** API キー必須。
- **クエリ:** `limit`（1〜500, デフォルト 100）, `offset`（デフォルト 0）。
- **レスポンス:** `[{"id": 1, "section_type": "listening", "part_type": "part_a"}, ...]`

---

## GET /api/v1/exercises/{exercise_id}（1 件）

Rails 同期用。指定した exercise_id の演習を 1 件返す。レスポンス形式は POST のリクエストスキーマと同形（`section_type`, `part_type`, `question_sets`）。

- **認証:** API キー必須。
- **404:** 存在しない exercise_id の場合は 404 を返す。