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

    sheet = Book.get_sheet_by_name("2 курс-біологи")
    result = list()

    Day = day_to_table(sheet, day)

    for i in range(Day,Day+6):
        if sheet[i][group+1].value != None:
            tempDateValue = sheet[i][1].value.replace(".", "\.").replace("-", "\-")
            tempLessonValue = sheet[i][group + 1].value\
                .replace(".", "\.")\
                .replace("(", "\(")\
                .replace(")", "\)")\
                .replace("[", "\[")\
                .replace("]", "\]")\
                .replace("-", "\-")
            result.append('[' + tempDateValue + ' \- ' + tempLessonValue)

    return result