"""
User Interface for SIGIC.
Interactive terminal menu for system navigation.
"""

import os
import sys
from typing import Optional
from modules.grafo import InfrastructureGraph
from modules.module import Module
from algorithms.analysis import SearchAlgorithms, NetworkAnalysis
from algorithms.dijkstra import Dijkstra
from modeling.math import MathematicalModeling
from visualization.network_viz import NetworkVisualization

class MenuSIGIC:
    """
    User interface class.
    Manages navigation and information display.
    """
    
    def __init__(self, graph: InfrastructureGraph):
        """
        Initializes the menu with the infrastructure graph.
        """
        self.graph = graph
        self.search = SearchAlgorithms(graph)
        self.analysis = NetworkAnalysis(graph)
        self.dijkstra = Dijkstra(graph)
        self.modeling = MathematicalModeling(graph)
        self.visualization = NetworkVisualization(graph)
        
        # System state
        self.selected_module: Optional[str] = None
        
    def run(self):
        """
        Executes the main menu system.
        """
        while True:
            self._clear_screen()
            self._display_header()
            self._display_main_menu()
            
            try:
                option = input("\nEscolha uma opcao: ").strip()
                
                if option == '0':
                    self._exit_system()
                    break
                elif option == '1':
                    self._menu_view_network()
                elif option == '2':
                    self._menu_query_module()
                elif option == '3':
                    self._menu_algorithms()
                elif option == '4':
                    self._menu_modeling()
                elif option == '5':
                    self._menu_sustainability()
                elif option == '6':
                    self._menu_simulations()
                elif option == '7':
                    self._menu_complete_analysis()
                elif option == '8':
                    self._display_about()
                else:
                    self._display_error("Opcao invalida! Tente novamente.")
                    
            except KeyboardInterrupt:
                print("\n\nSaindo do sistema...")
                break
            except Exception as e:
                self._display_error(f"Erro inesperado: {e}")
                input("\nPressione ENTER para continuar...")
    
    def _clear_screen(self):
        """Clears the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _display_header(self):
        """Displays the system header."""
        print("=" * 70)
        print("SIGIC - SISTEMA INTELIGENTE DE GERENCIAMENTO")
        print("INFRAESTRUTURA DA COLONIA AURORA SIGER")
        print("=" * 70)
        print(f"Status: {self.graph.get_module_count()} modulos ativos")
        print(f"Conexoes: {self.graph.get_connection_count()}")
        print("-" * 70)
    
    def _display_main_menu(self):
        """Displays the main menu."""
        print("\nMENU PRINCIPAL")
        print("=" * 70)
        print(" 1. Visualizar Rede da Colonia")
        print(" 2. Consultar Modulo")
        print(" 3. Algoritmos de Rede")
        print(" 4. Modelagem Matematica")
        print(" 5. Sustentabilidade e Governanca")
        print(" 6. Simulacoes Operacionais")
        print(" 7. Analise Completa")
        print(" 8. Sobre o Sistema")
        print(" 0. Sair")
        print("=" * 70)
    
    # ==================== MENU 1: VIEW NETWORK ====================
    
    def _menu_view_network(self):
        """Menu to visualize the network."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("VISUALIZACAO DA REDE")
        print("=" * 70)
        
        print("\nESTRUTURA DA REDE:")
        print("-" * 70)
        
        # Displays modules with status icons
        print("\nMODULOS:")
        for module in self.graph.module_list:
            status_icon = self._get_status_icon(module.status)
            priority_bar = "█" * (module.priority // 2) + "░" * (5 - module.priority // 2)
            print(f"  {status_icon} {module.name} (ID: {module.id})")
            print(f"     Consumo: {module.consumption} kWh  |  Prioridade: [{priority_bar}] {module.priority}/10")
            print(f"     Capacidade: {module.capacity} kWh  |  Comunicacao: {module.communication}/10")
        
        # Displays connections
        print("\nCONEXOES:")
        seen_connections = set()
        for id1, neighbors in self.graph.adjacency_list.items():
            for id2 in neighbors:
                key = tuple(sorted([id1, id2]))
                if key not in seen_connections:
                    seen_connections.add(key)
                    weight = self.graph.get_weight(id1, id2)
                    conn_type = self.graph.connection_types.get(self.graph._get_edge_key(id1, id2), 'energy')
                    type_icon = self._get_type_icon(conn_type)
                    print(f"  {type_icon} {self.graph.modules[id1].name} <-> {self.graph.modules[id2].name}")
                    print(f"     Distancia: {weight:.1f} unidades  |  Tipo: {conn_type}")

        # Estatisticas gerais da rede (modulo de visualizacao)
        print("\n" + "-" * 70)
        print(self.visualization.generate_statistics())

        print("\n" + "=" * 70)
        input("\nPressione ENTER para voltar ao menu...")
    
    def _get_status_icon(self, status: str) -> str:
        """Returns icon for module status."""
        icons = {
            'active': '[A]',
            'maintenance': '[M]',
            'alert': '[!]',
            'inactive': '[X]'
        }
        return icons.get(status, '[?]')
    
    def _get_type_icon(self, conn_type: str) -> str:
        """Returns icon for connection type."""
        icons = {
            'energy': '[E]',
            'data': '[D]',
            'communication': '[C]',
            'life': '[L]',
            'water': '[W]',
            'air': '[A]'
        }
        return icons.get(conn_type, '[-]')
    
    # ==================== MENU 2: QUERY MODULE ====================
    
    def _menu_query_module(self):
        """Menu to query a specific module."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("CONSULTA DE MODULO")
        print("=" * 70)
        
        # Displays numbered module list
        print("\nModulos disponiveis:")
        print("-" * 40)
        for i, module in enumerate(self.graph.module_list, 1):
            status_icon = self._get_status_icon(module.status)
            print(f"  {i:2d}. {status_icon} {module.name} (Prioridade: {module.priority})")
        
        try:
            print("\n" + "-" * 40)
            option = input("Selecione o numero do modulo (0 para voltar): ").strip()
            
            if option == '0':
                return
            
            idx = int(option) - 1
            if 0 <= idx < len(self.graph.module_list):
                module = self.graph.module_list[idx]
                self._display_module_details(module.id)
            else:
                self._display_error("Opcao invalida!")
                
        except ValueError:
            self._display_error("Entrada invalida! Digite um numero.")
        except Exception as e:
            self._display_error(f"Erro: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def _display_module_details(self, module_id: str):
        """Displays complete module details."""
        module = self.graph.get_module(module_id)
        if not module:
            self._display_error("Modulo nao encontrado!")
            return
        
        self._clear_screen()
        print("\n" + "=" * 70)
        print(f"DETALHES DO MODULO: {module.name}")
        print("=" * 70)
        
        # Basic information
        print(f"\nINFORMACOES GERAIS:")
        print("-" * 40)
        print(f"  ID: {module.id}")
        print(f"  Status: {module.status.upper()} {self._get_status_icon(module.status)}")
        
        # Performance indicators
        print(f"\nINDICADORES OPERACIONAIS:")
        print("-" * 40)
        print(f"  Consumo energetico: {module.consumption} kWh")
        print(f"  Capacidade: {module.capacity} kWh")
        print(f"  Comunicacao: {module.communication}/10")
        print(f"  Prioridade: {module.priority}/10")
        
        # Priority bar
        priority_bar = "█" * module.priority + "░" * (10 - module.priority)
        print(f"     [{priority_bar}]")
        
        # Connections
        print(f"\nCONEXOES:")
        print("-" * 40)
        neighbors = self.graph.get_neighbors(module_id)
        if neighbors:
            for neighbor_id in neighbors:
                neighbor = self.graph.get_module(neighbor_id)
                weight = self.graph.get_weight(module_id, neighbor_id)
                edge_key = self.graph._get_edge_key(module_id, neighbor_id)
                conn_type = self.graph.connection_types.get(edge_key, 'energy')
                type_icon = self._get_type_icon(conn_type)
                print(f"  {type_icon} {neighbor.name} (Distancia: {weight:.1f}, Tipo: {conn_type})")
        else:
            print("  Nenhuma conexao encontrada.")
        
        # Efficiency analysis
        print(f"\nANALISE DE EFICIENCIA:")
        print("-" * 40)
        efficiency = self.modeling.distribution_efficiency(module_id)
        print(f"  Eficiencia de distribuicao: {efficiency['efficiency']*100:.1f}%")
        print(f"  Capacidade total disponivel: {efficiency['total_capacity']:.2f} kWh")
        print(f"  Distancia media: {efficiency['average_distance']:.2f}")
        print(f"  Status: {efficiency['status'].upper()}")
        
        # Recommendations
        print(f"\nRECOMENDACOES:")
        print("-" * 40)
        if efficiency['efficiency'] < 0.6:
            print("  Eficiencia baixa. Considere:")
            print("     * Aumentar a capacidade de armazenamento")
            print("     * Otimizar rotas de distribuicao")
            print("     * Verificar conexoes criticas")
        elif efficiency['efficiency'] < 0.8:
            print("  Eficiencia media. Sugestoes:")
            print("     * Monitorar consumo regularmente")
            print("     * Planejar expansao gradual")
        else:
            print("  Modulo operando com alta eficiencia!")
            print("     * Manter praticas atuais")
            print("     * Servir como referencia para outros modulos")
        
        print("\n" + "=" * 70)
    
    # ==================== MENU 3: ALGORITHMS ====================
    
    def _menu_algorithms(self):
        """Menu for network algorithms execution."""
        while True:
            self._clear_screen()
            print("\n" + "=" * 70)
            print("ALGORITMOS DE REDE")
            print("=" * 70)
            print("\n 1. BFS - Busca em Largura")
            print(" 2. DFS - Busca em Profundidade")
            print(" 3. Dijkstra - Caminho Minimo")
            print(" 4. Dijkstra - Caminho com Restricoes de Prioridade")
            print(" 5. Dijkstra - Caminhos Minimos para Todos os Destinos")
            print(" 6. Analise de Eficiencia da Rede")
            print(" 7. Detectar Pontos Criticos")
            print(" 8. Analise de Centralidade")
            print(" 9. Componentes Conexos")
            print(" 0. Voltar")
            print("=" * 70)
            
            try:
                option = input("\nEscolha uma opcao: ").strip()
                
                if option == '0':
                    break
                elif option == '1':
                    self._execute_bfs()
                elif option == '2':
                    self._execute_dfs()
                elif option == '3':
                    self._execute_dijkstra()
                elif option == '4':
                    self._execute_dijkstra_constraints()
                elif option == '5':
                    self._execute_dijkstra_all()
                elif option == '6':
                    self._analyze_efficiency()
                elif option == '7':
                    self._detect_critical_points()
                elif option == '8':
                    self._analyze_centrality()
                elif option == '9':
                    self._list_components()
                else:
                    self._display_error("Opcao invalida!")
                    
            except ValueError:
                self._display_error("Entrada invalida!")
            except KeyboardInterrupt:
                break
    
    def _select_module(self, message: str = "Selecione o modulo") -> Optional[str]:
        """Helper to select a module."""
        print("\nModulos disponiveis:")
        for i, module in enumerate(self.graph.module_list, 1):
            print(f"  {i:2d}. {module.name}")
        
        try:
            option = int(input(f"\n{message} (numero): ")) - 1
            if 0 <= option < len(self.graph.module_list):
                return self.graph.module_list[option].id
            else:
                self._display_error("Opcao invalida!")
                return None
        except ValueError:
            self._display_error("Entrada invalida!")
            return None
    
    def _execute_bfs(self):
        """Executes BFS on the network."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("BFS - BUSCA EM LARGURA")
        print("=" * 70)
        
        start = self._select_module("Modulo de inicio")
        if not start:
            return
        
        search_target = input("\nBuscar um alvo especifico? (s/n): ").strip().lower()
        target = None
        if search_target == 's':
            target = self._select_module("Modulo alvo")
        
        self.search.bfs(start, target)
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _execute_dfs(self):
        """Executes DFS on the network."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("DFS - BUSCA EM PROFUNDIDADE")
        print("=" * 70)
        
        start = self._select_module("Modulo de inicio")
        if not start:
            return
        
        search_target = input("\nBuscar um alvo especifico? (s/n): ").strip().lower()
        target = None
        if search_target == 's':
            target = self._select_module("Modulo alvo")
        
        path = self.search.dfs(start, target)
        if path:
            print(f"\nCaminho encontrado:")
            print(f"   {' -> '.join([self.graph.modules[m].name for m in path])}")
        else:
            print("\nNenhum caminho encontrado.")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _execute_dijkstra(self):
        """Executes Dijkstra for shortest path."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("DIJKSTRA - CAMINHO MINIMO")
        print("=" * 70)
        
        origin = self._select_module("Modulo de origem")
        if not origin:
            return
        
        destination = self._select_module("Modulo de destino")
        if not destination:
            return
        
        path, distance = self.dijkstra.find_path(origin, destination)
        
        if path:
            print(f"\nRota mais eficiente:")
            print(f"   {' -> '.join([self.graph.modules[m].name for m in path])}")
            print(f"   Distancia total: {distance:.2f}")
        else:
            print("\nNao foi possivel encontrar um caminho.")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _execute_dijkstra_constraints(self):
        """Executes Dijkstra with priority constraints."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("DIJKSTRA - CAMINHO COM RESTRICOES")
        print("=" * 70)
        
        origin = self._select_module("Modulo de origem")
        if not origin:
            return
        
        destination = self._select_module("Modulo de destino")
        if not destination:
            return
        
        try:
            min_priority = int(input("\nPrioridade minima requerida (0-10): "))
            if min_priority < 0 or min_priority > 10:
                self._display_error("Prioridade deve estar entre 0 e 10!")
                return
            
            path, distance = self.dijkstra.find_path_with_constraints(origin, destination, min_priority)
            
            if path:
                print(f"\nRota encontrada com restricoes:")
                print(f"   {' -> '.join([self.graph.modules[m].name for m in path])}")
                print(f"   Distancia total: {distance:.2f}")
            else:
                print("\nNao foi possivel encontrar um caminho com as restricoes.")
                
        except ValueError:
            self._display_error("Entrada invalida!")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _execute_dijkstra_all(self):
        """Executes Dijkstra from one origin to all reachable destinations."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("DIJKSTRA - CAMINHOS MINIMOS PARA TODOS OS DESTINOS")
        print("=" * 70)

        origin = self._select_module("Modulo de origem")
        if not origin:
            return

        results = self.dijkstra.find_all_paths(origin)

        print(f"\nOrigem: {self.graph.modules[origin].name}")
        print("-" * 70)

        if not results:
            print("\nNenhum destino alcancavel a partir deste modulo.")
        else:
            # Sorted by distance (closest first) for a readable summary table.
            ordered = sorted(results.items(), key=lambda item: item[1][1])
            print(f"\n{'Destino':22} | {'Dist.':>5} | Rota")
            print("-" * 70)
            for destination, (path, distance) in ordered:
                route = ' -> '.join(self.graph.modules[m].name for m in path)
                print(f"{self.graph.modules[destination].name:22} | {distance:5.1f} | {route}")

        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")

    def _analyze_efficiency(self):
        """Analyzes network efficiency."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("ANALISE DE EFICIENCIA OPERACIONAL")
        print("=" * 70)
        
        efficiency = self.analysis.analyze_efficiency()
        
        print(f"\nMETRICAS GERAIS:")
        print("-" * 40)
        print(f"  Total de modulos: {efficiency['total_modules']}")
        print(f"  Total de conexoes: {efficiency['total_connections']}")
        print(f"  Grau medio: {efficiency['average_degree']:.2f}")
        print(f"  Coeficiente de cluster: {efficiency['clustering_coefficient']:.3f}")
        
        print(f"\nEFICIENCIA:")
        print("-" * 40)
        print(f"  Comunicacao: {efficiency['communication_efficiency']*100:.1f}%")
        print(f"  Energetica: {efficiency['energy_efficiency']*100:.1f}%")
        print(f"  Status geral: {efficiency['overall_status'].upper()}")
        
        print(f"\nPESOS DAS ARESTAS:")
        print("-" * 40)
        print(f"  Media: {efficiency['avg_edge_weight']:.2f}")
        print(f"  Maximo: {efficiency['max_edge_weight']}")
        print(f"  Minimo: {efficiency['min_edge_weight']}")
        
        if efficiency['critical_modules']:
            print(f"\nMODULOS CRITICOS:")
            print("-" * 40)
            for mod in efficiency['critical_modules']:
                print(f"  * {mod}")
        
        if efficiency['articulation_points']:
            print(f"\nPONTOS DE ARTICULACAO (vertices criticos):")
            print("-" * 40)
            for ponto in efficiency['articulation_points']:
                print(f"  * {ponto}")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _detect_critical_points(self):
        """Detects critical points in the network."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("DETECCAO DE PONTOS CRITICOS")
        print("=" * 70)
        
        points = self.analysis.detect_critical_points()
        
        if points:
            print(f"\nPontos criticos encontrados ({len(points)}):")
            print("-" * 40)
            for p in points:
                module = self.graph.get_module(p)
                if module:
                    print(f"  * {module.name} (ID: {p})")
                    print(f"    Prioridade: {module.priority}")
                    print(f"    Conexoes: {len(self.graph.get_neighbors(p))}")
                    print(f"    Status: {module.status}")
                    print()
        else:
            print("\nNenhum ponto critico detectado!")
            print("   A rede esta robusta e interconectada.")
        
        print("\nIMPLICACOES:")
        print("-" * 40)
        if points:
            print("  A remocao de qualquer um desses modulos pode desconectar a rede.")
            print("  Recomendacoes:")
            print("  * Criar conexoes redundantes para estes pontos")
            print("  * Manter monitoramento constante")
            print("  * Ter planos de contingencia")
        else:
            print("  A rede e resiliente a falhas individuais.")
            print("  Estrutura bem projetada para suportar contingencias.")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _analyze_centrality(self):
        """Analyzes module centrality."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("ANALISE DE CENTRALIDADE")
        print("=" * 70)
        
        centrality = self.analysis.analyze_centrality()
        
        print("\nCENTRALIDADE DOS MODULOS:")
        print("-" * 40)
        
        sorted_modules = sorted(
            centrality.items(),
            key=lambda x: x[1]['degree'],
            reverse=True
        )
        
        for mod_id, data in sorted_modules:
            bar = "█" * min(data['degree'], 10) + "░" * (10 - min(data['degree'], 10))
            print(f"  {data['name']:20} | Grau: {data['degree']:2d} {bar}")
            print(f"                      | Intermediacao: {data['betweenness']:.3f}")
            print(f"                      | Prioridade: {data['priority']}/10")
            print()
        
        print("INTERPRETACAO:")
        print("-" * 40)
        print("  * Grau: Numero de conexoes diretas")
        print("  * Intermediacao: Importancia como ponte entre modulos")
        print("  * Modulos com alto grau sao hubs da rede")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _list_components(self):
        """Lists connected components."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("COMPONENTES CONEXOS")
        print("=" * 70)
        
        components = self.search.bfs_components()
        
        print(f"\nTotal de componentes: {len(components)}")
        print("-" * 40)
        
        for i, component in enumerate(components, 1):
            print(f"\nComponente {i}:")
            for mod_id in component:
                module = self.graph.get_module(mod_id)
                if module:
                    print(f"  * {module.name}")
        
        if len(components) > 1:
            print("\nATENCAO:")
            print("  A rede possui mais de um componente conexo.")
            print("  Isso significa que ha modulos isolados.")
            print("  Recomendacao: Criar conexoes adicionais.")
        else:
            print("\nA rede e totalmente conexa.")
            print("  Todos os modulos estao interligados.")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    # ==================== MENU 4: MATHEMATICAL MODELING ====================
    
    def _menu_modeling(self):
        """Menu for mathematical modeling."""
        while True:
            self._clear_screen()
            print("\n" + "=" * 70)
            print("MODELAGEM MATEMATICA")
            print("=" * 70)
            print("\n 1. Projecao de Consumo Energetico")
            print(" 2. Perda Energetica por Distancia")
            print(" 3. Previsao de Crescimento")
            print(" 4. Analise de Custo-Beneficio")
            print(" 5. Analise Temporal (Derivadas)")
            print(" 6. Otimizacao de Distribuicao")
            print(" 7. Simulacao de Cenarios")
            print(" 8. Analise Completa com Calculo")
            print(" 0. Voltar")
            print("=" * 70)
            
            try:
                option = input("\nEscolha uma opcao: ").strip()
                
                if option == '0':
                    break
                elif option == '1':
                    self._project_consumption()
                elif option == '2':
                    self._analyze_energy_loss()
                elif option == '3':
                    self._predict_growth()
                elif option == '4':
                    self._analyze_cost_benefit()
                elif option == '5':
                    self._temporal_analysis()
                elif option == '6':
                    self._optimize_distribution()
                elif option == '7':
                    self._simulate_scenarios()
                elif option == '8':
                    self._complete_calculus_analysis()
                else:
                    self._display_error("Opcao invalida!")
                    
            except ValueError:
                self._display_error("Entrada invalida!")
    
    def _project_consumption(self):
        """Projects energy consumption growth."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("PROJECAO DE CONSUMO ENERGETICO")
        print("=" * 70)
        
        try:
            years = int(input("\nNumero de anos para projecao: "))
            if years <= 0:
                self._display_error("Deve ser um numero positivo!")
                return
            
            # Uses temporal analysis for projection
            analysis = self.modeling.temporal_consumption_analysis(years=years, points=years * 10)
            
            initial_consumption = sum(module.consumption for module in self.graph.module_list)
            print(f"\nConsumo inicial: {initial_consumption:.2f} kWh")
            print(f"Projecao para {years} anos:")
            print("-" * 50)
            
            print("\nAno | Consumo Total | Media por Modulo | Crescimento")
            print("-" * 50)
            for t in range(years):
                if t % 2 == 0 or t == years - 1:
                    idx = t * 10
                    if idx < len(analysis['data']['consumption']):
                        consumption = analysis['data']['consumption'][idx]
                        avg_consumption = consumption / self.graph.get_module_count()
                        growth = analysis['data']['growth_rate'][idx] if idx < len(analysis['data']['growth_rate']) else 0
                        print(f"{t:3d}  | {consumption:12.2f} | {avg_consumption:16.2f} | {growth:6.1f}%")
            
            total_growth = analysis['total_growth']
            print(f"\nANALISE:")
            print("-" * 40)
            print(f"  Crescimento total: {total_growth:.1f}%")
            
            if total_growth > 100:
                print("  Crescimento exponencial - infraestrutura precisa de expansao")
                print("  Recomendacao: Investir em fontes alternativas de energia")
            elif total_growth > 50:
                print("  Crescimento significativo - planejar expansao gradual")
                print("  Recomendacao: Otimizar eficiencia dos modulos existentes")
            else:
                print("  Crescimento controlado - infraestrutura suficiente")
                print("  Recomendacao: Manter praticas atuais e monitorar")
            
        except ValueError:
            self._display_error("Entrada invalida!")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _analyze_energy_loss(self):
        """Analyzes energy loss by distance."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("PERDA ENERGETICA POR DISTANCIA")
        print("=" * 70)
        
        print("\nANALISE DE PERDAS:")
        print("-" * 40)
        
        # edge_weights mapeia chave "id1-id2" (string) -> peso.
        # Como so precisamos dos pesos (distancias), iteramos os valores.
        distances = set(self.graph.edge_weights.values())
        
        print("\nDistancia | Perda | Eficiencia")
        print("-" * 40)
        for d in sorted(distances):
            loss = self.modeling.energy_loss_by_distance(float(d))
            efficiency = 1 - loss
            bar = "█" * int(efficiency * 10) + "░" * (10 - int(efficiency * 10))
            print(f"  {d:5.1f}    | {loss*100:5.1f}%  | {bar} {efficiency*100:.1f}%")
        
        print("\nANALISE:")
        print("-" * 40)
        print("  * A perda segue uma curva exponencial")
        print("  * Distancias menores reduzem significativamente as perdas")
        print("  * Conexoes com perda > 30% sao consideradas ineficientes")
        
        high_loss = [d for d in sorted(distances) if self.modeling.energy_loss_by_distance(float(d)) > 0.3]
        if high_loss:
            print("\nConexoes com perda > 30%:")
            for d in high_loss:
                print(f"  * Distancia {d:.1f} - Considere otimizar")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _predict_growth(self):
        """Predicts infrastructure growth."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("PREVISAO DE CRESCIMENTO DA INFRAESTRUTURA")
        print("=" * 70)
        
        try:
            years = int(input("\nNumero de anos para previsao: "))
            if years <= 0:
                self._display_error("Deve ser um numero positivo!")
                return
            
            prediction = self.modeling.growth_prediction(years)
            
            print(f"\nPREVISAO PARA {years} ANOS:")
            print("-" * 50)
            print(f"  Modulos atuais: {prediction['current_modules']}")
            print(f"  Ano base: {prediction['current_year']}")
            print(f"  Modulos necessarios em {years} anos: {prediction['modules_needed'][-1]}")
            print(f"  Expansao necessaria: {prediction['expansion_needed']} modulos")
            
            print("\nProjecao detalhada:")
            print("Ano | Modulos | Consumo Total")
            print("-" * 40)
            for t in range(years):
                if t % 2 == 0 or t == years - 1:
                    print(f"{prediction['current_year'] + t:4d} | {prediction['modules_needed'][t]:8d} | {prediction['projected_consumption'][t]:12.2f} kWh")
            
        except ValueError:
            self._display_error("Entrada invalida!")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _analyze_cost_benefit(self):
        """Analyzes cost-benefit of modules."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("ANALISE DE CUSTO-BENEFICIO")
        print("=" * 70)
        
        results = self.modeling.cost_benefit_analysis()
        
        print("\nMODULOS ORDENADOS POR EFICIENCIA:")
        print("-" * 40)
        
        sorted_modules = sorted(
            results.items(),
            key=lambda x: x[1]['priority_per_consumption'],
            reverse=True
        )
        
        for mod_id, data in sorted_modules:
            print(f"  {data['name']:20}")
            print(f"    Prioridade/Consumo: {data['priority_per_consumption']:.3f}")
            print(f"    Eficiencia: {data['distribution_efficiency']*100:.1f}%")
            print(f"    Status: {data['distribution_status'].upper()}")
            print(f"    Custo: {data['operational_cost']:.2f}")
            print(f"    Valor estrategico: {data['strategic_value']:.2f}")
            print()
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _temporal_analysis(self):
        """Performs temporal analysis with derivatives."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("ANALISE TEMPORAL (DERIVADAS)")
        print("=" * 70)
        
        try:
            years = int(input("\nNumero de anos para analise: "))
            if years <= 0:
                self._display_error("Deve ser um numero positivo!")
                return
            
            analysis = self.modeling.temporal_consumption_analysis(years=years, points=50)
            
            print(f"\nANALISE PARA {years} ANOS:")
            print("-" * 40)
            print(f"Consumo inicial: {analysis['initial_consumption']:.2f} kWh")
            print(f"Consumo final: {analysis['final_consumption']:.2f} kWh")
            print(f"Crescimento total: {analysis['total_growth']:.1f}%")
            print(f"Taxa media de crescimento: {analysis['avg_growth_rate']:.2f}%")
            
            if analysis['inflection_points']:
                print(f"Pontos de inflexao detectados: {analysis['inflection_points']}")
            
            print(analysis['qualitative_analysis'])
            
        except ValueError:
            self._display_error("Entrada invalida!")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _optimize_distribution(self):
        """Optimizes energy distribution."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("OTIMIZACAO DE DISTRIBUICAO DE ENERGIA")
        print("=" * 70)
        
        results = self.modeling.optimize_energy_distribution()
        
        print("\nOTIMIZACAO POR MODULO:")
        print("-" * 40)
        
        for mod_id, data in results.items():
            print(f"\n  {data['name']}:")
            print(f"    Consumo atual: {data['current_consumption']:.2f} kWh")
            print(f"    Consumo otimo: {data['optimal_consumption']:.2f} kWh")
            print(f"    Eficiencia atual: {data['current_efficiency']*100:.1f}%")
            print(f"    Eficiencia otima: {data['optimal_efficiency']*100:.1f}%")
            if data['improvement'] > 0:
                print(f"    Melhoria potencial: +{data['improvement']:.1f}%")
            else:
                print(f"    Ja otimizado")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _simulate_scenarios(self):
        """Simulates different scenarios."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("SIMULACAO DE CENARIOS")
        print("=" * 70)
        
        scenarios = self.modeling.simulate_scenarios()
        
        print("\nCENARIOS DE CRESCIMENTO (10 ANOS):")
        print("-" * 40)
        
        for name, data in scenarios.items():
            print(f"\n  {name.upper()}:")
            print(f"    Taxa anual: {data['avg_annual_rate']:.1f}%")
            print(f"    Consumo final: {data['final_consumption']:.2f} kWh")
            print(f"    Crescimento: {data['growth_percentage']:.1f}%")
            print(f"    {data['analysis']}")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    def _complete_calculus_analysis(self):
        """Performs complete calculus analysis."""
        self.modeling.complete_analysis()
        input("\nPressione ENTER para continuar...")
    
    # ==================== MENU 5: SUSTAINABILITY ====================
    
    def _menu_sustainability(self):
        """Menu for sustainability and governance."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("SUSTENTABILIDADE E GOVERNANCA")
        print("=" * 70)
        
        print("\nANALISE DE SUSTENTABILIDADE:")
        print("-" * 40)
        
        # Calculates sustainability metrics
        total_consumption = sum(m.consumption for m in self.graph.module_list)
        total_capacity = sum(m.capacity for m in self.graph.module_list)
        critical_modules = len([m for m in self.graph.module_list if m.priority >= 8])
        
        print(f"  Consumo total: {total_consumption} kWh")
        print(f"  Capacidade total: {total_capacity} kWh")
        print(f"  Margem de seguranca: {(total_capacity - total_consumption) / total_capacity * 100:.1f}%")
        print(f"  Modulos criticos: {critical_modules}")
        
        print("\nRECOMENDACOES ESG:")
        print("-" * 40)
        print("  * Ambiental:")
        print("    - Otimizar consumo energetico")
        print("    - Implementar fontes renovaveis")
        print("    - Reduzir perdas nas conexoes")
        print("  * Social:")
        print("    - Garantir prioridade aos modulos de suporte a vida")
        print("    - Manter comunicacao constante com a tripulacao")
        print("  * Governanca:")
        print("    - Estabelecer protocolos de decisao")
        print("    - Monitorar metricas continuamente")
        print("    - Planejar expansao sustentavel")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    # ==================== MENU 6: SIMULATIONS ====================
    
    def _menu_simulations(self):
        """Menu for operational simulations."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("SIMULACOES OPERACIONAIS")
        print("=" * 70)
        
        print("\n 1. Simular Falha de Modulo")
        print(" 2. Simular Pico de Consumo")
        print(" 3. Simular Expansao")
        print(" 4. Simular Otimizacao")
        print(" 0. Voltar")
        print("=" * 70)
        
        try:
            option = input("\nEscolha uma opcao: ").strip()
            
            if option == '0':
                return
            elif option == '1':
                self._simulate_failure()
            elif option == '2':
                self._simulate_consumption_peak()
            elif option == '3':
                self._simulate_expansion()
            elif option == '4':
                self._simulate_optimization()
            else:
                self._display_error("Opcao invalida!")
                
        except ValueError:
            self._display_error("Entrada invalida!")
        
        input("\nPressione ENTER para continuar...")
    
    def _simulate_failure(self):
        """Simulates module failure."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("SIMULACAO DE FALHA DE MODULO")
        print("=" * 70)
        
        module = self._select_module("Modulo para simular falha")
        if not module:
            return
        
        print(f"\nSimulando falha no modulo: {self.graph.modules[module].name}")
        print("-" * 40)
        
        # Checks impact on the network
        neighbors = self.graph.get_neighbors(module)
        print(f"  Conexoes afetadas: {len(neighbors)}")
        
        # Checks if it's a critical point
        critical = self.analysis.detect_critical_points()
        if module in critical:
            print("  IMPACTO: Ponto critico - rede pode ser desconectada!")
            print("  Recomendacao: Implementar redundancia imediatamente")
        else:
            print("  IMPACTO: A rede continua operacional")
            print("  Recomendacao: Monitorar e planejar substituto")
        
        # Recommends alternative paths
        if len(neighbors) > 1:
            print("\n  Rotas alternativas disponiveis:")
            for i, neighbor in enumerate(neighbors[:3], 1):
                n_mod = self.graph.get_module(neighbor)
                print(f"    {i}. Via {n_mod.name}")
    
    def _simulate_consumption_peak(self):
        """Simulates consumption peak."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("SIMULACAO DE PICO DE CONSUMO")
        print("=" * 70)
        
        try:
            peak = int(input("\nPercentual de aumento no consumo (%): "))
            if peak <= 0:
                self._display_error("Deve ser um numero positivo!")
                return
            
            print(f"\nSimulando pico de {peak}% no consumo:")
            print("-" * 40)
            
            total_current = sum(m.consumption for m in self.graph.module_list)
            total_capacity = sum(m.capacity for m in self.graph.module_list)
            total_peak = total_current * (1 + peak / 100)
            
            print(f"  Consumo atual: {total_current:.2f} kWh")
            print(f"  Consumo no pico: {total_peak:.2f} kWh")
            print(f"  Capacidade total: {total_capacity:.2f} kWh")
            print(f"  Margem: {total_capacity - total_peak:.2f} kWh")
            
            if total_peak > total_capacity:
                print("  ALERTA: Demanda excede capacidade!")
                print("  Recomendacao: Reduzir consumo em modulos nao criticos")
            else:
                print("  OK: Capacidade suficiente para o pico")
                print("  Recomendacao: Monitorar e planejar expansao futura")
            
            # Identifies modules that would exceed capacity
            print("\n  Modulos que excederiam sua capacidade:")
            for m in self.graph.module_list:
                consumption_peak = m.consumption * (1 + peak / 100)
                if consumption_peak > m.capacity:
                    print(f"    * {m.name}: {consumption_peak:.2f} kWh > {m.capacity:.2f} kWh")
                    
        except ValueError:
            self._display_error("Entrada invalida!")
    
    def _simulate_expansion(self):
        """Simulates infrastructure expansion."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("SIMULACAO DE EXPANSAO")
        print("=" * 70)
        
        try:
            years = int(input("\nNumero de anos para expansao: "))
            if years <= 0:
                self._display_error("Deve ser um numero positivo!")
                return
            
            prediction = self.modeling.growth_prediction(years)
            
            print(f"\nSIMULACAO DE EXPANSAO PARA {years} ANOS:")
            print("-" * 40)
            print(f"  Modulos atuais: {prediction['current_modules']}")
            print(f"  Modulos necessarios: {prediction['modules_needed'][-1]}")
            print(f"  Expansao necessaria: {prediction['expansion_needed']} modulos")
            
            print("\n  Cronograma sugerido:")
            for t in range(0, years + 1, 2):
                modules = prediction['modules_needed'][t] if t < len(prediction['modules_needed']) else prediction['modules_needed'][-1]
                print(f"    Ano {prediction['current_year'] + t}: {modules} modulos")
            
        except ValueError:
            self._display_error("Entrada invalida!")
    
    def _simulate_optimization(self):
        """Simulates optimization."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("SIMULACAO DE OTIMIZACAO")
        print("=" * 70)
        
        print("\nOtimizando distribuicao de energia:")
        print("-" * 40)
        
        results = self.modeling.optimize_energy_distribution()
        
        total_savings = 0
        for data in results.values():
            if data['improvement'] > 0:
                total_savings += data['current_consumption'] * (data['improvement'] / 100)
        
        print(f"  Economia total potencial: {total_savings:.2f} kWh")
        
        print("\n  Modulos com maior potencial de melhoria:")
        sorted_modules = sorted(
            results.items(),
            key=lambda x: x[1]['improvement'],
            reverse=True
        )[:3]
        
        for mod_id, data in sorted_modules:
            if data['improvement'] > 0:
                print(f"    * {data['name']}: {data['improvement']:.1f}%")
    
    # ==================== MENU 7: COMPLETE ANALYSIS ====================
    
    def _menu_complete_analysis(self):
        """Performs complete system analysis."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("ANALISE COMPLETA DO SISTEMA")
        print("=" * 70)
        
        # 1. Network analysis
        efficiency = self.analysis.analyze_efficiency()
        
        print("\n1. ANALISE DA REDE:")
        print("-" * 40)
        print(f"  Modulos: {efficiency['total_modules']}")
        print(f"  Conexoes: {efficiency['total_connections']}")
        print(f"  Eficiencia global: {efficiency['overall_status'].upper()}")
        
        # 2. Critical points
        critical = self.analysis.detect_critical_points()
        print(f"\n2. PONTOS CRITICOS:")
        print("-" * 40)
        if critical:
            print(f"  Encontrados: {len(critical)}")
            for c in critical[:5]:
                print(f"    * {self.graph.modules[c].name}")
        else:
            print("  Nenhum ponto critico detectado")
        
        # 3. Consumption analysis
        total_consumption = sum(m.consumption for m in self.graph.module_list)
        total_capacity = sum(m.capacity for m in self.graph.module_list)
        print(f"\n3. CONSUMO E CAPACIDADE:")
        print("-" * 40)
        print(f"  Consumo total: {total_consumption:.2f} kWh")
        print(f"  Capacidade total: {total_capacity:.2f} kWh")
        print(f"  Utilizacao: {total_consumption/total_capacity*100:.1f}%")
        
        # 4. Recommendations
        print("\n4. RECOMENDACOES:")
        print("-" * 40)
        if efficiency['overall_status'] == 'critico':
            print("  * Implementar melhorias urgentes na rede")
        elif efficiency['overall_status'] == 'bom':
            print("  * Otimizar areas com baixa eficiencia")
        else:
            print("  * Manter monitoramento continuo")
        
        if critical:
            print("  * Criar redundancia para pontos criticos")
        
        if total_consumption / total_capacity > 0.8:
            print("  * Planejar expansao de capacidade")
        
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    # ==================== MENU 8: ABOUT ====================
    
    def _display_about(self):
        """Displays system information."""
        self._clear_screen()
        print("\n" + "=" * 70)
        print("SOBRE O SISTEMA")
        print("=" * 70)
        print("\nSIGIC - Sistema Inteligente de Gerenciamento")
        print("Infraestrutura da Colonia Aurora Siger")
        print("\nVersao: 1.0")
        print("Autor: Equipe SIGIC")
        print("\nDisciplinas Integradas:")
        print("  * Algoritmos e Estruturas de Dados")
        print("  * Grafos e Algoritmos de Redes")
        print("  * Modelagem Matematica")
        print("  * Calculo Diferencial")
        print("  * Sustentabilidade e Governanca ESG")
        print("\nFuncionalidades:")
        print("  * Visualizacao da rede")
        print("  * Consulta de modulos")
        print("  * Algoritmos de caminho minimo")
        print("  * Modelagem matematica")
        print("  * Simulacoes operacionais")
        print("  * Analise de eficiencia")
        print("\n" + "=" * 70)
        input("\nPressione ENTER para continuar...")
    
    # ==================== UTILITY FUNCTIONS ====================
    
    def _display_error(self, message: str):
        """Displays an error message."""
        print(f"\n[ERRO] {message}")
    
    def _exit_system(self):
        """Exits the system."""
        print("\nSaindo do SIGIC...")
        print("Obrigado por utilizar o sistema!")