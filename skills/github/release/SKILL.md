---
name: release
description: GitHub Release, tag, version, changelog, release note를 계획·검증·생성할 때 사용한다. 일반 배포나 패키지 publish에는 사용하지 않는다.
---

# Release

저장소의 version source, tag 형식, changelog, CI artifact, 이전 release를 확인한다. 포함 commit과 breaking change를 실제 diff에서 산출하고 사용자 영향 중심으로 note를 작성한다.

tag·release 생성 전 target SHA, version 중복, required checks, artifact provenance를 확인한다. draft를 기본으로 제안하며 명시적 승인 없이 publish하지 않는다. 생성 뒤 tag와 release URL이 같은 SHA를 가리키는지 검증한다.
