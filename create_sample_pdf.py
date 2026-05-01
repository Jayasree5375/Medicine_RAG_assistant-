from reportlab.pdfgen import canvas

def create_sample_pdf(filename):
    c = canvas.Canvas(filename)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "MediCure - Drug Information Sheet")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, "Generic Name: CureAll")
    c.drawString(100, 700, "Indications: CureAll is used to treat mild to moderate headaches and fever.")
    c.drawString(100, 680, "Dosage: Take one tablet every 4-6 hours. Do not exceed 6 tablets in 24 hours.")
    c.drawString(100, 660, "Side Effects: May cause drowsiness, nausea, or dry mouth.")
    c.drawString(100, 640, "Warnings: Do not drive or operate heavy machinery while taking this medication.")
    c.drawString(100, 620, "Keep out of reach of children.")
    
    c.save()

if __name__ == "__main__":
    create_sample_pdf("sample_medicine.pdf")
