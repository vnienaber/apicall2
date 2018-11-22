'''This script fetches information on articles for certain Funders
It takes input either from a csv file that holds information on the funders (id and name, e.g. "501100001840,Icelandic Centre")
or from an users input (id and name)
The result is a csv-file of all articles (with additional information) for each funder

'''

from habanero import Crossref
import csv
from crossref.restful import Funders

funder = Funders()


def get_funders_works(fundersfile):
    # read in funder ids from csv-file

    funders = []
    with open(fundersfile, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader, None)
        for row in reader:
            id = row[0]
            name = row[1]
            funders.append(row)

    # create items
    list = []
    cr = Crossref()

    # get works for funders
    for f in funders:
        print(f)
        filestr = str(f[0]) + '_' + str(f[1]) + '.csv'

        # create resulting csv-file
        with open(filestr, mode='w') as csvfile:

            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['Funder ID', 'Funder Name', 'DOI', 'Type', 'Publishing Date', 'Year', 'Title',
                                 'Publication', 'Authors', 'Funders', 'Awards'])

        id = f[0]
        funders_name = f[1]
        res = cr.funders(ids=id)
        number_works = res['message']['work-count']
        # print(id)
        print('Number of associated works: ' + str(number_works))

        items = funder.works(id)
        authors = []
        funders = []
        awards = []
        incr = 0
        j = 0
        k = 0
        m = 0

        try:
            for item in items:
                try:
                    funder_ids = id
                    funder_name = funders_name
                    try:
                        doi = item['DOI']
                    except:
                        pass
                    try:
                        types = item['type']
                    except:
                        pass
                    try:
                        publishing_date = ", ".join(map(str, item['issued']['date-parts'][0]))
                    except:
                        pass
                    try:
                        year = ", ".join(map(str, item['issued']['date-parts'][0]))
                        year = year[0:4]
                    except:
                        pass
                    try:
                        title = item['title']
                    except:
                        pass
                    try:
                        publication = ", ".join(map(str, item['container-title']))
                    except:
                        pass
                    try:
                        author = item['author']
                        for a in author:
                            try:
                                family = a['given']
                            except:
                                pass
                            try:
                                given = a['family']
                            except:
                                pass
                            name = family + ' ' + given
                            authors.append(name.encode('utf-8'))

                    except:
                        pass
                    try:
                        fund = item['funder']
                        for f in fund:
                            funders.append(f['name'].encode('utf-8'))
                            awards.append(f['award'].encode('utf-8'))
                    except:
                        pass
                except:
                    pass
                list.append([funder_ids, funder_name, doi, types, publishing_date, year, title, publication,
                             ", ".join(map(str, authors)), ", ".join(map(str, funders))])

                j += 1
                k+=1
                m += 1
                authors = []
                funders = []
                awards = []
                # print len(list)
                # when all works are processed, write information to csv file

                if incr < number_works and k == 1000:
                    print incr
                    print j
                    print k
                    print m
                    with open(str(filestr) + str(incr), 'a') as f:
                        writer = csv.writer(f)
                        for i in list:
                            writer.writerow(i)
                        list = []
                        k = 0

                if incr < number_works and j == 100000:
                    print incr
                    print j
                    with open(str(filestr) + str(incr), 'a') as f:
                        writer = csv.writer(f)
                        for i in list:
                            writer.writerow(i)
                        list = []
                        j = 0
                        incr += 1

                if m >= number_works-100:
                    print(incr)
                    with open(str(filestr) + 'last', 'a') as f:
                        writer = csv.writer(f)
                        for i in list:
                            writer.writerow(i)
                        list = []

                        break
        except:
            pass


def get_funderid_works(funderid, fundername):
    # read in funder ids from csv-file
    # create items
    list = []
    cr = Crossref()



    filestr = str(funderid) + '_' + str(fundername) + '.csv'
    print filestr
    # create resulting csv-file
    with open(filestr, mode='w') as csvfile:

        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Funder ID', 'Funder Name', 'DOI', 'Type', 'Publishing Date', 'Year', 'Title',
                             'Publication', 'Authors', 'Funders', 'Awards'])

    id = funderid
    funders_name = fundername
    res = cr.funders(ids=id)
    number_works = res['message']['work-count']
    # print(id)
    print('Number of associated works: ' + str(number_works))
    incr = 0
    j = 0
    items = funder.works(id)
    authors = []
    funders = []
    awards = []
    for item in items:
        # print item['funder']
        fund = item['funder']

        funder_ids = id
        funder_name = funders_name
        try:
            doi = item['DOI']
        except:
            pass
        try:
            type = item['type']
        except:
            pass
        try:
            publishing_date = ", ".join(map(str, item['issued']['date-parts'][0]))
        except:
            pass
        try:
            year = ", ".join(map(str, item['issued']['date-parts'][0]))
            year = year[0:4]
        except:
            pass
        try:
            title = item['title']
        except:
            pass
        try:
            publication = ", ".join(map(str, item['container-title']))
        except:
            pass
        try:
            author = item['author']
            for a in author:
                try:
                    family = a['given']
                except:
                    pass
                try:
                    given = a['family']
                except:
                    pass
                name = family + ' ' + given
                authors.append(name.encode('utf-8'))

        except:
            pass
        try:
            fund = item['funder']
            for f in fund:
                funders.append(f['name'].encode('utf-8'))
                awards.append(f['award'].encode('utf-8'))
        except:
            pass

        list.append([funder_ids, funder_name, doi, type, publishing_date, year, title, publication,
                     ", ".join(map(str, authors)), ", ".join(map(str, funders))])

        incr += 1
        j += 1

        authors = []
        funders = []
        awards = []
        # print len(list)
        # when all works are processed, write information to csv file

        if incr < number_works and j == 10:
            print incr
            print j
            with open(str(filestr) + str(incr), 'a') as f:
                writer = csv.writer(f)
                for i in list:
                    writer.writerow(i)
                list = []
                j = 0

        if incr >= number_works:
            print(incr)
            with open(str(filestr) + 'last', 'a') as f:
                writer = csv.writer(f)
                for i in list:
                    writer.writerow(i)
                list = []

                break


def main():
    # get info on test doi
    #try:
    get_funders_works('funders_8.csv')
    #get_funderid_works('501100004663','Ministry of Science and Technology Taiwan')

if __name__ == "__main__":
    main()
