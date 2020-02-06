#!user/bin/env python3 
# -*- coding: utf-8 -*- 
import xlrd,xlwt
import decimal
def get_excel_form(insert_data,applicant,claim_time):
	wbk = xlwt.Workbook()
	alignment, cost_alignment, right_blank_alignment, left_blank_alignment = xlwt.Alignment(), xlwt.Alignment(), xlwt.Alignment(), xlwt.Alignment()
	alignment.horz, cost_alignment.horz, right_blank_alignment.horz, left_blank_alignment.horz = xlwt.Alignment.HORZ_CENTER, xlwt.Alignment.HORZ_RIGHT, xlwt.Alignment.HORZ_RIGHT, xlwt.Alignment.HORZ_LEFT
	alignment.vert, cost_alignment.vert, right_blank_alignment.vert, left_blank_alignment.vert = xlwt.Alignment.VERT_CENTER, xlwt.Alignment.VERT_CENTER, xlwt.Alignment.VERT_CENTER, xlwt.Alignment.VERT_CENTER
	alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT
	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = 22
	borders = xlwt.Borders()
	borders.left, borders.right, borders.top, borders.bottom = xlwt.Borders.MEDIUM, xlwt.Borders.MEDIUM, xlwt.Borders.MEDIUM, xlwt.Borders.MEDIUM
	style_1, style_2, style_3,style_4, style_5 = xlwt.XFStyle(), xlwt.XFStyle(), xlwt.XFStyle(), xlwt.XFStyle(), xlwt.XFStyle()
	style_1.alignment, style_2.alignment, style_3.alignment, style_4.alignment, style_5.alignment = alignment, alignment, cost_alignment, right_blank_alignment, left_blank_alignment
	style_1.pattern, style_3.pattern = pattern, pattern
	style_1.borders, style_2.borders, style_3.borders, style_4.borders, style_5.borders = borders, borders, borders, borders, borders
	sheet = wbk.add_sheet("expense claim form(费用报销单)",cell_overwrite_ok=True)
	for i in range(54):
		change_col = sheet.col(i)
		change_col.width = 256*3
	### header part ###
	row_1, row_1_width, row_1_height = [u"受益成本中心\nBeneficial cost center", "Company 公司", "Region 地区部/代表处", "Department 部门"], [11,13,11,19], 2
	row_2, row_2_width, row_2_height = ["Name 名称", "深圳市普信天宇电子有限公司", "中国", "合肥"], [11,13,11,19], 1
	claim_title = claim_time[0] + "年费用报销单" if len(claim_time) == 1 else claim_time[0] + "年" + claim_time[1] + "月份费用报销单"
	row_3, row_3_width, row_3_height = ["Business Details 公务详情描述:", claim_title, u"Reimbursement Currency\n取款币种", "CNY"], [14,23,11,6], 2
	row_4, row_4_width, row_4_height = [u"Start/End Date\n起止日期\n(YY/MM/DD)", "Expense Description 费用描述", u"Expense Type\n费用类型", u"Receipt\nReference\n发票索引", u"Receipt\nCurrency\n发票币种", u"Receipt\nAmount\n发票金额", u"Exchange\nRate\n汇率", u"Converted\nAmount\n折算金额"], [7,14,7,5,5,6,4,6], 3
	def header_write(start_row, row, row_width, row_heigth):
		col_cursor = 0
		for i in range(0,len(row)):
			if "深圳" in row[i] or "中国" in row[i] or "合肥" in row[i] or "报销单" in row[i] or "CNY" in row[i]:
				sheet.write_merge(start_row,start_row+row_heigth-1,col_cursor,col_cursor+row_width[i]-1,row[i],style_2)
			else:
				sheet.write_merge(start_row,start_row+row_heigth-1,col_cursor,col_cursor+row_width[i]-1,row[i],style_1)
			col_cursor += row_width[i]
	header_write(0, row_1, row_1_width, row_1_height)
	header_write(2, row_2, row_2_width, row_2_height)
	header_write(3, row_3, row_3_width, row_3_height)
	header_write(5, row_4, row_4_width, row_4_height)
	### data part ###
	footer_row_index = 8
	expense_sum = 0.0
	for i in range(len(insert_data)):
		col_cursor = 0
		for j in range(8):
			if j == 5:
				sheet.write_merge(footer_row_index,footer_row_index,col_cursor,col_cursor+row_4_width[j]-1,str(decimal.Decimal("%.2f" % insert_data[i][j])),style_4)
			elif j == 6:
				sheet.write_merge(footer_row_index,footer_row_index,col_cursor,col_cursor+row_4_width[j]-1,str(decimal.Decimal("%.4f" % insert_data[i][j])),style_2)
			elif j == 7:
				expense_sum += insert_data[i][j]
				sheet.write_merge(footer_row_index,footer_row_index,col_cursor,col_cursor+row_4_width[j]-1,str(decimal.Decimal("%.2f" % insert_data[i][j])),style_2)
			else:
				sheet.write_merge(footer_row_index,footer_row_index,col_cursor,col_cursor+row_4_width[j]-1,insert_data[i][j],style_2)
			col_cursor += row_4_width[j]
		footer_row_index += 1
	expense_sum = str(decimal.Decimal("%.2f" % expense_sum))
	integer, Decimal = expense_sum.split(".")[0], expense_sum.split(".")[1]
	integer = integer.zfill(8)
	capital_cost = integer + Decimal
	integer_list = ["0","1","2","3","4","5","6","7","8","9"]
	capital_chinese = ["零","壹","贰","叁","肆","伍","陆","柒","捌","玖"]
	calcul_result = []
	for i in range(len(capital_cost)):
		calcul_result.append(capital_chinese[integer_list.index(capital_cost[i])])
	### footer part ###
	def footer_write(params,content,style):
		sheet.write_merge(params[0],params[1],params[2],params[3],content,style)
	params_list = [[footer_row_index,footer_row_index+2,0,10],[footer_row_index,footer_row_index,11,16],\
	[footer_row_index,footer_row_index,17,47],[footer_row_index,footer_row_index,48,53],\
	[footer_row_index+1,footer_row_index+2,11,16],[footer_row_index+1,footer_row_index+2,17,19],\
	[footer_row_index+1,footer_row_index+2,20,20]]
	temp = 21
	while temp <= 47:
		new_param = [footer_row_index+1, footer_row_index+2, temp, temp+1]
		params_list.append(new_param)
		temp += 2
		new_param = [footer_row_index+1, footer_row_index+2, temp, temp]
		params_list.append(new_param)
		temp += 1
	params_list.append([footer_row_index+1, footer_row_index+2, 48, 53])
	last_params_list = [[footer_row_index+3, footer_row_index+3, 0, 53],[footer_row_index+4, footer_row_index+4, 0, 53],\
	[footer_row_index+5, footer_row_index+6, 0, 53],[footer_row_index+7,footer_row_index+7,0,7],[footer_row_index+7,footer_row_index+7,8,14],\
	[footer_row_index+7,footer_row_index+7,15,20],[footer_row_index+7,footer_row_index+7,21,26],[footer_row_index+7,footer_row_index+8,27,27],\
	[footer_row_index+7,footer_row_index+7,28,53],[footer_row_index+8,footer_row_index+8,0,7],[footer_row_index+8,footer_row_index+8,8,26],\
	[footer_row_index+8,footer_row_index+8,28,34],[footer_row_index+8,footer_row_index+8,35,40],[footer_row_index+8,footer_row_index+8,41,41],\
	[footer_row_index+8,footer_row_index+8,42,46],[footer_row_index+8,footer_row_index+8,47,53],[footer_row_index+9,footer_row_index+9,0,53],\
	[footer_row_index+10,footer_row_index+10,0,53],[footer_row_index+11,footer_row_index+11,0,26],[footer_row_index+11,footer_row_index+11,27,53],\
	[footer_row_index+12,footer_row_index+12,0,5],[footer_row_index+12,footer_row_index+12,6,14],[footer_row_index+12,footer_row_index+12,15,15],\
	[footer_row_index+12,footer_row_index+12,16,19],[footer_row_index+12,footer_row_index+12,20,25],[footer_row_index+12,footer_row_index+12,26,26],\
	[footer_row_index+12,footer_row_index+12,27,32],[footer_row_index+12,footer_row_index+12,33,41],[footer_row_index+12,footer_row_index+12,42,42],\
	[footer_row_index+12,footer_row_index+12,43,46],[footer_row_index+12,footer_row_index+12,47,53],[footer_row_index+13,footer_row_index+13,0,26],\
	[footer_row_index+13,footer_row_index+13,27,53],[footer_row_index+14,footer_row_index+14,0,53],[footer_row_index+15,footer_row_index+16,0,53]]
	content_list = [u"Total Amount Claimed\n合    计","Say in Words","",expense_sum,"大写金额", calcul_result[0], "仟", calcul_result[1],\
	"佰", calcul_result[2], "拾", calcul_result[3], "万", calcul_result[4], "仟", calcul_result[5], "佰", calcul_result[6], "拾", calcul_result[7], "元" ,calcul_result[8], "角", calcul_result[9], "分", "", "", "",\
	"APPLICANT  申请人", "Name 姓名:", applicant, "Staff No. 工号:", "", "", "我保证上述费用是公务期间发生的合理且准确的费用。 1 guarantee",\
	"City 常驻工作地:", "合肥", "Signature 签名:", "", "", "Date 日期:" , "", "", "", "REVIEWED BY SUPERVISOR 领导审核", \
	"REVIEWED BY SUPERVISOR 领导审核","Signature 签名:", "", "", "Date 日期:" , "", "","Signature 签名:", "", "", "Date 日期:" , "", \
	"", "", "", "VERIFIED BY ACCOUNTANT 会计核定"]
	style_list = [style_1,style_1,style_2,style_2,style_1,style_3,style_1,style_3,style_1,style_3,style_1,\
	style_3,style_1,style_3,style_1,style_3,style_1,style_3,style_1,style_3,style_1,style_3,style_1,style_3,\
	style_1,style_2,style_2,style_2,style_1,style_4,style_2,style_2,style_2,style_2,style_5,style_4,style_2\
	,style_2,style_2,style_2,style_2,style_2,style_2,style_2,style_1,style_1,style_2,style_2,style_2,style_2,\
	style_2,style_2,style_2,style_2,style_2,style_2,style_2,style_2,style_2,style_2,style_1]
	for param in last_params_list:
		params_list.append(param)
	for i in range(len(params_list)):
		footer_write(params_list[i], content_list[i], style_list[i])
	wbk.save("expense_claim_form.xlsx")
