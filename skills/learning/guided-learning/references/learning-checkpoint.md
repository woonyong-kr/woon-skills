# 학습 체크포인트 계약

## 읽기

대상 canonical 문서를 `woon_knowledge_get`으로 읽고 `## 학습 체크포인트`의 Core-owned block만 재개 상태로 사용한다.

- `범위`: 마지막으로 실제 다룬 장·문제·개념
- `상태`: `확인됨`, `부분 이해`, `다시 연습`
- `실행 증거`: 설명 재현, test·notebook 실행, 계산, 변형 문제 결과
- `아직 불안정함`: 틀림·모호함·누락 또는 미실행 범위
- `다음 인출 질문`: 다음 세션이 바로 시작할 질문 하나

본문의 목차·개념 설명·프로젝트 상태를 체크포인트로 대체하지 않는다. 날짜가 최신이라는 이유만으로 실행 증거보다 우선하지 않는다.

## 쓰기

세션 종료 직전에 canonical 문서를 다시 읽어 최신 revision을 얻고 `woon_knowledge_learning_checkpoint`를 호출한다. CLI가 필요하면 같은 계약의 명령을 사용한다.

```bash
woon knowledge learning-checkpoint \
  --canonical-id <canonical-id> \
  --unit <학습-범위> \
  --status <confirmed|partial|retry> \
  --evidence <실행-또는-재현-근거> \
  --unstable <아직-불안정한-항목> \
  --next-question <다음-인출-질문> \
  --recorded-on <YYYY-MM-DD> \
  --expected-revision <현재-revision> \
  --vault <vault-path>
```

- `confirmed`, `partial`은 실제 evidence가 하나 이상이어야 한다.
- `partial`, `retry`는 unstable 항목이 하나 이상이어야 한다.
- 같은 상태를 다시 쓰면 새 기록을 만들지 않는다.
- revision 충돌이면 문서를 다시 읽고 사용자 답과 실행 결과를 보존해 병합한다.
- compiler 페이지는 새 curated source·claim·receipt로, 그 밖의 canonical 페이지는 YAML을 보존하는 Core body writer로 갱신한다.
- 새 주제를 배웠다는 이유만으로 새 진도 문서를 만들지 않는다. 독립 정본 조건을 충족할 때만 기존 Wiki 성장 절차를 사용한다.
