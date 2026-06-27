# Data Cleaning & Preparation: The Architecture of Data Integrity

## 📌 Project Overview
This repository contains **Project 1** of the **DecodeLabs Industrial Training Kit (Batch 2026)**. In an e-commerce data analytics pipeline, dirty data propagates exponentially—turning minor initial errors into massive strategic collapses. This project serves as the foundational phase, transforming a raw, messy transactional dataset into a verified, production-ready "Gold Standard" source of truth.

Using a programmatic, script-based workflow in **Python (pandas, openpyxl)**, a rigorous record-by-record audit was executed to ensure absolute data integrity, meeting the strict **0% error rate** threshold required to pass the Project 2 Verification Gate.

---

## 📊 Dataset Specifications
The pipeline processed the dataset `Dataset_for_Data_Analytics.xlsx`, containing **1,200 e-commerce order records** evaluated across **14 distinct fields**:

| Column Name | Data Type | Analytical Description |
| :--- | :--- | :--- |
| **OrderID** | Text (ID) | Unique order identifier, regex-validated format: `ORD######` |
| **Date** | Date | Transaction timestamp standardized to ISO 8601 (`YYYY-MM-DD`) |
| **CustomerID** | Text (ID) | Unique customer identifier, regex-validated format: `C#####` |
| **Product** | Categorical | Item purchased (7 core categories) |
| **Quantity** | Numeric | Discrete units purchased per order (Range: 1–5) |
| **UnitPrice** | Numeric | Base cost per unit (Standardized 2-decimal currency float) |
| **ShippingAddress** | Text | Delivery destination |
| **PaymentMethod** | Categorical | Settlement channel used (5 categories) |
| **OrderStatus** | Categorical | Current fulfillment state (5 categories) |
| **Tracking Number** | Text (ID) | Shipment tracking code, regex-validated format: `TRK###########` |
| **ItemsInCart** | Numeric | Total items present in the digital cart at checkout |
| **CouponCode** | Categorical | Promotional code applied (3 active codes + imputed missing records) |
| **Referral Source** | Categorical | Marketing channel driving the acquisition (5 categories) |
| **TotalPrice** | Numeric | Total order value; programmatically cross-validated against ($Quantity \times UnitPrice$) |

---

## 🛠️ Data Quality Audit & Methodology
While the dataset's scale sits within Excel limits, **Python with pandas** was deliberately chosen to ensure a fully automated, reproducible, and auditable pipeline—avoiding the risks associated with manual point-and-click modifications.

### Core Pipeline Validations
1. **Null/Blank Scanning:** Exhaustive cross-field checks across all 1,200 rows.
2. **Duplicate Detection:** Multi-level testing evaluating full rows, unique `OrderID` tokens, and `Tracking Number` strings.
3. **Regex Pattern Enforcements:** Ensuring perfect structural conformance for all unique identifier fields.
4. **Logical & Mathematical Constraints:** Cross-field checking that $\text{TotalPrice} = \text{Quantity} \times \text{UnitPrice}$ and assessing structural consistency between `ItemsInCart` and `Quantity`.
5. **Text Standardization:** Global whitespace trims and case-insensitivity scans.

---

## 🔍 Key Audit Findings & Imputation Logic

### Categorical Imputation vs. Listwise Deletion
The data quality audit revealed that **309 out of 1,200 records (25.75%)** lacked a value in the `CouponCode` column. 

* **The Problem with Deletion:** Dropping these rows (listwise deletion) would systematically discard over a quarter of the dataset, severely diminishing statistical power.
* **The Engineering Solution:** A granular review confirmed that the missing fields were not data-entry errors, but legitimate categorical gaps representing orders finalized without a promotional discount. All 309 null records were programmatically imputed with the explicit domain label `"No Coupon"`. 

This treatment preserves all 1,200 rows for downstream business intelligence (e.g., calculating true coupon conversion rates) while preventing downstream analysis engines from misinterpreting raw null values.

#### Post-Imputation Distribution of `CouponCode`
* **FREESHIP:** 313 records (26.08%)
* **No Coupon (Imputed):** 309 records (25.75%)
* **WINTER15:** 292 records (24.33%)
* **SAVE10:** 286 records (23.83%)

---

## 🏁 Verification Gate Results
To transition from Project 1 (Preparation) to Project 2 (Modeling/Analytics), the data had to clear an absolute quality threshold:

| Evaluation Criterion | Required Threshold | Final Achieved Result | Status |
| :--- | :--- | :--- | :--- |
| **Duplicate Identifiers (`OrderID`)** | 0% Error Rate | 0% | ✅ PASS |
| **Duplicate Identifiers (`Tracking Number`)** | 0% Error Rate | 0% | ✅ PASS |
| **Date Format Anomalies** | 0% Error Rate | 0% | ✅ PASS |
| **Unresolved Missing Values** | Fully Remediated | 0 Remaining | ✅ PASS |

---

## 📑 Programmatic Change Log
Every data transformation is strictly tracked to ensure historical reproducibility:

* **`CR001`** | Standardized `Date` column to strict ISO 8601 (`YYYY-MM-DD`) formatting. (Impact: 1,200 rows standardized).
* **`CR002`** | Imputed missing `CouponCode` blank entries with categorical label `"No Coupon"`. (Impact: 309 rows preserved and optimized for analysis).
* **`CR003`** | Audited `OrderID` and `Tracking Number` spaces for duplicates. (Impact: Confirmed 0 duplicate identifiers; no rows dropped).
* **`CR004`** | Executed formula integrity cross-checks ($\text{TotalPrice} = \text{Quantity} \times \text{UnitPrice}$). (Impact: 100% mathematical consistency verified).
* **`CR005`** | Scanned categorical column matrices for inconsistent string casings or trailing whitespaces. (Impact: 0 structural text inconsistencies discovered).
* **`CR006`** | Evaluated ID string formations via Regex expressions. (Impact: Confirmed 100% structural pattern conformance).

---

## 📂 Deliverables & Repository Structure
* `/data/Dataset_for_Data_Analytics.xlsx` - Raw, incoming messy dataset.
* `/data/Dataset_for_Data_Analytics_CLEANED.xlsx` - The finalized, verified production-ready file.
* `/src/data_cleaning_pipeline.py` - Programmatic pandas workflow script execution.
* `/docs/Project_1_Submission_Report.pdf` - Fully documented engineering milestone paper.
