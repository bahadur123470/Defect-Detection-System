"""
Report generation module for defect detection results
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os


class ReportGenerator:
    """Generates PDF reports for defect detection results"""
    
    def __init__(self):
        self.report_dir = 'reports'
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate(self, results_data, image_path):
        """
        Generate PDF report from detection results
        
        Args:
            results_data: Dictionary containing detection results
            image_path: Path to processed image with annotations
            
        Returns:
            Path to generated PDF report
        """
        # Create PDF filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"defect_report_{timestamp}.pdf"
        pdf_path = os.path.join(self.report_dir, pdf_filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12
        )
        
        # Title
        title = Paragraph("Defect Detection Report", title_style)
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Report metadata
        metadata = [
            ['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Original Image:', results_data.get('original_filename', 'N/A')],
            ['Processed Image:', results_data.get('processed_filename', 'N/A')],
        ]
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(metadata_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Summary section
        summary_heading = Paragraph("Summary", heading_style)
        story.append(summary_heading)
        
        defect_count = results_data.get('defect_count', 0)
        summary_text = f"Total defects detected: <b>{defect_count}</b>"
        summary_para = Paragraph(summary_text, styles['Normal'])
        story.append(summary_para)
        story.append(Spacer(1, 0.2*inch))
        
        # Defect type breakdown
        detections = results_data.get('detections', [])
        if detections:
            defect_types = {}
            for det in detections:
                defect_type = det.get('type', 'Unknown')
                defect_types[defect_type] = defect_types.get(defect_type, 0) + 1
            
            type_heading = Paragraph("Defect Type Breakdown", heading_style)
            story.append(type_heading)
            
            type_data = [['Defect Type', 'Count']]
            for defect_type, count in defect_types.items():
                type_data.append([defect_type, str(count)])
            
            type_table = Table(type_data, colWidths=[4*inch, 2*inch])
            type_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            story.append(type_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Detailed detections
        if detections:
            details_heading = Paragraph("Detailed Detections", heading_style)
            story.append(details_heading)
            
            details_data = [['#', 'Type', 'Confidence', 'Location (x1, y1, x2, y2)']]
            for idx, det in enumerate(detections, 1):
                bbox = det.get('bbox', [0, 0, 0, 0])
                bbox_str = f"({bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]})"
                details_data.append([
                    str(idx),
                    det.get('type', 'Unknown'),
                    f"{det.get('confidence', 0):.2f}",
                    bbox_str
                ])
            
            details_table = Table(details_data, colWidths=[0.5*inch, 2*inch, 1.5*inch, 2.5*inch])
            details_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ]))
            story.append(details_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Add processed image if available
        if os.path.exists(image_path):
            try:
                img_heading = Paragraph("Annotated Image", heading_style)
                story.append(img_heading)
                
                # Add image (resize to fit page)
                img = Image(image_path, width=5*inch, height=5*inch)
                story.append(img)
            except Exception as e:
                print(f"Error adding image to report: {e}")
        
        # Build PDF
        doc.build(story)
        
        return pdf_path

