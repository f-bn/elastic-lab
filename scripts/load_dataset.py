import argparse
import json
import logging
from pathlib import Path

from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk


logger = logging.getLogger(__name__)

def get_file_basename(file: str):
    """Return the basename of a file path."""
    return Path(file).stem

def get_index_configuration(index_settings: dict):
    """Return settings and mappings from wrapped or bare mapping configuration."""
    if any(key in index_settings for key in ("settings", "mappings")):
        return index_settings.get("settings"), index_settings.get("mappings")
    return None, index_settings

def load_dataset(file: str, index: str):
    """Yield non-empty NDJSON lines as Elasticsearch bulk indexing actions."""
    with open(file, "r") as f:
        for line in f:
            if line.strip():
                yield {
                    "_index": index,
                    "_source": json.loads(line),
                }

def bulk_upload(file: str, index: str, index_settings: dict | None, chunk_size: int):
    """Create an index if needed and upload dataset documents in bulk."""
    client = Elasticsearch("http://localhost:9200")

    if not client.indices.exists(index=index):
        if index_settings is None:
            client.indices.create(index=index)
            logger.info("Index '%s' created", index)
        else:
            settings, mappings = get_index_configuration(index_settings)
            client.indices.create(
                index=index,
                settings=settings,
                mappings=mappings,
            )
            logger.info("Index '%s' created with specified configuration", index)
    else:
        logger.info("Index '%s' already exists; skipping index creation", index)

    logger.info("Indexing documents from '%s' into index '%s'", file, index)

    processed_docs: int = 0
    indexed_docs: int = 0
    failed_docs: int = 0

    for success, err in streaming_bulk(
        client=client,
        actions=load_dataset(file, index),
        chunk_size=chunk_size,
        raise_on_error=False
    ):
        processed_docs += 1
        if not success:
            failed_docs += 1
            logger.error("Failed to load document into index '%s': %s", index, err)
        else:
            indexed_docs += 1

    logger.info(
        "Indexing complete: %d processed, %d indexed, %d failed",
        processed_docs,
        indexed_docs,
        failed_docs,
    )


def main():
    parser = argparse.ArgumentParser(description="Load dataset data into an ElasticSearch index")
    parser.add_argument(
        "file",
        type=str,
        help="Path to dataset file"
    )
    parser.add_argument(
        "-i", "--index",
        dest="index_name",
        default=None,
        type=str,
        help="Name of the index"
    )
    parser.add_argument(
        "-s", "--settings-file",
        dest="settings_file",
        type=str,
        help="Path to index settings file (includes settings and/or mappings)",
    )
    parser.add_argument(
        "-c", "--chunk-size",
        dest="chunk_size",
        default=1000,
        type=int,
        help="Number of documents to send per bulk batch (default: 1000)"
    )
    args = parser.parse_args()

    logging.getLogger("elastic_transport").setLevel(logging.WARNING)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    if args.chunk_size <= 0:
        raise ValueError("--chunk-size flag must be a positive integer")

    index_name: str = args.index_name or get_file_basename(args.file)

    settings: dict | None = None
    if args.settings_file:
        with open(args.settings_file, "r") as f:
            settings = json.load(f)

    bulk_upload(
        file=args.file,
        index=index_name,
        index_settings=settings,
        chunk_size=args.chunk_size
    )

if __name__ == "__main__":
    main()
