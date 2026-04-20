# similarity_checker.py
# Real plagiarism detection using TF-IDF cosine similarity.
# Compares a new document against all previously submitted documents in the uploads folder.

import os
import re
import math


def _tokenize(text):
    """Lowercase, strip HTML tags, and extract word tokens."""
    text = re.sub(r'<[^>]+>', ' ', text)               # strip HTML
    text = text.lower()
    tokens = re.findall(r'\b[a-z]{3,}\b', text)        # only words ≥3 chars
    return tokens


def _term_frequency(tokens):
    """Build a term-frequency dict from a token list."""
    tf = {}
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1
    return tf


def _cosine_similarity(tf_a, tf_b):
    """Compute cosine similarity between two TF dicts."""
    common = set(tf_a.keys()) & set(tf_b.keys())
    if not common:
        return 0.0

    dot = sum(tf_a[t] * tf_b[t] for t in common)
    mag_a = math.sqrt(sum(v * v for v in tf_a.values()))
    mag_b = math.sqrt(sum(v * v for v in tf_b.values()))

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot / (mag_a * mag_b)


def compute_similarity(new_text, existing_texts):
    """
    Compare new_text against a list of existing document texts.

    Returns the highest similarity score found (0–100 integer, rounded).
    """
    if not new_text.strip() or not existing_texts:
        return 0

    new_tokens = _tokenize(new_text)
    if not new_tokens:
        return 0

    new_tf = _term_frequency(new_tokens)

    max_score = 0.0
    for existing_text in existing_texts:
        if not existing_text.strip():
            continue
        ex_tokens = _tokenize(existing_text)
        if not ex_tokens:
            continue
        ex_tf = _term_frequency(ex_tokens)
        score = _cosine_similarity(new_tf, ex_tf)
        if score > max_score:
            max_score = score

    return min(100, round(max_score * 100))
