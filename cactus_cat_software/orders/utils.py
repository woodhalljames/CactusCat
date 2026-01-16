"""Utility functions for orders app."""

from io import BytesIO

from django.conf import settings


def generate_order_receipt_pdf(order):
    """Generate a PDF receipt for an order.

    Args:
        order: Order instance

    Returns:
        BytesIO: PDF file buffer
    """
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    except ImportError:
        # Fallback to simple text receipt if reportlab not installed
        return generate_simple_text_receipt(order)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#83A384'),
        spaceAfter=30,
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#83A384'),
        spaceAfter=12,
    )

    # Title
    story.append(Paragraph("Cactus Cat Software", title_style))
    story.append(Paragraph("Order Receipt", styles['Heading2']))
    story.append(Spacer(1, 0.3 * inch))

    # Order Information
    story.append(Paragraph("Order Information", heading_style))
    order_data = [
        ["Order Number:", order.order_number],
        ["Order Date:", order.created.strftime("%B %d, %Y")],
        ["Status:", order.get_status_display()],
    ]
    order_table = Table(order_data, colWidths=[2 * inch, 4 * inch])
    order_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(order_table)
    story.append(Spacer(1, 0.3 * inch))

    # Customer Information
    story.append(Paragraph("Customer Information", heading_style))
    customer_data = [
        ["Name:", order.customer_name],
        ["Email:", order.customer_email],
        ["Phone:", order.customer_phone or "N/A"],
        ["Company:", order.company_name or "N/A"],
    ]
    customer_table = Table(customer_data, colWidths=[2 * inch, 4 * inch])
    customer_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(customer_table)
    story.append(Spacer(1, 0.3 * inch))

    # Order Items
    story.append(Paragraph("Order Items", heading_style))

    # Check if order has items (cart-based order) or single service
    if order.items.exists():
        items_data = [["Service", "Quantity", "Price", "Total"]]
        for item in order.items.all():
            items_data.append([
                item.service_package.name,
                str(item.quantity),
                f"${item.price}",
                f"${item.get_total_price()}"
            ])
    else:
        # Legacy single-item order
        items_data = [["Service", "Quantity", "Price", "Total"]]
        items_data.append([
            order.service_package.name if order.service_package else "N/A",
            "1",
            f"${order.total_amount}",
            f"${order.total_amount}"
        ])

    items_table = Table(items_data, colWidths=[3 * inch, 1 * inch, 1.2 * inch, 1.2 * inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#83A384')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.2 * inch))

    # Total
    total_data = [["Total Amount:", f"${order.total_amount}"]]
    total_table = Table(total_data, colWidths=[4.2 * inch, 1.2 * inch])
    total_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#83A384')),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#83A384')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(total_table)

    # Custom Requirements
    if order.custom_requirements:
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("Special Requirements", heading_style))
        story.append(Paragraph(order.custom_requirements, styles['Normal']))

    # Footer
    story.append(Spacer(1, 0.5 * inch))
    footer_text = """
    <para align=center>
    <font size=9 color="#83A384">
    Thank you for choosing Cactus Cat Software!<br/>
    For questions or support, contact us at hello@cactuscatsoftware.com
    </font>
    </para>
    """
    story.append(Paragraph(footer_text, styles['Normal']))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_simple_text_receipt(order):
    """Generate a simple text receipt if PDF library not available."""
    buffer = BytesIO()

    text = f"""
    CACTUS CAT SOFTWARE
    Order Receipt

    Order Number: {order.order_number}
    Order Date: {order.created.strftime("%B %d, %Y")}
    Status: {order.get_status_display()}

    Customer Information:
    Name: {order.customer_name}
    Email: {order.customer_email}
    Phone: {order.customer_phone or "N/A"}
    Company: {order.company_name or "N/A"}

    Order Items:
    """

    if order.items.exists():
        for item in order.items.all():
            text += f"\n- {item.quantity}x {item.service_package.name} - ${item.get_total_price()}"
    else:
        text += f"\n- 1x {order.service_package.name if order.service_package else 'N/A'} - ${order.total_amount}"

    text += f"\n\nTotal: ${order.total_amount}"

    if order.custom_requirements:
        text += f"\n\nSpecial Requirements:\n{order.custom_requirements}"

    text += "\n\nThank you for choosing Cactus Cat Software!"
    text += "\nFor questions or support, contact us at hello@cactuscatsoftware.com"

    buffer.write(text.encode('utf-8'))
    buffer.seek(0)
    return buffer
