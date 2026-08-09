---
name: docker
description: Dockerfile, BuildKit, Compose, image layer·cache·multi-stage build와 Docker CI를 작성·최적화·진단할 때 사용한다.
---

# Docker

base image는 official source와 digest/version을 확인한다. dependency manifest를 먼저 copy해 cache를 활용하고 compiler/build tool은 multi-stage final image에서 제거한다.

`.dockerignore`로 secret·VCS·build output을 제외하고 `COPY . .` 전 context를 검사한다. `latest`와 unverified curl pipe를 피한다. Compose는 service dependency와 readiness를 구분하고 host-specific absolute path를 commit하지 않는다.

build, image history/size, non-root start, health와 실제 command를 검증한다.
