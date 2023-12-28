mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"aleks.kapich@pbc.pl\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[theme]\n\
base = 'light'\n\
primaryColor = '#00AADB'\n\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml