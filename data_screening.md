# 결측값 원인 분석 보고서

## 개요
`fault_code`와 `fault_category` 컬럼에 결측값이 많이 존재하는 이유를 파악하기 위해 각 데이터셋에서 결측 레코드와 `maintenance_type`(정비 유형) 간의 관계를 분석했습니다.

## 분석 결과 요약

| 데이터셋 | 전체 행 수 | `fault_code` 결측 수 | `fault_category` 결측 수 | 둘 다 결측 | 결측 시 `maintenance_type` 분포 | 비결측 시 `maintenance_type` 분포 |
|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

-|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

-|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

--|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

--|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

-|
| **drone_test.csv** | 1,241 | 876 | 876 | 876 | 예방정비: 876 | 사후정비: 279, 긴급정비: 86 |
| **drone_this_month.csv** | 106* | 62 | 62 | 62 | 예방정비: 62 | 사후정비: 31, 긴급정비: 13 |
| **drone_train.csv** | 2,346 | 1,707 | 1,707 | 1,707 | 예방정비: 1,707 | 사후정비: 468, 긴급정비: 171 |

* `drone_this_month.csv`의 행 수가 106으로 표시된 것은 스크립트가 해당 파일을 잘못 읽은 가능성이 있습니다(원래는 2,346행이어야 함). 데이터 파일을 다시 확인해 보시기 바랍니다.

## 해석
- **예방정비(예방정비)** 시에는 고장(`fault_code`, `fault_category`)이 발생하지 않으므로 해당 컬럼에 값이 기록되지 않습니다. 따라서 **결측값은 입력 실수가 아니라 의도된 결측**(즉, 실제로 고장이 없어서 기록이 없는 경우)으로 판단됩니다.
- **사후정비(사후정비)**와 **긴급정비(긴급정비)** 에서는 실제 고장이 존재하므로 `fault_code`와 `fault_category`가 채워져 있습니다.
- 결측값이 전부 `예방정비`와 연관돼 있기 때문에, 이 컬럼들을 모델에 사용할 때는 **결측을 ‘고장 없음’으로 처리**하거나 별도 플래그(`no_fault`)를 추가하는 것이 바람직합니다.

## 권고사항
1. **결측값 처리**
   - `fault_code`와 `fault_category`가 결측인 레코드에 대해 `no_fault = 1` (고장 없음) 플래그를 추가하고, 실제 고장 정보가 있는 경우 `no_fault = 0` 으로 설정합니다.
   - 필요 시 결측값을 문자열 `'None'` 혹은 `NaN` 대신 `0`(또는 별도 코드)으로 대체해 모델이 정상적으로 학습하도록 합니다.
2. **데이터 검증**
   - `drone_this_month.csv` 파일의 행 수가 기대와 다르므로 파일이 올바르게 저장되었는지 확인하고, 필요 시 재생성합니다.
3. **추가 컬럼 생성**
   - `maintenance_type`을 원‑핫 인코딩하고, `no_fault` 플래그와 함께 사용하면 정비 유형에 따라 고장 발생 여부를 명확히 구분할 수 있습니다.
4. **분석 확장**
   - 다른 컬럼(`equipment_type`, `unit_code` 등)과 `no_fault` 플래그 간의 상관관계를 살펴보면 고장 발생 패턴을 더 잘 이해할 수 있습니다.

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |



*보고서는 Antigravity (GPT‑OSS 120B) 모델을 사용해 2026‑11‑17에 생성되었습니다.*

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |



## 드론 유형·계절·고장 유형 패턴

아래는 `equipment_type`(드론 유형), `season`(계절), `fault_category`(고장 유형) 간에 눈에 띄는 비율(> 20 %)을 보이는 주요 패턴을 정리한 내용입니다. 각 패턴은 해당 조합에서 고장 유형이 차지하는 비율(`percentage`)을 기준으로 선정했습니다.

| 드론 유형 | 계절 | 고장 유형 | 비율 (%) |
|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

--|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

--|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

-|
| 정찰드론 | 겨울 (Winter) | 배터리 | 35.94 |
| 정찰드론 | 겨울 | 센서 | 21.09 |
| 정찰드론 | 여름 (Summer) | 모터 | 32.89 |
| 정찰드론 | 여름 | 배터리 | 25.00 |
| 정찰드론 | 봄 (Spring) | 배터리 | 32.69 |
| 정찰드론 | 가을 (Fall) | 배터리 | 27.03 |
| 정찰드론 | 가을 | 통신 | 22.97 |
| 수송드론 | 겨울 | 배터리 | 38.52 |
| 수송드론 | 겨울 | 모터 | 28.69 |
| 수송드론 | 여름 | 모터 | 51.40 |
| 수송드론 | 봄 | 모터 | 32.73 |
| 수송드론 | 봄 | 통신 | 21.82 |
| 수송드론 | 가을 | 모터 | 38.57 |
| 교육용드론 | 겨울 | 배터리 | 54.29 |
| 교육용드론 | 여름 | 배터리 | 27.50 |
| 교육용드론 | 여름 | 센서 | 22.50 |
| 교육용드론 | 여름 | 통신 | 22.50 |
| 교육용드론 | 봄 | 배터리 | 26.09 |
| 교육용드론 | 봄 | 기체 | 21.74 |
| 교육용드론 | 봄 | 통신 | 21.74 |
| 교육용드론 | 가을 | 배터리 | 27.59 |
| 감시드론 | 겨울 | 배터리 | 33.33 |
| 감시드론 | 겨울 | 모터 | 19.70 |
| 감시드론 | 겨울 | 센서 | 18.18 |
| 감시드론 | 여름 | 통신 | 28.24 |
| 감시드론 | 여름 | 배터리 | 25.88 |
| 감시드론 | 여름 | 모터 | 20.00 |
| 감시드론 | 여름 | 센서 | 17.65 |
| 감시드론 | 봄 | 통신 | 29.55 |
| 감시드론 | 봄 | 센서 | 25.00 |
| 감시드론 | 봄 | 모터 | 15.91 |
| 감시드론 | 가을 | 배터리 | 38.10 |
| 감시드론 | 가을 | 센서 | 21.43 |
| 감시드론 | 가을 | 통신 | 19.05 |

### 해석 포인트
- **배터리 고장**은 대부분의 드론 유형에서 겨울에 높은 비율을 보이며, 특히 **수송드론**과 **교육용드론**에서 두드러집니다.
- **모터 고장**은 **수송드론**과 **정찰드론**의 여름에 집중됩니다.
- **통신 고장**은 **감시드론**의 여름과 가을에 비교적 높은 비율을 나타냅니다.
- **센서 고장**은 **정찰드론** 겨울과 **감시드론** 겨울/봄에 나타납니다.

### 활용 방안
- 계절별 고장 위험도를 반영해 **예방정비 스케줄**을 조정할 수 있습니다 (예: 겨울에 배터리 교체 주기 확대).
- 고장이 빈번히 발생하는 조합을 대상으로 **부품 재고**를 미리 확보하거나 **특정 부품 교체 정책**을 설계합니다.
- 머신러닝 모델에 `season`과 `equipment_type`을 특성으로 포함하면 고장 유형 예측 정확도를 높일 수 있습니다.

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |



## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |



## 드론 유형·계절·고장 유형 패턴

아래는 `equipment_type`(드론 유형), `season`(계절), `fault_category`(고장 유형) 간에 눈에 띄는 비율(> 20 %)을 보이는 주요 패턴을 정리한 내용입니다. 각 패턴은 해당 조합에서 고장 유형이 차지하는 비율(`percentage`)을 기준으로 선정했습니다.

| 드론 유형 | 계절 | 고장 유형 | 비율 (%) |
|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

--|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

--|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

-|
| 정찰드론 | 겨울 (Winter) | 배터리 | 35.94 |
| 정찰드론 | 겨울 | 센서 | 21.09 |
| 정찰드론 | 여름 (Summer) | 모터 | 32.89 |
| 정찰드론 | 여름 | 배터리 | 25.00 |
| 정찰드론 | 봄 (Spring) | 배터리 | 32.69 |
| 정찰드론 | 가을 (Fall) | 배터리 | 27.03 |
| 정찰드론 | 가을 | 통신 | 22.97 |
| 수송드론 | 겨울 | 배터리 | 38.52 |
| 수송드론 | 겨울 | 모터 | 28.69 |
| 수송드론 | 여름 | 모터 | 51.40 |
| 수송드론 | 봄 | 모터 | 32.73 |
| 수송드론 | 봄 | 통신 | 21.82 |
| 수송드론 | 가을 | 모터 | 38.57 |
| 교육용드론 | 겨울 | 배터리 | 54.29 |
| 교육용드론 | 여름 | 배터리 | 27.50 |
| 교육용드론 | 여름 | 센서 | 22.50 |
| 교육용드론 | 여름 | 통신 | 22.50 |
| 교육용드론 | 봄 | 배터리 | 26.09 |
| 교육용드론 | 봄 | 기체 | 21.74 |
| 교육용드론 | 봄 | 통신 | 21.74 |
| 교육용드론 | 가을 | 배터리 | 27.59 |
| 감시드론 | 겨울 | 배터리 | 33.33 |
| 감시드론 | 겨울 | 모터 | 19.70 |
| 감시드론 | 겨울 | 센서 | 18.18 |
| 감시드론 | 여름 | 통신 | 28.24 |
| 감시드론 | 여름 | 배터리 | 25.88 |
| 감시드론 | 여름 | 모터 | 20.00 |
| 감시드론 | 여름 | 센서 | 17.65 |
| 감시드론 | 봄 | 통신 | 29.55 |
| 감시드론 | 봄 | 센서 | 25.00 |
| 감시드론 | 봄 | 모터 | 15.91 |
| 감시드론 | 가을 | 배터리 | 38.10 |
| 감시드론 | 가을 | 센서 | 21.43 |
| 감시드론 | 가을 | 통신 | 19.05 |

### 해석 포인트
- **배터리 고장**은 대부분의 드론 유형에서 겨울에 높은 비율을 보이며, 특히 **수송드론**과 **교육용드론**에서 두드러집니다.
- **모터 고장**은 **수송드론**과 **정찰드론**의 여름에 집중됩니다.
- **통신 고장**은 **감시드론**의 여름과 가을에 비교적 높은 비율을 나타냅니다.
- **센서 고장**은 **정찰드론** 겨울과 **감시드론** 겨울/봄에 나타납니다.

### 활용 방안
- 계절별 고장 위험도를 반영해 **예방정비 스케줄**을 조정할 수 있습니다 (예: 겨울에 배터리 교체 주기 확대).
- 고장이 빈번히 발생하는 조합을 대상으로 **부품 재고**를 미리 확보하거나 **특정 부품 교체 정책**을 설계합니다.
- 머신러닝 모델에 `season`과 `equipment_type`을 특성으로 포함하면 고장 유형 예측 정확도를 높일 수 있습니다.

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |



## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |



## 데이터 처리 기준을 판단할 대상 컬럼 및 제거(또는 정제) 고려 이유

아래 표는 **이상치**와 **결측치** 판단이 필요해 보이는 주요 컬럼을 정리한 것입니다. 각 컬럼에 대해 **왜 정제(제거 혹은 대체)가 필요할 수 있는지**에 대한 근거만 적어두었습니다. 실제 처리 여부는 사용자께서 판단해 주세요.

| 컬럼 | 판단 대상 | 정제(제거/대체) 고려 이유 |
|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

-|
| `downtime_hours` | 이상치 | 총 196 건(드론 테스트)·425 건(전체) 이상의 **극단값**(최대 61.8 h) 존재, 분포가 극히 오른쪽으로 치우쳐 있어 평균·분산에 큰 영향을 미침.
| `repair_duration_hours` | 이상치 | 186 건·345 건 이상의 **극단값**(최대 55.9 h) 발견, 일부 수치가 실제 운영과 동떨어진 수준으로 모델 학습 시 편향을 초래할 수 있음.
| `maintenance_cost` | 이상치 | 비용 컬럼이 **히스토그램이 긴 꼬리**(최대 19 000) 형태이며, 158 건·434 건의 이상치가 존재. 고가 사건이 전체 모델에 과도한 가중치를 줄 위험.
| `parts_replaced_count` | 이상치 | 146 건·253 건 이상의 **비정상적으로 높은 부품 교체 횟수**(최대 10) 발견, 대부분 0‑3 회인 상황에서 드물게 높은 값은 데이터 입력 오류 가능성.
| `availability_rate` | 이상치 | 0.3 ~ 0.998 범위 내에 **낮은 값(≤0.5)**이 307 건 존재, 가용률이 0에 가까운 경우 실제 운영 불능을 의미하거나 데이터 기록 오류일 수 있음.
| `failure_within_30days` | 이상치 | 0/1 이진값이지만 **525 건**에 해당하는 과도한 1값(22 % 비율)으로 클래스 불균형이 심함. 필요 시 리샘플링 혹은 플래그 재정의 검토.
| `fault_code` / `fault_category` | 결측 | `fault_code`와 `fault_category`가 **예방정비** 시 전체 결측(876‑1 707건)이며, 고장 없는 경우 의도적 결측. 결측을 ‘고장 없음’ 플래그(`no_fault`)로 변환하거나, 분석 목적에 따라 해당 레코드 삭제 검토.
| `days_since_last_maintenance` | 결측 | `drone_this_month.csv`·`drone_train.csv`에서 **150 건**(≈6 %) 결측 존재, 최신 정비 일자를 알 수 없어 시계열 특성에 영향을 줄 수 있음. 대체 방법 필요.
| `equipment_age_years` | 이상치 (가능성) | 일부 고연령(≥8 년) 값이 **극단적**(최대 8.9)으로 나타나며, 연령과 고장 간 관계 분석 시 이상치가 회귀 계수에 과도한 영향을 줄 수 있음.
| `maintenance_success` | 이상치 | 73 건·131 건의 **0값**(실패) 비율이 상대적으로 높아, 실패와 성공이 불균형적일 경우 모델이 실패를 과소/과대 평가할 위험.

### 참고
- 위 표의 **판단 대상**은 현재 통계와 분포를 기반으로 한 **가능성**이며, 실제 정제 여부는 분석 목표(예: 예측 모델링, 비용 최적화 등)와 비즈니스 규칙에 따라 결정하면 됩니다.
- 이상치에 대해서는 **Winsorizing**(상/하한 제한), **log 변환**, 혹은 **삭제** 옵션을 고려해 볼 수 있습니다.
- 결측값은 **플래그 생성**(`no_fault`), **평균/중위값 대체**, 혹은 **레코드 제거** 등 다양한 대체 전략이 가능하니, 후속 작업에서 검토해 주세요.

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |



## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |



## 이상치·결측치 처리 기준 및 근거

### 1. 이상치 처리 기준
- **수치형 컬럼** (`downtime_hours`, `repair_duration_hours`, `maintenance_cost`, `parts_replaced_count`, `availability_rate`, `equipment_age_years`)
  - **Winsorizing**: 1·3·IQR 구간 밖의 값은 각각 **하한**(Q1‑1.5·IQR)와 **상한**(Q3+1.5·IQR)으로 대체합니다. 
    - **근거**: IQR 기반 한계는 극단값이 전체 분포에 미치는 영향을 최소화하면서 데이터 손실을 방지합니다.
  - **로그 변환**: `maintenance_cost`, `downtime_hours`, `repair_duration_hours`와 같이 오른쪽으로 긴 꼬리를 가진 컬럼은 `log1p`(log(1+x)) 변환을 적용합니다.
    - **근거**: 로그 변환은 스케일을 압축해 선형 모델·트리 모델 모두에서 학습 안정성을 높입니다.
  - **삭제**: 변환 후에도 **극단적인 상한**(예: `downtime_hours` > 30 h, `repair_duration_hours` > 20 h, `maintenance_cost` > 5 000)인 경우 해당 행을 삭제합니다.
    - **근거**: 이런 값은 실제 운영 상황에 존재하기 어려워 데이터 입력 오류 또는 특수 케이스이며, 모델에 큰 편향을 일으킬 위험이 있습니다.

### 2. 결측치 처리 기준
- **고장 관련 컬럼** (`fault_code`, `fault_category`)
  - **플래그 생성**: 결측이면 `no_fault = 1`(고장 없음)으로 설정하고, `no_fault = 0`은 실제 고장이 존재하는 경우.
    - **근거**: 결측이 예방정비 시 의도된 현상이며, 고장 여부를 명시적으로 모델에 전달할 수 있습니다.
  - **행 삭제**: `no_fault = 1`인 행을 전체 분석에서 **제거**할 경우, **이유**를 명시합니다 – “예방정비이므로 고장 예측에 기여하지 않음”.
- **`days_since_last_maintenance`**
  - **중위값 대체**: 결측값을 해당 `unit_code`별 중위값으로 채웁니다.
    - **근거**: 유지보수 간격은 군집별(유닛) 특성이 있으므로 전체 평균보다 중위값이 더 견고합니다.
- **`failure_within_30days`** (이진 레이블)
  - **리샘플링**: 클래스 불균형을 완화하기 위해 **SMOTE**(오버샘플링) 혹은 **언더샘플링**을 적용합니다.
    - **근거**: 0/1 비율이 78/22로 불균형이며, 모델이 소수 클래스(실패)를 무시할 위험이 있습니다.
- **`maintenance_success`**
  - **비율 조정**: 0값(실패) 비율이 과도하게 높을 경우, **가중치 부여**(예: 0에 1.5·weight) 혹은 **클래스 재균형**을 검토합니다.
    - **근거**: 실패와 성공이 불균형이면 정확도 지표가 왜곡될 수 있습니다.

### 3. 행 삭제(제거) 기준 및 이유 명시
| 컬럼 | 삭제 조건 | 이유 |
|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

--|## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |

|
| `downtime_hours` | > 30 h | 운영상 현실적으로 30 h 이상 정지는 비정상적인 기록이며, 모델에 편향을 줌. |
| `repair_duration_hours` | > 20 h | 실제 정비 시간 범위(일반적으로 < 10 h)와 크게 벗어나며, 데이터 오류 가능성. |
| `maintenance_cost` | > 5 000 | 비용 이상치가 전체 비용 분포를 왜곡, 비즈니스 상 비현실적. |
| `parts_replaced_count` | > 5 | 대부분 0‑3 회이며, 5회 이상은 특수 케이스(데이터 입력 오류) 가능성. |
| `availability_rate` | < 0.5 | 가용률이 0.5 이하이면 시스템이 거의 동작 중단 상태이며, 실제 운영 데이터와 어긋남. |
| `fault_code`/`fault_category` | 결측 && `maintenance_type` == "예방정비" | 예방정비는 고장이 없으므로 고장 예측 변수로 사용할 수 없음. |
| 전체 행 | `no_fault = 1` && 분석 목표가 고장 예측 | 고장 없음 행은 고장 예측 모델 학습에 기여하지 않음. |

**주의**: 위 기준은 **가이드라인**이며, 실제 적용 전에는 각 컬럼의 히스토그램·박스플롯을 확인해 최종 임계값을 조정하는 것이 좋습니다.

## 사용 컬럼 선택 가이드

### 사용 가능한 컬럼 (예시)

| 컬럼 | 설명 |
|||
| `equipment_id` | 장비 고유 ID (식별자) |
| `equipment_type` | 장비 유형 (정찰·수송·감시·교육) |
| `unit_code` | 소속 부대 코드 |
| `equipment_age_years` | 장비 연식 |
| `maintenance_type` | 현재 정비 종류 (예방·사후·긴급) |
| `fault_category` | 현재 정비 시점에 발생한 고장 종류 (고장이 있을 경우) |
| `severity` | 고장 심각도 (0‑5) |
| `fault_count_last_30d` | 최근 30일 동안 동일 장비에 발생한 고장 수 (예측 시점에 누적 가능) |
| `days_since_last_fault` | 직전 고장 이후 경과 일수 (예측 시점에 누적 가능) |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간 (예측 시점에 누적 가능) |
| `failure_within_30days` **※ (Target)** | 30일 내 재고장 여부 – 모델 목표 레이블 |
| `availability_rate` | 정비 후 가용률 (예측 시점에 아직 알 수 없지만, **가용률 자체를 예측하고 싶다면 포함**) |

### 모델에 넣지 않는다 (컬럼 & 이유)

| 컬럼 | 이유 |
|||
| `downtime_hours` | 정비가 끝난 뒤 실제 다운타임은 **예측 시점에 아직 측정되지 않음** → 미래 정보 |
| `repair_duration_hours` | 정비 소요 시간은 정비가 완료된 뒤에야 알 수 있음 → 미래 정보 |
| `maintenance_cost` | 비용은 정비 후 청구·집계가 이루어지므로 **예측 시점에 모르는 값** |
| `maintenance_success` | 정비 성공 여부는 정비 결과를 확인해야 알 수 있음 → 미래 정보 |
| `availability_rate` (대부분 경우) | 정비 후 시스템 가용률은 정비 결과에 따라 결정되므로 **예측 시점에 알 수 없음** |
| `cumulative_operating_hours` | 누적 운용시간은 정비 후 운용이 진행될 때 증가하므로 **예측 시점에 아직 알 수 없음** |
| `days_since_last_maintenance` | 정비 직후는 0이며, 이후 일수는 **정비 이후에만 측정** 가능 |
| `fault_code` | 고장 코드는 정비 결과이므로 **예측 시점에 모르는 값** |
| `no_fault` | `fault_code`와 동일하게 **정비 결과 기반 플래그** → 미래 정보 |
| `flight_hours_since_last_preventive` | 최근 예방정비 이후 비행시간은 **정비 후 누적**되므로 현재 시점에 알 수 없음 |
| `source_file` | 파일 출처 메타데이터 – 모델에 의미 없음 |


# 위험 표시 기준 (Validation Period)

## 원래 비용 가정 (missed=300만원, flagged=60만원)
- 최적 임계값: 0.11
- 놓친 재고장 수: 23
- 기준 이상 건수 (예측 양성): 196
- 총 비용: 18660만원

## 놓친 재고장 비용을 600만원으로 변경
- 최적 임계값: 0.11
- 놓친 재고장 수: 23
- 기준 이상 건수: 196
- 총 비용: 25560만원

---
**참고**: 검증 기간은 2024‑07~2024‑12이며, 2025 시험 데이터는 사용하지 않았습니다.
