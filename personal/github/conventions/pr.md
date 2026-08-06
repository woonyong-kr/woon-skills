# PR 컨벤션

## 제목 규칙

commit-convention과 동일한 형식을 사용한다.

```
<type>: <한국어 제목>
```

예시:
```
feat: 로그인 API에 JWT 갱신 로직을 추가
fix: 만료된 토큰으로 요청 시 401 대신 500이 반환되는 오류를 수정
refactor: 인증 미들웨어를 컨트롤러에서 분리
docs: API 엔드포인트 명세를 README에 추가
```

## 본문 템플릿

```markdown
## 변경 내용

{변경 이유와 결과를 3~5문장으로 서술. style.md 어투 규칙 적용}

## 테스트 방법

1. {검증 단계 1}
2. {검증 단계 2}

## 관련 이슈

closes #{이슈 번호}
```

관련 이슈가 없으면 "관련 이슈" 섹션을 생략한다.
테스트 방법이 자명하면 해당 섹션을 생략한다.

## 라벨 자동 매핑

| 커밋 타입 | GitHub 라벨 |
|-----------|------------|
| feat      | enhancement |
| fix       | bug |
| docs      | documentation |
| refactor  | refactor |
| test      | test |
| chore     | maintenance |
| perf      | performance |
| build     | build |
| ci        | ci |

## Draft 규칙

작업이 진행 중이거나 리뷰 준비가 안 된 경우에만 Draft로 생성한다.
사용자가 명시적으로 요청하지 않으면 일반 PR로 생성한다.

## 금지 항목

style.md의 절대 금지 항목을 모두 따른다.
PR 본문에 "이 PR은 ~을 구현합니다" 같은 영문 요약을 추가하지 않는다.
