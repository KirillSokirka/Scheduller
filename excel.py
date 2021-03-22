import openpyxl
import config


EF = open(config.ExcelFile, 'rb')
Book = openpyxl.open(EF, read_only=True)


def day_to_table(sheet, day):

    for Day in range(5,30,6):
        sheetvalue = str(sheet[Day][0].value).replace(' ', '')
        if sheetvalue == day:
            break

    return Day


def ExcelOneDay(group, day):

    sheet = Book.active
    result = list()

    Day = day_to_table(sheet, day)

    for i in range(Day,Day+6):
        if sheet[i][group+1].value != None:
            result.append('[' + sheet[i][1].value + ' \- ' + sheet[i][group+1].value)

    return result