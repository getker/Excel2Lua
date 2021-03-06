#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Author: Kerven

# import xlrd
import xlrd2 as xlrd
import os.path
import time
import os
import sys
import codecs

SCRIPT_HEAD = "-- This file is generated by program!\n\
-- Don't change it manaully.\n\
-- Author: hankangwen@qq.com  Kerven\n\
-- Source file: %s\n\
-- Created at: %s\n\
\n\
\n\
"

"--properties\n\
-- ID:string // 主键值\n\ "

def make_table(filename):
	if not os.path.isfile(filename):
		sys.exit("%s is	not	a valid	filename" % filename)
	book_xlrd = xlrd.open_workbook(filename)

	excel = {}
	excel["filename"] = filename
	excel["data"] = {}
	excel["meta"] = {}
	for sheet in book_xlrd.sheets():
		sheet_name = sheet.name.replace(" ", "_")
		if not sheet_name.startswith("OUT_"):
			continue
		sheet_name = sheet_name[4:]
		print(sheet_name + " sheet")
		excel["data"][sheet_name] = {}
		excel["meta"][sheet_name] = {}

		# 必须大于3行 一行描述，一行键值，一行类型
		if sheet.nrows <= 3:
			return {}, -1, "sheet[" + sheet_name + "]" + " rows must > 3"

		desc = {}		# 解析注释（第一行）
		title = {}		# 解析标题（第二行）
		type_dict = {} 	# 解析类型（第三行）
		col_idx = 0
		for col_idx in range(sheet.ncols):
			#第一行注释
			value = sheet.cell_value(0, col_idx)
			vtype = sheet.cell_type(0, col_idx)
			desc[col_idx] = str(value).replace("\n", " ")
			#第二行键值，亦即标题
			value = sheet.cell_value(1, col_idx)
			vtype = sheet.cell_type(1, col_idx)
			#主键值必须时int或者string型
			if (len(str(value)) == 0): continue;
			else:
				if vtype != 1: return {}, -1, "sheet[" + sheet_name + "]" + "title columns[" + str(col_idx + 1) + "] must be string"
			title[col_idx] = str(value).replace(" ", "_")
			
			#第三行类型，int，string等
			value = sheet.cell_value(2, col_idx)
			vtype = sheet.cell_type(2, col_idx)
			type_dict[col_idx] = str(value)
			if (type_dict[col_idx].lower() != "none" \
				and type_dict[col_idx].lower() != "int" \
				and type_dict[col_idx].lower() != "float" \
				and type_dict[col_idx].lower() != "string" \
				and type_dict[col_idx].lower() != "boolean"\
				and type_dict[col_idx].lower() != "intarr"\
				and type_dict[col_idx].lower() != "floatarr"\
				and type_dict[col_idx].lower() != "stringarr"\
				and type_dict[col_idx].lower() != "booleanarr"):
				return {}, -1, "sheet[" + sheet_name + "]" + \
					" row[3] column[" + str(col_idx + 1) + \
					"] type must be [none] [int] or [float] or [string] or [boolean] or [intarr] or [stringarr] or [floatarr] or [booleanarr]"

		#主键值必须是int或者string型
		if type_dict[0].lower() != "int" and type_dict[0].lower() != "string":
			return {}, -1,"sheet[" + sheet_name + "]" + " first column type must be [int] or [string]"
 
		excel["meta"][sheet_name]["desc"] = desc
		excel["meta"][sheet_name]["title"] = title
		excel["meta"][sheet_name]["type"] = type_dict

		#数据从第3行开始
		row_idx = 3
		for row_idx in range(3, sheet.nrows):
			row = {}
			col_idx = 0
			for col_idx in range(len(title)):
				value = sheet.cell_value(row_idx, col_idx)
				vtype = sheet.cell_type(row_idx, col_idx)
				# 本行有数据
				valueItem = None
				if type_dict[col_idx].lower() == "int" and vtype == 2:
					valueItem = int(value)
				elif type_dict[col_idx].lower() == "float" and vtype == 2:
					valueItem = float(value)
				elif type_dict[col_idx].lower() == "string":					
					valueItem = format_str(value)
					valueItem = valueItem.replace('.0','')
				elif type_dict[col_idx].lower() == "boolean" and vtype == 4:
					if value == 1:
						valueItem = "true"
					else:
						valueItem = "false"
				elif type_dict[col_idx].lower() == "intarr" and vtype == 1:
					valueItem = str(value)
				elif type_dict[col_idx].lower() == "floatarr" and vtype == 1:
					valueItem = str(value)
				elif type_dict[col_idx].lower() == "stringarr":
					valueItem = format_str(value)
				elif type_dict[col_idx].lower() == "booleanarr" and vtype == 1:
					valueItem = str(value)
				row[col_idx] = valueItem
				
			if(len(str(row[0])) == 0):continue;
			excel["data"][sheet_name][row_idx - 3] = row

	return excel, 0 , "ok"

def format_str(value):
	if type(value) == int or type(value) == float:
		value =  str(value)
	
	value = value.replace('\"','\\\"')
	value = value.replace('\'','\\\'')
	return value

def get_int(value):
	if value is None:
		return 0
	return value

def get_float(value):
	if value is None:
		return 0
	return value

def get_string(value):
	if value is None:
		return ""
	return value

def get_boolean(value):
	if value is None:
		return "false"
	return value

def get_array_int( value ):
	if value is None:
		return "{}"
	tmp_vec_str = value.split(';')
	res_str = "{"
	i = 0
	for val in tmp_vec_str:
		if val != None and val != "":
			if i != 0:
				res_str += ","
			res_str = res_str + val
			i+=1
	res_str += "}"
	return res_str

def get_array_float( value ):
	if value is None:
		return "{}"
	tmp_vec_str = value.split(';')
	res_str = "{"
	i = 0
	for val in tmp_vec_str:
		if val != None and val != "":
			if i != 0:
				res_str += ","
			res_str = res_str + val
			i+=1
	res_str += "}"
	return res_str

def get_array_string( value ):
	if value is None:
		return "{}"
	tmp_vec_str = value.split(';')
	res_str = "{"
	i = 0
	for val in tmp_vec_str:
		if val != None and val != "":
			if i != 0:
				res_str += ","
			res_str = res_str + "\"" + val + "\""
			i+=1
	res_str += "}"
	return res_str

def get_array_boolean( value ):
	if value is None:
		return "{}"
	tmp_vec_str = value.split(';')
	res_str = "{"
	i = 0
	for val in tmp_vec_str:
		if val != None and val != "":
			if i != 0:
				res_str += ","
			res_str = res_str + val.lower()
			i+=1
	res_str += "}"
	return res_str

def write_to_lua_script(excel, output_path):
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	for (sheet_name, sheet) in excel["data"].items():

		desc = excel["meta"][sheet_name]["desc"]
		title = excel["meta"][sheet_name]["title"]
		type_dict= excel["meta"][sheet_name]["type"]

		outfp = codecs.open(output_path + "/" + sheet_name + ".lua", 'w', 'UTF-8')
		#写入文件头
		# create_time = time.strftime("%a %b %d %H:%M:%S %Y", time.gmtime(time.time()))
		create_time = time.strftime("%b %Y", time.gmtime(time.time()))
		outfp.write(SCRIPT_HEAD % (excel["filename"], create_time)) 

		#写入列名、属性、注释等
		outfp.write("--properties\n")
		for (col_idx) in title:
			if type_dict[col_idx] == "none":continue
			outfp.write("-- " + str(title[col_idx]) + ":" + str(type_dict[col_idx]) + "  //  " + str(desc[col_idx]) + "\n")
		outfp.write("\n\n")

		#写入lua data table 数据内容
		outfp.write("local data = {}\n")
		outfp.write("\n")
		
		row_idx = 0;
		for (row_idx, row) in sheet.items():
			#每行主键
			if type_dict[0] == "int":
				outfp.write("data[" + str(row[0]) + "] = { ")
			elif  type_dict[0] == "string":
				outfp.write("data[" + "\"" + str(row[0]) + "\"" + "] = { ")

			#每行具体列名及数据
			field_index = 0
			for (col_idx, field) in row.items():
				if type_dict[col_idx] == "none":continue
				if field_index > 0: outfp.write(", ")
				field_index += 1
				if type_dict[col_idx] == "int":
					tmp_str = get_int(row[col_idx])
					outfp.write(" " + str(title[col_idx]) + " = " + str(tmp_str))
				elif type_dict[col_idx] == "float":
					tmp_str = get_float(row[col_idx])
					outfp.write(" " + str(title[col_idx]) + " = " + str(tmp_str))
				elif type_dict[col_idx] == "string":
					tmp_str = get_string(row[col_idx]) 
					outfp.write(" " + str(title[col_idx]) + " = \"" + str(tmp_str) + "\"")
				elif type_dict[col_idx] == "boolean":
					tmp_str = get_boolean(row[col_idx])
					outfp.write(" " + str(title[col_idx]) + " = " + str(tmp_str))
				elif type_dict[col_idx] == "intArr":
					tmp_str = get_array_int(row[col_idx])
					outfp.write(" " + str(title[col_idx]) + " = " + str(tmp_str))
				elif type_dict[col_idx] == "floatArr":
					tmp_str = get_array_float(row[col_idx])
					outfp.write(" " + str(title[col_idx]) + " = " + str(tmp_str))
				elif type_dict[col_idx] == "stringArr":
					tmp_str = get_array_string(row[col_idx])
					outfp.write(" " + str(title[col_idx]) + " = " + str(tmp_str))
				elif type_dict[col_idx] == "booleanArr":
					tmp_str = get_array_boolean(row[col_idx])
					outfp.write(" " + str(title[col_idx]) + " = " + str(tmp_str))
				else:
					outfp.close()
					sys.exit("error: there is some wrong in type.")

			outfp.write(" }\n")

		outfp.write("\nreturn data\n")
		outfp.close()

#单个Excel文件操作
def handler_file(excel_name, output_path):
	data, ret, errstr = make_table(excel_name)
	if ret != 0:
		print(excel_name)
		print("error: " + errstr)
	else:
		print(excel_name)
		print("res:")
		#print(data)
		print("success!!!")
		write_to_lua_script(data, output_path)

#对某个目录下的所有Excel文件操作
def handler_path(excel_path, output_path):
	from platform import python_version
	print('Python', python_version())
	
	if (os.path.exists(output_path)==False):		
		os.makedirs(output_path)
		
	for parent, dirnames, filenames in os.walk(excel_path):				
		for filename in filenames:          
			if (parent == excel_path):
				handler_file(os.path.join(parent, filename), output_path)

if __name__=="__main__":
	handler_path("策划数值配置/", "Config/")