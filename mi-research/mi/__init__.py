"""
Modernization Index Research Platform

A quantitative diagnostic framework for measuring how complex
governance systems respond to structural stress.
"""

from mi.scoring import score_country, load_country_data
from mi.diagnostics import full_diagnostic, classify_strategy, generate_predictions
from mi.safeguards import evaluate_all_safeguards

__version__ = "1.0.0-live"
