from dataclasses import dataclass


@dataclass
class ScreenCostCalculator:
    purchase_price: float
    residual_value: float = 0.0
    useful_life_years: float = 5.0

    power_watts: float = 150.0
    electricity_price_kwh: float = 1.00
    hours_per_day: float = 12.0
    days_per_month: int = 30

    internet_monthly_cost: float = 0.0
    maintenance_monthly_cost: float = 0.0
    platform_monthly_cost: float = 0.0
    other_monthly_costs: float = 0.0

    ads_per_hour: int = 12
    revenue_per_ad: float = 0.10

    @property
    def depreciable_value(self) -> float:
        return max(self.purchase_price - self.residual_value, 0)

    @property
    def monthly_depreciation(self) -> float:
        return self.depreciable_value / (self.useful_life_years * 12)

    @property
    def electricity_kwh_per_hour(self) -> float:
        return self.power_watts / 1000

    @property
    def electricity_cost_per_hour(self) -> float:
        return self.electricity_kwh_per_hour * self.electricity_price_kwh

    @property
    def electricity_cost_per_day(self) -> float:
        return self.electricity_cost_per_hour * self.hours_per_day

    @property
    def electricity_cost_per_month(self) -> float:
        return self.electricity_cost_per_day * self.days_per_month

    @property
    def fixed_monthly_costs(self) -> float:
        return (
            self.internet_monthly_cost
            + self.maintenance_monthly_cost
            + self.platform_monthly_cost
            + self.other_monthly_costs
        )

    @property
    def total_monthly_cost(self) -> float:
        return (
            self.monthly_depreciation
            + self.electricity_cost_per_month
            + self.fixed_monthly_costs
        )

    @property
    def total_daily_cost(self) -> float:
        return self.total_monthly_cost / self.days_per_month

    @property
    def total_hourly_cost(self) -> float:
        monthly_hours = self.hours_per_day * self.days_per_month
        return self.total_monthly_cost / monthly_hours

    @property
    def monthly_ads_capacity(self) -> int:
        return int(self.ads_per_hour * self.hours_per_day * self.days_per_month)

    @property
    def revenue_per_month(self) -> float:
        return self.monthly_ads_capacity * self.revenue_per_ad

    @property
    def profit_per_month(self) -> float:
        return self.revenue_per_month - self.total_monthly_cost

    @property
    def cost_per_ad(self) -> float:
        if self.monthly_ads_capacity == 0:
            return 0
        return self.total_monthly_cost / self.monthly_ads_capacity

    @property
    def break_even_ads_per_month(self) -> int:
        if self.revenue_per_ad <= 0:
            return 0
        return int(self.total_monthly_cost / self.revenue_per_ad)

    @property
    def break_even_ads_per_day(self) -> float:
        return self.break_even_ads_per_month / self.days_per_month

    def accumulated_depreciation(self, months: int) -> float:
        return min(self.monthly_depreciation * months, self.depreciable_value)

    def book_value(self, months: int) -> float:
        return max(
            self.purchase_price - self.accumulated_depreciation(months),
            self.residual_value
        )

    def summary(self) -> dict:
        return {
            "depreciacao_mensal": round(self.monthly_depreciation, 2),
            "energia_por_hora": round(self.electricity_cost_per_hour, 4),
            "energia_por_mes": round(self.electricity_cost_per_month, 2),
            "custos_fixos_mensais": round(self.fixed_monthly_costs, 2),
            "custo_total_mensal": round(self.total_monthly_cost, 2),
            "custo_total_diario": round(self.total_daily_cost, 2),
            "custo_total_hora": round(self.total_hourly_cost, 4),
            "capacidade_anuncios_mes": self.monthly_ads_capacity,
            "custo_por_anuncio": round(self.cost_per_ad, 4),
            "receita_mensal": round(self.revenue_per_month, 2),
            "lucro_mensal": round(self.profit_per_month, 2),
            "break_even_anuncios_mes": self.break_even_ads_per_month,
            "break_even_anuncios_dia": round(self.break_even_ads_per_day, 2),
        }


if __name__ == "__main__":
    screen = ScreenCostCalculator(
        purchase_price=3000.00,
        residual_value=300.00,
        useful_life_years=5,
        power_watts=150,
        electricity_price_kwh=1.00,
        hours_per_day=6,
        days_per_month=30,
        internet_monthly_cost=0,
        maintenance_monthly_cost=15,
        platform_monthly_cost=20,
        ads_per_hour=180,
        revenue_per_ad=0.25
    )

    for key, value in screen.summary().items():
        print(f"{key}: {value}")