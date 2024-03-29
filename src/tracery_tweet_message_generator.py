import json
import logging
import tracery
from tracery.modifiers import base_english


logger = logging.getLogger(__name__)


class TraceryTweetMessageGenerator:
    tracery_source_file = "tracery.json"

    def __init__(self):
        logger.info(f"opening {self.tracery_source_file}")
        with open(self.tracery_source_file) as f:
            tracery_rules = json.load(f)

            self.grammar = tracery.Grammar(tracery_rules)
            self.grammar.add_modifiers(base_english)

    def get_random_tweet(self) -> str:
        return self.grammar.flatten("#origin#")
