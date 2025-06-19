from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

def evaluate_bleu(prediction: str, reference: str) -> float:
    pred_tokens = prediction.split()
    ref_tokens = [reference.split()]
    return sentence_bleu(ref_tokens, pred_tokens)

def evaluate_rouge(prediction: str, reference: str) -> dict:
    rouge = Rouge()
    return rouge.get_scores(prediction, reference)[0]