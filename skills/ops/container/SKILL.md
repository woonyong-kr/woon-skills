---
name: container
description: OCI image와 container runtime의 실행, mount, network, environment, resource, non-root와 runtime 장애를 설계·진단할 때 사용한다.
---

# Container

image, container, volume, host path를 구분한다. 실행 전 image digest, command/entrypoint, user, mount direction, port, env source를 확인한다.

workspace mount는 필요한 path만 최소 권한으로 연결하고 source를 덮는 anonymous volume을 주의한다. secret을 image layer나 command history에 넣지 않는다. non-root, read-only filesystem, capability drop, resource limit과 healthcheck를 workload에 맞게 적용한다.

문제 진단은 inspect→logs→process→network→mount 순으로 증거를 모으고 container 삭제 전 data volume ownership을 확인한다.
