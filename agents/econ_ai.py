class EconAI:

    def calculate_profit(self, production=1000, market_price=2500):

        revenue = production * market_price
        cost = revenue * 0.65
        profit = revenue - cost

        if profit > 700000:
            grade = "매우 우수"
        elif profit > 400000:
            grade = "우수"
        else:
            grade = "보통"

        return {
            "production": production,
            "market_price": market_price,
            "revenue": revenue,
            "profit": profit,
            "grade": grade
        }
