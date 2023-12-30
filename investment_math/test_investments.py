from investments import monthly_mortgage_payment

def test_monthly_mortgage_payment():
    # Test case 1: No down payment
    assert monthly_mortgage_payment(200000, 0.05, 30) == 1073.64

    # Test case 2: With down payment as a percentage
    assert monthly_mortgage_payment(200000, 0.05, 30, down_payment='10%') == 966.28

    # Test case 3: With down payment as an absolute value
    assert monthly_mortgage_payment(200000, 0.05, 30, down_payment=20000) == 966.28

    # Test case 4: Zero loan amount
    assert monthly_mortgage_payment(0, 0.05, 30) == 0

    # Test case 5: Zero years
    assert monthly_mortgage_payment(200000, 0.05, 0) == 200000

    # Test case 6: Zero annual interest rate
    assert monthly_mortgage_payment(200000, 0, 30) == 555.56

    # Test case 7: Negative loan amount
    assert monthly_mortgage_payment(-200000, 0.05, 30) == 0

    # Test case 8: Negative annual interest rate
    assert monthly_mortgage_payment(200000, -0.05, 30) == 0


test_monthly_mortgage_payment()
print("All test cases pass")