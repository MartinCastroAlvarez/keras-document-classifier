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
python3 paris.py search --term "Coffee Shop New Orleans" --pages 2
python3 paris.py search --term "Coffee Shop" --pages 2
python3 paris.py search --term "Restaurant" --pages 2
python3 paris.py search --term "Italian Dinner" --pages 2
python3 paris.py search --term "Food Bad Hamburguer" --pages 2
python3 paris.py search --term "Indian Food Restaurant" --pages 2
python3 paris.py search --term "Mexican Food Bar" --pages 2
python3 paris.py search --term "Night Theatre" --pages 2
python3 paris.py search --term "History Tour New Orleans" --pages 2
python3 paris.py search --term "History Tour San Francisco" --pages 2
python3 paris.py search --term "History Tour Los Angeles" --pages 2
python3 paris.py search --term "New Orleans Organic Span" --pages 2
python3 paris.py search --term "Beer Bar California" --pages 2
python3 paris.py search --term "Night Bar California" --pages 2
python3 paris.py search --term "Night Out Las Vegas" --pages 2
python3 paris.py search --term "Cafe Las Vegas" --pages 2
python3 paris.py search --term "Lounge Bar California" --pages 2
python3 paris.py search --term "Rooftop Bar New York" --pages 2
python3 paris.py search --term "Wedding Cake House" --pages 2
python3 paris.py search --term "Donuts Los Angeles" --pages 2
python3 paris.py search --term "Pizza Bar New York" --pages 2
python3 paris.py search --term "Pizza Bar Los Angeles" --pages 2
python3 paris.py search --term "Donuts New York" --pages 2
python3 paris.py search --term "Tea Cafe" --pages 2
python3 paris.py search --term "Town Bar" --pages 2
python3 paris.py search --term "Night Concerts in New Orleans" --pages 2
python3 paris.py search --term "Night Concerts in San Francisco" --pages 2
python3 paris.py search --term "Night Concerts in Los Angeles" --pages 2
python3 paris.py search --term "Museum in New Orleans" --pages 1
python3 paris.py search --term "Museum in Los Angeles" --pages 1
python3 paris.py search --term "Museum in San Francisco" --pages 1
python3 paris.py search --term "Donuts San Francisco" --pages 2
```
Add negative search results to your dataset:
```bash
python3 paris.py search --term "Amazon Web Services" --pages 3 --is-negative
python3 paris.py search --term "Buy New Car Used" --pages 3 --is-negative
python3 paris.py search --term "Stack Overflow" --pages 3 --is-negative
python3 paris.py search --term "Java Tutorial Kubernetes" --pages 3 --is-negative
python3 paris.py search --term "Java Hadoop" --pages 3 --is-negative
python3 paris.py search --term "Docker Cassandra" --pages 3 --is-negative
```
Export the dataset:
```bash
python3 paris.py export --name "my-dataset-1.csv"
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
