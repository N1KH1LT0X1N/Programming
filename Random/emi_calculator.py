#!/usr/bin/env python3
"""
EMI (Equated Monthly Installment) Calculator

Calculates monthly EMI for loans with fixed interest rates.
EMI Formula: EMI = (P × r × (1 + r)^n) / ((1 + r)^n - 1)
where:
  P = Principal amount
  r = Monthly interest rate (annual rate / 12 / 100)
  n = Number of months (years × 12)
"""

def calculate_emi(principal, annual_rate, years):
    """
    Calculate EMI for a loan.
    
    Args:
        principal (float): Loan amount in currency units
        annual_rate (float): Annual interest rate as percentage (e.g., 8.5 for 8.5%)
        years (int/float): Loan tenure in years
    
    Returns:
        dict: Contains EMI, total amount payable, and total interest
    """
    if principal <= 0 or annual_rate < 0 or years <= 0:
        raise ValueError("Principal and years must be positive, interest rate must be non-negative")
    
    # Convert annual rate to monthly rate
    monthly_rate = annual_rate / 12 / 100
    
    # Convert years to months
    num_months = int(years * 12)
    
    # Handle edge case where monthly rate is 0 (0% interest)
    if monthly_rate == 0:
        emi = principal / num_months
    else:
        # EMI formula
        numerator = principal * monthly_rate * ((1 + monthly_rate) ** num_months)
        denominator = ((1 + monthly_rate) ** num_months) - 1
        emi = numerator / denominator
    
    total_payable = emi * num_months
    total_interest = total_payable - principal
    
    return {
        "emi": round(emi, 2),
        "total_payable": round(total_payable, 2),
        "total_interest": round(total_interest, 2),
        "num_months": num_months,
        "principal": principal,
        "annual_rate": annual_rate
    }


def amortization_schedule(principal, annual_rate, years):
    """
    Generate month-by-month amortization schedule.
    
    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate as percentage
        years (int/float): Loan tenure in years
    
    Yields:
        dict: Monthly payment details (month, payment, principal, interest, balance)
    """
    emi_data = calculate_emi(principal, annual_rate, years)
    emi = emi_data["emi"]
    
    monthly_rate = annual_rate / 12 / 100
    balance = principal
    
    for month in range(1, emi_data["num_months"] + 1):
        interest_payment = round(balance * monthly_rate, 2)
        principal_payment = round(emi - interest_payment, 2)
        balance = round(balance - principal_payment, 2)
        
        # Adjust for last payment to account for rounding
        if month == emi_data["num_months"]:
            principal_payment = round(principal_payment + balance, 2)
            balance = 0
        
        yield {
            "month": month,
            "emi": emi,
            "principal": principal_payment,
            "interest": interest_payment,
            "balance": balance
        }


def interactive_calculator():
    """Interactive CLI for EMI calculator."""
    print("\n" + "="*50)
    print("       EMI Calculator")
    print("="*50 + "\n")
    
    try:
        principal = float(input("Enter loan amount (Principal): "))
        annual_rate = float(input("Enter annual interest rate (%): "))
        years = float(input("Enter loan tenure (years): "))
        
        result = calculate_emi(principal, annual_rate, years)
        
        print("\n" + "-"*50)
        print("LOAN DETAILS:")
        print("-"*50)
        print(f"Principal Amount:      ${result['principal']:,.2f}")
        print(f"Annual Interest Rate:  {result['annual_rate']}%")
        print(f"Loan Tenure:           {years} years ({result['num_months']} months)")
        print("-"*50)
        print(f"Monthly EMI:           ${result['emi']:,.2f}")
        print(f"Total Amount Payable:  ${result['total_payable']:,.2f}")
        print(f"Total Interest:        ${result['total_interest']:,.2f}")
        print("-"*50 + "\n")
        
        # Ask if user wants amortization schedule
        show_schedule = input("Show amortization schedule? (y/n): ").lower()
        if show_schedule == 'y':
            print("\n" + "-"*70)
            print(f"{'Month':<6} {'EMI':<12} {'Principal':<12} {'Interest':<12} {'Balance':<12}")
            print("-"*70)
            
            for row in amortization_schedule(principal, annual_rate, years):
                print(f"{row['month']:<6} ${row['emi']:<11,.2f} ${row['principal']:<11,.2f} ${row['interest']:<11,.2f} ${row['balance']:<11,.2f}")
            print("-"*70 + "\n")
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Invalid input: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 4:
        # Command line usage: python emi_calculator.py <principal> <rate> <years>
        try:
            principal = float(sys.argv[1])
            annual_rate = float(sys.argv[2])
            years = float(sys.argv[3])
            
            result = calculate_emi(principal, annual_rate, years)
            print(f"\nPrincipal: ${result['principal']:,.2f}")
            print(f"Rate: {result['annual_rate']}% p.a.")
            print(f"Tenure: {years} years")
            print(f"\nMonthly EMI: ${result['emi']:,.2f}")
            print(f"Total Interest: ${result['total_interest']:,.2f}")
            print(f"Total Payable: ${result['total_payable']:,.2f}\n")
        except ValueError:
            print("Usage: python emi_calculator.py <principal> <interest_rate> <years>")
    else:
        # Interactive mode
        interactive_calculator()
