 ``` plantuml
@startuml

' テーブル定義
entity "users" {
  *id : INTEGER <<PK>>
  --
  *username : VARCHAR(80) <<UQ>>
  *hashed_password : VARCHAR(80)
}

entity "quizzes" {
  *id : INTEGER <<PK>>
  --
  *university_name : VARCHAR(256)
  department_count : INTEGER = 0
  question_count : INTEGER = 0
  option_count : INTEGER = 0
  created_by : INTEGER <<FK>>
}

entity "departments" {
  *id : INTEGER <<PK>>
  --
  *department_name : VARCHAR(256)
  *quiz_id : INTEGER <<FK>>
}

entity "questions" {
  *id : INTEGER <<PK>>
  --
  *question_text : VARCHAR(256)
  *quiz_id : INTEGER <<FK>>
}

entity "options" {
  *id : INTEGER <<PK>>
  --
  *option_text : VARCHAR(256)
  *question_id : INTEGER <<FK>>
}

entity "scores" {
  *id : INTEGER <<PK>>
  --
  *score : INTEGER
  *department_id : INTEGER <<FK>>
  *option_id : INTEGER <<FK>>
}

' リレーションシップ
users ||--o{ quizzes : creates
quizzes ||--o{ departments : has
quizzes ||--o{ questions : contains
questions ||--o{ options : has
departments ||--o{ scores : achieves
options ||--o{ scores : receives

@enduml
 ```