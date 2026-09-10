# Commit examples and related owners

메시지 규칙의 정본은 [Commit](../SKILL.md)이다. 이 파일은 예시와 소유권만 설명한다.

```text
fix(wiki): preserve link labels when retargeting pages
```

이유가 제목만으로 드러나지 않을 때:

```text
fix(tasks): preserve user notes when deleting recurring records

Remove only rows with the reviewed routine IDs. Reject changed daily
files before deletion so concurrent personal edits remain intact.
```

호환성을 깨는 변경은 실제 변경·migration이 확인된 경우에만 표시한다.

```text
feat(api)!: replace createRenderer with createRoot

BREAKING CHANGE: Call createRoot instead of createRenderer.
```

검증 본문은 실제 실행한 명령·결과가 리뷰에 필요할 때만 추가한다. 위 예시를 현재 작업의 실행 근거로 복사하지 않는다.

브랜치 전략·merge·rebase는 [Branch](../../branch/SKILL.md), 히스토리 복구는 [History](../../history/SKILL.md)가 소유한다. PR 작성은 [PR](../../../github/pr/SKILL.md)이 소유한다. 저장소 template이 있으면 따르고, 없으면 문제와 바뀐 동작을 먼저 설명한 뒤 실제 수행한 검증과 남은 한계를 적는다. 단순 변경에 해당하지 않는 테스트·문서 체크리스트를 만들지 않는다.
