from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

text = "User John Doe (john@example.com) purchased item X."
results = analyzer.analyze(text=text, language="en")
anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
print(anonymized.text)  # "User <PERSON> (<EMAIL_ADDRESS>) purchased item X."