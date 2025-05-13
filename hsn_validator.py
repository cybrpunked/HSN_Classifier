import streamlit as st
import pandas as pd
import re
import io
from typing import List, Dict, Tuple, Optional, Union

# --- SESSION STATE INITIALIZATION ---
if 'hsn_data' not in st.session_state:
    st.session_state.hsn_data = None
if 'sac_data' not in st.session_state:
    st.session_state.sac_data = None
if 'loaded_files' not in st.session_state:
    st.session_state.loaded_files = False

# --- MAIN CLASS ---
class HSNValidator:
    def __init__(self):
        pass  # Keeping this in case future state needs to be added

    def load_sample_data(self):
        """Preloads example HSN and SAC entries for demonstration purposes."""
        hsn_data = {
            'HSNCode': ['01', '0101', '01011010'],
            'Description': [
                'Live Animals', 
                'Live Horses and Similar Creatures', 
                'Pure-bred Breeding Horses'
            ]
        }

        sac_data = {
            'SAC_CD': ['99', '9954', '995411'],
            'SAC_Description': [
                'All Services',
                'Construction Services',
                'Affordable Residential Construction'
            ]
        }

        st.session_state.hsn_data = pd.DataFrame(hsn_data)
        st.session_state.sac_data = pd.DataFrame(sac_data)
        st.session_state.loaded_files = True
        return True

    def load_data(self, hsn_file=None, sac_file=None):
        """Allows users to upload their own Excel datasets."""
        try:
            if hsn_file:
                hsn_df = pd.read_excel(hsn_file)
                hsn_df.columns = [col.strip() for col in hsn_df.columns]
                if 'HSNCode' not in hsn_df or 'Description' not in hsn_df:
                    st.error("Missing expected columns in HSN file.")
                    return False
                hsn_df['HSNCode'] = hsn_df['HSNCode'].astype(str)
                st.session_state.hsn_data = hsn_df

            if sac_file:
                sac_df = pd.read_excel(sac_file)
                sac_df.columns = [col.strip() for col in sac_df.columns]
                if 'SAC_CD' not in sac_df or 'SAC_Description' not in sac_df:
                    st.error("Missing expected columns in SAC file.")
                    return False
                sac_df['SAC_CD'] = sac_df['SAC_CD'].astype(str)
                st.session_state.sac_data = sac_df

            st.session_state.loaded_files = True
            return True

        except Exception as e:
            st.error(f"An error occurred while loading files: {e}")
            return False

    def validate_format(self, code: str, code_type: str = 'HSN') -> bool:
        """Checks if a code follows the correct format."""
        code = code.strip()
        if not code:
            return False

        pattern = r'^\d{1,8}$' if code_type == 'HSN' else r'^\d{1,6}$'
        return bool(re.match(pattern, code))

    def validate_existence(self, code: str, code_type: str = 'HSN') -> bool:
        """Checks if a code exists in the dataset."""
        code = code.strip()
        data = st.session_state.hsn_data if code_type == 'HSN' else st.session_state.sac_data
        column = 'HSNCode' if code_type == 'HSN' else 'SAC_CD'
        return code in data[column].values if data is not None else False

    def get_description(self, code: str, code_type: str = 'HSN') -> str:
        """Fetches the description for a given code."""
        data = st.session_state.hsn_data if code_type == 'HSN' else st.session_state.sac_data
        column = 'HSNCode' if code_type == 'HSN' else 'SAC_CD'
        desc_col = 'Description' if code_type == 'HSN' else 'SAC_Description'

        if data is not None:
            result = data[data[column] == code.strip()]
            if not result.empty:
                return result.iloc[0][desc_col]

        return ""

    def validate_codes(self, codes: Union[str, List[str]], code_type: str = 'HSN') -> List[Dict]:
        """Validates a list or comma-separated string of codes."""
        if isinstance(codes, str):
            codes = [c.strip() for c in codes.split(',') if c.strip()]

        results = []
        for code in codes:
            valid_format = self.validate_format(code, code_type)
            exists = self.validate_existence(code, code_type) if valid_format else False
            description = self.get_description(code, code_type) if exists else ""

            results.append({
                "code": code,
                "format_valid": valid_format,
                "exists": exists,
                "description": description
            })

        return results
