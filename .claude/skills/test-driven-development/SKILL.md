---
name: test-driven-development
description: 모든 기능 구현이나 버그 수정 시, 구현 코드를 작성하기 전에 사용할 것
---

# 테스트 주도 개발 (TDD)

## 개요

테스트를 먼저 작성하라. 실패하는 것을 확인하라. 통과시킬 최소한의 코드를 작성하라.

**핵심 원칙:** 테스트가 실패하는 것을 직접 보지 않았다면, 그 테스트가 올바른 것을 검증하는지 알 수 없다.

**규칙의 문자(letter)를 어기는 것은 곧 규칙의 정신(spirit)을 어기는 것이다.**

## 사용 시점

**항상:**
- 새로운 기능
- 버그 수정
- 리팩터링
- 동작(behavior) 변경

**예외 (사람 파트너에게 물어볼 것):**
- 일회성 프로토타입
- 자동 생성된 코드
- 설정(configuration) 파일

"이번 한 번만 TDD를 건너뛸까?"라고 생각하고 있는가? 멈춰라. 그건 합리화다.

## 철의 법칙 (The Iron Law)

```
실패하는 테스트가 먼저 존재하지 않는 한, 프로덕션 코드를 작성하지 않는다
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

테스트보다 먼저 코드를 작성했다면? 삭제하라. 처음부터 다시 시작하라.

**예외 없음:**
- "참고용"으로 남겨두지 말 것
- 테스트를 쓰면서 그 코드를 "각색(adapt)"하지 말 것
- 그 코드를 쳐다보지도 말 것
- 삭제는 진짜 삭제를 의미한다

테스트로부터 새롭게(fresh) 구현하라. 그게 전부다.

## Agent 기반 TDD (Human-in-the-Loop)

Claude Code와 같은 Agent로 TDD를 진행할 때는, 각 단계마다 사람 파트너의 검토 없이 다음 단계로 넘어가지 않는다. Agent가 혼자 RED-GREEN-REFACTOR를 전부 끝내고 결과만 보고하는 방식은 금지된다.

### 1. RED — 목표 설정 & Plan 검토

- Agent에게 넘기기 전에 이번 사이클에서 검증할 목표(하나의 동작)를 정확히 설정한다.
- Agent에게 구현이 아니라 **Plan.md 작성**을 먼저 요청한다. Plan.md에는 다음을 포함한다.
  - 이번에 작성할 실패하는 테스트(들)와 그 의도
  - 테스트를 통과시키기 위해 예상되는 최소 구현 범위
- **사람 파트너가 Plan.md를 검토하고 승인한 뒤에만** Agent가 테스트 코드를 작성하도록 진행시킨다. 목표가 잘못 설정되었거나 범위가 넓다면 이 시점에서 되돌린다.
- Agent가 작성한 테스트를 실행해 실제로 실패하는지, 예상한 이유로 실패하는지 직접 확인한다 (RED 검증 절차와 동일).
- **승인된 Plan.md를 커밋한다.** 구현 코드보다 먼저, Plan.md 단독으로 커밋을 남겨 이번 사이클의 목표를 기록으로 고정한다.

### 2. GREEN — Plan 대로 구현 & 통과 확인

- Agent에게 RED 단계에서 승인된 Plan.md의 목표만 달성하도록 구현을 요청한다. Plan에 없는 범위를 임의로 확장하지 않도록 한다.
- 구현 후 **테스트를 직접 실행해 실제로 통과하는지 확인**한다. Agent의 "통과했습니다" 보고를 그대로 믿지 않고 테스트 실행 로그를 확인한다.
- 다른 기존 테스트가 깨지지 않았는지도 함께 확인한다.

### 3. Review — 코드 리뷰, 리팩토링 요청 & 커밋

- GREEN 단계에서 만들어진 코드를 사람 파트너가 리뷰한다.
- 다음을 반드시 확인한다.
  - **Plan.md에 없던 사항이 구현되었는가** (범위 초과, 불필요한 추상화, 과도한 설계 등)
  - 테스트가 실제 동작을 검증하는지, mock으로 우회하지 않았는지
- 리팩토링이 필요하다고 판단되면 Agent에게 구체적으로 리팩토링을 요청한다 (테스트는 그린 상태를 유지한 채로).
- Plan 외 사항이 발견되면 되돌리거나(삭제 후 재작성) 별도 사이클로 분리해 다시 RED부터 진행한다.
- 리뷰가 끝나고 (필요한 리팩토링까지 반영되어) 테스트가 그린인 코드만 커밋한다. Plan.md 커밋과 구현 커밋을 분리해, 커밋 로그만으로 "무엇을 하려 했는지"와 "실제로 무엇을 했는지"를 구분할 수 있게 한다.

이 흐름은 위의 Red-Green-Refactor 원칙을 대체하는 것이 아니라, Agent를 사용할 때 각 단계 사이에 사람의 승인 체크포인트를 명시적으로 추가한 것이다.

## Red-Green-Refactor

### RED - 실패하는 테스트 작성

무엇이 일어나야 하는지를 보여주는 최소한의 테스트 한 개를 작성하라.

<Good>
```python
def test_retries_failed_operations_3_times():
    attempts = 0

    def operation():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("fail")
        return "success"

    result = retry_operation(operation)

    assert result == "success"
    assert attempts == 3
```
명확한 이름, 실제 동작 검증, 한 가지만 검증
</Good>

<Bad>
```python
def test_retry_works(mocker):
    mock = mocker.Mock(side_effect=[RuntimeError(), RuntimeError(), "success"])
    retry_operation(mock)
    assert mock.call_count == 3
```
모호한 이름, 실제 코드가 아닌 mock을 검증
</Bad>

**요건:**
- 하나의 동작(behavior)
- 명확한 이름
- 실제 코드 (불가피한 경우가 아니면 mock 사용 금지)

### RED 검증 - 실패하는 것을 직접 보기

**필수. 절대 건너뛰지 말 것.**

```bash
pytest path/to/test_file.py
```

다음을 확인하라:
- 테스트가 실패한다 (에러가 아니라)
- 실패 메시지가 예상한 그대로다
- 기능이 없어서 실패한다 (오타 때문이 아니라)

**테스트가 통과한다고?** 이미 존재하는 동작을 검증하고 있는 것이다. 테스트를 고쳐라.

**테스트가 에러를 낸다고?** 에러를 고치고, 제대로 실패할 때까지 다시 실행하라.

### GREEN - 최소한의 코드

테스트를 통과시키는 가장 단순한 코드를 작성하라.

<Good>
```python
def retry_operation(fn):
    for i in range(3):
        try:
            return fn()
        except Exception as e:
            if i == 2:
                raise
    raise RuntimeError("unreachable")
```
통과시킬 만큼만
</Good>

<Bad>
```python
def retry_operation(
    fn,
    max_retries=3,
    backoff="linear",  # "linear" | "exponential"
    on_retry=None,
):
    # YAGNI (You Aren't Gonna Need It)
    ...
```
과도한 설계
</Bad>

기능을 추가하지 말고, 다른 코드를 리팩터링하지 말고, 테스트가 요구하는 것 이상으로 "개선"하지 말라.

### GREEN 검증 - 통과하는 것을 직접 보기

**필수.**

```bash
pytest path/to/test_file.py
```

다음을 확인하라:
- 테스트가 통과한다
- 다른 테스트들도 여전히 통과한다
- 출력이 깨끗하다 (에러, 경고 없음)

**테스트가 실패한다?** 테스트가 아니라 코드를 고쳐라.

**다른 테스트가 실패한다?** 지금 당장 고쳐라.

### REFACTOR - 정리

그린 상태가 된 후에만:
- 중복 제거
- 이름 개선
- 헬퍼(helper) 추출

테스트는 그린으로 유지하라. 동작을 추가하지 말라.

### 반복

다음 기능에 대한 다음 실패하는 테스트를 작성하라.

## 좋은 테스트

| 품질 | 좋음 | 나쁨 |
|------|------|------|
| **최소성** | 한 가지만 검증. 이름에 "and"가 들어가는가? 분리하라. | `test_validates_email_and_domain_and_whitespace` |
| **명확성** | 이름이 동작을 설명한다 | `test_test1` |
| **의도 표현** | 원하는 API를 보여준다 | 코드가 무엇을 해야 하는지 가린다 |

## 흔한 합리화들

| 변명 | 현실 |
|------|------|
| "너무 단순해서 테스트할 게 없어요" | 단순한 코드도 깨진다. 테스트는 30초면 쓴다. |
| "나중에 테스트할게요" | 즉시 통과하는 테스트는 아무것도 증명하지 않는다. |
| "사후 테스트도 같은 목표 달성" | 사후 = "무엇을 하는가?" 사전 = "무엇을 해야 하는가?" |
| "이미 수동으로 테스트했어요" | 임시방편 ≠ 체계적. 기록 없음, 재실행 불가. |
| "X시간 작업 지우는 건 낭비" | 매몰비용 오류. 미검증 코드 유지가 기술 부채. |
| "참고용으로 두고 테스트부터" | 결국 그 코드를 각색하게 된다. 그게 사후 테스트다. 삭제는 진짜 삭제다. |
| "먼저 탐색(explore)이 필요해요" | 좋다. 탐색물은 버리고, TDD로 시작하라. |
| "테스트가 어렵다는 건 설계가 불명확하다는 뜻" | 테스트의 말을 들어라. 테스트하기 어려우면 사용하기도 어렵다. |
| "TDD는 나를 느리게 해요" | TDD가 디버깅보다 빠르다. 실용적 = 테스트 우선. |
| "수동 테스트가 더 빨라요" | 수동은 엣지 케이스를 증명하지 못한다. 매번 다시 테스트해야 한다. |
| "기존 코드엔 테스트가 없어요" | 당신이 그 코드를 개선하는 중이다. 기존 코드에 대한 테스트도 추가하라. |

## 위험 신호 (Red Flags) - 멈추고 처음부터

- 테스트보다 코드가 먼저 있다
- 구현 후에 테스트를 쓴다
- 테스트가 즉시 통과한다
- 왜 테스트가 실패했는지 설명할 수 없다
- 테스트를 "나중에" 추가한다
- "이번 한 번만"이라고 합리화한다
- "이미 수동으로 테스트했어요"
- "사후 테스트도 같은 목적을 달성해요"
- "정신이 중요하지 의식이 중요한 게 아니에요"
- "참고용으로 두고" 또는 "기존 코드 각색"
- "이미 X시간 썼는데, 지우는 건 낭비"
- "TDD는 교조적, 나는 실용적"
- "이건 다른 경우인데..."

**이 모든 것은 다음을 의미한다: 코드를 삭제하라. TDD로 다시 시작하라.**

## 예시: 버그 수정

**버그:** 빈 이메일이 허용됨

**RED**
```python
def test_rejects_empty_email():
    result = submit_form({"email": ""})
    assert result["error"] == "Email required"
```

**RED 검증**
```bash
$ pytest
FAILED: KeyError: 'error'   (또는 'Email required'를 기대했으나 다른 값)
```

**GREEN**
```python
def submit_form(data):
    email = data.get("email", "")
    if not email.strip():
        return {"error": "Email required"}
    # ...
```

**GREEN 검증**
```bash
$ pytest
PASSED
```

**REFACTOR**
여러 필드에 대한 검증이 필요해지면 검증 로직을 추출하라.

## 검증 체크리스트

작업을 완료(complete)로 표시하기 전에:

- [ ] 모든 새 함수/메서드에 테스트가 있다
- [ ] 각 테스트가 실패하는 것을 직접 보고 구현했다
- [ ] 각 테스트가 예상한 이유로 실패했다 (오타가 아니라 기능 부재로)
- [ ] 각 테스트를 통과시키는 최소한의 코드를 작성했다
- [ ] 모든 테스트가 통과한다
- [ ] 출력이 깨끗하다 (에러, 경고 없음)
- [ ] 테스트가 실제 코드를 사용한다 (mock은 불가피할 때만)
- [ ] 엣지 케이스와 에러 케이스가 커버되어 있다

체크박스를 모두 채울 수 없다면? TDD를 건너뛴 것이다. 처음부터 다시 시작하라.

## 막혔을 때

| 문제 | 해결 |
|------|------|
| 어떻게 테스트할지 모르겠다 | 원하는 API를 먼저 적어보라. assertion부터 작성하라. 사람 파트너에게 물어보라. |
| 테스트가 너무 복잡하다 | 설계가 너무 복잡하다. 인터페이스를 단순화하라. |
| 모든 것을 mock해야 한다 | 코드가 너무 결합(coupled)되어 있다. 의존성 주입(DI)을 사용하라. |
| 테스트 셋업이 거대하다 | 헬퍼를 추출하라. 그래도 복잡하면 설계를 단순화하라. |

## 디버깅 통합

버그를 발견했는가? 그 버그를 재현하는 실패하는 테스트를 먼저 작성하라. TDD 사이클을 따르라. 그 테스트가 수정을 증명하고 회귀를 방지한다.

테스트 없이 버그를 수정하지 말라.

## pytest 관련 추가 팁 (Python 특화)

### 픽스처(Fixtures)는 절제해서 사용하라

```python
# 좋음: 분명히 재사용되는 셋업만 픽스처로
@pytest.fixture
def temp_db():
    db = create_in_memory_db()
    yield db
    db.close()

def test_user_creation(temp_db):
    user = create_user(temp_db, name="Alice")
    assert user.id is not None
```

픽스처가 너무 많아지면 테스트의 의도가 흐려진다. 단순한 셋업은 테스트 안에 그대로 두는 편이 명확할 때가 많다.

### parametrize는 같은 동작의 여러 입력에만 사용하라

```python
# 좋음: 같은 동작 규칙, 여러 입력
@pytest.mark.parametrize("email", ["", "   ", "\t\n"])
def test_rejects_blank_email(email):
    result = submit_form({"email": email})
    assert result["error"] == "Email required"
```

서로 다른 동작을 parametrize로 묶지 말라. 그건 테스트 한 개가 아니라 여러 개로 나뉘어야 한다.

### mock은 외부 경계에서만

`unittest.mock` 또는 `pytest-mock`의 `mocker`를 쓸 때는, 우리가 제어할 수 없는 경계(네트워크, 파일시스템, 시간 등)에서만 사용하라. 우리 코드 내부 모듈 사이의 호출을 mock하기 시작했다면, 결합도가 너무 높다는 신호다.

### 테스트 실행 명령

```bash
# 단일 파일
pytest path/to/test_file.py

# 단일 테스트
pytest path/to/test_file.py::test_specific_case

# 첫 실패에서 멈춤 (빠른 RED 확인용)
pytest -x

# 자세한 출력
pytest -v

# 출력(print) 캡처 끔 (디버깅용)
pytest -s
```

## 최종 규칙

```
프로덕션 코드 → 테스트가 존재하고, 먼저 실패했다
그 외 → TDD가 아니다
```

사람 파트너의 허가 없이는 예외 없음.
