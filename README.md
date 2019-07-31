# France
Neural Network using Keras and Google Search API.

![image-alt](./france.jpg)

## References
- [Python3 Newspaper](https://pypi.org/project/newspaper3k/)
- [Google Search API](https://github.com/abenassi/Google-Search-API)
- [Python3 Begins](https://pypi.org/project/begins/)

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
python3 paris.py search --term "Amazon Web Services" --pages 3 --is-negative
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
