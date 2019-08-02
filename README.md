# France
Neural Network using Keras, Google Search API and AsyncIO.

![image-alt](./france.jpg)

## References
- [Python3 Newspaper](https://pypi.org/project/newspaper3k/)
- [Google Search API](https://github.com/abenassi/Google-Search-API)
- [Python3 Begins](https://pypi.org/project/begins/)
- [AioHttp](https://aiohttp.readthedocs.io/en/stable/)
- [Common mistakes using AsyncIO](https://xinhuang.github.io/posts/2017-07-31-common-mistakes-using-python3-asyncio.html)
- [AsyncIO Generators](https://github.com/python-trio/async_generator)
- [AsyncIO Event Loop](https://docs.python.org/3/library/asyncio-eventloop.html)

## Instructions

#### Setup
Install this repo:
```bash
git clone ssh://git@github.com/MartinCastroAlvarez/france
```
Install all the dependencies:
```bash
cd france
virtualenv -p python3 .env
source .env/bin/activate
pip install -r requirements.txt
```

#### Generating a Dataset
Search for sample pages in Google:
```bash
python3 paris.py search --term "Coffee Shop New Orleans" --limit 5
python3 paris.py search --term "Coffee Shop" --limit 5
python3 paris.py search --term "Restaurant" --limit 5
python3 paris.py search --term "Italian Dinner" --limit 5
python3 paris.py search --term "Food Bad Hamburguer" --limit 5
python3 paris.py search --term "Indian Food Restaurant" --limit 5
python3 paris.py search --term "Mexican Food Bar" --limit 5
python3 paris.py search --term "Night Theatre" --limit 5
python3 paris.py search --term "History Tour New Orleans" --limit 5
python3 paris.py search --term "History Tour San Francisco" --limit 5
python3 paris.py search --term "History Tour Los Angeles" --limit 5
python3 paris.py search --term "New Orleans Organic Span" --limit 5
python3 paris.py search --term "Beer Bar California" --limit 5
python3 paris.py search --term "Night Bar California" --limit 5
python3 paris.py search --term "Night Out Las Vegas" --limit 5
python3 paris.py search --term "Cafe Las Vegas" --limit 5
python3 paris.py search --term "Lounge Bar California" --limit 5
python3 paris.py search --term "Rooftop Bar New York" --limit 5
python3 paris.py search --term "Wedding Cake House" --limit 5
python3 paris.py search --term "Donuts Los Angeles" --limit 5
python3 paris.py search --term "Pizza Bar New York" --limit 5
python3 paris.py search --term "Pizza Bar Los Angeles" --limit 5
python3 paris.py search --term "Donuts New York" --limit 5
python3 paris.py search --term "Parks" --limit 5
python3 paris.py search --term "Tea Cafe" --limit 5
python3 paris.py search --term "Town Bar" --limit 5
python3 paris.py search --term "Night Concerts in New Orleans" --limit 5
python3 paris.py search --term "Night Concerts in San Francisco" --limit 5
python3 paris.py search --term "Night Concerts in Los Angeles" --limit 5
python3 paris.py search --term "Museum in New Orleans" --limit 5
python3 paris.py search --term "Museum in Los Angeles" --limit 5
python3 paris.py search --term "Museum in San Francisco" --limit 5
python3 paris.py search --term "Donuts San Francisco" --limit 5
python3 paris.py search --term "Donuts Los Angeles" --limit 5
python3 paris.py search --term "Parks in San Francisco" --limit 5
python3 paris.py search --term "Parks in New Orleans" --limit 5
```
Add negative search results to your dataset:
```bash
python3 paris.py search --term "Amazon Web Services" --limit 50 --is-negative
python3 paris.py search --term "Buy New Car Used" --limit 50 --is-negative
python3 paris.py search --term "Stack Overflow" --limit 50 --is-negative
python3 paris.py search --term "Java Tutorial Kubernetes" --limit 50 --is-negative
python3 paris.py search --term "Java Hadoop" --limit 50 --is-negative
python3 paris.py search --term "Docker Cassandra" --limit 50 --is-negative
python3 paris.py search --term "BBC News" --limit 50 --is-negative
python3 paris.py search --term "Clarin Economia" --limit 50 --is-negative
python3 paris.py search --term "Que es el cambio climatico" --limit 50 --is-negative
python3 paris.py search --term "Global Warming" --limit 50 --is-negative
python3 paris.py search --term "Black Hole" --limit 50 --is-negative
python3 paris.py search --term "NASA News" --limit 50 --is-negative
python3 paris.py search --term "China Technology" --limit 50 --is-negative
python3 paris.py search --term "Venezuela News" --limit 50 --is-negative
python3 paris.py search --term "Financial Consulting" --limit 50 --is-negative
python3 paris.py search --term "Insurance" --limit 50 --is-negative
python3 paris.py search --term "Hospital" --limit 50 --is-negative
python3 paris.py search --term "Top 10" --limit 50 --is-negative
python3 paris.py search --term "Top 5" --limit 50 --is-negative
python3 paris.py search --term "Best 10 Places" --limit 50 --is-negative
python3 paris.py search --term "Best 10 Beer" --limit 50 --is-negative
python3 paris.py search --term "Best 5 Beer" --limit 50 --is-negative
```
You may also run some combinatorics:
```bash
CITIES=("Los Angeles" "Las Vegas" "San Francisco" "New Orleans" "New York"
        "Boston" "Phoenix" "Chicago" "Houston" "Philadelfia" "San Antonio"
        "San Diego" "Dallas" "Austin" "Seattle" "Detroit" "Miami" "Orlando")
PLACES=("Restaurant" "Bar" "Lounge" "Donuts" "Coffee" "Cafe" "Museum" "Park" "BBQ"
        "Theatre" "Disco" "Club" "Square" "Neighborhood" "Pizza" "Italian Food"
        "Mexican Food" "Indian Food" "Sushi" "Taqueria" "Beer" "Brewery")
for CITY in "${CITIES[@]}"
do
    for PLACE in "${PLACES[@]}"
    do
        SEARCH="${PLACE} in ${CITY} -best -list"
        python3 paris.py search --term "${SEARCH}" --limit 5
    done
done
```
Export the dataset:
```bash
python3 paris.py export --name "my-dataset-1.csv"
```

#### Persisting the Dataset.
Optionally, you can upload the dataset to S3.
First create a new S3 Bucket:
```bash
aws s3api --profile "martin" create-bucket \
    --bucket "datasets.martincastroalvarez.com" --region "us-east-1"
```
Then, upload the dataset to the S3 Bucket:
```bash
aws s3 --profile "martin" cp "./datasets/my-dataset-1.csv" \
    "s3://datasets.martincastroalvarez.com/my-dataset-1.csv"
```
Finally, generate a pre-signed public URL that expires automatically:
```bash
aws s3 --profile "martin" presign --expires-in 10000 \
    "s3://datasets.martincastroalvarez.com/my-dataset-1.csv"
```

#### Training a Prediction Model
Generate a prediction model using Neural Networks:
```bash
python3 paris.py learn --dataset "my-dataset-1.csv"
```

#### Making Predictions
Make a prediction:
```bash
python3 paris.py predict --urls "https://www.iacovonekitchen.com/"
```
