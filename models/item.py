import re
import requests
import uuid
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import Dict
from models.model import Model


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile(r"(\d+[,|.]\d*)")
        price_str = pattern.search(string_price).group(1)
        if pattern.search(string_price).group(1).find(','):
            price_str = price_str.replace(",", ".")
        self.price = float(price_str)
        return self.price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query
        }
