[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bathing-water.streamlit.app)
# Bathing water quality and lakes temperatures - Multi page streamlit app
## About project
App is made out of 3 pages:
* `Hello` - Welcome/About page
* `Temperatura Jezior Polska` - Daily temperatures of lakes in Poland for May - September 2023 (chart)
* `Bathing Water Quality EU` - Bathing water quality in EU for 1990 - 2022 (map, detailed info) 
## Built with
### Libraries

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.com)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white)](https://kaggle.com)
[![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Folium](https://img.shields.io/badge/folium-77B829?style=for-the-badge&logo=folium&logoColor=black)](https://python-visualization.github.io/folium/latest/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com/)

### Datasets

* [Bathing water quality for EU 1990 - 2022](https://www.kaggle.com/datasets/krzysztofkulasik/status-of-bathing-water-europe-union-2008-2022)
* [Daily temperatures of lakes in Poland for 2023](https://www.kaggle.com/datasets/krzysztofkulasik/daily-temperatures-of-lakes-poland)

## Getting Started
### Prerequisites
* Docker
### Installation

1. Clone repository
```shell
git clone https://github.com/kkulasik/bwq-lakes-streamlit-app.git
```

2. Build docker image
```shell
docker build -t bwq-ls-image .
```

3. Run container
```shell
docker run --name bwq-ls-container \
-p 80:80 -d \
-e KAGGLE_USERNAME=YOUR-KAGGLE-USERNAME \
-e KAGGLE_KEY=YOUR-KAGGLE-KEY \
bwq-ls-image
```

## Contact
[![Linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/kkulasik)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=Kaggle&logoColor=white)](https://www.kaggle.com/krzysztofkulasik)
