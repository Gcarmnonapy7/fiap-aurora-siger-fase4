"""
Mathematical modeling of Aurora Siger colony phenomena.
Includes differential calculus applications: rates of change, optimization, and derivative analysis.
"""

import math
from typing import Dict, List, Tuple, Optional
from modules.grafo import InfrastructureGraph
from data.data_modules import GENERATION_CAPACITY

class MathematicalModeling:
    """
    Class for mathematical modeling of colony phenomena.
    Applies differential calculus concepts for analysis and optimization.
    """
    
    def __init__(self, graph: InfrastructureGraph):
        self.graph = graph
        self.h = 0.001  # Step for numerical differentiation
        # Installed generation capacity of the colony (kW). The critical point and
        # scenarios compare projected CONSUMPTION (kW) against this, not against
        # storage capacity (kWh), which is a different physical quantity.
        self.generation_capacity = GENERATION_CAPACITY
    
    # ==================== BASE FUNCTIONS ====================
    
    def total_consumption(self, t: float, growth_rate: float = 0.12) -> float:
        """
        Total consumption function over time.
        
        C(t) = C0 * e^(r*t)
        
        Where:
        - C0: Initial consumption (sum of all modules' consumption)
        - r: Annual growth rate (12% by default)
        - t: Time in years
        
        This is an exponential function, typical of population growth and resource consumption models.
        """
        initial_consumption = sum(module.consumption for module in self.graph.module_list)
        return initial_consumption * math.exp(growth_rate * t)
    
    def consumption_per_module(self, t: float, growth_rate: float = 0.12) -> float:
        """
        Average consumption per module over time.
        
        Cm(t) = C(t) / N(t)
        
        Where N(t) is the number of modules (assuming linear growth).
        """
        n_modules = self.graph.get_module_count()
        expansion_rate = 0.5  # 0.5 new modules per year
        current_n = n_modules + expansion_rate * t
        return self.total_consumption(t, growth_rate) / current_n
    
    # ==================== DERIVATIVES (DIFFERENTIAL CALCULUS) ====================
    
    def consumption_derivative(self, t: float, growth_rate: float = 0.12) -> float:
        """
        Calculates the derivative of the consumption function at time t.
        
        Uses numerical differentiation (central difference method):
        f'(t) ≈ [f(t+h) - f(t-h)] / (2h)
        
        Interpretation: Rate of change of energy consumption at instant t.
        Measures how fast consumption is increasing or decreasing.
        """
        return (self.total_consumption(t + self.h, growth_rate) - 
                self.total_consumption(t - self.h, growth_rate)) / (2 * self.h)
    
    def consumption_second_derivative(self, t: float, growth_rate: float = 0.12) -> float:
        """
        Calculates the second derivative of the consumption function.
        
        f''(t) ≈ [f(t+h) - 2f(t) + f(t-h)] / h^2
        
        Interpretation: Consumption acceleration. If > 0, consumption is accelerating.
        If < 0, it's decelerating.
        """
        return (self.total_consumption(t + self.h, growth_rate) - 
                2 * self.total_consumption(t, growth_rate) + 
                self.total_consumption(t - self.h, growth_rate)) / (self.h ** 2)
    
    def consumption_rate_analysis(self, t: float, growth_rate: float = 0.12) -> Dict:
        """
        Complete analysis of consumption rates of change at time t.
        
        Application of differential calculus to understand consumption dynamics.
        """
        consumption = self.total_consumption(t, growth_rate)
        derivative = self.consumption_derivative(t, growth_rate)
        second_derivative = self.consumption_second_derivative(t, growth_rate)
        
        relative_rate = (derivative / consumption) * 100 if consumption > 0 else 0
        
        return {
            'time': t,
            'consumption': consumption,
            'first_derivative': derivative,
            'second_derivative': second_derivative,
            'relative_rate': relative_rate,
            'interpretation': self._interpret_rate_of_change(derivative, second_derivative)
        }
    
    def _interpret_rate_of_change(self, derivative: float, second_derivative: float) -> str:
        """
        Qualitatively interprets the derivatives.
        """
        if derivative > 0 and second_derivative > 0:
            return "Crescimento acelerado do consumo (curva convexa)"
        elif derivative > 0 and second_derivative < 0:
            return "Crescimento desacelerado do consumo (curva concava)"
        elif derivative < 0 and second_derivative > 0:
            return "Decrescimento desacelerado do consumo"
        elif derivative < 0 and second_derivative < 0:
            return "Decrescimento acelerado do consumo"
        elif abs(derivative) < 0.001:
            return "Ponto critico (maximo, minimo ou inflexao)"
        else:
            return "Crescimento estavel do consumo"
    
    # ==================== OPTIMIZATION WITH CALCULUS ====================
    
    def optimal_consumption_point(self, t_min: float = 0, t_max: float = 20) -> Dict:
        """
        Finds the optimal consumption point using calculus.
        
        Applies the extreme value theorem: maxima and minima occur where
        the derivative is zero (critical points) or at interval endpoints.
        
        For an exponential function, the minimum is at t=0 (initial consumption)
        and there is no maximum in a finite interval.
        """
        # Critical points: where derivative = 0
        critical_points = self._find_critical_points(t_min, t_max)
        
        # Evaluates at critical points and endpoints
        evaluations = []
        
        # Endpoints
        for t in [t_min, t_max]:
            evaluations.append({
                't': t,
                'consumption': self.total_consumption(t),
                'type': 'extreme'
            })
        
        # Critical points
        for t in critical_points:
            if t_min <= t <= t_max:
                second_derivative = self.consumption_second_derivative(t)
                point_type = self._classify_critical_point(second_derivative)
                evaluations.append({
                    't': t,
                    'consumption': self.total_consumption(t),
                    'type': point_type,
                    'second_derivative': second_derivative
                })
        
        # Finds minimum and maximum
        min_point = min(evaluations, key=lambda x: x['consumption']) if evaluations else None
        max_point = max(evaluations, key=lambda x: x['consumption']) if evaluations else None
        
        return {
            'critical_points': critical_points,
            'minimum': min_point,
            'maximum': max_point,
            'analysis': self._analyze_optimization(evaluations)
        }
    
    def _find_critical_points(self, t_min: float, t_max: float) -> List[float]:
        """
        Finds points where the derivative is zero (bisection method).
        
        For the exponential function C(t) = C0*e^(rt), the derivative is r*C0*e^(rt),
        which is never zero for finite t. Returns empty list.
        """
        points = []
        step = 0.1
        t = t_min
        
        while t <= t_max:
            derivative = self.consumption_derivative(t)
            if abs(derivative) < 0.001:  # Close to zero
                points.append(t)
            t += step
        
        return points
    
    def _classify_critical_point(self, second_derivative: float) -> str:
        """
        Classifies the critical point using the second derivative test.
        
        - If f''(x) > 0: local minimum
        - If f''(x) < 0: local maximum
        - If f''(x) = 0: inflection point (inconclusive test)
        """
        if second_derivative > 0:
            return "minimo_local"
        elif second_derivative < 0:
            return "maximo_local"
        else:
            return "ponto_inflexao"
    
    def _analyze_optimization(self, evaluations: List[Dict]) -> str:
        """
        Qualitative analysis of optimization.
        """
        if not evaluations:
            return "Nenhum ponto de otimizacao encontrado."
        
        min_point = min(evaluations, key=lambda x: x['consumption'])
        max_point = max(evaluations, key=lambda x: x['consumption'])
        
        return f"""
    Analise de Otimizacao do Consumo Energetico:
    ------------------------------------------
    * Consumo minimo: {min_point['consumption']:.2f} kWh em t = {min_point['t']:.2f} anos
    * Consumo maximo: {max_point['consumption']:.2f} kWh em t = {max_point['t']:.2f} anos
    * Variacao total: {max_point['consumption'] - min_point['consumption']:.2f} kWh
    
    Recomendacao: Para minimizar o consumo, mantenha a operacao no ponto de minimo.
    """
    
    # ==================== COST AND EFFICIENCY FUNCTIONS ====================
    
    def operational_cost_function(self, t: float) -> float:
        """
        Operational cost function of the colony.
        
        C(t) = C0 * t * e^(alpha*t) + beta * t^2
        
        Where:
        - C0: Base cost
        - alpha: Exponential growth factor
        - beta: Quadratic growth factor
        
        This function models costs that grow both exponentially and quadratically over time.
        """
        c0 = 1000
        alpha = 0.08
        beta = 50
        
        return c0 * t * math.exp(alpha * t) + beta * (t ** 2)
    
    def marginal_cost(self, t: float) -> float:
        """
        Calculates the marginal cost (derivative of cost).
        
        C'(t) = C0 * e^(alpha*t) * (1 + alpha*t) + 2*beta*t
        
        Interpretation: Marginal cost is the additional cost per unit of time.
        Useful for expansion decisions.
        """
        c0 = 1000
        alpha = 0.08
        beta = 50
        
        exponential_derivative = c0 * math.exp(alpha * t) * (1 + alpha * t)
        quadratic_derivative = 2 * beta * t
        
        return exponential_derivative + quadratic_derivative
    
    def marginal_efficiency(self, t: float) -> float:
        """
        Marginal efficiency = derivative of efficiency / derivative of cost.
        
        Measures the efficiency gain per unit of additional cost.
        """
        efficiency = 1 / self.total_consumption(t) if self.total_consumption(t) > 0 else 0
        
        efficiency_h = 1 / self.total_consumption(t + self.h) if self.total_consumption(t + self.h) > 0 else 0
        efficiency_minus_h = 1 / self.total_consumption(t - self.h) if self.total_consumption(t - self.h) > 0 else 0
        efficiency_derivative = (efficiency_h - efficiency_minus_h) / (2 * self.h)
        
        marginal_cost = self.marginal_cost(t)
        
        if marginal_cost != 0:
            return efficiency_derivative / marginal_cost
        return 0
    
    # ==================== TIME SERIES ANALYSIS ====================
    
    def temporal_consumption_analysis(self, years: int = 10, points: int = 100) -> Dict:
        """
        Complete consumption analysis over time using calculus.
        
        Includes:
        - Consumption function
        - First and second derivatives
        - Trend analysis
        - Critical point prediction
        """
        step = years / points
        times = [i * step for i in range(points + 1)]
        
        data = {
            'times': times,
            'consumption': [],
            'first_derivative': [],
            'second_derivative': [],
            'growth_rate': [],
            'trend_analysis': []
        }
        
        for t in times:
            consumption = self.total_consumption(t)
            derivative = self.consumption_derivative(t)
            second_derivative = self.consumption_second_derivative(t)
            
            data['consumption'].append(consumption)
            data['first_derivative'].append(derivative)
            data['second_derivative'].append(second_derivative)
            
            if t > 0:
                previous_consumption = self.total_consumption(t - step)
                if previous_consumption > 0:
                    rate = ((consumption - previous_consumption) / previous_consumption) * 100
                else:
                    rate = 0
                data['growth_rate'].append(rate)
            else:
                data['growth_rate'].append(0)
            
            data['trend_analysis'].append(self._interpret_rate_of_change(derivative, second_derivative))
        
        # Finds inflection points (where second derivative = 0)
        inflection_points = []
        for i in range(1, len(times) - 1):
            if (data['second_derivative'][i-1] < 0 and data['second_derivative'][i+1] > 0) or \
               (data['second_derivative'][i-1] > 0 and data['second_derivative'][i+1] < 0):
                inflection_points.append(times[i])
        
        return {
            'data': data,
            'inflection_points': inflection_points,
            'final_consumption': data['consumption'][-1],
            'initial_consumption': data['consumption'][0],
            'total_growth': ((data['consumption'][-1] / data['consumption'][0]) - 1) * 100 if data['consumption'][0] > 0 else 0,
            # Effective annual growth rate (CAGR), independent of the sampling
            # resolution: (final/initial)^(1/anos) - 1. For C(t)=C0*e^(rt) this is
            # e^r - 1 (~12.75% for r=0.12), consistent with the scenario rates.
            'avg_growth_rate': self._annual_growth_rate(data),
            'qualitative_analysis': self._qualitative_temporal_analysis(data)
        }
    
    def _annual_growth_rate(self, data: Dict) -> float:
        """
        Effective annual growth rate (CAGR) of consumption over the analysed span,
        in percent. Independent of the number of sample points used.
        """
        consumption = data['consumption']
        years_span = data['times'][-1] if data['times'] else 0
        if consumption and consumption[0] > 0 and years_span > 0:
            return ((consumption[-1] / consumption[0]) ** (1 / years_span) - 1) * 100
        return 0.0

    def _qualitative_temporal_analysis(self, data: Dict) -> str:
        """
        Qualitative analysis of the time series.
        """
        derivatives = data['first_derivative']
        second_derivatives = data['second_derivative']
        
        avg_growth = sum(1 for d in derivatives if d > 0) / len(derivatives) if derivatives else 0
        
        if avg_growth > 0.8:
            trend = "Crescimento acelerado"
        elif avg_growth > 0.5:
            trend = "Crescimento moderado"
        else:
            trend = "Crescimento lento ou estabilizacao"
        
        positive_concavity = sum(1 for d in second_derivatives if d > 0) / len(second_derivatives) if second_derivatives else 0
        
        if positive_concavity > 0.6:
            concavity = "Convexo (acelerando)"
        elif positive_concavity < 0.4:
            concavity = "Concavo (desacelerando)"
        else:
            concavity = "Misto"
        
        return f"""
    Analise Qualitativa do Consumo Temporal:
    ----------------------------------------
    * Tendencia: {trend}
    * Comportamento: {concavity}
    * Taxa de crescimento anual: {self._annual_growth_rate(data):.2f}%
    
    Implicacoes para a Colonia:
    {self._generate_recommendations(trend, concavity)}
    """
    
    def _generate_recommendations(self, trend: str, concavity: str) -> str:
        """
        Generates recommendations based on analysis.
        """
        recommendations = []
        
        if "acelerado" in trend:
            recommendations.append("* Consumo crescendo rapidamente. Investir em eficiencia energetica e urgente.")
        elif "moderado" in trend:
            recommendations.append("* Consumo em crescimento controlado. Monitorar tendencias.")
        else:
            recommendations.append("* Consumo estavel. Manter praticas atuais.")
        
        if "acelerando" in concavity:
            recommendations.append("* A taxa de crescimento esta aumentando. Considerar expansao da capacidade.")
        elif "desacelerando" in concavity:
            recommendations.append("* A taxa de crescimento esta diminuindo. Bom sinal de eficiencia.")
        
        return "\n    ".join(recommendations)
    
    # ==================== RESOURCE OPTIMIZATION ====================
    
    def optimize_energy_distribution(self) -> Dict:
        """
        Optimizes energy distribution using partial derivatives.
        
        Finds the point where total efficiency is maximized.
        """
        modules = self.graph.module_list
        results = {}
        
        for module in modules:
            neighbors = self.graph.get_neighbors(module.id)
            
            def module_efficiency(allocated_consumption: float) -> float:
                if allocated_consumption <= 0:
                    return 0
                
                distances = [self.graph.get_weight(module.id, v) for v in neighbors]
                if distances:
                    avg_dist = sum(d for d in distances if d != float('inf')) / len(neighbors)
                    loss = 1 - math.exp(-avg_dist * 0.1)
                else:
                    loss = 0.1
                
                return allocated_consumption / (allocated_consumption + loss)
            
            def efficiency_derivative(x: float) -> float:
                return (module_efficiency(x + self.h) - module_efficiency(x - self.h)) / (2 * self.h)
            
            optimal = module.consumption
            
            for _ in range(10):
                der = efficiency_derivative(optimal)
                if abs(der) < 0.001:
                    break
                optimal = optimal - der / ((efficiency_derivative(optimal + self.h) - efficiency_derivative(optimal - self.h)) / (2 * self.h))
                optimal = max(0, optimal)
            
            results[module.id] = {
                'name': module.name,
                'current_consumption': module.consumption,
                'optimal_consumption': optimal,
                'current_efficiency': module_efficiency(module.consumption),
                'optimal_efficiency': module_efficiency(optimal),
                'improvement': (module_efficiency(optimal) - module_efficiency(module.consumption)) * 100 if module_efficiency(module.consumption) > 0 else 0
            }
        
        return results
    
    # ==================== PREDICTION AND SIMULATION ====================
    
    def predict_critical_point(self, t_max: int = 50) -> Dict:
        """
        Predicts when projected consumption will reach a critical fraction (90%)
        of the colony's installed GENERATION capacity (kW vs kW).
        """
        generation_capacity = self.generation_capacity
        current_t = 0
        step = 0.5

        while current_t < t_max:
            consumption = self.total_consumption(current_t)
            if consumption >= generation_capacity * 0.9:
                return {
                    'critical_year': 2026 + current_t,
                    'consumption': consumption,
                    'capacity': generation_capacity,
                    'percentage': (consumption / generation_capacity) * 100,
                    'alert_level': 'Alto' if consumption / generation_capacity > 0.95 else 'Medio'
                }
            current_t += step

        return {
            'critical_year': None,
            'message': f'Nao atingira capacidade critica de geracao nos proximos {t_max} anos.'
        }
    
    def simulate_scenarios(self) -> Dict:
        """
        Simulates different growth scenarios using calculus.
        """
        scenarios = {
            'otimista': 0.08,
            'moderado': 0.12,
            'pessimista': 0.18
        }
        
        results = {}
        years = 10
        
        for name, rate in scenarios.items():
            initial_consumption = sum(module.consumption for module in self.graph.module_list)
            
            data = {
                'final_consumption': initial_consumption * math.exp(rate * years),
                'growth_percentage': (math.exp(rate * years) - 1) * 100,
                'avg_annual_rate': rate * 100,
                'max_derivative': self.consumption_derivative(years, rate),
                'min_derivative': self.consumption_derivative(0, rate),
                'analysis': self._analyze_scenario(name, rate, years)
            }
            
            results[name] = data
        
        return results
    
    def _analyze_scenario(self, name: str, rate: float, years: int) -> str:
        """
        Qualitatively analyzes a scenario.
        """
        final_consumption = sum(module.consumption for module in self.graph.module_list) * math.exp(rate * years)
        generation_capacity = self.generation_capacity

        if final_consumption > generation_capacity:
            return f"Cenario {name}: CRITICO - Demanda excedera a geracao em {years} anos"
        elif final_consumption > generation_capacity * 0.8:
            return f"Cenario {name}: ATENCAO - Demanda proxima da geracao em {years} anos"
        else:
            return f"Cenario {name}: SEGURO - Geracao suficiente para {years} anos"
    
    # ==================== COMPLETE ANALYSIS ====================
    
    def complete_analysis(self) -> Dict:
        """
        Performs complete infrastructure analysis using differential calculus.
        """
        print("\n" + "="*60)
        print("ANALISE COMPLETA COM CALCULO DIFERENCIAL")
        print("="*60)
        
        # 1. Temporal consumption analysis
        print("\n1. ANALISE TEMPORAL DO CONSUMO")
        print("-" * 40)
        temporal_analysis = self.temporal_consumption_analysis(years=10, points=100)
        
        print(f"Consumo inicial: {temporal_analysis['initial_consumption']:.2f} kWh")
        print(f"Consumo final (10 anos): {temporal_analysis['final_consumption']:.2f} kWh")
        print(f"Crescimento total: {temporal_analysis['total_growth']:.2f}%")
        print(f"Taxa media de crescimento: {temporal_analysis['avg_growth_rate']:.2f}%")
        
        if temporal_analysis['inflection_points']:
            print(f"Pontos de inflexao detectados em: {temporal_analysis['inflection_points']}")
        
        # 2. Consumption optimization
        print("\n2. OTIMIZACAO DO CONSUMO")
        print("-" * 40)
        optimal = self.optimal_consumption_point()
        if optimal['minimum']:
            print(f"Ponto de minimo: t = {optimal['minimum']['t']:.2f} anos")
            print(f"Consumo minimo: {optimal['minimum']['consumption']:.2f} kWh")
        
        # 3. Distribution optimization
        print("\n3. OTIMIZACAO DA DISTRIBUICAO DE ENERGIA")
        print("-" * 40)
        distribution = self.optimize_energy_distribution()
        
        improvements = []
        for mod_id, data in distribution.items():
            if data['improvement'] > 5:
                improvements.append(f"  * {data['name']}: melhoria de {data['improvement']:.1f}%")
        
        if improvements:
            print("Modulos com melhoria potencial significativa:")
            print("\n".join(improvements))
        else:
            print("Distribuicao atual ja esta otimizada.")
        
        # 4. Scenario analysis
        print("\n4. ANALISE DE CENARIOS")
        print("-" * 40)
        scenarios = self.simulate_scenarios()
        for name, data in scenarios.items():
            print(f"\nCenario {name.upper()}:")
            print(f"  Taxa de crescimento: {data['avg_annual_rate']:.1f}% ao ano")
            print(f"  Consumo final: {data['final_consumption']:.2f} kWh")
            print(f"  {data['analysis']}")
        
        # 5. Critical point prediction
        print("\n5. PREVISAO DE PONTO CRITICO")
        print("-" * 40)
        critical = self.predict_critical_point()
        if critical['critical_year']:
            print(f"Ponto critico previsto para: {critical['critical_year']:.0f}")
            print(f"   Consumo: {critical['consumption']:.2f} kWh")
            print(f"   Capacidade: {critical['capacity']:.2f} kWh")
            print(f"   Percentual: {critical['percentage']:.1f}%")
            print(f"   Nivel de alerta: {critical['alert_level']}")
        else:
            print(critical['message'])
        
        return {
            'temporal_analysis': temporal_analysis,
            'consumption_optimization': optimal,
            'distribution_optimization': distribution,
            'scenarios': scenarios,
            'critical_point': critical
        }
    
    # ==================== ADDITIONAL ANALYSIS METHODS ====================
    
    def energy_loss_by_distance(self, distance: float, transmission_efficiency: float = 0.95) -> float:
        """
        Models energy loss along connections.
        
        Formula: P(loss) = 1 - e^(-d * (1-η))
        Where:
        - d: Connection distance
        - η: Transmission efficiency (95% by default)
        
        Analysis: Loss follows an exponential curve, where larger distances
        result in significant losses.
        """
        return 1 - math.exp(-distance * (1 - transmission_efficiency))
    
    def distribution_efficiency(self, module_id: str) -> Dict:
        """
        Evaluates the energy distribution efficiency for a module.
        
        Formula: E = P_consumed / P_available
        Where:
        - P_consumed: Actual module consumption
        - P_available: Network delivery capacity
        """
        module = self.graph.get_module(module_id)
        if not module:
            return {'efficiency': 0, 'status': 'module_not_found'}
        
        # Calculates total delivery capacity based on neighbors
        neighbors = self.graph.get_neighbors(module_id)
        total_capacity = 0
        distances = []
        
        for neighbor_id in neighbors:
            neighbor = self.graph.get_module(neighbor_id)
            if neighbor:
                total_capacity += neighbor.capacity
                weight = self.graph.get_weight(module_id, neighbor_id)
                if weight != float('inf'):
                    distances.append(weight)
        
        # Efficiency factor based on average distance
        if distances:
            avg_distance = sum(distances) / len(distances)
            distance_factor = 1.0 / (1.0 + avg_distance * 0.1)
        else:
            avg_distance = 1.0
            distance_factor = 1.0
        
        # Efficiency = consumption / (available capacity * distance_factor)
        effective_capacity = total_capacity * distance_factor
        if effective_capacity > 0:
            efficiency = min(1.0, module.consumption / effective_capacity)
        else:
            efficiency = 0
        
        return {
            'efficiency': efficiency,
            'total_capacity': total_capacity,
            'average_distance': avg_distance,
            'status': 'otimo' if efficiency > 0.8 else ('bom' if efficiency > 0.6 else 'critico')
        }
    
    def growth_prediction(self, years: int = 10) -> Dict:
        """
        Infrastructure growth prediction.
        """
        current_modules = self.graph.get_module_count()

        # Fixed baseline: average consumption per module TODAY. As total consumption
        # grows over time, the number of modules the base must support is the
        # projected consumption divided by this fixed per-module baseline. Using a
        # fixed baseline (not one recalculated each year) avoids the circular
        # identity modules_needed == current_modules.
        base_per_module = (
            sum(m.consumption for m in self.graph.module_list) / current_modules
            if current_modules > 0 else 0
        )

        # Consumption sampled at each integer year (0..years), so index t == year t.
        projected_consumption = [self.total_consumption(float(t)) for t in range(years + 1)]
        needed = []
        for consumption in projected_consumption:
            if base_per_module > 0:
                needed.append(max(current_modules, math.ceil(consumption / base_per_module)))
            else:
                needed.append(current_modules)

        return {
            'current_year': 2026,
            'years': list(range(years + 1)),
            'current_modules': current_modules,
            'modules_needed': needed,
            'projected_consumption': projected_consumption,
            'expansion_needed': max(0, max(needed) - current_modules)
        }
    
    def cost_benefit_analysis(self) -> Dict:
        """
        Analyzes the cost-benefit of modules based on consumption and priority.
        """
        results = {}
        
        for module in self.graph.module_list:
            # Priority/consumption ratio (higher is better)
            ratio = module.priority / module.consumption if module.consumption > 0 else 0
            
            # Module efficiency
            efficiency = self.distribution_efficiency(module.id)
            
            results[module.id] = {
                'name': module.name,
                'priority_per_consumption': ratio,
                'distribution_efficiency': efficiency['efficiency'],
                'distribution_status': efficiency['status'],
                'operational_cost': module.consumption / 10,
                'strategic_value': module.priority * 2
            }
        
        return results