from index.abstract_index import AbstractIndex
from index.utils import Utils
from collections import Counter
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class NonPositionalIndex(AbstractIndex):
    def __init__(
            self,
            index={},
            urls=None,
            type='title',
            delete_stopwords=False
    ) -> None:
        super().__init__(
            index=index,
            urls=urls,
            type=type,
            delete_stopwords=delete_stopwords
        )
        

    def create_index(self):
        for doc_id, url in enumerate(self.urls):
            text = self.get_text_from_url(url=url)
            if text:
                self.visited_urls.append(url)
                self.nb_visited_urls += 1
                tokens = self.tokenize(text=text)
                tokens_count = Counter(tokens)
                index = self.get_index()
                for token in tokens_count:
                    if token not in index.keys():
                        index[token] = [
                            {'doc_id': doc_id, 'count': tokens_count[token]}]
                    else:
                        index[token].append(
                            {'doc_id': doc_id, 'count': tokens_count[token]})
            else:
                self.failed_urls.append(url)
                self.nb_failed_urls += 1

    def get_metadata(self):
        return super().get_metadata()


    def run(self, sort=True):
        self.create_index()
        index = self.get_index()
        if sort:
            index = dict(sorted(index.items()))
        
        print("\n------------------------------------------------------------------------------------")
        print("------------------------------- NON POSITIONAL INDEX -------------------------------")
        print("------------------------------------------------------------------------------------\n")
        print(self.get_statistics())
        print()
        print(self.get_metadata())
        metadata = self.export_metadata()
        utils = Utils()
        utils.write_index(index=index, is_positional=False, index_type=self.type)
        utils.write_metadata(metadata=metadata, is_positional=False, index_type=self.type)
