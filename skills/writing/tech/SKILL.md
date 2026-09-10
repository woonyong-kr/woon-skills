---
name: tech
description: 기술 블로그, 학습 글, engineering note를 근거 중심의 한국어 Markdown으로 작성·재구성·검수할 때 사용한다.
---

# Tech

독자가 먼저 알아야 할 결론·문제와 조건·판단·실행 또는 원리·증거·한계·다음 질문을 빠뜨리지 않는다. 다만 학습 문서는 이 순서를 고정 목차로 쓰지 않고, 독자가 이미 본 장면과 이번에 답할 질문에 맞춰 시작점과 설명 순서를 고른다. 원본의 기술 사실과 source identifier를 보존하고, 새 사실은 공식 출처나 실행 결과로 확인한다.

기술 블로그는 독자가 재사용할 하나의 engineering 질문에 답한다. 채용용 자기소개, 역할 요약과 성과 카드 문법을 섞지 않는다. private 정본을 블로그 candidate로 바꾸거나 같은 근거로 포트폴리오도 함께 만들 때는 `$site-promotion`이 공개 경계와 두 산출물의 claim 일관성을 먼저 소유한다.

한국어 문장과 어조의 교정은 [공통 문장 교정](repo://skills/skills/writing/humanize/SKILL.md)을 적용한다. `$tech`는 기술 사실, 학습 전개와 실행 증거를 소유하며 같은 문체 규칙을 따로 만들지 않는다. 성능·정확도 숫자에는 dataset, 환경, 횟수와 측정 방식을 붙인다. diagram은 prose보다 관계를 명확히 할 때만 `$diagram`으로 만든다.

일반 기술 글에서 한국어 문장, 제목, code·output 연결과 증거 표기 기준이 필요하면 [style guide](references/style-guide.md)를 읽는다. 학습 문서는 아래 learning-content 표준이 같은 영역을 더 구체적으로 소유하므로 별도 tone 요구가 없으면 style guide를 함께 읽지 않는다. 이 reference는 저장소별 frontmatter를 소유하지 않는다.

학습 문서에는 아래 명령으로 quality gate, 적응형 writing harness와 표본 근거를 읽는다. 같은 revision을 이미 읽었다면 재사용하고 필요한 reference만 추가 확인한다. 이 계약의 source 보존·근거·학습 품질 기준을 현재 요청의 목적과 범위에 맞게 적용한다.

```bash
bash "$(woon resolve repo://skills/skills/writing/tech/scripts/learning-context.sh)"
```

요청받은 주제 하나를 독자가 따라 읽는 작은 교과서 한 장으로 보고, 정의를 요약하는 참고 문서처럼 쓰지 않는다. 정본·검색 책임은 source/claim/page/receipt와 heading 구조가, 설명과 강의 책임은 하나의 한국어 본문이 맡는다. LLM 검색을 위해 본문을 키워드 나열이나 기계적으로 짧은 문장으로 바꾸지 않는다. 하네스는 주제·증거·독자에 필요한 route만 고르며 같은 heading 수나 문장 수를 강요하지 않는다. 사용자의 현재 형식·구조 지시를 우선하고 적용되지 않는 gate를 기계적으로 강제하지 않는다. 실제 충돌이 있으면 산출물 밖에서 영향을 한 문장으로 설명하되 아직 설명하지 않은 용어를 반복하지 않는다. 첫 본문 문장은 선택한 route에 맞는 구체적인 목표, 자료, 현재 상태, 판단 장면 또는 실패를 잡는다. 코드 실행이 없는 기록·결정·참고 문서에 가상의 실패나 실행 결과를 만들지 않는다. source 보존·근거·공개 경계가 달라지는 요청은 해당 소유 skill의 계약에 따라 처리한다.

작성하거나 변경한 `text`·`console` output의 근거 상태를 확인하고 같은 source·환경에서 검증한 output은 재사용한다. 일반 학습 글은 각 fence가 실제 compile·run 결과인지 미실행 예상 결과인지 명시한다. 책의 `source-landed`·`translated` leaf에는 원문 밖 `검증 상태` 라벨을 삽입하지 않고 source coverage manifest와 receipt에만 실행 여부를 기록한다. 첫 실행 예제만 확인하고 연습·반례의 output을 건너뛰지 않는다. output fence 안에 shell command가 있거나, 독립 실행할 수 없는 부분 snippet에 결과가 붙으면 command를 분리하고 완전한 source로 검증한다.

학습 문서의 3-participant `sequenceDiagram`은 `$diagram`의 Obsidian 폭·init 계약을 적용한다. 현재 diagram과 renderer로 통과한 검증 근거를 재사용하고, source가 바뀌었을 때만 다시 확인한다.

Mermaid fence 직전에는 그림이 답할 질문을 한 문장으로 둔다. 코드·실행 흐름 그림은 실제 identifier를 포함하고 `?` 또는 `하는가.`로 끝나게 하며, 조사·결정·일반 구조 그림은 source에 있는 안정적인 역할·행위자·개념 이름을 사용한다. heading이나 장식적 설명만 두고 그림을 시작하지 않는다.

Obsidian 정본으로 저장할 때는 `$archive`가 frontmatter·H1 envelope를 소유한다. `$tech`는 H2 이하의 검증된 본문만 넘기고 metadata를 복제하지 않는다. 독립 학습 Markdown은 학습 목표를 드러내는 H1을 정확히 하나 두고, 그 밖의 공개 글은 대상 저장소 계약에 따라 H1·frontmatter를 정한다.
