import logging
from relevancy.dcg import ndcg_at_k
from relevancy.esclient import EsClient

logging.basicConfig(level=logging.ERROR)


def calculate_relevancy(ground_truth, search_results):
    if not (ground_truth and search_results):
        logging.warn("Parameters are empty")
        return [(0.0, 0)]

    relevancy_map = {x: i + 1 for i, x in enumerate(reversed(ground_truth))}
    logging.debug("Found relevancy {}".format(relevancy_map))

    rel = [relevancy_map.get(result, 0) for result in search_results]
    logging.debug("Found relevancy {}".format(rel))

    starting_value = min(3, len(ground_truth))
    ranges = [starting_value] + [i for i in [3, 5, 10, 15, 25, 50, 100] if i > starting_value]
    scores = [(ndcg_at_k(rel, i), i) for i in ranges
              if i > starting_value]
    logging.debug("Found relevancy score {}".format(scores))
    return scores


import boto3
import io

client = boto3.client('s3')
resource = boto3.resource('s3')
queries_bucket = resource.Bucket('hired-etl')

import argparse

parser = argparse.ArgumentParser(description='Search relevancy calculation across ES environments')
parser.add_argument('--es1', metavar='N', type=str)
parser.add_argument('--es2', metavar='N', type=str)

args = parser.parse_args()

es_client1 = EsClient(args.es1,
                      index_name='hired_staging_candidate')
es_client2 = EsClient(args.es2,
                      index_name='hired_staging_candidate')

if __name__ == "__main__":
    queries = list(queries_bucket.objects.filter(Prefix='data_catalog/queries'))
    for query_content in queries:
        obj = client.get_object(Bucket='hired-etl', Key=query_content.key)
        query = io.BytesIO(obj['Body'].read()).read()
        result1 = es_client1.execute_query(query)
        result2 = es_client2.execute_query(query)
        relevancy = calculate_relevancy(result1, result2)

        discrepancies = [(relevancy_score, k) for relevancy_score, k in relevancy
                         if relevancy_score < 1 and k > 0]

        for relevancy_score, k in discrepancies:
            logging.error(
                "Failed for {0} for k {1} with score {2}".format(query_content.key, k,
                                                                 relevancy_score))

    score = sum([rs for rs,k in discrepancies]) / float(len(discrepancies))
    print(score)

