mkdir -p ~/.streamlit/
echo "[server]\nheadless = true\n\n[global]\ndevelopmentMode = false" > ~/.streamlit/config.toml
pip install plotly pymysql
