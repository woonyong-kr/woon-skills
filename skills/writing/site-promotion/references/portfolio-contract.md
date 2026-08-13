# 포트폴리오 승격 계약

## 목적

포트폴리오는 평가자가 짧게 훑어도 `무슨 문제였는가`, `이 사람의 몫은 무엇인가`, `어떤 결과와 근거가 있는가`를 분리해 확인하게 한다. 기술 튜토리얼이나 블로그 목록을 메인 화면으로 만들지 않는다.

## Project candidate

다음 순서를 기본으로 하되 확인된 내용만 쓴다.

1. 한 줄 정의: 대상 시스템과 해결한 문제.
2. context: 팀 규모·기간·운영 조건. 팀 사실로 표시한다.
3. personal role: 직접 설계·구현·검증한 범위.
4. actions: 개인 행동과 중요한 기술 판단 2~4개.
5. outcomes: 조건이 완전한 실측치와 팀 성과를 소유권별로 분리.
6. evidence: public code·test·demo·blog·architecture로 한 번에 이동.
7. limits: 교육 프로젝트, prototype, 미운영, 공유 계정 같은 오해 가능성.

`우리`를 `내가`로 바꾸지 않는다. 팀 프로젝트 종료 뒤 개인 확장은 `post-project-personal`로 별도 표시한다. 기술 원리의 장문 설명은 블로그로 보내고 portfolio에는 판단과 결과만 남긴다.

## 선택과 media

portfolio 메인은 자동 최신 글 목록이 아니다. 사용자가 직접 선택한 work만 `portfolio: true`로 노출한다. `portfolioPinned: true`는 동시에 하나만 허용하며 자동으로 정하지 않는다.

architecture가 프로젝트 이해나 claim 검증의 핵심이면 다음을 모두 요구한다.

- `cardImage`: 사용자가 승인한 대표 architecture thumbnail
- `architecture`: title, image, alt, description, public route가 모두 있는 항목
- image file 존재, 권리 범위와 provenance 확인
- card와 상세 route에서 실제 render 확인

본문 claim이 rights 때문에 보류돼도 `public-approved` architecture asset은 포트폴리오 후보 안에 `cardImage: <relative-path>` 형태로 반복해 남긴다. private 위치는 쓰지 않고, title·alt·description에 필요한 공개 claim이 없으면 그 metadata와 실제 반영만 보류한다.

장식 image를 만들거나 private diagram을 공개 asset으로 복사하지 않는다. blog image와 같은 bytes를 쓸 수는 있지만 각 화면의 alt와 설명은 독자 질문에 맞게 쓴다.
