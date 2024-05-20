MIN_TAXABLE_AGE = 18
MIN_TAXABLE_INCOME = 300000
TAX_BRACKETS = [
    (0, 300000, 0),
    (300001, 400000, 0.1),
    (400001, 650000, 0.15),
    (650001, 1000000, 0.2),
    (1000001, 1500000, 0.25),
    (1500001, float('inf'), 0.3)
]
SURCHARGE_THRESHOLD = 1000000
SURCHARGE_RATE = 0.1
EDUCATION_ALLOWANCE = 350000
INSURANCE_PREMIUM_LIMIT = 100000
DONATION_LIMIT = 0.05
SPONSORED_CHILD_EDUCATION_LIMIT = 350000
PENSION_FUND_RATE = {
    'Government': {'Regular': 0.05, 'Contract': 0},
    'Private': {'Regular': 0.1, 'Contract': 0.1},
    'Corporate': {'Regular': 0.1, 'Contract': 0.1}
}
BONUS_RATE = {
    'Government': 0.05,
    'Private': 0.1,
    'Corporate': 0.07
}

class Employee:
    def __init__(self, name, age, salary, organization, employment_type, marital_status, num_children, children_in_school, rental_income, dividend_income):
        self.name = name
        self.age = age
        self.salary = salary
        self.organization = organization
        self.employment_type = employment_type
        self.marital_status = marital_status
        self.num_children = num_children
        self.children_in_school = children_in_school
        self.rental_income = rental_income
        self.dividend_income = dividend_income

    def calculate_tax(self):
        if self.age < MIN_TAXABLE_AGE:
            print("You are below the minimum taxable age. No tax payable.")
            return

        gross_income = self.salary + self.salary * BONUS_RATE[self.organization] + self.rental_income + self.dividend_income
        deductions = self._calculate_deductions()
        taxable_income = gross_income - deductions

        if taxable_income < MIN_TAXABLE_INCOME:
            print("Your taxable income is below the minimum taxable limit. No tax payable.")
            return

        tax_payable = self._calculate_tax_payable(taxable_income)
        surcharge = 0
        if tax_payable >= SURCHARGE_THRESHOLD:
            surcharge = tax_payable * SURCHARGE_RATE

        total_tax = tax_payable + surcharge
        print(f"Total tax payable: Nu. {total_tax:.2f}")

        # Giving the result in a tabular form
        print("\nTax Calculation Summary:")
        print("+------------------------+-----------------------+")
        print(" | Item                  | Amount                |")
        print(" +-----------------------+-----------------------+")
        print(f"| Gross Income          | {gross_income:.2f}    |")
        print(f"| Deductions            | {deductions:.2f}      |")
        print(f"| Taxable Income        | {taxable_income:.2f}  |")
        print(f"| Tax Payable           | {tax_payable:.2f}     |")
        print(f"| Surcharge             | {surcharge:.2f}       |")
        print(f"| Total Tax Payable     | {total_tax:.2f}       |")
        print("+-----------------------+------------------------+")

    def _calculate_deductions(self):
        deductions = 0
        employment_type = self.employment_type.lower()
        if employment_type == 'regular':
            employment_type = 'Regular'
        elif employment_type == 'contract':
            employment_type = 'Contract'
        pension_fund_rate = PENSION_FUND_RATE[self.organization][employment_type]
        deductions += self.salary * pension_fund_rate

        if self.marital_status == 'Married':
            deductions += EDUCATION_ALLOWANCE * self.num_children
            if self.children_in_school:
                deductions += SPONSORED_CHILD_EDUCATION_LIMIT * self.num_children

        deductions += min(self.salary * 0.1, INSURANCE_PREMIUM_LIMIT)
        deductions += min(self.salary * DONATION_LIMIT, self.salary * 0.05)

        # Dividend income decductions
        if self.dividend_income > 30000:
            deductions += self.dividend_income - 30000

        # Rental income deductions
        deductions += self.rental_income * 0.2

        return deductions

    def _calculate_tax_payable(self, taxable_income):
        tax_payable = 0
        remaining_income = taxable_income
        for income_limit, next_limit, rate in TAX_BRACKETS:
            if remaining_income <= 0:
                break
            elif remaining_income > next_limit - income_limit:
                tax_payable += (next_limit - income_limit) * rate
                remaining_income -= next_limit - income_limit
            else:
                tax_payable += remaining_income * rate
                remaining_income = 0
        return tax_payable

def main():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    if age < MIN_TAXABLE_AGE:
        print("You are below the minimum taxable age. No tax payable.")
        return

    salary = float(input("Enter your annual salary: "))
    organization = input("Enter your organization type (Government/Private/Corporate): ").capitalize()
    if organization not in ['Government', 'Private', 'Corporate']:
        print("Invalid organization type.")
        return

    if organization in ['Private', 'Corporate']:
        employment_type = 'Regular'
    else:
        employment_type = input("Enter your employment type (Regular/Contract): ").lower()
        if employment_type not in ['regular', 'contract']:
            print("Invalid employment type.")
            return
        if employment_type == 'regular':
            employment_type = 'Regular'
        else:
            employment_type = 'Contract'

    marital_status = input("Enter your marital status (Married/Single): ").capitalize()
    if marital_status not in ['Married', 'Single']:
        print("Invalid marital status.")
        return

    if marital_status == 'Married':
        have_children = input("Do you have children? (Yes/No): ").capitalize()
        if have_children not in ['Yes', 'No']:
            print("Invalid response.")
            return
        if have_children == 'Yes':
            num_children = int(input("Enter the number of children: "))
            if num_children < 0:
                print("Number of children cannot be negative.")
                return
            children_in_school = input("Do all your children go to school? (Yes/No): ").capitalize()
            if children_in_school not in ['Yes', 'No']:
                print("Invalid response.")
                return
            children_in_school = (children_in_school == 'Yes')
        else:
            num_children = 0
            children_in_school = False
    else:
        num_children = 0
        children_in_school = False

    rental_income = float(input("Enter your rental income: "))
    if rental_income < 0:
        print("Rental income cannot be negative.")
        return
    dividend_income = float(input("Enter your dividend income: "))
    if dividend_income < 0:
        print("Dividend income cannot be negative.")
        return

    employee = Employee(name, age, salary, organization, employment_type, marital_status, num_children, children_in_school, rental_income, dividend_income)
    employee.calculate_tax()

if __name__ == "__main__":
    main()