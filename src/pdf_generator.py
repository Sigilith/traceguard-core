from fpdf import FPDF
import json

class EnterprisePDFExporter(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 10)
        self.set_text_color(88, 166, 255)
        self.cell(0, 10, 'TRACEGUARD-CORE // ENTERPRISE COMPLIANCE DIVISION', 0, 1, 'L')
        self.set_draw_color(48, 54, 61)
        self.line(10, 18, 200, 18)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(139, 148, 158)
        self.cell(0, 10, f'Page {self.page_no()} | Immutable Audit Record — Confidential', 0, 0, 'C')

def generate_compliance_pdf(packet: dict, filename: str = "compliance_audit_packet.pdf"):
    pdf = EnterprisePDFExporter()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title Section
    pdf.set_font('helvetica', 'B', 15)
    pdf.set_text_color(33, 33, 33)
    pdf.cell(0, 10, 'ENTERPRISE COMPLIANCE & ASSURANCE AUDIT PACKET', 0, 1, 'L')
    
    # Metadata Block
    pdf.set_font('helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    meta = packet['artifact_metadata']
    pdf.cell(0, 6, f"System Name: {meta['system_name']}", 0, 1, 'L')
    pdf.cell(0, 6, f"Audit UUID: {meta['audit_uuid']}", 0, 1, 'L')
    pdf.cell(0, 6, f"Timestamp (UTC): {meta['timestamp_utc']}", 0, 1, 'L')
    pdf.ln(4)
    
    # Section 1: Tier Classification
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(24, 100, 175)
    pdf.cell(0, 8, '1. Executive Tier Classification', 0, 1, 'L')
    
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(50, 50, 50)
    risk = packet['risk_classification']
    pdf.cell(0, 6, f"Assigned Tier: {risk['assigned_tier']}", 0, 1, 'L')
    pdf.cell(0, 6, f"Composite Risk Score: {risk['composite_score']} (Consequence: {risk['consequence_level']} | Autonomy: {risk['autonomy_level']} | Oversight: {risk['human_oversight_enforced']})", 0, 1, 'L')
    pdf.ln(4)
    
    # Section 2: Regulatory Alignment
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(24, 100, 175)
    pdf.cell(0, 8, '2. Regulatory Alignment', 0, 1, 'L')
    pdf.set_font('helvetica', '', 10)
    reg_str = ", ".join(packet['regulatory_mapping'])
    pdf.multi_cell(0, 6, f"Frameworks Mapped: {reg_str}")
    pdf.ln(4)
    
    # Section 3: Mandatory Governance Controls
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(24, 100, 175)
    pdf.cell(0, 8, '3. Mandatory Governance Controls', 0, 1, 'L')
    pdf.set_font('helvetica', '', 10)
    for control in packet['mandatory_controls']:
        pdf.cell(0, 6, f"[X] {control}", 0, 1, 'L')
    pdf.ln(4)
    
    # Section 4: Runtime Boundary Blueprint
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(24, 100, 175)
    pdf.cell(0, 8, '4. Runtime Boundary Blueprint', 0, 1, 'L')
    pdf.set_font('helvetica', '', 10)
    bp = packet['runtime_boundary_blueprint']
    pdf.cell(0, 6, f"TraceGuard Enforcement: {bp['traceguard_enforcement']}", 0, 1, 'L')
    pdf.cell(0, 6, f"AXIOMOS Drift Status: {bp['aximos_drift_status']}", 0, 1, 'L')
    pdf.multi_cell(0, 6, f"Permitted Action Schema: {json.dumps(bp['allowed_action_schema'])}")
    
    pdf.output(filename)
    return filename
