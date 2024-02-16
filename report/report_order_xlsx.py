# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from pytz import timezone, UTC
from datetime import datetime, timedelta

class ReportOrdersXlsx(models.AbstractModel):
    _name = 'report.fom.order_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, orders):
        for order_num, order in enumerate(orders, start=1):

            sheet = workbook.add_worksheet('Report Freezer Order')
            bold = workbook.add_format({'bold': True, 'align': 'center', 'color':'black', 'bg_color': '#B8B8B8'})
            title = workbook.add_format({'bold': True, 'align': 'center', 'color':'white', 'bg_color': '#000000', 'size': '17'})

            # Center formating
            currency_format = workbook.add_format({'num_format': '_-R$ * #,##0.00_-;[Red]-R$ * #,##0.00', 'align': 'center', 'color':'black', 'bg_color': '#F0F0F0'} )
            alignment = workbook.add_format({'bold': False, 'align': 'center', 'color':'black', 'bg_color': '#F0F0F0'})

            # Title
            sheet.merge_range(0, 0, 0, 5, 'Order Information', title)

            # Column names.
            headers = ['Product', 'Internal Code', 'Quantity', 'Unit Price', 'Tax', 'Total']
            for col_num, header in enumerate(headers):
                sheet.write(1, col_num, header, bold)

            # Loop for writing orders cells
            row_num = 2
            for line in order.order_line:
                sheet.write(row_num, 0, line.product_id.name,alignment)
                if not line.product_id.default_code == False : sheet.write(row_num, 1, line.product_id.default_code,alignment)
                if line.product_id.default_code == False : sheet.write(row_num, 1, 'No Code',alignment)
                sheet.write(row_num, 2, line.product_uom_qty,alignment)
                sheet.write(row_num, 3, line.price_unit,currency_format)
                sheet.write(row_num, 4, line.tax,currency_format)
                total = line.subtotal + line.tax
                sheet.write(row_num, 5, total,currency_format)

                # Width of the colum based on the value
                sheet.set_column(0, 0, len(str(line.product_id.name)) + 8)
                sheet.set_column(1, 1, len(str(line.product_id.default_code)) + 8)
                sheet.set_column(2, 2, len(str(line.product_uom_qty)) + 7)
                sheet.set_column(3, 3, len(str(line.price_unit)) + 7)
                sheet.set_column(4, 4, len(str(line.tax)) + 7)
                sheet.set_column(5, 5, len(str(line.subtotal)) + 7)

                # Adds coutner +1 to the for loop 
                row_num += 1

            # Line around the cells
            border_format=workbook.add_format({
                            'border':1,
                            'align':'left',
                            'font_size':10
                           })
            sheet.conditional_format( 'A1:F4' , { 'type' : 'no_blanks' , 'format' : border_format} )
       


            # ---------------------------- Second Table --------------------------------
            # Title
            title2 = workbook.add_format({'bold': True, 'align': 'center', 'color':'white', 'bg_color': '#000000', 'size': '17'})
            sheet.merge_range('H1:M1', 'Order Information', title2)

            # Column names.
            headers2 = ['Order ID', 'Order Type', 'Order Date', 'Market Type', 'Costumer', 'Status']
            for col_num, header in enumerate(headers2):
                sheet.write(1, 7 + col_num, header, bold)
            
            # Loop for writing orders cells
            row_num2 = 2
            for line in order:
                sheet.write(row_num2, 7, line.name, alignment)
                sheet.write(row_num2, 8, line.ordertype, alignment)

                db_timezone = timezone('America/Sao_Paulo')
                adjusted_date = line.dateorder.replace(tzinfo=UTC).astimezone(db_timezone)
                formatted_date = adjusted_date.strftime("%Y-%m-%d %H:%M:%S")

                # 
                dt_object = datetime.strptime(formatted_date, "%Y-%m-%d %H:%M:%S")
                dt_minus_one_hour = dt_object - timedelta(hours=1)
                formatted_result = dt_minus_one_hour.strftime("%Y-%m-%d %H:%M:%S")
                                
                
                sheet.write(row_num2, 9, formatted_result, alignment)
                sheet.write(row_num2, 10, line.markettype, alignment)
                sheet.write(row_num2, 11, line.customer_id.name if line.customer_id else '', alignment)

                # Name Frrom the state.
                state_display_name = dict(line._fields['state'].selection).get(line.state, '')
                sheet.write(row_num2, 12, state_display_name, alignment)  

                # Width of the column based on the value
                sheet.set_column(7, 7, len(str(line.name)) + 8)
                sheet.set_column(8, 8, len(str(line.ordertype)) + 10)
                sheet.set_column(9, 9, len(str(formatted_result)) + 6)
                sheet.set_column(10, 10, len(str(line.markettype)) + 10)
                sheet.set_column(11, 11, len(str(line.customer_id.name)) + 6)
                sheet.set_column(12, 12, len(str(line.state)) + 10)

                # Adds counter +1 to the for loop 
                row_num2 += 1
            
            # Line around the cells
            border_forma2=workbook.add_format({
                            'border':1,
                            'align':'left',
                            'font_size':10
                           })
            sheet.conditional_format( 'H1:M4' , { 'type' : 'no_blanks' , 'format' : border_forma2} )