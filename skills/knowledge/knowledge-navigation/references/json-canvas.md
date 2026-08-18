# JSON Canvas reference

- 공식 형식: <https://jsoncanvas.org/spec/1.0/>
- Woon에서는 `nodes`와 `edges`만 사용하며 node type은 `file`로 제한한다.
- `file`은 vault 상대 Markdown 경로이고, `subpath`는 `# heading` 또는 `#^block-id`다.
- `text`, `link`, `group` node와 edge label은 Markdown에 없는 내용을 Canvas에 새로 만들 수 있으므로 탐색 지도에서 사용하지 않는다.
