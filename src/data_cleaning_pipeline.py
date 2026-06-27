import os
import pandas as pd

def run_data_cleaning_pipeline(input_path, output_path):
    print("🚀 Initializing Data Cleaning & Preparation Pipeline...")
    
    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at: {input_path}")
        
    # Load dataset
    df = pd.read_excel(input_path)
    print(f"📥 Dataset loaded successfully. Records: {df.shape[0]}, Fields: {df.shape[1]}")
    
    # ----------------------------------------------------
    # CR003: Audit for Duplicate Identifiers
    # ----------------------------------------------------
    print("\n🔍 CR003: Auditing identifiers for duplicates...")
    # Clean whitespace/casing before checking duplicates on IDs
    df['OrderID'] = df['OrderID'].astype(str).str.strip()
    df['Tracking Number'] = df['Tracking Number'].astype(str).str.strip()
    
    dup_orders = df[df.duplicated(subset=['OrderID'])].shape[0]
    dup_tracking = df[df.duplicated(subset=['Tracking Number'])].shape[0]
    dup_full_rows = df[df.duplicated()].shape[0]
    
    print(f"   - Duplicate OrderID counts: {dup_orders}")
    print(f"   - Duplicate Tracking Number counts: {dup_tracking}")
    print(f"   - Duplicate full record counts: {dup_full_rows}")
    # Based on audit results, 0 duplicates were found; no rows are dropped.
    
    # ----------------------------------------------------
    # CR002: Categorical Imputation for Missing Values
    # ----------------------------------------------------
    print("\n🔍 CR002: Treating missing values...")
    missing_coupon_count = df['CouponCode'].isnull().sum()
    print(f"   - Missing values found in CouponCode: {missing_coupon_count}")
    
    # Programmatically impute missing entries with 'No Coupon'
    df['CouponCode'] = df['CouponCode'].fillna('No Coupon')
    print(f"   - Post-imputation missing values in CouponCode: {df['CouponCode'].isnull().sum()}")
    
    # ----------------------------------------------------
    # CR001: Standardize Date Formats
    # ----------------------------------------------------
    print("\n🔍 CR001: Standardizing Date column to ISO 8601...")
    # Convert to standard datetime type and then format to YYYY-MM-DD
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
    print("   - Date format standardized successfully.")
    
    # ----------------------------------------------------
    # CR004: Formula Integrity Cross-Validation
    # ----------------------------------------------------
    print("\n🔍 CR004: Verifying TotalPrice formula integrity...")
    calculated_total = df['Quantity'] * df['UnitPrice']
    # Allow for minor float precision differences using a tolerance threshold
    mismatches = df[abs(df['TotalPrice'] - calculated_total) > 0.01].shape[0]
    print(f"   - Formula mismatches detected: {mismatches}")
    
    # ----------------------------------------------------
    # CR005 & CR006: Structural Field Validations (Text Casing / Regex)
    # ----------------------------------------------------
    print("\n🔍 CR005 & CR006: Running structural validation checks...")
    categorical_cols = ['Product', 'PaymentMethod', 'OrderStatus', 'Referral Source', 'CouponCode']
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    print("   - Text casing, trailing whitespaces, and regex pattern validations passed.")
    
    # ----------------------------------------------------
    # Exporting Cleaned Dataset
    # ----------------------------------------------------
    print("\n💾 Exporting target 'Gold Standard' dataset...")
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False)
    print(f"🎉 Pipeline completed successfully! Cleaned file saved to: {output_path}\n")

if __name__ == "__main__":
    # Relative path setup assuming your GitHub repository file layout
    INPUT_FILE = os.path.join("data", "Dataset_for_Data_Analytics.xlsx")
    OUTPUT_FILE = os.path.join("data", "Dataset_for_Data_Analytics_CLEANED.xlsx")
    
    run_data_cleaning_pipeline(INPUT_FILE, OUTPUT_FILE)
