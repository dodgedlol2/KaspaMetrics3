import pandas as pd
import numpy as np
import gspread
from google.oauth2 import service_account
from scipy.stats import linregress
import streamlit as st
from datetime import datetime, timedelta
import os

class KaspaDataManager:
    """
    Centralized data management system for Kaspa Analytics Platform
    Handles all Google Sheets data loading and analysis functions
    """
    
    def __init__(self):
        self.genesis_date = pd.to_datetime('2021-11-07', utc=True)
        self._client = None
    
    def get_google_credentials(self):
        """
        Get Google Cloud credentials from environment variables (Heroku) 
        or Streamlit secrets (local development)
        """
        try:
            # Try environment variables first (Heroku - Method 2)
            gcp_type = os.environ.get("GCP_TYPE")
            
            if gcp_type:
                # Build credentials from individual environment variables
                credentials = {
                    "type": os.environ.get("GCP_TYPE"),
                    "project_id": os.environ.get("GCP_PROJECT_ID"),
                    "private_key_id": os.environ.get("GCP_PRIVATE_KEY_ID"),
                    "private_key": os.environ.get("GCP_PRIVATE_KEY"),
                    "client_email": os.environ.get("GCP_CLIENT_EMAIL"),
                    "client_id": os.environ.get("GCP_CLIENT_ID"),
                    "auth_uri": os.environ.get("GCP_AUTH_URI"),
                    "token_uri": os.environ.get("GCP_TOKEN_URI"),
                    "auth_provider_x509_cert_url": os.environ.get("GCP_AUTH_PROVIDER_X509_CERT_URL"),
                    "client_x509_cert_url": os.environ.get("GCP_CLIENT_X509_CERT_URL"),
                    "universe_domain": os.environ.get("GCP_UNIVERSE_DOMAIN")
                }
                
                # Remove any None values
                credentials = {k: v for k, v in credentials.items() if v is not None}
                
                st.write("Debug: Google credentials loaded from environment variables")
                return credentials
                
            # Fallback: Try Streamlit secrets (local development)
            else:
                gcp_secrets = st.secrets["gcp_service_account"]
                credentials = dict(gcp_secrets)
                st.write("Debug: Google credentials loaded from Streamlit secrets")
                return credentials
                
        except Exception as e:
            st.write(f"Debug: Error loading Google credentials: {e}")
            return None
    
    @property
    def client(self):
        """Lazy initialization of Google Sheets client"""
        if self._client is None:
            try:
                # Get credentials using the new method
                creds_dict = self.get_google_credentials()
                
                if not creds_dict:
                    st.error("Google credentials not found!")
                    return None
                
                # Create credentials object
                credentials = service_account.Credentials.from_service_account_info(
                    creds_dict,
                    scopes=["https://www.googleapis.com/auth/spreadsheets"]
                )
                
                self._client = gspread.authorize(credentials)
                st.success("✅ Connected to Google Sheets!")
                
            except Exception as e:
                st.error(f"Error connecting to Google Sheets: {e}")
                return None
                
        return self._client
    
    # ===== DATA LOADING METHODS =====
    
    @st.cache_data(ttl=3600)
    def load_hashrate_data(_self):
        """Load hashrate data from Google Sheets"""
        try:
            if not _self.client:
                st.error("Google Sheets client not available")
                return pd.DataFrame(), _self.genesis_date
                
            sheet_id = "1NPwQh2FQKVES7OYUzKQLKwuOrRuIivGhOtQWZZ-Sp80"
            worksheet = _self.client.open_by_key(sheet_id).worksheet("kaspa_daily_hashrate (3)")
            data = worksheet.get_all_values()
            
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df[['Date', 'Hashrate (H/s)']]
            
            df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y', utc=True)
            df['Hashrate (H/s)'] = df['Hashrate (H/s)'].astype(float)
            
            df['days_from_genesis'] = (df['Date'] - _self.genesis_date).dt.days
            df = df[df['days_from_genesis'] >= 0]
            df['Hashrate_PH'] = df['Hashrate (H/s)'] / 1e15
            
            return df.sort_values('Date').reset_index(drop=True), _self.genesis_date
        except Exception as e:
            st.error(f"Failed to load hashrate data: {str(e)}")
            return pd.DataFrame(), _self.genesis_date
    
    @st.cache_data(ttl=3600)
    def load_price_data(_self):
        """Load price data from Google Sheets"""
        try:
            if not _self.client:
                st.error("Google Sheets client not available")
                return pd.DataFrame(), _self.genesis_date
                
            sheet_id = "1rMBuWn0CscUZkcKy2gleH85rXSO6U4YOSk3Sz2KuR_s"
            worksheet = _self.client.open_by_key(sheet_id).worksheet("kaspa_daily_price")
            data = worksheet.get_all_values()
            
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df[['Date', 'Price']]
            
            df['Date'] = pd.to_datetime(df['Date'], utc=True)
            df['Price'] = df['Price'].astype(float)
            
            df['days_from_genesis'] = (df['Date'] - _self.genesis_date).dt.days
            df = df[df['days_from_genesis'] >= 0]
            
            return df.sort_values('Date').reset_index(drop=True), _self.genesis_date
        except Exception as e:
            st.error(f"Failed to load price data: {str(e)}")
            return pd.DataFrame(), _self.genesis_date
    
    @st.cache_data(ttl=3600)
    def load_volume_data(_self):
        """Load volume data from Google Sheets"""
        try:
            if not _self.client:
                st.error("Google Sheets client not available")
                return pd.DataFrame()
                
            sheet_id = "1IdAmETrtZ8_lCuSQwEyDLtMIGiQbJFOyGGpMa9_hxZc"
            worksheet = _self.client.open_by_key(sheet_id).worksheet("KAS_VOLUME_ETC")
            data = worksheet.get_all_values()
            
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df[['date', 'price', 'total_volume']]
            df = df.rename(columns={
                'date': 'Date',
                'price': 'Price',
                'total_volume': 'Volume_USD'
            })
            
            df['Date'] = pd.to_datetime(df['Date'], utc=True)
            df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
            df['Volume_USD'] = pd.to_numeric(df['Volume_USD'], errors='coerce')
            df = df.dropna()
            
            df['days_from_genesis'] = (df['Date'] - _self.genesis_date).dt.days
            df = df[df['days_from_genesis'] >= 0]
            
            return df.sort_values('Date').reset_index(drop=True)
        except Exception as e:
            st.error(f"Failed to load volume data: {str(e)}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=3600)
    def load_marketcap_data(_self):
        """Load market cap data from Google Sheets"""
        try:
            if not _self.client:
                st.error("Google Sheets client not available")
                return pd.DataFrame(), _self.genesis_date
                
            sheet_id = "15BZcsswJPZZF2MQ6S_m9CtbHPtVJVcET_VjZ9_aJ8nY"
            worksheet = _self.client.open_by_key(sheet_id).worksheet("kaspa_market_cap")
            data = worksheet.get_all_values()
            
            df = pd.DataFrame(data[1:], columns=data[0])
            df = df[['Date', 'MarketCap']]
            
            df['Date'] = pd.to_datetime(df['Date'], utc=True)
            df['MarketCap'] = df['MarketCap'].astype(float)
            
            df['days_from_genesis'] = (df['Date'] - _self.genesis_date).dt.days
            df = df[df['days_from_genesis'] >= 0]
            df['MarketCap_B'] = df['MarketCap'] / 1e9
            
            return df.sort_values('Date').reset_index(drop=True), _self.genesis_date
        except Exception as e:
            st.error(f"Failed to load market cap data: {str(e)}")
            return pd.DataFrame(), _self.genesis_date
    
    @st.cache_data(ttl=3600)
    def load_difficulty_data(_self):
        """Load mining difficulty data from Google Sheets"""
        try:
            if not _self.client:
                st.error("Google Sheets client not available")
                return pd.DataFrame(), _self.genesis_date
                
            # Using same hashrate sheet for now - you can update with actual difficulty sheet ID
            sheet_id = "1NPwQh2FQKVES7OYUzKQLKwuOrRuIivGhOtQWZZ-Sp80"
            worksheet = _self.client.open_by_key(sheet_id).worksheet("kaspa_daily_hashrate (3)")
            data = worksheet.get_all_values()
            
            df = pd.DataFrame(data[1:], columns=data[0])
            # Assuming difficulty data is in the same sheet - adjust column names as needed
            if 'Difficulty' in df.columns:
                df = df[['Date', 'Difficulty']]
                df['Difficulty'] = df['Difficulty'].astype(float)
            else:
                # Fallback: calculate estimated difficulty from hashrate
                df = df[['Date', 'Hashrate (H/s)']]
                df['Hashrate (H/s)'] = df['Hashrate (H/s)'].astype(float)
                # Rough estimate: Difficulty ≈ Hashrate * target_time / actual_time
                df['Difficulty'] = df['Hashrate (H/s)'] * 1.0  # Placeholder calculation
            
            df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y', utc=True)
            df['days_from_genesis'] = (df['Date'] - _self.genesis_date).dt.days
            df = df[df['days_from_genesis'] >= 0]
            
            return df.sort_values('Date').reset_index(drop=True), _self.genesis_date
        except Exception as e:
            st.error(f"Failed to load difficulty data: {str(e)}")
            return pd.DataFrame(), _self.genesis_date
    
    @st.cache_data(ttl=3600)
    def load_social_metrics_data(_self):
        """Load social media metrics data - placeholder for future implementation"""
        try:
            # Placeholder for social metrics Google Sheet
            # You'll need to provide the actual sheet ID and structure
            social_data = {
                'Date': pd.date_range(start='2024-01-01', end='2024-12-31', freq='D'),
                'Twitter_Followers': np.random.randint(10000, 50000, 365),
                'Reddit_Members': np.random.randint(5000, 25000, 365),
                'Discord_Members': np.random.randint(3000, 15000, 365),
                'Telegram_Members': np.random.randint(2000, 10000, 365)
            }
            
            df = pd.DataFrame(social_data)
            df['days_from_genesis'] = (df['Date'] - _self.genesis_date).dt.days
            df = df[df['days_from_genesis'] >= 0]
            
            return df.sort_values('Date').reset_index(drop=True)
        except Exception as e:
            st.error(f"Failed to load social metrics data: {str(e)}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=3600)
    def load_social_trends_data(_self):
        """Load social trends data - placeholder for future implementation"""
        try:
            # Placeholder for social trends analysis
            trends_data = {
                'Date': pd.date_range(start='2024-01-01', end='2024-12-31', freq='D'),
                'Sentiment_Score': np.random.uniform(-1, 1, 365),
                'Mention_Volume': np.random.randint(100, 1000, 365),
                'Engagement_Rate': np.random.uniform(0, 0.1, 365),
                'Trending_Score': np.random.uniform(0, 100, 365)
            }
            
            df = pd.DataFrame(trends_data)
            df['days_from_genesis'] = (df['Date'] - _self.genesis_date).dt.days
            df = df[df['days_from_genesis'] >= 0]
            
            return df.sort_values('Date').reset_index(drop=True)
        except Exception as e:
            st.error(f"Failed to load social trends data: {str(e)}")
            return pd.DataFrame()
    
    # ===== ANALYSIS METHODS =====
    
    def fit_power_law(self, df, y_col='Hashrate_PH', x_col=None):
        """
        Fits a power law y = a*x^b to the data
        Maintains backward compatibility while adding new functionality
        
        Args:
            df: DataFrame containing the data
            y_col: Column name for dependent variable
            x_col: Optional column name for independent variable (default: 'days_from_genesis')
        """
        # Handle backward compatibility
        if x_col is None:
            x_col = 'days_from_genesis'
        
        # Filter out invalid values
        valid_data = df[(df[x_col] > 0) & (df[y_col] > 0)].copy()
        
        if len(valid_data) < 2:
            raise ValueError("Not enough valid data points for power law fitting")
        
        # Perform linear regression on log-transformed data
        slope, intercept, r_value, _, _ = linregress(
            np.log(valid_data[x_col]),
            np.log(valid_data[y_col]))
        
        # Convert back to power law coefficients
        a = np.exp(intercept)
        b = slope
        r2 = r_value**2
        
        return a, b, r2
    
    def calculate_growth_metrics(self, df, value_col='Price', date_col='Date'):
        """Calculate periodic growth rates and volatility"""
        df = df.sort_values(date_col).copy()
        
        metrics = {
            'current_value': df[value_col].iloc[-1] if len(df) > 0 else 0,
            'daily_return': df[value_col].pct_change().iloc[-1] if len(df) > 1 else 0,
            'weekly_return': df[value_col].pct_change(7).iloc[-1] if len(df) > 7 else 0,
            'monthly_return': df[value_col].pct_change(30).iloc[-1] if len(df) > 30 else 0,
            'annualized_volatility': df[value_col].pct_change().std() * np.sqrt(365) if len(df) > 1 else 0
        }
        
        return metrics
    
    def calculate_correlation_matrix(self, price_df, volume_df, hashrate_df, marketcap_df):
        """Calculate correlation matrix between different metrics"""
        try:
            # Merge all dataframes on Date
            merged_df = price_df[['Date', 'Price']].copy()
            
            if not volume_df.empty:
                merged_df = merged_df.merge(volume_df[['Date', 'Volume_USD']], on='Date', how='outer')
            
            if not hashrate_df.empty:
                merged_df = merged_df.merge(hashrate_df[['Date', 'Hashrate_PH']], on='Date', how='outer')
            
            if not marketcap_df.empty:
                merged_df = merged_df.merge(marketcap_df[['Date', 'MarketCap_B']], on='Date', how='outer')
            
            # Calculate correlation matrix
            numeric_cols = merged_df.select_dtypes(include=[np.number]).columns
            correlation_matrix = merged_df[numeric_cols].corr()
            
            return correlation_matrix
        except Exception as e:
            st.error(f"Failed to calculate correlation matrix: {str(e)}")
            return pd.DataFrame()
    
    def filter_data_by_timeframe(self, df, timeframe='All', date_col='Date'):
        """Filter dataframe by specified timeframe"""
        if df.empty:
            return df
            
        df = df.sort_values(date_col).copy()
        last_date = df[date_col].iloc[-1]
        
        if timeframe == "1W":
            start_date = last_date - timedelta(days=7)
        elif timeframe == "1M":
            start_date = last_date - timedelta(days=30)
        elif timeframe == "3M":
            start_date = last_date - timedelta(days=90)
        elif timeframe == "6M":
            start_date = last_date - timedelta(days=180)
        elif timeframe == "1Y":
            start_date = last_date - timedelta(days=365)
        else:  # "All"
            return df
            
        return df[df[date_col] >= start_date].reset_index(drop=True)
    
    def get_latest_metrics(self, df, value_col, date_col='Date'):
        """Get latest value and percentage changes for metrics cards"""
        if df.empty:
            return {
                'current': 0,
                'daily_change': 0,
                'weekly_change': 0,
                'monthly_change': 0
            }
        
        df = df.sort_values(date_col).copy()
        current_value = df[value_col].iloc[-1]
        
        # Calculate percentage changes
        changes = {}
        
        # Daily change
        if len(df) >= 2:
            prev_value = df[value_col].iloc[-2]
            changes['daily_change'] = ((current_value - prev_value) / prev_value * 100) if prev_value != 0 else 0
        else:
            changes['daily_change'] = 0
        
        # Weekly change
        if len(df) >= 8:
            week_ago_value = df[value_col].iloc[-8]
            changes['weekly_change'] = ((current_value - week_ago_value) / week_ago_value * 100) if week_ago_value != 0 else 0
        else:
            changes['weekly_change'] = 0
        
        # Monthly change
        if len(df) >= 31:
            month_ago_value = df[value_col].iloc[-31]
            changes['monthly_change'] = ((current_value - month_ago_value) / month_ago_value * 100) if month_ago_value != 0 else 0
        else:
            changes['monthly_change'] = 0
        
        return {
            'current': current_value,
            **changes
        }

# Create a global instance for easy importing
kaspa_data = KaspaDataManager()

# Convenience functions for backward compatibility and easy access
def load_hashrate_data():
    """Convenience function for loading hashrate data"""
    return kaspa_data.load_hashrate_data()

def load_price_data():
    """Convenience function for loading price data"""
    return kaspa_data.load_price_data()

def load_volume_data():
    """Convenience function for loading volume data"""
    return kaspa_data.load_volume_data()

def load_marketcap_data():
    """Convenience function for loading market cap data"""
    return kaspa_data.load_marketcap_data()

def load_difficulty_data():
    """Convenience function for loading difficulty data"""
    return kaspa_data.load_difficulty_data()

def load_social_metrics_data():
    """Convenience function for loading social metrics data"""
    return kaspa_data.load_social_metrics_data()

def load_social_trends_data():
    """Convenience function for loading social trends data"""
    return kaspa_data.load_social_trends_data()

def fit_power_law(df, y_col='Hashrate_PH', x_col=None):
    """Convenience function for power law fitting"""
    return kaspa_data.fit_power_law(df, y_col, x_col)

def calculate_growth_metrics(df, value_col='Price', date_col='Date'):
    """Convenience function for growth metrics calculation"""
    return kaspa_data.calculate_growth_metrics(df, value_col, date_col)
