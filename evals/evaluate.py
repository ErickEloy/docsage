#!/usr/bin/env python3
"""
Evaluation script for Docsage RAG system.
Measures accuracy, retrieval quality, and response time.
"""
import json
import time
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.llm import ask_question
from app.services.vector_store import reset_vector_store


def load_questions(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def evaluate_accuracy(questions, api_url='http://localhost:8000'):
    """Calculate accuracy based on keyword matching."""
    correct = 0
    total = len(questions)
    results = []

    for q in questions:
        try:
            start = time.time()
            answer, sources = ask_question(q['question'], top_k=5)
            elapsed = time.time() - start

            answer_lower = answer.lower()
            has_keywords = any(kw in answer_lower for kw in q['expected_keywords'])
            has_sources = len(sources) > 0

            is_correct = has_keywords and has_sources
            if is_correct:
                correct += 1

            results.append({
                'question': q['question'],
                'answer': answer[:200] + '...' if len(answer) > 200 else answer,
                'correct': is_correct,
                'has_keywords': has_keywords,
                'has_sources': has_sources,
                'response_time': elapsed,
                'num_sources': len(sources)
            })
        except Exception as e:
            results.append({
                'question': q['question'],
                'error': str(e),
                'correct': False
            })

    accuracy = correct / total if total > 0 else 0
    return accuracy, results


def print_report(accuracy, results):
    print("\n" + "="*80)
    print("DOCSAGE EVALUATION REPORT")
    print("="*80)
    print(f"\nOverall Accuracy: {accuracy*100:.1f}% ({sum(1 for r in results if r.get('correct'))}/{len(results)})")
    print("\nDetailed Results:")
    print("-"*80)

    for i, r in enumerate(results, 1):
        status = "✓" if r.get('correct') else "✗"
        print(f"\n{i}. [{status}] {r['question']}")
        if 'error' in r:
            print(f"   Error: {r['error']}")
        else:
            print(f"   Response time: {r['response_time']:.2f}s")
            print(f"   Sources found: {r['num_sources']}")
            print(f"   Answer preview: {r['answer'][:100]}...")


def main():
    questions_file = os.path.join(os.path.dirname(__file__), 'questions.json')
    questions = load_questions(questions_file)

    print(f"Running evaluation on {len(questions)} questions...")
    accuracy, results = evaluate_accuracy(questions)
    print_report(accuracy, results)

    # Save detailed results
    output_file = os.path.join(os.path.dirname(__file__), 'evaluation_results.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'accuracy': accuracy,
            'results': results
        }, f, indent=2, ensure_ascii=False)

    print(f"\nDetailed results saved to: {output_file}")


if __name__ == '__main__':
    main()