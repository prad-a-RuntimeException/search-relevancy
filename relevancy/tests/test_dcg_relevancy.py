from relevancy.dcg import dcg_at_k, ndcg_at_k
import logging

logging.basicConfig(level=logging.INFO)


def test_calculating_dcg():
    ground_truth = [4, 3, 2, 1, 0]
    case1 = [3, 4, 2, 1, 0]
    case2 = [3, 2, 4, 1, 0]
    case3 = [0, 1, 2, 3, 4]
    dcg_score_ideal = dcg_at_k(ground_truth, 5)
    dcg_score_good = dcg_at_k(case1, 5)
    dcg_score_avg = dcg_at_k(case2, 5)
    dcg_score_bad = dcg_at_k(case3, 5)

    assert [dcg_score_ideal, dcg_score_good, dcg_score_avg, dcg_score_bad] == \
           sorted([dcg_score_avg, dcg_score_ideal, dcg_score_good, dcg_score_bad], reverse=True)


def test_calculating_ndcg():
    ground_truth = [4, 3, 2, 1, 0]
    dcg_score_ideal = ndcg_at_k(ground_truth, 5)
    assert dcg_score_ideal == 1.0


def test_calculating_ndcg_non_ideal_case():
    case1 = [4, 3, 2, 0, 1]
    case2 = [4, 2, 3, 0, 1]
    case3 = [0, 1, 2, 3, 4]
    dcg_score_1 = ndcg_at_k(case1, 5)
    dcg_score_2 = ndcg_at_k(case2, 5)
    dcg_score_3 = ndcg_at_k(case3, 5)
    assert [dcg_score_1, dcg_score_2, dcg_score_3] == sorted(
        [dcg_score_2, dcg_score_1, dcg_score_3], reverse=True)


def test_calculating_ndcg_test_index():
    case1 = [4, 3, 2, 0, 1]
    dcg_score_1 = ndcg_at_k(case1, 3)
    dcg_score_2 = ndcg_at_k(case1, 4)
    dcg_score_3 = ndcg_at_k(case1, 5)
    assert [dcg_score_1, dcg_score_3, dcg_score_2] == sorted(
        [dcg_score_2, dcg_score_1, dcg_score_3], reverse=True)

def test_calculating_ndcg_extra_k():
    case1 = [4, 3, 2, 0]
    dcg_score_1 = ndcg_at_k(case1, 5)
    print(dcg_score_1)
