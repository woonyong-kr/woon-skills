from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "evals/fixtures/learning-content/verify.py"
SPEC = importlib.util.spec_from_file_location("learning_content_verify", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
validate_markdown = MODULE.validate_markdown
validate_obsidian_index = MODULE.validate_obsidian_index

SCORE_SCRIPT = ROOT / "evals/fixtures/learning-content/score_artifact.py"
SCORE_SPEC = importlib.util.spec_from_file_location(
    "learning_content_score", SCORE_SCRIPT
)
assert SCORE_SPEC is not None and SCORE_SPEC.loader is not None
SCORE_MODULE = importlib.util.module_from_spec(SCORE_SPEC)
sys.modules[SCORE_SPEC.name] = SCORE_MODULE
SCORE_SPEC.loader.exec_module(SCORE_MODULE)
score_artifact = SCORE_MODULE.score_artifact
diagram_snapshot_mismatches = SCORE_MODULE.diagram_snapshot_mismatches
outputs_after_first_java = SCORE_MODULE.outputs_after_first_java
java_output_pairs = SCORE_MODULE.java_output_pairs
concept_mentions = SCORE_MODULE.concept_mentions
is_console_command_block = SCORE_MODULE.is_console_command_block
NUMBERED_ARROW = MODULE.NUMBERED_ARROW


class LearningContentTest(unittest.TestCase):
    def setUp(self) -> None:
        fixture = ROOT / "evals/fixtures/learning-content"
        self.markdown = (fixture / "immutable-address.md").read_text(encoding="utf-8")
        self.source = (fixture / "AddressLesson.java").read_text(encoding="utf-8")
        self.output = (
            "문제: memberA=부산, memberB=부산\n개선: memberA=서울, memberB=부산\n"
        )

    def test_accepts_executable_linear_document(self) -> None:
        self.assertEqual(validate_markdown(self.markdown, self.source, self.output), [])

    def test_rejects_documented_output_that_differs_from_execution(self) -> None:
        errors = validate_markdown(self.markdown, self.source, "추측한 출력\n")
        self.assertTrue(any("output" in error for error in errors))

    def test_rejects_color_coded_mermaid(self) -> None:
        changed = self.markdown.replace(
            "sequenceDiagram", "sequenceDiagram\n    %% #ff0000"
        )
        errors = validate_markdown(changed, self.source, self.output)
        self.assertTrue(any("color" in error for error in errors))

    def test_rejects_term_before_observed_problem(self) -> None:
        changed = self.markdown.replace(
            "회원 B의 주소만", "공유 참조라고 합니다. 회원 B의 주소만", 1
        )
        errors = validate_markdown(changed, self.source, self.output)
        self.assertTrue(any("shared-reference" in error for error in errors))

    def test_scores_executable_fixture_without_hard_fail(self) -> None:
        result = score_artifact(
            self.markdown,
            ("memberA", "memberB", "sharedAddress"),
            "불변 객체",
        )
        self.assertTrue(result["passed"])
        self.assertGreaterEqual(result["score"], 15)
        self.assertEqual(result["hard_fail"], [])

    def test_accepts_numbered_arrows_with_or_without_dot(self) -> None:
        diagram = """sequenceDiagram
    A->>B: 1 request()
    B-->>A: 2. response
    A->>A: ③ finish
    A--xB: 4: failure
"""
        self.assertEqual(len(NUMBERED_ARROW.findall(diagram)), 4)

    def test_rejects_diagram_control_flow_absent_from_preceding_code(self) -> None:
        markdown = """```java
class Main { void run() {} }
```

```mermaid
sequenceDiagram
    Main->>Main: 1 catch(CustomException e)
```
"""
        self.assertEqual(
            diagram_snapshot_mismatches(markdown),
            ["diagram introduces catch absent from preceding Java"],
        )

    def test_requires_evidence_state_before_output_fence(self) -> None:
        markdown = """```java
class Main {}
```

```text
expected
```

위 값은 예상 결과다.
"""
        output, _, evidence_before = outputs_after_first_java(markdown)
        self.assertEqual(output, "expected")
        self.assertFalse(evidence_before)

    def test_combines_labeled_stdout_and_stderr_in_order(self) -> None:
        markdown = """```java
class Main {}
```

예상 결과 (미실행) — 표준 출력:

```text
start
```

예상 결과 (미실행) — 표준 오류:

```console
failure
```
"""
        output, _, evidence_before = outputs_after_first_java(markdown)
        self.assertEqual(output, "start\nfailure")
        self.assertTrue(evidence_before)

    def test_accepts_toolchain_named_actual_evidence_before_output(self) -> None:
        markdown = """```java
public class Main { public static void main(String[] args) {} }
```

```bash
javac Main.java
java Main
```

실제 JDK 21에서 컴파일하고 실행한 결과입니다.

```text
done
```
"""
        _, _, evidence_before = outputs_after_first_java(markdown)
        self.assertTrue(evidence_before)

    def test_skips_console_command_block_before_documented_output(self) -> None:
        markdown = """```java
public class Main { public static void main(String[] args) {} }
```

컴파일하고 실행합니다.

```console
javac Main.java
java Main
```

다음은 JDK 21에서 실제 컴파일·실행한 결과입니다.

```text
done
```
"""
        output, _, evidence_before = outputs_after_first_java(markdown)
        self.assertEqual(output, "done")
        self.assertTrue(evidence_before)
        self.assertTrue(
            is_console_command_block("console", "javac Main.java\njava Main")
        )

    def test_scores_later_runnable_pair_after_compile_failure_example(self) -> None:
        markdown = """# 예외 전파

문제를 실행 결과로 확인한다.

## 컴파일 실패 문제

```java
public class Main { public static void main(String[] args) { missing(); } }
```

실행하지 않은 예상 결과다.

```text
compile error
```

## 실행 가능한 예제

```java
class NetworkClient {}
class NetworkService {}
public class Main {
    public static void main(String[] args) {
        System.out.println("예외 전파 확인");
    }
}
```

직접 실행한 결과다.

```text
예외 전파 확인
```

이 그림은 예외가 어디로 전파되는지 답합니다.

```mermaid
sequenceDiagram
    Main->>NetworkService: 1. request()
    NetworkService->>NetworkClient: 2. send()
    NetworkClient-->>Main: 3. 예외 전파
```

1. Main이 호출한다.
2. NetworkService가 위임한다.
3. NetworkClient의 예외가 전파된다.

## 적용 경계

예외 전파는 catch 위치에서 멈춘다.

## 연습

catch 위치를 바꾼다.

## 정리

호출 경계를 따라 전파된다.
"""
        self.assertEqual(len(java_output_pairs(markdown)), 2)
        result = score_artifact(
            markdown,
            ("NetworkClient", "NetworkService", "Main"),
            "예외 전파",
        )
        self.assertEqual(result["scores"]["runnable_example_and_output"], 2)
        self.assertEqual(result["evidence"]["executed_java_block"], 2)

    def test_recognizes_natural_exception_propagation_phrasing(self) -> None:
        markdown = (
            "예외가 NetworkService를 거쳐 Main으로 전파된다.\n"
            "예외를 호출한 쪽으로 계속 전달한다.\n"
        )
        self.assertEqual(len(concept_mentions(markdown, "예외 전파")), 2)

    def test_accepts_obsidian_index_contract(self) -> None:
        fixture = ROOT / "evals/fixtures/learning-content/obsidian-index.md"
        self.assertEqual(
            validate_obsidian_index(fixture.read_text(encoding="utf-8")), []
        )

    def test_rejects_obsidian_index_without_callout_or_wikilink(self) -> None:
        markdown = "# 학습 문서 검증\n\n일반 Markdown 링크만 있습니다.\n"
        errors = validate_obsidian_index(markdown)
        self.assertTrue(any("callout" in error for error in errors))
        self.assertTrue(any("wikilink" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
