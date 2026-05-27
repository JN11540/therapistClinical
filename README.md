# TherapistClinical — 系統說明文件

---

## 專案結構

```
webServer/
├── main.py
├── __init__.py
├── controller/
│   ├── __init__.py
│   ├── auth.py
│   ├── clinician.py
│   ├── patient.py
│   ├── measurement.py
│   ├── rom_assessment.py
│   ├── mmt_assessment.py
│   ├── tug_assessment.py
│   ├── sf_36_assessment.py
│   ├── womac_assessment.py
│   └── koos_assessment.py
├── service/
│   ├── __init__.py
│   ├── clinician.py
│   ├── patient.py
│   ├── measurement.py
│   ├── rom_assessment.py
│   ├── mmt_assessment.py
│   ├── tug_assessment.py
│   ├── sf_36_assessment.py
│   ├── womac_assessment.py
│   └── koos_assessment.py
├── model/
│   ├── __init__.py
│   ├── clinician.py
│   ├── patient.py
│   ├── measurement.py
│   ├── rom_assessment.py
│   ├── mmt_assessment.py
│   ├── tug_assessment.py
│   ├── sf_36_assessment.py
│   ├── womac_assessment.py
│   └── koos_assessment.py
├── schema/
│   ├── __init__.py
│   ├── clinician.py
│   ├── patient.py
│   ├── measurement.py
│   ├── rom_assessment.py
│   ├── mmt_assessment.py
│   ├── tug_assessment.py
│   ├── sf_36_assessment.py
│   ├── womac_assessment.py
│   └── koos_assessment.py
├── crud/
│   ├── __init__.py
│   ├── base.py
│   ├── clinician.py
│   ├── patient.py
│   ├── measurement.py
│   ├── rom_assessment.py
│   ├── mmt_assessment.py
│   ├── tug_assessment.py
│   ├── sf_36_assessment.py
│   ├── womac_assessment.py
│   └── koos_assessment.py
└── core/
    ├── __init__.py
    ├── config.py
    ├── database.py
    ├── security.py
    └── dependencies.py
```

---

## 資料庫結構說明

本文件說明系統的資料庫 Schema，涵蓋臨床醫師、病患基本資料，以及各項評估量表。

各量表透過自身的 `measurement_id` 與 `measurement` 建立關聯（一對一）。

---

## 資料表總覽

| 資料表 | 說明 |
|---|---|
| `clinician` | 臨床醫師帳號與基本資料 |
| `patient` | 病患基本資料與病史 |
| `measurement` | 病患單次評估紀錄 |
| `rom_assessment` | 關節活動度（ROM）評估 |
| `mmt_assessment` | 徒手肌力測試（MMT）評估 |
| `tug_assessment` | 計時起走測試（TUG）評估 |
| `sf_36_assessment` | SF-36 生活品質量表 |
| `womac_assessment` | WOMAC 骨關節炎量表 |
| `koos_assessment` | KOOS 膝關節損傷量表 |
| `treatment` | 病患治療計畫 |
| `treatment_content` | 治療計畫的動作內容 |
| `exercise` | 運動動作定義 |

---

## clinician

臨床醫師的帳號資訊與所屬機構。

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `name` | str | | 姓名 |
| `email` | str | ✓ | 電子信箱 |
| `phone` | str | ✓ | 電話 |
| `profession` | str | ✓ | 職種 |
| `specialty` | str | ✓ | 專科 |
| `years_of_experience` | int | ✓ | 年資 |
| `institution` | str | ✓ | 所屬機構 |
| `department` | str | ✓ | 科別 |
| `clinic_location` | str | ✓ | 診間地點 |
| `username` | str | | 登入帳號 |
| `password_hash` | str | | 密碼雜湊值 |
| `created_at` | int (Unix timestamp) | | 建立時間 |
| `updated_at` | int (Unix timestamp) | | 更新時間 |

---

## patient

病患基本資料、病史及臨床背景。

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `clinician_id` | int | | 所屬醫師（FK → clinician） |
| `name` | str | | 姓名 |
| `height` | float | | 身高（公分） |
| `weight` | float | | 體重（公斤） |
| `phone` | str | | 電話 |
| `email` | str | | 信箱 |
| `diagnosis` | str | | 診斷（e.g., 雙側膝退化性關節炎 Grade I） |
| `date_of_birth` | int (Unix timestamp) | | 出生日期 |
| `gender` | int | | 性別（0: female / 1: male） |
| `profession` | str | ✓ | 職業（e.g., 雜貨店員工） |
| `kl_grade` | int | ✓ | KL Grade（X 光骨關節炎分級） |
| `chief_complaint` | str | ✓ | 主訴（e.g., 晨間僵硬、內側疼痛） |
| `aggravating_factors` | str | ✓ | 加重因素（e.g., 長時間步行、屈膝） |
| `medical_history` | str | ✓ | 相關病史（e.g., 貧血、脾腫大） |
| `imaging_findings` | str | ✓ | 影像學結果（X 光描述） |
| `symptom_duration_months` | int | ✓ | 病程（月） |
| `visit_flow` | str | ✓ | 就診流程紀錄 |
| `other_knee_treatment_comment` | str | ✓ | 接受其他膝蓋治療描述 |
| `created_at` | int (Unix timestamp) | | 建立時間 |
| `updated_at` | int (Unix timestamp) | | 更新時間 |

---

## measurement

每次評估的基本紀錄，各量表透過 `measurement_id` 與此表關聯。

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `patient_id` | int | | 所屬病患（FK → patient） |
| `name` | str | | 評估記錄名稱 |
| `measured_at` | int (Unix timestamp) | | 評估時間 |
| `sf_36_total` | int | ✓ | 總分 |
| `womac_total` | int | ✓ | 總分（0–96 分） |
| `koos_total` | int | ✓ | 總分 |
| `created_at` | int (Unix timestamp) | | 建立時間 |
| `updated_at` | int (Unix timestamp) | | 更新時間 |

---

## objective_measurement

病患客觀量表

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `measurement_id` | int | | 所屬病患量表（FK → measurement） |
| `side` | int | | 評估側（0: left / 1: right） |
| `vas_before_test` | int | ✓ | 測試前數值疼痛評分（VAS） |
| `vas_after_test` | int | ✓ | 測試後數值疼痛評分（VAS） |
| `tug_time_seconds` | float | | tug 完成時間（秒） |
| `tug_assistive_device` | bool | ✓ | tug 輔具使用情況 |
| `tug_comment` | str | ✓ | tug 註記 |
| `ftsst_time_seconds` | float | | ftsst 完成時間（秒） |
| `ftsst_assistive_device` | bool | ✓ | ftsst 輔具使用情況 |
| `ftsst_comment` | str | ✓ | ftsst 註記 |
| `mwt_10_time_seconds` | float | | 10mwt 完成時間（秒） |
| `mwt_10_assistive_device` | bool | ✓ | 10mwt 輔具使用情況 |
| `mwt_10_comment` | str | ✓ | 10mwt 註記 |
| `sls_time_seconds` | float | | sls 完成時間（秒） |
| `sls_comment` | str | ✓ | sls 註記 |
| `rom_knee_flexion_min` | int | | 膝屈曲最小角度 |
| `rom_knee_flexion_max` | int | | 膝屈曲最大角度 |
| `rom_knee_flexion_comment` | str | ✓ | 膝伸直備註 |
| `rom_knee_extension_min` | int | ✓ | 膝伸直最小角度 |
| `rom_knee_extension_max` | int | ✓ | 膝伸直最大角度 |
| `rom_knee_extension_comment` | str | ✓ | 膝伸直備註 |
| `mmt_knee_flexion` | int | | 膝屈曲 |
| `mmt_knee_extension` | int | | 膝伸直 |
| `thigh_circumference` | float | ✓ | 大腿圍 |

---

## treatment

病患的治療計畫，記錄計畫名稱、所屬病患及執行期間。

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `name` | str | | 治療計畫名稱 |
| `patient_id` | int | | 所屬病患（FK → patient） |
| `start_time` | int (Unix timestamp) | | 開始時間 |
| `end_time` | int (Unix timestamp) | | 結束時間 |
| `created_at` | int (Unix timestamp) | | 建立時間 |
| `updated_at` | int (Unix timestamp) | ✓ | 修改時間 |

---

## treatment_content

治療計畫的動作內容，記錄每個動作的組數、次數與休息時間。

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `treatment_id` | int | | 所屬治療計畫（FK → treatment） |
| `exercise_id` | int | | 所屬動作（FK → exercise） |
| `sets` | int | | 組數 |
| `set_rest_time` | int | | 組間休息時間（秒） |
| `reps` | int | | 每組次數 |
| `date` | int (Unix timestamp) | | 規劃時間 |

---

## exercise

可用的運動動作定義。

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `name` | str | | 動作名稱 |
| `rep_stage1` | int | | 動作（第一階段）時間（秒） |
| `rep_stage2` | int | | 動作（第二階段）時間（秒） |
| `rep_stage3` | int | | 動作（第三階段）時間（秒） |
| `rep_stage4` | int | | 動作（第四階段）時間（秒） |

---

## treatment_result

| 欄位 | 型別 | Nullable | 說明 |
|---|---|:---:|---|
| `id` | int | | 主鍵 |
| `treatment_id` | int | | 所屬治療計畫（FK → treatment） |
| `treatment_content_id` | int | | 所屬治療計畫的動作內容（FK → treatment_content） |
| `reps` | int | | 實作總次數 |
| `total_time` | int | | 實作總時間（秒） |
| `date` | int (Unix timestamp) | | 實作時間 |