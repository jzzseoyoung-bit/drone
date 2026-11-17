# AGENT.md

## 개요

이 Antigravity 에이전트는 **드론 유지보수 데이터셋**(`c:\\workspaces\\drone_data\\data` 폴더) 를 분석하도록 구성되었습니다. 수행 단계는 다음과 같습니다:
1. `drone_test.csv`, `drone_this_month.csv`, `drone_train.csv` 세 파일을 스캔합니다.
2. 각 컬럼에 대해 데이터 타입, 비NULL 수, NULL 수, 고유값 수 등을 계산합니다.
3. 수치형 컬럼에 대해 IQR 방식을 이용해 이상치를 탐지합니다.
4. 결측값 패턴과 이상치 개수를 요약합니다.
5. 사람에게 읽기 쉬운 마크다운 보고서(`data_analysis_summary.md`)를 생성합니다.
6. 결과는 한글로 작성합니다.

에이전트는 또한 **원시 통계의 JSON 덤프**를 제공하여 downstream 처리에 활용할 수 있습니다.

---

## 생성된 파일

| 파일 | 설명 |
|------|-----|
| `data_analysis.py` | CSV 파일을 읽고 통계를 계산해 JSON 객체를 출력하는 파이썬 스크립트 |
| `data_analysis_summary.md` | 컬럼 분포, 결측값, 이상치 등을 한눈에 보기 쉽게 정리한 보고서 |
| `AGENT.md` | 현재 보고서 (이 파일) |

---

## 분석 실행 방법

```powershell
# 워크스페이스 루트에서 실행 (c:\\workspaces\\drone_data)
python C:\\Users\\USER\\.gemini\\antigravity\\brain\\22d06901-63f8-4b31-a318-b0fa43b1cf62\\data_analysis.py
```
스크립트는 **stdout**에 JSON을 출력하며, 전체 출력은 시스템 생성 단계 로그에도 저장됩니다.

---

## 주요 결과 ( `data_analysis_summary.md` 참고)

- **결측된 고장 정보**: `fault_code`와 `fault_category`에 다수 결측값 존재 (`drone_test.csv` 876건, 다른 파일 1,707건).
- **이상치**: `downtime_hours`, `repair_duration_hours`, `maintenance_cost`, `availability_rate` 등 수치형 컬럼에 이상치가 많이 발견됩니다.
- **Severity** 값은 0‑5 범위이며 평균은 약 0.8‑0.9입니다.
- **Availability rate** 은 0.3 ~ 0.998 사이에 분포하고, 낮은 값들의 이상치가 다수 존재합니다.
- **30일 내 고장 발생**(`failure_within_30days`) 은 전체의 약 22 % 정도이며, 이상치가 많습니다.

---

## 권고사항
1. **결측 고장 데이터 처리** – `fault_code`·`fault_category`가 결측인 행을 보완하거나 플래그(`no_fault`)를 추가하고, 필요 시 삭제합니다.
2. **이상치 완화** – 3·IQR 초과값에 대해 Winsorizing하거나 상한/하한을 설정합니다.
3. **왜도 조정** – `maintenance_cost`와 같이 오른쪽으로 치우친 컬럼은 로그 변환(`log1p`)을 적용합니다.
4. **특성 엔지니어링** – 범주형 컬럼(`equipment_type`, `unit_code`, `severity`)을 원‑핫 인코딩하고, 고비용·장시간 다운타임 이벤트에 대한 이진 플래그를 추가합니다.
5. **추가 분석** – 변수 간 상관관계를 탐색하고, `failure_within_30days` 예측 모델을 구축하거나 유지보수 효율성을 평가합니다.

---

## 에이전트 확장 아이디어
- `matplotlib`, `seaborn` 등으로 **히스토그램·박스플롯** 시각화 추가
- 위 권고사항을 자동으로 적용하는 **데이터 클리닝 파이프라인** 구현
- **Google Sheets**, **BigQuery** 플러그인을 연계해 정제된 데이터를 자동으로 전송

---

*이 문서는 Antigravity (GPT‑OSS 120B) 모델을 사용해 2026‑11‑17에 생성되었습니다.*