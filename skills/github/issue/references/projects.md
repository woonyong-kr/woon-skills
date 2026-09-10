# GitHub Projects 일정과 권한

공식 `gh` CLI를 등록 adapter로 사용한다. 일정 변경마다 새 실행기·browser 자동화·상주 동기화를 만들지 않는다. 이 절차는 실행 권한 자체를 부여하지 않는다. 사용자가 승인한 계정·저장소·Issue·Project·필드·날짜와 OAuth 추가 범위를 현재 대화에서 확정한다.

## 계정과 최소 추가 권한

1. `gh auth status --hostname github.com`으로 활성 계정, credential 저장 방식과 scope를 확인한다. token을 출력하는 옵션·명령은 사용하지 않는다. 환경 token이 활성 인증을 덮는 경우 값은 읽지 않고 그 존재만 확인하며, keyring 인증이 갱신됐다고 주장하지 않는다.
2. 기존 계정에 Projects 쓰기 권한 추가가 승인됐을 때만 아래 공식 OAuth 흐름을 수행한다. `--reset-scopes`, `--remove-scopes`, 계정 변경, 평문 저장을 함께 수행하지 않는다.

   ```sh
   gh auth refresh -h github.com -s project
   gh auth status --hostname github.com
   gh api graphql -f query='query { viewer { login id } }'
   ```

3. 승인 전후 활성 계정과 기존 scope가 유지되고 `project`가 추가됐는지 확인한다. OAuth 화면은 CLI가 연 공식 grant 흐름만 사용한다. 비밀번호·2FA 등 사용자 전용 인증이 필요하면 그 단계만 사용자에게 넘기며 값을 요청하거나 기록하지 않는다. 이미 완료한 grant를 반복하지 않는다.
4. 권한 성공은 실제 대상 Project GraphQL readback까지 확인한다. 인증 성공과 일정 변경 성공을 분리한다. [gh auth refresh 공식 계약](https://cli.github.com/manual/gh_auth_refresh).

## 정확한 대상과 변경

변경 전에 local JSON manifest에 host, actor login, repository, Issue URL·node ID, Project URL·node ID, item ID, field ID·이름·타입, before와 요청 날짜를 기록한다. 실제 ID는 조회 결과에서만 가져오며 프로젝트 번호·Issue 번호와 node ID를 혼용하지 않는다. 예를 들어 승인 범위가 Issue 1·22·23이면 해당 저장소의 그 세 Issue URL만 허용하고 나머지를 포함하지 않는다. task별 ID·개인 경로를 이 정본 문서나 catalog에 고정하지 않는다.

`gh project view|field-list|item-list --format json` 또는 `gh api graphql`로 Project·필드·item을 조회한다. 모든 관련 페이지를 끝까지 읽었는지 확인한 뒤 Issue node ID로 기존 item을 찾는다. 읽기 실패나 첫 페이지의 부재를 item 없음으로 해석하지 않는다. 기존 item이 있으면 반드시 재사용한다. 추가가 명시 승인되고 전체 조회로 부재가 확인된 때만 `gh project item-add`를 사용할 수 있다.

대상 Project는 다음처럼 조회한 node ID로 다시 확인할 수 있다. `project_node_id`는 위 manifest에서 읽은 값이다.

```sh
gh api graphql -F id="$project_node_id" -f query='query($id: ID!) { node(id: $id) { ... on ProjectV2 { id title url closed } } }'
```

DATE 타입 필드만 `YYYY-MM-DD`로 변경하며 의도와 다른 시간 변환을 하지 않는다. 실행 직전 item 소속·Issue·field ID·현재 값을 다시 대조한다. 값이 달라졌으면 덮어쓰지 않고 최신값으로 계획을 갱신한다. 이미 원하는 값이면 mutation 없이 `unchanged`로 기록한다.

사용자가 해당 Project의 일정 작성을 승인했고 편집 가능한 날짜 필드가 없다면, 승인 범위에 필요한 `Start date`·`Target date` 두 DATE 필드만 생성할 수 있다. `Created at`·`Updated at`·`Closed at` 같은 자동 시각 필드를 일정으로 전용하지 않는다. 먼저 모든 필드를 조회해 같은 이름·DATE 타입이 있으면 재사용한다. 이름이 같은 다른 타입이나 복수 후보가 있으면 임의 선택·중복 생성하지 않는다. 다음 `project_number`·`project_owner`도 검토한 manifest에서 읽는다.

```sh
gh project field-create "$project_number" --owner "$project_owner" --name 'Start date' --data-type DATE --format json
gh project field-create "$project_number" --owner "$project_owner" --name 'Target date' --data-type DATE --format json
gh project field-list "$project_number" --owner "$project_owner" --format json
```

없는 필드의 생성 명령만 실행하고 이름·DATE 타입·새 ID를 재조회해 manifest에 추가한 뒤 item을 수정한다. 생성 응답이 불확실하면 먼저 필드를 재조회한다. 필드 삭제·타입 변경·범위 밖 필드 생성은 이 절차에 포함하지 않는다. [gh project field-create 공식 계약](https://cli.github.com/manual/gh_project_field-create).

다음 변수는 검토한 manifest에서 읽고 비어 있지 않음을 확인한다. 한 호출은 정확한 item의 필드 하나만 변경한다.

```sh
gh project item-edit --project-id "$project_node_id" --id "$item_node_id" \
  --field-id "$date_field_node_id" --date "$requested_date" --format json
```

동일한 공식 GraphQL `updateProjectV2ItemFieldValue`를 사용해도 같은 대상·권한·재조회 경계를 지킨다. Projects 필드 변경을 UI로 우회하지 않는다. [gh project item-edit 공식 계약](https://cli.github.com/manual/gh_project_item-edit).

## 영수증과 불확실한 결과

local JSON receipt는 operation ID, 승인 범위, manifest SHA-256, 시작·종료 시각, actor, 정확한 대상 ID, before, requested, mutation 응답의 필요한 필드, requery 값과 상태만 보관한다. token·Authorization header·device code·전체 credential 출력은 제외한다. 공개 Git에 개인 운영 영수증을 넣지 않는다.

mutation 응답만으로 성공 처리하지 않는다. 같은 item·field를 공식 API로 재조회하여 요청값과 일치할 때 `verified`, 기존값과 요청값이 같아서 호출하지 않았으면 `unchanged`로 기록한다. timeout·끊김·응답 파싱 실패는 `unknown-result`다. 이때 쓰기를 반복하지 말고 먼저 대상값과 item 중복 여부를 재조회한다. 확인할 수 없으면 상태를 유지하고 막힌 조회를 보고한다. 복구는 보존한 before를 근거로 같은 승인·최신값 대조·재조회 절차를 따른다.
