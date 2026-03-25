# Horiba 準拠 FastAPI 問題投入 API 仕様

**規定:** 本 API の規定は `API仕様書.md` とする。本ドキュメントは規定に準拠しつつ、[hinatahoriba/Preness](https://github.com/hinatahoriba/Preness)（Horiba_Preness）の Rails バックエンド・DB との対応および実装上の差異を追記したものである。

**DB スキーマ参照:** [db/schema.rb](https://github.com/hinatahoriba/Preness/blob/main/db/schema.rb)

---

## 概要（規定に準拠）

- **データ投入元:** 外部の問題生成アプリケーション（FastAPI）から POST リクエストを受け取ります。
- **管理画面:** 不要（問題の確認・編集も API のみで行い、DB に直接反映されます）
- **認証方式（規定）:** 特定の送信元 IP アドレス制限
- **許可IP（規定）:** 環境変数 `ALLOWED_CONTENT_SOURCE_IPS` で管理

---

## エンドポイント一覧

| エンドポイント | 用途 |
| --- | --- |
| `POST /api/v1/mocks` | 模擬試験の問題投入 |
| `POST /api/v1/exercises` | セクション別演習の問題投入 |

---

## 認証

規定では送信元 IP アドレス制限（`ALLOWED_CONTENT_SOURCE_IPS`）を想定している。

**Horiba 実装上の認証:** 現状の Horiba Rails では API Key 認証を使用する。

- **ヘッダ:** `Authorization: Bearer <API_KEY>` または `X-Api-Key: <API_KEY>`
- **環境変数:** サーバ側で `CONTENT_SOURCE_API_KEY` を設定。クライアントは同じ値を渡す。
- **失敗時:** `401 Unauthorized`、body: `{ "status": "error", "errors": ["Unauthorized"] }`

---

## POST /api/v1/mocks

模擬試験は投入されたセクション構成に従って表示されます。規定と同様、**listening / structure / reading の 3 セクションがすべて必須。**

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
              "passage": null,
              "audio_url": "https://example.com/part_b_02.wav",
              "questions": [
                {
                  "display_order": 1,
                  "question_text": "What does the woman imply?",
                  "audio_url": "https://example.com/q1.wav",
                  "choice_a": "The man should buy the book online.",
                  "choice_b": "The book might be held at a specific location.",
                  "choice_c": "The library is closed for research.",
                  "choice_d": "She has the book in her dorm room.",
                  "correct_choice": "B",
                  "explanation": "女性は本が on reserve かもしれないと言っており、特定の場所に保管されている可能性を示唆している。",
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
              "passage": "Modern computers are capable of performing billions of operations per second...",
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

### フィールド説明（mocks）

規定に準拠。

| フィールド | 必須 | 説明 |
| --- | --- | --- |
| `title` | ✅ | 模擬試験タイトル |
| `sections[].section_type` | ✅ | `listening` / `structure` / `reading` |
| `sections[].display_order` | ✅ | 表示順（1始まり） |
| `parts[].part_type` | ✅ | `part_a` / `part_b` / `part_c` / `passages` |
| `parts[].display_order` | ✅ | 表示順 |
| `question_sets[].passage` | 条件付き | readingのみ必須 |
| `question_sets[].audio_url` | 任意 | Part B / C のセット共通音声の S3 URL |
| `question_sets[].display_order` | ✅ | 表示順 |
| `questions[].display_order` | ✅ | 表示順 |
| `questions[].question_text` | ✅ | 問題文 |
| `questions[].audio_url` | 任意 | 問題個別音声の S3 URL |
| `questions[].choice_a`～`choice_d` | ✅ | 選択肢 A～D |
| `questions[].correct_choice` | ✅ | 正解 `A`/`B`/`C`/`D` |
| `questions[].explanation` | 任意 | 解説文 |
| `questions[].tag` | 任意 | 規定で定義（例: shortConv） |
| `questions[].wrong_reason_a`～`wrong_reason_d` | 任意 | 規定で定義。不正解理由（正解の場合は null 可） |

**Horiba 実装・DB について:** 現状の [schema.rb](https://github.com/hinatahoriba/Preness/blob/main/db/schema.rb) の `questions` テーブルには `tag`, `wrong_reason_*` のカラムがない。規定に従って送信する場合は、Rails で保存するには DB マイグレーションおよび Strong Parameters の追加が必要。

### バリデーション（mocks）

規定と同様。

- `sections` に `listening` / `structure` / `reading` の3つが全て含まれること
- `correct_choice` は `A` / `B` / `C` / `D` のいずれか
- `audio_url` が指定された場合、そのまま DB に保存する（Active Storage は使用しない）

### レスポンス（成功時）

規定どおり。

```json
{
  "status": "success",
  "mock_id": 1,
  "title": "模擬試験 Vol.1"
}
```

規定では HTTP ステータスコードは明示されていない。Horiba 実装では `201 Created` を返す。

### レスポンス（失敗時）

規定どおり。

```json
{
  "status": "error",
  "errors": ["Validation failed: title can't be blank"]
}
```

Horiba 実装では `422 Unprocessable Entity` を返す。必須パラメータ不足時は `Parameter missing: <key>`、レコード不正時は `ActiveRecord::RecordInvalid` のメッセージが `errors` に含まれる。

---

## POST /api/v1/exercises

セクション別演習はパート単位で追加可能（3セクション揃っていなくても可）。規定と同様。

### リクエストスキーマ

規定に準拠。`questions` には規定どおり `tag`, `wrong_reason_a`～`wrong_reason_d` を含める。

```json
{
  "section_type": "listening",
  "part_type": "part_a",
  "question_sets": [
    {
      "display_order": 1,
      "passage": null,
      "audio_url": null,
      "questions": [
        {
          "display_order": 1,
          "question_text": "What does the woman suggest?",
          "audio_url": "https://s3.example.com/audio/practice_q1.mp3",
          "choice_a": "...",
          "choice_b": "...",
          "choice_c": "...",
          "choice_d": "...",
          "correct_choice": "A",
          "explanation": "...",
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

### セクション・パートの有効組み合わせ（exercises）

規定では「section_type と part_type の組み合わせが有効であること」とある。以下はその具体化（Horiba 実装での検証内容）。

| section_type | 有効な part_type |
| --- | --- |
| listening | part_a, part_b, part_c |
| structure | part_a, part_b |
| reading | passages |

### フィールド説明（exercises）

規定に準拠。

| フィールド | 必須 | 説明 |
| --- | --- | --- |
| `section_type` | ✅ | `listening` / `structure` / `reading` |
| `part_type` | ✅ | `part_a` / `part_b` / `part_c` / `passages`（上表の有効組み合わせ） |
| `question_sets` | ✅ | 1件以上 |
| `question_sets[].passage` | 条件付き | `reading` かつ `passages` の場合は必須 |
| `question_sets[].audio_url` | 任意 | Part B / C のセット共通音声 |
| `questions[].audio_url` | 任意 | 個別音声 |
| `questions[].tag`, `wrong_reason_a`～`wrong_reason_d` | 任意 | 規定で定義。mocks と同様。 |

### バリデーション（exercises）

規定と同様。

- `section_type` と `part_type` の組み合わせが有効であること（例: listening に passages は不可）

### レスポンス（成功時）

規定では成功時レスポンスは未定義。Horiba 実装では以下を返す。

- **Status:** `201 Created`
- **Body:**
```json
{
  "status": "success",
  "exercise_ids": [1, 2, 3],
  "created_count": 3
}
```

### レスポンス（失敗時）

規定では HTTP ステータスは明示されていない。Horiba 実装では `422 Unprocessable Entity`。Body 例:
```json
{
  "status": "error",
  "errors": ["Validation failed: invalid combination of section_type and part_type"]
}
```

```json
{
  "status": "error",
  "errors": ["Validation failed: question_sets must have at least 1 item"]
}
```

---

## データベーススキーマ（Horiba Rails 準拠）

**規定（API仕様書.md）には含まれない。Horiba 実装・FastAPI 実装のための補足。**

FastAPI から投入したデータが格納されるテーブルと、本 API で利用する主なカラムの対応。完全な定義は [db/schema.rb](https://github.com/hinatahoriba/Preness/blob/main/db/schema.rb) を参照。

### 問題投入で使用するテーブル

| テーブル | 説明 | 主なカラム |
| --- | --- | --- |
| **mocks** | 模擬試験 1 件 | id, title, created_at, updated_at |
| **exercises** | 演習 1 件（中身は section に紐づく） | id, created_at, updated_at |
| **sections** | セクション（polymorphic: sectionable_type/sectionable_id → Mock または Exercise） | id, sectionable_type, sectionable_id, section_type, display_order |
| **parts** | パート | id, section_id, part_type, display_order |
| **question_sets** | 問題セット（長文・音声共有単位） | id, part_id, passage, audio_url, display_order |
| **questions** | 問題 1 問 | id, question_set_id, display_order, question_text, audio_url, choice_a～d, correct_choice, explanation |

### その他関連テーブル（本 API では作成しない）

| テーブル | 説明 |
| --- | --- |
| users | ユーザ（Devise） |
| attempts | 受験履歴（mockable: Mock/Exercise） |
| answers | 解答（attempt_id, question_id, selected_choice, is_correct, skipped） |
| mock_tests | 有料模試メタ（Stripe 等） |
| purchases | 購入履歴 |
| subscriptions | サブスク |

### リレーション概要

- **Mock** has_many **sections** → Section has_many **parts** → Part has_many **question_sets** → QuestionSet has_many **questions**.
- **Exercise** has_many **sections** → 以降は上と同じ（parts → question_sets → questions）。

---

## FastAPI 実装時の注意

**規定（API仕様書.md）には含まれない。Horiba 実装・FastAPI 実装のための補足。**

1. **認証:** 規定では IP 制限。Horiba 実装では API Key を使用するため、全ての `/api/v1/*` リクエストに `Authorization: Bearer <CONTENT_SOURCE_API_KEY>` または `X-Api-Key: <CONTENT_SOURCE_API_KEY>` を付与する。
2. **Content-Type:** `application/json` で送信する。
3. **スキーマ整合:** 送信する JSON は規定のリクエストスキーマに合わせる。`tag`, `wrong_reason_a`～`wrong_reason_d` は規定で定義されているが、現状の Horiba DB にカラムが無い場合は Rails 側で保存されない（マイグレーション追加で対応可能）。
4. **scripts フィールド:** Listening 問題では `scripts`（listening_script 配列）を含めて送信できるが、現状の Horiba Rails の `questions` テーブルには対応カラムが無いため、そのままでは保存されない。必要に応じて Rails 側でカラム追加・Strong Parameters 拡張を行うか、API レスポンス時のみ利用する想定とする。
5. **エラー処理:** `status: "error"` かつ `errors` 配列をパースしてバリデーション・必須パラメータ不足を識別する。
