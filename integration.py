from retriever import * 

def main():
    dates=input("Please input the start date and end date in the format mm-dd-yyyy")
    dates=format_data(dates)  
    print(dates)
    choice=input("1.A/R Adjustments\n2.Tickets\n")



def format_data(dates):
    dates=dates.split(" ")
    return dates



if __name__ =="__main__":
    main()