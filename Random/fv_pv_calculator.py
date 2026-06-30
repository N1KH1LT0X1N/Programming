#!/usr/bin/env python3
"""
Future Value (FV) and Present Value (PV) Calculator

Calculates the future value of investments and present value of future cash flows.

Formulas:
  FV = PV × (1 + r)^n
  PV = FV / (1 + r)^n
  
where:
  FV = Future Value
  PV = Present Value
  r = Interest rate per period (annual rate / 100 / periods per year)
  n = Number of periods
"""

def calculate_fv(present_value, annual_rate, years, compounds_per_year=1):
    """
    Calculate Future Value of an investment.
    
    Args:
        present_value (float): Initial investment amount
        annual_rate (float): Annual interest rate as percentage (e.g., 8.5 for 8.5%)
        years (float): Investment period in years
        compounds_per_year (int): Compounding frequency:
                                  1=annually, 2=semi-annually, 4=quarterly, 12=monthly, 365=daily
    
    Returns:
        dict: Contains FV, total interest earned, and calculation details
    """
    if present_value <= 0 or annual_rate < 0 or years <= 0 or compounds_per_year <= 0:
        raise ValueError("PV and years must be positive, rate must be non-negative")
    
    # Convert annual rate to rate per period
    rate_per_period = annual_rate / 100 / compounds_per_year
    
    # Calculate number of periods
    num_periods = int(years * compounds_per_year)
    
    # FV formula
    future_value = present_value * ((1 + rate_per_period) ** num_periods)
    interest_earned = future_value - present_value
    
    return {
        "future_value": round(future_value, 2),
        "present_value": present_value,
        "interest_earned": round(interest_earned, 2),
        "annual_rate": annual_rate,
        "years": years,
        "compounds_per_year": compounds_per_year,
        "num_periods": num_periods,
        "effective_annual_rate": round((((1 + rate_per_period) ** compounds_per_year) - 1) * 100, 4)
    }


def calculate_pv(future_value, annual_rate, years, compounds_per_year=1):
    """
    Calculate Present Value of a future cash flow.
    
    Args:
        future_value (float): Future amount to be received
        annual_rate (float): Annual discount/interest rate as percentage
        years (float): Time period in years
        compounds_per_year (int): Compounding frequency
    
    Returns:
        dict: Contains PV, discount amount, and calculation details
    """
    if future_value <= 0 or annual_rate < 0 or years <= 0 or compounds_per_year <= 0:
        raise ValueError("FV and years must be positive, rate must be non-negative")
    
    # Convert annual rate to rate per period
    rate_per_period = annual_rate / 100 / compounds_per_year
    
    # Calculate number of periods
    num_periods = int(years * compounds_per_year)
    
    # PV formula
    present_value = future_value / ((1 + rate_per_period) ** num_periods)
    discount = future_value - present_value
    
    return {
        "present_value": round(present_value, 2),
        "future_value": future_value,
        "discount": round(discount, 2),
        "annual_rate": annual_rate,
        "years": years,
        "compounds_per_year": compounds_per_year,
        "num_periods": num_periods,
        "effective_annual_rate": round((((1 + rate_per_period) ** compounds_per_year) - 1) * 100, 4)
    }


def fv_with_regular_deposits(deposit, annual_rate, years, compounds_per_year=12):
    """
    Calculate Future Value with regular periodic deposits (annuity).
    
    Args:
        deposit (float): Regular deposit amount per period
        annual_rate (float): Annual interest rate as percentage
        years (float): Investment period in years
        compounds_per_year (int): Number of deposits per year (default 12 for monthly)
    
    Returns:
        dict: Contains FV with deposits, total deposits, and interest earned
    """
    if deposit <= 0 or annual_rate < 0 or years <= 0:
        raise ValueError("Deposit and years must be positive")
    
    rate_per_period = annual_rate / 100 / compounds_per_year
    num_periods = int(years * compounds_per_year)
    
    if rate_per_period == 0:
        future_value = deposit * num_periods
    else:
        # Future Value of Annuity formula
        future_value = deposit * (((1 + rate_per_period) ** num_periods - 1) / rate_per_period)
    
    total_deposits = deposit * num_periods
    interest_earned = future_value - total_deposits
    
    return {
        "future_value": round(future_value, 2),
        "total_deposits": round(total_deposits, 2),
        "interest_earned": round(interest_earned, 2),
        "periodic_deposit": deposit,
        "annual_rate": annual_rate,
        "years": years,
        "deposits_per_year": compounds_per_year,
        "num_periods": num_periods
    }


def pv_of_annuity(periodic_payment, annual_rate, years, compounds_per_year=12):
    """
    Calculate Present Value of an annuity (series of equal payments).
    
    Args:
        periodic_payment (float): Regular payment amount per period
        annual_rate (float): Annual discount rate as percentage
        years (float): Time period in years
        compounds_per_year (int): Payments per year (default 12 for monthly)
    
    Returns:
        dict: Contains PV of annuity and calculation details
    """
    if periodic_payment <= 0 or annual_rate < 0 or years <= 0:
        raise ValueError("Payment and years must be positive")
    
    rate_per_period = annual_rate / 100 / compounds_per_year
    num_periods = int(years * compounds_per_year)
    
    if rate_per_period == 0:
        present_value = periodic_payment * num_periods
    else:
        # PV of Annuity formula
        present_value = periodic_payment * ((1 - (1 + rate_per_period) ** -num_periods) / rate_per_period)
    
    total_payments = periodic_payment * num_periods
    
    return {
        "present_value": round(present_value, 2),
        "total_payments": round(total_payments, 2),
        "periodic_payment": periodic_payment,
        "annual_rate": annual_rate,
        "years": years,
        "payments_per_year": compounds_per_year,
        "num_periods": num_periods
    }


def interactive_fv_calculator():
    """Interactive FV calculator."""
    print("\n" + "="*60)
    print("       FUTURE VALUE (FV) Calculator")
    print("="*60 + "\n")
    
    print("1. Single Investment (lump sum)")
    print("2. Regular Deposits (annuity)\n")
    
    choice = input("Select option (1 or 2): ").strip()
    
    try:
        if choice == "1":
            pv = float(input("Enter initial investment: "))
            rate = float(input("Enter annual interest rate (%): "))
            years = float(input("Enter investment period (years): "))
            
            print("\nCompounding frequency:")
            print("1. Annual   2. Semi-annual   3. Quarterly   4. Monthly   5. Daily")
            freq_choice = input("Select (1-5, default=1): ").strip() or "1"
            
            freq_map = {"1": 1, "2": 2, "3": 4, "4": 12, "5": 365}
            compounds = freq_map.get(freq_choice, 1)
            
            result = calculate_fv(pv, rate, years, compounds)
            
            print("\n" + "-"*60)
            print("INVESTMENT DETAILS:")
            print("-"*60)
            print(f"Initial Investment:        ${result['present_value']:,.2f}")
            print(f"Annual Interest Rate:      {result['annual_rate']}%")
            print(f"Effective Annual Rate:     {result['effective_annual_rate']}%")
            print(f"Investment Period:         {result['years']} years")
            print(f"Compounding Frequency:     {result['compounds_per_year']}x per year")
            print("-"*60)
            print(f"Future Value:              ${result['future_value']:,.2f}")
            print(f"Interest Earned:           ${result['interest_earned']:,.2f}")
            print("-"*60 + "\n")
        
        elif choice == "2":
            deposit = float(input("Enter periodic deposit amount: "))
            rate = float(input("Enter annual interest rate (%): "))
            years = float(input("Enter investment period (years): "))
            
            print("\nDeposit frequency:")
            print("1. Monthly   2. Quarterly   3. Semi-annual   4. Annual")
            freq_choice = input("Select (1-4, default=1): ").strip() or "1"
            
            freq_map = {"1": 12, "2": 4, "3": 2, "4": 1}
            freq = freq_map.get(freq_choice, 12)
            
            result = fv_with_regular_deposits(deposit, rate, years, freq)
            
            print("\n" + "-"*60)
            print("INVESTMENT DETAILS:")
            print("-"*60)
            print(f"Periodic Deposit:          ${result['periodic_deposit']:,.2f}")
            print(f"Deposit Frequency:         {result['deposits_per_year']}x per year")
            print(f"Annual Interest Rate:      {result['annual_rate']}%")
            print(f"Investment Period:         {result['years']} years")
            print(f"Total Periods:             {result['num_periods']}")
            print("-"*60)
            print(f"Total Deposits:            ${result['total_deposits']:,.2f}")
            print(f"Interest Earned:           ${result['interest_earned']:,.2f}")
            print(f"Future Value:              ${result['future_value']:,.2f}")
            print("-"*60 + "\n")
    
    except Exception as e:
        print(f"Error: {e}")


def interactive_pv_calculator():
    """Interactive PV calculator."""
    print("\n" + "="*60)
    print("       PRESENT VALUE (PV) Calculator")
    print("="*60 + "\n")
    
    print("1. Single Future Cash Flow")
    print("2. Series of Equal Payments (Annuity)\n")
    
    choice = input("Select option (1 or 2): ").strip()
    
    try:
        if choice == "1":
            fv = float(input("Enter future amount: "))
            rate = float(input("Enter annual discount rate (%): "))
            years = float(input("Enter time period (years): "))
            
            print("\nCompounding frequency:")
            print("1. Annual   2. Semi-annual   3. Quarterly   4. Monthly   5. Daily")
            freq_choice = input("Select (1-5, default=1): ").strip() or "1"
            
            freq_map = {"1": 1, "2": 2, "3": 4, "4": 12, "5": 365}
            compounds = freq_map.get(freq_choice, 1)
            
            result = calculate_pv(fv, rate, years, compounds)
            
            print("\n" + "-"*60)
            print("CASH FLOW DETAILS:")
            print("-"*60)
            print(f"Future Amount:             ${result['future_value']:,.2f}")
            print(f"Annual Discount Rate:      {result['annual_rate']}%")
            print(f"Effective Annual Rate:     {result['effective_annual_rate']}%")
            print(f"Time Period:               {result['years']} years")
            print(f"Compounding Frequency:     {result['compounds_per_year']}x per year")
            print("-"*60)
            print(f"Present Value:             ${result['present_value']:,.2f}")
            print(f"Discount:                  ${result['discount']:,.2f}")
            print("-"*60 + "\n")
        
        elif choice == "2":
            payment = float(input("Enter periodic payment: "))
            rate = float(input("Enter annual discount rate (%): "))
            years = float(input("Enter time period (years): "))
            
            print("\nPayment frequency:")
            print("1. Monthly   2. Quarterly   3. Semi-annual   4. Annual")
            freq_choice = input("Select (1-4, default=1): ").strip() or "1"
            
            freq_map = {"1": 12, "2": 4, "3": 2, "4": 1}
            freq = freq_map.get(freq_choice, 12)
            
            result = pv_of_annuity(payment, rate, years, freq)
            
            print("\n" + "-"*60)
            print("ANNUITY DETAILS:")
            print("-"*60)
            print(f"Periodic Payment:          ${result['periodic_payment']:,.2f}")
            print(f"Payment Frequency:         {result['payments_per_year']}x per year")
            print(f"Annual Discount Rate:      {result['annual_rate']}%")
            print(f"Time Period:               {result['years']} years")
            print(f"Total Periods:             {result['num_periods']}")
            print("-"*60)
            print(f"Total Payments:            ${result['total_payments']:,.2f}")
            print(f"Present Value:             ${result['present_value']:,.2f}")
            print("-"*60 + "\n")
    
    except Exception as e:
        print(f"Error: {e}")


def main_menu():
    """Main menu for FV/PV calculators."""
    while True:
        print("\n" + "="*60)
        print("       FINANCIAL CALCULATORS - Main Menu")
        print("="*60)
        print("\n1. Future Value (FV) Calculator")
        print("2. Present Value (PV) Calculator")
        print("3. Exit\n")
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == "1":
            interactive_fv_calculator()
        elif choice == "2":
            interactive_pv_calculator()
        elif choice == "3":
            print("\nThank you for using Financial Calculators!\n")
            break
        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Command line usage
        if sys.argv[1] == "fv" and len(sys.argv) == 5:
            try:
                pv = float(sys.argv[2])
                rate = float(sys.argv[3])
                years = float(sys.argv[4])
                result = calculate_fv(pv, rate, years)
                print(f"\nPresent Value: ${result['present_value']:,.2f}")
                print(f"Future Value: ${result['future_value']:,.2f}")
                print(f"Interest Earned: ${result['interest_earned']:,.2f}\n")
            except ValueError:
                print("Usage: python fv_pv_calculator.py fv <pv> <rate> <years>")
        
        elif sys.argv[1] == "pv" and len(sys.argv) == 5:
            try:
                fv = float(sys.argv[2])
                rate = float(sys.argv[3])
                years = float(sys.argv[4])
                result = calculate_pv(fv, rate, years)
                print(f"\nFuture Value: ${result['future_value']:,.2f}")
                print(f"Present Value: ${result['present_value']:,.2f}")
                print(f"Discount: ${result['discount']:,.2f}\n")
            except ValueError:
                print("Usage: python fv_pv_calculator.py pv <fv> <rate> <years>")
        
        elif sys.argv[1] == "fv-annuity" and len(sys.argv) == 5:
            try:
                deposit = float(sys.argv[2])
                rate = float(sys.argv[3])
                years = float(sys.argv[4])
                result = fv_with_regular_deposits(deposit, rate, years)
                print(f"\nFuture Value (Annuity): ${result['future_value']:,.2f}")
                print(f"Total Deposits: ${result['total_deposits']:,.2f}")
                print(f"Interest Earned: ${result['interest_earned']:,.2f}\n")
            except ValueError:
                print("Usage: python fv_pv_calculator.py fv-annuity <deposit> <rate> <years>")
        
        elif sys.argv[1] == "pv-annuity" and len(sys.argv) == 5:
            try:
                payment = float(sys.argv[2])
                rate = float(sys.argv[3])
                years = float(sys.argv[4])
                result = pv_of_annuity(payment, rate, years)
                print(f"\nPresent Value (Annuity): ${result['present_value']:,.2f}")
                print(f"Total Payments: ${result['total_payments']:,.2f}\n")
            except ValueError:
                print("Usage: python fv_pv_calculator.py pv-annuity <payment> <rate> <years>")
        
        else:
            print("Usage:")
            print("  python fv_pv_calculator.py fv <pv> <rate> <years>")
            print("  python fv_pv_calculator.py pv <fv> <rate> <years>")
            print("  python fv_pv_calculator.py fv-annuity <deposit> <rate> <years>")
            print("  python fv_pv_calculator.py pv-annuity <payment> <rate> <years>")
    else:
        # Interactive mode
        main_menu()
