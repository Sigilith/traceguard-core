from traceguard.pdf_generator import generate_compliance_pdf

generate_compliance_pdf("example_report.pdf", {"status": "VERIFIED"})
print("PDF generated: example_report.pdf")
