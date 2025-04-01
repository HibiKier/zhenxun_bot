from strenum import StrEnum


class BankHandleType(StrEnum):
    DEPOSIT = "DEPOSIT"
    """存款"""
    WITHDRAW = "WITHDRAW"
    """取款"""
    LOAN = "LOAN"
    """贷款"""
    REPAYMENT = "REPAYMENT"
    """还款"""
    INTEREST = "INTEREST"
    """利息"""
