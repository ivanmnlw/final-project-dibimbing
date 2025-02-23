# Financial Sentiment Analysis
Pada project ini dilakukan web scraping dari berita CNN dan New York Times untuk dianalisis sentiment untuk tiap berita

## Tools yang digunakan
- airflow
- docker
- python
- selenium
- huggingface
- spark
- bigquery
- tableau

## Architecture
Pada architecture pipeline ini dimulai dengan extract data webscraping -> transform -> load di bigquery -> visualisasi 

![Uploading airflow.png…]()

## Extract
Data di extract dari berita US. Untuk CNN menggunakan request dan beatifulsoup dan New York Times dengan selenium karena dynamic website.
Setelah di extract data akan dibersihkan dan dibuat dataframe (url, datetime, title, text, source) dan disimpan ke csv

## Transform 
Data dari hasil extract akan dibaca oleh spark dan dilakukannya transform untuk menghilangkan duplikasi data dan missing values
Setelah itu data dibuat kedalam bentuk dataframe pandas dan dilanjutkan sentiment analysis menggunakan hugging face
Sehingga didapatkan kolom baru berupa score dan label('POSTIVE' atau 'NEGATIVE')

## Load
![Uploading load_bigquery.png…]()
Data akan di load ke dalam bigquery
Di dalam bigquery data akan diquery lagi untuk kebutuhan visualisasi

## Visualization
![Uploading visualization.png…]()
Dari hasil visualisasi didapatkan kesimpulan bahwa sulit untuk memprediksi kenaikan harga SP500 dengan satu metric sentiment analysis.
Sentiment analysis ini hanya bersifat membantu untuk kebutuhan analisa saja
