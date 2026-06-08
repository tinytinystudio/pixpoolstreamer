from dataclasses import dataclass
from math import ceil, inf
from pprint import pprint


@dataclass
class ScreenCostCalculator:
    # Investimento / ativo
    purchase_price: float
    residual_value: float = 0.0
    useful_life_years: float = 5.0

    # Operação da tela
    power_watts: float = 150.0
    electricity_price_kwh: float = 1.00
    hours_per_day: float = 12.0
    days_per_month: int = 30

    # Custos do dono da tela
    internet_monthly_cost: float = 0.0
    maintenance_monthly_cost: float = 0.0
    other_screen_monthly_costs: float = 0.0

    # Custos da plataforma por tela
    platform_monthly_cost: float = 0.0

    # Receita
    ads_per_hour: int = 12
    revenue_per_ad: float = 0.10

    # Divisão de receita
    platform_commission_percent: float = 30.0

    # ---------- Depreciação ----------

    @property
    def depreciable_value(self) -> float:
        return max(self.purchase_price - self.residual_value, 0)

    @property
    def monthly_depreciation(self) -> float:
        return self.depreciable_value / (self.useful_life_years * 12)

    @property
    def annual_depreciation(self) -> float:
        return self.depreciable_value / self.useful_life_years

    def accumulated_depreciation(self, months: int) -> float:
        return min(self.monthly_depreciation * months, self.depreciable_value)

    def book_value(self, months: int) -> float:
        return max(
            self.purchase_price - self.accumulated_depreciation(months),
            self.residual_value
        )

    # ---------- Energia ----------

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

    # ---------- Custos ----------

    @property
    def screen_monthly_cost(self) -> float:
        return (
            self.monthly_depreciation
            + self.electricity_cost_per_month
            + self.internet_monthly_cost
            + self.maintenance_monthly_cost
            + self.other_screen_monthly_costs
        )

    @property
    def screen_daily_cost(self) -> float:
        return self.screen_monthly_cost / self.days_per_month

    @property
    def screen_hourly_cost(self) -> float:
        monthly_hours = self.hours_per_day * self.days_per_month
        if monthly_hours <= 0:
            return 0
        return self.screen_monthly_cost / monthly_hours

    @property
    def total_business_monthly_cost(self) -> float:
        return self.screen_monthly_cost + self.platform_monthly_cost

    # ---------- Capacidade comercial ----------

    @property
    def monthly_operating_hours(self) -> float:
        return self.hours_per_day * self.days_per_month

    @property
    def daily_ads_capacity(self) -> int:
        return int(self.ads_per_hour * self.hours_per_day)

    @property
    def monthly_ads_capacity(self) -> int:
        return int(self.daily_ads_capacity * self.days_per_month)

    # ---------- Receita ----------

    @property
    def gross_revenue_month(self) -> float:
        return self.monthly_ads_capacity * self.revenue_per_ad

    @property
    def gross_revenue_day(self) -> float:
        return self.gross_revenue_month / self.days_per_month

    @property
    def platform_commission_rate(self) -> float:
        return self.platform_commission_percent / 100

    @property
    def platform_revenue_month(self) -> float:
        return self.gross_revenue_month * self.platform_commission_rate

    @property
    def screen_owner_revenue_month(self) -> float:
        return self.gross_revenue_month - self.platform_revenue_month

    # ---------- Lucro ----------

    @property
    def screen_owner_profit_month(self) -> float:
        return self.screen_owner_revenue_month - self.screen_monthly_cost

    @property
    def platform_profit_month(self) -> float:
        return self.platform_revenue_month - self.platform_monthly_cost

    @property
    def business_profit_month(self) -> float:
        return self.screen_owner_profit_month + self.platform_profit_month

    @property
    def screen_owner_margin_percent(self) -> float:
        if self.screen_owner_revenue_month <= 0:
            return 0
        return (self.screen_owner_profit_month / self.screen_owner_revenue_month) * 100

    @property
    def platform_margin_percent(self) -> float:
        if self.platform_revenue_month <= 0:
            return 0
        return (self.platform_profit_month / self.platform_revenue_month) * 100

    # ---------- Unit economics ----------

    @property
    def cost_per_ad_screen_owner(self) -> float:
        if self.monthly_ads_capacity <= 0:
            return 0
        return self.screen_monthly_cost / self.monthly_ads_capacity

    @property
    def platform_cost_per_ad(self) -> float:
        if self.monthly_ads_capacity <= 0:
            return 0
        return self.platform_monthly_cost / self.monthly_ads_capacity

    @property
    def business_cost_per_ad(self) -> float:
        if self.monthly_ads_capacity <= 0:
            return 0
        return self.total_business_monthly_cost / self.monthly_ads_capacity

    @property
    def profit_per_ad_screen_owner(self) -> float:
        owner_revenue_per_ad = self.revenue_per_ad * (1 - self.platform_commission_rate)
        return owner_revenue_per_ad - self.cost_per_ad_screen_owner

    @property
    def profit_per_ad_platform(self) -> float:
        platform_revenue_per_ad = self.revenue_per_ad * self.platform_commission_rate
        return platform_revenue_per_ad - self.platform_cost_per_ad

    # ---------- Break-even ----------

    @property
    def break_even_ads_per_month_screen_owner(self) -> int:
        owner_revenue_per_ad = self.revenue_per_ad * (1 - self.platform_commission_rate)
        if owner_revenue_per_ad <= 0:
            return 0
        return ceil(self.screen_monthly_cost / owner_revenue_per_ad)

    @property
    def break_even_ads_per_day_screen_owner(self) -> float:
        return self.break_even_ads_per_month_screen_owner / self.days_per_month

    @property
    def break_even_ads_per_month_platform(self) -> int:
        platform_revenue_per_ad = self.revenue_per_ad * self.platform_commission_rate
        if platform_revenue_per_ad <= 0:
            return 0
        return ceil(self.platform_monthly_cost / platform_revenue_per_ad)

    @property
    def break_even_ads_per_day_platform(self) -> float:
        return self.break_even_ads_per_month_platform / self.days_per_month

    # ---------- Payback / ROI ----------

    @property
    def payback_months_screen_owner(self) -> float:
        if self.screen_owner_profit_month <= 0:
            return inf
        return self.purchase_price / self.screen_owner_profit_month

    @property
    def roi_monthly_screen_owner_percent(self) -> float:
        if self.purchase_price <= 0:
            return 0
        return (self.screen_owner_profit_month / self.purchase_price) * 100

    @property
    def roi_annual_screen_owner_percent(self) -> float:
        return self.roi_monthly_screen_owner_percent * 12

    # ---------- Resumos ----------

    def screen_owner_summary(self) -> dict:
        return {
            "receita_mensal_dono_tela": round(self.screen_owner_revenue_month, 2),
            "custo_mensal_dono_tela": round(self.screen_monthly_cost, 2),
            "lucro_mensal_dono_tela": round(self.screen_owner_profit_month, 2),
            "margem_dono_tela_percent": round(self.screen_owner_margin_percent, 2),
            "payback_meses_dono_tela": (
                None if self.payback_months_screen_owner == inf
                else round(self.payback_months_screen_owner, 2)
            ),
            "roi_mensal_dono_tela_percent": round(self.roi_monthly_screen_owner_percent, 2),
            "roi_anual_dono_tela_percent": round(self.roi_annual_screen_owner_percent, 2),
            "break_even_ads_dia_dono_tela": round(self.break_even_ads_per_day_screen_owner, 2),
        }

    def platform_summary(self) -> dict:
        return {
            "receita_mensal_plataforma": round(self.platform_revenue_month, 2),
            "custo_mensal_plataforma": round(self.platform_monthly_cost, 2),
            "lucro_mensal_plataforma": round(self.platform_profit_month, 2),
            "margem_plataforma_percent": round(self.platform_margin_percent, 2),
            "break_even_ads_dia_plataforma": round(self.break_even_ads_per_day_platform, 2),
        }

    def business_summary(self) -> dict:
        return {
            "horas_operacao_mes": round(self.monthly_operating_hours, 2),
            "capacidade_anuncios_dia": self.daily_ads_capacity,
            "capacidade_anuncios_mes": self.monthly_ads_capacity,
            "receita_bruta_mensal": round(self.gross_revenue_month, 2),
            "receita_bruta_diaria": round(self.gross_revenue_day, 2),
            "comissao_plataforma_percent": self.platform_commission_percent,
            "custo_total_negocio_mes": round(self.total_business_monthly_cost, 2),
            "lucro_total_negocio_mes": round(self.business_profit_month, 2),
            "custo_por_anuncio_negocio": round(self.business_cost_per_ad, 4),
            "lucro_por_anuncio_dono_tela": round(self.profit_per_ad_screen_owner, 4),
            "lucro_por_anuncio_plataforma": round(self.profit_per_ad_platform, 4),
        }

    def full_summary(self) -> dict:
        return {
            "dono_tela": self.screen_owner_summary(),
            "plataforma": self.platform_summary(),
            "negocio": self.business_summary(),
            "custos_operacionais": {
                "depreciacao_mensal": round(self.monthly_depreciation, 2),
                "energia_mensal": round(self.electricity_cost_per_month, 2),
                "energia_por_hora": round(self.electricity_cost_per_hour, 4),
                "internet_mensal": round(self.internet_monthly_cost, 2),
                "manutencao_mensal": round(self.maintenance_monthly_cost, 2),
                "outros_custos_tela": round(self.other_screen_monthly_costs, 2),
            }
        }


if __name__ == "__main__":
    screen = ScreenCostCalculator(
        purchase_price=5000.00,
        residual_value=300.00,
        useful_life_years=5,
        power_watts=150,
        electricity_price_kwh=1.00,
        hours_per_day=8,
        days_per_month=30,
        internet_monthly_cost=0,
        maintenance_monthly_cost=15,
        other_screen_monthly_costs=0,
        platform_monthly_cost=50,
        ads_per_hour=36,
        revenue_per_ad=0.15,
        platform_commission_percent=30
    )

    pprint(screen.business_summary())