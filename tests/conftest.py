import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
for folder in ["oop", "design_patterns/creational", "design_patterns/structural", "design_patterns/behavioral"]:
    sys.path.insert(0, os.path.join(ROOT, folder))
