from openpyxl import load_workbook


# wb = load_workbook(filename='information.xlsx')
# ws = wb.get_sheet_by_name('info')
# print(wb.get_sheet_names())
# rowdata = tuple(ws.rows)
# if len(rowdata) > 2:
#     for i in range(1, len(rowdata)):
#         print(rowdata[i])
#         for cell in rowdata[i]:
#             print(cell.value)
#

class Excel:
    def __init__(self, path='information.xlsx'):
        self.path = path
        try:
            self.wb = load_workbook(filename=path)

        except Exception as e:
            print(e)

    # def get_work_sheet(self, sheet='info'):
    #     return self.wb.get_sheet_by_name(sheet)

    def get_datalist_from_sheet(self, sheet_name='info'):
        ws = self.wb.get_sheet_by_name(sheet_name)
        rowsObj = tuple(ws.rows)
        all_value = []
        if len(rowsObj) >= 2:
            for i in range(1, len(rowsObj)):
                # print(rowdata[i])
                row_value = []
                for cell in rowsObj[i]:
                    # print(cell.value)
                    row_value.append(str(cell.value))
                all_value.append(row_value)
        return all_value

    #TODO
    def get_datadict_by_proid(self, proid='1178', sheet_name='proinfo'):
        ws = self.wb.get_sheet_by_name(sheet_name)
        rowsObj = tuple(ws.rows)
        if len(rowsObj) >= 2:
            all_value = []
            for i in range(1, len(rowsObj)):
                if (proid == '1178'):  ##why???
                    row_value = []
                    for cell in rowsObj[i]:
                        # print(cell.value)
                        row_value.append(str(cell.value))
                    all_value.append(row_value)
            return all_value

            # cells2=tuple(ws.columns)
            # print(len(cells2))
            # print(ws['1:2'])
            # print(ws['A1:C2'])
            # print(ws['A:C'])


e = Excel('information.xlsx')
print(e.get_datadict_by_proid('1178','proinfo'))
