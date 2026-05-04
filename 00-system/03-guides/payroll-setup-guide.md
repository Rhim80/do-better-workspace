# Payroll 셋업 가이드

> 어려운 결정은 모두 셋업 도구가 묻고 권장값을 알려줍니다.
> 그대로 Enter만 누르셔도 동작하니, 처음에는 가볍게 진행하세요.

---

## 한 번에 끝내기

```bash
pip install openpyxl pyyaml google-api-python-client google-auth google-auth-oauthlib
python3 .claude/skills/payroll/scripts/setup.py --create-sheet
```

이 두 줄이면 끝납니다. 셋업 도구가 4단계로 묻습니다:

1. **회사 정보** — 회사 이름, 사업주 성함
2. **직원 규모와 매장** — 직원 몇 명? / 매장 여러 개?
3. **휴일·추가근무 가산율** — 잘 모르시면 그대로 Enter
4. **세무사 정보** — 메일 발송 안 쓰시면 N

마지막에 Google 계정 인증 창이 한 번 열리면, **자기 Google 계정으로 로그인**만 하면 됩니다. 직원DB 시트가 자동으로 만들어지고 ID도 자동으로 저장됩니다.

---

## 자주 막히는 곳

### "Google 라이브러리가 없어요" 에러
```bash
pip install google-api-python-client google-auth google-auth-oauthlib
```
설치하고 다시 setup 실행.

### "credentials.json이 없다"
워크스페이스에서 Google Calendar / Google Sheets 등 다른 스킬이 이미 동작하고 있다면 이 단계를 건너뛸 수 있습니다. 처음 쓰시는 거라면 [Google Cloud OAuth 셋업](#google-cloud-oauth-처음-한-번) 섹션 참고.

### 셋업했는데 다시 처음부터 하고 싶음
```bash
python3 .claude/skills/payroll/scripts/setup.py
```
다시 실행하면 됩니다. 기존 `company.yaml`은 자동 백업됩니다 (`company.yaml.backup-YYYYMMDD-HHMMSS`).

### 현재 설정 확인
```bash
python3 .claude/skills/payroll/scripts/setup.py --show
```

### 일부 항목만 바꾸고 싶음
`.claude/skills/payroll/config/company.yaml` 파일을 직접 에디터로 열어 수정. 나머지 셋업을 다시 할 필요 없음.

---

## 셋업이 끝나면

매월 28일~말일 사이에 Claude에게 이렇게 말하면 됩니다:

> 이번 달 급여 처리하자

자세한 흐름은 [SKILL.md](../../../.claude/skills/payroll/SKILL.md) 참고.

---

## Google Cloud OAuth (처음 한 번)

> 워크스페이스에서 이미 다른 Google 스킬을 쓰고 있다면 건너뛰셔도 됩니다.

1. https://console.cloud.google.com 접속, 프로젝트 생성
2. **APIs & Services → Library**: Google Sheets API + Google Drive API 활성화
3. **APIs & Services → OAuth consent screen**: External, 본인 Gmail을 Test users에 추가
4. **APIs & Services → Credentials → Create Credentials → OAuth client ID**: Desktop app
5. JSON 다운로드 → `~/.claude/lib/credentials.json` 으로 저장
6. setup.py 다시 실행 → 브라우저가 열리면 본인 Google 계정으로 로그인

이게 어렵게 느껴지시면, 워크스페이스 운영자(또는 도와주는 사람)에게 한 번만 부탁드리세요. 한 번 끝나면 그 다음부터는 자동입니다.

---

## 핵심 원칙

- **모든 결정은 setup이 권장값으로 미리 채워둠** — 그대로 Enter만 눌러도 OK
- **가산율 같은 노동법 용어**는 회사가 실제 어떻게 운영하는지를 회계담당/세무사에게 물어서 나중에 `company.yaml`에 반영
- **회사 정보(`company.yaml`)는 git에 올라가지 않음** — 안전합니다
