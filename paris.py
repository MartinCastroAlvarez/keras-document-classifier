"""
This script is responsible for generating a dataset.
"""

import os
import csv
import uuid
import json
import begin
import typing
import logging

import asyncio
import aiohttp
from async_generator import async_generator, yield_

from google.modules.standard_search import GoogleResult
from google import google
from slugify import slugify
from newspaper import Article

logger = logging.getLogger(__name__)


def to_string(x: typing.Any) -> str:
    """
    Utility to cast to string.
    """
    if isinstance(x, list):
        return json.dumps([
            to_string(y)
            for y in x
        ])
    if isinstance(x, dict):
        return json.dumps({
            y: to_string(z)
            for y, z in x.items()
        })
    return x.replace("\n", " ").replace("\r", "").encode("utf-8", "ignore").decode("utf-8")


class Path:
    """
    App paths.
    """
    ROOT = os.path.dirname(os.path.realpath(__file__))
    SEARCH = os.path.join(ROOT, "search")
    MODELS = os.path.join(ROOT, "models")
    DATASETS = os.path.join(ROOT, "datasets")
    PREDICTIONS = os.path.join(ROOT, "predictions")


class SearchResult:
    """
    Search result entity.
    """

    TITLE = "title"
    DESCRIPTION = "description"
    URL = "url"
    SLUG = "slug"
    HTML = "html"
    IS_NEGATIVE = "negative"

    IMAGE = "images"
    MOVIES = "movies"
    TEXT = "text"
    AUTHORS = "authors"
    DATE = "date"
    SUMMARY = "summary"
    KEYWORDS = "keywords"

    def __init__(self, data: GoogleResult, is_negative: bool = False) -> None:
        """
        Result constructor.
        """
        logger.debug("Constructing Result. | sf_data=%s", data)
        self.__data: GoogleResult = data
        self.is_negative = is_negative
        self.__article: typing.Optional[Article] = ""

    def __str__(self) -> str:
        """
        String serializer.
        """
        return "<Result: '{}'>".format(self.url)

    def to_json(self) -> str:
        """
        JSON serializer.
        """
        return {
            self.HTML: self.article.html,
            self.IMAGE: self.article.top_image,
            self.MOVIES: self.article.movies,
            self.TEXT: self.article.text,
            self.DATE: str(self.article.publish_date),
            self.AUTHORS: self.article.authors,
            self.SUMMARY: self.article.summary,
            self.KEYWORDS: self.article.keywords,
            self.TITLE: self.title,
            self.DESCRIPTION: self.description,
            self.URL: self.url,
            self.SLUG: self.slug,
            self.IS_NEGATIVE: self.is_negative,
        }

    @property
    def title(self) -> str:
        """
        Title getter.
        """
        return self.__data.name

    @property
    def description(self) -> str:
        """
        Description getter.
        """
        return self.__data.description

    @property
    def url(self) -> str:
        """
        URL getter.
        """
        return self.__data.link

    @property
    def slug(self) -> str:
        """
        Slugified name getter.
        """
        return slugify(self.url).replace("/", "-").replace(".", "-")

    @property
    def path(self) -> str:
        """
        Path getter.
        """
        return os.path.join(Path.SEARCH, "{}.json".format(self.slug))

    @property
    def article(self) -> Article:
        """
        Article getter.
        """
        return self.__article

    async def download(self) -> None:
        """
        Public method to download site.
        """
        logger.debug("Loading URL. | sf_url=%s", self.url)
        if self.__is_cached():
            logger.debug("Loading URL from Cache. | sf_url=%s", self.url)
            text = self.__load_from_cache()
        else:
            logger.debug("Loading URL from the Web. | sf_url=%s", self.url)
            text = await self.__download()
        self.__parse_text(text)
        self.__save_to_cache()

    def __parse_text(self, text: str) -> None:
        """
        Private method to analyze text using Newspaper3K.
        """
        logger.debug("Analyzing Text. | sf_text=%s", len(text))
        self.__article = Article(self.url)
        self.__article.set_html(text)
        logger.debug("Parsing URL. | sf_url=%s", self.url)
        self.__article.parse()
        logger.debug("Running NLP. | sf_url=%s", self.url)
        self.__article.nlp()
        logger.debug("Loaded URL. | sf_url=%s", self.url)
        logger.debug("Text Analyzed. | sf_text=%s", len(text))

    async def __download(self) -> str:
        """
        Private async method to download from the web.
        """
        logger.info("Downloading | sf_url=%s", self.url)
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                logger.debug("Downloaded. | sf_response=%s", response)
                return await response.text()

    def __load_from_cache(self) -> str:
        """
        Private method to load article from string.
        """
        logger.debug("Loading Cache | sf_url=%s", self.url)
        with open(self.path, "r") as file_buffer:
            return file_buffer.read().replace("\n", " ").strip()

    def __is_cached(self) -> bool:
        """
        Private method to evaluate if file is cached.
        """
        return os.path.isfile(self.path)

    def __save_to_cache(self) -> None:
        """
        Private method to save URL to file.
        """
        logger.debug("Saving Result. | sf_result=%s", self)
        with open(self.path, "w") as file_buffer:
            json.dump(self.to_json(), file_buffer)
        logger.debug("Saved Result. | sf_result=%s", self)



class Google:
    """
    Google entity.
    """

    def __str__(self) -> str:
        """
        String serializer.
        """
        return "<Google>"

    @async_generator
    async def search(self, term: str, is_negative: bool,
                     limit: int = 10) -> typing.Generator[SearchResult, None, None]:
        """
        Public method to send a search request.
        """
        logger.debug("Google search | sf_term=%s")
        total_results = 0
        page = 0
        while True:
            logger.debug("New Page | sf_page=%s", page)
            results = google.search(term, page)
            for result in results:
                logger.debug("New Result | sf_result=%s", total_results)
                total_results += 1
                if total_results > limit:
                    logger.debug("No More Results | sf_result=%s", total_results)
                    break
                logger.debug("Search result | sf_result=result")
                r = SearchResult(result, is_negative=is_negative)
                if r.url:
                    try:
                        await r.download()
                        await yield_(r)
                    except asyncio.TimeoutError:
                        logger.exception("URL failed. | sf_url=%s", self.url)
            if total_results > limit:
                logger.debug("No More Results | sf_page=%s", page)
                break
            logger.debug("End of Page | sf_page=%s", page)
            page += 1
        logger.debug("End of Google search | sf_term=%s", term)


class Dataset:
    """
    Dataset entity.
    """

    REJECTED = "REJECTED"
    ID = {
        SearchResult.URL,
        SearchResult.SLUG,
    }
    INPUTS = {
        SearchResult.HTML,
    }
    OUTPUTS = {
        SearchResult.TITLE,
        SearchResult.DESCRIPTION,
        SearchResult.IMAGE,
        SearchResult.MOVIES,
        SearchResult.TEXT,
        SearchResult.AUTHORS,
        SearchResult.DATE,
        SearchResult.SUMMARY,
        SearchResult.KEYWORDS,
    }
    COLUMNS = list(ID | INPUTS | OUTPUTS)

    def __init__(self, name: str = "") -> None:
        """
        Dataset constructor.
        """
        logger.debug("Constructing Dataset | sf_name=%s", name)
        self.__name = name or uuid.uuid4().hex

    def __str__(self) -> str:
        """
        String serializer.
        """
        return "<Dataset: '{}'>".format(self.path)

    @property
    def name(self) -> str:
        """
        Name getter.
        """
        return self.__name

    @property
    def path(self) -> str:
        """
        Path getter.
        """
        return os.path.join(Path.DATASETS,
                            self.name if self.name.endswith(".csv") \
                            else "{}.csv".format(self.name))

    @property
    def lines(self) -> int:
        """
        File lines getter.
        """
        with open(self.path) as file_buffer:
            for i, _ in enumerate(file_buffer):
                pass
        return i

    @property
    def rows(self) -> typing.Generator[dict, None, None]:
        """
        Dataset rows getter.
        """
        logger.debug("Reading Rows. | sf_dataset=%s", self)
        for row_name in os.listdir(Path.SEARCH):
            if row_name.endswith(".json"):
                logger.debug("Found result. | sf_name=%s", row_name)
                file_name = os.path.join(Path.SEARCH, row_name)
                with open(file_name, "r") as file_buffer:
                    try:
                        row = DatasetRow(json.load(file_buffer))
                    except json.decoder.JSONDecodeError:
                        raise RuntimeError("Can't open JSON file:", file_name)
                    if row.is_valid():
                        yield row.to_json()
        logger.debug("All Rows read. | sf_dataset=%s", self)

    def save(self) -> None:
        """
        Public method to save Dataset.
        """
        logger.debug("Saving Dataset. | sf_dataset=%s", self)
        with open(self.path, "w") as file_buffer:
            writer = csv.DictWriter(file_buffer, fieldnames=self.COLUMNS)
            writer.writeheader()
            for i, row in enumerate(self.rows):
                logger.debug("Saving Row | sf_row=%s", row)
                if not i % 50:
                    logger.info("Dataset is being generated | sf_rows=%s", i)
                writer.writerow(row)
        logger.debug("Saved Dataset. | sf_dataset=%s", self)


class DatasetRow:
    """
    Dataset row entity.
    """

    REQUIRED = {
        SearchResult.TITLE,
        SearchResult.DESCRIPTION,
        SearchResult.TEXT,
        SearchResult.SUMMARY,
        SearchResult.KEYWORDS,
    }

    def __init__(self, data: dict) -> None:
        """
        Dataset row constructor.
        """
        logger.debug("Constructing row. | sf_data=%s", data)
        self.__data = data

    def __str__(self) -> str:
        """
        String serializer.
        """
        return "<Row: '{}'>".format(self.__data)

    def is_valid(self) -> bool:
        """
        Public method that evaluates if a row is valid.
        """
        return not self.empty & self.REQUIRED

    @property
    def empty(self) -> set:
        """
        Returns a set of empty values.
        """
        return {
            c
            for c in Dataset.COLUMNS
            if not self.__data[c]
       }

    def is_negative(self) -> bool:
        """
        Public method that evaluates if a row is positive or negative.
        """
        return bool(self.__data.get(SearchResult.IS_NEGATIVE))

    def to_json(self) -> dict:
        """
        JSON serialier.
        """
        if self.is_negative():
            return self.__to_json_negative()
        return self.__to_json_positive()

    def __to_json_positive(self) -> dict:
        """
        Private positive JSON serialier.
        """
        return {
            k: to_string(v)
            for k, v in self.__data.items()
            if k in Dataset.COLUMNS
        }

    def __to_json_negative(self) -> dict:
        """
        Private negative JSON serialier.
        """
        return {
            k: Dataset.REJECTED if self.is_negative() \
                and k in Dataset.OUTPUTS else v
            for k, v in self.__to_json_positive().items()
        }


class Main:
    """
    Main handler.
    """

    @staticmethod
    async def search(term="", limit=10, is_negative=False):
        """
        Search for interesting pages asynchronously.
        """
        logger.info("Searching | sf_term=%s | sf_limit=%s", term, limit)
        g = Google()
        async for r in g.search(term=term, limit=int(limit), is_negative=is_negative):
            logger.info("URL saved. | sf_path=%s", r.path)
        logger.info("Search finished.")

    @staticmethod
    def export(name=""):
        """
        Export a dataset.
        """
        logger.info("Exporting dataset.")
        d = Dataset(name)
        d.save()
        logger.info("Dataset saved. | sf_path=%s | sf_lines=%s", d.path, d.lines)

    @staticmethod
    def predict(name="", *url):
        """
        Make a prediction.
        """
        logger.info("Predicting | sf_model=%s | sf_urls=%s", name, urls)
        m = Model()
        m.load(name)
        m.predict(*urls)
        m.predictions.save()
        logger.info("Predictions generated. | sf_path=%s", m.predictions.path)

    @staticmethod
    def learn(split_ratio_test=0.2,
              split_ratio_validation=0.1,
              loss_function="categorical_crossentropy",
              optimizer_function="adam",
              accuracy_metric="accuracy",
              epochs=5,
              batch_size=300):
        """
        Learn from dataset.
        """
        logger.info("Learning | sf_dataset=%s", dataset)
        n = NeuralNetwork()
        n.learn(split_ratio_test=float(split_ratio_test),
                split_ratio_validation=float(split_ratio_validation),
                loss_function=loss_function,
                optimizer_function=optimizer_function,
                accuracy_metric=accuracy,
                epochs=int(epochs),
                batch_size=int(batch_size))
        n.model.save()
        logger.info("Model generated. | sf_path=%s", m.model.path)


@begin.subcommand
@begin.logging
def search(term="", limit=10, is_negative=False):
    """
    CLI Alias: Search for keyword.
    """
    loop = asyncio.get_event_loop()
    s = Main.search(term, limit, is_negative)
    loop.run_until_complete(s)


@begin.subcommand
@begin.logging
def export(name=""):
    """
    CLI Alias: Export a dataset.
    """
    Main.export(name=name)


@begin.subcommand
@begin.logging
def learn(split_ratio_test=0.2,
          split_ratio_validation=0.1,
          loss_function="categorical_crossentropy",
          optimizer_function="adam",
          accuracy_metric="accuracy",
          epochs=5,
          batch_size=300):
    """
    CLI Alias: Learn from dataset.
    """
    Main.learn(split_ratio_test=float(split_ratio_test),
               split_ratio_validation=float(split_ratio_validation),
               loss_function=loss_function,
               optimizer_function=optimizer_function,
               accuracy_metric=accuracy,
               epochs=int(epochs),
               batch_size=int(batch_size))


@begin.subcommand
@begin.logging
def predict(name="", *urls):
    """
    CLI Alias: Make a prediction.
    """
    Main.predict(name, *urls)


@begin.start(lexical_order=True, short_args=True)
@begin.logging
def run():
    """
    Main task.
    This method will be called by executing this script from the CLI.
    """
