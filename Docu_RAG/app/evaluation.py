from typing import List, Dict
from rouge_score import rouge_scorer
import sacrebleu
import numpy as np

def bleu_score(refs: List[str], hyps: List[str]) -> float:
    return sacrebleu.corpus_bleu(hyps, [refs]).score

def rouge_l(refs: List[str], hyps: List[str]) -> float:
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = [scorer.score(r, h)['rougeL'].fmeasure for r, h in zip(refs, hyps)]
    return float(np.mean(scores))

def recall_at_k(ground_truth_ids: List[str], ranked_ids: List[str], k: int = 5) -> float:
    topk = set(ranked_ids[:k])
    return 1.0 if any(g in topk for g in ground_truth_ids) else 0.0
