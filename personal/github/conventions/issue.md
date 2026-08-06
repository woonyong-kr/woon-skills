# 이슈 컨벤션

## 제목 형식

```
[bug] 설명
[feat] 설명
[docs] 설명
[question] 설명
[chore] 설명
```

예시:
```
[bug] 만료된 토큰으로 요청 시 500 반환
[feat] 리프레시 토큰 자동 갱신 기능 추가
[docs] 인증 흐름 다이어그램 필요
```

## 본문 템플릿: bug

```markdown
## 재현 방법

1. {단계 1}
2. {단계 2}

## 예상 동작

{어떻게 동작해야 하는지}

## 실제 동작

{실제로 어떻게 동작하는지}

## 환경

- OS:
- 버전:
```

## 본문 템플릿: feat

```markdown
## 목적

{왜 필요한지 1~2문장}

## 수용 기준

- [ ] {조건 1}
- [ ] {조건 2}
```

## 본문 템플릿: question / docs / chore

```markdown
{자유 서술. style.md 어투 규칙 적용}
```

## 라벨 자동 매핑

| 제목 태그 | GitHub 라벨 |
|----------|------------|
| bug      | bug |
| feat     | enhancement |
| docs     | documentation |
| question | question |
| chore    | maintenance |

## 금지 항목

style.md의 절대 금지 항목을 모두 따른다.
