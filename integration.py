from retriever import *

def main():
    dates=input("Please input the start date and end date in the format mm-dd-yyyy")
    dates=format_data(dates)  

    choice=input("1.A/R Adjustments\n2.Tickets\n")

    if choice == '1':
        get_ar(dates)
    elif choice =='2':
        get_tickets(dates)


def format_data(dates):
    dates=dates.split(" ")
    return dates

def get_ar(dates):
    print("inside")
    adj_query(dates)
    return 

def get_tickets(dates):
    return 

if __name__ =="__main__":
    main()